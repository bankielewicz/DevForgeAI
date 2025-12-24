---
description: Transform business idea into structured requirements
argument-hint: [business-idea-description]
model: opus
allowed-tools: Read, Write, Edit, Glob, Skill, AskUserQuestion
---

# /ideate - Transform Business Idea into Structured Requirements

**Purpose:** Entry point for DevForgeAI framework - transforms business ideas into structured epics and requirements through comprehensive discovery.

**Output:** Epic documents, requirements specification, complexity assessment

**Process:** Invokes `devforgeai-ideation` skill which executes 6-phase discovery with 10-60 interactive questions.

---

## Phase 0: Brainstorm Auto-Detection

**Purpose:** Check for existing brainstorm documents and offer to use them as input.

### 0.1 Check for Existing Brainstorms

**Search for brainstorm documents:**
```
brainstorms = Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.brainstorm.md")
```

**If brainstorms found:**
```
IF len(brainstorms) > 0:
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Existing Brainstorm(s) Detected
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  FOR each brainstorm:
    # Read frontmatter to get title and confidence
    Read(file_path=brainstorm, limit=30)
    Display: "- {id}: {title} (Confidence: {confidence_level})"
```

**Ask user if they want to use a brainstorm:**
```
AskUserQuestion(
  questions=[{
    question: "Would you like to use an existing brainstorm as input for ideation?",
    header: "Brainstorm",
    options: [
      {
        label: "Yes - use most recent",
        description: "Pre-populate ideation with brainstorm data"
      },
      {
        label: "Yes - let me choose",
        description: "Select which brainstorm to use"
      },
      {
        label: "No - start fresh",
        description: "Begin new ideation discovery"
      }
    ],
    multiSelect: false
  }]
)
```

### 0.2 Load Brainstorm Context (if selected)

**If user selected a brainstorm:**
```
# Read full brainstorm document
brainstorm_content = Read(file_path=selected_brainstorm)

# Extract YAML frontmatter
frontmatter = parse_yaml_frontmatter(brainstorm_content)

# Set context markers for skill
$BRAINSTORM_CONTEXT = {
  brainstorm_id: frontmatter.id,
  problem_statement: frontmatter.problem_statement,
  target_outcome: frontmatter.target_outcome,
  user_personas: frontmatter.user_personas,
  hard_constraints: frontmatter.hard_constraints,
  must_have_capabilities: frontmatter.must_have_capabilities,
  critical_assumptions: frontmatter.critical_assumptions,
  confidence_level: frontmatter.confidence_level
}

Display:
"Pre-populated from {brainstorm_id}:
  ✓ Problem: {problem_statement}
  ✓ Users: {len(user_personas)} persona(s)
  ✓ Constraints: {len(hard_constraints)} identified
  ✓ Must-haves: {len(must_have_capabilities)} capabilities

Proceeding to ideation with brainstorm context..."
```

**If no brainstorms or user chose "start fresh":**
```
$BRAINSTORM_CONTEXT = null
# Continue to Phase 1 normally
```

### 0.3 Continue to Phase 1

Pass `$BRAINSTORM_CONTEXT` to subsequent phases. The ideation skill will use this to:
- Skip or shorten Phase 1 discovery questions (already answered in brainstorm)
- Pre-populate requirements with must-have capabilities
- Validate constraints against brainstorm findings

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

### Skill Validation Failure (Phase 6.4)

**If skill's Phase 6.4 self-validation detects critical failures:**

The skill's Phase 6.4 validates all generated artifacts and reports failures. When skill validation fails:

```
HALT: Skill validation failed

The devforgeai-ideation skill's Phase 6.4 self-validation reported critical failure(s).
Error details are displayed in the skill's validation report above.

The command does NOT attempt recovery or re-validation.
Error messages from skill Phase 6.4 are passed through verbatim.

To resolve:
1. Review the validation error message from the skill
2. Address the specific issue (e.g., missing required field, invalid YAML)
3. Re-run `/ideate [business-idea]` to retry ideation
```

**Note:** Artifact verification (YAML syntax, ID format, required fields) is delegated entirely to the skill's Phase 6.4 self-validation workflow. The command trusts skill validation results without re-verification.

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

**Command responsibilities (lean orchestration):**
- ✅ Argument validation and capture
- ✅ Brainstorm auto-detection and loading
- ✅ Skill invocation with context markers
- ✅ Hook eligibility checking and feedback invocation (Phase N)
- ✅ Error propagation from skill (HALT on skill validation failure)

**Skill responsibilities (all implementation):**
- ✅ Complete 6-phase discovery workflow
- ✅ User interaction (10-60 questions)
- ✅ Epic and requirements generation
- ✅ Self-validation of all artifacts (Phase 6.4)
- ✅ Detailed summary presentation (Phase 6.5)
- ✅ Next action determination (Phase 6.6)
- ✅ Error handling and recovery

**Validation delegation:** Command trusts skill's Phase 6.4 self-validation for artifact verification (YAML syntax, ID format, required fields). No duplicate validation logic in command.

**Architecture principle:** Commands orchestrate, skills implement, references provide deep knowledge through progressive disclosure.
