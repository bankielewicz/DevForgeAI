# Phase 06: Documentation & Formatter

**Purpose:** Create UI specification summary, update story file (if story mode), and invoke ui-spec-formatter subagent.

**Pre-Flight:** Verify Phase 05 completed.

---

## Step 6.1: Load Documentation Update Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/documentation-update.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/documentation-update.md")
```

**VERIFY:**
- File content loaded into context
- Content contains documentation procedures

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=06 --step=6.1 --project-root=. 2>&1")
```

---

## Step 6.2: Generate UI Spec Summary

**EXECUTE:**
Create a UI-SPEC-SUMMARY.md file with:
- Date and generation mode (story/standalone)
- Story ID (if applicable)
- Components generated (file path, framework, type)
- Technology stack selected
- Dependencies required
- Integration instructions
- Next steps for development

```
Write(file_path="devforgeai/specs/ui/UI-SPEC-SUMMARY.md", content=${SUMMARY_CONTENT})
```

**VERIFY:**
```
Glob(pattern="devforgeai/specs/ui/UI-SPEC-SUMMARY.md")
```
- File exists on disk

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=06 --step=6.2 --project-root=. 2>&1")
```

---

## Step 6.3: Update Story File (Story Mode Only)

**EXECUTE:**
```
IF MODE == "story":
    Read the story file
    Edit the story's Technical Specification section to add UI component references:
    - Generated component file path
    - Framework and styling used
    - Integration notes
ELSE:
    SKIP — standalone mode has no story file to update
```

**VERIFY:**
- Story mode: Story file updated with UI references
- Standalone mode: Step marked as skipped (valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=06 --step=6.3 --project-root=. 2>&1")
```

---

## Step 6.4: Load Formatter Integration Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/ui-spec-formatter-integration.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/ui-spec-formatter-integration.md")
```

Also load formatter guardrails:
```
Read(file_path="src/claude/skills/spec-driven-ui/references/ui-result-formatting-guide.md")
```

**VERIFY:**
- Both files loaded into context
- Integration reference contains invocation protocol

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=06 --step=6.4 --project-root=. 2>&1")
```

---

## Step 6.5: Invoke ui-spec-formatter Subagent

**EXECUTE:**
```
Agent(subagent_type="ui-spec-formatter", prompt="""
Validate and format the UI specification for display.

Input:
- UI Spec file: devforgeai/specs/ui/UI-SPEC-SUMMARY.md
- Generated component: ${OUTPUT_PATH}
- Mode: ${MODE}
- Framework: ${FRAMEWORK}
- UI Type: ${UI_TYPE}
- Styling: ${STYLING}
- Theme: ${THEME}
- Components: ${COMPONENTS}

Validate against context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, anti-patterns.md).
Return structured JSON with: status (SUCCESS/PARTIAL/FAILED), display template, component details, validation results, next steps.
""")
```

Capture subagent output as FORMATTER_RESULT.

**VERIFY:**
- FORMATTER_RESULT is non-empty
- FORMATTER_RESULT contains a status field (SUCCESS, PARTIAL, or FAILED)
- If FAILED: Record failure reason for Phase 07 handling

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=06 --step=6.5 --project-root=. 2>&1")
```

---

## Phase 06 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=06 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 07 (Specification Validation).
