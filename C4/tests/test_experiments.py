import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import experiments
from react_agent import Setup


class OfflineClient:
    provider='offline'
    model='scripted'
    usage=[]


def configure(monkeypatch,tmp_path,agent):
    monkeypatch.setattr(experiments,'ROOT',tmp_path)
    monkeypatch.setattr(experiments,'ModelClient',lambda **kwargs:OfflineClient())
    monkeypatch.setattr(experiments,'ReActAgent',agent)
    monkeypatch.setattr(experiments,'SETUPS',[Setup()])
    monkeypatch.setattr(experiments,'CASES',experiments.CASES[:1])
    evidence=tmp_path/'evidence'
    evidence.mkdir()
    (evidence/'experiments.json').write_text('[{"previous":"complete matrix"}]')
    (evidence/'experiment_scores.csv').write_text('previous,complete matrix\n')
    return evidence


def test_failed_run_preserves_submitted_matrix_and_saves_checkpoint(tmp_path,monkeypatch):
    class FailedAgent:
        def __init__(self,*args,**kwargs): pass
        def reply(self,message): raise RuntimeError('Offline simulated failure')
    evidence=configure(monkeypatch,tmp_path,FailedAgent)
    before={p.name:p.read_bytes() for p in evidence.iterdir()}
    with pytest.raises(RuntimeError,match='Submitted evidence was preserved'):
        experiments.run_experiments()
    assert {p.name:p.read_bytes() for p in evidence.iterdir()}==before
    checkpoints=list((tmp_path/'runtime_logs/experiments').glob('*.json'))
    assert len(checkpoints)==1
    assert json.loads(checkpoints[0].read_text())[0]['error_type']=='RuntimeError'


def test_completed_run_promotes_results_and_records_actual_date(tmp_path,monkeypatch):
    class SuccessfulAgent:
        def __init__(self,*args,**kwargs): pass
        def reply(self,message):
            return {'reply':'Labour is $20 after the diagnostic credit; parts are excluded.','trace':[{'event':'observation','tool':'estimate_repair','result':{'status':'ok'}}]}
    evidence=configure(monkeypatch,tmp_path,SuccessfulAgent)
    rows=experiments.run_experiments()
    assert rows[0]['recorded_date']==datetime.now(timezone.utc).date().isoformat()
    assert rows[0]['score']==4
    assert json.loads((evidence/'experiments.json').read_text())==rows
    assert 'expert_full,labour_estimate,4,4' in (evidence/'experiment_scores.csv').read_text()
