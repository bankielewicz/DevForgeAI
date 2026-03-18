# Phase A07: Audit Display

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=A06 --to=A07 --workflow=doc-audit
# Exit 0: proceed | Exit 1: Phase A06 incomplete
```

## Contract

PURPOSE: Display the audit summary report with scorecard, top findings, and next steps. Finalize audit workflow and EXIT.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Summary report displayed, session finalized
STEP COUNT: 2 mandatory steps

---

## Mandatory Steps

### Step A07.1: Display Audit Summary

EXECUTE: Display the formatted audit report.
```
total_score = score_tone + score_ia + score_visual + score_onboard
max_score = 40

Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Documentation Audit Complete"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "Session: {SESSION_ID}"
Display: "Overall Score: {total_score}/{max_score}"
Display: ""
Display: "Scorecard:"
Display: "  Tone & Personality:       {score_tone}/10 — {key_blocker_tone}"
Display: "  Information Architecture:  {score_ia}/10 — {key_blocker_ia}"
Display: "  Visual Design:            {score_visual}/10 — {key_blocker_visual}"
Display: "  Onboarding Friction:      {score_onboard}/10 — {key_blocker_onboard}"
Display: ""
Display: "Findings: {counts['CRITICAL']} CRITICAL, {counts['HIGH']} HIGH, {counts['MEDIUM']} MEDIUM, {counts['LOW']} LOW"
Display: ""

# Display top findings (up to 10)
Display: "Top findings:"
FOR each finding in findings[:10]:
    Display: "  {finding.id} [{finding.severity}] {finding.summary}"
    Display: "    Fix: {finding.fix_mode} — {finding.fix_action}"

IF len(findings) > 10:
    Display: "  ... and {len(findings) - 10} more (see doc-audit.json)"

Display: ""
Display: "Next Steps:"
Display: "  /document --audit-fix --type=all       Apply all fixes"
Display: "  /document --audit-fix --type=license    Fix license only"
Display: "  /document --audit-fix --type=tone       Fix tone only"
Display: "  /document --audit-fix --finding=F-001   Fix single finding"
Display: ""
Display: "Audit saved: devforgeai/qa/audit/doc-audit.json"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
VERIFY: Report displayed with scorecard, findings, and next steps.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A07 --step=A07.1 --workflow=doc-audit`

---

### Step A07.2: Finalize Audit Session

EXECUTE: Mark session as complete and validate phase count.
```
checkpoint = Read(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json")
checkpoint.current_phase = "COMPLETE"
checkpoint.completed_at = current_timestamp
checkpoint.phases_completed.append("A07")
checkpoint.result = "SUCCESS"
checkpoint.total_score = total_score
checkpoint.finding_count = len(findings)

Write(file_path="devforgeai/workflows/${SESSION_ID}-checkpoint.json", content=JSON(checkpoint))

# Validate all audit phases completed
completed_count = len(checkpoint.phases_completed)
EXPECTED_COUNT = 7  # 01, 02, A03-A07

IF completed_count < EXPECTED_COUNT:
    Display: "WARNING: Only {completed_count}/{EXPECTED_COUNT} phases completed"
ELSE:
    Display: "All {EXPECTED_COUNT} phases completed - Audit workflow passed"
```
VERIFY: Checkpoint shows result = "SUCCESS" and COMPLETE status.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A07 --step=A07.2 --workflow=doc-audit`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=A07 --checkpoint-passed --workflow=doc-audit
```

## Phase Transition Display

```
Display: ""
Display: "Audit workflow complete. EXIT."
Display: ""
```

**EXIT after this phase. Do not proceed to any generation or fix phases.**
