---
name: devforgeai-qa
description: Validates code quality through hybrid progressive validation (light checks during development, deep analysis after completion). Enforces test coverage (95%/85%/80% strict thresholds), detects anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when validating implementations, ensuring quality standards, or preparing for release.
tools: Read, Write, Edit, Glob, Grep, Bash
model: inherit
---

# DevForgeAI QA Skill

Quality validation skill that enforces architectural constraints, test coverage thresholds, and code quality standards through progressive validation modes.

---

## CRITICAL: Extracting Parameters from Conversation Context

**IMPORTANT:** Skills CANNOT accept runtime parameters like `--mode=deep`. All information must be extracted from conversation context.

### How Slash Commands Pass "Parameters" to Skills

When `/qa` command invokes this skill, it:
1. Loads story file via @file reference: `@.ai_docs/Stories/STORY-XXX.story.md`
2. States context explicitly: "Story ID: STORY-XXX" and "Validation mode: deep"
3. Invokes skill WITHOUT arguments: `Skill(command="devforgeai-qa")`

**You must extract story ID and mode from the conversation.**

### Story ID Extraction

**Method 1: Read YAML frontmatter**
```
Look for YAML frontmatter in conversation:
  ---
  id: STORY-XXX
  title: ...
  status: ...
  ---

Extract: id field = Story ID
```

**Method 2: Search for file reference**
```
Search conversation for pattern:
  ".ai_docs/Stories/STORY-XXX"

Extract STORY-XXX from file path
```

**Method 3: Search for explicit statement**
```
Search conversation for:
  "Story ID: STORY-XXX"
  "Story: STORY-XXX"

Extract STORY-XXX
```

### Validation Mode Extraction

**Look for mode in conversation:**
```
Search for patterns:
  - "Validation mode: deep" → MODE = deep
  - "Validation mode: light" → MODE = light
  - "Mode: deep" → MODE = deep
  - "Mode: light" → MODE = light
```

**If not found:**
```
Check story status from YAML frontmatter:
  - status: "Dev Complete" → MODE = deep (comprehensive validation before approval)
  - status: "In Development" → MODE = light (quick checks during development)
  - Other status → MODE = deep (default to thorough validation)
```

**Default:** deep (if unable to determine from context)

### Validation Before Proceeding

Before starting QA validation, verify:
- [ ] Story ID extracted successfully
- [ ] Story content available in conversation
- [ ] Validation mode determined (light or deep)
- [ ] Ready to proceed with QA phases

**If extraction fails:**
```
HALT with error:
"Cannot extract required parameters from conversation context.

Expected to find:
  - Story ID: YAML frontmatter with 'id: STORY-XXX' OR file reference
  - Validation mode: 'Validation mode: deep' OR inferred from story status

Please ensure story is loaded via slash command or provide parameters explicitly."
```

---

## Purpose

Validate code quality and enforce strict standards through:
- **Light validation** during development (fast feedback, ~10K tokens)
- **Deep validation** after completion (comprehensive analysis, ~65K tokens)
- **Coverage enforcement** (95% business logic, 85% application, 80% infrastructure)
- **Anti-pattern detection** (critical violations block immediately)
- **Spec compliance** (acceptance criteria, API contracts, NFRs)

---

## When to Use

### Automatic Invocation (Light Mode)
- **After implementation** (Phase 2 - Green in TDD)
- **After refactoring** (Phase 3 - Refactor in TDD)
- **After integration** (Phase 4 - Integration tests)

### Manual Invocation
- **Deep validation**: After story completion (`--mode=deep`)
- **Pre-release gates**: Before moving to QA Approved status
- **Technical debt assessment**: Analyze code quality metrics
- **Coverage improvement**: Identify test gaps

---

## Validation Modes

### Light Validation (~10,000 tokens)

**Purpose**: Fast feedback loop during development phases

**Checks**:
1. ✅ Build succeeds
2. ✅ Linting passes (auto-fix attempted)
3. ✅ Tests pass (phase-specific subset)
4. ✅ Quick coverage check (≥80% overall for integration phase)
5. ✅ Critical anti-patterns only (SQL injection, hardcoded secrets, layer violations, library substitution, file location violations)

**Success Criteria**:
- All checks pass
- Zero CRITICAL violations
- Token usage < 10,000

**Blocks immediately on**:
- Build failures
- Test failures
- Any CRITICAL violation

**Reference**: `./references/validation-procedures.md` (sections: Light Validation, Step 1-4)

---

### Deep Validation (~65,000 tokens)

**Purpose**: Comprehensive quality validation after story completion

**Phases**:
1. **Test Coverage Analysis** (Phase 1)
2. **Anti-Pattern Detection** (Phase 2)
3. **Spec Compliance Validation** (Phase 3)
4. **Code Quality Metrics** (Phase 4)
5. **Report Generation** (Phase 5)

**Success Criteria**:
- Coverage meets strict thresholds (95%/85%/80% by layer)
- Zero CRITICAL violations
- Zero HIGH violations (or approved exceptions)
- All acceptance criteria validated
- Quality metrics within thresholds
- Comprehensive report generated
- Story status updated
- Token usage < 65,000

**Reference**: `./references/validation-procedures.md` (section: Deep Validation)

---

## Phase 1: Test Coverage Analysis

### Step 1: Load Coverage Thresholds

```
Read(file_path=".devforgeai/qa/coverage-thresholds.md")

IF file not found:
    Use default strict thresholds:
    - Business Logic: 95%
    - Application: 85%
    - Infrastructure: 80%
    - Overall: 80%
```

### Step 2: Generate Coverage Reports

```
Read(file_path=".devforgeai/context/tech-stack.md")
# Extract language

# Execute language-specific coverage command
# See: ./references/language-specific-tooling.md

IF language == ".NET":
    Bash(command="dotnet test --collect:'XPlat Code Coverage'")
    coverage_file = "TestResults/*/coverage.cobertura.xml"

IF language == "Python":
    Bash(command="pytest --cov=src --cov-report=json")
    coverage_file = "coverage.json"

IF language == "Node.js":
    Bash(command="npm test -- --coverage")
    coverage_file = "coverage/coverage-summary.json"

IF language == "Go":
    Bash(command="go test ./... -coverprofile=coverage.out")
    coverage_file = "coverage.out"

IF language == "Rust":
    Bash(command="cargo tarpaulin --out Json")
    coverage_file = "tarpaulin-report.json"

IF language == "Java":
    Bash(command="mvn test jacoco:report")
    coverage_file = "target/site/jacoco/jacoco.xml"

Read(file_path=coverage_file)
```

### Step 3: Classify Files by Layer

```
Read(file_path=".devforgeai/context/source-tree.md")
# Extract layer definitions

# Classify files into Business Logic, Application, Infrastructure
# Based on source-tree patterns

business_logic_files = Glob matching business logic patterns
application_files = Glob matching application patterns
infrastructure_files = Glob matching infrastructure patterns
```

### Step 4: Calculate Coverage by Layer

Parse coverage data and aggregate by layer.

**Detailed procedures**: `./references/coverage-analysis.md`

### Step 5: Validate Against Thresholds

```
violations = []

IF business_logic_coverage < 95%:
    violations.append(CRITICAL: "Business logic coverage below 95%")

IF application_coverage < 85%:
    violations.append(CRITICAL: "Application coverage below 85%")

IF infrastructure_coverage < 80%:
    violations.append(HIGH: "Infrastructure coverage below 80%")

IF overall_coverage < 80%:
    violations.append(CRITICAL: "Overall coverage below 80%")
```

### Step 6: Identify Coverage Gaps

Find untested methods, generate test suggestions.

**Detailed procedures**: `./references/coverage-analysis.md` (section: Identifying Untested Code Paths)

### Step 7: Analyze Test Quality

- Count assertions per test (target: ≥1.5)
- Detect over-mocking (mocks > tests * 2)
- Validate test pyramid (70% unit, 20% integration, 10% E2E)

**Detailed procedures**: `./references/coverage-analysis.md` (sections: Test Quality Assessment, Test Pyramid)

---

## Phase 2: Anti-Pattern Detection

### Step 1: Load Context Files

```
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/source-tree.md")
Read(file_path=".devforgeai/context/architecture-constraints.md")
Read(file_path=".devforgeai/context/anti-patterns.md")
```

### Step 2: Detect Anti-Patterns by Category

#### Category 1: Library Substitution (CRITICAL)

```
# Check for library substitution
locked_orm = extract_from_tech_stack("ORM")

IF locked_orm == "Dapper":
    Grep(pattern="using EntityFramework|using Microsoft\\.EntityFrameworkCore",
         path="src/",
         output_mode="content")

    IF found:
        BLOCK: CRITICAL - Library substitution (EF instead of Dapper)
```

**Full detection algorithms**: `./references/anti-pattern-detection.md`

#### Category 2: Structure Violations (HIGH)

Validate file locations match source-tree.md rules.

**Detection algorithm**: `./references/anti-pattern-detection.md` (section: Category 2)

#### Category 3: Cross-Layer Dependencies (CRITICAL)

```
# Domain layer purity check
Grep(pattern="using.*Infrastructure|using.*Application",
     path="src/Domain/",
     output_mode="content")

IF found:
    BLOCK: CRITICAL - Domain layer references Infrastructure/Application
```

**Full detection**: `./references/anti-pattern-detection.md` (section: Category 3)

#### Category 4: Security Anti-Patterns (CRITICAL)

**SQL Injection:**
```
Grep(pattern="ExecuteRawSql\\(.*\\+|string\\.Format.*SELECT|f\"SELECT.*\\{",
     path="src/",
     output_mode="content")

IF found:
    BLOCK: CRITICAL - SQL Injection vulnerability
```

**Hardcoded Secrets:**
```
Grep(pattern="password|apikey|api_key|secret|token\\s*=\\s*[\"'][^\"']+[\"']",
     path="src/",
     -i=true,
     output_mode="content")

IF found AND looks_like_hardcoded_value:
    BLOCK: CRITICAL - Hardcoded secret detected
```

**Full security patterns**: `./references/security-scanning.md`

#### Category 5: Code Smells (MEDIUM/LOW)

- God Objects (>500 lines or >20 methods)
- High Complexity (cyclomatic complexity >10)
- Magic Numbers
- Long Methods (>100 lines)
- Code Duplication (>5%)

**Detection algorithms**: `./references/anti-pattern-detection.md` (section: Category 5)

### Step 3: Run Security Scanners

```
# Language-specific security scanners
IF language == "Python":
    Bash(command="bandit -r src/ -f json -o bandit-report.json")

IF language == "Node.js":
    Bash(command="npm audit --json > audit-report.json")

IF language == ".NET":
    Bash(command="dotnet list package --vulnerable --include-transitive")

IF language == "Rust":
    Bash(command="cargo audit")
```

**Full security scanning**: `./references/security-scanning.md`

### Step 4: Categorize Violations by Severity

```
CRITICAL: Security, architecture, library substitution violations
HIGH: Spec violations, structure violations
MEDIUM: Maintainability issues, code smells
LOW: Code quality, documentation
```

**Severity assessment**: `./references/anti-pattern-detection.md` (section: Severity Assessment)

---

## Phase 3: Spec Compliance Validation

### Step 0: Validate Story Documentation (CRITICAL)

**Before validating code, verify story file is properly documented**

```
Read(file_path=".ai_docs/Stories/{story_id}.story.md")
```

**Check for Implementation Notes section:**

```
IF "## Implementation Notes" NOT found in story:
    VIOLATION:
      Type: "Story documentation missing"
      Severity: HIGH
      Message: "Story file lacks Implementation Notes section"
      Impact: "Cannot validate spec compliance without documented implementation"
      Remediation: "Developer must update story file with Implementation Notes before QA approval"

    Record violation in QA report

    IF deep mode:
        FAIL QA - Story documentation is mandatory for deep validation
    ELSE IF light mode:
        WARN - Story documentation missing (not blocking for light QA)
```

**If Implementation Notes exist, validate completeness:**

```
Extract Implementation Notes section

Check required subsections:
1. Definition of Done Status
   - Verify: Each DoD item from story has status ([x] or [ ])
   - Verify: Incomplete items ([]) have reason (deferred/blocked/out of scope)

2. Test Results
   - Verify: Test counts present (unit/integration/e2e)
   - Verify: Coverage percentage documented
   - Verify: All tests passing status documented

3. Acceptance Criteria Verification
   - Verify: Each acceptance criterion has verification entry
   - Verify: Verification method documented (test name, manual check, etc.)

4. Files Created/Modified
   - Verify: At least one file listed
   - Verify: Files organized by layer (if applicable)

IF any required subsection missing:
    VIOLATION:
      Type: "Story documentation incomplete"
      Severity: MEDIUM
      Message: "Implementation Notes missing required section: {section_name}"
      Remediation: "Add {section_name} to Implementation Notes"

    Record violation

    IF deep mode:
        WARN - Documentation incomplete (may impact compliance validation)
```

**Validation success:**
```
✓ Story documentation complete
✓ Definition of Done documented
✓ Implementation decisions preserved
✓ Test results recorded
✓ Acceptance criteria verification present

Continue to Step 1 (Load Story Specification)
```

**Purpose of this validation:**
- Ensures story file is complete (requirements + implementation)
- Provides audit trail for QA validation
- Prevents knowledge loss (implementation decisions documented)
- Enables programmatic spec compliance checking
- Fulfills "spec-driven development" principle

---

### Step 1: Load Story Specification

```
Read(file_path=".ai_docs/Stories/{story_id}.story.md")
# Extract:
# - Acceptance criteria
# - API contracts
# - Non-functional requirements
# - Business rules
# - Implementation Notes (now validated in Step 0)
```

### Step 2: Validate Acceptance Criteria (Using Implementation Notes)

```
FOR each acceptance_criterion:
    # Extract keywords
    keywords = extract_keywords(criterion)

    # Find tests matching criterion
    test_pattern = create_pattern(keywords)
    tests = Grep(pattern=test_pattern, path="tests/", output_mode="files_with_matches")

    IF no tests found:
        FAIL: "No tests for acceptance criterion: {criterion}"
        Suggest test name

    IF tests found:
        # Verify tests pass
        Bash(command="[run specific tests]")

        IF tests fail:
            FAIL: "Tests fail for criterion: {criterion}"
```

**Detailed procedures**: `./references/spec-validation.md` (section: Acceptance Criteria Validation)

**Enhancement:** Cross-reference with Implementation Notes "Acceptance Criteria Verification" section to see how developer verified each criterion.

### Step 3: Validate API Contracts

```
FOR each api_endpoint in spec:
    # Check endpoint exists
    endpoint_pattern = create_route_pattern(endpoint)
    found = Grep(pattern=endpoint_pattern, path="src/")

    IF not found:
        FAIL: CRITICAL - Endpoint not implemented: {endpoint.path}

    IF found:
        # Validate request/response models
        actual_request = extract_request_model(found.file)
        actual_response = extract_response_model(found.file)

        IF actual_request != expected_request:
            FAIL: HIGH - Request model mismatch

        IF actual_response != expected_response:
            FAIL: HIGH - Response model mismatch
```

**Detailed procedures**: `./references/spec-validation.md` (section: API Contract Validation)

### Step 4: Validate Non-Functional Requirements

```
FOR each nfr in spec.nfrs:
    IF nfr.type == "performance":
        # Check for performance tests
        perf_tests = Glob(pattern="tests/Performance/**/*")

        IF no perf_tests:
            FAIL: "No performance tests for NFR: {nfr}"

    IF nfr.type == "security":
        # Check authentication/authorization
        endpoints = find_api_endpoints()
        FOR endpoint in endpoints:
            IF not has_auth_attribute(endpoint):
                FAIL: "Missing authentication: {endpoint}"
```

**Detailed procedures**: `./references/spec-validation.md` (section: Non-Functional Requirements)

### Step 5: Generate Traceability Matrix

```
traceability_matrix = []

FOR criterion in acceptance_criteria:
    tests = find_tests_for_criterion(criterion)
    impl = find_implementation(criterion)

    matrix.append({
        "requirement": criterion,
        "tests": tests,
        "implementation": impl,
        "status": "COMPLETE" if tests and impl else "INCOMPLETE"
    })
```

---

## Phase 4: Code Quality Metrics

### Step 1: Analyze Cyclomatic Complexity

```
# Use language-specific tools
IF language == "Python":
    Bash(command="radon cc src/ -a -j > complexity.json")

IF language == "Node.js":
    Bash(command="npx complexity-report src/ --format json > complexity.json")

Read(file_path="complexity.json")

# Parse results
FOR method WITH complexity > 10:
    violations.append(MEDIUM: "High complexity: {method} ({complexity})")
```

**Tools and thresholds**: `./references/quality-metrics.md`

### Step 2: Calculate Maintainability Index

```
IF language == "Python":
    Bash(command="radon mi src/ -s -j > maintainability.json")

Read(file_path="maintainability.json")

FOR file WITH maintainability_index < 70:
    violations.append(MEDIUM: "Low maintainability: {file} ({index})")
```

**Formula and thresholds**: `./references/quality-metrics.md` (section: Maintainability Index)

### Step 3: Detect Code Duplication

```
Bash(command="jscpd src/ --format json --output duplication.json")

Read(file_path="duplication.json")

duplication_percentage = calculate_duplication(duplication_data)

IF duplication_percentage > 5%:
    violations.append(LOW: "Code duplication {duplication_percentage}% (threshold 5%)")
```

**Thresholds**: `./references/quality-metrics.md` (section: Code Duplication)

### Step 4: Measure Documentation Coverage

```
# Count documented vs undocumented public APIs
public_apis = Grep(pattern="^\\s*public", path="src/", output_mode="count")

# Count documentation comments based on language
IF language == ".NET":
    docs = Grep(pattern="^\\s*///", path="src/", output_mode="count")

IF language == "Python":
    docs = Grep(pattern="^\\s*\"\"\"", path="src/", output_mode="count")

documentation_coverage = (docs / public_apis) * 100

IF documentation_coverage < 80%:
    violations.append(LOW: "Documentation coverage {documentation_coverage}% (target 80%)")
```

**Thresholds**: `./references/quality-metrics.md` (section: Documentation Coverage)

### Step 5: Analyze Dependency Coupling

```
# Detect circular dependencies
IF language == "Node.js":
    Bash(command="npx madge --circular src/ --json > circular.json")

Read(file_path="circular.json")

IF circular_dependencies found:
    violations.append(MEDIUM: "Circular dependencies detected")

# Count dependencies per file
FOR file WITH dependency_count > 10:
    violations.append(MEDIUM: "High coupling: {file} ({dependency_count} dependencies)")
```

**Tools and analysis**: `./references/quality-metrics.md` (section: Dependency Analysis)

---

## Phase 5: Generate QA Report

### Step 1: Aggregate Results

```
qa_results = {
    "story_id": story_id,
    "timestamp": current_timestamp(),
    "overall_status": determine_status(),
    "coverage": {
        "overall": overall_coverage,
        "business_logic": business_logic_coverage,
        "application": application_coverage,
        "infrastructure": infrastructure_coverage,
        "gaps": coverage_gaps
    },
    "anti_patterns": {
        "critical": critical_violations,
        "high": high_violations,
        "medium": medium_violations,
        "low": low_violations
    },
    "spec_compliance": {
        "acceptance_criteria": criteria_results,
        "api_contracts": contract_results,
        "nfrs": nfr_results,
        "traceability": traceability_matrix
    },
    "quality_metrics": {
        "complexity": complexity_results,
        "maintainability": maintainability_results,
        "duplication": duplication_results,
        "documentation": documentation_results,
        "coupling": coupling_results
    }
}
```

### Step 2: Determine Overall Status

```
IF critical_violations.count > 0:
    overall_status = "FAIL"
    blocking_reason = "Critical violations must be resolved"

IF high_violations.count > 0:
    overall_status = "FAIL"
    blocking_reason = "High severity violations must be resolved"

IF coverage_below_threshold:
    overall_status = "FAIL"
    blocking_reason = "Coverage below thresholds"

IF acceptance_criteria_failures > 0:
    overall_status = "FAIL"
    blocking_reason = "Acceptance criteria not met"

IF all above pass:
    overall_status = "PASS"
```

### Step 3: Write QA Report

```
report = generate_comprehensive_report(qa_results)

Write(file_path=".devforgeai/qa/reports/{story_id}-qa-report.md",
      content=report)
```

**Report template structure:**
```markdown
# QA Report: {story_id}

## Summary
- Status: {PASS/FAIL}
- Timestamp: {timestamp}
- Blocking Issues: {count}

## Test Coverage
- Overall: {percentage}% [✅/❌]
- By Layer: [table]
- Gaps: [list]

## Anti-Patterns
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}
- Details: [list]

## Spec Compliance
- Acceptance Criteria: {passed}/{total}
- API Contracts: {status}
- NFRs: {status}
- Traceability: [matrix]

## Code Quality Metrics
- Complexity: [results]
- Maintainability: [results]
- Duplication: [percentage]
- Documentation: [percentage]
```

### Step 4: Update Story Status

```
Read(file_path=".ai_docs/Stories/{story_id}.story.md")

IF overall_status == "PASS":
    Edit(file_path=".ai_docs/Stories/{story_id}.story.md",
         old_string="status: Dev Complete",
         new_string="status: QA Approved ✅")

    # Add QA completion to workflow history
    Add workflow history entry: "QA validation PASSED"

IF overall_status == "FAIL":
    Edit(file_path=".ai_docs/Stories/{story_id}.story.md",
         old_string="status: Dev Complete",
         new_string="status: QA Failed ❌")

    # Add failure details to workflow history
    Add workflow history entry: "QA validation FAILED: {blocking_reason}"
```

---

## Automation Scripts

### Python Scripts for Quality Analysis

The QA skill includes 6 Python automation scripts to accelerate quality analysis. These scripts can be invoked during deep validation phases to automate repetitive analysis tasks.

**Scripts Location:** `.claude/skills/devforgeai-qa/scripts/`

### Available Scripts

#### 1. `generate_coverage_report.py`
**Phase:** Phase 1 - Test Coverage Analysis
**Purpose:** Generate comprehensive test coverage reports with line, branch, and function coverage metrics
**Usage:**
```bash
python .claude/skills/devforgeai-qa/scripts/generate_coverage_report.py \
  --project-path=/path/to/project \
  --output=.devforgeai/qa/coverage/coverage-report.json
```

#### 2. `detect_duplicates.py`
**Phase:** Phase 2 - Anti-Pattern Detection (Code Duplication)
**Purpose:** Detect duplicated code blocks and calculate duplication percentage
**Usage:**
```bash
python .claude/skills/devforgeai-qa/scripts/detect_duplicates.py \
  --project-path=/path/to/project \
  --threshold=6 \
  --output=.devforgeai/qa/anti-patterns/duplicates-report.json
```

#### 3. `analyze_complexity.py`
**Phase:** Phase 2 - Anti-Pattern Detection (Cyclomatic Complexity)
**Purpose:** Calculate cyclomatic complexity and identify overly complex functions (complexity > 10)
**Usage:**
```bash
python .claude/skills/devforgeai-qa/scripts/analyze_complexity.py \
  --project-path=/path/to/project \
  --max-complexity=10 \
  --output=.devforgeai/qa/anti-patterns/complexity-report.json
```

#### 4. `security_scan.py`
**Phase:** Phase 2 - Anti-Pattern Detection (Security Vulnerabilities)
**Purpose:** Scan for common security anti-patterns (SQL injection, XSS, hardcoded secrets, etc.)
**Usage:**
```bash
python .claude/skills/devforgeai-qa/scripts/security_scan.py \
  --project-path=/path/to/project \
  --output=.devforgeai/qa/anti-patterns/security-report.json
```

#### 5. `validate_spec_compliance.py`
**Phase:** Phase 3 - Spec Compliance Validation
**Purpose:** Compare implementation against story acceptance criteria and validate API contracts
**Usage:**
```bash
python .claude/skills/devforgeai-qa/scripts/validate_spec_compliance.py \
  --story-path=.ai_docs/Stories/STORY-001.story.md \
  --project-path=/path/to/project \
  --output=.devforgeai/qa/spec-compliance/STORY-001-compliance-report.json
```

#### 6. `generate_test_stubs.py`
**Phase:** Phase 5 - Test Gap Auto-Fix
**Purpose:** Generate test stub templates for untested functions/methods
**Usage:**
```bash
python .claude/skills/devforgeai-qa/scripts/generate_test_stubs.py \
  --coverage-report=.devforgeai/qa/coverage/coverage-report.json \
  --output-dir=tests/generated/ \
  --framework=pytest
```

### Installation

**Install script dependencies:**
```bash
pip install -r .claude/skills/devforgeai-qa/scripts/requirements.txt
```

**Dependencies:**
- `coverage` - Test coverage measurement
- `radon` - Cyclomatic complexity analysis
- `bandit` - Security vulnerability detection
- `pytest` - Test framework integration
- `jinja2` - Test stub template generation

### Integration with Deep Validation

Scripts are automatically invoked during deep validation phases:

```python
# Phase 1: Test Coverage Analysis
Bash(command="python .claude/skills/devforgeai-qa/scripts/generate_coverage_report.py --project-path=. --output=.devforgeai/qa/coverage/coverage-report.json")
Read(file_path=".devforgeai/qa/coverage/coverage-report.json")

# Phase 2: Anti-Pattern Detection
Bash(command="python .claude/skills/devforgeai-qa/scripts/detect_duplicates.py --project-path=. --output=.devforgeai/qa/anti-patterns/duplicates-report.json")
Bash(command="python .claude/skills/devforgeai-qa/scripts/analyze_complexity.py --project-path=. --output=.devforgeai/qa/anti-patterns/complexity-report.json")
Bash(command="python .claude/skills/devforgeai-qa/scripts/security_scan.py --project-path=. --output=.devforgeai/qa/anti-patterns/security-report.json")
Read anti-pattern reports and aggregate violations

# Phase 3: Spec Compliance
Bash(command="python .claude/skills/devforgeai-qa/scripts/validate_spec_compliance.py --story-path=.ai_docs/Stories/{story_id}.story.md --output=.devforgeai/qa/spec-compliance/{story_id}-compliance-report.json")
```

### Manual Script Usage

Scripts can also be run manually by developers during development:

```bash
# Check coverage before committing
python .claude/skills/devforgeai-qa/scripts/generate_coverage_report.py --project-path=.

# Detect code duplication
python .claude/skills/devforgeai-qa/scripts/detect_duplicates.py --project-path=.

# Security scan
python .claude/skills/devforgeai-qa/scripts/security_scan.py --project-path=.
```

For detailed documentation on each script, see `.claude/skills/devforgeai-qa/scripts/README.md`.

---

## Success Criteria

### Light Validation Success
- ✅ Build succeeds
- ✅ Linting passes
- ✅ Tests pass
- ✅ Coverage ≥ 80% (integration phase only)
- ✅ Zero CRITICAL anti-patterns
- ✅ Token usage < 10,000

### Deep Validation Success
- ✅ Coverage meets strict thresholds (95%/85%/80%)
- ✅ Zero CRITICAL violations
- ✅ Zero HIGH violations (or approved exceptions)
- ✅ All acceptance criteria validated
- ✅ Quality metrics within thresholds
- ✅ Comprehensive report generated
- ✅ Story status updated
- ✅ Token usage < 65,000

---

## Reference Files

Load these on demand for detailed procedures:

### Core Validation
- **`./references/validation-procedures.md`** - Light and deep validation workflows, step-by-step procedures

### Coverage Analysis
- **`./references/coverage-analysis.md`** - Coverage metrics, tools, layer analysis, gap identification, test quality, pyramid validation

### Anti-Pattern Detection
- **`./references/anti-pattern-detection.md`** - Detection algorithms, categories, severity assessment, false positive handling

### Spec Compliance
- **`./references/spec-validation.md`** - Acceptance criteria validation, API contracts, NFRs, traceability matrix

### Code Quality
- **`./references/quality-metrics.md`** - Complexity, maintainability, duplication, documentation, coupling formulas and thresholds

### Security
- **`./references/security-scanning.md`** - Security patterns, SAST tools, OWASP Top 10 checks, vulnerability detection

### Language Tools
- **`./references/language-specific-tooling.md`** - Testing, coverage, linting, and quality tools for .NET, Python, Node.js, Go, Java, Rust

---

## Token Budget Management

**Target Budget**:
- Light validation: ~10,000 tokens
- Deep validation: ~65,000 tokens

**Optimization Strategies**:
1. Load reference files only when needed
2. Use Grep with `output_mode="files_with_matches"` for discovery (then Read specific files)
3. Parse coverage data incrementally by layer
4. Run language-specific tools efficiently (single command per tool)
5. Generate report at end (aggregate results in memory first)

---

**REMEMBER**: This skill enforces quality gates. CRITICAL and HIGH violations MUST block progression. Use AskUserQuestion for ambiguous cases only (coverage within 5% of threshold, non-critical code patterns).
