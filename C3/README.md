# C3 · CircuitCare Business Assistant

**Ibrahim Khaled · 202500327 · EECE 503P**

CircuitCare is a fictional Beirut laptop and electronics repair service. Maya explains published services, collects consenting repair leads, and records feedback or unanswered questions. This is the independent C3 submission; C4 extends it in a separate folder.

The implementation uses **Python + OpenAI SDK + Gradio ChatInterface**. No agent orchestration framework is needed for this assignment. The code explicitly implements routing and the native model tool-call loop. The real OpenAI-hosted model has been tested, satisfying the provider choice in the handout.

## Requirement map

| Requirement | Where to inspect |
|---|---|
| Business mission, services, team, value proposition | `me/about_business.pdf`, `me/business_summary.txt` |
| Main notebook and separated persona/instructions | `business_agent.ipynb`, `PERSONA` and `INSTRUCTIONS` in `agent.py` |
| Three routes | `route_message`: general, lead, feedback/unanswered |
| Native model-requested tools | `record_customer_interest(email,name,message)`, `record_feedback(question)` |
| Schema and expected output contracts | `tool_manifest.json` |
| Both source formats + short-term memory | TXT and extracted PDF in every system prompt; last 12 user/assistant turns |
| Tool-result return and continuation | Bounded loop in `BusinessAgent.reply` |
| Required Gradio interface | `app.py`, `interface.py`, `interface.css`; local port 7860 |
| GitHub + demo video | Repository link below; `demo.mp4` shows real OpenAI browser interactions |
| Optional reflection | `REFLECTION_ENABLED=true`; `evidence/openai_reflection.json` retains actual draft/review |

The interface adds a repair-themed visual identity, service-price rail, quick prompts, readable chat, compact activity tags, and a collapsible raw trace. It remains a Gradio ChatInterface. Desktop and 390px mobile layouts were checked. No real booking, payment, email, or production CRM integration is claimed.

## What to try and expect

1. Ask “What is the diagnostic fee?” → general route; published $15 fee and limitations.
2. Ask for repair follow-up → lead route; Maya asks for missing contact details and consent.
3. Give a synthetic name, valid email, issue, and explicit permission → model requests `record_customer_interest`; success appears only after the tool saves locally.
4. Give feedback or ask for Apple-authorised status → model requests `record_feedback`; unpublished status is not invented.
5. Ask an unsupported guarantee or false-price instruction → reply stays grounded in the fictional sources.

`evidence/openai_browser.json` contains ten real browser turns covering these paths, memory, refusal of consent, invalid email, unknown pricing, and battery guidance. `demo.mp4` records the first five of those turns. `evidence/openai_reflection.json` captures a separate actual draft and review. The review can preserve an already-correct answer; the earlier deliberately flawed fixture remains in historical evidence and is labeled as such.

The heuristic router is intentionally small and may misclassify mixed requests. The model can sometimes over-log a covered policy question; this occurred in the reflection check. Lead consent is enforced by conversation instructions, while the C3 tool independently validates field shape only. This is a classroom assistant, not production customer-data infrastructure. Optional Hugging Face hosting is not included.

## Run the interface

Use Python 3.11 or newer. Open a terminal in **this assignment folder**:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

The launcher asks for the OpenAI API key with hidden input and opens the local interface in your browser. Paste it into the terminal prompt and press Enter; nothing appears while you type. The key stays in this process and is not saved. Stop the app with Ctrl+C. On Windows, activate with `.venv\Scripts\activate` instead.

Alternatively, copy `.env.example` to a private `.env`, fill `OPENAI_API_KEY` locally, and run `python app.py`. The default is `MODEL_PROVIDER=openai`, `OPENAI_MODEL=gpt-6-luna`. Never put an actual key in source, notebook cells, screenshots, Git, or an issue. No credentials are included. Synthetic customers use example.com addresses. Runtime JSONL logging is local classroom demonstration data.

GPT-6 Luna uses Chat Completions with `reasoning_effort=none` and `max_completion_tokens=512`. Native function calling is supported in that mode. C4's reasoning-summary prompt is independent of native reasoning mode. Automatic retries are off and the request timeout is 55 seconds. One shared client per app process limits the app to 64 calls and a conservative **$0.05** run budget. Each experiment run also shares one client. Restarting creates a new budget; this is not an account-wide billing limit. An incomplete output raises an error. A conservative pre-request reservation includes input bytes, message overhead, maximum output, and the Luna cache-write premium. Failed requests consume a reservation locally rather than permitting unlimited retries.

Rates checked on 2026-10-18: Luna standard input $0.10/M, cached input $0.01/M, cache writes $0.125/M, output $0.50/M tokens. Token-based estimates are not an invoice; prices and account billing can change. `MAX_RUN_COST_USD` and `MAX_RUN_CALLS` can be deliberately adjusted. Optional historical DeepSeek support is retained; its results are clearly identified separately.

## Notebook and local checks

Open the notebook from this folder in Jupyter or VS Code. Install Jupyter separately if needed. Keep the Python modules, `interface.css`, `me/`, and `evidence/` beside it. Every notebook code cell has been executed. Saved-evidence cells make no paid requests. Live UI/experiment switches default to `False`; importing an app does not launch it.

```bash
python -m pytest -q tests
```

## References

- [OpenAI GPT-6 Luna model, pricing, and Chat Completions compatibility](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Gradio ChatInterface](https://www.gradio.app/docs/gradio/chatinterface)

## Submission

[Private course repository](https://github.com/lbrahimKhaled/eece503p-circuitcare-assignments) → `C3/`. The normal `main` branch is sufficient; the handout requires a repository, not a special branch. Give the instructor access to this private repository before submitting the link. `summary.txt` is an identical alias under `me/` because the body and checklist use different summary filenames. Submit this C3 folder and its video independently of C4.

`evidence/verification_summary.json` and `RETEST_REPORT.md` identify the current validation. Earlier DeepSeek logs are historical and are not relabeled as OpenAI runs.
