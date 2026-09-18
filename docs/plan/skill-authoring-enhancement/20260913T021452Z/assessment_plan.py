from pathlib import Path
import hashlib
import json
RUN = Path(__file__).resolve().parent
OUT = RUN / 'assessment-plans'
OUT.mkdir()
requirements = {
'AC-01':('workflow','Conversational request captured before generation; no prerequisite approved specification'),
'AC-02':('instructions','Consequential ambiguity elicits focused questions; discoverable facts reused'),
'AC-03':('workflow','Resolved project recommendation and selected portable directory including spaces'),
'AC-04':('behavior','Occupied initializer refuses without overwrite or silent identity change'),
'AC-05':('behavior','Observed first edit captures before and preserves unrelated paths/metadata'),
'AC-06':('behavior','Later untested authoring baseline permits authorized revision with no quality carryover'),
'AC-07':('behavior','Ownership conflicts, input drift and interrupted writes retain conflicts/partial evidence'),
'AC-08':('behavior','UI edits preserve unrelated fields/policy; explicit-only changes require request'),
'AC-09':('instructions','Proportionate resources/instructions and preserved contracts'),
'AC-10':('workflow','Builder trace has no checker, grader, tests, sample execution or validator invocation'),
'AC-11':('behavior','Manual exact-byte packet accepted by validator; stale packet rejected; validator executes tests'),
'AC-12':('workflow','Legacy schema meanings, valid origins and historical bytes preserved'),
'AC-13':('workflow','Authoring does not depend on available validator and returns usable NOT_PERFORMED handoff'),
'AC-14':('instructions','Structural, deterministic, routing, native, behavioral and self-review coverage separately reported')}
for name in ('skill-builder','skill-validator'):
    rules = []
    for ident,(dimension,expected) in requirements.items():
        applicable = name=='skill-builder' or ident in ('AC-07','AC-11','AC-12','AC-14')
        rules.append({'rule_id':ident,'revision':'1','title':expected,'authority_class':'project_policy','applicability':'applicable' if applicable else 'not_applicable','method':'behavioral' if dimension=='behavior' else 'semantic','expected_observation':expected,'required':applicable,'dimension':dimension,'limitation':'Bounded implementation observations; no native activation, installation or Rust authority.'})
    rules.append({'rule_id':'FORMAT','revision':'2026-09-13','title':'Applicable SKILL.md metadata and resource structure','authority_class':'format_requirement','applicability':'applicable','method':'deterministic','expected_observation':'Operational structure and actual installed Skill Creator checker report no required mismatches','required':True,'dimension':'standards','limitation':'Checker and selected source coverage only; named format disagreements remain separate.'})
    p=OUT/(name+'.json')
    p.write_text(json.dumps({'schema_version':'1','target_name':name,'specification_sha256':'43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14','rules':rules,'planning_note':'Pinned before final delivery assessment; preceding preliminary runs retained independently.'},indent=2))
print('Pinned final assessment applicability and expected outcomes.')
