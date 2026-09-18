"""Freeze editable development evidence for independent QA; grants no acceptance."""
import json
import shutil
from pathlib import Path
import record

snapshot = record.ROOT/'candidate-snapshot'
snapshot.mkdir(exist_ok=False)
manifest = []
for path in sorted(record.PACKAGE.rglob('*')):
    relative = path.relative_to(record.PACKAGE)
    if not path.is_file() or 'target' in relative.parts:
        continue
    target = snapshot/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(path,target)
    manifest.append({'path':str(path),'bytes':path.stat().st_size,'sha256':record.sha(path)})
record.write('candidate-manifest.json',manifest)
old = {entry['path']:entry for entry in json.loads((record.ROOT/'baseline-manifest.json').read_text(encoding='utf-8-sig'))}
now = {entry['path']:entry for entry in manifest}
record.write('changes.json',{'added':[p for p in now if p not in old], 'removed':[p for p in old if p not in now],
    'changed':[p for p in now if p in old and now[p]['sha256']!=old[p]['sha256']]})
inputs = [record.WORK/p for p in ['AGENTS.md','docs/prompt/qa.md',
    'docs/specs/framework/runtime/codex-worker-feasibility-v1.md',
    'docs/specs/framework/runtime/codex-worker-native-readiness-v1.md',
    'docs/specs/framework/runtime/codex-worker-preflight-v1.md',
    'docs/plan/devforgeai-codex-rust-enforcement-design.md',
    'docs/plan/framework-worker-contract/20260915T151300Z/schema-manifest.json',
    '.agents/skills/dev/SKILL.md','.agents/skills/qa/SKILL.md']]
record.write('inputs-manifest.json',[{'path':str(p),'bytes':p.stat().st_size,'sha256':record.sha(p)} for p in inputs])
record.write('source-denominator.json',{'rule':'All first-party executable lines in src/**/*.rs, no first-party runtime exclusions; test/support and dependencies excluded by resolved path.',
    'source_files':[e for e in manifest if Path(e['path']).suffix=='.rs' and 'src' in Path(e['path']).relative_to(record.PACKAGE).parts],
    'platform':'Windows x64','features':'default; package defines no optional feature combinations','branch_coverage':'NOT_RUN unless separately measured'})
print(json.dumps({'candidate_files':len(manifest),'candidate_manifest_sha256':record.sha(record.ROOT/'candidate-manifest.json'),
                  'inputs_manifest_sha256':record.sha(record.ROOT/'inputs-manifest.json')}))
