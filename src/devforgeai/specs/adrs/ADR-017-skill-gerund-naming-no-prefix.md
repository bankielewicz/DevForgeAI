# ADR-017: Skill Gerund Naming Convention with Prefix Removal

**Status:** Accepted
**Date:** 2026-02-16
**Decision Makers:** DevForgeAI Framework Team
**Context:** EPIC-065, EPIC-066 (cancelled)

---

## Context

DevForgeAI skill names use generic noun-form naming with a framework prefix (`devforgeai-development`, `devforgeai-qa`, `devforgeai-architecture`). This naming pattern has two conformance gaps against Anthropic's official Agent Skills best practices:

1. **Non-gerund naming:** Anthropic recommends gerund form (verb + -ing) for skill names.
   > *"We recommend using gerund form (verb + -ing) for Skill names, as this clearly describes the activity or capability the Skill provides."*
   > (Source: `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md`, lines 156-157)

2. **Unnecessary framework prefix:** Anthropic's skill naming examples use no framework prefix.
   > Good naming examples: `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`, `testing-code`, `writing-documentation`
   > (Source: `best-practices.md`, lines 160-165)

The current naming convention is LOCKED in two constitutional context files:
- `devforgeai/specs/context/coding-standards.md`, line 117: `devforgeai-[phase]`
- `devforgeai/specs/context/source-tree.md`, lines 835-841: pattern and examples

This ADR authorizes the change to both context files.

---

## Decision

### 1. Adopt gerund naming convention for all skills

**New pattern:** `[gerund-phrase]`

Where `[gerund-phrase]` follows Anthropic's `[activity]-[input]` pattern:
- Activity: gerund form verb (implementing, validating, creating, etc.)
- Input: the object of the activity (stories, quality, architecture, etc.)

### 2. Remove `devforgeai-` prefix from all skill names

The prefix adds 11 characters of noise to every skill name and ~11 tokens to the always-loaded system prompt metadata. Anthropic's examples consistently use no framework prefix. Skills are already namespaced by their directory location (`.claude/skills/`).

### 3. Transition period

- Legacy names accepted in `.backup` directories and Tier 5 historical files (feedback, completed workflows, archives)
- New skills MUST use new convention immediately
- Existing skills migrated incrementally (MVP skill first, then batch)

---

## Migration Table

| Current Name | New Name (Gerund, No Prefix) | Priority |
|-------------|------------------------------|----------|
| `devforgeai-development` | `implementing-stories` | MVP |
| `devforgeai-qa` | `validating-quality` | HIGH |
| `devforgeai-story-creation` | `creating-stories` | HIGH |
| `devforgeai-architecture` | `designing-architecture` | MEDIUM |
| `devforgeai-ideation` | `discovering-requirements` | MEDIUM |
| `devforgeai-orchestration` | `orchestrating-workflows` | MEDIUM |
| `devforgeai-documentation` | `generating-documentation` | LOW |
| `devforgeai-feedback` | `collecting-feedback` | LOW |
| `devforgeai-rca` | `analyzing-root-causes` | LOW |
| `devforgeai-release` | `releasing-stories` | LOW |
| `devforgeai-ui-generator` | `generating-ui-specs` | LOW |
| `devforgeai-subagent-creation` | `creating-subagents` | LOW |
| `devforgeai-brainstorming` | `brainstorming-ideas` | LOW |
| `devforgeai-mcp-cli-converter` | `converting-mcp-cli` | LOW |

**Exempt (no rename):**
- `devforgeai-shared` — utility module, not user-facing skill
- `claude-code-terminal-expert` — non-`devforgeai-` prefix, different namespace
- `skill-creator` — non-`devforgeai-` prefix, different namespace

---

## Rationale

### Anthropic Alignment

Anthropic's Agent Skills specification is the platform vendor's official guidance. Conforming to it:
- Improves Claude's skill discovery accuracy (gerund names describe activities)
- Reduces context window waste (shorter names in always-loaded metadata)
- Establishes professional naming consistency across the skill library
- Follows the Anthropic Skills Checklist requirement: *"Consistent terminology throughout"* (Source: `best-practices.md`, line 1087)

### Prefix Removal Justification

| Argument | Resolution |
|----------|------------|
| "Prefix helps identify DevForgeAI skills" | The skill description field handles identification better than a name prefix |
| "Prefix prevents name collisions" | Skills live in `.claude/skills/` — directory provides namespacing |
| "Prefix maintains consistency" | Gerund naming provides better consistency (describes what skill does) |

### Token Savings

- 14 skills × ~11 tokens saved per prefix = ~154 fewer tokens in system prompt metadata
- System prompt metadata is loaded at EVERY conversation start (L1 loading level)

---

## Constitutional Files Updated

This ADR authorizes changes to the following LOCKED files:

### 1. `devforgeai/specs/context/coding-standards.md`
**Line 117:** `devforgeai-[phase]` → `[gerund-phrase]`

### 2. `devforgeai/specs/context/source-tree.md`
**Lines 834-841:** Pattern and examples updated to new convention

### 3. `devforgeai/specs/context/architecture-constraints.md`
**Lines 32-34:** Skill name examples updated (e.g., `devforgeai-development` → `implementing-stories`)

---

## Consequences

### Positive
- Full alignment with Anthropic Agent Skills best practices
- Shorter, more descriptive skill names
- Reduced system prompt token usage
- Clearer skill purpose from name alone

### Negative
- One-time migration effort (~76 story points total across all skills)
- Transition period with mixed naming (legacy in historical files)
- All cross-references must be updated (~169 files for MVP skill alone)

### Risks
- Missed references during migration → Mitigated by post-rename grep scan
- Breaking changes in operational `.claude/` → Mitigated by src/-first development, user-controlled sync

---

## References

- Anthropic Skills Best Practices: `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md`
- Anthropic Skills Overview: `.claude/skills/claude-code-terminal-expert/references/skills/overview.md`
- Migration Plan: `.claude/plans/idempotent-hatching-treasure.md`
- EPIC-065: `devforgeai/specs/Epics/EPIC-065-skill-gerund-naming-convention-migration.epic.md`
