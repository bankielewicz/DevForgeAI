# DevForgeAI Slash Commands Reference

Complete guide to the 9 user-facing slash commands for DevForgeAI workflows.

---

## Command Overview

DevForgeAI provides 9 slash commands organized into 4 categories:

**Planning & Setup (4 commands):**
- `/ideate` - Transform business idea to structured requirements
- `/create-context` - Generate 6 architectural context files
- `/create-epic` - Generate epic from requirements
- `/create-sprint` - Plan 2-week sprint with story selection

**Story Development (3 commands):**
- `/create-story` - Generate story with acceptance criteria
- `/create-ui` - Generate UI component specs (web/GUI/terminal)
- `/dev` - Execute TDD development cycle (Red→Green→Refactor)

**Validation & Release (2 commands):**
- `/qa` - Run quality validation (light/deep modes)
- `/release` - Deploy to staging and production

**Orchestration (1 command):**
- `/orchestrate` - Full lifecycle: Dev → QA → Release

---

## Command Details

### /ideate [business-idea]

**Purpose:** Transform business idea into structured requirements

**Invokes:** `devforgeai-ideation` skill

**Workflow:**
1. Business idea capture from arguments
2. Requirements discovery (6-phase process)
3. Complexity assessment (0-60 scoring)
4. Epic generation
5. Auto-transition to architecture skill

**Example:**
```
> /ideate Build a task management system with AI prioritization
```

**Output:**
- Epic document in `.ai_docs/Epics/`
- Requirements spec in `.devforgeai/specs/requirements/`
- Complexity assessment report

---

### /create-context [project-name]

**Purpose:** Generate 6 architectural context files

**Invokes:** `devforgeai-architecture` skill

**Workflow:**
1. Interactive technology selection (via AskUserQuestion)
2. Generate all 6 context files
3. Create initial ADR
4. Validate context completeness

**Example:**
```
> /create-context my-saas-platform
```

**Output:**
- `tech-stack.md` - Technology choices
- `source-tree.md` - Project structure
- `dependencies.md` - Approved packages
- `coding-standards.md` - Code patterns
- `architecture-constraints.md` - Layer boundaries
- `anti-patterns.md` - Forbidden patterns

---

### /create-epic [epic-name]

**Purpose:** Create epic with feature breakdown

**Uses:** `requirements-analyst` subagent

**Workflow:**
1. Capture epic details
2. Feature decomposition
3. Complexity estimation
4. Epic file generation

**Example:**
```
> /create-epic User Authentication System
```

**Output:**
- Epic file in `.ai_docs/Epics/{EPIC-ID}.epic.md`
- Feature list with descriptions

---

### /create-sprint [sprint-number]

**Purpose:** Plan 2-week sprint with story selection

**Uses:** `requirements-analyst` subagent

**Workflow:**
1. Determine sprint ID
2. Story selection (via AskUserQuestion)
3. Capacity calculation
4. Sprint file generation
5. Update selected story statuses

**Example:**
```
> /create-sprint 1
```

**Output:**
- Sprint file in `.ai_docs/Sprints/Sprint-{N}.md`
- Stories linked to sprint

---

### /create-story [story-description]

**Purpose:** Generate user story with acceptance criteria

**Uses:** `requirements-analyst` subagent

**Workflow:**
1. Story details from arguments
2. Acceptance criteria generation (Given/When/Then)
3. Technical specification
4. Non-functional requirements
5. Story file creation

**Example:**
```
> /create-story User login with email and password
```

**Output:**
- Story file in `.ai_docs/Stories/{STORY-ID}.story.md`
- YAML frontmatter with metadata
- Testable acceptance criteria

---

### /create-ui [STORY-ID]

**Purpose:** Generate UI component specs (web/GUI/terminal)

**Invokes:** `devforgeai-ui-generator` skill

**Workflow:**
1. Context validation (requires 6 context files)
2. Story analysis (extract UI requirements)
3. Interactive technology selection (React, Blazor, WPF, Tkinter, etc.)
4. Styling preferences (Tailwind, Bootstrap, etc.)
5. Code generation
6. Story update with UI reference

**Example:**
```
> /create-ui STORY-042
```

**Output:**
- UI component code in `.devforgeai/specs/ui/`
- UI-SPEC-SUMMARY.md
- Story updated with UI references

---

### /dev [STORY-ID]

**Purpose:** Execute TDD development cycle (Red→Green→Refactor)

**Invokes:** `devforgeai-development` skill

**Workflow:**
1. **Phase 0a-c:** Argument validation, technology detection, QA failure detection
2. **Phase 1:** Story validation and status gate
3. **Phase 2:** Invoke devforgeai-development skill (complete TDD cycle)
4. **Phase 2.5:** Three-layer DoD validation (NEW - RCA-006 Recs 1-3)
   - **Layer 1:** Python format validator (<100ms, ~200 tokens)
   - **Layer 2:** Interactive checkpoint (user approval MANDATORY)
   - **Layer 3:** AI subagent validation (feasibility, circular detection)
5. **Phase 3:** Verify completion (tests pass, story updated)
6. **Phase 4:** Report results

**Example:**
```
> /dev STORY-042
```

**Output:**
- Implementation code in source tree
- Test files with 100% pass rate
- Git commits
- Story status updated to "Dev Complete"

**RCA-006 Implementation (Recommendations 1-3 Complete):**

**Three-Layer DoD Validation:**
- **Layer 1 (Python):** Fast format check validates basic justification patterns
  - Script: `.claude/scripts/validate_deferrals.py`
  - Speed: <100ms
  - Token cost: ~200
  - Blocking: No (warnings only)
  - Coverage: 80% of format errors

- **Layer 2 (Interactive):** User approval checkpoint prevents autonomous deferrals
  - Task file: `.claude/tasks/dod-validation-checkpoint.md`
  - Requires: AskUserQuestion for ALL incomplete items
  - Options: Complete now, Defer to story, Scope change (ADR), External blocker
  - Token cost: ~7,000
  - Blocking: Yes (MANDATORY)
  - Creates: Follow-up stories, ADRs via subagents

- **Layer 3 (AI):** Comprehensive validation via deferral-validator subagent
  - Subagent: `.claude/agents/deferral-validator.md`
  - Validates: Feasibility, circular deferrals, reference existence
  - Token cost: ~500 to main (~5,000 in isolated context)
  - Blocking: Yes (on CRITICAL/HIGH violations)
  - Coverage: 95% (comprehensive analysis)

**Combined:** 99% violation detection, ZERO autonomous deferrals possible

---

### /qa [STORY-ID] [mode]

**Purpose:** Run quality validation (light or deep mode)

**Syntax:** `/qa [STORY-ID] [mode]`
- Mode: `deep` or `light` (no -- prefix)
- Default: `deep` if not specified

**Invokes:** `devforgeai-qa` skill

**Modes:**
- **Light (~10K tokens)**: Build/syntax checks, test execution, quick anti-pattern scan
- **Deep (~65K tokens)**: Coverage analysis, comprehensive anti-patterns, spec compliance, quality metrics

**Workflow:**
1. Story validation
2. Mode selection (default: deep)
3. Quality analysis (includes **deferral validation** - NEW)
4. **Phase 2: Handle QA Results** (NEW - RCA-006)
5. Report generation
6. Story status update ("QA Approved" or "QA Failed")

**Example:**
```
> /qa STORY-042           # Defaults to deep mode
> /qa STORY-042 deep      # Explicit deep mode
> /qa STORY-042 light     # Explicit light mode
```

**Output:**
- QA report in `.devforgeai/qa/reports/{STORY-ID}-qa-report.md`
- Coverage report
- Story status updated
- **QA Validation History** section added to story (NEW - tracks attempts)

**RCA-006 Enhanced Features:**
- Invokes **deferral-validator** subagent (validates all deferred DoD items)
- **FAILS QA** on CRITICAL (circular deferrals) or HIGH (unjustified deferrals) violations
- **Phase 2: Handles QA failures** - guides user to resolution (return to dev, fix manually, or review report)
- Tracks **QA iteration history** in story file (attempt number, violations, resolutions)

---

### /release [STORY-ID] [environment]

**Purpose:** Deploy to staging and/or production

**Syntax:** `/release [STORY-ID] [environment]`
- Environment: `staging` or `production` (no -- prefix)
- Default: `staging` if not specified

**Invokes:** `devforgeai-release` skill

**Workflow:**
1. Pre-release validation (QA approved)
2. Staging deployment + smoke tests
3. Production deployment (if staging succeeds)
4. Post-deployment validation
5. Release documentation
6. Story status update to "Released"

**Example:**
```
> /release STORY-042              # Defaults to staging
> /release STORY-042 staging      # Explicit staging
> /release STORY-042 production   # Production deployment
```

**Output:**
- Code deployed to environments
- Smoke tests executed
- Release notes generated
- Story status = "Released"

---

### /orchestrate [STORY-ID]

**Purpose:** Execute complete story lifecycle end-to-end

**Invokes:** Multiple skills sequentially

**Workflow:**
1. Story validation & checkpoint detection
2. Development phase (invokes devforgeai-development)
3. QA validation (invokes devforgeai-qa)
4. **Phase 3.5: QA Failure Handling** (NEW - RCA-006) - Retry loop with max 3 attempts
5. Staging release (invokes devforgeai-release --env=staging)
6. Production release (invokes devforgeai-release --env=production)
7. Workflow history finalization

**Checkpoint Recovery:**
- Resumes from last successful phase if failures occur
- Checkpoints: DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE

**Example:**
```
> /orchestrate STORY-042
```

**Output:**
- Complete story lifecycle executed
- All quality gates passed
- Story deployed to production
- Workflow history documented

**RCA-006 Enhanced Features:**
- **QA Failure Retry Loop** (Phase 3.5) - Automatic Dev → QA FAIL → Dev fix → QA retry (max 3 attempts)
- **Deferral failure handling** - Creates follow-up stories or guides user to resolution
- **Loop prevention** - HALTS after 3 QA failures (suggests story split)
- **Tracks retry history** in story workflow history section

---

---

## Slash Command Syntax & Limitations

### What Works

**Positional arguments:**
```
/qa STORY-001 deep           ✅ Correct
/release STORY-001 production ✅ Correct
```

**Multiple arguments:**
```
$1 = First argument (e.g., STORY-001)
$2 = Second argument (e.g., deep, production)
$3 = Third argument (if needed)
```

**@file references with $1:**
```
@.ai_docs/Stories/$1.story.md  ✅ Correct
```

### What Doesn't Work

**Flag syntax:**
```
/qa --mode=deep STORY-001      ❌ Wrong (will ask for clarification)
/qa STORY-001 --mode=deep      ⚠️ Works but educates user
/release STORY-001 --env=prod  ⚠️ Works but educates user
```

**@file with $ARGUMENTS:**
```
@.ai_docs/Stories/$ARGUMENTS.story.md  ❌ Wrong (includes all args/flags in filename)
```

**Skill invocations with arguments:**
```
Skill(command="devforgeai-qa --mode=deep")  ❌ Wrong (Skills don't accept parameters)
```

### Correct Parameter Passing to Skills

**Skills cannot accept command-line parameters.** Use conversation context instead:

```
# Step 1: Load context (via @file or explicit text)
@.ai_docs/Stories/STORY-001.story.md

# Step 2: State parameters explicitly
**Validation Mode:** deep
**Environment:** staging

# Step 3: Invoke skill WITHOUT arguments
Skill(command="devforgeai-qa")

# Skill extracts parameters from conversation context
```

---

## Command Discovery

All commands appear in `/help` after terminal restart.

**To see available commands:**
```
> /help
```

---

## Command Files Location

All command files are in `.claude/commands/`:
- `ideate.md` (397 lines)
- `create-context.md` (496 lines)
- `create-epic.md` (250 lines)
- `create-sprint.md` (293 lines)
- `create-story.md` (452 lines)
- `create-ui.md` (622 lines)
- `dev.md` (350 lines)
- `qa.md` (372 lines)
- `release.md` (~400 lines)
- `orchestrate.md` (401 lines)

---

## Integration Patterns

Commands integrate with skills using the Skill tool:
```
Skill(command="devforgeai-development --story=STORY-001")
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")
Skill(command="devforgeai-release --story=STORY-001")
```

This creates **context isolation** - each skill operates in a separate context window, keeping main conversation efficient.
