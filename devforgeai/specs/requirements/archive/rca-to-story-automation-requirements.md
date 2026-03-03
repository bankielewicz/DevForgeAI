# RCA-to-Story Automation - Requirements Specification

**Version:** 1.0
**Date:** 2025-12-24
**Status:** Draft
**Author:** DevForgeAI Ideation
**Complexity Score:** 20/60 (Tier 2)
**Epic:** EPIC-032

---

## 1. Project Overview

### 1.1 Project Context
**Type:** Brownfield (DevForgeAI framework enhancement)
**Domain:** Developer tooling / Workflow automation
**Timeline:** 1-2 sprints (2-4 weeks)
**Team:** AI-assisted development (Claude)

### 1.2 Problem Statement

Currently, RCA recommendations require manual story creation, creating three pain points:

1. **Manual Effort:** Creating stories from RCA recommendations takes 15-30 minutes each, requiring copy-paste of recommendation details and reformatting for story template.

2. **Traceability Gap:** No automatic linkage between RCA recommendations and implementation stories. Developers must manually track which recommendations have been addressed.

3. **Process Inconsistency:** Epic→Story decomposition is automated via `/create-missing-stories`, but RCA→Story is entirely manual, creating an inconsistent developer experience.

### 1.3 Solution Overview

Create a `/create-stories-from-rca` slash command that:
1. Parses RCA documents from `devforgeai/RCA/`
2. Extracts recommendations by priority (CRITICAL/HIGH/MEDIUM/LOW)
3. Filters implementable items (>2 hour effort estimate)
4. Allows interactive selection of recommendations
5. Creates stories via batch `devforgeai-story-creation` skill invocation
6. Updates RCA document with story references

### 1.4 Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| Time to create stories from RCA | 15-30 min manual | <5 min automated |
| Traceability coverage | 0% (manual tracking) | 100% (auto-linking) |
| Story quality score | N/A | Equal to epic-generated stories |

---

## 2. User Roles & Personas

### 2.1 Primary Users

1. **Developer** - Uses DevForgeAI to build software projects
2. **Framework Maintainer** - Maintains DevForgeAI framework itself

### 2.2 User Personas

**Persona 1: Developer (David)**
- **Role:** Software developer using DevForgeAI for project development
- **Goals:** Quickly fix issues discovered during RCA, maintain high code quality
- **Needs:** Fast story creation, clear acceptance criteria, traceability
- **Pain Points:** Manual story creation is tedious, easy to forget recommendations

**Persona 2: Framework Maintainer (Maya)**
- **Role:** DevForgeAI framework contributor
- **Goals:** Improve framework reliability, prevent recurring issues
- **Needs:** Systematic tracking of framework improvements, RCA documentation
- **Pain Points:** RCA recommendations pile up without implementation tracking

---

## 3. Functional Requirements

### 3.1 User Stories

**US-001: Parse RCA Document**
```
As a developer,
I want to parse an RCA document by ID,
So that I can extract all recommendations for story creation.
```

**US-002: Filter Recommendations by Effort**
```
As a developer,
I want recommendations filtered to only show items >2 hours effort,
So that quick fixes remain in the RCA and only substantial work becomes stories.
```

**US-003: Select Recommendations Interactively**
```
As a developer,
I want to interactively select which recommendations to convert,
So that I maintain control over story creation.
```

**US-004: Create Stories in Batch**
```
As a developer,
I want stories created via batch mode,
So that they match the quality of epic-generated stories.
```

**US-005: Link Stories to RCA**
```
As a developer,
I want the RCA document updated with story references,
So that I can trace recommendations to implementation.
```

**US-006: Validate Against Context Files**
```
As a developer,
I want created stories to comply with constitutional context files,
So that they follow tech-stack and architecture constraints.
```

### 3.2 Feature Requirements

#### Feature 1.1: RCA Document Parsing

**FR-1.1.1:** Command shall accept RCA ID as argument (e.g., `RCA-022`)
**FR-1.1.2:** Command shall locate RCA file in `devforgeai/RCA/` directory
**FR-1.1.3:** Parser shall extract YAML-style frontmatter (date, severity, status)
**FR-1.1.4:** Parser shall extract all `### REC-N:` sections
**FR-1.1.5:** Parser shall extract priority from section header (CRITICAL/HIGH/MEDIUM/LOW)
**FR-1.1.6:** Parser shall extract effort estimate from `**Effort Estimate:**` line

#### Feature 1.2: Interactive Recommendation Selection

**FR-1.2.1:** Command shall display summary table of parsed recommendations
**FR-1.2.2:** Table shall include: REC ID, Priority, Title, Effort Estimate
**FR-1.2.3:** Command shall use AskUserQuestion with multiSelect: true
**FR-1.2.4:** User may select all, none, or subset of recommendations

#### Feature 1.3: Batch Story Creation

**FR-1.3.1:** Command shall set batch context markers per devforgeai-story-creation spec
**FR-1.3.2:** Markers shall include: Story ID, Epic ID, Feature Name, Priority, Points, Sprint, Batch Mode
**FR-1.3.3:** Command shall invoke `Skill(command="devforgeai-story-creation")` for each selection
**FR-1.3.4:** Command shall report success/failure per story

#### Feature 1.4: RCA-Story Linking

**FR-1.4.1:** Command shall update RCA Implementation Checklist section
**FR-1.4.2:** Update shall add story reference (e.g., `- [x] See STORY-XXX`)
**FR-1.4.3:** Command shall update recommendation section with story reference

#### Feature 1.5: Command Shell

**FR-1.5.1:** Command file shall be created at `.claude/commands/create-stories-from-rca.md`
**FR-1.5.2:** Command shall follow lean orchestration pattern (<15K characters)
**FR-1.5.3:** Command shall include help text accessible via `--help` flag
**FR-1.5.4:** Command shall handle invalid RCA ID with clear error message

---

## 4. Data Requirements

### 4.1 Data Model

#### Entity: RCA Document
```yaml
path: devforgeai/RCA/RCA-{NNN}-{slug}.md
id: RCA-{NNN}
title: string
severity: CRITICAL | HIGH | MEDIUM | LOW
status: OPEN | IN_PROGRESS | RESOLVED
date: YYYY-MM-DD
recommendations: Recommendation[]
```

#### Entity: Recommendation
```yaml
id: REC-{N}
priority: CRITICAL | HIGH | MEDIUM | LOW
title: string
description: string
effort_hours: number
effort_points: number (optional)
success_criteria: string[]
implementation_details: string
```

#### Entity: Story (output)
```yaml
id: STORY-{NNN}
title: string (from recommendation title)
epic: EPIC-{NNN} (optional)
type: feature | bugfix | refactor | documentation
priority: High | Medium | Low
points: number
sprint: string
source_rca: RCA-{NNN}
source_recommendation: REC-{N}
```

### 4.2 Data Constraints

- RCA ID format: `RCA-` followed by 3 digits (`RCA-001` to `RCA-999`)
- Recommendation ID format: `REC-` followed by 1-2 digits
- Effort threshold: Only recommendations with effort >2 hours converted to stories
- Priority mapping: RCA CRITICAL/HIGH → Story High, RCA MEDIUM → Story Medium, RCA LOW → Story Low

---

## 5. Integration Requirements

### 5.1 Internal Integrations

| Integration | Direction | Purpose |
|-------------|-----------|---------|
| devforgeai-story-creation skill | Outbound | Create stories via batch mode |
| devforgeai/RCA/*.md | Inbound | Read RCA documents |
| devforgeai/specs/Stories/*.md | Outbound | Write story files |

### 5.2 Skill Integration Contract

**Batch Context Markers (per devforgeai-story-creation SKILL.md):**
```markdown
**Story ID:** STORY-{NNN}
**Epic ID:** EPIC-{NNN} (optional)
**Feature Number:** 1.{N}
**Feature Name:** {Recommendation title}
**Feature Description:** {Recommendation description}
**Priority:** {Priority}
**Points:** {Points}
**Type:** {Story type}
**Sprint:** {Sprint}
**Batch Mode:** true
**Batch Index:** {N}
**Batch Total:** {Total}
**Created From:** /create-stories-from-rca
**Source RCA:** RCA-{NNN}
**Source Recommendation:** REC-{N}
```

---

## 6. Non-Functional Requirements

### 6.1 Architecture

| Requirement | Specification |
|-------------|---------------|
| Pattern | Lean orchestration (command → skill delegation) |
| Command size | <15,000 characters (per lean orchestration standard) |
| Business logic | Zero in command, all in skill |
| Dependencies | Only devforgeai-story-creation skill |

### 6.2 Performance

| Metric | Target |
|--------|--------|
| RCA parse time | <2 seconds |
| Story creation (per story) | <30 seconds |
| Batch of 5 stories | <3 minutes |

### 6.3 Compliance

| Requirement | Specification |
|-------------|---------------|
| tech-stack.md | Stories comply with allowed technologies |
| architecture-constraints.md | Stories comply with architecture patterns |
| source-tree.md | Command placed in `.claude/commands/` |
| coding-standards.md | Markdown format, YAML frontmatter |

### 6.4 Error Handling

| Error Scenario | Handling |
|----------------|----------|
| Invalid RCA ID format | Display format help, list valid RCAs |
| RCA file not found | Display error, suggest `/rca` to create |
| No recommendations found | Display message, exit gracefully |
| Parse failure | Best-effort + AskUserQuestion to clarify |
| Story creation failure | Continue to next, report failures at end |

---

## 7. Complexity Assessment

**Total Score:** 20/60
**Architecture Tier:** Tier 2 (Moderate Application)

### 7.1 Score Breakdown

| Dimension | Score | Details |
|-----------|-------|---------|
| Functional Complexity | 8/20 | 2 roles, 3 entities, 1 integration, linear workflow |
| Technical Complexity | 5/20 | Low data volume, single user, batch processing |
| Team/Organizational | 3/10 | Solo development, no distribution |
| Non-Functional | 4/10 | Lean orchestration + context compliance |

### 7.2 Architecture Recommendation

- **Pattern:** Lean orchestration
- **Layers:** Command → Skill
- **Technology:** Markdown files, regex parsing
- **Deployment:** Claude Code terminal

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: FEASIBLE

| Factor | Assessment |
|--------|------------|
| Technology maturity | Proven (markdown parsing, skill invocation) |
| Integration complexity | Simple (single skill integration) |
| Data complexity | Simple (file-based, no DB) |

### 8.2 Business Feasibility: FEASIBLE

| Factor | Assessment |
|--------|------------|
| Budget | Zero external costs |
| Timeline | 1-2 sprints (achievable) |
| Value | Immediate ROI on first use |

### 8.3 Resource Feasibility: FEASIBLE

| Factor | Assessment |
|--------|------------|
| Team capacity | AI-assisted (Claude) |
| Skill gaps | None (reuses existing patterns) |
| Dependencies | All available |

### 8.4 Risk Register

| Risk | Probability | Impact | Severity | Mitigation |
|------|-------------|--------|----------|------------|
| RCA format variance | Medium | Low | LOW | Best-effort parsing + interactive recovery |
| Skill interface changes | Low | Medium | LOW | Follow stable batch mode pattern |

### 8.5 Overall Feasibility: FEASIBLE

**Recommendation:** Proceed with implementation

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints

- Command must remain <15K characters (lean orchestration)
- Must use existing devforgeai-story-creation skill (no duplication)
- Must comply with 6 constitutional context files

### 9.2 Business Constraints

- Feature must integrate with existing RCA workflow
- No breaking changes to RCA document format

### 9.3 Assumptions (Require Validation)

| Assumption | Validation Method |
|------------|-------------------|
| RCAs follow standard format with `### REC-N:` headers | Analyze existing RCAs |
| Effort estimates are in consistent format | Parse 5 sample RCAs |
| Users prefer interactive selection over auto-create-all | User feedback |

---

## 10. Epic Breakdown

### 10.1 Implementation Roadmap

**Sprint 1:** Features 1.1, 1.2, 1.5 (parsing, selection, command shell)
**Sprint 2:** Features 1.3, 1.4 (batch creation, linking)

### 10.2 Story Summary

| Feature | Stories | Points |
|---------|---------|--------|
| 1.1 RCA Parsing | 3 | 5-8 |
| 1.2 Interactive Selection | 2 | 3-5 |
| 1.3 Batch Creation | 2 | 5-8 |
| 1.4 RCA-Story Linking | 2 | 3-5 |
| 1.5 Command Shell | 3 | 5-8 |
| **Total** | **12** | **21-34** |

---

## 11. Next Steps

1. **Story Creation:** Run `/create-story` for each feature
2. **Sprint Planning:** Assign stories to Sprint 14/15
3. **Implementation:** Start TDD workflow via `/dev STORY-XXX`

---

## Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| RCA | Root Cause Analysis - systematic investigation of framework issues |
| Recommendation | Proposed solution within an RCA document |
| Lean Orchestration | Pattern where commands delegate to skills, contain <15K chars |
| Batch Mode | Story creation mode that skips interactive questions |

### B. References

- `/create-missing-stories` command (similar pattern)
- `devforgeai-story-creation` skill (batch mode documentation)
- RCA document structure (devforgeai/RCA/README.md)
- Lean orchestration pattern (CLAUDE.md)

### C. Open Questions

1. Should the command support creating an epic from multiple RCAs?
2. Should there be an `--auto` flag for non-interactive mode?
3. Should the command support filtering by RCA status (OPEN only)?

---

**Document Created:** 2025-12-24
**Created By:** DevForgeAI Ideation Skill
**Epic Reference:** EPIC-032
