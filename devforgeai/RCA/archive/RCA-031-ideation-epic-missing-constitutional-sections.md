# RCA-031: Ideation Epic Missing Constitutional Sections

**Date:** 2026-01-26
**Reporter:** User
**Component:** devforgeai-ideation skill (Phase 6: Artifact Generation)
**Severity:** HIGH
**Status:** In Progress

---

## Issue Description

Epic documents created by the devforgeai-ideation skill (Phase 6.1-6.3) were missing required constitutional sections that another Claude session would need to successfully run `/create-story`. The generated epics lacked:

- Out of Scope section
- User Stories section (As a... I want... So that...)
- Stakeholders section
- Target Sprints breakdown with story lists
- Timeline section with visual timeline
- Progress Tracking table
- Measurement Plan details

Additionally, the epics contained:
- Undefined schemas (ai-analysis.json, observation schema)
- Vague file paths (lines TBD)
- Source-tree.md violations (proposed directories not in constitutional file)
- No explicit acceptance criteria for features

**Impact:** Another Claude session running `/create-story` would lack contextual knowledge from the ideation session, leading to ambiguous story creation, scope creep, and potential constitutional violations.

---

## 5 Whys Analysis

### Why #1: Why were the epic documents missing constitutional sections?

**Answer:** The artifact-generation.md reference file (Phase 6.1-6.3) contains a simplified inline epic template (lines 36-139, ~100 lines) that does NOT match the constitutional epic-template.md (265 lines).

**Evidence:**
- artifact-generation.md lines 36-139: Inline template with only 12 sections
- epic-template.md lines 1-265: Constitutional template with 20+ sections including Out of Scope, User Stories, Stakeholders, Target Sprints, Timeline, Progress Tracking

### Why #2: Why does artifact-generation.md contain a simplified template?

**Answer:** artifact-generation.md was created as a **standalone workflow document** with an embedded template, rather than referencing the canonical epic-template.md. There's no `Read()` instruction to load the constitutional template.

**Evidence:**
```markdown
# artifact-generation.md line 18
Create epic documents in `devforgeai/specs/Epics/EPIC-NNN-[name].epic.md` following the DevForgeAI epic template.

# But lines 36-139 contain its OWN inline template, not:
Read(file_path=".claude/skills/devforgeai-orchestration/assets/templates/epic-template.md")
```

### Why #3: Why doesn't artifact-generation.md reference the constitutional template?

**Answer:** The ideation skill was designed for **self-contained execution** without cross-skill dependencies. Each skill operates in isolation without shared asset access patterns established.

**Evidence:**
- No cross-skill Read() pattern in artifact-generation.md
- Directory Structure Requirements (lines 579-605) focuses on output locations, not template compliance
- Reference file list in SKILL.md (lines 325-358) doesn't include epic-template.md

### Why #4: Why doesn't Phase 6.4 validation catch the missing sections?

**Answer:** The self-validation workflow validates **YAML frontmatter fields** (id, title, status, complexity-score) but NOT **section completeness**. There's no validation rule: "epic contains all sections from epic-template.md".

**Evidence:**
```markdown
# self-validation-workflow.md lines 97-104 (frontmatter validation only)
validate_frontmatter(epic_file):
    - [ ] id field matches filename
    - [ ] title field present and non-empty
    - [ ] business-value field quantified
    - [ ] status field = "Planning"
    - [ ] priority field = High|Medium|Low
    - [ ] created date in YYYY-MM-DD format
    - [ ] complexity-score present
    - [ ] architecture-tier present

# No section validation like:
# - [ ] Out of Scope section present
# - [ ] User Stories section present
# - [ ] Stakeholders section present
```

### Why #5 (ROOT CAUSE): Why is there no template compliance enforcement?

**ROOT CAUSE:** The DevForgeAI framework has **no single-source-of-truth enforcement** for epic templates. The constitutional epic-template.md exists but:
1. No reference links it from devforgeai-ideation skill
2. No validation checks epic content against it
3. artifact-generation.md has a divergent inline template (~40% of constitutional)
4. Cross-skill asset references are not established as a pattern

This violates the DevForgeAI principle of "constitutional context files are immutable" - the epic template should be treated as constitutional but isn't enforced.

---

## Evidence Collected

### File 1: artifact-generation.md (CRITICAL)

**Path:** `.claude/skills/devforgeai-ideation/references/artifact-generation.md`
**Lines:** 36-139

**Finding:** Contains simplified inline template missing 8+ constitutional sections

**Excerpt (inline template - truncated):**
```markdown
---
id: EPIC-{NNN}
title: {Epic Name}
business-value: {Quantified business outcome}
status: Planning
priority: {High|Medium|Low}
complexity-score: {score from Phase 3}
architecture-tier: {Tier 1|2|3|4}
created: {YYYY-MM-DD}
estimated-points: {total story points}
target-sprints: {estimated sprint count}
---

# {Epic Name}

## Business Goal
## Features
## Requirements Summary
## Architecture Considerations
## Risks & Mitigations
## Dependencies
## Next Steps
```

**Missing from inline template:**
- Out of Scope section
- User Stories section
- Stakeholders section
- Target Sprints breakdown (with sprint-level story lists)
- Communication Plan section
- Timeline section (visual timeline)
- Key Milestones section
- Progress Tracking table
- Retrospective section

**Significance:** This is the direct cause - the ideation skill uses this incomplete template.

---

### File 2: epic-template.md (CRITICAL)

**Path:** `.claude/skills/devforgeai-orchestration/assets/templates/epic-template.md`
**Lines:** 1-265

**Finding:** This is the CONSTITUTIONAL epic template with ALL required sections

**Excerpt (constitutional sections present):**
```markdown
## Scope
### In Scope
### Out of Scope                     # ✓ Present
- ❌ [e.g., Cryptocurrency payment support - deferred]

## Target Sprints                    # ✓ Present with story lists
### Sprint 1 (SPRINT-XXX): [Sprint Name/Theme]
**Goal:** [What will be achieved]
**Features:**
- Feature 1: [Story list]

## User Stories                      # ✓ Present
1. **As a** [user role], **I want** [capability], **so that** [benefit]

## Stakeholders                      # ✓ Present
### Primary Stakeholders
### Additional Stakeholders

## Timeline                          # ✓ Present
```
Epic Timeline:
════════════════════════════════════════════════════
Week 1-2:  Sprint 1 - Core checkout flow
```

## Progress Tracking                 # ✓ Present
### Sprint Summary
| Sprint | Status | Points | Stories | Completed |
```

**Significance:** This is what the generated epic SHOULD contain.

---

### File 3: self-validation-workflow.md (HIGH)

**Path:** `.claude/skills/devforgeai-ideation/references/self-validation-workflow.md`
**Lines:** 90-131

**Finding:** Validates frontmatter only, no section compliance validation

**Excerpt:**
```markdown
validate_frontmatter(epic_file):
    - [ ] id field matches filename (e.g., EPIC-001 in filename → id: EPIC-001)
    - [ ] title field present and non-empty
    - [ ] business-value field quantified (measurable outcome)
    - [ ] status field = "Planning" (default for new epics)
    - [ ] priority field = High|Medium|Low
    - [ ] created date in YYYY-MM-DD format
    - [ ] complexity-score present (from Phase 3)
    - [ ] architecture-tier present (Tier 1-4)
```

**Missing validation:**
```markdown
# Should have:
validate_section_compliance(epic_file):
    - [ ] Out of Scope section present
    - [ ] User Stories section present (minimum 3 stories)
    - [ ] Stakeholders section present
    - [ ] Target Sprints section with story lists
    - [ ] Timeline section with visual timeline
    - [ ] Progress Tracking table present
```

**Significance:** This is why missing sections weren't caught.

---

### File 4: SKILL.md (HIGH)

**Path:** `.claude/skills/devforgeai-ideation/SKILL.md`
**Lines:** 255-266

**Finding:** Phase 6 references artifact-generation.md but not constitutional template

**Excerpt:**
```markdown
### Phase 6: Requirements Documentation & Handoff
**Workflow:** 3 sub-phases | **Output:** Epic documents, requirements spec (optional), completion summary

**6.1-6.3 Artifact Generation:** Generate epics, optional requirements spec, verify creation, transition to architecture
**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/artifact-generation.md")`

**6.4 Self-Validation:** Validate artifacts, auto-correct issues, HALT on critical failures
**Load:** `Read(file_path=".claude/skills/devforgeai-ideation/references/self-validation-workflow.md")`
```

**Missing:**
```markdown
# Should include before artifact generation:
**Load Template:** `Read(file_path=".claude/skills/devforgeai-orchestration/assets/templates/epic-template.md")`
```

**Significance:** Shows skill architecture doesn't include template loading.

---

## Recommendations

### CRITICAL: REC-1 - Add Template Loading to Artifact Generation
**Implemented in:** STORY-324

**Problem Addressed:** artifact-generation.md uses divergent inline template instead of constitutional template

**Proposed Solution:** Add explicit template loading instruction at the start of artifact-generation.md

**Implementation Details:**

**File:** `.claude/skills/devforgeai-ideation/references/artifact-generation.md`

**Section:** After line 17 "Create epic documents..."

**Add:**
```markdown
### Load Constitutional Epic Template

**CRITICAL: Before generating any epic document, load the canonical template:**

```
Read(file_path=".claude/skills/devforgeai-orchestration/assets/templates/epic-template.md")
```

**Use this template structure for ALL epic documents. Do NOT use the abbreviated template below - it is for reference only. The full template from devforgeai-orchestration/assets/templates/epic-template.md is the source of truth.**

**Required Sections (from canonical template):**
- [ ] YAML Frontmatter (id, title, status, owner, tech_lead, team, etc.)
- [ ] Business Goal with Success Metrics and Measurement Plan
- [ ] Scope (In Scope AND Out of Scope)
- [ ] Target Sprints with story lists per sprint
- [ ] User Stories (As a... I want... So that... format)
- [ ] Technical Considerations
- [ ] Dependencies (Internal and External)
- [ ] Risks & Mitigation
- [ ] Stakeholders (Primary and Additional)
- [ ] Communication Plan
- [ ] Timeline (visual timeline + Key Milestones)
- [ ] Progress Tracking (Sprint Summary table)
```

**Rationale:** Constitutional templates must be loaded explicitly to ensure all required sections are generated. This follows the DevForgeAI principle of "context files are immutable" by treating the epic template as constitutional.

**Testing:**
1. Run `/ideate` with a test brainstorm
2. Verify generated epic contains ALL sections from epic-template.md
3. Compare section-by-section against canonical template
4. Confirm another session can run `/create-story` without ambiguity

**Effort:** Low (30 minutes)
**Impact:** HIGH - Prevents all future incomplete epics

---

### CRITICAL: REC-2 - Add Section Compliance Validation
**Implemented in:** STORY-325

**Problem Addressed:** Phase 6.4 validation only checks frontmatter, not section completeness

**Proposed Solution:** Add section compliance validation to self-validation-workflow.md

**Implementation Details:**

**File:** `.claude/skills/devforgeai-ideation/references/self-validation-workflow.md`

**Section:** After Step 2 "Validate Epic Content Quality" (after line 131)

**Add:**
```markdown
### Step 2.5: Validate Section Compliance

**Check epic contains all constitutional sections:**

```
REQUIRED_SECTIONS = [
    "## Business Goal",
    "## Scope",
    "### Out of Scope",
    "## Target Sprints",
    "## User Stories",
    "## Technical Considerations",
    "## Dependencies",
    "## Risks & Mitigation",
    "## Stakeholders",
    "## Timeline",
    "## Progress Tracking"
]

for epic_file in epic_files:
    epic_content = Read(file_path=epic_file)

    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in epic_content:
            missing_sections.append(section)

    if len(missing_sections) > 0:
        # CRITICAL failure - epic incomplete
        CRITICAL: Epic {epic_file} missing required sections:
        {missing_sections}

        Self-healing attempt:
        1. Re-read canonical template
        2. Add missing sections with placeholder content
        3. Flag for user completion

        If missing > 3 sections:
            HALT: Epic structure too incomplete for self-healing
            Recommend: Regenerate epic using full template
```

**Validation checklist update (lines 217-229):**
```markdown
- [ ] All planned epics created and validated
- [ ] All epics contain required sections (11 minimum)      # NEW
- [ ] Out of Scope section prevents scope creep             # NEW
- [ ] User Stories in proper format (3+ stories)            # NEW
- [ ] Target Sprints have story lists                       # NEW
- [ ] Requirements specification complete
- [ ] Complexity assessment finalized
- [ ] No critical ambiguities remain
```

**Rationale:** Section compliance is as important as frontmatter validation. Missing sections cause downstream failures in `/create-story`.

**Testing:**
1. Create epic with missing sections
2. Run validation
3. Verify CRITICAL failure raised
4. Verify self-healing attempts to add missing sections
5. Verify HALT if >3 sections missing

**Effort:** Medium (1 hour)
**Impact:** HIGH - Catches incomplete epics before handoff

---

### HIGH: REC-3 - Remove Divergent Inline Template
**Implemented in:** STORY-326

**Problem Addressed:** artifact-generation.md lines 36-139 contain divergent template that conflicts with constitutional template

**Proposed Solution:** Replace inline template with reference pointer and compliance checklist

**Implementation Details:**

**File:** `.claude/skills/devforgeai-ideation/references/artifact-generation.md`

**Section:** Lines 34-139 (entire inline template section)

**Replace with:**
```markdown
### Epic Template Reference

**DO NOT use an inline template. Always load the constitutional template:**

```
Read(file_path=".claude/skills/devforgeai-orchestration/assets/templates/epic-template.md")
```

**Section Checklist (verify after generation):**

| Section | Required | Purpose |
|---------|----------|---------|
| YAML Frontmatter | ✓ | ID, title, status, dates, ownership |
| Business Goal | ✓ | Why this epic matters, success metrics |
| Scope - In Scope | ✓ | What's included |
| Scope - Out of Scope | ✓ | Explicit exclusions to prevent scope creep |
| Target Sprints | ✓ | Sprint-level breakdown with story lists |
| User Stories | ✓ | 3+ stories in As a/I want/So that format |
| Technical Considerations | ✓ | Architecture, security, performance |
| Dependencies | ✓ | Internal and external blockers |
| Risks & Mitigation | ✓ | Risk register with mitigations |
| Stakeholders | ✓ | Primary and additional stakeholders |
| Timeline | ✓ | Visual timeline and key milestones |
| Progress Tracking | ✓ | Sprint summary table |

**Cross-Session Context Requirements:**

Each epic MUST contain sufficient detail for another Claude session to run `/create-story` without:
- Asking for missing context (schemas, file paths)
- Making assumptions about scope
- Violating source-tree.md (new directories require ADR)
- Creating ambiguous acceptance criteria
```

**Rationale:** Removing the divergent inline template eliminates the possibility of using it. The checklist ensures compliance without duplicating template content.

**Testing:**
1. Verify artifact-generation.md no longer contains inline template
2. Run `/ideate` and confirm canonical template is loaded
3. Verify generated epic matches canonical structure

**Effort:** Medium (1 hour)
**Impact:** HIGH - Eliminates source of template divergence

---

### HIGH: REC-4 - Add Source-Tree Validation for New Directories
**Implemented in:** STORY-327

**Problem Addressed:** EPIC-052 proposed `.claude/memory/sessions/` and `.claude/memory/learning/` directories that don't exist in source-tree.md

**Proposed Solution:** Add source-tree.md validation to artifact-generation.md and self-validation-workflow.md

**Implementation Details:**

**File:** `.claude/skills/devforgeai-ideation/references/artifact-generation.md`

**Section:** Add after Step 6.3 "Transition to Architecture Skill"

**Add:**
```markdown
### Step 6.3.5: Validate Source Tree Compliance

**Before completing artifact generation, check for constitutional violations:**

```
# Read source-tree.md for valid directories
source_tree = Read(file_path="devforgeai/specs/context/source-tree.md")

# Extract all file/directory paths from generated epics
for epic_file in epic_files:
    epic_content = Read(file_path=epic_file)

    # Find all proposed paths (lines containing .claude/, devforgeai/, src/)
    proposed_paths = Grep(pattern="\\.(claude|devforgeai)/[a-zA-Z/]+", path=epic_file, output_mode="content")

    for path in proposed_paths:
        if path not in source_tree:
            # Constitutional violation detected
            WARNING: Proposed path not in source-tree.md: {path}

            # Add ADR requirement to epic
            Add to epic Prerequisites section:
            """
            ### ADR Required: Source Tree Update

            This epic proposes directories not in source-tree.md:
            - {path}

            **Action Required:** Create ADR before implementation to update source-tree.md
            """
```

**Rationale:** source-tree.md is constitutional. Proposing new directories without ADR violates framework constraints.

**Testing:**
1. Create epic with new directory proposal
2. Run validation
3. Verify WARNING raised
4. Verify ADR requirement added to epic

**Effort:** Medium (1 hour)
**Impact:** MEDIUM - Prevents constitutional violations

---

### MEDIUM: REC-5 - Add Explicit Schema Documentation Requirement
**Implemented in:** STORY-328

**Problem Addressed:** Epics contained undefined schemas (ai-analysis.json, observation schema) without explicit specification

**Proposed Solution:** Add schema documentation requirement to epic template validation

**Implementation Details:**

**File:** `.claude/skills/devforgeai-ideation/references/self-validation-workflow.md`

**Section:** Add to Step 2.5 Section Compliance

**Add:**
```markdown
### Schema Completeness Check

For each epic, verify all referenced data structures are explicitly documented:

```
# Find schema references (JSON, YAML, TypeScript interfaces)
schema_refs = Grep(pattern="schema|interface|structure|format", path=epic_file, output_mode="content")

for schema_ref in schema_refs:
    # Check if schema is defined in epic
    if schema_ref mentions data structure without code block:
        WARNING: Schema referenced but not defined: {schema_ref}

        Recommend: Add explicit schema definition in Feature section
        Example:
        """
        **Schema (add to Feature section):**
        ```json
        {
          "field1": "type",
          "field2": "type"
        }
        ```
        """
```

**Cross-session context rule:** Another Claude session must be able to implement features without asking "What does this schema look like?"

**Rationale:** Undefined schemas cause ambiguity for downstream story creation and implementation.

**Testing:**
1. Create epic with schema reference but no definition
2. Run validation
3. Verify WARNING raised with recommendation

**Effort:** Low (30 minutes)
**Impact:** MEDIUM - Reduces ambiguity

---

## Implementation Checklist

### Immediate Actions (Implement Now)

- [ ] **REC-1:** Add template loading instruction to artifact-generation.md: See STORY-324
- [ ] **REC-2:** Add section compliance validation to self-validation-workflow.md: See STORY-325
- [ ] **REC-3:** Remove divergent inline template from artifact-generation.md: See STORY-326

### Sprint Backlog (Implement This Sprint)

- [ ] **REC-4:** Add source-tree validation to artifact-generation.md: See STORY-327
- [ ] **REC-5:** Add schema completeness check to validation workflow: See STORY-328

### Verification

- [ ] Run `/ideate` with test brainstorm
- [ ] Verify generated epic contains ALL constitutional sections
- [ ] Verify validation catches missing sections
- [ ] Verify another session can run `/create-story` successfully

---

## Prevention Strategy

### Short-Term

1. **Template loading mandatory:** All artifact generation must load canonical templates via explicit `Read()` instruction
2. **Section compliance validation:** Validation must check for all required sections, not just frontmatter
3. **Remove inline templates:** Reference files should NOT contain divergent templates

### Long-Term

1. **Establish cross-skill asset pattern:** Create convention for referencing canonical templates across skills
2. **Constitutional template registry:** Document which templates are constitutional and must be loaded
3. **Validation completeness audit:** Review all skills for validation gaps (frontmatter-only vs section-complete)

### Monitoring

- **Audit trigger:** After every `/ideate` run, verify epic section completeness
- **Cross-session test:** Periodically test `/create-story` in fresh session with only epic context
- **Template drift detection:** Compare inline references against canonical templates

---

## Related RCAs

- **RCA-020:** Story Creation Missing Evidence Verification - Similar issue with story template compliance
- **RCA-028:** Manual Story Creation Ground Truth Validation Failure - Related to missing validation

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | RCA created | DevForgeAI RCA Skill |
