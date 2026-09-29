# ADD-001 verification record

Candidate: the documentation working tree dated 2026-09-28. This workspace has an
empty `.git` directory rather than a usable Git repository, so no revision SHA is
available. Scope is [ADD-001](ADD-001.md), [ADR-001](../adr/ADR-001.md), and this record.
The approved [PRD-001](../prd/PRD-001.md) remains unchanged.

## Evidence

| Check | Status | Evidence / outcome |
|---|---|---|
| Approved source preserved | PASS | SHA-256 matches the value captured before editing; PRD contents and generated epic-map placeholder are unchanged. |
| Requirement traceability and readiness | PASS | Parsed all active/current PRD requirements; all six appear once in the readiness matrix with ownership, disposition, and future verification criteria, and all six have upstream references. |
| Frontmatter and local document links | PASS | YAML parses; ADD remains draft, ADR remains proposed, no approval is fabricated; all eight local links resolve and code fences balance. |
| FR-001 design review | PASS | Identity adapter contract, explicit unresolved ADR, bounded resolution work, and delivery dependencies are recorded. This is not a passing sign-in test. |
| FR-002 design review | PASS | Transaction boundary, final-place concurrency, uniqueness, retry behavior, and session-actor binding are defined. |
| FR-003 design review | PASS | Coordinator boundary, committed-data source, local-day calculation, refresh behavior, and privacy projection are defined. |
| NFR-001 design review | PASS | Shared session generation, per-request primary-store validation, fail-closed behavior, issuance/revocation serialization, and bounded in-flight work address the five-minute requirement. |
| NFR-002 design review | PASS | Coordinator-only phone projection covers server responses, page data, logs, caches, and administrator-only access; the permission matrix includes negative tests. |
| NFR-003 design review | PASS | All runtime components are hosted; every functional epic explicitly inherits the constraint. |
| Repository-defined gates and implementation tests | NOT_RUN | No source code, test configuration, validation scripts, or repository instructions were supplied. No behavior was changed; TDD red/green does not apply to these documentation additions. |
| Provider-specific FR-001 readiness | BLOCKED | ADR-001 is proposed; provider, sign-in method, and account lifecycle evidence are missing. |

Commands run from the project root:

- `rg --files --hidden` and `ls -la .agents .codex .git docs docs/specs docs/specs/prd`: source inventory; only the PRD was initially present.
- `git status --short`: exit 128, no usable Git repository. Verification therefore identifies document content by hash.
- `sha256sum docs/specs/prd/PRD-001.md`: captured the approved source hash before changes.
- `python3 /tmp/validate_prd001_architecture.py`: exit 0. Temporary validation script uses PyYAML and checks source preservation, metadata, upstream references, exact six-row coverage, readiness dispositions, links, and balanced fences.
- `sed -n '1,280p' docs/specs/add/ADD-001.md` and `sed -n '1,180p' docs/specs/adr/ADR-001.md`: read the candidate documents for the manual design review above.

Verified content hashes (SHA-256):

```text
73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef  docs/specs/prd/PRD-001.md
de228f35abe55e11742fa65c39e789c5dae63b36fb916dd9845019667e0f8d9f  docs/specs/add/ADD-001.md
32b78025a346bb824d5f7552331dfa5a5a023fe7f83e9585be680abbc46697c6  docs/specs/adr/ADR-001.md
```

## Remaining evidence for implementation

All implementation acceptance tests in ADD-001 section 8 are **NOT_RUN**. Session
revocation, privacy, concurrency, mobile sign-in, roster freshness, and hosted
deployment have design coverage only. No provider experiment or deployed application
exists in this workspace. Follow the criteria in that matrix when creating epics.

NFR-003 must be inherited by every epic because it governs the whole product.
FR-002/003 delivery depends on FR-001 even though their epic definitions can proceed.
Proposed booking semantics, timezone configuration, roster polling target, operator
setup, and operational settings must be carried into planning as documented in
ADD-001 section 7. The architecture is draft and has no recorded human approval.
