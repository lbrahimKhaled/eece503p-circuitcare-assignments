"""Check submission structure and C3-to-C4 inheritance without API calls."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def verify():
    checks={}
    def check(label,condition):
        checks[label]=bool(condition)
    c3=ROOT/'C3';c4=ROOT/'C4'
    required=['me/about_business.pdf','me/business_summary.txt','me/summary.txt','business_agent.ipynb','app.py','requirements.txt','.env.example','.gitignore']
    for folder in [c3,c4]:
        for path in required:
            check(folder.name+' structure: '+path,(folder/path).is_file())
        check(folder.name+' credentials excluded','.env' in (folder/'.gitignore').read_text().splitlines())
    for path in ['agent.py','history.py','model_client.py','me/about_business.pdf','me/business_summary.txt','me/summary.txt']:
        a=c3/path;b=c4/path
        check('Unchanged C3 foundation: '+path,a.is_file() and b.is_file() and hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest())
    c3source=(c3/'agent.py').read_text();c4source=(c4/'react_agent.py').read_text();tools=(c4/'tools.py').read_text()
    functions={node.name for node in ast.walk(ast.parse(c3source)) if isinstance(node,ast.FunctionDef)}
    check('C3 required tool names',{'record_customer_interest','record_feedback'}<=functions)
    check('C3 separate persona/instructions','PERSONA =' in c3source and 'INSTRUCTIONS =' in c3source)
    check('C3 both business-source formats','PdfReader(' in c3source and 'business_summary.txt' in c3source)
    check('C3 native tool-result loop',"'tool_call_id'" in c3source and 'self.dispatch(call,' in c3source)
    check('C3 required demo video',(c3/'demo.mp4').is_file() and (c3/'demo.mp4').stat().st_size>0)
    imported={name.name for node in ast.walk(ast.parse(c4source)) if isinstance(node,ast.ImportFrom) and node.module=='agent' for name in node.names}
    check('C4 reuses C3 source loader and router',{'load_business_context','route_message'}<=imported)
    imported_tools={name.name for node in ast.walk(ast.parse(tools)) if isinstance(node,ast.ImportFrom) and node.module=='agent' for name in node.names}
    check('C4 reuses both C3 tool functions',{'record_customer_interest','record_feedback'}<=imported_tools)
    check('C4 manual LangGraph loop','from langgraph.graph import StateGraph' in c4source and "graph.add_node('reason',self.reason)" in c4source and "graph.add_edge('act','reason')" in c4source)
    check('C4 no prebuilt executor',not any(token in c4source for token in ['AgentExecutor','create_react_agent','ToolNode']))
    check('C4 retained notebook filename',(c4/'business_agent.ipynb').read_bytes()==(c4/'react_agent.ipynb').read_bytes())
    for folder,name in [(c3,'business_agent.ipynb'),(c4,'business_agent.ipynb')]:
        notebook=json.loads((folder/name).read_text());cells=[cell for cell in notebook['cells'] if cell['cell_type']=='code']
        check(folder.name+' executed notebook',bool(cells) and all(cell.get('execution_count') is not None for cell in cells) and not any(output['output_type']=='error' for cell in cells for output in cell.get('outputs',[])))
        check(folder.name+' Gradio ChatInterface','gr.ChatInterface(' in (folder/'app.py').read_text())
        sources={''.join(cell['source']).strip() for cell in cells}
        modules=['model_client.py','history.py','agent.py','app.py']
        if folder==c4:
            modules+=['tools.py','react_agent.py','experiments.py']
        for module in modules:
            source=(folder/module).read_text()
            if module=='model_client.py':
                source=source.replace('ROOT = Path(__file__).resolve().parent','ROOT = PROJECT')
            if module in {'app.py','experiments.py'}:
                source=source.split('\nif __name__')[0]
            check(folder.name+' notebook matches '+module,source.strip() in sources)
    rows=json.loads((c4/'evidence/experiments.json').read_text())
    configurations={r['setup']['name'] for r in rows}
    check('C4 complete matrix',len(rows)==21 and len(configurations)==7 and len({r['case']['id'] for r in rows})==3 and not any(r.get('error_type') for r in rows))
    check('C4 two tested personas',{'friendly','expert'}<={r['setup']['persona'] for r in rows})
    check('C4 reasoning-summary/direct contrast',{True,False}=={r['setup']['planning'] for r in rows})
    check('C4 zero-shot/few-shot contrast',{True,False}=={r['setup']['few_shot'] for r in rows})
    check('C4 system/in-message contrast',{'system','user'}=={r['setup']['instruction_role'] for r in rows})
    check('C4 matching LLM configuration contrast','expert_warm_config' in configurations and 'expert_full' in configurations)
    check('C4 dedicated instructions, example, reflection','INSTRUCTIONS =' in c4source and 'Worked example:' in c4source and (c4/'reflection.md').is_file())
    demonstration=json.loads((c4/'evidence/c3_extension_live.json').read_text())
    check('C4 inherited workflows live-tested',{'published_service','lead','feedback','unknown'}<={r['case'] for r in demonstration})
    return checks


if __name__=='__main__':
    results=verify()
    for label,passed in results.items():
        print(('PASS' if passed else 'FAIL')+' · '+label)
    print(str(sum(results.values()))+'/'+str(len(results))+' structural and evidence checks passed. This is not an instructor grade.')
    raise SystemExit(0 if all(results.values()) else 1)
