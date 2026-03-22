---
id: EPIC-044
title: Discovery & Advanced Features
business-value: Enhance skill discoverability through category registry and add advanced safety controls for sensitive operations
status: Planning
priority: Low
complexity-score: 26
architecture-tier: Tier 2
created: 2026-01-18
estimated-points: 8
target-sprints: 1-2
brainstorm-source: BRAINSTORM-004
dependencies:
  - EPIC-042
  - EPIC-043
---

# Discovery & Advanced Features

## Business Goal

Enhance framework usability by improving skill discoverability through categorization and add advanced safety controls for sensitive operations like releases.

**Success Metrics:**
- Skill category registry created and populated
- disable-model-invocation added to devforgeai-release
- Compliance dashboard shows status across all skills
- Discovery time for skills reduced (qualitative)

## Features

### Feature 1: Skill Category Registry
**Description:** Create a registry that organizes skills by category for easier discovery.
**User Stories (high-level):**
1. Define skill categories (lifecycle, workflow, utility, meta, integration)
2. Create category registry file or metadata
3. Update skill discoverability in CLAUDE.md
4. Add category navigation to documentation

**Estimated Effort:** Small (3 points)

### Feature 2: disable-model-invocation Safety Flag
**Description:** Add the Agent Skills spec disable-model-invocation flag to devforgeai-release to prevent accidental autonomous releases.
**User Stories (high-level):**
1. Add disable-model-invocation: true to devforgeai-release
2. Document rationale (release requires explicit user action)
3. Test that model cannot auto-invoke release

**Estimated Effort:** Small (2 points)

### Feature 3: Compliance Dashboard
**Description:** Create a view showing Agent Skills compliance status across all skills.
**User Stories (high-level):**
1. Create /skills-status command or view
2. Show compliance status per skill (pass/fail)
3. Show version numbers
4. Show allowed-tools summary

**Estimated Effort:** Small (3 points)

## Requirements Summary

### Functional Requirements
- Category taxonomy for skills
- Safety flag for dangerous operations
- Compliance visibility across framework

### Skill Categories (Proposed)

| Category | Skills | Description |
|----------|--------|-------------|
| Lifecycle | ideation, architecture, story-creation | Early development phases |
| Workflow | development, qa, orchestration, release | Core TDD workflow |
| Documentation | documentation, feedback, rca | Supporting documentation |
| Utility | ui-generator, brainstorming | Specialized utilities |
| Meta | skill-creator, subagent-creation, github-actions | Framework generation |
| Integration | mcp-cli-converter, internet-sleuth | External integrations |
| Expert | claude-code-terminal-expert | Knowledge base |

### Non-Functional Requirements

**Usability:**
- Categories should be intuitive
- Navigation should be fast

**Safety:**
- disable-model-invocation must prevent autonomous release

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Metadata extension + documentation update
- Strategy: Incremental enhancement

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Category taxonomy doesn't fit user mental model | LOW | Validate with users |
| disable-model-invocation blocks legitimate use | LOW | Document explicitly |

## Dependencies

**Prerequisites:**
- EPIC-042: Core Skills Migration
- EPIC-043: Security & Quality Enhancement

**Dependents:**
- None (final epic in sequence)

## Next Steps

1. **Complete EPIC-042 and EPIC-043:** Prerequisites must finish first
2. **Define categories:** Finalize taxonomy
3. **Add safety flags:** Update devforgeai-release
4. **Build dashboard:** Create compliance view

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-18 | Created from BRAINSTORM-004 ideation | DevForgeAI |
