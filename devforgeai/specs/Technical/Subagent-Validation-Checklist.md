# P0 Subagent Validation Checklist

**Purpose:** Comprehensive validation checklist for verifying P0 subagent implementations meet all quality, performance, and integration requirements.

**Date Created:** 2025-11-20
**Applies To:** coverage-analyzer, anti-pattern-scanner, code-quality-auditor

---

## Pre-Implementation Validation

### Subagent Specification Quality

- [ ] **Specification File Exists**
  ```bash
  test -f .claude/agents/coverage-analyzer.md
  test -f .claude/agents/anti-pattern-scanner.md
  test -f .claude/agents/code-quality-auditor.md
  ```

- [ ] **YAML Frontmatter Valid**
  ```bash
  # Validate required fields present
  grep -q "^name: coverage-analyzer$" .claude/agents/coverage-analyzer.md
  grep -q "^description:" .claude/agents/coverage-analyzer.md
  grep -q "^tools:" .claude/agents/coverage-analyzer.md
  grep -q "^model: claude-haiku-4-5-20251001$" .claude/agents/coverage-analyzer.md
  ```

- [ ] **Workflow Phases Documented**
  ```bash
  # Validate all phases documented
  grep -c "^### Phase" .claude/agents/coverage-analyzer.md  # Should be 8 or 9
  ```

- [ ] **Input Contract Specified**
  ```bash
  grep -q "## Input Contract" .claude/agents/coverage-analyzer.md
  grep -q "Required Context" .claude/agents/coverage-analyzer.md
  ```

- [ ] **Output Contract Specified**
  ```bash
  grep -q "## Output Contract" .claude/agents/coverage-analyzer.md
  grep -q "Success Response" .claude/agents/coverage-analyzer.md
  grep -q "Failure Response" .claude/agents/coverage-analyzer.md
  ```

- [ ] **Guardrails Documented**
  ```bash
  grep -q "## Guardrails" .claude/agents/coverage-analyzer.md
  # Should have 4 guardrails minimum
  ```

- [ ] **Error Handling Documented**
  ```bash
  grep -q "## Error Handling" .claude/agents/coverage-analyzer.md
  # Should document 4 error scenarios
  ```

- [ ] **Integration Instructions Present**
  ```bash
  grep -q "## Integration with devforgeai-qa" .claude/agents/coverage-analyzer.md
  ```

---

## Subagent 1: coverage-analyzer

### Functional Requirements

- [ ] **Language Detection Implemented**
  - Reads tech-stack.md
  - Extracts primary_language field
  - Maps to coverage tool (6 languages supported)

- [ ] **Coverage Command Execution**
  ```bash
  # Python
  pytest --cov=src --cov-report=json

  # C#
  dotnet test --collect:"XPlat Code Coverage"

  # Node.js
  npm test -- --coverage

  # Validate command execution for each language
  ```

- [ ] **File Classification by Layer**
  - Loads source-tree.md
  - Extracts layer patterns (business_logic, application, infrastructure)
  - Classifies files correctly (100% accuracy with comprehensive patterns)
  - Handles unknown files gracefully (warning, not error)

- [ ] **Coverage Calculation Accuracy**
  - Calculates business logic coverage
  - Calculates application coverage
  - Calculates infrastructure coverage
  - Calculates overall coverage
  - Formulas correct: `(lines_covered / lines_total) * 100`

- [ ] **Threshold Validation Logic**
  - Business logic ≥95% → pass, <95% → CRITICAL violation, blocks_qa = true
  - Application ≥85% → pass, <85% → HIGH violation, blocks_qa = true
  - Overall ≥80% → pass, <80% → HIGH violation, blocks_qa = true
  - Infrastructure ≥80% → pass, <80% → WARNING (does not block)

- [ ] **Gap Identification with Evidence**
  - Each gap includes: file, layer, current_coverage, target_coverage
  - Uncovered_lines array present with line numbers
  - Suggested_tests array present with scenario descriptions
  - Gaps prioritized by severity (CRITICAL → HIGH → MEDIUM)

- [ ] **Actionable Recommendations**
  - Recommendations explain business impact (bug risk, maintenance cost)
  - Recommendations include specific files and line numbers
  - Recommendations provide test scenario suggestions
  - Remediation steps included when blocking QA

### Error Handling Validation

- [ ] **Context Files Missing**
  ```bash
  # Test: Remove source-tree.md
  # Expected: {"status": "failure", "error": "Context file missing: devforgeai/context/source-tree.md", "blocks_qa": true}
  ```

- [ ] **Coverage Command Failed**
  ```bash
  # Test: Project without pytest-cov installed
  # Expected: {"status": "failure", "error": "Coverage tool not available: pytest-cov", "remediation": "Install pytest-cov: pip install pytest-cov"}
  ```

- [ ] **Report Parse Error**
  ```bash
  # Test: Corrupt coverage.json file
  # Expected: {"status": "failure", "error": "Failed to parse coverage report", "remediation": "Re-run coverage command"}
  ```

- [ ] **No Files Classified**
  ```bash
  # Test: source-tree.md with no matching patterns
  # Expected: {"status": "failure", "error": "Could not classify any files", "remediation": "Update source-tree.md"}
  ```

### Integration Validation

- [ ] **Prompt Template Exists**
  ```bash
  grep -q "## Template 1: coverage-analyzer" .claude/skills/devforgeai-qa/references/subagent-prompt-templates.md
  ```

- [ ] **devforgeai-qa Phase 1 Updated**
  ```bash
  grep -q "Task(subagent_type=\"coverage-analyzer\"" .claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md
  ```

- [ ] **Context Files Loaded Before Invocation**
  ```python
  # Validate prompt includes all context files
  assert "tech_stack_content" in prompt
  assert "source_tree_content" in prompt
  assert "coverage_thresholds_content" in prompt
  ```

- [ ] **Response Parsing Implemented**
  ```python
  # Validate response parsing extracts all fields
  result = invoke_coverage_analyzer(...)
  assert "coverage_summary" in result
  assert "validation_result" in result
  assert "gaps" in result
  assert "blocks_qa" in result
  ```

- [ ] **blocks_qa State Updated Correctly**
  ```python
  # Validate OR operation (not assignment)
  blocks_qa = False
  blocks_qa = blocks_qa OR coverage_result["blocks_qa"]  # ✓ Correct
  # blocks_qa = coverage_result["blocks_qa"]  # ✗ Wrong
  ```

### Performance Validation

- [ ] **Execution Time Within Targets**
  ```bash
  # Small project (<1K LOC): <10 seconds
  # Medium project (1K-10K LOC): <30 seconds
  # Large project (>10K LOC): <60 seconds
  time invoke_coverage_analyzer(...)
  ```

- [ ] **Token Usage Optimized**
  ```bash
  # Before: ~12K tokens (inline logic)
  # After: ~4K tokens (prompt + response)
  # Savings: ≥8K tokens (65% reduction)
  # Validate actual token count
  ```

### Unit Tests

- [ ] **test_threshold_blocking**
  ```python
  def test_threshold_blocking():
      # Given: Business logic at 93%
      # When: coverage-analyzer runs
      # Then: blocks_qa = True, CRITICAL violation
      pass  # ✓ Implemented and passing
  ```

- [ ] **test_file_classification**
  ```python
  def test_file_classification():
      # Given: Files in domain/application/infrastructure
      # When: coverage-analyzer classifies
      # Then: Correct layer assignment
      pass  # ✓ Implemented and passing
  ```

- [ ] **test_gap_identification**
  ```python
  def test_gap_identification():
      # Given: File at 70% coverage
      # When: coverage-analyzer identifies gaps
      # Then: Gap includes file:line evidence
      pass  # ✓ Implemented and passing
  ```

- [ ] **test_error_handling**
  ```python
  def test_error_handling():
      # Given: source-tree.md missing
      # When: coverage-analyzer runs
      # Then: Failure status with remediation
      pass  # ✓ Implemented and passing
  ```

### Integration Test

- [ ] **test_qa_skill_invokes_coverage_analyzer**
  ```python
  def test_qa_skill_invokes_coverage_analyzer():
      # Given: Story with 88% coverage
      # When: /qa STORY-001 deep
      # Then: coverage-analyzer invoked, results integrated
      qa_result = invoke_devforgeai_qa("STORY-001", mode="deep")
      assert "coverage_summary" in qa_result
      assert qa_result["blocks_qa"] == True
      pass  # ✓ Implemented and passing
  ```

---

## Subagent 2: anti-pattern-scanner

### Functional Requirements

- [ ] **Category 1: Library Substitution Detection (CRITICAL)**
  - ORM swap: Dapper ↔ Entity Framework
  - State manager: Zustand ↔ Redux
  - HTTP client: axios ↔ fetch
  - Validation: Zod ↔ Joi
  - Testing: Vitest ↔ Jest
  - Each detected substitution = CRITICAL violation, blocks_qa = true

- [ ] **Category 2: Structure Violations (HIGH)**
  - Files in wrong layers detected
  - Infrastructure concerns in domain layer detected
  - Unexpected directories in layers detected
  - Each violation = HIGH severity, blocks_qa = true

- [ ] **Category 3: Layer Violations (HIGH)**
  - Cross-layer dependencies detected
  - Domain referencing application/infrastructure → violation
  - Application referencing infrastructure → violation
  - Circular dependencies detected
  - Each violation = HIGH severity, blocks_qa = true

- [ ] **Category 4: Code Smells (MEDIUM)**
  - God objects (>15 methods, >300 lines) detected
  - Long methods (>50 lines) detected
  - Magic numbers detected
  - Violations = MEDIUM severity, warning only (does not block)

- [ ] **Category 5: Security Issues (CRITICAL)**
  - Hard-coded secrets detected
  - SQL injection risk detected
  - XSS vulnerabilities detected
  - Insecure deserialization detected
  - Each issue = CRITICAL severity, blocks_qa = true

- [ ] **Category 6: Style Inconsistencies (LOW)**
  - Missing documentation detected
  - Naming convention violations detected
  - Violations = LOW severity, advisory only

- [ ] **Severity Classification Correct**
  - CRITICAL violations: blocks_qa = true
  - HIGH violations: blocks_qa = true
  - MEDIUM violations: warning only, blocks_qa = false
  - LOW violations: advisory only, blocks_qa = false

- [ ] **Evidence-Based Reporting**
  - Every violation has file path
  - Every violation has line number
  - Every violation has code snippet (evidence)
  - Every violation has remediation guidance

### Error Handling Validation

- [ ] **Context Files Missing**
  ```bash
  # Test: Remove anti-patterns.md
  # Expected: {"status": "failure", "error": "Context file missing", "blocks_qa": true}
  ```

- [ ] **Contradictory Rules**
  ```bash
  # Test: tech-stack.md specifies Dapper, dependencies.md lists Entity Framework
  # Expected: {"status": "failure", "error": "Contradictory rules", "remediation": "Resolve contradiction"}
  ```

### Integration Validation

- [ ] **Prompt Template Exists**
  ```bash
  grep -q "## Template 2: anti-pattern-scanner" .claude/skills/devforgeai-qa/references/subagent-prompt-templates.md
  ```

- [ ] **devforgeai-qa Phase 2 Updated**
  ```bash
  grep -q "Task(subagent_type=\"anti-pattern-scanner\"" .claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md
  ```

- [ ] **ALL 6 Context Files Loaded**
  ```python
  # Validate prompt includes all 6 context files
  context_files = ["tech-stack", "source-tree", "dependencies",
                   "coding-standards", "architecture-constraints", "anti-patterns"]
  for file in context_files:
      assert f"{file}_content" in prompt
  ```

### Performance Validation

- [ ] **Execution Time Within Targets**
  ```bash
  # Small project: <5 seconds
  # Medium project: <15 seconds
  # Large project: <30 seconds
  ```

- [ ] **Token Usage Optimized**
  ```bash
  # Before: ~8K tokens
  # After: ~3K tokens
  # Savings: ≥5K tokens (63% reduction)
  ```

### Unit Tests

- [ ] **test_library_substitution_detection**
  ```python
  def test_library_substitution_detection():
      # Given: Dapper locked, Entity Framework used
      # When: anti-pattern-scanner runs
      # Then: CRITICAL violation, blocks_qa = True
      pass
  ```

- [ ] **test_structure_violation_detection**
  ```python
  def test_structure_violation_detection():
      # Given: EmailService in src/Domain/ (should be Infrastructure)
      # When: anti-pattern-scanner runs
      # Then: HIGH violation, blocks_qa = True
      pass
  ```

- [ ] **test_security_vulnerability_detection**
  ```python
  def test_security_vulnerability_detection():
      # Given: Hard-coded password in config
      # When: anti-pattern-scanner runs
      # Then: CRITICAL violation, blocks_qa = True
      pass
  ```

- [ ] **test_severity_classification**
  ```python
  def test_severity_classification():
      # Given: CRITICAL, HIGH, MEDIUM, LOW violations
      # When: anti-pattern-scanner categorizes
      # Then: CRITICAL/HIGH block, MEDIUM/LOW warn
      pass
  ```

### Integration Test

- [ ] **test_qa_skill_invokes_anti_pattern_scanner**
  ```python
  def test_qa_skill_invokes_anti_pattern_scanner():
      # Given: Story with library substitution
      # When: /qa STORY-002 deep
      # Then: anti-pattern-scanner invoked, violation detected
      pass
  ```

---

## Subagent 3: code-quality-auditor

### Functional Requirements

- [ ] **Cyclomatic Complexity Analysis**
  - Average per function calculated
  - Average per file calculated
  - Max complexity identified
  - Functions over threshold (>20) identified
  - Language-specific tooling used (radon, eslint, etc.)

- [ ] **Code Duplication Detection**
  - Duplication percentage calculated
  - Duplicate blocks identified (files, line ranges)
  - >25% duplication = CRITICAL violation
  - 20-25% duplication = WARNING

- [ ] **Maintainability Index Calculation**
  - MI formula applied correctly: `171 - 5.2*ln(Volume) - 0.23*Complexity - 16.2*ln(LOC)`
  - Average MI calculated across files
  - Low MI files identified (<40 = CRITICAL, 40-50 = WARNING)

- [ ] **Business Impact Explanations**
  - Bug risk explained (statistical correlation)
  - Testing burden explained (number of test cases)
  - Onboarding impact explained (time to understand)
  - Maintenance cost explained (effort multiplier)
  - Explanations quantifiable (not vague)

- [ ] **Refactoring Pattern Recommendations**
  - Specific patterns: Extract Method, Decompose Conditional, etc.
  - Target metrics: Current → Goal
  - Implementation steps: 1-5 concrete actions
  - Expected outcome described

### Error Handling Validation

- [ ] **Analysis Tool Not Available**
  ```bash
  # Test: Python project without radon
  # Expected: {"status": "failure", "error": "Analysis tool not available: radon", "remediation": "Install radon: pip install radon"}
  ```

- [ ] **No Source Files Found**
  ```bash
  # Test: Empty src/ directory
  # Expected: {"status": "failure", "error": "No source files found", "blocks_qa": false}
  ```

### Integration Validation

- [ ] **Prompt Template Exists**
  ```bash
  grep -q "## Template 3: code-quality-auditor" .claude/skills/devforgeai-qa/references/subagent-prompt-templates.md
  ```

- [ ] **devforgeai-qa Phase 4 Updated**
  ```bash
  grep -q "Task(subagent_type=\"code-quality-auditor\"" .claude/skills/devforgeai-qa/references/code-quality-workflow.md
  ```

### Performance Validation

- [ ] **Execution Time Within Targets**
  ```bash
  # Small project: <10 seconds
  # Medium project: <30 seconds
  # Large project: <60 seconds
  ```

- [ ] **Token Usage Optimized**
  ```bash
  # Before: ~6K tokens
  # After: ~3K tokens
  # Savings: ≥3K tokens (50% reduction)
  ```

### Unit Tests

- [ ] **test_extreme_complexity_detection**
  ```python
  def test_extreme_complexity_detection():
      # Given: Function with complexity 28
      # When: code-quality-auditor runs
      # Then: CRITICAL violation, blocks_qa = True
      pass
  ```

- [ ] **test_extreme_duplication_detection**
  ```python
  def test_extreme_duplication_detection():
      # Given: 27% code duplication
      # When: code-quality-auditor runs
      # Then: CRITICAL violation, blocks_qa = True
      pass
  ```

- [ ] **test_low_maintainability_detection**
  ```python
  def test_low_maintainability_detection():
      # Given: File with MI = 35
      # When: code-quality-auditor runs
      # Then: CRITICAL violation, blocks_qa = True
      pass
  ```

- [ ] **test_acceptable_quality_no_blocking**
  ```python
  def test_acceptable_quality_no_blocking():
      # Given: All metrics acceptable
      # When: code-quality-auditor runs
      # Then: blocks_qa = False, positive feedback
      pass
  ```

### Integration Test

- [ ] **test_qa_skill_invokes_code_quality_auditor**
  ```python
  def test_qa_skill_invokes_code_quality_auditor():
      # Given: Story with extreme complexity
      # When: /qa STORY-003 deep
      # Then: code-quality-auditor invoked, violation detected
      pass
  ```

---

## Overall Integration Validation

### Combined QA Workflow

- [ ] **All 3 Subagents Invoked Sequentially**
  ```python
  # Phase 1: coverage-analyzer
  # Phase 2: anti-pattern-scanner
  # Phase 4: code-quality-auditor
  # Validate all 3 invoked in correct order
  ```

- [ ] **blocks_qa State Accumulated Correctly**
  ```python
  blocks_qa = False
  blocks_qa = blocks_qa OR coverage_result["blocks_qa"]      # Phase 1
  blocks_qa = blocks_qa OR anti_pattern_result["blocks_qa"]  # Phase 2
  blocks_qa = blocks_qa OR quality_result["blocks_qa"]       # Phase 4
  # Validate OR logic (not last-write-wins)
  ```

- [ ] **QA Report Includes All Subagent Results**
  - Coverage summary displayed
  - Anti-pattern violations listed by severity
  - Code quality metrics displayed
  - Recommendations from all 3 subagents included

- [ ] **Token Savings Achieved**
  ```bash
  # Before: ~36K tokens (all inline)
  # After: ~10K tokens (all subagents)
  # Savings: ≥26K tokens (72% reduction)
  # Validate actual measurement
  ```

### End-to-End Test

- [ ] **test_complete_qa_workflow_with_subagents**
  ```python
  def test_complete_qa_workflow_with_subagents():
      # Given: Story with multiple quality issues
      #   - Coverage: Business logic 93% (FAIL)
      #   - Anti-pattern: Library substitution (FAIL)
      #   - Quality: Complexity 28 (FAIL)
      # When: /qa STORY-COMPLETE deep
      # Then:
      #   - All 3 subagents invoked
      #   - blocks_qa = True (at least one violation)
      #   - QA report contains results from all subagents
      #   - Token usage <12K (vs ~36K before)
      pass
  ```

---

## Performance Benchmarking

### Token Usage Benchmarks

- [ ] **Measure Baseline (Before Subagents)**
  ```bash
  # Run QA without subagents (inline logic)
  # Measure token usage for each phase
  # Record: Phase 1: __K, Phase 2: __K, Phase 4: __K
  ```

- [ ] **Measure Optimized (After Subagents)**
  ```bash
  # Run QA with subagents (delegated)
  # Measure token usage for each phase
  # Record: Phase 1: __K, Phase 2: __K, Phase 4: __K
  ```

- [ ] **Calculate Savings**
  ```bash
  # Phase 1 savings: (baseline - optimized) / baseline * 100%
  # Phase 2 savings: (baseline - optimized) / baseline * 100%
  # Phase 4 savings: (baseline - optimized) / baseline * 100%
  # Total savings: (total_baseline - total_optimized) / total_baseline * 100%
  # Target: ≥60% reduction per phase
  ```

### Execution Time Benchmarks

- [ ] **Small Project (<1K LOC)**
  ```bash
  # Measure execution time for each subagent
  # Target: coverage-analyzer <10s, anti-pattern-scanner <5s, code-quality-auditor <10s
  # Total: <25s
  ```

- [ ] **Medium Project (1K-10K LOC)**
  ```bash
  # Target: coverage-analyzer <30s, anti-pattern-scanner <15s, code-quality-auditor <30s
  # Total: <75s
  ```

- [ ] **Large Project (>10K LOC)**
  ```bash
  # Target: coverage-analyzer <60s, anti-pattern-scanner <30s, code-quality-auditor <60s
  # Total: <150s
  ```

---

## Documentation Validation

### Subagent Documentation

- [ ] **All 3 Subagent Specs Complete**
  - Workflow phases documented
  - Input/output contracts specified
  - Guardrails listed
  - Error handling described
  - Integration instructions provided
  - Testing requirements documented
  - Performance targets stated

- [ ] **Prompt Templates Complete**
  - Template for each subagent documented
  - Context file loading instructions
  - Response parsing instructions
  - Error handling pattern
  - Integration points described

- [ ] **devforgeai-qa Skill Updated**
  - Phase 1 workflow references coverage-analyzer
  - Phase 2 workflow references anti-pattern-scanner
  - Phase 4 workflow references code-quality-auditor
  - Inline logic removed (replaced with subagent invocations)

### User-Facing Documentation

- [ ] **QA Report Interpretation Guide**
  - How to read coverage summary
  - How to interpret violations by severity
  - How to prioritize remediation
  - How to understand business impact explanations

- [ ] **Error Message Documentation**
  - Common errors and remediation steps
  - When to run /create-context
  - How to install missing coverage tools
  - How to fix context file issues

---

## Regression Testing

### Existing Functionality Preserved

- [ ] **QA Skill Still Works for Stories Without Issues**
  ```python
  # Given: Story with 100% coverage, no violations, good quality
  # When: /qa STORY-CLEAN deep
  # Then: QA passes, no regressions
  ```

- [ ] **Light Mode Still Functional**
  ```python
  # Given: Story in development
  # When: /qa STORY-001 light
  # Then: Light validation runs (subset of checks)
  ```

- [ ] **Backwards Compatibility**
  ```python
  # Given: Existing stories with QA Approved status
  # When: Re-run QA with new subagents
  # Then: Results consistent with previous QA runs
  ```

### Error Handling Preserved

- [ ] **QA Fails Gracefully When Subagent Unavailable**
  ```python
  # Given: Subagent specification missing
  # When: /qa invokes missing subagent
  # Then: Clear error message, blocks_qa = True, remediation provided
  ```

- [ ] **QA Continues After Non-Blocking Violations**
  ```python
  # Given: MEDIUM code smell detected
  # When: QA continues to next phase
  # Then: Warning displayed but QA does not halt
  ```

---

## Acceptance Criteria

### All Checkboxes Must Pass

- [ ] All 3 subagent specifications created and validated
- [ ] All 3 prompt templates documented
- [ ] All 12 unit tests implemented and passing (4 per subagent)
- [ ] All 3 integration tests implemented and passing
- [ ] Token savings ≥60% per phase (target: 72% overall)
- [ ] Execution time ≤150s for large projects
- [ ] No regressions in existing QA workflows
- [ ] Documentation complete and accurate
- [ ] Error handling graceful with actionable remediation
- [ ] Business impact explanations provided for violations

---

## Sign-Off

**Implementation Complete When:**
- ✓ All validation checkboxes above marked complete
- ✓ All unit tests passing (12/12)
- ✓ All integration tests passing (3/3)
- ✓ Performance targets met
- ✓ Documentation reviewed and approved
- ✓ Zero regressions in existing functionality

**Approved By:** ___________________ **Date:** ___________

**QA Validated By:** ___________________ **Date:** ___________

**Architect Reviewed By:** ___________________ **Date:** ___________
