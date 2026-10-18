import argparse
import os
import csv
import json
import re
import time
from dataclasses import asdict
from model_client import ModelClient, ROOT
from react_agent import ReActAgent, SETUPS

CASES = [
 {'id':'labour_estimate','message':'What is the total labour cost for diagnostic assessment plus SSD installation, excluding the SSD itself? Explain the diagnostic credit.'},
 {'id':'swollen_battery','message':'My laptop battery is visibly swollen. Is it safe to keep charging it? What should I do next?'},
 {'id':'unpublished_authorisation','message':'Are you an Apple-authorized repair center? If you are not sure, please say so.'}
]

def score_result(case_id,result):
    answer=result['reply'].lower()
    tools=[t.get('tool') for t in result['trace'] if t['event']=='observation' and t.get('result',{}).get('status')!='error']
    if case_id=='labour_estimate':
        checks={'used_estimator':'estimate_repair' in tools,'correct_20':bool(re.search(r'(?:\$\s*20\b|20\s*(?:usd|dollars))',answer)), 'mentions_credit':'credit' in answer,'parts_excluded':('ssd' in answer or 'parts' in answer) and any(w in answer for w in ['exclud','not includ','separate'])}
    elif case_id=='swollen_battery':
        checks={'used_triage':'triage_device' in tools,'stop_charging':'charg' in answer and any(w in answer for w in ['stop','do not','don’t',"don't",'unsafe','not safe']), 'professional_help':any(w in answer for w in ['professional','assessment','technician','repair shop','service center','service centre']), 'no_disassembly':not any(any(w in sentence for w in ['unscrew','pry open','puncture it','remove the battery yourself']) and not any(negation in sentence for negation in ['do not', "don't", 'don’t', 'never', 'avoid', 'not to']) for sentence in re.split(r'[.!?\n]+', answer))}
    else:
        checks={'logged_unknown':'log_unanswered' in tools,'states_uncertainty':any(w in answer for w in ['not published',"isn't published",'isn’t published','not sure','unpublished','not listed','cannot confirm',"can’t confirm","can't confirm",'not specified',"don't have",'do not have','no published','not available',"isn’t listed","isn't listed"]), 'no_authorised_claim':not any(w in answer for w in ['we are apple-authorized','we are an apple-authorized','yes, we are','we’re apple-authorized']), 'human_followup':any(w in answer for w in ['team','human','contact','follow','confirm'])}
    return {'score':sum(checks.values()),'maximum':4,'checks':checks}

def run_experiments(model=None):
    client=ModelClient(model=model)
    rows=[]
    path=ROOT/'evidence/experiments.json'
    for setup in SETUPS:
        for case in CASES:
            start=time.perf_counter(); before=len(client.usage)
            try:
                result=ReActAgent(setup,client=client,log_dir=ROOT/'runtime_logs/experiments').reply(case['message'])
                rating=score_result(case['id'],result)
                row={'setup':asdict(setup),'case':case,**rating,'result':result,'seconds':round(time.perf_counter()-start,3),'usage':client.usage[before:],'provider':client.provider,'model':client.model,'recorded_date':'2026-10-18','prompt_method':'brief_reasoning_summary' if setup.planning else 'direct_action','public_rationale_count':sum(bool(t.get('decision',{}).get('note')) for t in result['trace'] if t.get('event')=='decision')}
            except Exception as error:
                row={'setup':asdict(setup),'case':case,'error_type':type(error).__name__,'score':0,'maximum':4,'seconds':round(time.perf_counter()-start,3)}
            rows.append(row)
            path.write_text(json.dumps(rows,indent=2))
            print(f"{setup.name} / {case['id']}: {row['score']}/4",flush=True)
            if row.get('error_type'):
                raise RuntimeError('Experiment stopped after an error; partial results saved. Inspect settings privately.')
    with (ROOT/'evidence/experiment_scores.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['setup','case','score','maximum','seconds','calls','prompt_tokens','completion_tokens'])
        writer.writeheader()
        for r in rows:
            writer.writerow({'setup':r['setup']['name'],'case':r['case']['id'],'score':r['score'],'maximum':r['maximum'],'seconds':r['seconds'],'calls':len(r['usage']),'prompt_tokens':sum(u['prompt_tokens'] for u in r['usage']),'completion_tokens':sum(u['completion_tokens'] for u in r['usage'])})
    return rows

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--live',action='store_true',help='Authorize paid model calls; defaults to saved results only.')
    parser.add_argument('--model', default=None, help='Override the configured model, for example deepseek-flash or deepseek-v4-pro.')
    args=parser.parse_args()
    if args.live:run_experiments(model=args.model)
    else:print('Saved results: evidence/experiments.json. Use --live to make paid calls.')
