# C3 live demonstration

Ibrahim Khaled · 202500327 · EECE 503P

Open `demo.mp4`. The video is a continuous live interaction with the delivered application and real OpenAI GPT-6 Luna responses. Synthetic contact details are used. No agent features were added for the demonstration.

The browser stays at 1600 × 1500 throughout. Export uses one fixed crop of the working area and a separate caption strip; the crop never changes. Loading before the demo is trimmed. There are no cuts between actions, zooms, speed changes, or fabricated application replies. Captions describe the existing behavior. The full video was decoded and checked; 1145 browser samples showed zero outer-page scrolling and zero frame-position/width drift. The encoded static region was also compared throughout the video.

| Time | Existing behavior shown |
|---|---|
| 0:00 | C3 / CircuitCare live demonstration — Real OpenAI responses | Fixed browser size | Continuous capture at normal speed |
| 0:05 | 01 / Answers grounded in the business profile — Published price and opening hours; general-question route is visible below. |
| 0:22 | 02 / Repair intake with short-term memory — The assistant collects missing details before saving a lead. |
| 0:40 | 03 / A genuine model-requested tool call — record_customer_interest returns a saved record ID in the open activity log. |
| 1:07 | 04 / Customer feedback becomes a saved record — The router selects feedback; record_feedback returns the saved record ID. |
| 1:25 | 05 / Unknown questions are logged honestly — The assistant logs the unpublished question and avoids inventing a quote or guarantee. |
| 1:46 | C3 / All three routes and both required tools demonstrated — The open trace shows real tool observations. Optional reflection logs are retained with the recording evidence. |

`demo.srt` contains the same chapter captions. `evidence/demo_live.json` contains the actual inputs, conversation history, model usage, replies, and tool traces. `evidence/demo_capture.json` contains the video and frame checks. `evidence/demo_testing_cost.json` covers recording work and rehearsals across both projects, including a conservative reservation for a failed connection; it is a usage estimate, not an invoice.

The optional reflection mode is enabled. Its completed draft/review pairs are retained in `evidence/demo_reflection.json`. The review receives the completed conversation and actual tool observations, so it can preserve a successful save confirmation. A regression test checks that grounding. The layout fix sets a stable page width; the agent's tools and workflows are unchanged.
