"""Package the selected development candidate without changing its source."""
import hashlib
import io
import json
from pathlib import Path
import tarfile

root = Path(__file__).resolve().parents[2]
archive = root / 'devforgeai-ubuntu-source-20260914.tar.gz'
assert not archive.exists(), f'Refusing to overwrite {archive}'
evidence = root / 'docs/plan/index-service-implementation/20260914T0727264112301Z'
candidate = json.loads((evidence/'attempts/085-windows-final-coverage/candidate.json').read_text())
sha = lambda data: hashlib.sha256(data).hexdigest()
for entry in candidate:
    assert sha((root/entry['path']).read_bytes()) == entry['sha256'], entry['path']

files = []
app = root / 'devforgeai'
for child in app.iterdir():
    if child.name == 'target':
        continue
    files.extend(p for p in child.rglob('*') if p.is_file()) if child.is_dir() else files.append(child)
files.extend(p for p in evidence.rglob('*') if p.is_file())
files.extend(root / name for name in [
    'AGENTS.md',
    'docs/plan/index-service-validation-playbook.html',
    'docs/plan/devforgeai-index-service-mvp-spec.md',
    'docs/plan/devforgeai-index-query-cli-spec.md',
    'docs/plan/devforgeai-codex-rust-enforcement-design.md',
])
payload = {}
for p in sorted(set(files)):
    assert not p.is_symlink(), p
    rel = p.relative_to(root).as_posix()
    assert not any(part in ('target', '.git', '.agents', '.codex') for part in Path(rel).parts), rel
    payload[rel] = p.read_bytes()
payload['TRANSFER-README.txt'] = b'''Ubuntu source qualification bundle

Extract into a new directory; do not overwrite an existing checkout.
From the extracted DevForgeAI directory run:
  sha256sum -c TRANSFER-SHA256SUMS
Then:
  cd devforgeai
Use docs/plan/index-service-validation-playbook.html and select standalone Linux.
The playbook's preparation commands create fresh evidence under ../docs/plan.

Prerequisites: Rust >=1.93, Cargo, a native C compiler; rustfmt, Clippy and
cargo-llvm-cov/LLVM tools for their respective checks. Dependencies are pinned
by Cargo.lock but are not vendored; the initial build needs network access
unless the host already has the dependency cache. No binaries are included.

Current candidate is PARTIAL. Windows and WSL coverage fail the 95% floor;
standalone Ubuntu is untested. Retained evidence contains original Windows
and WSL absolute paths. Those historical paths are not Ubuntu setup commands.
Operational skills referenced in old input manifests are not included or
needed for building this application. No installation or startup changes are
performed by extracting this archive. Follow the playbook for isolated data.
'''
manifest = ''.join(f'{sha(data)}  {name}\n' for name, data in sorted(payload.items()))
payload['TRANSFER-SHA256SUMS'] = manifest.encode()
with tarfile.open(archive, 'x:gz') as tar:
    for name, data in sorted(payload.items()):
        info = tarfile.TarInfo('DevForgeAI/' + name)
        info.size = len(data)
        info.mode = 0o755 if name.endswith('.sh') else 0o644
        info.mtime = 0
        tar.addfile(info, io.BytesIO(data))
with tarfile.open(archive, 'r:gz') as tar:
    members = tar.getmembers()
    assert len(members) == len(payload)
    for member in members:
        assert member.isfile() and member.name.startswith('DevForgeAI/')
        assert tar.extractfile(member).read() == payload[member.name[len('DevForgeAI/'):]]
for p in files:
    assert p.read_bytes() == payload[p.relative_to(root).as_posix()], f'Source changed: {p}'
checksum = archive.with_name(archive.name + '.sha256')
checksum.write_text(f'{sha(archive.read_bytes())}  {archive.name}\n', encoding='ascii')
print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size,
                  'files': len(payload), 'sha256': sha(archive.read_bytes()),
                  'checksum': str(checksum), 'archive_byte_verification': 'PASS',
                  'source_readback': 'PASS'}, indent=2))
