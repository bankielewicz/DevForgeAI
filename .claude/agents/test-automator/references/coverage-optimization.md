# Coverage Optimization

Reference documentation for test-automator subagent. Contains coverage gap detection, layer thresholds, and test pyramid validation.

---

## Coverage Thresholds by Layer

| Layer | Minimum Coverage | Priority |
|-------|------------------|----------|
| Business Logic | 95% | High - Core domain rules |
| Application | 85% | Medium - Use case orchestration |
| Infrastructure | 80% | Lower - Framework glue code |

---

## Focus on Business Logic

### High Priority (95% coverage)

- Domain entities and business rules
- Calculation logic
- Validation logic
- State transitions

### Medium Priority (85% coverage)

- Application services
- Use case orchestration
- API controllers

### Lower Priority (80% coverage)

- Infrastructure code (repositories, file I/O)
- Framework glue code

---

## Avoid Testing Framework Code

**Don't test:**
- Third-party libraries (already tested)
- Trivial getters/setters (no logic)
- Auto-generated code
- Framework-provided functionality

---

## Coverage Tools by Framework

### Python

```bash
pytest --cov=src --cov-report=term --cov-report=html
```

**Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-branch"

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

### JavaScript

```bash
jest --coverage
```

**Configuration (jest.config.js):**
```javascript
module.exports = {
  collectCoverage: true,
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

### C#

```bash
dotnet test --collect:"XPlat Code Coverage"
```

**Configuration (.runsettings):**
```xml
<RunSettings>
  <DataCollectionRunSettings>
    <DataCollectors>
      <DataCollector friendlyName="XPlat Code Coverage">
        <Configuration>
          <Format>cobertura</Format>
          <Exclude>[*]*.Generated.*</Exclude>
        </Configuration>
      </DataCollector>
    </DataCollectors>
  </DataCollectionRunSettings>
</RunSettings>
```

---

## Gap Detection Workflow

### 1. Read Coverage Report

```python
Read(file_path="devforgeai/qa/coverage/coverage-report.json")
```

- Identify files with coverage < thresholds
- Find uncovered lines, branches, functions

### 2. Classify by Layer

```python
def classify_file_layer(file_path):
    if "domain" in file_path or "entities" in file_path:
        return "business_logic", 95
    elif "services" in file_path or "application" in file_path:
        return "application", 85
    else:
        return "infrastructure", 80
```

### 3. Identify Gap Files

```python
for file in coverage_report.files:
    layer, threshold = classify_file_layer(file.path)
    if file.coverage < threshold:
        gaps.append({
            "file": file.path,
            "layer": layer,
            "current": file.coverage,
            "target": threshold,
            "gap": threshold - file.coverage
        })
```

### 4. Prioritize Gaps

```python
# Sort by gap size (largest first) within each layer
gaps.sort(key=lambda g: (layer_priority(g.layer), -g.gap))
```

---

## Test Pyramid Validation

### Expected Distribution

```
       /\
      /E2E\      10% - Critical user paths only
     /------\
    /Integr.\   20% - Component interactions
   /----------\
  /   Unit    \ 70% - Individual functions/methods
 /--------------\
```

### Distribution Validation

```python
def validate_test_pyramid(test_counts):
    total = sum(test_counts.values())
    if total == 0:
        return {"valid": False, "error": "No tests found"}

    unit_pct = test_counts["unit"] / total * 100
    integration_pct = test_counts["integration"] / total * 100
    e2e_pct = test_counts["e2e"] / total * 100

    # Tolerance: +/- 10%
    issues = []
    if unit_pct < 60:
        issues.append(f"Unit tests too low: {unit_pct:.1f}% (expect >= 60%)")
    if integration_pct > 30:
        issues.append(f"Integration tests too high: {integration_pct:.1f}% (expect <= 30%)")
    if e2e_pct > 15:
        issues.append(f"E2E tests too high: {e2e_pct:.1f}% (expect <= 15%)")

    return {
        "valid": len(issues) == 0,
        "distribution": {
            "unit": unit_pct,
            "integration": integration_pct,
            "e2e": e2e_pct
        },
        "issues": issues
    }
```

### Test Type Detection

```python
def detect_test_type(test_file_path, test_content):
    # Check directory patterns
    if "/unit/" in test_file_path or "test_unit_" in test_file_path:
        return "unit"
    if "/integration/" in test_file_path or "test_integration_" in test_file_path:
        return "integration"
    if "/e2e/" in test_file_path or "test_e2e_" in test_file_path:
        return "e2e"

    # Check content patterns
    if has_external_dependencies(test_content):
        return "integration"
    if has_ui_automation(test_content):
        return "e2e"

    return "unit"  # Default
```

---

## Coverage Gap Recommendations

### When Coverage is Below Threshold

**Generate recommendations for each gap:**

```python
def generate_recommendations(gap):
    recommendations = []

    # Read the source file
    source = Read(file_path=gap.file)

    # Find untested functions
    untested = find_untested_functions(source, gap.uncovered_lines)

    for func in untested:
        recommendations.append({
            "function": func.name,
            "lines": func.lines,
            "suggested_tests": [
                f"Test happy path for {func.name}",
                f"Test error handling in {func.name}",
                f"Test boundary conditions for {func.name}"
            ]
        })

    return recommendations
```

### Prioritization Criteria

1. **Business logic gaps first** - Highest impact on quality
2. **High complexity functions** - More likely to have bugs
3. **Recently modified code** - Most likely to introduce issues
4. **Public API methods** - User-facing behavior

---

## Coverage Report Format

### Input (coverage-report.json)

```json
{
  "summary": {
    "total_lines": 1000,
    "covered_lines": 850,
    "coverage_percentage": 85.0
  },
  "files": [
    {
      "path": "src/domain/order.py",
      "lines": 100,
      "covered": 92,
      "coverage": 92.0,
      "uncovered_lines": [45, 67, 89, 90, 91, 92, 93, 94]
    }
  ]
}
```

### Output (gaps.json)

```json
{
  "story_id": "STORY-123",
  "coverage_gaps": [
    {
      "file": "src/domain/order.py",
      "layer": "business_logic",
      "current_coverage": 92.0,
      "target_coverage": 95.0,
      "gap_percentage": 3.0,
      "uncovered_line_count": 8,
      "suggested_tests": [
        "Test order cancellation for partially shipped orders",
        "Test order total recalculation on item removal"
      ]
    }
  ]
}
```

---

## Best Practices

### 1. Focus on Meaningful Coverage

- Test behavior, not just lines
- Branch coverage matters more than line coverage
- Don't chase 100% - diminishing returns

### 2. Identify Untestable Code

- If code is hard to test, consider refactoring
- Extract dependencies for mocking
- Use dependency injection

### 3. Balance Speed and Coverage

- Unit tests should be fast
- Run coverage on CI, not every local commit
- Incremental coverage checking

### 4. Track Coverage Trends

- Monitor coverage over time
- Set PR gates for coverage regression
- Celebrate coverage improvements
