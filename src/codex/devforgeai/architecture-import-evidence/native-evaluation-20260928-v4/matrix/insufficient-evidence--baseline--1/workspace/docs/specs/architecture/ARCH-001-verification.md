# ARCH-001 verification — 2026-09-28

Scope: documentation only. No application behavior was changed. This workspace
has no runnable application, repository test command, quality gate, or TDD policy
file. Runtime tests and a meaningful failing behavior test could not be established.

| Check | Status | Evidence |
|---|---|---|
| Approved PRD preserved | PASS | SHA-256 matches the value captured before editing |
| FR-001–FR-003 and NFR-001–NFR-003 mapped | PASS | Every requirement has an architecture evidence row |
| Internal document links and code fences | PASS | Python document checks below exit 0 |
| User's auth reuse direction recorded | PASS | ADR-001 accepts reuse while explicitly marking compliance unverified |
| Runtime FR-001 / NFR-001 / NFR-003 | BLOCKED | No existing auth contract, deployment inventory, or runnable integration |
| Remaining runtime acceptance checks | NOT_RUN | No implementation; specific future checks are recorded in ARCH-001 |

Candidate SHA-256 values (no usable Git repository is present):

```text
73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef  docs/specs/prd/PRD-001.md
e19a5beb022133ddc018ff880237fcc449c8364aae09267a3c901ad058d2664e  docs/specs/architecture/ARCH-001.md
26df189a90d96333924b941f378052568fe113bbff4b8e827383abf23f0204f8  docs/specs/adr/ADR-001.md
```

Run from the workspace root:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, re
root = Path('docs/specs')
prd = root / 'prd/PRD-001.md'
arch = root / 'architecture/ARCH-001.md'
adr = root / 'adr/ADR-001.md'
assert hashlib.sha256(prd.read_bytes()).hexdigest() == '73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef'
ids = set(re.findall(r'id: ((?:FR|NFR)-\d+)', prd.read_text()))
assert len(ids) == 6
for rid in ids:
    assert re.search(r'^\| ' + rid + r' \|', arch.read_text(), re.M), rid
for path in (arch, adr):
    assert path.read_text().count('```') % 2 == 0
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        assert (path.parent / link).resolve().is_file(), (path, link)
assert 'status: accepted' in adr.read_text()
assert 'reuse our current auth service' in adr.read_text()
assert 'BLOCKED' in adr.read_text()
print('PASS: PRD preservation, requirement rows, links, fences, auth decision')
for path in (prd, arch, adr):
    print(hashlib.sha256(path.read_bytes()).hexdigest(), path)
PY
```

The first attempt used `python`, which is unavailable (exit 127); the check was
rerun with `python3`. `git status --short` returned exit 128 because `.git` is an
empty placeholder; file hashes identify the reviewed candidate instead.

Unresolved findings: verify current auth protocol, identity mapping, revocation
and refresh semantics, the five-minute bound, and hosted deployment; configure
warehouse timezone, capacities, profile/contact import, roles, and retention
before pilot release. No implementation acceptance result is inferred from these
document checks.
