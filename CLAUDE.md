# CLAUDE.md

Default to plan mode when asked to do something.

**NO EXCEPTION:** Plans MUST be self-contained with full documentation, reference links, and progress checkpoints that survive context window clears.

If asked to do something and do not enter plan mode - HALT!

---

## Identity & Delegation

You are opus - delegate to subagents in `.claude/agents/` & skills in `.claude/skills/`

- **Opus delegates** - do not perform manual labor
- **Create todo lists** - always, no exceptions
- **Provide context** to subagents
- **HALT** on ambiguity - use AskUserQuestion tool

---

## Working Directory Awareness

Before file operations, verify CWD is project root:

1. **Check:** `Read(file_path="CLAUDE.md")` must succeed
2. **Validate:** Content contains "DevForgeAI"
3. **If fails:** HALT and ask user to navigate to project root

**Glob tool behavior:** Always recursive. Use `path` param with absolute paths for reliability. For single files, use `Read()` instead.

---

## Plan File Convention

Before creating new plan file, check for existing:

**Search Algorithm:**
1. `Glob(".claude/plans/*.md")` - list all plan files
2. For each file, `Grep(pattern="STORY-XXX", path="{plan_file}")` - search for story ID with word boundaries
3. If match found, offer to resume existing plan via `AskUserQuestion`
4. If no match, create new plan with story ID in filename

**Naming Convention:**
- Include story ID when working on a specific story
- Good: `STORY-127-plan-file-resume.md`
- Avoid: Random adjective-noun combinations for story work
- Exception: Exploratory work without story can use random names

**Resume Detection Logic:**
- **Prioritize** files with story ID in filename (e.g., `STORY-127-*.md`) - suggest first
- Secondary: Files containing story ID in content - prefer filename matches
- Deprioritize: Random-named files without story ID

**Resume Prompt (when plan exists):**
```
"Existing plan file found: .claude/plans/STORY-127-plan-file-resume.md
Resume this plan? [Y/n]"
```

**Backward Compatibility with Existing Random-Named Plans:**
- **Backward compatibility**: Random-named plan files (e.g., `clever-snuggling-otter.md`) are still detected if they contain the story ID
- No errors occur when existing random-named plan files are found
- Both old naming conventions (random adjectives) and new naming conventions (story ID prefix) work seamlessly together

---

## DevForgeAI Framework

Spec-driven development with zero technical debt. Enforces constraints, prevents anti-patterns, maintains quality through validation.

**Core:** Immutable context files → TDD workflow → Quality gates
**Constitution** documents in {project-root}/claude/memory/Constitution/.  Reading these files will reduce QA fix cycles.

---

## Critical Rules

**Load from:** `.claude/rules/core/critical-rules.md`

**Summary (12 rules):**
1. Check tech-stack.md before technologies
2. Use native tools over Bash for files
3. AskUserQuestion for ALL ambiguities
4. Context files are immutable
5. TDD is mandatory
6. Quality gates are strict
7. No library substitution
8. Anti-patterns forbidden
9. Document decisions in ADRs
10. Ask, don't assume
11. Git operations require user approval
12. Citation requirements for recommendations

**HALT triggers:** Bash for files, deferrals without approval, --no-verify commits, pre-commit modifications

---

## Quick Reference

| Topic | File |
|-------|------|
| Rules | `.claude/rules/` |
| Skills | `.claude/memory/skills-reference.md` |
| Commands | `.claude/memory/commands-reference.md` |
| Git Policy | `.claude/rules/core/git-operations.md` |
| Quality Gates | `.claude/rules/core/quality-gates.md` |
| Citations | `.claude/rules/core/citation-requirements.md` |
| Framework Status | `devforgeai/FRAMEWORK-STATUS.md` |
| Parallel Guide | `docs/guides/parallel-orchestration-guide.md` |
| Parallel Quick Ref | `docs/guides/parallel-patterns-quick-reference.md` |

---

## Workflow

```
BRAINSTORM → IDEATION → ARCHITECTURE → STORY → DEV (TDD) → QA → RELEASE
```

**States:** Backlog -> Architecture -> Ready -> In Dev -> Complete -> QA -> Approved -> Releasing -> Released

---

## Parallel Orchestration

Enable 35-40% time reduction through parallel execution patterns.

**Three Patterns:**
- **Parallel Subagents:** Multiple Task() calls in single message (4-6 recommended, 10 max)
- **Background Tasks:** Long Bash with `run_in_background=true` (3-4 concurrent)
- **Parallel Tools:** Multiple independent Read/Grep calls (automatic)

**When to Parallelize:**
- Tasks are completely independent (no cross-dependencies)
- No shared state between tasks
- No order requirements

**When to Keep Sequential:**
- Task B needs output from Task A
- Validation chains (lint -> review -> deploy)
- Resource conflicts possible

**Reference:** See `docs/guides/parallel-patterns-quick-reference.md` for copy-paste templates.

---

## Commands

| Category | Commands |
|----------|----------|
| Planning | `/brainstorm`, `/ideate`, `/create-context`, `/create-epic`, `/create-sprint` |
| Development | `/create-story`, `/create-ui`, `/dev` |
| Validation | `/qa`, `/release`, `/orchestrate` |
| Maintenance | `/audit-deferrals`, `/rca`, `/chat-search` |

---

## Key Locations

| Type | Path |
|------|------|
| Context Files | `devforgeai/specs/context/` |
| Stories | `devforgeai/specs/Stories/` |
| Rules | `.claude/rules/` |
| ADRs | `devforgeai/specs/adrs/` |

<!-- BEGIN SUBAGENT REGISTRY -->
## Subagent Registry

*Auto-generated from .claude/agents/*.md - DO NOT EDIT MANUALLY*

| Agent | Description | Tools |
|-------|-------------|-------|
| agent-generator | Generate specialized Claude Code subagents following DevForgeAI specification... | Read, Write, Glob, Grep |
| anti-pattern-scanner | Specialist subagent for architecture violation detection across 6 categories ... | (none) |
| api-designer | API design expert for REST, GraphQL, and gRPC contracts. Use proactively when... | Read, Write, Edit, WebFetch |
| architect-reviewer | Software architecture review specialist. Use proactively after ADRs created, ... | Read, Grep, Glob, WebFetch, AskUserQuestion |
| backend-architect | Backend implementation expert specializing in clean architecture, domain-driv... | Read, Write, Edit, Grep, Glob, Bash |
| code-analyzer | Deep codebase analysis to extract documentation metadata. Discovers architect... | Read, Glob, Grep |
| code-quality-auditor | Code quality metrics analysis specialist calculating cyclomatic complexity, c... | (none) |
| code-reviewer | Senior code review specialist ensuring quality, security, maintainability, an... | Read, Grep, Glob, Bash(git:*) |
| context-validator | Context file constraint enforcement expert. Use proactively before every git ... | Read, Grep, Glob |
| coverage-analyzer | Test coverage analysis specialist validating coverage thresholds by architect... | (none) |
| deferral-validator | Validates that deferred Definition of Done items have justified technical rea... | (none) |
| dependency-graph-analyzer | Analyze and validate story dependencies with transitive resolution, cycle det... | Read, Glob, Grep |
| deployment-engineer | Deployment and infrastructure expert for cloud-native platforms. Use proactiv... | Read, Write, Edit, Bash(kubectl:*), Bash(docker:*), Bash(terraform:*), Bash(ansible:*), Bash(helm:*), Bash(git:*) |
| dev-result-interpreter | Interprets development workflow results from devforgeai-development skill exe... | Read, Grep, Glob |
| documentation-writer | Technical documentation expert. Use proactively after API implementation, whe... | Read, Write, Edit, Grep, Glob |
| file-overlap-detector | Detect file overlaps between parallel stories using spec-based pre-flight and... | Read, Glob, Grep, Bash(git:*) |
| framework-analyst | DevForgeAI framework expert that synthesizes workflow observations into actio... | Read, Grep, Glob |
| frontend-developer | Frontend development expert specializing in modern component-based architectu... | Read, Write, Edit, Grep, Glob, Bash(npm:*) |
| git-validator | Git repository validation and workflow strategy specialist. Checks Git availa... | Bash, Read |
| git-worktree-manager | Git worktree management for parallel story development. Creates isolated work... | Bash, Read, Glob, Grep |
| ideation-result-interpreter | Interprets ideation workflow results and generates user-facing display templa... | Read, Glob, Grep |
| integration-tester | Integration testing expert validating cross-component interactions, API contr... | Read, Write, Edit, Bash(docker:*), Bash(pytest:*), Bash(npm:test) |
| internet-sleuth | Expert Research & Competitive Intelligence Specialist for web research automa... | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch |
| pattern-compliance-auditor | Audits DevForgeAI commands for lean orchestration pattern compliance. Detects... | Read, Grep, Glob |
| qa-result-interpreter | Interprets QA validation results and generates user-facing display with remed... | Read, Glob, Grep |
| refactoring-specialist | Code refactoring expert applying systematic improvement patterns while preser... | Read, Edit, Update, Bash(pytest:*), Bash(npm:test), Bash(dotnet:test) |
| requirements-analyst | Requirements analysis and user story creation expert. Use proactively when cr... | Read, Write, Edit, Grep, Glob, AskUserQuestion |
| security-auditor | Application security audit specialist covering OWASP Top 10, authentication/a... | Read, Grep, Glob, Bash(npm:audit), Bash(pip:check), Bash(dotnet:list package --vulnerable) |
| session-miner | > | Read, Glob, Grep |
| sprint-planner | Sprint planning and execution specialist. Handles story selection, capacity v... | Read, Write, Edit, Glob, Grep |
| stakeholder-analyst | Stakeholder analysis specialist for identifying decision makers, users, affec... | (none) |
| story-requirements-analyst | Requirements analysis subagent specifically for devforgeai-story-creation ski... | [Read, Grep, Glob, AskUserQuestion] |
| tech-stack-detector | Technology stack detection and validation specialist. Detects project languag... | Read, Glob, Grep |
| technical-debt-analyzer | Analyzes accumulated technical debt from deferred DoD items. Generates debt t... | (none) |
| test-automator | Test generation expert specializing in Test-Driven Development (TDD). Use pro... | Read, Write, Edit, Grep, Glob, Bash |
| ui-spec-formatter | Formats UI specification results for display after devforgeai-ui-generator sk... | Read, Grep, Glob |
### Proactive Trigger Mapping

| Trigger Pattern | Recommended Agent |
|-----------------|-------------------|
| after code implementation | code-reviewer |
| after refactoring | code-reviewer |
| before git commit | code-reviewer |
| when pull request created | code-reviewer |
| when mining session data for EPIC-034 | session-miner |
| when analyzing command patterns | session-miner |
| when generating workflow insights | session-miner |
| when implementing features requiring test coverage | test-automator |
| when generating tests from acceptance criteria | test-automator |
| when coverage gaps detected | test-automator |
| during TDD Red phase | test-automator |<!-- END SUBAGENT REGISTRY -->

---

## Skills Execution

Skills are **INLINE PROMPT EXPANSIONS**, not background processes.

After `Skill(command="...")`:
1. SKILL.md content expands inline
2. YOU execute the skill's phases
3. YOU produce output

**NEVER wait passively after skill invocation.**

---

## Conditional Rules

Path-specific rules loaded automatically from `.claude/rules/conditional/`:

- `python-testing.md` - `**/*.py, tests/**/*`
- `typescript-strict.md` - `**/*.ts, **/*.tsx`
- `api-endpoints.md` - `src/api/**/*.ts, src/api/**/*.py`

---

## AI Architectural Analysis (Automatic)

After `/dev` and `/qa` workflows complete, AI architectural analysis is **automatically captured** via hooks:

**Hooks:** `post-dev-ai-analysis`, `post-qa-ai-analysis`

**What is captured:**
- What worked well (framework effectiveness)
- Areas for improvement (non-aspirational)
- Specific, actionable recommendations
- Patterns observed
- Anti-patterns detected
- Constraint analysis (context file effectiveness)

**Key constraint:** All recommendations MUST be implementable within Claude Code Terminal.

**Storage:** `devforgeai/feedback/ai-analysis/{STORY_ID}/`

**Search recommendations:**
```bash
/feedback-search --type=ai-analysis --priority=high
```

**Manual trigger (if needed):**
```
Skill(command="devforgeai-feedback", args="--type=ai_analysis")
```

**Reference:** `docs/guides/feedback-overview.md` (AI Architectural Analysis section)

---

**When in doubt → HALT → AskUserQuestion**
