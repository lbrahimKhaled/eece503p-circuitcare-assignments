from html import escape
from pathlib import Path
import gradio as gr

CSS = (Path(__file__).resolve().parent / 'interface.css').read_text()
THEME = gr.themes.Soft(primary_hue='teal', neutral_hue='slate', font=['DM Sans', 'Arial', 'sans-serif'])


def activity_html(trace, route=None):
    """Show public tool activity without exposing contact records or internal prompts."""
    labels = {'general_question':'General question', 'lead_collection':'Repair follow-up', 'feedback_and_unanswered':'Feedback & unanswered'}
    tags = [labels.get(route, route)] if route else []
    for event in trace:
        if event.get('event') == 'tool':
            tags.append(event.get('name', 'tool').replace('_', ' '))
    if not tags:
        tags = ['Ready for your question']
    return '<div class="activity-line"><span class="dot"></span>Latest activity ' + ''.join('<span class="activity-tag">'+escape(str(tag))+'</span>' for tag in dict.fromkeys(tags)) + '</div>'


def inspector_html(trace):
    """Render the application's recorded actions and concise decision summaries."""
    cards=[]
    for event in trace:
        if event.get('event')=='decision':
            note=event.get('decision',{}).get('note')
            if note:
                cards.append(('<strong>Decision '+str(event['step'])+'</strong><span>'+escape(str(note))+'</span>'))
        if event.get('event')=='observation':
            result=event.get('result',{})
            if 'estimated_labour_usd' in result:
                detail='Labour estimate: $'+str(result['estimated_labour_usd'])+' · parts excluded'
            elif 'price_usd' in result:
                detail='Listed price: $'+str(result['price_usd'])
            else:
                detail='Status: '+str(result.get('status','observation returned'))
            cards.append('<strong>'+escape(event.get('tool','tool').replace('_',' '))+'</strong><span>'+escape(detail)+'</span>')
    if not cards:
        return '<div class="small-note">Actions and tool observations will appear here after you send a message.</div>'
    return ''.join('<div class="tool-card">'+card+'</div>' for card in cards)


def footer(assignment):
    return '<div class="page-footer"><span>CircuitCare · Fictional business for EECE 503P · '+assignment+'</span><span>Ibrahim Khaled · 202500327</span></div>'

HEAD = """<style>
body:has(.workbench),.gradio-container:has(.workbench){background:#f2f4fa!important}
@media(max-width:850px){
.gradio-container{width:100%!important;max-width:100%!important;min-width:0!important;box-sizing:border-box!important;padding:0 18px 20px!important}
.main.app{min-width:0!important;width:100%!important}
#main-layout{flex-direction:column!important}
#chat-panel,#service-rail,#inspector{width:100%!important;min-width:0!important;box-sizing:border-box!important}
.hero{gap:12px!important}.hero-title{font-size:35px!important}.hero-art{width:210px!important;height:140px!important}.nav-links .nav-label{display:none!important}.page-footer{flex-direction:column!important}
.toast-wrap{max-width:calc(100vw - 24px)!important;width:auto!important}
}
@media(max-width:540px){.hero-art{display:none!important}.hero-title{font-size:33px!important}.topnav{padding:16px 0!important}.brand{font-size:20px!important}.nav-links{gap:8px!important}.pill{font-size:9px!important;padding:6px 8px!important}.hero-copy{font-size:12px!important}.page-footer{line-height:1.7!important}}
</style>"""
