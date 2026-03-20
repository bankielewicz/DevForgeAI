# Phase 05: Validation & Summary

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=ci --from=04 --to=05 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 05 |
| 1 | Phase 04 incomplete | HALT - complete Phase 04 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Final validation of all generated files and display comprehensive setup summary
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** Validation report, setup summary displayed to user
- **STEP COUNT:** 5 mandatory steps
- **REFERENCE FILES:** yaml-validation-procedures.md, security-prerequisites.md

---

## Reference Loading [MANDATORY]

Load ALL reference files fresh. Do NOT rely on memory from previous reads.

```
Read(file_path=".claude/skills/spec-driven-ci/references/yaml-validation-procedures.md")
Read(file_path=".claude/skills/spec-driven-ci/references/security-prerequisites.md")
```

---

## Mandatory Steps (5)

### Step 5.1: Load Validation Procedures Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/yaml-validation-procedures.md")
```

**VERIFY:**
File content is loaded into context. YAML validation rules and checklist are visible.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=05 --step=5.1 --project-root=.
```

---

### Step 5.2: Validate All 4 Workflow Files

**EXECUTE:**

Verify each workflow file exists and has correct YAML structure:

```
Read(file_path=".github/workflows/dev-story.yml")
```
Check: `name:`, `on:`, `jobs:`, `steps:` keys present.

```
Read(file_path=".github/workflows/qa-validation.yml")
```
Check: `name:`, `on:`, `jobs:`, `steps:` keys present.

```
Read(file_path=".github/workflows/parallel-stories.yml")
```
Check: `name:`, `on:`, `jobs:`, `steps:`, `strategy:` keys present.

IF installer-testing.yml was generated (not skipped):
```
Read(file_path=".github/workflows/installer-testing.yml")
```
Check: `name:`, `on:`, `jobs:`, `steps:` keys present.

**Validation Checklist:**
| File | Exists | Has name: | Has on: | Has jobs: | Has steps: |
|------|--------|-----------|---------|-----------|------------|
| dev-story.yml | | | | | |
| qa-validation.yml | | | | | |
| parallel-stories.yml | | | | | |
| installer-testing.yml | | | | | |

**VERIFY:**
All generated files pass validation. Log results in the checklist table above.

IF any file fails: HALT with specific error. Do NOT proceed with invalid workflows.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=05 --step=5.2 --project-root=.
```

---

### Step 5.3: Validate Configuration Files

**EXECUTE:**

Verify both configuration files exist and have correct structure:

```
Read(file_path="devforgeai/config/ci/github-actions.yaml")
```
Check: `cost_optimization:` section present with `enable_prompt_caching`, `prefer_haiku`, `max_turns` keys.

```
Read(file_path="devforgeai/config/ci/ci-answers.yaml")
```
Check: File is non-empty and contains answer entries.

**VERIFY:**
Both config files exist and pass structural validation.

| File | Exists | Valid Structure |
|------|--------|-----------------|
| github-actions.yaml | | |
| ci-answers.yaml | | |

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=05 --step=5.3 --project-root=.
```

---

### Step 5.4: Display Security Setup Reminder

**EXECUTE:**

Load the security prerequisites reference fresh:
```
Read(file_path=".claude/skills/spec-driven-ci/references/security-prerequisites.md")
```

Display the next-steps setup guide:

```
NEXT STEPS - Required Before First Workflow Run:

1. Add ANTHROPIC_API_KEY to GitHub Secrets
   Repository Settings > Secrets and variables > Actions > New repository secret
   Name: ANTHROPIC_API_KEY
   Value: Your API key from console.anthropic.com

2. Review ci-answers.yaml for headless prompts
   File: devforgeai/config/ci/ci-answers.yaml
   Pre-configured responses for AskUserQuestion in headless mode

3. Trigger your first workflow
   Actions tab > DevForgeAI Story Development > Run workflow
   Enter a Story ID (e.g., STORY-001)
```

**VERIFY:**
Security and next-steps information displayed to user.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=05 --step=5.4 --project-root=.
```

---

### Step 5.5: Display Completion Summary

**EXECUTE:**

Display the final completion banner:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CI/CD Setup Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Workflow files created:
  - .github/workflows/dev-story.yml
  - .github/workflows/qa-validation.yml
  - .github/workflows/parallel-stories.yml
  - .github/workflows/installer-testing.yml [if generated]

Configuration files created:
  - devforgeai/config/ci/github-actions.yaml
  - devforgeai/config/ci/ci-answers.yaml

Cost optimization:
  - Prompt caching: {enabled/disabled}
  - Model: {model preference}
  - Max parallel: {value}
  - Max cost/story: $0.15

Session: ${SESSION_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**VERIFY:**
Completion banner displayed to user with all file paths and configuration summary.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=05 --step=5.5 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=ci --phase=05 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 05 complete | Workflow generation finished |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Workflow generation finished |

**Phase 05 Summary:**
- Workflow files validated: {count}/4
- Config files validated: 2/2
- Security setup documented: Yes
- Summary displayed: Yes
- All 5 phases completed successfully
