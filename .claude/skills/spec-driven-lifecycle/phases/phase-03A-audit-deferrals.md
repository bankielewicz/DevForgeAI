# Phase 03A: Audit Deferrals

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --from=01 --to=03A
```

## Contract

PURPOSE: Scan all QA Approved and Released stories for deferred DoD items, validate deferral legitimacy, and generate comprehensive audit report. Audit Deferrals mode only.
REQUIRED SUBAGENTS: deferral-validator
REQUIRED ARTIFACTS: Audit report generated at devforgeai/qa/deferral-audit-{timestamp}.md
STEP COUNT: 6 mandatory steps

---

## Mandatory Steps

### Step 1: Discover Eligible Stories

EXECUTE: Find all stories with QA Approved or Released status.
```
all_stories = Glob(pattern="devforgeai/specs/Stories/*.story.md")
eligible_stories = []

FOR story_file in all_stories:
  Grep(pattern="^status: (QA Approved|Released)", path=story_file)
  IF match:
    eligible_stories.append(story_file)

audit_story_count = len(eligible_stories)
Display: "Found {audit_story_count} stories to audit"
```

VERIFY: At least 1 eligible story found.
```
IF audit_story_count == 0:
  Display: "No QA Approved or Released stories to audit."
  HALT (graceful - return success with zero findings)
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03A --step=1`

### Step 2: Scan for Deferred Items

EXECUTE: Scan each eligible story for deferred DoD items.
```
deferred_items = []

FOR story_file in eligible_stories:
  Read(file_path=story_file)

  # Look for deferred markers
  Grep(pattern="- \\[ \\].*[Dd]efer", path=story_file)
  Grep(pattern="[Dd]eferred.*to.*STORY-", path=story_file)
  Grep(pattern="\\[DEFERRED\\]", path=story_file)

  IF any deferred patterns found:
    deferred_items.append({
      "story": story_file,
      "items": matched_items,
      "count": len(matched_items)
    })

deferral_count = sum(item["count"] for item in deferred_items)
Display: "Found {deferral_count} deferred items across {len(deferred_items)} stories"
```

VERIFY: Scan completed for all eligible stories.
```
IF deferral_count == 0:
  Display: "No deferred items found - all stories clean."
  # Continue to generate clean audit report
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03A --step=2`

### Step 3: Validate Blockers (Resolvable Check)

EXECUTE: For each deferred item, check if the blocker is still valid.
```
FOR item in deferred_items:
  FOR deferred in item["items"]:
    # Check if deferred-to story exists
    IF deferred references another story:
      target_story = Glob(pattern="devforgeai/specs/Stories/${target_id}*.story.md")
      IF target_story exists:
        Read(file_path=target_story[0])
        Grep(pattern="^status:", path=target_story[0])
        IF target_status == "Released":
          deferred["resolvable"] = true
          deferred["reason"] = "Target story {target_id} is now Released"
        ELSE:
          deferred["resolvable"] = false
          deferred["reason"] = "Target story {target_id} status: {target_status}"
      ELSE:
        deferred["resolvable"] = false
        deferred["reason"] = "Target story {target_id} not found"

    # Check if deferred due to ADR
    ELSE IF deferred references an ADR:
      Grep(pattern="Status:.*Accepted", path="devforgeai/specs/adrs/{adr_id}.md")
      deferred["valid"] = (match found)
```

VERIFY: All deferred items have resolvable/valid flags set.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03A --step=3`

### Step 4: Invoke Deferral-Validator Subagent

EXECUTE: For stories with deferrals, invoke deferral-validator for deep validation.
```
FOR item in deferred_items:
  Task(subagent_type="deferral-validator",
    prompt="Validate deferred DoD items in story: {item.story}
      Deferred items: {item.items}
      Check for:
      1. Justified technical reasons
      2. Circular deferral chains
      3. Referenced story/ADR existence
      4. Implementation feasibility
      Return: validation_result per item")
```

VERIFY: Deferral-validator returned results for each story.
```
IF any validation_result is empty:
  Display "Warning: Validation incomplete for some stories"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03A --step=4 --subagent=deferral-validator`

### Step 5: Aggregate Results by Severity

EXECUTE: Categorize all findings by severity.
```
findings = {
  "CRITICAL": [],   # Circular chains, missing references
  "HIGH": [],       # Invalid deferrals without justification
  "MEDIUM": [],     # Resolvable deferrals (target story complete)
  "LOW": []         # Valid deferrals with proper documentation
}

FOR item in deferred_items:
  FOR deferred in item["items"]:
    IF deferred has circular chain:
      findings["CRITICAL"].append(deferred)
    ELSE IF deferred is invalid (no justification):
      findings["HIGH"].append(deferred)
    ELSE IF deferred is resolvable:
      findings["MEDIUM"].append(deferred)
    ELSE:
      findings["LOW"].append(deferred)

violation_count = len(findings["CRITICAL"]) + len(findings["HIGH"])
violation_summary = "CRITICAL: {len(CRITICAL)}, HIGH: {len(HIGH)}, MEDIUM: {len(MEDIUM)}, LOW: {len(LOW)}"
```

VERIFY: All deferred items categorized.
```
total_categorized = sum(len(v) for v in findings.values())
IF total_categorized != deferral_count:
  Display "Warning: {deferral_count - total_categorized} items not categorized"
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03A --step=5`

### Step 6: Generate Audit Report

EXECUTE: Write comprehensive audit report to file.
```
timestamp = current_datetime_formatted
audit_report_path = "devforgeai/qa/deferral-audit-{timestamp}.md"

Write(file_path=audit_report_path, content="""
# Deferral Audit Report
**Generated:** {timestamp}
**Stories Audited:** {audit_story_count}
**Deferrals Found:** {deferral_count}

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | {len(CRITICAL)} |
| HIGH | {len(HIGH)} |
| MEDIUM | {len(MEDIUM)} |
| LOW | {len(LOW)} |

## Findings
{FOR severity, items in findings:}
### {severity}
{FOR item in items:}
- {item.story}: {item.description} ({item.reason})
{END FOR}
{END FOR}

## Recommendations
{generated_recommendations}
""")
```

VERIFY: Audit report file created.
```
Glob(pattern="devforgeai/qa/deferral-audit-*.md")
IF not found: HALT -- "Audit report not created."
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --phase=03A --step=6`

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=03A --checkpoint-passed
```
