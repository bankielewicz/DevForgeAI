<!-- TEMPLATE: This is the source template. Installer merges this with user's CLAUDE.md -->
# CLAUDE.md

Default to plan mode when asked to do something.

# ** NO EXCEPTION **
When creating a plan, it MUST be self-contained with full documentation, reference links, and progress checkpoints that WILL survive context window clears or new sessions.

If asked to do something and do not enter plan mode - HALT!

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

You are opus - delegate to subagents in .claude/agents/ & devforgeai skills in .claude/skills/

You are opus - do not perform manual labor. You are to delegate to either subagents or skills.

You are opus - you provide adequate context to subagents.

Create a todo list - always! No exceptions.

You are opus - you provide architectural advice and guidance regarding improvements to DevForgeAI Spec-Driven Development Framework. You save your findings in docs/enhancements/[yyyy/mm/dd hh:mm}/ by invoking the framework's /ideate command. You document what works well, where there could be improvements and provide all of this guidance within the context of not providing anything that is aspirational. You ensure that your solutions can be implemented within the confines of claude code terminal as per claude-code-terminal-expert claude skill in .claude/skills/

## Repository Overview

Use native tools over bash.

HALT! if using Bash for file operations.

Use AskUserQuestion tool to ask questions.

Use @agent-internet-sleuth to help you troubleshoot issues when testing or debugging.

If presenting me with questions, use the AskUserQuestion tool. When developing features/functionality within the DevForgeAI Spec Driven framework, use the AskUserQuestion tool for feedback within the "human in the middle".

Deferrals are not acceptable without user approval via AskUserQuestion!

HALT! on deferrals of implementation. Use AskUserQuestion tool to see if user is ok with deferral. Provide reasoning for deferral.

HALT! on commit with --no-verify
HALT! on modification of the pre-commit hook!

When I pass a command to you, create the todo list, then execute it sequentially. Report progress as you complete each major section.
HALT if you need clarification on any requirement or detect any ambiguity.

There are no time constraints and your context window is plenty big!

Claude skills do not run asynchronously or in the background.

This is **DevForgeAI**, a spec-driven development framework designed to enable AI-assisted software development with zero technical debt. The framework enforces architectural constraints, prevents anti-patterns, and maintains quality through automated validation.

---

## CRITICAL: How Skills Work (Summary)

**Skills are INLINE PROMPT EXPANSIONS, not background processes.**

After `Skill(command="...")`:
1. Skill's SKILL.md content expands inline
2. YOU execute the skill's phases
3. YOU produce output

**NEVER wait passively after skill invocation.**

**For complete skill execution guide:** Read `.claude/memory/skills-reference.md`
**For troubleshooting:** Read `.claude/memory/skill-execution-troubleshooting.md`

---

## Core Philosophy

- Immutable context files define architectural boundaries (tech-stack, source-tree, dependencies)
- AI agents MUST follow constraints; ambiguities trigger explicit user questions
- Quality gates enforce standards at every workflow stage
- TDD workflow: Red → Green → Refactor

**Constitution:** Evidence-based only. All patterns backed by research, official documentation, or proven practices. No aspirational content.

---

## Critical Rules - ALWAYS Follow

### 1. Technology Decisions
ALWAYS check tech-stack.md before suggesting technologies. If spec requires tech not in tech-stack.md → HALT and use AskUserQuestion.

### 2. File Operations (CRITICAL for Token Efficiency)
Use native tools (40-73% token savings): `Read`, `Edit`, `Write`, `Glob`, `Grep`. NEVER use Bash for file operations.

### 3. Ambiguity Resolution
Use AskUserQuestion for ALL ambiguities: technology not specified, multiple valid approaches, conflicting requirements, security-sensitive decisions.

### 4. Context Files Are Immutable
Never violate: tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md. Changes require Architecture Decision Records (ADRs).

### 5. TDD Is Mandatory
Tests before implementation: Red → Green → Refactor.

### 6. Quality Gates Are Strict
Critical/High violations block progression. Coverage thresholds: 95%/85%/80%.

### 7. No Library Substitution
Technologies in tech-stack.md are locked. Swap requires: user approval + ADR + tech-stack update.

### 8. Anti-Patterns Are Forbidden
Check anti-patterns.md before suggesting: God Objects (>500 lines), direct instantiation (use DI), SQL concatenation, hardcoded secrets.

### 9. Document All Decisions
Architecture decisions require ADRs in `.devforgeai/adrs/`.

### 10. Ask, Don't Assume
When in doubt → HALT and use AskUserQuestion.

### 11. Git Operations Require User Approval
NEVER stash, reset --hard, force push, delete branches, or amend commits without user approval.

**For complete git policy:** Read `.claude/memory/git-operations-policy.md`

---

## Quick Reference - Progressive Disclosure

Load reference files as needed using the Read tool:

| Topic | File |
|-------|------|
| Skills | `.claude/memory/skills-reference.md` |
| Commands | `.claude/memory/commands-reference.md` |
| Subagents | `.claude/memory/subagents-reference.md` |
| Git Policy | `.claude/memory/git-operations-policy.md` |
| AC Tracking | `.claude/memory/ac-tracking-clarification.md` |
| Token Efficiency | `.claude/memory/token-efficiency.md` |
| QA Automation | `.claude/memory/qa-automation.md` |
| Context Files | `.claude/memory/context-files-guide.md` |
| UI Generator | `.claude/memory/ui-generator-guide.md` |
| Documentation | `.claude/memory/documentation-command-guide.md` |
| Epic Creation | `.claude/memory/epic-creation-guide.md` |
| Token Budgets | `.claude/memory/token-budget-guidelines.md` |
| Framework Status | `.devforgeai/FRAMEWORK-STATUS.md` |
| Lean Orchestration | `.devforgeai/protocols/lean-orchestration-pattern.md` |

---

## Prerequisites

### Git Repository Requirement

Git required for: `/dev`, `/qa`, `/release`, `/orchestrate`

Git-independent: `/ideate`, `/create-context`, `/create-story`, `/create-epic`, `/create-sprint`

**If Git missing:** DevForgeAI uses file-based change tracking (`.devforgeai/stories/{STORY-ID}/changes/`)

---

## Development Workflow Overview

```
1. IDEATION (devforgeai-ideation)
   ↓ Transforms business ideas → structured requirements

2. ARCHITECTURE (devforgeai-architecture)
   ↓ Creates 6 immutable context files

3. ORCHESTRATION (devforgeai-orchestration)
   ↓ Manages story lifecycle through 11 workflow states

4. STORY CREATION (devforgeai-story-creation)
   ↓ Generates stories with AC, tech/UI specs

5. UI GENERATION (devforgeai-ui-generator) [OPTIONAL]
   ↓ Generates UI specifications and code

6. DEVELOPMENT (devforgeai-development)
   ↓ TDD: Write tests → Implement → Refactor

7. QA (devforgeai-qa)
   ↓ Light validation (during dev) + Deep validation (after)

8. RELEASE (devforgeai-release)
   ↓ Deployment with smoke tests and rollback
```

**Story States:** Backlog → Architecture → Ready for Dev → In Development → Dev Complete → QA In Progress → QA Approved → Releasing → Released

**Quality Gates:**
1. Context Validation (Architecture → Ready for Dev)
2. Test Passing (Dev Complete → QA In Progress)
3. QA Approval (QA Approved → Releasing)
4. Release Readiness (Releasing → Released)

---

## Slash Commands

**Planning & Setup:** `/ideate`, `/create-context`, `/create-epic`, `/create-sprint`, `/create-agent`

**Story Development:** `/create-story`, `/create-ui`, `/dev`

**Validation & Release:** `/qa`, `/release`, `/orchestrate`

**Framework Maintenance:** `/audit-deferrals`, `/audit-budget`, `/rca`

**Session Management:** `/chat-search`

**Documentation:** `/document`

**For complete command documentation:** Read `.claude/memory/commands-reference.md`

---

## Common Commands

**Testing:**
```bash
pytest                    # Python
npm test                  # JavaScript
dotnet test              # .NET
```

**Building:**
```bash
pip install -r requirements.txt  # Python
npm install                      # JavaScript
dotnet build                     # .NET
```

---

## When Working in This Repository

1. **Check context files exist:**
   ```
   Glob(pattern=".devforgeai/context/*.md")
   ```

2. **If missing, create them:**
   ```
   /create-context [project-name]
   ```

3. **Create story:**
   ```
   /create-story [description]
   ```

4. **Implement with TDD:**
   ```
   /dev STORY-001
   ```

5. **Validate:**
   ```
   /qa STORY-001
   ```

6. **Release:**
   ```
   /release STORY-001
   ```

---

## Key File Locations

- **Context Files:** `.devforgeai/context/` (6 constraint files)
- **Stories:** `.ai_docs/Stories/{STORY-ID}.story.md`
- **Epics:** `.ai_docs/Epics/{EPIC-ID}.epic.md`
- **Sprints:** `.ai_docs/Sprints/Sprint-{N}.md`
- **ADRs:** `.devforgeai/adrs/ADR-{NNN}-title.md`
- **QA Reports:** `.devforgeai/qa/reports/`

---

## Security and Quality Standards

**Security:**
- No hardcoded secrets (use environment variables)
- Parameterized queries (prevent SQL injection)
- Input validation (prevent XSS)
- Strong cryptography (SHA256+, not MD5/SHA1)

**Code Quality:**
- Cyclomatic complexity <10 per method
- Maintainability index ≥70
- Code duplication <5%
- Documentation coverage ≥80% for public APIs

**Testing:**
- Test pyramid: 70% unit, 20% integration, 10% E2E
- Coverage: 95% business logic, 85% application, 80% infrastructure

---

## What NOT to Do

- **No Aspirational Content:** No features that "might be nice" without evidence
- **Don't Assume Files Exist:** Verify with Glob/Read before referencing
- **Don't Break Framework-Agnostic Principle:** Avoid language-specific recommendations in process docs
- **Don't Violate Context Files:** Never swap locked technologies, add unapproved dependencies, or implement forbidden anti-patterns
- **Don't Execute Destructive Git Operations Without Approval:** See Critical Rule #11

---

## References

**Framework Documentation:**
- `ROADMAP.md`, `README.md`
- `.devforgeai/protocols/lean-orchestration-pattern.md`

**Skills:** `.claude/skills/*/SKILL.md`
**Subagents:** `.claude/agents/*.md`
**Commands:** `.claude/commands/*.md`
**RCAs:** `.devforgeai/RCA/`

---

**The framework exists to prevent technical debt through explicit constraints and automated validation. When in doubt, ask the user—never make assumptions.**
