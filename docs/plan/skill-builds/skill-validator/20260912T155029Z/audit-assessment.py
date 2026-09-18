import datetime, json, re
from pathlib import Path
from bootstrap import ROOT, PROJECT, write, digest, inventory
from verification import reference

A=PROJECT/'docs/plan/skill-validations/skill-builder/20260912T161842Z'
receipt=json.loads((A/'final-readback-receipt.json').read_text(encoding='utf-8'))
target=PROJECT/'src/agents/skills/skill-builder'; validator=PROJECT/'src/agents/skills/skill-validator'
before=json.loads((ROOT/'development-builder-before-manifest.json').read_text())
assert inventory(target)['files']==before['files']
assert inventory(validator)['files']==json.loads((ROOT/'destination-manifest.json').read_text())['files']
manifest=json.loads((A/'source-manifest.json').read_text()); assert inventory(target)['files']==manifest['files']
assert inventory(A/'source')['files']==manifest['files']
rows=receipt['retained_files_excluding_this_receipt']
for row in rows:
    p=A/row['path']; assert p.stat().st_size==row['bytes'] and digest(p.read_bytes())==row['sha256']
def check_ref(ref):
    assert digest((A/ref['path']).read_bytes())==ref['sha256']
for key in ['report','proposal','handoff','source_readback','input_readback_receipt','record_integrity']: check_ref(receipt[key])
handoff=json.loads((A/'handoff.json').read_text()); assert handoff['builder_readiness']=='BLOCKED' and handoff['proposal_review_state']=='pending'
for key in ['original_manifest','origin','proposed_spec','findings','report']: check_ref(handoff[key])
findings=json.loads((A/'findings.json').read_text())['findings']; assert len(findings)==1
finding=findings[0]; assert finding['severity']=='minor'
assert finding['finding_id']=='F-'+digest(json.dumps(finding['identity'],ensure_ascii=False,separators=(',',':')).encode())
text=(target/finding['subject_path']).read_text().replace('\r\n','\n').replace('\r','\n')
assert finding['identity'][2] in text
records=json.loads((A/receipt['record_integrity']['path']).read_text()); assert not records['errors'] and records['overall_assessment']=='FAIL'
links=0
for name in ['validation-report.md','revision-spec.md']:
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)',(A/name).read_text()):
        path=match[1]
        if '://' in path: continue
        # Proposed replacement text links evaluation.md relative to the future target reference file.
        if path.startswith('evaluation.md#') and name=='revision-spec.md':
            assert (target/'references/evaluation.md').exists(); continue
        assert (A/path.split('#')[0]).exists(), path
        links+=1
audit={'audited_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assessment_run':str(A),'retained_files_verified':len(rows),'report_and_proposal_links_verified':links,'target_files_unchanged':36,'validator_files_unchanged':15,'finding_identity_verified':finding['finding_id'],'outcome':'FAIL','behavior':'INCOMPLETE','required_coverage':'7/8','builder_readiness':'BLOCKED','proposal_review_state':'pending','report':{'original_path':str(A/'validation-report.md'),'sha256':digest((A/'validation-report.md').read_bytes())},'proposal':{'original_path':str(A/'revision-spec.md'),'sha256':digest((A/'revision-spec.md').read_bytes())},'authority':'NONE','result':'MATCH'}
write(ROOT/'first-assessment-root-audit.json',audit)
write(ROOT/'turn-completion.json',{'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'validator_build':'DEVELOPMENT_BUILD_COMPLETE','build_report':reference(ROOT/'build-report.md'),'build_provenance':reference(ROOT/'build-provenance.json'),'delivery_audit':reference(ROOT/'delivery-audit.json'),'first_assessment_completed':True,'first_assessment_audit':reference(ROOT/'first-assessment-root-audit.json'),'existing_project_skills_and_operational_copies_unchanged':True,'remaining_user_decision':'Review the proposed skill-builder documentation revision; no repair/adoption/install/builder invocation authorized or performed.'})
print(json.dumps({'audit':'MATCH','retained_files':len(rows),'target_unchanged':True,'validator_unchanged':True,'findings':len(findings),'overall':'FAIL','behavior':'INCOMPLETE'}))
