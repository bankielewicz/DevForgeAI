---
story_id: STORY-063
title: Implement code-quality-auditor subagent for code quality metrics analysis
epic_id: null
sprint: Backlog
priority: Medium
points: 5
status: Backlog
created: 2025-11-20
updated: 2025-11-20
assignee: null
labels: [subagent, qa, code-quality, refactoring, technical-debt]
---

# STORY-063: Implement code-quality-auditor Subagent for Code Quality Metrics Analysis

## User Story

**As a** DevForgeAI QA validation engineer
**I want** a specialized code-quality-auditor subagent that analyzes cyclomatic complexity, code duplication, and maintainability index
**So that** I can identify extreme quality violations (complexity >20, duplication >25%, MI <40) with business impact explanations and specific refactoring patterns without loading 6K tokens of inline metric calculation logic into the main QA skill

## Business Value

**Problem:** devforgeai-qa skill Phase 4 (Code Quality Metrics) contains ~250 lines (~6K tokens) of inline metric calculation logic for complexity, duplication, and maintainability index analysis.

**Solution:** Delegate code quality analysis to a specialized code-quality-auditor subagent that focuses on EXTREME violations only, explains business impact (bug risk, maintenance cost), and provides specific refactoring patterns.

**Impact:**
- **Token Efficiency:** 70% reduction (6K → 3K tokens for Phase 4)
- **Focus:** Only flags extreme violations (complexity >20, not every function >5)
- **Business Context:** Explains WHY metrics matter (40% higher defect rates, 3x onboarding time)
- **Actionable Guidance:** Specific refactoring patterns (Extract Method, Template Method, etc.)

## Acceptance Criteria

### AC1: Subagent Specification Created with 8-Phase Workflow
**Given** the DevForgeAI framework needs a code quality analysis specialist
**When** I create the `src/claude/agents/code-quality-auditor.md` subagent file
**Then** the subagent specification must include:
- [ ] YAML frontmatter with `name: code-quality-auditor`, `description`, `tools` (Read, Bash language analysis tools), `model: claude-haiku-4-5-20251001`
- [ ] Complete 8-phase workflow: Context Loading, Complexity Analysis, Duplication Analysis, Maintainability Analysis, Business Impact Explanation, Refactoring Patterns, Aggregate Results, Return Results
- [ ] Input contract specifying required context (story_id, language, source_paths, exclude_paths, thresholds)
- [ ] Output contract specifying JSON structure (metrics, extreme_violations, blocks_qa, recommendations)
- [ ] 4 guardrails: Read-only analysis, Context file enforcement, Threshold blocking (extreme only), Metric interpretation
- [ ] Error handling for 3 scenarios: analysis tool not available, no source files, tool execution failed
- [ ] Integration instructions for devforgeai-qa skill Phase 4
- [ ] Testing requirements (4 unit tests, 1 integration test)
- [ ] Performance targets (<60s for large projects)
- [ ] Success criteria checklist (8 items)

**Test:**
```bash
# Validate subagent file exists in source tree
test -f src/claude/agents/code-quality-auditor.md
grep -q "name: code-quality-auditor" src/claude/agents/code-quality-auditor.md
grep -q "model: claude-haiku-4-5-20251001" src/claude/agents/code-quality-auditor.md

# Validate 8-phase workflow documented
grep -q "Phase 1: Context Loading" src/claude/agents/code-quality-auditor.md
grep -q "Phase 8: Return Results" src/claude/agents/code-quality-auditor.md

# Validate all 3 metrics documented
grep -q "Cyclomatic Complexity" src/claude/agents/code-quality-auditor.md
grep -q "Code Duplication" src/claude/agents/code-quality-auditor.md
grep -q "Maintainability Index" src/claude/agents/code-quality-auditor.md
```

---

### AC2: Cyclomatic Complexity Analysis with Language-Specific Tooling
**Given** projects use different languages requiring different analysis tools
**When** code-quality-auditor analyzes complexity
**Then** it must:
- [ ] Detect language from tech-stack.md
- [ ] Map language to tool:
  - Python → `radon cc src/ -s -j` (JSON output)
  - Node.js → `npx eslint --rule 'complexity: [error, 20]'`
  - C# → Use existing `src/claude/skills/devforgeai-qa/scripts/analyze_complexity.py`
  - Go → `gocyclo`
  - Rust → `cargo-geiger`
  - Java → `PMD`
- [ ] Calculate average complexity per function
- [ ] Calculate average complexity per file
- [ ] Identify max complexity (worst offender)
- [ ] Flag functions with complexity >20 as CRITICAL violations
- [ ] Flag functions with complexity 15-20 as WARNING (does not block)

**Test:**
```python
def test_python_complexity_analysis():
    # Given: Python project with function at complexity 28
    # When: code-quality-auditor runs
    # Then: CRITICAL violation detected
    result = invoke_code_quality_auditor(
        language="Python",
        code="""
        def process_order(order):
            # 28 code paths (lots of if/elif/else)
            ...
        """
    )
    assert result["metrics"]["complexity"]["max_complexity"]["score"] == 28
    assert result["extreme_violations"][0]["severity"] == "CRITICAL"
    assert result["blocks_qa"] == True
```

---

### AC3: Code Duplication Detection with Percentage Calculation
**Given** duplicated code increases maintenance cost and bug risk
**When** code-quality-auditor analyzes duplication
**Then** it must:
- [ ] Use existing `src/claude/skills/devforgeai-qa/scripts/detect_duplicates.py` (Python, C#)
- [ ] Use `jscpd` for Node.js projects
- [ ] Calculate duplication_percentage = (duplicate_lines / total_lines) * 100
- [ ] Identify duplicate_blocks with file:line ranges
- [ ] Flag >25% duplication as CRITICAL violation
- [ ] Flag 20-25% duplication as WARNING (does not block)
- [ ] Provide pattern description for each duplicate block

**Test:**
```python
def test_duplication_detection():
    # Given: Project with 27% code duplication
    # When: code-quality-auditor runs
    # Then: CRITICAL violation detected
    result = invoke_code_quality_auditor(
        duplication_percentage=27.0,
        duplicate_blocks=[
            {"files": ["src/ServiceA.cs:45-67", "src/ServiceB.cs:123-145"], "lines": 23}
        ]
    )
    assert result["metrics"]["duplication"]["percentage"] == 27.0
    assert result["extreme_violations"][0]["type"] == "duplication"
    assert result["extreme_violations"][0]["severity"] == "CRITICAL"
    assert result["blocks_qa"] == True
```

---

### AC4: Maintainability Index Calculation (0-100 Scale)
**Given** maintainability index quantifies code maintainability
**When** code-quality-auditor calculates MI
**Then** it must:
- [ ] Use radon for Python: `python -m radon mi src/ -s -j`
- [ ] Calculate manually for other languages: `MI = 171 - 5.2*ln(Volume) - 0.23*Complexity - 16.2*ln(LOC)`
- [ ] Calculate average MI across all files
- [ ] Identify low maintainability files (MI <40 = CRITICAL, 40-50 = WARNING)
- [ ] Flag MI <40 as CRITICAL violation
- [ ] Explain MI scale: >85 Excellent, 65-85 Good, 50-65 Moderate, <50 Difficult

**Test:**
```python
def test_maintainability_index():
    # Given: File with MI = 35 (below 40 threshold)
    # When: code-quality-auditor runs
    # Then: CRITICAL violation detected
    result = invoke_code_quality_auditor(
        files=[{"path": "src/LegacyService.cs", "mi": 35.2}]
    )
    assert result["metrics"]["maintainability"]["low_maintainability_files"][0]["mi"] == 35.2
    assert result["extreme_violations"][0]["type"] == "maintainability"
    assert result["extreme_violations"][0]["severity"] == "CRITICAL"
    assert result["blocks_qa"] == True
```

---

### AC5: Business Impact Explanations for Violations
**Given** developers need to understand WHY metrics matter
**When** code-quality-auditor identifies extreme violations
**Then** each violation must explain business impact:
- [ ] **Complexity >20:** "40% higher defect rate, {N} test cases required, 3x onboarding time"
- [ ] **Duplication >25%:** "Changes in {N} places, bug multiplication risk, {%} redundant code"
- [ ] **MI <40:** "50% slower modifications, 3x bug introduction risk, team morale impact"
- [ ] Impact quantified (percentages, multipliers, specific metrics)
- [ ] Statistical evidence referenced (e.g., "studies show >20 complexity correlates with 40% more defects")

**Test:**
```python
def test_business_impact_explanation():
    # Given: Extreme complexity violation
    # When: code-quality-auditor generates business_impact
    # Then: Explanation includes quantified metrics
    violation = result["extreme_violations"][0]
    assert "business_impact" in violation
    assert "40% more defects" in violation["business_impact"] or "defect rate" in violation["business_impact"]
    assert "test cases" in violation["business_impact"]
    assert "onboarding" in violation["business_impact"].lower()
```

---

### AC6: Specific Refactoring Pattern Recommendations
**Given** developers need actionable guidance for fixing violations
**When** code-quality-auditor generates recommendations
**Then** each violation must include refactoring_pattern with:
- [ ] **Complexity:** "Extract Method: Split into 5 methods (ValidateOrder, CalculateTotal, ...). Target: <6 complexity each."
- [ ] **Duplication:** "Extract to shared utility class: Create ValidationService with ValidateInput method. Location: src/Common/Utilities/."
- [ ] **MI:** "Simplify logic: Extract methods, reduce file size, improve naming. Target: MI >50."
- [ ] Specific pattern names (Extract Method, Template Method, Strategy Pattern, etc.)
- [ ] Target metrics (Current → Goal)
- [ ] 1-5 concrete implementation steps

**Test:**
```python
def test_refactoring_pattern_recommendation():
    # Given: Extreme complexity violation (28)
    # When: code-quality-auditor generates refactoring_pattern
    # Then: Specific pattern with steps
    violation = result["extreme_violations"][0]
    assert "refactoring_pattern" in violation
    assert "Extract Method" in violation["refactoring_pattern"]
    assert "Target:" in violation["refactoring_pattern"]
    # Should contain numbered steps
    assert "1." in violation["refactoring_pattern"] or "2." in violation["refactoring_pattern"]
```

---

### AC7: Integration with devforgeai-qa Skill Phase 4
**Given** devforgeai-qa skill Phase 4 needs code quality metrics analysis
**When** QA skill invokes code-quality-auditor subagent
**Then** integration must:
- [ ] Load 2 context files (tech-stack.md, quality-metrics.md)
- [ ] Extract language from tech-stack.md
- [ ] Invoke subagent with complete prompt (context files, story_id, language, source_paths, exclude_paths)
- [ ] Parse JSON response from subagent
- [ ] Update `blocks_qa` state using OR operation: `blocks_qa = blocks_qa OR quality_result["blocks_qa"]`
- [ ] Display metrics summary to user (complexity, duplication, MI)
- [ ] Store extreme_violations for QA report
- [ ] Continue to Phase 5 if successful, HALT if failed

**Test:**
```python
def test_qa_skill_integration():
    # Given: Story with extreme complexity (function with complexity 28)
    # When: devforgeai-qa skill runs Phase 4
    # Then: code-quality-auditor invoked, violation detected, blocks_qa updated
    qa_result = invoke_devforgeai_qa("STORY-TEST-003", mode="deep")
    assert "metrics" in qa_result
    assert qa_result["metrics"]["complexity"]["max_complexity"]["score"] == 28
    assert qa_result["blocks_qa"] == True
    assert "business_impact" in qa_result["extreme_violations"][0]
```

---

### AC8: Prompt Template Documented
**Given** devforgeai-qa skill needs standardized invocation pattern
**When** I document the code-quality-auditor prompt template
**Then** the template must be added to `src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md` including:
- [ ] Context file loading instructions (tech-stack, quality-metrics)
- [ ] Language extraction and tool selection logic
- [ ] Complete Task() invocation with f-string prompt
- [ ] All 3 metric descriptions (complexity, duplication, MI)
- [ ] Business impact requirements
- [ ] Refactoring pattern requirements
- [ ] Response parsing instructions
- [ ] Error handling pattern
- [ ] Token budget impact (Before: 6K inline, After: 3K prompt = 70% reduction)

**Test:**
```bash
# Validate prompt template exists
test -f src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md

# Validate code-quality-auditor template section exists
grep -q "## Template 3: code-quality-auditor" src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md

# Validate business impact requirement documented
grep -q "Business Impact Requirements" src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md
```

---

### AC9: Extreme Violations Only (No Noise)
**Given** code quality analysis can generate excessive warnings
**When** code-quality-auditor reports violations
**Then** it must ONLY report extreme violations:
- [ ] Complexity >20 = CRITICAL (15-20 = WARNING, <15 = acceptable, not reported)
- [ ] Duplication >25% = CRITICAL (20-25% = WARNING, <20% = acceptable)
- [ ] MI <40 = CRITICAL (40-50 = WARNING, >50 = acceptable)
- [ ] NO reporting of acceptable metrics (avoids noise)
- [ ] Positive feedback when metrics good ("✅ EXCELLENT: MI 72.4 indicates high-quality code")

**Test:**
```python
def test_only_extreme_violations_reported():
    # Given: Complexity 12 (acceptable), duplication 15% (acceptable), MI 65 (good)
    # When: code-quality-auditor runs
    # Then: No violations, blocks_qa = False, positive feedback
    result = invoke_code_quality_auditor(
        complexity_avg=12,
        duplication_pct=15,
        mi_avg=65
    )
    assert len(result["extreme_violations"]) == 0
    assert result["blocks_qa"] == False
    assert "✅" in result["recommendations"][0]  # Positive feedback
```

---

### AC10: Error Handling for Missing Analysis Tools
**Given** code quality analysis requires language-specific tools
**When** tools not installed (radon, eslint, jscpd, etc.)
**Then** error handling must:
- [ ] **Tool not available:** Return `{"status": "failure", "error": "Analysis tool not available: radon", "blocks_qa": true, "remediation": "Install radon: pip install radon"}`
- [ ] **No source files:** Return `{"status": "failure", "error": "No source files found in src/", "blocks_qa": false, "remediation": "Check source_paths configuration"}`
- [ ] **Tool execution failed:** Return failure with stderr and remediation

**Test:**
```python
def test_error_handling_tool_not_available():
    # Given: Python project but radon not installed
    # When: code-quality-auditor runs
    # Then: Returns failure status with installation instructions
    result = invoke_code_quality_auditor(
        language="Python",
        radon_installed=False
    )
    assert result["status"] == "failure"
    assert "radon not installed" in result["error"]
    assert result["blocks_qa"] == True
    assert "pip install radon" in result["remediation"]
```

---

## Technical Specification

```yaml
components:
  - type: Subagent
    name: code-quality-auditor
    file: src/claude/agents/code-quality-auditor.md
    description: "Code quality metrics analysis specialist focusing on extreme violations with business impact explanations"
    tools:
      - Read (context files, source code)
      - Bash(python:*) (Python script execution)
      - Bash(radon:*) (Python complexity/MI)
      - Bash(pylint:*) (Python linting)
      - Bash(eslint:*) (JavaScript/TypeScript complexity)
      - Bash(rubocop:*) (Ruby complexity)
      - Bash(cloc:*) (Line counting)
    model: claude-haiku-4-5-20251001
    responsibilities:
      - Execute language-specific complexity analysis
      - Calculate cyclomatic complexity (per function, per file, average, max)
      - Execute code duplication detection (percentage, duplicate blocks)
      - Calculate maintainability index (0-100 scale, per file, average)
      - Identify extreme violations (complexity >20, duplication >25%, MI <40)
      - Generate business impact explanations (bug risk, maintenance cost, onboarding time)
      - Provide specific refactoring patterns (Extract Method, Template Method, etc.)
      - Determine blocking status (extreme violations block QA)
      - Return structured JSON with metrics and recommendations
    test_requirement: "MUST be tested with 4 unit tests and 1 integration test"

  - type: Configuration
    name: subagent-prompt-templates.md
    file: src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md
    description: "Template 3: code-quality-auditor invocation pattern"
    purpose: "Provides consistent invocation pattern for code-quality-auditor from devforgeai-qa skill Phase 4"
    test_requirement: "MUST document business impact requirements, refactoring pattern requirements, response parsing"

  - type: Integration
    name: devforgeai-qa Phase 4 modification
    file: src/claude/skills/devforgeai-qa/references/code-quality-workflow.md
    description: "Replace inline quality metrics calculation (~250 lines) with subagent delegation"
    before_token_cost: "~6K tokens (inline metric calculation)"
    after_token_cost: "~3K tokens (prompt + response parsing)"
    token_savings: "~3K tokens (70% reduction)"
    test_requirement: "MUST be tested with integration test showing QA skill invokes code-quality-auditor and processes results"

  - type: Script
    name: analyze_complexity.py
    file: src/claude/skills/devforgeai-qa/scripts/analyze_complexity.py
    description: "Existing Python script for cyclomatic complexity analysis (used by subagent for C# projects)"
    test_requirement: "Script already tested, no changes needed"

  - type: Script
    name: detect_duplicates.py
    file: src/claude/skills/devforgeai-qa/scripts/detect_duplicates.py
    description: "Existing Python script for code duplication detection (used by subagent for multiple languages)"
    test_requirement: "Script already tested, no changes needed"

business_rules:
  - rule: "Complexity >20 is CRITICAL violation (blocks QA approval)"
    rationale: "Studies show >20 complexity correlates with 40% more production defects"
    blocking: true
    test_requirement: "Test function with complexity 28 triggers CRITICAL and blocks_qa = true"

  - rule: "Duplication >25% is CRITICAL violation (blocks QA approval)"
    rationale: "Extreme duplication violates DRY principle, increases maintenance cost exponentially"
    blocking: true
    test_requirement: "Test 27% duplication triggers CRITICAL and blocks_qa = true"

  - rule: "Maintainability Index <40 is CRITICAL violation (blocks QA approval)"
    rationale: "MI <40 indicates severe technical debt, 50% slower modifications, 3x bug introduction risk"
    blocking: true
    test_requirement: "Test file with MI 35 triggers CRITICAL and blocks_qa = true"

  - rule: "WARNING violations (complexity 15-20, duplication 20-25%, MI 40-50) do NOT block QA"
    rationale: "Warnings indicate areas for improvement but don't prevent release"
    blocking: false
    test_requirement: "Test complexity 18 triggers WARNING but blocks_qa = false"

  - rule: "Acceptable metrics (<15 complexity, <20% duplication, >50 MI) generate positive feedback"
    rationale: "Positive reinforcement for good code quality"
    blocking: false
    test_requirement: "Test good metrics generate '✅ EXCELLENT' feedback"

  - rule: "code-quality-auditor MUST operate read-only"
    rationale: "Analysis subagent should never modify code or refactor - only recommend"
    blocking: true
    test_requirement: "Test code-quality-auditor cannot use Write or Edit tools"

  - rule: "Business impact MUST be quantifiable (not vague)"
    rationale: "Quantified impact helps prioritize refactoring (e.g., '40% more defects' not 'higher risk')"
    blocking: true
    test_requirement: "Test business_impact includes percentages, multipliers, or specific numbers"

  - rule: "Refactoring patterns MUST be specific (not generic)"
    rationale: "Specific patterns actionable (e.g., 'Extract Method: Split ProcessOrder into...' not 'improve code quality')"
    blocking: true
    test_requirement: "Test refactoring_pattern includes pattern name and implementation steps"

non_functional_requirements:
  - category: Performance
    requirement: "Code quality analysis MUST complete within 60 seconds for large projects (>10K LOC)"
    measurement: "Execution time from subagent invocation to JSON response"
    target: "<10s for small (<10K LOC), <30s for medium (10K-50K LOC), <60s for large (>50K LOC)"
    test: "Measure actual execution time with sample projects of varying sizes"

  - category: Token Efficiency
    requirement: "Subagent invocation MUST reduce Phase 4 token usage by ≥50%"
    measurement: "Token count before (inline) vs after (subagent delegation)"
    target: "Before: ~6K tokens, After: ~3K tokens, Savings: ≥3K tokens (70%)"
    test: "Count tokens in devforgeai-qa Phase 4 before and after subagent integration"

  - category: Accuracy
    requirement: "Complexity calculation MUST be accurate within ±1 for all languages"
    measurement: "Comparison with manual cyclomatic complexity calculation"
    target: "100% accuracy (complexity is deterministic)"
    test: "Manually calculate complexity for 10 functions, compare with subagent results"

  - category: Focus
    requirement: "MUST focus on extreme violations only (no noise from acceptable metrics)"
    measurement: "Number of violations reported vs actual extreme violations"
    target: "Precision 100% (only report >20 complexity, >25% duplication, <40 MI)"
    test: "Validate no violations reported for complexity 12, duplication 15%, MI 65"

  - category: Reusability
    requirement: "code-quality-auditor MUST be invocable from any skill/command"
    measurement: "Can be invoked from devforgeai-development, refactoring-specialist, custom commands"
    target: "Generic input/output contract allowing any caller"
    test: "Invoke code-quality-auditor from refactoring-specialist subagent (not just QA)"

---

## Edge Cases

### Edge Case 1: No Violations (Perfect Code Quality)
**Scenario:** All metrics acceptable (complexity <15, duplication <20%, MI >50)
**Expected Behavior:**
- extreme_violations array empty: `[]`
- `blocks_qa = false`
- Recommendations include positive feedback: "✅ EXCELLENT: All quality metrics meet or exceed thresholds"

### Edge Case 2: Multiple Violations in Same File
**Scenario:** Function has both extreme complexity (28) and is in file with low MI (35)
**Expected Behavior:**
- Two separate violations reported (complexity violation + MI violation)
- Both reference same file
- Both explain business impact
- Recommendations prioritize by severity and impact

### Edge Case 3: Analysis Tool Version Incompatibility
**Scenario:** Radon 5.x installed but code-quality-auditor expects radon 6.x
**Expected Behavior:**
- Tool executes but output format different
- Parse error detected
- Returns failure: "Failed to parse radon output (version incompatibility?)"
- Remediation: "Update radon: pip install --upgrade radon"

### Edge Case 4: Generated Code Excluded
**Scenario:** Project has auto-generated code (migrations, scaffolded controllers) with high complexity
**Expected Behavior:**
- code-quality-auditor accepts exclude_paths parameter: ["generated/", "migrations/"]
- Excludes these paths from analysis
- Documents excluded paths in result
- Metrics calculated only for non-excluded code

### Edge Case 5: Language Without Native Tool Support
**Scenario:** Rust project but cargo-geiger not available
**Expected Behavior:**
- Falls back to manual complexity calculation (parse AST, count branches)
- Logs warning: "Using fallback complexity calculation (install cargo-geiger for better accuracy)"
- Returns results with caveat in recommendations

---

## UI Specification

N/A - This is a subagent (backend component) with no user interface. Interaction happens through:
1. **devforgeai-qa skill:** Invokes subagent programmatically, displays metrics summary in QA report
2. **Manual testing:** Can be invoked directly via Task() for testing/debugging
3. **refactoring-specialist:** Can invoke for pre-refactoring quality baseline

---

## Dependencies

### Required Context Files
- `.devforgeai/context/tech-stack.md` - Language detection
- `src/claude/skills/devforgeai-qa/assets/config/quality-metrics.md` - Threshold configuration

### Analysis Tools (Language-Specific)
- **Python:** radon (complexity + MI), pylint (optional)
- **Node.js:** eslint (complexity), jscpd (duplication)
- **C#:** Roslyn analyzers, existing Python scripts
- **Go:** gocyclo (complexity)
- **Rust:** cargo-geiger (complexity)
- **Java:** PMD (complexity), CPD (duplication)

### Existing Scripts (Reused)
- `src/claude/skills/devforgeai-qa/scripts/analyze_complexity.py` - Multi-language complexity
- `src/claude/skills/devforgeai-qa/scripts/detect_duplicates.py` - Multi-language duplication

### Existing Subagents (Reference Patterns)
- `src/claude/agents/coverage-analyzer.md` - Sister subagent for Phase 1 (STORY-061)
- `src/claude/agents/anti-pattern-scanner.md` - Sister subagent for Phase 2 (STORY-062)

---

## Definition of Done

### Implementation
- [ ] code-quality-auditor subagent specification created (`src/claude/agents/code-quality-auditor.md`)
- [ ] Subagent includes all 8 phases in workflow
- [ ] All 3 metrics implemented (complexity, duplication, MI)
- [ ] Language-specific tooling documented (6 languages)
- [ ] Input/output contracts specified (JSON schemas)
- [ ] 4 guardrails documented (read-only, context enforcement, extreme-only, metric interpretation)
- [ ] Error handling for 3 scenarios (tool unavailable, no files, execution failed)
- [ ] Operational copy in `.claude/agents/code-quality-auditor.md` (for immediate use)

### Quality
- [ ] Unit tests created (4 scenarios minimum):
  - test_detects_extreme_complexity (complexity 28 → CRITICAL, blocks_qa = true)
  - test_detects_extreme_duplication (27% → CRITICAL, blocks_qa = true)
  - test_detects_low_maintainability (MI 35 → CRITICAL, blocks_qa = true)
  - test_acceptable_quality_no_blocking (all good → blocks_qa = false)
- [ ] Integration test created (1 scenario):
  - test_qa_skill_invokes_code_quality_auditor (end-to-end)
- [ ] Prompt template documented in `src/claude/skills/devforgeai-qa/references/subagent-prompt-templates.md` (Template 3)
- [ ] Token savings validated (6K → 3K = 70% reduction)
- [ ] Performance target met (<60s for large projects)

### Testing
- [ ] Manual invocation test: Task(subagent_type="code-quality-auditor", ...) returns valid JSON
- [ ] QA skill integration test: devforgeai-qa Phase 4 successfully delegates to code-quality-auditor
- [ ] Multi-language test: Subagent works with Python, C#, Node.js projects
- [ ] Business impact test: Explanations include quantified metrics

### Documentation
- [ ] Subagent specification complete with all 8 phases
- [ ] Business impact explanation templates documented
- [ ] Refactoring pattern templates documented
- [ ] Integration instructions added to devforgeai-qa skill references
- [ ] Prompt template added to subagent-prompt-templates.md (Template 3)
- [ ] Success criteria checklist included

### Review
- [ ] Code review by architect (subagent design patterns)
- [ ] Refactoring specialist review (pattern recommendations quality)
- [ ] QA review (test coverage adequacy)
- [ ] Documentation review (business impact clarity)

---

## Implementation Notes

Status: Backlog - Story created and ready for development. All Definition of Done items will be completed during TDD cycle.

**Approved Deferrals:**
- All DoD items [ ] are expected at Backlog stage (pre-implementation)
- Approval: Backlog stories have deferred DoD items by design - items will be implemented during TDD cycle
- User approved: 2025-11-21 (Backlog story creation, pre-implementation)

## Definition of Done

### Implementation
- [ ] `.claude/agents/code-quality-auditor.md` created with complete specification
- [ ] 4-phase workflow documented (Collect, Analyze, Validate, Report)
- [ ] Input/output contracts defined
- [ ] 3 metric categories (complexity, duplication, maintainability)
- [ ] Threshold validation (extreme violations only: complexity >15, duplication >5%, MI <50)
- [ ] Business impact explanations provided
- [ ] Actionable refactoring patterns included

### Quality
- [ ] All AC have passing tests
- [ ] Language-agnostic tooling (6 languages)
- [ ] Positive feedback mechanism working
- [ ] Subagent follows DevForgeAI patterns

### Testing
- [ ] Unit tests pass (9 test scenarios across 3 metrics)
- [ ] Integration test passes (1 integration scenario)
- [ ] Haiku model performance acceptable (<60s)
- [ ] All tests passing (10/10 test categories)

### Documentation
- [ ] Subagent file complete and cross-referenced
- [ ] devforgeai-qa skill updated to invoke subagent
- [ ] Integration example documented
- [ ] Versioned in git

---

## Workflow History

- **2025-11-20:** Story created (STORY-063)
- Status: Backlog → Ready for Dev (after STORY-061 and STORY-062 complete)

---

## Notes

**Subagent Design Philosophy:**
- **Focus on Extreme:** Only report violations that truly matter (complexity >20, not >5)
- **Business Context:** Every violation explains business impact in quantifiable terms
- **Actionable Patterns:** Specific refactoring patterns with implementation steps
- **Positive Feedback:** Acknowledge good metrics ("✅ EXCELLENT: MI 72.4")
- **Language Agnostic:** Supports 6 languages with appropriate tooling
- **Haiku Model:** Uses claude-haiku-4-5-20251001 for cost efficiency

**Metric Thresholds:**
- **Complexity:** <15 acceptable, 15-20 warning, >20 critical
- **Duplication:** <20% acceptable, 20-25% warning, >25% critical
- **MI:** >50 acceptable, 40-50 warning, <40 critical

**Integration Pattern:**
```python
# devforgeai-qa Phase 4 (NEW pattern with subagent)
quality_result = Task(
    subagent_type="code-quality-auditor",
    prompt=f"Analyze quality metrics for {story_id}...",
    model="claude-haiku-4-5-20251001"
)
blocks_qa = blocks_qa OR quality_result["blocks_qa"]
```

**Token Savings:**
- Before: ~6K tokens (inline metric calculation)
- After: ~3K tokens (prompt + response)
- Savings: ~3K tokens (70% reduction)
- Per QA run: 3K tokens saved
- Per 10 stories: 30K tokens saved
- Per 100 stories: 300K tokens saved

**Combined P0 Savings (STORY-061 + STORY-062 + STORY-063):**
- Total savings: 26K tokens per QA run (72% reduction)
- Cost impact: Significant (2.6M tokens saved per 100 QA runs)
- Maintainability: All QA validation logic isolated in 3 specialized subagents

**Related Stories:**
- STORY-061: Implement coverage-analyzer subagent (12K token savings) - PREREQUISITE
- STORY-062: Implement anti-pattern-scanner subagent (8K token savings) - PREREQUISITE
- Combined: Complete QA subagent delegation (26K total savings)
