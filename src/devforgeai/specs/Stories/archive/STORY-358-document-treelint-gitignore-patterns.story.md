---
id: STORY-358
title: Document .treelint/ Gitignore Patterns
type: documentation
epic: EPIC-056
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-357"]
priority: High
advisory: false
assigned_to: Unassigned
created: 2026-02-04
format_version: "2.8"
---

# Story: Document .treelint/ Gitignore Patterns

## Description

**As a** DevForgeAI framework contributor or project maintainer,
**I want** gitignore pattern guidance for `.treelint/` files documented in source-tree.md with a rationale for each pattern,
**so that** I know which `.treelint/` artifacts to commit (project-specific configuration) and which to exclude (regenerable data, ephemeral sockets), preventing repository bloat and ensuring consistent team workflows.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="treelint-integration">
    <quote>"Prevents accidental commits of large index files and ephemeral sockets"</quote>
    <line_reference>EPIC-056, Feature 2 User Value</line_reference>
    <quantified_impact>Prevents repository bloat from index.db (can grow to hundreds of MB for large codebases)</quantified_impact>
  </origin>

  <decision rationale="document-in-source-tree">
    <selected>Document gitignore patterns within source-tree.md alongside the .treelint/ directory rules</selected>
    <rejected alternative="separate-gitignore-guide">
      A separate document would fragment information — developers check source-tree.md for directory guidance
    </rejected>
    <trade_off>Increases source-tree.md size slightly (~20 lines) but keeps all .treelint/ guidance co-located</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Gitignore Pattern Section Added to source-tree.md

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>source-tree.md contains the .treelint/ directory entry in the Framework Directory Structure tree diagram (added by STORY-357)</given>
  <when>a gitignore pattern documentation subsection is added within the .treelint/ rules in the "Directory Purpose and Rules" section</when>
  <then>the section lists exactly three file patterns (index.db, daemon.sock, config.toml) with their gitignore recommendation (GITIGNORED or OPTIONAL COMMIT) and each pattern has a rationale explaining WHY</then>
  <verification>
    <source_files>
      <file hint="Constitutional context file being modified">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-358/test_ac1_gitignore_patterns.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: index.db Documented as Gitignored with Rationale

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>the gitignore pattern documentation for .treelint/ exists in source-tree.md</given>
  <when>the entry for .treelint/index.db is examined</when>
  <then>index.db is marked as GITIGNORED with a rationale stating it is a SQLite AST index that can grow large (proportional to codebase size), is fully regenerable by running treelint commands, and would cause unnecessary merge conflicts if committed</then>
  <verification>
    <source_files>
      <file hint="Constitutional context file">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-358/test_ac2_index_db_gitignored.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: daemon.sock Documented as Gitignored with Rationale

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>the gitignore pattern documentation for .treelint/ exists in source-tree.md</given>
  <when>the entry for .treelint/daemon.sock is examined</when>
  <then>daemon.sock is marked as GITIGNORED with a rationale stating it is an ephemeral Unix IPC socket created at runtime by the Treelint daemon, is machine-specific, and cannot meaningfully exist in version control</then>
  <verification>
    <source_files>
      <file hint="Constitutional context file">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-358/test_ac3_daemon_sock_gitignored.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: config.toml Documented as Optional-Commit with Rationale

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>the gitignore pattern documentation for .treelint/ exists in source-tree.md</given>
  <when>the entry for .treelint/config.toml is examined</when>
  <then>config.toml is marked as OPTIONAL COMMIT with a rationale stating it contains project-specific Treelint settings (language filters, ignore patterns, daemon config) that benefit from team-wide consistency when committed, and a note that the current .gitignore blanket pattern (.treelint/) would need a negation rule (!.treelint/config.toml) to allow committing</then>
  <verification>
    <source_files>
      <file hint="Constitutional context file">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-358/test_ac4_config_toml_optional.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "source-tree.md gitignore patterns"
      file_path: "devforgeai/specs/context/source-tree.md"
      required_keys:
        - key: "Gitignore pattern table/section"
          type: "string"
          example: "| index.db | GITIGNORED | SQLite AST index, regenerable, can be large |"
          required: true
          validation: "Must list 3 file patterns with recommendation and rationale"
          test_requirement: "Test: Grep for 3 .treelint/ file patterns in gitignore section"
        - key: "index.db GITIGNORED entry"
          type: "string"
          required: true
          validation: "Must contain 'gitignored' and 'regenerable' keywords"
          test_requirement: "Test: Grep for index.db with gitignored rationale"
        - key: "daemon.sock GITIGNORED entry"
          type: "string"
          required: true
          validation: "Must contain 'gitignored' and 'ephemeral' keywords"
          test_requirement: "Test: Grep for daemon.sock with ephemeral rationale"
        - key: "config.toml OPTIONAL COMMIT entry"
          type: "string"
          required: true
          validation: "Must contain 'optional' and 'project' keywords"
          test_requirement: "Test: Grep for config.toml with optional commit rationale"
        - key: "Negation pattern note"
          type: "string"
          required: true
          validation: "Must reference !.treelint/config.toml or equivalent guidance"
          test_requirement: "Test: Grep for negation pattern reference"

  business_rules:
    - id: "BR-001"
      rule: "LOCKED status marker must remain unchanged"
      trigger: "Any modification to source-tree.md"
      validation: "Line 3 must contain **Status**: LOCKED"
      error_handling: "HALT if LOCKED marker modified or removed"
      test_requirement: "Test: Verify line 3 contains exact LOCKED marker string"
      priority: "Critical"
    - id: "BR-002"
      rule: "Only two valid recommendation values: GITIGNORED and OPTIONAL COMMIT"
      trigger: "Pattern documentation creation"
      validation: "Each entry uses exactly one of these two values"
      error_handling: "HALT if other values used (e.g., COMMITTED, REQUIRED)"
      test_requirement: "Test: Verify all pattern entries use valid recommendation values"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "All 6 context files pass framework validation after change"
      metric: "100% validation pass rate"
      test_requirement: "Test: Run context-validator against all 6 context files"
      priority: "Critical"
    - id: "NFR-002"
      category: "Performance"
      requirement: "source-tree.md size increase is minimal"
      metric: "Less than 500 bytes / 25 lines added"
      test_requirement: "Test: Compare line count before/after modification"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- No runtime performance impact (documentation-only change)
- source-tree.md file size increase: < 500 bytes (~15-25 lines)
- AI agent context loading: < 200 additional tokens

### Security
- No secrets, credentials, or sensitive data introduced
- config.toml guidance explicitly notes Treelint configuration files should not contain secrets

### Reliability
- Markdown formatting validated: no broken tables, no unclosed code blocks
- Pattern table format consistent with existing source-tree.md conventions
- All rationales have minimum 2 sentences

### Scalability
- Pattern table supports row-append for new .treelint/ files in future versions
- Maximum 20 entries before requiring a separate document (currently 3)

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-357:** Update source-tree.md with .treelint/ Directory Structure
  - **Why:** The .treelint/ directory entry must exist before adding gitignore pattern documentation
  - **Status:** Backlog

- [x] **STORY-349:** Approve ADR-013 Treelint Integration
  - **Why:** ADR-013 must be approved before modifying context files
  - **Status:** QA Approved

### External Dependencies
None.

### Technology Dependencies
None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ structural validation

**Test Scenarios:**
1. **Happy Path:** 3 gitignore patterns documented with recommendations and rationales
2. **Edge Cases:**
   - .gitignore negation pattern note present for config.toml
   - Cross-platform note for daemon.sock (Unix-only)
   - Pattern table extensible (row-append format)
   - LOCKED marker preserved
3. **Error Cases:**
   - Missing pattern entry (< 3 patterns)
   - Missing rationale for any pattern
   - Invalid recommendation value (not GITIGNORED or OPTIONAL COMMIT)

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Context Validation:** All 6 context files pass framework validation
2. **Cross-Reference:** .treelint/ directory entry (STORY-357) exists as prerequisite

---

## Acceptance Criteria Verification Checklist

### AC#1: Gitignore Pattern Section Added

- [ ] Gitignore pattern section exists in source-tree.md - **Phase:** 2 - **Evidence:** tests/STORY-358/test_ac1_gitignore_patterns.sh
- [ ] Exactly 3 file patterns listed - **Phase:** 2 - **Evidence:** Grep count
- [ ] Each pattern has recommendation and rationale - **Phase:** 2 - **Evidence:** Grep

### AC#2: index.db Documented as Gitignored

- [ ] index.db entry present with GITIGNORED recommendation - **Phase:** 2 - **Evidence:** tests/STORY-358/test_ac2_index_db_gitignored.sh
- [ ] Rationale mentions regenerable - **Phase:** 2 - **Evidence:** Grep
- [ ] Rationale mentions size concern - **Phase:** 2 - **Evidence:** Grep

### AC#3: daemon.sock Documented as Gitignored

- [ ] daemon.sock entry with GITIGNORED recommendation - **Phase:** 2 - **Evidence:** tests/STORY-358/test_ac3_daemon_sock_gitignored.sh
- [ ] Rationale mentions ephemeral - **Phase:** 2 - **Evidence:** Grep
- [ ] Rationale mentions runtime/IPC socket - **Phase:** 2 - **Evidence:** Grep

### AC#4: config.toml Documented as Optional-Commit

- [ ] config.toml entry with OPTIONAL COMMIT recommendation - **Phase:** 2 - **Evidence:** tests/STORY-358/test_ac4_config_toml_optional.sh
- [ ] Rationale mentions project-specific settings - **Phase:** 2 - **Evidence:** Grep
- [ ] .gitignore negation pattern note included - **Phase:** 2 - **Evidence:** Grep

---

**Checklist Progress:** 0/12 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Gitignore pattern section added to source-tree.md within .treelint/ rules - Completed: Added "`.treelint/` Gitignore Pattern Guidance" section at lines 712-720
- [x] index.db documented as GITIGNORED with regenerable/size rationale - Completed: Table row with GITIGNORED recommendation and multi-sentence rationale
- [x] daemon.sock documented as GITIGNORED with ephemeral/IPC rationale - Completed: Table row with GITIGNORED recommendation and ephemeral/IPC rationale
- [x] config.toml documented as OPTIONAL COMMIT with project-settings rationale - Completed: Table row with OPTIONAL COMMIT and project-specific rationale
- [x] .gitignore negation pattern guidance included for config.toml - Completed: Negation rule `!.treelint/config.toml` documented in rationale
- [x] Version incremented in source-tree.md header - Completed: v3.6 → v3.7 with STORY-358 reference
- [x] Last Updated date set to implementation date - Completed: 2026-02-05
- [x] LOCKED status marker preserved - Completed: Line 3 unchanged

### Quality
- [x] All 4 acceptance criteria have passing tests - Completed: 19/19 tests passing across 4 test files
- [x] Pattern format consistent with existing source-tree.md conventions - Completed: Table format with pipe delimiters
- [x] All rationales have minimum 2 sentences - Completed: Verified by AC2-4 tests
- [x] Only GITIGNORED and OPTIONAL COMMIT values used - Completed: No invalid values (COMMITTED/REQUIRED)

### Testing
- [x] tests/STORY-358/test_ac1_gitignore_patterns.sh passes - Completed: 6/6 tests pass
- [x] tests/STORY-358/test_ac2_index_db_gitignored.sh passes - Completed: 4/4 tests pass
- [x] tests/STORY-358/test_ac3_daemon_sock_gitignored.sh passes - Completed: 4/4 tests pass
- [x] tests/STORY-358/test_ac4_config_toml_optional.sh passes - Completed: 5/5 tests pass
- [x] Context-validator passes for all 6 context files - Completed: All 6 LOCKED, no violations

### Documentation
- [x] source-tree.md updated with gitignore pattern section - Completed: Lines 712-720 added
- [x] EPIC-056 Stories table updated with STORY-358 - Completed: Already present at line 261

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-02-05
**Branch:** main

- [x] Gitignore pattern section added to source-tree.md within .treelint/ rules - Completed: Added "`.treelint/` Gitignore Pattern Guidance" section at lines 712-720
- [x] index.db documented as GITIGNORED with regenerable/size rationale - Completed: Table row with GITIGNORED recommendation and multi-sentence rationale
- [x] daemon.sock documented as GITIGNORED with ephemeral/IPC rationale - Completed: Table row with GITIGNORED recommendation and ephemeral/IPC rationale
- [x] config.toml documented as OPTIONAL COMMIT with project-settings rationale - Completed: Table row with OPTIONAL COMMIT and project-specific rationale
- [x] .gitignore negation pattern guidance included for config.toml - Completed: Negation rule `!.treelint/config.toml` documented in rationale
- [x] Version incremented in source-tree.md header - Completed: v3.6 → v3.7 with STORY-358 reference
- [x] Last Updated date set to implementation date - Completed: 2026-02-05
- [x] LOCKED status marker preserved - Completed: Line 3 unchanged
- [x] All 4 acceptance criteria have passing tests - Completed: 19/19 tests passing across 4 test files
- [x] Pattern format consistent with existing source-tree.md conventions - Completed: Table format with pipe delimiters
- [x] All rationales have minimum 2 sentences - Completed: Verified by AC2-4 tests
- [x] Only GITIGNORED and OPTIONAL COMMIT values used - Completed: No invalid values (COMMITTED/REQUIRED)
- [x] tests/STORY-358/test_ac1_gitignore_patterns.sh passes - Completed: 6/6 tests pass
- [x] tests/STORY-358/test_ac2_index_db_gitignored.sh passes - Completed: 4/4 tests pass
- [x] tests/STORY-358/test_ac3_daemon_sock_gitignored.sh passes - Completed: 4/4 tests pass
- [x] tests/STORY-358/test_ac4_config_toml_optional.sh passes - Completed: 5/5 tests pass
- [x] Context-validator passes for all 6 context files - Completed: All 6 LOCKED, no violations
- [x] source-tree.md updated with gitignore pattern section - Completed: Lines 712-720 added
- [x] EPIC-056 Stories table updated with STORY-358 - Completed: Already present at line 261

### TDD Workflow Summary

**Phase 02 (Red):** Generated 19 tests covering all 4 ACs (test_ac1-4_*.sh)
**Phase 03 (Green):** Implemented gitignore pattern guidance table in source-tree.md
**Phase 04 (Refactor):** Added horizontal rule separator for consistency
**Phase 05 (Integration):** Verified Markdown validity, context file consistency
**Phase 06 (Deferral):** No deferrals needed - all DoD items completable

### Files Modified

- devforgeai/specs/context/source-tree.md (v3.7)

### Files Created

- tests/STORY-358/test_ac1_gitignore_patterns.sh
- tests/STORY-358/test_ac2_index_db_gitignored.sh
- tests/STORY-358/test_ac3_daemon_sock_gitignored.sh
- tests/STORY-358/test_ac4_config_toml_optional.sh

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-04 | claude/story-requirements-analyst | Created | Story created from EPIC-056 Feature 2 | STORY-358-document-treelint-gitignore-patterns.story.md |
| 2026-02-05 | claude/opus | Development | TDD workflow complete (19/19 tests pass), DoD validated | source-tree.md, tests/STORY-358/*.sh |
| 2026-02-05 | claude/qa-result-interpreter | QA Deep | PASSED: 19/19 tests, 1/1 validators, 0 violations | STORY-358-qa-report.md |

## Notes

**Design Decisions:**
- Gitignore patterns documented co-located with .treelint/ directory rules in source-tree.md (not a separate document)
- Table format used for extensibility (new files can be appended as rows)
- Only two recommendation values: GITIGNORED and OPTIONAL COMMIT (no COMMITTED because no .treelint/ file is unconditionally required in VCS)

**Edge Cases:**
- Current .gitignore blanket pattern (.treelint/) conflicts with optional-commit guidance for config.toml — resolution documented
- daemon.sock is Unix-only — Windows may use named pipe or TCP fallback
- Future Treelint versions may add new artifacts — table format supports row-append

**Related ADRs:**
- [ADR-013: Treelint Integration](../adrs/ADR-013-treelint-integration.md)

**References:**
- [EPIC-056: Treelint Context File Integration](../Epics/EPIC-056-treelint-context-file-integration.epic.md)
- [STORY-357: Update source-tree.md with .treelint/ Directory](STORY-357-update-source-tree-treelint-directory.story.md) — prerequisite

---

Story Template Version: 2.8
Last Updated: 2026-02-04
