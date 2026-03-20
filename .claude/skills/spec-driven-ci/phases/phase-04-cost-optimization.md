# Phase 04: Cost Optimization

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=ci --from=03 --to=04 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 04 |
| 1 | Phase 03 incomplete | HALT - complete Phase 03 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Verify and apply cost optimization settings in all generated workflows
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** All workflows verified with cost optimization settings
- **STEP COUNT:** 5 mandatory steps
- **REFERENCE FILES:** cost-optimization-strategies.md

---

## Reference Loading [MANDATORY]

Load ALL reference files fresh. Do NOT rely on memory from previous reads.

```
Read(file_path=".claude/skills/spec-driven-ci/references/cost-optimization-strategies.md")
```

---

## Mandatory Steps (5)

### Step 4.1: Load Cost Optimization Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/cost-optimization-strategies.md")
```

**VERIFY:**
File content is loaded into context. Token pricing, optimization strategies, and cost monitoring patterns are visible.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=04 --step=4.1 --project-root=.
```

---

### Step 4.2: Verify Prompt Caching Enabled

**EXECUTE:**
Check all generated workflow files for prompt caching:

```
Grep(pattern="CLAUDE_CODE_CACHE_ENABLED", path=".github/workflows/dev-story.yml", output_mode="content")
Grep(pattern="CLAUDE_CODE_CACHE_ENABLED", path=".github/workflows/qa-validation.yml", output_mode="content")
Grep(pattern="CLAUDE_CODE_CACHE_ENABLED", path=".github/workflows/parallel-stories.yml", output_mode="content")
```

IF $MERGED_CONFIG.enable_prompt_caching == true:
  Verify each file contains `CLAUDE_CODE_CACHE_ENABLED: true`.

  IF any file is missing the setting:
    Edit the file to add `CLAUDE_CODE_CACHE_ENABLED: true` to the env section.

**VERIFY:**
All workflow files contain `CLAUDE_CODE_CACHE_ENABLED: true` (if caching is enabled in config).

```
Grep(pattern="CLAUDE_CODE_CACHE_ENABLED: true", path=".github/workflows/", output_mode="count")
```

Expected count: 3 (or 4 if installer-testing.yml was generated).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=04 --step=4.2 --project-root=.
```

---

### Step 4.3: Verify Model Preference Applied

**EXECUTE:**
Check all workflow files for model configuration:

```
Grep(pattern="CLAUDE_CODE_MODEL", path=".github/workflows/dev-story.yml", output_mode="content")
Grep(pattern="CLAUDE_CODE_MODEL", path=".github/workflows/parallel-stories.yml", output_mode="content")
```

IF $MERGED_CONFIG.prefer_haiku == true:
  Verify model is set appropriately for cost optimization.

IF any file has incorrect model setting:
  Edit to match the configured preference.

**VERIFY:**
All workflow files that set CLAUDE_CODE_MODEL use the configured model preference.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=04 --step=4.3 --project-root=.
```

---

### Step 4.4: Verify Max-Parallel Configuration

**EXECUTE:**
Check parallel-stories.yml for max-parallel setting:

```
Grep(pattern="max-parallel", path=".github/workflows/parallel-stories.yml", output_mode="content")
```

Verify the value matches $MERGED_CONFIG.max_parallel_jobs.

IF value does not match:
  Edit `parallel-stories.yml` to set `max-parallel: {$MERGED_CONFIG.max_parallel_jobs}`.

**VERIFY:**
```
Grep(pattern="max-parallel: ${MERGED_CONFIG.max_parallel_jobs}", path=".github/workflows/parallel-stories.yml", output_mode="content")
```
Match found.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=04 --step=4.4 --project-root=.
```

---

### Step 4.5: Verify Cost Monitoring Steps

**EXECUTE:**
Check each workflow for cost monitoring or summary output:

```
Grep(pattern="GITHUB_STEP_SUMMARY\\|Cost Summary\\|upload-artifact", path=".github/workflows/dev-story.yml", output_mode="content")
Grep(pattern="GITHUB_STEP_SUMMARY\\|Cost Summary\\|upload-artifact", path=".github/workflows/parallel-stories.yml", output_mode="content")
```

Verify each workflow either:
1. Has a cost summary step writing to `$GITHUB_STEP_SUMMARY`, OR
2. Has artifact upload for results tracking

IF neither present in a workflow:
  Add an artifact upload step to ensure results are captured.

**VERIFY:**
All workflow files have either cost tracking or artifact upload steps present.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=04 --step=4.5 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=ci --phase=04 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 04 complete | Proceed to Phase 05 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 05 |

**Phase 04 Summary:**
- Prompt caching: {enabled/disabled} across {N} workflows
- Model preference: {model} applied
- Max-parallel: {value} configured
- Cost monitoring: Present in all workflows
