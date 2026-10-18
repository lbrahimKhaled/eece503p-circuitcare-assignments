# Current OpenAI validation · C3

Ibrahim Khaled · 202500327 · EECE 503P

Verified on 2026-10-18 against the complete supplied handouts. This report supersedes earlier retest summaries; historical evidence remains labeled by its provider and implementation stage.

- 13 offline tests passed, including isolated submission-package checks. The complete main notebook was executed with live switches off.
- All 46 repository structure, inheritance, notebook, and evidence checks passed through `verify_submission.py`.
- Real OpenAI GPT-6 Luna requests use native reasoning effort none. Each app has a shared $0.05 / 64-call process budget.
- Initial OpenAI delivery testing was estimated at $0.00874825; the explicit inheritance audit added $0.00659535. Initial delivery plus inheritance audit estimate: $0.01534360, across both projects. These are conservative usage estimates, not an account invoice; earlier DeepSeek usage is separate.
- API credential files, runtime logs, caches, and Git metadata are excluded from submission ZIPs. Notebook outputs and package contents were scanned for secret patterns.
- Private repository: https://github.com/lbrahimKhaled/eece503p-circuitcare-assignments, folder C3/, branch main. Give the instructor access before submitting a private link.

The required C3 paths are present, including both summary filename variants used by the handout. Persona and instructions, three-way routing, exact required tool names, PDF/TXT context, native tool-result continuation, and Gradio ChatInterface are retained.

The 10 live browser turns in `evidence/openai_browser.json` contain both required model-requested tools and all three routes. The 114.52-second `demo.mp4` showcases OpenAI interactions and was fully decoded without errors. Desktop and 390px mobile layouts were inspected; no horizontal overflow was observed. The actual reflection draft/review is preserved in `evidence/openai_reflection.json`. The model sometimes over-logs a covered policy; C3 semantic consent relies on conversation instructions. Optional Hugging Face hosting is not implemented or claimed.

## Stable live demonstration update

The replacement `demo.mp4` is 114.52 seconds, at 1320 × 1000 and 25 fps. It shows 5 real browser turns, with continuous normal-speed capture, one fixed crop, and chapter captions. All frames decode; browser geometry sampling and encoded static-region comparison verify stable framing. Both interfaces also passed a fresh 390px mobile-width check. See `DEMO_GUIDE.md` for the chapter map and evidence.

Current offline tests: 13 in this project, 36 across both projects. Recording/rehearsal OpenAI usage is estimated at $0.006554790; combined OpenAI work across all three delivery stages is estimated at $0.021898390. API receipts are retained without credentials. These are conservative usage estimates, not an account invoice.

An existing optional-review bug was corrected: the reflection pass now receives completed messages and tool observations, preventing an uninformed review from denying a successful save. The new regression test and the real saved-lead video turn verify this. The unchanged core copy in C4 includes the same correction.
