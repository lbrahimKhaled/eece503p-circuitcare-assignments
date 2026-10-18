# C4 testing

Ibrahim Khaled · 202500327 · EECE 503P

Checked on 2026-10-18.

| Check | Result |
|---|---|
| Offline behavior tests | 26 passed |
| Repository structure and notebook/source checks | 57 passed across C3 and C4 |
| Main notebook | All code cells executed; live switches off |
| Separate submission ZIP | Extracted and checked independently |
| Desktop and mobile interface | Desktop checked; 390px layout has no horizontal overflow |
| Demo video | 141.44 seconds; all frames decode; fixed outer frame |

Run `python -m pytest -q tests` from this folder. Tests use scripted model responses and do not spend API credit. Run `python verify_submission.py` from the repository root for structure, shared-source, notebook, and recorded-experiment checks.

Tests cover the manual graph, action validation, malformed JSON, loop limits, hazard fallback, history formats, consent flags, the estimator, inherited C3 tools, failed writes, request budgets, and experiment checkpoints. A failed experiment preserves the submitted matrix and stores partial results locally.

The recorded 21-run OpenAI matrix passes 84/84 keyword/tool checks. All seven setups tie, with one sample per case/setup. These checks do not establish a best persona or complete correctness. The demonstration retains a missed save after a short consent continuation; repeating all fields and permission produces a saved observation.

The review used separate environments installed from each requirements file and tests from freshly extracted ZIPs. No additional paid model requests were used for this review. Saved live evidence remains dated to its original run. Credentials, runtime logs, caches, and Git metadata are excluded from the ZIPs.
