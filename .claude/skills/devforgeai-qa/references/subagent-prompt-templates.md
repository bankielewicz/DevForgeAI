# QA Subagent Prompt Templates

Standardized prompt templates for invoking QA validation subagents from devforgeai-qa skill.

---

## Template 1: coverage-analyzer

### Usage Context
**Replaces:** Phase 1 - Test Coverage Analysis Workflow (inline ~300 lines)
**When to invoke:** After story implementation, before anti-pattern scanning
**Token savings:** ~12,000 tokens

### Invocation Template

```python
# Step 1: Load context files
tech_stack_content = Read(file_path=".devforgeai/context/tech-stack.md")
source_tree_content = Read(file_path=".devforgeai/context/source-tree.md")
coverage_thresholds_content = Read(file_path=".claude/skills/devforgeai-qa/assets/config/coverage-thresholds.md")

# Step 2: Extract language & determine test command
language = extract_language_from_tech_stack(tech_stack_content)
test_command = {
    "C#": "dotnet test --collect:'XPlat Code Coverage' --results-directory:./TestResults",
    "Python": "pytest --cov=src --cov-report=json --cov-report=term",
    "Node.js": "npm test -- --coverage --coverageReporters=json-summary",
    "Go": "go test ./... -coverprofile=coverage.out",
    "Rust": "cargo tarpaulin --out Json",
    "Java": "mvn test jacoco:report"
}.get(language)

# Step 3: Invoke subagent
coverage_result = Task(
    subagent_type="coverage-analyzer",
    description="Analyze test coverage by architectural layer",
    prompt=f"""Analyze test coverage for {story_id}.
**Context Files (READ-ONLY):**
{tech_stack_content}
{source_tree_content}
{coverage_thresholds_content}

Execute your 8-phase workflow: Load → Execute command → Classify by layer → Calculate → Validate → Identify gaps → Generate recommendations → Return JSON.
**Output:** coverage_summary, validation_result, gaps (file/layer/coverage/target/uncovered_lines/suggested_tests), blocks_qa, violations, recommendations.""",
    model="claude-haiku-4-5-20251001"
)

# Step 4: Handle response
if coverage_result["status"] != "success":
    Display: f"❌ Coverage analysis failed: {coverage_result['error']}"
    Display: f"   Remediation: {coverage_result['remediation']}"
    Return: {"status": "failure", "blocks_qa": true}

# Step 5: Extract results & update state
coverage_summary = coverage_result["coverage_summary"]
blocks_qa = blocks_qa OR coverage_result["blocks_qa"]

# Step 6: Display results
Display: f"\n=== Phase 1: Coverage Analysis ===\n  Overall: {coverage_summary['overall_coverage']:.1f}%\n  Business Logic: {coverage_summary['business_logic_coverage']:.1f}%\n  Application: {coverage_summary['application_coverage']:.1f}%\n  Infrastructure: {coverage_summary['infrastructure_coverage']:.1f}%"
```

### Response Handling

**Success response structure:**
```json
{
  "status": "success",
  "coverage_summary": { "overall_coverage": 87.5, "business_logic_coverage": 96.2, "application_coverage": 88.1, "infrastructure_coverage": 79.3 },
  "validation_result": { "business_logic_passed": true, "application_passed": true, "infrastructure_passed": false, "overall_passed": true },
  "gaps": [...],
  "blocks_qa": false,
  "violations": [...],
  "recommendations": [...]
}
```

**Error response structure:**
```json
{
  "status": "failure",
  "error": "Coverage command failed: ModuleNotFoundError: No module named 'pytest_cov'",
  "blocks_qa": true,
  "remediation": "Install pytest-cov: pip install pytest-cov"
}
```

### Integration Points

**Before invoking:**
- Load all 3 context files (tech-stack, source-tree, coverage-thresholds)
- Extract language from tech-stack.md
- Determine test command based on language

**After receiving response:**
- Check `status` field (success/failure)
- Update `blocks_qa` state: `blocks_qa = blocks_qa OR coverage_result["blocks_qa"]`
- Display coverage summary
- Store gaps for QA report
- Continue to Phase 2 if successful, HALT if failed

---

## Template 2: anti-pattern-scanner

### Usage Context
**Replaces:** Phase 2 - Anti-Pattern Detection Workflow (inline ~300 lines)
**When to invoke:** After coverage analysis, before spec compliance validation
**Token savings:** ~8,000 tokens

### Invocation Template

```python
# Step 1: Load all 6 context files
context_files = {}
for file in ["tech-stack.md", "source-tree.md", "dependencies.md",
             "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"]:
    context_files[file] = Read(file_path=f".devforgeai/context/{file}")

# Step 2: Extract language
language = extract_language_from_tech_stack(context_files["tech-stack.md"])

# Step 3: Invoke subagent
anti_pattern_result = Task(
    subagent_type="anti-pattern-scanner",
    description="Scan for anti-patterns and architecture violations",
    prompt=f"""Scan codebase for anti-patterns and architecture violations.
**Context Files (ENFORCE AS LAW):** {' | '.join(context_files.keys())}
Execute 9-phase workflow: Load & validate → Detect library substitution → Structure violations → Layer violations → Code smells → Security issues → Style inconsistencies → Aggregate violations → Return JSON.
**Detection Categories:** Library substitution (ORM/state manager/HTTP client/validation/testing swaps), Structure violations (wrong layers, unexpected dirs), Layer violations (cross-layer refs, circular deps), Code smells (God objects >15 methods, long methods >50 lines, magic numbers), Security (secrets, SQL injection, XSS, insecure deserialization), Style (missing docs, naming)
**Output:** violations {{critical: [], high: [], medium: [], low: []}}, summary {{counts}}, blocks_qa, blocking_reasons, recommendations.""",
    model="claude-haiku-4-5-20251001"
)

# Step 4: Handle response
if anti_pattern_result["status"] != "success":
    Display: f"❌ Anti-pattern scanning failed: {anti_pattern_result['error']}"
    Return: {"status": "failure", "blocks_qa": true}

# Step 5: Extract results & update state
summary = anti_pattern_result["summary"]
blocks_qa = blocks_qa OR anti_pattern_result["blocks_qa"]

# Step 6: Display results
Display: f"\n=== Phase 2: Anti-Pattern Detection ===\n  Critical: {summary['critical_count']}, High: {summary['high_count']}, Medium: {summary['medium_count']}, Low: {summary['low_count']}"
```

### Response Handling

**Success response structure:**
```json
{
  "status": "success",
  "violations": { "critical": [...], "high": [...], "medium": [...], "low": [...] },
  "summary": { "critical_count": 1, "high_count": 2, "medium_count": 5, "low_count": 12, "total_violations": 20 },
  "blocks_qa": true,
  "blocking_reasons": ["1 CRITICAL: Library substitution (Entity Framework ↔ Dapper)", "2 HIGH: Structure violations"],
  "recommendations": [...]
}
```

**Violation object:**
```json
{
  "type": "library_substitution | structure_violation | layer_violation | code_smell | security_vulnerability | style_inconsistency",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW",
  "file": "absolute/path/to/file.cs",
  "line": 142,
  "pattern": "ORM substitution",
  "locked_technology": "Dapper",
  "detected_technology": "Entity Framework Core",
  "evidence": "using Microsoft.EntityFrameworkCore;",
  "remediation": "Replace Entity Framework with Dapper per tech-stack.md."
}
```

**Error response:**
```json
{
  "status": "failure",
  "error": "Context file missing: .devforgeai/context/anti-patterns.md",
  "blocks_qa": true,
  "remediation": "Run /create-context to generate missing context files"
}
```

### Integration Points

**Before invoking:**
- Load ALL 6 context files
- Extract language from tech-stack.md

**After receiving response:**
- Check `status` field (success/failure)
- Update `blocks_qa` state: `blocks_qa = blocks_qa OR anti_pattern_result["blocks_qa"]`
- Display violation summary
- Store violations by severity for QA report
- Continue to Phase 3 if successful, HALT if failed

---

## Template 3: code-quality-auditor

### Usage Context
**Replaces:** Phase 4 - Code Quality Metrics Workflow (inline ~250 lines)
**When to invoke:** After spec compliance validation, before QA report generation
**Token savings:** ~6,000 tokens

### Invocation Template

```python
# Step 1: Load context files
tech_stack_content = Read(file_path=".devforgeai/context/tech-stack.md")
quality_metrics_content = Read(file_path=".claude/skills/devforgeai-qa/assets/config/quality-metrics.md")

# Step 2: Extract language
language = extract_language_from_tech_stack(tech_stack_content)

# Step 3: Invoke subagent
quality_result = Task(
    subagent_type="code-quality-auditor",
    description="Analyze code quality metrics (complexity, duplication, maintainability)",
    prompt=f"""Analyze code quality metrics for {story_id}.
**Context Files:** {tech_stack_content[:200]} | {quality_metrics_content[:200]}
Execute 8-phase workflow: Load & validate → Complexity analysis → Duplication detection → Maintainability calculation → Business impact → Refactoring patterns → Aggregate results → Return JSON.
**Metrics to Calculate:**
1. Cyclomatic complexity: avg per function, avg per file, max, functions >20 (CRITICAL), 15-20 (WARNING)
2. Code duplication: percentage, duplicate blocks, >25% (CRITICAL), 20-25% (WARNING)
3. Maintainability index (0-100): avg, low files <40 (CRITICAL), 40-50 (WARNING)
**Output:** metrics {{complexity, duplication, maintainability}}, extreme_violations (FOCUS on EXTREME ONLY: complexity >20, duplication >25%, MI <40), blocks_qa, blocking_reasons, recommendations.""",
    model="claude-haiku-4-5-20251001"
)

# Step 4: Handle response
if quality_result["status"] != "success":
    Display: f"❌ Code quality analysis failed: {quality_result['error']}"
    Return: {"status": "failure", "blocks_qa": true}

# Step 5: Extract results & update state
metrics = quality_result["metrics"]
blocks_qa = blocks_qa OR quality_result["blocks_qa"]

# Step 6: Display results
Display: f"\n=== Phase 4: Code Quality ===\n  Complexity: {metrics['complexity']['average_per_function']:.1f}, Duplication: {metrics['duplication']['percentage']:.1f}%, Maintainability: {metrics['maintainability']['average_index']:.1f}"
```

### Response Handling

**Success response structure:**
```json
{
  "status": "success",
  "metrics": {
    "complexity": { "average_per_function": 4.2, "average_per_file": 8.7, "max_complexity": { "file": "...", "function": "ProcessOrder", "score": 28, "threshold": 20 }, "functions_over_threshold": [...] },
    "duplication": { "percentage": 8.5, "threshold": 20, "duplicate_blocks": [...] },
    "maintainability": { "average_index": 72.4, "threshold": 50, "low_maintainability_files": [] }
  },
  "extreme_violations": [...],
  "blocks_qa": false,
  "blocking_reasons": [],
  "recommendations": [...]
}
```

**Extreme violation object:**
```json
{
  "type": "complexity | duplication | maintainability",
  "severity": "CRITICAL",
  "file": "src/Services/OrderProcessingService.cs",
  "function": "ProcessOrder",
  "line": 145,
  "metric": "Cyclomatic complexity: 28",
  "threshold": 20,
  "business_impact": "High bug risk (>20 complexity = 40% more defects). Difficult to test (28 code paths = 28 test cases). Onboarding slow (3x longer).",
  "refactoring_pattern": "Extract Method: Split ProcessOrder into ValidateOrder, CalculateTotal, ApplyDiscounts, ProcessPayment, UpdateInventory. Target: 5 methods <6 complexity each."
}
```

**Error response:**
```json
{
  "status": "failure",
  "error": "Analysis tool not available: radon (Python complexity analyzer)",
  "blocks_qa": true,
  "remediation": "Install radon: pip install radon"
}
```

### Integration Points

**Before invoking:**
- Load tech-stack.md and quality-metrics.md
- Extract language from tech-stack.md
- Define source paths and exclusions

**After receiving response:**
- Check `status` field (success/failure)
- Update `blocks_qa` state: `blocks_qa = blocks_qa OR quality_result["blocks_qa"]`
- Display metrics summary
- Store extreme violations for QA report
- Continue to Phase 5 if successful, HALT if failed

---

## Common Error Handling Pattern

For all three subagents, use this pattern:

```python
if result["status"] != "success":
    Display: f"❌ {phase_name} FAILED: {result['error']}"
    if "remediation" in result:
        Display: f"   Remediation: {result['remediation']}"

    blocks_qa = true
    Return: {"status": "failure", "phase_failed": phase_name, "subagent": subagent_name, "error": result["error"], "blocks_qa": true}
    HALT
```

---

## Subagent Invocation Checklist

Before invoking ANY subagent, verify:

| Item | Verification |
|------|--------------|
| **Context Files** | All required files loaded and passed to subagent |
| **Language Extraction** | Extracted from tech-stack.md correctly |
| **Story ID** | Available in scope |
| **Subagent Name** | Spelled correctly (coverage-analyzer, anti-pattern-scanner, code-quality-auditor) |
| **Model** | Specified (claude-haiku-4-5-20251001) |
| **Prompt Content** | Complete context passed, expected output format documented, guardrails included |
| **Error Handling** | Check status field, display errors + remediation |
| **State Management** | blocks_qa updated with OR operation (not assignment) |
| **Results Display** | Show subagent results to user |
| **Report Storage** | Results stored for QA report generation |

---

## Token Budget Impact

**Before subagent delegation:**
- Phase 1 (Coverage): ~12K tokens (inline)
- Phase 2 (Anti-Patterns): ~8K tokens (inline)
- Phase 4 (Quality): ~6K tokens (inline)
- **Total: ~26K tokens**

**After subagent delegation:**
- Phase 1 prompt: ~3K tokens
- Phase 2 prompt: ~4K tokens
- Phase 4 prompt: ~2K tokens
- **Total: ~9K tokens**

**Savings: ~17K tokens (65% reduction)**

---

## Testing Subagent Integration

### Integration Test Template

```python
def test_qa_skill_invokes_coverage_analyzer():
    """Test that devforgeai-qa skill successfully invokes coverage-analyzer"""
    # Given: Story with 88% coverage (below 95% business logic threshold)
    story_id = "STORY-TEST-001"

    # When: QA skill runs Phase 1
    qa_result = invoke_devforgeai_qa(story_id, mode="deep")

    # Then: coverage-analyzer was invoked
    assert "coverage_summary" in qa_result
    assert qa_result["coverage_summary"]["business_logic_coverage"] < 95

    # And: blocks_qa set correctly
    assert qa_result["blocks_qa"] == true

    # And: Gap recommendations provided
    assert len(qa_result["coverage_gaps"]) > 0


def test_qa_skill_invokes_anti_pattern_scanner():
    """Test that devforgeai-qa skill successfully invokes anti-pattern-scanner"""
    # Given: Story with library substitution (Dapper → Entity Framework)
    story_id = "STORY-TEST-002"

    # When: QA skill runs Phase 2
    qa_result = invoke_devforgeai_qa(story_id, mode="deep")

    # Then: anti-pattern-scanner was invoked
    assert "violations" in qa_result
    assert qa_result["violations"]["critical"][0]["type"] == "library_substitution"

    # And: blocks_qa set correctly
    assert qa_result["blocks_qa"] == true


def test_qa_skill_invokes_code_quality_auditor():
    """Test that devforgeai-qa skill successfully invokes code-quality-auditor"""
    # Given: Story with extreme complexity (function with complexity 28)
    story_id = "STORY-TEST-003"

    # When: QA skill runs Phase 4
    qa_result = invoke_devforgeai_qa(story_id, mode="deep")

    # Then: code-quality-auditor was invoked
    assert "metrics" in qa_result
    assert qa_result["metrics"]["complexity"]["max_complexity"]["score"] == 28

    # And: blocks_qa set correctly
    assert qa_result["blocks_qa"] == true

    # And: Business impact explanation provided
    assert "High bug risk" in qa_result["extreme_violations"][0]["business_impact"]
```

---

## Maintenance

**When to Update Templates:**
- **Context file format changes:** Update file loading logic
- **New language support:** Add language → tool mapping
- **Threshold changes:** Update threshold values in prompts
- **New subagent features:** Update prompt to invoke new capabilities
- **Output contract changes:** Update response parsing logic

**Template Version History:**
- v1.0 (2025-11-20): Initial templates for coverage-analyzer, anti-pattern-scanner, code-quality-auditor
- v1.1 (2025-11-24): Refactored for clarity, consolidated examples, improved formatting
