# ARC-001 verification — 2026-09-28

Candidate: the working-tree documentation below. The workspace has an empty `.git` directory rather than a usable Git repository, so file SHA-256 hashes identify the reviewed state.

| File | SHA-256 |
|---|---|
| `docs/specs/prd/PRD-001.md` | `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef` |
| `docs/specs/policy/POL-001.md` | `16184a253d0e29d5797600b9ae3b366326374dceb5e89fb2711015eba8190dbe` |
| `docs/specs/architecture/ARC-001.md` | `8b9acc1b267f1b3755036014bb8d03f22e4e0784b2bee849be9d138f059c9dfb` |
| `docs/specs/adr/ADR-001.md` | `db20975e6618b6d9107ac0fc8472ab480acacf6a332d85cb1a892bf7c731376e` |

## Documentation checks

| Check | Result | Evidence |
|---|---|---|
| All six active FR/NFR items allocated and classified | PASS | ARC-001 sections 2, 5, and 6; automated readiness-row check below. |
| Non-functional requirements have enforcement and verification mechanisms | PASS | NFR-001: generation check and replay/race tests; NFR-002: server authorization/projection and role tests; NFR-003: whole-product hosted boundary and deployment inventory. Design review only. |
| Identity decision is represented without false closure | PASS | ADR-001 is proposed, provider unresolved, FR-001 BLOCKED; dependent delivery work is identified separately. |
| Approved source documents preserved | PASS | Source hashes match the initial read. The PRD's generated epic map is untouched. |
| YAML, upstream requirement references, and relative links | PASS | Command below completed successfully against this candidate. |
| Required repository gates | NOT_RUN | No gate scripts, application, or test configuration exist in the supplied repository. |
| Runtime acceptance | NOT_RUN | Documentation only; no runnable application or deployment. FR-001 additionally BLOCKED by ADR-001. See ARC-001 section 6 for per-requirement evidence still required. |

No runtime behavior was changed, so no meaningful failing runtime test could be established. No acceptance criterion or validation threshold was weakened. Architectural readiness is separate from runtime acceptance.

## Commands and outcomes

`git status --short` returned exit 128: not a Git repository. `python` was unavailable; the checks used `/usr/bin/python3` with the already installed PyYAML. `sha256sum` on the four paths above returned the recorded hashes.

Run from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, re, yaml

root = Path('docs/specs')
arc = (root / 'architecture/ARC-001.md').read_text()
report = (root / 'architecture/ARC-001-verification.md').read_text()
prd = (root / 'prd/PRD-001.md').read_text()
items = [yaml.safe_load(b) for b in re.findall(r'```yaml items\n(.*?)```', prd, re.S)]
ids = {v['id'] for b in items for k, values in b.items()
       if k in ('functional_requirements', 'non_functional_requirements') for v in values}
assert ids == {'FR-001', 'FR-002', 'FR-003', 'NFR-001', 'NFR-002', 'NFR-003'}
for item in ids:
    expected = 'BLOCKED' if item == 'FR-001' else 'READY'
    assert re.search(r'\| ' + item + r':[^\n]+\| ' + expected + r' \|', arc), item
for path in root.rglob('*.md'):
    content = path.read_text()
    if content.startswith('---\n'):
        metadata = yaml.safe_load(content.split('---', 2)[1])
        assert metadata['id'] == path.stem, path
        for upstream in metadata.get('upstream', []):
            if path.stem in ('ARC-001', 'ADR-001') and upstream['id'] == 'PRD-001':
                assert upstream.get('item') is None or upstream['item'] in ids
    for link in re.findall(r'\]\(([^)]+)\)', content):
        if '://' not in link:
            assert (path.parent / link.split('#')[0]).is_file(), (path, link)
for name, digest in re.findall(r'\| `(docs/[^`]+)` \| `([0-9a-f]{64})` \|', report):
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
assert yaml.safe_load((root / 'adr/ADR-001.md').read_text().split('---', 2)[1])['status'] == 'proposed'
print('PASS: 6 requirement readiness rows; metadata, trace references, links, and 4 file hashes')
PY
```

Unresolved findings: identity-provider selection and the explicitly labeled operational assumptions in ARC-001 section 7. No identity decision approval, implementation test pass, or pilot release readiness is claimed.
