# Phase 03: Reporting

## Entry Gate

```bash
devforgeai-validate phase-check W3-AUDIT --workflow=w3-compliance --from=02 --to=03 --project-root=.
# Exit 0: proceed | Exit 1: HALT (Phase 02 not complete)
```

## Contract

PURPOSE: Generate and display the W3 compliance audit report with violation tables, remediation guidance, and formatted output matching other DevForgeAI audit commands.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Formatted report displayed to user
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 3.1: Load Report Template References [MANDATORY]

EXECUTE: Load report template and W3 rules reference files from disk. Do NOT rely on memory of previous reads.
```
Read(file_path="src/claude/skills/spec-driven-w3-compliance/references/report-templates.md")
Read(file_path="src/claude/skills/spec-driven-w3-compliance/references/w3-rules.md")

IF any Read fails:
    HALT -- "Phase reference files not loaded. Cannot proceed."
    Do NOT rely on memory of previous reads. Load ALL references fresh.
```
VERIFY: Both reference files are loaded into context. Content from report-templates.md includes box-drawing report format. Content from w3-rules.md includes remediation guidance.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=03 --step=3.1 --project-root=.`

---

### Step 3.2: Generate and Display Report

EXECUTE: Generate the formatted W3 compliance audit report using violation data from Phase 02. Follow the report template exactly.
```
IF NOT $QUIET:
    # Display report header with box-drawing characters
    Display:
    "╔════════════════════════════════════════════════════════════════════╗"
    "║                    W3 COMPLIANCE AUDIT REPORT                    ║"
    "╠════════════════════════════════════════════════════════════════════╣"
    "║  Scanned: ${TOTAL_FILES} files in .claude/                       ║"
    "║  Violations: {CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT}        ║"
    "║    CRITICAL: ${CRITICAL_COUNT}                                   ║"
    "║    HIGH: ${HIGH_COUNT}                                           ║"
    "║    MEDIUM: ${MEDIUM_COUNT}                                       ║"
    "╚════════════════════════════════════════════════════════════════════╝"

    # Display CRITICAL violations table
    IF CRITICAL_COUNT > 0:
        Display:
        ""
        "## CRITICAL Violations (Block Release)"
        ""
        "| File | Line | Issue |"
        "|------|------|-------|"
        FOR v in subagent_violations:
            "| {v.file} | {v.line} | Subagent invoking Skill() - FORBIDDEN |"
        ""
        "**Action Required:** Subagents CANNOT invoke skills per architecture-constraints.md"

    # Display HIGH violations table
    IF HIGH_COUNT > 0:
        Display:
        ""
        "## HIGH Priority (Review Required)"
        ""
        "| File | Line | Issue |"
        "|------|------|-------|"
        FOR v in skill_violations:
            "| {v.file} | {v.line} | Auto-invokes skill without user approval |"
        ""
        "**Action Required:** Add user consent gate before Skill() OR use display-only pattern"

    # Display MEDIUM violations table
    IF MEDIUM_COUNT > 0:
        Display:
        ""
        "## MEDIUM Priority (Documentation Gap)"
        ""
        "| File | Issue |"
        "|------|-------|"
        FOR f in missing_w3_notes:
            "| {f} | Missing W3 compliance note |"
        ""
        "**Action Required:** Add W3 compliance note explaining invocation pattern"

    # Display clean audit message if no violations
    IF CRITICAL_COUNT == 0 AND HIGH_COUNT == 0 AND MEDIUM_COUNT == 0:
        Display: ""
        Display: "No W3 violations detected. All skill invocations are compliant."

ELSE:
    # Quiet mode: summary only
    Display: "W3 Audit: CRITICAL={CRITICAL_COUNT} HIGH={HIGH_COUNT} MEDIUM={MEDIUM_COUNT}"
```
VERIFY: Report is displayed to user. If $QUIET=false, box-drawing header is visible. All violation tables rendered for non-zero counts.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=03 --step=3.2 --project-root=.`

---

### Step 3.3: Display Remediation Hints (Conditional)

EXECUTE: If $FIX_HINTS is true, display the remediation pattern showing how to convert W3 violations into compliant code.
```
IF $FIX_HINTS:
    Display:
    ""
    "## Remediation Pattern (STORY-135)"
    ""
    "**BEFORE (W3 Violation):**"
    "```"
    "Skill(command=\"spec-driven-architecture\")"
    "```"
    ""
    "**AFTER (W3 Compliant - Option A: Display-Only Recommendation):**"
    "```"
    "**Recommended Next Action (display-only, no auto-invocation):**"
    "Run /create-context [project-name]"
    "**NOTE:** Per W3 compliance, this skill does NOT auto-invoke other skills."
    "```"
    ""
    "**AFTER (W3 Compliant - Option B: User Consent Gate):**"
    "```"
    "AskUserQuestion:"
    "    Question: \"Proceed with architecture creation?\""
    "    Options: [\"Yes, invoke /create-context\", \"No, skip\"]"
    ""
    "IF user approves:"
    "    Skill(command=\"spec-driven-architecture\")"
    "```"
ELSE:
    Display: ""
    Display: "Tip: Run with --fix-hints to see remediation patterns"
```
VERIFY: If $FIX_HINTS=true, remediation examples are displayed. If false, tip message is displayed.
RECORD: `devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase=03 --step=3.3 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete W3-AUDIT --workflow=w3-compliance --phase=03 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 04 | Exit 1: HALT
```

## Phase 03 Completion Display

```
Phase 03 Complete: Reporting
  Report displayed: Yes
  Quiet mode: ${QUIET}
  Fix hints: ${FIX_HINTS}
```
