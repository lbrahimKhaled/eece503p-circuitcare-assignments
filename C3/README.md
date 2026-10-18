# C3 · CircuitCare Business Assistant

**Ibrahim Khaled · 202500327 · EECE 503P**

Maya represents a fictional Beirut electronics repair service. She answers questions from the business profile, collects repair leads with permission, and logs feedback or unanswered questions.

The application uses Python, the OpenAI SDK, and Gradio ChatInterface. A three-way router runs before an explicit native tool-call loop. Both the text summary and extracted PDF are included in the system context. Persona and instructions are separate blocks in `agent.py` and the notebook.

## Files

| File | Purpose |
|---|---|
| `business_agent.ipynb` | Main notebook: implementation, recorded examples, reflection, tests |
| `agent.py` | Persona, instructions, router, tools, native model loop |
| `model_client.py`, `history.py` | API requests, process budget, short-term memory |
| `app.py`, `interface.py`, `interface.css` | Gradio repair desk, activity display, trace |
| `me/about_business.pdf`, `me/business_summary.txt` | Fictional business identity and policies |
| `me/summary.txt` | Identical summary under the alternate filename used in the handout |
| `tool_manifest.json` | Tool inputs and expected outputs |
| `demo.mp4`, `DEMO_GUIDE.md` | Demonstration and chapter guide |

## Try it

- Ask about the diagnostic fee or opening hours: the general route uses published facts.
- Request repair follow-up: Maya asks for missing name, email, issue, and permission.
- Supply synthetic details and consent: the model calls `record_customer_interest(email, name, message)`.
- Give feedback or ask an unpublished question: the model calls `record_feedback(question)`.

Both tools print a record ID and append to local JSONL files. They do not book a repair or send an email. The trace shows tool observations. Ten recorded browser turns are in `evidence/openai_browser.json`; the newer five-turn recording has its own inputs and results in `evidence/demo_live.json`.

Set `REFLECTION_ENABLED=true` for the optional draft-review step. Its draft and revised reply are logged locally; recorded examples are in `evidence/demo_reflection.json`. If review fails after a draft is complete, the original reply and completed tool results are preserved.

## Run

Use Python 3.11 or newer and run these commands from this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

On Windows, activate with `.venv\Scripts\activate`. Enter the OpenAI API key at the hidden prompt; the launcher keeps it in memory and opens the browser. Stop with Ctrl+C. Alternatively, copy `.env.example` to `.env`, fill in the key privately, and run `python app.py`.

The default is `MODEL_PROVIDER=openai`, `OPENAI_MODEL=gpt-6-luna`. Requests use 512 completion tokens, no automatic retries, and a 55-second timeout. A shared client limits each app process to 64 requests and an estimated $0.05. Failed requests consume a conservative local reservation. Restarting resets the process limit. `MAX_RUN_COST_USD` and `MAX_RUN_CALLS` configure these limits.

## Notebook and tests

Open `business_agent.ipynb` in Jupyter or VS Code from this folder. Install Jupyter separately if needed, select the same environment, and keep the modules, `me/`, and `evidence/` beside the notebook. Saved evidence can be inspected without an API key. Live switches are off by default.

```bash
python -m pytest -q tests
```

See [TESTING.md](TESTING.md) for test coverage and limitations. API keys, `.env`, and local `runtime_logs/` must stay out of the submission.

The interface runs at `http://127.0.0.1:7860`.

## Limits

The router uses simple heuristics and can miss mixed requests. Consent is checked by the model from the conversation; the C3 function validates contact-field shape. Model decisions can still miss or overuse tools. The business is fictional, prices are illustrative, and local logging is intended for course demonstrations. Hugging Face hosting is not included.

## References

- [OpenAI model](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Gradio ChatInterface](https://www.gradio.app/docs/gradio/chatinterface)
