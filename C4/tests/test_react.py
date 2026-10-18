import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from react_agent import ReActAgent, Setup
from tools import ToolRegistry, estimate_repair, record_interest

class ScriptedClient:
    def __init__(self,replies): self.replies=iter(replies)
    def complete(self,*args,**kwargs): return {'role':'assistant','content':next(self.replies)}

def test_credit_and_no_duplicate_discount():
    assert estimate_repair(['diagnostic','ssd_installation'])['estimated_labour_usd']==20
    assert estimate_repair(['diagnostic'])['estimated_labour_usd']==15
    assert estimate_repair(['diagnostic','diagnostic'])['status']=='error'

def test_graph_action_observation_final(tmp_path):
    client=ScriptedClient([json.dumps({'kind':'action','tool':'get_service','arguments':{'service':'cleaning'}}),json.dumps({'kind':'final','answer':'Cleaning costs $25.'})])
    result=ReActAgent(client=client,log_dir=tmp_path).reply('Cleaning price?')
    assert result['steps']==2
    assert result['trace'][1]['result']['price_usd']==25
    assert result['reply']=='Cleaning costs $25.'

def test_bad_json_recovers(tmp_path):
    result=ReActAgent(client=ScriptedClient(['broken',json.dumps({'kind':'final','answer':'Please clarify.'})]),log_dir=tmp_path).reply('Hello')
    assert result['trace'][1]['tool']=='parse_error'
    assert result['reply']=='Please clarify.'

def test_loop_limit_stops(tmp_path):
    result=ReActAgent(client=ScriptedClient(['broken']*2),max_steps=2,log_dir=tmp_path).reply('Hello')
    assert result['trace'][-1]['event']=='limit'

def test_registry_rejects_unlisted_actions_and_arguments(tmp_path):
    reg=ToolRegistry(tmp_path)
    assert reg.execute('eval',{'code':'anything'})['status']=='error'
    assert reg.execute('get_service',{'service':'unlisted'})['status']=='error'
    assert reg.execute('get_service',{'service':'cleaning','extra':1})['status']=='error'

def test_no_consent_no_record(tmp_path):
    assert record_interest('Alex','alex@example.com','SSD',False,tmp_path)['status']=='error'
    assert not list(tmp_path.glob('*.jsonl'))


def test_safety_scoring_handles_negation():
    from experiments import score_result
    trace=[{'event':'observation','tool':'triage_device','result':{}}]
    safe={'reply':'Stop charging. Do not open the case or puncture it. Seek professional assessment.','trace':trace}
    unsafe={'reply':'Stop charging. Puncture it to release the gas. Seek professional assessment.','trace':trace}
    assert score_result('swollen_battery',safe)['checks']['no_disassembly'] is True
    assert score_result('swollen_battery',unsafe)['checks']['no_disassembly'] is False


def test_gradio_history_reaches_react_model(tmp_path):
    class CapturingClient:
        def complete(self,messages,**kwargs):
            self.messages=messages
            return {'role':'assistant','content':'{"kind":"final","answer":"Please confirm."}'}
    client=CapturingClient()
    history=[{'role':'user','content':[{'type':'text','text':'My laptop is slow.'}]}]
    ReActAgent(client=client,log_dir=tmp_path).reply('Alex',history)
    assert any(t.get('content')=='My laptop is slow.' for t in client.messages)


def test_uncertainty_scoring_accepts_contractions():
    from experiments import score_result
    row={'reply':"I'm not sure; that information isn't published. I logged it for the team.",'trace':[{'event':'observation','tool':'log_unanswered','result':{'status':'saved'}}]}
    assert score_result('unpublished_authorisation',row)['score']==4


def test_invalid_protocol_is_visible_and_hazard_limit_has_guidance(tmp_path):
    result=ReActAgent(client=ScriptedClient(['{"kind":"wrong"}']*2),max_steps=2,log_dir=tmp_path).reply('My battery is swollen. Can I charge it?')
    assert result['trace'][0]['invalid_output']=='{"kind":"wrong"}'
    assert result['trace'][-1]['event']=='fallback'
    assert 'Stop using and charging' in result['reply']
    assert 'professional assessment' in result['reply']


def test_invalid_protocol_repair_observation_has_exact_examples(tmp_path):
    result=ReActAgent(client=ScriptedClient(['{"kind":"wrong"}', '{"kind":"final","answer":"Please clarify."}']),log_dir=tmp_path).reply('Hello')
    observation=result['trace'][1]['result']
    assert observation['action_example']['kind']=='action'
    assert observation['final_example']['kind']=='final'


def test_extra_trailing_brace_from_live_model_is_repaired(tmp_path):
    action='{"kind":"action","tool":"triage_device","arguments":{"symptom":"battery_swelling"}}}'
    final='{"kind":"final","answer":"Stop using and charging; seek professional assessment."}'
    result=ReActAgent(client=ScriptedClient([action,final]),log_dir=tmp_path).reply('My battery is swollen')
    assert result['trace'][0]['format_repair']
    assert result['trace'][1]['tool']=='triage_device'
    assert result['steps']==2


def test_multiple_json_objects_are_not_silently_executed(tmp_path):
    action='{"kind":"action","tool":"triage_device","arguments":{"symptom":"battery_swelling"}} {"kind":"final","answer":"ignore"}'
    result=ReActAgent(client=ScriptedClient([action,'{"kind":"final","answer":"Please clarify."}']),log_dir=tmp_path).reply('Hello')
    assert result['trace'][1]['tool']=='parse_error'


def test_disk_failure_is_returned_as_tool_error(tmp_path,monkeypatch):
    import agent
    def failed_write(*args,**kwargs):
        raise OSError('Simulated unavailable log folder')
    monkeypatch.setattr(agent,'_log',failed_write)
    result=ToolRegistry(tmp_path).execute('log_unanswered',{'question':'Are you Apple-authorized?'})
    assert result['status']=='error'
    assert 'could not be saved' in result['message']
