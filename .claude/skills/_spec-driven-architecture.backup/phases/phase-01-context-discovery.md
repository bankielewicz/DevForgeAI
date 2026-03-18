# Phase 01: Context Discovery

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Detect greenfield/brownfield project mode, gather technology inventory, apply question patterns for architecture decisions |
| **REFERENCES** | `designing-systems/references/context-discovery-workflow.md`, `designing-systems/references/user-input-guidance.md`, `designing-systems/references/architecture-user-input-integration.md` |
| **STEP COUNT** | 5 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] `project_mode` recorded as one of: "greenfield", "brownfield", "partial"
- [ ] `architecture_style` recorded from user selection
- [ ] `tech_inventory` recorded (or explicitly skipped for greenfield)
- [ ] `context_check_completed` set to true
- [ ] Checkpoint updated with phase data

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 02.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/references/context-discovery-workflow.md")
Read(file_path=".claude/skills/designing-systems/references/user-input-guidance.md")
Read(file_path=".claude/skills/designing-systems/references/architecture-user-input-integration.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 1.1: Detect Project Mode

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/context/*.md")
```
Count matching files. Classification:
- 6 files found = `brownfield`
- 0 files found = `greenfield`
- 1-5 files found = `partial`

**VERIFY:**
- Glob returned a result (even if empty array)
- `project_mode` is one of the three valid values
- If `partial`, list which files exist and which are missing

**RECORD:**
```json
{
  "phase": "01",
  "step": "1.1",
  "project_mode": "<greenfield|brownfield|partial>",
  "existing_context_files": ["<list of found files>"],
  "missing_context_files": ["<list of missing files>"]
}
```

---

### Step 1.2: Load Question Patterns

**EXECUTE:**
```
Read(file_path=".claude/skills/designing-systems/references/user-input-guidance.md")
```
Parse elicitation patterns from the loaded reference. Extract question categories and prompting strategies.

If file is missing or unreadable, degrade gracefully: use built-in question set (architecture style, language, database, deployment target).

**VERIFY:**
- Read returned content with length > 0, OR graceful degradation flag is set
- At least 3 question categories are available for subsequent steps

**RECORD:**
```json
{
  "step": "1.2",
  "question_patterns_loaded": true,
  "source": "<reference_file|built_in_fallback>",
  "category_count": "<number>"
}
```

---

### Step 1.3: Gather Architecture Preferences

**EXECUTE:**
```
AskUserQuestion:
  Question: "What architecture style best fits this project?"
  Header: "Architecture Style Selection"
  Options:
    - label: "Monolithic"
      description: "Single deployable unit. Best for MVPs, small teams, simple domains."
    - label: "Microservices"
      description: "Independent services per domain. Best for large teams, complex domains."
    - label: "Serverless"
      description: "Function-as-a-Service. Best for event-driven, variable-load workloads."
    - label: "Modular Monolith"
      description: "Monolith with enforced module boundaries. Best for growing projects."
  multiSelect: false
```

**VERIFY:**
- User response is non-empty
- User response matches one of the four valid options
- If user provides a custom answer outside the options, record verbatim and proceed

**RECORD:**
```json
{
  "step": "1.3",
  "architecture_style": "<user_selection>",
  "user_response_raw": "<verbatim response>"
}
```

---

### Step 1.4: Technology Inventory (Brownfield)

**CONDITIONAL:** Only execute if `project_mode` is `brownfield` or `partial`. If `greenfield`, skip with explicit skip record.

**EXECUTE:**
```
Glob(pattern="**/*.{ts,js,py,cs,java,go,rs}")
Glob(pattern="**/package.json")
Glob(pattern="**/requirements.txt")
Glob(pattern="**/*.csproj")
Glob(pattern="**/go.mod")
Glob(pattern="**/Cargo.toml")
```
Read the first matching config file from each pattern to extract language, framework, and dependency information.

**VERIFY:**
- At least one code file or config file was found (for brownfield/partial)
- `tech_inventory` object contains at least `languages` array with one entry
- If greenfield: verify skip was explicitly recorded, not silently omitted

**RECORD:**
```json
{
  "step": "1.4",
  "executed": "<true|false>",
  "skip_reason": "<greenfield_project|null>",
  "tech_inventory": {
    "languages": ["<detected languages>"],
    "frameworks": ["<detected frameworks>"],
    "config_files": ["<paths to config files read>"]
  }
}
```

---

### Step 1.5: Context Window Check

**EXECUTE:**
Estimate current context usage based on:
- Number of files read in this phase
- Size of checkpoint data accumulated
- Remaining phases to execute (3 more phases minimum)

If approaching 70% estimated capacity, offer save-and-resume:
```
AskUserQuestion:
  Question: "Context window is approaching capacity. Save checkpoint and resume in a new session?"
  Header: "Context Capacity Check"
  Options:
    - label: "Continue"
      description: "Proceed with remaining phases in this session"
    - label: "Save and Resume"
      description: "Write checkpoint file and resume later"
  multiSelect: false
```

**VERIFY:**
- Context check was performed (not skipped)
- If save-and-resume selected: checkpoint file written and verified via Glob
- If continue selected: proceed normally

**RECORD:**
```json
{
  "step": "1.5",
  "context_check_completed": true,
  "action": "<continue|save_and_resume>",
  "files_read_this_phase": "<count>"
}
```

---

## Phase Transition Display

```
Display:
  "Phase 01 Complete: Context Discovery"
  "Project mode: {project_mode} | Architecture: {architecture_style}"
  "Proceeding to Phase 02: Context Creation"
```
