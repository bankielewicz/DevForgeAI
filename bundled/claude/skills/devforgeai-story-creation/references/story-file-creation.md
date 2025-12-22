# Phase 5: Story File Creation

Construct complete story document from collected information and write to disk.

## Overview

This phase assembles all information gathered from Phases 1-4 into a complete story document following DevForgeAI structure standards.

---

## Step 5.1: Load Story Template

**Objective:** Load base template structure

**Read template from assets:**
```
template = Read(file_path=".claude/skills/devforgeai-story-creation/assets/templates/story-template.md")
```

**Load structure guide:**
```
Read(file_path=".claude/skills/devforgeai-story-creation/references/story-structure-guide.md")
```

This reference provides:
- YAML frontmatter field descriptions
- Required vs optional sections
- Section ordering requirements
- Markdown formatting standards

---

## Step 5.2: Construct YAML Frontmatter

**Objective:** Build frontmatter with all metadata from Phase 1

**Build frontmatter with all metadata:**

```yaml
---
id: {story_id}                     # STORY-001, STORY-002, etc.
title: {brief_title}               # 5-10 words, descriptive
epic: {epic_id or null}            # EPIC-001 or null
sprint: {sprint_id or "Backlog"}   # SPRINT-001 or "Backlog"
status: Backlog                    # Always "Backlog" initially
priority: {Critical|High|Medium|Low}
points: {1|2|3|5|8|13}
created: {YYYY-MM-DD}              # Today's date
updated: {YYYY-MM-DD}              # Same as created initially
assigned_to: null                  # Not assigned yet
tags: []                           # Empty initially, can add later
---
```

**Generate brief title from feature description:**
```
# Example: "Add user registration with email verification"
# Title: "User registration with email verification"

# Keep under 80 characters
# Remove filler words ("add", "implement", "create")
# Use title case
```

---

## Step 5.3: Build Markdown Sections

**Objective:** Assemble all sections from previous phases

**Section 1: User Story**
```markdown
## User Story

As a {role},
I want {action},
So that {benefit}.
```

**Section 2: Acceptance Criteria**
```markdown
## Acceptance Criteria

### AC1: {Criterion title}
**Given** {context/precondition}
**When** {action/trigger}
**Then** {expected outcome}

### AC2: {Criterion title}
**Given** {context/precondition}
**When** {action/trigger}
**Then** {expected outcome}

[... all acceptance criteria from Phase 2 ...]
```

**Section 3: Technical Specification**
```markdown
## Technical Specification

### API Contracts

{Include API contracts from Phase 3.2 if applicable}

### Data Models

{Include data models from Phase 3.3}

### Business Rules

{Include business rules from Phase 3.4}

### Dependencies

{Include dependencies from Phase 3.5}
```

**Section 4: UI Specification (if applicable)**
```markdown
## UI Specification

### Components

{Include component documentation from Phase 4.2}

### Layout Mockup

```
{Include ASCII mockup from Phase 4.3}
```

### Component Interfaces

{Include TypeScript/C# interfaces from Phase 4.4}

### User Interactions

{Include interaction flows from Phase 4.5}

### Accessibility

{Include accessibility requirements from Phase 4.6}
```

**Section 5: Non-Functional Requirements**
```markdown
## Non-Functional Requirements

### Performance
{Performance targets from Phase 2}

### Security
{Security requirements from Phase 2}

### Usability
{Usability requirements from Phase 2}

### Scalability
{Scalability targets from Phase 2}
```

**Section 6: Edge Cases & Error Handling**
```markdown
## Edge Cases & Error Handling

{Include edge cases from Phase 2}

Example format:
1. **Case:** User closes browser during form submission
   **Expected:** Transaction completes or rolls back, no partial state

2. **Case:** Duplicate email registration attempt
   **Expected:** Error message "Email already registered", suggest login
```

**Step 5.3.5: Generate AC Verification Checklist Section [NEW - RCA-011]**

**Purpose:** Break down acceptance criteria into granular, testable sub-items mapped to TDD phases

**See:** `devforgeai/specs/enhancements/AC-CHECKLIST-TEMPLATE-DESIGN.md` for complete generation logic

**Generate checklist by analyzing ACs:**
```
ac_verification_checklist_section = "## Acceptance Criteria Verification Checklist\n\n"
ac_verification_checklist_section += "**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.\n\n"
ac_verification_checklist_section += "**Usage:** The devforgeai-development skill updates this checklist at the end of each TDD phase (Phases 1-5), providing granular visibility into AC completion progress.\n\n"
ac_verification_checklist_section += "**Tracking Mechanisms:**\n"
ac_verification_checklist_section += "- **TodoWrite:** Phase-level tracking (AI monitors workflow position)\n"
ac_verification_checklist_section += "- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE\n"
ac_verification_checklist_section += "- **Definition of Done:** Official completion record (quality gate validation)\n\n"

FOR each AC in acceptance_criteria:
  ac_verification_checklist_section += f"### AC#{ac.number}: {ac.title}\n\n"

  # Break AC into testable sub-items
  sub_items = generate_sub_items_from_ac(ac)

  FOR each sub_item in sub_items:
    # Infer phase mapping
    phase = infer_phase_from_item(sub_item)

    # Infer evidence location
    evidence = infer_evidence_location(sub_item, story_type)

    ac_verification_checklist_section += f"- [ ] {sub_item} - **Phase:** {phase} - **Evidence:** {evidence}\n"

  ac_verification_checklist_section += "\n"

ac_verification_checklist_section += "---\n\n"
ac_verification_checklist_section += "**Checklist Progress:** 0/{total_items} items complete (0%)\n\n"
```

**Helper function: generate_sub_items_from_ac(ac):**
```
IF ac contains Given/When/Then:
  Extract testable assertions from Then clause
  Example: "Then user receives 201 Created" → "201 Created response validated"

IF ac contains metrics (≤, ≥, <, >):
  Extract metric as sub-item
  Example: "Character count ≤15,000" → "Character count ≤15,000"

IF ac contains "all", "every", "each":
  Create sub-item for each instance
  Example: "All 6 scenarios pass" → 6 sub-items (one per scenario)

IF ac mentions implementation:
  Create implementation sub-item
  Example: "Business logic extracted" → "Business logic in correct location"
```

**Helper function: infer_phase_from_item(sub_item):**
```
IF sub_item contains "test" or "coverage":
  RETURN 1  # Red phase (test generation)

ELIF sub_item contains "implement" or "create" or "endpoint" or "code":
  RETURN 2  # Green phase (implementation)

ELIF sub_item contains "refactor" or "quality" or "complexity" or "pattern":
  RETURN 3  # Refactor phase (code quality)

ELIF sub_item contains "integration" or "scenario" or "performance" or "coverage threshold":
  RETURN 4  # Integration phase

ELIF sub_item contains "deferral" or "approval":
  RETURN 4.5  # Deferral challenge

ELIF sub_item contains "commit" or "status" or "backward":
  RETURN 5  # Git workflow

ELSE:
  RETURN 2  # Default to implementation phase
```

**Helper function: infer_evidence_location(sub_item, story_type):**
```
IF sub_item contains "test":
  IF story_type == "CRUD":
    RETURN "tests/integration/test_{entity}_crud.py"
  ELIF story_type == "Refactoring":
    RETURN "tests/unit/test_{component}_refactoring.py"
  ELSE:
    RETURN "tests/ (test files)"

ELIF sub_item contains "character count" or "line count":
  RETURN "wc -c/-l < {file_path}"

ELIF sub_item contains "endpoint":
  RETURN "src/controllers/{entity}.controller.{ext}"

ELIF sub_item contains "commit":
  RETURN "git log -1"

ELSE:
  RETURN "{implementation_location}"
```

---

**Section 7: Definition of Done**
```markdown
## Definition of Done

### Implementation
- [ ] All acceptance criteria implemented
- [ ] Unit tests written and passing (95% coverage for business logic)
- [ ] Integration tests written and passing
- [ ] API endpoints implemented (if applicable)
- [ ] UI components implemented (if applicable)
- [ ] Error handling implemented for all edge cases
- [ ] Logging added for debugging

### Code Quality
- [ ] Code follows coding-standards.md
- [ ] No violations of architecture-constraints.md
- [ ] No anti-patterns from anti-patterns.md
- [ ] Cyclomatic complexity <10 per method
- [ ] Code review completed

### Testing
- [ ] All acceptance criteria have automated tests
- [ ] Edge cases have tests
- [ ] Test coverage meets thresholds (95%/85%/80%)
- [ ] All tests passing (100% pass rate)

### Documentation
- [ ] Code comments for complex logic
- [ ] API documentation generated (Swagger/OpenAPI)
- [ ] README updated if needed

### Security
- [ ] Input validation implemented
- [ ] Authentication/authorization implemented (if applicable)
- [ ] No hardcoded secrets or credentials
- [ ] Security scan passed (no CRITICAL or HIGH vulnerabilities)
```

**Section 8: Workflow History**
```markdown
## Workflow History

- **{timestamp}** - Story created, status: Backlog
```

---

## Step 5.4: Write Story File

**Objective:** Write complete story document to disk

**Construct complete file:**
```
story_content = f"""---
{frontmatter}
---

{user_story_section}

{acceptance_criteria_section}

{technical_specification_section}

{ui_specification_section or ''}

{nfr_section}

{edge_cases_section}

{ac_verification_checklist_section}

{definition_of_done_section}

{workflow_history_section}
"""
```

**Note:** `ac_verification_checklist_section` is generated in Step 5.3.5 (NEW - RCA-011)

**Write to disk:**
```
# Ensure directory exists
Bash(mkdir -p devforgeai/specs/Stories/)

# Generate filename slug
slug = slugify(title)  # "user-registration" from "User Registration"

# Write file
Write(
  file_path=f"devforgeai/specs/Stories/{story_id}-{slug}.story.md",
  content=story_content
)
```

**Verify file creation:**
```
# Read back to confirm
created_file = Read(file_path=f"devforgeai/specs/Stories/{story_id}-{slug}.story.md", limit=30)

# Verify frontmatter parses correctly
if not created_file.startswith("---"):
    ERROR: Story file creation failed or corrupted
```

**Update TodoWrite:**
```
TodoWrite: Mark story creation as completed
```

---

## Reference Files Used

**Phase 5 references:**
- `assets/templates/story-template.md` (609 lines) - Base template structure
- `story-structure-guide.md` (662 lines) - YAML frontmatter, section formatting

---

## Output

**Phase 5 produces:**
- ✅ Complete story file created at `devforgeai/specs/Stories/{STORY-ID}-{slug}.story.md`
- ✅ All sections populated (user story, AC, tech spec, UI spec, NFRs, edge cases, DoD, history)
- ✅ YAML frontmatter valid
- ✅ File verified on disk

---

## Error Handling

**Error 1: File write failed**
- **Detection:** Write tool returns error or file doesn't exist after write
- **Recovery:** Check directory permissions, verify path, retry write

**Error 2: YAML frontmatter invalid**
- **Detection:** Read-back shows corrupted frontmatter (missing ---, invalid fields)
- **Recovery:** Reconstruct frontmatter, validate all fields, re-write

**Error 3: Missing required sections**
- **Detection:** Sections from Phases 2-4 not included in final document
- **Recovery:** Verify phase outputs exist, re-assemble content

See `error-handling.md` for comprehensive error recovery procedures.

---

## Next Phase

**After Phase 5 completes →** Phase 6: Epic/Sprint Linking

Load `epic-sprint-linking.md` for Phase 6 workflow.
