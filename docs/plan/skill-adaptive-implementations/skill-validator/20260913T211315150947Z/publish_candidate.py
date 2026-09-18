"""Refresh exact evaluation bindings and capture a reviewable candidate."""
import difflib
import json
from harness import RUN, ROOT, TARGET, read, write, save, ref, inventory, sha, now

manifest=TARGET/'evals/build-manifest.json'
before=json.loads(read(RUN/'source-manifest.json'))
selected={'scripts/adaptive_observe.py','scripts/text_resources.py','tests/test_confirmed_findings.py','evals/build-manifest.json'}
current=inventory(TARGET)
old={r['path']:r for r in before['files']}
new={r['path']:r for r in current['files']}
changed={p for p in old.keys()|new.keys() if old.get(p)!=new.get(p)}
assert changed<=selected and not old.keys()-new.keys()
value=json.loads(read(manifest))
write(RUN/'inputs/build-manifest-before-refresh.json',read(manifest))
value['artifacts']={r['path']:r['sha256'] for r in current['files'] if r['path']!='evals/build-manifest.json'}
manifest.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
after=inventory(TARGET)
save(RUN/'candidate-manifest.json',after)
patch=[]
for r in after['files']:
    write(RUN/'candidate'/r['path'],read(TARGET/r['path']))
    if old.get(r['path'])!=r:
        original=read(RUN/'source'/r['path']).decode().splitlines(keepends=True) if r['path'] in old else []
        patch.extend(difflib.unified_diff(original,read(TARGET/r['path']).decode().splitlines(keepends=True),fromfile='before/'+r['path'],tofile='after/'+r['path']))
write(RUN/'candidate.patch',''.join(patch))
save(RUN/'candidate-delta.json',{'changed':[p for p in sorted(old.keys()|{r['path'] for r in after['files']}) if old.get(p)!=next((r for r in after['files'] if r['path']==p),None)],'removed':[],'before_digest':before['package_digest'],'after_digest':after['package_digest'],'manifest_binding':ref(manifest),'refactor':'Removed unused test import; no unrelated production refactor needed.','time':now()})
print(after['package_digest'],len(after['files']))
