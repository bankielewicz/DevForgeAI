# DevForgeAI - Spec-Driven Development Framework

A comprehensive framework for AI-assisted software development with zero technical debt, leveraging Claude Code Terminal's capabilities for systematic, constraint-enforced development.

## Overview

DevForgeAI transforms the software development lifecycle through **Spec-Driven Development (SDD)**, combining Claude Code Terminal's Skills, Subagents, and Slash Commands into a cohesive workflow that prevents technical debt through explicit constraints and automated validation.

### Core Philosophy

**Spec-Driven Development with AI Enforcement:**
- Immutable context files define architectural boundaries (tech-stack, source-tree, dependencies)
- AI agents MUST follow constraints; ambiguities trigger explicit user questions
- Quality gates enforce standards at every workflow stage
- Test-Driven Development (TDD) workflow: Red → Green → Refactor

**Constitution**: Evidence-based only. All patterns backed by research, official documentation, or proven practices. No aspirational content.

## Architecture

DevForgeAI implements a **three-layer architecture** optimized for Claude Code Terminal:

### Layer 1: Skills (Framework Implementation)

8 autonomous, model-invoked capabilities for each development phase:

- **devforgeai-ideation** - Requirements discovery & epic creation (greenfield/brownfield entry point)
- **devforgeai-architecture** - Context file creation & architecture decision records
- **devforgeai-orchestration** - Workflow coordinator (Epic → Sprint → Story → Dev → QA → Release)
- **devforgeai-story-creation** - Complete story generation with AC, tech/UI specs, and self-validation
- **devforgeai-ui-generator** - Interactive UI spec generation (web/GUI/terminal) with context validation
- **devforgeai-development** - TDD implementation with constraint enforcement
- **devforgeai-qa** - Hybrid validation (light during dev, deep after)
- **devforgeai-release** - Production deployment with automated validation, smoke testing, and rollback

### Layer 2: Subagents (Parallel Task Execution)

16 specialized AI workers with separate context windows for concurrent execution:

**Core Development:**
- **test-automator** - TDD test generation and execution
- **backend-architect** - API/service implementation (clean architecture, DDD)
- **frontend-developer** - UI component development (React, Vue, Angular)
- **integration-tester** - Cross-component testing and API contracts

**Quality & Review:**
- **context-validator** - Fast constraint enforcement (6 context files)
- **code-reviewer** - Quality assessment, optimization, and deferral review
- **security-auditor** - OWASP Top 10, auth/authz scanning
- **refactoring-specialist** - Safe refactoring and code smell removal
- **deferral-validator** - Validates deferred DoD items, detects circular deferrals (NEW - RCA-006)

**Architecture & Planning:**
- **requirements-analyst** - User story creation, acceptance criteria
- **architect-reviewer** - Technical design validation and scalability
- **api-designer** - REST/GraphQL/gRPC contract design
- **technical-debt-analyzer** - Debt trend analysis and pattern detection (NEW - RCA-006)

**Operations & Documentation:**
- **deployment-engineer** - Infrastructure, IaC, CI/CD pipelines
- **documentation-writer** - Technical docs, API specs, user guides
- **agent-generator** - Meta-agent for generating new specialized subagents

### Layer 3: Slash Commands (Reusable Workflows)

9 user-invoked, parameterized workflows for common tasks:

**Planning & Setup:**
- `/ideate [business-idea]` - Transform idea to structured requirements
- `/create-context [project-name]` - Generate 6 architectural context files
- `/create-epic [epic-name]` - Generate epic from requirements
- `/create-sprint [sprint-number]` - Plan 2-week sprint with story selection
- `/create-agent [name] [options]` - Create framework-aware subagent (NEW 2025-11-15)

**Story Development:**
- `/create-story [story-name]` - Generate story with acceptance criteria
- `/create-ui [STORY-ID]` - Generate UI component specs (web/GUI/terminal)
- `/dev [STORY-ID]` - Execute TDD development cycle (Red→Green→Refactor)

**Validation & Release:**
- `/qa [STORY-ID]` - Run quality validation (light/deep modes)
- `/release [STORY-ID]` - Deploy to staging and production

**Orchestration:**
- `/orchestrate [STORY-ID]` - Full lifecycle: Dev → QA → Release

## Development Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. IDEATION (devforgeai-ideation)                              │
│    Transforms business ideas → structured requirements          │
│    Output: Epic documents, requirements specifications          │
├─────────────────────────────────────────────────────────────────┤
│ 2. ARCHITECTURE (devforgeai-architecture)                      │
│    Creates immutable context files defining constraints         │
│    Output: 6 context files in .devforgeai/context/             │
├─────────────────────────────────────────────────────────────────┤
│ 3. ORCHESTRATION (devforgeai-orchestration)                    │
│    Manages story lifecycle through 11 workflow states           │
│    Output: Sprint plans, story files with acceptance criteria   │
├─────────────────────────────────────────────────────────────────┤
│ 4. DEVELOPMENT (devforgeai-development)                        │
│    TDD implementation: Write tests → Implement → Refactor       │
│    Output: Production code with 95%/85%/80% test coverage      │
├─────────────────────────────────────────────────────────────────┤
│ 5. QA (devforgeai-qa)                                          │
│    Light validation (during dev) + Deep validation (after)      │
│    Output: Quality reports, coverage analysis, compliance       │
├─────────────────────────────────────────────────────────────────┤
│ 6. RELEASE (devforgeai-release)                                │
│    Automated deployment with smoke tests and rollback           │
│    Output: Production deployment, release notes, monitoring     │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Claude Code Terminal (version 1.0+)
- Git repository
- Development environment for your tech stack

### Initial Setup

1. **Start Ideation Phase:**
   ```bash
   claude
   > /ideate "Build a task management system with AI prioritization"
   ```

2. **Create Architectural Context:**
   ```bash
   > /create-context task-management-system
   ```

3. **Generate Epic and Sprint:**
   ```bash
   > /create-epic EPIC-001-task-management
   > /create-sprint 1
   ```

### Implementing a Story

1. **Execute TDD Development Cycle:**
   ```bash
   > /dev STORY-001
   ```
   Behind the scenes:
   - Reads story acceptance criteria
   - Invokes test-automator (writes failing tests)
   - Invokes backend-architect (implements code)
   - Runs light QA after each phase
   - Updates story status to "Dev Complete"

2. **Run Quality Validation:**
   ```bash
   > /qa STORY-001
   ```
   Behind the scenes:
   - Runs coverage analysis (strict thresholds)
   - Scans for anti-patterns
   - Validates acceptance criteria
   - Updates story status to "QA Approved"

3. **Deploy to Production:**
   ```bash
   > /release STORY-001
   ```
   Behind the scenes:
   - Deploys to staging → smoke tests
   - Deploys to production
   - Post-deployment validation
   - Updates story status to "Released"

### Orchestrated Workflow

Execute entire story lifecycle with one command:
```bash
> /orchestrate STORY-001
```

## Project Structure

```
.claude/
├── skills/              # Framework implementation (8 skills)
│   ├── devforgeai-ideation/
│   ├── devforgeai-architecture/
│   │   └── assets/adr-examples/
│   │       ├── ADR-EXAMPLE-001-database-selection.md
│   │       └── ADR-EXAMPLE-006-scope-descope.md (NEW)
│   ├── devforgeai-orchestration/
│   │   └── references/quality-gates.md (enhanced with deferral validation)
│   ├── devforgeai-ui-generator/
│   ├── devforgeai-development/ (enhanced with deferral validation)
│   ├── devforgeai-qa/ (enhanced with deferral validation)
│   └── devforgeai-release/
│
├── agents/              # Specialized subagents (18 agents)
│   ├── test-automator.md
│   ├── backend-architect.md
│   ├── frontend-developer.md
│   ├── integration-tester.md
│   ├── context-validator.md
│   ├── tech-stack-detector.md (NEW - 2025-11-05)
│   ├── git-validator.md (NEW - 2025-11-05)
│   ├── code-reviewer.md (enhanced with DoD completeness review)
│   ├── security-auditor.md
│   ├── refactoring-specialist.md
│   ├── requirements-analyst.md
│   ├── architect-reviewer.md
│   ├── api-designer.md
│   ├── deployment-engineer.md
│   ├── documentation-writer.md
│   ├── agent-generator.md
│   ├── deferral-validator.md (NEW - RCA-006)
│   └── technical-debt-analyzer.md (NEW - RCA-006)
│
└── commands/            # User-facing workflows (9 commands)
    ├── ideate.md
    ├── create-context.md
    ├── create-epic.md
    ├── create-sprint.md
    ├── create-story.md
    ├── create-ui.md
    ├── dev.md
    ├── qa.md
    ├── release.md
    └── orchestrate.md

.devforgeai/
├── context/             # Immutable architectural constraints
│   ├── tech-stack.md
│   ├── source-tree.md
│   ├── dependencies.md
│   ├── coding-standards.md
│   ├── architecture-constraints.md
│   └── anti-patterns.md
│
├── qa/                  # QA validation outputs
│   ├── coverage-thresholds.md
│   ├── quality-metrics.md
│   └── reports/
│
├── specs/
│   ├── requirements/    # Planning documents and specs
│   └── enhancements/    # RCA documents (RCA-001 through RCA-006)
│
├── technical-debt-register.md (NEW - RCA-006)
└── adrs/                # Architecture Decision Records

src/                     # Framework source for installer (NEW - STORY-041, EPIC-009 Phase 1)
├── claude/              # Claude Code Terminal components
│   ├── skills/          # 10 skill subdirectories
│   ├── agents/          # Subagent definitions
│   ├── commands/        # Slash command definitions
│   └── memory/          # Reference documentation
│
└── devforgeai/          # DevForgeAI framework components
    ├── context/         # Context file templates
    ├── protocols/       # Framework protocols
    ├── specs/           # Specifications (enhancements, requirements, ui)
    ├── adrs/            # ADR templates and examples
    ├── deployment/      # Deployment configurations
    └── qa/              # QA templates and tooling

.ai_docs/
├── Epics/               # High-level business initiatives
├── Sprints/             # 2-week iteration plans
└── Stories/             # Atomic work units with acceptance criteria
```

## Key Features

### Context-First Development

Before ANY code is written:
1. Check for 6 context files in `.devforgeai/context/`
2. If missing → Auto-invoke `devforgeai-architecture` skill
3. Context files become THE LAW for all development

Context files prevent:
- Library substitution (e.g., Dapper → Entity Framework)
- Structure violations (files in wrong locations)
- Cross-layer dependencies (Domain → Infrastructure)
- Framework mixing (Redux in Zustand project)
- Unapproved package additions

### Quality Gates

Stories must progress through workflow stages sequentially:

**Gate 1: Context Validation** (Architecture → Ready for Dev)
- All 6 context files exist and are non-empty
- No placeholder content (TODO, TBD)

**Gate 2: Test Passing** (Dev Complete → QA In Progress)
- Build succeeds
- All tests pass (100% pass rate)
- Light validation passed

**Gate 3: QA Approval** (QA Approved → Releasing)
- Deep validation PASSED
- Coverage meets strict thresholds (95%/85%/80%)
- Zero CRITICAL violations (includes circular deferrals)
- Zero HIGH violations (includes unjustified deferrals, invalid story refs)
- All deferred DoD items have valid technical justification (NEW - RCA-006)

**Gate 4: Release Readiness** (Releasing → Released)
- QA approved
- All workflow checkboxes complete
- No blocking dependencies

### Token Efficiency

Optimized for Claude Code Terminal's constraints:
- Light QA validation: ~10,000 tokens
- Deep QA validation: ~65,000 tokens
- Feature implementation: ~80,000 tokens
- Total per story (dev + QA): ~155,000 tokens

Achieved through:
- Using native tools instead of Bash (40-73% token savings)
- Progressive disclosure (reference files loaded on demand)
- Parallel tool invocations when possible
- Focused validation (don't re-validate passing components)

## Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed implementation phases, timelines, and success metrics.

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive guide for Claude Code (project instructions)
- **[ROADMAP.md](ROADMAP.md)** - Implementation phases and timelines
- **[.ai_docs/Terminal/](/.ai_docs/Terminal/)** - Claude Code Terminal best practices
- **[.devforgeai/specs/requirements/](/.devforgeai/specs/requirements/)** - Requirements specifications

## Technical Stack

Framework-agnostic design supports:
- **Languages**: Node.js, Python, C#, Go, Java, Rust, etc.
- **Testing**: Jest, pytest, xUnit, Go test, JUnit, etc.
- **Deployment**: Kubernetes, Azure App Service, AWS ECS/Lambda, Docker, VPS
- **CI/CD**: GitHub Actions, GitLab CI, Azure DevOps, Jenkins

## Benefits

### For Developers
- Systematic TDD workflow with automated test generation
- Architectural constraints prevent common mistakes
- Automated quality validation catches issues early
- One-command deployment reduces manual effort

### For Teams
- Consistent development patterns across projects
- Shared context files enforce architectural decisions
- Quality gates ensure code review standards
- Audit trails track all workflow transitions

### For Organizations
- Zero technical debt through constraint enforcement
- Predictable delivery with story-based estimation
- Automated compliance through anti-pattern detection
- Knowledge preservation through ADRs and documentation

## Research Foundation

DevForgeAI is built on proven patterns from:
- **Official Claude Code Documentation** (docs.claude.com)
- **Production Implementations** (Pimzino's spec-workflow, OneRedOak's dual-loop architecture)
- **Community Best Practices** (julibuilds' command library, qdhenry's Command Suite)
- **Token Efficiency Research** (40-73% savings with native tools vs Bash)

All patterns are evidence-based, backed by research, official documentation, or proven practices. No aspirational content.

## Contributing

1. Follow spec-driven development workflow
2. All changes must pass quality gates
3. Context files are immutable (require ADR for changes)
4. Test coverage requirements: 95%/85%/80% by layer
5. Document all architectural decisions

## License

MIT License - See [LICENSE](LICENSE) for details

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: [.ai_docs/](.ai_docs/)

---

**Built with Claude Code Terminal** - Leveraging Skills, Subagents, and Slash Commands for systematic, constraint-enforced development.
