import json, shutil
from bootstrap import ROOT, write, digest

r=ROOT/'routing/attempt-001'; r.mkdir(parents=True,exist_ok=False)
b=(ROOT/'candidate/SKILL.md').read_bytes(); (r/'SKILL.md').write_bytes(b)
prompts=[('R01','Validate the Codex skill at src/agents/skills/ledger.'),('R02','Audit this skill workflow for unreachable steps.'),('R03','Review whether the checklist in this skill is ceremonial.'),('R04','I edited SKILL.md by hand; assess its resources and behavior.'),('R05','Revalidate the skill delivered by the builder.'),('R06','Explain what a Codex skill is.'),('R07','Build a new skill from this approved specification.'),('R08','Fix the application Python parser.'),('R09','Install this skill into my user skill folder.'),('R10','Configure GitHub CI for this repository.'),('R11','Write a product requirements specification for a shopping app.'),('R12','Inspect progressive disclosure in the named development skill before adoption.')]
write(r/'prompts.json',{'schema_version':'1','cases':[{'case_id':i,'request':s} for i,s in prompts]})
write(ROOT/'routing/expected.json',{'cases':[{'case_id':i,'route':'validate' if i in ('R01','R02','R03','R04','R05','R12') else 'outside_scope'} for i,_ in prompts]})
write(r/'inputs-before.json',{'SKILL.md':digest(b),'prompts.json':digest((r/'prompts.json').read_bytes()),'expected_snapshot':{'path':'../expected.json','sha256':digest((ROOT/'routing/expected.json').read_bytes())},'native_invocation':'NOT_RUN','purpose':'Independent description classification; no discovery activation claim'})
print(str(r))
