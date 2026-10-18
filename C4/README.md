# C4 · CircuitCare Personas and ReAct

**Ibrahim Khaled · 202500327 · EECE 503P**

This project extends the C3 business assistant with a manually implemented ReAct loop in LangGraph StateGraph. It helps non-expert laptop customers understand services, calculate labour estimates, triage symptoms, and request follow-up. OpenAI supplies model responses; Gradio provides the interface.

## Extension of C3

`agent.py`, `history.py`, `model_client.py`, and all `me/` files match C3. The graph imports C3's `load_business_context` and `route_message`. The new adapters call the original `record_customer_interest` and `record_feedback` functions. C4 is self-contained and does not require a neighbouring C3 folder.

| Tool | Purpose |
|---|---|
| `get_service` | Look up a published service price |
| `triage_device` | Return conservative first steps for a symptom |
| `estimate_repair` | Calculate labour and apply the diagnostic credit once |
| `record_interest` | Validate a consent flag, then call C3 lead logging |
| `log_unanswered` | Call C3 feedback logging for feedback or missing facts |

Schemas validate tool arguments. The assistant cannot inspect devices, make a final diagnosis, quote parts, query inventory, book repairs, or guarantee completion dates.

## Manual loop

```text
START → reason → act → reason → … → answer → END
             ↘ stop → END
```

`react_agent.py` defines the graph and owns action detection, JSON parsing, tool execution, observations, and final-answer parsing. It uses no prebuilt agent executor. The loop stops after at most five decisions. Invalid outputs receive a corrective observation; one extra trailing closing brace can be repaired with the original output retained. Exhausted hazard requests have labeled application fallback guidance.

The dedicated instructions are separate from persona text and include input/output requirements and a worked example.

## Personas and experiments

| Persona | Task and style | Temperature | top-p |
|---|---|---:|---:|
| Maya | Friendly intake; plain language, affordability, consent | 0.7 | 0.95 |
| Rami | Technical triage; precise language, safety, verified estimates | 0.1 | 0.8 |

Seven configurations were tested on the same three cases: diagnostic-credit calculation, swollen-battery advice, and unpublished brand authorisation. The 21 runs compare personas, reasoning-summary prompting versus direct action, zero/few-shot examples, system/in-message instructions, an instructions/examples ablation, and warmer expert sampling.

| Setup | Checks | Model calls | Rationale notes | Output tokens |
|---|---:|---:|---:|---:|
| friendly_full | 12/12 | 6 | 6 | 458 |
| expert_full | 12/12 | 6 | 6 | 424 |
| expert_no_planning | 12/12 | 6 | 0 | 275 |
| expert_zero_shot | 12/12 | 6 | 6 | 473 |
| expert_user_instructions | 12/12 | 7 | 7 | 479 |
| expert_without_instructions | 12/12 | 6 | 6 | 444 |
| expert_warm_config | 12/12 | 6 | 6 | 415 |

All configurations tied on 84 functional checks. There is one sample per case/setup, and the checks use keywords and tool observations. They do not establish a best persona or measure naturalness. The Chain-of-Thought comparison uses brief public explanations of relevant evidence and action choice; it does not request private reasoning. Zero-shot removes all examples. The ablation removes instructions and examples together. Temperature and top-p change together in the warm condition. The model and token cap stay fixed.

`evidence/experiments.json` contains settings, replies, actions, observations, timing, and usage; `experiment_scores.csv` contains the comparison table. The five reflection questions are answered in [reflection.md](reflection.md) and the main notebook.

```bash
python experiments.py          # inspect the saved-results location; no API calls
python experiments.py --live   # paid matrix; replaces evidence after successful completion
```

An interrupted run keeps its partial checkpoint under `runtime_logs/experiments/` and preserves the submitted evidence. Results are dated in UTC when run.

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

The interface runs at `http://127.0.0.1:7861`. Switching personas clears conversation history. `react_agent.ipynb` is an identical alias of the main notebook.

## Demonstrations and limits

[demo.mp4](demo.mp4) shows estimation, triage, unanswered-question logging, persona switching, refusal of consent, and a saved follow-up. [DEMO_GUIDE.md](DEMO_GUIDE.md) lists chapters. `evidence/c3_extension_live.json` records the inherited workflows; `evidence/openai_browser.json` records additional interface checks.

The recording includes a short consent continuation where the model promises a save without calling the tool. The next message, with all fields and consent, produces the actual saved observation. The caption identifies the incomplete action. Model promises alone do not confirm saved records. Consent validation also relies on the model correctly interpreting the conversation. This is a course prototype with fictional business data and local logging.

## References

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [OpenAI model](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [Gradio ChatInterface](https://www.gradio.app/docs/gradio/chatinterface)
