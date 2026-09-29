# ARCH-001 verification — 2026-09-28

Scope: architecture documentation for PRD-001 v1 and the user's direction to reuse the current auth service. No product behavior was implemented or changed. The workspace has no usable Git metadata (`git status --short` reports “not a git repository”), so evidence is tied to file SHA-256 values rather than a commit.

| Candidate file | SHA-256 |
|---|---|
| `docs/specs/prd/PRD-001.md` | `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef` |
| `docs/specs/architecture/ARCH-001.md` | `70d7d59225f3734fc68c6d882ecbc3da174217432d044075cf0f6a8973021e61` |
| `docs/specs/adr/ADR-001.md` | `fdefda50708b07ffeb6825f656b7094c04a32858d3d09ce8bfb14a72d4d1ecb0` |

| Check | Status | Evidence / limitation |
|---|---|---|
| Preserve approved PRD | PASS | Source hash matches the value captured before edits |
| Architecture coverage of FR-001–003 and NFR-001–003 | PASS | Six explicit acceptance rows, component responsibilities, data flows and required tests; coverage is not proof of runtime compliance |
| Reuse current auth service | PASS | ADR-001 records the explicit user decision; ARCH-001 defines an adapter without selecting a new provider |
| Material unknowns recorded | PASS | Auth protocol, revocation/refresh behavior, phone claims and hosting are identified as unverified dependencies |
| Relative document links and fenced blocks | PASS | Python check below against final documentation files |
| Behavior tests, TDD red/green, deployment checks | NOT_RUN | No code, harness, service credentials or deployment artifacts supplied; documentation-only change |
| Actual auth compatibility | BLOCKED | Existing service contract unavailable; no inference of five-minute revocation or hosted deployment compliance |
| Repository-required gates | NOT_RUN | File inventory and parent instruction checks found no test commands, validation scripts or repository instructions |

Inspection commands: `rg --files --hidden -g '!.git/**'`, `find .. -name AGENTS.md -print`, reads of PRD-001 and checks for ancestor AGENTS.md files. `.agents`, `.codex` and `.git` were empty. An initial check invocation using `python` failed because that executable is unavailable; the same checks succeeded with `python3`.

Reproduce the final structural check from the project root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import re

expected = {
    'docs/specs/prd/PRD-001.md': '73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef',
    'docs/specs/architecture/ARCH-001.md': '70d7d59225f3734fc68c6d882ecbc3da174217432d044075cf0f6a8973021e61',
    'docs/specs/adr/ADR-001.md': 'fdefda50708b07ffeb6825f656b7094c04a32858d3d09ce8bfb14a72d4d1ecb0',
}
for name, digest in expected.items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
prd = Path('docs/specs/prd/PRD-001.md').read_text()
arch = Path('docs/specs/architecture/ARCH-001.md').read_text()
requirements = set(re.findall(r'^  - id: ((?:FR|NFR)-\d+)$', prd, re.M))
rows = set(re.findall(r'^\| ((?:FR|NFR)-\d+) \|', arch, re.M))
assert requirements == rows and len(rows) == 6
for name in ['docs/specs/architecture/ARCH-001.md',
             'docs/specs/adr/ADR-001.md',
             'docs/specs/architecture/ARCH-001-verification.md']:
    path = Path(name)
    body = path.read_text()
    fences = [line for line in body.splitlines() if line.startswith('```')]
    assert len(fences) % 2 == 0, name
    for link in re.findall(r'\]\(([^)]+)\)', body):
        assert (path.parent / link.split('#')[0]).is_file(), (name, link)
print('PASS: candidate hashes, six requirement rows, relative links, code fences')
PY
```

Runtime acceptance statuses and concrete test scenarios remain in [ARCH-001](ARCH-001.md). No numerical availability, performance, or coverage thresholds were supplied, and none were relaxed to obtain a passing documentation check.
