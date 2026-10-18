# EECE 503P · CircuitCare assignments

**Ibrahim Khaled · 202500327**

One private course repository, two independent submissions:

| Folder | Assignment | Implementation | Start |
|---|---|---|---|
| [C3](C3/) | Business chatbot | OpenAI SDK, explicit native tool loop, Gradio | `python run.py` inside C3 |
| [C4](C4/) | Configurable custom ReAct | Manual LangGraph StateGraph, OpenAI, Gradio | `python run.py` inside C4 |

Each folder contains its own notebook, requirements, source, fictional business data, real model evidence, tests, and README. C3 additionally contains the required demo video. C4 contains its five-question reflection and 21-run experiment matrix. Submit the corresponding folder/link independently for each assignment. The `main` branch is sufficient; a special Git branch is not required by the supplied handouts. Give the instructor access before submitting this private repository.

## Run either project

Open a terminal in the chosen C3 or C4 folder, then:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

Paste the API key at the hidden terminal prompt and press Enter. The launcher opens the interface in the browser and keeps the key only for this process. C3 uses local port 7860, C4 uses 7861. Stop with Ctrl+C. Windows activation is `.venv\Scripts\activate`. Read the assignment README for notebook instructions and the optional private `.env` method.

The default model is OpenAI GPT-6 Luna. Each app shares a $0.05 / 64-call process budget; restarting begins a new budget. Tests and saved notebook evidence do not make paid calls. Combined OpenAI delivery testing, the explicit C3-to-C4 inheritance audit, and live demonstration recording are conservatively estimated at $0.021898390 across both projects; precise usage estimates and limitations are in each evidence folder. Earlier DeepSeek logs remain historical.

## Assignment compliance

C4 now directly imports C3’s unchanged router, PDF/TXT loader, and original lead/feedback functions. It retains the C3 business files and main notebook filename, then adds the manual LangGraph extension. [Requirement-by-requirement checklist](SUBMISSION_CHECKLIST.md). Run `python verify_submission.py` from this repository root for structural and inheritance checks without API calls.

## Preview

[C3 repair desk](C3/evidence/openai_interface.png) · [C4 agent workbench](C4/evidence/openai_expert_interface.png) · [C3 demo video](C3/demo.mp4) · [C4 demo video](C4/demo.mp4)

## Relationship to JafetAI

[JafetAI](https://github.com/lbrahimKhaled/JafetAI) is a separate public AUB-library assistant. The reviewed revision was `491c00d3448f29a70d887a932481ec39b4be4dae`. Its root and SQL agents use Google ADK LlmAgent/AgentTool, with an ADK runner controlling execution. It overlaps with agent/tool concepts, but it does not satisfy either handout as submitted:

- C3 asks for a fictional business profile in PDF/TXT, the specified three-way router and two named tools, and a Gradio ChatInterface. JafetAI has a different scenario, tools, and interface.
- C4 permits LangGraph, CrewAI, AutoGen, or OpenAI Agents SDK and asks for a manually implemented loop plus persona/prompt/configuration experiments. Google ADK is outside that list, and the reviewed ADK setup does not supply the required controlled assignment experiments.

JafetAI was inspected as reference material only. No code was run, no booking was attempted, and its repository was not modified. The CircuitCare submissions retain the user's chosen scenario and use the frameworks specified above.

Primary references: [JafetAI root agent](https://github.com/lbrahimKhaled/JafetAI/blob/491c00d3448f29a70d887a932481ec39b4be4dae/jafet/agent.py), [SQL agent](https://github.com/lbrahimKhaled/JafetAI/blob/491c00d3448f29a70d887a932481ec39b4be4dae/jafet/books/sql_agent.py), [OpenAI model](https://developers.openai.com/api/docs/models/gpt-6-luna), [LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api).
