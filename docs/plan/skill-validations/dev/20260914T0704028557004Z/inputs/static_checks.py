"""Retain independent native-Windows deterministic observations."""
import continue_evaluation as c
import json
import sys
from pathlib import Path
r=c.RUN
checker=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
c.copy_file(checker,r/'inputs/checker/quick_validate.py')
for name,args in [
    ('structure',[str(c.LOADED/'scripts/observe.py'),'structure','--source',str(r/'source')]),
    ('installed-skill-creator',[str(checker),str(r/'source')]),
    ('package',[str(c.LOADED/'scripts/adaptive_observe.py'),'package','--source',str(r/'source'),'--tokenizer','tiktoken','--encoding','cl100k_base']),
]:
    c.h.execute(name,[sys.executable,'-B','-X','utf8',*args])
originals=[]
for row in c.load(r/'inputs/prior-inputs/input-index.json'):
    path=Path(row['original_path'])
    digest=c.h.sha(path.read_bytes())
    originals.append({'original_path':str(path),'expected':row['snapshot']['sha256'],'actual':digest,'matches':digest==row['snapshot']['sha256']})
assert all(x['matches'] for x in originals)
c.save(r/'inputs/current-input-readback.json',originals)
c.save(r/'inputs/rule-pin.json',{'path':str(r/'rule-set.json'),'sha256':c.h.sha((r/'rule-set.json').read_bytes()),
 'official_refresh':{'path':str(r/'inputs/official-build-skills.md'),'sha256':c.h.sha((r/'inputs/official-build-skills.md').read_bytes()),
 'url':'https://learn.chatgpt.com/docs/build-skills','retrieved_at_utc':c.h.now(),'transport':'OpenAI Docs search then fetch'},
 'freshness':'Existing frozen rules retained; refreshed official guidance corroborates metadata, disclosure, optional resources and triggering boundaries.'})
print('STATIC_COMMANDS_COMPLETE')

