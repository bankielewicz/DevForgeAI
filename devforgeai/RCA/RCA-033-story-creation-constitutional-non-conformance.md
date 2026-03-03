# RCA-033: Story Creation Constitutional Non-Conformance

## Header

| Field | Value |
|-------|-------|
| **RCA Number** | RCA-033 |
| **Title** | Story Creation Constitutional Non-Conformance |
| **Date** | 2026-01-26 |
| **Reporter** | User |
| **Affected Component** | devforgeai-story-creation skill, /create-story command |
| **Severity** | HIGH |
| **Status** | OPEN |

---

## Issue Description

Stories created via `/create-story epic-051` contained ambiguities and constitutional non-conformance that would cause failures or confusion when another Claude session runs `/dev`:

**Specific Issues:**
1. **Wrong test file paths** - Stories used `devforgeai/tests/STORY-XXX/` but source-tree.md line 368 specifies `tests/` as the canonical test directory
2. **Dual-location architecture not addressed** - Stories didn't specify whether to modify `src/claude/agents/` (source of truth) or `.claude/agents/` (operational)
3. **"Output Section" location ambiguous** - No guidance on where to place new schema in subagent files
4. **Missing Implementation Guidance section** - Stories lacked operational context another Claude session would need
5. **Phase numbers wrong in AC checklist** - Used generic "Phase 2" instead of specific "Phase 03"

**Impact:**
- Stories required manual user intervention to fix before being implementable
- Fresh Claude session running `/dev` would encounter path errors and ambiguity
- Constitutional validation (Step 7.7) did not catch these issues

**Expected Behavior:**
- Stories should be self-contained and implementable by any Claude session
- Test paths should conform to source-tree.md canonical location
- Dual-location architecture should be explicitly addressed
- Implementation Guidance section should exist for operational nuances

---

## 5 Whys Analysis

### Issue Statement

Story documents created via `/create-story epic-051` contained ambiguities and constitutional non-conformance that would cause another Claude session to fail or be confused when running `/dev`.

### Why #1: Surface Level

**Q:** Why did the stories contain ambiguities and constitutional non-conformance?

**A:** Because story content was populated directly from the requirements-analyst subagent output without validating that the output conformed to constitutional context files (source-tree.md) or contained sufficient implementation guidance for cross-session portability.

**Evidence:**
- story-validation-workflow.md Step 7.7 (lines 642-783) validates context file compliance, but was not fully executed during batch story creation
- Stories referenced `devforgeai/tests/STORY-XXX/` but source-tree.md line 368 specifies `tests/` as the test directory

### Why #2: First Layer Deeper

**Q:** Why was Step 7.7 context file compliance validation not fully executed?

**A:** Because in batch mode, the skill's 8-phase workflow was shortcut by directly assembling content from the subagent without executing all validation phases. The skill execution model says "YOU execute the skill's phases" but execution was optimized for speed over compliance.

**Evidence:**
- SKILL.md lines 22-36: "After invocation, YOU (Claude) execute these instructions phase by phase... Do NOT stop workflow after invocation"
- RCA-032 lines 50-55 identifies the same pattern: "I wrote stories directly using the Write() tool instead of invoking the `devforgeai-story-creation` skill"

### Why #3: Second Layer Deeper

**Q:** Why was the 8-phase workflow shortcut in batch mode?

**A:** Because the batch workflow documentation doesn't explicitly enforce validation steps. Batch mode guidance (SKILL.md lines 142-177) says "Phases 2-7: Execute normally" but doesn't include HALT triggers or enforcement checkpoints to ensure compliance.

**Evidence:**
- SKILL.md lines 147-150: "Batch mode behavior: Phase 1 modified: Skip interactive questions... Phases 2-7: Execute normally"
- No HALT enforcement if Phase 7 validation is skipped

### Why #4: Third Layer Deeper

**Q:** Why doesn't the batch workflow have HALT enforcement for validation phases?

**A:** Because the DevForgeAI framework relies on documentation-driven compliance (Claude reading and following instructions) rather than runtime enforcement. The assumption is that if Phase 7 is documented, Claude will execute it.

**Evidence:**
- RCA-032 lines 79-86: "Because Claude Code is a stateless conversation system. There's no persistent runtime to enforce compliance. The framework is documentation-driven, relying on Claude reading and following instructions."
- SKILL.md execution model relies on "YOU execute these instructions"

### Why #5: ROOT CAUSE

**Q:** Why did the documentation-driven compliance model fail for this story creation?

**A:** **ROOT CAUSE:** The story validation workflow (Step 7.7) validates constitutional compliance at a high level (checking technologies, general file paths) but does NOT validate:
1. **Specific test file paths** against source-tree.md's canonical `tests/` directory
2. **Dual-location architecture** requirements from source-tree.md (src/ vs .claude/)
3. **Implementation guidance** for operational nuances another Claude session would need

The validation checklists check frontmatter, user story format, AC format, tech spec completeness - but NOT constitutional path compliance for test file references or cross-session portability.

**Evidence:**
1. story-validation-workflow.md Step 7.7 (lines 787-793) validation checks: `source-tree.md | File paths in tech spec match allowed directories` - but tech spec components don't include test file path validation
2. validation-checklists.md (lines 1-100) validates frontmatter fields and formats but NOT test path locations
3. RCA-032 lines 95-97: "Step 7.7 validates context files but not cross-session portability... story-template.md has no 'Current State' section requirement"

---

## Evidence Collected

### Files Examined

#### 1. `.claude/skills/devforgeai-story-creation/SKILL.md` (CRITICAL)

**Lines:** 22-36, 142-177
**Finding:** Execution model relies on Claude following phases; batch mode says "Phases 2-7: Execute normally" but has no HALT enforcement
**Significance:** Primary skill that should enforce constitutional compliance

**Excerpt (lines 22-36):**
```markdown
## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation
```

---

#### 2. `.claude/skills/devforgeai-story-creation/references/story-validation-workflow.md` (CRITICAL)

**Lines:** 642-793
**Finding:** Step 7.7 validates context file compliance but doesn't validate test file paths or dual-location architecture
**Significance:** Validation gap - the validation exists but doesn't cover the specific issues

**Excerpt (lines 787-793):**
```markdown
| Context File | Validation Checks |
|--------------|-------------------|
| tech-stack.md | All technologies in tech spec are LOCKED or approved |
| source-tree.md | File paths in tech spec match allowed directories |
| dependencies.md | All packages in Dependencies section are approved |
| coding-standards.md | Coverage thresholds match layer (95%/85%/80%) |
| architecture-constraints.md | No cross-layer violations in design |
```

**Gap:** "File paths in tech spec match allowed directories" does NOT include:
- Test file paths in AC verification blocks
- Test file paths in Test Strategy section
- Dual-location architecture requirements

---

#### 3. `.claude/skills/devforgeai-story-creation/references/validation-checklists.md` (HIGH)

**Lines:** 1-100
**Finding:** Validates frontmatter fields and formats but NOT constitutional path compliance for test files
**Significance:** Validation checklist is incomplete for cross-session portability

---

#### 4. `devforgeai/RCA/RCA-032-story-creation-missing-cross-session-context-validation.md` (HIGH)

**Lines:** 1-520
**Finding:** Directly related RCA identifying the same pattern for /create-stories-from-rca command
**Relationship:** Same root cause pattern - validation doesn't check cross-session portability
**Significance:** Confirms this is a systemic issue, not a one-time error

---

#### 5. `devforgeai/specs/context/source-tree.md` (HIGH)

**Lines:** 368, 496-516
**Finding:** Defines canonical test path (`tests/`) and dual-location architecture
**Significance:** Constitutional document that was violated

**Excerpt (lines 496-516):**
```markdown
### Dual-Location Architecture (STORY-048, Updated for devforgeai/ migration)

**DevForgeAI maintains TWO parallel structures:**

1. **OPERATIONAL folders** (`.claude/` and `devforgeai/`) - Used by Claude Code Terminal during development
2. **DISTRIBUTION source** (`src/`) - Clean copies for external deployment via installer
```

---

### Context File Compliance

| Context File | Status | Notes |
|--------------|--------|-------|
| tech-stack.md | EXISTS | Not violated |
| source-tree.md | EXISTS | **VIOLATED** - Test paths used `devforgeai/tests/` instead of `tests/` |
| dependencies.md | EXISTS | Not violated |
| coding-standards.md | EXISTS | Not violated |
| architecture-constraints.md | EXISTS | **VIOLATED** - Dual-location architecture not addressed in stories |
| anti-patterns.md | EXISTS | Not violated |

---

## Recommendations

### REC-1: Add Test Path Validation to Step 7.7 (CRITICAL)

**Problem Addressed:** Stories reference non-canonical test paths that violate source-tree.md

**Proposed Solution:** Add explicit test file path validation to Step 7.7 that checks all test paths against source-tree.md

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/references/story-validation-workflow.md`
**Section:** Step 7.7: Context File Compliance Validation (after line 700)

```markdown
### Test Path Validation (RCA-033)

```
# Extract test file paths from story content
test_path_patterns = [
  r'tests/STORY-\d+/',           # Correct pattern
  r'devforgeai/tests/STORY-\d+/' # INCORRECT pattern
]

# Read story content
story_content = Read(file_path=story_file_path)

# Check for incorrect test paths
incorrect_paths = []
FOR match in regex_find_all(r'devforgeai/tests/STORY-\d+/', story_content):
  incorrect_paths.append(match)

IF len(incorrect_paths) > 0:
  HALT: """
  ❌ CRITICAL: Test paths violate source-tree.md

  Found: {incorrect_paths}
  Expected: tests/STORY-XXX/ (per source-tree.md line 368)

  Fix: Change all test paths from devforgeai/tests/STORY-XXX/ to tests/STORY-XXX/
  """
```
```

**Rationale:**
- source-tree.md line 368 specifies `tests/` as the canonical test directory
- Stories I created used `devforgeai/tests/` which doesn't exist in canonical structure
- HALT trigger ensures correction before story completion

**Testing:**
1. Create story with test references
2. Verify Step 7.7 catches `devforgeai/tests/` paths
3. Verify HALT message shows correction

**Effort:** Low (30 minutes)
**Impact:** HIGH - Prevents all future test path violations

---

### REC-2: Add Dual-Location Validation to Step 7.7 (CRITICAL)

**Problem Addressed:** Stories don't address dual-location architecture requirements

**Proposed Solution:** Add validation that stories modifying `.claude/` or `src/claude/` files include Implementation Guidance section

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/references/story-validation-workflow.md`
**Section:** Step 7.7 (after test path validation above)

```markdown
### Dual-Location Architecture Validation (RCA-033)

```
# Check if story modifies .claude/ or src/claude/ files
file_path_pattern = r'\.claude/|src/claude/'
tech_spec_content = extract_section(story_content, "Technical Specification")

modifies_claude_dirs = regex_search(file_path_pattern, tech_spec_content)

IF modifies_claude_dirs:
  # Check for Implementation Guidance section
  has_implementation_guidance = "## Implementation Guidance" in story_content
  has_dual_location = "dual-location" in story_content.lower() OR "source of truth" in story_content.lower()

  IF NOT has_implementation_guidance OR NOT has_dual_location:
    HALT: """
    ⚠️ Dual-Location Architecture Not Addressed

    This story modifies .claude/ or src/claude/ files but doesn't include
    Implementation Guidance section addressing dual-location architecture.

    Per source-tree.md lines 496-516:
    - src/claude/ is SOURCE OF TRUTH
    - .claude/ is OPERATIONAL (mirror from src/)

    Add Implementation Guidance section with:
    1. Which location to modify first (usually src/)
    2. Mirror instructions to other location
    3. Implementation sequence
    """
```
```

**Rationale:**
- source-tree.md lines 496-516 define dual-location architecture
- Stories I created didn't specify whether to modify src/ or .claude/
- Clear guidance prevents implementation confusion

**Testing:**
1. Create story that modifies `.claude/agents/` file
2. Verify Step 7.7 requires Implementation Guidance section
3. Verify section includes dual-location instructions

**Effort:** Medium (1 hour)
**Impact:** HIGH - Ensures stories are implementable

---

### REC-3: Add Implementation Guidance Section to Story Template (HIGH)

**Problem Addressed:** Story template lacks section for operational context

**Proposed Solution:** Add optional Implementation Guidance section to story-template.md

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
**Section:** After "## Dependencies", before "## Test Strategy"

```markdown
## Implementation Guidance (Constitutional Compliance)

{Include when story modifies files in .claude/, src/claude/, or devforgeai/ directories}

### Dual-Location Architecture (source-tree.md lines 496-516)

**Per source-tree.md, DevForgeAI maintains TWO parallel structures:**

1. **Source of truth:** `src/claude/` - Make changes here FIRST
2. **Operational:** `.claude/` - Mirror changes here for runtime

**Implementation sequence:**
```
1. Modify {path1} in src/ (source of truth)
2. Mirror to {path2} in .claude/ (operational)
```

### File Placement Location

**Where to add/modify content:**
{Specific guidance on insertion points, section headers, line numbers}

### Story Type Clarification

{Clarify if this is SPECIFICATION story, CODE story, etc. and what tests should verify}
```

**Rationale:**
- Template guides Claude to include necessary context
- Consistent with RCA-032 recommendations for cross-session portability
- Evidence: This is the pattern I used to fix STORY-318 and STORY-319

**Testing:**
1. Create story using updated template
2. Verify Implementation Guidance section appears for .claude/ modifications
3. Check dual-location instructions included

**Effort:** Low (30 minutes)
**Impact:** MEDIUM - Template guidance

---

### REC-4: Add HALT Enforcement for Batch Mode Phase 7 (HIGH)

**Problem Addressed:** Batch mode allows skipping Phase 7 validation

**Proposed Solution:** Add explicit HALT trigger in batch mode workflow requiring Phase 7 completion

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`
**Section:** Batch Mode Support (after line 176)

```markdown
**CRITICAL ENFORCEMENT (RCA-033):**

In batch mode, Phase 7 validation is MANDATORY, not optional:

```
HALT_TRIGGER: """
Phase 7 (Self-Validation) MUST execute for EVERY story in batch

IF batch_story_created_without_phase_7:
  HALT: """
  ❌ CRITICAL: Phase 7 validation required

  Batch mode skipped Phase 7 validation for {story_id}

  Phase 7 validates:
  - Constitutional compliance (Step 7.7)
  - Test path validation (RCA-033)
  - Dual-location architecture (RCA-033)
  - Cross-session portability

  You MUST execute Phase 7 for each story before proceeding to next.
  """
"""
```
```

**Rationale:**
- Batch mode documentation said "Phases 2-7: Execute normally" but no enforcement
- HALT trigger ensures Phase 7 cannot be skipped
- Evidence: I skipped Phase 7 during batch creation

**Testing:**
1. Create stories in batch mode
2. Attempt to skip Phase 7
3. Verify HALT triggers
4. Verify all stories pass Phase 7 validation

**Effort:** Low (30 minutes)
**Impact:** HIGH - Prevents validation bypass

---

### REC-5: Update Validation Checklists with Test Path Check (MEDIUM)

**Problem Addressed:** validation-checklists.md doesn't include test path validation

**Proposed Solution:** Add test path checklist item to validation-checklists.md

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/references/validation-checklists.md`
**Section:** Add new section after "YAML Frontmatter Validation"

```markdown
## Test Path Validation (RCA-033)

### Canonical Test Path Checklist

```
Validate test file paths:

- [ ] All test paths use `tests/STORY-XXX/` format
- [ ] NO paths use `devforgeai/tests/STORY-XXX/` (wrong)
- [ ] Test paths in AC verification blocks are correct
- [ ] Test paths in Test Strategy section are correct
- [ ] Test paths in AC Checklist evidence fields are correct

If any path uses devforgeai/tests/:
    CRITICAL: Wrong test path
    # Self-healing: Replace with tests/STORY-XXX/
    # Edit story file
    # Retry validation
```
```

**Rationale:**
- validation-checklists.md is the authoritative checklist for Phase 7
- Adding explicit test path check ensures it's not overlooked
- Self-healing pattern consistent with other checklist items

**Testing:**
1. Create story with devforgeai/tests/ paths
2. Run Phase 7 validation
3. Verify self-healing corrects paths

**Effort:** Low (15 minutes)
**Impact:** MEDIUM - Checklist completeness

---

### REC-6: Document Cross-Session Portability Principle in CLAUDE.md (LOW)

**Problem Addressed:** No explicit documentation of portability requirement

**Proposed Solution:** Add principle to CLAUDE.md

**Implementation:**

**File:** `CLAUDE.md`
**Section:** After "Story Progress Tracking"

```markdown
## Cross-Session Portability Principle

**All stories must be self-contained for cross-session implementation.**

When creating stories, ensure:
- **Test paths** conform to source-tree.md (`tests/STORY-XXX/`, not `devforgeai/tests/`)
- **Dual-location architecture** addressed for .claude/ modifications (src/ is source of truth)
- **Implementation Guidance section** included for operational nuances
- **File excerpts** provided for modification tasks ("Current State" section)

**Why:** Another Claude session running `/dev` won't have your contextual knowledge.
```

**Rationale:**
- Explicit documentation reinforces behavior
- Consistent with RCA-030 and RCA-032 principles
- Evidence: Required manual user intervention

**Effort:** Low (15 minutes)
**Impact:** LOW - Documentation only

---

## Implementation Checklist

- [ ] **REC-1:** Add test path validation to Step 7.7 in story-validation-workflow.md
- [ ] **REC-2:** Add dual-location validation to Step 7.7 in story-validation-workflow.md
- [ ] **REC-3:** Add Implementation Guidance section to story-template.md
- [ ] **REC-4:** Add HALT enforcement for batch mode Phase 7 to SKILL.md
- [ ] **REC-5:** Update validation-checklists.md with test path check
- [ ] **REC-6:** Document cross-session portability principle in CLAUDE.md
- [ ] Test with repeat of /create-story epic-051 scenario
- [ ] Verify stories are implementable by fresh Claude session
- [ ] Update this RCA status to RESOLVED
- [ ] Commit changes

---

## Prevention Strategy

### Short-term (Implement CRITICAL recommendations)

1. **REC-1:** Add test path validation to Step 7.7
   - Prevents immediate recurrence of test path violations
   - HALT trigger catches wrong paths

2. **REC-2:** Add dual-location validation to Step 7.7
   - Ensures Implementation Guidance section exists
   - Prevents dual-location confusion

### Long-term (Implement HIGH/MEDIUM recommendations)

3. **REC-3:** Template update
   - Guides Claude to include implementation context
   - Makes requirements visible in template

4. **REC-4:** Batch mode HALT enforcement
   - Prevents Phase 7 bypass
   - Ensures all stories validated

### Monitoring

- Watch for stories that cause /dev ambiguity
- Audit stories for test path compliance
- Check stories modifying .claude/ for Implementation Guidance section
- Track Phase 7 skip attempts in batch mode

---

## Related RCAs

- **RCA-032:** Story Creation Missing Cross-Session Context Validation
  - **Relationship:** Same pattern - stories lacking context for fresh sessions
  - **Note:** RCA-032 focused on /create-stories-from-rca; this RCA focuses on /create-story batch mode

- **RCA-030:** Brainstorm Output Missing Cross-Session Context
  - **Relationship:** Same pattern applied to different output type (brainstorms vs stories)
  - **Note:** Cross-session portability is a systemic issue across multiple output types

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-01-26 | Claude/devforgeai-rca | RCA document created |

---

**End of RCA-033**
