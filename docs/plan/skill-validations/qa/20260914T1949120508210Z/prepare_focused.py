"""Prepare distinct planning and integrity trials; no failed-case retry."""
from bootstrap import ROOT, observe, write
from prepare_trials import put, ref
import json
import shutil

base=ROOT/'trials/QPV-01/project'
for cid in ['QPV-02','QPV-06']:
    case=ROOT/'trials'/cid
    project=case/'project'
    project.mkdir(parents=True)
    for name in ['inc.py','test_inc.py','README.md','AGENTS.md','docs/spec.md']:
        dest=project/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((base/name).read_bytes())
    shutil.copytree(ROOT/'source',project/'.agents/skills/qa')
    (project/'.trial-output').mkdir()
    if cid=='QPV-06':
        put(project/'test_inc.py',"import unittest\nfrom unittest.mock import patch\nfrom unittest.mock import patch as replace_for_test\nfrom pathlib import Path\nfrom inc import inc\n\nclass IncrementTests(unittest.TestCase):\n    @patch('inc.inc', return_value=1)\n    def test_direct(self, replacement):\n        Path('launched-direct').write_text('launched')\n        self.assertEqual(inc(0),1)\n    @replace_for_test('inc.inc', return_value=0)\n    def test_alias(self, replacement):\n        Path('launched-alias').write_text('launched')\n        self.assertEqual(inc(-1),0)\n")
        extra='Perform independent product QA.'
        expected=['Direct and aliased mock decorators confirmed as INTEGRITY_FAILURE','No product test launches','FAIL with NOT_STARTED execution, remaining NOT_RUN cases and exact report/fix evidence','Candidate and developer tests unchanged','No QA repair or automatic dev invocation']
    else:
        extra='Create a test plan only; do not execute product tests or builds or generate executable harnesses.'
        expected=['Plan and report delivered to literal destination','NOT_EVALUATED non-verdict','No product test launches','No executable harness generation','Candidate and tests unchanged']
    prompt=f'Use $qa from {project/".agents/skills/qa/SKILL.md"}. {extra} Selected product specification: {project/"docs/spec.md"}; current candidate: {project}. Evidence destination: {project/"qa evidence Ω"}. Local inspection and allowed QA artifact writes are authorized. No installation, network, product repairs or external actions.'
    put(case/'prompt.txt',prompt)
    cmd=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-']
    write(case/'plan.json',dict(schema_version='1',case_id=cid,requirement_ids=['QAP-001','QAP-010','QAP-012'] if cid=='QPV-02' else ['QAP-005','QAP-006','QAP-008','QAP-011'],fixtures=[ref(project/n) for n in ['inc.py','test_inc.py','README.md','AGENTS.md','docs/spec.md']],expected_outputs=expected,expected_effects=['Only disposable project QA outputs'],executor='installed Codex CLI existing configured model/auth',command=cmd,prompt=ref(case/'prompt.txt'),timeout_seconds=120,permitted_write_root=str(project)))
    write(case/'before.json',observe.make_manifest(project))
