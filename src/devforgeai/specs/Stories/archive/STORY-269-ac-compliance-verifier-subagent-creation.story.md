---
id: STORY-269
title: AC Compliance Verifier Subagent File Creation
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 2
depends_on: []
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: AC Compliance Verifier Subagent File Creation

## Description

**As a** framework developer,
**I want** the ac-compliance-verifier subagent to have proper YAML frontmatter and system prompt,
**so that** Claude Code Terminal can discover and invoke it correctly for fresh-context AC verification.

## Acceptance Criteria

### AC#1: Subagent File Structure

**Given** the DevForgeAI framework directory structure,
**When** the ac-compliance-verifier subagent is created,
**Then** the file is located at `.claude/agents/ac-compliance-verifier.md` following framework conventions.

---

### AC#2: YAML Frontmatter Compliance

**Given** the subagent file exists,
**When** Claude Code Terminal parses the frontmatter,
**Then** it contains required fields: `name: ac-compliance-verifier`, `description`, `tools: [Read, Grep, Glob]`, and `model: opus`.

---

### AC#3: System Prompt Fresh-Context Technique

**Given** the subagent system prompt,
**When** it is invoked for AC verification,
**Then** the prompt explicitly instructs fresh-context verification technique (no prior implementation knowledge).

---

### AC#4: Single Responsibility Enforcement

**Given** the subagent definition,
**When** reviewed against architecture-constraints.md,
**Then** it handles ONLY AC verification (no implementation, no file modification, no test execution).

---

### AC#5: Tool Restriction Compliance

**Given** the subagent's tool list,
**When** validated against tech-stack.md principle of least privilege,
**Then** only Read, Grep, Glob tools are available (no Write, Edit, Bash, WebFetch, WebSearch).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "ac-compliance-verifier.md"
      file_path: ".claude/agents/ac-compliance-verifier.md"
      required_keys:
        - key: "name"
          type: "string"
          example: "ac-compliance-verifier"
          required: true
          validation: "Must be lowercase with hyphens"
          test_requirement: "Test: Verify name field is 'ac-compliance-verifier'"
        - key: "description"
          type: "string"
          example: "Fresh-context AC compliance verification specialist..."
          required: true
          validation: "Must describe when to invoke"
          test_requirement: "Test: Verify description contains 'fresh-context' and 'AC'"
        - key: "tools"
          type: "array"
          example: "[Read, Grep, Glob]"
          required: true
          validation: "Must be exactly [Read, Grep, Glob]"
          test_requirement: "Test: Verify tools array contains only Read, Grep, Glob"
        - key: "model"
          type: "string"
          example: "sonnet"
          required: true
          validation: "Must be valid model (sonnet, haiku, opus)"
          test_requirement: "Test: Verify model is 'sonnet'"

  business_rules:
    - id: "BR-001"
      rule: "Subagent must be read-only (no Write/Edit tools)"
      trigger: "During tool restriction validation"
      validation: "Check tools array excludes Write, Edit, Bash"
      error_handling: "HALT if Write or Edit present"
      test_requirement: "Test: Verify Write/Edit tools are NOT in tools array"
      priority: "Critical"
    - id: "BR-002"
      rule: "System prompt must enforce fresh-context technique"
      trigger: "During prompt content validation"
      validation: "Prompt contains 'fresh context' OR 'no prior knowledge'"
      error_handling: "Warn if missing, suggest adding"
      test_requirement: "Test: Grep system prompt for fresh-context keywords"
      priority: "High"
    - id: "BR-003"
      rule: "Subagent must follow single responsibility principle"
      trigger: "During architecture review"
      validation: "Description indicates AC verification ONLY"
      error_handling: "Fail if multi-responsibility detected"
      test_requirement: "Test: Verify description does not mention implementation or modification"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Subagent file must be under 500 lines"
      metric: "< 500 lines (target: 200-300 lines)"
      test_requirement: "Test: Count lines in subagent file, verify < 500"
      priority: "Medium"
    - id: "NFR-002"
      category: "Security"
      requirement: "No network access tools"
      metric: "0 network tools (WebFetch, WebSearch)"
      test_requirement: "Test: Verify tools array excludes WebFetch, WebSearch"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Subagent invocation: < 500ms to start
- File parsing: < 100ms

**File Size:**
- Subagent file: < 500 lines (target: 200-300 lines)

---

### Security

**Authentication:** N/A (framework internal)

**Authorization:** N/A (framework internal)

**Tool Restrictions:**
- Read-only access enforced via tool list
- No network access (WebFetch, WebSearch excluded)
- No file modification (Write, Edit excluded)
- No command execution (Bash excluded)

---

## Dependencies

### Prerequisite Stories

None - This is the foundational story for Feature 1.

### External Dependencies

None

### Technology Dependencies

- Claude Code Terminal 1.0+ (existing)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for subagent validation

**Test Scenarios:**
1. **Happy Path:** Subagent file created with valid frontmatter
2. **Edge Cases:**
   - Missing required field (name, description, tools, model)
   - Invalid tool in tools array
   - Multi-line description formatting
3. **Error Cases:**
   - File at wrong location
   - Invalid YAML syntax
   - Prohibited tool (Write, Edit) in tools array

**Test File:** `tests/STORY-269/test_ac1_subagent_structure.py`

---

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Discovery Test:** Claude Code Terminal discovers subagent via Glob
2. **Invocation Test:** Task() successfully invokes subagent

---

## Acceptance Criteria Verification Checklist

### AC#1: Subagent File Structure

- [x] File exists at `.claude/agents/ac-compliance-verifier.md` - **Phase:** 3 - **Evidence:** test-ac1-subagent-file-structure.sh PASSED
- [x] File follows naming convention (lowercase-hyphens) - **Phase:** 3 - **Evidence:** test-ac1-subagent-file-structure.sh PASSED

### AC#2: YAML Frontmatter Compliance

- [x] `name` field present and correct - **Phase:** 3 - **Evidence:** test-ac2-yaml-frontmatter-compliance.sh PASSED
- [x] `description` field present - **Phase:** 3 - **Evidence:** test-ac2-yaml-frontmatter-compliance.sh PASSED
- [x] `tools` field is array [Read, Grep, Glob] - **Phase:** 3 - **Evidence:** test-ac2-yaml-frontmatter-compliance.sh PASSED
- [x] `model` field present (sonnet) - **Phase:** 3 - **Evidence:** test-ac2-yaml-frontmatter-compliance.sh PASSED

### AC#3: System Prompt Fresh-Context Technique

- [x] Prompt mentions "fresh context" or equivalent - **Phase:** 3 - **Evidence:** test-ac3-fresh-context-technique.sh PASSED
- [x] Prompt explicitly states no prior implementation knowledge - **Phase:** 3 - **Evidence:** test-ac3-fresh-context-technique.sh PASSED

### AC#4: Single Responsibility Enforcement

- [x] Description indicates AC verification only - **Phase:** 3 - **Evidence:** test-ac4-single-responsibility.sh PASSED
- [x] No implementation-related instructions - **Phase:** 3 - **Evidence:** test-ac4-single-responsibility.sh PASSED

### AC#5: Tool Restriction Compliance

- [x] Write tool NOT in tools array - **Phase:** 3 - **Evidence:** test-ac5-tool-restriction-compliance.sh PASSED
- [x] Edit tool NOT in tools array - **Phase:** 3 - **Evidence:** test-ac5-tool-restriction-compliance.sh PASSED
- [x] Bash tool NOT in tools array - **Phase:** 3 - **Evidence:** test-ac5-tool-restriction-compliance.sh PASSED
- [x] WebFetch tool NOT in tools array - **Phase:** 3 - **Evidence:** test-ac5-tool-restriction-compliance.sh PASSED

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Subagent file created at `.claude/agents/ac-compliance-verifier.md`
- [x] YAML frontmatter with name, description, tools, model fields
- [x] System prompt with fresh-context verification instructions
- [x] Tool list restricted to [Read, Grep, Glob]

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Frontmatter validates against YAML spec
- [x] No prohibited tools in tools array
- [x] File under 500 lines

### Testing
- [x] Unit tests for frontmatter validation
- [x] Unit tests for tool restriction
- [x] Integration test for Claude Code Terminal discovery

### Documentation
- [x] Subagent added to source-tree.md registry
- [x] Subagent added to CLAUDE.md subagent registry
- [x] Description explains when to invoke

---

## Implementation Notes

- [x] Unit tests for frontmatter validation - Completed: Phase 02, test-ac2-yaml-frontmatter-compliance.sh
- [x] Unit tests for tool restriction - Completed: Phase 02, test-ac5-tool-restriction-compliance.sh, test-br001-read-only-enforcement.sh
- [x] Subagent file created at `.claude/agents/ac-compliance-verifier.md` - Completed: Phase 03
- [x] YAML frontmatter with name, description, tools, model fields - Completed: Phase 03
- [x] System prompt with fresh-context verification instructions - Completed: Phase 03
- [x] Tool list restricted to [Read, Grep, Glob] - Completed: Phase 03

### Test Suite Created (Phase 02)
- 9 test files in `devforgeai/tests/STORY-269/`
- Tests cover all 5 ACs + 3 Business Rules + 1 NFR
- TDD Red Phase: 9/9 tests failing (expected)

### Implementation (Phase 03)
- Subagent file: 272 lines
- All 9 tests GREEN
- Context validation: ALL 6 CONTEXT FILES PASS
- Test regex fixes applied for proper ERE alternation syntax

### Documentation Updates (Phase 06)
- [x] Integration test for Claude Code Terminal discovery - Completed: Phase 05
- [x] Subagent added to source-tree.md registry - Completed: Phase 06 (32 agents total)
- [x] Subagent added to CLAUDE.md subagent registry - Completed: Phase 06
- [x] Description explains when to invoke - Completed: Phase 03 (lines 17-25)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 14:30 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 1.1 | STORY-269.story.md |
| 2026-01-19 12:49 | claude/test-automator | Red (Phase 02) | Generated 9 test files for AC verification | devforgeai/tests/STORY-269/*.sh |
| 2026-01-19 13:20 | claude/backend-architect | Green (Phase 03) | Created ac-compliance-verifier subagent (272 lines), fixed test regex | .claude/agents/ac-compliance-verifier.md, devforgeai/tests/STORY-269/*.sh |
| 2026-01-19 | claude/opus | Dev Complete (Phase 07) | All 10 TDD phases completed, registries updated, DoD 100% | source-tree.md, CLAUDE.md, STORY-269.story.md |
| 2026-01-19 | claude/qa-result-interpreter | QA Deep | PASSED: 9/9 tests, 0 violations, security 9/10 | devforgeai/qa/reports/STORY-269-qa-report.md |

## Notes

**Design Decisions:**
- Tool restriction to [Read, Grep, Glob] enforces read-only access per principle of least privilege
- Model set to 'sonnet' for balanced performance/capability
- Fresh-context technique codified from manual workaround in BRAINSTORM-005

**Open Questions:**
- None

**Related ADRs:**
- None yet (may create ADR for fresh-context verification pattern)

**References:**
- EPIC-046: AC Compliance Verification System
- BRAINSTORM-005: 100% Spec Compliance
- source-tree.md: Subagent location conventions
- architecture-constraints.md: Single responsibility principle
