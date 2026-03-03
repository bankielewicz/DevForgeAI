---
id: STORY-319
title: Create Observation Extractor Subagent
type: feature
epic: EPIC-051
sprint: Backlog
status: QA Approved
points: 8
depends_on: []
priority: High
assigned_to: null
created: 2026-01-26
updated: 2026-01-26
format_version: "2.7"
tags: [feedback-system, subagents, observations, extraction, EPIC-051]
---

# Story: Create Observation Extractor Subagent

## Description

**As a** Framework Architect (Claude),
**I want** an observation-extractor subagent that mines existing subagent outputs for observations,
**so that** observations are automatically captured even from subagents without explicit schema changes, enabling the framework to self-improve without additional cognitive load during development.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-051-feedback-capture-system.epic.md" section="feature-2">
    <quote>"Create new observation-extractor subagent to mine existing outputs for observations"</quote>
    <line_reference>EPIC-051 Feature 2</line_reference>
    <quantified_impact>Enable observation capture from legacy subagents without code changes</quantified_impact>
  </origin>

  <decision rationale="non-invasive-extraction">
    <selected>Create dedicated extractor subagent that parses existing output formats</selected>
    <rejected alternative="modify-all-subagents">Would require changes to 20+ subagent files</rejected>
    <trade_off>Extraction rules must be maintained separately from subagent definitions</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="automatic-observation-capture">
    <quote>"I want observations automatically captured from existing subagent outputs"</quote>
    <source>EPIC-051, User Stories section</source>
  </stakeholder>

  <hypothesis id="H2" validation="extraction-accuracy" success_criteria="90% of meaningful insights captured automatically">
    Mining existing outputs will capture observations without requiring schema changes to all subagents
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Subagent File Creation

```xml
<acceptance_criteria id="AC1" implements="SPEC-001">
  <given>The DevForgeAI framework requires an observation-extractor subagent</given>
  <when>The observation-extractor.md file is created</when>
  <then>The file exists at `.claude/agents/observation-extractor.md` with valid YAML frontmatter containing name, description, tools, and model fields</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac1_subagent_file_creation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Test-Automator Extraction Rules

```xml
<acceptance_criteria id="AC2" implements="SPEC-002">
  <given>The test-automator subagent returns coverage gaps and test failures</given>
  <when>The observation-extractor receives test-automator output containing `coverage_result.gaps[]`</when>
  <then>Observations are extracted with category "gap" for each coverage gap entry, and when `test_failures[]` exists, observations are extracted with category "friction" for each failure entry</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac2_test_automator_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Code-Reviewer Extraction Rules

```xml
<acceptance_criteria id="AC3" implements="SPEC-003">
  <given>The code-reviewer subagent returns issues with severity levels</given>
  <when>The observation-extractor receives code-reviewer output containing issues with `severity == "high"`</when>
  <then>Observations are extracted with category "friction" for each high-severity issue, and when issues have `severity == "medium"`, observations are extracted with category "warning"</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac3_code_reviewer_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Backend-Architect Extraction Rules

```xml
<acceptance_criteria id="AC4" implements="SPEC-004">
  <given>The backend-architect subagent returns pattern compliance results</given>
  <when>The observation-extractor receives backend-architect output containing `pattern_compliance.violations[]`</when>
  <then>Observations are extracted with category "pattern" for each violation entry</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac4_backend_architect_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: AC-Compliance-Verifier Extraction Rules

```xml
<acceptance_criteria id="AC5" implements="SPEC-005">
  <given>The ac-compliance-verifier subagent returns verification results</given>
  <when>The observation-extractor receives ac-compliance-verifier output containing `verification_results[].status == "FAIL"`</when>
  <then>Observations are extracted with category "gap" for each failed AC verification</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac5_ac_compliance_verifier_extraction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Silent Skip for Missing Fields

```xml
<acceptance_criteria id="AC6" implements="BR-001">
  <given>A subagent output may not contain all expected fields</given>
  <when>The observation-extractor attempts to extract from a non-existent field (e.g., `coverage_result.gaps[]` not present)</when>
  <then>The extraction silently skips that rule without errors or warnings and continues processing other extraction rules for the same output</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac6_silent_skip.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#7: Observation Schema Compliance

```xml
<acceptance_criteria id="AC7" implements="SPEC-006">
  <given>Extracted observations must integrate with phase-state.json</given>
  <when>Observations are extracted from any subagent output</when>
  <then>Each observation includes all required fields: id (format: `obs-{phase}-{sequence}`), phase, category (one of: friction, success, pattern, gap, idea, bug, warning), note (max 200 chars), severity (low/medium/high), and optionally includes files array with related file paths</then>
  <verification>
    <source_files>
      <file hint="New subagent spec">.claude/agents/observation-extractor.md</file>
    </source_files>
    <test_file>tests/STORY-319/test_ac7_schema_compliance.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Subagent"
      name: "observation-extractor"
      file_path: "src/claude/agents/observation-extractor.md"  # Source of truth (mirror to .claude/agents/)
      mirror_path: ".claude/agents/observation-extractor.md"   # Operational location
      purpose: "Mine existing subagent outputs for observations without requiring schema changes"
      dependencies: []
      requirements:
        - id: "SPEC-001"
          description: "Create subagent specification file with valid YAML frontmatter"
          testable: true
          test_requirement: "Test: File exists at .claude/agents/observation-extractor.md with name, description, tools, model fields"
          priority: "Critical"
          implements_ac: ["AC#1"]
        - id: "SPEC-002"
          description: "Implement extraction rules for test-automator output"
          testable: true
          test_requirement: "Test: coverage_result.gaps[] maps to category 'gap'; test_failures[] maps to category 'friction'"
          priority: "Critical"
          implements_ac: ["AC#2"]
        - id: "SPEC-003"
          description: "Implement extraction rules for code-reviewer output"
          testable: true
          test_requirement: "Test: issues[].severity=='high' maps to 'friction'; severity=='medium' maps to 'warning'"
          priority: "Critical"
          implements_ac: ["AC#3"]
        - id: "SPEC-004"
          description: "Implement extraction rules for backend-architect output"
          testable: true
          test_requirement: "Test: pattern_compliance.violations[] maps to category 'pattern'"
          priority: "Critical"
          implements_ac: ["AC#4"]
        - id: "SPEC-005"
          description: "Implement extraction rules for ac-compliance-verifier output"
          testable: true
          test_requirement: "Test: verification_results[].status=='FAIL' maps to category 'gap'"
          priority: "Critical"
          implements_ac: ["AC#5"]
        - id: "SPEC-006"
          description: "Generate observations conforming to phase-state.json schema"
          testable: true
          test_requirement: "Test: Each observation has id, phase, category, note, severity fields; files optional"
          priority: "Critical"
          implements_ac: ["AC#7"]

  business_rules:
    - id: "BR-001"
      rule: "Silent skip when expected fields are missing from subagent output"
      trigger: "When accessing fields like coverage_result.gaps[] that may not exist"
      validation: "No error thrown, empty array returned for that extraction rule"
      error_handling: "Log debug-level message, continue processing other rules"
      test_requirement: "Test: When coverage_result.gaps is undefined, no error thrown"
      priority: "High"

    - id: "BR-002"
      rule: "Truncate notes exceeding 200 characters"
      trigger: "When source text for observation note exceeds 200 characters"
      validation: "Note length <= 200 characters"
      error_handling: "Truncate to 197 characters and append '...'"
      test_requirement: "Test: 250-character note becomes 197 chars + '...'"
      priority: "Medium"

    - id: "BR-003"
      rule: "Filter sensitive fields from observation notes"
      trigger: "When extracting observation note from source data"
      validation: "No fields containing 'password', 'secret', 'token', 'key' in notes"
      error_handling: "Skip sensitive fields, extract from safe fields only"
      test_requirement: "Test: Source with 'password' field excluded from observation note"
      priority: "High"

    - id: "BR-004"
      rule: "Limit extraction to 20 items per category from large arrays"
      trigger: "When source array contains more than 20 items"
      validation: "Maximum 20 observations per category per extraction"
      error_handling: "Add summary observation noting 'X additional items not captured'"
      test_requirement: "Test: Array with 50 items produces 20 observations + 1 summary"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Extraction processing time under 50ms per subagent output"
      metric: "< 50ms per subagent output parsing"
      test_requirement: "Test: Benchmark extraction with typical output, verify < 50ms"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Total extraction latency under 200ms for all 4 subagent types"
      metric: "< 200ms when processing outputs from all 4 subagent types sequentially"
      test_requirement: "Test: Sequential extraction from 4 outputs completes in < 200ms"
      priority: "Medium"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "Graceful degradation on malformed input"
      metric: "Return empty array on invalid JSON, never throw exception"
      test_requirement: "Test: Malformed JSON input returns [] without exception"
      priority: "Critical"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Idempotent execution"
      metric: "Same input always produces same output observations"
      test_requirement: "Test: Run extraction twice with same input, verify identical output"
      priority: "High"

    - id: "NFR-005"
      category: "Security"
      requirement: "No sensitive data exposure in observations"
      metric: "0 observations contain password/secret/token/key field values"
      test_requirement: "Test: Verify filtering of sensitive fields"
      priority: "Critical"
```

### Extraction Rules Table

**Note:** These extraction rules are **forward-looking specifications**. The referenced source fields may not currently exist in all subagent outputs. The observation-extractor's "Silent Skip" behavior (AC#6) ensures graceful handling when fields are absent.

| Subagent | Source Field | Target Category | Severity | Condition | Field Status |
|----------|--------------|-----------------|----------|-----------|--------------|
| test-automator | `coverage_result.gaps[]` | gap | medium | Any gap exists | ⚠️ Define in subagent |
| test-automator | `test_failures[]` | friction | high | Any failure exists | ⚠️ Define in subagent |
| code-reviewer | `issues[].severity == "high"` | friction | high | High severity issues | ⚠️ Define in subagent |
| code-reviewer | `issues[].severity == "medium"` | warning | medium | Medium severity issues | ⚠️ Define in subagent |
| backend-architect | `pattern_compliance.violations[]` | pattern | medium | Any violation exists | ⚠️ Define in subagent |
| ac-compliance-verifier | `verification_results[].status == "FAIL"` | gap | high | Any AC fails | ⚠️ Define in subagent |

**Implementation Note:** When implementing observation-extractor, use defensive field access patterns (e.g., `field?.property` or `getattr(obj, 'field', None)`) to handle missing fields gracefully.

### Invocation Pattern

```markdown
# Called by phase files at exit gate
Task(subagent_type="observation-extractor",
     prompt="Extract observations from phase {phase_number} subagent outputs",
     context="{subagent_output_json}")
```

### Output Schema

```yaml
# observation-extractor returns array of observations
observations:
  - id: "obs-02-001"           # Format: obs-{phase}-{sequence}
    phase: "02"                 # Source phase (01-09)
    category: "gap"             # One of 7 categories
    note: "Coverage gap in installer/rollback.py: 63.6% (target 95%)"
    severity: "medium"          # low | medium | high
    files:                      # Optional: related files
      - "installer/rollback.py"
    source_subagent: "test-automator"  # Which subagent produced source data
    extraction_rule: "coverage_result.gaps[]"  # Which rule matched
```

---

## Edge Cases & Error Handling

1. **Empty Subagent Output:** When observation-extractor receives an empty JSON object `{}` or null context, return empty observations array without errors. Validate input is valid JSON before processing.

2. **Malformed JSON Input:** When the context parameter contains invalid JSON (syntax errors, truncated data), log a warning message "Invalid JSON input received" and return empty observations array without throwing exceptions.

3. **Nested Field Access Failures:** When accessing deeply nested fields like `coverage_result.gaps[]` where intermediate objects are null/undefined (e.g., `coverage_result` exists but has no `gaps` property), skip silently per AC6 rather than throwing null reference errors.

4. **Duplicate Observations:** When the same issue appears in multiple subagent outputs (e.g., same file mentioned in both code-reviewer issues and backend-architect violations), generate separate observations for each source to preserve context traceability.

5. **Very Large Output Arrays:** When a subagent returns arrays with 100+ items (e.g., 150 test failures), limit observation extraction to first 20 items per category to prevent observation noise, and add a summary observation noting "X additional items not captured."

6. **Unknown Subagent Type:** When invoked with output from an unrecognized subagent type (not test-automator, code-reviewer, backend-architect, or ac-compliance-verifier), return empty observations array and log informational message "No extraction rules defined for subagent type: {type}."

---

## Data Validation Rules

1. **Context Parameter:** Must be valid JSON string or object; maximum 500KB payload size
2. **Phase Number:** Must be string value "01" through "09" matching source phase
3. **Observation ID Format:** Must match pattern `obs-{phase}-{sequence}` where sequence is 3-digit zero-padded integer (e.g., `obs-02-001`)
4. **Category Values:** Must be one of exactly 7 values: friction, success, pattern, gap, idea, bug, warning (case-sensitive, lowercase)
5. **Severity Values:** Must be one of: low, medium, high (case-sensitive, lowercase)
6. **Note Length:** Maximum 200 characters; truncate with "..." if source text exceeds limit
7. **Files Array:** Each entry must be relative path from project root (no leading `/`, no absolute paths starting with `/mnt/` or `C:\`)

---

## Non-Functional Requirements

### Performance
- Extraction processing time: < 50ms per subagent output parsing
- Total extraction latency: < 200ms when processing outputs from all 4 subagent types sequentially
- Memory footprint: < 5MB per extraction operation
- JSON parsing: < 10ms for payloads up to 500KB

### Security
- Input validation: JSON schema validation before field access to prevent injection
- No file system writes: Subagent returns observations only; phase files write to phase-state.json
- No external network calls: All operations local to provided context
- No credential exposure: Observations must not capture sensitive data from source outputs (filter out any fields containing "password", "secret", "token", "key")

### Reliability
- Error handling: Graceful degradation on malformed input (return empty array, not exception)
- Idempotent execution: Same input always produces same output observations
- Partial extraction: If 3/4 extraction rules succeed and 1 fails, return the 3 successful extractions
- Fallback behavior: On any unexpected error, log context and return empty observations array

### Scalability
- Stateless design: No persistence between invocations; all context passed per-call
- Concurrent safe: Can be invoked multiple times in parallel without conflicts (no shared state)
- Extensible rules: Extraction rules defined in declarative format for easy addition of new subagent types

---

## Dependencies

### Prerequisite Stories
- None (can be developed in parallel with STORY-318)

### Related Stories
- STORY-318: Adds observation schema to 4 subagents (parallel development)
- Feature 3 (EPIC-051): Phase State Integration (will consume observations from this subagent)

### External Dependencies
None - Framework-internal subagent creation.

### Technology Dependencies
None - Markdown specification file.

---

## Implementation Guidance (Constitutional Compliance)

### Dual-Location Architecture (source-tree.md lines 496-516)

**Per source-tree.md, DevForgeAI maintains TWO parallel structures:**

1. **Source of truth:** `src/claude/agents/` - Create file here FIRST
2. **Operational:** `.claude/agents/` - Mirror file here for runtime

**Implementation sequence:**
```
1. Create src/claude/agents/observation-extractor.md (source)
2. Mirror to .claude/agents/observation-extractor.md (operational)
```

### Extraction Rules - Field Coordination with STORY-318

**IMPORTANT:** The extraction rules in this story reference output fields that may not yet exist in the target subagent specifications:

| Source Field | Referenced Subagent | Exists Currently? |
|--------------|--------------------|--------------------|
| `coverage_result.gaps[]` | test-automator | ⚠️ Not documented |
| `test_failures[]` | test-automator | ⚠️ Not documented |
| `issues[]` | code-reviewer | ⚠️ Not documented |
| `pattern_compliance.violations[]` | backend-architect | ⚠️ Not documented |
| `verification_results[]` | ac-compliance-verifier | ⚠️ Not documented |

**Resolution approach:**
1. These extraction rules are **forward-looking** - they define what the extractor WILL parse
2. The actual output schemas will be refined as subagents are updated
3. The "Silent Skip" behavior (AC#6) ensures the extractor works even when fields don't exist
4. Coordinate with STORY-318 to ensure observation output schema is consistent

**Rationale:** The observation-extractor must be designed to gracefully handle missing fields because:
- Not all subagent invocations produce all output fields
- Subagent output schemas evolve over time
- Some subagents may not have the referenced fields yet

### Story Type Clarification

**This is a SPECIFICATION story**, not a code implementation story. The deliverable is a **subagent contract file** (Markdown) that defines:
- Expected behavior
- Input/output schemas
- Extraction rules
- Error handling behavior

The subagent itself is executed by Claude Code Terminal when invoked via `Task(subagent_type="observation-extractor", ...)`.

### Out of Scope

**Phase file modifications to invoke observation-extractor are OUT OF SCOPE:**
- Adding invocation code to phase-01 through phase-09 files
- Modifying phase-state.json schema to store observations
- These are handled in EPIC-051 Feature 3: Phase State Integration

---

## Test Strategy

### Unit Tests (Structural Validation)

**Coverage Target:** 100% of structural assertions (specification story)

**Test Location:** `tests/STORY-319/` (per source-tree.md line 368)

**Test Scenarios:**
1. **File existence:** Verify `src/claude/agents/observation-extractor.md` exists
   - `test -f src/claude/agents/observation-extractor.md`

2. **YAML frontmatter:** Verify required fields present
   - `grep -q "^name:" src/claude/agents/observation-extractor.md`
   - `grep -q "^description:" src/claude/agents/observation-extractor.md`
   - `grep -q "^tools:" src/claude/agents/observation-extractor.md`
   - `grep -q "^model:" src/claude/agents/observation-extractor.md`

3. **Extraction rules:** Verify all 6 extraction rules documented
   - `grep -q "coverage_result.gaps" <file>` (test-automator gap rule)
   - `grep -q "test_failures" <file>` (test-automator friction rule)
   - `grep -q 'issues.*severity.*high' <file>` (code-reviewer friction rule)
   - `grep -q 'issues.*severity.*medium' <file>` (code-reviewer warning rule)
   - `grep -q "pattern_compliance.violations" <file>` (backend-architect rule)
   - `grep -q 'verification_results.*FAIL' <file>` (ac-compliance-verifier rule)

4. **Output schema:** Verify observation output schema documented
   - `grep -q "obs-.*-.*" <file>` (ID format)
   - `grep -q "category:" <file>` (category field)
   - `grep -q "severity:" <file>` (severity field)

5. **Mirror validation:** Verify operational copy matches source
   - `diff src/claude/agents/observation-extractor.md .claude/agents/observation-extractor.md`

### Integration Tests

**Coverage Target:** Smoke test level (verify no regression)

**Test Scenarios:**
1. **Rule coverage:** Each of 4 subagent types has extraction rules documented
2. **Category mapping:** Each extraction rule maps to valid observation category (friction, success, pattern, gap, idea, bug, warning)
3. **Schema compliance:** Output schema includes all required fields (id, phase, category, note, severity)

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: Subagent File Creation

- [ ] File exists at `src/claude/agents/observation-extractor.md` (source) - **Phase:** 03 - **Evidence:** `test -f src/claude/agents/observation-extractor.md`
- [ ] File mirrored to `.claude/agents/observation-extractor.md` (operational) - **Phase:** 03 - **Evidence:** `diff src/claude/agents/observation-extractor.md .claude/agents/observation-extractor.md`
- [ ] YAML frontmatter contains `name: observation-extractor` - **Phase:** 03 - **Evidence:** `grep -q "^name:" src/claude/agents/observation-extractor.md`
- [ ] YAML frontmatter contains description field - **Phase:** 03 - **Evidence:** `grep -q "^description:" <file>`
- [ ] YAML frontmatter contains tools field - **Phase:** 03 - **Evidence:** `grep -q "^tools:" <file>`
- [ ] YAML frontmatter contains model field - **Phase:** 03 - **Evidence:** `grep -q "^model:" <file>`

### AC#2: Test-Automator Extraction Rules

- [ ] Extraction rule for `coverage_result.gaps[]` documented - **Phase:** 03 - **Evidence:** `grep -q "coverage_result.gaps" <file>`
- [ ] Extraction rule maps to category "gap" - **Phase:** 03 - **Evidence:** `grep -A2 "coverage_result.gaps" <file> | grep -q "gap"`
- [ ] Extraction rule for `test_failures[]` documented - **Phase:** 03 - **Evidence:** `grep -q "test_failures" <file>`
- [ ] Test failures map to category "friction" - **Phase:** 03 - **Evidence:** `grep -A2 "test_failures" <file> | grep -q "friction"`

### AC#3: Code-Reviewer Extraction Rules

- [ ] Extraction rule for high severity issues documented - **Phase:** 03 - **Evidence:** `grep -q 'severity.*high' <file>`
- [ ] High severity maps to category "friction" - **Phase:** 03 - **Evidence:** grep context shows friction
- [ ] Medium severity maps to category "warning" - **Phase:** 03 - **Evidence:** `grep -q 'severity.*medium' <file>`

### AC#4: Backend-Architect Extraction Rules

- [ ] Extraction rule for `pattern_compliance.violations[]` documented - **Phase:** 03 - **Evidence:** `grep -q "pattern_compliance.violations" <file>`
- [ ] Violations map to category "pattern" - **Phase:** 03 - **Evidence:** grep context shows pattern category

### AC#5: AC-Compliance-Verifier Extraction Rules

- [ ] Extraction rule for failed verification results documented - **Phase:** 03 - **Evidence:** `grep -q "verification_results" <file>`
- [ ] Failed verifications map to category "gap" - **Phase:** 03 - **Evidence:** `grep -A2 "verification_results" <file> | grep -q "gap"`

### AC#6: Silent Skip for Missing Fields

- [ ] Silent skip behavior documented - **Phase:** 03 - **Evidence:** `grep -qi "silent" <file>` OR `grep -qi "skip" <file>`
- [ ] Graceful handling of missing fields documented - **Phase:** 03 - **Evidence:** `grep -qi "graceful" <file>` OR `grep -qi "missing field" <file>`

### AC#7: Observation Schema Compliance

- [ ] Observation `id` format documented (`obs-{phase}-{sequence}`) - **Phase:** 03 - **Evidence:** `grep -q "obs-.*-" <file>`
- [ ] Observation `phase` field documented - **Phase:** 03 - **Evidence:** `grep -q 'phase.*"0[1-9]"' <file>`
- [ ] Observation `category` field documented - **Phase:** 03 - **Evidence:** `grep -q "category:" <file>`
- [ ] Observation `note` field documented - **Phase:** 03 - **Evidence:** `grep -q "note:" <file>`
- [ ] Observation `severity` field documented - **Phase:** 03 - **Evidence:** `grep -q "severity:" <file>`
- [ ] Optional `files` array documented - **Phase:** 03 - **Evidence:** `grep -q "files:" <file>`

---

**Checklist Progress:** 0/25 items complete (0%)

---

## Definition of Done

### Implementation
- [x] observation-extractor.md created at `src/claude/agents/observation-extractor.md` (source of truth) - Completed: File created with 356 lines
- [x] observation-extractor.md mirrored to `.claude/agents/observation-extractor.md` (operational) - Completed: Identical mirror created
- [x] Valid YAML frontmatter with name, description, tools, model fields - Completed: Lines 1-6 contain all required fields
- [x] Extraction rules for test-automator documented (gaps → gap, failures → friction) - Completed: Lines 40-41, 47-82
- [x] Extraction rules for code-reviewer documented (high → friction, medium → warning) - Completed: Lines 42-43, 84-115
- [x] Extraction rules for backend-architect documented (violations → pattern) - Completed: Lines 44, 117-142
- [x] Extraction rules for ac-compliance-verifier documented (FAIL → gap) - Completed: Lines 45, 144-168
- [x] Silent skip behavior for missing fields documented - Completed: Lines 172-204
- [x] Observation output schema documented with all required fields - Completed: Lines 207-270

### Code Quality
- [x] Extraction rules table formatted consistently - Completed: Source Field Mapping Table at lines 36-46
- [x] Output schema matches phase-state.json format - Completed: Schema at lines 207-224
- [x] No anti-patterns in specification - Completed: Verified by code-reviewer
- [x] Clear separation between rules for different subagent types - Completed: Separate subsections for each subagent

### Testing
- [x] Structural tests verify file existence and frontmatter - Completed: test_ac1_subagent_file_creation.sh
- [x] Structural tests verify all 6 extraction rules present - Completed: test_ac2-5 scripts
- [x] Structural tests verify output schema documented - Completed: test_ac7_schema_compliance.sh
- [x] All tests passing - Completed: 7/7 tests pass

### Documentation
- [x] Invocation pattern documented with example - Completed: Lines 273-294
- [x] Edge cases documented (empty input, malformed JSON, missing fields) - Completed: Lines 310-318
- [x] Data validation rules documented - Completed: Lines 298-306
- [x] Error handling behavior documented - Completed: Lines 310-318

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-27
**Branch:** main

- [x] observation-extractor.md created at `src/claude/agents/observation-extractor.md` (source of truth) - Completed: File created with 356 lines
- [x] observation-extractor.md mirrored to `.claude/agents/observation-extractor.md` (operational) - Completed: Identical mirror created
- [x] Valid YAML frontmatter with name, description, tools, model fields - Completed: Lines 1-6 contain all required fields
- [x] Extraction rules for test-automator documented (gaps → gap, failures → friction) - Completed: Lines 40-41, 47-82
- [x] Extraction rules for code-reviewer documented (high → friction, medium → warning) - Completed: Lines 42-43, 84-115
- [x] Extraction rules for backend-architect documented (violations → pattern) - Completed: Lines 44, 117-142
- [x] Extraction rules for ac-compliance-verifier documented (FAIL → gap) - Completed: Lines 45, 144-168
- [x] Silent skip behavior for missing fields documented - Completed: Lines 172-204
- [x] Observation output schema documented with all required fields - Completed: Lines 207-270
- [x] Extraction rules table formatted consistently - Completed: Source Field Mapping Table at lines 36-46
- [x] Output schema matches phase-state.json format - Completed: Schema at lines 207-224
- [x] No anti-patterns in specification - Completed: Verified by code-reviewer
- [x] Clear separation between rules for different subagent types - Completed: Separate subsections for each subagent
- [x] Structural tests verify file existence and frontmatter - Completed: test_ac1_subagent_file_creation.sh
- [x] Structural tests verify all 6 extraction rules present - Completed: test_ac2-5 scripts
- [x] Structural tests verify output schema documented - Completed: test_ac7_schema_compliance.sh
- [x] All tests passing - Completed: 7/7 tests pass
- [x] Invocation pattern documented with example - Completed: Lines 273-294
- [x] Edge cases documented (empty input, malformed JSON, missing fields) - Completed: Lines 310-318
- [x] Data validation rules documented - Completed: Lines 298-306
- [x] Error handling behavior documented - Completed: Lines 310-318

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 7 structural test scripts covering all 7 acceptance criteria
- Tests placed in tests/STORY-319/
- Tests use Bash/Shell for specification validation (per tech-stack.md)

**Phase 03 (Green): Implementation**
- Created observation-extractor.md subagent specification
- Implemented via backend-architect subagent
- All 7 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code quality reviewed by refactoring-specialist and code-reviewer
- No structural changes required - specification well-organized
- All tests remain green after review

**Phase 04.5 & 05.5 (AC Verification)**
- Fresh-context AC verification passed (7/7 ACs verified)
- Evidence documented with line numbers

**Phase 05 (Integration): Full Validation**
- Source-operational file sync verified (files identical)
- All extraction rules reference valid subagents
- Integration points documented

### Files Created

- `src/claude/agents/observation-extractor.md` (356 lines)
- `.claude/agents/observation-extractor.md` (identical mirror)
- `tests/STORY-319/test_ac1_subagent_file_creation.sh`
- `tests/STORY-319/test_ac2_test_automator_extraction.sh`
- `tests/STORY-319/test_ac3_code_reviewer_extraction.sh`
- `tests/STORY-319/test_ac4_backend_architect_extraction.sh`
- `tests/STORY-319/test_ac5_ac_compliance_verifier_extraction.sh`
- `tests/STORY-319/test_ac6_silent_skip.sh`
- `tests/STORY-319/test_ac7_schema_compliance.sh`

### Test Results

- **Total tests:** 7
- **Pass rate:** 100%
- **Coverage:** N/A (specification story - no executable code)

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 | claude/story-requirements-analyst | Created | Story created from EPIC-051 Feature 2 | STORY-319-observation-extractor-subagent.story.md |
| 2026-01-27 | claude/opus | DoD Update (Phase 07) | Development complete - all 7 ACs implemented | observation-extractor.md, test files |
| 2026-01-27 | claude/qa-result-interpreter | QA Deep | PASSED: 37/37 tests pass, 0 CRITICAL/HIGH violations, all validators pass | - |

---

## Notes

**Design Decisions:**
- Stateless subagent design: All context passed per invocation, no persistence needed
- Declarative extraction rules: Easy to extend for new subagent types
- Conservative limits: 20 items per category prevents observation noise
- Sensitive field filtering: Security-first approach to prevent credential leakage

**Open Questions:**
None - Requirements are fully specified in EPIC-051.

**Related ADRs:**
None - No architectural decisions required.

**References:**
- EPIC-051: Framework Feedback Capture System
- STORY-318: Subagent Observation Schema (parallel development)

---

Story Template Version: 2.7
Last Updated: 2026-01-26
