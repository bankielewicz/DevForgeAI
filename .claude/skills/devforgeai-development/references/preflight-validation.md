# Phase 0: Pre-Flight Validation

**Purpose:** Comprehensive validation before TDD workflow begins. This phase ensures all prerequisites are met.

**Execution:** Before Phase 1 (Red phase) starts

**Token Cost:** ~6,000 tokens when loaded

---

## Overview

Phase 0 executes 8 validation steps before proceeding to TDD implementation. This prevents starting work in an invalid environment.

**Steps:**
1. Validate Git repository status
2. Adapt TDD workflow based on Git availability
3. File-based change tracking template (if no Git)
4. Validate context files exist
5. Load story specification
6. Validate spec vs context files
7. Detect and validate technology stack
8. Detect previous QA failures

---

## Step 0.1: Validate Git Repository Status

**Invoke git-validator subagent to check Git availability:**

```
Task(
  subagent_type="git-validator",
  description="Validate Git repository status",
  prompt="Check the Git repository status for the current directory.

  Validate:
  1. Is Git installed and accessible?
  2. Is this directory a Git repository?
  3. Are there existing commits?
  4. What is the current branch?
  5. Are there uncommitted changes?

  Return JSON with Git status, assessment, and recommendations.

  CRITICAL: Always provide fallback strategy if Git unavailable - DevForgeAI must adapt gracefully."
)
```

**Parse subagent JSON response:**

```javascript
result = parse_json(subagent_output)

# Extract workflow configuration
GIT_AVAILABLE = result["git_status"]["installed"] AND result["git_status"]["repository_exists"]
WORKFLOW_MODE = result["assessment"]["workflow_mode"]  # "full", "partial", or "fallback"
CAN_COMMIT = result["assessment"]["can_commit"]
CURRENT_BRANCH = result["git_status"]["current_branch"]
UNCOMMITTED_CHANGES = result["git_status"]["uncommitted_changes"]

# Display status to user
IF WORKFLOW_MODE == "full":
    Display: "✓ Git repository validated - full workflow enabled"
    Display: "  - Repository: Initialized with {result['git_status']['commit_count']} commits"
    Display: "  - Branch: {CURRENT_BRANCH}"
    Display: "  - Uncommitted changes: {UNCOMMITTED_CHANGES}"

    IF UNCOMMITTED_CHANGES > 0:
        Display: "  ⚠️  Warning: {UNCOMMITTED_CHANGES} uncommitted changes detected"
        Display: "  Recommendation: Commit or stash before proceeding"

ELIF WORKFLOW_MODE == "partial":
    Display: "⚠ Git repository needs initial commit"
    Display: "  Repository initialized but no commits yet"
    Display: "  Recommendation:"
    FOR cmd in result["recommendations"]["commands"]:
        Display: "    {cmd}"

ELIF WORKFLOW_MODE == "fallback":
    IF result["git_status"]["installed"]:
        Display: "⚠ Git available but repository not initialized"
        Display: "  To enable full workflow:"
        FOR cmd in result["recommendations"]["commands"]:
            Display: "    {cmd}"
    ELSE:
        Display: "⚠ Git not installed - file-based workflow enabled"
        Display: "  Changes will be tracked in:"
        Display: "    .devforgeai/stories/{STORY-ID}/changes/"

    Display: ""
    Display: "  Fallback mode active (limited version control features)"

# Store flags for workflow adaptation
$GIT_AVAILABLE = GIT_AVAILABLE
$WORKFLOW_MODE = WORKFLOW_MODE
$CAN_COMMIT = CAN_COMMIT
```

**Token cost:** ~500 tokens in main conversation (~3,000 in isolated subagent context)

**Benefits:**
- Context isolation (Git checks in separate context window)
- Reusable validation (other skills can use git-validator)
- Framework-aware (subagent understands fallback strategies)
- Structured output (JSON parsing vs text interpretation)

---

## Step 0.2: Adapt TDD Workflow Based on Git Availability

**Workflow adaptations apply throughout all phases:**

**IF WORKFLOW_MODE == "file_based":**

- **Phase 0 (Context Validation):**
  - ✅ Check context files (same as git_based)
  - ✅ Validate story structure (same as git_based)
  - ⚠️ SKIP: Git status checks
  - ⚠️ SKIP: Branch validation

- **Phase 1-4 (Red/Green/Refactor/Integration):**
  - ✅ All TDD phases execute normally (test generation, implementation, refactoring)
  - ✅ All test execution works identically
  - ⚠️ SKIP: Any Git commands in these phases (if present)

- **Phase 5 (Git Workflow):**
  - ⚠️ REPLACE: Git commit workflow → File-based change tracking (see Step 0.3)

**IF WORKFLOW_MODE == "git_based":**
  - ✅ All phases execute normally with full Git integration

---

## Step 0.3: File-Based Change Tracking (Alternative to Git Workflow)

**ONLY executed when WORKFLOW_MODE == "file_based"**

This replaces Phase 5 (Git Workflow) with file-based artifact tracking.

**Implementation (executed in Phase 5 when Git unavailable):**

```markdown
### Phase 5 Alternative: File-Based Change Tracking

**ONLY when GIT_AVAILABLE == false**

#### Step 1: Create Change Documentation Directory

```
# Create story-specific changes directory
IF not exists .devforgeai/stories/${STORY_ID}/changes/:
    # Use native Write tool to create directory marker
    Write(
        file_path=".devforgeai/stories/${STORY_ID}/changes/.gitkeep",
        content="# Change tracking directory for ${STORY_ID}\n"
    )
```

#### Step 2: Generate Change Manifest

```
# Generate timestamp
TIMESTAMP = {current_datetime in ISO8601 format}

# List modified files (manual tracking since no Git)
# Developer must identify changed files from implementation work

Write(
    file_path=".devforgeai/stories/${STORY_ID}/changes/implementation-${TIMESTAMP}.md",
    content="""# Implementation Changes - ${STORY_ID}

**Timestamp:** ${TIMESTAMP}
**Story:** ${STORY_TITLE}
**Phase:** Dev Complete
**Workflow Mode:** File-Based (Git not available)

## Files Created

${list_files_created_during_implementation}

## Files Modified

${list_files_modified_during_implementation}

## Files Deleted

${list_files_deleted_if_any}

## Test Results

- Total Tests: ${total_tests}
- Passed: ${passed_tests}
- Failed: ${failed_tests}
- Coverage: ${coverage_percentage}%

## Acceptance Criteria Status

${copy_acceptance_criteria_completion_status_from_story}

## Implementation Notes

${implementation_summary_from_story_Implementation_Notes_section}

## Next Steps

To enable full version control:
1. Initialize Git: git init
2. Add files: git add .
3. Create initial commit: git commit -m "Initial commit"
4. Re-run /dev to use Git-based workflow
"""
)

Display: "✓ File-based change manifest created"
Display: "  Location: .devforgeai/stories/${STORY_ID}/changes/implementation-${TIMESTAMP}.md"
```

#### Step 3: Update Story File with Change Reference

```
Read(file_path=".ai_docs/Stories/${STORY_ID}.story.md")

# Add to Workflow History section
Edit(
    file_path=".ai_docs/Stories/${STORY_ID}.story.md",
    old_string="## Workflow History",
    new_string="""## Workflow History

### Development Complete - ${TIMESTAMP} (File-Based)
- **Status:** Dev Complete
- **Workflow Mode:** File-Based (Git not available)
- **Changes:** .devforgeai/stories/${STORY_ID}/changes/implementation-${TIMESTAMP}.md
- **Tests:** ${passed_tests}/${total_tests} passing (${coverage_percentage}% coverage)
- **Note:** Git not available - changes tracked in story artifacts

{preserve existing workflow history below}
"""
)

Display: "✓ Story file updated with file-based tracking reference"
```

#### Step 4: Display Completion Summary

```
Display:
"┌─────────────────────────────────────────────────────────────────┐
│ ✅ Development Complete (File-Based Workflow)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Story: ${STORY_ID} - ${STORY_TITLE}                            │
│ Status: Dev Complete                                            │
│                                                                 │
│ Tests: ${passed_tests}/${total_tests} passing                  │
│ Coverage: ${coverage_percentage}%                               │
│                                                                 │
│ Changes tracked in:                                             │
│   .devforgeai/stories/${STORY_ID}/changes/implementation-...   │
│                                                                 │
│ Git Integration: Not Available                                  │
│                                                                 │
│ To enable Git workflow:                                         │
│   git init                                                      │
│   git add .                                                     │
│   git commit -m 'Initial commit'                               │
│   Then re-run: /dev ${STORY_ID}                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘"
```
```

**Benefits of file-based tracking:**
- Enables DevForgeAI in non-Git environments
- Maintains traceability through file artifacts
- Same TDD workflow, different tracking mechanism
- Clear path to Git migration when ready

---

## Step 0.4: Validate Context Files Exist

**Check for all 6 DevForgeAI context files:**

```
Read all 6 context files in PARALLEL:
- Read(file_path=".devforgeai/context/tech-stack.md")
- Read(file_path=".devforgeai/context/source-tree.md")
- Read(file_path=".devforgeai/context/dependencies.md")
- Read(file_path=".devforgeai/context/coding-standards.md")
- Read(file_path=".devforgeai/context/architecture-constraints.md")
- Read(file_path=".devforgeai/context/anti-patterns.md")
```

**If ANY file is missing:**

```
Display: "❌ Context files missing - architecture setup required"
Display: "  Missing files prevent development (would cause technical debt from assumptions)"
Display: ""
Display: "Invoking devforgeai-architecture skill to create context files..."

Skill(command="devforgeai-architecture")

Display: "✓ Architecture skill completed"
Display: "Re-validating context files..."

# Re-read context files after architecture skill completes
[Execute same parallel Read operations above]
```

**STOP development until all context files exist.** This prevents technical debt from ambiguous assumptions.

**Token cost:** ~2,000 tokens (6 files × ~300 tokens each, read in parallel)

---

## Step 0.5: Load Story Specification

**Story already loaded via @file reference from slash command.**

The story file was loaded by the `/dev` command via:
```
@.ai_docs/Stories/STORY-XXX.story.md
```

**Verify story content accessible:**
- [ ] YAML frontmatter with id, title, status, epic, sprint
- [ ] Acceptance criteria section exists
- [ ] Technical specification section exists
- [ ] Non-functional requirements documented

**If story content not available in conversation:**
```
HALT with error:
"Story file not loaded in conversation context.

Expected: Story loaded via @file reference from /dev command
Actual: No story content found

Please ensure /dev command properly loads story file before invoking this skill."
```

---

## Step 0.6: Validate Spec vs Context Files

**Check for conflicts between story requirements and context file constraints:**

From story Technical Specification section, extract:
- Required technologies (languages, frameworks, libraries)
- Required patterns (architectures, designs)
- File locations (where code should be placed)

Compare against:
- tech-stack.md (locked technologies)
- architecture-constraints.md (design patterns)
- source-tree.md (file placement rules)

**If conflicts detected → Use AskUserQuestion:**

```
Question: "Spec requires [X], but tech-stack.md specifies [Y]. Which is correct?"
Header: "Spec conflict"
options:
  - label: "Follow tech-stack.md (use [Y])"
    description: "Maintain consistency with existing architecture"
  - label: "Update tech-stack.md (use [X] + create ADR)"
    description: "Document architecture change in ADR and update tech-stack.md"
multiSelect: false
```

**After user response:**
- If "Update tech-stack.md" chosen:
  - Create ADR documenting technology decision
  - Update tech-stack.md
  - Proceed with development
- If "Follow tech-stack.md" chosen:
  - Proceed with development using tech-stack.md technologies

**Token cost:** ~1,000 tokens (conflict detection) + ~3,000 (if AskUserQuestion needed)

---

## Step 0.7: Detect and Validate Technology Stack

**Invoke tech-stack-detector subagent to detect technologies and validate against tech-stack.md:**

```
Task(
  subagent_type="tech-stack-detector",
  description="Detect and validate tech stack",
  prompt="Analyze the project structure in the current directory.

  Detect:
  1. Primary programming language
  2. Framework/runtime
  3. Test framework
  4. Build tool
  5. Package manager

  Then validate against .devforgeai/context/tech-stack.md if it exists.

  Return JSON with detected technologies, validation results, and recommended commands.

  CRITICAL: If conflicts found between detected and specified technologies, provide clear resolution options."
)
```

**Parse subagent JSON response:**

```javascript
result = parse_json(subagent_output)

# Extract detected technologies
LANGUAGE = result["detected"]["language"]["primary"]
FRAMEWORK = result["detected"]["framework"]["name"]
TEST_FRAMEWORK = result["detected"]["test_framework"]["primary"]

# Extract workflow commands (CRITICAL - used in subsequent phases)
TEST_COMMAND = result["commands"]["test"]
TEST_COVERAGE_COMMAND = result["commands"]["test_coverage"]
BUILD_COMMAND = result["commands"]["build"]
INSTALL_COMMAND = result["commands"]["install"]

# Check validation status
VALIDATION_STATUS = result["validation"]["status"]

IF VALIDATION_STATUS == "PASS":
    Display: "✓ Technology stack validated"
    Display: "  - Language: {LANGUAGE}"
    Display: "  - Framework: {FRAMEWORK}"
    Display: "  - Test framework: {TEST_FRAMEWORK}"
    Display: "  - Test command: {TEST_COMMAND}"

ELIF VALIDATION_STATUS == "FAIL":
    # CRITICAL conflicts detected - HALT
    Display: "❌ Technology stack validation FAILED"
    Display: "Conflicts detected between project and tech-stack.md"

    FOR conflict in result["validation"]["conflicts"]:
        IF conflict["severity"] == "CRITICAL":
            # Use AskUserQuestion to resolve
            AskUserQuestion:
                question: "Project uses {conflict['detected']} but tech-stack.md specifies {conflict['specified']}. How to resolve?"
                header: "Tech Conflict"
                options:
                    - label: "Follow spec (update project)"
                      description: "Change project to use {conflict['specified']}"
                    - label: "Update spec (create ADR)"
                      description: "Update tech-stack.md, document in ADR"
                multiSelect: false

            # Handle user response
            IF "Update spec" chosen:
                # Create ADR, update tech-stack.md, re-validate

ELIF VALIDATION_STATUS == "ERROR":
    IF result["validation"]["context_missing"]:
        # tech-stack.md not found - invoke architecture skill
        Display: "❌ tech-stack.md not found"
        Display: "Invoking devforgeai-architecture skill..."
        Skill(command="devforgeai-architecture")

        # After architecture completes, re-run tech-stack-detector
        # [Re-invoke Task with same parameters]

# Store commands for Phases 1-5
$TEST_COMMAND = TEST_COMMAND
$TEST_COVERAGE_COMMAND = TEST_COVERAGE_COMMAND
$BUILD_COMMAND = BUILD_COMMAND
```

**Token cost:** ~700 tokens in skill context (~8,000 in isolated subagent context)

---

## Step 0.8: Detect Previous QA Failures

**Check if story has failed QA due to deferral or other issues:**

```
# Search for QA reports for this story
Glob(pattern=".devforgeai/qa/reports/${STORY_ID}-qa-report*.md")

IF reports found:
    # Read most recent report
    reports_sorted = sort_by_timestamp(reports)
    latest_report = reports_sorted[0]

    Read(file_path=latest_report)

    # Parse QA status
    IF report contains "Status: FAILED":
        # Extract failure type
        IF report contains "Deferral Validation FAILED":
            # Deferral-specific failure
            Display: "⚠ Previous QA failed due to deferral issues"
            Display: "  QA Report: {latest_report}"
            Display: ""

            # Extract deferral violations from report
            Grep(
                pattern="- \\[ \\] .* - (Deferred to|Blocked by|Out of scope)",
                path=latest_report,
                output_mode="content",
                -n=true
            )

            Display: "Development will focus on resolving deferral issues."
            Display: "The 'Handling QA Deferral Failures' workflow will guide resolution."
            Display: ""

            # Set flag for later use
            $QA_DEFERRAL_FAILURE = true
            $QA_FAILURE_REPORT = latest_report

        ELIF report contains "Coverage Below Threshold":
            Display: "⚠ Previous QA failed due to coverage issues"
            Display: "  Focus: Increase test coverage"
            $QA_COVERAGE_FAILURE = true

        ELIF report contains "Anti-Pattern Violations":
            Display: "⚠ Previous QA failed due to anti-patterns"
            Display: "  Focus: Refactor to remove violations"
            $QA_ANTIPATTERN_FAILURE = true

        ELSE:
            Display: "⚠ Previous QA failed (review report for details)"
            Display: "  Report: {latest_report}"
            $QA_GENERIC_FAILURE = true

    ELIF report contains "Status: PASSED":
        # QA already passed - unusual to be in Dev again
        Display: "Note: QA already passed for this story"
        Display: "  Proceeding with development (may be enhancement or bug fix)"
        $QA_PASSED = true

ELSE:
    # No QA reports found - first development iteration
    Display: "✓ First development iteration (no previous QA attempts)"
    $QA_FIRST_ITERATION = true
```

**Token cost:** ~1,500 tokens (Glob + Read + Grep + parsing)

**Use in subsequent phases:**
- If `$QA_DEFERRAL_FAILURE == true` → Invoke "Handling QA Deferral Failures" workflow
- If `$QA_COVERAGE_FAILURE == true` → Focus on test coverage in Phase 1
- If `$QA_ANTIPATTERN_FAILURE == true` → Extra validation in Phase 3 (Refactor)

---

## Phase 0 Complete

**All pre-flight validations passed. Ready to begin TDD cycle.**

**Variables set for Phases 1-5:**
- `$GIT_AVAILABLE` - Boolean
- `$WORKFLOW_MODE` - "full", "partial", or "fallback"
- `$CAN_COMMIT` - Boolean
- `$TEST_COMMAND` - e.g., "pytest", "npm test", "dotnet test"
- `$TEST_COVERAGE_COMMAND` - e.g., "pytest --cov", "npm test -- --coverage"
- `$BUILD_COMMAND` - e.g., "dotnet build", "npm run build"
- `$QA_*_FAILURE` - Boolean flags for QA failure context

**Next:** Proceed to Phase 1 (Test-First Design - Red Phase)
