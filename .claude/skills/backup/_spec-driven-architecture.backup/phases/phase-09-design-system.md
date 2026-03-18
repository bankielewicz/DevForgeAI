# Phase 09: Design System

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Generate design system context file for UI projects. CONDITIONAL phase — skip if no frontend framework detected in tech-stack.md |
| **REFERENCES** | `.claude/skills/designing-systems/assets/context-templates/design-system.md` |
| **STEP COUNT** | 3 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] UI framework detection executed against `tech-stack.md`
- [ ] Phase marked as either "completed" or "skipped-auto" in checkpoint
- [ ] If UI framework detected: `devforgeai/specs/context/design-system.md` exists and is non-empty
- [ ] If no UI framework: "09" added to `phases_skipped` array

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 10.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/assets/context-templates/design-system.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 9.0: UI Framework Detection (GATE)

**EXECUTE:**
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
```
Grep the loaded content for frontend framework indicators:
```
Grep(pattern="(React|Vue|Angular|Svelte|Next\\.js|Nuxt|Remix|SvelteKit|Blazor|WPF|WinForms|Electron|Tauri|Flutter|MAUI)", path="devforgeai/specs/context/tech-stack.md", output_mode="content")
```

**Decision logic:**
- If Grep returns zero matches: This is a backend-only or CLI project. Skip design system generation.
- If Grep returns one or more matches: UI framework detected. Proceed to Step 9.1.

If skipping, display:
```
"No UI framework detected in tech-stack.md. Skipping design system generation."
```

**VERIFY:**
- `tech-stack.md` was successfully read (non-empty content returned)
- Grep executed without error
- Decision (proceed or skip) is unambiguous based on match count

**RECORD:**
```json
checkpoint.phase_09.step_9_0 = {
  "tech_stack_read": true,
  "ui_framework_detected": "<true|false>",
  "detected_frameworks": ["<matched framework names>"],
  "gate_decision": "<proceed|skip>"
}
```

If `gate_decision` is "skip":
```json
checkpoint.phase_09.status = "skipped-auto",
checkpoint.phases_skipped = [...existing, "09"]
```
STOP phase execution. Proceed directly to Phase 10.

---

### Step 9.1: Gather Design Preferences

**EXECUTE:**
```
AskUserQuestion:
  Question: "What design system approach do you want for this project?"
  Header: "Design System Selection"
  Options:
    - label: "Custom design system"
      description: "Build from scratch with custom tokens, typography, and components"
    - label: "Framework-based"
      description: "Use an existing UI framework (Material UI, Tailwind, Bootstrap, Ant Design)"
    - label: "Existing design system"
      description: "Reference an existing design system document or URL"
  multiSelect: false
```

Based on user selection, gather additional preferences:
```
AskUserQuestion:
  Question: "Provide your design preferences (answer any that apply):"
  Header: "Design Preferences"
  Options:
    - label: "Color palette"
      description: "Primary, secondary, accent colors (e.g., '#3B82F6 blue primary')"
    - label: "Typography"
      description: "Font families (e.g., 'Inter for body, Fira Code for code')"
    - label: "Spacing scale"
      description: "Base unit (e.g., '4px base, 8-point grid')"
    - label: "Accessibility level"
      description: "WCAG AA (minimum) or WCAG AAA (enhanced)"
    - label: "Responsive breakpoints"
      description: "Target breakpoints (e.g., 'mobile 640px, tablet 1024px, desktop 1280px')"
  multiSelect: true
```

**VERIFY:**
- User response to design approach is non-empty
- At least one design preference was provided
- If "Existing design system" selected: user provided a reference path or URL

**RECORD:**
```json
checkpoint.phase_09.step_9_1 = {
  "design_approach": "<custom|framework_based|existing>",
  "framework_choice": "<Material UI|Tailwind|Bootstrap|Ant Design|null>",
  "color_palette": "<user input or null>",
  "typography": "<user input or null>",
  "spacing_scale": "<user input or null>",
  "accessibility_level": "<AA|AAA>",
  "responsive_breakpoints": "<user input or null>",
  "preferences_gathered": true
}
```

---

### Step 9.2: Generate design-system.md

**EXECUTE:**
```
Read(file_path=".claude/skills/designing-systems/assets/context-templates/design-system.md")
```
Load the template. Customize all template sections with user preferences from Step 9.1:
- Replace color token placeholders with user-specified palette
- Replace typography placeholders with user-specified fonts
- Replace spacing scale with user-specified base unit
- Set accessibility section to user-specified WCAG level
- Set breakpoints to user-specified values
- Add component library section based on framework choice

Write the customized file:
```
Write(file_path="devforgeai/specs/context/design-system.md", content=<customized_template>)
```

Verify the file was created:
```
Glob(pattern="devforgeai/specs/context/design-system.md")
```

**VERIFY:**
- Template was loaded successfully (Read returned non-empty content)
- `design-system.md` exists at target path (Glob returned exactly 1 match)
- File content length > 200 characters (not a stub or empty file)

**RECORD:**
```json
checkpoint.phase_09.step_9_2 = {
  "template_loaded": true,
  "file_written": "devforgeai/specs/context/design-system.md",
  "file_verified": true,
  "content_length": "<character count>",
  "status": "completed"
}
checkpoint.phase_09.status = "completed"
```

---

## Phase Transition Display

```
============================================================
  PHASE 09 COMPLETE: Design System
============================================================
  Status:              [COMPLETED / SKIPPED (no UI framework)]
  UI Framework:        [<detected> / None]
  Design Approach:     [<approach> / N/A]
  File Created:        [devforgeai/specs/context/design-system.md / N/A]
------------------------------------------------------------
  Proceeding to Phase 10: Validation Report
============================================================
```
