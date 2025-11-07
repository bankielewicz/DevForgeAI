# DevForgeAI Skills Reference

Detailed guidance for working with the 8 DevForgeAI skills + 1 infrastructure skill.

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
- Brownfield projects need architectural documentation
- **Use after ideation, before orchestration/development**

**Invocation:**
```
Skill(command="devforgeai-architecture")
```

**Workflow (5 Phases - Progressive Disclosure):**
1. Project Context Discovery (greenfield vs brownfield, technology inventory)
2. Create Immutable Context Files (6 files: tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
3. Create Architecture Decision Records (document all major decisions with ADRs)
4. Create Technical Specifications (optional: use cases, API specs, database schemas, NFRs)
5. Validate Spec Against Context (ensure no conflicts)

**Reference Files (REFACTORED 2025-01-06 - Progressive Loading):**

**Workflow Files (6 files, 2,964 lines):**
- context-discovery-workflow.md (169 lines) - Phase 1
- context-file-creation-workflow.md (1,050 lines) - Phase 2 (MASSIVE consolidation of all 6 context file workflows)
- adr-creation-workflow.md (386 lines) - Phase 3
- technical-specification-workflow.md (392 lines) - Phase 4
- architecture-validation.md (200 lines) - Phase 5
- brownfield-integration.md (767 lines) - Existing project adoption

**Guide Files (4 files, 2,153 lines):**
- adr-policy.md (324 lines) - When to create ADRs
- adr-template.md (217 lines) - ADR structure
- ambiguity-detection-guide.md (540 lines) - When to use AskUserQuestion
- system-design-patterns.md (1,072 lines) - Architecture patterns

**Asset Files (12 files, 9,079 lines):**
- 6 context templates (3,922 lines)
- 6 ADR examples (5,157 lines)

**Entry Point:** SKILL.md - 212 lines (78% reduction from 978)
**Token Efficiency:** 4.6x improvement (7,824→1,696 tokens on activation)

**Key Features:**
- **Progressive disclosure** - Each phase loads its workflow file on-demand
- **Template-based** - Uses comprehensive asset templates (no inline workflows)
- **Ambiguity resolution** - MUST use AskUserQuestion for all technology/pattern decisions
- **Brownfield support** - Discovery → gap analysis → migration strategy
- **Immutable constraints** - 6 context files serve as "the law" for all AI agents

---

### devforgeai-orchestration

**Use when:**
- Starting new epics or sprints
- Creating stories from requirements
- Managing story workflow progression
- Enforcing quality gates
- Tracking deferred work (NEW - RCA-006)
- Analyzing technical debt (NEW - RCA-006)
- **Creating epics with feature decomposition** (NEW - 2025-11-06)

**Invocation (Story Management Mode):**
```
# Load story first
@.ai_docs/Stories/STORY-001.story.md

Skill(command="devforgeai-orchestration")
```

**Invocation (Epic Creation Mode):**
```
# Set context markers
**Epic name:** User Authentication System
**Command:** create-epic

Skill(command="devforgeai-orchestration")
```

**Invocation (Sprint Planning Mode):**
```
# Set context markers
**Sprint Name:** Sprint-1
**Command:** create-sprint
**Selected Stories:** STORY-001, STORY-002, STORY-003

Skill(command="devforgeai-orchestration")
```

**Key Features:**
- Tracks **deferred work** (Phase 4.5) - ensures follow-up stories/ADRs exist
- Invokes **technical-debt-analyzer** during sprint planning (identifies stale debt, circular deferrals)
- Validates **deferral tracking** (story references, ADR references)
- Creates **follow-up stories** for missing references
- **Epic creation workflow** (Phase 4A - NEW 2025-11-06) - 8-phase comprehensive epic creation
- **Sprint planning workflow** (Phase 3 - 2025-11-05) - Sprint creation with capacity validation
- **Sprint retrospective** (Phase 7 - RCA-006 Phase 2 NEW 2025-11-06) - Auto-audit technical debt, create debt reduction sprints

**Epic Creation Workflow (8 Phases - NEW):**
1. Epic Discovery - Generate EPIC-ID, check duplicates
2. Context Gathering - Goal, timeline, priority, stakeholders, success criteria (4 AskUserQuestion flows)
3. Feature Decomposition - requirements-analyst subagent, 3-8 features, user review loop
4. Technical Assessment - architect-reviewer subagent, complexity 0-10, risk identification, context file validation
5. Epic File Creation - Populate epic-template.md, write to .ai_docs/Epics/{EPIC-ID}.epic.md
6. Requirements Spec - Optional requirements-analyst subagent, write to .devforgeai/specs/requirements/
7. Validation & Self-Healing - 9 validation checks, auto-correct correctable issues, HALT on critical failures
8. Completion Summary - Return structured JSON to command

**Reference Files (Progressive Loading - REFACTORED 2025-01-06):**

**Core Workflow (9 files):**
- mode-detection.md (329 lines) - 4 modes detection logic
- checkpoint-detection.md (474 lines) - Resume functionality
- story-validation.md (345 lines) - Pre-execution validation
- skill-invocation.md (509 lines) - 4 skill coordination
- story-status-update.md (278 lines) - Status transitions
- qa-retry-workflow.md (919 lines) - Max 3 attempts with recovery
- deferred-tracking.md (714 lines) - Technical debt tracking
- next-action-determination.md (287 lines) - Workflow guidance
- orchestration-finalization.md (513 lines) - Completion summary

**Epic Management (4 files):**
- epic-management.md (496 lines - Phases 1-2)
- feature-decomposition-patterns.md (903 lines - Phase 3)
- technical-assessment-guide.md (914 lines - Phase 4)
- epic-validation-checklist.md (760 lines - Phase 7)

**Sprint Management (1 file):**
- sprint-planning-guide.md (631 lines)

**State Management (2 files):**
- workflow-states.md (585 lines)
- state-transitions.md (1,105 lines)

**Supporting (4 files):**
- quality-gates.md (1,017 lines)
- story-management.md (633 lines)
- user-interaction-patterns.md (513 lines) - 12 AskUserQuestion patterns
- troubleshooting.md (935 lines) - 13 common issues + solutions

**Total Reference Content:** 20 files, 12,860 lines (loaded progressively on-demand)

**Entry Point:** SKILL.md - 230 lines (93% reduction from 3,249)
**Token Efficiency:** 14.1x improvement (25,992→1,840 tokens on activation)

**Subagents Used:**
- requirements-analyst (Epic Phase 3 feature decomposition, Phase 6 optional requirements spec)
- architect-reviewer (Epic Phase 4 technical assessment)
- sprint-planner (Sprint Phase 3 complete workflow)
- technical-debt-analyzer (Phase 4.5 debt trend analysis)

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

**Key Features (Enhanced 2025-11-06 - RCA-006):**
- **Lean command architecture:** /dev command delegates to skill (513 lines, down from 860)
- **Subagent-powered validation:**
  - **git-validator** subagent (Phase 0 Step 1) - Git status and workflow strategy
  - **tech-stack-detector** subagent (Phase 0 Step 7) - Technology detection and validation
- **Git-aware workflow:** Automatically detects Git and uses file-based fallback if unavailable
- **Phase 4.5: Deferral Challenge Checkpoint** (RCA-006 - NEW):
  - Challenges ALL deferrals (pre-existing from template + new from TDD)
  - Invokes deferral-validator subagent for blocker validation
  - Requires user approval for EVERY deferred item (zero autonomous deferrals)
  - Timestamps all approvals for audit trail
  - Enforces "Attempt First, Defer Only If Blocked" pattern
- **Phase 5: New Incomplete Items:**
  - Layer 1: Python format validator (~200 tokens, <100ms)
  - Layer 2: Interactive checkpoint (AskUserQuestion for new items only)
  - Layer 3: Git commit or file-based tracking
- **QA failure recovery:** Detects previous QA failures, guides resolution workflow (Phase 0 Step 8)
- **Framework-aware subagents:** All subagents understand DevForgeAI constraints (prevent silos)
- **Zero autonomous deferrals:** User approval mandatory for all deferred/incomplete DoD items

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

---

### claude-code-terminal-expert

**Use when:**
- User asks about Claude Code Terminal features ("Can Claude Code...?" / "Does Claude Code have...?")
- Creating subagents, skills, slash commands, plugins, or hooks
- Configuring settings, models, permissions, or MCP servers
- Setting up CI/CD integration (GitHub Actions, GitLab)
- Troubleshooting Claude Code issues (installation, auth, performance)
- Any questions about Claude Code Terminal capabilities
- **This is infrastructure support - provides terminal expertise**

**Invocation:**
```
# Skill automatically triggers on Claude Code Terminal questions
# No special invocation needed - model-invoked based on question context
```

**Key Features:**
- **Comprehensive knowledge:** 28 topics covering all Claude Code Terminal features
- **Self-updating:** Can fetch latest docs from code.claude.com when needed
- **Progressive disclosure:** 6 reference files + 2 assets loaded as needed
- **100% official:** All content from official Anthropic documentation
- **Token efficient:** 95% savings vs loading all docs (2,100-6,000 tokens typical)

**Reference Files (Progressive Loading):**
- core-features.md (2,428 lines - Subagents, Skills, Commands, Plugins, MCP)
- configuration-guide.md (1,513 lines - Settings, Models, CLI, Permissions)
- integration-patterns.md (2,790 lines - CI/CD, Hooks, Headless, Containers)
- troubleshooting-guide.md (2,128 lines - Installation, Auth, Performance, Errors)
- advanced-features.md (3,553 lines - Sandboxing, Network, Monitoring, Security)
- best-practices.md (1,230 lines - Workflows, Efficiency, Prompts, Token Optimization)

**Asset Files:**
- quick-reference.md (726 lines - Command cheat sheet, keyboard shortcuts)
- comparison-matrix.md (600 lines - Feature comparison, decision matrices)

**Documentation URLs (Self-Updating):**
All 29 official code.claude.com URLs embedded for auto-updates

**Skill Type:** Knowledge/expertise skill (not workflow execution)

**Integration:** Complements DevForgeAI by providing Claude Code Terminal knowledge, reducing "Claude doesn't know this feature" friction

---
