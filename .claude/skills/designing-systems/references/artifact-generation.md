# Epic Artifact Generation Reference

Epic-related artifact generation guidance extracted from ideation Phase 6 for use by the architecture skill.

## Overview

This reference contains epic-specific artifact generation patterns including constitutional template loading, section compliance, epic document creation, numbering conventions, and status management.

---

## Load Constitutional Epic Template

**CRITICAL: Before generating any epic, load the canonical template:**

```
Read(file_path=".claude/skills/devforgeai-orchestration/assets/templates/epic-template.md")
```

This ensures all generated epics contain the complete constitutional structure.

**IMPORTANT - Source of Truth Warning:**

> **DO NOT** create epics manually or use any inline template. Always load the constitutional template via the Read() instruction above. The canonical template contains all 13 required sections; abbreviated versions are incomplete and non-compliant.

### Section Compliance Checklist

| Section | Required | Purpose |
|---------|----------|---------|
| YAML Frontmatter | ✓ | Epic metadata (id, title, status, dates, points, owner, team) |
| Business Goal | ✓ | Problem statement and value proposition |
| Success Metrics | ✓ | Measurable outcomes with targets and measurement plan |
| Scope | ✓ | In-scope features and explicit out-of-scope exclusions |
| Target Sprints | ✓ | Sprint breakdown with goals, points, and deliverables |
| User Stories | ✓ | High-level stories to decompose into detailed stories |
| Technical Considerations | ✓ | Architecture, technology decisions, security, performance |
| Dependencies | ✓ | Internal and external dependencies with status tracking |
| Risks & Mitigation | ✓ | Risk register with probability, impact, and mitigation |
| Stakeholders | ✓ | Primary stakeholders and communication plan |
| Timeline | ✓ | Key milestones and epic timeline visualization |
| Progress Tracking | ✓ | Sprint summary table and burndown metrics |
| Decision Context | ✓ | Design rationale, rejected alternatives, constraints, key insights |

Every generated epic MUST contain all 13 constitutional sections. Verify against this checklist above.

**Validation:** After generating an epic, verify all 13 sections are present. Missing sections = non-compliant epic.

### Cross-Session Context Requirements

When another Claude session resumes epic generation, it needs:

- **Brainstorm document:** The source `BRAINSTORM-NNN.brainstorm.md` with problem statement and discovery data
- **Complexity score:** Phase 3 assessment results (score out of 60, architecture tier 1-4)
- **Epic decomposition:** Phase 4 feature breakdown and epic boundaries
- **Feasibility assessment:** Phase 5 risk analysis and go/no-go recommendation
- **Project context files:** If brownfield, existing `devforgeai/specs/context/*.md` constraints

**Recovery pattern:** Load brainstorm → Read complexity assessment → Load epic template → Generate compliant epic

---

## Step 6.1: Generate Epic Document(s)

### Epic Document Structure

Create epic documents in `devforgeai/specs/Epics/EPIC-NNN-[name].epic.md` following the DevForgeAI epic template.

**CRITICAL: Track epic creation with TodoWrite**

```
At start of epic generation, create todos for each epic:

TodoWrite([
  {"content": "Create EPIC-001: {name}", "status": "pending", "activeForm": "Creating EPIC-001"},
  {"content": "Create EPIC-002: {name}", "status": "pending", "activeForm": "Creating EPIC-002"},
  {"content": "Create EPIC-003: {name}", "status": "pending", "activeForm": "Creating EPIC-003"}
])

Mark each epic as in_progress before creating, completed after file written.
```

### Verify Epic Creation

**CRITICAL verification gate:**

```
# Count planned epics (from Phase 4 decomposition)
planned_epics = {count from Phase 4}

# Count created epic files
created_epic_files = Glob(pattern="devforgeai/specs/Epics/EPIC-*.epic.md")
created_count = len(created_epic_files)

# Verification gate
if created_count < planned_epics:
    # HALT - Incomplete work detected
    missing_count = planned_epics - created_count

    ERROR: Only {created_count}/{planned_epics} epics created

    Missing epics: Review Phase 4 decomposition and create remaining epic documents

    DO NOT PROCEED to Step 6.2 until all epics are created and verified.

else:
    # All epics created, safe to proceed
    ✓ All {planned_epics} epics created and verified
    → Proceed to Step 6.2
```

**Why this gate is critical:**
- Prevents incomplete artifact generation
- Ensures all planned work documented
- Catches TodoWrite tracking errors
- Verifies file system writes succeeded

---

## Step 6.1.5: Cross-Reference Auto-Update

**Purpose:** After epic documents are created, update the source requirements document to replace placeholder cross-reference IDs with actual assigned IDs.

**Context:** The requirements document at `devforgeai/specs/requirements/{project-name}-requirements.md` may contain placeholder references like `EPIC-NNN` and `ADR-NNN` that were written before actual IDs were assigned. This step resolves those placeholders.

### Replacement Procedure

```python
# Step 1: Read the source requirements document
requirements_path = "devforgeai/specs/requirements/{project-name}-requirements.md"
requirements_content = Read(file_path=requirements_path)

# Step 2: Build replacement map from created artifacts
# Epic replacements: Map each EPIC-NNN placeholder to actual EPIC-XXX ID
# ADR replacements: Map each ADR-NNN placeholder to actual ADR-XXX ID
epic_map = {
    "EPIC-NNN": "EPIC-001",  # Replace with actual assigned epic ID
    # Add additional mappings if multiple epics reference different placeholders
}
adr_map = {
    "ADR-NNN": "ADR-007",  # Replace with actual assigned ADR ID
    # Add additional mappings for each ADR created during this workflow
}

# Step 3: Apply replacements using Edit tool
for placeholder, actual_id in epic_map.items():
    Edit(file_path=requirements_path, old_string=placeholder, new_string=actual_id, replace_all=True)

for placeholder, actual_id in adr_map.items():
    Edit(file_path=requirements_path, old_string=placeholder, new_string=actual_id, replace_all=True)
```

### STORY-NNN Placeholders: Leave As-Is

**Do NOT replace `STORY-NNN` placeholders.** Stories are not yet created at epic creation time. Story IDs are assigned later during sprint planning and story creation phases. Replacing them prematurely would produce incorrect references.

```python
# CORRECT: Skip STORY-NNN placeholders entirely
# STORY-NNN references will be resolved during /create-story execution

# WRONG: Do NOT attempt to resolve story placeholders
# Edit(old_string="STORY-NNN", new_string="STORY-???")  # FORBIDDEN
```

### Verification Check

```python
# After replacements, verify no stale EPIC-NNN or ADR-NNN placeholders remain
remaining_epic = Grep(pattern="EPIC-NNN", path=requirements_path, output_mode="count")
remaining_adr = Grep(pattern="ADR-NNN", path=requirements_path, output_mode="count")

if remaining_epic > 0 or remaining_adr > 0:
    WARNING: Stale placeholders remain in requirements document
    Review and resolve manually or add missing mappings

# Confirm STORY-NNN placeholders are still present (expected)
story_placeholders = Grep(pattern="STORY-NNN", path=requirements_path, output_mode="count")
# story_placeholders > 0 is EXPECTED and correct at this stage
```

---

## Step 6.1.7: Epic Completeness Scorecard Display

**Purpose:** After epic creation, display a completeness scorecard so the user can identify gaps before leaving the session.

### Scorecard Procedure

```python
# Step 1: Define the 13 constitutional sections to check
# Each section is scored as present and populated (✅) or missing or empty (⚠️)
sections = [
    "YAML Frontmatter",
    "Business Goal",
    "Success Metrics",
    "Scope",
    "Target Sprints",
    "User Stories",
    "Technical Considerations",
    "Dependencies",
    "Risks & Mitigation",
    "Stakeholders",
    "Timeline",
    "Progress Tracking",
    "Decision Context",
]

# Decision Context subsections scored individually
decision_subsections = [
    "Design Rationale",
    "Rejected Alternatives",
]

# Step 2: Score each section
scored = []
for section in sections:
    if section_present_and_populated(epic_content, section):
        scored.append(("✅", section))   # present and populated
    else:
        scored.append(("⚠️", section))   # missing or empty

# Step 3: Score Decision Context subsections individually
for sub in decision_subsections:
    if section_present_and_populated(epic_content, sub):
        scored.append(("✅", f"  └─ {sub}"))   # present and populated
    else:
        scored.append(("⚠️", f"  └─ {sub}"))   # missing or empty

# Step 4: Calculate overall score
present_count = sum(1 for s, _ in scored if s == "✅")
total_count = len(scored)
```

### Scorecard Display Format

```
Display scorecard after epic creation:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Epic Completeness Scorecard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ YAML Frontmatter
✅ Business Goal
✅ Success Metrics
⚠️ Scope
✅ Target Sprints
✅ User Stories
✅ Technical Considerations
✅ Dependencies
⚠️ Risks & Mitigation
✅ Stakeholders
✅ Timeline
✅ Progress Tracking
✅ Decision Context
  ✅ Design Rationale          (present and populated)
  ⚠️ Rejected Alternatives    (missing or empty)

Overall: 12/15 sections complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Note:** The scorecard includes the 13 constitutional sections plus Decision Context subsections (Design Rationale, Rejected Alternatives) scored individually.

---

## Directory Structure Requirements

**Expected structure after artifact generation:**

```
devforgeai/specs/
├── Epics/
│   ├── EPIC-001-user-management.epic.md
│   ├── EPIC-002-product-catalog.epic.md
│   └── EPIC-003-shopping-checkout.epic.md

devforgeai/
├── specs/
│   └── requirements/
│       └── {project-name}-requirements.md
```

**Validation:**

```
# Ensure directories exist using Write/.gitkeep pattern (Constitutional C1 compliant)
Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
Write(file_path="devforgeai/specs/requirements/.gitkeep", content="")

# Verify creation
Glob(pattern="devforgeai/specs/Epics/")  # Should exist
Glob(pattern="devforgeai/specs/requirements/")  # Should exist
```

---

## Epic Numbering Convention

**Sequential numbering starting from 001:**

```
# Find highest existing epic number
existing_epics = Glob(pattern="devforgeai/specs/Epics/EPIC-*.epic.md")

if len(existing_epics) == 0:
    next_epic_number = 1
else:
    # Extract numbers from filenames
    epic_numbers = []
    for epic_file in existing_epics:
        # Parse EPIC-NNN from filename
        number = extract_epic_number(epic_file)
        epic_numbers.append(number)

    next_epic_number = max(epic_numbers) + 1

# Format as 3-digit: EPIC-001, EPIC-002, etc.
epic_id = f"EPIC-{next_epic_number:03d}"
```

**Prevents:**
- Epic ID collisions
- Numbering gaps (if epics deleted)
- Confusion in brownfield projects

---

## Epic Status Field

**Valid statuses:**
- **Planning:** Epic created, not started (default for new epics)
- **In Progress:** At least one story started
- **Paused:** Work temporarily stopped (external blocker, reprioritization)
- **Completed:** All features delivered
- **Archived:** No longer relevant

**Status managed by:**
- Ideation skill: Sets "Planning" on creation
- Orchestration skill: Updates during story lifecycle
- Manual: User can edit status in epic file

---

## Integration with Phase 4 Decomposition

**Phase 4 provides:**
- Epic list (1-3 epics)
- Feature breakdown (3-8 features per epic)
- High-level story outlines (2-5 stories per feature)
- Epic dependencies
- Priority assignments

**Step 6.1 transforms into:**
- Structured epic documents with YAML frontmatter
- Complete feature descriptions
- Business goals and success metrics
- Complexity and architecture recommendations
- Risk register

**Key difference:** Phase 4 = planning data, Step 6.1 = formal documents

---

## Success Criteria for Epic Generation

Epic artifact generation complete when:
- [ ] All planned epics created (verified via Glob)
- [ ] All epic files have valid YAML frontmatter
- [ ] All epics have features section (3-8 features)
- [ ] All epics have business goals and success metrics
- [ ] No write errors occurred
- [ ] TodoWrite tracking matches file system reality

**Token Budget:** ~5,000-12,000 tokens (generate 1-3 epics)
