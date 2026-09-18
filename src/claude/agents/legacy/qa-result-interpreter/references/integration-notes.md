# QA Result Interpreter -- Integration Notes

Reference content extracted from the core agent definition. Documents framework integration points and principles.

---

## Invoked By

**spec-driven-qa skill (Phase 5, Step 3):**
```
After generating QA report, invoke interpreter:

Task(
    subagent_type="qa-result-interpreter",
    description="Interpret QA results",
    prompt="QA report generated at devforgeai/qa/reports/{STORY_ID}-qa-report.md

            Interpret results and generate user-friendly display.

            Story loaded in conversation.
            Validation mode: {mode}
            Story status: {status}

            Return structured result summary with display template and next steps."
)

Parse response as JSON
Return result_summary to command
```

## Returns To

**spec-driven-qa skill receives:**
- Structured result object
- Display template (ready to output)
- Next steps (to communicate to user)
- Remediation guidance (to include in report)

**Command receives (from skill):**
- Result summary
- Display template
- Outputs directly (no additional processing needed)

## Framework-Aware Principles

This subagent respects DevForgeAI constraints:

**Tech Stack Awareness:**
- Display recommendations based on tech-stack.md language/framework
- Suggest language-specific test frameworks for coverage gaps
- Reference language-specific tools

**Architecture Constraints:**
- Remediation guidance respects source-tree/ file locations
- Violation messages reference architecture-constraints.md boundaries
- Defer violations explained in context of layer structure

**Anti-Patterns:**
- Violations classified using anti-patterns.md categories
- Remediation prioritizes anti-pattern fixes

**Coding Standards:**
- Next steps include reference to coding-standards.md where relevant
- Complexity violations include standards threshold references

**Story Workflow:**
- Next steps align with story status and workflow state
- Understands Light QA (blocks), Deep QA (gates), and retry limits
- Recommends `/orchestrate` for full lifecycle if appropriate
