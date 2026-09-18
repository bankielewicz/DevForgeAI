import datetime as dt
import hashlib
import json
from pathlib import Path
import re
from prepare_validation import ROOT,PROJECT,put,sha
errors=[];links=0;references=0
for name in ['validation-report.md','revision-spec.md','record-integrity.md']:
    text=(ROOT/name).read_text(encoding='utf-8')
    for dest in re.findall(r'\]\(([^)]+)\)',text):
        if dest.startswith(('https://','http://','#')):continue
        p=ROOT/dest.split('#')[0]
        links+=1
        if not p.exists():errors.append(name+': missing '+dest)
for name in ['handoff.json','evaluation-bundle-manifest.json']:
    def walk(v):
        global references
        if isinstance(v,dict):
            if 'path' in v and 'sha256' in v:
                references+=1
                if sha(ROOT/v['path'])!=v['sha256']:errors.append(name+': stale '+v['path'])
            for item in v.values():walk(item)
        elif isinstance(v,list):
            for item in v:walk(item)
    walk(json.loads((ROOT/name).read_bytes()))
manifest=json.loads((ROOT/'source-manifest.json').read_bytes())
for row in manifest['files']:
    if sha(PROJECT/'src/agents/skills/skill-builder'/row['path'])!=row['sha256']:errors.append('Original target changed '+row['path'])
sources=json.loads((ROOT/'sources.json').read_bytes())
for row in sources['sources']:
    if 'original_path' in row and sha(row['original_path'])!=row['sha256']:errors.append('Original input changed '+row['source_id'])
result={'result':'PASS' if not errors else 'FAIL','errors':errors,'local_report_links_checked':links,'packet_bundle_references_checked':references,'original_source_files_unchanged':len(manifest['files']),'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'report_sha256':sha(ROOT/'validation-report.md'),'proposal_sha256':sha(ROOT/'revision-spec.md'),'limitations':'Direct artifact readback, not framework acceptance or the unavailable full-run records inventory.'}
put('delivery-readback.json',result)
print(json.dumps(result))
