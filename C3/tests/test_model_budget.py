import sys
from pathlib import Path
from unittest.mock import Mock
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model_client import ModelClient


def test_pro_request_reserves_higher_output_cost_before_network(monkeypatch):
    monkeypatch.setenv('MODEL_PROVIDER','deepseek')
    monkeypatch.setenv('DEEPSEEK_API_KEY','offline-test-value')
    client=ModelClient(model='deepseek-v4-pro')
    client.max_cost=0.001
    network=Mock()
    client.client=network
    with pytest.raises(RuntimeError,match='budget reached'):
        client.complete([{'role':'user','content':'Hello'}])
    network.chat.completions.create.assert_not_called()


def test_unknown_deepseek_model_cannot_bypass_price_check(monkeypatch):
    monkeypatch.setenv('MODEL_PROVIDER','deepseek')
    monkeypatch.setenv('DEEPSEEK_API_KEY','offline-test-value')
    with pytest.raises(ValueError,match='documented DeepSeek model'):
        ModelClient(model='unpriced-model')


def test_cache_billing_uses_reported_hits_and_handles_missing_metadata():
    from model_client import deepseek_cost_upper
    assert deepseek_cost_upper({'prompt_tokens':10000,'prompt_cache_hit_tokens':9000,'completion_tokens':500},'deepseek-v4-pro') == pytest.approx(0.003696)
    assert deepseek_cost_upper({'prompt_tokens':10000,'completion_tokens':500},'deepseek-v4-pro') == pytest.approx(0.01518)
    assert deepseek_cost_upper({'prompt_tokens':10000,'prompt_tokens_details':{'cached_tokens':9000},'completion_tokens':500},'deepseek-v4-pro') == pytest.approx(0.003696)


def test_openai_budget_blocks_before_network(monkeypatch):
    monkeypatch.setenv('MODEL_PROVIDER','openai')
    monkeypatch.setenv('OPENAI_API_KEY','offline-test-value')
    client=ModelClient(model='gpt-6-luna')
    client.max_cost=0.00001
    network=Mock()
    client.client=network
    with pytest.raises(RuntimeError,match='budget reached'):
        client.complete([{'role':'user','content':'Hello'}])
    network.chat.completions.create.assert_not_called()


def test_luna_cache_write_premium_is_counted():
    from model_client import usage_cost_upper
    usage={'prompt_tokens':10000,'prompt_tokens_details':{'cached_tokens':6000,'cache_write_tokens':1000},'completion_tokens':500}
    assert usage_cost_upper(usage,'gpt-6-luna') == pytest.approx(0.000735)


def test_luna_request_disables_native_reasoning_and_uses_completion_limit(monkeypatch):
    monkeypatch.setenv('MODEL_PROVIDER','openai')
    monkeypatch.setenv('OPENAI_API_KEY','offline-test-value')
    client=ModelClient(model='gpt-6-luna')
    response=Mock()
    response.usage.model_dump.return_value={'prompt_tokens':10,'completion_tokens':4}
    response.choices=[Mock()]
    response.choices[0].finish_reason='stop'
    response.choices[0].message.model_dump.return_value={'role':'assistant','content':'Ready'}
    network=Mock()
    network.chat.completions.create.return_value=response
    client.client=network
    client.complete([{'role':'user','content':'Hello'}])
    args=network.chat.completions.create.call_args.kwargs
    assert args['reasoning_effort']=='none' and args['max_completion_tokens']==512
    assert 'max_tokens' not in args
    assert client.calls==1 and client.cost_upper>0
