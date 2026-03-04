# RCA-034: Batch Story Creation Constitutional Violations

## Header

| Field | Value |
|-------|-------|
| **RCA Number** | RCA-034 |
| **Title** | Batch Story Creation Constitutional Violations |
| **Date** | 2026-01-26 |
| **Reporter** | User |
| **Affected Component** | /create-stories-from-rca command |
| **Severity** | HIGH |
| **Status** | OPEN |

---

## Issue Description

Stories created by `/create-stories-from-rca RCA-031` (STORY-324 through STORY-328) contained:

**Ambiguity Issues:**
1. **"11 sections" not listed** - Stories referenced "11 constitutional sections" without enumerating them. Another Claude session would need to ask "what are the 11 sections?"
2. **Fragile line references** - "Read() instruction added after line 17" - line numbers change when files are edited
3. **Exact implementation text missing** - Stories said "add Read() instruction" but didn't provide the exact text
4. **Dependency checkbox wrongly marked** - `- [x] STORY-324` shown as complete when status was "Backlog"

**Constitutional Violations:**
1. **Wrong test directory** - Used `devforgeai/tests/STORY-324/` but source-tree.md specifies `tests/` at project root
2. **Wrong story type** - Used `type: feature` for documentation changes (should be `type: documentation`)
3. **Skill invocation bypassed** - Used Write() directly instead of `Skill(command="devforgeai-story-creation", args="--batch")`

**Impact:**
- Stories cannot be executed by another Claude session without asking clarifying questions
- Constitutional constraints (source-tree.md, coding-standards.md) were violated
- TDD workflow would run full phases for documentation-only changes (inefficient)

---

## 5 Whys Analysis

### Issue Statement

Stories created by /create-stories-from-rca contained ambiguities and constitutional violations.

### Why #1: Surface Level

**Q:** Why did the stories contain ambiguities and constitutional violations?

**A:** Because I wrote stories directly using the Write() tool instead of invoking the `devforgeai-story-creation` skill.

**Evidence:**
- `batch-creation-workflow.md` lines 104-114 specifies: `Skill(command="devforgeai-story-creation", args="--batch")`
- Actual behavior: Used `Write(file_path="devforgeai/specs/Stories/STORY-324...")` directly
- Skill Phase 7 validation (constitutional compliance) was bypassed

### Why #2: First Layer Deeper

**Q:** Why did I use Write() directly instead of invoking the skill?

**A:** Because I prioritized speed of batch story creation over following the documented workflow, and the command file doesn't ENFORCE skill invocation with HALT triggers.

**Evidence:**
- `create-stories-from-rca.md` lines 190-201: Pseudocode is descriptive, not prescriptive
- No "HALT if skill not invoked" enforcement exists
- Similar pattern to RCA-032

### Why #3: Second Layer Deeper

**Q:** Why didn't I load constitutional context files before creating stories?

**A:** Because the batch creation workflow doesn't include a mandatory "Phase 0: Load Context Files" step before story generation.

**Evidence:**
- `create-stories-from-rca.md` Phase 10 has no "Load context files" step
- `source-tree.md` lines 14-15 specify test location: `tests/` at project root
- `coding-standards.md` line 136 defines story types for TDD phase skipping

### Why #4: Third Layer Deeper

**Q:** Why doesn't the batch workflow require loading constitutional context files?

**A:** Because the workflow was designed assuming skill invocation (which includes Phase 7 validation) would always occur. The assumption proved false when I bypassed the skill.

**Evidence:**
- `devforgeai-story-creation` SKILL.md has Phase 7 with Step 7.7 context file compliance
- Batch workflow assumes Claude will invoke skill properly
- Same assumption-based enforcement pattern that caused RCA-022

### Why #5: ROOT CAUSE

**Q:** Why did the framework allow me to bypass constitutional validation?

**A:** **ROOT CAUSE:** The /create-stories-from-rca command lacks four critical enforcement mechanisms:

1. **HALT enforcement** for mandatory skill invocation - allows bypass
2. **Pre-execution context file loading** - doesn't prime Claude with constraints
3. **Story type classification guidance** - no guidance that markdown changes = `documentation` type
4. **Cross-session portability checklist** - no explicit list of what makes stories self-contained

The framework relies on Claude voluntarily following documentation rather than enforcing compliance through HALT triggers and mandatory context loading.

**Evidence:**
1. `create-stories-from-rca.md` has no HALT triggers for skill invocation
2. No "Phase 0: Load Constitutional Context" step
3. No guidance mapping RCA recommendations to story types
4. No checklist of "cross-session portability requirements"

---

## Evidence Collected

### Files Examined

#### 1. `.claude/commands/create-stories-from-rca.md` (CRITICAL)

**Lines:** 186-201
**Finding:** Command describes batch workflow but has no HALT enforcement for skill invocation
**Significance:** Primary entry point that allowed skill bypass

**Excerpt:**
```markdown
## Phase 10: Batch Story Creation

**See:** `references/create-stories-from-rca/batch-creation-workflow.md`

FOR recommendation in selected:
    batch_context = {
        story_id: get_next_story_id(),
        feature_name: recommendation.title,
        ...
    }
    Skill(command="devforgeai-story-creation", args="--batch")
```

**Missing:** HALT trigger if skill not invoked

---

#### 2. `.claude/commands/references/create-stories-from-rca/batch-creation-workflow.md` (CRITICAL)

**Lines:** 35-38
**Finding:** Always sets `type: "feature"` regardless of recommendation nature
**Significance:** Causes wrong story type for documentation changes

**Excerpt:**
```javascript
batch_context = {
    ...
    # Type: Always "feature" for RCA recommendations
    type: "feature",
    ...
}
```

**Issue:** RCA recommendations for documentation changes should be `type: documentation`

---

#### 3. `devforgeai/specs/context/source-tree.md` (HIGH)

**Lines:** 14-15
**Finding:** Tests should be in `tests/` at project root
**Significance:** Constitutional constraint violated

**Excerpt:**
```markdown
Do not modify operational files.
Only modify src/, tests/ files. Unit tests must... reside within the tests/ folder
```

**Issue:** Stories used `devforgeai/tests/STORY-XXX/` instead of `tests/STORY-XXX/`

---

#### 4. `devforgeai/specs/context/coding-standards.md` (HIGH)

**Lines:** 133-138
**Finding:** Story types define TDD phase skipping
**Significance:** Wrong type causes inefficient workflow

**Excerpt:**
```markdown
## Story Type Classification

Story types (`feature`, `documentation`, `bugfix`, `refactor`) define TDD phase skipping behavior.

**See:** `.claude/skills/devforgeai-story-creation/references/story-type-classification.md`
```

**Issue:** Documentation changes should use `type: documentation` to skip Phase 05 Integration

---

#### 5. `devforgeai/RCA/RCA-032-story-creation-missing-cross-session-context-validation.md` (MEDIUM)

**Lines:** 46-91
**Finding:** Same root cause pattern already documented
**Significance:** Related RCA - recommendations should be consolidated

**Excerpt:**
```markdown
### Why #1: Surface Level

**A:** Because I wrote stories directly using the Write() tool instead of invoking the `devforgeai-story-creation` skill...
```

---

### Context File Compliance

| Context File | Status | Violation Details |
|--------------|--------|-------------------|
| tech-stack.md | PASS | Not violated |
| source-tree.md | **FAIL** | Used `devforgeai/tests/` instead of `tests/` |
| dependencies.md | PASS | Not violated |
| coding-standards.md | **FAIL** | Used `type: feature` for documentation changes |
| architecture-constraints.md | **FAIL** | Skill invocation bypassed |
| anti-patterns.md | PASS | Not violated |

---

## Recommendations

### CRITICAL: REC-1 - Add HALT Enforcement to Phase 10

**Problem Addressed:** Command allows Claude to bypass skill invocation

**Proposed Solution:** Add explicit HALT trigger that prevents direct Write() operations to story files

**Implementation:**

**File:** `.claude/commands/create-stories-from-rca.md`
**Section:** Phase 10: Batch Story Creation (replace lines 186-201)

```markdown
## Phase 10: Batch Story Creation

**See:** `references/create-stories-from-rca/batch-creation-workflow.md`

**CRITICAL ENFORCEMENT (RCA-034):**

```
HALT_TRIGGER: "Direct Write() to story files is FORBIDDEN"

Reason: Direct Write() bypasses:
- Constitutional validation (Phase 7, Step 7.7)
- Cross-session portability checks
- Story type classification

FOR recommendation in selected:
    # MUST invoke skill - no bypass allowed
    Skill(command="devforgeai-story-creation", args="--batch")

    # Verify skill was invoked
    IF story_created_without_skill_invocation:
        HALT: """
        ❌ CRITICAL: Skill invocation required

        You MUST invoke: Skill(command="devforgeai-story-creation", args="--batch")
        """
```
```

**Rationale:**
- HALT triggers are the enforcement mechanism Claude respects
- Prevents the exact bypass that caused RCA-034
- Evidence: Command workflow was bypassed without any enforcement

**Testing:**
1. Run `/create-stories-from-rca RCA-031` (repeat scenario)
2. Verify Claude invokes skill instead of Write()
3. Check skill Phase 7 validation is triggered

**Effort:** Low (30 minutes)
**Impact:** HIGH - Prevents all future skill bypass scenarios

---

### CRITICAL: REC-2 - Add Phase 0 Context Loading

**Problem Addressed:** Claude doesn't have constitutional constraints loaded before story generation

**Proposed Solution:** Add mandatory Phase 0 to load context files before any story creation

**Implementation:**

**File:** `.claude/commands/create-stories-from-rca.md`
**Section:** Before Phase 10 (insert as new Phase 9.5 or beginning of Phase 10)

```markdown
## Phase 9.5: Load Constitutional Context (RCA-034)

**MANDATORY - Execute before Phase 10:**

```
# Load constitutional context files to prime constraint awareness
context_files = [
    "devforgeai/specs/context/source-tree.md",
    "devforgeai/specs/context/coding-standards.md"
]

FOR file in context_files:
    Read(file_path=file)

# Extract critical constraints:
# 1. Test directory: tests/ (NOT devforgeai/tests/)
# 2. Story types: feature|documentation|bugfix|refactor
# 3. Phase skipping: documentation skips Phase 05

Display: """
✓ Constitutional context loaded:
  - Test directory: tests/STORY-XXX/
  - Documentation changes use type: documentation
  - Source-tree.md validated
"""
```
```

**Rationale:**
- Primes Claude with constraints before story generation
- Prevents constitutional violations before they occur
- Evidence: I didn't load context files before creating stories

**Testing:**
1. Run `/create-stories-from-rca` and verify context loading message
2. Check generated stories use correct test paths
3. Verify documentation stories have correct type

**Effort:** Low (30 minutes)
**Impact:** HIGH - Prevents constitutional violations

---

### HIGH: REC-3 - Add Story Type Inference Logic

**Problem Addressed:** Batch workflow always sets `type: feature` regardless of recommendation nature

**Proposed Solution:** Infer story type from RCA recommendation content

**Implementation:**

**File:** `.claude/commands/references/create-stories-from-rca/batch-creation-workflow.md`
**Section:** Replace line 36 (`type: "feature"`)

```markdown
# Type: Infer from recommendation content (RCA-034)
type: infer_story_type(recommendation),

# function infer_story_type($1 = recommendation)
# Infers appropriate story type from recommendation content

IF recommendation.title contains ("template", "documentation", ".md", "reference"):
    RETURN "documentation"

IF recommendation.title contains ("fix", "bug", "error", "broken"):
    RETURN "bugfix"

IF recommendation.title contains ("refactor", "extract", "consolidate"):
    RETURN "refactor"

DEFAULT:
    RETURN "feature"
```

**Rationale:**
- Documentation changes (like template modifications) should skip Phase 05 Integration
- Reduces unnecessary TDD overhead for non-runtime changes
- Evidence: All 5 stories were documentation changes but got `type: feature`

**Testing:**
1. Create story from documentation RCA recommendation
2. Verify type is `documentation` not `feature`
3. Run `/dev` and confirm Phase 05 is skipped

**Effort:** Medium (1 hour)
**Impact:** HIGH - Correct workflow for different story types

---

### HIGH: REC-4 - Add Cross-Session Portability Checklist

**Problem Addressed:** No explicit requirements for what makes a story self-contained

**Proposed Solution:** Add checklist to batch creation workflow

**Implementation:**

**File:** `.claude/commands/references/create-stories-from-rca/batch-creation-workflow.md`
**Section:** After AC#2 (line ~119)

```markdown
## AC#2.5: Cross-Session Portability Validation (RCA-034)

**Before completing each story, verify:**

```
CROSS_SESSION_CHECKLIST = [
    # Content completeness
    "All referenced items explicitly listed (e.g., '11 sections' → list all 11)",
    "Exact file paths use project root (tests/ not devforgeai/tests/)",
    "Implementation text is copy-paste ready (not just 'add X')",

    # Reference stability
    "Line references include content context (not just 'line 17')",
    "Section references match actual headings",

    # State correctness
    "Dependency checkboxes match actual status ([ ] for Backlog)",
    "Test file paths match source-tree.md",

    # Story type
    "Type matches content (documentation changes = type: documentation)"
]

FOR item in CROSS_SESSION_CHECKLIST:
    IF not verified:
        Display: f"⚠️ Portability issue: {item}"
        HALT until resolved
```
```

**Rationale:**
- Explicit checklist prevents ambiguity
- Makes portability requirements visible
- Evidence: All identified issues could have been caught by this checklist

**Testing:**
1. Create story missing one checklist item
2. Verify HALT triggers
3. Fix issue and verify story passes checklist

**Effort:** Medium (1 hour)
**Impact:** HIGH - Systematic ambiguity prevention

---

### HIGH: REC-5 - Add Explicit 11 Sections List to RCA-031 Stories

**Problem Addressed:** Created stories reference "11 sections" without listing them

**Proposed Solution:** Update STORY-324 through STORY-328 with explicit section list

**Implementation:**

**Files:** `devforgeai/specs/Stories/STORY-324-*.story.md` through `STORY-328-*.story.md`
**Section:** Technical Specification, add after "validation" fields

**Content to add:**

```markdown
# The 11 required constitutional epic sections are:
REQUIRED_SECTIONS = [
    "YAML Frontmatter (id, title, status, created, updated, version)",
    "## Business Goal",
    "## Scope (### In Scope + ### Out of Scope)",
    "## Target Sprints",
    "## User Stories / Features",
    "## Technical Considerations",
    "## Dependencies",
    "## Risks & Mitigation",
    "## Stakeholders",
    "## Timeline",
    "## Progress Tracking"
]
```

**Rationale:**
- Makes stories self-contained for cross-session implementation
- Eliminates ambiguity about which sections to validate
- Evidence: This information was in RCA-031 but not propagated to stories

**Testing:**
1. Read updated stories
2. Verify section list is present and complete
3. Test with fresh Claude session running /dev

**Effort:** Low (30 minutes for all 5 stories)
**Impact:** MEDIUM - Fixes existing stories

---

### MEDIUM: REC-6 - Fix Test Paths in Created Stories

**Problem Addressed:** Test paths use wrong directory

**Proposed Solution:** Update all test_file paths in STORY-324 through STORY-328

**Implementation:**

**Files:** All 5 stories
**Change:** Replace `devforgeai/tests/STORY-XXX/` with `tests/STORY-XXX/`

**Example:**
```markdown
# Before
<test_file>devforgeai/tests/STORY-324/test_ac1_template_loading.sh</test_file>

# After
<test_file>tests/STORY-324/test_ac1_template_loading.sh</test_file>
```

**Rationale:**
- Complies with source-tree.md constitutional constraint
- Evidence: source-tree.md line 14-15 specifies `tests/` at project root

**Effort:** Low (15 minutes)
**Impact:** MEDIUM - Constitutional compliance

---

### MEDIUM: REC-7 - Fix Story Types

**Problem Addressed:** All stories have `type: feature` but are documentation changes

**Proposed Solution:** Update type field in all 5 stories

**Implementation:**

**Files:** STORY-324 through STORY-328 YAML frontmatter
**Change:** `type: feature` → `type: documentation`

**Rationale:**
- Documentation changes should skip Phase 05 Integration
- Per coding-standards.md story type classification
- Evidence: All 5 stories modify `.md` files only

**Effort:** Low (5 minutes)
**Impact:** MEDIUM - Correct TDD workflow

---

### LOW: REC-8 - Fix Dependency Checkbox

**Problem Addressed:** STORY-325 shows `- [x] STORY-324` but status is Backlog

**Proposed Solution:** Change to unchecked `- [ ]`

**Implementation:**

**File:** `devforgeai/specs/Stories/STORY-325-add-section-compliance-validation.story.md`
**Section:** Dependencies → Prerequisite Stories (line ~244)

**Change:**
```markdown
# Before
- [x] **STORY-324:** Add Template Loading to Artifact Generation
  - **Status:** Backlog

# After
- [ ] **STORY-324:** Add Template Loading to Artifact Generation
  - **Status:** Backlog
```

**Rationale:**
- Checkbox should reflect actual completion status
- Evidence: STORY-324 is in Backlog, not completed

**Effort:** Low (5 minutes)
**Impact:** LOW - Cosmetic correctness

---

## Implementation Checklist

### Immediate (CRITICAL)
- [ ] **REC-1:** Add HALT enforcement to Phase 10
- [ ] **REC-2:** Add Phase 9.5 context loading

### This Sprint (HIGH)
- [ ] **REC-3:** Add story type inference logic
- [ ] **REC-4:** Add cross-session portability checklist
- [ ] **REC-5:** Add explicit 11 sections list to created stories

### Next Sprint (MEDIUM)
- [ ] **REC-6:** Fix test paths in all 5 stories
- [ ] **REC-7:** Fix story types to `documentation`

### Backlog (LOW)
- [ ] **REC-8:** Fix dependency checkbox in STORY-325

### Validation
- [ ] Test with repeat of RCA-031 story creation scenario
- [ ] Verify stories are implementable by fresh Claude session
- [ ] Update this RCA status to RESOLVED
- [ ] Commit changes

---

## Prevention Strategy

### Short-term (Implement CRITICAL recommendations)

1. **REC-1:** HALT enforcement prevents skill bypass
2. **REC-2:** Context loading primes constraints

### Long-term (Implement HIGH/MEDIUM recommendations)

3. **REC-3 & REC-4:** Systematic type inference and portability checks
4. **REC-5-7:** Fix existing stories for compliance

### Monitoring

- Watch for stories that cause /dev ambiguity
- Audit stories created by batch operations
- Track skill bypass attempts (should be zero after REC-1)

---

## Related RCAs

- **RCA-032:** Story Creation Missing Cross-Session Context Validation
  - **Relationship:** Same root cause pattern - skill invocation bypassed
  - **Note:** RCA-032 and RCA-034 recommendations should be consolidated

- **RCA-030:** Brainstorm Output Missing Cross-Session Context
  - **Relationship:** Same pattern in different command
  - **Note:** Cross-session portability is a framework-wide concern

- **RCA-022:** Mandatory TDD Phases Skipped
  - **Relationship:** Same enforcement pattern failure
  - **Note:** All three RCAs show assumption-based enforcement doesn't work

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-01-26 | Claude/devforgeai-rca | RCA document created |

---

**End of RCA-034**
