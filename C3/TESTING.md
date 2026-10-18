# C3 testing

Ibrahim Khaled · 202500327 · EECE 503P

Checked on 2026-10-18.

| Check | Result |
|---|---|
| Offline behavior tests | 16 passed |
| Repository structure and notebook/source checks | 57 passed across C3 and C4 |
| Main notebook | All code cells executed; live switches off |
| Separate submission ZIP | Extracted and checked independently |
| Desktop and mobile interface | Desktop checked; 390px layout has no horizontal overflow |
| Demo video | 114.52 seconds; all frames decode; fixed outer frame |

Run `python -m pytest -q tests` from this folder. Tests use scripted model responses and do not spend API credit. Run `python verify_submission.py` from the repository root for structure, shared-source, notebook, and recorded-experiment checks.

Tests cover the three routes, history formats, valid and invalid tool calls, loop limits, request budgets, reflection observations, and failed reflection after a completed save. A route cannot execute a tool that was not offered to the model. Failed local writes return an error observation.

Recorded model behavior is in `evidence/openai_browser.json` and `evidence/demo_live.json`. Both required tools and all routes are represented. Reflection pairs are in `evidence/demo_reflection.json`. The router is heuristic, and semantic consent depends on the model interpreting the dialogue.

The review used separate environments installed from each requirements file and tests from freshly extracted ZIPs. No additional paid model requests were used for this review. Saved live evidence remains dated to its original run. Credentials, runtime logs, caches, and Git metadata are excluded from the ZIPs.
