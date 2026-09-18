"""Prepare actual failing predecessor evidence and corrected synthetic candidate."""
import json
import shutil
import subprocess
import sys
from bootstrap import RUN, ROOT, write, ref
from prepare_trials import put
from prepare_campaign import project
sys.path.insert(0,str(ROOT/'.agents/skills/skill-validator/scripts'))
import observe

def main():
    old=RUN/'trials/retest-prior'
    old.mkdir(exist_ok=False)
    tests='import unittest\nfrom library import add\nclass Tests(unittest.TestCase):\n    def test_sum(self): self.assertEqual(add(-2,3),1)\n    def test_bool(self):\n        with self.assertRaises(ValueError): add(True,2)\n'
    put(old/'library.py','def add(a,b):\n    return a+b\n')
    put(old/'test_library.py',tests)
    result=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_library'],cwd=old,capture_output=True,timeout=30)
    (old/'stdout.txt').write_bytes(result.stdout);(old/'stderr.txt').write_bytes(result.stderr)
    assert result.returncode==1 and b'ValueError not raised' in result.stderr
    write('trials/retest-prior/receipt.json',{'command':[sys.executable,'-B','-m','unittest','-v','test_library'],'cwd':str(old),'exit_code':result.returncode,'timeout_seconds':30,'kind':'validator-executed synthetic prior failure; not dev/qa integration'})
    project('retest',{'specification.md':'# Selected contract\nAC-1: add(-2,3) returns 1.\nAC-2: boolean arguments raise ValueError.\nWindows Python; standard library only. The required unit inventory is test_library.Tests.test_sum and test_library.Tests.test_bool. Eligible product executable source is library.py; no other product executable files. tests are excluded from product line coverage but remain in integrity inspection. Downstream after QA PASS is owner review; no deployment is authorized.\n','library.py':'def add(a,b):\n    if isinstance(a,bool) or isinstance(b,bool):\n        raise ValueError("boolean")\n    return a+b\n','test_library.py':tests,'prior-qa-report.md':f'# Seeded previous defect for retest fixture\nD-1 OPEN: AC-2 violated; boolean input returned 3 instead of raising ValueError. Confirmed by actual retained predecessor execution at {old}. This seeded fixture report was written by the validator; it is not claimed as output of a previous qa skill invocation. Reproduction: python -B -m unittest -v test_library in that predecessor directory.\n'},'Retest D-1 and affected AC-1 regression against the corrected library. Execute python -B -m unittest -v test_library. If installed, measure executed-line coverage of library.py in a disposable copy with coverage.py. Reinspect test integrity. Independently determine defect status; the supplied development claim is not closure.', ['D-1 independently tested before VERIFIED_FIXED','both unit cases and product lines measured from actual commands','previous failed evidence remains intact','PASS routes to owner review without deployment authority','implicit skill selected from fixture discovery, no explicit file instruction'],['QV-19','QV-20','native-implicit'])
    p=RUN/'trials/retest/project'
    put(p/'dev-return.json',json.dumps({'kind':'synthetic development handoff','candidate_manifest':ref('trials/retest/project/candidate-manifest.json'),'defects':[{'id':'D-1','state':'FIX_REPORTED','correction':'Reject boolean arguments with ValueError'}]},indent=2))
    local=p/'.agents/skills/qa'
    shutil.copytree(RUN/'source',local)
    prompt=f'Independently retest defect D-1 using {p/"selected-plan.md"}, corrected candidate {p/"candidate-manifest.json"}, specification.md, prior-qa-report.md and dev-return.json in project {p}. The selected plan\'s local test/evidence effects are authorized. Save outputs under {p/"custom receipts/QA résumé"}. Preserve prior evidence and source. End with the user handoff.'
    put(RUN/'trials/retest/prompt.txt',prompt)
    case=json.loads((RUN/'trials/retest/case.json').read_text())
    case['prompt']=ref('trials/retest/prompt.txt')
    case['mode']='implicit native retest'
    write('trials/retest/case.json',case)
    write('trials/retest/before-manifest.json',observe.make_manifest(p))
    print('Prepared retest and implicit discovery with actual previous failure')

if __name__=='__main__':main()
