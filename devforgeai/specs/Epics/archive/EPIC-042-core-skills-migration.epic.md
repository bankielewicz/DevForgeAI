---
id: EPIC-042
title: Core Skills Migration
business-value: Migrate all 17 non-compliant DevForgeAI skills to Agent Skills specification, enabling version tracking, tool security, and automated validation
status: Planning
priority: High
complexity-score: 26
architecture-tier: Tier 2
created: 2026-01-18
estimated-points: 51
target-sprints: 4-6
brainstorm-source: BRAINSTORM-004
dependencies:
  - EPIC-041
---

# Core Skills Migration

## Business Goal

Migrate all 17 non-compliant DevForgeAI skills to full Agent Skills specification compliance, enabling consistent version tracking, tool security enforcement, and automated validation across the framework.

**Success Metrics:**
- 17/17 skills pass skills-ref validate
- All skills have metadata.version field (framework-aligned versioning)
- All skills have allowed-tools section
- Zero workflow disruption during migration

## Features

### Feature 1: Core Workflow Skills Migration
**Description:** Migrate the three most critical workflow skills that form the TDD backbone.
**User Stories (high-level):**
1. Migrate devforgeai-development to Agent Skills spec
2. Migrate devforgeai-qa to Agent Skills spec
3. Migrate devforgeai-orchestration to Agent Skills spec

**Estimated Effort:** Medium (9 points - 3 per skill)

### Feature 2: Lifecycle Skills Migration
**Description:** Migrate skills that handle the early phases of development lifecycle.
**User Stories (high-level):**
1. Migrate devforgeai-ideation to Agent Skills spec
2. Migrate designing-systems to Agent Skills spec
3. Migrate devforgeai-story-creation to Agent Skills spec

**Estimated Effort:** Medium (9 points - 3 per skill)

### Feature 3: Release & Documentation Skills Migration
**Description:** Migrate skills that handle release and documentation phases.
**User Stories (high-level):**
1. Migrate devforgeai-release to Agent Skills spec
2. Migrate devforgeai-documentation to Agent Skills spec
3. Migrate devforgeai-feedback to Agent Skills spec

**Estimated Effort:** Medium (9 points - 3 per skill)

### Feature 4: Utility Skills Migration
**Description:** Migrate utility skills for specialized functions.
**User Stories (high-level):**
1. Migrate devforgeai-rca to Agent Skills spec
2. Migrate devforgeai-ui-generator to Agent Skills spec
3. Migrate devforgeai-brainstorming to Agent Skills spec

**Estimated Effort:** Medium (9 points - 3 per skill)

### Feature 5: Meta Skills Migration
**Description:** Migrate skills that create or manage other skills/agents.
**User Stories (high-level):**
1. Migrate skill-creator to Agent Skills spec
2. Migrate devforgeai-subagent-creation to Agent Skills spec
3. Migrate devforgeai-github-actions to Agent Skills spec

**Estimated Effort:** Medium (9 points - 3 per skill)

### Feature 6: Integration Skills Migration
**Description:** Migrate skills for external integrations.
**User Stories (high-level):**
1. Migrate devforgeai-mcp-cli-converter to Agent Skills spec
2. Migrate internet-sleuth-integration to Agent Skills spec

**Estimated Effort:** Small (6 points - 3 per skill)

## Requirements Summary

### Functional Requirements
- Each skill must have valid YAML frontmatter with Agent Skills fields
- Each skill must pass skills-ref validate
- Each skill must have allowed-tools defined
- Version numbers must align with framework version

### Migration Template
For each skill migration:
1. Add/update YAML frontmatter with Agent Skills fields
2. Add metadata.version (framework-aligned)
3. Add allowed-tools section
4. Add any missing required fields per spec
5. Run skills-ref validate
6. Verify skill functionality unchanged

### Data Model
**Entities:**
- Skill files: 17 SKILL.md files to update
- Metadata: YAML frontmatter extensions

### Non-Functional Requirements

**Backward Compatibility:**
- Full backward compatibility required
- Old workflows continue functioning during migration

**Validation:**
- skills-ref validate MUST pass (FAIL on non-compliance)

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Sequential file updates with validation gate
- Strategy: One skill per commit, validate before proceeding

**Migration Order:**
1. Core workflow (dev, qa, orchestration) - highest usage
2. Lifecycle (ideation, architecture, story-creation)
3. Release & docs (release, documentation, feedback)
4. Utility (rca, ui-generator, brainstorming)
5. Meta (skill-creator, subagent-creation, github-actions)
6. Integration (mcp-cli-converter, internet-sleuth)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Merge conflicts during migration | MEDIUM | Migrate one skill at a time, commit frequently |
| Skill functionality regression | MEDIUM | Test each skill after migration |
| Token budget increase from metadata | LOW | Measure before/after, optimize if needed |

## Dependencies

**Prerequisites:**
- EPIC-041: Agent Skills Foundation (template + validation tooling)

**Dependents:**
- EPIC-043: Security & Quality Enhancement (requires migrated skills)
- EPIC-044: Discovery & Advanced Features (requires migrated skills)

## Next Steps

1. **Complete EPIC-041:** Foundation must be in place first
2. **Start with core workflow:** devforgeai-development first
3. **Validate each migration:** skills-ref validate per skill
4. **Track progress:** Update this epic as skills migrate

---

## Migration Tracking

| Skill | Status | Version | validated |
|-------|--------|---------|-----------|
| claude-code-terminal-expert | ✅ DONE | 3.0.0 | Yes |
| devforgeai-development | ⏳ Pending | - | - |
| devforgeai-qa | ⏳ Pending | - | - |
| devforgeai-orchestration | ⏳ Pending | - | - |
| devforgeai-ideation | ⏳ Pending | - | - |
| designing-systems | ⏳ Pending | - | - |
| devforgeai-story-creation | ⏳ Pending | - | - |
| devforgeai-release | ⏳ Pending | - | - |
| devforgeai-documentation | ⏳ Pending | - | - |
| devforgeai-feedback | ⏳ Pending | - | - |
| devforgeai-rca | ⏳ Pending | - | - |
| devforgeai-ui-generator | ⏳ Pending | - | - |
| devforgeai-brainstorming | ⏳ Pending | - | - |
| skill-creator | ⏳ Pending | - | - |
| devforgeai-subagent-creation | ⏳ Pending | - | - |
| devforgeai-github-actions | ⏳ Pending | - | - |
| devforgeai-mcp-cli-converter | ⏳ Pending | - | - |
| internet-sleuth-integration | ⏳ Pending | - | - |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-18 | Created from BRAINSTORM-004 ideation | DevForgeAI |
