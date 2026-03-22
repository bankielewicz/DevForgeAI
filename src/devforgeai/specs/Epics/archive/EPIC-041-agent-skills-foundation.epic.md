---
id: EPIC-041
title: Agent Skills Foundation
business-value: Establish baseline infrastructure for Agent Skills specification compliance, enabling standardized skill development and automated validation
status: Planning
priority: High
complexity-score: 26
architecture-tier: Tier 2
created: 2026-01-18
estimated-points: 13
target-sprints: 1-2
brainstorm-source: BRAINSTORM-004
dependencies: []
---

# Agent Skills Foundation

## Business Goal

Establish the foundational infrastructure for Agent Skills specification compliance, enabling all future skill development to be spec-compliant from creation and providing automated validation tooling.

**Success Metrics:**
- ADR-011 documented and approved
- skill-creator template generates Agent Skills compliant skills
- skills-ref validate integrated into /qa Phase 1
- Compliance audit script can identify non-compliant skills

## Features

### Feature 1: ADR-011 Agent Skills Adoption
**Description:** Create Architecture Decision Record documenting the decision to adopt Agent Skills specification (agentskills.io) for all DevForgeAI skills.
**User Stories (high-level):**
1. Create ADR-011 with decision context, options considered, and rationale
2. Document migration strategy (phased approach)
3. Document backward compatibility guarantees

**Estimated Effort:** Small (3 points)

### Feature 2: skill-creator Template Update
**Description:** Update the skill-creator skill template to generate Agent Skills compliant skills with all required metadata fields.
**User Stories (high-level):**
1. Add metadata.version field to template
2. Add allowed-tools section to template
3. Add all Agent Skills spec required fields
4. Update skill-creator SKILL.md to generate compliant output

**Estimated Effort:** Medium (5 points)

### Feature 3: QA Validation Integration
**Description:** Integrate skills-ref validate into /qa Phase 1 preflight validation to automatically check skill compliance.
**User Stories (high-level):**
1. Add skills-ref validate call to /qa preflight
2. Configure FAIL behavior for non-compliance (per user requirement)
3. Display compliance status in QA report

**Estimated Effort:** Small (3 points)

### Feature 4: Compliance Audit Script
**Description:** Create a command to audit all skills and report compliance status.
**User Stories (high-level):**
1. Create /audit-skills command
2. Scan all 18 skills for Agent Skills compliance
3. Generate compliance report with pass/fail per skill

**Estimated Effort:** Small (2 points)

## Requirements Summary

### Functional Requirements
- ADR creation following DevForgeAI ADR template
- Template update with Agent Skills metadata fields
- skills-ref CLI integration (external tool)
- Compliance reporting with detailed status per skill

### Data Model
**Entities:**
- ADR-011: Architecture Decision Record for Agent Skills adoption
- Skill metadata: Extended YAML frontmatter with version, allowed-tools

**Relationships:**
- ADR-011 → All skill migrations (governance)
- skill-creator template → New skills (generation)

### Integration Points
1. skills-ref CLI: External validation tool (invoked via Bash)
2. /qa workflow: Validation integration point

### Non-Functional Requirements

**Performance:**
- skills-ref validate should complete in <5 seconds per skill

**Backward Compatibility:**
- Old skills continue to work during migration
- No workflow disruption for users

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Modular documentation updates
- Layers: SKILL.md → references/
- Database: N/A (file-based)
- Deployment: In-place updates to framework files

**Technology Recommendations:**
- Markdown with YAML frontmatter
- skills-ref CLI for validation
- Bash for automation scripts

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| skills-ref CLI breaking changes | MEDIUM | Pin version, test before upgrade |
| Template changes break existing workflow | LOW | Thorough testing before release |

## Dependencies

**Prerequisites:**
- None (foundation epic)

**Dependents:**
- EPIC-042: Core Skills Migration (depends on template + validation)
- EPIC-043: Security & Quality Enhancement (depends on migration)
- EPIC-044: Discovery & Advanced Features (depends on migration)

## Next Steps

1. **Create ADR-011:** Document Agent Skills adoption decision
2. **Update skill-creator:** Add Agent Skills template fields
3. **Integrate validation:** Add skills-ref to /qa workflow
4. **Audit existing skills:** Identify compliance gaps

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-18 | Created from BRAINSTORM-004 ideation | DevForgeAI |
