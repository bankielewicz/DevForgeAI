# Phase 07: Specification Validation

**Purpose:** Comprehensive validation of generated UI specification with user-driven issue resolution.

**Core Principle:** "Ask, Don't Assume" — Never auto-fix. All issues presented to user for resolution.

**Pre-Flight:** Verify Phase 06 completed.

---

## Step 7.1: Load Specification Validation Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/specification-validation.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/specification-validation.md")
```

**VERIFY:**
- File content loaded into context
- Content contains validation checklist

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=07 --step=7.1 --project-root=. 2>&1")
```

---

## Step 7.2: Completeness Check

**EXECUTE:**
Read the generated spec and validate these 10 required sections exist:
1. Component hierarchy
2. Props/API documented
3. State management approach
4. Styling approach
5. Accessibility considerations
6. Responsive behavior
7. Test strategy
8. Usage examples
9. Integration instructions
10. Dependencies listed

Record which sections are present and which are missing.

**VERIFY:**
- All 10 sections checked
- Missing sections list compiled

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=07 --step=7.2 --project-root=. 2>&1")
```

---

## Step 7.3: Placeholder Detection

**EXECUTE:**
```
Grep(pattern="TODO|TBD|FILL IN|PLACEHOLDER|FIXME", path="${OUTPUT_PATH}", output_mode="content")
```

Record all placeholders with line numbers.

**VERIFY:**
- Grep completed (even if no matches)
- Placeholder list compiled (may be empty — that's valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=07 --step=7.3 --project-root=. 2>&1")
```

---

## Step 7.4: Framework Constraint Validation

**EXECUTE:**
Read and validate against context files:
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

Check:
- Technology used matches tech-stack.md approved list
- File location matches source-tree.md patterns
- Dependencies are in dependencies.md approved list
- No forbidden anti-patterns present (God Objects, hardcoded values, etc.)

Compile validation summary with severity levels: HIGH / MEDIUM / LOW.

**VERIFY:**
- All 4 context files read
- Validation summary compiled with severity ratings

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=07 --step=7.4 --project-root=. 2>&1")
```

---

## Step 7.5: User Resolution of Issues

**EXECUTE:**
For each category of issues found, present to user via AskUserQuestion:

**Missing sections (if any):**
```
AskUserQuestion:
  Question: "The following spec sections are missing: [list]. How should I handle them?"
  Header: "Missing Sections"
  Options:
    - label: "Add with defaults"
      description: "I'll generate reasonable defaults for missing sections"
    - label: "Accept as-is"
      description: "Proceed without these sections (PARTIAL status)"
    - label: "Regenerate"
      description: "Regenerate the component with all sections"
  multiSelect: false
```

**Placeholders (if any):**
```
AskUserQuestion:
  Question: "Found ${COUNT} placeholders in the generated code. How should I handle them?"
  Header: "Placeholders"
  Options:
    - label: "Resolve now"
      description: "I'll help fill in each placeholder"
    - label: "Accept as-is"
      description: "Leave placeholders for manual resolution later"
  multiSelect: false
```

**Framework violations (if any):**
```
AskUserQuestion:
  Question: "Found constraint violations: [summary]. How should I proceed?"
  Header: "Violations"
  Options:
    - label: "Fix now"
      description: "Apply fixes to resolve violations"
    - label: "Show detailed report"
      description: "Display full violation details"
    - label: "Accept with warnings"
      description: "Proceed with PARTIAL status"
  multiSelect: false
```

Apply user decisions.

**VERIFY:**
- All issue categories presented to user (or skipped if no issues)
- User decisions captured and applied

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=07 --step=7.5 --project-root=. 2>&1")
```

---

## Step 7.6: Determine Final Validation Status

**EXECUTE:**
Based on validation results and user decisions:

```
IF no issues OR all issues resolved:
    STATUS = "SUCCESS"
ELIF user accepted warnings / partial completion:
    STATUS = "PARTIAL"
ELIF critical violations remain unresolved:
    STATUS = "FAILED"
    HALT — "Specification validation failed. Critical issues remain unresolved."
```

Display final status to user.

**VERIFY:**
- STATUS is one of: SUCCESS, PARTIAL, FAILED
- If FAILED: Workflow halts with error message

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=07 --step=7.6 --project-root=. 2>&1")
```

---

## Phase 07 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=07 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 08 (Feedback & Completion).
