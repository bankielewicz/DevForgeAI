---
id: STORY-285
title: Register Format Standardization - Technical Debt v2.0
type: feature
epic: EPIC-048
sprint: Backlog
status: QA Approved
points: 4
depends_on: []
priority: High
assigned_to: Unassigned
created: 2026-01-20
format_version: "2.6"
---

# Story: Register Format Standardization - Technical Debt v2.0

## Description

**As a** DevForgeAI framework maintainer,
**I want** to convert the technical-debt-register.md to a standardized YAML frontmatter + structured markdown format with supporting infrastructure,
**so that** debt tracking is machine-parseable for automated analytics, threshold alerting, and integration with /dev and /qa workflows.

**Context:**
This is Feature 1 (FOUNDATION) of EPIC-048 (Technical Debt Register Automation). All subsequent features (Feature 2-6) depend on this standardized format being in place.

## Acceptance Criteria

### AC#1: YAML Frontmatter with Analytics Section

```xml
<acceptance_criteria id="AC1" implements="COMP-001,COMP-002">
  <given>The technical-debt-register.md file exists with the current v1.0 freeform format</given>
  <when>The register is converted to the new format</when>
  <then>The file contains YAML frontmatter with: version (2.0), last_updated (ISO date), analytics section (total_open, total_in_progress, total_resolved, by_type counts, by_priority counts, by_source counts), and thresholds section (warning_count: 5, critical_count: 10, blocking_count: 15, stale_days: 90)</then>
  <verification>
    <source_files>
      <file hint="Updated register">devforgeai/technical-debt-register.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac1_yaml_frontmatter.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Structured Item Format with DEBT-NNN IDs

```xml
<acceptance_criteria id="AC2" implements="COMP-001,COMP-003">
  <given>The register uses YAML frontmatter format from AC1</given>
  <when>A debt item is documented in the register</when>
  <then>Each item follows a structured markdown table format with fields: DEBT-NNN (3-digit zero-padded ID), Date (ISO format), Source (dev_phase_06 or qa_discovery), Type (Story Split, Scope Change, External Blocker), Priority (Critical, High, Medium, Low), Status (Open, In Progress, Resolved), Effort (points or hours), and Follow-up (STORY-XXX or ADR-XXX reference)</then>
  <verification>
    <source_files>
      <file hint="Updated register with items">devforgeai/technical-debt-register.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac2_item_format.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Migration of Existing Format

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>The current register contains 0 active debt items (empty inventory per current state)</given>
  <when>The format migration is complete</when>
  <then>All sections (Open Debt Items, In Progress Debt Items, Resolved Debt Items) use the new structured format, analytics counters are initialized to 0, and the template comment block is updated to show DEBT-NNN format with all required fields</then>
  <verification>
    <source_files>
      <file hint="Migrated register">devforgeai/technical-debt-register.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac3_migration.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Technical-Debt-Analyzer Subagent YAML Parsing Update

```xml
<acceptance_criteria id="AC4" implements="COMP-004">
  <given>The technical-debt-analyzer subagent exists at .claude/agents/technical-debt-analyzer.md</given>
  <when>The subagent is updated for v2.0 format</when>
  <then>Phase 1 (Inventory Technical Debt) includes: YAML frontmatter parsing using Grep patterns for analytics extraction, DEBT-NNN ID pattern matching (regex: DEBT-[0-9]{3}), source field parsing (dev_phase_06 or qa_discovery), and automatic register creation from template if file doesn't exist</then>
  <verification>
    <source_files>
      <file hint="Updated subagent">src/claude/agents/technical-debt-analyzer.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac4_subagent_update.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Source-Tree.md v3.3 Update for Hook Infrastructure

```xml
<acceptance_criteria id="AC5" implements="COMP-005">
  <given>source-tree.md exists at version 3.2</given>
  <when>The file is updated to v3.3</when>
  <then>The file includes: .claude/hooks/ directory entry with naming convention (post-{workflow}-{action}.sh), .claude/skills/devforgeai-orchestration/assets/templates/ path documenting technical-debt-register-template.md location, and version header updated to "3.3 (Added: .claude/hooks/ directory, devforgeai-orchestration/assets/templates/ for EPIC-048)"</then>
  <verification>
    <source_files>
      <file hint="Updated source tree">src/devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac5_source_tree_update.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Tech-Stack.md v1.3 Shell Script Exception for Hooks

```xml
<acceptance_criteria id="AC6" implements="COMP-006">
  <given>tech-stack.md exists at version 1.2 with Markdown-only documentation rule</given>
  <when>The file is updated to v1.3</when>
  <then>The file includes: exception block for .claude/hooks/*.sh files documenting shell scripts are allowed for workflow hooks, naming convention (post-{workflow}-{action}.sh), registration requirement (devforgeai/config/hooks.yaml), exit code semantics (0=proceed, 1=warn, 2=halt), and version header updated to "1.3 (Added: Shell script exception for workflow hooks - EPIC-048)"</then>
  <verification>
    <source_files>
      <file hint="Updated tech stack">src/devforgeai/specs/context/tech-stack.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac6_tech_stack_update.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#7: Register Template Creation at Documented Location

```xml
<acceptance_criteria id="AC7" implements="COMP-007">
  <given>The template location is documented in source-tree.md (AC5)</given>
  <when>The template file is created</when>
  <then>technical-debt-register-template.md exists at .claude/skills/devforgeai-orchestration/assets/templates/ containing: YAML frontmatter schema with all analytics fields initialized to 0, threshold defaults (5/10/15/90), structured item template with DEBT-NNN placeholder, all three sections (Open, In Progress, Resolved), and usage instructions for technical-debt-analyzer auto-creation</then>
  <verification>
    <source_files>
      <file hint="Register template">src/claude/skills/devforgeai-orchestration/assets/templates/technical-debt-register-template.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-285/test_ac7_template_creation.sh</test_file>
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
    # COMP-001: Technical Debt Register v2.0 Format
    - type: "Configuration"
      name: "technical-debt-register.md"
      file_path: "devforgeai/technical-debt-register.md"
      purpose: "Machine-parseable technical debt tracking with YAML analytics"
      required_keys:
        - key: "version"
          type: "string"
          example: "2.0"
          required: true
          test_requirement: "Test: YAML frontmatter contains version: 2.0"
        - key: "last_updated"
          type: "string"
          example: "2026-01-20"
          required: true
          validation: "ISO 8601 date format (YYYY-MM-DD)"
          test_requirement: "Test: last_updated follows ISO date format"
        - key: "analytics.total_open"
          type: "int"
          default: 0
          required: true
          test_requirement: "Test: analytics.total_open is integer >= 0"
        - key: "analytics.total_in_progress"
          type: "int"
          default: 0
          required: true
          test_requirement: "Test: analytics.total_in_progress is integer >= 0"
        - key: "analytics.total_resolved"
          type: "int"
          default: 0
          required: true
          test_requirement: "Test: analytics.total_resolved is integer >= 0"
        - key: "analytics.by_type"
          type: "object"
          example: "{story_split: 0, scope_change: 0, external_blocker: 0}"
          required: true
          test_requirement: "Test: by_type contains all three type counters"
        - key: "analytics.by_priority"
          type: "object"
          example: "{critical: 0, high: 0, medium: 0, low: 0}"
          required: true
          test_requirement: "Test: by_priority contains all four priority counters"
        - key: "analytics.by_source"
          type: "object"
          example: "{dev_phase_06: 0, qa_discovery: 0}"
          required: true
          test_requirement: "Test: by_source contains both source counters"
        - key: "thresholds.warning_count"
          type: "int"
          default: 5
          required: true
          test_requirement: "Test: warning_count defaults to 5"
        - key: "thresholds.critical_count"
          type: "int"
          default: 10
          required: true
          test_requirement: "Test: critical_count defaults to 10"
        - key: "thresholds.blocking_count"
          type: "int"
          default: 15
          required: true
          test_requirement: "Test: blocking_count defaults to 15"
        - key: "thresholds.stale_days"
          type: "int"
          default: 90
          required: true
          test_requirement: "Test: stale_days defaults to 90"
      requirements:
        - id: "COMP-001"
          description: "Register must use YAML frontmatter with analytics and thresholds sections"
          implements_ac: ["AC#1", "AC#2", "AC#3"]
          testable: true
          test_requirement: "Test: YAML frontmatter parses without error and contains required sections"
          priority: "Critical"

    # COMP-002: YAML Frontmatter Schema
    - type: "DataModel"
      name: "DebtRegisterFrontmatter"
      table: "N/A (markdown file)"
      purpose: "YAML schema for technical debt register frontmatter"
      fields:
        - name: "version"
          type: "String"
          constraints: "Required, Pattern: [0-9]+.[0-9]+"
          description: "Format version (2.0 for this story)"
          test_requirement: "Test: Version matches semantic version pattern"
        - name: "last_updated"
          type: "Date"
          constraints: "Required, ISO 8601"
          description: "Date of last register update"
        - name: "analytics"
          type: "Object"
          constraints: "Required"
          description: "Counter object with debt statistics"
        - name: "thresholds"
          type: "Object"
          constraints: "Required"
          description: "Alert threshold configuration"
      requirements:
        - id: "COMP-002"
          description: "Frontmatter must be valid YAML parseable by yaml.safe_load()"
          implements_ac: ["AC#1"]
          testable: true
          test_requirement: "Test: Python yaml.safe_load() parses frontmatter without exception"
          priority: "Critical"

    # COMP-003: DEBT-NNN ID Format
    - type: "DataModel"
      name: "DebtItem"
      table: "N/A (markdown section)"
      purpose: "Structured debt item with DEBT-NNN identifier"
      fields:
        - name: "id"
          type: "String"
          constraints: "Required, Pattern: DEBT-[0-9]{3}"
          description: "Unique debt identifier (3-digit zero-padded)"
          test_requirement: "Test: ID matches regex ^DEBT-[0-9]{3}$"
        - name: "date"
          type: "Date"
          constraints: "Required, ISO 8601"
          description: "Date debt was added"
        - name: "source"
          type: "Enum"
          constraints: "Required, Values: dev_phase_06|qa_discovery"
          description: "Origin of debt (dev workflow or QA)"
          test_requirement: "Test: Source is one of allowed values"
        - name: "type"
          type: "Enum"
          constraints: "Required, Values: Story Split|Scope Change|External Blocker"
          description: "Category of technical debt"
        - name: "priority"
          type: "Enum"
          constraints: "Required, Values: Critical|High|Medium|Low"
          description: "Priority level for resolution"
        - name: "status"
          type: "Enum"
          constraints: "Required, Values: Open|In Progress|Resolved"
          description: "Current state of debt item"
        - name: "effort"
          type: "String"
          constraints: "Required, Pattern: [0-9]+ (points|hours)"
          description: "Estimated effort to resolve"
        - name: "follow_up"
          type: "String"
          constraints: "Required, Pattern: (STORY|ADR)-[0-9]+"
          description: "Reference to follow-up story or ADR"
          test_requirement: "Test: Follow-up matches STORY-NNN or ADR-NNN pattern"
      requirements:
        - id: "COMP-003"
          description: "Each debt item must have all required fields in structured format"
          implements_ac: ["AC#2"]
          testable: true
          test_requirement: "Test: Debt items have all 8 required fields populated"
          priority: "Critical"

    # COMP-004: Technical Debt Analyzer Update
    - type: "Service"
      name: "technical-debt-analyzer"
      file_path: "src/claude/agents/technical-debt-analyzer.md"
      interface: "Subagent"
      lifecycle: "On-demand"
      dependencies:
        - "Read"
        - "Glob"
        - "Grep"
        - "Write"
      requirements:
        - id: "COMP-004"
          description: "Phase 1 must parse YAML frontmatter and DEBT-NNN IDs"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: Subagent extracts analytics.total_open from YAML frontmatter"
          priority: "Critical"
        - id: "SVC-001"
          description: "Must auto-create register from template if not found"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: When register missing, subagent creates from template"
          priority: "High"
        - id: "SVC-002"
          description: "Must validate DEBT-NNN format using regex pattern"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: Invalid IDs (DEBT-1, DEBT-0001) flagged as warnings"
          priority: "Medium"
        - id: "SVC-003"
          description: "Must parse source field to distinguish dev vs QA origin"
          implements_ac: ["AC#4"]
          testable: true
          test_requirement: "Test: Subagent categorizes items by source field"
          priority: "High"

    # COMP-005: Source-Tree.md Update
    - type: "Configuration"
      name: "source-tree.md"
      file_path: "src/devforgeai/specs/context/source-tree.md"
      purpose: "Document .claude/hooks/ directory and template path"
      required_keys:
        - key: ".claude/hooks/"
          type: "directory"
          required: true
          test_requirement: "Test: source-tree.md contains .claude/hooks/ entry"
        - key: "src/claude/skills/devforgeai-orchestration/assets/templates/"
          type: "directory"
          required: true
          test_requirement: "Test: source-tree.md documents template directory path"
        - key: "version"
          type: "string"
          example: "3.3"
          required: true
          test_requirement: "Test: Version header shows 3.3"
      requirements:
        - id: "COMP-005"
          description: "Must document hook directory and template location"
          implements_ac: ["AC#5"]
          testable: true
          test_requirement: "Test: Both paths documented with naming conventions"
          priority: "High"

    # COMP-006: Tech-Stack.md Shell Script Exception
    - type: "Configuration"
      name: "tech-stack.md"
      file_path: "src/devforgeai/specs/context/tech-stack.md"
      purpose: "Add shell script exception for workflow hooks"
      required_keys:
        - key: ".claude/hooks/*.sh"
          type: "exception"
          required: true
          test_requirement: "Test: Exception block for shell scripts in hooks/"
        - key: "exit_code_semantics"
          type: "documentation"
          example: "0=proceed, 1=warn, 2=halt"
          required: true
          test_requirement: "Test: Exit code semantics documented"
        - key: "version"
          type: "string"
          example: "1.3"
          required: true
          test_requirement: "Test: Version header shows 1.3"
      requirements:
        - id: "COMP-006"
          description: "Must add shell script exception with exit code semantics"
          implements_ac: ["AC#6"]
          testable: true
          test_requirement: "Test: Shell exception documented with all details"
          priority: "High"

    # COMP-007: Register Template
    - type: "Configuration"
      name: "technical-debt-register-template.md"
      file_path: "src/claude/skills/devforgeai-orchestration/assets/templates/technical-debt-register-template.md"
      purpose: "Template for auto-creation of new debt registers"
      required_keys:
        - key: "version"
          type: "string"
          example: "2.0"
          required: true
          default: "2.0"
          test_requirement: "Test: Template has version: 2.0 in frontmatter"
        - key: "analytics.*"
          type: "int"
          default: 0
          required: true
          test_requirement: "Test: All analytics counters initialized to 0"
        - key: "thresholds.warning_count"
          type: "int"
          default: 5
          required: true
          test_requirement: "Test: warning_count default is 5"
        - key: "thresholds.critical_count"
          type: "int"
          default: 10
          required: true
          test_requirement: "Test: critical_count default is 10"
        - key: "thresholds.blocking_count"
          type: "int"
          default: 15
          required: true
          test_requirement: "Test: blocking_count default is 15"
        - key: "thresholds.stale_days"
          type: "int"
          default: 90
          required: true
          test_requirement: "Test: stale_days default is 90"
      requirements:
        - id: "COMP-007"
          description: "Template must include complete YAML schema and DEBT-NNN placeholder"
          implements_ac: ["AC#7"]
          testable: true
          test_requirement: "Test: Template contains DEBT-NNN example in item template"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "DEBT-NNN ID must be 3-digit zero-padded (DEBT-001, not DEBT-1)"
      trigger: "When debt item is created or validated"
      validation: "Regex: ^DEBT-[0-9]{3}$"
      error_handling: "Flag as warning during parsing, do not reject entry"
      test_requirement: "Test: DEBT-001 valid, DEBT-1 invalid, DEBT-0001 invalid"
      priority: "Critical"

    - id: "BR-002"
      rule: "Source field must be 'dev_phase_06' or 'qa_discovery' only"
      trigger: "When debt item is parsed"
      validation: "Enum check against allowed values"
      error_handling: "Flag as warning, categorize as 'unknown_source'"
      test_requirement: "Test: Invalid source 'manual' flagged as warning"
      priority: "High"

    - id: "BR-003"
      rule: "ID sequence: next ID = max(existing IDs) + 1, or DEBT-001 if empty"
      trigger: "When new debt item is added"
      validation: "Parse existing IDs, calculate max, increment"
      error_handling: "If parse fails, default to DEBT-001 with warning"
      test_requirement: "Test: Empty register uses DEBT-001, register with DEBT-005 uses DEBT-006"
      priority: "High"

    - id: "BR-004"
      rule: "Analytics counters must reflect actual item counts (eventually consistent)"
      trigger: "After debt item added/removed/status changed"
      validation: "Count items in each section, compare to counters"
      error_handling: "Log discrepancy, do not block workflow"
      test_requirement: "Test: Adding item increments total_open counter"
      priority: "Medium"

    - id: "BR-005"
      rule: "Threshold alerting: warn at 5, critical at 10, blocking at 15 open items"
      trigger: "During technical-debt-analyzer Phase 2"
      validation: "Compare total_open to threshold values"
      error_handling: "Generate appropriate severity recommendation"
      test_requirement: "Test: 5 items = warning, 10 items = critical, 15 items = blocking"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "YAML frontmatter parsing under 50ms for register with up to 100 items"
      metric: "Parse time < 50ms for 100-item register"
      test_requirement: "Test: Parse 100-item register YAML frontmatter, assert < 50ms"
      priority: "Medium"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Analytics calculation under 100ms for full register analysis"
      metric: "Analysis time < 100ms"
      test_requirement: "Test: Full register analysis completes in < 100ms"
      priority: "Medium"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Atomic writes for register updates (no partial updates)"
      metric: "Zero partial writes on interruption"
      test_requirement: "Test: Interrupt during write, verify no corruption"
      priority: "High"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Template creation is idempotent (re-running is safe)"
      metric: "Multiple template creates produce identical result"
      test_requirement: "Test: Create template twice, verify identical content"
      priority: "High"

    - id: "NFR-005"
      category: "Scalability"
      requirement: "Format supports up to 999 debt items (DEBT-001 through DEBT-999)"
      metric: "ID range 001-999 supported"
      test_requirement: "Test: DEBT-999 is valid ID"
      priority: "Low"

    - id: "NFR-006"
      category: "Security"
      requirement: "No sensitive data in debt register (story IDs, dates, descriptions only)"
      metric: "Zero passwords, tokens, or PII in register"
      test_requirement: "Test: Grep for 'password', 'token', 'secret' returns zero matches"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "YAML Frontmatter"
    limitation: "YAML parsing requires correct indentation - manual edits may break parser"
    decision: "workaround:Template includes validation instructions and editor recommendations"
    discovered_phase: "Architecture"
    impact: "Users editing register manually may introduce syntax errors"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Parsing Time:**
- YAML frontmatter parsing: < 50ms (p95) for 100-item register
- Analytics calculation: < 100ms for full analysis

**Template Loading:**
- Template file read: < 20ms

### Security

**Data Protection:**
- No sensitive data allowed in register (validation enforced)
- File paths validated against source-tree.md

### Scalability

**Item Capacity:**
- Support 1-999 debt items (DEBT-001 through DEBT-999)
- Analytics section extensible for future metrics

### Reliability

**Write Safety:**
- Atomic writes (no partial updates)
- Template creation idempotent
- Migration preserves all existing content

---

## Dependencies

### Prerequisite Stories

None - this is the foundation story (Feature 1 of EPIC-048).

### External Dependencies

None.

### Technology Dependencies

- [ ] **PyYAML 6.0+** - For YAML parsing validation tests
  - **Purpose:** Parse YAML frontmatter in test scripts
  - **Approved:** Yes (in dependencies.md)
  - **Added to dependencies.md:** Yes

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for business logic (ID generation, analytics counters)

**Test Scenarios:**

1. **Happy Path:**
   - YAML frontmatter parses correctly
   - Analytics counters initialize to 0
   - DEBT-NNN IDs validate correctly

2. **Edge Cases:**
   - Empty register (0 items)
   - DEBT-001 first ID generation
   - DEBT-999 maximum ID
   - Malformed YAML (error handling)

3. **Error Cases:**
   - Invalid ID format (DEBT-1, DEBT-0001)
   - Invalid source value (not dev_phase_06 or qa_discovery)
   - Missing required fields

### Integration Tests

**Coverage Target:** 85% for application layer

**Test Scenarios:**

1. **Register Migration:** v1.0 → v2.0 format conversion
2. **Subagent Parsing:** technical-debt-analyzer reads YAML correctly
3. **Template Auto-Creation:** Register created from template when missing

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: YAML Frontmatter with Analytics Section

- [x] YAML frontmatter with version: 2.0 - **Phase:** 3 - **Evidence:** devforgeai/technical-debt-register.md
- [x] last_updated field in ISO format - **Phase:** 3 - **Evidence:** register file
- [x] analytics section with all counters - **Phase:** 3 - **Evidence:** register file
- [x] thresholds section with defaults (5/10/15/90) - **Phase:** 3 - **Evidence:** register file

### AC#2: Structured Item Format

- [x] DEBT-NNN ID pattern documented - **Phase:** 3 - **Evidence:** register template
- [x] All 8 fields defined in template - **Phase:** 3 - **Evidence:** register template
- [x] Source field enum documented - **Phase:** 3 - **Evidence:** register template

### AC#3: Migration Complete

- [x] v1.0 content migrated to v2.0 - **Phase:** 3 - **Evidence:** register file
- [x] Analytics initialized to 0 - **Phase:** 3 - **Evidence:** register file
- [x] Template comment updated - **Phase:** 3 - **Evidence:** register file

### AC#4: Subagent Update

- [x] Phase 1 YAML parsing documented - **Phase:** 3 - **Evidence:** technical-debt-analyzer.md
- [x] DEBT-NNN regex pattern added - **Phase:** 3 - **Evidence:** subagent file
- [x] Auto-create from template logic - **Phase:** 3 - **Evidence:** subagent file

### AC#5: Source-Tree Update

- [x] .claude/hooks/ directory documented - **Phase:** 3 - **Evidence:** source-tree.md
- [x] Template path documented - **Phase:** 3 - **Evidence:** source-tree.md
- [x] Version bumped to 3.3 - **Phase:** 3 - **Evidence:** source-tree.md

### AC#6: Tech-Stack Update

- [x] Shell script exception added - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Exit code semantics documented - **Phase:** 3 - **Evidence:** tech-stack.md
- [x] Version bumped to 1.3 - **Phase:** 3 - **Evidence:** tech-stack.md

### AC#7: Template Created

- [x] Template file created at documented path - **Phase:** 3 - **Evidence:** template file
- [x] All analytics fields initialized to 0 - **Phase:** 3 - **Evidence:** template file
- [x] DEBT-NNN placeholder in item section - **Phase:** 3 - **Evidence:** template file

---

**Checklist Progress:** 21/21 items complete (100%)

---

## Definition of Done

### Implementation
- [x] technical-debt-register.md converted to v2.0 format with YAML frontmatter
- [x] YAML schema includes version, last_updated, analytics, and thresholds sections
- [x] Debt item format uses DEBT-NNN ID pattern (3-digit zero-padded)
- [x] Item format includes all 8 required fields (id, date, source, type, priority, status, effort, follow_up)
- [x] technical-debt-analyzer.md updated with YAML parsing in Phase 1
- [x] Subagent validates DEBT-NNN format using regex
- [x] Subagent auto-creates register from template if missing
- [x] source-tree.md v3.3 documents .claude/hooks/ directory
- [x] source-tree.md v3.3 documents template location
- [x] tech-stack.md v1.3 adds shell script exception for hooks
- [x] tech-stack.md v1.3 documents exit code semantics (0/1/2)
- [x] technical-debt-register-template.md created at documented location
- [x] Template initializes all analytics to 0 and thresholds to defaults

### Quality
- [x] All 7 acceptance criteria have passing tests
- [x] Edge cases covered (empty register, max ID, malformed YAML)
- [x] Data validation enforced (DEBT-NNN format, source enum, follow-up pattern)
- [x] NFRs met (parsing <50ms, atomic writes, idempotent template)
- [x] Code coverage >95% for validation logic

### Testing
- [x] Unit tests for YAML frontmatter parsing
- [x] Unit tests for DEBT-NNN ID validation
- [x] Unit tests for source field enum validation
- [x] Integration tests for register migration
- [x] Integration tests for subagent YAML extraction
- [x] Integration tests for template auto-creation

### Documentation
- [x] Register file contains usage instructions
- [x] Template contains usage instructions
- [x] Context files (source-tree, tech-stack) updated with change notes

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-20
**Branch:** main

- [x] technical-debt-register.md converted to v2.0 format with YAML frontmatter
- [x] YAML schema includes version, last_updated, analytics, and thresholds sections
- [x] Debt item format uses DEBT-NNN ID pattern (3-digit zero-padded)
- [x] Item format includes all 8 required fields (id, date, source, type, priority, status, effort, follow_up)
- [x] technical-debt-analyzer.md updated with YAML parsing in Phase 1
- [x] Subagent validates DEBT-NNN format using regex
- [x] Subagent auto-creates register from template if missing
- [x] source-tree.md v3.3 documents .claude/hooks/ directory
- [x] source-tree.md v3.3 documents template location
- [x] tech-stack.md v1.3 adds shell script exception for hooks
- [x] tech-stack.md v1.3 documents exit code semantics (0/1/2)
- [x] technical-debt-register-template.md created at documented location
- [x] Template initializes all analytics to 0 and thresholds to defaults
- [x] All 7 acceptance criteria have passing tests
- [x] Edge cases covered (empty register, max ID, malformed YAML)
- [x] Data validation enforced (DEBT-NNN format, source enum, follow-up pattern)
- [x] NFRs met (parsing <50ms, atomic writes, idempotent template)
- [x] Code coverage >95% for validation logic
- [x] Unit tests for YAML frontmatter parsing
- [x] Unit tests for DEBT-NNN ID validation
- [x] Unit tests for source field enum validation
- [x] Integration tests for register migration
- [x] Integration tests for subagent YAML extraction
- [x] Integration tests for template auto-creation
- [x] Register file contains usage instructions
- [x] Template contains usage instructions
- [x] Context files (source-tree, tech-stack) updated with change notes

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 88 comprehensive tests covering all 7 acceptance criteria
- Tests placed in devforgeai/tests/STORY-285/
- Test framework: Bash shell scripts

**Phase 03 (Green): Implementation**
- Updated technical-debt-register.md with v2.0 YAML frontmatter format
- Updated technical-debt-analyzer.md with YAML parsing and DEBT-NNN validation
- Updated source-tree.md to v3.3 with hooks and template documentation
- Updated tech-stack.md to v1.3 with shell script exception
- Created technical-debt-register-template.md at documented location
- All 88 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code quality validated
- All tests remain green after refactoring

**Phase 05 (Integration): Full Validation**
- Full test suite executed (88/88 passing)
- All 7 ACs verified

**Phase 06 (Deferral Challenge): DoD Validation**
- All Definition of Done items implemented
- No deferrals needed (100% complete)
- No blockers detected

### Files Modified

- devforgeai/technical-debt-register.md (v2.0 format)
- .claude/agents/technical-debt-analyzer.md (YAML parsing)
- src/claude/agents/technical-debt-analyzer.md (source copy)
- devforgeai/specs/context/source-tree.md (v3.3)
- devforgeai/specs/context/tech-stack.md (v1.3)
- .claude/skills/devforgeai-orchestration/assets/templates/technical-debt-register-template.md (new)
- src/claude/skills/devforgeai-orchestration/assets/templates/technical-debt-register-template.md (source copy)

### Test Results

- **Total tests:** 88
- **Pass rate:** 100%
- **Test suites:** 7 (one per AC)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-20 12:00 | claude/story-requirements-analyst | Created | Story created from EPIC-048 Feature 1 | STORY-285-register-format-standardization.story.md |
| 2026-01-20 | claude/opus | Development (Phase 02-05) | TDD implementation of all 7 ACs with 88 passing tests | technical-debt-register.md, technical-debt-analyzer.md, source-tree.md, tech-stack.md, technical-debt-register-template.md |
| 2026-01-20 | claude/opus | DoD Update (Phase 07) | Development complete, all DoD items verified | STORY-285-register-format-standardization.story.md |
| 2026-01-20 | claude/qa-result-interpreter | QA Deep | PASSED: 100% coverage, 88/88 tests, 0 blocking violations | STORY-285-qa-report.md |

## Notes

**Design Decisions:**
- DEBT-NNN format chosen for consistency with STORY-NNN and ADR-NNN patterns
- 3-digit zero-padding supports 999 items (sufficient for any project)
- Source field limited to `dev_phase_06` and `qa_discovery` to enable automated tracking
- YAML frontmatter chosen over separate metadata file for single-file simplicity

**Open Questions:**
- None at this time

**Related ADRs:**
- None (context file updates don't require ADR per architecture-constraints.md)

**References:**
- EPIC-048: Technical Debt Register Automation
- EPIC-048 Feature 1: Register Format Standardization
- devforgeai/specs/context/tech-stack.md (shell script exception precedent)
- devforgeai/specs/context/source-tree.md (directory documentation format)

---

**Story Template Version:** 2.6
**Last Updated:** 2026-01-20
