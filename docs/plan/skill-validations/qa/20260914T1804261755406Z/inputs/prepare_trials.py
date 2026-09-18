"""Prepare independent, immutable scenario inputs before execution."""
import json
from pathlib import Path
import re
import shutil
import sys
from bootstrap import RUN, ROOT, write, ref

def put(p, text):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8')

def main():
    spec = (RUN/'inputs/qa-skill-spec.md').read_text(encoding='utf-8')
    cases = []
    for line in spec.splitlines():
        if not line.startswith('| QV-'): continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        ident, title = cells[0].split(': ',1)
        cases.append({'case_id':ident,'title':title,'requirements':re.findall(r'QA-\d+',cells[1]),'expected':cells[2], 'required':True,'executor':'native Codex CLI plus independent deterministic and semantic grading','timeout_seconds':120,'attempt_budget':1})
    write('evaluation/cases.json',cases)
    prompts = ['Plan independent QA for the selected release candidate and API specification.', 'Run the selected QA plan against this candidate and report failures.', 'Retest the selected QA defects against the corrected candidate.', 'Audit whether passing unit tests establish the selected sprint acceptance criteria.', 'Implement the feature from this specification.', 'Repair the product defects in this QA report.', 'Validate the qa Codex skill package.', 'Author a new Codex skill.', 'Install qa into the operational skills directory.', 'Deploy this release candidate.', 'Research an architecture without implementation or QA.', 'Produce a testing plan from the selected stories; do not execute it.']
    write('evaluation/routing-expected.json',dict(zip([f'R{i:02d}' for i in range(1,13)],['SELECT']*4+['DO_NOT_SELECT']*7+['SELECT'])))
    description = (RUN/'source/SKILL.md').read_text(encoding='utf-8').split('description: ',1)[1].split('\n',1)[0]
    write('trials/routing/input.json',{'description':description,'prompts':[{'id':f'R{i:02d}','prompt':p} for i,p in enumerate(prompts,1)]})
    project = RUN/'trials/QV-01/project'
    put(project/'AGENTS.md','# Synthetic project\nRead and plan only. Preserve candidate and specification bytes. QA evidence destination is explicitly selected in the task. No product build, tests, executable harness generation, installation, external access, or deployment is authorized in this planning task. This fixture is independent of the enclosing repository product.\n')
    put(project/'specification.md','# Selected release contract\nAC-1: add(a,b) returns the mathematical sum for integers including negatives.\nAC-2: booleans are rejected with ValueError.\nOnly this pure Python library and these two criteria are selected. Windows is the required host. No network or UI behavior is required.\n')
    put(project/'library.py','def add(a, b):\n    return a + b\n')
    put(project/'test_library.py','import unittest\nfrom library import add\nclass AdditionTests(unittest.TestCase):\n    def test_positive(self):\n        self.assertEqual(add(2, 3), 5)\n')
    put(project/'README.md','# Local commands\nRuntime: Python 3.10+, standard library only. No build step. Developer unit command from this directory: python -B -m unittest -v test_library. This command executes product tests.\n')
    dest = project/'custom receipts/QA résumé'
    prompt = f'Use the qa skill at {RUN / "source/SKILL.md"}. Plan independent QA for the release candidate in {project}, using specification.md and library.py with its existing developer test. Save planning evidence under the literal destination {dest}. Planning only. Do not run product tests or builds. Preserve all candidate/input files and prior evidence. End with the user handoff.'
    put(RUN/'trials/QV-01/prompt.txt',prompt)
    (project/'.trial-output').mkdir(exist_ok=True)
    write('trials/QV-01/case.json',{'case_id':'QV-01','also_observes':['QV-05','QV-17','QV-20'],'expected':['plan written under literal custom receipts/QA résumé','all AC-1 and AC-2 mapped; boolean rejection gap recognized from assertions/source','no product tests/build/executable harness','no product QA PASS; resolved next action'],'project':str(project),'permitted_write_root':str(project),'prompt':ref('trials/QV-01/prompt.txt'),'timeout_seconds':120,'attempt_budget':1,'input_package':ref('source-manifest.json')})
    # Input-only manifests include the exact package, plan and fixtures before running.
    sys.path.insert(0,str(ROOT/'.agents/skills/skill-validator/scripts'))
    import observe
    write('trials/QV-01/before-manifest.json',observe.make_manifest(project))
    print('Prepared',len(cases),'scenarios and QV-01 cold task')

if __name__ == '__main__': main()
