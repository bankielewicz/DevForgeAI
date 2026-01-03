# Implementation Guide: session-miner Subagent

**Target File:** `.claude/agents/session-miner.md`
**Story:** STORY-221 - Parse and Normalize history.jsonl Data for Session Mining
**Status:** GREEN Phase (Implementation)
**Estimated Size:** <500 lines (framework constraint)

---

## Quick Start

### Minimum Viable Implementation

To make tests PASS (AC#1), start with this structure:

```markdown
---
name: session-miner
description: Extract and normalize session metadata from history.jsonl files
tools: [Read, Glob, Grep]
model: claude-opus-4-5
---

# Session Miner Subagent

You are a JSON lines parsing specialist. Your role is to:
1. Parse history.jsonl files (JSON lines format)
2. Extract and normalize metadata fields
3. Handle errors gracefully
4. Support streaming/pagination for large files
5. Return structured JSON output

## Core Responsibilities

### Task 1: Parse JSON Lines with Error Tolerance
- Read history.jsonl line by line
- Parse valid JSON entries
- Log malformed entries (line number, error)
- Continue processing despite errors

### Task 2: Normalize Fields
- Timestamp → ISO8601 format
- Status → enum (success|error|partial)
- Duration → numeric milliseconds
- All 8 fields present in output

### Task 3: Streaming Support
- Accept offset parameter (skip N entries)
- Accept limit parameter (process max N)
- Return pagination metadata
- Avoid loading entire file

### Task 4: Output Structure
Return consistent JSON:
{
  "entries": [...],
  "metadata": {
    "total_count": 0,
    "processed_count": 0,
    "error_count": 0,
    "errors": []
  }
}

## Input Parameters
- file_path: Path to history.jsonl
- offset: (optional) Skip first N entries
- limit: (optional) Process max N entries

## Output Format
Always return valid JSON with entries array and metadata object.
```

---

## Implementation Checklist

### AC#1: JSON Lines Parsing with Error Tolerance

**Tests:** 5 tests in `test-ac1-json-lines-parsing-error-tolerance.sh`

- [ ] Read history.jsonl file line by line
- [ ] Parse each line as JSON (using native tools)
- [ ] Validate JSON structure for each entry
- [ ] Log malformed entries with:
  - Line number where error occurred
  - Error description (missing brace, invalid syntax, etc.)
- [ ] Continue processing after malformed entry
- [ ] Return list of successfully parsed entries
- [ ] Include error log in metadata

**Key Implementation Detail:**
Use `Read()` tool with line-by-line processing. For each line:
1. Check if line is valid JSON
2. If valid: add to entries array
3. If invalid: log error with line number and continue

**Error Log Example:**
```json
{
  "errors": [
    {
      "line": 3,
      "error": "MALFORMED_JSON",
      "message": "Missing closing brace"
    }
  ]
}
```

---

### AC#2: Structured Field Extraction (8 Fields)

**Tests:** 8 tests in `test-ac2-structured-field-extraction.sh`

Normalize these 8 required fields:

#### 1. timestamp
- **Current Format:** ISO8601 string (e.g., "2025-01-01T10:00:00Z")
- **Normalization:** Keep ISO8601, verify format
- **Validation:** Must match pattern: `YYYY-MM-DDTHH:MM:SSZ`
- [ ] Extract timestamp from entry
- [ ] Validate ISO8601 format
- [ ] Reject or correct non-ISO8601 timestamps

#### 2. command
- **Current Format:** String (e.g., "dev", "qa", "release")
- **Normalization:** Keep as-is (already normalized)
- **Validation:** Non-empty string
- [ ] Extract command field
- [ ] Ensure non-empty value

#### 3. status
- **Current Format:** String
- **Normalization:** Enum - must be "success", "error", or "partial"
- **Validation:** Only accept enum values
- [ ] Extract status field
- [ ] Validate against enum (success|error|partial)
- [ ] Log error if status not in enum

#### 4. duration_ms
- **Current Format:** Integer (milliseconds)
- **Normalization:** Must be numeric, positive
- **Validation:** Integer >= 0
- [ ] Extract duration_ms field
- [ ] Validate is numeric
- [ ] Validate is non-negative

#### 5. user_input
- **Current Format:** String
- **Normalization:** Keep as-is
- **Validation:** Non-empty string
- [ ] Extract user_input field
- [ ] Ensure non-empty value

#### 6. model
- **Current Format:** String (e.g., "claude-opus", "claude-haiku")
- **Normalization:** Standardize model names if needed
- **Validation:** Non-empty string
- [ ] Extract model field
- [ ] Keep consistent formatting

#### 7. session_id
- **Current Format:** String identifier (e.g., "sess-001")
- **Normalization:** Ensure consistent format
- **Validation:** Non-empty string
- [ ] Extract session_id field
- [ ] Ensure consistent identifier format

#### 8. project
- **Current Format:** String (e.g., "devforgeai", "test-project")
- **Normalization:** Standardize to lowercase
- **Validation:** Non-empty string
- [ ] Extract project field
- [ ] Normalize to lowercase or consistent case

**Implementation Pattern:**
```
For each valid JSON entry:
  IF entry has all 8 fields:
    Add to entries array with normalized values
  ELSE:
    Log missing field error
    Optionally skip entry or use defaults
```

---

### AC#3: Streaming/Pagination Support

**Tests:** 7 tests in `test-ac3-streaming-pagination-large-files.sh`

Support these parameters for large files:

#### offset Parameter
- **Purpose:** Skip first N entries
- **Type:** Integer
- **Default:** 0 (start from beginning)
- **Example:** offset=100 skips first 100 entries
- [ ] Accept offset parameter
- [ ] Skip first offset entries
- [ ] Start processing from entry at index offset

#### limit Parameter
- **Purpose:** Process maximum N entries per call
- **Type:** Integer
- **Default:** None (process all)
- **Example:** limit=50 processes only 50 entries
- [ ] Accept limit parameter
- [ ] Stop processing after limit entries
- [ ] Return exactly limit entries (or fewer if EOF)

#### Combined Usage
- **Example:** offset=200, limit=50 → Process entries 200-249
- [ ] Support both parameters together
- [ ] Correct handling of combined offset+limit

#### Pagination Metadata
Return in metadata object:
- `has_more`: Boolean - true if more entries after this batch
- `next_offset`: Integer - offset to use for next request
- `total_available`: Integer - total entries in file (if known)

**Example:**
```json
{
  "metadata": {
    "processed": 50,
    "has_more": true,
    "next_offset": 250,
    "total_available": 1000
  }
}
```

**Implementation Pattern:**
```
1. Read history.jsonl
2. Skip first offset entries (without processing)
3. Process limit entries (or remaining if < limit)
4. Set has_more = (processed_count + offset < total_count)
5. Set next_offset = offset + processed_count
6. Return pagination metadata
```

---

### AC#4: Output Structure Normalization

**Tests:** 8 tests in `test-ac4-output-structure-normalization.sh`

Ensure consistent JSON output structure:

#### Required Output Format

```json
{
  "entries": [
    {
      "timestamp": "ISO8601_string",
      "command": "string",
      "status": "success|error|partial",
      "duration_ms": number,
      "user_input": "string",
      "model": "string",
      "session_id": "string",
      "project": "string"
    }
  ],
  "metadata": {
    "total_count": number,
    "processed_count": number,
    "error_count": number,
    "has_more": boolean,
    "next_offset": number|null,
    "offset": number,
    "limit": number|null,
    "timestamp": "ISO8601_string",
    "errors": [
      {
        "line": number,
        "error": "error_type",
        "message": "error description"
      }
    ]
  }
}
```

**Validation Checklist:**
- [ ] All entries have exactly 8 fields
- [ ] All field types match specification
- [ ] timestamp is ISO8601 string
- [ ] duration_ms is integer
- [ ] status is enum value
- [ ] All other fields are strings
- [ ] metadata object present
- [ ] error_count reflects size of errors array
- [ ] processed_count = entries array length

#### Field Type Requirements

| Field | Type | Example |
|-------|------|---------|
| timestamp | string (ISO8601) | "2025-01-01T10:00:00Z" |
| command | string | "dev" |
| status | string (enum) | "success" |
| duration_ms | number (integer) | 5000 |
| user_input | string | "STORY-001" |
| model | string | "claude-opus" |
| session_id | string | "sess-001" |
| project | string | "devforgeai" |

---

## Test Data for Manual Testing

### Create test-data.jsonl

```bash
cat > /tmp/test-history.jsonl << 'EOF'
{"timestamp": "2025-01-01T10:00:00Z", "command": "dev", "status": "success", "duration_ms": 5000, "user_input": "STORY-001", "model": "claude-opus", "session_id": "sess-001", "project": "devforgeai"}
{"timestamp": "2025-01-01T10:05:00Z", "command": "qa", "status": "error", "duration_ms": 3000, "user_input": "STORY-002", "model": "claude-haiku", "session_id": "sess-002", "project": "test-project"}
{MALFORMED_LINE
{"timestamp": "2025-01-01T10:15:00Z", "command": "release", "status": "partial", "duration_ms": 7500, "user_input": "deploy", "model": "claude-sonnet", "session_id": "sess-001", "project": "devforgeai"}
EOF
```

### Test Invocations

**Test 1: Basic parsing**
```
Invoke session-miner to parse /tmp/test-history.jsonl
Expected: 3 valid entries, 1 malformed logged, processing continues
```

**Test 2: With offset**
```
Invoke session-miner with offset=1, limit=2 on /tmp/test-history.jsonl
Expected: Entries 1-2 returned (qa, then skip malformed), release not included
```

**Test 3: Output structure**
```
Verify output has entries[] and metadata{}
Verify metadata has error_count=1, processed_count=3
```

---

## Development Workflow

### Step 1: Create Skeleton
```
Create .claude/agents/session-miner.md with:
- YAML frontmatter
- System prompt
- Core tasks (parsing, normalization, streaming, output)
```

### Step 2: Implement AC#1 (Error Tolerance)
```bash
bash test-ac1-json-lines-parsing-error-tolerance.sh
# Target: 5/5 PASS
```

### Step 3: Implement AC#2 (Field Extraction)
```bash
bash test-ac2-structured-field-extraction.sh
# Target: 8/8 PASS
```

### Step 4: Implement AC#3 (Streaming)
```bash
bash test-ac3-streaming-pagination-large-files.sh
# Target: 7/7 PASS
```

### Step 5: Implement AC#4 (Output)
```bash
bash test-ac4-output-structure-normalization.sh
# Target: 8/8 PASS
```

### Step 6: Run Full Suite
```bash
bash run-all-tests.sh
# Target: 28/28 PASS
```

---

## Performance Optimization Tips

### For 86MB File Processing

**Challenge:** Context window exhaustion with large files

**Solution:** Streaming with offset/limit

**Implementation:**
1. Don't use `Read()` to load entire file
2. Use `Grep` with limits to find lines
3. Read only offset to offset+limit lines
4. Return pagination metadata for next request

**Pseudo-code:**
```
function parse_batch(file_path, offset, limit):
    # Use Grep to find line numbers in range
    start_line = offset + 1  # 1-indexed
    end_line = offset + limit

    # Use Read with offset/limit to get lines
    lines = Read(file_path, offset=start_line, limit=limit)

    # Parse lines
    entries = parse_json_lines(lines)

    # Return with pagination metadata
    return {
        entries: entries,
        metadata: {
            processed: len(entries),
            has_more: (offset + limit < total_lines),
            next_offset: offset + limit
        }
    }
```

---

## Troubleshooting

### Issue: "Missing session-miner subagent"
**Cause:** File not at `.claude/agents/session-miner.md`
**Solution:** Create file at exact location

### Issue: "Tests timeout during parsing"
**Cause:** Loading entire 86MB file at once
**Solution:** Use streaming with offset/limit parameters

### Issue: "Invalid JSON in output"
**Cause:** Concatenating strings instead of building JSON structure
**Solution:** Use proper JSON array/object syntax

### Issue: "Malformed entries not logged"
**Cause:** Skipping errors without recording
**Solution:** Collect errors in array and include in metadata.errors

### Issue: "Field types mismatched"
**Cause:** Inconsistent types (e.g., duration_ms as string)
**Solution:** Validate types during normalization

---

## Framework Constraints (MUST FOLLOW)

1. **Location:** `.claude/agents/session-miner.md` (required)
2. **Size:** <500 lines maximum
3. **Tools:** Read, Glob, Grep only (no external libraries)
4. **Dependencies:** Zero (no pip install, npm install)
5. **No Skills:** Cannot invoke skills from subagent
6. **Format:** Markdown with YAML frontmatter

---

## Success Criteria

- [ ] All 28 tests PASS
- [ ] No external dependencies
- [ ] <500 lines of code
- [ ] Output follows exact JSON schema
- [ ] Handles 86MB files without timeout
- [ ] Error messages clear and helpful
- [ ] Pagination metadata correct
- [ ] All 8 fields normalized

---

## References

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-221-history-jsonl-parser.story.md`
- **Tests:** `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-221/`
- **Test Summary:** `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-221/TEST-SUMMARY.md`
- **Epic:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Epics/EPIC-034-session-data-mining.epic.md`

---

**Next Step:** Create `.claude/agents/session-miner.md` and implement the 4 ACs above.

Run tests frequently: `bash run-all-tests.sh`
