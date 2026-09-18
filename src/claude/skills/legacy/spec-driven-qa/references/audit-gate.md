# QA Audit Gate Behavior Reference (Plan D2 / ADR-059)

**Used by:** `spec-driven-qa` SKILL.md EXIT GATE step (5.a) — `devforgeai-validate audit-gate ${STORY_ID} --workflow=qa --phase={phase_id}`
**Source of truth:** `audit-policy.yaml` (in this skill directory)
**Shared canonical:** `src/claude/scripts/devforgeai_cli/audit/README.md` (behavior matrix, failure recovery, bypass procedure — workflow-agnostic)
**ADR:** `devforgeai/specs/adrs/ADR-059-spec-driven-qa-audit-integration.md`

This is a thin pointer per code-reviewer Q5. QA-specific carve-outs only; defer operational details to the shared canonical.

## Per-phase audit summary (canonical source: `audit-policy.yaml`)

| Phase | Audit | Mode | Fail Mode | What is verified |
|---|---|---|---|---|
| 01 Setup | No | — | — | Pre-flight; no findings |
| 02 Validation | Yes | single | closed | Coverage `uncovered_lines` cite real file:lines |
| 03 Diff Regression | Yes | single | closed | Regression findings match git diff hunks (RCA-046 forcing function) |
| 04 Analysis | Yes | single | **open** | Subagent INVOCATION + OUTPUT PRESERVATION only |
| 05 Reporting | Yes | consensus_when_available | closed | gaps.json fidelity per `qa-output-fidelity.md` + ADR-010 |
| 06 Cleanup | No | — | — | Terminal phase |

## QA-specific carve-outs (must NOT verify)

- **Phase 04 audit MUST NOT** re-derive deferral severity (deferral-validator authoritative; mirrors dev Phase 06)
- **Phase 04 audit MUST NOT** contradict deferral-validator JSON output
- **Phase 04 audit MUST NOT** downgrade test-integrity verdicts to environmental causes (CLAUDE.md HALT trigger #10)
- **Phase 05 audit MUST NOT** re-derive severity classification
- **Phase 05 audit MUST NOT** override deferral-validator semantic verdicts; transcription fidelity ONLY

## Asymmetric semantics (vs dev workflow)

- **Fixture path namespace:** dev uses `devforgeai/audit/phases/<STORY>-phase<NN>/`; QA uses `devforgeai/audit/qa/<STORY>-phase<NN>/` (Plan D2 D2 — symmetric move deferred)
- **REMEDIATION_MODE:** dev `respect_remediation_mode=true` (audit skipped during /dev --fix); QA `respect_remediation_mode=false` — QA NEVER bypasses audit because adversarial verification is QA's purpose (Plan D2 D13)
- **Light mode:** QA `light_mode_audit=false` — audit gate fires only in deep mode

## Cross-references

- **Behavior matrix, failure recovery, bypass procedure:** `src/claude/scripts/devforgeai_cli/audit/README.md`
- **Audit gate technical reference (post-Plan-D):** `docs/gates/audit-gate-reference.md`
- **QA output fidelity rule:** `.claude/rules/workflow/qa-output-fidelity.md`
- **ADR-058 (precedent):** `devforgeai/specs/adrs/ADR-058-spec-driven-dev-audit-integration.md`
- **ADR-059 (this gate):** `devforgeai/specs/adrs/ADR-059-spec-driven-qa-audit-integration.md`
- **Sibling dev reference:** `src/claude/skills/spec-driven-dev/references/audit-gate.md`
