---
# =============================================================================
# REQUIREMENTS SPECIFICATION
# =============================================================================
# Schema Version: 1.0 (STORY-435)
# Purpose: Structured requirements for cross-session AI consumption
#
# IMPORTANT: This YAML frontmatter contains ALL structured data.
# The markdown body below is for human readability only - do not duplicate data.

schema_version: "1.0"
document_id: "REQ-XXX"
title: "[Project/Feature Title]"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
status: "Draft"

# DECISIONS (locked choices with excluded options)
decisions:
  - id: "DR-1"
    domain: "[domain]"
    decision: "[The chosen approach - no hedging language]"
    rejected:
      - option: "[Alternative not chosen]"
        reason: "[Why this was rejected]"
    rationale: "[Why this choice was made]"
    locked: true

#
# SCOPE (explicit boundaries with deferral targets)
#
scope:
  in:
    - "[Feature/requirement included]"
  out:
    - item: "[Feature/requirement excluded]"
      deferral_target: "[Phase 2|Post-MVP|Never]"

#
# SUCCESS CRITERIA (quantified, measurable)
#
success_criteria:
  - id: "SC-1"
    metric: "[What to measure]"
    target: "[Quantified target with numbers/comparators]"
    measurement: "[How to verify]"

#
# CONSTRAINTS (technical, business, regulatory)
#
constraints:
  - type: "technical"
    constraint: "[Constraint statement]"
    source: "[Reference/source]"

#
# NON-FUNCTIONAL REQUIREMENTS
#
nfrs:
  - category: "performance"
    requirement: "[NFR statement]"
    priority: "High"

#
# STAKEHOLDERS  (lightweight -- retained for backward compatibility)
#
stakeholders:
  - role: "[Role/Title]"
    goals:
      - "[Goal 1]"
    decision_authority:
      - "[Decision area]"

#
# RISK REGISTER  (Inception PM-plan section)
# Carried from brainstorm risk_analysis.risks[] OR elicited in Phase 03.
#
risks:
  - id: "RISK-001"
    description: "[Risk statement]"
    likelihood: "Medium"
    impact: "High"
    severity: "High"
    mitigation: "[Planned mitigation or contingency]"
    owner: "[Accountable stakeholder]"

#
# MILESTONE ROADMAP  (Inception PM-plan section)
# Carried from brainstorm release_roadmap OR derived from MoSCoW + scope.future.
# BOUNDED: no schedule durations, no resource loading, no budget breakdown.
#
roadmap:
  - phase: "MVP"
    items:
      - "[Requirement ID or capability name]"
    dependencies: []
    rationale: "[Why these items form this milestone]"
  - phase: "Release 2"
    items:
      - "[Requirement ID or capability name]"
    dependencies:
      - "MVP"
    rationale: "[Why this milestone follows]"

#
# STAKEHOLDER REGISTER  (Inception PM-plan section -- PM depth)
# Carried from brainstorm stakeholders.registry[], merged with ideation personas.
#
stakeholder_register:
  - id: "STK-001"
    name_or_role: "[Stakeholder name or role]"
    category: "Primary"
    influence: "High"
    interest: "High"
    raci: "Accountable"
    goals:
      - "[Goal]"
    concerns:
      - "[Concern]"

#
# ASSUMPTIONS  (Inception PM-plan section)
# Merges brainstorm Phase-08 assumptions with ideation-elicited assumptions.
#
assumptions:
  - id: "ASMP-001"
    statement: "[The assumption]"
    validation_method: "[How it will be validated]"
    source: "[brainstorm:BRAINSTORM-XXX | ideation:IDEATION-XXX]"

#
# IDEA BACKLOG REFERENCE  (Inception PM-plan section)
# Points to the standalone living idea-backlog artifact (DEF-NNN items).
#
idea_backlog_ref: "devforgeai/specs/ideation/[project-name]-idea-backlog.md"

#
# PROVENANCE
#
source_brainstorm: "BRAINSTORM-XXX"

---

# Requirements: [Project/Feature Title]

## Overview

This document is the **Inception Project-Management plan** produced by the
spec-driven-ideation (Project Management) phase. It captures the structured
requirements plus the PM-plan registers — scope baseline, milestone roadmap,
risk register, stakeholder register, assumptions, and a reference to the idea
backlog. All data is stored in the YAML frontmatter above for cross-session AI
consumption; the generated output SHOULD validate against
`references/ideation-output.schema.json` v1.0.

## Reading This Document

- **Decisions:** See `decisions` in frontmatter - locked choices with explicit excluded options
- **Scope Baseline:** See `scope.in` (included) and `scope.out` (excluded with deferral targets)
- **Success Criteria:** See `success_criteria` - quantified metrics with targets
- **Prioritized Requirements:** See `functional_requirements` - with MoSCoW priority
- **Constraints:** See `constraints` - technical, business, regulatory limits
- **NFRs:** See `nfrs` - performance, security, scalability requirements
- **Risk Register:** See `risks` - RISK-NNN entries with likelihood/impact/mitigation
- **Milestone Roadmap:** See `roadmap` - phased releases with build order and dependencies
- **Stakeholder Register:** See `stakeholder_register` - influence, interest, RACI
- **Assumptions:** See `assumptions` - ASMP-NNN entries with validation methods
- **Idea Backlog:** See `idea_backlog_ref` - path to the standalone living idea-backlog file

## Risk Register

RISK-NNN entries are stored in the `risks` frontmatter array. When a brainstorm
fed this ideation session, risks were carried verbatim from the brainstorm risk
analysis; otherwise they were elicited during Phase 03. An empty register is
valid and is reported as a validation warning, not a failure.

## Milestone Roadmap

The `roadmap` frontmatter array sequences delivery into phased milestones
(MVP / Release 2 / Future), each carrying its included items and build-order
dependencies. It carries **no** schedule durations, resource loading, or budget
breakdown — those are out of scope for the inception PM plan and are produced by
the downstream architecture skills.

## Stakeholder Register

The `stakeholder_register` frontmatter array records stakeholders with their
influence, interest, and RACI / decision authority — sourced from the brainstorm
stakeholder registry when present and merged with ideation's own personas.

## Assumptions

The `assumptions` frontmatter array (ASMP-NNN) records assumptions that, if
invalidated, would become downstream defects. Each carries a validation method.

## Idea Backlog

`idea_backlog_ref` points to the standalone living idea-backlog artifact
(`devforgeai/specs/ideation/[project-name]-idea-backlog.md`). That file
accumulates ideas raised but intentionally not in the current MVP (DEF-NNN
items) and is appended — never overwritten — by every `/ideate` session.

## Next Steps

1. Review locked decisions in frontmatter
2. Validate scope baseline and milestone roadmap
3. Review the risk register and assumptions
4. Proceed to `/create-solution-architecture` with this requirements document

---

*Generated by spec-driven-ideation skill (Project Management phase) | Schema v1.0*
