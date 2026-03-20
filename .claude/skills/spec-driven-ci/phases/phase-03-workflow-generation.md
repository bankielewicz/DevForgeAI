# Phase 03: Workflow Template Generation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=ci --from=02 --to=03 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 03 |
| 1 | Phase 02 incomplete | HALT - complete Phase 02 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Generate all 4 workflow YAML files from templates and merged configuration
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** 4 workflow files in `.github/workflows/`
- **STEP COUNT:** 6 mandatory steps
- **REFERENCE FILES:** workflow-templates.md

---

## Reference Loading [MANDATORY]

Load ALL reference files fresh. Do NOT rely on memory from previous reads.

```
Read(file_path=".claude/skills/spec-driven-ci/references/workflow-templates.md")
```

---

## Mandatory Steps (6)

### Step 3.1: Load Workflow Templates Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/workflow-templates.md")
```

**VERIFY:**
File content is loaded into context. All 4 workflow template structures are visible.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=03 --step=3.1 --project-root=.
```

---

### Step 3.2: Generate dev-story.yml

**EXECUTE:**

Read the template:
```
Read(file_path=".claude/skills/spec-driven-ci/assets/templates/dev-story-workflow.yml")
```

Apply $MERGED_CONFIG values:
- Set `timeout-minutes` from $MERGED_CONFIG.timeout_minutes
- Set `CLAUDE_CODE_CACHE_ENABLED` from $MERGED_CONFIG.enable_prompt_caching
- Set `CLAUDE_CODE_MODEL` based on $MERGED_CONFIG.prefer_haiku
- Set `runs-on` from $MERGED_CONFIG.runner

IF $FORCE_FLAG == false AND file exists at `.github/workflows/dev-story.yml`:
  AskUserQuestion to confirm overwrite.

Write the configured workflow to `.github/workflows/dev-story.yml`.

**VERIFY:**
```
Glob(pattern=".github/workflows/dev-story.yml")
```
File exists. Read the file and confirm it contains:
- `workflow_dispatch` trigger with `story_id` input
- `CLAUDE_CODE_CACHE_ENABLED` environment variable
- `claude -p "/dev` command
- `actions/upload-artifact` step

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=03 --step=3.2 --project-root=.
```

---

### Step 3.3: Generate qa-validation.yml

**EXECUTE:**

Read the template:
```
Read(file_path=".claude/skills/spec-driven-ci/assets/templates/qa-validation-workflow.yml")
```

Apply $MERGED_CONFIG values:
- Set `timeout-minutes` from $MERGED_CONFIG.timeout_minutes
- Set `CLAUDE_CODE_CACHE_ENABLED` from $MERGED_CONFIG.enable_prompt_caching
- Set `runs-on` from $MERGED_CONFIG.runner

IF $FORCE_FLAG == false AND file exists at `.github/workflows/qa-validation.yml`:
  AskUserQuestion to confirm overwrite.

Write the configured workflow to `.github/workflows/qa-validation.yml`.

**VERIFY:**
```
Glob(pattern=".github/workflows/qa-validation.yml")
```
File exists. Read the file and confirm it contains:
- `pull_request` trigger on `main` branch
- Story ID extraction from PR title
- `claude -p "/qa` command
- `actions/github-script` for posting results

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=03 --step=3.3 --project-root=.
```

---

### Step 3.4: Generate parallel-stories.yml

**EXECUTE:**

Read the template:
```
Read(file_path=".claude/skills/spec-driven-ci/assets/templates/parallel-stories-workflow.yml")
```

Apply $MERGED_CONFIG values:
- Set `timeout-minutes` from $MERGED_CONFIG.timeout_minutes
- Set `max-parallel` from $MERGED_CONFIG.max_parallel_jobs
- Set `CLAUDE_CODE_CACHE_ENABLED` from $MERGED_CONFIG.enable_prompt_caching
- Set `CLAUDE_CODE_MODEL` based on $MERGED_CONFIG.prefer_haiku
- Set `runs-on` from $MERGED_CONFIG.runner

IF $FORCE_FLAG == false AND file exists at `.github/workflows/parallel-stories.yml`:
  AskUserQuestion to confirm overwrite.

Write the configured workflow to `.github/workflows/parallel-stories.yml`.

**VERIFY:**
```
Glob(pattern=".github/workflows/parallel-stories.yml")
```
File exists. Read the file and confirm it contains:
- `workflow_dispatch` trigger with `story_ids` input
- `matrix.story_id` with `fromJSON`
- `max-parallel` set to $MERGED_CONFIG.max_parallel_jobs
- `fail-fast: false`

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=03 --step=3.4 --project-root=.
```

---

### Step 3.5: Generate installer-testing.yml (Conditional)

**EXECUTE:**

Check if installer testing is enabled in $MERGED_CONFIG:

IF $MERGED_CONFIG has `installer_testing.enabled == true` OR if no explicit config and project has `installer/` directory:
  Read the template:
  ```
  Read(file_path=".claude/skills/spec-driven-ci/assets/templates/installer-testing-workflow.yml")
  ```
  Write to `.github/workflows/installer-testing.yml`.

ELSE:
  Display: "Installer testing workflow skipped (not enabled in configuration)."
  Set $INSTALLER_TESTING_SKIPPED = true with reason.

**VERIFY:**

IF generated:
```
Glob(pattern=".github/workflows/installer-testing.yml")
```
File exists.

IF skipped:
$INSTALLER_TESTING_SKIPPED = true with documented reason.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=03 --step=3.5 --project-root=.
```

---

### Step 3.6: Verify All Generated Workflows

**EXECUTE:**

Verify all generated workflow files have valid YAML structure by reading each one:

```
Read(file_path=".github/workflows/dev-story.yml")
Read(file_path=".github/workflows/qa-validation.yml")
Read(file_path=".github/workflows/parallel-stories.yml")
```

For each file, check:
1. File is non-empty
2. Contains `name:` key
3. Contains `on:` trigger section
4. Contains `jobs:` section
5. Contains `steps:` under each job

IF installer-testing.yml was generated:
```
Read(file_path=".github/workflows/installer-testing.yml")
```
Apply same checks.

**VERIFY:**
All generated files pass basic structural validation. Log the count of validated files.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=03 --step=3.6 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=ci --phase=03 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 03 complete | Proceed to Phase 04 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 04 |

**Phase 03 Summary:**
- dev-story.yml: Generated
- qa-validation.yml: Generated
- parallel-stories.yml: Generated
- installer-testing.yml: {Generated | Skipped: reason}
- All files validated: {true/false}
