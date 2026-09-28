# VERIFY-001 — PRD-001 architecture verification

Date: 2026-09-28. Scope: the local document candidate, not implemented software.

## Results

| Check | Result | Evidence or limitation |
|---|---|---|
| Approved input preserved | PASS | PRD-001 SHA-256 remains `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef`. |
| Requirement coverage | PASS | The structural check below finds exactly one readiness row for each of the six PRD requirements. ARCH-001 sections 2–5 describe mechanisms, boundaries, dependencies, and acceptance evidence. |
| FR-001 epic readiness | BLOCKED | ADR-001 records the unresolved provider/enrollment/recovery decision and its exit criteria. The generic session contract does not resolve provider-specific sign-in. |
| FR-002 epic readiness | PASS | Architecture defines open-shift defaults, atomic capacity enforcement, uniqueness, request outcomes, and the FR-001 delivery dependency. |
| FR-003 epic readiness | PASS | Architecture defines coordinator authorization, roster projection, date boundaries, freshness defaults, and delivery dependencies. |
| NFR-001 epic criteria | PASS | Session-generation checks, atomic revocation, failure behavior, multi-instance/in-flight coverage, and the 300-second test bound are defined. Applies to all authenticated features. |
| NFR-002 epic criteria | PASS | Coordinator-only disclosure is specified across responses, contact queries, role grants, caches, logs, and provider integration. |
| NFR-003 epic criteria | PASS | Hosted operation covers the entire system and is inherited by every delivery epic. |
| Local links and document structure | PASS | The structural check below verifies local file targets, unique document IDs, and balanced code fences. |
| Product acceptance tests, all six requirements | NOT_RUN | No application, deployed provider, executable tests, or test configuration was supplied. Planned tests in ARCH-001 are not passing-test evidence. |
| Repository quality gates | NOT_RUN | No AGENTS.md, validation scripts, or quality-gate configuration exists in the supplied workspace. Documentation-only work changes no executable behavior; failing-test-first TDD does not apply. |
| Git diff/revision evidence | NOT_RUN | `git status --short` returned “not a git repository.” Candidate evidence therefore uses file hashes and local content checks. |

The first interpreter probe used `python` and failed because it is unavailable.
Verification uses the available `/usr/bin/python3` and standard library only.

## Reproducible structural check

Run from the workspace root. This checks document consistency, not security or
runtime correctness. Semantic readiness judgments are explained in ARCH-001's
coverage table and ADR-001; they are not inferred from this script alone.

```python
from pathlib import Path
import hashlib
import re

root = Path.cwd()
prd = root / "docs/specs/prd/PRD-001.md"
arch = root / "docs/specs/architecture/ARCH-001.md"
adr = root / "docs/specs/adr/ADR-001.md"
report = root / "docs/specs/architecture/VERIFY-001.md"
expected_prd_hash = "73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef"
assert hashlib.sha256(prd.read_bytes()).hexdigest() == expected_prd_hash
requirements = re.findall(r"^  - id: ((?:FR|NFR)-\d+)$", prd.read_text(), re.M)
rows = re.findall(r"^\| ((?:FR|NFR)-\d+) \|.*$", arch.read_text(), re.M)
assert len(requirements) == 6
assert len(rows) == len(set(rows)) == len(requirements)
assert set(rows) == set(requirements)
assert re.search(r"^\| FR-001 \|.*\| BLOCKED \|", arch.read_text(), re.M)
for requirement in ("FR-002", "FR-003", "NFR-001", "NFR-002", "NFR-003"):
    assert re.search(r"^\| " + requirement + r" \|.*\| READY", arch.read_text(), re.M)
for path, doc_id in ((prd, "PRD-001"), (arch, "ARCH-001"), (adr, "ADR-001")):
    assert re.findall(r"^id: (.+)$", path.read_text(), re.M) == [doc_id]
for path in (prd, arch, adr, report):
    contents = path.read_text()
    assert len(re.findall(r"^```", contents, re.M)) % 2 == 0, path
    prose = re.sub(r"```.*?```", "", contents, flags=re.S)
    for target in re.findall(r"\]\(([^)]+)\)", prose):
        if not target.startswith(("https://", "http://", "#")):
            assert (path.parent / target.split("#")[0]).is_file(), (path, target)
for path in (prd, arch, adr):
    print(hashlib.sha256(path.read_bytes()).hexdigest(), path.relative_to(root))
print("PASS: input preserved; 6/6 requirement rows; readiness labels; IDs; fences; local links")
```

Execution command (runs the exact check above):

```sh
python3 - <<'PY'
from pathlib import Path
import re
report = Path("docs/specs/architecture/VERIFY-001.md").read_text()
check = re.search(r"```python\n(.*?)\n```", report, re.S).group(1)
exec(compile(check, "VERIFY-001 structural check", "exec"))
PY
```

Observed result: exit code 0. Changes to architecture or ADR content require
rerunning the check.

```text
73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef docs/specs/prd/PRD-001.md
3704d08a087a77ab28b07f28b376f2ec2a4aa77883d439574ecc913848f86098 docs/specs/architecture/ARCH-001.md
347d308b402b2998d5de4c2c1b556dcdeb04e552ae61e6aa882d334f7125c93c docs/specs/adr/ADR-001.md
PASS: input preserved; 6/6 requirement rows; readiness labels; IDs; fences; local links
```
