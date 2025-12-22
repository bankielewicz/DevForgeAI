---
id: STORY-142
title: Replace Bash mkdir with Write/.gitkeep Pattern
epic: EPIC-030
sprint: Backlog
status: Backlog
points: 3
depends_on: []
priority: High
assigned_to: TBD
created: 2025-12-22
format_version: "2.3"
---

# Story: Replace Bash mkdir with Write/.gitkeep Pattern

## Description

**As a** framework maintainer,
**I want** to replace all Bash mkdir commands with Write/.gitkeep pattern calls in ideation files,
**so that** constitutional compliance is achieved and the framework consistently uses native tools instead of Bash for file operations.

## Acceptance Criteria

### AC#1: Replace mkdir in artifact-generation.md

**Given** artifact-generation.md contains Bash(command="mkdir -p ...") calls,
**When** all mkdir commands are replaced with Write(file_path=".../.gitkeep", content=""),
**Then** the file contains zero Bash mkdir invocations and uses Write tool instead for directory creation.

---

### AC#2: Validation confirms zero Bash mkdir in ideation files

**Given** ideation-related files have been updated,
**When** grep search is executed for pattern `Bash.*mkdir` across all ideation skill files,
**Then** the search returns zero matches in:
- .claude/commands/ideate.md
- .claude/skills/devforgeai-ideation/SKILL.md
- .claude/skills/devforgeai-ideation/references/artifact-generation.md

---

### AC#3: Directory structure created with .gitkeep patterns

**Given** Write tool is invoked with file_path="devforgeai/specs/Epics/.gitkeep" and content="",
**When** the Write operation completes successfully,
**Then** the target directory exists with .gitkeep file present, allowing version control tracking without dummy content.

---

### AC#4: Framework constitutional compliance passes

**Given** all C1 violations related to Bash file operations have been addressed,
**When** context-validator runs its constitutional compliance checks,
**Then** zero C1 violations are reported for ideation-related files.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    command_file: ".claude/commands/ideate.md"
    artifact_generation: ".claude/skills/devforgeai-ideation/references/artifact-generation.md"
    error_handling: ".claude/skills/devforgeai-ideation/references/error-handling.md"
    tech_stack: "devforgeai/specs/context/tech-stack.md"

  verified_violations:
    description: "Bash mkdir violations found during story creation (2025-12-22)"
    locations:
      - file: ".claude/skills/devforgeai-ideation/references/artifact-generation.md"
        lines: [469, 598, 599]
        count: 3
      - file: ".claude/skills/devforgeai-ideation/references/error-handling.md"
        lines: [184, 868]
        count: 2
      - file: ".claude/commands/ideate.md"
        count: 0
        note: "No violations found"
      - file: ".claude/skills/devforgeai-ideation/SKILL.md"
        count: 0
        note: "No violations found (only in backup files)"
    total_violations: 5

  components:
    - type: "Configuration"
      name: "artifact-generation.md"
      file_path: ".claude/skills/devforgeai-ideation/references/artifact-generation.md"
      requirements:
        - id: "CFG-001"
          description: "Replace 3 Bash mkdir commands (lines 469, 598, 599) with Write/.gitkeep pattern"
          testable: true
          test_requirement: "Test: Grep for 'Bash.*mkdir' returns zero matches"
          priority: "Critical"

    - type: "Configuration"
      name: "error-handling.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-handling.md"
      requirements:
        - id: "CFG-002"
          description: "Replace 2 Bash mkdir commands (lines 184, 868) with Write/.gitkeep pattern"
          testable: true
          test_requirement: "Test: Grep for 'Bash.*mkdir' returns zero matches"
          priority: "Critical"

    - type: "Configuration"
      name: "ideate.md"
      file_path: ".claude/commands/ideate.md"
      requirements:
        - id: "CFG-003"
          description: "Verify no Bash mkdir commands exist (none found during story creation)"
          testable: true
          test_requirement: "Test: Grep for 'Bash.*mkdir' returns zero matches"
          priority: "Low"

    - type: "Configuration"
      name: "SKILL.md"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      requirements:
        - id: "CFG-004"
          description: "Verify no Bash mkdir commands exist (none found during story creation)"
          testable: true
          test_requirement: "Test: Grep for 'Bash.*mkdir' returns zero matches"
          priority: "Low"

  business_rules:
    - id: "BR-001"
      rule: "Native Write tool must be used for directory creation instead of Bash"
      test_requirement: "Test: Validate no Bash file operations in ideation files"

    - id: "BR-002"
      rule: ".gitkeep files must have empty content (content='')"
      test_requirement: "Test: All Write/.gitkeep calls use content=''"

    - id: "BR-003"
      rule: "Directory creation pattern must be idempotent"
      test_requirement: "Test: Multiple Write calls to same .gitkeep path succeed without error"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Write operation completion time"
      metric: "< 50ms per .gitkeep file (p99)"
      test_requirement: "Test: Measure Write operation execution time"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Write operations must be idempotent"
      metric: "100% success rate on repeated calls"
      test_requirement: "Test: Multiple calls produce identical results without errors"

    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Pattern clarity and reusability"
      metric: "Zero Bash fallback code paths remain"
      test_requirement: "Test: Grep confirms no Bash mkdir alternatives exist"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **Directory already exists during replacement:** When the mkdir target directory already exists, Write(.gitkeep) should still succeed without error. Verify that the updated code handles pre-existing directories gracefully.

2. **Nested directory structure requirements:** If artifact generation requires creating multiple nested directories (e.g., devforgeai/specs/Epics/subdir/.gitkeep), ensure all parent directories are implicitly created by the Write tool or explicitly created via separate Write calls to .gitkeep files.

3. **File permissions and write failures:** If the Write operation fails due to permissions, the error handling must provide clear diagnostic information indicating which path failed and why, rather than silently continuing.

4. **Existing .gitkeep file conflicts:** If a .gitkeep file already exists in the target directory, the Write operation should overwrite it (since .gitkeep is always empty) without warnings.

## Data Validation Rules

1. **File path format:** All file_path parameters must be valid relative paths (e.g., "devforgeai/specs/Epics/.gitkeep"), properly formatted with forward slashes, and must target the .gitkeep file within the desired directory structure.

2. **.gitkeep content:** Content parameter must be an empty string ("") for all .gitkeep Write operations. No whitespace, no comments, no placeholder text.

3. **Bash pattern matching:** Grep validation must use pattern `Bash.*mkdir` (case-sensitive) to detect violations. Zero matches required for compliance.

4. **File scope:** Replacements must be limited to these three files:
   - .claude/commands/ideate.md
   - .claude/skills/devforgeai-ideation/SKILL.md
   - .claude/skills/devforgeai-ideation/references/artifact-generation.md

## Non-Functional Requirements

### Performance
- Write operation completion: < 50ms per .gitkeep file (p99)
- Grep validation scan: < 1 second for all three ideation files combined
- No degradation to overall ideation skill performance after changes

### Security
- File paths must not allow directory traversal (validate no "../" patterns)
- Write operations must execute with caller's existing file permissions (no privilege elevation)
- No temporary files or side effects during directory creation

### Reliability
- Write operations are idempotent: calling multiple times with same path/content produces identical result
- Failure handling: If Write fails, error message must clearly indicate which file path failed and root cause
- No partial directory structures (either full directory tree exists or operation fails cleanly)

### Maintainability
- Code pattern is clear and reusable: developers understand Write(.gitkeep) pattern for future directory creation
- No Bash fallback code paths remain (eliminates maintenance burden of Bash+Write inconsistency)
- Pattern is documented in artifact-generation.md reference file for consistency across ideation workflows

### Compliance
- Constitutional validator confirms zero C1 violations after changes
- Tech-stack.md guidelines enforced: native Write tool required over Bash for file operations
- All three ideation files pass compliance scanning before merge

## UI Specification

N/A - This story modifies framework documentation files only. No user interface changes required.

## Definition of Done

### Implementation
- [ ] All Bash mkdir commands identified in ideation files
- [ ] ideate.md updated: Bash mkdir replaced with Write/.gitkeep
- [ ] SKILL.md updated: Bash mkdir replaced with Write/.gitkeep
- [ ] artifact-generation.md updated: Bash mkdir replaced with Write/.gitkeep
- [ ] Code follows established patterns from tech-stack.md

### Quality
- [ ] Grep validation: Zero matches for `Bash.*mkdir` in all three files
- [ ] Write/.gitkeep pattern tested and working
- [ ] No regressions in ideation skill functionality
- [ ] Code review completed

### Testing
- [ ] Manual test: Run ideation workflow with new pattern
- [ ] Validation test: Grep confirms zero Bash mkdir violations
- [ ] Directory creation test: .gitkeep files created successfully

### Documentation
- [ ] Pattern documented in artifact-generation.md reference file
- [ ] Story file updated with implementation notes

## Implementation Notes

*To be filled during development*

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Acceptance Criteria Verification Checklist

### AC#1: Replace mkdir in artifact-generation.md
- [ ] Identified all Bash mkdir calls in artifact-generation.md
- [ ] Replaced each with Write(file_path=".../.gitkeep", content="")
- [ ] Verified zero Bash mkdir calls remain

### AC#2: Validation confirms zero Bash mkdir in ideation files
- [ ] Ran Grep for `Bash.*mkdir` in ideate.md - zero matches
- [ ] Ran Grep for `Bash.*mkdir` in SKILL.md - zero matches
- [ ] Ran Grep for `Bash.*mkdir` in artifact-generation.md - zero matches

### AC#3: Directory structure created with .gitkeep patterns
- [ ] Write tool successfully creates .gitkeep file
- [ ] Parent directories created automatically (if Write tool supports)
- [ ] .gitkeep file content is empty string

### AC#4: Framework constitutional compliance passes
- [ ] context-validator reports zero C1 violations for ideation files
- [ ] Constitutional compliance check passes
