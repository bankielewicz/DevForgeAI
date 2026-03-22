---
id: ADR-014
title: "Memory Directory Structure for Feedback Display and Learning"
status: APPROVED
created: 2026-02-02
updated: 2026-02-02
author: DevForgeAI Framework
source_epic: EPIC-052
---

# ADR-014: Memory Directory Structure for Feedback Display and Learning

## Status

**APPROVED** - 2026-02-02

## Context

EPIC-052 (Framework Feedback Display & Memory System) requires a structured approach to storing and retrieving framework learning artifacts. The current `.claude/memory/` directory serves as a progressive disclosure reference area containing:

- Skills, commands, and subagents reference documentation
- Constitution directory (mirrors of context files)
- Ad-hoc guides and best practices

However, the framework lacks structured storage for:

1. **Session data**: Individual Claude Code session artifacts (observations, decisions, outcomes)
2. **Learned patterns**: Cross-session insights extracted from feedback analysis
3. **Framework improvements**: Validated recommendations ready for implementation

### Current State

```
.claude/memory/
├── Constitution/           # Context file mirrors
├── skills-reference.md     # Reference documentation
├── commands-reference.md
├── subagents-reference.md
├── [various guides].md     # Ad-hoc documentation
```

### Problem Statement

The Framework Feedback Display & Memory System needs:
- A place to store session-level observations captured during `/dev` and `/qa` workflows
- A place to accumulate validated learnings that persist across context window boundaries
- Clear separation between volatile session data and consolidated framework knowledge

Without dedicated directories, session data would be scattered across `devforgeai/feedback/` without semantic organization, and learnings would have no designated home.

## Decision

**We will add two new subdirectories to `.claude/memory/` to support the multi-layer memory architecture:**

### New Directory Structure

```
.claude/memory/
├── Constitution/           # Existing - context file mirrors (UNCHANGED)
├── sessions/               # NEW - Session-level artifacts
│   └── {SESSION-ID}/       # Per-session directories
│       ├── observations.json
│       ├── decisions.json
│       └── outcomes.json
├── learning/               # NEW - Cross-session learnings
│   ├── patterns/           # Validated patterns
│   │   └── {pattern-id}.md
│   ├── improvements/       # Pending framework improvements
│   │   └── {improvement-id}.md
│   └── index.md            # Learning catalog
├── skills-reference.md     # Existing (UNCHANGED)
├── commands-reference.md   # Existing (UNCHANGED)
└── [other existing files]  # Existing (UNCHANGED)
```

### Directory Purpose

| Directory | Purpose | Lifecycle |
|-----------|---------|-----------|
| `sessions/` | Store raw session artifacts (observations, decisions, outcomes) | Ephemeral - pruned after consolidation |
| `learning/` | Store validated cross-session insights | Persistent - grows over time |
| `learning/patterns/` | Documented workflow patterns that improve outcomes | Permanent |
| `learning/improvements/` | Validated recommendations pending implementation | Until implemented |

### Design Rationale

1. **Multi-layer architecture**: Mirrors human learning (short-term session memory -> long-term learned patterns)
2. **Clear boundaries**: Session data is disposable, learnings are persistent
3. **Progressive disclosure**: Index files enable efficient discovery without loading all content
4. **Constitutional compliance**: Extends existing `.claude/memory/` pattern rather than creating new top-level directories

## Consequences

### Positive

- **Structured feedback storage**: Session observations have a canonical home
- **Cross-session learning**: Framework can accumulate and apply insights over time
- **Token efficiency**: Index-based discovery enables progressive disclosure
- **EPIC-052 enablement**: Unblocks implementation of feedback display and memory system
- **Auditability**: Clear separation between raw data and validated learnings

### Negative

- **Directory proliferation**: More subdirectories to maintain
- **Migration effort**: Existing feedback data may need reorganization
- **Index maintenance**: `learning/index.md` requires updates as patterns are added
- **Pruning policy**: Need to define session retention period

### Neutral

- **No runtime behavior change**: Existing workflows continue unchanged
- **Backward compatible**: No existing files moved or renamed
- **source-tree.md update required**: Constitutional change (this ADR authorizes)

## Alternatives Considered

### 1. Store Everything in `devforgeai/feedback/`

**Rejected because:**
- Mixes raw feedback with consolidated learnings
- No progressive disclosure - would need to load all feedback to find patterns
- `devforgeai/` is for specifications, not runtime memory

### 2. Create New Top-Level `memory/` Directory

**Rejected because:**
- Violates existing `.claude/memory/` pattern
- Would fragment memory-related files across two locations
- source-tree.md already establishes `.claude/memory/` as the memory location

### 3. Use `devforgeai/specs/research/` for Learnings

**Rejected because:**
- Research is for human-authored analysis documents
- Learnings are AI-generated insights from feedback analysis
- Different audiences and update frequencies

### 4. Flat File Structure (No Subdirectories)

**Rejected because:**
- Sessions would accumulate as hundreds of files
- No semantic grouping of patterns vs improvements
- Harder to implement retention policies

## Implementation Plan

### Phase 1: Directory Creation (STORY-339)

1. Create `sessions/` subdirectory with `.gitkeep`
2. Create `learning/` subdirectory structure
3. Create `learning/index.md` template
4. Update `devforgeai/specs/context/source-tree.md` (authorized by this ADR)

### Phase 2: Integration (EPIC-052 Stories)

1. Update `devforgeai-feedback` skill to write to `sessions/`
2. Create session-miner subagent to consolidate sessions -> learnings
3. Update framework-analyst to read from `learning/`
4. Implement session pruning policy (retain 30 days by default)

### Phase 3: Display (EPIC-052 Stories)

1. Create `/feedback-display` command reading from `learning/`
2. Add learning search to `/feedback-search`
3. Generate learning reports in QA workflow

## Validation Criteria

| Criterion | Measurement | Story |
|-----------|-------------|-------|
| Directories created | `sessions/` and `learning/` exist | STORY-339 |
| source-tree.md updated | New directories documented | STORY-339 |
| Session write path works | `/dev` writes to `sessions/` | EPIC-052 |
| Learning consolidation works | session-miner populates `learning/` | EPIC-052 |
| No regression | Existing memory files unchanged | STORY-339 |

## References

- [EPIC-052](../Epics/EPIC-052-framework-feedback-display-memory.epic.md) - Framework Feedback Display & Memory System
- [source-tree.md](../context/source-tree.md) - Current directory structure (lines 291-302)
- [devforgeai-feedback SKILL.md](../../../.claude/skills/devforgeai-feedback/SKILL.md) - Feedback skill
- [session-miner.md](../../../.claude/agents/session-miner.md) - Session mining subagent

## Decision Record

| Date | Action | By |
|------|--------|-----|
| 2026-02-02 | ADR created for STORY-339 | DevForgeAI |
| TBD | ADR approved | Framework Architect |
| TBD | source-tree.md updated | Framework Maintainer |
| TBD | Directories created | STORY-339 Implementation |
