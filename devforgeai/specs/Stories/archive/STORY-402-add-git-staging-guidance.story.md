---
id: STORY-402
title: Add Git Staging Guidance for Parallel Stories
type: refactor
epic: EPIC-063
sprint: Backlog
status: QA Approved
priority: Medium
points: 2
created: 2026-02-08
updated: 2026-02-08
assignee: unassigned
tags: [framework, git, documentation, parallel-development, refactor]
source_recommendation: REC-STORY370-003
template_version: "2.8"
---

# STORY-402: Add Git Staging Guidance for Parallel Stories

## Description

Add a "Selective Staging for Parallel Stories" section to git-workflow-conventions.md with explicit `git add` patterns for when multiple stories have uncommitted changes in the same working tree.

<!-- provenance>
  <origin document="EPIC-063" section="Feature 4">
    <quote>Add selective staging guidance with explicit git add patterns for when multiple stories have uncommitted changes in the same working tree</quote>
    <line_reference>lines 263-326</line_reference>
  </origin>
  <decision rationale="Documentation prevents cross-story commit contamination">
    <selected>Add selective staging section to git-workflow-conventions.md</selected>
    <rejected>Rely on developers to discover patterns independently</rejected>
    <trade_off>Documentation overhead vs developer experience</trade_off>
  </decision>
</provenance -->

## User Story

**As a** framework developer working on multiple stories simultaneously in a shared working tree,
**I want** explicit selective staging guidance with pattern-based `git add` examples in the git workflow conventions reference,
**So that** I avoid accidentally contaminating commits with changes belonging to other in-progress stories.

## Acceptance Criteria

<acceptance_criteria id="AC1" title="New section exists in git-workflow-conventions.md">
  <given>The file `src/claude/skills/devforgeai-development/references/git-workflow-conventions.md` currently contains staging strategy content</given>
  <when>The new "Selective Staging for Parallel Stories" section is added</when>
  <then>The section is positioned after existing staging strategy content with a level-2 heading `## Selective Staging for Parallel Stories`</then>
  <verification>
    <method>Grep file for "## Selective Staging for Parallel Stories"</method>
    <expected_result>Exactly 1 match, positioned after staging strategy section</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/git-workflow-conventions.md" hint="Add after staging strategy"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC2" title="Pattern-based git add examples included">
  <given>The new "Selective Staging for Parallel Stories" section exists</given>
  <when>A developer reads the section</when>
  <then>It contains at least three `git add` command examples using story-specific file patterns including story files, phase state, and implementation-specific patterns</then>
  <verification>
    <method>Count git add examples with STORY-XXX patterns</method>
    <expected_result>At least 3 git add commands with story-specific patterns</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/git-workflow-conventions.md" hint="Pattern examples required"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC3" title="Verification command documented">
  <given>The new section contains pattern-based staging examples</given>
  <when>A developer follows the documented workflow</when>
  <then>The section includes a `git diff --cached --name-only` verification command with instruction to run before every commit</then>
  <verification>
    <method>Grep for "git diff --cached --name-only"</method>
    <expected_result>Command present with verification instruction</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/git-workflow-conventions.md" hint="Verification step required"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC4" title="Anti-pattern warning for broad staging commands">
  <given>The new section exists</given>
  <when>A developer reads the anti-pattern warning subsection</when>
  <then>The section warns against using `git add .` and `git add -A` in multi-story working trees, explaining these can contaminate commits</then>
  <verification>
    <method>Grep for warnings about "git add ." and "git add -A"</method>
    <expected_result>Both anti-patterns explicitly warned against</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/git-workflow-conventions.md" hint="Anti-pattern warning required"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC5" title="Worktree recommendation with cross-reference">
  <given>The new section covers selective staging for shared working trees</given>
  <when>A developer reads the "When to Use Worktrees Instead" subsection</when>
  <then>The section references the existing lock coordination section and recommends worktrees for stories touching many shared files</then>
  <verification>
    <method>Grep for reference to "Lock Coordination" or "Phase 08.0.5"</method>
    <expected_result>Cross-reference to existing worktree documentation</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/git-workflow-conventions.md" hint="Line 199: Lock Coordination section"/>
  </source_files>
</acceptance_criteria>

## Technical Specification

### Component Overview

| Component | Type | Description |
|-----------|------|-------------|
| git-workflow-conventions.md | Configuration | Git workflow reference (add new section) |

### Technical Details

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Configuration
      name: Selective Staging Section
      file_path: src/claude/skills/devforgeai-development/references/git-workflow-conventions.md
      description: New section for selective staging in multi-story working trees
      dependencies:
        - Phase 08.0.5 Lock Coordination (same file)
        - devforgeai/specs/context/source-tree.md (path validation)
      test_requirement: Section exists with 3+ git add examples and verification command

  business_rules:
    - rule: Never use broad staging in multi-story trees
      description: git add . and git add -A are anti-patterns for parallel stories
      test_requirement: Section contains explicit warning against both commands

    - rule: Always verify before commit
      description: git diff --cached --name-only must be run before every commit
      test_requirement: Verification command documented in section

  non_functional_requirements:
    - category: Reliability
      requirement: Accurate cross-references
      metric: All referenced sections exist
      test_requirement: Grep confirms Phase 08.0.5 exists at referenced location
```

### Section Structure

```markdown
## Selective Staging for Parallel Stories

### When This Applies
[Scenario explanation]

### Pattern-Based Staging Examples
[git add examples with STORY-XXX patterns]

### Verification Command
[git diff --cached --name-only with instruction]

### Anti-Pattern Warning
[Warning against git add . and git add -A]

### When to Use Worktrees Instead
[Cross-reference to lock coordination, recommendations]
```

### Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `src/claude/skills/devforgeai-development/references/git-workflow-conventions.md` | Edit | Add new section after staging strategy |

## Edge Cases

1. **Stories modifying same file:** Selective staging by filename insufficient. Recommend `git add -p` or worktrees.

2. **Untracked new files with ambiguous ownership:** Developers must check new files against story specification.

3. **Phase state files from concurrent /dev runs:** Call out phase state files as common oversight (STORY-XXX pattern helps).

4. **Test directory overlap:** Note that `tests/STORY-XXX/` convention supports clean separation.

5. **Session memory files:** These may be created as side effects and should typically be excluded from story-specific commits.

## Non-Functional Requirements

| Category | Requirement | Metric |
|----------|-------------|--------|
| Performance | No runtime impact | Documentation-only change |
| Reliability | Accurate cross-references | All referenced sections exist |
| Security | No sensitive patterns | Examples use explicit paths, not wildcards |

## Definition of Done

### Implementation
- [x] New section "Selective Staging for Parallel Stories" added
- [x] Section positioned after existing staging strategy content
- [x] At least 3 pattern-based `git add` examples included
- [x] `git diff --cached --name-only` verification command documented
- [x] Anti-pattern warning for `git add .` and `git add -A` included
- [x] Cross-reference to lock coordination section included

### Quality
- [x] Section uses correct heading format (## level-2)
- [x] Code blocks use ```bash language tag
- [x] STORY-XXX placeholder used consistently
- [x] Cross-references accurate and sections exist

### Testing
- [x] Grep confirms new section heading exists
- [x] Grep confirms at least 3 git add examples
- [x] Grep confirms verification command present
- [x] Grep confirms anti-pattern warnings present
- [x] Grep confirms lock coordination cross-reference

### Documentation
- [x] Self-documenting (the story IS the documentation change)

## Implementation Notes

- [x] New section "Selective Staging for Parallel Stories" added - Completed: Added at lines 1117-1233 of git-workflow-conventions.md
- [x] Section positioned after existing staging strategy content - Completed: Positioned after line 1100 (existing staging ends at ~1114)
- [x] At least 3 pattern-based `git add` examples included - Completed: 7 examples provided with STORY-XXX patterns
- [x] `git diff --cached --name-only` verification command documented - Completed: Documented in Verification Command subsection with before-commit instruction
- [x] Anti-pattern warning for `git add .` and `git add -A` included - Completed: Anti-Pattern Warning subsection with contamination explanation
- [x] Cross-reference to lock coordination section included - Completed: Reference to Phase 08.0.5 Lock Coordination in When to Use Worktrees Instead subsection
- [x] Section uses correct heading format (## level-2) - Completed: Section uses ## heading
- [x] Code blocks use ```bash language tag - Completed: All code blocks tagged with bash
- [x] STORY-XXX placeholder used consistently - Completed: Consistent placeholder usage throughout
- [x] Cross-references accurate and sections exist - Completed: All cross-references verified
- [x] Grep confirms new section heading exists - Completed: Test AC1.1 PASS
- [x] Grep confirms at least 3 git add examples - Completed: Test AC2.1 PASS (found 7)
- [x] Grep confirms verification command present - Completed: Test AC3.1 PASS
- [x] Grep confirms anti-pattern warnings present - Completed: Tests AC4.1-AC4.3 PASS
- [x] Grep confirms lock coordination cross-reference - Completed: Test AC5.1 PASS
- [x] Self-documenting (the story IS the documentation change) - Completed: Story adds documentation as its deliverable

### Test Results
- Total: 14 tests
- Passed: 14
- Failed: 0
- Status: GREEN

## Notes

- **Source Recommendation:** REC-STORY370-003 from STORY-370 Phase 09 framework-analyst analysis
- **Root Cause:** No guidance for selective staging in shared working trees
- **Impact:** Prevents cross-story commit contamination

## Key References

| Reference | Path | Relevance |
|-----------|------|-----------|
| Git Workflow Conventions | `src/claude/skills/devforgeai-development/references/git-workflow-conventions.md` | Target file (1,557 lines) |
| Git Operations Policy | `.claude/rules/core/git-operations.md` | Safe operations policy |

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/opus | Story Creation | Initial story created from EPIC-063 Feature 4 | STORY-402-add-git-staging-guidance.story.md |
| 2026-02-09 | claude/opus | Dev Complete | TDD workflow complete: Added "Selective Staging for Parallel Stories" section (116 lines) with pattern-based staging examples, verification command, anti-pattern warnings, and worktree cross-reference. 14/14 tests passing. | src/claude/skills/devforgeai-development/references/git-workflow-conventions.md, tests/STORY-402/test-ac-validation.sh |
| 2026-02-09 | .claude/qa-result-interpreter | QA Deep | PASSED: 14/14 tests, 100% traceability, 2/2 validators passed, 0 violations | - |
