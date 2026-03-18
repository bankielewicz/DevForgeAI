# Phase 02: Context Creation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Create all 6 immutable context files. These files become THE LAW for all subsequent development. |
| **REFERENCES** | `spec-driven-architecture/references/context-file-creation-workflow.md`, `spec-driven-architecture/assets/context-templates/*.md` (6 templates) |
| **STEP COUNT** | 7 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] All 6 context files exist at `devforgeai/specs/context/`
- [ ] Each file has content length > 100 characters (not empty/stub)
- [ ] Each file was customized with user input (not raw template)
- [ ] Checkpoint updated with all 6 file creation records

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 03.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-architecture/references/context-file-creation-workflow.md")
Read(file_path=".claude/skills/spec-driven-architecture/assets/context-templates/tech-stack.md")
Read(file_path=".claude/skills/spec-driven-architecture/assets/context-templates/source-tree.md")
Read(file_path=".claude/skills/spec-driven-architecture/assets/context-templates/dependencies.md")
Read(file_path=".claude/skills/spec-driven-architecture/assets/context-templates/coding-standards.md")
Read(file_path=".claude/skills/spec-driven-architecture/assets/context-templates/architecture-constraints.md")
Read(file_path=".claude/skills/spec-driven-architecture/assets/context-templates/anti-patterns.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 2.1: Create tech-stack.md

**EXECUTE:**
Load template from `spec-driven-architecture/assets/context-templates/tech-stack.md`. Present user with structured questions:
```
AskUserQuestion:
  Question: "Define the technology stack for this project. Specify: (1) Primary language and version, (2) Framework and version, (3) Database engine, (4) ORM/data access layer, (5) Testing framework, (6) Build/package tool."
  Header: "Technology Stack Definition"
```
Customize template with user responses. Write the completed file:
```
Write(file_path="devforgeai/specs/context/tech-stack.md", content=<customized_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/context/tech-stack.md")
```
- File exists (Glob returns exactly 1 match)
- Read file back and confirm content length > 100 characters
- Content includes user-specified language and framework

**RECORD:**
```json
{
  "step": "2.1",
  "file": "tech-stack.md",
  "created": true,
  "content_length": "<char_count>",
  "primary_language": "<from user input>"
}
```

---

### Step 2.2: Create source-tree.md

**EXECUTE:**
Load template from `spec-driven-architecture/assets/context-templates/source-tree.md`. Query user:
```
AskUserQuestion:
  Question: "Define the project directory structure. Specify: (1) Source code root directory, (2) Test directory pattern, (3) Layer structure (e.g., controllers/services/repositories), (4) Configuration directory, (5) Documentation directory."
  Header: "Source Tree Definition"
```
Customize template. Write:
```
Write(file_path="devforgeai/specs/context/source-tree.md", content=<customized_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/context/source-tree.md")
```
- File exists, content length > 100 characters
- Content includes user-specified directory structure

**RECORD:**
```json
{
  "step": "2.2",
  "file": "source-tree.md",
  "created": true,
  "content_length": "<char_count>"
}
```

---

### Step 2.3: Create dependencies.md

**EXECUTE:**
Load template from `spec-driven-architecture/assets/context-templates/dependencies.md`. Query user:
```
AskUserQuestion:
  Question: "List the project dependencies. For each: (1) Package name, (2) Version or range, (3) Purpose (runtime/dev/test), (4) Any version constraints or pinning requirements."
  Header: "Dependency Manifest"
```
Customize template. Write:
```
Write(file_path="devforgeai/specs/context/dependencies.md", content=<customized_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/context/dependencies.md")
```
- File exists, content length > 100 characters

**RECORD:**
```json
{
  "step": "2.3",
  "file": "dependencies.md",
  "created": true,
  "content_length": "<char_count>"
}
```

---

### Step 2.4: Create coding-standards.md

**EXECUTE:**
Load template from `spec-driven-architecture/assets/context-templates/coding-standards.md`. Query user:
```
AskUserQuestion:
  Question: "Define coding standards. Specify: (1) Naming conventions (variables, classes, files), (2) Error handling pattern, (3) Logging strategy, (4) Comment requirements, (5) Maximum function/file length."
  Header: "Coding Standards Definition"
```
Customize template. Write:
```
Write(file_path="devforgeai/specs/context/coding-standards.md", content=<customized_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/context/coding-standards.md")
```
- File exists, content length > 100 characters

**RECORD:**
```json
{
  "step": "2.4",
  "file": "coding-standards.md",
  "created": true,
  "content_length": "<char_count>"
}
```

---

### Step 2.5: Create architecture-constraints.md

**EXECUTE:**
Load template from `spec-driven-architecture/assets/context-templates/architecture-constraints.md`. Query user:
```
AskUserQuestion:
  Question: "Define architecture constraints. Specify: (1) Layer boundaries and allowed dependencies, (2) Mandatory design patterns (DI, Repository, etc.), (3) Forbidden cross-layer calls, (4) API versioning strategy, (5) Data access rules."
  Header: "Architecture Constraints Definition"
```
Customize template. Write:
```
Write(file_path="devforgeai/specs/context/architecture-constraints.md", content=<customized_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/context/architecture-constraints.md")
```
- File exists, content length > 100 characters

**RECORD:**
```json
{
  "step": "2.5",
  "file": "architecture-constraints.md",
  "created": true,
  "content_length": "<char_count>"
}
```

---

### Step 2.6: Create anti-patterns.md

**EXECUTE:**
Load template from `spec-driven-architecture/assets/context-templates/anti-patterns.md`. Query user:
```
AskUserQuestion:
  Question: "Define anti-patterns to enforce. Specify: (1) Project-specific code smells to detect, (2) Maximum complexity thresholds, (3) Forbidden library usage patterns, (4) Known pitfalls from prior projects."
  Header: "Anti-Pattern Definitions"
```
Customize template. Write:
```
Write(file_path="devforgeai/specs/context/anti-patterns.md", content=<customized_content>)
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/context/anti-patterns.md")
```
- File exists, content length > 100 characters

**RECORD:**
```json
{
  "step": "2.6",
  "file": "anti-patterns.md",
  "created": true,
  "content_length": "<char_count>"
}
```

---

### Step 2.7: Verify All 6 Files

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/context/*.md")
```
Verify exactly 6 files returned. Read each file to confirm non-empty content:
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

**VERIFY:**
- Glob returns exactly 6 files
- Each file has content length > 100 characters
- No file contains only template placeholders (search for `TODO` or `PLACEHOLDER`)
- If ANY file is missing or empty: HALT immediately

**RECORD:**
```json
{
  "step": "2.7",
  "total_files": 6,
  "all_verified": true,
  "file_sizes": {
    "tech-stack.md": "<char_count>",
    "source-tree.md": "<char_count>",
    "dependencies.md": "<char_count>",
    "coding-standards.md": "<char_count>",
    "architecture-constraints.md": "<char_count>",
    "anti-patterns.md": "<char_count>"
  }
}
```

---

## Phase Transition Display

```
Display:
  "Phase 02 Complete: Context Creation"
  "All 6 immutable context files created and verified."
  "These files are now THE LAW for all development."
  "Proceeding to Phase 03: ADR Creation"
```
