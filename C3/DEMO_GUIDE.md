# C3 demonstration

Ibrahim Khaled · 202500327 · EECE 503P

Open [demo.mp4](demo.mp4). Duration: 114.52 seconds. The recording uses the local Gradio app, OpenAI GPT-6 Luna, and synthetic contact details.

| Time | Behavior shown |
|---|---|
| 0:05 | Published diagnostic fee and opening hours; general-question route. |
| 0:22 | Repair intake asks for missing contact details and permission. |
| 0:40 | The model calls record_customer_interest and receives a saved record ID. |
| 1:07 | Customer feedback is saved through record_feedback. |
| 1:25 | An unpublished question is logged without an invented quote or guarantee. |

The browser remains at 1600 × 1500. Export uses one fixed crop, a caption strip, and normal speed. The video is 1320 × 1000, 25 fps. All frames decoded successfully; 1145 browser samples showed no outer-frame drift or page scrolling. Chapter captions are in `demo.srt`.

Inputs, replies, tool traces, and model usage are in `evidence/demo_live.json`. Video checks are in `evidence/demo_capture.json`.

Reflection is enabled in the recording. Draft and revised replies are in `evidence/demo_reflection.json`; the reviewer receives completed tool observations.
