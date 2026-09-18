"""Independent synthetic cases. Never modifies selected source packages."""
from bootstrap import ROOT, PROJECT, VALIDATOR, write, run, observe
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def ref(path):
    return dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

if __name__ == '__main__':
    sources=[]
    for row in json.loads((ROOT/'input-bindings.json').read_bytes()):
        if Path(row['original_path']).name in ('qa-skill-spec.md','qa-skill-postmvp-spec.md','manual-evaluation-obligations.md','AGENTS.md'):
            sources.append(dict(source_id=Path(row['original_path']).stem,original_path=row['original_path'],retrieved_at_utc=None,sha256=row['sha256'],snapshot_path=row['snapshot_path'],sections=['Selected contract'],freshness='snapshot_only'))
    av=ROOT/'inputs/validator/references/adaptive-validation.md'
    sources.append(dict(source_id='AV-catalog',original_path=str(VALIDATOR/'references/adaptive-validation.md'),retrieved_at_utc=None,sha256=ref(av)['sha256'],snapshot_path=ref(av)['path'],sections=['3.1','4.1'],freshness='snapshot_only'))
    write(ROOT/'sources.json',dict(schema_version='1',run_id=ROOT.name,target_name='qa',sources=sources))
    rules=[]
    for line in av.read_text(encoding='utf-8').splitlines():
        m=re.match(r'\| (AV-[A-Z]\d+) \| (.*?) \| (.*?) \|',line)
        if not m: continue
        rid,method,expected=m.groups()
        adaptive=rid.startswith('AV-A')
        rules.append(dict(rule_id=rid,revision='2026-09-12',title=method,source_refs=[dict(**ref(av),source_id='AV-catalog',locator={'section':'3.1 / 4.1'})],authority_class='project_policy',applicability='not_applicable' if adaptive else 'applicable',method='behavioral' if rid in ['AV-W01','AV-W02'] else 'semantic' if rid.startswith(('AV-I','AV-S')) else 'deterministic',expected_observation=expected,required=True,limitation='Ordinary skill; no adaptive descriptor or set required.' if adaptive else 'Method coverage separated in checks; no framework acceptance.'))
    cases=[]
    for spec in ['qa-skill-spec.md','qa-skill-postmvp-spec.md']:
        sp=next(ROOT/r['snapshot_path'] for r in sources if Path(r['original_path']).name==spec)
        for line in sp.read_text(encoding='utf-8').splitlines():
            m=re.match(r'\| (Q(?:P)?V-\d+): (.*?) \| (.*?) \| (.*?) \|',line)
            if m:
                cid,title,requirements,expected=m.groups()
                if cid=='QV-01': expected='Explicit planning-only request. '+expected
                cases.append(dict(case_id=cid,title=title,requirements=requirements.split(', '),expected=expected,spec=ref(sp),compatibility=next(r['snapshot_path'] for r in sources if Path(r['original_path']).name=='manual-evaluation-obligations.md'),required=True,status='NOT_RUN'))
    assert len(cases)==42
    for c in cases:
        rules.append(dict(rule_id=c['case_id'],revision='1',title=c['title'],source_refs=[dict(**c['spec'],source_id='qa-contract',locator={'section':c['case_id']})],authority_class='project_policy',applicability='applicable',method='behavioral',expected_observation=c['expected'],required=True,limitation='All named variants required; partial exercises cannot qualify the entire scenario.'))
    write(ROOT/'rule-set.json',dict(schema_version='1',run_id=ROOT.name,target_name='qa',rules=rules))
    write(ROOT/'case-catalog.json',cases)
    write(ROOT/'routing-plan.json',dict(method='independent description-only agent',expected={f'P{i}':'SELECT' if i<=4 else 'DO_NOT_SELECT' for i in range(1,11)},limitation='Expected labels fixed from selected description; native activation requires separate evidence.'))
    case=ROOT/'trials/QPV-01'
    project=case/'project'
    project.mkdir(parents=True)
    shutil.copytree(ROOT/'source',project/'.agents/skills/qa')
    put(project/'docs/spec.md','# Increment contract\n\nAC-1: inc(0) returns 1.\nAC-2: inc(-1) returns 0.\nAC-3: inc(41) returns 42.\nRequired host: current Windows Python. No other platforms, services or UI.\n')
    put(project/'inc.py','def inc(value):\n    return value + 1\n')
    put(project/'test_inc.py',"import unittest\nfrom pathlib import Path\nfrom inc import inc\n\nclass IncrementTests(unittest.TestCase):\n    def test_zero(self):\n        with Path('launches.jsonl').open('a', encoding='utf-8') as f:\n            f.write('{\"event\":\"test_launch\",\"case_id\":\"unit-zero\"}\\n')\n        self.assertEqual(inc(0), 1)\n    def test_negative(self):\n        with Path('launches.jsonl').open('a', encoding='utf-8') as f:\n            f.write('{\"event\":\"test_launch\",\"case_id\":\"unit-negative\"}\\n')\n        self.assertEqual(inc(-1), 0)\n    def test_positive(self):\n        with Path('launches.jsonl').open('a', encoding='utf-8') as f:\n            f.write('{\"event\":\"test_launch\",\"case_id\":\"unit-positive\"}\\n')\n        self.assertEqual(inc(41), 42)\n")
    put(project/'README.md','# Project\nPython standard-library unittest. Run `python -B -m unittest -v test_inc`. Installed coverage.py may collect inc.py coverage using `python -B -m coverage run --source=inc -m unittest -v test_inc` and `python -B -m coverage json -o coverage.json`. The source denominator is inc.py; tests are not application code. launches.jsonl is instrumentation, not a result oracle. No dependencies to install.\n')
    put(project/'AGENTS.md','# Synthetic project boundaries\nThis is an isolated product fixture. Use only this project. Source inc.py, test_inc.py and docs/spec.md are immutable inputs. Local QA evidence and independent fixtures may be created here. No installs, networking, GUI, real services, product repairs or external writes. Python is the product language; this fixture is not DevForgeAI framework implementation. No required downstream deployment.\n')
    (project/'.trial-output').mkdir()
    prompt=f'Use $qa from {project / ".agents/skills/qa/SKILL.md"} to perform independent product QA against {project / "docs/spec.md"} and the current candidate in {project}. Write QA artifacts under {project / "qa evidence Ω"}. Local isolated QA preparation and test execution are authorized. Preserve the candidate and supplied developer tests. No installation, network or external actions.'
    put(case/'prompt.txt',prompt)
    cmd=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-']
    write(case/'plan.json',dict(schema_version='1',case_id='QPV-01',requirement_ids=['QAP-001','QAP-002','QAP-003','QAP-004'],fixtures=[ref(project/'docs/spec.md'),ref(project/'inc.py'),ref(project/'test_inc.py'),ref(project/'README.md'),ref(project/'AGENTS.md')],expected_outputs=['Bound plan and QA report beneath exact selected root','At least three actual developer test launch markers in same invocation','Independent specification-based evidence','No second approval or final execute handoff','Candidate and tests unchanged'],expected_effects=['Only disposable project writes'],executor='installed Codex CLI existing configured model/auth',command=cmd,prompt=ref(case/'prompt.txt'),timeout_seconds=120,permitted_write_root=str(project)))
    write(case/'before.json',observe.make_manifest(project))
    run('structure',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'structure','--source',str(ROOT/'source')])
    run('installed-checker',[sys.executable,'-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(ROOT/'source')])
    run('text-resources',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'package','--source',str(ROOT/'source'),'--tokenizer','tiktoken','--encoding','o200k_base'])
