# QA Result Interpreter -- Remediation Guide

Reference content extracted from the core agent definition. Contains remediation guidance schema and the next-steps emission contract (cold-start handoff block).

---

## Remediation Guidance Schema (Step 6)

```
Analyze violations and create remediation steps:

FOR each CRITICAL violation:
    priority = 1
    action = "FIX IMMEDIATELY - blocks approval"

FOR each HIGH violation:
    priority = 2
    action = "FIX - blocks approval"

FOR each MEDIUM violation:
    priority = 3
    action = "DOCUMENT - document in QA report (may not block)"

FOR each LOW violation:
    priority = 4
    action = "CONSIDER - improvement (informational)"

Sort by priority and generate ordered remediation list:

remediation = {
    "priority": [
        {
            "order": 1,
            "severity": "CRITICAL",
            "items": [
                {
                    "violation": {violation_desc},
                    "location": {file:line if available},
                    "fix": {remediation_steps}
                }
            ]
        }
    ],
    "estimated_effort": "X hours",
    "workflow_recommendation": "return_to_dev | fix_manually | request_exception"
}
```

## Next-Steps Emission Contract (Cold-Start Handoff Block)

This block MUST be emitted when `overall_status` is PASS_WITH_WARNINGS or FAILED AND
`qa-recommendations-status` reports at least one open MEDIUM or LOW recommendation.

```
IF overall_status in ("PASS_WITH_WARNINGS", "PASS WITH WARNINGS", "FAILED"):
    status_result = Bash(command="devforgeai-validate qa-recommendations-status --story-id={STORY_ID} --project-root=. --format=json 2>&1")
    IF status_result.exit_code == 0:
        parsed = json.loads(status_result.stdout)
        medium_low_rec_ids = [r for r in parsed.open_rec_ids
                              if severity_of(r) in ("M", "L")]  # MEDIUM + LOW
        IF len(medium_low_rec_ids) > 0:
            medium_count = parsed.by_severity.get("MEDIUM", 0)
            low_count    = parsed.by_severity.get("LOW", 0)
            rec_id_csv   = ",".join(medium_low_rec_ids)

            next_steps.append("")
            next_steps.append("## Next Steps")
            next_steps.append("")
            next_steps.append(
                f"To convert the {medium_count} MEDIUM + {low_count} LOW advisory "
                "recommendations into a follow-up story, run ONE of the following in "
                "your current session OR a fresh session:"
            )
            next_steps.append("")
            next_steps.append("  # Variant 1 -- Default (bundle MEDIUM + LOW, auto-filled --rec-ids):")
            next_steps.append(f"  /create-story --from-recommendations={STORY_ID} --rec-ids={rec_id_csv}")
            next_steps.append("")
            next_steps.append("  # Variant 2 -- Interactive (skill prompts you to select):")
            next_steps.append(f"  /create-story --from-recommendations={STORY_ID}")
            next_steps.append("")
            next_steps.append("  # Variant 3 -- Include Blocking (NOT RECOMMENDED; fix in-cycle via /dev {STORY_ID} --fix instead):")
            next_steps.append(f"  /create-story --from-recommendations={STORY_ID} --include-blocking")
            next_steps.append("")
            next_steps.append(
                f"See devforgeai/qa/reports/{STORY_ID}-next-steps.md for the persisted copy "
                "(safe to run from a new session)."
            )
            # Do NOT add prose. Do NOT wrap the 3 commands in narrative text.
            # Do NOT omit any variant. Full contract: see qa-result-formatting-guide.md.
```

**Rules for the handoff block:**
- Do NOT add prose or narrative text
- Do NOT wrap the 3 command variants in narrative text
- Do NOT omit any variant
- The persisted copy at `devforgeai/qa/reports/{STORY_ID}-next-steps.md` allows safe execution from a fresh session
