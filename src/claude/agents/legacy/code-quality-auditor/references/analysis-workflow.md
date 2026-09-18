# Code Quality Auditor - Analysis Workflow Details

**Version**: 1.0
**Parent Agent**: code-quality-auditor.md

This reference contains the detailed analysis workflows for complexity, duplication, maintainability, and Treelint integration that were extracted from the core agent file for progressive disclosure.

---

## Phase 2: Complexity Analysis (Detailed)

### Language-Specific Commands

**Python Projects:**
```
Bash(command="python -m radon cc src/ -s -j")  # JSON output
```

**Node.js Projects:**
```
Bash(command="npx eslint src/ --format json --rule 'complexity: [error, 20]'")
```

**C# Projects:**
```
Bash(command="python .claude/skills/spec-driven-qa/scripts/analyze_complexity.py src/")
```

### Aggregate Metrics Calculation

```
Collect all functions from analysis results:
  all_functions = []  # List of {file, function, complexity, line}

Calculate statistics:
  average_complexity = mean([f.complexity for f in all_functions])
  max_complexity = max([f.complexity for f in all_functions])

Filter functions exceeding thresholds:
  functions_over_threshold = [f for f in all_functions if f.complexity > complexity_warning]
```

---

## Phase 3: Duplication Analysis (Detailed)

### Language-Specific Commands

**Python:**
```
Bash(command="python .claude/skills/spec-driven-qa/scripts/detect_duplicates.py src/")
```

**Node.js:**
```
Bash(command="npx jscpd src/ --format json")
```

### Duplication Percentage Calculation

```
total_lines = count_lines_in_directory("src/")
duplicate_lines = sum([block.lines for block in duplicate_blocks])
duplication_percentage = (duplicate_lines / total_lines) * 100
```

---

## Phase 4: Maintainability Index (Detailed)

### MI Formula (Universal)

```
MI = 171 - 5.2 * ln(Halstead_Volume) - 0.23 * Cyclomatic_Complexity - 16.2 * ln(LOC)

Where:
  N = total_operators + total_operands
  n = unique_operators + unique_operands
  Halstead_Volume = N * log2(n)
```

### MI Scale

| MI Score | Rating | Description |
|----------|--------|-------------|
| >85 | Excellent | Highly maintainable |
| 65-85 | Good | Maintainable with minor improvements |
| 50-65 | Moderate | Some complexity issues |
| <50 | Difficult | High technical debt |
| <40 | Critical | Immediate refactoring needed |

**Python MI:** `Bash(command="python -m radon mi src/ -s -j")`

---

## Phase 1.5: Treelint AST Metrics Integration

### Step 1.5.1: Version Check
```
Bash(command="treelint --version 2>&1")
```
- Minimum: v0.12.0
- If unavailable or below minimum: `treelint_available = false` (fallback to language tools)

### Step 1.5.2: Language Extension Mapping
Supported: `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.rs`
Unsupported (skip Treelint): `.cs`, `.go`, `.java`

### Step 1.5.3: Function Length Extraction
```
Bash(command="treelint metrics --function-length --file {path} --format json")
```
Response schema: `{ file, functions: [{ name, line_start, line_end, length }] }`

### Step 1.5.4: Nesting Depth Calculation
```
Bash(command="treelint metrics --nesting-depth --file {path} --format json")
```
Response schema: `{ file, functions: [{ name, nesting_depth }] }`

### Step 1.5.5: Classification Thresholds
| Metric | WARNING | CRITICAL |
|--------|---------|----------|
| Function length | 100-149 lines | 150+ lines |
| Complexity | 10-14 | 15+ |
| Nesting depth | 4-5 levels | 6+ levels |

### Step 1.5.6: JSON Schema Validation
Required fields: `file` (string), `functions` (array), each function: `name`, `line_start`, `line_end`
If schema validation fails: log error, set `treelint_available = false`, fall back

### Step 1.5.7: Fallback and Error Handling
- Treelint not installed: fall back to radon/eslint/rubocop
- Version too low: fall back
- Unsupported file type: skip Treelint for that file
- Schema mismatch: log and fall back
- **NO HALT on Treelint failure** - workflow continues with fallback tools

### Step 1.5.8: Combined Results
Treelint is PRIMARY source when available (supplements, not replaces language-specific tools).
Output includes `source_attribution` array indicating which tools provided data.

---

## Phase 5: Business Impact Explanations

### Complexity Impact

| Complexity | Risk Level | Defect Rate | Testing Burden |
|-----------|------------|-------------|----------------|
| >30 | EXTREME | 60% more defects | 30+ test cases minimum |
| >20 | HIGH | 40% higher rate | N test cases for N complexity |
| >15 | WARNING | Approaching threshold | Consider preemptive refactoring |

### Duplication Impact
- Maintenance: linear cost increase per duplicate
- Bug risk: multiplicative (N duplicates = N places to fix)
- Code bloat: redundant codebase size increase

### Maintainability Index Impact
- MI <40: 50% slower modifications, 3x higher bug introduction risk
- MI 40-50: 2x longer modification time vs well-maintained code

---

## Phase 6: Refactoring Pattern Generation

### For High Complexity (>20)
1. Extract Method: break into 3-5 smaller focused methods
2. Guard Clauses: replace nested conditionals with early returns
3. Extract Validation: move validation to separate validator class

### For Extreme Complexity (>30)
1. Extract Method: split into 5-8 smaller methods (target <6 each)
2. Replace Conditional with Polymorphism
3. Introduce Parameter Object (if >5 parameters)
4. Replace Temp with Query
5. Decompose Conditional

### For High Duplication
1. Extract to shared utility class
2. Pull Up Method (for subclass duplication)
3. Template Method (for algorithm variations)

### For Low MI
1. Split file if >300 lines
2. Decompose class if >15 methods (SRP)
3. Extract methods for long functions
4. Simplify conditionals with guard clauses
