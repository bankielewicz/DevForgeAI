import hashlib
import json
from pathlib import Path
RUN = Path(__file__).resolve().parent
B, V = [RUN / 'candidate' / name for name in ('skill-builder','skill-validator')]
for root, loc in ((V,'evals/build-manifest.json'), (B,'package-manifest.json')):
    artifacts = {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and p != root / loc}
    if root == V:
        manifest = json.loads((root / loc).read_text())
        manifest['artifacts'] = artifacts
    else:
        manifest = {'schema_version':'authoring-package-v1','artifacts':artifacts}
    (root / loc).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
