# Current OpenAI validation · C4

Ibrahim Khaled · 202500327 · EECE 503P

Verified on 2026-10-18 against the complete supplied handouts. This report supersedes earlier retest summaries; historical evidence remains labeled by its provider and implementation stage.

- 23 offline tests passed, including isolated submission-package checks. The complete main notebook was executed with live switches off.
- All 46 repository structure, inheritance, notebook, and evidence checks passed through `verify_submission.py`.
- Real OpenAI GPT-6 Luna requests use native reasoning effort none. Each app has a shared $0.05 / 64-call process budget.
- Initial OpenAI delivery testing was estimated at $0.00874825; the explicit inheritance audit added $0.00659535. Initial delivery plus inheritance audit estimate: $0.01534360, across both projects. These are conservative usage estimates, not an account invoice; earlier DeepSeek usage is separate.
- API credential files, runtime logs, caches, and Git metadata are excluded from submission ZIPs. Notebook outputs and package contents were scanned for secret patterns.
- Private repository: https://github.com/lbrahimKhaled/eece503p-circuitcare-assignments, folder C4/, branch main. Give the instructor access before submitting a private link.

C4 imports C3's unchanged router, PDF/TXT loader, and original lead/feedback functions. `agent.py`, `history.py`, `model_client.py`, and all business files match C3 byte-for-byte. Four additional tests verify inherited sources, routing, lead record shape, and feedback logging. Four current live cases in `evidence/c3_extension_live.json` verify published service answers, consenting lead saving, feedback, and an unanswered question through the extended graph.

The primary 21-run OpenAI matrix was rerun after these changes and passed 84/84 functional checks across seven setups. All setups tied. The matched reasoning-summary and direct conditions emitted 6 versus 0 public notes in six decisions each, using 424 versus 275 output tokens. Twenty runs used two model decisions; one used three. These narrow functional checks are not an instructor grade or a human naturalness evaluation.

The manual LangGraph nodes implement decision, action, observation, final parsing, and bounded stopping. The main `business_agent.ipynb` and compatibility alias `react_agent.ipynb` are byte-identical. Both personas, prompt/configuration comparisons, a focused instructions block with worked example, and all five reflection answers are included. The C4 handout gives no separate mandatory file tree; the C3 baseline is preserved and extended.

The five earlier browser turns in `evidence/openai_browser.json` document the unchanged interface, consent refusal, and persona-switch memory reset. Desktop and 390px mobile layouts were inspected without horizontal overflow. Current backend behavior is documented by the newer live extension checks and experiment matrix.

## Stable live demonstration update

The replacement `demo.mp4` is 141.44 seconds, at 1320 × 1200 and 25 fps. It shows 6 real browser turns, with continuous normal-speed capture, one fixed crop, and chapter captions. All frames decode; browser geometry sampling and encoded static-region comparison verify stable framing. Both interfaces also passed a fresh 390px mobile-width check. See `DEMO_GUIDE.md` for the chapter map and evidence.

Current offline tests: 23 in this project, 36 across both projects. Recording/rehearsal OpenAI usage is estimated at $0.006554790; combined OpenAI work across all three delivery stages is estimated at $0.021898390. API receipts are retained without credentials. These are conservative usage estimates, not an account invoice.
