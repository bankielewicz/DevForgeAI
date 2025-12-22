# STORY-053: Framework-Internal Guidance Reference - Test Suite

## Overview

This test suite validates the creation and quality of `user-input-guidance.md`, a framework-internal reference file that provides proven patterns, templates, and quantification tables for requirements elicitation.

**Purpose**: Ensure the guidance document is complete, accurate, well-integrated, and aligned with DevForgeAI terminology.

**Status**: Tests are written to FAIL initially (RED phase - TDD). They pass when the `user-input-guidance.md` file is created with proper content.

---

## Test Files

### 1. `test-pattern-structure.sh` - AC1 Validation
**Purpose**: Validate Pattern Completeness (10-15 patterns with required sections)

**Tests**:
- Pattern count is 10-15 (overall validation)
- Functional patterns (3-4)
- NFR patterns (2-3)
- Edge case patterns (2-3)
- Integration patterns (2-3)
- Constraint patterns (1-2)
- Each pattern has Problem section
- Each pattern has Solution section
- Each pattern has AskUserQuestion template
- Each pattern has Example section
- Patterns include cross-references
- Problem descriptions have adequate content
- Solutions include step-by-step guidance
- Examples reference DevForgeAI context

**Related Requirements**:
- AC#1: Pattern Completeness
- DOC-001: Create 10-15 elicitation patterns
- BR-001: All patterns must include AskUserQuestion template

**Example PASS Output**:
```
✓ PASS: Found 12 patterns (10-15 required)
✓ PASS: Found 4 functional patterns (3-4 required)
✓ PASS: All 12 patterns have Problem sections
✓ PASS: All 12 patterns have Solution sections
```

---

### 2. `test-template-syntax.py` - AC2 Validation
**Purpose**: Validate Template Usability (20-30 templates with correct syntax)

**Tests**:
- Template count is 20-30
- Valid AskUserQuestion syntax in templates
- Each template has 'question' field
- Each template has 'header' field
- Each template has 'options' array
- Each template has 3-5 options
- Options have 'label' field
- Options have 'description' field
- Each template specifies multiSelect property
- Functional specification templates (3+)
- NFR templates (3+)
- Edge case templates (3+)
- Integration templates (3+)
- Constraint templates (2+)
- Templates include customization guidance
- YAML syntax is valid and consistent

**Related Requirements**:
- AC#2: Template Usability
- DOC-002: Create 20-30 AskUserQuestion templates
- BR-002: All templates must have 3-5 options

**Example PASS Output**:
```
✓ PASS: Found 25 templates (20-30 required)
✓ PASS: Found 25 question fields
✓ PASS: All 25 templates have valid option count (3-5)
✓ PASS: Found 8/10 key terms with good density
```

---

### 3. `test-quantification-table.py` - AC3 Validation
**Purpose**: Validate NFR Quantification (≥15 vague terms with measurable ranges)

**Tests**:
- Quantification table exists
- Vague terms extracted (≥15)
- Vague terms have measurable target ranges
- Measurable ranges include numeric values or percentiles
- DevForgeAI context examples included
- Each quantification entry references a template
- Performance targets (latency, throughput, response time)
- Security/reliability targets
- Scalability targets (users, load, capacity)
- Usability targets (learning curve, error rate)
- Table uses proper markdown formatting
- Table has column headers
- Table has separator row
- Table has minimum required rows (≥15)
- Guidance provided for unmapped terms

**Related Requirements**:
- AC#3: NFR Quantification Accuracy
- DOC-003: Create NFR quantification table (≥15 vague terms)
- BR-003: Measurable targets must have numbers

**Example PASS Output**:
```
✓ PASS: Found 18 vague terms (≥15 required)
✓ PASS: Found 42 numeric metrics or percentiles
✓ PASS: Table has 22 rows (≥15 required)
✓ PASS: Found 3 performance target types
```

---

### 4. `test-skill-integration.sh` - AC4 Validation
**Purpose**: Validate Skill Integration (5 skills can load file, reduce re-invocations)

**Tests**:
- File exists at expected location
- 5 skill integration sections documented
- Each integration specifies workflow phase
- Use cases documented (3-5 per skill)
- Read commands syntactically correct
- Read commands reference correct file path
- File paths use correct absolute format
- Grep search completes in <30 seconds
- Only one user-input-guidance.md file exists
- All 5 skills reference the same guidance file
- Ideation skill integration documented
- Story-Creation skill integration documented
- Architecture skill integration documented
- UI-Generator skill integration documented
- Orchestration skill integration documented

**Related Requirements**:
- AC#4: Skill Integration Success
- DOC-004: Document integration for 5 skills
- NFR-002: Grep search <30 seconds
- NFR-009: Single file shared by all 5 skills

**Example PASS Output**:
```
✓ PASS: Found integration references for 5 skills
✓ PASS: Found 8 Read command references
✓ PASS: All 5 skills reference the guidance file
✓ PASS: Grep search completed in 15ms (< 30s required)
```

---

### 5. `test-framework-alignment.sh` - AC5 Validation
**Purpose**: Validate Framework Alignment (100% terminology match with framework docs)

**Tests**:
- Guidance references all 6 context files
- Context files mentioned by name (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
- Quality gates referenced (Gate 1-4)
- Workflow states correctly referenced
- Story structure terminology correct
- Core concepts (DoD, TDD, AAA) present
- File path references use correct format (.claude/ or devforgeai/)
- No external URLs (framework-only references)
- Referenced framework files exist
- Key terms match CLAUDE.md definitions
- Cross-references to effective-prompting-guide.md (2+)
- Cross-references to claude-code-terminal-expert (2+)

**Related Requirements**:
- AC#5: Framework Alignment
- DOC-005: Terminology consistency (100% match)
- BR-004: Patterns must cite DevForgeAI reference files

**Example PASS Output**:
```
✓ PASS: Found 6 context file references (≥6 required)
✓ PASS: All 6 context files referenced in guidance
✓ PASS: Found 4/4 quality gates referenced
✓ PASS: Found 3 matching terminology with CLAUDE.md
```

---

### 6. `test-performance.py` - NFR Validation
**Purpose**: Validate Performance Requirements (file load, search speed, token overhead)

**Tests**:
- File load time <500ms (NFR-001)
- File size <500KB
- File is optimized for Grep searches (NFR-002)
- Estimated Grep search time <30 seconds
- Token count ≤3,000 tokens (NFR-003)
- File has good structural markers
- Contains expected content sections (Pattern, Template, Quantification, Integration, Framework)
- Good keyword density for common searches
- File has searchable elements (>50)

**Related Requirements**:
- NFR-001: File load <500ms
- NFR-002: Grep search <30 seconds
- NFR-003: Token overhead ≤3,000
- NFR-004: ≥90% template usage without customization
- NFR-005: ≥85% vague NFR quantification success

**Example PASS Output**:
```
✓ PASS: File loads in 12.34ms (< 500ms required)
✓ PASS: File size: 125.5KB (< 500KB)
✓ PASS: Estimated 2,847 tokens (≤ 3,000 required)
✓ PASS: File has good structural markers (4/4 types)
```

---

## Running the Tests

### Run All Tests
```bash
bash tests/STORY-053/run_all_tests.sh
```

### Run Individual Test Suite
```bash
# Pattern structure
bash tests/STORY-053/test-pattern-structure.sh

# Template syntax
python3 tests/STORY-053/test-template-syntax.py

# Quantification table
python3 tests/STORY-053/test-quantification-table.py

# Skill integration
bash tests/STORY-053/test-skill-integration.sh

# Framework alignment
bash tests/STORY-053/test-framework-alignment.sh

# Performance
python3 tests/STORY-053/test-performance.py
```

---

## Test Execution Flow (TDD Red Phase)

### Initial State (Before Implementation)
```
File: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
Status: DOES NOT EXIST

Test Results: ALL FAIL
├─ test-pattern-structure.sh: 0/14 PASS
├─ test-template-syntax.py: 0/15 PASS
├─ test-quantification-table.py: 0/14 PASS
├─ test-skill-integration.sh: 0/14 PASS
├─ test-framework-alignment.sh: 0/11 PASS
└─ test-performance.py: 0/8 PASS

Total: 0/76 tests passing (RED PHASE - Expected)
```

### After File Creation (Before Content)
```
File: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
Status: EMPTY (File exists but no content)

Test Results: MOSTLY FAIL
├─ test-pattern-structure.sh: 2/14 PASS (file exists checks)
├─ test-template-syntax.py: 1/15 PASS (file exists checks)
├─ test-quantification-table.py: 1/14 PASS (file exists checks)
├─ test-skill-integration.sh: 1/14 PASS (file exists checks)
├─ test-framework-alignment.sh: 1/11 PASS (file exists checks)
└─ test-performance.py: 2/8 PASS (file metrics)

Total: 8/76 tests passing (Improving but still mostly RED)
```

### After Full Implementation
```
File: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
Status: COMPLETE (All content present and valid)

Test Results: ALL PASS
├─ test-pattern-structure.sh: 14/14 PASS
├─ test-template-syntax.py: 15/15 PASS
├─ test-quantification-table.py: 14/14 PASS
├─ test-skill-integration.sh: 14/14 PASS
├─ test-framework-alignment.sh: 11/11 PASS
└─ test-performance.py: 8/8 PASS

Total: 76/76 tests passing (GREEN PHASE - Success!)
```

---

## Acceptance Criteria Mapping

### AC#1: Pattern Completeness
- **Test**: `test-pattern-structure.sh`
- **Critical Tests**:
  - Pattern count: 10-15
  - Each pattern has Problem, Solution, Template, Example sections
  - Coverage across 5 categories (functional, NFR, edge case, integration, constraint)
- **Pass Criteria**: All pattern validation tests pass

### AC#2: Template Usability
- **Test**: `test-template-syntax.py`
- **Critical Tests**:
  - Template count: 20-30
  - Each template has question, header, options (3-5), customization notes
  - Coverage across 5 scenario types
- **Pass Criteria**: All template validation tests pass

### AC#3: NFR Quantification Accuracy
- **Test**: `test-quantification-table.py`
- **Critical Tests**:
  - Vague terms: ≥15
  - Measurable ranges with numeric values
  - DevForgeAI examples present
  - Table format is valid
- **Pass Criteria**: All quantification validation tests pass

### AC#4: Skill Integration Success
- **Test**: `test-skill-integration.sh`
- **Critical Tests**:
  - 5 skills documented (ideation, story-creation, architecture, ui-generator, orchestration)
  - Read commands valid and reference correct file path
  - Grep search <30 seconds
  - Single file shared by all 5 skills
- **Pass Criteria**: All integration validation tests pass

### AC#5: Framework Alignment
- **Test**: `test-framework-alignment.sh`
- **Critical Tests**:
  - All 6 context files referenced
  - Quality gates, workflow states, story structure terms correct
  - Framework-only references (no external URLs)
  - Cross-references to related guides
- **Pass Criteria**: All alignment validation tests pass

---

## Expected Test Results When File Complete

### Test Summary
```
STORY-053 Test Suite Results
=====================================

Test Suite 1: Pattern Structure
  Total: 14 | Passed: 14 | Failed: 0 ✓

Test Suite 2: Template Syntax
  Total: 15 | Passed: 15 | Failed: 0 ✓

Test Suite 3: Quantification Table
  Total: 14 | Passed: 14 | Failed: 0 ✓

Test Suite 4: Skill Integration
  Total: 14 | Passed: 14 | Failed: 0 ✓

Test Suite 5: Framework Alignment
  Total: 11 | Passed: 11 | Failed: 0 ✓

Test Suite 6: Performance
  Total: 8 | Passed: 8 | Failed: 0 ✓

OVERALL: 76/76 tests passing (100%) ✓✓✓
```

---

## Integration Checklist

### How Tests Prove Each Acceptance Criterion

#### AC#1 Proof
- [ ] `test-pattern-structure.sh` shows pattern count in range 10-15
- [ ] `test-pattern-structure.sh` shows each category has required count
- [ ] `test-pattern-structure.sh` shows all 4 required sections per pattern
- **Evidence**: Pattern structure test output with counts and section validation

#### AC#2 Proof
- [ ] `test-template-syntax.py` shows template count in range 20-30
- [ ] `test-template-syntax.py` shows all templates have required fields
- [ ] `test-template-syntax.py` shows option counts in range 3-5
- [ ] `test-template-syntax.py` shows coverage across 5 scenario types
- **Evidence**: Template syntax test output with field validation

#### AC#3 Proof
- [ ] `test-quantification-table.py` shows vague term count ≥15
- [ ] `test-quantification-table.py` shows measurable ranges with numbers
- [ ] `test-quantification-table.py` shows DevForgeAI examples present
- [ ] `test-quantification-table.py` shows valid table format
- **Evidence**: Quantification table test output with term/range validation

#### AC#4 Proof
- [ ] `test-skill-integration.sh` shows 5 skills documented
- [ ] `test-skill-integration.sh` shows valid Read commands
- [ ] `test-skill-integration.sh` shows file load <30s (Grep search)
- [ ] `test-skill-integration.sh` shows single file shared by 5 skills
- **Evidence**: Skill integration test output with integration validation

#### AC#5 Proof
- [ ] `test-framework-alignment.sh` shows 6 context files referenced
- [ ] `test-framework-alignment.sh` shows quality gates, workflow states, story structure terms
- [ ] `test-framework-alignment.sh` shows framework-only references
- [ ] `test-framework-alignment.sh` shows 100% terminology match
- **Evidence**: Framework alignment test output with terminology validation

---

## Implementation Guidance

### What the File Should Contain

1. **10-15 Patterns** with:
   - Problem Description (2-3 sentences)
   - Solution (step-by-step)
   - AskUserQuestion Template (copy-paste ready)
   - Example (real DevForgeAI scenario)
   - Related Patterns (cross-references)

2. **20-30 AskUserQuestion Templates** covering:
   - Functional specifications (3+)
   - Non-functional requirements (3+)
   - Edge cases (3+)
   - Integration points (3+)
   - Constraints (2+)

3. **NFR Quantification Table** with:
   - ≥15 vague terms (e.g., "fast", "scalable", "secure")
   - Measurable target ranges (with units: ms, %, Mbps, etc.)
   - DevForgeAI context examples
   - Template links/references
   - Handling for unmapped terms

4. **5 Skill Integration Sections** documenting:
   - Skill name (ideation, story-creation, architecture, ui-generator, orchestration)
   - Workflow phase and step references
   - Use cases (3-5 per skill)
   - Read command invocation

5. **Framework Terminology** ensuring:
   - 100% match with CLAUDE.md
   - References to all 6 context files
   - Quality gates (Gate 1-4)
   - Workflow states (Backlog → Released)
   - Story structure (YAML, Given/When/Then, tech specs)

### File Location
```
src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
```

---

## Performance Targets

| Metric | Target | Test |
|--------|--------|------|
| File load time (Read tool) | <500ms | `test-performance.py` |
| Grep search time | <30 seconds | `test-skill-integration.sh` |
| Token overhead | ≤3,000 tokens | `test-performance.py` |
| File size | <500KB | `test-performance.py` |
| Template usage without customization | ≥90% | Manual (NFR-004) |
| Vague NFR quantification success | ≥85% | Manual (NFR-005) |

---

## Notes for Developers

1. **TDD Approach**: Tests are written FIRST. They will fail until the guidance file is created with proper content.

2. **Test Independence**: Each test suite can run independently. They all depend on the same file, but validate different aspects.

3. **Failure Messages**: When tests fail, they show:
   - What was found (actual value)
   - What was expected (target value)
   - Context about why it matters

4. **Documentation Testing**: These tests validate MARKDOWN FILE CONTENT, not code implementation. They use text parsing and content analysis.

5. **Skill Integration**: Tests verify that 5 skills can reference the guidance file. The actual usage and "30% reduction in re-invocations" is measured manually during QA phase.

6. **Progressive Disclosure**: The guidance file should be progressive - patterns first (what to ask), templates second (how to ask), quantification third (how to measure), integrations fourth (where to use).

---

## Troubleshooting

### All Tests Fail with "File does not exist"
- Create the file: `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
- File must exist even if empty to progress past initial checks

### Pattern Tests Fail on Count
- Verify patterns use heading format: `### Pattern [name]`
- Check that required sections are properly formatted:
  - `#### Problem` (or `#### Problem:`)
  - `#### Solution`
  - `AskUserQuestion(` code block
  - `#### Example`

### Template Tests Fail on Syntax
- Verify YAML syntax in template blocks
- Check that all templates have: `question:`, `header:`, `options:`, `multiSelect:`
- Ensure options array has 3-5 items with `label:` and `description:`

### Quantification Tests Fail on Table
- Verify table uses markdown format with pipes: `| Column | Column |`
- Check that rows contain: vague term, measurable range (with numbers), example
- Ensure at least 15 different terms are present

### Integration Tests Fail on 5 Skills
- Verify all 5 skills are referenced: ideation, story-creation, architecture, ui-generator, orchestration
- Check that Read commands use correct path syntax: `Read(file_path="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md")`
- Verify 5 skill SKILL.md files reference the guidance file

### Alignment Tests Fail on Terminology
- Cross-reference all terms with CLAUDE.md
- Verify 6 context files are mentioned by name
- Check that no external URLs are present
- Ensure Quality Gate numbers (Gate 1, Gate 2, etc.) are correct

---

## File Structure Checklist

```markdown
# User Input Guidance [Reference File]

## Overview
- Describe purpose and scope

## Section 1: Elicitation Patterns (10-15 patterns)
### Pattern 1: [Name]
#### Problem
[Description]

#### Solution
[Steps]

#### Template
```
AskUserQuestion(...)
```

#### Example
[Real scenario]

#### Related Patterns
...

[Repeat for 10-15 patterns total]

## Section 2: AskUserQuestion Templates (20-30 templates)
### Functional Specification Templates
[3+ templates]

### Non-Functional Requirement Templates
[3+ templates]

[etc. for edge cases, integration, constraints]

## Section 3: NFR Quantification Table
| Vague Term | Measurable Range | Example | Template |
|------------|------------------|---------|----------|
| fast       | < 200ms          | [Example] | [Link] |
[≥15 more rows]

## Section 4: Skill Integration
### Integration: devforgeai-ideation
[Phases, use cases, Read command]

### Integration: devforgeai-story-creation
[Phases, use cases, Read command]

[etc. for 5 skills total]

## Section 5: Framework Terminology
[References to context files, quality gates, workflow states, story structure]
```

---

**Last Updated**: 2025-01-20
**Version**: 1.0
**Test Suite Version**: 1.0
