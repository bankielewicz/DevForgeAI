---
id: STORY-043
title: Update Internal Path References from .claude/ to src/claude/
epic: EPIC-009
sprint: Backlog
status: Backlog
points: 13
priority: High
assigned_to: TBD
created: 2025-11-16
format_version: "2.0"
---

# Story: Update Internal Path References from .claude/ to src/claude/

## Description

**As a** framework developer performing package distribution,
**I want** all internal path references updated from `.claude/` and `.devforgeai/` to `src/claude/` and `src/devforgeai/` in framework source files,
**so that** the framework operates correctly from the packaged source structure with zero broken references and proper progressive disclosure loading.

## Acceptance Criteria

### 1. [ ] Comprehensive Path Audit with Classification

**Given** the framework contains ~2,800+ path references across 450+ files
**When** I execute the audit scan with grep patterns for `.claude/` and `.devforgeai/`
**Then** the audit produces a classification report with 4 categories:
- **Deploy-time references** (KEEP AS-IS): @file references in CLAUDE.md, deployed .devforgeai/context/ references, CLI tool paths (~689 refs)
- **Source-time references** (UPDATE): Read() calls in skills loading references/ and assets/, documentation referencing source structure (~164 refs)
- **Ambiguous references** (MANUAL REVIEW): Mixed contexts requiring developer judgment (~35 refs)
- **Backup/archive files** (EXCLUDE): .backup, .original files that don't need updates (~1,926 refs)
**And** classification files created in `.devforgeai/specs/STORY-043/`:
  - path-audit-deploy-time.txt (689 refs)
  - path-audit-source-time.txt (164 refs)
  - path-audit-ambiguous.txt (35 refs)
  - path-audit-excluded.txt (1,926 refs)
**And** total references sum: 689 + 164 + 35 + 1,926 = 2,814

---

### 2. [ ] Surgical Update Strategy with Rollback Safety

**Given** the path audit identifies ~164 source-time references requiring updates across 87 files
**When** I execute the update script with dry-run validation
**Then** the script creates timestamped backup (`.backups/story-043-path-updates-{timestamp}/` with all 87 files)
**And** executes updates in 3 phases:
  1. Phase 1: Skills Read() calls for references/ and assets/ (74 refs updated)
  2. Phase 2: Documentation referencing source structure (52 refs updated)
  3. Phase 3: Agent/subagent framework integration references (38 refs updated)
**And** generates diff summary (`.devforgeai/specs/STORY-043/update-diff-summary.md`)
**And** provides rollback script (`.devforgeai/specs/STORY-043/rollback-updates.sh`)
**And** update execution report shows: "164 references updated across 87 files, 0 errors"

---

### 3. [ ] Zero Broken References Post-Update

**Given** all source-time path updates have been applied
**When** I execute the validation scan checking all updated paths
**Then** the scan confirms:
- 0 broken Read() calls (all `src/claude/skills/*/references/` paths resolve)
- 0 broken asset loads (all `src/claude/skills/*/assets/` paths resolve)
- 0 broken documentation links (all source structure references valid)
- 100% deployed references preserved (@file paths in CLAUDE.md unchanged)
- 100% context file references preserved (.devforgeai/context/ paths unchanged)
**And** validation report shows:
  - Skills: 74/74 Read() calls resolve (100%)
  - Assets: 18/18 asset loads resolve (100%)
  - Docs: 52/52 documentation links valid (100%)
  - Deploy references preserved: 689/689 (100%)
  - Context references preserved: 417/417 (100%)
  - Broken references detected: 0
**And** validation status: PASSED

---

### 4. [ ] Progressive Disclosure Loading from src/ Structure

**Given** skills load references/ files during workflow execution
**When** I test devforgeai-story-creation skill Phase 2 (loads acceptance-criteria-patterns.md from src/)
**Then** the skill executes `Read(file_path="src/claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md")`
**And** successfully loads 1,259 lines (48.2 KB)
**And** applies patterns for Given/When/Then AC generation
**And** no file-not-found errors occur
**And** progressive disclosure works identically to pre-refactor behavior
**And** test execution log confirms: "Progressive disclosure: WORKING (src/ structure)"

---

### 5. [ ] Framework Integration Validated (Skills + Subagents + Commands)

**Given** updated paths affect skills, subagents, and commands
**When** I execute the integration test suite (3 representative workflows)
**Then** all 3 workflows complete successfully:

**Test 1: Epic Creation** (`/create-epic User Authentication`)
- Command invokes devforgeai-orchestration skill ✓
- Skill loads feature-decomposition-patterns.md from src/claude/skills/devforgeai-orchestration/references/ ✓
- requirements-analyst subagent generates features ✓
- Epic file created with 5 features, 0 path errors ✓

**Test 2: Story Creation** (`/create-story User login with email/password`)
- Command invokes devforgeai-story-creation skill ✓
- Skill loads 6 reference files from src/claude/skills/devforgeai-story-creation/references/ ✓
- story-requirements-analyst subagent generates AC ✓
- Story file created with 5 Given/When/Then AC, 0 path errors ✓

**Test 3: Development Workflow** (`/dev STORY-044`)
- Command invokes devforgeai-development skill ✓
- Skill loads phase references from src/claude/skills/devforgeai-development/references/ ✓
- git-validator, tech-stack-detector subagents execute ✓
- TDD cycle completes, story status updated, 0 path errors ✓

**And** integration test report shows: "INTEGRATION: PASSED (3/3 workflows, 0 path errors)"

---

### 6. [ ] Deployment References Preserved (No .claude/ → src/claude/ for Deploy-Time)

**Given** CLAUDE.md contains 21 @file references to deployed locations
**When** I inspect CLAUDE.md after path updates
**Then** all 21 @file references remain unchanged:
- @.claude/memory/skills-reference.md ✓
- @.claude/memory/subagents-reference.md ✓
- @.claude/memory/commands-reference.md ✓
- @.devforgeai/protocols/lean-orchestration-pattern.md ✓
- ... (17 more)
**And** rationale documented: "These reference deployed framework files after installer runs, NOT source files"
**And** grep validation confirms:
  - `grep -c "@.claude/memory/" CLAUDE.md` returns 17
  - `grep -c "@src/claude/memory/" CLAUDE.md` returns 0
**And** deployed references status: PRESERVED (21/21, 100%)

---

### 7. [ ] Automated Update Script with Safety Guardrails

**Given** manual updates across 87 files would be error-prone
**When** I execute `.devforgeai/specs/STORY-043/update-paths.sh`
**Then** the script executes with safety guardrails:
- **Pre-flight checks**: Git status clean, backup space available (50 MB)
- **Backup creation**: Timestamped backup in .backups/ (87 files)
- **Classification loading**: Reads source-time.txt (164 refs to update)
- **Surgical updates**: Uses sed to update ONLY source-time references
- **Validation**: Runs zero-broken-references scan
- **Rollback on failure**: Auto-executes rollback if validation fails
- **Success reporting**: Generates summary (164 refs updated, 0 errors)
**And** script execution log shows all phases completed successfully

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Worker"
      name: "PathAuditScanner"
      file_path: "src/scripts/audit-path-references.sh"
      requirements:
        - id: "WKR-001"
          description: "Scan all files in src/ for .claude/ and .devforgeai/ path patterns"
          testable: true
          test_requirement: "Test: grep -r '\\.claude/' src/ | wc -l returns ~2800"
          priority: "Critical"

        - id: "WKR-002"
          description: "Classify references into 4 categories (deploy, source, ambiguous, excluded)"
          testable: true
          test_requirement: "Test: wc -l path-audit-*.txt files sum to total ref count"
          priority: "Critical"

        - id: "WKR-003"
          description: "Generate classification files for each category"
          testable: true
          test_requirement: "Test: All 4 classification files exist with >0 lines"
          priority: "High"

    - type: "Worker"
      name: "PathUpdateScript"
      file_path: "src/scripts/update-paths.sh"
      requirements:
        - id: "WKR-004"
          description: "Create timestamped backup before updates"
          testable: true
          test_requirement: "Test: Backup directory exists with all 87 files"
          priority: "Critical"

        - id: "WKR-005"
          description: "Update source-time references using sed (164 refs across 87 files)"
          testable: true
          test_requirement: "Test: git diff shows 164 line changes across 87 files"
          priority: "Critical"

        - id: "WKR-006"
          description: "Preserve deploy-time references (689 refs unchanged)"
          testable: true
          test_requirement: "Test: grep -c '@\\.claude/memory/' CLAUDE.md unchanged"
          priority: "Critical"

        - id: "WKR-007"
          description: "Run validation scan post-update (detect broken references)"
          testable: true
          test_requirement: "Test: Validation exits 0, reports 'Zero broken references'"
          priority: "Critical"

        - id: "WKR-008"
          description: "Auto-rollback on validation failure"
          testable: true
          test_requirement: "Test: Inject broken reference, script detects and rolls back"
          priority: "High"

    - type: "Worker"
      name: "ValidationScanner"
      file_path: "src/scripts/validate-paths.sh"
      requirements:
        - id: "WKR-009"
          description: "Syntactic validation: No old .claude/ patterns in Read() calls"
          testable: true
          test_requirement: "Test: grep 'Read.*\\.claude/' src/ returns 0 matches"
          priority: "Critical"

        - id: "WKR-010"
          description: "Semantic validation: All Read() paths resolve to existing files"
          testable: true
          test_requirement: "Test: Extract all Read() paths, verify with [ -f path ]"
          priority: "Critical"

        - id: "WKR-011"
          description: "Behavioral validation: Run 3 workflows, log 0 path errors"
          testable: true
          test_requirement: "Test: /create-epic, /create-story, /dev execute with 0 FileNotFoundError"
          priority: "High"

    - type: "Worker"
      name: "RollbackScript"
      file_path: "src/scripts/rollback-path-updates.sh"
      requirements:
        - id: "WKR-012"
          description: "Validate backup exists and is complete (87 files)"
          testable: true
          test_requirement: "Test: find backup-dir -type f | wc -l returns 87"
          priority: "Critical"

        - id: "WKR-013"
          description: "Restore all 87 files from backup using rsync"
          testable: true
          test_requirement: "Test: After rollback, git diff shows 0 changes (restored to pre-update)"
          priority: "Critical"

        - id: "WKR-014"
          description: "Re-run validation to confirm restoration successful"
          testable: true
          test_requirement: "Test: validate-paths-pre-update.sh exits 0 after rollback"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Deploy-time references must NEVER be updated (689 refs preserved)"
      test_requirement: "Test: Diff CLAUDE.md before/after shows 0 changes to @file lines"

    - id: "BR-002"
      rule: "Source-time references must ALL be updated (164 refs, 100% success)"
      test_requirement: "Test: grep 'Read.*src/claude/' src/ | wc -l returns 74"

    - id: "BR-003"
      rule: "Backup must be created BEFORE any file modifications"
      test_requirement: "Test: Update script timestamps show backup creation before first sed operation"

    - id: "BR-004"
      rule: "Validation failure triggers automatic rollback (no manual intervention)"
      test_requirement: "Test: Inject broken ref, script detects in validation, auto-rolls back"

    - id: "BR-005"
      rule: "Classification total must equal audit total (no references unaccounted for)"
      test_requirement: "Test: Sum of 4 classification file line counts equals total grep results"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Update script execution completes quickly"
      metric: "< 30 seconds for 164 reference updates across 87 files"
      test_requirement: "Test: time bash update-paths.sh, assert < 30s"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Validation scan completes in reasonable time"
      metric: "< 45 seconds for 2,800 reference checks"
      test_requirement: "Test: time bash validate-paths.sh, assert < 45s"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Atomic updates with crash safety"
      metric: "0 partial states (sed creates .bak files, rollback on crash)"
      test_requirement: "Test: Kill script mid-execution, verify .bak files allow recovery"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Idempotent execution"
      metric: "0 errors on second run (skips already-updated files)"
      test_requirement: "Test: Run update-paths.sh twice, second run reports '0 updates needed'"

    - id: "NFR-005"
      category: "Security"
      requirement: "No privileged operations required"
      metric: "Script runs with user permissions (no sudo)"
      test_requirement: "Test: Execute as non-root user, completes successfully"
```

### Dependencies

**Prerequisite Stories:**
- STORY-042 (File migration MUST be complete - src/ must contain files before updating paths)

**External Tools:**
- grep, sed, find (standard Unix utilities)
- git (for diff and status checks)
- rsync (for backup/restore)
- jq (optional, for JSON validation)

---

## Edge Cases

### 1. Circular Reference Detection
**Scenario:** Skill A loads reference from skill B which references skill A's assets
**Expected:** Detect and document circular chains (non-blocking, informational only)
**Handling:** Build reference dependency graph, report cycles: "Circular: devforgeai-development → qa-automation.md → devforgeai-development/scripts/"

### 2. Mixed Context References
**Scenario:** File contains both deploy-time (.devforgeai/context/) and source-time (Read .claude/skills/) references
**Expected:** Line-specific updates (deploy refs stay, source refs change)
**Handling:** Use line-aware sed patterns, manual review of 20 mixed-context files

### 3. Backup File Preservation
**Scenario:** .backup, .original files contain old paths intentionally (historical record)
**Expected:** Exclude from updates to preserve diff history
**Handling:** Audit excludes files matching `*.backup*`, `*.original`, `*.pre-*` patterns

### 4. Windows Path Separators
**Scenario:** Running in WSL with Windows-style paths (C:\Projects\...)
**Expected:** Ensure updates use forward slashes consistently
**Handling:** Normalize all paths to forward slashes before sed operations

### 5. Progressive Disclosure Chain Breaks
**Scenario:** Skill loads reference A which loads reference B (2-level chain)
**Expected:** Both references must update correctly or chain breaks
**Handling:** Validate 2-level reference chains (trace loaded files during skill execution)

### 6. Package.json Scripts Referencing .claude/
**Scenario:** npm scripts contain `.claude/scripts/install_hooks.sh`
**Expected:** These are DEPLOY-TIME references (stay unchanged)
**Handling:** Classification identifies package.json refs as deploy-time, audit preserves

### 7. Symlink Handling
**Scenario:** If src/claude/ is symlink during development (ln -s .claude src/claude)
**Expected:** Read() calls resolve correctly through symlinks
**Handling:** Test with symlink configuration, verify file resolution works

---

## Data Validation Rules

1. **Path format validation:** All updated paths must match `src/claude/` or `src/devforgeai/` (no trailing spaces, no mixed separators)

2. **File existence post-update:** Every updated Read() path must resolve to existing file (validate with test script checking all 164 paths)

3. **Deploy-time preservation:** Audit confirms 689 deploy-time refs unchanged (diff shows 0 changes for CLAUDE.md @file lines, .devforgeai/context/ refs)

4. **Backup completeness:** Backup must contain all 87 files being modified (compare file lists pre/post backup, assert equality)

5. **Rollback idempotency:** Running rollback twice produces identical result (no double-revert, checksums match original)

6. **Classification coverage:** Sum of 4 categories equals total references (689 + 164 + 35 + 1,926 = 2,814)

7. **Reference type consistency:** Within same file, similar references should classify the same way (e.g., all Read() calls in skills are source-time)

---

## Non-Functional Requirements

### Performance
- Update script: < 30 seconds for 164 updates
- Validation scan: < 45 seconds for 2,800 checks
- Backup creation: < 10 seconds for 87 files
- No file locking or blocking

### Security
- No sudo required (user permissions)
- Backup isolation (.backups/ gitignored)
- Script validation (set -euo pipefail)
- Rollback protection (validates backup exists)

### Reliability
- Atomic updates (sed -i with .bak)
- Validation gates (halt on failure)
- Idempotent (safe to retry)
- Error logging (update-errors.log)

### Maintainability
- Classification files human-readable
- Diff summary for code review
- Rollback script documented
- sed patterns documented in header

---

## Definition of Done

### Implementation
- [ ] Path audit script created and executed
- [ ] Classification files generated (4 categories)
- [ ] Update script created with 3-phase logic
- [ ] 164 source-time references updated across 87 files
- [ ] Validation script created (3-layer validation)
- [ ] Rollback script created and tested
- [ ] Diff summary generated for review
- [ ] Git staged (87 modified files)

### Quality
- [ ] All 7 acceptance criteria validated
- [ ] All 5 business rules enforced
- [ ] All 5 NFRs met and measured
- [ ] All 7 edge cases handled
- [ ] Zero broken references (validation passed)
- [ ] 100% deploy-time refs preserved

### Testing
- [ ] 10 unit tests (classification, backup, updates, rollback)
- [ ] 3 integration tests (epic/story/dev workflows)
- [ ] 5 regression tests (progressive disclosure, commands, skills, subagents, deploy refs)
- [ ] 3 performance benchmarks (update, validation, backup)
- [ ] Negative test (broken reference detection)

### Documentation
- [ ] PATH-UPDATE-STRATEGY.md created
- [ ] Update diff summary generated
- [ ] Rollback procedure documented
- [ ] EPIC-009 updated with Phase 3 status
- [ ] STORY-044 notified (src/ paths ready)

### Release Readiness
- [ ] Git commit with detailed message
- [ ] Code review completed (87 file diffs)
- [ ] Integration tests: 3/3 passed
- [ ] Phase 3 Go/No-Go: PASSED (zero broken refs)

---

## Workflow History

- **2025-11-16:** Story created for EPIC-009 Phase 3 (path reference updates)
- **2025-11-16:** Priority: High, Points: 13 (HIGH RISK refactoring)
- **2025-11-16:** Depends on STORY-042 (files must be in src/ first)
- **2025-11-16:** Blocks STORY-044 (installer needs updated paths)
- **2025-11-16:** Requirements analyst generated 7 ACs with classification strategy
- **2025-11-16:** Status: Backlog (awaiting STORY-042 completion)
