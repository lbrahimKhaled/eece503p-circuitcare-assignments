# CircuitCare · EECE 503P

**Ibrahim Khaled · 202500327**

CircuitCare is a fictional laptop and electronics repair service. The two assignments are submitted separately in this repository.

| Folder | Assignment | Implementation | Demo |
|---|---|---|---|
| [C3](C3/) | Business assistant | OpenAI SDK, native tool calls, Gradio | [Video](C3/demo.mp4) |
| [C4](C4/) | Personas and ReAct | Manual LangGraph loop, OpenAI, Gradio | [Video](C4/demo.mp4) |

C4 extends C3's business context, router, and logging functions. Each folder is self-contained and includes its own main notebook, requirements, tests, business files, and demonstration.

## Run

Use Python 3.11 or newer. Open a terminal in either `C3/` or `C4/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

On Windows, activate with `.venv\Scripts\activate`. Enter the API key at the hidden prompt. The browser opens automatically: C3 uses port 7860 and C4 uses 7861. Stop with Ctrl+C. Keys can also be stored in a private `.env` copied from `.env.example`.

The default model is OpenAI GPT-6 Luna. Each app limits a process to an estimated $0.05 and 64 requests. Restarting resets that limit. Credentials and runtime logs are excluded from Git.

## Check the submission

Run `python verify_submission.py` here for structural checks. Run `python -m pytest -q tests` inside each assignment folder for its behavior tests. These commands make no model requests. See [the requirement map](SUBMISSION_CHECKLIST.md) and the individual READMEs for notebook and experiment instructions.

Submit the appropriate folder link for each assignment and give the instructor access to this private repository.
