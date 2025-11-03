---
description: Implement user story using TDD workflow
argument-hint: [STORY-ID]
model: haiku
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Task, Bash(pytest:*), Bash(npm:test), Bash(dotnet:test), Bash(git:*)
---

# /dev - TDD Development Workflow

Execute full Test-Driven Development cycle for a user story.

## Pre-execution Context

**Story:** @.ai_docs/Stories/$1.story.md
**Git Status:** !`git status`

## Workflow

### Phase 0a: Argument Validation

**Extract story ID:**
```
STORY_ID = $1
```

**Validate story ID format:**
```
IF $1 is empty OR does NOT match pattern "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I develop?"
  Header: "Story ID"
  Options:
    - "List stories in Ready for Dev status"
    - "List stories in Backlog status"
    - "Show correct /dev command syntax"
  multiSelect: false

  Extract STORY_ID from user response
```

**Validate story file exists:**
```
Glob(pattern=".ai_docs/Stories/${STORY_ID}*.story.md")

IF no matches found:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story not found"
  Options:
    - "List all available stories"
    - "Create ${STORY_ID} (run /create-story first)"
    - "Cancel command"
  multiSelect: false

  Handle based on user selection

IF multiple matches found:
  AskUserQuestion:
  Question: "Multiple files match ${STORY_ID}. Which one?"
  Header: "Story selection"
  Options:
    [List each matched filename]
  multiSelect: false

  STORY_FILE = user selection
```

**Validation summary:**
```
✓ Story ID: ${STORY_ID}
✓ Story file: ${STORY_FILE}
✓ Proceeding with development...
```

---

### Phase 0b: Technology Detection & Context Validation

**CRITICAL: Detect project technology before executing any test commands**

**Step 1: Verify context files exist**
```
Check: Glob(pattern=".devforgeai/context/*.md")
Expected: 6 files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)

IF context files missing:
  HALT with error:
  "Context files not found. This is a greenfield project.

   Run this first:
   > /create-context [project-name]

   Then retry:
   > /dev $ARGUMENTS"

  DO NOT PROCEED to development without context files.
```

**Step 2: Detect technology stack**
```
IF tech-stack.md exists:
  Read tech-stack.md
  Extract:
    - Programming language (Node.js, Python, .NET, Go, Java, Rust, etc.)
    - Test framework (npm test, pytest, dotnet test, go test, etc.)
    - Build tool (npm, pip, dotnet, go, mvn, etc.)

ELSE IF tech-stack.md missing (but other context files exist):
  Detect via project markers:
    - Glob(pattern="package.json") → Node.js → Test: npm test
    - Glob(pattern="*.csproj") → .NET → Test: dotnet test
    - Glob(pattern="pyproject.toml") OR Glob(pattern="requirements.txt") → Python → Test: pytest
    - Glob(pattern="go.mod") → Go → Test: go test ./...
    - Glob(pattern="pom.xml") → Java/Maven → Test: mvn test
    - Glob(pattern="build.gradle*") → Java/Gradle → Test: gradle test
    - Glob(pattern="Cargo.toml") → Rust → Test: cargo test

ELSE IF detection fails:
  Use AskUserQuestion:
  "Unable to detect project technology. What command runs tests?"
  Options:
    - npm test (Node.js/JavaScript/TypeScript)
    - pytest (Python)
    - dotnet test (.NET/C#)
    - go test ./... (Go)
    - mvn test (Java/Maven)
    - cargo test (Rust)
    - Other (specify custom command)
```

**Step 3: Store detected test command**
```
TEST_COMMAND = [detected command from Step 2]

Example outputs:
  - Node.js project → TEST_COMMAND = "npm test"
  - .NET project → TEST_COMMAND = "dotnet test"
  - Python project → TEST_COMMAND = "pytest"
```

**Validation:**
- [ ] Technology detected successfully
- [ ] Test command identified
- [ ] Ready to proceed to Phase 1

---

### Phase 1: Story Validation

**Read story file:**
```
Story file loaded via @ context reference above
```

**Parse and validate:**
1. Extract YAML frontmatter (id, status, title, epic, sprint)
2. Verify status is "Ready for Dev" or "Backlog"
3. Extract acceptance criteria (Given/When/Then)
4. Extract technical specification
5. Extract non-functional requirements

**Status Gate:**
- ✅ Status = "Ready for Dev" or "Backlog" → Continue
- ❌ Status = other → HALT with error

**Validation Checks:**
- [ ] Story ID matches argument
- [ ] Status allows development
- [ ] Acceptance criteria defined
- [ ] Technical spec exists

**Error Handling:**

IF story file not found:
```
ERROR: Story file not found at .ai_docs/Stories/$ARGUMENTS.story.md

Available stories:
[List .ai_docs/Stories/*.story.md]

HALT: Provide valid story ID
```

IF status invalid:
```
ERROR: Story status is "$STATUS" (expected "Ready for Dev" or "Backlog")

Current workflow state: $STATUS
Required state: Ready for Dev

HALT: Story must be in correct workflow state
```

IF acceptance criteria missing:
```
ERROR: Story has no acceptance criteria

Stories require testable acceptance criteria in Given/When/Then format.

HALT: Update story with acceptance criteria
```

### Phase 2: Invoke Development Skill

**Delegate to devforgeai-development skill:**

**Context for skill:**
- Story content loaded via @file reference above
- Story ID: ${STORY_ID}

```bash
Skill(command="devforgeai-development")
```

**Note:** Skill will extract story ID from conversation context (YAML frontmatter in loaded story file)

**Skill handles complete TDD cycle:**

1. **Context Validation**
   - Checks 6 context files exist
   - Auto-invokes devforgeai-architecture if missing
   - Validates tech stack, source tree, dependencies

2. **Test-First (Red)**
   - Invokes test-automator subagent
   - Generates failing tests from acceptance criteria
   - Validates tests fail as expected
   - Runs light QA (syntax, build)

3. **Implementation (Green)**
   - Invokes backend-architect or frontend-developer subagent
   - Implements minimal code to pass tests
   - Validates all tests pass
   - Runs light QA (anti-patterns, compliance)

4. **Refactor**
   - Invokes refactoring-specialist subagent
   - Improves code quality while keeping tests green
   - Invokes code-reviewer for quality check
   - Runs light QA (complexity, duplication)

5. **Integration**
   - Invokes integration-tester subagent
   - Runs full test suite
   - Validates coverage thresholds
   - Runs light QA (full validation)

6. **Git Workflow**
   - Stages changes
   - Creates commit with TDD message
   - Pushes to origin

7. **Story Update**
   - Updates story status to "Dev Complete"
   - Adds workflow history entry
   - Records completion timestamp

**Skill execution is comprehensive - no additional work needed in command**

### Phase 3: Verify Completion

**Check skill execution success:**

1. **Verify story status updated:**
```bash
Read(file_path=".ai_docs/Stories/$1.story.md")
```

Extract status from frontmatter:
- ✅ Status = "Dev Complete" → Success
- ❌ Status = other → Skill failed

2. **Verify git commit created:**
```bash
# Check if commits exist first (handles empty repositories)
!`git rev-list -n 1 HEAD 2>/dev/null && git log -1 --oneline || echo "Initial commit pending"`
```

Check commit message contains story ID (if commits exist).

3. **Verify tests passing:**

**Execute test command detected in Phase 0:**
```bash
# Use TEST_COMMAND variable from Phase 0 technology detection
Bash(command=TEST_COMMAND)

# Examples based on detected technology:
# - Node.js: npm test
# - Python: pytest --tb=short
# - .NET: dotnet test
# - Go: go test ./...
# - Java: mvn test OR gradle test
# - Rust: cargo test
```

**Test Gate:**
- ✅ All tests pass → Success
- ❌ Any test fails → Report failure
- ❌ TEST_COMMAND not set → Error (technology detection failed in Phase 0)

### Phase 4: Report Results

**Success Report:**

```markdown
## Development Complete ✅

**Story:** $STORY_ID - $TITLE
**Status:** Dev Complete
**Epic:** $EPIC_ID
**Sprint:** $SPRINT_ID

### Completed Phases
- [x] Context validation
- [x] Test generation (Red)
- [x] Implementation (Green)
- [x] Refactoring
- [x] Integration testing
- [x] Git workflow
- [x] Story update

### Test Results
- **Total Tests:** $TOTAL
- **Passed:** $PASSED
- **Failed:** $FAILED
- **Coverage:** $COVERAGE%

### Git Commit
$COMMIT_HASH: $COMMIT_MESSAGE

### Next Steps
1. Run deep QA validation:
   `/qa $STORY_ID --mode=deep`

2. Review changes:
   `git diff HEAD~1`

3. If QA passes, transition to "QA Approved":
   `/orchestrate transition $STORY_ID QA-Approved`
```

**Failure Report:**

```markdown
## Development Failed ❌

**Story:** $STORY_ID - $TITLE
**Status:** $CURRENT_STATUS
**Error:** $ERROR_MESSAGE

### Failed Phase
$FAILED_PHASE

### Error Details
$ERROR_DETAILS

### Resolution Steps
$RESOLUTION_STEPS

### Common Issues

**If context files missing:**
- Run: `/arch` to create context files

**If tests fail:**
- Review test output above
- Check acceptance criteria match implementation
- Verify dependencies installed

**If light QA blocks:**
- Fix reported violations
- Re-run: `/dev $STORY_ID`

**If git conflicts:**
- Resolve conflicts: `git status`
- Re-run: `/dev $STORY_ID`
```

## Success Criteria

- [ ] Story status = "Dev Complete"
- [ ] All tests passing (100% pass rate)
- [ ] Light QA passed (no blocking violations)
- [ ] Code coverage meets thresholds (95%/85%/80%)
- [ ] Git commit created and pushed
- [ ] Workflow history updated in story file
- [ ] No anti-pattern violations
- [ ] Spec compliance validated

## Error Handling

### Story Not Found
```
ERROR: Story file not found

Path: .ai_docs/Stories/$ARGUMENTS.story.md

Actions:
1. List available stories: `ls .ai_docs/Stories/`
2. Check story ID spelling
3. Verify story created: `/orchestrate create-story`
```

### Invalid Status
```
ERROR: Story not ready for development

Current status: $STATUS
Required: "Ready for Dev" or "Backlog"

Actions:
1. Check workflow state: `/orchestrate status $STORY_ID`
2. Transition if needed: `/orchestrate transition $STORY_ID Ready-for-Dev`
3. Ensure context files exist: `/arch`
```

### Skill Execution Failed
```
ERROR: Development skill failed

Phase: $FAILED_PHASE
Error: $ERROR_MESSAGE

Actions:
1. Review error details above
2. Fix reported issues
3. Re-run: `/dev $STORY_ID`
4. If context missing: `/arch`
5. If persistent: Report to framework maintainer
```

### Test Failures
```
ERROR: Tests failing after implementation

Failed tests: $FAILED_COUNT
Passed tests: $PASSED_COUNT

Actions:
1. Review test output above
2. Check implementation against acceptance criteria
3. Fix failing tests or implementation
4. Re-run: `/dev $STORY_ID`
```

### Light QA Blocking
```
ERROR: Light QA validation failed

Violations: $VIOLATION_COUNT
Severity: $SEVERITY

Actions:
1. Review QA report in story file
2. Fix violations (anti-patterns, complexity, etc.)
3. Re-run: `/dev $STORY_ID`
4. Check anti-patterns.md for forbidden patterns
```

### Git Conflicts
```
ERROR: Git merge conflicts detected

Conflicted files: $FILES

Actions:
1. Resolve conflicts: `git status`
2. Stage resolved files: `git add $FILES`
3. Re-run: `/dev $STORY_ID`
```

### Coverage Below Threshold
```
ERROR: Code coverage below threshold

Current: $CURRENT%
Required: 95% (business logic), 85% (application), 80% (infrastructure)

Actions:
1. Review coverage report
2. Add missing tests
3. Re-run: `/dev $STORY_ID`
```

## Token Optimization

**Target:** <100K tokens per execution

**Optimization strategies:**

1. **Skill delegation:** Development skill handles all complexity
2. **Context loading:** Story file loaded once via @ reference
3. **Native tools:** Use Read/Edit/Grep (not Bash)
4. **Focused validation:** Only verify completion, not re-execute
5. **Conditional execution:** Skip phases if already complete

**Token breakdown:**
- Story validation: ~2K
- Skill invocation: ~80K (handled by skill)
- Verification: ~5K
- Reporting: ~3K
- Error handling: ~5K (only if errors)
- **Total:** ~95K tokens

## Integration

**Invokes:**
- devforgeai-development skill (comprehensive TDD implementation)

**Invoked by:**
- User (manual story implementation)
- /orchestrate command (automated workflow)

**Follows:**
- /arch (creates context files if missing)
- /story (creates story to develop)

**Precedes:**
- /qa (validates implementation)
- /release (deploys after QA approval)

## Notes

**Command is intentionally thin:**
- Validation and delegation only
- Heavy lifting done by devforgeai-development skill
- Achieves 250-350 line target by avoiding duplication

**Development skill handles:**
- Context validation
- Test generation (test-automator subagent)
- Implementation (backend-architect/frontend-developer subagents)
- Refactoring (refactoring-specialist + code-reviewer subagents)
- Integration testing (integration-tester subagent)
- Git workflow
- Story updates
- Light QA at every phase

**Command responsibilities:**
- Parse story file
- Validate workflow state
- Invoke skill
- Verify completion
- Report results

**No duplication:** All TDD logic lives in skill, not command.

---

**Token Budget:** <100K
**Priority:** CRITICAL
**Model:** Sonnet
**Status:** Production Ready
