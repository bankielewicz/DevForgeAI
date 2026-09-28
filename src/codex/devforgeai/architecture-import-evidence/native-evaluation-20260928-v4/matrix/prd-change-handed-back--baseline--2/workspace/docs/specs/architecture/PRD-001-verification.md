# PRD-001 architecture verification

Date: 2026-09-28. Scope: documentation-only working-tree candidate. No application code or approved source requirements changed. No Git revision is available: `git status --short` returned `fatal: not a git repository`. No repository-defined tests, validation scripts, TDD policy, or quality thresholds were present. Behavior-test TDD is not applicable to this documentation change; implementation tests remain NOT_RUN.

## Candidate identity

SHA-256 hashes bind this record to the inspected source and architecture content:

| File | SHA-256 |
|---|---|
| [PRD-001](../prd/PRD-001.md) | `4069b2181cdffd5c24900d596981044544301abc44d85ea9db52b02ab7a26ffb` |
| [POL-001](../policy/POL-001.md) | `d72a0123479999d2d9e03453f89725b7bccb1bacba5f681c36d0e5a116d66602` |
| [ARCH-001](ARCH-001.md) | `90d98545cee20da00285c76e188e62b4741a6be827a609e46d0c52528393482d` |
| [ADR-001](../adr/ADR-001.md) | `39e05eca3a48fb835b50eacf8544f5f2e8721a590adb592692721d9161b133ea` |

## Checks and outcomes

| Check | Status | Evidence / limitation |
|---|---|---|
| Source preservation and current candidate identity | PASS | SHA-256 comparison in command below; original PRD and policy bytes preserved |
| Requirement coverage | PASS | All seven FR/NFR IDs occur exactly once in ARCH-001 §8, with coverage, readiness, blockers and planned acceptance evidence |
| Policy resolution | PASS | Manual comparison of POL-001 SET-01/SET-02 with ARCH-001 §§2, 6–8 and ADR-001; mandated platform retained, both mandatory quality categories applied to internal pilot |
| Dependency propagation | PASS | Manual inspection of ARCH-001 §§7–9: identity blockers propagated to dependent protected flows; hosting and quality constraints apply across the product |
| Decision honesty | PASS | ADR remains proposed/blocked, federation is conditional, and neither external ADR-104 contents nor approvals are asserted |
| Syntax and local references | PASS | Command below parses all spec front matter, resolves local Markdown file links and anchors, and checks fences/trailing whitespace |
| Identity compatibility and integration | BLOCKED | B-01; ADR-104/platform evidence absent; no platform integration was exercised |
| Mandatory quality acceptance criteria | BLOCKED | B-02/B-03; compliance and accessibility requirements need authorized definition |
| Booking and roster business semantics | BLOCKED | B-04/B-05; proposed rules need product decisions |
| Runtime FR/NFR acceptance, performance, privacy enforcement, accessibility and compliance controls | NOT_RUN | No implementation, deployed environment, credentials, or approved quality test criteria supplied; architecture coverage is not runtime evidence |
| Repository-defined gates | NOT_RUN | None supplied; documentation checks below are supplemental, not a substitute for future implementation gates |

## Reproducible documentation check

Run from the project root. This command completed successfully on the candidate above. Manual policy/design review is recorded separately in the table; the script does not prove those semantic findings.

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import re
import yaml

root = Path('docs/specs')
expected = {
    'prd/PRD-001.md': '4069b2181cdffd5c24900d596981044544301abc44d85ea9db52b02ab7a26ffb',
    'policy/POL-001.md': 'd72a0123479999d2d9e03453f89725b7bccb1bacba5f681c36d0e5a116d66602',
    'architecture/ARCH-001.md': '90d98545cee20da00285c76e188e62b4741a6be827a609e46d0c52528393482d',
    'adr/ADR-001.md': '39e05eca3a48fb835b50eacf8544f5f2e8721a590adb592692721d9161b133ea',
}
for name, digest in expected.items():
    path = root / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
    assert yaml.safe_load(path.read_text().split('---', 2)[1])['id'] == path.stem
print('PASS: source/candidate hashes and four YAML front-matter blocks')

prd = (root / 'prd/PRD-001.md').read_text()
arch = (root / 'architecture/ARCH-001.md').read_text()
ids = re.findall(r'^  - id: ((?:FR|NFR)-\d+)$', prd, re.M)
rows = re.findall(r'^\| ((?:FR|NFR)-\d+):.*$', arch, re.M)
assert len(ids) == 7 and sorted(ids) == sorted(rows)
for line in arch.splitlines():
    if re.match(r'^\| (?:FR|NFR)-\d+:', line):
        cells = line.split('|')
        assert len(cells) == 7 and cells[4].strip().startswith('BLOCKED:')
        assert cells[5].strip()
for bid in ['B-01', 'B-02', 'B-03', 'B-04', 'B-05']:
    assert re.search(r'^\| ' + bid + r' \|', arch, re.M), bid
print('PASS: seven readiness/evidence rows and five blocker definitions')

def anchors(text):
    headings = re.findall(r'^#{1,6} (.+)$', text, re.M)
    return {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings}

paths = [root / 'architecture/ARCH-001.md', root / 'adr/ADR-001.md',
         root / 'architecture/PRD-001-verification.md']
for path in paths:
    text = path.read_text()
    assert len(re.findall(r'^```', text, re.M)) % 2 == 0, path
    assert all(line == line.rstrip() for line in text.splitlines()), path
    for target in re.findall(r'\]\(([^)\n]+)\)', text):
        name, _, anchor = target.partition('#')
        linked = path.parent / name if name else path
        assert linked.is_file(), (path, target)
        if anchor:
            assert anchor in anchors(linked.read_text()), (path, target)
print('PASS: local links/anchors, code fences and whitespace in three new documents')
PY
```

The first full documentation-check run failed because its fence counter counted a literal backtick sequence inside its own code sample. The checker was corrected to count fence lines, and the complete command above was rerun. No acceptance criterion or requirement was changed.

No requirement has a runtime PASS. Epic-readiness blockers remain open as explicitly listed in ARCH-001; completing this architecture assessment does not close them.
