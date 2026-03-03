# STORY-135 Test Suite

## Display-Only Architecture Handoff

**Purpose:** Validate that the `/ideate` command and `devforgeai-ideation` skill do NOT auto-invoke the `devforgeai-architecture` skill, ensuring W3 compliance and user control.

## W3 Definition

From BRAINSTORM-001 Code Smell W3:
> "Auto-invokes architecture skill (token overflow)"
>
> Problem: The /ideate command previously auto-invoked the devforgeai-architecture
> skill after ideation completed, causing potential token overflow in long sessions.
>
> Solution: Commands should orchestrate (display next steps), not auto-execute chains.
> The user must manually run `/create-context` when ready.

## Test Structure

| Test File | AC Coverage | Test Count |
|-----------|-------------|------------|
| test-ac1-no-auto-architecture-invocation.sh | AC#1 | 4 tests |
| test-ac2-skill-displays-next-action.sh | AC#2 | 4 tests |
| test-ac3-display-without-invoking.sh | AC#3 | 4 tests |
| test-ac4-user-control.sh | AC#4 | 4 tests |

## Running Tests

```bash
# Run all tests
cd tests/STORY-135
bash run-all-tests.sh

# Run individual AC test
bash test-ac1-no-auto-architecture-invocation.sh
```

## Acceptance Criteria Mapping

### AC#1: Remove Auto-Architecture Invocation from Command
- Test 1.1: No Skill(devforgeai-architecture) in ideate.md
- Test 1.2: No Task() calls for architecture in ideate.md
- Test 1.3: No Skill(devforgeai-architecture) in artifact-generation.md
- Test 1.4: Uses result-interpreter for display-only

### AC#2: Skill Phase 6.6 Displays Recommended Next Action
- Test 2.1: /create-context recommendation exists
- Test 2.2: "Run /create-context" format present
- Test 2.3: Step 6.6 section exists
- Test 2.4: Greenfield path recommends /create-context

### AC#3: Command Displays Recommendation Without Invoking Architecture
- Test 3.1: Phase 3 Result Interpretation exists
- Test 3.2: Display template pattern present
- Test 3.3: No Skill(devforgeai-architecture) after Phase 3
- Test 3.4: "Commands orchestrate" principle stated

### AC#4: User Maintains Control Over Architecture Skill Execution
- Test 4.1: AskUserQuestion for next action
- Test 4.2: Command Complete section exists
- Test 4.3: No forced workflow chaining
- Test 4.4: W3 compliance verified

## Implementation Summary

**Key Change:** Removed auto-invocation `Skill(command="devforgeai-architecture")` from `artifact-generation.md` and replaced with display-only recommendation text.

**Files Modified:**
- `.claude/skills/devforgeai-ideation/references/artifact-generation.md`

**No Changes Required:**
- `.claude/commands/ideate.md` (already clean)
- `.claude/skills/devforgeai-ideation/references/completion-handoff.md` (already has correct format)
