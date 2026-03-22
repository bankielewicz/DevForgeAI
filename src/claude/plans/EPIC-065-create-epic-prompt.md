# AI Prompt: Create EPIC-065 — Skill Gerund Naming Convention Migration

**Purpose:** Copy-paste this entire document as your first message in a new Claude Code session to create EPIC-065.
**Created:** 2026-02-15
**Source Plan:** `.claude/plans/dev-analysis-phase2-online-docs.md` (Phase 3 + Phase 4)

---

## Instructions for Claude

You are starting a new session with NO prior conversation context. Your task is to create an epic using the `/create-epic` command. All decisions have already been made in a prior analysis session and are documented in the plan file referenced below. **Do NOT re-derive, re-evaluate, or second-guess any decisions.**

### Step 1: Read the Source Plan (MANDATORY FIRST)

Before doing ANYTHING else, read the complete plan file:

```
Read(file_path=".claude/plans/dev-analysis-phase2-online-docs.md")
```

This file is ~1,100 lines. You MUST read ALL of it, especially:
- **Phase 3** (Sections 3.1 through 3.12): The complete rename analysis, constitutional conflict resolution, migration checklist, and full-fleet roadmap
- **Phase 4** (Sections 4.1 through 4.7): Session handoff guide with pre-made decisions, ADR draft, and workflow commands

After reading, confirm you understand the following key facts (do NOT ask the user to confirm — these are established):
- The skill `devforgeai-development` is being renamed to `devforgeai-implementing-stories`
- This requires ADR-017 because two LOCKED context files define a `devforgeai-[phase]` naming convention that must change
- ADR-016 is ALREADY TAKEN (`ADR-016-dead-code-detector-read-only.md`) — use ADR-017
- The latest epic is EPIC-064 — use EPIC-065
- The latest story is STORY-412 — MVP story will be STORY-413+
- 14 skills need renaming total; this epic covers all of them; the MVP story covers only `devforgeai-development`
- `/brainstorm` and `/ideate` have been SKIPPED — their value is captured in the plan

### Step 2: Execute the /create-epic Command

```
/create-epic Skill Gerund Naming Convention Migration
```

The `/create-epic` command invokes the `devforgeai-orchestration` skill, which runs an interactive 8-phase workflow. It will ask you questions via `AskUserQuestion`. Use the answers below.

### Step 3: Answer Interactive Questions

When the orchestration skill asks questions during epic creation, use these pre-determined answers:

**Epic Goal / Business Problem:**
> DevForgeAI skill names use generic noun-form naming (`devforgeai-development`, `devforgeai-qa`, `designing-systems`) that violates Anthropic's officially recommended gerund naming convention (Source: `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md`, line 156). Gerund form (verb+-ing) names like `devforgeai-implementing-stories` more clearly describe what each skill does, improving Claude's skill discovery accuracy. This also resolves the Phase 2 analysis finding N3 (score gap in skill naming). The migration requires an ADR (ADR-017) because the current naming convention is LOCKED in two constitutional context files (source-tree.md line 834, coding-standards.md line 117).

**Timeline:**
> 3-4 sprints. MVP (first skill rename) in Sprint 1. Remaining 13 skills across Sprints 2-4.

**Priority:**
> MEDIUM — This is a quality improvement, not a blocking deficiency. Skills function with old names. But new skills created after ADR-017 MUST use gerund form, so the convention change should happen soon.

**Business Value:**
> Alignment with Anthropic best practices; improved skill discovery accuracy; clearer skill naming for users and Claude; establishes naming convention that scales as more skills are added.

**Stakeholders:**
> DevForgeAI framework maintainers, Claude Code users who invoke `/dev`, `/qa`, and other commands.

**Success Criteria:**
> All 14 `devforgeai-*` skills use gerund naming (3 exempt: devforgeai-shared, claude-code-terminal-expert, skill-creator). All 6 context files updated. All commands function correctly. Zero grep hits for old skill names in active (Tier 0-4) files.

**Features (when asked to decompose):**
The plan defines these features — provide them when the requirements-analyst subagent asks:

1. **ADR-017 Creation & Constitutional Updates** — Create ADR-017-skill-gerund-naming-convention.md establishing the new `devforgeai-[gerund-phrase]` convention. Update 5 constitutional context files (source-tree.md, coding-standards.md, architecture-constraints.md, anti-patterns.md, tech-stack.md) with new naming pattern, bump versions. Update `.claude/memory/Constitution/` mirrors.

2. **MVP: Rename devforgeai-development → devforgeai-implementing-stories** — Rename skill directory in both `.claude/skills/` and `src/claude/skills/`. Update SKILL.md frontmatter (name + description third-person fix). Update 3 command files (dev.md, resume-dev.md, orchestrate.md). Update ~165 reference files across CLAUDE.md, memory files, subagent files, other skills, and rules. Verify zero residual references. Functional test with `/dev`.

3. **Rename devforgeai-qa → devforgeai-validating-quality** — Same pattern as Feature 2 applied to QA skill. Estimated ~400-600 file references.

4. **Rename devforgeai-story-creation → devforgeai-creating-stories** — Same pattern. Estimated ~300-500 file references.

5. **Rename Remaining Skills (10 skills)** — Progressive migration of architecture, ideation, orchestration, documentation, feedback, rca, release, ui-generator, subagent-creation, mcp-cli-converter. One story per skill. See plan Section 3.12 for complete proposed names.

6. **Full-Fleet Verification** — Final verification story confirming all skills renamed, all context files clean, all commands functional. Remove "legacy accepted" language from context files.

**Technical Assessment (when architect-reviewer asks):**
> Complexity: 4/10 — Mechanical find-replace operations, no logic changes. Risk: Medium — high file count (~169 for MVP, ~1,425 total references) means missed references are likely. Mitigation: post-rename grep scan. Prerequisites: None — context files exist, all referenced files verified. Framework validation: ADR-017 resolves the constitutional conflict; no other violations.

**If asked about context files / greenfield vs brownfield:**
> Brownfield — all 6 context files exist in `devforgeai/specs/context/`. This is an existing framework refactoring, not a new project.

### Step 4: Review and Accept the Epic

After the orchestration skill creates the epic file:
1. Review the generated epic at `devforgeai/specs/Epics/EPIC-065-skill-gerund-naming-convention-migration.epic.md`
2. Verify it includes all 6 features listed above
3. Verify the technical assessment reflects complexity 4/10
4. Accept the epic

### Step 5: Report Completion

After the epic is created, display:
- The epic file path
- Feature count
- A reminder that the next step is: `/create-story` for the MVP story (Feature 2: rename devforgeai-development)
- A reminder to reference plan Section 4.2 Step 3 for the complete MVP story specification (8 pre-written acceptance criteria)

---

## What NOT to Do

- ❌ Do NOT run `/brainstorm` or `/ideate` — already completed (plan Sections 3.1-3.3)
- ❌ Do NOT change the recommended skill name — `devforgeai-implementing-stories` was chosen from 5 candidates (plan Section 3.2)
- ❌ Do NOT use ADR-016 — it's taken. Use ADR-017.
- ❌ Do NOT rename any skill files — this session only creates the EPIC
- ❌ Do NOT skip reading the plan file — it contains constitutional conflict analysis that is critical context
- ❌ Do NOT create stories in this session — epic first, stories in a subsequent session

## Troubleshooting

**If `/create-epic` asks for a name and you already provided one:**
Re-provide: `Skill Gerund Naming Convention Migration`

**If the orchestration skill HALTs on context file validation:**
This is expected — the skill validates against current context files which still use the old `devforgeai-[phase]` convention. Explain that ADR-017 (Feature 1) will update the convention, and the epic is planning that change.

**If epic ID EPIC-065 is already taken (created between plan and execution):**
Use the next available ID. Check with: `Glob(pattern="devforgeai/specs/Epics/EPIC-06*.md")`

**If the skill asks questions not covered above:**
Use the plan file (`.claude/plans/dev-analysis-phase2-online-docs.md`) as the authoritative source. If the answer isn't in the plan, use `AskUserQuestion` to ask the human user — do NOT guess.
