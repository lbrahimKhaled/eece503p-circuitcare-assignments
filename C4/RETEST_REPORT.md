# Current OpenAI validation · C4

Ibrahim Khaled · 202500327 · EECE 503P

Verified on 2026-10-18. This report supersedes the older DeepSeek-only retest summaries; historical evidence remains labeled by its provider.

- Real OpenAI GPT-6 Luna requests completed with native reasoning effort none.
- 19 offline tests passed. The complete notebook was executed with all live switches off.
- 5 real browser turns are saved in evidence/openai_browser.json; synthetic contacts only.
- Desktop interface inspected; 390px mobile viewport checked with actual content width 390px and no horizontal overflow.
- Per-process app budget: $0.05 / 64 calls, shared across messages. Additional OpenAI testing across both projects conservatively estimated at $0.00874825, below the separate $0.10 test cap. This is an estimate, not an account invoice.
- Credential files and runtime logs are excluded. Notebook outputs and archive contents were scanned for secret patterns.
- Private repository: https://github.com/lbrahimKhaled/eece503p-circuitcare-assignments, folder C4/, branch main. Instructor access is required for a private submission link.

The complete current matrix has 21 OpenAI runs and scores 84/84 functional checks. All seven configurations tied. Reasoning-summary versus direct prompting generated 6 versus 1 public notes in their matched six decisions; direct prompting was not perfectly followed. Private model reasoning is neither requested nor inferred from those notes. No statistical or grading claim is made.
