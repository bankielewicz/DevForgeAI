# Phase 05: Code Generation

**Purpose:** Generate production-ready UI component code based on template, requirements, and constraints.

**Pre-Flight:** Verify Phase 04 completed.

---

## Step 5.1: Load Code Generation Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/code-generation.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/code-generation.md")
```

**VERIFY:**
- File content loaded into context
- Content contains code generation procedures

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=05 --step=5.1 --project-root=. 2>&1")
```

---

## Step 5.2: Ensure Output Directory Exists

**EXECUTE:**
```
Bash(command="python src/claude/skills/spec-driven-ui/scripts/ensure_spec_dir.py 2>&1")
```
If script fails, try fallback:
```
Bash(command="python .claude/skills/spec-driven-ui/scripts/ensure_spec_dir.py 2>&1")
```

Parse source-tree.md for UI component directory (default: `devforgeai/specs/ui/`).

**VERIFY:**
- Script exits with code 0
- Output directory exists or was created

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=05 --step=5.2 --project-root=. 2>&1")
```

---

## Step 5.3: Generate Component Code

**EXECUTE:**
Using the loaded template (Phase 04), requirements (Phase 02), and technology selections (Phase 03):

1. Start with the loaded template as the base structure
2. Apply styling choices (STYLING from Phase 03)
3. Implement component structure from COMPONENTS list
4. Follow best practices loaded in Phase 04
5. Respect coding-standards.md conventions
6. Add accessibility features:
   - ARIA labels and roles
   - Semantic HTML elements
   - Keyboard navigation support
   - Focus management
7. Include inline comments explaining key sections
8. Apply anti-pattern prevention (check anti-patterns.md constraints)

Generate the final component code.

**VERIFY:**
- Generated code is non-empty
- Code uses the selected FRAMEWORK syntax
- Code includes accessibility attributes (ARIA or equivalent)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=05 --step=5.3 --project-root=. 2>&1")
```

---

## Step 5.4: Confirm Output Filename

**EXECUTE:**
Propose a filename based on component name and framework:

```
AskUserQuestion:
  Question: "Where should I save the generated component? Proposed: ${DEFAULT_PATH}"
  Header: "Output Path"
  Options:
    - label: "Use proposed path"
      description: "${DEFAULT_PATH}"
    - label: "Custom path"
      description: "I'll specify a different filename or location"
  multiSelect: false
```

If custom path: Accept user input for the file path.

Store as OUTPUT_PATH.

**VERIFY:**
- OUTPUT_PATH is set and non-empty
- Path is within project directory

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=05 --step=5.4 --project-root=. 2>&1")
```

---

## Step 5.5: Write Generated Code to File

**EXECUTE:**
```
Write(file_path="${OUTPUT_PATH}", content=${GENERATED_CODE})
```

**VERIFY:**
```
Glob(pattern="${OUTPUT_PATH}")
```
- File exists on disk
- File is non-empty

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=05 --step=5.5 --project-root=. 2>&1")
```

---

## Phase 05 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=05 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 06 (Documentation).
