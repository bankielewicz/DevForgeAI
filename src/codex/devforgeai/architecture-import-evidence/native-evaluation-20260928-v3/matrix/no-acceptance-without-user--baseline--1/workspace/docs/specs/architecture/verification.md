# PRD-001 architecture verification

Verification date: 2026-09-28. Scope: the supplied working-tree documents, not a
Git revision (the workspace has no usable Git repository). Architecture and ADR
content fingerprints are recorded below after validation. This is documentation
verification; no product behavior is claimed to pass.

| Check | Result | Evidence or unresolved finding |
|---|---|---|
| Approved input preserved | PASS | PRD-001 full-file SHA-256 matches the recorded source hash; generated epic map unchanged |
| All active current requirements covered | PASS | Six unique requirement rows, each with allocation, readiness, dependency and verification references |
| FR-001 identity architecture | BLOCKED | ADR-001 explicitly retains the unresolved provider/enrollment/recovery decision |
| NFR-001 revocation architecture | BLOCKED | Enforcement design present; provider renewal/SSO integration evidence still needed |
| FR-002 and FR-003 architecture allocation | PASS | Transaction and roster flows defined; identity dependency recorded; epic decomposition is possible |
| NFR-002 privacy allocation | PASS | Coordinator-only projection; administrator-only and volunteer roles denied phone access; negative tests specified |
| NFR-003 global allocation | PASS | Hosted boundary includes identity, application, data, sessions and operations; inherited by every epic |
| YAML, local links and evidence IDs | PASS | Reproducible command below exits 0 |
| V-01 through V-06 runtime acceptance | NOT_RUN | No implementation or test harness supplied; obligations recorded in ARC-001 |
| Repository-defined quality gates | NOT_RUN | No build/test/validation configuration supplied |

Manual review checked requirement wording against the architecture, preserved the
FR-003 should priority, and distinguished epic decomposition from integration and
release readiness. No epic or stakeholder approval was fabricated. Pending pilot
configuration and ASM-01 remain recorded in ARC-001.

Run from the project root (Python 3 and PyYAML were available):

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import re
import yaml

base = Path('docs/specs')
prd = base / 'prd/PRD-001.md'
arc = base / 'architecture/ARC-001.md'
adr = base / 'adr/ADR-001.md'
expected = '73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef'
assert hashlib.sha256(prd.read_bytes()).hexdigest() == expected
metadata = {}
for path in (prd, arc, adr):
    metadata[path] = yaml.safe_load(path.read_text().split('---', 2)[1])
assert metadata[arc]['upstream'][0]['hash'] == expected
assert metadata[arc]['status'] == 'draft'
assert metadata[adr]['status'] == 'proposed'
requirements = set()
for block in re.findall(r'```yaml items\n(.*?)```', prd.read_text(), re.S):
    parsed = yaml.safe_load(block)
    for key in ('functional_requirements', 'non_functional_requirements'):
        requirements.update(item['id'] for item in parsed.get(key, [])
                            if item['status'] == 'active' and item['release'] == 'current')
rows = re.findall(r'^\| ((?:NFR|FR)-\d{3}) \| (.+)$', arc.read_text(), re.M)
assert len(rows) == len(requirements) == 6
assert {item for item, _ in rows} == requirements
blocked = {'FR-001', 'NFR-001'}
assert set(metadata[arc]['blocked_by'][0]['items']) == blocked
assert metadata[arc]['blocked_by'][0]['id'] == metadata[adr]['id']
evidence = set(re.findall(r'^\| (V-\d{2}) \|', arc.read_text(), re.M))
assert evidence == {f'V-{i:02}' for i in range(1, 7)}
for item, row in rows:
    cells = [cell.strip() for cell in row.split('|')[:-1]]
    assert len(cells) == 4 and all(cells)
    assert cells[1] == ('BLOCKED' if item in blocked else 'READY')
    refs = set(re.findall(r'V-\d{2}', cells[-1]))
    assert refs and refs <= evidence
for path in base.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if not target.startswith(('https://', 'http://', '#')):
            assert (path.parent / target.split('#')[0]).exists(), (path, target)
print('PASS: source preservation, YAML, 6 requirement mappings, readiness, evidence IDs, local links')
for path in (prd, arc, adr):
    print(hashlib.sha256(path.read_bytes()).hexdigest(), path)
PY
```

Candidate fingerprints and command output are recorded below.

```text
PASS: source preservation, YAML, 6 requirement mappings, readiness, evidence IDs, local links
73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef docs/specs/prd/PRD-001.md
21fe24bfc6448b94da922859d965ac86134dbd6d0182c4d4987fa60d0c2fc153 docs/specs/architecture/ARC-001.md
2da45e027183d2816e6f14b2c9f29838985f1b9cfa04e6b40030a9850b3ec2eb docs/specs/adr/ADR-001.md
```

Exit status: 0. No unresolved document-check failures. ADR-001 remains the material
architecture blocker. Runtime acceptance evidence remains NOT_RUN.
