## Integration with DevForgeAI Framework

### Invoked By

**spec-driven-design skill (Phase 6, Step 4):**
```
After generating UI specification, invoke formatter:

Task(
    subagent_type="ui-spec-formatter",
    description="Format UI spec results",
    prompt="UI specification generated at devforgeai/specs/ui/{SPEC_ID}-ui-spec.md

            Format results and generate user-friendly display.

            Story mode: {mode}
            Framework: {framework}
            Component count: {count}
            Story ID: {story_id or 'standalone'}

            Return structured result with display template and implementation guidance."
)

Parse response as JSON
Return result_summary to command
```

### Returns To

**spec-driven-design skill receives:**
- Structured result object
- Display template (ready to output)
- Component details (for story file update)
- Implementation guidance (to communicate to user)

**Command receives (from skill):**
- Result summary
- Display template
- File locations
- Outputs directly (no additional processing needed)

### Framework-Aware Principles

This subagent respects DevForgeAI constraints:

**Tech Stack Awareness:**
- Validates framework against tech-stack.md
- Warns if styling library not in approved list
- Suggests alternative if conflict detected

**Source Tree Awareness:**
- Validates file locations against source-tree/
- Recommends correct file structure for generated files
- Alerts if placement violates directory rules

**Architecture Constraints:**
- Validates component structure against layer boundaries
- Ensures UI components respect presentation layer isolation
- Checks for cross-layer dependency violations

**Anti-Patterns:**
- Detects if generated code uses forbidden patterns
- Alerts developer to review and correct
- References specific anti-patterns.md entries

**Story Workflow:**
- Next steps align with story status and workflow state
- Understands UI generation as pre-implementation phase
- Recommends `/dev` for implementation, `/qa` for validation

---
