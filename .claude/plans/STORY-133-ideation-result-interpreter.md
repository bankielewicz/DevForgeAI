# STORY-133: Create Ideation-Result-Interpreter Subagent - Test Generation Plan

**Status**: Phase 01 Pre-Flight Validation Complete
**Git Status**: Uncommitted changes present (10+ files)
**Test Framework**: Bash (shell scripts)
**Test Directory**: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-133/`

---

## Execution Log

### Phase 01: Pre-Flight Validation (COMPLETE)

**Step 1.1 - Git Repository Validation**
- ✓ Git available and repository initialized
- Current branch: `refactor/devforgeai-migration`
- Status: 10 modified files, 15 untracked files
- No blocking issues for test generation

**Step 1.2 - Story File Status**
- ✗ Story file not yet created: `devforgeai/specs/Stories/STORY-133-create-ideation-result-interpreter.story.md`
- Will be created first before generating tests (narrative context needed)

**Step 1.3 - Context Files Validated**
- ✓ `devforgeai/specs/context/tech-stack.md` (verified)
- ✓ `devforgeai/specs/context/source-tree.md` (verified, test location: `devforgeai/tests/STORY-133/`)

**Step 1.4 - Test Framework Detection**
- ✓ Test framework: **Bash shell scripts** (standard for DevForgeAI framework test suite)
- Pattern: `test-ac#-[description].sh` files
- Location: `devforgeai/tests/STORY-133/`

**Step 1.5 - Pattern Analysis**
- Reviewed dev-result-interpreter.md (existing subagent)
- YAML frontmatter required: name, description, tools, model, color
- Content structure: Purpose, When Invoked, Workflow, Templates, Error Handling, Related Subagents
- Typical size: 850+ lines

---

## Test Requirements Breakdown

### AC#1: Subagent Structure and Initialization (FAILING TESTS TO CREATE)

**Test File**: `test-ac1-subagent-structure.sh`

Test cases:
1. Verify file exists at `.claude/agents/ideation-result-interpreter.md`
2. Verify YAML frontmatter has all required fields
   - `name:` field
   - `description:` field
   - `tools:` field
   - `model:` field
3. Verify frontmatter is valid YAML (between `---` markers)
4. Verify all required sections exist as markdown headers
   - `# Purpose`
   - `# When Invoked`
   - `# Workflow`
   - `# Templates`
   - `# Error Handling`
   - `# Related Subagents`

### AC#2: Ideation-Specific Output Parsing (FAILING TESTS TO CREATE)

**Test File**: `test-ac2-output-parsing.sh`

Test cases:
1. Verify workflow includes epic count extraction logic
2. Verify complexity score (0-60) extraction mentioned
3. Verify architecture tier (1-4) extraction mentioned
4. Verify requirements summary parsing (functional, NFR, integration counts)
5. Verify next-action guidance workflow:
   - Greenfield → `/create-context`
   - Brownfield → `/orchestrate`

### AC#3: Display Template Generation for Success Cases (FAILING TESTS TO CREATE)

**Test File**: `test-ac3-success-templates.sh`

Test cases:
1. Verify success template includes header with epic count
2. Verify success template includes complexity score
3. Verify architecture tier classification section
4. Verify requirements breakdown section
5. Verify key design decisions section
6. Verify recommended next command section

### AC#4: Display Template Generation for Warning Cases (FAILING TESTS TO CREATE)

**Test File**: `test-ac4-warning-templates.sh`

Test cases:
1. Verify warning template exists for incomplete ideation
2. Verify completion status display
3. Verify quality warnings with severity levels
4. Verify incomplete sections highlighted
5. Verify resolution path with recommendations

### AC#5: Framework Integration and Tool Restrictions (FAILING TESTS TO CREATE)

**Test File**: `test-ac5-tool-restrictions.sh`

Test cases:
1. Verify YAML `tools:` field contains ONLY "Read, Glob, Grep"
2. Verify NO `Write` tool in tools list
3. Verify NO `Edit` tool in tools list
4. Verify NO `Bash` tool in tools list
5. Verify NO file creation logic in workflow sections
6. Verify no hardcoded file operations (Bash commands)

### NFR: File Size (FAILING TEST TO CREATE)

**Test File**: `test-nfr-file-size.sh`

Test cases:
1. Verify file line count ≤ 200 lines
2. Verify file size reasonable (not truncated)

---

## Test Implementation Strategy

Each test script will follow this pattern:

```bash
#!/bin/bash
# test-ac#-[description].sh
# Test AC#N: [Acceptance Criteria Name]
# Expected: All checks pass (exit 0)

STORY_ID="STORY-133"
AGENT_FILE=".claude/agents/ideation-result-interpreter.md"
TEST_RESULTS=0

# Test 1: File exists
echo "TEST: File exists at $AGENT_FILE"
if [ -f "$AGENT_FILE" ]; then
    echo "  ✓ PASS: File found"
else
    echo "  ✗ FAIL: File not found"
    TEST_RESULTS=1
fi

# Test 2-N: Specific validations using grep/wc/sed
# ... more tests ...

exit $TEST_RESULTS
```

---

## Execution Phases

**Phase 02: Test-First Design (COMPLETE ✓)**
1. ✓ Create story file with AC details
2. ✓ Generate all 6 test files (failing initially)
3. ✓ Verify all tests fail (TDD Red phase)
4. ✓ Document test results

**Test Results**:
- test-ac1-subagent-structure.sh: FAIL ✗ (expected)
- test-ac2-output-parsing.sh: FAIL ✗ (expected)
- test-ac3-success-templates.sh: FAIL ✗ (expected)
- test-ac4-warning-templates.sh: FAIL ✗ (expected)
- test-ac5-tool-restrictions.sh: FAIL ✗ (expected)
- test-nfr-file-size.sh: FAIL ✗ (expected)

**All 6 tests failing** = TDD Red phase successful ✓

**Artifacts Created**:
- Story file: `devforgeai/specs/Stories/STORY-133-create-ideation-result-interpreter.story.md`
- Test directory: `devforgeai/tests/STORY-133/`
- 6 test scripts: 1,196 lines of Bash code
- Test report: `STORY-133-TEST-GENERATION-REPORT.md`
- Plan file: `.claude/plans/STORY-133-ideation-result-interpreter.md`

**Phase 03: Implementation**
1. Create `.claude/agents/ideation-result-interpreter.md`
2. Implement subagent following dev-result-interpreter pattern
3. Adapt for ideation-specific concerns (epics, complexity, architecture tiers)
4. Run tests, verify all pass

**Phase 04: Refactoring**
1. Code review for quality
2. Complexity check
3. Pattern compliance

**Phase 05: Integration**
1. Integration tests with devforgeai-ideation skill
2. Framework integration validation

**Phase 06-08**: Deferral Challenge, DoD Update, Git Workflow

---

## References

- **Pattern Model**: `.claude/agents/dev-result-interpreter.md` (existing 866-line subagent)
- **Tool Constraints**: `devforgeai/specs/context/tech-stack.md` (lines 328-329, principle of least privilege)
- **Source Tree**: `devforgeai/specs/context/source-tree.md` (lines 500-548, subagent rules)
- **TDD Workflow**: `.claude/skills/devforgeai-development/SKILL.md` (skill execution model)

---

**Next Action**: Generate failing test scripts in Phase 02
