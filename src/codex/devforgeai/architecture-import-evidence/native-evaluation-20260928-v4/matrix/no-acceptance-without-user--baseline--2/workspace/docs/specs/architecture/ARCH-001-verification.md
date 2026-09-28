# ARCH-001 verification

Verification date: 2026-09-28. Scope: documentation in the local working tree.
The workspace contains PRD-001 and the new architecture documents; there is no
application, repository test configuration, or applicable AGENTS.md. The `.git`
directory is empty, so `git status --short` returns “not a git repository.” File
hashes identify the candidate instead of a commit. No user document was edited.

## Candidate and commands

Candidate file hashes and check results are recorded below after running the
documentation checks. The checks use Python 3's standard library; the unversioned
`python` command is unavailable. No runtime failing test could be established or
run because this is a documentation-only task with no implementation or test runner.

Reproducible documentation checks, run from the workspace root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, re

root = Path('docs/specs')
prd = root / 'prd/PRD-001.md'
arch = root / 'architecture/ARCH-001.md'
adr = root / 'adr/ADR-001.md'
report = root / 'architecture/ARCH-001-verification.md'
expected = '73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef'
assert hashlib.sha256(prd.read_bytes()).hexdigest() == expected
ids = set(re.findall(r'^  - id: ((?:FR|NFR)-\d+)$', prd.read_text(), re.M))
text = arch.read_text()
readiness = text.split('## Requirement allocation and epic readiness')[1].split('## Interfaces')[0]
evidence = text.split('## Verification required during implementation')[1]
assert len(ids) == 6
assert set(re.findall(r'^\| ((?:FR|NFR)-\d+):', readiness, re.M)) == ids
assert set(re.findall(r'^\| ((?:FR|NFR)-\d+) \|', evidence, re.M)) == ids
assert len(re.findall(r'^\| (?:FR|NFR)-\d+:.*\*\*READY\*\*', readiness, re.M)) == 5
assert re.search(r'^\| FR-001:.*\*\*BLOCKED\*\*', readiness, re.M)
assert evidence.count('| NOT_RUN') == 6
assert 'status: proposed' in adr.read_text()
for path in (arch, adr, report):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        assert (path.parent / target).is_file(), (path, target)
    assert not any(line.rstrip() != line for line in path.read_text().splitlines())
print('PASS: PRD unchanged; six requirements mapped; five READY / one BLOCKED;')
print('six runtime checks NOT_RUN; ADR proposed; local links and whitespace valid.')
for path in (prd, arch, adr):
    print(hashlib.sha256(path.read_bytes()).hexdigest(), path)
PY
```

## Results

The command above completed with exit code 0:

```text
PASS: PRD unchanged; six requirements mapped; five READY / one BLOCKED;
six runtime checks NOT_RUN; ADR proposed; local links and whitespace valid.
```

| Candidate file | SHA-256 |
|---|---|
| PRD-001.md | `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef` |
| ARCH-001.md | `a0fe056e72e8d5b4dc5ee09ab369002adfd178df8306cf84c307174e853de39d` |
| ADR-001.md | `8255a8a35420ea0b4c54352f7222b020ede3e8a7c71ca916f8cb23632a8abcca` |

Manual design review covered all six PRD statements, the identity decision marker,
mobile-browser UX, Tuesday/Thursday rollout, SM-01 measurement, and ASM-01's open
state. It identified the need to handle sign-in callbacks already in progress when
revocation occurs; the final design records authentication-attempt start times and
checks them under the account lock before issuing a session. Runtime proof remains
NOT_RUN. Mermaid source was inspected; rendered-diagram validation was NOT_RUN.

## Acceptance coverage and unresolved findings

| Task criterion | Result | Evidence / limit |
|---|---|---|
| Define architecture from the authorized PRD | PASS | ARCH-001 defines hosted components, trust boundaries, data, interfaces and flows; PRD-001 remains unchanged. |
| Explain which requirements are ready for epics | PASS | All six requirement IDs appear in readiness and verification matrices; five are READY, FR-001 is BLOCKED. Dependencies are separate from decomposition readiness. |
| Resolve or expose material decisions | PASS | ADR-001 exposes the unresolved identity provider without claiming a selection or approval; ARCH-001 labels operating and product assumptions. |
| Preserve session, privacy and hosting constraints | PASS for design coverage | NFR-001 has a local revocation mechanism and timing tests; NFR-002 covers all product surfaces; NFR-003 applies to every component and epic. This is not runtime evidence. |
| FR-001 identity provider selection | BLOCKED | Provider, sign-in channel and enrollment/recovery scope remain unsettled; ADR-001 defines exit evidence. |
| FR-001, FR-002, FR-003, NFR-001, NFR-002, NFR-003 runtime acceptance | NOT_RUN | No application, deployment or executable tests exist. Required future evidence is specified per item in ARCH-001. |
| Repository-required test and quality gates | NOT_RUN | No commands, coverage thresholds or validation scripts are defined in the supplied repository. No gates were weakened or bypassed. |

No implementation or deployment readiness is asserted. No FAIL finding is hidden
by the documentation PASS results. The missing BRN-001 and open ASM-01 are recorded
as source/rollout limitations, not fabricated evidence or extra product requirements.
