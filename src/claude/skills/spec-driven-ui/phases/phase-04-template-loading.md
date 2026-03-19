# Phase 04: Template & Best Practices Loading

**Purpose:** Load framework-specific templates and UI type-specific best practices.

**Pre-Flight:** Verify Phase 03 completed.

---

## Step 4.1: Load Template Loading Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/template-loading.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/template-loading.md")
```

**VERIFY:**
- File content loaded into context
- Content contains template file mappings

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=04 --step=4.1 --project-root=. 2>&1")
```

---

## Step 4.2: Determine Template File

**EXECUTE:**
Map FRAMEWORK (from Phase 03) to template file:

| Framework | Template File |
|-----------|--------------|
| React | `assets/web-template.jsx` |
| Blazor | `assets/web-template.blazor.razor` |
| ASP.NET MVC | `assets/web-template.aspnet.cshtml` |
| Plain HTML | `assets/web-template.html` |
| WPF | `assets/gui-template.wpf.xaml` |
| Tkinter | `assets/gui-template.py` |
| Terminal | `assets/tui-template.py` |

**VERIFY:**
- Template file path determined
- Framework has a matching template

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=04 --step=4.2 --project-root=. 2>&1")
```

---

## Step 4.3: Load Template File

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/${TEMPLATE_PATH}")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/${TEMPLATE_PATH}")
```

**VERIFY:**
- Template content loaded into context
- Content is non-empty and contains component structure

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=04 --step=4.3 --project-root=. 2>&1")
```

---

## Step 4.4: Load UI Type-Specific Best Practices

**EXECUTE:**
Load ONLY the best practices file matching UI_TYPE (from Phase 03):

```
IF UI_TYPE == "web":
    Read(file_path="src/claude/skills/spec-driven-ui/references/web-best-practices.md")
ELIF UI_TYPE == "gui":
    Read(file_path="src/claude/skills/spec-driven-ui/references/gui-best-practices.md")
ELIF UI_TYPE == "tui":
    Read(file_path="src/claude/skills/spec-driven-ui/references/tui-best-practices.md")
```
If Read fails, try fallback path with `.claude/skills/...`

**VERIFY:**
- Best practices file loaded
- Content contains guidelines relevant to the UI type

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=04 --step=4.4 --project-root=. 2>&1")
```

---

## Step 4.5: Load Integration Guide

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/devforgeai-integration-guide.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/devforgeai-integration-guide.md")
```

**VERIFY:**
- File content loaded into context
- Content contains framework integration patterns

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=04 --step=4.5 --project-root=. 2>&1")
```

---

## Phase 04 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=04 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 05 (Code Generation).
