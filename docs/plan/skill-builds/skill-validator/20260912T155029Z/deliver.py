import json
from bootstrap import ROOT, PROJECT, write, inventory, digest
from verification import copy_package, evaluate

destination=PROJECT/'src/agents/skills/skill-validator'
assert not destination.exists(), 'Destination collision: do not overwrite'
contract=json.loads((ROOT/'build-contract.json').read_text())
for row in contract['inputs']:
    assert digest(__import__('pathlib').Path(row['resolved_path']).read_bytes())==row['sha256']
assert inventory(PROJECT/'.agents/skills/skill-builder')['files']==json.loads((ROOT/'builder-before-manifest.json').read_text())['files']
write(ROOT/'delivery-before.json',{'destination':str(destination),'absent':not destination.exists(),'candidate':inventory(ROOT/'candidate'),'status':'Checks pending; no successful provenance published'})
copy_package(ROOT/'candidate',ROOT/'generated-baseline')
copy_package(ROOT/'candidate',destination)
write(ROOT/'destination-manifest.json',inventory(destination))
assert inventory(destination)['files']==inventory(ROOT/'generated-baseline')['files']
code,folder=evaluate('delivered-001',destination)
assert code==0
write(ROOT/'delivery-readback.json',{'source':'actual delivered development package','destination':str(destination),'baseline_separate':True,'delivered_matches_generated_baseline':inventory(destination)['files']==inventory(ROOT/'generated-baseline')['files'],'full_file_set_readback':True,'evaluator_root':str(folder),'provenance_publication':'PENDING behavioral case review and labeled self-review'})
print(str(destination))
