---
id: BRAINSTORM-003
title: "DevForgeAI Project Manager Skill"
created_at: 2025-12-30T18:30:00Z
status: COMPLETE
confidence_level: HIGH
session_duration: "45 minutes"
questions_answered: 18
market_research: true
research_report: "RESEARCH-001-pm-ai-dev-market-analysis.md"
---

# BRAINSTORM-003: DevForgeAI Project Manager Skill

## Executive Summary

Design and create a **devforgeai-project-manager** skill to apply project management best practices to DevForgeAI spec-driven framework projects. The skill addresses critical gaps in project organization, scope management, enhancement tracking, and release coordination.

---

## Problem Statement

**"DevForgeAI users** experience **lack of project visibility, scope creep, and lost enhancements** because **the framework was designed for individual story workflows without project-level aggregation**, resulting in **reduced productivity, delivery delays, quality issues, and lost opportunities**."

---

## Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Type | Goals | Concerns |
|-------------|------|-------|----------|
| Solo Developers | Primary User | Track progress, prevent scope creep | No visibility, enhancements lost |
| Development Teams | Primary User | Coordinate releases, document decisions | Stories pile up without releases |
| Project Managers | Primary User | All goals - visibility + coordination | Need aggregated project view |

### Stakeholder Goals
1. Track progress and velocity
2. Prevent scope creep
3. Coordinate releases
4. Document decisions

### Key Concerns
- No visibility into overall progress
- Stories pile up without releases
- Enhancement requests get lost

### Conflicts
- None significant - stakeholders are aligned

---

## Root Cause Analysis (5 Whys)

| Level | Why | Answer |
|-------|-----|--------|
| 1 | Why no visibility? | No dashboard, data scattered, manual tracking |
| 2 | Why scattered data? | Designed for individual story workflows |
| 3 | Why individual focus? | Initial TDD quality priority, organic growth |
| 4 | Why no PM features? | Higher priorities, out of scope, complexity |
| 5 | **Root cause** | Framework matured + scaling needs + differentiation opportunity |

---

## Current State

**PM Process Today:** No process exists - PM is ad-hoc or not done at all

### Pain Points (Ranked by Impact)
1. No project health overview - can't see if on track
2. Sprint/release coordination is manual
3. Scope creep happens silently
4. Enhancement ideas get lost
5. Release planning is guesswork
6. Documentation gaps accumulate

### Business Impact
- 💰 Reduced productivity (manual coordination)
- 💰 Delivery delays (poor planning)
- 💰 Quality issues (rushed work)
- 💰 Lost opportunities (ideas never captured)

---

## Market Research Findings

**Research Report:** `devforgeai/specs/research/shared/RESEARCH-001-pm-ai-dev-market-analysis.md`

### Three Critical Market Insights

1. **Context-First PM is Replacing External Tools**
   - GitHub Copilot Spaces, Cursor IDE, Claude Code all building native PM
   - DevForgeAI's document-first approach aligns with 2025 trends

2. **Specification-Driven Development is Mainstream (2025)**
   - GitHub Spec Kit (GA Sept 2025) validates spec-first methodology
   - DevForgeAI already has this pattern - competitive advantage

3. **Model Context Protocol (MCP) is Future Integration Standard**
   - Anthropic's standard enables tool integration without lock-in
   - Consider for future PM tool bridges

### 5 Market Gaps (DevForgeAI Opportunities)
1. Integrated spec → code execution
2. Automatic PM tool synchronization
3. **Scope boundary enforcement** ← Priority
4. **Quality assurance for AI code** ← Existing /qa
5. **AI-assisted release management** ← Priority

### DevForgeAI Competitive Advantages
- Document-first development (matches Spec Kit pattern)
- TDD mandatory (matches quality standards)
- Phase gates (workflow enforcement)
- ADR pattern (decisions logged)
- Context files (scope boundaries already exist)

---

## Opportunities Identified

### Ideal State Vision
1. Single command for full project status
2. Automatic release planning
3. Real-time scope tracking
4. Integrated backlog management

### Technology Approaches
- **Event-driven hooks** (user-preferred approach)
- Must work within **Claude Code terminal**
- No external API dependencies (Max paid plan)
- Minimal external dependencies

### Adjacent Opportunities (V2+)
- Sprint retrospectives
- Dependency tracking
- Technical debt management

---

## Constraints

| Constraint Type | Value | Impact |
|-----------------|-------|--------|
| **Budget** | Internal time only | No external purchases; use existing tools |
| **Timeline** | No hard deadline | Quality-focused development |
| **Technical** | Existing tools + new subagents | Self-contained; minimal dependencies |
| **Process** | Follow DevForgeAI patterns | Integrate with /dev, /qa, /release |
| **Platform** | Claude Code terminal | No external dependencies; Max plan |

### Critical Constraint
Must use existing DevForgeAI tools where possible, can add new subagents/skills, minimal external dependencies. Solution must work entirely within Claude Code terminal.

---

## Hypotheses to Validate

### Hypothesis 1: Scope Creep Detection (SHOULD HAVE)
**IF** we validate story implementations against scope boundaries during /dev workflow, **THEN** we will reduce scope creep and prevent enhancement requests from being lost.

- Success criteria: Flag out-of-scope changes before commit
- Validation: Measure ratio of flagged vs. accepted changes
- Risk: False positives frustrate users

### Hypothesis 2: Enhancement Backlog Capture (MUST HAVE)
**IF** we add a `/pm-enhancement` command to capture ideas during development, **THEN** good ideas won't be lost and can be triaged for future sprints.

- Success criteria: Enhancements captured and retrievable
- Validation: Enhancement-to-story conversion rate
- Risk: Creates another backlog that gets ignored

### Hypothesis 3: Release Coordination (SHOULD HAVE)
**IF** we track story dependencies and QA status in a release-planning view, **THEN** users can make confident decisions about what to include in releases.

- Success criteria: Clear release readiness dashboard
- Validation: Reduced "surprise" issues during release
- Risk: Over-engineering if releases are simple

### Hypothesis 4: Project Dashboard (WON'T HAVE v1)
**IF** we create a `/pm-status` command that aggregates data from epics, sprints, stories, and QA reports, **THEN** users will have visibility into overall project progress.

- Deferred to v2 - not critical for initial version

---

## Prioritization (MoSCoW)

| Capability | Priority | Impact | Effort | Order |
|------------|----------|--------|--------|-------|
| Enhancement Backlog Capture | 🔴 MUST HAVE | HIGH | LOW | 1st |
| Scope Creep Detection | 🟡 SHOULD HAVE | MEDIUM | LOW | 2nd |
| Release Coordination | 🟡 SHOULD HAVE | HIGH | HIGH | 3rd |
| Project Dashboard | ⚪ WON'T HAVE (v1) | MEDIUM | MEDIUM | Defer |

### Recommended Implementation Order
1. **Enhancement Capture** - Quick win, must have
2. **Scope Detection** - Can integrate with /dev workflow
3. **Release Coordination** - Requires more design work

---

## Proposed Solution Outline

### Skill Structure: `devforgeai-project-manager`

**Location:** `.claude/skills/devforgeai-project-manager/`

**Core Commands:**
- `/pm-enhance` - Capture enhancement ideas during development
- `/pm-scope-check` - Validate implementation against story scope
- `/pm-release-ready` - Check release readiness for QA-approved stories

**Supporting Commands (V1):**
- `/pm-backlog` - View enhancement backlog
- `/pm-triage` - Prioritize enhancements for future sprints

**Data Storage:**
- `devforgeai/specs/enhancements/` - Enhancement backlog
- `devforgeai/specs/releases/` - Release planning documents

**Integration Points:**
- Post-dev hook: Auto-check scope after /dev completes
- Post-qa hook: Update release readiness after QA approval
- Enhancement capture: Callable from any workflow

### Workflow Integration

```
/dev workflow
    ↓
Post-dev hook → /pm-scope-check (validates scope)
    ↓
If out-of-scope → /pm-enhance (captures as enhancement)
    ↓
/qa workflow
    ↓
Post-qa hook → /pm-release-ready (updates readiness)
    ↓
/release workflow → Uses readiness data
```

---

## Must-Have Capabilities (V1)

1. **Enhancement Capture**
   - `/pm-enhance [description]` - Capture idea with context
   - Store in `devforgeai/specs/enhancements/ENHANCE-{NNN}.md`
   - Track source story, capture date, priority (TBD)
   - List/search/triage capabilities

2. **Scope Detection** (integrate with /dev)
   - Read story scope boundaries from story file
   - Detect out-of-scope changes during implementation
   - Flag for user decision: implement now OR capture as enhancement
   - Non-blocking (user can override)

3. **Release Readiness Tracking**
   - Aggregate QA-approved stories
   - Show dependencies between stories
   - Identify blocking issues
   - Generate release notes draft from story summaries

---

## Success Criteria

### V1 Success
- [ ] Enhancement ideas captured and not lost (>90% capture rate)
- [ ] Scope creep flagged before commit (>80% detection)
- [ ] Release decisions informed by data (clear readiness view)
- [ ] No disruption to existing /dev, /qa, /release workflows

### Long-term Success
- [ ] Reduced scope creep in story implementations
- [ ] Enhancements converted to stories (>50% triage rate)
- [ ] Faster release decisions (reduced planning time)
- [ ] Improved documentation (auto-generated release notes)

---

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scope detection false positives | HIGH | Make non-blocking; user can override |
| Enhancement backlog ignored | MEDIUM | Add triage reminders; connect to sprint planning |
| Over-engineering for simple projects | MEDIUM | Make features optional; graceful degradation |
| Integration complexity | LOW | Use existing hook patterns; follow DevForgeAI conventions |

---

## Next Steps

1. **Run `/ideate`** - Transform this brainstorm into formal epic/requirements
2. **Create architecture** - Define skill structure and data models
3. **Implement MVP** - Enhancement capture first (quick win)
4. **Iterate** - Add scope detection, then release coordination

---

## Supporting Documents

- **Market Research:** `devforgeai/specs/research/shared/RESEARCH-001-pm-ai-dev-market-analysis.md`
- **Research Summary:** `devforgeai/specs/research/shared/RESEARCH-001-SUMMARY.md`
- **Market Gaps:** `devforgeai/specs/research/shared/RESEARCH-001-MARKET-GAPS.md`
- **Existing Patterns:** `.claude/skills/devforgeai-orchestration/` (workflow integration)

---

## Session Metadata

- **Session ID:** BRAINSTORM-003
- **Created:** 2025-12-30
- **Duration:** ~45 minutes
- **Questions Answered:** 18
- **Research Included:** Yes (internet-sleuth subagent)
- **Confidence Level:** HIGH
- **Ready for Ideation:** YES

---

**Recommended Command:**
```
/ideate
```

The brainstorm document will be automatically detected and pre-populated into the ideation workflow.
