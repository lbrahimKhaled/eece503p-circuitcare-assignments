import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import agent as c3_base
from react_agent import ReActAgent
from tools import ToolRegistry

class CaptureClient:
    def complete(self,messages,**settings):
        self.messages=messages
        return {'role':'assistant','content':'{"kind":"final","answer":"Please provide your email and permission to save your details."}'}


def test_extended_graph_receives_both_original_business_sources(tmp_path):
    client=CaptureClient()
    ReActAgent(client=client,log_dir=tmp_path).reply('What services do you offer?')
    prompt=client.messages[0]['content']
    assert 'BUSINESS SUMMARY\n' in prompt
    assert 'BUSINESS PDF\n' in prompt
    assert (c3_base.ROOT/'me/about_business.pdf').is_file()
    assert (c3_base.ROOT/'me/summary.txt').read_bytes()==(c3_base.ROOT/'me/business_summary.txt').read_bytes()


def test_c3_router_still_classifies_before_react_decisions(tmp_path):
    client=CaptureClient()
    result=ReActAgent(client=client,log_dir=tmp_path).reply('Please contact me about a repair.')
    assert result['route']=='lead_collection'
    assert 'C3 ROUTE: lead_collection' in client.messages[0]['content']


def test_extended_lead_tool_preserves_c3_record_contract(tmp_path):
    result=ToolRegistry(tmp_path).execute('record_interest',{'name':'Alex Demo','email':'alex@example.com','issue':'Slow laptop','consent':True})
    assert result['status']=='saved'
    saved=json.loads((tmp_path/'leads.jsonl').read_text())
    assert saved['id']==result['id']
    assert saved['name']=='Alex Demo' and saved['email']=='alex@example.com'
    assert saved['message']=='Slow laptop'


def test_extended_feedback_tool_uses_original_feedback_logging(tmp_path):
    question='Feedback: please explain updates more clearly.'
    result=ToolRegistry(tmp_path).execute('log_unanswered',{'question':question})
    assert result['status']=='saved'
    saved=json.loads((tmp_path/'feedback.jsonl').read_text())
    assert saved['question']==question and saved['id']==result['id']
