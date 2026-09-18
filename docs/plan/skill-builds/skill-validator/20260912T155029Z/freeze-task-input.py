import json, sys
from pathlib import Path
from bootstrap import ROOT, write, inventory, digest
from verification import copy_package
name=sys.argv[1]
root=ROOT/'task-trials'/name; root.mkdir(parents=True,exist_ok=False)
copy_package(ROOT/'candidate',root/'validator')
write(root/'validator-before-manifest.json',inventory(root/'validator'))
write(root/'case-before.json',{'case_file':'validator/evals/cases.jsonl','sha256':digest((root/'validator/evals/cases.jsonl').read_bytes()),'expectations_sha256':digest((ROOT/'task-expectations.json').read_bytes()),'expectation_visibility':'not supplied to executor; separate grader after task'})
print(str(root))
