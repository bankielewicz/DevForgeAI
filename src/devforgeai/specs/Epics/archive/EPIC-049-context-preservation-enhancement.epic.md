---
id: EPIC-049
title: Context Preservation Enhancement
status: Planning
priority: P1
start_date: 2026-01-20
target_date: 2026-03-03
total_points: 32
created: 2026-01-20
updated: 2026-01-20
source_research:
  - RESEARCH-003-ai-framework-document-handoff-patterns
  - RESEARCH-004-anthropic-prompt-engineering-long-documents
  - SYNTHESIS-context-preservation-specification
source_plan: /home/bryan/.claude/plans/rosy-tinkering-minsky.md
---

# Epic: Context Preservation Enhancement

## Business Goal

**Eliminate 75% context loss at workflow handoff boundaries** by implementing the BMAD "Artifacts Travel With Work" pattern and Anthropic's Inverted Pyramid document structure.

Currently, when brainstorm documents flow to ideation → epic → story:
- Only YAML frontmatter is consumed (12 fields)
- 7 markdown body sections are ignored (75% context loss)
- WHY decisions were made is lost
- Stakeholder goals and hypotheses are abandoned

This epic implements proven patterns from AWS Kiro, GitHub Spec Kit, BMAD-METHOD, and Anthropic's official documentation to achieve **100% context traceability**.

## Success Metrics

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| **Context Traceability** | ~25% | 100% | Stories trace "As a..." to brainstorm persona |
| **Decision Coverage** | 0% | 80% | Epic features have documented alternatives |
| **Token Efficiency** | N/A | <40K/workflow | Token tracking in phase state |
| **Phase Compliance** | ~70% | >95% | Phase skip detection |
| **Context Consumption** | 25% | 100% | Brainstorm body sections extracted |

## Scope

### Overview

This epic implements a comprehensive context preservation system across the DevForgeAI workflow pipeline. It introduces provenance tags, enhanced data mapping, schema validation, and context preservation hooks to ensure business rationale flows from brainstorm through to implementation.

### Features

1. **Provenance XML Section (Story Template v2.7)**
   - Description: Add `<provenance>` XML section to story template with origin, decision, stakeholder, and hypothesis elements
   - User Value: Stories self-document WHY they exist and trace decisions to source documents
   - Estimated Points: 3 pts
   - Research Source: BMAD "Artifacts Travel With Work" pattern

2. **Enhanced Brainstorm Data Mapping**
   - Description: Extend brainstorm-data-mapping.md to extract markdown body sections (stakeholder analysis, 5 Whys, hypotheses, impact-effort matrix)
   - User Value: 75% → 100% context consumption from brainstorm documents
   - Estimated Points: 5 pts
   - Research Source: Gap analysis of current implementation

3. **Inverted Pyramid Skill Structure**
   - Description: Restructure devforgeai-development SKILL.md with methodology at top, queries at bottom
   - User Value: 30% improvement in phase compliance (Anthropic research)
   - Estimated Points: 3 pts
   - Research Source: Anthropic prompt engineering documentation

4. **Context Preservation Validator Subagent**
   - Description: New subagent that validates context linkage at workflow transitions (/create-epic, /create-story, /dev Phase 01)
   - User Value: Automated detection of context loss before it propagates
   - Estimated Points: 5 pts
   - Research Source: Windsurf hooks pattern

5. **Schema Validation for Skill Outputs**
   - Description: Add Pydantic/JSON schema validation at skill handoff boundaries (brainstorm → ideation → epic → story)
   - User Value: Prevent format drift and ensure data completeness
   - Estimated Points: 5 pts
   - Research Source: Industry standard (2026)

6. **Compaction Checkpoint at 70%**
   - Description: Implement context compaction checkpoint at 70% token capacity (140K/200K) instead of waiting for 95%
   - User Value: Prevent context overflow and preserve state across session restarts
   - Estimated Points: 3 pts
   - Research Source: Anthropic prompt engineering documentation

7. **Context Preservation Hooks (/create-epic)**
   - Description: Add pre/post hooks to /create-epic to validate context linkage to source brainstorm
   - User Value: Ensure epics preserve business rationale from brainstorm
   - Estimated Points: 3 pts
   - Research Source: Windsurf autonomous memory pattern

8. **Context Preservation Hooks (/create-story)**
   - Description: Add pre/post hooks to /create-story to validate context linkage to epic and brainstorm
   - User Value: Ensure stories preserve full context chain
   - Estimated Points: 3 pts
   - Research Source: Windsurf autonomous memory pattern

9. **Memory Files for Cross-Session State**
   - Description: Update memory file format to persist workflow state (progress, decisions, blockers) across session restarts
   - User Value: 39% performance improvement (Anthropic research) + session recovery
   - Estimated Points: 2 pts
   - Research Source: Anthropic prompt engineering documentation

### Out of Scope

- EARS notation for acceptance criteria (lower priority, defer to future epic)
- Grounding in quotes requirement (can be added later)
- Full skill restructuring beyond devforgeai-development (start with one skill, extend pattern)
- Automated context compaction/summarization AI

## Target Sprints

**Estimated Duration:** 3 sprints / 4-6 weeks

**Sprint Breakdown:**

### Sprint 1: Foundation (11 pts) - CRITICAL + HIGH priorities
- **STORY-296**: Provenance XML Section - 3 pts ✅ Created
- **STORY-297**: Enhanced Brainstorm Data Mapping - 5 pts ✅ Created
- **STORY-298**: Inverted Pyramid Skill Structure - 3 pts ✅ Created
- **Milestone**: Core context preservation infrastructure in place

### Sprint 2: Validation (13 pts) - HIGH priorities
- **STORY-299**: Context Preservation Validator Subagent - 5 pts ✅ Created
- **STORY-301**: Schema Validation for Skill Outputs - 5 pts ✅ Created
- **STORY-J**: Compaction Checkpoint at 70% - 3 pts (pending)
- **Milestone**: Automated validation and protection against context loss

### Sprint 3: Integration (8 pts) - MEDIUM priorities
- **STORY-300**: Context Preservation Hooks (/create-epic) - 3 pts ✅ Created
- **STORY-302**: Context Preservation Hooks (/create-story) - 3 pts ✅ Created
- **STORY-303**: Memory Files for Cross-Session State - 2 pts ✅ Created
- **Milestone**: Full integration across workflow pipeline

## Dependencies

### External Dependencies
- None - all changes are internal to DevForgeAI framework

### Internal Dependencies
- **EPIC-046** (AC Compliance Verification): Should complete first as it establishes XML AC patterns that provenance tags will follow
- **Story Template v2.6**: Current template must be in place (already exists)

### Blocking Issues
- None identified

## Stakeholders

- **Product Owner:** DevForgeAI Framework Users
- **Tech Lead:** AI Agent (Claude)
- **Domain Expert:** Research findings from BMAD, Kiro, Anthropic

## Requirements

### Functional Requirements

#### User Story 1: Provenance Tags
```
As a DevForgeAI user,
I want stories to contain embedded provenance tags,
So that I can trace WHY a feature exists back to the original business problem.
```

**Acceptance Criteria:**
- [ ] Story template v2.7 includes `<provenance>` XML section
- [ ] Provenance contains: origin (document, quote, line reference), decision (selected, rejected, trade-off), stakeholder (role, goal, quote), hypothesis (id, validation, success criteria)
- [ ] Provenance tags render correctly in story files
- [ ] /create-story skill populates provenance from brainstorm/epic chain

#### User Story 2: Enhanced Brainstorm Extraction
```
As a DevForgeAI user,
I want ideation skill to consume ALL brainstorm content,
So that stakeholder analysis, root cause analysis, and hypotheses inform requirements.
```

**Acceptance Criteria:**
- [ ] brainstorm-data-mapping.md extracts all 7 markdown body sections
- [ ] Stakeholder Analysis table parsed into structured data
- [ ] Root Cause Analysis (5 Whys) extracted
- [ ] Hypothesis Register parsed with validation criteria
- [ ] Impact-Effort Matrix quadrants extracted
- [ ] Backward compatible with existing brainstorm files

#### User Story 3: Context Validation
```
As a DevForgeAI user,
I want automated validation of context linkage,
So that context loss is detected before it propagates through the workflow.
```

**Acceptance Criteria:**
- [ ] context-preservation-validator subagent created
- [ ] Validates epic → brainstorm linkage
- [ ] Validates story → epic → brainstorm chain
- [ ] Reports missing context with specific recommendations
- [ ] Integrated with /create-epic, /create-story, /dev Phase 01

### Non-Functional Requirements (NFRs)

#### Performance
- **Token Overhead:** Provenance tags add <10% token cost per story
- **Validation Speed:** Context validation completes in <5 seconds
- **Compaction Trigger:** 70% capacity detection accurate within 5%

#### Usability
- **Backward Compatibility:** All changes backward compatible with existing documents
- **Progressive Enhancement:** Features work with or without source brainstorm

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate Complexity**
- **Score:** 22/60 points
- **Rationale:** Framework-internal changes, no external dependencies, well-defined scope from research

### Recommended Architecture Pattern
**Documentation-as-Code** with XML-structured semantic sections

**Justification:** Follows BMAD principle that documentation is the source of truth, code is derivative. XML tags leverage Claude's fine-tuned attention to structured content.

### Files to Modify

| File | Change | Priority |
|------|--------|----------|
| `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` | Add `<provenance>` section (v2.7) | CRITICAL |
| `.claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md` | Extract markdown body | HIGH |
| `.claude/skills/devforgeai-development/SKILL.md` | Inverted pyramid structure | HIGH |
| `.claude/agents/context-preservation-validator.md` | New subagent | HIGH |
| `.claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml` | New schema file | HIGH |
| `devforgeai/specs/context/architecture-constraints.md` | Add context preservation rules | MEDIUM |

### Technology Constraints
- Must use Claude Code native tools (Read, Write, Edit, Glob, Grep)
- Must follow Markdown documentation format
- Must maintain <1000 line skill limit
- Must use XML for structured content (per coding-standards.md)

## Risks & Constraints

### Technical Risks

**Risk 1: Token Overhead**
- **Description:** Provenance tags may significantly increase story token cost
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Measured at <10% overhead in research; use progressive disclosure if needed

**Risk 2: Extraction Accuracy**
- **Description:** Markdown body extraction may fail on non-standard brainstorm formats
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Graceful fallback to YAML-only extraction; validation warnings

### Constraints

**Constraint 1: Framework-Agnostic**
- **Description:** All solutions must work within Claude Code Terminal capabilities
- **Impact:** Cannot use external Python libraries for parsing
- **Mitigation:** Use Claude's native understanding of markdown/XML

**Constraint 2: Backward Compatibility**
- **Description:** Must not break existing stories, brainstorms, or workflows
- **Impact:** Cannot change existing field names or required sections
- **Mitigation:** All new sections are additive; existing documents valid without provenance

## Assumptions

1. **Brainstorm template is stable**: Template structure (7 sections) will not change during implementation
2. **XML attention is effective**: Claude's fine-tuning for XML tags will improve context preservation
3. **70% compaction is sufficient**: Research suggests 70% trigger prevents overflow; may need adjustment
4. **Schema validation is feasible**: Markdown-based validation achievable without external libraries

## Research Foundation

This epic is grounded in extensive research conducted 2026-01-20:

### RESEARCH-003: AI Framework Document Handoff Patterns
- **Frameworks Analyzed:** AWS Kiro, GitHub Spec Kit, BMAD-METHOD, Cursor, Windsurf
- **Key Finding:** "Artifacts Travel With Work" - documentation travels with work items
- **Applied To:** Provenance tags, context preservation hooks

### RESEARCH-004: Anthropic Prompt Engineering
- **Source:** Official Anthropic documentation
- **Key Findings:** Inverted pyramid (30% improvement), compaction at 70%, memory files (39% improvement)
- **Applied To:** Skill structure, compaction checkpoints, memory files

### SYNTHESIS Document
- **Location:** `devforgeai/specs/research/SYNTHESIS-context-preservation-specification.md`
- **Contents:** Unified specification with prioritized recommendations

## Next Steps

### Immediate Actions
1. **Create Sprint 1 Stories:** `/create-story` for STORY-A, STORY-B, STORY-C
2. **Begin Implementation:** `/dev` starting with STORY-A (provenance tags)
3. **Update Plan Checkpoint:** Mark CHECKPOINT 5 (Design) complete

### Pre-Development Checklist
- [x] Research complete (RESEARCH-003, RESEARCH-004, SYNTHESIS)
- [x] Epic created with feature breakdown
- [x] Sprint 1 stories created in devforgeai/specs/Stories/ (STORY-296, STORY-297)
- [x] Story dependencies documented (none for foundation stories)
- [ ] Implementation order confirmed

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (merge to main)

## Notes

- **Plan File:** Full context preservation plan at `/home/bryan/.claude/plans/rosy-tinkering-minsky.md`
- **Recovery Prompt:** Session recovery instructions at `/home/bryan/.claude/plans/RESUME-rosy-tinkering-minsky.md`
- **Open Question:** Should EARS notation be added in Sprint 3 or deferred to future epic? (Currently deferred)

---

**Epic Status:**
- **In Progress** - Sprint 1 stories created, ready for development

**Created Stories:**
| Story ID | Title | Points | Sprint | Status |
|----------|-------|--------|--------|--------|
| STORY-296 | Provenance XML Section | 3 | Sprint-1 | Backlog |
| STORY-297 | Enhanced Brainstorm Data Mapping | 5 | Sprint-1 | Backlog |
| STORY-298 | Inverted Pyramid Skill Structure | 3 | Sprint-1 | Backlog |
| STORY-299 | Context Preservation Validator Subagent | 5 | Sprint-2 | Backlog |
| STORY-300 | Context Preservation Hooks (/create-epic) | 3 | Sprint-3 | Backlog |
| STORY-301 | Schema Validation for Skill Outputs | 5 | Sprint-2 | Backlog |
| STORY-302 | Context Preservation Hooks (/create-story) | 3 | Sprint-3 | Backlog |
| STORY-303 | Memory Files for Cross-Session State | 2 | Sprint-3 | Backlog |

**Last Updated:** 2026-01-20 by Claude (via /create-story)
