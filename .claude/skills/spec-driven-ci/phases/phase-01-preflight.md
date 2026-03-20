# Phase 01: Pre-Flight Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=ci --from=00 --to=01 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 01 |
| 1 | Previous phase incomplete | HALT - complete Phase 00 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Validate all prerequisites for GitHub Actions workflow generation
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** $FORCE_FLAG, $CWD_VALID, $GIT_VALID, $DIRECTORIES_VALID, $CONTEXT_FILES_VALID
- **STEP COUNT:** 7 mandatory steps
- **REFERENCE FILES:** parameter-extraction.md, git-repo-validation.md, context-file-validation.md, security-prerequisites.md

---

## Reference Loading [MANDATORY]

Load ALL reference files fresh. Do NOT rely on memory from previous reads.

```
Read(file_path=".claude/skills/spec-driven-ci/references/parameter-extraction.md")
Read(file_path=".claude/skills/spec-driven-ci/references/git-repo-validation.md")
Read(file_path=".claude/skills/spec-driven-ci/references/context-file-validation.md")
Read(file_path=".claude/skills/spec-driven-ci/references/security-prerequisites.md")
```

---

## Mandatory Steps (7)

### Step 1.1: Load Parameter Extraction Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/parameter-extraction.md")
```

**VERIFY:**
File content is loaded into context. Configuration priority rules are visible.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.1 --project-root=.
```

---

### Step 1.2: Parse Force Flag from Conversation Context

**EXECUTE:**
Scan conversation context for `$FORCE_FLAG` or `--force` argument set by the `/setup-github-actions` command.

```
IF "--force" found in conversation context:
    FORCE_FLAG = true
    Display: "Force mode enabled - will overwrite existing files"
ELSE:
    FORCE_FLAG = false
```

**VERIFY:**
$FORCE_FLAG is a boolean value (true or false). Log the value.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.2 --project-root=.
```

---

### Step 1.3: Validate Working Directory is Project Root

**EXECUTE:**
```
Read(file_path="CLAUDE.md")
```
Confirm the file exists and contains project instructions.

**VERIFY:**
Read succeeds and content contains "DevForgeAI" or project-specific markers. Set $CWD_VALID = true.

IF Read fails: HALT with "Working directory is not the project root. Navigate to the project root before running this skill."

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.3 --project-root=.
```

---

### Step 1.4: Validate Git Repository

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/git-repo-validation.md")
```

Then validate:
```
Glob(pattern=".git/HEAD")
```

**VERIFY:**
`.git/HEAD` file exists. Set $GIT_VALID = true.

IF .git/ not found: HALT with "Not a Git repository. Initialize git before running CI setup."

Additionally, check for clean working tree:
```bash
git status --porcelain
```
If output is non-empty, display warning: "Warning: Uncommitted changes detected. Generated workflows will be uncommitted."

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.4 --project-root=.
```

---

### Step 1.5: Ensure Required Directories Exist

**EXECUTE:**
Check and create directories if missing:

```
Glob(pattern=".github/workflows/")
```

IF `.github/workflows/` does not exist:
```bash
mkdir -p .github/workflows
```

```
Glob(pattern="devforgeai/config/ci/")
```

IF `devforgeai/config/ci/` does not exist:
```bash
mkdir -p devforgeai/config/ci
```

**VERIFY:**
Both directories exist:
```
Glob(pattern=".github/workflows/")
Glob(pattern="devforgeai/config/ci/")
```
Both return results. Set $DIRECTORIES_VALID = true.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.5 --project-root=.
```

---

### Step 1.6: Validate Context Files

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/context-file-validation.md")
```

Then check all 6 context files exist:
```
Glob(pattern="devforgeai/specs/context/tech-stack.md")
Glob(pattern="devforgeai/specs/context/source-tree.md")
Glob(pattern="devforgeai/specs/context/dependencies.md")
Glob(pattern="devforgeai/specs/context/coding-standards.md")
Glob(pattern="devforgeai/specs/context/architecture-constraints.md")
Glob(pattern="devforgeai/specs/context/anti-patterns.md")
```

**VERIFY:**
Count found context files.

IF all 6 found: Set $CONTEXT_FILES_VALID = true
IF fewer than 6 found: Set $CONTEXT_FILES_VALID = "warn". Display warning listing missing files. Workflows may not function correctly without full context.

Do NOT halt on missing context files -- they are a prerequisite for /dev and /qa execution, not for workflow generation.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.6 --project-root=.
```

---

### Step 1.7: Display Security Prerequisites

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ci/references/security-prerequisites.md")
```

Display security reminder to user:
```
IMPORTANT: GitHub Actions workflows require ANTHROPIC_API_KEY to be configured as a GitHub Secret.

Setup: Repository Settings > Secrets and variables > Actions > New repository secret
Name: ANTHROPIC_API_KEY
Value: Your API key from console.anthropic.com

Workflows will fail-fast if this secret is missing.
```

**VERIFY:**
Security information displayed to user. Confirmed via conversation output.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase=01 --step=1.7 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=ci --phase=01 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 01 complete | Proceed to Phase 02 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 02 |

**Phase 01 Summary:**
- $FORCE_FLAG: {value}
- $CWD_VALID: {value}
- $GIT_VALID: {value}
- $DIRECTORIES_VALID: {value}
- $CONTEXT_FILES_VALID: {value}
