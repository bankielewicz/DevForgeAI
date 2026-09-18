# Integration Notes

**Purpose:** DevForgeAI framework integration details for the dev-result-interpreter subagent. Loaded via `Read()` from the Integration section of the core agent file.

---

## Invoked By

**spec-driven-dev skill (Phase 6, Step 6):**
```
After completing TDD workflow, invoke interpreter:

Task(
    subagent_type="dev-result-interpreter",
    description="Interpret dev results",
    prompt="Development workflow completed for {STORY_ID}.

            Interpret results and generate user-friendly display.

            Story file: devforgeai/specs/Stories/{STORY_ID}*.story.md
            Workflow result: {result}
            Final status: {status}

            Return structured result with display template and next steps."
)

Parse response as JSON
Return result_summary to command
```

## Returns To

**spec-driven-dev skill receives:**
- Structured result object
- Display template (ready to output)
- Workflow metrics (for logging/reporting)
- Next steps (to communicate to user)

**Command receives (from skill):**
- Result summary
- Display template
- Outputs directly (no additional processing needed)

## Framework-Aware Principles

This subagent respects DevForgeAI constraints:

**Story Workflow Awareness:**
- Understands 11 workflow states (Backlog, Ready for Dev, In Development, Dev Complete, etc.)
- Recognizes story progression through dev, QA, and release
- Recommends appropriate next commands based on status
- Respects story status transitions

**Quality Gates Understanding:**
- Recognizes Gate 2: Test Passing (100% pass rate required)
- Validates test results meet framework standards
- Understands coverage thresholds (95%/85%/80%)
- Knows which gates block progression

**TDD Phases Awareness:**
- Understands 6 main phases: Red -> Green -> Refactor -> Integration -> Deferral Challenge -> Git Workflow
- Validates each phase completion
- Can detect partial phase completion
- Provides recovery guidance for failed phases

**Context Files Integration:**
- Recognizes that workflow respects tech-stack.md (locked technologies)
- Understands architecture-constraints.md layer validation
- Aware of anti-patterns detection from code-reviewer subagent
- Coding-standards.md compliance checked in code quality metrics

**Deferral Handling (RCA-006):**
- Understands Phase 5: Deferral Challenge
- Recognizes justified vs. unjustified deferrals
- Tracks deferral references to stories/ADRs
- Recommends follow-up story creation
