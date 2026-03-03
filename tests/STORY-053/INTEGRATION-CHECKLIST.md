# STORY-053: Test Suite Integration Checklist

## Quick Reference

**Test Suite Version**: 1.0
**Story ID**: STORY-053
**Story Title**: Framework-Internal Guidance Reference
**File Under Test**: `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`

**Total Tests**: 76 (across 6 test suites)
**Expected Pass Rate (Complete File)**: 100% (76/76)

---

## Test Suite Overview

| Suite | File | Language | Tests | AC Coverage |
|-------|------|----------|-------|-------------|
| Pattern Structure | `test-pattern-structure.sh` | Bash | 14 | AC#1 |
| Template Syntax | `test-template-syntax.py` | Python | 15 | AC#2 |
| Quantification Table | `test-quantification-table.py` | Python | 14 | AC#3 |
| Skill Integration | `test-skill-integration.sh` | Bash | 14 | AC#4 |
| Framework Alignment | `test-framework-alignment.sh` | Bash | 11 | AC#5 |
| Performance & NFR | `test-performance.py` | Python | 8 | NFR-001,002,003 |
| **TOTAL** | | | **76** | **All AC + NFR** |

---

## Acceptance Criteria Validation Matrix

### AC#1: Pattern Completeness ✓
**Test File**: `test-pattern-structure.sh`
**Pass Criteria**: All 14 tests pass

| Test | Requirement | Evidence | Status |
|------|-------------|----------|--------|
| File exists | File location valid | File found at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` | ☐ |
| Pattern count | 10-15 patterns | `grep -c "^### Pattern"` returns 10-15 | ☐ |
| Functional patterns | 3-4 patterns | Pattern type count validation | ☐ |
| NFR patterns | 2-3 patterns | Pattern type count validation | ☐ |
| Edge case patterns | 2-3 patterns | Pattern type count validation | ☐ |
| Integration patterns | 2-3 patterns | Pattern type count validation | ☐ |
| Constraint patterns | 1-2 patterns | Pattern type count validation | ☐ |
| Problem sections | One per pattern | All patterns have `#### Problem` | ☐ |
| Solution sections | One per pattern | All patterns have `#### Solution` | ☐ |
| Template sections | One per pattern | All patterns have AskUserQuestion | ☐ |
| Example sections | One per pattern | All patterns have `#### Example` | ☐ |
| Cross-references | Pattern links present | Related patterns documented | ☐ |
| Problem quality | 2-3 sentences | Problem descriptions have content | ☐ |
| Solution quality | Step-by-step | Solutions have numbered/bulleted steps | ☐ |
| Example context | DevForgeAI references | Examples mention STORY-/EPIC-/skill/workflow | ☐ |

**Pass Condition**: ✓ If 14/14 tests pass

---

### AC#2: Template Usability ✓
**Test File**: `test-template-syntax.py`
**Pass Criteria**: All 15 tests pass

| Test | Requirement | Evidence | Status |
|------|-------------|----------|--------|
| File exists | File present | File readable | ☐ |
| Template count | 20-30 templates | AskUserQuestion( count | ☐ |
| Valid YAML | Proper syntax | Parsing succeeds | ☐ |
| Question field | Required in all | `question:` present in all | ☐ |
| Header field | Required in all | `header:` present in all | ☐ |
| Options array | Required in all | `options:` present in all | ☐ |
| Option count | 3-5 per template | Option count validation | ☐ |
| Label field | Required in all | `label:` in all options | ☐ |
| Description field | Required in all | `description:` in all options | ☐ |
| MultiSelect field | Required in all | `multiSelect:` specified | ☐ |
| Functional templates | 3+ templates | Template type coverage | ☐ |
| NFR templates | 3+ templates | Template type coverage | ☐ |
| Edge case templates | 3+ templates | Template type coverage | ☐ |
| Integration templates | 3+ templates | Template type coverage | ☐ |
| Constraint templates | 2+ templates | Template type coverage | ☐ |
| Customization notes | Present | Each template includes guidance | ☐ |

**Pass Condition**: ✓ If 15/15 tests pass

---

### AC#3: NFR Quantification Accuracy ✓
**Test File**: `test-quantification-table.py`
**Pass Criteria**: All 14 tests pass

| Test | Requirement | Evidence | Status |
|------|-------------|----------|--------|
| File exists | File present | File readable | ☐ |
| Table exists | Quantification section | "quantification" or "vague term" in content | ☐ |
| Table parsed | Table extractable | Rows identified and parsed | ☐ |
| Vague term count | ≥15 terms | Count validation | ☐ |
| Measurable ranges | All terms have ranges | Numeric values or percentiles present | ☐ |
| Numeric values | Specific measurements | Numbers (ms, %, Mbps, etc.) present | ☐ |
| Percentiles | Alternative metrics | p95, p99, median, etc. if applicable | ☐ |
| DevForgeAI examples | Context references | QA times, story metrics cited | ☐ |
| Template references | Links to templates | Each term has template link | ☐ |
| Performance targets | latency, throughput, response time | ≥3 types | ☐ |
| Security/Reliability targets | encryption, uptime, SLA | ≥2 types | ☐ |
| Scalability targets | users, load, capacity | ≥3 types | ☐ |
| Usability targets | learning, satisfaction, error rate | ≥2 types | ☐ |
| Unmapped terms | Fallback guidance | Guidance for terms not in table | ☐ |

**Pass Condition**: ✓ If 14/14 tests pass

---

### AC#4: Skill Integration Success ✓
**Test File**: `test-skill-integration.sh`
**Pass Criteria**: All 14 tests pass

| Test | Requirement | Evidence | Status |
|------|-------------|----------|--------|
| File exists | File location valid | File found and readable | ☐ |
| 5 skill integrations | All skills documented | References found for all 5 | ☐ |
| Workflow phases | Each skill phase specified | "Phase X Step Y" documented | ☐ |
| Use cases | 3-5 per skill | Use cases enumerated | ☐ |
| Read commands | Syntactically valid | `Read(` pattern found | ☐ |
| File path reference | Correct path | Path to user-input-guidance.md cited | ☐ |
| Path format | Absolute path | `.claude/skills/` or `src/` prefix | ☐ |
| Grep performance | <30s search | Time measurement <30,000ms | ☐ |
| Single file | Only one exists | 1 user-input-guidance.md file found | ☐ |
| 5 skills reference | All reference file | All 5 skill SKILL.md files reference it | ☐ |
| Ideation documented | Integration present | devforgeai-ideation section found | ☐ |
| Story-Creation documented | Integration present | devforgeai-story-creation section found | ☐ |
| Architecture documented | Integration present | devforgeai-architecture section found | ☐ |
| UI-Generator documented | Integration present | devforgeai-ui-generator section found | ☐ |
| Orchestration documented | Integration present | devforgeai-orchestration section found | ☐ |

**Pass Condition**: ✓ If 14/14 tests pass

---

### AC#5: Framework Alignment ✓
**Test File**: `test-framework-alignment.sh`
**Pass Criteria**: All 11 tests pass

| Test | Requirement | Evidence | Status |
|------|-------------|----------|--------|
| File exists | File present | File readable | ☐ |
| Context files | All 6 cited | tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns | ☐ |
| Quality gates | Gate 1-4 referenced | Gate definitions match CLAUDE.md | ☐ |
| Workflow states | States correct | Backlog, Architecture, Ready for Dev, etc. | ☐ |
| Story structure | YAML, AC, tech specs | Correct terminology used | ☐ |
| Core concepts | DoD, TDD, AAA present | Framework concepts referenced | ☐ |
| File path format | .claude/ or devforgeai/ | Only framework paths used | ☐ |
| No external URLs | 0 external references | http://, https://, www. not present | ☐ |
| Framework files exist | Referenced files valid | Sample files: CLAUDE.md, skills-reference.md, tech-stack.md | ☐ |
| Prompting guide reference | 2+ references | Cross-references to effective-prompting-guide.md | ☐ |
| Claude Code reference | 2+ references | Cross-references to claude-code-terminal-expert | ☐ |

**Pass Condition**: ✓ If 11/11 tests pass

---

## NFR Validation Matrix

| NFR | Category | Requirement | Test | Target | Status |
|-----|----------|-------------|------|--------|--------|
| NFR-001 | Performance | File load <500ms | `test-performance.py` | <500ms | ☐ |
| NFR-002 | Performance | Grep search <30s | `test-skill-integration.sh` | <30s | ☐ |
| NFR-003 | Performance | Token count ≤3,000 | `test-performance.py` | ≤3,000 tokens | ☐ |
| NFR-004 | Usability | Template usage ≥90% | Manual (Phase 4) | ≥90% | ☐ |
| NFR-005 | Usability | NFR quantification ≥85% | Manual (Phase 4) | ≥85% | ☐ |
| NFR-006 | Maintainability | Document versioned | Manual (Phase 2) | semver format | ☐ |
| NFR-007 | Quality | Pattern coverage ≥90% | Manual (Phase 4) | ≥90% | ☐ |
| NFR-008 | Quality | Template completeness ≥80% | Manual (Phase 4) | ≥80% | ☐ |
| NFR-009 | Reusability | 5 skills use same file | `test-skill-integration.sh` | 5 skills | ☐ |
| NFR-010 | Scalability | 30-50 patterns support | Manual (Future) | <30s search | ☐ |

---

## Test Execution Checklist

### Pre-Execution
- [ ] All 6 test files exist in `tests/STORY-053/`
  - [ ] `test-pattern-structure.sh` (bash script)
  - [ ] `test-template-syntax.py` (python3)
  - [ ] `test-quantification-table.py` (python3)
  - [ ] `test-skill-integration.sh` (bash script)
  - [ ] `test-framework-alignment.sh` (bash script)
  - [ ] `test-performance.py` (python3)
  - [ ] `run_all_tests.sh` (test runner)

- [ ] Target file location determined:
  - [ ] Path: `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
  - [ ] OR: `.claude/skills/devforgeai-ideation/references/user-input-guidance.md`

- [ ] Test environment ready:
  - [ ] Bash available (`bash --version`)
  - [ ] Python3 available (`python3 --version`)
  - [ ] Grep available (`grep --version`)

### Execution
- [ ] Run test suite: `bash tests/STORY-053/run_all_tests.sh`
- [ ] OR run individual tests as needed

### Post-Execution
- [ ] Review test output for each suite
- [ ] Identify failures by AC/NFR
- [ ] Use failure messages to guide implementation

---

## How Tests Prove Acceptance Criteria

### How AC#1 is Proven
```
Step 1: Run test-pattern-structure.sh
Step 2: Verify pattern count output: "Found 12 patterns (10-15 required)"
Step 3: Verify category counts:
  - Functional patterns: "Found 4 functional patterns (3-4 required)"
  - NFR patterns: "Found 3 NFR patterns (2-3 required)"
  - [etc. for all categories]
Step 4: Verify each pattern has all sections:
  - "All 12 patterns have Problem sections"
  - "All 12 patterns have Solution sections"
  - "All 12 patterns have AskUserQuestion templates"
  - "All 12 patterns have Example sections"

PROOF: All 4 assertions pass = AC#1 complete
```

### How AC#2 is Proven
```
Step 1: Run test-template-syntax.py
Step 2: Verify template count: "Found 25 templates (20-30 required)"
Step 3: Verify field presence in all templates:
  - "Found 25 question fields"
  - "Found 25 header fields"
  - "Found 25 options arrays"
Step 4: Verify option count per template:
  - "All 25 templates have 3-5 options"
Step 5: Verify scenario coverage:
  - "Found 4 functional specification templates"
  - "Found 3 NFR templates"
  - [etc. for all scenarios]
Step 6: Verify customization guidance:
  - "Found 25 customization guidance references"

PROOF: All 6+ assertions pass = AC#2 complete
```

### How AC#3 is Proven
```
Step 1: Run test-quantification-table.py
Step 2: Verify table exists: "Quantification/NFR table section found"
Step 3: Verify vague term count: "Found 18 vague terms (≥15 required)"
Step 4: Verify measurable ranges: "Found 42 numeric metrics or percentiles"
Step 5: Verify examples: "Found 12 DevForgeAI context references in examples"
Step 6: Verify table format: "Table uses markdown format"
Step 7: Verify template references: "Found 10 template references"

PROOF: All 7+ assertions pass = AC#3 complete
```

### How AC#4 is Proven
```
Step 1: Run test-skill-integration.sh
Step 2: Verify file exists and is loadable: "File exists: user-input-guidance.md"
Step 3: Verify 5 skills documented: "Found integration references for 5 skills"
Step 4: Verify Read commands: "Found 8 Read command references"
Step 5: Verify Grep performance: "Grep search completed in 15ms (< 30s required)"
Step 6: Verify single file: "Single guidance file found"
Step 7: Verify all 5 skills reference it: "All 5 skills reference the guidance file"
Step 8: Verify each skill integration:
  - "Ideation skill integration found"
  - "Story-Creation skill integration found"
  - [etc. for all 5 skills]

PROOF: All 8+ assertions pass = AC#4 complete
```

### How AC#5 is Proven
```
Step 1: Run test-framework-alignment.sh
Step 2: Verify context files: "All 6 context files referenced in guidance"
Step 3: Verify quality gates: "Found 4/4 quality gates referenced"
Step 4: Verify workflow states: "Found 4/4 workflow states referenced"
Step 5: Verify story structure: "Found 3/3 story structure elements referenced"
Step 6: Verify core concepts: "Found 3/3 core concept references"
Step 7: Verify file path format: "Found framework file references"
Step 8: Verify no external URLs: "No external URLs found"
Step 9: Verify referenced files exist: "Framework files exist"
Step 10: Verify CLAUDE.md consistency: "Found 3 matching terminology with CLAUDE.md"
Step 11: Verify cross-references:
  - "Found 2+ references to prompting guide"
  - "Found 2+ references to Claude Code expert"

PROOF: All 11+ assertions pass = AC#5 complete
```

---

## Implementation Progress Tracking

### Phase 1: File Creation (Red → Green)
```
Status: ⚪ Not Started

Actions:
1. Create directory: src/claude/skills/devforgeai-ideation/references/
2. Create file: user-input-guidance.md
3. Run tests: bash tests/STORY-053/test-pattern-structure.sh
   Expected: 2/14 PASS (file exists checks)
4. Add content incrementally
5. Rerun tests after each section
```

### Phase 2: Pattern Section (Red → Yellow → Green)
```
Status: ⚪ Not Started

Actions:
1. Add 10-15 patterns with all required sections
2. Ensure categories covered: Functional (3-4), NFR (2-3), Edge (2-3), Integration (2-3), Constraint (1-2)
3. Run tests: bash tests/STORY-053/test-pattern-structure.sh
   Expected: 14/14 PASS when complete
4. All other tests still failing (waiting for templates, table, etc.)
```

### Phase 3: Template Section (Red → Yellow → Green)
```
Status: ⚪ Not Started

Actions:
1. Add 20-30 AskUserQuestion templates
2. Ensure all have: question, header, options (3-5), multiSelect
3. Ensure scenario coverage: Functional (3+), NFR (3+), Edge (3+), Integration (3+), Constraint (2+)
4. Run tests: python3 tests/STORY-053/test-template-syntax.py
   Expected: 15/15 PASS when complete
5. Patterns still passing, other tests still failing
```

### Phase 4: Quantification Section (Red → Yellow → Green)
```
Status: ⚪ Not Started

Actions:
1. Add NFR quantification table
2. Include ≥15 vague terms with measurable ranges
3. Add DevForgeAI examples
4. Add template references
5. Run tests: python3 tests/STORY-053/test-quantification-table.py
   Expected: 14/14 PASS when complete
6. Patterns + Templates still passing, others still failing
```

### Phase 5: Integration Section (Red → Yellow → Green)
```
Status: ⚪ Not Started

Actions:
1. Add integration sections for 5 skills
2. Document workflow phases and use cases
3. Add Read commands for each skill
4. Run tests: bash tests/STORY-053/test-skill-integration.sh
   Expected: 14/14 PASS when complete
5. Pattern, Template, Quantification passing, alignment still failing
```

### Phase 6: Framework Alignment (Red → Yellow → Green)
```
Status: ⚪ Not Started

Actions:
1. Add framework terminology references
2. Cite all 6 context files
3. Reference quality gates, workflow states, story structure
4. Add cross-references to prompting guide and Claude Code expert
5. Run tests: bash tests/STORY-053/test-framework-alignment.sh
   Expected: 11/11 PASS when complete
6. All 5 test suites passing, performance still pending
```

### Phase 7: Performance Validation (Red → Yellow → Green)
```
Status: ⚪ Not Started

Actions:
1. Verify file structure is optimized
2. Check file size < 500KB
3. Ensure good searchability
4. Run tests: python3 tests/STORY-053/test-performance.py
   Expected: 8/8 PASS when complete
5. All 6 test suites passing = STORY-053 COMPLETE
```

### Final Status
```
Expected Outcome:
✓ test-pattern-structure.sh: 14/14 PASS
✓ test-template-syntax.py: 15/15 PASS
✓ test-quantification-table.py: 14/14 PASS
✓ test-skill-integration.sh: 14/14 PASS
✓ test-framework-alignment.sh: 11/11 PASS
✓ test-performance.py: 8/8 PASS

TOTAL: 76/76 PASS (100%) ✓✓✓

All Acceptance Criteria Met: ✓
All NFRs Validated: ✓
Story Ready for QA: ✓
```

---

## Success Metrics Summary

| Metric | Target | How Measured | Owner |
|--------|--------|--------------|-------|
| Pattern count | 10-15 | test-pattern-structure.sh | TDD (test first) |
| Template count | 20-30 | test-template-syntax.py | TDD (test first) |
| Vague terms | ≥15 | test-quantification-table.py | TDD (test first) |
| Skill integrations | 5 skills | test-skill-integration.sh | TDD (test first) |
| Framework terminology | 100% match | test-framework-alignment.sh | TDD (test first) |
| File load time | <500ms | test-performance.py | TDD (test first) |
| Grep search time | <30s | test-skill-integration.sh | TDD (test first) |
| Token overhead | ≤3,000 | test-performance.py | TDD (test first) |
| AC#1 completion | All tests pass | test-pattern-structure.sh | Implementation |
| AC#2 completion | All tests pass | test-template-syntax.py | Implementation |
| AC#3 completion | All tests pass | test-quantification-table.py | Implementation |
| AC#4 completion | All tests pass | test-skill-integration.sh | Implementation |
| AC#5 completion | All tests pass | test-framework-alignment.sh | Implementation |
| Re-invocation reduction | ≥30% | Manual measurement (Phase 4) | QA |
| Pattern applicability | ≥90% | Manual survey (Phase 4) | QA |
| Template completeness | ≥80% | Manual measurement (Phase 4) | QA |

---

## Test Result Template

### For Documentation
```markdown
## Test Results - [Date]

### Test Execution Summary
- Execution Date: YYYY-MM-DD
- Executor: [Name]
- Environment: [OS, Python, Bash versions]

### Test Results by Suite

#### Suite 1: Pattern Structure
- File: test-pattern-structure.sh
- Status: ✓ PASSED / ✗ FAILED
- Tests: 14/14 passed

#### Suite 2: Template Syntax
- File: test-template-syntax.py
- Status: ✓ PASSED / ✗ FAILED
- Tests: 15/15 passed

[... etc. for all 6 suites]

### Overall Results
- Total Tests: 76
- Passed: 76
- Failed: 0
- Success Rate: 100%

### Acceptance Criteria Status
- AC#1 Pattern Completeness: ✓ PASS
- AC#2 Template Usability: ✓ PASS
- AC#3 NFR Quantification: ✓ PASS
- AC#4 Skill Integration: ✓ PASS
- AC#5 Framework Alignment: ✓ PASS

### Next Steps
- [ ] Move story to QA phase
- [ ] Schedule manual validation
- [ ] Update skill SKILL.md files with cross-references
```

---

**Document Version**: 1.0
**Created**: 2025-01-20
**Last Updated**: 2025-01-20
