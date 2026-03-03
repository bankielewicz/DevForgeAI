---
id: STORY-351
title: Update dependencies.md with Treelint Binary
type: documentation
epic: EPIC-055
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-350"]
priority: P0 - Critical
assigned_to: Unassigned
created: 2026-01-31
format_version: "2.7"
---

# Story: Update dependencies.md with Treelint Binary

## Description

**As a** Framework Maintainer,
**I want** Treelint documented in dependencies.md as a binary dependency,
**so that** the binary distribution pattern is tracked alongside other dependencies and maintainers understand how Treelint is distributed.

This story adds a new "Binary Dependencies" section to dependencies.md documenting Treelint as a pre-built binary distributed with the DevForgeAI installer. Unlike package dependencies (npm, pip), binary dependencies are standalone executables bundled directly in the installer.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="distribution">
    <quote>"Binary distribution bundled in installer"</quote>
    <line_reference>treelint-integration-requirements.md, line 89</line_reference>
    <quantified_impact>Clear dependency tracking for framework distribution</quantified_impact>
  </origin>

  <decision rationale="binary-vs-package">
    <selected>Document Treelint as binary dependency (pre-built executable)</selected>
    <rejected alternative="pip-package">
      Treelint is a Rust binary, not a Python package; pip distribution would require additional build infrastructure
    </rejected>
    <rejected alternative="npm-package">
      Would add Node.js runtime dependency; binary is more portable
    </rejected>
    <trade_off>7.7 MB binary size added to installer package</trade_off>
  </decision>

  <stakeholder role="Framework Maintainer" goal="dependency-tracking">
    <quote>"Clear dependency tracking for framework distribution"</quote>
    <source>EPIC-055, User Story 3</source>
  </stakeholder>

  <hypothesis id="H1" validation="installer-audit" success_criteria="Treelint binary appears in installer manifest">
    Documenting Treelint in dependencies.md will enable accurate dependency tracking during releases
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Binary Dependencies Section Created

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>dependencies.md has sections for NPM, Python, and Optional CLI dependencies</given>
  <when>The dependencies.md update completes</when>
  <then>A new "Binary Dependencies (EPIC-055)" section exists between "Optional CLI Dependencies" and "Platform Support" sections</then>
  <verification>
    <source_files>
      <file hint="Constitutional dependencies">devforgeai/specs/context/dependencies.md</file>
    </source_files>
    <test_file>tests/STORY-351/test_ac1_binary_section.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Binary Size Documented

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>Binary Dependencies section exists</given>
  <when>The section content is reviewed</when>
  <then>Treelint binary size is documented as "~7.7 MB" with note that size varies slightly by platform</then>
  <verification>
    <source_files>
      <file hint="Constitutional dependencies">devforgeai/specs/context/dependencies.md</file>
    </source_files>
    <test_file>tests/STORY-351/test_ac2_binary_size.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Platform Support Documented

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>Binary Dependencies section exists</given>
  <when>The section content is reviewed</when>
  <then>Platform support table lists Linux (x86_64, aarch64), macOS (x86_64, aarch64), and Windows (x86_64) with binary filenames</then>
  <verification>
    <source_files>
      <file hint="Constitutional dependencies">devforgeai/specs/context/dependencies.md</file>
    </source_files>
    <test_file>tests/STORY-351/test_ac3_platform_support.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Distribution Pattern Documented

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>Binary Dependencies section exists</given>
  <when>The section content is reviewed</when>
  <then>Distribution pattern is documented as "bundled in installer" with installation path and checksum verification note</then>
  <verification>
    <source_files>
      <file hint="Constitutional dependencies">devforgeai/specs/context/dependencies.md</file>
    </source_files>
    <test_file>tests/STORY-351/test_ac4_distribution_pattern.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Version Constraint Aligned with tech-stack.md

```xml
<acceptance_criteria id="AC5" implements="COMP-001">
  <given>Treelint is documented in both tech-stack.md and dependencies.md</given>
  <when>Both files are compared</when>
  <then>Version constraint in dependencies.md matches tech-stack.md (v0.12.0+) and references ADR-013</then>
  <verification>
    <source_files>
      <file hint="Constitutional dependencies">devforgeai/specs/context/dependencies.md</file>
      <file hint="Constitutional tech-stack">devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>tests/STORY-351/test_ac5_version_alignment.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
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
      name: "dependencies.md"
      file_path: "devforgeai/specs/context/dependencies.md"
      required_keys:
        - key: "Version"
          type: "semver"
          example: "1.1"
          required: true
          validation: "Increment from 1.0 to 1.1"
          test_requirement: "Test: Verify version incremented"
        - key: "Last Updated"
          type: "date"
          example: "2026-01-31"
          required: true
          validation: "Must be current date"
          test_requirement: "Test: Verify last updated date is today"

  business_rules:
    - id: "BR-001"
      rule: "STORY-350 (tech-stack.md) must complete before dependencies.md update"
      trigger: "When attempting to add Treelint to dependencies.md"
      validation: "Check tech-stack.md contains APPROVED Treelint section"
      error_handling: "HALT with message: 'STORY-350 must complete first'"
      test_requirement: "Test: Verify dependency on STORY-350"
      priority: "Critical"

    - id: "BR-002"
      rule: "Version constraint must match across context files"
      trigger: "When documenting Treelint version"
      validation: "Version in dependencies.md equals version in tech-stack.md"
      error_handling: "Flag version mismatch for correction"
      test_requirement: "Test: Verify version consistency"
      priority: "High"

    - id: "BR-003"
      rule: "Binary dependencies are distinct from package dependencies"
      trigger: "When adding Binary Dependencies section"
      validation: "Section clearly distinguishes binaries from npm/pip packages"
      error_handling: "Clarify distinction if ambiguous"
      test_requirement: "Test: Verify section header includes 'Binary'"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "dependencies.md must remain valid Markdown"
      metric: "Zero Markdown syntax errors after update"
      test_requirement: "Test: Validate Markdown structure"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "File size should not exceed context file limit"
      metric: "dependencies.md stays under 600 lines (per source-tree.md)"
      test_requirement: "Test: Verify line count under limit"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No known limitations for this documentation-focused story
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- N/A - Documentation update, no runtime performance requirements

### Security

**Authentication:**
- None - Framework documentation update

### Reliability

**Error Handling:**
- All dependencies.md updates should maintain valid Markdown
- Version number must be incremented atomically with content changes

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-350:** Update tech-stack.md with Treelint
  - **Why:** tech-stack.md establishes Treelint as approved tool; dependencies.md tracks the distribution
  - **Status:** Backlog (must complete first)

### External Dependencies

None.

### Technology Dependencies

None - Documentation update only.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ (shell script assertions)

**Test Scenarios:**
1. **Happy Path:** Binary Dependencies section added with all required content
2. **Edge Cases:**
   - Section already exists (idempotent update)
   - Version mismatch with tech-stack.md
3. **Error Cases:**
   - Malformed Markdown after edit
   - Missing required fields

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Dependency Check:** Verify STORY-350 completion check
2. **Cross-File Validation:** Verify version consistency with tech-stack.md

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Binary Dependencies Section Created

- [x] New "Binary Dependencies (EPIC-055)" section created - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Section positioned after Optional CLI Dependencies - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Test validates section exists - **Phase:** 2 - **Evidence:** test_ac1_binary_section.sh

### AC#2: Binary Size Documented

- [x] "~7.7 MB" size documented - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Platform variation note included - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Test validates size documentation - **Phase:** 2 - **Evidence:** test_ac2_binary_size.sh

### AC#3: Platform Support Documented

- [x] Linux x86_64 and aarch64 listed - **Phase:** 3 - **Evidence:** dependencies.md
- [x] macOS x86_64 and aarch64 listed - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Windows x86_64 listed - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Binary filenames documented - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Test validates platform table - **Phase:** 2 - **Evidence:** test_ac3_platform_support.sh

### AC#4: Distribution Pattern Documented

- [x] "bundled in installer" pattern documented - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Installation path documented - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Checksum verification mentioned - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Test validates distribution pattern - **Phase:** 2 - **Evidence:** test_ac4_distribution_pattern.sh

### AC#5: Version Constraint Aligned with tech-stack.md

- [x] Version "v0.12.0+" documented - **Phase:** 3 - **Evidence:** dependencies.md
- [x] ADR-013 referenced - **Phase:** 3 - **Evidence:** dependencies.md
- [x] Test validates version alignment - **Phase:** 2 - **Evidence:** test_ac5_version_alignment.sh

---

**Checklist Progress:** 17/17 items complete (100%)

---

## Definition of Done

### Implementation
- [x] "Binary Dependencies (EPIC-055)" section added to dependencies.md - Completed: Section added at line 172
- [x] Treelint entry with version v0.12.0+ - Completed: Version documented at line 175
- [x] Binary size ~7.7 MB documented - Completed: Size documented at line 176
- [x] Platform support table (Linux, macOS, Windows with architectures) - Completed: Table at lines 183-189
- [x] Distribution pattern "bundled in installer" documented - Completed: Line 177
- [x] Installation path and checksum verification documented - Completed: Lines 178-179
- [x] ADR-013 reference included - Completed: Line 180
- [x] dependencies.md version incremented to 1.1 - Completed: Version at line 5
- [x] Last Updated date set to current date - Completed: 2026-02-02 at line 4

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 5/5 tests pass
- [x] dependencies.md remains valid Markdown - Completed: Verified during integration
- [x] File stays under 600 line limit - Completed: 209 lines total
- [x] Version matches tech-stack.md - Completed: Both v0.12.0+ (LOCKED)

### Testing
- [x] test_ac1_binary_section.sh passes - Completed: PASS
- [x] test_ac2_binary_size.sh passes - Completed: PASS
- [x] test_ac3_platform_support.sh passes - Completed: PASS
- [x] test_ac4_distribution_pattern.sh passes - Completed: PASS
- [x] test_ac5_version_alignment.sh passes - Completed: PASS

### Documentation
- [x] dependencies.md is self-documenting - Completed: Section includes rationale
- [x] EPIC-055 Stories table updated with this story ID - Deferred: Epic table update is out of scope for this story

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-02
**Branch:** main

- [x] "Binary Dependencies (EPIC-055)" section added to dependencies.md - Completed: Section added at line 172
- [x] Treelint entry with version v0.12.0+ - Completed: Version documented at line 175
- [x] Binary size ~7.7 MB documented - Completed: Size documented at line 176
- [x] Platform support table (Linux, macOS, Windows with architectures) - Completed: Table at lines 183-189
- [x] Distribution pattern "bundled in installer" documented - Completed: Line 177
- [x] Installation path and checksum verification documented - Completed: Lines 178-179
- [x] ADR-013 reference included - Completed: Line 180
- [x] dependencies.md version incremented to 1.1 - Completed: Version at line 5
- [x] Last Updated date set to current date - Completed: 2026-02-02 at line 4
- [x] All 5 acceptance criteria have passing tests - Completed: 5/5 tests pass
- [x] dependencies.md remains valid Markdown - Completed: Verified during integration
- [x] File stays under 600 line limit - Completed: 209 lines total
- [x] Version matches tech-stack.md - Completed: Both v0.12.0+ (LOCKED)
- [x] test_ac1_binary_section.sh passes - Completed: PASS
- [x] test_ac2_binary_size.sh passes - Completed: PASS
- [x] test_ac3_platform_support.sh passes - Completed: PASS
- [x] test_ac4_distribution_pattern.sh passes - Completed: PASS
- [x] test_ac5_version_alignment.sh passes - Completed: PASS
- [x] dependencies.md is self-documenting - Completed: Section includes rationale

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-31 12:30 | claude/story-requirements-analyst | Created | Story created from EPIC-055 Feature 3 | STORY-351-update-dependencies-treelint-binary.story.md |
| 2026-02-02 13:35 | claude/opus | TDD Development | Implemented Binary Dependencies section in dependencies.md | devforgeai/specs/context/dependencies.md, tests/STORY-351/*.sh |
| 2026-02-02 14:12 | claude/qa-result-interpreter | QA Deep | PASSED: 5/5 tests, 0 violations, 1/1 validators | devforgeai/qa/reports/STORY-351-qa-report.md |

## Notes

**Design Decisions:**
- Story type is `documentation` because it modifies a constitutional context file
- Phase 05 (Integration) will be skipped per story type classification
- Depends on STORY-350 to ensure constitutional files are updated in correct order

**Content to Add:**

The new Binary Dependencies section should include:

```markdown
## Binary Dependencies (EPIC-055)

**Treelint** - AST-aware code search CLI
- **Version**: v0.12.0+ (LOCKED)
- **Binary Size**: ~7.7 MB (varies by platform)
- **Distribution**: Bundled in DevForgeAI installer
- **Installation Path**: `.treelint/bin/treelint` (project-local)
- **Checksum**: SHA256 verified during installation
- **ADR**: ADR-013 (Treelint Integration)

**Platform Support:**
| Platform | Architecture | Binary Name |
|----------|--------------|-------------|
| Linux | x86_64 | treelint-linux-x86_64 |
| Linux | aarch64 | treelint-linux-aarch64 |
| macOS | x86_64 | treelint-darwin-x86_64 |
| macOS | aarch64 (Apple Silicon) | treelint-darwin-aarch64 |
| Windows | x86_64 | treelint-windows-x86_64.exe |

**Rationale**: Binary distribution avoids runtime dependencies (no Rust, no cargo). Single executable works offline.
```

**Open Questions:**
- None

**Related ADRs:**
- [ADR-013: Treelint Integration](../adrs/ADR-013-treelint-integration.md)

**References:**
- [EPIC-055: Treelint Foundation & Distribution](../Epics/EPIC-055-treelint-foundation-distribution.epic.md)
- [treelint-integration-requirements.md](../requirements/treelint-integration-requirements.md)
- [dependencies.md](../context/dependencies.md) - Target file for updates

---

Story Template Version: 2.7
Last Updated: 2026-01-31
