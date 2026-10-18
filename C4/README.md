# C4 · CircuitCare Configurable ReAct Agent

**Ibrahim Khaled · 202500327 · EECE 503P**

This independent C4 submission extends the CircuitCare business with a **manual ReAct loop inside LangGraph StateGraph**, OpenAI GPT-6 Luna, and a Gradio persona-switching workbench. Google ADK is not used. LangGraph is explicitly one of the frameworks permitted by the handout.

## Goal, audience, tools, limits

The assistant helps non-expert laptop customers understand published services, obtain illustrative labour estimates, safely triage symptoms, and request human follow-up. Tools are `get_service`, `triage_device`, `estimate_repair`, `record_interest`, and `log_unanswered`. The allowlist and JSON schemas validate action arguments. Follow-up saving requires valid contact fields and a true consent flag. It cannot inspect a device, make a final diagnosis, quote unpublished parts, query stock, guarantee a deadline, book a repair, or charge anyone. All business facts are fictional.

## Manually implemented cycle

```text
START → reason → act → reason → … → answer → END
             ↘ stop → END  (bounded failure)
```

`reason` calls the model and parses one action or final JSON object. `act` executes a validated local tool and returns an observation to the next model decision. Conditional edges decide whether to act, answer, or stop after five decisions. There is no AgentExecutor, create_react_agent, or prebuilt ToolNode. LangGraph supplies state transitions; this code owns the loop. One unmatched trailing closing brace can be repaired with the raw output retained. Other malformed output produces a corrective observation. Exhausted hazard questions have separately labeled application fallback guidance.

## Personas and configurations

| Persona | Primary task, style, values | Temperature | top-p |
|---|---|---:|---:|
| Maya | Friendly intake; plain language; affordability and consent | 0.7 | 0.95 |
| Rami | Technical triage; precise language; safety, evidence, verified costs | 0.1 | 0.8 |

The dedicated instructions are separate from persona text, specify the input and JSON output, and contain a worked example. Examples and instruction placement are independently selectable in `Setup`. The final OpenAI setup varies temperature and top-p; live nonzero repetition-penalty probes returned server errors, so those parameters are not part of the delivered configurations. `top_k` is not sent. Model and 512-token cap remain fixed within the primary matrix.

## Controlled prompt comparisons and results

Seven setups × three shared cases = 21 **real OpenAI** runs. The cases cover diagnostic-credit calculation, swollen-battery guidance, and unpublished brand-authorisation status. Contrasts cover personas, brief task-level reasoning summaries versus direct action selection, zero/few-shot examples, system/user-message instructions, a combined instructions/examples ablation, and a warmer expert configuration.

The assignment's with/without Chain-of-Thought prompt comparison is implemented using brief public reasoning summaries of relevant evidence and action choice. Private chain-of-thought is never requested. The direct condition asks for no note; it nevertheless emitted one note in six decisions. The summary condition emitted six notes. These logs support a comparison of prompts and public explanations, not a claim about hidden cognition. The zero-shot condition removes all examples, including the inline instructions example; the working baseline keeps it. The ablation removes instructions and examples together, so it is not an isolated test of one sentence.

| Setup | Checks | Calls | Public rationale notes | Output tokens |
|---|---:|---:|---:|---:|
| friendly_full | 12/12 | 6 | 6 | 425 |
| expert_full | 12/12 | 6 | 6 | 433 |
| expert_no_planning | 12/12 | 6 | 1 | 283 |
| expert_zero_shot | 12/12 | 6 | 6 | 423 |
| expert_user_instructions | 12/12 | 6 | 6 | 424 |
| expert_without_instructions | 12/12 | 6 | 6 | 433 |
| expert_warm_config | 12/12 | 6 | 6 | 431 |

All 84 functional checks passed. This is a small keyword/tool-based screen, not an instructor grade or complete measure of correctness, safety, or naturalness. Each condition has one sample per case. All seven configurations tied; no best model or persona is established. Public rationale counts and output tokens are reported separately from the functional score. See `reflection.md` and the notebook for all five reflection answers and the limitations.

## Files and demonstrations

- `react_agent.ipynb`: complete implementation, executed evidence cells, comparisons, reflection.
- `react_agent.py`, `tools.py`: manual graph, personas, focused instructions, schemas, tool functions.
- `experiments.py`: repeatable matrix and explicit scoring checks.
- `evidence/experiments.json`, `experiment_scores.csv`: current OpenAI results with settings, usage, timing, actions, observations, replies, rationale counts.
- `evidence/openai_browser.json`: real UI checks for $45 combined labour, Maya's consenting intake, refusal of consent, hazard triage, and cleared history on persona switch.
- `app.py`, `interface.py`, `interface.css`: repair workbench, persona profile, public decision/tool cards, expandable full trace; local port 7861.
- `evidence/deepseek_pro_matrix.json`, `flash_original.json`, and earlier retest files: historical provider/prompt versions, preserved without relabeling.

```bash
python experiments.py             # no paid calls; points to saved evidence
python experiments.py --live      # paid OpenAI matrix; overwrites primary results
```

The historical `model_comparison.py` is read-only; its older Flash/Pro comparison is not a current controlled experiment. Starting an app or experiment requires a private credential, but reading recorded evidence does not.

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

[Private course repository](https://github.com/lbrahimKhaled/eece503p-circuitcare-assignments) → `C4/`. Submit this folder independently of C3. Give the instructor access to the private repository. `reflection.md` and the notebook contain the complete reflection; there is no separate PDF requirement for C4 when the reflection is in the notebook. Hosting is not claimed.

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
