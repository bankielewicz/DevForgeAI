import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
def walk(root):
    rows = {}
    excluded = []
    pending = [root]
    while pending:
        for p in sorted(pending.pop().iterdir()):
            rel = p.relative_to(root).as_posix()
            if p == RUN or p.name.lower() in ('devforgeai_cli', '.git', '__pycache__') or 'backup' in p.name.lower():
                excluded.append(rel)
                continue
            info = p.lstat()
            if p.is_symlink() or getattr(info, 'st_file_attributes', 0) & 0x400:
                excluded.append(rel)
            elif p.is_dir():
                pending.append(p)
            elif p.is_file():
                rows[rel] = {'bytes': info.st_size, 'sha256': sha(p)}
            else:
                raise ValueError('special file: ' + str(p))
    return {'files': rows, 'excluded': excluded}

if __name__ == '__main__':
    spec = ROOT / 'docs/plan/skill-builder-authoring-enhancement-spec.md'
    assert sha(spec) == '43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14'
    if len(sys.argv) > 1 and sys.argv[1] == 'readback':
        before = json.loads((RUN / 'workspace-before.json').read_text())
        after = walk(ROOT)
        changed = [p for p in sorted(set(before['files']) | set(after['files'])) if before['files'].get(p) != after['files'].get(p)]
        allowed = ('src/agents/skills/skill-builder/', 'src/agents/skills/skill-validator/')
        report = {'changed': changed, 'unauthorized': [p for p in changed if not p.startswith(allowed)], 'excluded_before': before['excluded'], 'excluded_after': after['excluded']}
        save(RUN / 'scope-readback.json', report)
        print(json.dumps(report))
        sys.exit(bool(report['unauthorized']))
    save(RUN / 'workspace-before.json', walk(ROOT))
    inputs = RUN / 'inputs'
    inputs.mkdir()
    shutil.copy2(spec, inputs / spec.name)
    for name in ('skill-builder', 'skill-validator'):
        source = ROOT / 'src/agents/skills' / name
        shutil.copytree(source, inputs / name)
        save(inputs / (name + '-manifest.json'), walk(source))
    creator = Path('C:/Users/bryan/.codex/skills/.system/skill-creator')
    shutil.copytree(creator, inputs / 'skill-creator', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(ROOT / '.agents/skills/skill-validator', inputs / 'operational-validator')
    shutil.copytree(ROOT / 'docs/codex', inputs / 'codex')
    history = {}
    b = ROOT / 'docs/plan/skill-builds/skill-builder/20260912T212438315Z'
    v = ROOT / 'docs/plan/skill-builds/skill-validator/20260912T155029Z'
    receipt = json.loads((b / 'FINAL-RECEIPT.json').read_text())
    current = walk(ROOT / 'src/agents/skills/skill-builder')['files']
    expected = {r['path']: {'bytes': r['bytes'], 'sha256': r['sha256']} for r in receipt['target_files']}
    history['builder_delivery_matches'] = current == expected
    history['builder_references'] = {k: {'expected': r['sha256'], 'actual': sha(Path(r['path']))} for k, r in receipt['references'].items()}
    provenance = json.loads((v / 'build-provenance.json').read_text())
    history['validator_generated_outputs'] = {r['path']: {'expected': r['sha256'], 'current': sha(ROOT / 'src/agents/skills/skill-validator' / r['path']), 'baseline': sha(v / r['baseline_path'])} for r in provenance['outputs']}
    for label, p in [('builder-provenance', b / 'published/revision/evidence/build-provenance.json'), ('builder-pointer', b / 'published/revision/evidence/active-baseline.json'), ('validator-provenance', v / 'build-provenance.json')]:
        shutil.copy2(p, inputs / (label + '.json'))
    save(RUN / 'history-check.json', history)
    print(json.dumps({'run': str(RUN), 'builder_delivery_matches': history['builder_delivery_matches'], 'builder_reference_mismatches': [k for k,r in history['builder_references'].items() if r['expected'] != r['actual']], 'validator_mismatches': [k for k,r in history['validator_generated_outputs'].items() if len(set(r.values())) != 1]}))
