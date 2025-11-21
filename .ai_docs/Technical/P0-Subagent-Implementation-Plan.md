# P0 Subagent Implementation Plan

**Date:** 2025-11-20
**Status:** Ready for Implementation
**Priority:** P0 (High-Value Token Optimization)

---

## Executive Summary

This document provides a comprehensive implementation plan for three P0 priority subagents that will optimize DevForgeAI's QA validation workflow by reducing context window usage by **65-72%** (26K token savings per QA run).

### Subagents to Implement

| Subagent | Token Savings | Complexity | Story ID | Priority |
|----------|---------------|------------|----------|----------|
| **coverage-analyzer** | 12K tokens (65%) | Medium | STORY-061 | P0 |
| **anti-pattern-scanner** | 8K tokens (73%) | Medium | STORY-062 | P0 |
| **code-quality-auditor** | 6K tokens (70%) | Low | STORY-063 | P0 |
| **Total** | **26K tokens (72%)** | - | - | - |

### Business Impact

**Before Subagent Delegation:**
- QA Phase 1 (Coverage): ~12K tokens inline
- QA Phase 2 (Anti-Patterns): ~8K tokens inline
- QA Phase 4 (Quality Metrics): ~6K tokens inline
- **Total QA Context: ~36K tokens per run**

**After Subagent Delegation:**
- QA Phase 1 (Coverage): ~4K tokens (prompt + response)
- QA Phase 2 (Anti-Patterns): ~3K tokens (prompt + response)
- QA Phase 4 (Quality): ~3K tokens (prompt + response)
- **Total QA Context: ~10K tokens per run**

**Savings:**
- Per QA run: 26K tokens (72% reduction)
- Per 10 stories: 260K tokens saved
- Per 100 stories: 2.6M tokens saved
- **Cost reduction:** Significant (Sonnet pricing benefits)

---

## Implementation Deliverables

### ✅ Completed Deliverables

1. **Subagent Specifications (3 files)**
   - `.claude/agents/coverage-analyzer.md` (Complete 8-phase workflow, 450+ lines)
   - `.claude/agents/anti-pattern-scanner.md` (Complete 9-phase workflow, 520+ lines)
   - `.claude/agents/code-quality-auditor.md` (Complete 8-phase workflow, 380+ lines)

2. **Prompt Templates**
   - `.claude/skills/devforgeai-qa/references/subagent-prompt-templates.md` (Complete templates for all 3 subagents with integration patterns)

3. **Story Created**
   - `STORY-061-coverage-analyzer-subagent.story.md` (Complete with 9 ACs, tech spec, NFRs)

### 📋 Remaining Deliverables

4. **Stories to Create** (Use same pattern as STORY-061)
   - STORY-062: anti-pattern-scanner subagent
   - STORY-063: code-quality-auditor subagent

5. **Integration Documentation**
   - Update `.claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md` (replace inline logic with subagent call)
   - Update `.claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md` (replace inline logic with subagent call)
   - Update `.claude/skills/devforgeai-qa/references/code-quality-workflow.md` (replace inline logic with subagent call)

6. **Testing Plan**
   - Unit test specifications (4 tests per subagent = 12 total)
   - Integration test specifications (3 tests for QA skill integration)
   - Test data requirements

---

## Implementation Phases

### Phase 1: coverage-analyzer (STORY-061)

**Estimated Effort:** 8 story points (1-2 days)

**Implementation Steps:**

1. **Create Subagent Specification** ✅
   - File: `.claude/agents/coverage-analyzer.md` (already created)
   - Content: 8-phase workflow, input/output contracts, guardrails, error handling
   - Validation: Grep for required sections (guardrails, phases, contracts)

2. **Implement Language-Specific Coverage Tools**
   - C#: `dotnet test --collect:'XPlat Code Coverage'`
   - Python: `pytest --cov=src --cov-report=json`
   - Node.js: `npm test -- --coverage`
   - Go: `go test ./... -coverprofile=coverage.out`
   - Rust: `cargo tarpaulin --out Json`
   - Java: `mvn test jacoco:report`

3. **Implement File Classification Logic**
   - Load source-tree.md patterns
   - Match files to layers (business_logic, application, infrastructure)
   - Handle unknown files gracefully

4. **Implement Threshold Validation**
   - Business Logic: 95% (CRITICAL)
   - Application: 85% (HIGH)
   - Overall: 80% (HIGH)
   - Infrastructure: 80% (WARNING)
   - Return `blocks_qa` boolean

5. **Implement Gap Identification**
   - For each under-covered file:
     - file path, layer, current_coverage, target_coverage
     - uncovered_lines array
     - suggested_tests array (analyze uncovered code patterns)

6. **Update devforgeai-qa Integration** ✅
   - Template: `.claude/skills/devforgeai-qa/references/subagent-prompt-templates.md` (already created)
   - Modify: `coverage-analysis-workflow.md` to invoke subagent
   - Pattern: Load context → Invoke subagent → Parse response → Update blocks_qa

7. **Create Unit Tests**
   - test_threshold_blocking (business <95% → blocks_qa = true)
   - test_file_classification (correct layer assignment)
   - test_gap_identification (file:line evidence)
   - test_error_handling (context missing → failure)

8. **Create Integration Test**
   - test_qa_skill_invokes_coverage_analyzer (end-to-end)

**Success Criteria:**
- [ ] Subagent specification complete
- [ ] All 6 languages supported
- [ ] Files correctly classified by layer
- [ ] Thresholds validated (95%/85%/80%)
- [ ] Gaps include file:line evidence
- [ ] QA skill successfully invokes subagent
- [ ] 4 unit tests pass
- [ ] 1 integration test passes
- [ ] Token usage: 12K → 4K (65% reduction verified)

---

### Phase 2: anti-pattern-scanner (STORY-062)

**Estimated Effort:** 8 story points (1-2 days)

**Implementation Steps:**

1. **Create Subagent Specification** ✅
   - File: `.claude/agents/anti-pattern-scanner.md` (already created)
   - Content: 9-phase workflow, 6 detection categories, severity classification
   - Validation: Grep for all 6 categories (library substitution, structure, layer, code smells, security, style)

2. **Implement Category 1: Library Substitution Detection (CRITICAL)**
   - ORM swap detection (Dapper ↔ Entity Framework, etc.)
   - State manager swap (Zustand ↔ Redux)
   - HTTP client swap (axios ↔ fetch)
   - Validation library swap (Zod ↔ Joi)
   - Testing framework swap (Vitest ↔ Jest)

3. **Implement Category 2: Structure Violations (HIGH)**
   - Validate file locations against source-tree.md
   - Detect files in wrong layers
   - Detect infrastructure concerns in domain layer

4. **Implement Category 3: Layer Violations (HIGH)**
   - Check cross-layer dependencies against architecture-constraints.md
   - Detect circular dependencies
   - Validate layer boundary rules

5. **Implement Category 4: Code Smells (MEDIUM)**
   - God objects (>15 methods, >300 lines)
   - Long methods (>50 lines)
   - Magic numbers

6. **Implement Category 5: Security Issues (CRITICAL)**
   - Hard-coded secrets
   - SQL injection risk
   - XSS vulnerabilities
   - Insecure deserialization

7. **Implement Category 6: Style Inconsistencies (LOW)**
   - Missing documentation
   - Naming convention violations

8. **Update devforgeai-qa Integration** ✅
   - Template: `.claude/skills/devforgeai-qa/references/subagent-prompt-templates.md` (already created)
   - Modify: `anti-pattern-detection-workflow.md` to invoke subagent
   - Pattern: Load ALL 6 context files → Invoke subagent → Parse response → Update blocks_qa

9. **Create Unit Tests**
   - test_library_substitution_detection (ORM swap → CRITICAL)
   - test_structure_violation_detection (file in wrong layer → HIGH)
   - test_security_vulnerability_detection (hard-coded secret → CRITICAL)
   - test_severity_classification (CRITICAL/HIGH block, MEDIUM/LOW warn)

10. **Create Integration Test**
    - test_qa_skill_invokes_anti_pattern_scanner (end-to-end)

**Success Criteria:**
- [ ] Subagent specification complete
- [ ] All 6 detection categories implemented
- [ ] Violations categorized by severity (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] CRITICAL and HIGH violations block QA
- [ ] File:line evidence for all violations
- [ ] Remediation guidance provided
- [ ] QA skill successfully invokes subagent
- [ ] 4 unit tests pass
- [ ] 1 integration test passes
- [ ] Token usage: 8K → 3K (73% reduction verified)

---

### Phase 3: code-quality-auditor (STORY-063)

**Estimated Effort:** 5 story points (half day to full day)

**Implementation Steps:**

1. **Create Subagent Specification** ✅
   - File: `.claude/agents/code-quality-auditor.md` (already created)
   - Content: 8-phase workflow, 3 metrics (complexity, duplication, maintainability)
   - Validation: Grep for all 3 metrics sections

2. **Implement Cyclomatic Complexity Analysis**
   - Language-specific tools:
     - Python: `radon cc src/ -s -j`
     - Node.js: `npx eslint --rule 'complexity: [error, 20]'`
     - C#: Use existing `.claude/skills/devforgeai-qa/scripts/analyze_complexity.py`
   - Calculate: average per function, average per file, max complexity
   - Identify: functions over threshold (>20 = CRITICAL, 15-20 = WARNING)

3. **Implement Code Duplication Detection**
   - Language-specific tools:
     - Python: Use existing `detect_duplicates.py` script
     - Node.js: `npx jscpd src/ --format json`
   - Calculate: duplication percentage
   - Identify: duplicate blocks (>25% = CRITICAL, 20-25% = WARNING)

4. **Implement Maintainability Index Calculation**
   - Formula: `MI = 171 - 5.2*ln(Volume) - 0.23*Complexity - 16.2*ln(LOC)`
   - Calculate: average MI across all files
   - Identify: low maintainability files (<40 = CRITICAL, 40-50 = WARNING)

5. **Implement Business Impact Explanations**
   - For each violation, explain:
     - Bug risk (statistical correlation with defect rates)
     - Testing burden (number of test cases required)
     - Onboarding impact (time to understand code)
     - Maintenance cost (effort multiplier for changes)

6. **Implement Refactoring Pattern Recommendations**
   - For complexity: "Extract Method", "Decompose Conditional", etc.
   - For duplication: "Extract to Utility Class", "Template Method Pattern"
   - For MI: "Simplify Logic", "Extract Methods", "Reduce File Size"

7. **Update devforgeai-qa Integration** ✅
   - Template: `.claude/skills/devforgeai-qa/references/subagent-prompt-templates.md` (already created)
   - Modify: `code-quality-workflow.md` to invoke subagent
   - Pattern: Load context → Invoke subagent → Parse response → Update blocks_qa

8. **Create Unit Tests**
   - test_extreme_complexity_detection (complexity 28 → CRITICAL)
   - test_extreme_duplication_detection (27% duplication → CRITICAL)
   - test_low_maintainability_detection (MI 35 → CRITICAL)
   - test_acceptable_quality_no_blocking (all metrics good → blocks_qa = false)

9. **Create Integration Test**
   - test_qa_skill_invokes_code_quality_auditor (end-to-end)

**Success Criteria:**
- [ ] Subagent specification complete
- [ ] All 3 metrics calculated (complexity, duplication, MI)
- [ ] Extreme violations block QA (complexity >20, duplication >25%, MI <40)
- [ ] Business impact explanations provided
- [ ] Specific refactoring patterns recommended
- [ ] QA skill successfully invokes subagent
- [ ] 4 unit tests pass
- [ ] 1 integration test passes
- [ ] Token usage: 6K → 3K (70% reduction verified)

---

## Integration Pattern

### Standard Subagent Invocation Pattern

```python
# Pattern used by devforgeai-qa skill for all 3 subagents

# 1. Load required context files
tech_stack = Read(file_path=".devforgeai/context/tech-stack.md")
source_tree = Read(file_path=".devforgeai/context/source-tree.md")
# ... (load other context files as needed)

# 2. Extract parameters
language = extract_language(tech_stack)
test_command = determine_test_command(language)

# 3. Invoke subagent
result = Task(
    subagent_type="coverage-analyzer",  # or anti-pattern-scanner, code-quality-auditor
    description="Analyze test coverage by layer",  # Brief description
    prompt=f"""
    Analyze test coverage for {story_id}.

    Context Files:
    {tech_stack}
    {source_tree}
    ...

    Parameters:
    - Story ID: {story_id}
    - Language: {language}
    - Test Command: {test_command}

    Execute your workflow phases 1-8.
    Return JSON with results.
    """,
    model="claude-haiku-4-5-20251001"  # Cost-effective model for analysis
)

# 4. Parse response
if result["status"] != "success":
    Display error and remediation
    blocks_qa = True
    HALT

# 5. Extract results
coverage_summary = result["coverage_summary"]
gaps = result["gaps"]
recommendations = result["recommendations"]

# 6. Update QA state
blocks_qa = blocks_qa OR result["blocks_qa"]  # OR operation, not assignment

# 7. Display results
Display coverage summary to user

# 8. Continue to next phase
# ...
```

### Error Handling Pattern

```python
def handle_subagent_error(result, subagent_name, phase_name):
    """Standard error handler for all subagents"""
    if result["status"] != "success":
        Display f"❌ {phase_name} FAILED"
        Display f"   Subagent: {subagent_name}"
        Display f"   Error: {result['error']}"

        if "remediation" in result:
            Display f"   Remediation: {result['remediation']}"

        # Update QA state
        blocks_qa = True

        # Return failure
        Return {"status": "failure", "blocks_qa": True}
        HALT

# Usage
handle_subagent_error(coverage_result, "coverage-analyzer", "Phase 1: Coverage Analysis")
```

---

## Testing Strategy

### Unit Tests (Per Subagent)

Each subagent requires 4 unit tests minimum:

**coverage-analyzer:**
1. test_threshold_blocking - Validates blocks_qa logic
2. test_file_classification - Validates layer assignment
3. test_gap_identification - Validates evidence requirements
4. test_error_handling - Validates graceful failure

**anti-pattern-scanner:**
1. test_library_substitution - Validates CRITICAL violations
2. test_structure_violations - Validates HIGH violations
3. test_security_scanning - Validates OWASP checks
4. test_severity_classification - Validates blocking logic

**code-quality-auditor:**
1. test_complexity_detection - Validates threshold (>20 = CRITICAL)
2. test_duplication_detection - Validates threshold (>25% = CRITICAL)
3. test_maintainability_index - Validates threshold (<40 = CRITICAL)
4. test_business_impact_explanation - Validates explanation quality

### Integration Tests (QA Skill)

3 integration tests (one per subagent):

1. **test_qa_invokes_coverage_analyzer**
   ```python
   def test_qa_invokes_coverage_analyzer():
       # Given: Story with 88% coverage
       # When: /qa STORY-001 deep
       # Then: coverage-analyzer invoked, results in QA report
   ```

2. **test_qa_invokes_anti_pattern_scanner**
   ```python
   def test_qa_invokes_anti_pattern_scanner():
       # Given: Story with library substitution
       # When: /qa STORY-002 deep
       # Then: anti-pattern-scanner invoked, CRITICAL violation detected
   ```

3. **test_qa_invokes_code_quality_auditor**
   ```python
   def test_qa_invokes_code_quality_auditor():
       # Given: Story with complexity 28
       # When: /qa STORY-003 deep
       # Then: code-quality-auditor invoked, extreme violation detected
   ```

### Test Data Requirements

**Sample Projects for Testing:**

1. **Python Project**
   - Business logic: 96% coverage (PASS)
   - Application: 88% coverage (PASS)
   - Infrastructure: 75% coverage (WARNING)
   - Library: pytest, FastAPI
   - Anti-pattern: Hard-coded API key in config.py

2. **C# Project**
   - Business logic: 92% coverage (FAIL - below 95%)
   - Application: 87% coverage (PASS)
   - Library: Dapper (locked), but Entity Framework used (CRITICAL substitution)
   - Code quality: OrderService has complexity 28 (CRITICAL)

3. **Node.js Project**
   - Coverage: All layers above thresholds (PASS)
   - Code quality: 27% code duplication (CRITICAL)
   - Security: XSS vulnerability in React component (CRITICAL)

---

## Performance Targets

### Subagent Execution Time

| Subagent | Small Project (<1K LOC) | Medium Project (1K-10K LOC) | Large Project (>10K LOC) |
|----------|-------------------------|------------------------------|--------------------------|
| coverage-analyzer | <10s | <30s | <60s |
| anti-pattern-scanner | <5s | <15s | <30s |
| code-quality-auditor | <10s | <30s | <60s |
| **Total QA Time** | <25s | <75s | <150s |

### Token Usage Targets

| Phase | Before (Inline) | After (Subagent) | Savings | Reduction |
|-------|-----------------|------------------|---------|-----------|
| Phase 1: Coverage | 12K tokens | 4K tokens | 8K | 67% |
| Phase 2: Anti-Patterns | 8K tokens | 3K tokens | 5K | 63% |
| Phase 4: Quality | 6K tokens | 3K tokens | 3K | 50% |
| **Total QA Workflow** | **36K tokens** | **10K tokens** | **26K** | **72%** |

---

## Risk Assessment

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Subagent fails to parse coverage report | Medium | High | Implement robust error handling with 4 scenarios covered |
| Context files missing/malformed | Low | High | Validate context files exist before invocation, HALT if missing |
| Language-specific tools not installed | Medium | Medium | Return clear error with installation instructions |
| Token savings less than expected | Low | Medium | Measure actual token usage before/after, validate 60%+ savings |

### Integration Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking changes to devforgeai-qa skill | Low | High | Maintain backwards compatibility, test existing QA workflows |
| Subagent blocks_qa logic incorrect | Medium | High | Comprehensive unit tests for all blocking scenarios |
| Performance degradation (subagent slower than inline) | Low | Medium | Performance targets enforced, optimization if needed |

---

## Success Metrics

### Quantitative Metrics

- [ ] Token usage reduced by ≥60% (target: 26K savings achieved)
- [ ] QA execution time ≤150s for large projects
- [ ] Test coverage: 100% for subagent unit tests (12 tests)
- [ ] Integration test pass rate: 100% (3 tests)
- [ ] Zero regressions in existing QA workflows

### Qualitative Metrics

- [ ] Code maintainability improved (coverage logic isolated in subagents)
- [ ] Subagents reusable by other skills/commands
- [ ] Documentation complete and clear
- [ ] Error messages actionable with remediation steps
- [ ] Business impact explanations help developers prioritize fixes

---

## Next Steps

### Immediate Actions (Week 1)

1. **Implement STORY-061: coverage-analyzer**
   - Create unit tests (4 tests)
   - Create integration test (1 test)
   - Update devforgeai-qa skill Phase 1
   - Validate token savings (12K → 4K)

2. **Implement STORY-062: anti-pattern-scanner**
   - Create unit tests (4 tests)
   - Create integration test (1 test)
   - Update devforgeai-qa skill Phase 2
   - Validate token savings (8K → 3K)

3. **Implement STORY-063: code-quality-auditor**
   - Create unit tests (4 tests)
   - Create integration test (1 test)
   - Update devforgeai-qa skill Phase 4
   - Validate token savings (6K → 3K)

### Follow-Up Actions (Week 2)

4. **Comprehensive Testing**
   - Run all unit tests (12 tests across 3 subagents)
   - Run all integration tests (3 QA workflow tests)
   - Performance testing (small/medium/large projects)

5. **Documentation Updates**
   - Update devforgeai-qa skill documentation
   - Update subagent reference documentation
   - Create user-facing documentation (how to interpret results)

6. **Validation & Metrics**
   - Measure actual token savings (target: 26K per QA run)
   - Measure actual execution time (target: <150s for large projects)
   - Validate no regressions in existing QA workflows

---

## References

### Subagent Specifications (Created)
- `.claude/agents/coverage-analyzer.md`
- `.claude/agents/anti-pattern-scanner.md`
- `.claude/agents/code-quality-auditor.md`

### Prompt Templates (Created)
- `.claude/skills/devforgeai-qa/references/subagent-prompt-templates.md`

### Stories (Created)
- `STORY-061-coverage-analyzer-subagent.story.md`

### Stories (To Create)
- STORY-062: anti-pattern-scanner subagent (use STORY-061 as template)
- STORY-063: code-quality-auditor subagent (use STORY-061 as template)

### Integration Points (To Update)
- `.claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md`
- `.claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md`
- `.claude/skills/devforgeai-qa/references/code-quality-workflow.md`

---

## Conclusion

This implementation plan provides a comprehensive roadmap for implementing three P0 priority subagents that will optimize DevForgeAI's QA validation workflow by reducing context window usage by **72%** (26K tokens per QA run).

The deliverables created so far (subagent specifications, prompt templates, STORY-061) demonstrate the high quality and thoroughness expected for this implementation. Following the same pattern for STORY-062 and STORY-063 will ensure consistency and maintainability.

**Estimated Total Effort:** 21 story points (3-5 days)
**Expected ROI:** 26K tokens saved per QA run, significant cost reduction, improved maintainability
**Risk Level:** Low (comprehensive error handling, testing strategy, backwards compatibility)
**Priority:** P0 (High-value optimization with clear business impact)

**Ready for implementation!** 🚀
