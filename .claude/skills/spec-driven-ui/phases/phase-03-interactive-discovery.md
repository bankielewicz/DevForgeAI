# Phase 03: Interactive Discovery

**Purpose:** Guide user through technology and styling choices via AskUserQuestion flows.

**Pre-Flight:** Verify Phase 02 completed.

---

## Step 3.1: Load Interactive Discovery Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/interactive-discovery.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/interactive-discovery.md")
```

**VERIFY:**
- File content loaded into context
- Content contains AskUserQuestion flow definitions

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.1 --project-root=. 2>&1")
```

---

## Step 3.2: Load User Input Integration Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/ui-user-input-integration.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/ui-user-input-integration.md")
```

**VERIFY:**
- File content loaded into context
- Content contains AskUserQuestion pattern mappings

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.2 --project-root=. 2>&1")
```

---

## Step 3.3: Determine UI Type

**EXECUTE:**
```
AskUserQuestion:
  Question: "What type of user interface should I generate?"
  Header: "UI Type"
  Options:
    - label: "Web UI"
      description: "Browser-based interface (React, Blazor, ASP.NET, HTML)"
    - label: "Desktop GUI"
      description: "Native desktop application (WPF, Tkinter)"
    - label: "Terminal UI"
      description: "Command-line interface with formatting (box drawing, colors, tables)"
  multiSelect: false
```

Store result as UI_TYPE.

**VERIFY:**
- UI_TYPE is set to one of: "web", "gui", "tui"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.3 --project-root=. 2>&1")
```

---

## Step 3.4: Select Technology Framework

**EXECUTE:**
Based on UI_TYPE, present framework options:

**Web UI:**
```
AskUserQuestion:
  Question: "Which web framework should I use?"
  Header: "Framework"
  Options:
    - label: "React"
      description: "Functional components with JSX"
    - label: "Blazor"
      description: "C# components (Server or WASM)"
    - label: "ASP.NET MVC"
      description: "Server-rendered views with Razor"
    - label: "Plain HTML"
      description: "Vanilla HTML5 + CSS + JavaScript"
  multiSelect: false
```

**Desktop GUI:**
```
AskUserQuestion:
  Question: "Which desktop framework should I use?"
  Header: "Framework"
  Options:
    - label: "WPF (C#)"
      description: "Windows Presentation Foundation with XAML"
    - label: "Tkinter (Python)"
      description: "Python standard GUI library"
  multiSelect: false
```

**Terminal UI:**
```
No framework selection needed — terminal formatting is framework-agnostic.
Set FRAMEWORK = "terminal"
```

Store result as FRAMEWORK.

**VERIFY:**
- FRAMEWORK is set and non-empty

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.4 --project-root=. 2>&1")
```

---

## Step 3.5: Validate Against tech-stack.md

**EXECUTE:**
Compare selected FRAMEWORK against approved technologies in tech-stack.md (loaded in Phase 01).

```
IF FRAMEWORK in tech_stack_approved:
    Display: "Technology validated against tech-stack.md"
ELIF tech-stack.md has no frontend section:
    Display: "tech-stack.md does not specify frontend frameworks. Proceeding with user selection."
ELSE:
    AskUserQuestion:
      Question: "Selected framework '${FRAMEWORK}' is not in tech-stack.md. How should I proceed?"
      Header: "Tech Conflict"
      Options:
        - label: "Use selected framework"
          description: "Proceed with ${FRAMEWORK} (may require tech-stack.md update + ADR)"
        - label: "Choose approved framework"
          description: "Select from frameworks listed in tech-stack.md"
      multiSelect: false
```

**VERIFY:**
- Either framework is approved, or user has made a conflict resolution decision

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.5 --project-root=. 2>&1")
```

---

## Step 3.6: Select Styling Approach (Web UI Only)

**EXECUTE:**
```
IF UI_TYPE == "web":
    AskUserQuestion:
      Question: "Which styling approach should I use?"
      Header: "Styling"
      Options:
        - label: "Tailwind CSS"
          description: "Utility-first CSS framework"
        - label: "Bootstrap"
          description: "Component-based CSS framework"
        - label: "CSS Modules"
          description: "Scoped CSS per component"
        - label: "None / Custom"
          description: "Plain CSS or inline styles"
      multiSelect: false
ELSE:
    SKIP — styling selection not applicable for GUI/TUI
```

Store result as STYLING.

**VERIFY:**
- Web: STYLING is set
- GUI/TUI: Step marked as skipped (valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.6 --project-root=. 2>&1")
```

---

## Step 3.7: Select Theme (Web UI Only)

**EXECUTE:**
```
IF UI_TYPE == "web":
    AskUserQuestion:
      Question: "Which theme should I apply?"
      Header: "Theme"
      Options:
        - label: "Light"
          description: "Light background, dark text"
        - label: "Dark"
          description: "Dark background, light text"
        - label: "System"
          description: "Follow OS preference (prefers-color-scheme)"
      multiSelect: false
ELSE:
    SKIP — theme selection not applicable for GUI/TUI
```

Store result as THEME.

**VERIFY:**
- Web: THEME is set
- GUI/TUI: Step marked as skipped (valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.7 --project-root=. 2>&1")
```

---

## Step 3.7a: Select Aesthetic Vibe (Web UI Only)

**EXECUTE:**
```
IF UI_TYPE == "web":
    AskUserQuestion:
      Question: "What aesthetic vibe should the UI convey? This guides the emotional tone of the design while staying within the design system constraints."
      Header: "Aesthetic Vibe"
      Options:
        - label: "Sleek Dark FinTech"
          description: "Professional dark theme with sharp contrasts, data-dense layouts, and subtle gradients"
        - label: "Flat Clean Enterprise"
          description: "Minimalist light theme with ample whitespace, muted colors, and clear hierarchy"
        - label: "Glassmorphism"
          description: "Frosted glass effects, translucent layers, and vibrant accent colors"
        - label: "Soft Minimal SaaS"
          description: "Rounded corners, pastel accents, friendly typography, and generous spacing"
        - label: "Custom"
          description: "Describe your own aesthetic direction"
      multiSelect: false
ELSE:
    SKIP — aesthetic vibe selection not applicable for GUI/TUI
```

Store result as AESTHETIC_VIBE.

If user selects "Custom":
```
AskUserQuestion:
  Question: "Describe the aesthetic vibe you want (e.g., 'Playful consumer social with bold gradients' or 'Brutalist with heavy borders and monospace type')."
  Header: "Custom Vibe"
  Options:
    - label: "Provide description"
      description: "I'll describe the vibe in text"
  multiSelect: false
```

Store the custom description as AESTHETIC_VIBE.

**VERIFY:**
- Web: AESTHETIC_VIBE is set and non-empty
- GUI/TUI: Step marked as skipped (valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.7a --project-root=. 2>&1")
```

---

## Step 3.8: Define Components

**EXECUTE:**
Based on requirements from Phase 02 and technology selections, propose a component list:

Display component list to user and ask for confirmation:
```
AskUserQuestion:
  Question: "Here are the proposed components: [list]. Should I proceed with these, or would you like to modify the list?"
  Header: "Components"
  Options:
    - label: "Proceed as proposed"
      description: "Generate all listed components"
    - label: "Modify component list"
      description: "I'll describe changes to make"
  multiSelect: false
```

If user wants to modify: Accept their input and update the component list.

Store final list as COMPONENTS.

**VERIFY:**
- COMPONENTS list is non-empty
- At least one component defined

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=03 --step=3.8 --project-root=. 2>&1")
```

---

## Phase 03 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=03 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 04 (Template Loading).
