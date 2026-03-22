---
id: EPIC-067
title: "/ideate Command & devforgeai-ideation Skill Anthropic Conformance Remediation"
status: Cancelled
superseded_by: EPIC-069
cancellation_reason: "Superseded by EPIC-069 which covers 28 findings from comprehensive 10-category audit against renamed discovering-requirements skill"
start_date: 2026-02-17
target_date: 2026-03-14
total_points: 25
completed_points: 0
created: 2026-02-17
owner: DevForgeAI Framework Team
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_analysis: devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md
source_brainstorm: "N/A - originated from ad-hoc conformance analysis (see source_analysis)"
---

# Epic: /ideate Command & devforgeai-ideation Skill Anthropic Conformance Remediation

## Business Goal

Remediate the 21 findings identified in the Ideation Anthropic Conformance Analysis to bring the `/ideate` slash command and `devforgeai-ideation` skill into full alignment with Anthropic's official Agent Skills specification (v1.0) and prompt engineering best practices.

**Problem:** The conformance analysis (completed 2026-02-17) scored the ideation ecosystem across 9 categories and found: 1 category non-conformant (Role Prompting & Examples), 6 categories partially conformant, and only 2 fully conformant. Key gaps include no role prompt, no multishot examples, no XML tags for structure or handoffs, and 114 lines of error-handling business logic in the command file.

**Value:** A conformant skill improves Claude's discovery accuracy, reduces context window waste, improves inter-phase data flow reliability, and ensures the ideation entry point — the first skill new users encounter — follows the platform vendor's official guidance.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md` (9/9 categories complete, 21 findings)

## Success Metrics

- **Metric 1:** All 5 High-severity findings resolved and verified
- **Metric 2:** All 11 Medium-severity findings resolved or documented as deferred with ADR justification
- **Metric 3:** Conformance analysis re-run shows 0 Non-Conformant categories, ≤2 Partially Conformant categories
- **Metric 4:** No regression in skill functionality — all existing ideation workflows continue to work

**Measurement Plan:**
- Tracked via story completion in `devforgeai/specs/Stories/`
- Re-run conformance analysis after Feature 1-3 (Sprint 1-2) to validate progress
- Final re-analysis after all features complete

## Scope

### In Scope

7 features implementing 21 findings across 3 sprints. Each feature groups related findings from the conformance analysis for efficient implementation.

**Primary files modified:**
- `.claude/skills/devforgeai-ideation/SKILL.md` (372 lines)
- `.claude/commands/ideate.md` (567 lines)
- `.claude/skills/devforgeai-ideation/references/` (28 files, ~13,345 lines)
- New files: `references/examples.md`, `references/command-error-handling.md`, `assets/templates/epic-example-completed.md`

### Features

1. **Feature 1: Role Prompting & Multishot Examples** (Category 8 remediation)
   - Description: Add role prompt to SKILL.md, create multishot examples reference file, create completed epic template example
   - Findings: 8.1 (High), 8.2 (High), 8.3 (Medium)
   - User Value: Dramatically improves output quality for discovery questions, requirements elicitation, epic decomposition, and complexity scoring — Anthropic's guidance shows role prompting is "the most powerful way to use system prompts"
   - Estimated Points: 5
   - Files Created: `references/examples.md`, `assets/templates/epic-example-completed.md`
   - Files Modified: `SKILL.md` (add Role section after execution model)

2. **Feature 2: XML Tag Adoption** (Categories 5, 7, 9 remediation)
   - Description: Introduce XML tags for instruction structure, context markers, and inter-phase handoffs
   - Findings: 5.1 (High), 5.2 (Medium), 7.1 (Medium), 9.3 (Medium)
   - User Value: Improves Claude's parsing accuracy, makes command-skill handoffs reliable, and enables structured inter-phase data flow — Anthropic says XML tags "help Claude parse your prompts more accurately"
   - Estimated Points: 5
   - Files Modified: `SKILL.md` (XML tags for execution model, phase outputs), `ideate.md` (XML context markers)

3. **Feature 3: Command-Skill Separation** (Category 9 remediation)
   - Description: Move error handling business logic from command to skill reference, simplify brainstorm parsing in command
   - Findings: 9.1 (High), 9.2 (Medium)
   - User Value: Reduces command from 567 to ~460 lines, properly separates orchestration from implementation, follows "commands orchestrate, skills implement" principle
   - Estimated Points: 3
   - Files Created: `references/command-error-handling.md`
   - Files Modified: `ideate.md` (remove error handling section, simplify Phase 0)

4. **Feature 4: YAML Frontmatter Compliance** (Category 1 remediation)
   - Description: Fix allowed-tools format, remove invalid tools, standardize model field
   - Findings: 1.1 (Medium), 1.2 (Medium), 1.3 (Low), 1.4 (Medium), 1.5 (High)
   - User Value: Ensures YAML frontmatter passes Agent Skills spec validation (`skills-ref validate`), resolves model field inconsistency
   - Estimated Points: 2
   - Files Modified: `SKILL.md` (lines 2-16), `ideate.md` (lines 4-6)

5. **Feature 5: Progressive Disclosure & Token Optimization** (Categories 3, 4 remediation)
   - Description: Add table of contents to 14 reference files exceeding 100 lines, remove redundant Core Philosophy section
   - Findings: 3.2 (Medium), 4.1 (Low)
   - User Value: Improves Claude's ability to navigate large reference files, saves ~120 tokens per invocation — Anthropic says "For reference files longer than 100 lines, include a table of contents at the top"
   - Estimated Points: 5
   - Files Modified: 14 reference files (add TOC), `SKILL.md` (remove Core Philosophy section)

6. **Feature 6: Workflow Enhancement** (Categories 6, 7 remediation)
   - Description: Add checklist tracking instruction to Success Criteria, add chain-of-thought guidance for complexity scoring
   - Findings: 6.1 (Medium), 7.2 (Medium)
   - User Value: Ensures Claude actively tracks completion during execution, improves accuracy and auditability of complexity scoring
   - Estimated Points: 2
   - Files Modified: `SKILL.md` (Success Criteria section), `references/complexity-assessment-workflow.md`

7. **Feature 7: Naming Convention Alignment** (Category 2 remediation)
   - Description: Evaluate gerund naming, remove vendor prefix, add trigger phrases to description
   - Findings: 2.1 (Low), 2.2 (Low), 2.3 (Low)
   - User Value: Aligns with Anthropic's naming best practice (gerund form) for improved discoverability — may require ADR if coding-standards.md locks current naming
   - Estimated Points: 3
   - Files Modified: `SKILL.md` (name, description), directory rename if approved, reference updates across codebase

### Out of Scope

- Analyzing other DevForgeAI skills (devforgeai-development, devforgeai-qa, etc.)
- Modifying constitutional context files (requires ADR process)
- Splitting devforgeai-ideation into multiple skills (Finding 3.3 — design observation, not actionable)
- Re-running the 9-category conformance analysis (separate task after remediation)

## Target Sprints

### Sprint 1: High-Impact Fixes

**Goal:** Resolve the highest-impact findings — role prompting, examples, and YAML frontmatter compliance
**Estimated Points:** 7
**Features:**
- Feature 1: Role Prompting & Multishot Examples (5 points)
- Feature 4: YAML Frontmatter Compliance (2 points)

**Rationale:** Feature 1 addresses the only Non-Conformant category (Category 8). Feature 4 is quick-win frontmatter fixes. Together they resolve 8 of 21 findings including 3 of 5 High-severity items.

---

### Sprint 2: Structural Changes

**Goal:** Restructure command-skill boundary and introduce XML tags
**Estimated Points:** 8
**Features:**
- Feature 2: XML Tag Adoption (5 points)
- Feature 3: Command-Skill Separation (3 points)

**Rationale:** Both features modify the same files (SKILL.md and ideate.md) and are structurally related. Feature 3 reduces command size before Feature 2 adds XML tags. Together they resolve 6 findings including 2 High-severity items.

**Dependencies:** Feature 3 should complete before Feature 2 (command size reduction first, then XML introduction).

---

### Sprint 3: Polish & Alignment

**Goal:** Complete remaining medium/low findings — TOC additions, workflow improvements, naming
**Estimated Points:** 10
**Features:**
- Feature 5: Progressive Disclosure & Token Optimization (5 points)
- Feature 6: Workflow Enhancement (2 points)
- Feature 7: Naming Convention Alignment (3 points)

**Rationale:** These are lower-priority improvements that polish the skill after structural changes are complete. Feature 7 (naming) may require ADR approval and is deliberately last.

**Dependencies:** No hard dependencies on Sprint 1-2, but naming changes (Feature 7) should be last since they affect directory paths.

---

## Dependencies

### Internal Dependencies

- [x] **Dependency 1:** Conformance analysis complete
  - **Status:** Complete (2026-02-17)
  - **Location:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`

- [x] **Dependency 2:** Anthropic Skills reference files available
  - **Status:** Complete
  - **Location:** `.claude/skills/claude-code-terminal-expert/references/skills/` and `references/prompt-engineering/`

- [x] **Dependency 3:** devforgeai-ideation skill ecosystem exists
  - **Status:** Complete
  - **Location:** `.claude/skills/devforgeai-ideation/`

### External Dependencies
- None. All changes are internal to the skill ecosystem.

### Blocking Issues

- **Potential Blocker:** Feature 7 (naming) may conflict with `devforgeai/specs/context/coding-standards.md` naming convention (`devforgeai-[phase]` pattern). If locked, requires ADR before rename.
  - **Mitigation:** Feature 7 is in Sprint 3 (last). If ADR is rejected, findings 2.1 and 2.2 are documented as "deferred — context file constraint" with no impact on overall conformance.

### Story Dependencies

```
Sprint 1:  F1 (Role/Examples) ─────────────────────┐
           F4 (YAML Frontmatter) ──── (parallel) ──┤
                                                    │
Sprint 2:  F3 (Command-Skill) ←── F1,F4            │
           F2 (XML Tags) ←── F3                     │
                                                    │
Sprint 3:  F5 (TOC/Tokens) ←── F2       (parallel) │
           F6 (Workflow) ←── F2          (parallel) │
           F7 (Naming) ←── F5,F6        (last)     │
```

## Risks & Mitigation

### Risk 1: XML tag changes break context marker detection
- **Probability:** Medium
- **Impact:** High — skill would fail to detect command context
- **Mitigation:** Feature 2 updates BOTH command (context marker emission) and skill (context marker detection) simultaneously. Test with `/ideate test idea` after each change.
- **Contingency:** Revert to markdown-bold markers if XML parsing proves unreliable in conversation context

### Risk 2: Command error handling extraction breaks error reporting
- **Probability:** Low
- **Impact:** Medium — errors would display incorrectly
- **Mitigation:** Feature 3 creates the reference file first, then updates the command to reference it. Both changes in single commit.
- **Contingency:** Error handling reference can be inlined back if progressive loading fails

### Risk 3: Naming convention change requires extensive reference updates
- **Probability:** High
- **Impact:** Low — Feature 7 is lowest priority
- **Mitigation:** Feature 7 is Sprint 3. If effort exceeds 3 points, defer to a separate epic or accept current naming with ADR justification.
- **Contingency:** Close findings 2.1/2.2 as "accepted — context file constraint takes priority"

### Risk 4: Multishot examples don't improve output quality measurably
- **Probability:** Low
- **Impact:** Low — examples still improve conformance even if quality improvement is marginal
- **Mitigation:** Create 2-3 focused examples rather than attempting comprehensive coverage. Test with real ideation session before committing.

## Stakeholders

- **Product Owner:** Framework Team — Ensures remediation aligns with framework improvement goals
- **Tech Lead:** DevForgeAI AI Agent — Executes remediation workflow

## Architecture Considerations

### Architecture Impact
- No new architecture patterns — all changes are within existing skill ecosystem
- Command-skill boundary is refined (Feature 3) but not restructured
- XML tag adoption (Feature 2) introduces a new convention for inter-component communication

### Technology Decisions
- No new technologies — changes are to Markdown prompt files only
- Compliant with zero-dependency framework model
  (Source: devforgeai/specs/context/dependencies.md)

### Context File Constraints
All remediation must respect:
1. `devforgeai/specs/context/tech-stack.md` — Native tools only
2. `devforgeai/specs/context/source-tree.md` — File location rules
3. `devforgeai/specs/context/coding-standards.md` — Size limits (Skills 500-800/1000 lines), naming conventions
4. `devforgeai/specs/context/architecture-constraints.md` — Commands orchestrate, skills implement
5. `devforgeai/specs/context/anti-patterns.md` — Forbidden patterns

**Known constraint conflict:** coding-standards.md line 117 locks `devforgeai-[phase]` naming convention. Gerund rename (Finding 2.1) may require ADR. Feature 7 documents this explicitly.

## Findings-to-Feature Mapping

| Finding | Severity | Category | Feature | Sprint |
|---------|----------|----------|---------|--------|
| 8.1: Add role prompt | High | 8. Role Prompting | F1 | Sprint 1 |
| 8.2: Add multishot examples | High | 8. Role Prompting | F1 | Sprint 1 |
| 5.1: XML tags for instructions | High | 5. XML Tags | F2 | Sprint 2 |
| 9.1: Move error handling to skill | High | 9. Command-Skill | F3 | Sprint 2 |
| 1.5: Standardize model field | High | 1. YAML Frontmatter | F4 | Sprint 1 |
| 5.2: XML context markers | Medium | 5. XML Tags | F2 | Sprint 2 |
| 1.1: Space-delimited allowed-tools | Medium | 1. YAML Frontmatter | F4 | Sprint 1 |
| 1.2: Remove Skill from tools | Medium | 1. YAML Frontmatter | F4 | Sprint 1 |
| 1.4: Fix command tools delimiter | Medium | 1. YAML Frontmatter | F4 | Sprint 1 |
| 3.2: Add TOC to 14 ref files | Medium | 3. Progressive Disclosure | F5 | Sprint 3 |
| 7.1: XML phase handoff tags | Medium | 7. Chain of Thought | F2 | Sprint 2 |
| 7.2: CoT for complexity scoring | Medium | 7. Chain of Thought | F6 | Sprint 3 |
| 6.1: Checklist tracking instruction | Medium | 6. Workflow | F6 | Sprint 3 |
| 9.2: Simplify brainstorm parsing | Medium | 9. Command-Skill | F3 | Sprint 2 |
| 9.3: XML command-skill handoff | Medium | 9. Command-Skill | F2 | Sprint 2 |
| 8.3: Completed epic template example | Medium | 8. Role Prompting | F1 | Sprint 1 |
| 2.1: Gerund naming | Low | 2. Naming | F7 | Sprint 3 |
| 2.2: Remove vendor prefix | Low | 2. Naming | F7 | Sprint 3 |
| 2.3: Add trigger phrases | Low | 2. Naming | F7 | Sprint 3 |
| 4.1: Remove Core Philosophy | Low | 4. Clarity | F5 | Sprint 3 |
| 1.3: Replace Bash(git:*) | Low | 1. YAML Frontmatter | F4 | Sprint 1 |

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════
Week 1-2:  Sprint 1 — High-Impact Fixes (F1, F4)       7pts
Week 2-3:  Sprint 2 — Structural Changes (F2, F3)      8pts
Week 3-4:  Sprint 3 — Polish & Alignment (F5, F6, F7) 10pts
════════════════════════════════════════════════════════════
Total Duration: 4 weeks
Target Completion: 2026-03-14
```

### Key Milestones
- [ ] **Milestone 1:** Sprint 1 complete — Category 8 (Role/Examples) moves from Non-Conformant to Conformant
- [ ] **Milestone 2:** Sprint 2 complete — Categories 5, 9 move from Partially Conformant to Conformant
- [ ] **Milestone 3:** Sprint 3 complete — All remaining categories at Conformant or Partially Conformant (naming only)
- [ ] **Milestone 4:** Re-run conformance analysis confirms ≤2 Partially Conformant categories

## Progress Tracking

### Story Links

Stories to be created via `/create-story` for each feature (not yet created).

| Feature | Story ID | Title | Sprint | Points | Status |
|---------|----------|-------|--------|--------|--------|
| F1 | STORY-425 | Role Prompting & Multishot Examples | Sprint 1 | 5 | Deferred (EPIC-068) |
| F4 | STORY-426 | YAML Frontmatter Compliance | Sprint 1 | 2 | Deferred (EPIC-068) |
| F3 | STORY-427 | Command-Skill Separation | Sprint 2 | 3 | Deferred (EPIC-068) |
| F2 | STORY-428 | XML Tag Adoption | Sprint 2 | 5 | Deferred (EPIC-068) |
| F5 | STORY-429 | Progressive Disclosure & Token Optimization | Sprint 3 | 5 | Deferred (EPIC-068) |
| F6 | STORY-430 | Workflow Enhancement | Sprint 3 | 2 | Deferred (EPIC-068) |
| F7 | STORY-431 | Naming Convention Alignment | Sprint 3 | 3 | Superseded (EPIC-068) |

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1: High-Impact | Ready | 7 | 2 | 0 | 0 | 0 |
| Sprint 2: Structural | Ready | 8 | 2 | 0 | 0 | 0 |
| Sprint 3: Polish | Ready | 10 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **25** | **7** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 25
- **Completed:** 0
- **Remaining:** 25
- **Stories Created:** 7 (2026-02-17)

## Next Steps

### Immediate Actions
1. Create stories for Sprint 1 features: `/create-story` for F1 (Role/Examples) and F4 (YAML Frontmatter)
2. Review Feature 7 naming constraint: Check coding-standards.md for `devforgeai-[phase]` lock status
3. Begin Sprint 1 implementation

### Pre-Development Checklist
- [x] Conformance analysis complete (9/9 categories)
- [x] Epic document created with feature breakdown
- [x] Sprint 1 stories created in `devforgeai/specs/Stories/` (STORY-425, STORY-426)
- [ ] Feature 7 ADR requirement assessed (naming convention conflict)

## Notes

- This epic is the remediation counterpart to the conformance analysis. EPIC-066 covers the /dev command analysis; this epic covers the /ideate command remediation.
- The conformance analysis identified Finding 3.3 (skill scope concern — 28 reference files, ~13,345 lines) as a design observation, not a blocking finding. This epic does not attempt to split the skill.
- Feature 7 (naming) has a known conflict with coding-standards.md. If the ADR process determines the context file constraint takes priority, findings 2.1 and 2.2 will be closed as "accepted — not applicable" with no impact on the epic's success metrics.

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-17
