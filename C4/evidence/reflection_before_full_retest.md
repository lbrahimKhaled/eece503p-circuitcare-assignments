### Which persona gave the most helpful or natural results?

Rami, the cautious technical specialist, was the best fit for the repair-triage default in this small test. His full configuration scored 12/12 across the three shared cases; Maya's full configuration scored 11/12. Both calculated the labour estimate correctly and used the safety tool for a swollen battery. Maya's authorisation answer was approachable and honest about uncertainty, but she offered to log the unanswered question instead of actually calling the logging tool. Rami's baseline completed that action before answering. This makes his baseline more useful for a workflow in which logging matters.

Maya's phrasing was often more conversational: she used reassurance and invited follow-up. Naturalness is a qualitative reading of the saved replies, not a measured human preference score. Her distinct intake role is demonstrated separately with a synthetic consenting customer. The experiment does not establish that one persona is universally better.

### Which prompt and configuration combination performed best?

The complete expert setup, the expert zero-shot setup, and the expert setup without the dedicated instructions/examples each scored 12/12 after applying the final scorer to the raw replies. The friendly baseline, expert without a planning request, expert with instructions in a user message, and expert with the warmer configuration each scored 11/12. In each of those lower-scoring setups, the missing point was the unanswered-question logging action.

I select the complete expert baseline as the default because it combines the observed functional score with explicit operating limits and a worked example that are easy to inspect and maintain. It is tied on this benchmark, so the data do not prove that few-shot prompting or the dedicated instruction block caused better performance. The full expert sampling settings are temperature 0.1, top_p 0.8, frequency penalty 0.0, and presence penalty 0.0. Maya uses 0.7, 0.95, 0.2, and 0.1 respectively. The warmer-expert comparison changes that entire configuration bundle. It cannot tell which individual parameter caused a difference.

The model and 384-token output cap were fixed. top_k was not tested because it is not exposed by this Chat Completions API. DeepSeek's native thinking mode was disabled throughout. The planning comparison changes prompt wording, asking for step-by-step consideration versus direct action selection; only short decision summaries are retained. This is not a comparison of hidden reasoning traces or native model reasoning modes.

### How well did the agent reason and use tools?

Every setup used the estimator for the diagnostic-plus-SSD case. The tool calculated $15 + $20 - $15 = $20 in illustrative labour, excluding the SSD. This moves arithmetic and the credit rule into deterministic code instead of relying on a fluent guess. The battery cases used the triage tool and returned conservative guidance. The main observed workflow weakness was omission of the logging action even when the final text admitted that a business fact was unavailable. A polite promise or offer to log is not equivalent to executing a tool.

The traces show actual parsed decisions, executed actions, and returned observations. They make it possible to check that the model used the appropriate function and read its result. They are not evidence that the model follows a reliable general reasoning process on unseen tasks. Five model decisions cap each turn. Offline tests additionally cover malformed JSON recovery, unknown tools, invalid arguments, loop termination, consent rejection, fee-credit behavior, and preservation of Gradio message history.

### Did the instructions block noticeably change behavior?

The instructions provide a clear JSON contract, state when tools are required, constrain business claims, and specify contact consent and device-safety limits. The full expert baseline followed the logging instruction, but the no-instructions/examples setup also did so on these same three cases. Both scored 12/12. Therefore this experiment shows no measurable gain from that block on the selected functional checks. The persona, tool descriptions, protocol, and business facts still supplied substantial guidance in the ablation.

Putting the instructions in a user message coincided with an omitted logging action in the authorisation case. The planning-off variant had the same omission. Each case was sampled once, so these differences could reflect sampling variation. The instructions ablation also removes examples, and the zero-shot contrast removes the inline worked example as well as the extra examples. These are practical prompt-package comparisons, not perfectly isolated causal measurements. More varied cases and repeated trials are needed before stronger conclusions.

### Biggest implementation challenges

The first challenge was implementing the cycle explicitly while using a framework. LangGraph handles state and edges, but custom nodes own parsing, allowlisted dispatch, observations, and final-answer extraction. Malformed output must become a recoverable observation rather than an exception or an unbounded loop. Tool argument validation and a step limit make this behavior inspectable.

The second challenge was separating persona from operational rules. A friendly invitation can delay a required logging action, as Maya's saved authorisation reply demonstrates. The final answer must be checked against the trace when claiming an action happened. Production use would benefit from additional policy checks, broader intent tests, and a consent gate grounded in structured user confirmation.

The third challenge was integrating current Gradio message formats. Live interface testing exposed a mismatch between content blocks and plain strings that dropped previous messages. A shared normalizer now preserves text from both formats, and regression tests verify that prior customer symptoms reach each model. Changing persona clears the visible chat and its internal history states.

The final challenge was evaluating cheaply without overstating the evidence. Seven setups and three shared cases produced 21 real runs, with raw responses, configuration, timing, and API-reported usage saved. A naive safety-keyword check initially treated “Do not ... puncture it” as unsafe. The scorer was corrected to recognize sentence-level negation, given a regression test, and reapplied to the same retained replies without extra model calls. Even the corrected scorer is only a small functional screen. It does not replace human review, measure all safety properties, or establish statistical superiority. Future work should use repeated runs, more symptom and consent scenarios, and blinded human assessment of clarity and naturalness.


### Follow-up: model choice

A targeted follow-up tested DeepSeek V4 Pro against the saved Flash failure for Maya on the same unpublished-authorisation question. The persona, prompt, examples, sampling settings, 384-token cap, and disabled native thinking were held fixed. Flash scored 3/4 because it offered to log rather than executing the tool. Pro executed `log_unanswered`, received a saved observation, and then acknowledged uncertainty and the logged question, scoring 4/4 on the final functional checks. The scorer was expanded to recognize “isn't published” and “not sure” as explicit uncertainty; a regression test checks these wordings. The raw replies remain available.

The C4 working assistant now selects Pro by default and retains Rami as the default persona. This is a practical choice based on the observed action completion, not proof that Pro is generally better. Only one follow-up task was sampled once with Maya, and Pro was not rerun across the entire original matrix or with Rami. Generalizing this result to the default expert persona is an inference that needs broader testing. The original 21 Flash runs are preserved, and the matrix code pins Flash so its model choice is reproducible. Flash remains available as the cheaper interactive setting. Pro has higher per-token prices, so cost limits now use model-specific rates rather than Flash rates for every DeepSeek request.
