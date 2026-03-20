# Phase 02: Configuration Loading

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=ci --from=01 --to=02 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 02 |
| 1 | Phase 01 incomplete | HALT - complete Phase 01 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Load or create CI configuration files with user preferences
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** $CONFIG_EXISTS, $CONFIG_LOADED, $CI_ANSWERS_LOADED, $MERGED_CONFIG
- **STEP COUNT:** 5 mandatory steps
- **REFERENCE FILES:** config-file-schema.md, ci-answers-protocol.md

---

## Reference Loading [MANDATORY]

Load ALL reference files fresh. Do NOT rely on memory from previous reads.

```
Read(file_path=".claude/skills/spec-driven-ci/references/config-file-schema.md")
Read(file_path=".claude/skills/spec-driven-ci/references/ci-answers-protocol.md")
```

---

## Mandatory Steps (5)

### Step 2.1: Load Configuration Schema Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/config-file-schema.md")
```

**VERIFY:**
File content is loaded into context. Schema for github-actions.yaml and ci-answers.yaml are visible.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=02 --step=2.1 --project-root=.
```

---

### Step 2.2: Check for Existing Configuration File

**EXECUTE:**
```
Glob(pattern="devforgeai/config/ci/github-actions.yaml")
```

IF file exists:
```
Read(file_path="devforgeai/config/ci/github-actions.yaml")
```
Set $CONFIG_EXISTS = true.

IF file does not exist:
Set $CONFIG_EXISTS = false. Display: "No existing configuration found. Will create with defaults."

**VERIFY:**
$CONFIG_EXISTS is boolean. If true, file content is loaded.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=02 --step=2.2 --project-root=.
```

---

### Step 2.3: Create or Merge Configuration

**EXECUTE:**

IF $CONFIG_EXISTS == false:
  Create `devforgeai/config/ci/github-actions.yaml` with defaults from the template:
  ```
  Read(file_path=".claude/skills/spec-driven-ci/assets/templates/github-actions-config.yaml")
  ```
  Write the template content to `devforgeai/config/ci/github-actions.yaml`.

IF $CONFIG_EXISTS == true:
  Merge existing values with defaults. Existing values take priority.
  Any missing keys are filled from template defaults.

Set $CONFIG_LOADED = true.

**Defaults:**
```yaml
cost_optimization:
  enable_prompt_caching: true
  prefer_haiku: true
  max_cost_per_story: 0.15
  max_turns:
    simple: 10
    complex: 20
    architecture: 30

workflow:
  max_parallel_jobs: 5
  timeout_minutes: 30
  runner: ubuntu-latest
```

**VERIFY:**
```
Read(file_path="devforgeai/config/ci/github-actions.yaml")
```
File exists and contains valid YAML with cost_optimization section.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=02 --step=2.3 --project-root=.
```

---

### Step 2.4: Load or Create CI Answers File

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/ci-answers-protocol.md")
```

Check for existing ci-answers.yaml:
```
Glob(pattern="devforgeai/config/ci/ci-answers.yaml")
```

IF file exists:
  ```
  Read(file_path="devforgeai/config/ci/ci-answers.yaml")
  ```
  Set $CI_ANSWERS_LOADED = true.

IF file does not exist:
  Create from template:
  ```
  Read(file_path=".claude/skills/spec-driven-ci/assets/templates/ci-answers-config.yaml")
  ```
  Write template content to `devforgeai/config/ci/ci-answers.yaml`.
  Set $CI_ANSWERS_LOADED = true.

**VERIFY:**
```
Read(file_path="devforgeai/config/ci/ci-answers.yaml")
```
File exists and contains headless answer entries.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=02 --step=2.4 --project-root=.
```

---

### Step 2.5: Collect User Configuration Overrides

**EXECUTE:**

Ask the user if they want to customize the default configuration:

```
AskUserQuestion:
  Question: "CI configuration uses these defaults. Would you like to customize?"
  Header: "CI Config"
  Options:
    - label: "Use defaults"
      description: "max-parallel: 5, prompt caching: on, Haiku model: on, timeout: 30min"
    - label: "Customize settings"
      description: "I'll ask about each setting individually"
  multiSelect: false
```

IF user selects "Customize settings":
  Ask about each configurable parameter:
  - max_parallel_jobs (1-10, default: 5)
  - enable_prompt_caching (true/false, default: true)
  - prefer_haiku (true/false, default: true)
  - timeout_minutes (10-60, default: 30)

  Update the configuration file with user's choices.

Set $MERGED_CONFIG = the final merged configuration values.

**VERIFY:**
$MERGED_CONFIG is populated with all required keys. Log the final values.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=02 --step=2.5 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=ci --phase=02 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 02 complete | Proceed to Phase 03 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 03 |

**Phase 02 Summary:**
- $CONFIG_EXISTS: {value}
- $CONFIG_LOADED: {value}
- $CI_ANSWERS_LOADED: {value}
- $MERGED_CONFIG: {summary of key values}
