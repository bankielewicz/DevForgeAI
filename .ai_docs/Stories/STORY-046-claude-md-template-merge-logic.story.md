---
id: STORY-046
title: CLAUDE.md Template Merge with Variable Substitution and Conflict Resolution
epic: EPIC-009
sprint: Backlog
status: Backlog
points: 13
priority: High
assigned_to: TBD
created: 2025-11-16
format_version: "2.0"
depends_on: STORY-045
---

# Story: CLAUDE.md Template Merge with Variable Substitution and Conflict Resolution

## Description

**As a** DevForgeAI user installing the framework in my project,
**I want** the installer to intelligently merge the DevForgeAI CLAUDE.md template with my existing project instructions, substituting variables and resolving conflicts with my approval,
**so that** I keep all my custom project rules while gaining DevForgeAI framework capabilities without manual editing.

## Acceptance Criteria

### 1. [ ] Framework Template Variables Detected and Substituted

**Given** src/CLAUDE.md contains template variables for project-specific values
**When** the installer runs variable detection and substitution
**Then** all variables are identified and replaced:
- `{{PROJECT_NAME}}` → Detected from git remote URL or directory name or user input
- `{{PROJECT_PATH}}` → Absolute path to target project (e.g., `/home/user/MyProject`)
- `{{PYTHON_VERSION}}` → Detected from `python3 --version` (e.g., "Python 3.10.11")
- `{{PYTHON_PATH}}` → Detected from `which python3` (e.g., "/usr/bin/python3")
- `{{TECH_STACK}}` → Detected from package files (package.json → "Node.js", requirements.txt → "Python", *.csproj → ".NET") or "Not configured"
- `{{INSTALLATION_DATE}}` → Current date in ISO 8601 format (e.g., "2025-11-17")
- `{{FRAMEWORK_VERSION}}` → From src/devforgeai/version.json (e.g., "1.0.1")
**And** substitution report shows: "7 variables detected, 7 substituted (100%)"
**And** resulting CLAUDE.md contains no unsubstituted `{{VAR}}` patterns (grep returns 0 matches)

---

### 2. [ ] User Custom Sections Preserved with Zero Data Loss

**Given** user has existing CLAUDE.md with custom instructions (e.g., "## My Project Rules", "## API Keys Location")
**When** the merge parser processes the existing file
**Then** all user sections are identified and preserved:
- Parser detects section boundaries (##, ###, #### markdown headers)
- Extracts user content for each custom section
- Marks sections with metadata: `<!-- USER_SECTION: My Project Rules -->`
- Preserves exact content (no whitespace changes, no reformatting)
- Stores in data structure for merge algorithm
**And** parser report shows: "Detected 8 user sections (total 450 lines) - will preserve"
**And** validation: `diff user-sections-extracted.md user-original.md` shows 0 content differences (only metadata markers added)

---

### 3. [ ] Intelligent Merge Algorithm Combines Framework + User Sections

**Given** framework template has 30 sections (Critical Rules, Workflows, Commands, etc.) and user has 8 custom sections
**When** the merge algorithm executes with strategy "preserve_user_append_framework"
**Then** the merged CLAUDE.md structure is:
```markdown
# CLAUDE.md

<!-- USER'S ORIGINAL INSTRUCTIONS -->
## My Project Rules
[User content preserved]

## API Keys Location
[User content preserved]

[... 6 more user sections]

---

<!-- DEVFORGEAI FRAMEWORK (AUTO-GENERATED 2025-11-17) -->
<!-- Version: 1.0.1 -->

## DevForgeAI Framework Configuration

### Python Environment (AUTO-DETECTED)
- Version: Python 3.10.11
- Path: /usr/bin/python3

[30 framework sections follow]
```
**And** section count: 8 user + 30 framework = 38 total sections
**And** user sections appear first (priority over framework)
**And** framework sections clearly marked with generation date and version
**And** total file size: User original + framework template ≈ 1,500-2,000 lines

---

### 4. [ ] Conflict Detection and User-Driven Resolution

**Given** user's CLAUDE.md has section "## Critical Rules" and framework template also has "## Critical Rules"
**When** merge algorithm detects overlapping section names
**Then** conflict resolution activates:
- Conflict detected: Section "Critical Rules" exists in both
- Installer pauses deployment
- Shows user diff:
  ```
  YOUR VERSION (50 lines):
  ## Critical Rules
  1. Never commit .env files
  2. Always use TypeScript strict mode
  [... 48 more lines]

  DEVFORGEAI VERSION (200 lines):
  ## Critical Rules
  1. Technology Decisions - Always check tech-stack.md
  2. File Operations - Use native tools (Read, not cat)
  [... 198 more lines]
  ```
- Prompts user via interactive question:
  - Option 1: "Keep mine, add DevForgeAI as subsection (## DevForgeAI Critical Rules)"
  - Option 2: "Use DevForgeAI, move mine to 'Original Instructions' section"
  - Option 3: "Merge both (I want all rules from both sources)"
  - Option 4: "Manual (I'll edit CLAUDE.md myself after installation)"
**And** user selection applied consistently to all conflicts (if 3 conflicts detected, same strategy for all)
**And** conflict resolution logged in `merge-report.md` (which sections conflicted, how resolved)

---

### 5. [ ] Merge Tested on 5 Representative CLAUDE.md Scenarios

**Given** real-world projects have varying CLAUDE.md complexity
**When** I test merge logic on 5 test fixtures
**Then** all fixtures merge successfully without data loss:

**Fixture 1: Minimal CLAUDE.md** (empty or 10 lines of basic instructions)
- Merge result: Framework template added in full, user content preserved
- Validation: User lines present, framework sections complete
- Expected conflicts: 0

**Fixture 2: Complex CLAUDE.md** (500+ lines with many custom sections)
- Merge result: User sections preserved, framework sections appended
- Validation: All user sections intact, framework sections added
- Expected conflicts: 2-3 (common section names like "Commands")

**Fixture 3: Conflicting Sections** (user has "## Critical Rules", "## Commands")
- Merge result: Conflict resolution activated for 2 sections
- Validation: User chose "Keep mine + subsection", both contents present
- Expected conflicts: 2 (resolved via user selection)

**Fixture 4: Previous DevForgeAI Installation** (CLAUDE.md has old framework sections from v0.9)
- Merge result: Old framework sections replaced with v1.0.1 sections, user sections preserved
- Validation: Framework updated to latest, user customizations intact
- Expected conflicts: 0 (framework sections auto-replace)

**Fixture 5: Custom Variables** (user has {{MY_VAR}} placeholders)
- Merge result: User variables preserved (not substituted), framework variables substituted
- Validation: User {{MY_VAR}} unchanged, framework {{PROJECT_NAME}} substituted
- Expected conflicts: 0

**And** merge success rate: 5/5 (100%)
**And** data loss detection: 0 user lines lost across all 5 fixtures
**And** each fixture generates merge-report.md with diff summary

---

### 6. [ ] Merged CLAUDE.md Validates Against Framework Requirements

**Given** the merge produced a final CLAUDE.md combining user + framework content
**When** I run validation checks on the merged file
**Then** all framework requirements are met:
- Contains "## Core Philosophy" section (framework philosophy present)
- Contains "## Critical Rules" section or subsection (11 rules documented)
- Contains "## Quick Reference - Progressive Disclosure" with 21 @file references
- Contains "## Development Workflow Overview" (7-step lifecycle)
- Contains Python environment detection ({{PYTHON_VERSION}} substituted)
- Framework sections total ≥ 800 lines (complete framework content)
- User sections preserved (no deletions from user original)
- No unsubstituted variables (grep for `{{[A-Z_]+}}` returns 0 matches except user's custom vars)
**And** validation report: "✅ Framework sections complete, ✅ User sections preserved, ✅ Variables substituted"

---

### 7. [ ] User Review and Approval Workflow Before Finalization

**Given** merge algorithm has produced candidate CLAUDE.md
**When** installer enters approval phase
**Then** user review workflow activates:
- Backup original CLAUDE.md: `CLAUDE.md.pre-merge-backup-{timestamp}`
- Generate diff: `diff -u CLAUDE.md CLAUDE.md.candidate > merge-diff.txt`
- Display diff summary:
  - Lines added: 800 (framework sections)
  - Lines deleted: 0 (user content preserved)
  - Lines modified: 5 (variable substitutions)
  - Conflicts resolved: 2 (via user selection in AC4)
- Prompt user:
  - Option 1: "Approve merge (apply changes to CLAUDE.md)"
  - Option 2: "Review diff first (open merge-diff.txt, then approve/reject)"
  - Option 3: "Reject merge (keep original CLAUDE.md, skip framework injection)"
  - Option 4: "Manual merge (I'll edit candidate file myself)"
**And** if user approves: CLAUDE.md replaced with candidate, backup kept
**And** if user rejects: Candidate deleted, original preserved, installation continues without CLAUDE.md update
**And** approval decision logged in installation report

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Worker"
      name: "TemplateVariableDetector"
      file_path: "installer/template_vars.py"
      requirements:
        - id: "WKR-001"
          description: "Detect all {{VARIABLE}} patterns in src/CLAUDE.md template"
          testable: true
          test_requirement: "Test: Regex finds 7 framework variables, 0 false positives"
          priority: "High"

        - id: "WKR-002"
          description: "Auto-detect PROJECT_NAME from git remote or directory name"
          testable: true
          test_requirement: "Test: Git repo with remote returns repo name, no git returns dirname"
          priority: "Medium"

        - id: "WKR-003"
          description: "Auto-detect PYTHON_VERSION and PYTHON_PATH from system"
          testable: true
          test_requirement: "Test: subprocess.run(['python3', '--version']) captures version string"
          priority: "High"

        - id: "WKR-004"
          description: "Auto-detect TECH_STACK from package managers (package.json, requirements.txt, *.csproj)"
          testable: true
          test_requirement: "Test: Project with package.json returns 'Node.js', with requirements.txt returns 'Python'"
          priority: "Medium"

        - id: "WKR-005"
          description: "Substitute all variables in template content"
          testable: true
          test_requirement: "Test: substitute_variables(template, vars) replaces all 7 {{VAR}} patterns"
          priority: "Critical"

    - type: "Worker"
      name: "CLAUDEmdParser"
      file_path: "installer/claude_parser.py"
      requirements:
        - id: "WKR-006"
          description: "Parse markdown into sections using regex for ## headers"
          testable: true
          test_requirement: "Test: Parse test CLAUDE.md with 10 sections, extract all 10 with content"
          priority: "Critical"

        - id: "WKR-007"
          description: "Detect section nesting levels (##, ###, ####)"
          testable: true
          test_requirement: "Test: Nested sections preserve hierarchy (parent → children)"
          priority: "High"

        - id: "WKR-008"
          description: "Extract user sections (not part of previous DevForgeAI installation)"
          testable: true
          test_requirement: "Test: Parse CLAUDE.md with 'USER_SECTION' markers, extract correctly"
          priority: "High"

        - id: "WKR-009"
          description: "Preserve exact content (no whitespace normalization, no line ending changes)"
          testable: true
          test_requirement: "Test: Extracted section content byte-identical to original"
          priority: "High"

    - type: "Worker"
      name: "MergeAlgorithm"
      file_path: "installer/merge.py"
      requirements:
        - id: "WKR-010"
          description: "Implement preserve_user_append_framework merge strategy"
          testable: true
          test_requirement: "Test: User sections appear first, framework sections follow"
          priority: "Critical"

        - id: "WKR-011"
          description: "Detect section name conflicts (same ## header in both files)"
          testable: true
          test_requirement: "Test: Template has '## Commands', user has '## Commands', conflict detected"
          priority: "Critical"

        - id: "WKR-012"
          description: "Resolve conflicts based on user-selected strategy"
          testable: true
          test_requirement: "Test: User selects 'keep mine + subsection', verify ## Commands → ## DevForgeAI Commands"
          priority: "Critical"

        - id: "WKR-013"
          description: "Mark framework sections with generation metadata"
          testable: true
          test_requirement: "Test: Framework sections have <!-- DEVFORGEAI (2025-11-17) --> marker"
          priority: "Medium"

    - type: "Configuration"
      name: "MergeConfig"
      file_path: "installer/merge-config.yaml"
      requirements:
        - id: "CONF-001"
          description: "Define variable substitution patterns and sources"
          testable: true
          test_requirement: "Test: Config lists 7 variables with detection methods"
          priority: "High"

        - id: "CONF-002"
          description: "Define merge strategies (preserve_user_append_framework, replace_all, manual)"
          testable: true
          test_requirement: "Test: Config has 'strategies' array with 3 options"
          priority: "Medium"

        - id: "CONF-003"
          description: "Define conflict resolution options (keep_user, use_framework, merge_both, manual)"
          testable: true
          test_requirement: "Test: Config has 'conflict_resolution_options' array with 4 choices"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "User content must NEVER be deleted or overwritten without explicit approval"
      test_requirement: "Test: Merge 5 fixtures, assert 0 user lines deleted (diff shows only additions)"

    - id: "BR-002"
      rule: "All framework sections must be present in merged result (completeness check)"
      test_requirement: "Test: Merged CLAUDE.md contains all 30 framework sections (grep count)"

    - id: "BR-003"
      rule: "Variables must be substituted before showing user preview (no {{VAR}} in diff)"
      test_requirement: "Test: Diff shown to user has no {{VAR}} patterns (all substituted)"

    - id: "BR-004"
      rule: "User must approve merge before CLAUDE.md is modified (explicit consent)"
      test_requirement: "Test: Without user approval, original CLAUDE.md unchanged"

    - id: "BR-005"
      rule: "Backup created before merge (CLAUDE.md.pre-merge-backup-{timestamp})"
      test_requirement: "Test: Backup file exists with identical content to original"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Template parsing and merge execution fast"
      metric: "< 5 seconds for CLAUDE.md merge (parse + substitute + merge + diff)"
      test_requirement: "Test: time merge_claude_md(), assert <5s"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Variable detection efficient (no expensive system calls)"
      metric: "< 2 seconds for all 7 variable detections"
      test_requirement: "Test: time detect_project_variables(), assert <2s"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Merge algorithm handles malformed markdown gracefully"
      metric: "0 crashes on invalid input (missing headers, unclosed code blocks)"
      test_requirement: "Test: Parse broken markdown, verify parser doesn't crash"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Rollback available if user rejects merge"
      metric: "100% restoration to pre-merge state (backup restoration)"
      test_requirement: "Test: Reject merge, verify CLAUDE.md unchanged (checksum matches pre-merge)"

    - id: "NFR-005"
      category: "Usability"
      requirement: "Diff preview clear and actionable"
      metric: "Diff shows additions (green), deletions (red), with line numbers"
      test_requirement: "Test: Diff format matches 'diff -u' output (standard format)"

    - id: "NFR-006"
      category: "Usability"
      requirement: "Conflict resolution options clear with examples"
      metric: "Each option shows before/after preview (what result will look like)"
      test_requirement: "Test: User prompt includes example for each of 4 resolution options"
```

### Dependencies

**External:**
- Python 3.8+ with re (regex), pathlib, git
- diff utility (for generating diffs)
- Markdown parsing library (optional, can use regex)

**Internal:**
- STORY-045 complete (installer core must exist to integrate merge logic)

---

## Edge Cases

### 1. User CLAUDE.md Has Nested DevForgeAI Sections from Previous Install
**Scenario:** CLAUDE.md already has `<!-- DEVFORGEAI -->` marker from v0.9 installation
**Expected:** Parser detects old framework sections, removes them before merge, replaces with v1.0.1 sections
**Handling:** Search for `<!-- DEVFORGEAI -->` marker, extract and remove everything after marker, append new framework sections

### 2. User CLAUDE.md Contains {{CUSTOM_VAR}} Placeholders
**Scenario:** User uses their own template variables like {{API_ENDPOINT}}
**Expected:** Merge preserves user variables (only substitute framework {{VAR}} patterns)
**Handling:** Variable substitution only operates on 7 known framework variables, user variables left as-is

### 3. Merge Produces Very Large CLAUDE.md (>3,000 Lines)
**Scenario:** User has 2,000 lines of custom content + 1,061 lines of framework = 3,061 lines
**Expected:** Installer warns: "Merged CLAUDE.md is large (3,061 lines). Consider moving some content to separate docs."
**Handling:** Display warning (non-blocking), continue with merge, suggest optimization

### 4. User Rejects Merge Multiple Times (Iterative Refinement)
**Scenario:** User reviews diff, rejects, edits candidate manually, re-runs installer
**Expected:** Installer detects candidate file exists, offers: "(1) Use existing candidate, (2) Regenerate from template"
**Handling:** Check for CLAUDE.md.candidate file, prompt user, apply selection

### 5. Framework Template Updated Between Attempts
**Scenario:** User rejects merge, framework team pushes v1.0.2, user retries installation
**Expected:** Installer re-reads src/CLAUDE.md (gets v1.0.2 template), regenerates merge with new content
**Handling:** Always read src/CLAUDE.md fresh (no caching), version in merge metadata updated

### 6. Encoding Issues (UTF-8 vs ASCII)
**Scenario:** User CLAUDE.md has UTF-8 emoji (🚀), framework template is ASCII
**Expected:** Merge preserves UTF-8 encoding, resulting file is UTF-8
**Handling:** Open files with `encoding='utf-8'`, write with same encoding

### 7. Line Ending Differences (LF vs CRLF)
**Scenario:** Windows user has CRLF, framework template has LF
**Expected:** Merge normalizes to user's line ending style (preserve CRLF if that's what they use)
**Handling:** Detect line endings in user file, apply same to merged result

---

## Data Validation Rules

1. **Variable pattern:** Must match `{{[A-Z_]+}}` (uppercase, underscores only)

2. **Section header:** Must match `^#{2,4} ` (2-4 hashes + space)

3. **Substitution completeness:** Zero unsubstituted framework variables in final result

4. **User content integrity:** 100% of user lines present in merged result (no deletions)

5. **Framework completeness:** All 30 framework sections present in merged result

6. **Conflict detection accuracy:** All duplicate section names detected (precision: 100%)

7. **Backup validation:** Backup file byte-identical to pre-merge original (checksum match)

---

## Non-Functional Requirements

### Performance
- Template parsing: <2 seconds
- Variable substitution: <2 seconds
- Merge algorithm: <5 seconds total
- Diff generation: <3 seconds

### Reliability
- No data loss: 100% user content preserved
- Conflict detection: 100% accuracy
- Backup safety: Always created before changes
- Rollback capability: 100% restoration

### Usability
- Clear diff preview: Color-coded if terminal supports
- Interactive prompts: Clear options with examples
- Progress updates: Show current step (1/5, 2/5, etc.)
- Error messages: Actionable fix suggestions

---

## Definition of Done

### Implementation
- [ ] installer/template_vars.py created (variable detection and substitution)
- [ ] installer/claude_parser.py created (markdown section parsing)
- [ ] installer/merge.py created (merge algorithm with strategies)
- [ ] installer/merge-config.yaml created (configuration)
- [ ] Merge integrated into installer/install.py (called during deployment)
- [ ] 5 test fixtures created (minimal, complex, conflicting, previous-install, custom-vars)
- [ ] Conflict resolution UI implemented (interactive prompts)
- [ ] User approval workflow implemented (diff preview + approval)

### Quality
- [ ] All 7 acceptance criteria validated with fixtures
- [ ] All 5 business rules enforced
- [ ] All 6 NFRs met and measured
- [ ] All 7 edge cases handled
- [ ] Zero data loss in all 5 test fixtures
- [ ] 100% conflict detection accuracy

### Testing
- [ ] Unit tests: Variable detection (7 variables)
- [ ] Unit tests: Parsing (5 markdown structures)
- [ ] Unit tests: Merge strategies (3 strategies)
- [ ] Unit tests: Conflict resolution (4 resolution types)
- [ ] Integration tests: 5 fixtures (all scenarios)
- [ ] Regression test: Merge doesn't break existing CLAUDE.md functionality

### Documentation
- [ ] Merge algorithm documented (installer/MERGE-ALGORITHM.md)
- [ ] Variable substitution guide (which variables, how detected)
- [ ] Conflict resolution guide (4 strategies explained)
- [ ] Test fixture documentation (what each tests)
- [ ] EPIC-009 updated (Phase 6 complete)

### Release Readiness
- [ ] Git commit with merge logic
- [ ] Tested on 5 diverse CLAUDE.md files
- [ ] Zero data loss validated (100% user content preserved)
- [ ] Ready for STORY-047 (external project testing)

---

## Workflow History

- **2025-11-16:** Story created for EPIC-009 Phase 6 (CLAUDE.md merge logic)
- **2025-11-16:** Priority: High, Points: 13 (complex merge with conflict resolution)
- **2025-11-16:** Depends on STORY-045 (installer core must exist)
- **2025-11-16:** Blocks STORY-047 (external testing needs complete installer)
- **2025-11-16:** HIGH RISK: User data loss potential, requires extensive testing
- **2025-11-16:** Status: Backlog (awaiting STORY-045 completion)
