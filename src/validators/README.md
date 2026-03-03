# Brainstorm Validator

**STORY-140: YAML-Malformed Brainstorm Detection**

## Overview

The `brainstorm-validator.js` module validates YAML syntax and schema for DevForgeAI brainstorm files. It ensures brainstorm files are properly formatted before being used by the ideation skill.

## Installation

The module is automatically available in the DevForgeAI framework. No additional installation required.

```javascript
const { BrainstormValidator, YAMLErrorMapper, ErrorTypes } = require('./src/validators/brainstorm-validator');
```

## Usage

### Basic Validation

```javascript
const { BrainstormValidator } = require('./src/validators/brainstorm-validator');

const result = BrainstormValidator.validate('/path/to/brainstorm.md');

if (result.valid) {
  console.log('Brainstorm is valid:', result.metadata);
} else {
  console.error(result.error.userMessage);
}
```

### Validation Result Structure

**Success:**
```javascript
{
  valid: true,
  metadata: {
    id: "BRAINSTORM-001",
    title: "User Authentication System",
    status: "Active",
    created: "2025-12-20",
    // Optional fields if present:
    problem_statement: "...",
    key_challenges: ["...", "..."],
    personas: ["...", "..."]
  }
}
```

**Failure:**
```javascript
{
  valid: false,
  error: {
    type: "UNCLOSED_FRONTMATTER",
    message: "Technical error description",
    userMessage: "User-friendly message with file path and line number",
    lineNumber: 5,
    canContinueWithoutBrainstorm: true
  }
}
```

---

## Validation Errors

The validator detects the following error types:

### Error Type 1: UNCLOSED_FRONTMATTER

**Cause:** Missing closing `---` delimiter in YAML frontmatter.

**Example Invalid File:**
```markdown
---
id: BRAINSTORM-001
title: My Brainstorm
status: Active
created: 2025-12-20
# Missing closing ---

Content here...
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Unclosed YAML frontmatter - missing closing --- delimiter
Line: 1

The file cannot be loaded in its current state.
```

**Resolution:**
Add the closing `---` delimiter after all frontmatter fields.

---

### Error Type 2: INVALID_INDENTATION

**Cause:** Tabs mixed with spaces in YAML frontmatter (YAML requires spaces only).

**Example Invalid File:**
```markdown
---
id: BRAINSTORM-001
key_challenges:
	- Challenge 1  # Tab character here!
  - Challenge 2
---
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Invalid indentation at line 4 - use spaces only (no tabs)
Line: 4

The file cannot be loaded in its current state.
```

**Resolution:**
Replace all tab characters with spaces (2 or 4 spaces per indent level).

---

### Error Type 3: DUPLICATE_KEY

**Cause:** Same key appears more than once in YAML frontmatter.

**Example Invalid File:**
```markdown
---
id: BRAINSTORM-001
title: My Brainstorm
id: BRAINSTORM-002  # Duplicate 'id' key!
status: Active
created: 2025-12-20
---
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Duplicate key 'id' at line 4
Line: 4

The file cannot be loaded in its current state.
```

**Resolution:**
Remove the duplicate key or rename if different values are needed.

---

### Error Type 4: INVALID_DATE_FORMAT

**Cause:** The `created` field doesn't match YYYY-MM-DD format.

**Example Invalid File:**
```markdown
---
id: BRAINSTORM-001
title: My Brainstorm
status: Active
created: December 20, 2025  # Wrong format!
---
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Invalid date format for 'created' field: expected YYYY-MM-DD, got 'December 20, 2025'

The file cannot be loaded in its current state.
```

**Resolution:**
Change the date to ISO format: `created: 2025-12-20`

---

### Error Type 5: MISSING_REQUIRED_FIELD

**Cause:** A required field (id, title, status, created) is missing.

**Example Invalid File:**
```markdown
---
title: My Brainstorm
status: Active
created: 2025-12-20
# Missing 'id' field!
---
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Missing required field: id

The file cannot be loaded in its current state.
```

**Resolution:**
Add the missing field with a valid value:
- `id: BRAINSTORM-NNN` (e.g., BRAINSTORM-001)
- `title: <descriptive title>`
- `status: Active|Complete|Abandoned`
- `created: YYYY-MM-DD`

---

### Error Type 6: INVALID_ID_PATTERN

**Cause:** The `id` field doesn't match the BRAINSTORM-NNN pattern.

**Example Invalid File:**
```markdown
---
id: my-brainstorm  # Wrong pattern!
title: My Brainstorm
status: Active
created: 2025-12-20
---
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Invalid id format: expected BRAINSTORM-NNN, got 'my-brainstorm'

The file cannot be loaded in its current state.
```

**Resolution:**
Change id to match pattern: `id: BRAINSTORM-001`

---

### Error Type 7: INVALID_STATUS_ENUM

**Cause:** The `status` field is not one of the allowed values.

**Example Invalid File:**
```markdown
---
id: BRAINSTORM-001
title: My Brainstorm
status: InProgress  # Not a valid status!
created: 2025-12-20
---
```

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: Invalid status: must be one of [Active, Complete, Abandoned], got 'InProgress'

The file cannot be loaded in its current state.
```

**Resolution:**
Change status to one of: `Active`, `Complete`, or `Abandoned`

---

### Error Type 8: EMPTY_FILE

**Cause:** The brainstorm file is empty (0 bytes).

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: File is empty - brainstorm files require YAML frontmatter

The file cannot be loaded in its current state.
```

**Resolution:**
Add YAML frontmatter with required fields (see template below).

---

### Error Type 9: BINARY_FILE

**Cause:** File contains binary content (not text).

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/file.md
Error: File contains binary content - cannot parse as text

The file cannot be loaded in its current state.
```

**Resolution:**
Ensure you're using the correct file (text-based Markdown, not binary).

---

### Error Type 10: FILE_NOT_FOUND

**Cause:** The specified file doesn't exist.

**Error Message:**
```
⚠️ Brainstorm file has invalid YAML

File: /path/to/nonexistent.md
Error: File not found: /path/to/nonexistent.md

The file cannot be loaded in its current state.
```

**Resolution:**
Verify the file path is correct and the file exists.

---

## Recovery Steps

When validation fails, you have two options:

### Option 1: Fix the File

1. Read the error message to identify the issue
2. Open the brainstorm file in an editor
3. Fix the specific issue mentioned (see error types above)
4. Re-run validation or the ideation command

### Option 2: Start Fresh

If the file is too corrupted to fix:
1. When prompted, choose "Yes, start fresh"
2. The ideation skill will continue without brainstorm context
3. You'll answer all discovery questions from scratch

---

## Valid Brainstorm Template

Use this template for creating valid brainstorm files:

```markdown
---
id: BRAINSTORM-001
title: Your Brainstorm Title
status: Active
created: 2025-12-20
problem_statement: One sentence describing the problem
key_challenges:
  - Challenge 1
  - Challenge 2
personas:
  - User type 1
  - User type 2
---

# Brainstorm: Your Title

## Problem Statement

Description of the problem...

## Key Challenges

1. Challenge details...

## Personas

- User type details...
```

---

## API Reference

### BrainstormValidator.validate(filePath)

Main entry point. Validates a brainstorm file.

**Parameters:**
- `filePath` (string): Absolute or relative path to the brainstorm file

**Returns:**
- Object with `valid` (boolean) and either `metadata` (on success) or `error` (on failure)

### BrainstormValidator.validateYAML(content, filePath)

Validates YAML syntax of file content.

**Parameters:**
- `content` (string): File content
- `filePath` (string): Path for error messages

**Returns:**
- Object with `valid` and `frontmatter` or `error`

### BrainstormValidator.validateSchema(frontmatter)

Validates schema of parsed frontmatter.

**Parameters:**
- `frontmatter` (object): Parsed YAML object

**Returns:**
- Object with `valid` or error details

### YAMLErrorMapper.mapError(yamlError)

Maps parser errors to user-friendly format.

**Parameters:**
- `yamlError` (Error): YAML parsing error

**Returns:**
- Object with `type`, `message`, `lineNumber`

---

## Test Coverage

- **33 unit tests** covering all acceptance criteria
- **Coverage:** 81.25% lines
- **Performance:** <10ms per validation (well under 100ms requirement)

Run tests:
```bash
npm test -- tests/STORY-140/test_brainstorm_validation.js --coverage
```

---

**Version:** 1.0.0
**STORY:** STORY-140
**Created:** 2025-12-28
