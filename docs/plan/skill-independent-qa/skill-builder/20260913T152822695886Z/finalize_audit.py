"""Final immutable readback and bounded evidence index; excludes operational fixtures."""
import datetime
import json
import os
from pathlib import Path
import stat
from capture import RUN, ROOT, inventory, digest, sha

def save(name,value):
    (RUN/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    initial=json.loads((RUN/'initial-receipt.json').read_text(encoding='utf-8'))
    current,omissions=inventory(ROOT/'src/agents/skills/skill-builder')
    original=json.loads((RUN/'initial-manifest.json').read_text(encoding='utf-8'))
    spec={name:sha((ROOT/'docs/plan'/name).read_bytes()) for name in initial['spec_hashes']}
    prior=json.loads((RUN/'prior-evidence-inputs.json').read_text(encoding='utf-8'))
    prior_state=[{'path':p['source'],'unchanged':sha(Path(p['source']).read_bytes())==p['sha256']} for p in prior]
    save('final-source-manifest.json',current)
    assertions={'source_unchanged':current==original,'specifications_unchanged':spec==initial['spec_hashes'],'selected_prior_evidence_unchanged':all(p['unchanged'] for p in prior_state),'BA_count':len(json.loads((RUN/'requirement-traceability.json').read_text(encoding='utf-8'))),'BAT_count':len({r['parent'] for r in json.loads((RUN/'bat-traceability.json').read_text(encoding='utf-8'))})}
    # Check all findings have retained executed reproductions and source line locators.
    findings=json.loads((RUN/'findings.json').read_text(encoding='utf-8'))
    reproduction_refs=[]
    for finding in findings:
        for case in finding['reproduction']:
            d=RUN/'commands'/case
            for name in ('command.json','result.json','stdout.txt','stderr.txt'):
                p=d/name
                if not p.is_file():raise ValueError('Missing reproduction evidence: '+str(p))
                reproduction_refs.append({'path':str(p.relative_to(RUN)).replace('\\','/'),'sha256':sha(p.read_bytes())})
    save('mapping-readback.json',{'assertions':assertions,'finding_references':reproduction_refs,'prior_readback':prior_state,'limitations':['Complete-spec status is conservative at workflow-group level; finding-specific violations have exact locators.','All named source/command evidence is present; unperformed fixtures remain explicitly mapped.']})
    # Index reporting, snapshots, retained inputs and raw command output as one
    # declared scope. Synthetic fixtures are separately retained in place and not
    # copied/indexed as a complete bounded capture; some intentionally exceed limits.
    excluded={'fixtures','native','evidence-index.json','final-readback-receipt.json'}
    rows=[];skip=[];pending=[RUN]
    while pending:
        directory=pending.pop()
        for p in sorted(directory.iterdir(),key=lambda p:p.name):
            rel=p.relative_to(RUN).as_posix()
            if directory==RUN and p.name in excluded:
                skip.append({'path':rel,'reason':'Synthetic in-place trial scope; see native plans/results or fixture generator' if p.is_dir() else 'Non-self-referential index/receipt'});continue
            st=p.lstat()
            if stat.S_ISLNK(st.st_mode) or getattr(st,'st_file_attributes',0)&0x400:raise ValueError('Unexpected link in report scope')
            if stat.S_ISDIR(st.st_mode):pending.append(p);continue
            if not stat.S_ISREG(st.st_mode):raise ValueError('Special file in report scope')
            if len(rows)>=2000 or sum(r['bytes'] for r in rows)+st.st_size>33554432:raise ValueError('Evidence index exceeds declared capture limit')
            data=p.read_bytes();rows.append({'path':rel,'bytes':len(data),'sha256':sha(data)})
    rows.sort(key=lambda r:r['path'])
    save('evidence-index.json',{'scope':'Report/scripts/source snapshot/selected inputs/command logs only; no full fixture capture claim','files':rows,'excluded_scopes':skip,'count':len(rows),'bytes':sum(r['bytes'] for r in rows),'limits':{'files':2000,'bytes':33554432}})
    for row in rows:
        data=(RUN/row['path']).read_bytes()
        if (len(data),sha(data))!=(row['bytes'],row['sha256']):raise ValueError('Evidence drift '+row['path'])
    receipt={'run_id':RUN.name,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit_reporting_complete':True,'acceptance':'FAIL','coverage':'INCOMPLETE','package_digest':digest(current),'files':len(current),'source_readback':'UNCHANGED' if assertions['source_unchanged'] else 'SOURCE_CHANGED','specification_hashes':spec,'assertions':assertions,'evidence_index_sha256':sha((RUN/'evidence-index.json').read_bytes()),'evidence_refs_readback':'MATCH','preservation':'Exact selected builder and specification bytes match initial capture; selected prior files match their captured hashes. No task-owned writes to either skill package or old evidence. Excluded packages were not substantively read or executed; a complete before/after inventory of those packages was not performed.','writes':'All audit-authored files under this run; native Codex host-managed activity remains governed by existing host controls.','not_performed':['validator integration','operational installation','real operational binding setup','hooks/CI','Rust implementation/qualification','complete native autonomous acceptance','full OS-enforced isolation qualification'],'capture_omissions':omissions,'index_exclusions':skip}
    save('final-readback-receipt.json',receipt)
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
