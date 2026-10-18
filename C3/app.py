import json
import os
from functools import lru_cache
import gradio as gr
from agent import BusinessAgent
from model_client import ModelClient
from interface import CSS, THEME, HEAD, activity_html, footer


def build_app():
    @lru_cache(maxsize=1)
    def shared_client():
        return ModelClient()

    def respond(message, history):
        try:
            agent = BusinessAgent(client=shared_client(), reflection=os.getenv('REFLECTION_ENABLED','false').lower() == 'true')
            result = agent.reply(message, history)
            return result['reply'], activity_html(result['trace'], result['route']), json.dumps(result['trace'], indent=2)
        except RuntimeError:
            return 'This session reached its request, output, or spending limit. Please ask the person running the demo to check the session.', activity_html([]), 'Request stopped by a runtime limit.'
        except Exception:
            return 'The model connection is unavailable. Check your private settings and try again.', activity_html([]), 'No request completed.'

    with gr.Blocks(title='CircuitCare | Repair desk', analytics_enabled=False) as demo:
        gr.HTML('<div class="topnav"><div class="brand"><span class="brand-icon">↗</span>CircuitCare<span style="color:#8aa297;font-weight:400">.</span></div><div class="nav-links"><span class="nav-label">REPAIR. REUSE. REIMAGINE.</span><span class="pill"><span class="dot"></span>YOUR REPAIR DESK</span></div></div>', elem_id='topnav')
        gr.HTML("""<section class="hero"><div><div class="eyebrow">A little care. A longer life.</div><h1 class="hero-title">Good devices deserve<br><em>a second life.</em></h1><div class="hero-copy">Clear answers, thoughtful repairs, and a practical next step.<br>Meet Maya, your CircuitCare service advisor.</div><div class="chips"><span class="chip">Transparent estimates</span><span class="chip">Repair before replace</span><span class="chip">Beirut, Lebanon</span></div></div><svg class="hero-art" viewBox="0 0 300 190" role="img" aria-label="Illustration of a laptop being repaired"><circle cx="156" cy="93" r="85" fill="#e2eddd"/><path d="M34 126h231" stroke="#b6cfbd" stroke-dasharray="3 5"/><rect x="68" y="39" width="165" height="107" rx="9" fill="#1b4141"/><rect x="75" y="46" width="151" height="92" rx="4" fill="#d7eee0"/><path d="M129 92l14 14 28-32" fill="none" stroke="#138574" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M54 147h194l16 12q0 7-10 7H48q-10 0-10-7z" fill="#9dbca8"/><path d="M124 148h53l-5 6h-43z" fill="#c8dfcc"/><circle cx="232" cy="45" r="24" fill="#c7ecae"/><path d="M222 45h20m-10-10v20" stroke="#275e47" stroke-width="3"/><circle cx="54" cy="85" r="7" fill="#f1ce7c"/></svg></section>""")
        with gr.Row(elem_id='main-layout'):
            with gr.Column(scale=1,min_width=250,elem_id='service-rail'):
                gr.HTML('<div class="rail-title">Your service advisor</div><div class="person"><div class="avatar">MN</div><div><div class="person-name">Maya Nassar</div><div class="person-desc">Friendly, clear, and here to help</div></div></div><div class="rail-title">The essentials</div><div class="service-row"><span>Diagnostic assessment</span><b>$15</b></div><div class="service-row"><span>Internal cleaning</span><b>$25</b></div><div class="service-row"><span>SSD installation labour</span><b>$20</b></div><div class="small-note">Illustrative USD prices. Parts excluded.<br>The diagnostic fee is credited against approved repair labour.</div><div class="rail-callout"><b>Visit the service desk</b><br>Mon–Fri · 09:00–18:00<br>Saturday · 10:00–14:00<br>Asia/Beirut · Sunday closed</div>')
            with gr.Column(scale=3,min_width=360,elem_id='chat-panel'):
                gr.HTML('<div class="panel-heading"><div><h2>Let’s figure out your next step.</h2><p>Ask about a service, request follow-up, or share feedback.</p></div><span class="pill"><span class="dot"></span>MAYA</span></div>')
                chatbot=gr.Chatbot(height=305,elem_id='conversation',show_label=False,layout='bubble',placeholder='<div style="text-align:center;padding:50px 15px;color:#73877d"><b style="font-size:18px;color:#315e4c">What can we help bring back to life?</b><br><span style="font-size:12px">Tell me about your device, or start with a question below.</span></div>',buttons=['copy'],render=False)
                textbox=gr.Textbox(placeholder='Ask Maya about your device or a service…',show_label=False,container=False,elem_id='composer',submit_btn='Send',render=False)
                activity=gr.HTML(activity_html([]),elem_id='activity',render=False)
                trace=gr.Textbox(label='Recorded application activity',lines=7,interactive=False,render=False)
                gr.ChatInterface(respond,chatbot=chatbot,textbox=textbox,additional_outputs=[activity,trace],examples=['What is the diagnostic fee?','I’d like repair follow-up.','I have feedback to share.'],examples_label='A place to start',run_examples_on_click=False,save_history=False,flagging_mode='never')
                activity.render()
                with gr.Accordion('Behind the reply · router & tools',open=False,elem_id='trace-details'):
                    trace.render()
        gr.HTML(footer('C3 · Business assistant'))
    return demo

if __name__ == '__main__':
    build_app().launch(server_name='127.0.0.1',server_port=int(os.getenv('PORT','7860')),share=False,theme=THEME,css=CSS,head=HEAD,footer_links=[])
