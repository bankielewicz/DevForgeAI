# DevForgeAI Skills Reference

Detailed guidance for working with the 7 DevForgeAI skills.

---

## When to Invoke Skills

### devforgeai-ideation

**Use when:**
- User has business idea without technical specs
- Starting greenfield projects ("I want to build...")
- Adding major features to existing systems
- Exploring solution spaces and feasibility
- User requests requirements discovery or epic creation
- **This is the entry point - use BEFORE architecture skill**

**Invocation:**
```
Skill(command="devforgeai-ideation")
```

---

### devforgeai-architecture

**Use when:**
- Context files missing or need updates
- Making technology decisions
- Defining project structure
- Documenting architectural decisions (ADRs)

**Invocation:**
```
Skill(command="devforgeai-architecture")
```

---

### devforgeai-orchestration

**Use when:**
- Starting new epics or sprints
- Creating stories from requirements
- Managing story workflow progression
- Enforcing quality gates
- Tracking deferred work (NEW - RCA-006)
- Analyzing technical debt (NEW - RCA-006)

**Invocation:**
```
# Load story first
@.ai_docs/Stories/STORY-001.story.md

Skill(command="devforgeai-orchestration")
```

**Key Features (RCA-006 Enhanced):**
- Tracks **deferred work** (Phase 4.5) - ensures follow-up stories/ADRs exist
- Invokes **technical-debt-analyzer** during sprint planning (identifies stale debt, circular deferrals)
- Validates **deferral tracking** (story references, ADR references)
- Creates **follow-up stories** for missing references

---

### devforgeai-ui-generator

**Use when:**
- Story requires UI components (forms, dashboards, dialogs)
- Generating visual specifications from requirements
- Creating mockups-as-code for web, desktop, or terminal interfaces
- Need to translate acceptance criteria into UI components
- **Invoked after architecture (requires context files), before or during development**

**Invocation:**
```
# Story mode - load story first
@.ai_docs/Stories/STORY-001.story.md
Skill(command="devforgeai-ui-generator")

# Standalone mode - provide description
**Component description:** Login form with validation
Skill(command="devforgeai-ui-generator")
```

---

### devforgeai-development

**Use when:**
- Implementing user stories or features
- Writing new code with TDD
- Refactoring while maintaining specs
- Resolving QA deferral failures (NEW - RCA-006)

**Prerequisites:**
- ✅ Git repository initialized (recommended, not required)
- ✅ Context files exist (.devforgeai/context/*.md)
- ✅ Story file exists (.ai_docs/Stories/{STORY-ID}.story.md)

**Git Availability:**
- **With Git:** Full workflow (branch management, commits, version control)
- **Without Git:** File-based tracking (changes documented in story artifacts)
- **Auto-detects:** Skill automatically checks Git availability and adapts workflow

**Invocation:**
```
# Load story first
@.ai_docs/Stories/STORY-001.story.md

Skill(command="devforgeai-development")
```

**Key Features (RCA-006 Enhanced):**
- **Git-aware workflow:** Automatically detects Git and uses file-based fallback if unavailable
- Same TDD cycle regardless of version control system
- Clear warnings when Git features disabled
- Requires **AskUserQuestion for ALL deferrals** (4 options: complete now, defer to story, scope change, external blocker)
- Invokes **deferral-validator** subagent (Phase 6.1.5) before git commit - HALTS on CRITICAL/HIGH violations
- Handles **QA deferral failures** (detects previous QA failures, guides resolution workflow)
- Automatically creates **follow-up stories** or **ADRs** when user approves deferrals
- No autonomous deferrals allowed - user approval mandatory

---

### devforgeai-qa

**Auto-invoked during development, or use manually for:**
- Deep validation after story completion
- Pre-release quality gates
- Technical debt assessment
- Deferral validation (NEW - RCA-006)

**Invocation:**
```
# Load story first
@.ai_docs/Stories/STORY-001.story.md

# Deep validation
**Validation mode:** deep
Skill(command="devforgeai-qa")

# Light validation
**Validation mode:** light
Skill(command="devforgeai-qa")
```

**Key Features (RCA-006 Enhanced):**
- Validates **deferred DoD items** via deferral-validator subagent (Phase 0 Step 2.5)
- **FAILS QA** on CRITICAL (circular deferrals) or HIGH (unjustified deferrals) violations
- Tracks **QA iteration history** (attempts, violations, resolutions) in story file
- Enables **feedback loop**: QA FAIL → Dev fix → QA retry

---

### devforgeai-release

**Use when:**
- Story status = "QA Approved" (ready for production)
- Coordinated sprint releases (multiple stories together)
- Hotfix deployments (critical bug fix, still requires QA)
- Rollback operations (production issue detected)
- **This is the final stage - use AFTER QA approval**

**Invocation:**
```
# Load story first
@.ai_docs/Stories/STORY-001.story.md

# Default (staging)
Skill(command="devforgeai-release")

# Explicit staging
**Environment:** staging
Skill(command="devforgeai-release")

# Production deployment
**Environment:** production
Skill(command="devforgeai-release")
```

---

## Workflow Sequences

### For New Projects or Major Features

```
1. devforgeai-ideation
   ↓ (discover requirements, create epics)

2. devforgeai-architecture
   ↓ (create context files, make tech decisions)

3. devforgeai-orchestration
   ↓ (create sprints, generate stories)

4. devforgeai-ui-generator [OPTIONAL]
   ↓ (generate UI specs if story has UI components)

5. devforgeai-development
   ↓ (implement stories with TDD)

6. devforgeai-qa
   ↓ (validate quality, coverage, compliance)

7. devforgeai-release
   (deploy to production)
```

### For Existing Projects with Defined Context

```
1. devforgeai-orchestration
   ↓ (create stories from requirements)

2. devforgeai-ui-generator [OPTIONAL]
   ↓ (generate UI specs if needed)

3. devforgeai-development
   ↓ (implement with TDD)

4. devforgeai-qa
   ↓ (validate)

5. devforgeai-release
   (deploy)
```

### For UI-Focused Stories

```
1. devforgeai-architecture
   ↓ (ensure context files exist)

2. devforgeai-ui-generator
   ↓ (interactive UI spec generation)

3. devforgeai-development
   ↓ (implement UI with tests)

4. devforgeai-qa
   (validate UI implementation)
```

---

---

## CRITICAL: Skills Cannot Accept Parameters

**From official Claude documentation:**
> "Skills CANNOT accept command-line style parameters. All parameters are conveyed through natural language in the conversation."

### How to Pass "Parameters" to Skills

**❌ WRONG:**
```
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")
Skill(command="devforgeai-development --story=STORY-001")
Skill(command="devforgeai-release --env=production")
```

**✅ CORRECT:**
```
# Step 1: Load story content into conversation
@.ai_docs/Stories/STORY-001.story.md

# Step 2: Set context with explicit statements
**Story ID:** STORY-001
**Validation Mode:** deep
**Environment:** staging

# Step 3: Invoke skill WITHOUT arguments
Skill(command="devforgeai-qa")

# Skill will extract story ID from YAML frontmatter in loaded story file
# Skill will extract mode from "Validation Mode: deep" statement
# Skill will extract environment from "Environment: staging" statement
```

### Why This Works

1. **@file loads content** - Story YAML frontmatter becomes part of conversation
2. **Explicit statements provide context** - Skills search conversation for patterns like "Mode: deep"
3. **Skills read conversation** - Extract needed information using pattern matching
4. **No parameter passing** - Skills operate on available conversation context only

---

## Skill Integration

Skills automatically invoke each other when needed:
- **devforgeai-development** auto-invokes **devforgeai-qa** (light mode) after each TDD phase
- **devforgeai-ideation** auto-transitions to **devforgeai-architecture**
- **devforgeai-orchestration** invokes other skills based on workflow state

---

## Skill-Specific Documentation

For detailed skill documentation, see:
- `.claude/skills/devforgeai-ideation/SKILL.md`
- `.claude/skills/devforgeai-architecture/SKILL.md`
- `.claude/skills/devforgeai-orchestration/SKILL.md`
- `.claude/skills/devforgeai-ui-generator/SKILL.md`
- `.claude/skills/devforgeai-development/SKILL.md`
- `.claude/skills/devforgeai-qa/SKILL.md`
- `.claude/skills/devforgeai-release/SKILL.md`

**Reference Files:** Each skill has a `references/` directory with detailed guides loaded progressively as needed.
