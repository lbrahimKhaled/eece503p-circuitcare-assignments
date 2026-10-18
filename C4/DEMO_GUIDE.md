# C4 live demonstration

Ibrahim Khaled · 202500327 · EECE 503P

Open `demo.mp4`. The video is a continuous live interaction with the delivered application and real OpenAI GPT-6 Luna responses. Synthetic contact details are used. No agent features were added for the demonstration.

The browser stays at 1600 × 1500 throughout. Export uses one fixed crop of the working area and a separate caption strip; the crop never changes. Loading before the demo is trimmed. There are no cuts between actions, zooms, speed changes, or fabricated application replies. Captions describe the existing behavior. The full video was decoded and checked; 1414 browser samples showed zero outer-page scrolling and zero frame-position/width drift. The encoded static region was also compared throughout the video.

| Time | Existing behavior shown |
|---|---|
| 0:00 | C4 / CircuitCare live demonstration — Real OpenAI responses | Fixed browser size | Continuous capture at normal speed |
| 0:05 | 01 / Calculate the combined labour estimate — The tool applies the $15 diagnostic credit: $60 subtotal becomes $45 labour. |
| 0:33 | 02 / Safety triage through a dedicated tool — Watch the decision, triage_device observation, and final guidance in the right panel. |
| 0:52 | 03 / C3 feedback logging inside the advanced agent — An unpublished business fact triggers log_unanswered, which calls the original C3 logger. |
| 1:08 | 04 / Switch persona and matching model configuration — Maya uses temperature 0.7 / top-p 0.95. Switching starts a fresh chat. |
| 1:14 | 05 / Consent controls whether details are saved — The assistant should not call record_interest when permission is refused. |
| 1:32 | 06 / Verify the tool result before trusting a save — This reply promises a save but has no tool observation yet; the record has not been saved. |
| 1:49 | 07 / Clear permission produces a real saved record — The consent adapter calls the original C3 lead function; the returned observation confirms saving. |
| 2:13 | C4 / Existing personas, tools, consent, and manual loop demonstrated — The activity cards are actual model decisions and tool observations; no application features were added. |

`demo.srt` contains the same chapter captions. `evidence/demo_live.json` contains the actual inputs, conversation history, model usage, replies, and tool traces. `evidence/demo_capture.json` contains the video and frame checks. `evidence/demo_testing_cost.json` covers recording work and rehearsals across both projects, including a conservative reservation for a failed connection; it is a usage estimate, not an invoice.

The persona switch starts a fresh chat. The recording retains a permission message after which the model promised a save but did not call the tool. Its caption explicitly identifies that incomplete action. A subsequent message supplies explicit permission with every field, and the real tool returns a saved record. This shows the model's actual interaction and a limitation of relying on model decisions; a promise is not evidence of a saved record. The tool panel displays public action summaries and actual observations, not private model reasoning.
