"""Audit-owned full text/schema inventory, local links and historical byte comparison."""
import ast
import json
from pathlib import Path
import re
from capture import RUN, ROOT, inventory, digest, sha

def save(name,value):
    (RUN/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    source=ROOT/'src/agents/skills/skill-builder'; manifest,omissions=inventory(source)
    records=[];links=[];schema_rows=[]
    for row in manifest:
        path=source/row['path'];data=path.read_bytes();text=data.decode('utf-8')
        records.append(dict(row,characters=len(text),lines=len(text.splitlines()),utf8=True,role='legacy schema' if path.name in ('adoption-evidence.schema.json','evidence.schema.json','build-artifacts.schema.json') else 'runtime template' if 'adaptive-runtime' in row['path'] else path.parent.name))
        if path.suffix=='.py':ast.parse(text,filename=str(path))
        if path.suffix=='.json':
            value=json.loads(text)
            def walk(v,loc='$'):
                if isinstance(v,dict):
                    if 'type' in v or 'const' in v or 'enum' in v or '$ref' in v:
                        schema_rows.append({'file':row['path'],'pointer':loc,'definition':{k:v[k] for k in ('type','const','enum','$ref','required','additionalProperties','minimum','minLength','maxLength','minItems','uniqueItems','pattern') if k in v}})
                    for k,x in v.items():walk(x,loc+'/'+k)
                elif isinstance(v,list):
                    for n,x in enumerate(v):walk(x,loc+'/'+str(n))
            if 'schemas/' in row['path']:walk(value)
        if path.suffix=='.md':
            for lineno,line in enumerate(text.splitlines(),1):
                for target in re.findall(r'\]\(([^)]+)\)',line):
                    if '://' in target:continue
                    raw=target.split('#')[0]
                    resolved=(path.parent/raw).resolve()
                    links.append({'source':row['path'],'line':lineno,'target':target,'exists':resolved.exists(),'in_package':resolved.is_relative_to(source),'anchor_review':'not needed' if '#' not in target else 'manual'})
    own=json.loads((source/'package-manifest.json').read_text(encoding='utf-8'))['artifacts']
    expected={r['path']:r['sha256'] for r in manifest if r['path']!='package-manifest.json'}
    old=ROOT/'docs/plan/skill-adaptive-implementations/skill-builder/20260913T083452607505Z'
    oldrows,oldomit=inventory(old/'before/builder')
    oldmap={r['path']:r for r in oldrows};newmap={r['path']:r for r in manifest}
    comparison={'before_digest':digest(oldrows),'before_count':len(oldrows),'unchanged':[p for p in oldmap if p in newmap and oldmap[p]==newmap[p]],'changed':[p for p in oldmap if p in newmap and oldmap[p]!=newmap[p]],'removed':sorted(set(oldmap)-set(newmap)),'added':sorted(set(newmap)-set(oldmap)),'omissions':oldomit}
    prior_selected=[old/'FINAL-RECEIPT.json',old/'independent-review.md',old/'semantic-review.md',old/'test_adaptive.py',old/'builder-before.json',ROOT/'docs/plan/skill-set-validations/20260913T135752395202Z/compatibility-report.md',ROOT/'docs/plan/skill-set-validations/20260913T135752395202Z/native-observation.md']
    prior=[]
    for i,p in enumerate(prior_selected):
        data=p.read_bytes();dest=RUN/'prior-inputs'/f'{i:02d}-{p.name}';dest.parent.mkdir(exist_ok=True);dest.write_bytes(data);prior.append({'source':str(p),'snapshot':str(dest.relative_to(RUN)),'bytes':len(data),'sha256':sha(data)})
    save('source-text-inventory.json',records);save('schema-review-inventory.json',schema_rows);save('resource-links.json',links);save('legacy-byte-comparison.json',comparison);save('prior-evidence-inputs.json',prior)
    save('static-summary.json',{'files_read':len(records),'python_ast_parse':'PASS','json_parse':'PASS','package_manifest_exact':own==expected,'broken_local_links':[l for l in links if not l['exists']],'source_digest':digest(manifest),'omissions':omissions})
    print(json.dumps({'static_files':len(records),'broken_links':[l for l in links if not l['exists']],'manifest_exact':own==expected,'legacy_comparison':comparison},indent=2))

if __name__=='__main__':main()
