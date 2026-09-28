# PRD-001 architecture verification

Candidate: documentation working tree dated 2026-09-28. No usable Git metadata
is present, so verification identifies the files by SHA-256 rather than commit.

Scope: [ARCH-001](ARCH-001.md), [ADR-001](../adr/ADR-001.md), and
[ADR-002](../adr/ADR-002.md), derived from the two supplied approved sources.

## Document checks

Command: `python3 /tmp/verify_prd001_architecture.py` (session-local checker).
Result: exit 0; all five check groups passed. This checks document structure and
traceability, not runtime correctness or architecture approval.

| Check | Result | Evidence |
|---|---|---|
| Approved source preservation | PASS | Both source hashes match their pre-edit values. |
| Requirement coverage | PASS | Exactly one readiness row for each of FR-001–FR-003 and NFR-001–NFR-004. |
| Matrix completeness | PASS | Each row has design, drafting status, dependencies, and proposed acceptance evidence. |
| Document integrity | PASS | Local Markdown file links resolve; document IDs are unique; fenced blocks balance. |
| Policy/gate recording | PASS | SET-01/SET-02 cited; G-01–G-05 each defined once; both ADRs remain proposed with no claimed approval. |
| Policy interpretation review | PASS | Mandated identity authority retained; personal Google constraint retained; no unsupported federation claim; compliance/accessibility apply to the internal pilot. |
| Scope review | PASS | No code, epics, external actions, or approved-source edits; roster freshness and missing operational definitions are explicit gates. |

The last two checks are document review against the supplied PRD and policy,
not assertions from an automated semantic validator. No repository schema or
Markdown validator is supplied, so conformance to an external document schema
is NOT_RUN.

## Requirement acceptance evidence

The PRD supplies requirement statements, not a separate acceptance-test suite.
ARCH-001 proposes evidence for every statement without claiming it has passed.

| Requirement | Runtime verification | Unresolved finding |
|---|---|---|
| FR-001 | NOT_RUN | Identity platform contract and Google federation unverified (G-01). |
| FR-002 | NOT_RUN | No implementation; eligibility/open-shift semantics pending G-04 and identity dependency unresolved. |
| FR-003 | NOT_RUN | No implementation; local-day/role definitions and freshness pending G-04/G-05. |
| NFR-001 | NOT_RUN | No revocation integration or measured five-minute test; G-01 unresolved. |
| NFR-002 | NOT_RUN | No endpoints or response/cache/log paths to test; role and data provisioning pending G-04. |
| NFR-003 | NOT_RUN | No hosted deployment inventory or restore evidence. |
| NFR-004 | NOT_RUN | No demonstrated personal Google sign-in through Org A (G-01). |
| Product-wide epic readiness | BLOCKED | Mandatory compliance and accessibility acceptance criteria absent (G-02/G-03). |
| Identity decision finalization | BLOCKED | ADR-104/platform contract absent; no product policy override allowed (G-01). |

No behavioral change was made, so a TDD failing test was not applicable. Runtime
tests and repository-required gates could not be run: no application, test runner,
validation scripts, or gate definitions exist in the supplied workspace.
`git status --short` reported “not a git repository”; no commit/diff evidence is
claimed. No failed runtime tests are hidden behind document-check PASS results.

## Candidate fingerprints

These hashes identify the actual source and design files checked. The report is
excluded from its own fingerprint set to avoid a self-referential hash.

| File | SHA-256 |
|---|---|
| PRD-001.md | `4069b2181cdffd5c24900d596981044544301abc44d85ea9db52b02ab7a26ffb` |
| POL-001.md | `d72a0123479999d2d9e03453f89725b7bccb1bacba5f681c36d0e5a116d66602` |
| ARCH-001.md | `3b3dc828b7fe18cacf845dae2bd3a1ddd9923b708aaa312291f4f07d28a19628` |
| ADR-001.md | `3273726899ff53e87f8817cbbca2eca70732ac1a935f6fb9ce62cdc12dbd00a8` |
| ADR-002.md | `11db5761d660a852255c46b24370ac7fd993e2e7173840859968b22455cc87ac` |
