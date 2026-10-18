# C4 demonstration

Ibrahim Khaled · 202500327 · EECE 503P

Open [demo.mp4](demo.mp4). Duration: 141.44 seconds. The recording uses the local Gradio app, OpenAI GPT-6 Luna, and synthetic contact details.

| Time | Behavior shown |
|---|---|
| 0:05 | Estimate: $60 subtotal minus the $15 diagnostic credit gives $45 labour. |
| 0:33 | Swollen-battery guidance through triage_device. |
| 0:52 | An unpublished question is logged through the original C3 feedback function. |
| 1:08 | Switch from Rami to Maya; matching model settings and fresh chat. |
| 1:14 | No lead tool call when consent is refused. |
| 1:32 | The model promises a save but has no saved tool observation yet. |
| 1:49 | All fields and explicit consent produce a real saved record. |

The browser remains at 1600 × 1500. Export uses one fixed crop, a caption strip, and normal speed. The video is 1320 × 1200, 25 fps. All frames decoded successfully; 1414 browser samples showed no outer-frame drift or page scrolling. Chapter captions are in `demo.srt`.

Inputs, replies, tool traces, and model usage are in `evidence/demo_live.json`. Video checks are in `evidence/demo_capture.json`.

The short consent continuation at 1:32 did not execute a save. That result is retained and identified by the caption. A subsequent message supplies every field and consent, after which the tool returns a saved record ID. The trace distinguishes an intended action from an executed action.
