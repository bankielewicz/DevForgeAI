import json, sys
from bootstrap import ROOT, PROJECT, write, inventory
from verification import copy_package, execute, reference

old=ROOT/'self-review/20260912T161000Z'; A=ROOT/'self-review/20260912T161000Z-retry01'
copy_package(old,A)
checks=[json.loads(l) for l in (A/'checks.jsonl').read_text().splitlines()]
for row in checks:
    for ref in row['evidence']:
        if ref['path']=='origin-record.json': ref.update(reference(A/'origin-record.json',A))
(A/'checks.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in checks),encoding='utf-8')
with (A/'validation-report.md').open('a',encoding='utf-8') as f:
    f.write('\nThe first record-integrity attempt rejected a stale citation digest after this author updated origin readback status. That exact failed input and output remain in the preceding directory and commands/self-records. This fresh attempt corrects the evidence reference only; no validator package bytes changed.\n')
handoff=json.loads((A/'handoff.json').read_text()); handoff['report']=reference(A/'validation-report.md',A); write(A/'handoff.json',handoff)
write(ROOT/'self-review/records-retry01-input-before.json',inventory(A))
helper=PROJECT/'src/agents/skills/skill-validator/scripts/observe.py'
code,p=execute('self-records-retry01',[sys.executable,'-B','-X','utf8',helper,'records','--run-root',A]); assert code==0
assert inventory(A)['files']==json.loads((ROOT/'self-review/records-retry01-input-before.json').read_text())['files']
write(ROOT/'self-review/final-receipt.json',{'case_id':'V16','review_kind':'self_review','report':reference(A/'validation-report.md'),'record_integrity_exit':code,'target_readback_unchanged':inventory(PROJECT/'src/agents/skills/skill-validator')['files']==json.loads((A/'source-manifest.json').read_text())['files'],'no_independent_self_verification_claim':True,'retry_reason':'Retained stale evidence digest failure; correction changed only external evidence.'})
print(str(A))
