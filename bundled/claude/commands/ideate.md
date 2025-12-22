---
description: Transform business idea into structured requirements
argument-hint: [business-idea-description]
model: haiku
allowed-tools: Read, Write, Edit, Glob, Skill, AskUserQuestion
---

# /ideate - Transform Business Idea into Structured Requirements

**Purpose:** Entry point for DevForgeAI framework - transforms business ideas into structured epics and requirements through comprehensive discovery.

**Output:** Epic documents, requirements specification, complexity assessment

**Process:** Invokes `devforgeai-ideation` skill which executes 6-phase discovery with 10-60 interactive questions.

---

## Phase 1: Argument Validation

### 1.1 Capture Business Idea

**Business idea from user:**
```
$ARGUMENTS
```

**If no arguments provided:**

Use AskUserQuestion to capture business idea:

```
AskUserQuestion(
  questions=[{
    question: "Please describe the business idea, feature, or problem you want to explore",
    header: "Business idea",
    options: [
      {
        label: "New project/product",
        description: "Starting from scratch (greenfield)"
      },
      {
        label: "Feature for existing system",
        description: "Adding to existing codebase (brownfield)"
      },
      {
        label: "Modernization/migration",
        description: "Replacing or upgrading legacy system"
      },
      {
        label: "Problem-solving",
        description: "Fixing issues in current system"
      }
    ],
    multiSelect: false
  }]
)
```

**Then ask for description:**
```
"Please provide a detailed description of the {project_type} you want to explore"
```

**Wait for user response before proceeding to Phase 2.**

### 1.2 Validate Description

**Minimum requirements:**
- Description has at least 10 words
- Describes a business capability or problem (not purely technical)

**If description too vague:**
```
Prompt user: "Please provide more details about:
- What business problem this solves
- Who the primary users/beneficiaries are
- What success looks like"
```

---

## Phase 2: Invoke Ideation Skill

### 2.1 Set Context for Skill

**Prepare context markers for skill execution:**

```
**Business Idea:** $ARGUMENTS (or user-provided description)

**Project Type:** {Greenfield|Brownfield|Modernization|Problem-solving}
```

### 2.2 Skill Invocation

**The devforgeai-ideation skill handles complete workflow:**

- **Phase 1:** Discovery & Problem Understanding (5-10 questions)
- **Phase 2:** Requirements Elicitation (15-25 questions)
- **Phase 3:** Complexity Assessment (0-60 scoring)
- **Phase 4:** Epic & Feature Decomposition
- **Phase 5:** Feasibility & Constraints Analysis
- **Phase 6:** Requirements Documentation (epics, requirements spec, validation, summary, next action)

**After skill completes:**
- **Phase N:** Hook Integration - Triggers post-ideation feedback (if configured)

**Expected interaction:**
- Skill asks 10-60 questions across 6 phases
- User answers guide requirements discovery
- Skill validates completeness internally (Phase 6.4)
- Skill generates all output artifacts
- Skill presents completion summary (Phase 6.5)
- Skill asks user for next action (Phase 6.6)

**Invoke skill:**

```
Skill(command="devforgeai-ideation")
```

**After skill invocation:**
- Skill's SKILL.md content expands inline in conversation
- **YOU execute the skill's workflow phases** (not waiting for external result)
- Follow the skill's instructions phase by phase
- Produce output as skill instructs

**The skill instructs you to:**
- Execute all 6 phases: Discovery, Requirements Elicitation, Complexity Assessment, Epic Decomposition, Feasibility Analysis, Documentation
- Handle all validation, error recovery, and user interaction (AskUserQuestion flows)
- Generate all output artifacts (epics, requirements spec, complexity assessment)
- Perform self-validation in Phase 6.4
- Present completion summary in Phase 6.5

---

## Phase 3: Verify Skill Completion

### 3.1 Check Skill Completion Status

**After skill returns control:**

Verify skill completed successfully by checking for expected artifacts:

```
# Check for epic documents
epic_files = Glob(pattern="devforgeai/specs/Epics/EPIC-*.epic.md")

# Check for requirements specification
req_files = Glob(pattern="devforgeai/specs/requirements/*.md")
```

**Expected artifacts:**
- 1+ epic documents in `devforgeai/specs/Epics/`
- 1 requirements specification in `devforgeai/specs/requirements/`
- Complexity assessment (embedded in requirements spec)

### 3.2 Handle Incomplete Execution

**If artifacts missing:**

```
if len(epic_files) == 0 or len(req_files) == 0:
    Report: """
    ⚠️ Ideation Skill Incomplete

    Expected artifacts not found:
    - Epic documents: {len(epic_files)} found (expected: 1+)
    - Requirements spec: {len(req_files)} found (expected: 1)

    Possible causes:
    1. Skill execution interrupted
    2. File system write permissions issue
    3. User exited during discovery questions

    Recommended action:
    - Re-run `/ideate [business-idea]` to complete ideation
    - Or check `devforgeai/specs/Epics/` and `devforgeai/specs/requirements/` for partial files
    """

    HALT - Do not proceed to Phase 4
```

**If artifacts present:**

```
✓ Skill completed successfully
✓ {len(epic_files)} epic document(s) created
✓ Requirements specification created

→ Proceed to Phase 4
```

---

## Phase 4: Quick Summary

**Note:** Skill already presented detailed summary in Phase 6.5. This phase provides brief confirmation only.

### 4.1 Confirm Completion

**Read first epic for quick validation:**

```
Read(file_path=epic_files[0], limit=20)  # Read frontmatter only
```

**Extract:**
- Epic count: {len(epic_files)}
- First epic title
- Complexity score (from requirements spec if needed)

**Brief confirmation:**

```
✅ Ideation phase complete

Generated:
- {epic_count} epic document(s) in devforgeai/specs/Epics/
- Requirements specification in devforgeai/specs/requirements/

The devforgeai-ideation skill has:
✓ Discovered and documented requirements
✓ Assessed complexity and recommended architecture tier
✓ Generated epic and requirements artifacts
✓ Validated all outputs (Phase 6.4)
✓ Presented detailed summary (Phase 6.5)
✓ Asked you for next action (Phase 6.6)
```

**Note:** If user missed skill's summary or next action prompt, they can review:
- Epic documents: `devforgeai/specs/Epics/EPIC-*.epic.md`
- Requirements spec: `devforgeai/specs/requirements/*.md`

---

## Phase 5: Verify Next Steps Communicated

### 5.1 Ensure User Understands Next Action

**Skill already asked user in Phase 6.6, but confirm understanding:**

```
The ideation skill should have asked you to choose next action:
- Create context files (run /create-context)
- Review requirements first
- Skip to orchestration (if context files exist)

If you didn't respond to that question or need clarification:
```

**Ask again:**

```
AskUserQuestion(
  questions=[{
    question: "Ready to proceed with next phase?",
    header: "Next step",
    options: [
      {
        label: "Yes - create context files",
        description: "Run /create-context to define architectural constraints (6 context files)"
      },
      {
        label: "Review requirements first",
        description: "I want to review/edit the generated requirements before proceeding"
      },
      {
        label: "Help - what are context files?",
        description: "Explain what /create-context does and why it's needed"
      }
    ],
    multiSelect: false
  }]
)
```

**Based on response:**

**"Yes - create context files":**
```
Run: `/create-context [project-name]`

Replace `[project-name]` with a short identifier (e.g., `task-manager`, `inventory-system`)

The architecture skill will:
1. Reference your requirements and complexity tier
2. Ask technology preference questions
3. Generate 6 context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
4. Create initial ADR
5. Validate requirements against constraints
```

**"Review requirements first":**
```
Review these files:
- Epics: `devforgeai/specs/Epics/EPIC-*.epic.md`
- Requirements: `devforgeai/specs/requirements/[project]-requirements.md`

You can:
- Manually edit files with your editor
- Ask me to make specific changes
- Run `/create-context [project-name]` when ready
```

**"Help - what are context files?":**
```
Context files are 6 immutable constraint documents that prevent technical debt:

1. **tech-stack.md** - Locked technology choices
   - Prevents library substitution
   - Example: "Use React 18+, not Vue"

2. **source-tree.md** - Project structure rules
   - Prevents chaos
   - Example: "Tests in tests/, source in src/"

3. **dependencies.md** - Approved packages
   - Prevents bloat
   - Example: "Express ^4.18.0 for web framework"

4. **coding-standards.md** - Code patterns
   - Enforces consistency
   - Example: "PascalCase for classes, camelCase for functions"

5. **architecture-constraints.md** - Layer boundaries
   - Prevents violations
   - Example: "Domain cannot import Infrastructure"

6. **anti-patterns.md** - Forbidden patterns
   - Prevents technical debt
   - Example: "No God Objects (classes >500 lines)"

These files ensure all development follows defined standards, preventing technical debt accumulation.

Once created, run:
- `/create-sprint 1` to plan first sprint
- `/create-story [description]` to create individual stories
- `/dev STORY-ID` to implement stories with TDD
```

---

## Phase N: Hook Integration

**Invoke reusable helper function for feedback hook integration:**

```bash
# Collect ideation artifacts for context
EPIC_FILES=$(ls -1 devforgeai/specs/Epics/EPIC-*.epic.md 2>/dev/null | tr '\n' ',' | sed 's/,$//' || echo "")

# Invoke helper function (handles check-hooks + invoke-hooks)
# Helper returns: exit 0 (success or graceful skip), never fails
.claude/scripts/invoke_feedback_hooks.sh ideate completed \
  --operation-type=ideation \
  --artifacts="$EPIC_FILES" || true
```

**Helper function handles:**
- N.1: Check hook eligibility (`devforgeai-validate check-hooks --operation=ideate --status=completed`)
- N.2: Invoke hooks if eligible (`devforgeai-validate invoke-hooks --operation=ideate ...`)
- N.3: Display status ("✓ Post-ideation feedback initiated" or "⚠ skipped")
- Error handling: All failures are non-blocking, command always succeeds

**Parameters passed to hooks:**
- `--operation-type=ideation` - Identifies this as ideation operation
- `--artifacts` - Comma-separated list of created epic files

**Note:** Complexity score and questions-asked count are captured by the ideation skill internally (Phase 6 summary) and passed via environment if needed.

**Next:** Proceed to Phase completion

---

## Error Handling

### Skill Invocation Failed

**If skill does not execute or throws error:**

```
ERROR: devforgeai-ideation skill invocation failed

Troubleshooting steps:
1. Verify skill file exists:
   Glob(pattern=".claude/skills/devforgeai-ideation/SKILL.md")

2. Check skill is properly registered (restart Claude Code terminal if needed)

3. Verify allowed-tools permissions include Skill tool

If issue persists:
- Review skill file for syntax errors
- Check skill frontmatter is valid YAML
- Try invoking skill directly: Skill(command="devforgeai-ideation")
```

### Artifacts Missing After Skill Completion

**If skill completes but artifacts missing:**

```
⚠️ Skill completed but expected artifacts not found

This indicates either:
1. Skill encountered errors during artifact generation
2. File system write permissions issue
3. Incorrect directory paths

Recommended action:
1. Check if skill reported any errors during execution
2. Verify directories exist and are writable:
   - devforgeai/specs/Epics/
   - devforgeai/specs/requirements/
3. Re-run `/ideate [business-idea]` to retry artifact generation
4. If persistent: Create artifacts manually and proceed to /create-context
```

### User Exits During Discovery

**If user cancels during skill's 10-60 question discovery:**

```
Ideation incomplete - user exited during discovery phase

To complete ideation:
- Re-run `/ideate [business-idea]` and answer all discovery questions
- Or skip ideation and create requirements manually

Note: Comprehensive discovery ensures zero ambiguity in requirements, preventing technical debt downstream.
```

---

## Command Complete

**This command delegates all implementation logic to the devforgeai-ideation skill.**

**Command responsibilities:**
- ✅ Argument validation and capture
- ✅ Skill invocation with context markers
- ✅ Basic artifact existence verification
- ✅ Brief completion confirmation
- ✅ Next steps guidance
- ✅ Hook eligibility checking and feedback invocation (Phase N)

**Skill responsibilities:**
- ✅ Complete 6-phase discovery workflow
- ✅ User interaction (10-60 questions)
- ✅ Epic and requirements generation
- ✅ Self-validation (Phase 6.4)
- ✅ Detailed summary presentation (Phase 6.5)
- ✅ Next action determination (Phase 6.6)
- ✅ Error handling and recovery

**Architecture principle:** Commands orchestrate, skills implement, references provide deep knowledge through progressive disclosure.
