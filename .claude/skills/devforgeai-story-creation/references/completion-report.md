# Phase 8: Completion Report Generation

Generate structured completion summary and guide user to next actions.

## Overview

This phase presents the completed story to the user with a summary and actionable next steps.

---

## Step 8.1: Generate Completion Summary

**Objective:** Present structured summary of created story

**Present to user:**

```markdown
## ✅ Story Created: {story_id}

**Title:** {story_title}

**Metadata:**
- Epic: {epic_id and epic_title, or "None"}
- Sprint: {sprint_id, or "Backlog"}
- Priority: {priority}
- Story Points: {points}
- Status: Backlog

**Specifications:**
- Acceptance Criteria: {ac_count}
- API Endpoints: {endpoint_count or "None"}
- Data Models: {entity_count}
- UI Components: {component_count or "None"}

**File Location:**
`.ai_docs/Stories/{story_id}-{slug}.story.md`

**Story validated:**
✓ User story format correct
✓ Acceptance criteria testable
✓ Technical specification complete
✓ All NFRs measurable
✓ Epic/sprint linked (if applicable)
```

---

## Step 8.2: Determine Next Action

**Objective:** Guide user to next step in workflow

**Ask user:**

```
AskUserQuestion(
  questions=[{
    question: "Story created successfully. What would you like to do next?",
    header: "Next action",
    options: [
      {
        label: "Create another story",
        description: "Generate another story for a different feature"
      },
      {
        label: "Start development",
        description: "Run /dev {story_id} to implement this story with TDD"
      },
      {
        label: "Add to sprint",
        description: "Add this story to a sprint for planning"
      },
      {
        label: "Review story file",
        description: "I want to review/edit the generated story"
      }
    ],
    multiSelect: false
  }]
)
```

**Based on response:**

**"Create another story":**
```
Report: "Run `/create-story [feature-description]` to create another story"
```

**"Start development":**
```
Report: """
Run: `/dev {story_id}`

Prerequisites before running /dev:
1. Context files must exist (run /create-context if needed)
2. Story status should be "Ready for Dev" (currently: Backlog)

The /dev command will:
1. Execute TDD cycle (Red → Green → Refactor)
2. Generate tests from acceptance criteria
3. Implement code to pass tests
4. Validate against context files
5. Update story status to "Dev Complete"
"""
```

**"Add to sprint":**
```
Report: """
Run: `/create-sprint {number}` to add stories to a sprint

Or manually:
1. Edit sprint file: `.ai_docs/Sprints/SPRINT-XXX.md`
2. Add story to Sprint Backlog section
3. Update story status to "Ready for Dev" when sprint starts
"""
```

**"Review story file":**
```
Report: """
Story file: `.ai_docs/Stories/{story_id}-{slug}.story.md`

You can:
- Open in your editor to review/edit
- Ask me to make specific changes
- Run /dev when ready to implement
"""
```

---

## Output

**Phase 8 produces:**
- ✅ Completion summary displayed to user
- ✅ Next action guidance provided
- ✅ User workflow continues seamlessly

---

## Error Handling

**Error 1: Story file missing at completion**
- **Detection:** Cannot read story file for summary generation
- **Recovery:** Re-execute Phase 5 (story file creation), verify write succeeded

**Error 2: Metadata missing for summary**
- **Detection:** Cannot extract ac_count, entity_count, etc. from story
- **Recovery:** Parse story file sections, extract counts manually

See `error-handling.md` for comprehensive error recovery procedures.

---

## Skill Completion

**After Phase 8 completes →** Skill execution finishes

Story creation workflow complete. User has actionable next steps.
