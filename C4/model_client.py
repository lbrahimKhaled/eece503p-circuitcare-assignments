import os
import json
import threading
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env', override=False)
RATES = {'deepseek-flash': (0.30, 0.006, 1.20), 'deepseek-v4-pro': (1.32, 0.044, 3.96), 'gpt-6-luna': (0.10, 0.01, 0.50), 'gpt-4.1-mini': (0.40, 0.10, 1.60)}

def usage_cost_upper(usage, model):
    """Estimate standard-rate USD, including Luna cache writes at 1.25x input."""
    input_rate, cached_rate, output_rate = RATES[model]
    prompt = max(0, usage.get('prompt_tokens', 0))
    details = usage.get('prompt_tokens_details') or {}
    cached = min(prompt, max(0, usage.get('prompt_cache_hit_tokens', details.get('cached_tokens', 0)) or 0))
    written = min(prompt-cached, max(0, details.get('cache_write_tokens', 0) or 0)) if model == 'gpt-6-luna' else 0
    return ((prompt-cached-written)*input_rate + cached*cached_rate + written*input_rate*1.25 + max(0, usage.get('completion_tokens', 0))*output_rate)/1_000_000

def deepseek_cost_upper(usage, model):
    """Retain the DeepSeek-specific helper for historical experiment reproducibility."""
    return usage_cost_upper(usage, model)

class ModelClient:
    """Bound requests and spend for one shared client; credentials stay in memory."""
    def __init__(self, model=None):
        self.provider = os.getenv('MODEL_PROVIDER', 'openai').lower()
        if self.provider not in {'openai', 'deepseek'}:
            raise ValueError('MODEL_PROVIDER must be openai or deepseek')
        variable = 'DEEPSEEK_API_KEY' if self.provider == 'deepseek' else 'OPENAI_API_KEY'
        key = os.getenv(variable)
        if not key:
            raise ValueError(f'Set {variable} privately, or start with python run.py.')
        base = 'https://api.deepseek.com' if self.provider == 'deepseek' else 'https://api.openai.com/v1'
        self.client = OpenAI(api_key=key, base_url=os.getenv('TEST_API_BASE_URL', base), timeout=55, max_retries=0)
        self.model = model or (os.getenv('DEEPSEEK_MODEL', 'deepseek-flash') if self.provider == 'deepseek' else os.getenv('OPENAI_MODEL', 'gpt-6-luna'))
        allowed = {'deepseek-flash','deepseek-v4-pro'} if self.provider == 'deepseek' else {'gpt-6-luna','gpt-4.1-mini'}
        if self.model not in allowed:
            raise ValueError('Use a documented DeepSeek model.' if self.provider == 'deepseek' else 'Use a priced OpenAI model: gpt-6-luna or gpt-4.1-mini.')
        self.input_rate, _, self.output_rate = RATES[self.model]
        self.usage = []
        self.cost_upper = 0.0
        self.calls = 0
        self.max_cost = float(os.getenv('MAX_RUN_COST_USD', '0.05'))
        self.max_calls = int(os.getenv('MAX_RUN_CALLS', '64'))
        if self.max_cost <= 0 or self.max_calls < 1:
            raise ValueError('Budget and call limit must be positive.')
        self.lock = threading.Lock()

    def complete(self, messages, tools=None, **settings):
        with self.lock:
            return self._complete(messages, tools, **settings)

    def _complete(self, messages, tools=None, **settings):
        args = {'model':self.model, 'messages':messages, 'max_tokens':512, **settings}
        if tools:
            args['tools'] = tools
        if self.provider == 'deepseek':
            args['extra_body'] = {'thinking': {'type': 'disabled'}}
        if self.model == 'gpt-6-luna':
            args['max_completion_tokens'] = args.pop('max_tokens')
            args['reasoning_effort'] = 'none'
        output_limit = args.get('max_completion_tokens', args.get('max_tokens'))
        if not isinstance(output_limit, int) or output_limit < 1 or output_limit > 2048:
            raise ValueError('Output token limit must be between 1 and 2048.')
        if self.calls >= self.max_calls:
            raise RuntimeError('Per-client call limit reached.')
        input_ceiling = len(json.dumps(messages, ensure_ascii=False).encode()) + len(json.dumps(tools or []).encode()) + 512
        reserve = input_ceiling*self.input_rate*(1.25 if self.model=='gpt-6-luna' else 1)/1_000_000 + output_limit*self.output_rate/1_000_000
        if self.cost_upper + reserve > self.max_cost:
            raise RuntimeError('Per-client budget reached. Restart only if you intend to spend more.')
        self.calls += 1
        try:
            response = self.client.chat.completions.create(**args)
        except Exception:
            self.cost_upper += reserve
            raise
        if response.usage:
            usage = response.usage.model_dump()
            self.usage.append(usage)
            self.cost_upper += usage_cost_upper(usage, self.model)
        else:
            self.cost_upper += reserve
        if response.choices[0].finish_reason == 'length':
            raise RuntimeError('Model output hit its token limit. Increase max_tokens deliberately and retry.')
        return response.choices[0].message.model_dump(exclude_none=True, include={'role','content','tool_calls'})
