# ARC-001 verification record

Date: 2026-09-28. Scope: the document working state identified below, not implemented software. There is no usable Git repository in this workspace, so file hashes identify the candidate. [ARC-001](ARC-001.md) defines readiness; [ADR-001](../adr/ADR-001.md) records the open identity decision.

## Candidate snapshot

| File | SHA-256 |
|---|---|
| PRD-001.md, version 1 | `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef` |
| ARC-001.md, version 1 | `5e41e49215bd7ae0948e80f534a9c0ed1903efd15b27592386db576c1f1d55ca` |
| ADR-001.md, version 1 | `4274aa0e118f022341dc1a9c56a6144d45c23acdf076ae551a4e89a1c22123b7` |

## Checks and evidence

| Acceptance/check | Result | Evidence |
|---|---|---|
| Preserve the approved specification and generated epic map | PASS | PRD SHA-256 equals the pre-edit snapshot; only architecture documents were added |
| Account for every active FR and NFR | PASS | YAML comparison against the PRD finds exactly six unique mapped requirements, with a readiness table and V-01 through V-06 verification scenarios |
| Define boundaries, data, and feature behavior | PASS | Manual review of ARC-001 sections 2–4: hosted modules, session/role boundary, schema invariants, atomic booking and daily roster contract |
| Propagate cross-cutting requirements to epics | PASS | Each FR lists all three NFRs; each NFR covers all FRs; NFR-003 explicitly has whole-product scope |
| Distinguish decomposition readiness from integration and release | PASS | FR-002/FR-003 list FR-001 integration dependencies; section 6 defines readiness and preserves the unresolved identity decision |
| Finalize volunteer sign-in architecture | BLOCKED | ADR-001 remains proposed: provider, usable identity channel, enrollment and recovery are unresolved; FR-001 is not marked ready |
| Record valid references without fabricated approval | PASS | Source IDs, source version/hash, local links and frontmatter checked; architecture is draft and ADR is proposed with no asserted approval |
| Validate FR-001 through FR-003 and NFR-001 through NFR-003 runtime behavior | NOT_RUN | No application, deployment or tests exist. V-01 through V-06 are required future evidence, not passing tests |
| Establish a failing behavior test before implementation | NOT_RUN | Documentation-only task; no product behavior implemented and no test harness is available |
| Run repository-required quality gates | NOT_RUN | No repository instructions, gate scripts or test commands are present; no thresholds were changed |

Commands used from the project root:

```sh
rg --files --hidden --no-ignore docs .agents .codex
git status --short
sha256sum docs/specs/prd/PRD-001.md docs/specs/architecture/ARC-001.md docs/specs/adr/ADR-001.md
python3 /tmp/validate_prd001_architecture.py
```

The file inventory established that only PRD-001 existed before the additions; `.agents` and `.codex` were empty. `git status --short` exited 128 because `.git` contains no repository metadata. The SHA-256 command and the temporary Python/PyYAML validation script exited 0. The script checks source preservation, exact requirement coverage, blockers and dependencies, global constraint propagation, source metadata, local Markdown links, fence balance, planned verification entries, and these candidate hashes. It is a session-local structural check, not a product test or an established repository gate.

## Remaining handoff findings

- Resolve ADR-001 before decomposing the full sign-in epic. Provider-independent booking, roster and shared-control epics may be decomposed now using the documented contracts.
- Carry A-01 through A-06 as explicit assumptions. Confirm pilot shift data, timezone, operational roles and identity-channel access before rollout. Resolve the phone-data infrastructure access boundary in A-05 before loading real phone numbers.
- Require actual runtime evidence for all six requirements before declaring the pilot ready. The approved staffing success metric continues to use the coordinator's shift log.
