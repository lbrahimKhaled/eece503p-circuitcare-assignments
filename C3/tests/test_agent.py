import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent import BusinessAgent, route_message, record_customer_interest

class ScriptedClient:
    def __init__(self,replies): self.replies=iter(replies)
    def complete(self,*args,**kwargs): return next(self.replies)

def test_router_and_lead_continuation():
    assert route_message('What are your hours?')=='general_question'
    assert route_message('Please contact me')=='lead_collection'
    assert route_message('Your staff were rude')=='feedback_and_unanswered'
    assert route_message('Ibrahim',[{'role':'assistant','content':'What is your name?'}])=='lead_collection'

def test_model_tool_call_round_trip(tmp_path):
    call={'id':'test','type':'function','function':{'name':'record_feedback','arguments':json.dumps({'question':'Do you repair consoles?'})}}
    client=ScriptedClient([{'role':'assistant','tool_calls':[call]},{'role':'assistant','content':'I logged that question for the team.'}])
    result=BusinessAgent(client=client,log_dir=tmp_path).reply('Do you repair consoles?')
    assert result['trace'][1]['name']=='record_feedback'
    assert json.loads((tmp_path/'feedback.jsonl').read_text())['question']=='Do you repair consoles?'
    assert 'logged' in result['reply']

def test_invalid_email_does_not_log(tmp_path):
    assert record_customer_interest('bad','Test','Laptop',tmp_path)['status']=='error'
    assert not list(tmp_path.glob('*.jsonl'))

def test_unknown_tool_and_bad_json_are_rejected(tmp_path):
    agent=BusinessAgent(client=ScriptedClient([]),log_dir=tmp_path)
    assert agent.dispatch({'function':{'name':'execute','arguments':'{}'}})['status']=='error'
    assert agent.dispatch({'function':{'name':'record_feedback','arguments':'broken'}})['status']=='error'

def test_tool_loop_is_bounded(tmp_path):
    call={'id':'test','type':'function','function':{'name':'record_feedback','arguments':'{}'}}
    agent=BusinessAgent(client=ScriptedClient([{'role':'assistant','tool_calls':[call]}]*4),log_dir=tmp_path)
    assert 'tool limit' in agent.reply('Unknown?')['reply']


def test_gradio_history_reaches_model(tmp_path):
    class CapturingClient:
        def complete(self,messages,**kwargs):
            self.messages=messages
            return {'role':'assistant','content':'Please confirm.'}
    client=CapturingClient()
    history=[{'role':'user','content':[{'type':'text','text':'My laptop is slow.'}]},{'role':'assistant','content':[{'type':'text','text':'What is your name?'}]}]
    BusinessAgent(client=client,log_dir=tmp_path).reply('Alex',history)
    assert any(t.get('content')=='My laptop is slow.' for t in client.messages)
