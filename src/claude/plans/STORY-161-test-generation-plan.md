# STORY-161: RCA-011 Immediate Execution Checkpoint - Test Generation Plan

**Story**: STORY-161-rca-011-immediate-execution-checkpoint.story.md
**Status**: Phase 02 (Test-First - Red)
**Created**: 2025-12-31

## Story Overview

This is a documentation-only story that modifies `.claude/skills/devforgeai-development/SKILL.md` to add an "Immediate Execution Checkpoint" section after line 45. The checkpoint validates that Claude proceeds directly to Phase 0 execution without stopping to ask about token budget, time constraints, or offering execution options.

## Test Strategy

Since STORY-161 is a documentation story (no implementation code), tests will be **specification verification tests** that validate the Markdown content using Bash/shell script tests with grep patterns.

### Test Scope

**AC-1: Checkpoint Added to SKILL.md**
- Verify "Immediate Execution Checkpoint" section exists
- Verify section is positioned correctly (after line 45)
- Verify section includes 5 self-check boxes
- Verify CLAUDE.md guidance references
- Verify recovery path text

**AC-2: Stop-and-Ask Detection**
- Verify checkpoint contains detection descriptions
- Verify mentions of token budget
- Verify mentions of time constraints
- Verify mentions of approach/scope options
- Verify mentions of waiting passively

**AC-3: CLAUDE.md References**
- Verify error message quotes CLAUDE.md
- Verify "no time constraints" reference
- Verify "context window is plenty big" reference
- Verify "Focus on quality" reference (if present)

**AC-4: Recovery Path**
- Verify recovery path message exists
- Verify "Go directly to Phase 0 now" text
- Verify "Do not ask questions" text

## Test Files

Location: `/mnt/c/Projects/DevForgeAI2/tests/STORY-161/`

Tests:
1. `test-ac1-checkpoint-section-exists.sh` - Verify section exists
2. `test-ac1-checkpoint-section-position.sh` - Verify positioning
3. `test-ac1-checkpoint-self-check-boxes.sh` - Verify 5 checkboxes
4. `test-ac1-checkpoint-claude-references.sh` - Verify CLAUDE.md references
5. `test-ac2-stop-and-ask-detection.sh` - Verify detection scenarios
6. `test-ac3-claude-md-quotes.sh` - Verify CLAUDE.md quotes
7. `test-ac4-recovery-path.sh` - Verify recovery instructions

## Test Naming Convention

Pattern: `test-ac{N}-{description}.sh`

Examples:
- `test-ac1-checkpoint-section-exists.sh`
- `test-ac2-stop-and-ask-detection.sh`
- `test-ac3-claude-md-quotes.sh`
- `test-ac4-recovery-path.sh`

## Test Characteristics (TDD Red Phase)

**All tests will FAIL initially** because:
1. The "Immediate Execution Checkpoint" section does NOT exist in `.claude/skills/devforgeai-development/SKILL.md` yet
2. Recovery path text is NOT present
3. Self-check boxes are NOT present

Tests will succeed after implementation adds the required content.

## Verification Strategy

Each test uses `grep` to search for required patterns in SKILL.md:

```bash
#!/bin/bash
# test-ac1-checkpoint-section-exists.sh

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

if grep -q "## Immediate Execution Checkpoint" "$SKILL_FILE"; then
    echo "PASS: Immediate Execution Checkpoint section found"
    exit 0
else
    echo "FAIL: Immediate Execution Checkpoint section not found"
    exit 1
fi
```

## Test Execution

Run all tests:
```bash
bash tests/STORY-161/test-ac1-checkpoint-section-exists.sh
bash tests/STORY-161/test-ac1-checkpoint-section-position.sh
# ... etc for all tests
```

Or use a test runner script (to be added):
```bash
bash tests/STORY-161/run-tests.sh
```

## Expected Results (Phase 02 Red)

All tests should **FAIL** with message like:
```
FAIL: Immediate Execution Checkpoint section not found
```

This is correct for TDD Red phase - tests drive the implementation.

## Next Steps (Phase 03 Green)

1. Add "Immediate Execution Checkpoint" section to SKILL.md
2. Add 5 self-check boxes
3. Add CLAUDE.md guidance references
4. Add recovery path instructions
5. Run tests again - all should PASS

## Test Coverage Map

| AC | Test File | Verification |
|-----|-----------|--------------|
| AC-1 | test-ac1-checkpoint-section-exists.sh | Section heading exists |
| AC-1 | test-ac1-checkpoint-section-position.sh | Section placed after line 45 |
| AC-1 | test-ac1-checkpoint-self-check-boxes.sh | Contains 5 checkboxes `- [ ]` |
| AC-1 | test-ac1-checkpoint-claude-references.sh | References CLAUDE.md |
| AC-2 | test-ac2-stop-and-ask-detection.sh | Contains detection descriptions |
| AC-3 | test-ac3-claude-md-quotes.sh | Contains required quotes |
| AC-4 | test-ac4-recovery-path.sh | Contains recovery instructions |

## Success Criteria for Phase 02

- [ ] All 7 test files created in `tests/STORY-161/`
- [ ] All tests follow naming convention `test-ac{N}-*.sh`
- [ ] All tests are executable bash scripts
- [ ] All tests use grep for pattern matching
- [ ] All tests produce clear PASS/FAIL output
- [ ] All tests FAIL initially (TDD Red)
- [ ] Test output format is consistent

## Implementation Notes

- Tests verify Markdown content, not code behavior
- No mocking or fixtures needed
- No external dependencies required
- Tests use bash and grep (native tools)
- Tests work in any directory (use absolute paths)

## Files to Verify

- `.claude/skills/devforgeai-development/SKILL.md` - Target file

## References

- Story file: `devforgeai/specs/Stories/STORY-161-rca-011-immediate-execution-checkpoint.story.md`
- Source RCA: `devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md`
- Tech spec: Markdown documentation only (no code)

---

**Last Updated**: 2025-12-31
**Created By**: test-automator
**Phase**: 02 (Test-First - Red)
