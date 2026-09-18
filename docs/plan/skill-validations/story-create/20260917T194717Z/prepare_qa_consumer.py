"""Prepare a cold QA consumer only after the unchanged real producer qualifies."""
import json
from pathlib import Path
import sys
from prepare_continuation import RUN,PROJECT,put,ref,copy_file,plan
sys.path.insert(0,str(PROJECT/'.agents/skills/skill-validator/scripts'))
import observe

producer=RUN/'trials/N12'
attempt=producer/'attempt-002'
result=json.loads((attempt/'result.json').read_bytes())
assert result['outcome']=='PASS' and result['input_unchanged'] and result['cleanup']=='VERIFIED'
review=(producer/'semantic-review.md').read_text(encoding='utf-8')
assert 'Result: **PASS**' in review
case=RUN/'trials/N13';project=case/'project'
paths=['AGENTS.md','input/request.md','docs/cli-contract.md','backlog/STORY-010.story.md','docs/restore-guide.md']
handoff=[]
for relative in paths:
    source=producer/'project'/relative;dest=project/relative
    copy_file(source,dest)
    handoff.append({'producer':ref(source),'consumer':ref(dest)})
files,excluded=observe.inventory(PROJECT/'.agents/skills/qa')
assert not excluded
for relative,source,info in files:copy_file(source,project/'.agents/skills/qa'/relative)
(project/'.trial-output').mkdir()
prompt=f'Use the qa skill at {(project/".agents/skills/qa/SKILL.md").as_posix()}. Selected project: {project.as_posix()}. Independently assess docs/restore-guide.md against backlog/STORY-010.story.md, input/request.md and docs/cli-contract.md. This is the separately selected product-documentation QA request; it authorizes evidence/qa/ writes and supersedes the fixture\'s prior authoring-only task scope. Save the final QA report at evidence/qa/qa-report.md, with supporting evidence under evidence/qa/. Preserve every supplied source, story, candidate and skill byte. Do not repair the guide or execute the documented fictional product command. Work only in this disposable project, with no installs, network, other checkout access or additional agents.\n'
plan(project,'N13',prompt,['SC-016'],[{'path':'.trial-output/final.txt','kind':'exists','requirement_id':'SC-016'},{'path':'evidence/qa/qa-report.md','kind':'exists','requirement_id':'SC-016'}],dependencies={'N12':str(attempt)})
put(case/'expected.json',{'case_id':'N13','producer_receipt':ref(attempt/'result.json'),'producer_adjudication':ref(producer/'semantic-review.md'),'source_handoff':handoff,'oracle':{'unchanged_actual_producer_consumed':True,'all_AC1_through_AC5_accounted':True,'actual_candidate_review_with_evidence':True,'documentation_runtime_nonapplicability':True,'no_repair_or_product_execution':True,'report_at_selected_path':True,'truthful_verdict':'Assess actual selected documentation against source requirements; producer claims alone are insufficient.'},'consumer_operational_snapshot':{'root':str(PROJECT/'.agents/skills/qa'),'files':[ref(source) for relative,source,info in files]}})
print(json.dumps({'prepared':'N13','producer_files':len(paths),'qa_package_files':len(files),'timeout_seconds':1800}))
