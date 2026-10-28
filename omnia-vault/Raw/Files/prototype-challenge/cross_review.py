from pathlib import Path
import random, json
from run_council import run, pack, local

seat_names=['skeptic','rebuilder','maximalist','outsider','operator']
available=[(n,(local/(n+'.txt')).read_text(encoding='utf-8')) for n in seat_names if (local/(n+'.txt')).exists() and (local/(n+'.txt')).stat().st_size]
random.SystemRandom().shuffle(available)
mapping={chr(65+i): n for i,(n,_) in enumerate(available)}
(local/'opinion-mapping.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8')
blind='\n\n'.join('Opinion '+chr(65+i)+'\n'+text for i,(_,text) in enumerate(available))
prompt='''You are a fresh blind council reviewer, not a seat. No tools, file access, writes or delegation. The opinions below are shuffled and stripped of author/model identity. Use the neutral context and then answer exactly three questions in 300-450 words total: 1. Strongest opinion and why (pick one letter). 2. Biggest blind spot in any single opinion. 3. What all available opinions missed. Do not infer absent perspectives or invent medical evidence.\n\n'''+pack+'\n\n'+blind
(local/'review-prompt.md').write_text(prompt,encoding='utf-8')
if __name__=='__main__':
    import sys
    bench=sys.argv[1] if len(sys.argv)>1 else 'codex'
    run('review-'+bench,bench,prompt)
