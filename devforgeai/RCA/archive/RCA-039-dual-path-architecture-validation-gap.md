# RCA-039: Dual-Path Architecture Validation Gap

**Date:** 2026-02-22
**Reported By:** User
**Affected Component:** /validate-stories command, devforgeai-story-creation skill (context-validation.md)
**Severity:** HIGH

---

## Issue Description

Stories 472-479 (EPIC-081 and EPIC-082) were created via `/create-story` with all technical specification `file_path` fields pointing to `.claude/` operational paths instead of `src/claude/` source-of-truth paths. Subsequently, `/validate-stories STORY-472..STORY-479` did not detect this as a violation.

**Specific Issues:**
1. **13 file_path values** across 6 stories referenced `.claude/` operational paths (e.g., `.claude/agents/alignment-auditor.md`) instead of `src/claude/` (e.g., `src/claude/agents/alignment-auditor.md`)
2. **No `dual_path_sync` block** existed in any story's technical specification
3. **No DoD items** for dual-path sync (create in src/, sync to .claude/, test against src/)
4. `/validate-stories` passed all 8 stories as COMPLIANT despite this constitutional violation

**Expected Behavior:**
- `/create-story` should generate `file_path` values pointing to `src/claude/` (source of truth per source-tree.md §Dual-Location Architecture)
- `/create-story` should include `dual_path_sync` block in technical spec for stories creating/modifying `.claude/` files
- `/validate-stories` should detect and flag stories with `.claude/` paths that lack corresponding `src/` paths

**Impact:**
- `/dev` workflow would create files in `.claude/` (operational) instead of `src/` (source of truth)
- Dual-path sync would be missed, causing `src/` tree to drift from operational folders
- Tests run against `src/` tree would fail because files were created in `.claude/` instead

---

## 5 Whys Analysis

**Issue:** Stories created with `.claude/` operational paths instead of `src/` source-of-truth paths, and `/validate-stories` did not detect the violation.

1. **Why did the stories contain `.claude/` paths instead of `src/` paths?**
   - The devforgeai-story-creation skill's technical specification phase generates `file_path` values from source-tree.md's directory listings. Source-tree.md lists `.claude/skills/`, `.claude/agents/`, `.claude/commands/` as the canonical structure. The skill uses these directly without translating to the `src/` development path.
   - **Evidence:** source-tree.md lines 26-291 (directory structure lists `.claude/` as primary); context-validation.md `validate_file_paths()` lines 117-119 builds `allowed_paths` from source-tree.md directory tree

2. **Why doesn't `validate_file_paths()` catch `.claude/` paths that should be `src/`?**
   - The function validates that paths exist in source-tree.md's directory structure, but doesn't check the dual-path architecture rule. It treats `.claude/agents/alignment-auditor.md` as a valid path because `.claude/agents/` IS listed in source-tree.md. The function has no concept of "development should happen in `src/`."
   - **Evidence:** context-validation.md lines 104-150 — `validate_file_paths()` checks FORBIDDEN and INVALID paths but has no check for dual-path compliance. Zero occurrences of "dual-path", "src/claude", or "source of truth" in the file.

3. **Why was dual-path validation never added to `validate_file_paths()`?**
   - The validation functions were written before the dual-path architecture was fully codified. When source-tree.md §Dual-Location Architecture was added (STORY-048), the context-validation.md reference was never updated to include dual-path compliance as a validation dimension.
   - **Evidence:** source-tree.md lines 556-576 (Dual-Location Architecture section exists); context-validation.md has no corresponding validation function for dual-path.

4. **Why wasn't this gap caught and fixed after it was first discovered?**
   - RCA-033 (2026-01-26, "Story Creation Constitutional Non-Conformance") identified this EXACT gap as issue #2: "Dual-location architecture not addressed — Stories didn't specify whether to modify `src/claude/agents/` (source of truth) or `.claude/agents/` (operational)." RCA-033 produced REC-2 (CRITICAL): "Add Dual-Location Validation to Step 7.7." However, the recommendation was never implemented.
   - **Evidence:** RCA-033 line 23 (issue #2), lines 265-299 (REC-2), line 519 (implementation checklist unchecked). RCA-033 status: OPEN.

5. **Why was RCA-033 REC-2 never implemented?**
   - **ROOT CAUSE:** The framework has no mechanism to track RCA recommendation implementation. RCA documents are created as standalone `.md` files in `devforgeai/RCA/` but recommendations are never automatically converted to stories, assigned to sprints, or tracked for completion. The pipeline from "RCA recommendation written" to "recommendation implemented" is entirely manual and has no enforcement, monitoring, or escalation.

---

## Evidence Collected

**Files Examined:**

| File | Lines | Finding | Significance |
|------|-------|---------|-------------|
| `devforgeai/specs/context/source-tree.md` | 556-576 | Dual-Location Architecture section clearly states `src/` is source of truth, `.claude/` is operational/read-only | CRITICAL — Constitutional rule exists but is not enforced by validators |
| `.claude/skills/devforgeai-story-creation/references/context-validation.md` | 104-150 | `validate_file_paths()` checks paths against source-tree.md directory tree but has zero dual-path checks | CRITICAL — The validation function is the gap |
| `.claude/commands/validate-stories.md` | Full file | Invokes context-validation.md functions; no independent dual-path check | HIGH — Command delegates to validation functions that lack the check |
| `devforgeai/RCA/RCA-033-story-creation-constitutional-non-conformance.md` | 23, 265-299 | Issue #2 and REC-2 identify this exact gap; status OPEN, checklist unchecked | CRITICAL — Known gap from 27 days ago, never fixed |
| Stories 472-479 | Technical spec YAML | All 13 `file_path` values reference `.claude/` instead of `src/claude/` | HIGH — Direct evidence of the gap's impact |

**Context Files Status:**

| File | Status | Dual-Path Rule |
|------|--------|---------------|
| source-tree.md | ✅ EXISTS | ✅ Rule defined (lines 556-576) |
| tech-stack.md | ✅ EXISTS | N/A |
| dependencies.md | ✅ EXISTS | N/A |
| coding-standards.md | ✅ EXISTS | N/A |
| architecture-constraints.md | ✅ EXISTS | N/A |
| anti-patterns.md | ✅ EXISTS | N/A |

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

#### REC-1: Add `validate_dual_path()` Function to context-validation.md

**Problem Addressed:** No validation function checks dual-path architecture compliance in story technical specifications.

**Proposed Solution:** Add a 7th validation function `validate_dual_path(tech_spec_content)` to `context-validation.md` after the existing 6 functions.

**Implementation Details:**

- **File:** `src/claude/skills/devforgeai-story-creation/references/context-validation.md`
- **Section:** After function #6 (`validate_anti_patterns`), before "Custody Chain Validation Functions"
- **Add:**

```markdown
### 7. validate_dual_path(tech_spec_content)

**Purpose:** Validate that stories creating/modifying .claude/ files specify src/ as development path

**Severity:** HIGH

**Input:** Technical specification content from story

**Process:**
```
1. Read source-tree.md:
   source_tree = Read(file_path="devforgeai/specs/context/source-tree.md")

2. Check if Dual-Location Architecture section exists:
   IF "Dual-Location Architecture" NOT in source_tree:
     RETURN []  # Project doesn't use dual-path

3. Extract file_path values from tech_spec_content:
   - Scan for file_path: "..." fields in YAML
   - Scan for file references in components section

4. Check dual-path compliance:
   FOR each path in file_paths:
     IF path starts with ".claude/":
       expected_src_path = path.replace(".claude/", "src/claude/")

       # Check if story has dual_path_sync block
       IF "dual_path_sync" NOT in tech_spec_content:
         violations.append({
           type: "MISSING_DUAL_PATH_SYNC",
           path: path,
           expected: expected_src_path,
           severity: "HIGH",
           source: "source-tree.md §Dual-Location Architecture",
           remediation: f"Change file_path to '{expected_src_path}' and add dual_path_sync block"
         })
       ELIF expected_src_path NOT in tech_spec_content:
         violations.append({
           type: "OPERATIONAL_PATH_AS_TARGET",
           path: path,
           expected: expected_src_path,
           severity: "HIGH",
           source: "source-tree.md §Dual-Location Architecture",
           remediation: f"file_path should be '{expected_src_path}' (src/ is source of truth)"
         })

5. Check exemptions:
   # These paths are NOT dual-path:
   exempt_prefixes = ["devforgeai/specs/", "CLAUDE.md", "README.md"]
   # devforgeai/specs/ content (stories, epics, ADRs, context) lives only in devforgeai/
   # Root files (CLAUDE.md, README.md) are single-path

6. Return violations list
```
```

**Rationale:** Source-tree.md lines 556-576 define `src/` as source of truth and `.claude/` as operational/read-only. This validation function enforces that constitutional rule during story creation and validation.

**Testing:**
- Create a test story with `.claude/agents/test.md` as file_path → should produce MISSING_DUAL_PATH_SYNC violation
- Create a test story with `src/claude/agents/test.md` and dual_path_sync block → should pass
- Create a test story with `devforgeai/specs/adrs/ADR-021.md` → should pass (exempt)

**Effort:** Medium (1-2 hours)

---

#### REC-2: Update `/validate-stories` Phase 2 to Invoke `validate_dual_path()`

**Problem Addressed:** `/validate-stories` Phase 2 invokes 6 validation functions but not dual-path validation.

**Proposed Solution:** Add `validate_dual_path()` call to Phase 2 validation loop.

**Implementation Details:**

- **File:** `src/claude/commands/validate-stories.md`
- **Section:** Phase 2, after existing validation calls
- **Add after line:** `IF context_status.anti_patterns: violations.extend(validate_anti_patterns(tech_spec))`
- **Add:**

```markdown
     IF context_status.source_tree:      violations.extend(validate_dual_path(tech_spec))
```

**Rationale:** The validate_dual_path function exists in context-validation.md (after REC-1). The command must invoke it alongside the other 6 validation functions.

**Testing:**
- Run `/validate-stories` on a story with `.claude/` paths → should flag as violation
- Run `/validate-stories` on a story with `src/` paths → should pass

**Effort:** Low (15 minutes)

---

### HIGH Priority (Implement This Sprint)

#### REC-3: Update devforgeai-story-creation Skill to Generate `src/` Paths

**Problem Addressed:** The story creation skill generates `.claude/` paths in technical specifications because it reads source-tree.md's directory listings directly.

**Proposed Solution:** In the technical-specification-creation phase, when generating `file_path` values for components in `.claude/` directories, automatically prefix with `src/` and add `dual_path_sync` block.

**Implementation Details:**

- **File:** `src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md`
- **Section:** File path generation logic
- **Add:** Path translation rule:

```markdown
## Dual-Path Translation Rule

When generating file_path values for technical specification components:

IF file_path starts with ".claude/":
  1. Replace file_path with "src/claude/{remainder}"
  2. Add dual_path_sync block to technical_specification YAML:

     dual_path_sync:
       note: "Per source-tree.md dual-path architecture, development happens in src/ tree."
       source_paths:
         - "src/claude/{remainder}"
       operational_paths:
         - ".claude/{remainder}"
       test_against: "src/"

  3. Add "Dual-Path Sync" subsection to Definition of Done:
     ### Dual-Path Sync
     - [ ] Files created/modified in src/claude/ (source of truth)
     - [ ] Files synced to .claude/ (operational)
     - [ ] Tests run against src/ tree

EXEMPT paths (single-path, no translation needed):
  - devforgeai/specs/* (stories, epics, ADRs, context files)
  - CLAUDE.md (project root)
  - README.md, ROADMAP.md, LICENSE (root files)
  - tests/* (test directory)
```

**Rationale:** Fixing the generation point prevents the issue from occurring. Combined with REC-1/REC-2 validation, this creates defense-in-depth.

**Testing:**
- Run `/create-story` for a feature creating `.claude/agents/new-agent.md` → file_path should be `src/claude/agents/new-agent.md` with dual_path_sync block
- Run `/create-story` for an ADR → file_path should remain `devforgeai/specs/adrs/` (no translation)

**Effort:** Medium (1-2 hours)

---

#### REC-4: Implement RCA Recommendation Tracking Mechanism

**Problem Addressed:** ROOT CAUSE — RCA-033 REC-2 was documented 27 days ago but never implemented because no tracking mechanism exists.

**Proposed Solution:** Add a post-RCA step that automatically creates a story or technical debt item for each CRITICAL/HIGH recommendation.

**Implementation Details:**

- **File:** `src/claude/skills/devforgeai-rca/SKILL.md`
- **Section:** After Phase 7 (Completion Report), add Phase 7.5
- **Add:**

```markdown
### Phase 7.5: Recommendation-to-Story Pipeline

FOR each recommendation with priority CRITICAL or HIGH:
  AskUserQuestion:
    Question: "REC-{N} ({priority}): {title}. Create a story for implementation?"
    Header: "RCA Story"
    Options:
      - "Create story now" / Description: "Run /create-story with REC details"
      - "Add to technical debt register" / Description: "Track in technical-debt-register.md"
      - "Skip" / Description: "Acknowledged, no action"

  IF "Create story":
    Display: "Run: /create-story {REC summary as feature description}"
  IF "Add to debt":
    Append to devforgeai/technical-debt-register.md
```

**Rationale:** This is the root cause fix. Without tracking, RCA recommendations decay into unimplemented documentation. The `/create-stories-from-rca` command already exists but is not automatically invoked after RCA creation.

**Testing:**
- Complete an RCA with CRITICAL recommendation → should prompt for story creation
- Select "Add to debt" → should appear in technical-debt-register.md

**Effort:** Medium (1-2 hours)

---

### MEDIUM Priority (Next Sprint)

#### REC-5: Close RCA-033 OPEN Recommendations

**Problem Addressed:** RCA-033 has been OPEN for 27 days with 6 unchecked recommendations, including the dual-path validation (REC-2) that this RCA re-identifies.

**Proposed Solution:** Run `/create-stories-from-rca RCA-033` to convert remaining open recommendations to implementable stories. Mark RCA-033 as RESOLVED after stories are created.

**Implementation Details:**

- **Command:** `/create-stories-from-rca RCA-033`
- **Expected Output:** 2-4 stories covering REC-1 through REC-6
- **Post-action:** Update RCA-033 status from OPEN to RESOLVED

**Rationale:** Prevents further recurrence by closing the loop on the original RCA.

**Effort:** Low (30 minutes)

---

### LOW Priority (Backlog)

#### REC-6: Add RCA Status Dashboard to `/audit-deferrals`

**Problem Addressed:** No visibility into OPEN RCA count or age.

**Proposed Solution:** Add an "Open RCAs" section to the `/audit-deferrals` command output showing RCA count, oldest open RCA, and recommendations awaiting implementation.

**Effort:** Low (1 hour)

---

## Implementation Checklist

- [ ] **REC-1+2:** Add `validate_dual_path()` + /validate-stories integration: See **STORY-487**
- [ ] **REC-3:** Add dual-path translation rule to create-story skill: See **STORY-488**
- [ ] **REC-4:** Add Phase 7.5 recommendation-to-story pipeline: See **STORY-489**
- [ ] **REC-5:** Run `/create-stories-from-rca RCA-033` to close open recommendations (command invocation, not story)
- [ ] **REC-6:** Add RCA status dashboard to `/audit-deferrals`: See **STORY-490**
- [ ] Sync all src/ changes to .claude/ operational folders
- [ ] Mark RCA-033 as RESOLVED (superseded by this RCA's implementation)
- [ ] Mark RCA-039 as RESOLVED after implementation complete

---

## Prevention Strategy

**Short-term (Immediate):**
- Implement REC-1 + REC-2 to add dual-path validation to `/validate-stories` and `/create-story`
- Implement REC-3 to fix path generation at source

**Long-term (Framework Enhancement):**
- Implement REC-4 to ensure RCA recommendations are tracked to completion
- Run `/create-stories-from-rca` after every RCA to prevent recommendation decay
- Consider automated RCA aging alerts (REC-6)

**Monitoring:**
- `/validate-stories all` periodic runs should catch dual-path violations
- `/audit-deferrals` should show open RCA count (after REC-6)
- Next story creation batch should produce `src/` paths (after REC-3)

---

## Related RCAs

- **RCA-033:** Story Creation Constitutional Non-Conformance (OPEN, 2026-01-26) — **DIRECT PREDECESSOR**: Identified the same dual-path gap as issue #2, produced REC-2, never implemented. This RCA (039) is the recurrence caused by RCA-033's unimplemented fix.
- **RCA-034:** Batch Story Creation Constitutional Violations — Related pattern of story creation producing non-conformant output
- **RCA-028:** Manual Story Creation Ground Truth Validation Failure — Related pattern of missing validation in story creation pipeline
