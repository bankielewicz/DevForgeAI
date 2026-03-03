# Phase 3.4-3.5: Completion Summary & Next Action Determination

Present ideation results and determine appropriate next steps based on project type and existing context.

## Table of Contents

- [Step 3.3.5: Validate-Fix-Repeat Feedback Loop](#step-335-validate-fix-repeat-feedback-loop)
- [Step 3.4: Present Completion Summary](#step-34-present-completion-summary)
- [Step 3.5: Determine Next Action](#step-35-determine-next-action)
- [Transition Logic Summary](#transition-logic-summary)
- [Phase 3.5: Display Final Summary](#phase-35-display-final-summary)
- [Common Issues and Recovery](#common-issues-and-recovery)
- [Integration with DevForgeAI Framework](#integration-with-devforgeai-framework)
- [Success Criteria](#success-criteria)

---

## Overview

Phase 3.4-3.5 completes the ideation workflow by presenting a comprehensive summary to the user and determining the appropriate next action (epic creation for all projects, then architecture creation for greenfield or orchestration for brownfield).

**Duration:** 2-5 minutes
**Output:** Completion summary with requirements.md artifact and next action recommendation

---

## Step 3.3.5: Validate-Fix-Repeat Feedback Loop

Replace the validate-halt pattern with a validate-fix-repeat feedback loop for resilient handoff validation.

### Feedback Loop Pattern

```
MAX_RETRIES = 3
retry_count = 0

WHILE retry_count < MAX_RETRIES:
    validation_result = validate_requirements()

    IF validation_result.status == "PASS":
        BREAK  # Proceed to completion

    IF validation_result.has_auto_fixable_issues:
        # Auto-fix where possible (formatting, missing optional fields)
        auto_fix(validation_result.fixable_issues)
        # Re-validate after fix to confirm resolution
        retry_count += 1
        CONTINUE  # Loop back to validate again

    IF validation_result.has_unfixable_critical_failures:
        # HALT on unfixable critical failures (missing required context files, schema violations)
        HALT: "Critical validation failure - cannot auto-fix"
        Display: validation_result.critical_errors
        RETURN failure

    # Non-critical, non-auto-fixable: warn and proceed
    Display: "⚠️ Warnings: {validation_result.warnings}"
    BREAK
```

### Auto-Fixable Issues (auto-fix applied)
- Missing optional YAML fields → insert defaults
- Formatting inconsistencies → normalize markdown
- Trailing whitespace → trim

### Unfixable Critical Failures (HALT)
- Missing required context files
- Schema validation failures on required fields
- Circular dependency detected

**Key Principle:** The validate-fix-repeat loop replaces the previous validate-halt pattern. Only HALT on unfixable critical failures. For everything else, auto-fix and re-validate after fix.

---

## Step 3.4: Present Completion Summary

### Generate Completion Summary

Use the **Ideation Completion Template**:

```markdown
## ✅ Ideation Complete

### Generated Artifacts

**Requirements Document:** requirements.md (YAML-structured per F4 schema)
- functional_requirements: {count} documented
- non_functional_requirements: {count} documented
- constraints: {count} identified
- dependencies: {count} identified

📁 **Location:** `devforgeai/specs/requirements/{project-name}-requirements.md`

---

### Requirements Summary

**Functional Requirements:**
- User roles: {count}
- Core features: {count}
- User stories: {count}

**Non-Functional Requirements:**
- Performance targets: {list}
- Security requirements: {list}
- Scalability targets: {list}

**Constraints:**
- Technical constraints: {count}
- Business constraints: {count}
- Regulatory constraints: {count}

---

### Next Steps

{Generated based on Step 3.5 decision - see below}
```

**Present formatted summary to user** - This is the primary output users see from ideation skill.

---

## Step 3.5: Determine Next Action

### Check for Existing Context Files

```
context_files = Glob(pattern="devforgeai/specs/context/*.md")

if len(context_files) == 6:
    # Brownfield project with existing DevForgeAI context
    project_mode = "brownfield"
    existing_context = True
else:
    # Greenfield project, need to create context
    project_mode = "greenfield"
    existing_context = False
```

### Greenfield Path (No Context Files)

**Present next action options:**

```
AskUserQuestion(
  questions=[{
    question: "Ideation phase complete. How would you like to proceed?",
    header: "Next action",
    options: [
      {
        label: "Create epics from requirements (Recommended)",
        description: "Run /create-epic to generate epic documents from requirements.md"
      },
      {
        label: "Review requirements first",
        description: "I want to review/edit requirements.md before creating epics"
      }
    ],
    multiSelect: false
  }]
)
```

**Based on user response:**

**Option: "Create epics from requirements"**

```
Report: """
Next step: Run `/create-epic {project-name}`

The architecture skill will:
1. Load requirements.md (YAML per F4 schema)
2. Perform complexity assessment
3. Generate epic documents with feature decomposition
4. Create feasibility analysis

After epic creation:
1. Run `/create-context {project-name}` to establish architectural constraints
2. Run `/create-missing-stories` to generate stories from epic features
3. Run `/create-sprint 1` to begin sprint planning
"""
```

**Option: "Review requirements first"**

```
Report: """
📂 Review this file:
- **Requirements:** `devforgeai/specs/requirements/{project-name}-requirements.md`

You can:
- Manually edit the YAML-structured requirements.md
- Ask me to make specific changes
- Run `/create-epic {project-name}` when ready to proceed

The requirements.md follows F4 schema with:
- functional_requirements
- non_functional_requirements
- constraints
- dependencies
"""
```

### Brownfield Path (Context Files Exist)

**Validate requirements against existing constraints:**

```
# Load existing context
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")

# Check for conflicts (should have been resolved in Phase 5)
# If new conflicts found, use AskUserQuestion to resolve
conflicts = validate_against_context_files(requirements)

if len(conflicts) > 0:
    # Present conflicts and resolution options
    for conflict in conflicts:
        AskUserQuestion(
            question: f"Requirement '{conflict.requirement}' conflicts with {conflict.context_file}. Resolve?",
            header: "Constraint conflict",
            options: [
                "Update context file (requires ADR)",
                "Modify requirement to comply",
                "Defer to future release"
            ]
        )

    # Document resolutions
    # Update requirements spec with resolved conflicts
```

**Present next action options:**

```
AskUserQuestion(
  questions=[{
    question: "Ideation complete. Context files detected. How would you like to proceed?",
    header: "Next action",
    options: [
      {
        label: "Proceed to sprint planning",
        description: "Create Sprint 1 with /create-sprint (existing context will be used)"
      },
      {
        label: "Update context files",
        description: "Run /create-context to update existing constraints (creates ADRs for changes)"
      },
      {
        label: "Review requirements first",
        description: "I want to review/edit generated requirements before proceeding"
      }
    ],
    multiSelect: false
  }]
)
```

**Based on user response:**

**Option: "Proceed to sprint planning"**

```
Report: """
✅ Requirements validated against existing constraints

Next steps:
1. Run `/create-missing-stories` to generate stories from epic features
2. Run `/create-sprint 1` to begin sprint planning

The orchestration skill will:
1. Use existing context files (tech-stack, architecture-constraints, etc.)
2. Reference epic documents from ideation
3. Create Sprint 1 plan with goals and capacity
4. Select stories from epic features for Sprint 1
5. Update story status to "Ready for Dev"

After sprint planning, run `/dev {STORY-ID}` to implement first story.
"""
```

**Option: "Update context files"**

```
Report: """
Next step: Run `/create-context {project-name}`

The architecture skill will:
1. Load existing context files
2. Review new requirements for conflicts
3. Ask technology preference questions for new capabilities
4. Update context files as needed
5. Create ADRs documenting changes (preserves decision history)
6. Validate updated constraints

This is recommended when:
- New requirements need different technologies
- New architecture patterns needed
- Compliance requirements changed
"""
```

**Option: "Review requirements first"**

```
Report: """
📂 Review this file:
- **Requirements:** `devforgeai/specs/requirements/{project-name}-requirements.md`
- **Existing Context:** `devforgeai/specs/context/*.md`

After review, proceed with:
- `/create-epic {project-name}` (to generate epics from requirements)
- `/create-sprint 1` (if context files are current)
"""
```

---

## Transition Logic Summary

**Decision Tree:**

```
Ideation Complete
  ↓
Check context files exist?
  ├─ NO (Greenfield)
  │   ↓
  │   User choice: Create context | Review first
  │   ↓
  │   If "Create context":
  │       → /create-context (architecture skill)
  │       → /create-missing-stories (story generation)
  │       → /create-sprint (orchestration skill)
  │   If "Review first":
  │       → User reviews files
  │       → Then /create-context when ready
  │
  └─ YES (Brownfield)
      ↓
      Validate against context
      ↓
      User choice: Sprint planning | Update context | Review first
      ↓
      If "Sprint planning":
          → /create-sprint (orchestration skill)
      If "Update context":
          → /create-context (architecture skill with ADRs)
          → Then /create-sprint
      If "Review first":
          → User reviews files
          → Then /create-sprint or /create-context when ready
```

---

## Output from Phase 3.4-3.5

**Completion summary presented to user** (formatted markdown)

**Next action determined** - One of:
- `/create-context {project-name}` (greenfield or context update)
- `/create-sprint 1` (brownfield with valid context)
- User review (pause for manual editing)

**Ideation skill completes** - Handoff successful

---

## Phase 3.5: Display Final Summary

**Purpose:** Present compact, actionable summary following QA skill pattern (Step 4.3).

**Display Template:**

```
╔════════════════════════════════════════════════════════╗
║               IDEATION COMPLETE                        ║
╠════════════════════════════════════════════════════════╣
║ Project: {project_name}                                ║
║ Mode: {Greenfield|Brownfield}                          ║
╠════════════════════════════════════════════════════════╣
║ Generated Artifacts:                                   ║
║   requirements.md: YAML per F4 schema                  ║
║   Functional Requirements: {count}                     ║
║   Non-Functional Requirements: {count}                 ║
║   Constraints: {count}                                 ║
╠════════════════════════════════════════════════════════╣
║ Next Steps (in order):                                 ║
║   1. /create-epic {project}                            ║
║   2. /create-context {project}                         ║
║   3. /create-sprint 1                                  ║
║   4. /dev {STORY-ID}                                   ║
╚════════════════════════════════════════════════════════╝
```

**Key Difference from QA Skill:**
- QA has pass/fail outcome variants
- Ideation produces requirements.md for downstream epic creation
- Both use numbered next steps for clarity

---

## Common Issues and Recovery

### Issue: User Unsure About Next Action

**Symptom:** User selects "Review requirements first" but uncertain what to review

**Recovery:**

```
Provide specific review guidance:

"Review these aspects of requirements.md:

1. **Functional Requirements:** Are all core features documented?
   - Check: functional_requirements section

2. **Non-Functional Requirements:** Are metrics quantified?
   - Check: non_functional_requirements section

3. **Constraints:** Are all constraints identified?
   - Check: constraints section

4. **Dependencies:** Are all external systems listed?
   - Check: dependencies section

After review, run `/create-epic {project-name}` to proceed."
```

### Issue: User Wants to Modify Requirements

**Symptom:** User says "Add requirement X to the list"

**Recovery:**

```
# Use Edit tool to modify requirements.md
Read(file_path="devforgeai/specs/requirements/{project-name}-requirements.md")

# Add requirement to appropriate section
Edit(
    file_path="devforgeai/specs/requirements/{project-name}-requirements.md",
    old_string="{existing section}",
    new_string="{existing section + new requirement}"
)

# Re-run validation to ensure F4 schema compliance
```

---

## References Used in Phase 3.4-3.5

**Primary:**
- **output-templates.md** (619 lines) - Completion summary templates, technology recommendations by tier

**Related:**
- **validation-checklists.md** - Handoff readiness criteria
- **domain-specific-patterns.md** - Domain-specific guidance for next steps

**On Error:**
- **error-handling.md** - Handoff failure recovery

---

## Success Criteria

Completion handoff successful when:
- [ ] Completion summary presented to user
- [ ] All artifacts listed with locations
- [ ] Complexity assessment communicated
- [ ] Technology recommendations provided
- [ ] Risk summary presented
- [ ] Next action determined (greenfield vs brownfield path)
- [ ] User understands what to do next
- [ ] Ideation workflow complete

**Token Budget:** ~3,000-6,000 tokens (load templates, generate summary, determine next action)

---

## Final Output Example

**What user sees:**

```
## ✅ Ideation Complete

### Generated Artifacts

**Requirements Document:** requirements.md (YAML per F4 schema)
- functional_requirements: 32 documented
- non_functional_requirements: 18 documented
- constraints: 8 identified
- dependencies: 5 external systems

📁 Location: `devforgeai/specs/requirements/ecommerce-platform-requirements.md`

---

### Next Steps

**Recommended action: Create epics from requirements**

Run `/create-epic ecommerce-platform`

The architecture skill will:
1. Load requirements.md (YAML per F4 schema)
2. Perform complexity assessment and feasibility analysis
3. Generate epic documents with feature decomposition

After epic creation:
1. Run `/create-context ecommerce-platform` to create architectural constraints
2. Run `/create-missing-stories` to generate stories from epic features
3. Run `/create-sprint 1` to select stories into sprint capacity

---

**Ideation complete.** Requirements discovery and elicitation finished. Ready for /create-epic.
```

---

## Common Issues and Recovery

### Issue: User Confused About Next Action

**Symptom:** User asks "What should I do now?"

**Recovery:**

```
Clarify based on project mode:

Greenfield: "Run `/create-context {project-name}` next. This creates the 6 architectural constraint files that prevent technical debt."

Brownfield: "Run `/create-sprint 1` next. This uses existing context files to plan Sprint 1 and generate stories from your epics."

Always: "You can review/edit epic documents in `devforgeai/specs/Epics/` before proceeding."
```

### Issue: User Wants Different Technology Than Recommended

**Symptom:** User says "I want to use technology X instead of recommended Y"

**Recovery:**

```
Acknowledge: "Technology recommendations are based on complexity tier, not mandatory."

Explain: "During `/create-context`, you'll be asked to choose technologies. You can select {preferred technology} at that time."

Note: "The architecture skill will validate your choices against requirements (performance, scalability, etc.) and create ADRs documenting decisions."

Proceed: Continue to next action (user makes final technology decisions in architecture phase)
```

### Issue: Completion Summary Too Long

**Symptom:** Summary is overwhelming with too much detail

**Recovery:**

```
# Create executive summary version (short)
Executive Summary (~30 lines):
- Requirements documented: {count}
- Next action: /create-epic

# Link to full details
"See complete details in:"
- Requirements: `devforgeai/specs/requirements/`
```

---

## Integration with DevForgeAI Framework

### Flows to Next Skills

**All projects:**
- Ideation → **/create-epic** (architecture skill creates epics) → /create-context → /create-sprint

### What Happens Next

**/create-epic receives:**
- requirements.md (YAML per F4 schema)

**/create-epic produces:**
- Epic documents with feature decomposition
- Complexity assessment
- Feasibility analysis

**Architecture skill (/create-context) receives:**
- Requirements specification
- Epic documents
- Constraints and assumptions

**Architecture skill produces:**
- 6 context files (immutable constraints)
- ADRs documenting technology decisions

**Orchestration skill receives:**
- Epic documents
- Context files (from architecture)
- Requirements spec

**Orchestration skill produces:**
- Sprint 1 plan
- Stories generated from epic features
- Story workflow setup

---

## Success Criteria

Steps 3.4-3.5 complete when:
- [ ] Completion summary presented to user
- [ ] requirements.md artifact listed
- [ ] Next action determined (/create-epic recommended)
- [ ] User knows exactly what to do next
- [ ] Ideation skill exits gracefully

**Token Budget:** ~2,000-4,000 tokens (generate summary, user interaction)

---

**Phase 3 Complete** - Ideation skill has successfully transformed business idea into structured requirements.md ready for /create-epic and architecture phases.

---

## References Used

**Primary:**
- [validation-checklists.md](validation-checklists.md) - Handoff readiness validation

---

**Ideation Workflow Complete** ✅
