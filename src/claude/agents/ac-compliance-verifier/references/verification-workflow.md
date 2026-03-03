# Verification Workflow

**Purpose:** Systematically inspect source code to verify AC implementation with documented evidence.

---

## Integration Points

**Invoked during /dev workflow:**
- **Phase 4.5** (Post-Refactoring) - Verify ACs after code refactoring complete
- **Phase 5.5** (Post-Integration) - Verify ACs after integration testing complete

**Invoked during /qa workflow:**
- Deep validation mode for comprehensive AC verification

**Reports stored at:**
- `devforgeai/qa/verification/STORY-XXX-ac-verification.json`

---

## Source Code Inspection Workflow

### Step 1: Load Source Files for Inspection

**When source_files hints are provided:**
```
# Use hints from <verification><source_files> block
FOR each source_file in ac.source_files:
  Read(file_path="{source_file}")
  # Store file contents for inspection
```

**When source_files hints are NOT provided (Discovery Fallback):**
```
# Extract keywords from AC Given/When/Then
keywords = extract_keywords(ac.given, ac.when, ac.then)

# Search for relevant files using Glob and Grep
Glob(pattern="**/*.py")    # Python files
Glob(pattern="**/*.ts")    # TypeScript files
Glob(pattern="**/*.md")    # Markdown files

Grep(pattern="{keyword}", path="src/")
Grep(pattern="{keyword}", path=".claude/")

# Discovery-based verification has LOWER confidence per BR-002
```

**File Loading Requirements:**
- Use Read() tool exclusively for loading source file contents
- Handle file not found gracefully: log warning, continue with other files
- Handle empty files: log as inspected with no evidence
- Large files (>10K lines): Inspect first 2000 lines, note limitation

### Step 2: Analyze Code for Implementation Patterns

**For each AC's Given/When/Then requirements:**

1. **Search for Given (precondition) implementation:**
   ```
   Grep(pattern="{given_keyword}", path="{source_file}")
   # Look for setup, initialization, configuration
   ```

2. **Search for When (trigger) implementation:**
   ```
   Grep(pattern="{when_keyword}", path="{source_file}")
   # Look for function calls, event handlers, triggers
   ```

3. **Search for Then (expected result) implementation:**
   ```
   Grep(pattern="{then_keyword}", path="{source_file}")
   # Look for assertions, return values, state changes
   ```

**Match Type Classification:**

| Match Type | Definition | Confidence Impact |
|------------|------------|-------------------|
| `DIRECT` | Exact keyword/pattern match found | HIGH |
| `INFERRED` | Related pattern suggests implementation | MEDIUM |
| `PARTIAL` | Some elements found, others missing | LOW |

### Step 3: Document File Evidence

**FileEvidence Data Model:**

```json
{
  "file_path": "src/validators/ac_parser.py",
  "lines": [45, 46, 47, 50, 51],
  "code_snippet": "def parse_acceptance_criteria(content):\n    # Extract AC blocks\n    pattern = r'<acceptance_criteria id=",
  "match_type": "DIRECT"
}
```

**FileEvidence Field Specifications:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `file_path` | String | **Yes** | Relative path from project root (no absolute paths) |
| `lines` | Array<Integer> | No | Line numbers where evidence found (positive integers) |
| `code_snippet` | String | No | Relevant code excerpt (max 500 characters) |
| `match_type` | Enum | **Yes** | One of: `DIRECT`, `INFERRED`, `PARTIAL` |

**BR-001 Enforcement:** All evidence MUST reference specific file locations. FileEvidence without file_path is invalid.

### Step 4: Multi-File Evidence Aggregation

**When an AC spans multiple source files:**

1. Inspect ALL relevant files
2. Create FileEvidence for each file
3. Aggregate into SourceInspectionResult

**SourceInspectionResult Data Model:**

```json
{
  "ac_id": "AC3",
  "files_inspected": [
    {
      "file_path": ".claude/agents/ac-compliance-verifier.md",
      "lines": [50, 51, 52],
      "code_snippet": "<acceptance_criteria id=\"AC1\">",
      "match_type": "DIRECT"
    },
    {
      "file_path": "devforgeai/specs/context/coding-standards.md",
      "lines": [362, 380, 400],
      "code_snippet": "XML Acceptance Criteria Schema",
      "match_type": "DIRECT"
    }
  ],
  "implementation_found": true,
  "confidence": "HIGH"
}
```

**SourceInspectionResult Field Specifications:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `ac_id` | String | **Yes** | AC identifier (e.g., "AC1", "AC2") |
| `files_inspected` | Array<FileEvidence> | **Yes** | Minimum 1 file evidence required |
| `implementation_found` | Boolean | **Yes** | True if AC implementation verified |
| `confidence` | Enum | **Yes** | One of: `HIGH`, `MEDIUM`, `LOW` |

---

## Coverage Verification Workflow

Verify test coverage exists for each AC before marking verification complete.

### Step 1: Locate Test Directory

**Given** a story ID being verified, locate test files in story-scoped directories.

**Primary locations (checked in order):**
```
# Check both possible test directory locations
Glob(pattern="tests/STORY-{STORY_ID}/**/*.sh")
Glob(pattern="tests/STORY-{STORY_ID}/**/*.py")
Glob(pattern="devforgeai/tests/STORY-{STORY_ID}/**/*.sh")
Glob(pattern="devforgeai/tests/STORY-{STORY_ID}/**/*.py")
```

**BR-002 Enforcement:** Test directory location follows convention `tests/STORY-XXX/` or `devforgeai/tests/STORY-XXX/`.

### Step 2: Discover Test Files

**Given** located test directory, analyze test files following naming conventions.

**BR-001 Enforcement:** Test file naming convention patterns:

| Pattern | Format | Example |
|---------|--------|---------|
| Python style | `test_ac{N}_*.py` | `test_ac1_authentication.py` |
| Bash style | `test-ac{N}-*.sh` | `test-ac1-test-file-location.sh` |

### Step 3: Map Tests to ACs

**Given** located test files, map them to their corresponding ACs.

**AC Number Extraction:**
```
# Extract AC number from filename
FOR each test_file in ac_tests:
  # Pattern 1: test_ac{N}_description.py
  match = regex("test_ac(\d+)_", filename)

  # Pattern 2: test-ac{N}-description.sh
  IF not match:
    match = regex("test-ac(\d+)-", filename)

  IF match:
    ac_number = int(match.group(1))
    ac_test_mapping[f"AC{ac_number}"].append(test_file)
```

### Step 4: Check Test Existence per AC

**Given** an AC being verified, check for corresponding test file existence.

**Per-AC Iteration:**
```
FOR each ac in parsed_acceptance_criteria:
  ac_id = ac.id  # e.g., "AC1", "AC2"

  tests_for_ac = ac_test_mapping.get(ac_id, [])

  IF len(tests_for_ac) == 0:
    # Flag missing test
    flag_message = f"No test found for AC#{ac_number}"
    coverage_result.coverage_met = false
  ELSE:
    coverage_result.tests_found = tests_for_ac
    coverage_result.coverage_met = true
```

### Step 5: Validate Test Content

**Given** a test file exists for an AC, inspect its content for assertions.

**Read Test File:**
```
# Load test file content
Read(file_path="{test_file_path}")
```

**Assertion Detection:**
```
# Search for assertion patterns
Grep(pattern="assert|PASS|FAIL|expect|should", path="{test_file}")

# Bash test assertions
Grep(pattern="\[PASS\]|\[FAIL\]|\[TEST\]", path="{test_file}")

# Python assertions
Grep(pattern="assert.*==|assertTrue|assertEqual", path="{test_file}")
```

### CoverageResult Data Model

```json
{
  "ac_id": "AC1",
  "tests_found": ["test-ac1-file-location.sh", "test_ac1_edge_cases.py"],
  "coverage_met": true,
  "assertions_validated": true
}
```

---

## Verification Steps Summary

Follow these steps EXACTLY in order:

### Step 1: Read Story File
```
Read(file_path="devforgeai/specs/Stories/STORY-XXX-*.story.md")
```

Extract from story:
- All acceptance criteria (AC#1, AC#2, etc.)
- Given/When/Then conditions for each AC
- Technical specification components
- Source file hints (if provided)

### Step 2: Parse Acceptance Criteria

For each AC, identify:
- **Trigger condition** (Given/When)
- **Expected behavior** (Then)
- **Verification method** (how to prove it works)

### Step 3: Discover Source Files

**If source files hinted in story:**
```
Read(file_path="{hinted_file}")
```

**If source files NOT hinted:**
```
# Search for relevant code patterns
Glob(pattern="**/*.{py,ts,js,md}")
Grep(pattern="{AC_keyword}", path=".")
```

### Step 4: Verify Each AC

For EACH acceptance criterion:

1. **Locate code** - Find file(s) containing the feature
2. **Verify Given condition** - Confirm precondition setup exists
3. **Verify When condition** - Confirm trigger mechanism exists
4. **Verify Then condition** - Confirm expected outcome is produced
5. **Document evidence** - File path, Line numbers, Code snippet, PASS/FAIL status

---

## Verification Methods by AC Type

### File Existence AC
```
Glob(pattern="{expected_file_path}")
# PASS if file found, FAIL if not
```

### Content Presence AC
```
Grep(pattern="{expected_content}", path="{file}")
# PASS if pattern found, FAIL if not
```

### Configuration AC
```
Read(file_path="{config_file}")
# Parse and verify required fields present
```

### Behavior AC
```
# Read test file to verify behavior is tested
Read(file_path="tests/STORY-XXX/*.sh")
# Verify test assertions match expected behavior
```

### Negative AC (Something should NOT exist)
```
Grep(pattern="{forbidden_pattern}", path="{file}")
# PASS if NOT found, FAIL if found
```

---

## Performance Requirements

**NFR-001: Single File Performance**
- Read() tool execution: < 500ms per file
- Grep search execution: < 1 second per pattern

**NFR-002: Total AC Inspection Performance**
- Total per-AC inspection: < 15 seconds (for ACs spanning 5 files)
- Includes: file loading + pattern search + evidence documentation

**Performance Optimization:**
- Use specific file paths when hints available (avoid full codebase scan)
- Limit Glob patterns to relevant directories
- Inspect first 2000 lines for large files (>10K lines)

---

**Version:** 1.0
**Extracted from:** ac-compliance-verifier.md (STORY-334)
