"""Read the historical Flash/Pro comparison without making paid calls."""
import json
from pathlib import Path

def saved_comparison():
    """Return the earlier model comparison with its original prompts and settings."""
    return json.loads((Path(__file__).resolve().parent/'evidence/model_comparison.json').read_text())

if __name__=='__main__':
    report=saved_comparison()
    for label in ['baseline','candidate']:
        row=report[label]
        print(row['model'],str(row['score'])+'/4 (historical)')
    print(report['limitation'])
