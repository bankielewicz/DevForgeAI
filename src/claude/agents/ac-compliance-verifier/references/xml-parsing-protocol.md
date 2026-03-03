# XML AC Parsing Protocol

**Purpose:** Parse XML-formatted acceptance criteria from story files.

**XML format is REQUIRED for all story acceptance criteria.** There is no fallback to legacy markdown format per EPIC-046.

---

## XML AC Format Requirement

Stories MUST use XML-tagged acceptance criteria in this format:

```xml
<acceptance_criteria id="AC1">
  <given>Initial context or state</given>
  <when>Action or event that occurs</when>
  <then>Expected outcome or result</then>
  <verification>
    <source_files>
      - path/to/file1.py
      - path/to/file2.md
    </source_files>
    <test_file>tests/STORY-XXX/test_ac1.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Step 1: Detect XML AC Blocks

When parsing a story file, search for all `<acceptance_criteria id="ACX">` blocks:

```
# Pattern to find XML AC blocks
Grep(pattern="<acceptance_criteria id=", path="${STORY_FILE}")
```

**Extraction rules:**
- Each AC block starts with `<acceptance_criteria id="ACX">` where X is a number (AC1, AC2, etc.)
- The id attribute is REQUIRED and must be unique within the story
- Extract the full block content between opening and closing tags

---

## Step 2: Extract Given/When/Then Elements

For each `<acceptance_criteria>` block, extract the mandatory child elements:

| Element | Required | Description |
|---------|----------|-------------|
| `<given>` | **YES** | Initial context/state (precondition) |
| `<when>` | **YES** | Action/event that triggers behavior |
| `<then>` | **YES** | Expected outcome/result |

**Parsing approach:**
```
For each <acceptance_criteria> block:
  1. Extract text content from <given> element
  2. Extract text content from <when> element
  3. Extract text content from <then> element
  4. If any element missing → Mark AC as "incomplete"
```

---

## Step 3: Extract Optional Verification Hints

The `<verification>` element is OPTIONAL and provides hints for targeted inspection:

| Element | Required | Description |
|---------|----------|-------------|
| `<verification>` | No | Container for verification hints |
| `<source_files>` | No | List of files to inspect for this AC |
| `<test_file>` | No | Expected test file location |
| `<coverage_threshold>` | No | Coverage percentage target (0-100) |

**Extraction rules:**
- If `<verification>` block is present, extract all child elements
- If `<source_files>` present, parse as array of relative file paths
- If `<verification>` block is absent, return empty array for source_files
- Handle missing optional elements gracefully (no error, use defaults)

---

## Step 4: Build AcceptanceCriterion Data Model

For each parsed AC, construct a structured object:

```json
{
  "id": "AC1",
  "given": "Initial context text",
  "when": "Action text",
  "then": "Expected outcome text",
  "source_files": ["path/to/file1.py", "path/to/file2.md"],
  "test_file": "tests/STORY-XXX/test_ac1.sh",
  "coverage_threshold": 95,
  "status": "complete"
}
```

**Validation rules (per Business Rules):**
- **BR-001**: XML AC format is REQUIRED (no fallback to legacy)
- **BR-002**: AC IDs must be unique within story (warn on duplicate, use first occurrence)
- **BR-003**: Given/When/Then are mandatory (mark incomplete if missing)

---

## Step 5: HALT on Missing XML Format

**CRITICAL:** If story file does NOT contain any `<acceptance_criteria>` blocks (legacy markdown format):

```
HALT with error message:
"Story lacks required XML AC format. Update story to XML format per EPIC-046."
```

**Detection logic:**
```
ac_count = count(<acceptance_criteria id=") patterns in story file

IF ac_count == 0:
  HALT "Story lacks required XML AC format. Update story to XML format per EPIC-046."
```

**Do NOT attempt to parse legacy formats like:**
- `### AC#1:` markdown headers
- Numbered lists without XML tags
- Plain text acceptance criteria

---

## Step 6: Multi-AC Story Support

Stories may contain 1-20 acceptance criteria. Parse and return ALL ACs as a structured list:

```json
{
  "story_id": "STORY-XXX",
  "ac_count": 5,
  "acceptance_criteria": [
    {"id": "AC1", "given": "...", "when": "...", "then": "...", ...},
    {"id": "AC2", "given": "...", "when": "...", "then": "...", ...},
    {"id": "AC3", "given": "...", "when": "...", "then": "...", ...},
    {"id": "AC4", "given": "...", "when": "...", "then": "...", ...},
    {"id": "AC5", "given": "...", "when": "...", "then": "...", ...}
  ],
  "parse_status": "success",
  "warnings": []
}
```

**Multi-AC handling:**
- Iterate through all `<acceptance_criteria>` blocks in document order
- Validate uniqueness of id attributes per BR-002
- Return complete list even if some ACs are incomplete (flag them in status)
- Support minimum 1 AC to maximum 20 ACs per story

---

**Version:** 1.0
**Extracted from:** ac-compliance-verifier.md (STORY-334)
