# ARCH-001 verification — 2026-09-28

This record covers the documentation candidate, not a running product. Sources were PRD-001 v1 and accepted ADR-001 v1. Discovery with `rg --files --hidden -g '!.git/**'` found no application, test runner, validation scripts or repository instructions. `.agents` and `.codex` were empty. `git status --short` exited 128 because `.git` is an empty directory; no commit identity or Git diff is available.

## Checks and outcomes

| Check | Result | Evidence |
|---|---|---|
| Preserve authorized requirements and accepted decision | PASS | SHA-256 comparison to the files read before editing; PRD-001 and ADR-001 unchanged |
| Define architecture for all six active requirements | PASS | ARCH-001 boundaries, data contracts, decision register and six-row readiness matrix; ADR-002 covers identity/revocation, ADR-003 privacy, ADR-004 hosting/booking/roster |
| Record truthful decision status and traceability | PASS | Parsed YAML for six specification files; unique IDs and valid PRD v1 item references; all new ADRs proposed with null approval fields |
| Identify material uncertainties | PASS | G1–G4 name closure evidence and proposed owners; NFR-003 propagates globally; ADR-001 is not treated as an identity decision |
| Local document links | PASS | Final structural validation resolves every relative Markdown document link |
| Committed-epic readiness | BLOCKED | All six requirements have unresolved gates as enumerated in ARCH-001; architecture proposals are available for outlining epics |
| Product behavior acceptance | NOT_RUN | No code or harness exists; per-requirement scenarios are specified in ARCH-001 and the ADR confirmation sections |
| Repository test/coverage gates | NOT_RUN | No repository commands, thresholds or TDD policy files were supplied; no runtime behavior changed |

The first structural check passed preservation and metadata checks but failed because this verification file had not yet been created. After adding the file, the same command was rerun. That intermediate failure was a documentation-link failure, not a runtime TDD result.

Validation command: `python3 /tmp/verify_prd001_architecture.py` (local validation helper, not a product test). It compares source hashes, parses YAML, checks unique IDs and upstream items, verifies proposal status without invented approvals, checks coverage and exactly one readiness row for each of the six active requirements, and resolves relative document links. Final output:

```text
PASS: original PRD-001 and ADR-001 preserved byte-for-byte
PASS: YAML, unique IDs, upstream references, proposal statuses, and six-requirement coverage
PASS: explicit readiness for all six requirements and local document links
```

Manual review checked the decision substance beyond reference presence: five-minute revocation has a database enforcement mechanism; phone restriction is server-side and distinguishes administrator from coordinator; hosted deployment includes identity, database and logging; roster derives from committed bookings; domain assumptions are identified rather than attributed to the PRD.

## Candidate fingerprint

Command: `sha256sum docs/specs/architecture/ARCH-001.md docs/specs/adr/ADR-002.md docs/specs/adr/ADR-003.md docs/specs/adr/ADR-004.md`. The verification record itself is excluded to avoid a self-referential hash.

| File | SHA-256 |
|---|---|
| PRD-001.md (unchanged input) | `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef` |
| ADR-001.md (unchanged input) | `da5b0578a29e00157f3e22966f538c0f45bd4d0469912df3344b4fa2e2a7d259` |
| ARCH-001.md | `8ec20d2dfd08498cd5393fe8270e796d728b8a572bdbe48f44d9a939810f58c4` |
| ADR-002.md | `ccc4b91c15819307f7913d336a217f4812a9b39f83a448237c8ab428eef35eab` |
| ADR-003.md | `0b9a2a3a02bdfe47e93b99f57869557712e23c8ffb6e4ebad524089ea3bfa710` |
| ADR-004.md | `2ff189e3a7b241ee0c6fb48bb097f104e4f9c95aebe54d1fbd77f9dff81baceb` |

## Unresolved findings

- G1: hosting provider/plan and budget compatibility with accepted 30-day native log retention.
- G2: identity provider acceptance, tenant ownership, volunteer enrollment/recovery and fresh-authentication behavior.
- G3: privacy decision acceptance, role assignments and operational contact custody.
- G4: shift capacity/open-state rules, provisioning and food-bank timezone.
- Upstream BRN-001 and validation of ASM-01 are unavailable; the approved PRD remains the task authority.

No requirement, test threshold or existing decision was weakened to report a pass. Structural PASS results do not clear the epic gates or establish runtime compliance.
