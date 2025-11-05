# DevForgeAI Skills Reference

Detailed guidance for working with the 8 DevForgeAI skills.

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

### devforgeai-story-creation

**Use when:**
- User runs `/create-story [feature-description]` command
- Orchestration skill creates stories from epic features
- Development skill creates tracking stories for deferred DoD items
- Sprint planning requires story generation
- Transforming feature descriptions into structured stories
- **Use after ideation/architecture, before development**

**Invocation:**
```
# Feature description in conversation context
**Feature Description:** {description}

Skill(command="devforgeai-story-creation")
```

**Workflow (8 Phases):**
1. **Story Discovery** - Generate story ID, discover epic/sprint context, collect metadata
2. **Requirements Analysis** - Invoke requirements-analyst subagent, generate user story + AC
3. **Technical Specification** - Invoke api-designer subagent (if API), define data models, business rules
4. **UI Specification** - Document components, mockups, interfaces, accessibility (if UI detected)
5. **Story File Creation** - Build YAML frontmatter + all markdown sections, write to disk
6. **Epic/Sprint Linking** - Update parent documents with story references
7. **Self-Validation** - Validate quality, self-heal issues, ensure completeness
8. **Completion Report** - Present summary, guide user to next actions

**Output:**
- Complete story document in `.ai_docs/Stories/{STORY-ID}-{slug}.story.md`
- All sections: User story, AC (3+ Given/When/Then), tech spec, UI spec (if applicable), NFRs, edge cases, DoD
- Epic/sprint files updated (if associated)
- Self-validated for quality

**Subagents Used:**
- requirements-analyst (Phase 2) - User story and acceptance criteria
- api-designer (Phase 3, conditional) - API contracts if endpoints detected

**Reference Files (6 files, 7,477 lines):**
- story-structure-guide.md - YAML frontmatter, sections, formatting
- acceptance-criteria-patterns.md - Given/When/Then patterns by story type
- technical-specification-guide.md - API contracts, data models, business rules
- ui-specification-guide.md - ASCII mockups, components, accessibility (WCAG AA)
- validation-checklists.md - Quality validation, self-healing
- story-examples.md - 4 complete examples (CRUD, auth, workflow, reporting)

**Key Features:**
- **Self-validation** (Phase 7) - Ensures quality before completion
- **Progressive disclosure** - 6 reference files loaded only when needed
- **Framework-aware** - Respects context files, integrates with other skills
- **Reusable** - Invoked by command, orchestration, development, sprint planning
- **Complete specifications** - API contracts, data models, UI mockups, accessibility

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

**Key Features (Enhanced 2025-11-05):**
- **Lean skill architecture:** SKILL.md delegates to reference files (1,740 lines, down from 2,130)
- **Progressive disclosure:** DoD validation reference loaded on-demand only (token efficiency)
- **Subagent-powered validation:**
  - **git-validator** subagent (Phase 0 Step 1) - Git status and workflow strategy
  - **tech-stack-detector** subagent (Phase 0 Step 7) - Technology detection and validation
- **Git-aware workflow:** Automatically detects Git and uses file-based fallback if unavailable
- **Three-layer DoD validation** (Phase 5):
  - Layer 1: Python format validator (~200 tokens, <100ms)
  - Layer 2: DoD checkpoint via `references/dod-validation-checkpoint.md` (progressive loading)
  - Layer 3: deferral-validator subagent (comprehensive analysis)
- **QA failure recovery:** Detects previous QA failures, guides resolution workflow (Phase 0 Step 8)
- **Framework-aware subagents:** All subagents understand DevForgeAI constraints (prevent silos)
- **Zero autonomous deferrals:** User approval mandatory for all incomplete DoD items

**Reference Files (6 files):**
- `references/dod-validation-checkpoint.md` (487 lines) - Layer 2 DoD validation procedure
- `references/tdd-patterns.md` (1,013 lines) - TDD workflow patterns
- `references/refactoring-patterns.md` (797 lines) - Code improvement techniques
- `references/git-workflow-conventions.md` (885 lines) - Version control best practices
- `references/story-documentation-pattern.md` (792 lines) - Implementation notes templates
- `references/slash-command-argument-validation-pattern.md` (812 lines) - Argument handling

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
1. devforgeai-orchestration OR devforgeai-story-creation
   ↓ (orchestration: create stories from epics)
   ↓ (story-creation: create individual story from feature description)

2. devforgeai-ui-generator [OPTIONAL]
   ↓ (generate UI specs if needed)

3. devforgeai-development
   ↓ (implement with TDD)

4. devforgeai-qa
   ↓ (validate)

5. devforgeai-release
   (deploy)
```

### For Individual Story Creation

```
1. devforgeai-story-creation
   ↓ (transform feature description → complete story)

2. devforgeai-ui-generator [OPTIONAL]
   ↓ (add UI specifications if needed)

3. devforgeai-development
   ↓ (implement story with TDD)

4. devforgeai-qa
   ↓ (validate implementation)

5. devforgeai-release
   (deploy to production)
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
