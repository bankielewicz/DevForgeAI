# Template: Checkpoint

**Producer:** any product workflow on interrupt, stop, or remaining work (`dev`, `qa`, and planned cores)  
**Consumers:** the **same** workflow on resume  
**Operational analog:** `src/agents/skills/dev/assets/checkpoint.md`  
**Does not:** complete the work item, override unmet authority predicates, or authorize replaying uncertain effects.

## Envelope

| Field | Value |
| --- | --- |
| Checkpoint ID / UTC | |
| Workflow | discover / specify / architect / story-create / dev / qa / release / … |
| Producer | [skill that stopped] |
| Downstream consumer | same skill on resume |
| Failure behavior | Stale candidate or changed hashes → invalidate affected claims |
| Non-claims | Navigation aid, not current truth; not COMPLETE |

## Resume keys

| Item | Value |
| --- | --- |
| Selected project / root | |
| Authorization / scope references | |
| Governing contract versions / hashes | |
| Requirement / story / defect IDs still in play | |
| Last identified candidate | |
| Evidence locators and limitations | |
| Open decisions and affected dependencies | |
| Owned jobs / processes / fixtures | |
| Next **safe** action | |

Exclude credentials and unnecessary private data.

## Validity checks on resume

1. Reread this checkpoint and the cited contracts.
2. Recompute relevant source / plan / candidate hashes.
3. If bytes changed, mark previously bound claims historical; do not treat them as current qualification.
4. Do not automatically repeat a failed or uncertain-effect command.
5. Protected work, when applicable, resumes from Rust-owned state — a checkpoint marked complete cannot override unmet predicates.
6. An ended session neither completes nor cancels the selected obligation.

## Downstream handoff

Resume continues the **same** selected objective unless the user changes it. Additional verification (“also test Linux”) adds obligations; it does not discard an unresolved repair.

**Return path:** none. If the wrong workflow would consume this file, stop and report the mismatch.
