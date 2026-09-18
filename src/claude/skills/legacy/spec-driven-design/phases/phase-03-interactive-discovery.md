# Phase 03: Interactive Discovery

**Purpose:** Guide user through technology and styling choices via AskUserQuestion flows. Step 3.0 offers a Claude Design fast-path that skips Steps 3.3 / 3.7 / 3.7a / 3.8 when the user provides a Claude Design handoff bundle (RESEARCH-010 REC-2, ADR-075). The existing 8-step flow remains the default fallback (user decision D3).

**Pre-Flight:** Verify Phase 02 completed.

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-design/references/interactive-discovery.md")
Read(file_path=".claude/skills/spec-driven-design/references/ui-user-input-integration.md")
Read(file_path=".claude/skills/spec-driven-design/references/claude-design-integration.md")
```

IF any Read fails: HALT -- "Phase 03 reference files not loaded."

---

## Step 3.0: Claude Design Fast-Path Detection

**Purpose:** Allow a user who has authored their design in Claude Design's web UI and exported a handoff bundle to skip the visual-discovery questions (UI type, theme, aesthetic vibe, component definition). The fast-path delegates token / component / layout extraction to `mockup-extractor` with `FRAMEWORK="claude-design-bundle"`. Framework choice + styling choice (Steps 3.4 + 3.6) still run because the bundle is framework-agnostic.

**EXECUTE:**
```
AskUserQuestion:
  Question: "Do you have a Claude Design handoff bundle to use for this UI?"
  Header: "Claude Design"
  Options:
    - label: "No — proceed with interactive discovery (8 questions)"
      description: "Use the standard Phase 03 flow: UI type, framework, styling, theme, aesthetic vibe, components."
    - label: "Yes — I have a bundle on disk"
      description: "Skip Steps 3.3 / 3.7 / 3.7a / 3.8 (extracted from bundle). Still asks framework + styling."
  multiSelect: false
```

```
IF answer == "No":
    CD_FASTPATH = false
    Continue to Step 3.1 (standard flow).
ELIF answer == "Yes":
    CD_FASTPATH = true
    AskUserQuestion:
      Question: "Path to the Claude Design handoff bundle directory?"
      Header: "Bundle path"
      Options:
        - label: "Provide path"
          description: "I'll enter the absolute or repo-relative path to the unpacked bundle."
      multiSelect: false
    Capture BUNDLE_PATH as the user-provided text.
    Validate:
      Glob(pattern="${BUNDLE_PATH}/PROMPT.md")
      Glob(pattern="${BUNDLE_PATH}/README.md")
      Glob(pattern="${BUNDLE_PATH}/INSTRUCTIONS.md")
    IF zero Instructions files found:
      Display: "No PROMPT.md / README.md / INSTRUCTIONS.md found at ${BUNDLE_PATH}. This does not appear to be a Claude Design bundle."
      AskUserQuestion: retry path / cancel fast-path (CD_FASTPATH=false) / cancel command (HALT).
```

**EXECUTE (fast-path branch — CD_FASTPATH=true):**
Bind the fast path explicitly to Web before accepting any bundle-derived state. Never infer platform later from the selected framework or artifact contents:

```
Bash(command="devforgeai-validate design-bind-context ${IDENTIFIER} ${WORKFLOW_FLAG} --platform=web --design-schema-version=1.1 --project-root=. 2>&1")
```

Any non-zero exit HALTs Phase 03 without recording step 3.0.

Set `PLATFORM = "web"`, then load the Web craft contract before any visual
choices or bundle-derived output are accepted:

```
IF PLATFORM == "web":
    Read(file_path=".claude/skills/spec-driven-design/references/design-craft.md")
```

```
Read(file_path=".claude/skills/spec-driven-design/references/claude-design-integration.md")
```
(Loads the bundle parsing contract — file detection candidates, defensive parsing rules, retirement triggers.)

```
Task(subagent_type="mockup-extractor",
     prompt=<<<
       FRAMEWORK: claude-design-bundle
       EXTRACT_PATH: ${BUNDLE_PATH}
       Follow the Claude Design Bundle pattern library in your agent definition.
       Probe for PROMPT.md / design-tokens.* / components.* / layout.* candidates
       per references/claude-design-integration.md. Extract tokens, components,
       layouts, flows. Populate design.md content. Return the standard
       structured JSON envelope.
     >>>
)
```

The subagent returns `design_md_content` along with the standard token / component / layout state. Primary writes `design.md`:

```
Write(file_path="devforgeai/specs/ui/design.md", content=design_md_content)
```

**VERIFY (fast-path):**
- `Glob(pattern="devforgeai/specs/ui/design.md")` returns 1 file.
- Read the file; confirm at least one COMP-NNN block, one token, and one LAYOUT-NNN block populated. If any is empty, emit a warning and ask the user whether to fall back to standard Phase 03 (CD_FASTPATH=false; re-run from Step 3.1).
- `mockup-extractor` returned `status` != `"bundle_not_detected"`; if it did, fall back automatically.

**RECORD (fast path only):**
```
IF CD_FASTPATH == true:
    Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.0 --project-root=. 2>&1")
```

The standard `CD_FASTPATH == false` branch does not record `3.0`; that step is
the deterministic alternative-path trigger.

**TRANSITION:**
- IF `CD_FASTPATH == false`: continue to Step 3.1.
- IF `CD_FASTPATH == true`: **SKIP Steps 3.1 / 3.2 / 3.3 / 3.7 / 3.7a / 3.8.** Continue to **Step 3.4** (framework selection — bundle is framework-agnostic) and complete Steps 3.4 / 3.5 / 3.6 only. Phase 03 then transitions to Phase 04.

---

## Step 3.1: Load Interactive Discovery Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-design/references/interactive-discovery.md")
```

**VERIFY:**
- File content loaded into context
- Content contains AskUserQuestion flow definitions

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.1 --project-root=. 2>&1")
```

---

## Step 3.2: Load User Input Integration Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-design/references/ui-user-input-integration.md")
```

**VERIFY:**
- File content loaded into context
- Content contains AskUserQuestion pattern mappings

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.2 --project-root=. 2>&1")
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
Set PLATFORM = UI_TYPE.

Bind the selected platform and generated document schema through the shared CLI before recording step 3.3:

```
Bash(command="devforgeai-validate design-bind-context ${IDENTIFIER} ${WORKFLOW_FLAG} --platform=${PLATFORM} --design-schema-version=1.1 --project-root=. 2>&1")
```

An identical retry is idempotent. Any invalid or conflicting binding HALTs without mutation.

Load craft only for the selected Web branch:

```
IF PLATFORM == "web":
    Read(file_path=".claude/skills/spec-driven-design/references/design-craft.md")
```

**VERIFY:**
- UI_TYPE is set to one of: "web", "gui", "tui"

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.3 --project-root=. 2>&1")
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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.4 --project-root=. 2>&1")
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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.5 --project-root=. 2>&1")
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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.6 --project-root=. 2>&1")
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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.7 --project-root=. 2>&1")
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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.7a --project-root=. 2>&1")
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
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --step=3.8 --project-root=. 2>&1")
```

---

## Phase 03 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate validate-design-phase ${IDENTIFIER} ${WORKFLOW_FLAG} --mode=${MODE} --phase=03 --project-root=. 2>&1")
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=03 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0; any non-zero result blocks completion

**NEXT:** Proceed to Phase 04 (Template Loading).

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
