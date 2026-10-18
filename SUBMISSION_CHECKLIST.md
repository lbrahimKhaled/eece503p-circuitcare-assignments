# Assignment compliance and C3 → C4 extension

**Ibrahim Khaled · 202500327 · EECE 503P**

Checked against the complete supplied C3 and C4 handouts. The requirements below are from those handouts; extra files are supporting implementation/evidence, not additional instructor requirements. C3 and C4 are separate submissions in one private repository.

## Directory structure

`C3/` is the project root called `business_bot/` in the C3 handout. That example root label is not a required Python package name. Required relative paths and filenames are preserved. The C4 handout specifies requirements, not a separate mandatory directory tree; C4 retains the C3 baseline structure and adds the extension.

```text
C3/
├── me/
│   ├── about_business.pdf
│   ├── business_summary.txt
│   └── summary.txt                 identical alias for the body's alternate filename
├── business_agent.ipynb            main C3 notebook
├── agent.py                       C3 persona, instructions, router, tools, model loop
├── app.py                         Gradio ChatInterface
├── .env.example                   empty credential template
├── requirements.txt
└── demo.mp4                       required demonstration video

C4/
├── me/
│   ├── about_business.pdf          unchanged C3 profile
│   ├── business_summary.txt        unchanged C3 summary
│   └── summary.txt                 unchanged alias
├── business_agent.ipynb            main C4 notebook, extended implementation
├── react_agent.ipynb               identical compatibility alias
├── agent.py                       unchanged C3 core, imported by the extension
├── react_agent.py                 manual LangGraph ReAct implementation
├── tools.py                       C3 adapters plus three new repair tools
├── app.py                         extended Gradio interface
├── .env.example                   empty credential template
├── requirements.txt
├── experiments.py
└── reflection.md
```

Both folders also contain tests, schemas, interface styling, evidence, and a README. A populated `.env` is intentionally excluded from the repository and ZIPs, as instructed by C3. The private local setup can copy `.env.example` to `.env`; the provided launcher also accepts a hidden process-only credential. No real API key is supplied in a submission.

## C3 requirement map

| Handout requirement | Implementation / evidence |
|---|---|
| Fictitious business name, mission, services, team, value proposition | `C3/me/about_business.pdf`, `business_summary.txt` |
| PDF and text formats with the required filenames | `C3/me/`; both summary filename variants supplied |
| Main chatbot notebook | `C3/business_agent.ipynb`, executed with implementation and evidence |
| Clearly separated persona and operational instructions | `PERSONA`, `INSTRUCTIONS` in `agent.py` and labeled notebook sections |
| General / lead / feedback-and-unanswered classification before the agent acts | `route_message`; route-specific handlers in `BusinessAgent.reply` |
| `record_customer_interest(email,name,message)` | Exact function name and required parameters retained in `agent.py` |
| `record_feedback(question)` | Exact function name and required parameter retained in `agent.py` |
| Logging through print/file mechanism | Both functions print identifiers and append local JSONL |
| Model really requests the tools | Native OpenAI tool requests in `evidence/openai_browser.json`; `demo.mp4` |
| Tool name, parameter, expected-output schemas | `tool_manifest.json`, notebook tool-contract section |
| Both summary and extracted PDF in system context | `load_business_context` |
| User input, recent history, tools, tool-result continuation | Native loop in `BusinessAgent.reply`; history regression tests |
| OpenAI or Gemini provider | Real OpenAI-hosted GPT-6 Luna evidence; current OpenAI SDK method |
| Gradio ChatInterface | `app.py`, designed local interface |
| GitHub repository with demonstration video | Private repository `C3/`, including `demo.mp4` |
| API credential kept private | `.env` ignored, empty example, hidden-input launcher, archive scans |
| Runs successfully | Executed notebook, live OpenAI evidence, passing tests and isolated ZIP checks |
| Optional reflection bonus | Current draft/review in `evidence/demo_reflection.json`; the review receives completed tool observations |
| Optional Hugging Face hosting bonus | Not implemented or claimed; not required for the core assignment |

The current SDK uses `OpenAI().chat.completions.create`, the supported modern spelling of the handout's older `openai.ChatCompletion` example.

## C4 requirement map

| Handout requirement | Implementation / evidence |
|---|---|
| Extend the previous business chatbot | Unchanged C3 core imported by C4; mappings below |
| Specify goal, audience, tools, constraints | C4 README and main notebook use-case section |
| Choose one permitted framework | LangGraph `StateGraph` |
| Manual loop, without a prebuilt agent executor | Explicit `reason`, `act`, `answer`, `stop` nodes and conditional edges |
| System prompt with behavior and tool descriptions | `initial_messages`, `PERSONAS`, `INSTRUCTIONS`, `PROTOCOL`, JSON schemas |
| Detect actions, validate/execute tools, return observations, continue | Parser, `ToolRegistry`, `act`, graph edges |
| Parse the final response and stop | `finish`, `next_node`, bounded `stop` path |
| Two different persona tasks, vocabulary, style, values | Maya intake and Rami technical triage, defined in `PERSONAS` |
| Match personas with LLM configuration | Temperature/top-p 0.7/0.95 versus 0.1/0.8 |
| With/without Chain-of-Thought prompting | Brief public step-by-step reasoning-summary condition versus direct action condition; logged contrast, no private internal transcript |
| Zero-shot versus few-shot | `expert_zero_shot` removes every worked example; baseline retains them |
| System prompt versus in-message instructions | `expert_full` versus `expert_user_instructions` |
| Vary LLM configuration and compare | `expert_warm_config`, same expert persona with warmer sampling; table and logs |
| Log experiment settings, outputs, tool traces, comparisons | `evidence/experiments.json`, CSV, notebook, reflection |
| Dedicated focused instructions, explicit inputs and outputs | Separate 21-rule `INSTRUCTIONS` block |
| Worked example inside the instructions | `Worked example:` in the delivered baseline instruction block |
| Persona and instructions do not conflict | Both personas share factual, safety, consent, and logging limits |
| Answer all five reflection questions | Main C4 notebook and `reflection.md` |
| Working assistant | Gradio app, current live extension evidence, current live matrix, tests |

The Chain-of-Thought prompt contrast uses short public explanations of relevant facts, calculations, and action choices. It does not request or claim access to private internal reasoning. Native model reasoning mode stays fixed across conditions. The zero-shot and instructions-ablation conditions intentionally remove the relevant material only for those experiments; the delivered working default retains the required instructions and worked example.

## Direct code inheritance

| Retained C3 component | How C4 uses it |
|---|---|
| `agent.py` | Byte-identical copy in C4, imported by both `react_agent.py` and `tools.py` |
| `load_business_context()` | Supplies original PDF and TXT facts to every ReAct request |
| `route_message()` | Classifies the input before the graph runs and populates the returned route |
| `record_customer_interest(email,name,message)` | Called by `record_interest` after C4 validates explicit consent |
| `record_feedback(question)` | Called by `log_unanswered` for both explicit feedback and unpublished questions |
| `history.py`, `model_client.py` | Retained shared behavior for short-term memory, model connection, and budgets |
| All three `me/` files | Byte-identical data in both independent submissions |

`C4/tests/test_c3_extension.py` verifies both source formats, inherited routing, C3 lead-record shape, and C3 feedback logging. `C4/evidence/c3_extension_live.json` verifies all original workflow types with the live extended agent. C4 adds catalogue lookup, triage, cost calculation, multiple configured personas, and a manually controlled state graph.

From the repository root, run `python verify_submission.py` for structural/inheritance/evidence checks without API calls. Run each folder's test suite for behavior checks. These checks verify the implementation and documented evidence; the functional score is not an instructor grade.
