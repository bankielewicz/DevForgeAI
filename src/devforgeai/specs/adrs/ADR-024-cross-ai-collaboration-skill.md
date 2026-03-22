# ADR-024: Add Cross-AI Collaboration Skill and /collaborate Command

## Status

Accepted

## Date

2026-02-24

## Context

DevForgeAI operates within a single-AI paradigm — all development workflows (brainstorming, story creation, TDD, QA, release) execute within Claude Code Terminal. However, complex issues sometimes benefit from a fresh perspective from an external AI system (Gemini, ChatGPT, etc.).

The project has prior art demonstrating this pattern: `tmp/gemini-collaboration-*.md` files from STORY-059 show successful Claude-to-Gemini collaboration that resolved test fixture optimization challenges (38.5% failure reduction in one round). These documents were hand-crafted each time, leading to inconsistency and incomplete context transfer.

A reusable prompt template was created at `tmp/cross-ai-collaboration-prompt.md` following Anthropic's prompt engineering best practices (XML tags, role prompting, structured chain-of-thought, progressive disclosure). However, using the template still requires manual variable filling, manual file reading, and manual constitution compliance checking.

## Decision

Add a `/collaborate` slash command and `cross-ai-collaboration` skill that automate the complete cross-AI collaboration workflow:

```
/collaborate command (src/claude/commands/collaborate.md)
  └── cross-ai-collaboration skill (src/claude/skills/cross-ai-collaboration/)
        ├── SKILL.md (6 phases, ~382 lines)
        └── references/
              └── collaboration-prompt-template.md (output structure template)
```

### Command: `/collaborate`

Thin orchestrator (91 lines) following the lean orchestration pattern:
- Phase 0: Validate arguments (issue description, target AI name)
- Phase 1: Invoke `cross-ai-collaboration` skill

### Skill: `cross-ai-collaboration`

6-phase interactive workflow (382 lines):
- Phase 01: Context Gathering — AskUserQuestion for affected files, attempts, priority
- Phase 02: Constitution Loading — Read all 6 context files, extract relevant constraints
- Phase 03: Code Collection — Read affected files, capture actual source code
- Phase 04: Analysis & Template Population — Reason through the issue, populate 10-section template
- Phase 05: Document Generation — Write self-contained document to `tmp/`
- Phase 06: Completion Report — Display summary and next steps

### Output Document Structure (10 Sections)

1. Executive Summary
2. Project Context (with constitution references)
3. The Specific Problem (Current/Expected/Impact)
4. Code Artifacts (actual code with file paths and line numbers)
5. What We've Tried (each approach + failure analysis)
6. Our Analysis (hypotheses, constraints, solution ideas)
7. Specific Questions for Target AI
8. Proposed Plan with Checkpoints
9. Files Reference Table
10. Constitutional Compliance Checklist

## Rationale

1. **Proven value**: STORY-059 collaboration with Gemini directly resolved issues that Claude alone could not. The "Staccato Style" technique from Gemini produced a 38.5% test failure reduction.
2. **Self-contained output**: The target AI has no access to our filesystem. The skill ensures ALL needed code, context, and constraints are included in the document.
3. **Constitution compliance**: Manual collaboration documents risk proposing solutions that violate framework constraints. The skill automatically reads all 6 context files and includes a compliance checklist.
4. **Follows framework patterns**: Command uses lean orchestration. Skill uses phased workflow with gates. Template uses progressive disclosure in `references/`.
5. **Non-aspirational**: Every section of the output requires concrete file paths, actual code, and specific questions — not vague requests.

### Alternatives Rejected

- **Manual template only**: Rejected because it requires the user to manually fill 10+ variables and read code files themselves.
- **Subagent instead of skill**: Rejected because the workflow requires interactive AskUserQuestion calls (subagents cannot use AskUserQuestion in the current architecture).
- **Embed in claude-code-terminal-expert skill**: Rejected because it violates Single Responsibility Principle (Source: devforgeai/specs/context/architecture-constraints.md). Collaboration is a distinct workflow from terminal expertise.

## Consequences

### Positive

- Standardized, repeatable cross-AI collaboration workflow
- All collaboration documents automatically include constitution compliance checks
- Actual code included in output (not summaries) — enabling meaningful external review
- Interactive gathering ensures no context is missed
- Output filename includes target AI, issue slug, and date for traceability

### Negative

- Adds 1 command and 1 skill to the framework (minor maintenance burden)
- Token cost for reading all 6 constitution files per collaboration (necessary for compliance)

### Changes Required

- `source-tree.md`: Updated to v4.2 — added skill and command entries, updated counts
- New files: `src/claude/commands/collaborate.md`, `src/claude/skills/cross-ai-collaboration/SKILL.md`, `src/claude/skills/cross-ai-collaboration/references/collaboration-prompt-template.md`
