# Source Tree Structure - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## CRITICAL RULE: Framework Organization

This file defines WHERE framework components belong in the DevForgeAI repository. Projects using DevForgeAI will have their own source-tree.md files created by the devforgeai-architecture skill.

---

## Framework Directory Structure

```
DevForgeAI2/
├── .claude/                     # Claude Code Terminal configuration
│   ├── skills/                  # Framework implementation (6 core skills)
│   │   ├── devforgeai-ideation/
│   │   │   ├── SKILL.md         # Main skill (500-800 lines)
│   │   │   └── references/      # Deep documentation (loaded on demand)
│   │   │       ├── requirements-elicitation-guide.md
│   │   │       ├── complexity-assessment-matrix.md
│   │   │       ├── domain-specific-patterns.md
│   │   │       └── feasibility-analysis-framework.md
│   │   ├── devforgeai-architecture/
│   │   │   ├── SKILL.md
│   │   │   ├── references/
│   │   │   │   ├── adr-template.md
│   │   │   │   ├── tech-stack-template.md
│   │   │   │   ├── source-tree-template.md
│   │   │   │   ├── system-design-patterns.md
│   │   │   │   └── ambiguity-detection-guide.md
│   │   │   └── assets/
│   │   │       └── context-templates/  # Templates for project context files
│   │   │           ├── tech-stack.md
│   │   │           ├── source-tree.md
│   │   │           ├── dependencies.md
│   │   │           ├── coding-standards.md
│   │   │           ├── architecture-constraints.md
│   │   │           └── anti-patterns.md
│   │   ├── devforgeai-orchestration/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── story-template.md
│   │   │       ├── sprint-template.md
│   │   │       └── workflow-state-machine.md
│   │   ├── devforgeai-development/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── tdd-workflow-guide.md
│   │   │       ├── refactoring-patterns.md
│   │   │       └── git-workflow-conventions.md
│   │   ├── devforgeai-qa/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── coverage-thresholds.md
│   │   │       ├── anti-patterns-catalog.md
│   │   │       └── quality-metrics-guide.md
│   │   └── devforgeai-release/
│   │       ├── SKILL.md
│   │       └── references/
│   │           ├── deployment-strategies.md
│   │           ├── smoke-testing-guide.md
│   │           ├── rollback-procedures.md
│   │           ├── monitoring-metrics.md
│   │           └── release-checklist.md
│   │
│   ├── agents/                  # Specialized subagents (8+ agents)
│   │   ├── requirements-analyst.md
│   │   ├── architect-reviewer.md
│   │   ├── backend-architect.md
│   │   ├── frontend-developer.md
│   │   ├── test-automator.md
│   │   ├── code-reviewer.md
│   │   ├── deployment-engineer.md
│   │   └── security-auditor.md
│   │
│   └── commands/                # User-facing workflows (8+ commands)
│       ├── ideate.md            # /ideate [business-idea]
│       ├── create-context.md    # /create-context [project-name]
│       ├── create-epic.md       # /create-epic [epic-name]
│       ├── create-sprint.md     # /create-sprint [sprint-number]
│       ├── create-story.md      # /create-story [story-name]
│       ├── dev.md               # /dev [STORY-ID]
│       ├── qa.md                # /qa [STORY-ID]
│       ├── release.md           # /release [STORY-ID]
│       └── orchestrate.md       # /orchestrate [STORY-ID]
│
├── .devforgeai/                 # Framework's own context (meta-level)
│   ├── context/                 # Framework architectural constraints
│   │   ├── tech-stack.md        # Framework implementation constraints
│   │   ├── source-tree.md       # This file
│   │   ├── dependencies.md      # Framework dependencies
│   │   ├── coding-standards.md  # Framework coding patterns
│   │   ├── architecture-constraints.md  # Framework design rules
│   │   └── anti-patterns.md     # Framework anti-patterns
│   │
│   ├── qa/                      # QA validation configuration
│   │   ├── coverage-thresholds.md   # 95%/85%/80% requirements
│   │   ├── quality-metrics.md       # Code quality thresholds
│   │   └── reports/                 # Per-story QA reports (generated)
│   │
│   └── specs/                   # Planning documents
│       └── requirements/        # Implementation specs
│           └── devforgeai-framework-requirements.md
│
├── .ai_docs/                    # Project management and research
│   ├── Epics/                   # High-level business initiatives
│   ├── Sprints/                 # 2-week iteration plans
│   ├── Stories/                 # Atomic work units
│   ├── Terminal/                # Claude Code Terminal research
│   │   ├── sub-agents.md
│   │   ├── agent-skills.md
│   │   ├── slash-commands-best-practices.md
│   │   ├── native-tools-vs-bash-efficiency-analysis.md
│   │   └── ...
│   ├── Workflows.md             # Workflow architecture research
│   └── prompt-engineering-best-practices.md
│
├── docs/                        # Framework documentation
│   ├── architecture/            # Architecture documentation
│   │   ├── decisions/           # Architecture Decision Records (ADRs)
│   │   │   ├── ADR-001-markdown-for-documentation.md
│   │   │   ├── ADR-002-skills-over-monolithic-workflows.md
│   │   │   ├── ADR-003-subagents-for-parallelism.md
│   │   │   └── ADR-NNN-[decision-name].md
│   │   ├── diagrams/            # Architecture diagrams (Mermaid)
│   │   └── patterns/            # Design patterns documentation
│   │
│   ├── guides/                  # User guides
│   │   ├── quickstart.md
│   │   ├── skill-development.md
│   │   └── subagent-development.md
│   │
│   └── api/                     # API specifications
│       ├── skill-api.md
│       ├── subagent-api.md
│       └── command-api.md
│
├── CLAUDE.md                    # Claude Code project instructions (main entry point)
├── README.md                    # Framework overview and quick start
├── ROADMAP.md                   # Implementation phases and timelines
├── LICENSE                      # MIT License
└── .gitignore                   # Git ignore rules
```

---

## Directory Purpose and Rules

### `.claude/` - Claude Code Configuration (LOCKED)

**Purpose**: Claude Code Terminal automatically discovers skills, subagents, and commands from this directory.

**Rules**:
- ✅ ALL skills go in `.claude/skills/[skill-name]/`
- ✅ ALL subagents go in `.claude/agents/[agent-name].md`
- ✅ ALL slash commands go in `.claude/commands/[command-name].md`
- ❌ NO executable code in `.claude/` (Markdown documentation only)
- ❌ NO language-specific implementations (framework must be agnostic)

**Rationale**: Claude Code Terminal's discovery mechanism requires this exact structure.

### `.claude/skills/` - Framework Skills (LOCKED)

**Purpose**: Autonomous, model-invoked capabilities for each development phase.

**Rules**:
- ✅ Each skill in its own subdirectory (e.g., `devforgeai-development/`)
- ✅ Main skill file MUST be named `SKILL.md`
- ✅ SKILL.md MUST have YAML frontmatter with `name:` and `description:`
- ✅ Keep SKILL.md under 1,000 lines (target: 500-800 lines)
- ✅ Deep documentation goes in `references/` subdirectory
- ✅ Templates and assets go in `assets/` subdirectory
- ❌ NO skills in root `.claude/` directory
- ❌ NO executable scripts in skill directories (documentation only)

**Naming Convention**: `devforgeai-[phase]` (e.g., `devforgeai-architecture`)

**Example**:
```
.claude/skills/devforgeai-development/
├── SKILL.md                 # Main skill (500-800 lines)
└── references/              # Loaded on demand
    ├── tdd-workflow-guide.md
    └── refactoring-patterns.md
```

### `.claude/agents/` - Specialized Subagents (LOCKED)

**Purpose**: Domain-specific AI workers with separate context windows.

**Rules**:
- ✅ Each subagent is a single `.md` file
- ✅ File name becomes subagent name (e.g., `test-automator.md` → `test-automator`)
- ✅ MUST have YAML frontmatter with `name:`, `description:`, `tools:`, `model:`
- ✅ Keep under 500 lines (target: 100-300 lines)
- ✅ Single responsibility per subagent
- ❌ NO subdirectories in `.claude/agents/`
- ❌ NO multi-responsibility subagents

**Naming Convention**: `[domain]-[role]` (e.g., `test-automator`, `backend-architect`)

**Example**:
```
.claude/agents/
├── test-automator.md        # Test generation specialist
├── backend-architect.md     # API implementation specialist
└── code-reviewer.md         # Quality assessment specialist
```

### `.claude/commands/` - Slash Commands (LOCKED)

**Purpose**: User-invoked, parameterized workflows.

**Rules**:
- ✅ Each command is a single `.md` file
- ✅ File name becomes command name (e.g., `dev.md` → `/dev`)
- ✅ MUST have YAML frontmatter with `description:` and `argument-hint:`
- ✅ Keep under 500 lines (target: 200-400 lines)
- ✅ Use `$ARGUMENTS` placeholder for parameters
- ✅ Can invoke skills and subagents
- ❌ NO subdirectories in `.claude/commands/` (flat structure)
- ❌ NO commands exceeding 500 lines (extract to skills)

**Naming Convention**: `[action]` or `[action]-[object]` (e.g., `dev`, `create-context`)

**Example**:
```
.claude/commands/
├── dev.md                   # /dev [STORY-ID]
├── qa.md                    # /qa [STORY-ID]
└── create-context.md        # /create-context [project-name]
```

### `.devforgeai/` - Framework Context (LOCKED)

**Purpose**: Framework's own architectural constraints (meta-level).

**Rules**:
- ✅ Framework's context files go in `.devforgeai/context/`
- ✅ QA configuration goes in `.devforgeai/qa/`
- ✅ Specifications go in `.devforgeai/specs/requirements/`
- ❌ NO project-specific files in `.devforgeai/` (this is framework meta-context)
- ❌ NO executable code in `.devforgeai/` (documentation only)

**Rationale**: Projects using DevForgeAI will have their own `.devforgeai/context/` files created by devforgeai-architecture skill.

### `.ai_docs/` - Project Management (LOCKED)

**Purpose**: Epics, sprints, stories, and research documentation.

**Rules**:
- ✅ Epics go in `.ai_docs/Epics/`
- ✅ Sprints go in `.ai_docs/Sprints/`
- ✅ Stories go in `.ai_docs/Stories/`
- ✅ Research documentation in `.ai_docs/Terminal/`
- ✅ Stories MUST have YAML frontmatter with id, title, epic, sprint, status, points, priority
- ❌ NO code in `.ai_docs/` (documentation only)

**Story Naming**: `STORY-NNN-[title].md` (e.g., `STORY-001-user-authentication.md`)
**Epic Naming**: `EPIC-NNN-[title].md` (e.g., `EPIC-001-user-management.md`)
**Sprint Naming**: `SPRINT-NNN.md` (e.g., `SPRINT-001.md`)

### `docs/` - Framework Documentation (LOCKED)

**Purpose**: Architecture documentation, ADRs, guides, API specs.

**Rules**:
- ✅ ADRs go in `docs/architecture/decisions/`
- ✅ Diagrams go in `docs/architecture/diagrams/`
- ✅ User guides go in `docs/guides/`
- ✅ API specifications go in `docs/api/`
- ❌ NO generated documentation (commit only source)
- ❌ NO language-specific docs (framework must be agnostic)

**ADR Naming**: `ADR-NNN-[decision-title].md` (e.g., `ADR-001-markdown-for-documentation.md`)

---

## File Naming Conventions

### Skills

**Pattern**: `devforgeai-[phase]`
**Examples**:
- ✅ `devforgeai-ideation`
- ✅ `devforgeai-architecture`
- ✅ `devforgeai-development`
- ❌ `IdeationSkill` (no CamelCase)
- ❌ `dev-skill` (use full phase name)

### Subagents

**Pattern**: `[domain]-[role]`
**Examples**:
- ✅ `test-automator`
- ✅ `backend-architect`
- ✅ `deployment-engineer`
- ❌ `TestAutomator` (no CamelCase)
- ❌ `test_automator` (use hyphens, not underscores)

### Slash Commands

**Pattern**: `[action]` or `[action]-[object]`
**Examples**:
- ✅ `dev`
- ✅ `qa`
- ✅ `create-context`
- ✅ `create-story`
- ❌ `DevCommand` (no CamelCase)
- ❌ `create_context` (use hyphens, not underscores)

### Context Files

**Pattern**: `[purpose].md` (all lowercase, hyphens)
**Required Files**:
- `tech-stack.md`
- `source-tree.md`
- `dependencies.md`
- `coding-standards.md`
- `architecture-constraints.md`
- `anti-patterns.md`

**Examples**:
- ✅ `tech-stack.md`
- ✅ `anti-patterns.md`
- ❌ `TechStack.md` (no CamelCase)
- ❌ `tech_stack.md` (use hyphens, not underscores)

### Documentation Files

**Pattern**: `[topic].md` or `[topic]-[subtopic].md`
**Examples**:
- ✅ `README.md`
- ✅ `ROADMAP.md`
- ✅ `tdd-workflow-guide.md`
- ✅ `complexity-assessment-matrix.md`
- ❌ `readme.md` (use UPPERCASE for root docs)
- ❌ `TDDWorkflowGuide.md` (no CamelCase for reference docs)

---

## Forbidden Patterns

### ❌ FORBIDDEN: Monolithic Skills

**Wrong**:
```
.claude/skills/
└── devforgeai-all-in-one/
    └── SKILL.md    # 5,000 lines doing everything
```

**Correct**:
```
.claude/skills/
├── devforgeai-ideation/
├── devforgeai-architecture/
├── devforgeai-development/
├── devforgeai-qa/
└── devforgeai-release/
```

**Rationale**: Modularity enables independent updates and token efficiency.

### ❌ FORBIDDEN: Executable Code in Framework

**Wrong**:
```
.claude/skills/devforgeai-development/
├── SKILL.md
└── scripts/
    └── implement.py    # Python implementation code
```

**Correct**:
```
.claude/skills/devforgeai-development/
├── SKILL.md
└── references/
    └── tdd-workflow-guide.md    # Documentation only
```

**Rationale**: Framework must be language-agnostic. Skills provide instructions, not code.

### ❌ FORBIDDEN: Flat Command Structure

**Wrong**:
```
.claude/commands/
├── dev-backend.md
├── dev-frontend.md
├── dev-database.md
└── dev-tests.md
```

**Correct**:
```
.claude/commands/
└── dev.md    # Single command that handles all development
```

**Rationale**: Commands should orchestrate subagents for specialization, not duplicate command for each domain.

### ❌ FORBIDDEN: Context Files Outside `.devforgeai/context/`

**Wrong**:
```
.claude/
├── tech-stack.md    # ❌ Wrong location
└── skills/
```

**Correct**:
```
.devforgeai/context/
├── tech-stack.md    # ✅ Correct location
```

**Rationale**: Consistent location for AI agents to discover constraints.

---

## Progressive Disclosure Pattern

**Principle**: Keep main files concise, deep details in references.

**Example**:
```
.claude/skills/devforgeai-ideation/
├── SKILL.md (500 lines)
│   # Phase 1: Discovery
│   # Phase 2: Requirements Elicitation
│   # For detailed questions by domain, see references/requirements-elicitation-guide.md
│   # Phase 3: Complexity Assessment
│   # For scoring rubric, see references/complexity-assessment-matrix.md
│
└── references/
    ├── requirements-elicitation-guide.md (1,000 lines)
    ├── complexity-assessment-matrix.md (800 lines)
    ├── domain-specific-patterns.md (1,200 lines)
    └── feasibility-analysis-framework.md (600 lines)
```

**Benefit**: SKILL.md loads immediately (~20K tokens), references load only when needed (saving 60-80% tokens).

---

## Project Context Pattern (For Projects Using DevForgeAI)

When devforgeai-architecture skill creates context for a **project** using DevForgeAI:

```
my-project/
├── .devforgeai/
│   └── context/
│       ├── tech-stack.md        # Project's tech choices (e.g., C#, React, PostgreSQL)
│       ├── source-tree.md       # Project's structure (e.g., Clean Architecture)
│       ├── dependencies.md      # Project's packages (e.g., Dapper 2.1.28)
│       ├── coding-standards.md  # Project's patterns (e.g., async/await rules)
│       ├── architecture-constraints.md  # Project's layer rules
│       └── anti-patterns.md     # Project's forbidden patterns
```

**Distinction**:
- **DevForgeAI's `.devforgeai/context/`**: Framework's own constraints (meta-level)
- **Project's `.devforgeai/context/`**: Project-specific constraints (implementation-level)

---

## Enforcement Checklist

Before committing framework changes:
- [ ] Skills are in `.claude/skills/[skill-name]/` with SKILL.md
- [ ] Subagents are in `.claude/agents/[agent-name].md`
- [ ] Commands are in `.claude/commands/[command-name].md`
- [ ] Context files are in `.devforgeai/context/`
- [ ] ADRs are in `docs/architecture/decisions/`
- [ ] NO executable code in `.claude/` or `.devforgeai/`
- [ ] ALL components use Markdown format (not JSON/YAML)
- [ ] File naming follows conventions (lowercase, hyphens)
- [ ] Main files under size limits (skills <1000 lines, commands <500 lines)
- [ ] Reference documentation uses progressive disclosure

---

## References

- [CLAUDE.md](CLAUDE.md) - Project instructions for Claude Code
- [README.md](README.md) - Framework overview
- [tech-stack.md](tech-stack.md) - Technology constraints
- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/agent-skills)

---

**REMEMBER**: This source-tree.md defines the **framework's own structure**. Projects using DevForgeAI will have their own source-tree.md files created by the devforgeai-architecture skill based on project architecture patterns.
