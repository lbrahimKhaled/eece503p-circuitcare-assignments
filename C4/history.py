def normalize_history(history, limit=12):
    """Convert plain and Gradio content-block messages to text-only model history."""
    turns=[]
    for turn in history:
        if turn.get('role') not in {'user','assistant'}:
            continue
        content=turn.get('content','')
        if isinstance(content,list):
            content='\n'.join(block.get('text','') for block in content if isinstance(block,dict) and block.get('type')=='text')
        if isinstance(content,str) and content.strip():
            turns.append({'role':turn['role'],'content':content})
    return turns[-limit:]
