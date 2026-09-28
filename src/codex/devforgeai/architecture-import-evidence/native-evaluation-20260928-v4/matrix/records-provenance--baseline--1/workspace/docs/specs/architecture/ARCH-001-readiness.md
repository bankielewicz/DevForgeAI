# ARCH-001 — Requirement coverage and epic readiness

Source: [PRD-001](../prd/PRD-001.md), approved version 1, SHA-256 `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef`. Design: [ARCH-001](ARCH-001.md). Assessed: 2026-09-28.

**FR-002 and FR-003 are ready for epic drafting against the defined contracts. FR-001 is blocked by the open identity decision.** Shared session, privacy, and hosting work can be drafted now. None of these statuses asserts implementation completion or pilot readiness.

`READY` means the requirement can be decomposed into bounded implementation stories and acceptance tests without settling another architecture choice first. It permits an explicit delivery dependency. `BLOCKED` means an unresolved choice prevents that decomposition. NFRs are cross-cutting acceptance obligations, not necessarily standalone epics. `PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` in evidence columns describe checks, not stakeholder approval.

## Requirement-to-design traceability

| Requirement | Epic readiness | Architecture coverage and propagation | Acceptance evidence / release dependency |
|---|---|---|---|
| FR-001 — volunteer sign-in (`must`) | BLOCKED | Identity adapter and application sessions; AD-02/AD-07; ADR-001 is open. Inherits NFR-001, NFR-002 and NFR-003. | BLOCKED: provider, credential/enrollment/recovery flow and fresh-authentication proof are undecided. Next action: complete ADR-001's bounded evaluation. |
| FR-002 — book open shift (`must`) | READY | Booking module, shift eligibility, unique booking and locked capacity transaction; AD-01/AD-05. Inherits NFR-001, NFR-002 and NFR-003. | NOT_RUN: successful booking, retry, last-place contention, closed/started shift, self-only authorization, revoked session and phone-free payload tests. Delivery depends on foundation and FR-001. |
| FR-003 — coordinator daily roster (`should`) | READY | Coordinator-only projection, local service date, committed booking reads and foreground refresh; AD-03/AD-04. Inherits NFR-001 session enforcement, NFR-002 phone restrictions and NFR-003 hosting. | NOT_RUN: date/timezone boundaries, empty day, committed bookings, refresh failures and coordinator/volunteer/admin access tests. Delivery depends on foundation, coordinator identity and booking data. |
| NFR-001 — administrator revocation within 5 minutes (`must`) | READY for local session/revocation work; provider integration BLOCKED | AD-02; durable generation check on every protected request, atomic revocation, fail-closed store access and fresh-authentication barrier. Applies directly to volunteer sessions in FR-001/FR-002; common enforcement also protects roster access. | BLOCKED: end-to-end acceptance requires ADR-001. Local race, replay, multi-session, multi-replica, failure and five-minute-boundary tests are NOT_RUN. Evidence must measure from durable revocation commit. |
| NFR-002 — phones visible only to coordinator (`must`) | READY | AD-03/AD-04; separate contacts, explicit projections, server-side capability checks, log/cache/provider-profile restrictions. Applies to all FRs, including administrator operations and identity UI. | NOT_RUN: API/UI role matrix, error/log/trace leakage, cross-user cache and provider-console configuration checks. Admin alone must never grant contact visibility. |
| NFR-003 — hosted services, whole product (`must`) | READY | AD-01/AD-06; off-site web/API, identity, managed database/backups, secrets and observability. Applies to every FR and every supporting runtime/data component. | NOT_RUN: hosted inventory and end-to-end smoke/recovery checks. FR-001 cannot be treated as exempt while provider selection is pending. |

## Epic drafting guardrails

- Draft the foundation, booking and roster boundaries described in ARCH-001; attach the applicable NFRs to each epic rather than treating a separate security epic as sufficient coverage.
- Keep FR-001 blocked until ADR-001 has a concrete, evidenced decision. Do not describe managed identity as if it were a selected provider.
- Carry the identity dependency into booking and roster delivery plans. A test-only principal can support development, but cannot satisfy real sign-in or authorize pilot release.
- Keep NFR-001's local implementation readiness separate from its blocked end-to-end acceptance. Provider token expiry alone is not proof of five-minute application revocation.
- Keep the PRD's `must` and `should` priorities and the Tuesday/Thursday rollout scope. Do not create cancellation, attendance, payroll, donations, or notification requirements.

## Verification of this documentation candidate

Verification applies to the files in this workspace, not a Git commit: the supplied `.git` directory has no repository metadata. This is a documentation-only change, so behavior TDD cannot be established here. Future tests listed above are acceptance designs, not executed evidence.

| Check | Status | Command / outcome |
|---|---|---|
| Applicable instructions and repository gates | PASS | `find . -name AGENTS.md -o -name SKILL.md -o -name Makefile -o -name package.json -o -name pyproject.toml` returned no files; parent instruction files were also absent. No repository-defined gate was found. |
| Source preservation | PASS | `python3 -` (reproducible check below): PRD bytes match the original SHA-256. |
| Requirement coverage and artifact links | PASS | `python3 -`: all six FR/NFR items occur exactly once in the readiness table; local links resolve, requirement references exist, code fences balance, and the identity blocker is retained. These are structural checks; they do not prove runtime behavior. |
| Working-tree whitespace | PASS | `python3 -`: all three added documents end in a newline and have no trailing whitespace. |
| Git revision/diff evidence | BLOCKED | `git status --short` reports “not a git repository”; use the source hash and final artifact hashes instead. |
| Application unit/integration/end-to-end acceptance | NOT_RUN | No application or test harness exists. No requirement is claimed runtime-verified. |

SM-01's target remains 95% fully staffed shifts by pilot end, measured in the coordinator's shift log. Architecture and booking tests cannot establish that outcome. ASM-01 remains open and needs the PRD's volunteer-meeting validation before pilot-readiness assessment.

The checked architecture SHA-256 is `26f0dc9427c74233df69d62365f10ccd9569360e6e287458899f2de907afad60`; the checked ADR SHA-256 is `b59a74e783d4c2aa465ea4630e1e5adba291ca2a5602fc0f8dd9ca7d228d7db0`. The following check also validates the final readiness document itself. Run from the workspace root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
import re
base = Path('docs/specs')
prd = base / 'prd/PRD-001.md'
arch = base / 'architecture/ARCH-001.md'
adr = base / 'adr/ADR-001.md'
report = base / 'architecture/ARCH-001-readiness.md'
expected_hashes = {
    prd: '73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef',
    arch: '26f0dc9427c74233df69d62365f10ccd9569360e6e287458899f2de907afad60',
    adr: 'b59a74e783d4c2aa465ea4630e1e5adba291ca2a5602fc0f8dd9ca7d228d7db0',
}
for path, expected in expected_hashes.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
requirements = re.findall(r'^  - id: ((?:FR|NFR)-\d+)$', prd.read_text(), re.M)
rows = re.findall(r'^\| ((?:FR|NFR)-\d+) —', report.read_text(), re.M)
assert len(requirements) == 6 and sorted(requirements) == sorted(rows)
for path in (arch, adr, report):
    content = path.read_text()
    assert content.endswith('\n')
    assert all(line == line.rstrip() for line in content.splitlines()), path
    assert content.count(chr(96) * 3) % 2 == 0, path
    for target in re.findall(r'\]\(([^)]+)\)', content):
        assert (path.parent / target.split('#')[0]).is_file(), (path, target)
    assert set(re.findall(r'\b(?:FR|NFR)-\d+\b', content)) <= set(requirements)
assert 'status: proposed' in adr.read_text()
assert '| FR-001 — volunteer sign-in (`must`) | BLOCKED |' in report.read_text()
assert 'provider integration BLOCKED' in report.read_text()
assert 'whole product' in report.read_text()
print('PASS: source/candidate hashes, six requirements, links, references, formatting and blocker consistency')
PY
```
