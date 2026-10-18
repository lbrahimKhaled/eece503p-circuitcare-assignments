import json
import os
from functools import lru_cache
import gradio as gr
from react_agent import ReActAgent, Setup
from model_client import ModelClient
from interface import CSS, THEME, HEAD, inspector_html, footer


def build_app():
    @lru_cache(maxsize=1)
    def shared_client():
        return ModelClient()

    def profile(persona):
        if persona=='friendly':
            return '<div class="person"><div class="avatar">MN</div><div><div class="person-name">Maya · Service advisor</div><div class="person-desc">Intake & practical next steps</div></div></div><div class="persona-description">Warm, approachable, and cost conscious. Helps you explain the issue and request follow-up.<br><br><b>Sampling</b> · temperature 0.7 · top-p 0.95</div>'
        return '<div class="person"><div class="avatar">RH</div><div><div class="person-name">Rami · Technical specialist</div><div class="person-desc">Safe triage & verified estimates</div></div></div><div class="persona-description">Cautious, precise, and evidence focused. Checks tools before giving symptom advice or combined prices.<br><br><b>Sampling</b> · temperature 0.1 · top-p 0.8</div>'

    def respond(message, history, persona):
        try:
            result=ReActAgent(Setup(name=persona+'_interactive',persona=persona),client=shared_client()).reply(message,history)
            return result['reply'], inspector_html(result['trace']), json.dumps(result['trace'],indent=2)
        except RuntimeError:
            return 'This session reached its request, output, or spending limit. Please ask the person running the demo to check the session.', inspector_html([]), 'Request stopped by a runtime limit.'
        except Exception:
            return 'The model connection is unavailable. Check your private settings and try again.', inspector_html([]), 'No request completed.'

    with gr.Blocks(title='CircuitCare | Agent workbench',analytics_enabled=False) as demo:
        with gr.Column(elem_classes='workbench'):
            gr.HTML('<div class="topnav"><div class="brand"><span class="brand-icon">↗</span>CircuitCare<span style="font-weight:400;color:#8c86b6">/ lab</span></div><div class="nav-links"><span class="nav-label">AGENT WORKBENCH</span><span class="pill">C4 · LANGGRAPH</span></div></div>',elem_id='topnav')
            gr.HTML('<section class="hero"><div><div class="eyebrow">The same care. A deeper look.</div><h1 class="hero-title">A specialist for <em>every next step.</em></h1><div class="hero-copy">Switch perspectives. Ask a repair question. See the tools behind the answer.</div><div class="flow"><span>01 · Decide</span><i>→</i><span>02 · Act</span><i>→</i><span>03 · Observe</span><i>↻</i><span>04 · Answer</span></div></div><span class="pill">MANUAL REACT LOOP</span></section>')
            with gr.Row(elem_id='main-layout'):
                with gr.Column(scale=3,min_width=360,elem_id='chat-panel') as chat_panel:
                    gr.HTML('<div class="panel-heading"><div><h2>Your repair, considered carefully.</h2><p>Service estimates, safe triage, and consent-based follow-up.</p></div></div>')
                    chatbot=gr.Chatbot(height=400,elem_id='conversation',show_label=False,layout='bubble',placeholder='<div style="text-align:center;padding:90px 20px;color:#8583a2"><b style="font-size:19px;color:#494374">Start with a question.</b><br><span style="font-size:12px">Your specialist will choose a tool, check its result, and answer.</span></div>',buttons=['copy'],render=False)
                    textbox=gr.Textbox(placeholder='Describe a symptom or ask for an estimate…',show_label=False,container=False,elem_id='composer',submit_btn='Send',render=False)
                with gr.Column(scale=1,min_width=300,elem_id='inspector'):
                    gr.HTML('<div class="rail-title">Choose your perspective</div>')
                    persona=gr.Dropdown(choices=[('Maya - friendly intake','friendly'),('Rami - cautious technical triage','expert')],value='expert',label='Active specialist',elem_id='persona-picker',allow_custom_value=False)
                    persona_profile=gr.HTML(profile('expert'),elem_id='persona-profile')
                    gr.HTML('<div class="rail-title" style="margin-top:18px">Behind the answer</div>')
                    activity=gr.HTML(inspector_html([]),elem_id='activity')
                    with gr.Accordion('Inspect the full trace',open=False,elem_id='trace-details'):
                        trace=gr.Textbox(label='Decision and observation log',lines=9,interactive=False)
                    gr.HTML('<div class="small-note">Switching specialists starts a fresh chat.<br>Tool results and brief decision summaries are shown here. Private model reasoning is never requested.</div>')
            with chat_panel:
                chat=gr.ChatInterface(respond,chatbot=chatbot,textbox=textbox,additional_inputs=[persona],additional_outputs=[activity,trace],examples=[['What is the labour total for a diagnostic and SSD installation?'],['My laptop battery is swollen. What should I do?']],examples_label='Explore a scenario',run_examples_on_click=False,save_history=False,flagging_mode='never')
            persona.change(lambda value:([],[],[],profile(value),inspector_html([]),''),inputs=[persona],outputs=[chat.chatbot,chat.chatbot_state,chat.chatbot_value,persona_profile,activity,trace])
            gr.HTML(footer('C4 · Configurable ReAct agent'))
    return demo

if __name__=='__main__':
    build_app().launch(server_name='127.0.0.1',server_port=int(os.getenv('PORT','7861')),share=False,theme=THEME,css=CSS,head=HEAD,footer_links=[])
