"""Bounded local observations; no remote lookup or target execution."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
from jsonschema import Draft202012Validator
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture import manifest, SOURCE, RUN

receipt=manifest(SOURCE)
expected=sys.argv[1] if len(sys.argv)>1 else 'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099'
assert receipt['package_digest']==expected
rows=[]; edges=[]; calls=[]; issues=[]
for row in receipt['manifest']:
    path=SOURCE/row['path']; data=path.read_bytes(); text=data.decode('utf-8')
    result={**row,'characters':len(text),'lines':len(text.splitlines())}
    if path.suffix=='.json':
        value=json.loads(text)
        if path.parent.name=='schemas':
            Draft202012Validator.check_schema(value)
            result['schema_meta_check']='PASS'
    if path.suffix=='.py':
        tree=ast.parse(text,filename=row['path']); result['python_parse']='PASS'
        result['functions']=[{'name':node.name,'line':node.lineno} for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.ClassDef))]
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                called=ast.unparse(node.func)
                if any(x in called for x in ('write','read','open','unlink','mkdir','run','exec','load','resolve','copy')):
                    calls.append({'path':row['path'],'line':node.lineno,'call':called})
    if path.suffix=='.md':
        fence=False
        for line_no,line in enumerate(text.splitlines(),1):
            if line.lstrip().startswith('```'): fence=not fence; continue
            if fence: continue
            for target in re.findall(r'\[[^\]]+\]\(([^ )]+)(?:[^)]*)\)',line):
                if '://' in target or target.startswith('#'): continue
                leaf=target.split('#',1)[0]
                destination=(path.parent/leaf).resolve()
                edge={'source':row['path'],'line':line_no,'target':target,'exists':destination.exists(),'inside_package':destination.is_relative_to(SOURCE)}
                edges.append(edge)
                if not edge['exists']: issues.append(edge)
    rows.append(result)
report={'target_digest':receipt['package_digest'],'files':rows,'local_links':edges,'source_to_effect_candidates':calls,'missing_local_links':issues,'limits':{'files':2000,'bytes':33554432},'remote_checks':'NOT_RUN; not required by local contract','semantic_notes':'All selected Markdown routing and Python source read independently; candidate call presence is not a defect verdict.'}
(RUN/('reports/static-observations-final04.json' if len(sys.argv)>1 else 'reports/static-observations.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(rows),'schemas':sum('schema_meta_check' in x for x in rows),'python_files':sum('python_parse' in x for x in rows),'local_links':len(edges),'missing_links':len(issues)}))
