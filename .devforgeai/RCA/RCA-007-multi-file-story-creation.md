# RCA-007: Multi-File Story Creation Violation

**Date:** 2025-11-06
**Reporter:** User
**Severity:** HIGH
**Status:** Open - Implementation Pending
**Related:** RCA-006 (Autonomous Deferrals)

---

## Executive Summary

The `/create-story` command created 5 files instead of the single `.story.md` file specified in the DevForgeAI framework design. This violates the spec-driven development principle and creates unnecessary file artifacts.

**Files Created:**
1. `STORY-009-index-characteristic-preservation.story.md` ✅ (Correct)
2. `STORY-009-SUMMARY.md` ❌ (Violation)
3. `STORY-009-QUICK-START.md` ❌ (Violation)
4. `STORY-009-VALIDATION-CHECKLIST.md` ❌ (Violation)
5. `STORY-009-FILE-INDEX.md` ❌ (Violation)

**Impact:**
- Framework design violated (single-file requirement)
- Workflow short-circuited (Phases 3-5 skipped)
- Template bypassed (story-template.md ignored)
- Uncontrolled file creation (subagent created files directly)

---

## 5 Whys Analysis

### Problem Statement

The `devforgeai-story-creation` skill created 5 extra files instead of the single `.story.md` file specified in framework design.

### Why #1: Why did the skill create 5 files instead of 1?

**Answer:** The `requirements-analyst` subagent generated output that included multiple supporting documents (SUMMARY, VALIDATION-CHECKLIST, QUICK-START, FILE-INDEX, DELIVERY-SUMMARY) in addition to the main story file.

**Evidence:** Subagent output summary explicitly stated:
```
### **6 Comprehensive Documents** (3,600+ lines total)
1. STORY-009-index-characteristic-preservation.story.md (Primary artifact - 900+ lines)
2. STORY-009-SUMMARY.md (Executive summary - 400+ lines)
3. STORY-009-VALIDATION-CHECKLIST.md (QA reference - 600+ lines)
4. STORY-009-QUICK-START.md (Developer guide - 500+ lines)
5. STORY-009-DELIVERY-SUMMARY.md (Project completion report - 700+ lines)
6. STORY-009-FILE-INDEX.md (Navigation guide - 500+ lines)
```

---

### Why #2: Why did the requirements-analyst subagent generate 6 documents?

**Answer:** The subagent's prompt did NOT constrain output to a single story file. The prompt asked for "user story, acceptance criteria, edge cases, data validation rules, NFRs" but did not explicitly prohibit creating supplementary documentation files.

**Evidence:** Phase 2 requirements analysis invocation prompt:
```
Transform feature description into structured user story for DevForgeAI framework.

Generate:
1. **User Story** (As a/I want/So that format)
2. **Acceptance Criteria** (Given/When/Then format, minimum 3)
3. **Edge Cases** (minimum 2)
4. **Data Validation Rules**
5. **Non-Functional Requirements**

Output Format: Markdown with clear sections
```

**Missing constraints:**
- ❌ "Output ONLY the content for insertion into story-template.md"
- ❌ "Do NOT create separate files"
- ❌ "Return structured sections that will be assembled into a single file"

---

### Why #3: Why was the prompt ambiguous about file creation?

**Answer:** The `devforgeai-story-creation` skill's workflow assumed subagents would return content (markdown text), not file artifacts. Phase 5 (Story File Creation) was designed to assemble content from previous phases into the template, but the skill never validated that Phase 2 returned content instead of file paths.

**Evidence:** From Phase 5 workflow (story-file-creation.md):
```markdown
## Step 5.3: Build Markdown Sections

**Section 2: Acceptance Criteria**
```markdown
## Acceptance Criteria

[... all acceptance criteria from Phase 2 ...]
```

This assumes Phase 2 produced text content, not file references.

---

### Why #4: Why did the skill architecture assume content instead of files?

**Answer:** The `requirements-analyst` subagent is a general-purpose subagent defined in `.claude/agents/requirements-analyst.md`, not a specialized subagent designed specifically for the `devforgeai-story-creation` workflow. General-purpose subagents optimize for **completeness** (comprehensive output with supporting docs) rather than **integration** (structured content that fits into a parent workflow).

**Evidence:** The subagent is in `.claude/agents/` (global) rather than `.claude/skills/devforgeai-story-creation/subagents/` (skill-specific).

**The subagent has no knowledge of:**
- The `story-template.md` structure
- Phase 5's assembly logic
- The single-file output requirement

---

### Why #5: Why are general-purpose subagents used instead of skill-specific subagents?

**Answer (Root Cause):** The DevForgeAI framework design made an architectural trade-off: reuse general-purpose subagents (requirements-analyst, api-designer) across multiple skills to reduce duplication, rather than creating tightly-coupled skill-specific subagents that understand the parent skill's output constraints.

**Trade-off rationale:**
- ✅ **Pro:** Avoid duplicating requirements analysis logic across skills
- ✅ **Pro:** General-purpose subagents can serve multiple skills (story-creation, epic-decomposition, etc.)
- ❌ **Con:** General-purpose subagents don't know parent skill's output format requirements
- ❌ **Con:** Parent skills must parse/transform subagent output to fit their needs

**Design decision NOT documented:** The framework never explicitly documented that general-purpose subagents would return comprehensive deliverables (with supporting docs) rather than structured content snippets for assembly.

---

## Root Causes Summary

| Root Cause | Type | Severity |
|------------|------|----------|
| **RC1:** Subagent prompt ambiguity (no explicit "single output only" constraint) | Design Gap | High |
| **RC2:** No output validation in Phase 2 (skill didn't check if subagent created files vs. returned content) | Missing Guardrail | High |
| **RC3:** General-purpose subagents optimize for completeness, not integration | Architectural Mismatch | Medium |
| **RC4:** No contract between skill and subagent (expected input/output format undocumented) | Missing Specification | Medium |
| **RC5:** Phase 5 assembly logic never executed (skill stopped after subagent returned "complete" output) | Workflow Short-Circuit | High |

---

## Impact Analysis

### What Happened

1. User ran `/create-story epic-002`
2. Skill invoked `requirements-analyst` subagent
3. Subagent generated 6 complete files (not content snippets)
4. Skill received subagent output saying "Story creation complete, 6 files created"
5. Skill skipped Phases 3-5 (tech spec, UI spec, file assembly) because subagent already created "complete" artifacts
6. Skill performed Phase 6 (epic/sprint linking) and Phase 7 (validation) on the main story file
7. **Result:** 5 extra files created, main story file is complete but additional files violate single-file design

### Violations of DevForgeAI Spec

| Violation | Spec Requirement | Actual Behavior |
|-----------|------------------|-----------------|
| **V1: Multi-file output** | Single `.story.md` file per story | 5 files created (SUMMARY, QUICK-START, VALIDATION-CHECKLIST, FILE-INDEX, DELIVERY-SUMMARY) |
| **V2: Workflow short-circuit** | 8-phase workflow must complete | Phases 3-5 skipped after subagent returned "complete" output |
| **V3: Template not used** | `story-template.md` defines canonical structure | Template ignored; subagent generated custom structure |
| **V4: Uncontrolled file creation** | Only skill creates files, subagents return content | Subagent created files directly |

---

## Recommendations (Non-Aspirational, Implementable in Claude Code Terminal)

### Immediate Fixes (High Priority - Week 1: 8-10 hours)

#### Fix 1: Constrain Subagent Output with Explicit Prompt Directive (30 minutes)

**Problem:** Subagent prompt doesn't prohibit file creation or require content-only output.

**Solution:** Update `references/requirements-analysis.md` (Phase 2) with explicit output constraints:

```markdown
## Step 2.1: Invoke Requirements Analyst Subagent

Task(
  subagent_type="requirements-analyst",
  prompt="""Transform feature description into structured user story for DevForgeAI framework.

  ...

  **CRITICAL OUTPUT CONSTRAINTS:**
  - Return ONLY markdown text content (no file creation)
  - Output will be inserted into story-template.md by parent skill
  - Do NOT create separate files (SUMMARY, QUICK-START, VALIDATION-CHECKLIST, etc.)
  - Structure output as sections: User Story, Acceptance Criteria, Edge Cases, NFRs
  - Parent skill (devforgeai-story-creation) will assemble all sections into single .story.md file

  Output Format: Markdown with clear sections (NOT file paths)
  """
)
```

**Validation:** Add to Phase 2 validation:
```markdown
## Step 2.2: Validate Subagent Output

**Check for file creation attempts:**
if subagent_output contains "File created:" or "STORY-*.md" file paths:
    ERROR: Subagent violated output constraints
    Reason: Subagent created files instead of returning content
    Recovery: Re-invoke subagent with corrected prompt
```

**Effort:** Low (30 minutes to update prompt)
**Files Modified:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

---

#### Fix 2: Add Output Validation Checkpoint After Phase 2 (1-2 hours)

**Problem:** Skill doesn't validate that subagent returned content (not file references) before proceeding to Phase 3.

**Solution:** Add validation step in `references/requirements-analysis.md`:

```markdown
## Step 2.3: Validate Output Type (NEW)

**Objective:** Ensure subagent returned content, not file artifacts

**Validation:**
```python
# Pseudo-code (conceptual)
subagent_output_text = subagent_result

# Check for file creation indicators
file_creation_patterns = [
    "File created:",
    ".md created",
    "STORY-\\d+-.*\\.md",
    "Writing to file",
    "Saved to disk"
]

for pattern in file_creation_patterns:
    if re.search(pattern, subagent_output_text):
        HALT: Subagent created files instead of returning content
        Log error: "Phase 2 validation failed - subagent output format violation"
        Recovery: Re-invoke subagent with explicit "content only" directive

# Check for required sections
required_sections = ["User Story", "Acceptance Criteria", "Edge Cases", "NFRs"]
missing_sections = [s for s in required_sections if s not in subagent_output_text]

if missing_sections:
    HALT: Subagent output incomplete
    Log error: f"Missing sections: {missing_sections}"
    Recovery: Re-invoke subagent or use AskUserQuestion to fill gaps
```

**Effort:** Medium (1-2 hours to implement validation logic)
**Files Modified:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

---

#### Fix 5: Add Pre-Flight Briefing (15 minutes)

**Problem:** Skill doesn't communicate output requirements to subagent before invocation.

**Solution:** Add pre-flight briefing in subagent prompt:

```markdown
## Step 2.1: Invoke Requirements Analyst Subagent

Task(
  subagent_type="requirements-analyst",
  prompt="""
  **PRE-FLIGHT BRIEFING:**
  You are being invoked by the devforgeai-story-creation skill.
  This skill will assemble your output into a single .story.md file.

  **YOUR ROLE:**
  - Generate requirements content (user story, AC, edge cases, NFRs)
  - Return content as markdown sections
  - Do NOT create files
  - Parent skill handles file creation (Phase 5)

  **OUTPUT WILL BE USED IN:**
  - Phase 5: Story File Creation (assembly into story-template.md)
  - Your output is CONTENT, not a complete deliverable

  **PROHIBITED ACTIONS:**
  - Creating files (SUMMARY.md, QUICK-START.md, etc.)
  - Writing to disk
  - Generating file paths or references

  Now proceed with requirements analysis:
  Feature Description: {feature_description}
  ...
  """
)
```

**Effort:** Low (15 minutes to add briefing section)
**Files Modified:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

---

### Medium-Term Improvements (Medium Priority - Week 2: 5-7 hours)

#### Fix 4: Define Subagent-Skill Contracts in YAML (3-4 hours)

**Problem:** No formal contract specifying expected input/output between skills and subagents.

**Solution:** Create `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`:

```yaml
# Contract: devforgeai-story-creation <-> requirements-analyst
skill: devforgeai-story-creation
subagent: requirements-analyst
phase: Phase 2 (Requirements Analysis)

input:
  feature_description: string (min 10 words)
  story_metadata:
    story_id: string (STORY-NNN format)
    epic_id: string or null
    priority: enum [Critical, High, Medium, Low]
    points: integer [1,2,3,5,8,13]

output_format: markdown_content  # NOT file paths
output_sections:
  - user_story: "As a [role], I want [action], so that [benefit]"
  - acceptance_criteria: array (min 3, Given/When/Then format)
  - edge_cases: array (min 2)
  - data_validation_rules: array
  - nfrs: object (performance, security, reliability, scalability)

constraints:
  - no_file_creation: true   # Subagent MUST NOT create files
  - content_only: true        # Return text content, not file references
  - max_output_length: 50000  # Fits in Phase 5 assembly

validation:
  - check_sections_present: true
  - check_no_file_paths: true
  - check_ac_format: "Given/When/Then"
```

**Parent skill reads contract and validates subagent output:**
```markdown
## Step 2.2: Validate Against Contract

contract = Read(".claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml")

if contract.constraints.no_file_creation == true:
    assert no file paths in subagent_output

if contract.output_format == "markdown_content":
    assert subagent_output is plain text (not file references)
```

**Effort:** Medium-High (3-4 hours to define contracts, update validation logic)
**Files Created:** `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`
**Files Modified:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

---

#### Fix 6: File System Diff Check Before/After Subagent Invocation (2-3 hours)

**Problem:** Skill has no visibility into what subagent does (file creation vs. content return).

**Solution:** Post-hoc validation (check file system after subagent completes):

```markdown
## Step 2.2: Validate No Files Created

files_before = Glob(pattern=".ai_docs/Stories/STORY-*.md")

# Invoke subagent
Task(subagent_type="requirements-analyst", ...)

files_after = Glob(pattern=".ai_docs/Stories/STORY-*.md")

new_files = set(files_after) - set(files_before)
if len(new_files) > 0:
    ERROR: Subagent created unauthorized files: {new_files}
    Rollback: Delete new_files
    Recovery: Re-invoke with stricter prompt
```

**Effort:** Medium (2-3 hours to implement file system diff checks)
**Files Modified:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

---

### Long-Term Architectural Changes (Lower Priority - Week 3-4: 10-14 hours)

#### Fix 3: Skill-Specific Subagent (4-6 hours)

**Problem:** General-purpose `requirements-analyst` subagent doesn't understand story-creation workflow constraints.

**Solution:** Create skill-specific subagent in `.claude/agents/story-requirements-analyst.md` (NOT `.claude/skills/devforgeai-story-creation/subagents/` - that's aspirational!):

```yaml
---
name: story-requirements-analyst
description: Requirements analysis subagent specifically for devforgeai-story-creation skill. Returns CONTENT ONLY (no file creation).
parent_skill: devforgeai-story-creation
output_format: content_only (no file creation)
tools: [Read, Grep, Glob, AskUserQuestion]
model: sonnet
---

# Story Requirements Analyst Subagent

**Purpose:** Generate user story, acceptance criteria, and NFRs as **markdown content** (not files) for assembly into story-template.md by parent skill.

**Output Contract:**
- Return markdown text ONLY (no file creation)
- Sections: User Story, Acceptance Criteria (Given/When/Then), Edge Cases, Data Validation Rules, NFRs
- Parent skill will assemble this content into .story.md template
- Do NOT create SUMMARY, QUICK-START, VALIDATION-CHECKLIST files

**Invocation Pattern:**
Parent skill provides: Feature description, Story metadata (ID, epic, priority, points)
Subagent returns: Structured markdown sections (no file paths)

**CRITICAL:** You are a CONTENT GENERATOR, not a DOCUMENT CREATOR. Your output will be assembled by the devforgeai-story-creation skill into a single .story.md file. Do NOT create files yourself.
```

**Update Phase 2 to use skill-specific subagent:**
```python
Task(
  subagent_type="story-requirements-analyst",  # Not "requirements-analyst"
  ...
)
```

**Effort:** High (4-6 hours to create skill-specific subagent, test, update references)
**Files Created:** `.claude/agents/story-requirements-analyst.md`
**Files Modified:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Trade-off:** Duplicates requirements logic, but ensures output fits workflow

---

#### Fix 7: JSON Output Schema (6-8 hours)

**Problem:** Subagent output format is unstructured markdown, hard to validate/parse.

**Solution:** Require subagents to return structured JSON output:

```python
Task(
  subagent_type="requirements-analyst",
  prompt="""
  ...

  **OUTPUT FORMAT: JSON (not markdown)**
  Return JSON object with this schema:

  {
    "user_story": {
      "role": "string",
      "action": "string",
      "benefit": "string"
    },
    "acceptance_criteria": [
      {
        "title": "string",
        "given": "string",
        "when": "string",
        "then": "string"
      }
    ],
    "edge_cases": ["string"],
    "nfrs": {
      "performance": {"target": "string", "measurable": true},
      "security": {"target": "string"},
      ...
    }
  }
  """
)

# Skill parses JSON and assembles into markdown template
import json
subagent_data = json.loads(subagent_output)

# Validate schema
assert "user_story" in subagent_data
assert "acceptance_criteria" in subagent_data
assert len(subagent_data["acceptance_criteria"]) >= 3

# Assemble into template
user_story_section = f"**As a** {subagent_data['user_story']['role']}, **I want** {subagent_data['user_story']['action']}, **so that** {subagent_data['user_story']['benefit']}."
```

**Effort:** High (6-8 hours to redesign subagent output format, update all skills)
**Benefit:** Strongly typed output, easy validation, clear contract
**Files Modified:** All skills using `requirements-analyst`, `api-designer` subagents

---

## Implementation Roadmap

### Phase 1: Immediate (Week 1 - 2-4 hours)

**Goal:** Stop multi-file creation immediately

**Tasks:**
1. ✅ Fix 1: Update requirements-analysis.md prompt (30 min)
2. ✅ Fix 5: Add pre-flight briefing (15 min)
3. ✅ Fix 2: Add post-subagent validation (1-2 hrs)

**Expected Outcome:** Subagent will return content instead of creating files (90% confidence)

**Testing:**
```bash
# Test case 1: Single story creation
/create-story User registration form

# Expected: 1 file created (STORY-XXX-user-registration-form.story.md)
# Actual before fix: 5 files created
# Actual after fix: 1 file created ✅

# Test case 2: Epic batch creation (enhancement)
/create-story epic-001

# Expected: N files created (one per selected feature)
# All files should be .story.md format only
```

---

### Phase 2: Short-Term (Week 2 - 5-7 hours)

**Goal:** Add contract-based validation

**Tasks:**
4. ✅ Fix 4: Define subagent-skill contracts in YAML (3-4 hrs)
5. ✅ Fix 6: Implement file system diff check (2-3 hrs)

**Expected Outcome:** Contract-based validation ensures workflow compliance

**Testing:**
```bash
# Test contract validation
# 1. Subagent creates file → Contract violation detected → Rollback
# 2. Subagent returns content → Contract validation passes → Continue
```

---

### Phase 3: Long-Term (Week 3-4 - 10-14 hours)

**Goal:** Create tightly-coupled skill-subagent pairs

**Tasks:**
6. ✅ Fix 3: Create skill-specific `story-requirements-analyst` subagent (4-6 hrs)
7. ⚠️ Fix 7: Migrate to JSON output format (6-8 hrs) - **OPTIONAL** if Fix 1-2 still show issues

**Expected Outcome:** Tightly-coupled skill-subagent pairs eliminate ambiguity

---

## Testing Strategy

### Unit Tests (Per Fix)

**Fix 1 & 5 (Prompt Constraints):**
- Test 1: Invoke requirements-analyst with constrained prompt → Verify returns markdown text
- Test 2: Check output for file creation indicators → Should be none
- Test 3: Validate required sections present → All sections exist

**Fix 2 (Output Validation):**
- Test 1: Subagent output contains "File created:" → Validation fails, re-invoke
- Test 2: Subagent output is plain markdown → Validation passes
- Test 3: Missing required section → Validation fails with specific error

**Fix 6 (File System Diff):**
- Test 1: Files created during subagent execution → Detected and rolled back
- Test 2: No files created → Diff check passes

**Fix 3 (Skill-Specific Subagent):**
- Test 1: Invoke story-requirements-analyst → Returns content, not files
- Test 2: Output format matches contract → Valid markdown sections
- Test 3: Integration with Phase 5 assembly → Story file created correctly

---

### Integration Tests

**Full Workflow Test:**
```bash
# 1. Create single story
/create-story Database migration rollback procedure

# Assertions:
# - Only 1 file created: STORY-XXX-database-migration-rollback.story.md
# - File contains all sections (User Story, AC, Tech Spec, NFRs, Edge Cases, DoD)
# - YAML frontmatter valid
# - No extra files (SUMMARY.md, QUICK-START.md, etc.)

# 2. Create batch stories
/create-story epic-003

# Select 3 features
# Assertions:
# - Only 3 .story.md files created (no extra files per story)
# - All stories numbered sequentially
# - Epic file updated with story references
# - Sprint file updated (if assigned)
```

---

### Regression Tests

**Ensure no behavior changes:**
- Story content quality unchanged (same AC depth, same tech spec detail)
- Self-validation still works (Phase 7)
- Epic/sprint linking still works (Phase 6)
- Completion report still generated (Phase 8)

---

## Success Criteria

### Fix 1 & 5 Success

- [ ] Subagent prompt includes "CRITICAL OUTPUT CONSTRAINTS" section
- [ ] Prompt explicitly prohibits file creation
- [ ] Prompt specifies "markdown content only"
- [ ] Pre-flight briefing explains parent skill's role
- [ ] Test: Create story → Only 1 .story.md file created

### Fix 2 Success

- [ ] Output validation step added to Phase 2
- [ ] File creation patterns detected and blocked
- [ ] Required sections validated
- [ ] Re-invocation logic implemented
- [ ] Test: Subagent attempts file creation → Validation catches and re-invokes

### Fix 4 Success

- [ ] YAML contract file created
- [ ] Contract defines input/output schema
- [ ] Contract specifies constraints (no_file_creation: true)
- [ ] Skill reads and validates against contract
- [ ] Test: Contract validation passes for valid output, fails for violations

### Fix 6 Success

- [ ] File system diff check implemented
- [ ] Unauthorized files detected and deleted
- [ ] Recovery logic re-invokes subagent
- [ ] Test: Subagent creates files → Diff check detects and rolls back

### Fix 3 Success

- [ ] story-requirements-analyst subagent created
- [ ] Subagent output contract documented
- [ ] Phase 2 updated to use skill-specific subagent
- [ ] Test: Skill-specific subagent returns content, not files

---

## Related Issues

- **RCA-006:** Autonomous Deferrals (similar pattern - subagents operating autonomously)
- **Enhancement Request:** Batch story creation from epics (lines 1431-2054 in output2.md)

---

## References

- Original conversation: `tmp/output2.md`
- Skill: `.claude/skills/devforgeai-story-creation/SKILL.md`
- Reference: `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`
- Subagent: `.claude/agents/requirements-analyst.md`
- Template: `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

---

**Next Steps:**
1. Review RCA with team
2. Approve implementation roadmap
3. Create implementation tasks
4. Begin Phase 1 fixes (Week 1)
5. Document enhancement request separately (batch story creation)
