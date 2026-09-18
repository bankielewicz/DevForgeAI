"""Capture immutable development inputs; evidence only."""
from pathlib import Path
import hashlib, json, shutil, subprocess, datetime

ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(r'C:\Projects\DevForgeAI')
PACKAGE = WORKSPACE / 'devforgeai/experiments/codex-worker-probe'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name, value):
    with (ROOT/name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2); f.write('\n')

prior = WORKSPACE/'docs/plan/framework-worker-native-completion/20260916T003840Z-dev'
shutil.copyfile(prior/'record.py', ROOT/'record.py')
import record
manifest = record.package_manifest()
write('baseline-manifest.json', manifest)
for entry in manifest:
    assert entry['kind'] == 'file', entry
    dst = ROOT/'baseline'/entry['path']
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PACKAGE/entry['path'], dst)
inputs = ['AGENTS.md', 'docs/prompt/qa.md', '.agents/skills/dev/SKILL.md', '.agents/skills/qa/SKILL.md',
          'docs/specs/framework/runtime/codex-worker-feasibility-v1.md',
          'docs/specs/framework/runtime/codex-worker-native-readiness-v1.md',
          'docs/specs/framework/runtime/codex-worker-preflight-v1.md',
          'docs/plan/devforgeai-codex-rust-enforcement-design.md',
          'docs/plan/framework-worker-native-continuation/20260916T013303Z/source-inventory-proposal.md']
write('input-manifest.json', [{'path':x, 'sha256':sha(WORKSPACE/x), 'bytes':(WORKSPACE/x).stat().st_size} for x in inputs])
write('context.json', {'selected_evidence_value':str(ROOT), 'selection_source':'AGENTS.md docs/plan distinct evidence rule; approved source-inventory-proposal selected by user ok - i approve then',
    'resolved_evidence_root':str(ROOT.resolve()), 'cwd':str(WORKSPACE), 'candidate':str(PACKAGE),
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'git_metadata_present':(WORKSPACE/'.git').exists(),
    'baseline_files':len(manifest), 'manifest_sha256':sha(ROOT/'baseline-manifest.json'),
    'scope':'Approved companion contract, compiled Rust bounded plugin junction identity, developer checks and separate independent QA; after PASS compiled source observation.',
    'preserve':'Old contracts/evidence and all installed/operational state. Native trials remain subject to profile prerequisites. Authority excluded.',
    'output_mapping':{'baseline':'baseline/', 'inputs':'input-manifest.json','commands':'unique attempt directories/receipt.json + raw streams','plan':'plan.md','delivery':'delivery.md','final_binding':'candidate-manifest.json','seal':'artifact-manifest.json (write once)'}})
print(json.dumps({'root':str(ROOT),'files':len(manifest),'baseline_sha256':sha(ROOT/'baseline-manifest.json')}))
