# Reflection · C4 CircuitCare

**Ibrahim Khaled · 202500327 · EECE 503P**

## Which persona gave the most helpful or natural results?

Both Maya and Rami passed 12/12 functional checks in the current OpenAI matrix. Maya's intended task is approachable intake; Rami's is cautious symptom triage and verified prices. Their replies were both concise and similarly factual on these technical questions. I prefer Rami as the initial technical persona and offer Maya for intake, but this is a design judgment: there is no human naturalness rating or measured persona winner. The browser intake check separately confirms Maya can save a consenting lead.

## Which prompt and configuration combination performed best?

All seven setups scored 12/12, so the functional rubric produced a tie. Rami with system instructions, examples, low temperature (0.1), and top-p 0.8 remains the working default because it makes the operating rules explicit. The direct-action setup also passed and used fewer output tokens: 275 versus 424 for the matched full-expert condition. The summary condition emitted notes in all 6 decisions; the direct condition emitted 0 notes in 6 decisions after removing the note field from its protocol examples. This measures visible prompt behavior, not whether internal reasoning occurs.

| Setup | Checks | Calls | Public rationale notes | Output tokens |
|---|---:|---:|---:|---:|
| friendly_full | 12/12 | 6 | 6 | 458 |
| expert_full | 12/12 | 6 | 6 | 424 |
| expert_no_planning | 12/12 | 6 | 0 | 275 |
| expert_zero_shot | 12/12 | 6 | 6 | 473 |
| expert_user_instructions | 12/12 | 7 | 7 | 479 |
| expert_without_instructions | 12/12 | 6 | 6 | 444 |
| expert_warm_config | 12/12 | 6 | 6 | 415 |

The brief-summary condition operationalizes the assignment's Chain-of-Thought prompting contrast as a short public task-level explanation of the relevant fact/constraint and chosen action, followed by a tool observation. It never requests a private internal reasoning transcript. It compares prompting and observable summaries; it does not measure hidden reasoning or establish that the model internally reasons differently. Zero-shot removes every example, including the inline worked example. The no-instructions condition removes instructions and examples together. The warm condition changes temperature and top-p together, not one parameter at a time. There is one run per case/setup, so no statistical superiority is claimed.

## How well did the agent reason and use tools?

Every current matrix case used the expected tool: estimate_repair for the $20 diagnostic/SSD labour result, triage_device for swelling, and log_unanswered for unpublished brand-authorisation status. The current decision counts were 20 runs with 2 decisions, one run with 3 decisions. The logs retain every intermediate action and observation, including the additional catalogue lookup. Application code owns action parsing, validation, execution, observation return, and final-answer parsing inside LangGraph. These successful narrow cases do not prove general repair competence. The agent cannot inspect a device or quote parts.

## Did the instructions block visibly change behavior?

The ablation tied the baseline at 12/12 in this OpenAI sample, so the current data does not demonstrate a functional improvement from that block on these three questions. Persona text, business facts, protocol, and tool descriptions remain in the ablation and can supply enough guidance. In the older DeepSeek Pro matrix, the combined instructions/examples ablation missed one logging action. That historical observation is separate evidence under another model and earlier prompt, not a controlled OpenAI result. I retain the dedicated instructions to make required behavior and expected output auditable, not because this small sample proves a gain.

## Biggest implementation challenges

The extension now imports C3’s unchanged router, PDF/TXT context loader, and both logging functions. The four additional extension tests check inherited sources, routing, lead record format, and feedback logging. The key work was controlling the manual loop, returning usable observations after invalid actions, keeping examples out of the zero-shot condition, preserving history correctly, and keeping budgets and credentials separate from evidence. An older Pro run emitted one extra trailing brace; the parser now repairs exactly that suffix, records the original output, rejects other trailing content, and stops repeated failures. Hazard fallback is explicitly labeled as application behavior, not a model tool call.

Live OpenAI checks returned server errors with nonzero frequency/presence penalties. The final personas and warm configuration therefore vary temperature and top-p, which completed the live matrix. GPT-6 Luna uses native reasoning effort none in every setup; the public reasoning-summary prompt is the experimental variable. This avoids spending output tokens on an unobserved native reasoning mode. Both app processes share a bounded model client. Browser tests checked consent refusal and cleared history on persona switch. Remaining limits include keyword-based scoring, no human review panel, three cases, one sample per condition, possible prompt noncompliance, and no real workshop integrations.
