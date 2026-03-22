# BRAINSTORM-004: Agent Skills Specification Compliance

**Session ID:** BRAINSTORM-004
**Created:** 2026-01-18
**Status:** COMPLETE
**Confidence:** HIGH
**Next Step:** `/ideate` or `/create-epic`

---

## Executive Summary

This brainstorm explores enhancing the DevForgeAI framework with full Agent Skills specification compliance (agentskills.io), addressing maintenance burden and feature requests through standardized skill metadata, automated validation, and improved discoverability.

---

## Problem Statement

> *"DevForgeAI framework users experience maintenance burden due to inconsistent skill metadata and lack of validation, resulting in version drift, security blind spots, and QA gaps that slow development velocity, cause quality issues, limit framework adoption, and constrain ecosystem growth."*

**Root Cause:** Skills were created before Agent Skills specification (Dec 2025); no retroactive compliance process exists.

---

## Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| **Framework Owner** | Full spec compliance, cross-platform portability, security | Migration effort, backward compatibility |
| **Power Users** | Fast discovery, version visibility, predictable boundaries | Workflow disruption, learning curve |

### Secondary Stakeholders

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| Claude Code Team | Ecosystem standardization | DevForgeAI setting good precedent |
| Contributors | Clear guidelines, automated validation | YAML complexity, merge conflicts |
| QA Engineers | Automated validation, clear pass/fail | Integration complexity |

### Key Conflicts

| Conflict | Resolution |
|----------|------------|
| Migration disruption | Phased rollout with backward compatibility |
| Validation strictness | Two-tier: WARN for dev, FAIL for release |
| Extensions vs Portability | Metadata segregation (portable vs extended) |

---

## Opportunity Analysis

### Identified Enhancements (8 total)

| # | Enhancement | User Priority | MoSCoW |
|---|-------------|---------------|--------|
| 1 | Standardize all 18 skills to Agent Skills spec | HIGH | MUST HAVE |
| 2 | Add `allowed-tools` security enforcement | HIGH | SHOULD HAVE |
| 3 | Integrate `skills-ref validate` into /qa | HIGH | MUST HAVE |
| 4 | Skill version tracking via `metadata.version` | HIGH | MUST HAVE |
| 5 | Progressive disclosure optimization | MEDIUM | SHOULD HAVE |
| 6 | `disable-model-invocation` for dangerous skills | MEDIUM | COULD HAVE |
| 7 | Skill category registry | MEDIUM | COULD HAVE |
| 8 | Cross-platform skill portability | LOW | WON'T HAVE |

### Ideal State

- Full Agent Skills spec compliance for all 18 skills
- Self-documenting skills with complete metadata
- Automated validation in QA pipeline
- Version tracking for all skills

---

## Constraint Analysis

| Category | Constraint |
|----------|------------|
| Timeline | No hard deadline (flexible) |
| Resources | Claude Code only (via /dev workflow) |
| Technical | Must work in Claude Code Terminal |
| Technical | Must maintain backward compatibility |
| Technical | Open to enhancing DevForgeAI CLI |
| Rollout | Phased migration (incremental) |

---

## Hypothesis Validation

| ID | Hypothesis | Risk if Wrong | Validation Approach |
|----|------------|---------------|---------------------|
| H1 | `skills-ref validate` works with DevForgeAI | Migration blocked | Test on claude-code-terminal-expert ✅ |
| H2 | Phased migration won't break workflows | User disruption | Test with old skills during migration |
| H3 | `allowed-tools` doesn't break functionality | Feature regression | Add to one skill, test all functions |
| H4 | Version tracking adds minimal overhead | Performance issues | Measure token usage before/after |

**H1 Validated:** claude-code-terminal-expert successfully updated to v3.0.0 with full Agent Skills compliance.

---

## Prioritized Implementation Roadmap

### Phase 1: Foundation (Quick Wins)

| Story | Enhancement | Effort | Dependencies |
|-------|-------------|--------|--------------|
| S1 | Add version tracking to skill-creator template | LOW | None |
| S2 | Integrate skills-ref validate into /qa Phase 1 | LOW | S1 |
| S3 | Create ADR-011: Agent Skills Spec Adoption | LOW | None |

### Phase 2: Core Migration (Major Project)

| Story | Enhancement | Effort | Dependencies |
|-------|-------------|--------|--------------|
| S4 | Update devforgeai-development to Agent Skills spec | MEDIUM | S1, S2 |
| S5 | Update devforgeai-qa to Agent Skills spec | MEDIUM | S4 |
| S6 | Update devforgeai-orchestration to Agent Skills spec | MEDIUM | S5 |
| S7-S18 | Update remaining 15 skills | MEDIUM each | S6 |

### Phase 3: Security & Quality (Should Have)

| Story | Enhancement | Effort | Dependencies |
|-------|-------------|--------|--------------|
| S19 | Add allowed-tools to all migrated skills | LOW | S4-S18 |
| S20 | Audit and enforce progressive disclosure | MEDIUM | S19 |

### Phase 4: Discovery & Safety (Could Have)

| Story | Enhancement | Effort | Dependencies |
|-------|-------------|--------|--------------|
| S21 | Create skill category registry | LOW | S18 |
| S22 | Add disable-model-invocation to devforgeai-release | LOW | S18 |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Skills compliant | 18/18 | `skills-ref validate` passes |
| QA integration | 100% | skills-ref in /qa Phase 1 |
| Version tracking | 18/18 | All skills have metadata.version |
| allowed-tools coverage | 18/18 | All skills have tool whitelist |
| Token efficiency | <5% increase | Compare before/after metadata |

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| skills-ref incompatibility | LOW | HIGH | Already validated on one skill |
| Workflow disruption | MEDIUM | MEDIUM | Phased migration, backward compat |
| Contributor confusion | MEDIUM | LOW | Update skill-creator template first |
| Merge conflicts | HIGH | LOW | Migrate one skill at a time |

---

## Artifacts to Create

### Required (via /ideate)

1. **EPIC-041:** Agent Skills Specification Compliance
2. **ADR-011:** Agent Skills Spec Adoption Decision
3. **22 Stories:** As outlined in roadmap above

### Reference Updates

1. Update skill-creator skill with Agent Skills template
2. Update coding-standards.md with skill metadata requirements
3. Add skills-ref to dependencies.md (optional dependency)

---

## Session Metadata

```yaml
session:
  id: BRAINSTORM-004
  topic: "Agent Skills Specification Compliance"
  duration: ~25 minutes
  phases_completed: 7/7
  questions_asked: 12
  stakeholders_identified: 10
  opportunities_mapped: 8
  hypotheses_formed: 4

discovery_summary:
  problem_validated: true
  root_cause: "Skills predate Agent Skills spec; no compliance process"
  solution_approach: "Phased migration with backward compatibility"

outputs:
  brainstorm_document: "devforgeai/specs/brainstorms/BRAINSTORM-004-agent-skills-compliance.brainstorm.md"
  next_command: "/ideate" or "/create-epic EPIC-041"
```

---

## Next Steps

1. **Review this document** for accuracy and completeness
2. **Run `/ideate`** to transform into formal requirements
   - This brainstorm will be auto-detected
   - Key inputs will be pre-populated
3. **Or run `/create-epic EPIC-041`** to create epic directly
4. **After epic creation:** `/create-sprint` to plan implementation

---

**Recommended Command:**
```
/create-epic EPIC-041 Agent Skills Specification Compliance
```
