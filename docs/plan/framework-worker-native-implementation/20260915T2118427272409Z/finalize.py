"""Build source/evidence inventories without following retained reparse fixtures."""
import json
import os
import shutil
from pathlib import Path
from record import ROOT, WORK, PACKAGE, sha, write

manifest = json.loads((ROOT/'candidate-manifest.json').read_text())
snapshot = ROOT/'candidate-snapshot'
snapshot.mkdir(exist_ok=False)
for item in manifest:
    source = Path(item['path'])
    assert sha(source) == item['sha256'], 'candidate changed after freeze'
    dest = snapshot/source.relative_to(PACKAGE)
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,dest)
before={x['path']:x['sha256'] for x in json.loads((ROOT/'baseline-manifest.json').read_text())}
write('changes.json',{'changed':[x['path'] for x in manifest if x['path'] in before and x['sha256']!=before[x['path']]],
    'added':[x['path'] for x in manifest if x['path'] not in before],
    'removed':[x for x in before if x not in {y['path'] for y in manifest}]})
write('inputs-readback.json',[{**x,'actual_sha256':sha(x['path']),'unchanged':sha(x['path'])==x['sha256']}
    for x in json.loads((ROOT/'inputs-manifest.json').read_text(encoding='utf-8-sig'))])

proposal=json.loads((WORK/'docs/plan/framework-native-readiness/20260915T1937559109498Z/restrictive-launch-policy.proposed.json').read_text())
proposal['policy_id']='codex-0.154.0-readonly-no-external-tools-v2-proposed'
proposal['status']='PROPOSED_NOT_RUNTIME_QUALIFIED_DO_NOT_LAUNCH'
proposal['unknown_keys']='Strict-config behavior and effective integration inactivity must be verified in the pinned app-server; features-list acceptance is insufficient.'
for key in ['hooks','plugins','apps','browser_use','browser_use_external','browser_use_full_cdp_access','computer_use',
            'image_generation','in_app_browser','multi_agent','shell_tool','tool_suggest','view_image']:
    proposal['argv'] += ['-c',f'features.{key}=false']
proposal['remaining']='Needs selected closed-schema preflight contract and pinned-version effective-effect verification before implementation or launch. See profile-research/compatibility.md.'
write('restrictive-launch-policy.next-proposed.json',proposal)
print(json.dumps({'snapshot_files':len(manifest),'candidate_manifest_sha256':sha(ROOT/'candidate-manifest.json'),
    'next_proposed_policy_sha256':sha(ROOT/'restrictive-launch-policy.next-proposed.json')}))
