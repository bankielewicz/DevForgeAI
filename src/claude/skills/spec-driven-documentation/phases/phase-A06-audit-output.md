# Phase A06: Audit Output

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=A05 --to=A06 --workflow=doc-audit
# Exit 0: proceed | Exit 1: Phase A05 incomplete
```

## Contract

PURPOSE: Write structured audit results to `devforgeai/qa/audit/doc-audit.json` with scorecard, findings, inventory, and fix session tracking.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: `devforgeai/qa/audit/doc-audit.json` written
STEP COUNT: 2 mandatory steps

---

## Mandatory Steps

### Step A06.1: Ensure Output Directory

EXECUTE: Create the audit output directory if it doesn't exist.
```
Bash(command="mkdir -p devforgeai/qa/audit")

Glob(pattern="devforgeai/qa/audit/")
Display: "Audit output directory verified"
```
VERIFY: Directory `devforgeai/qa/audit/` exists.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A06 --step=A06.1 --workflow=doc-audit`

---

### Step A06.2: Write Audit JSON

EXECUTE: Write the complete audit result to JSON file.
```
audit_result = {
    "version": "1.0.0",
    "generated": current_timestamp,
    "session_id": SESSION_ID,
    "project_root": ".",
    "scorecard": {
        "tone_personality": {
            "score": score_tone,
            "max": 10,
            "key_blocker": key_blocker_tone
        },
        "information_architecture": {
            "score": score_ia,
            "max": 10,
            "key_blocker": key_blocker_ia
        },
        "visual_design": {
            "score": score_visual,
            "max": 10,
            "key_blocker": key_blocker_visual
        },
        "onboarding_friction": {
            "score": score_onboard,
            "max": 10,
            "key_blocker": key_blocker_onboard
        }
    },
    "findings": findings,
    "inventory": {
        "docs_files": filtered_docs,
        "community_files": community_checklist,
        "orphaned_files": orphaned_files,
        "duplicate_groups": duplicates if duplicates else []
    },
    "fix_sessions": []
}

Write(file_path="devforgeai/qa/audit/doc-audit.json", content=JSON(audit_result, indent=2))

Display: "Audit results written: devforgeai/qa/audit/doc-audit.json"
```
VERIFY: File exists and is valid JSON.
```
result = Read(file_path="devforgeai/qa/audit/doc-audit.json")
IF Read fails: HALT -- "Audit JSON file not written"
IF "scorecard" not in result: HALT -- "Audit JSON missing scorecard"
IF "findings" not in result: HALT -- "Audit JSON missing findings"
```
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A06 --step=A06.2 --workflow=doc-audit`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=A06 --checkpoint-passed --workflow=doc-audit
```

## Phase Transition Display

```
Display: "Phase A06 complete: Audit Output"
Display: "  File: devforgeai/qa/audit/doc-audit.json"
Display: "  Proceeding to Phase A07: Audit Display"
```
