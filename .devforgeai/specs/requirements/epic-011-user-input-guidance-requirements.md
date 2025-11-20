# EPIC-011: User Input Guidance System - Requirements Specification

**Epic ID:** EPIC-011
**Created:** 2025-01-20
**Status:** Planning
**Complexity:** 18/60 (Simple → Moderate)

---

## 1. Executive Summary

### Problem Statement
DevForgeAI framework lacks unified guidance on how users should provide input to commands, resulting in 40% incomplete stories, token waste, and poor user experience.

### Solution Overview
Create two complementary guidance documents (user-facing + framework-internal) plus enhance claude-code-terminal-expert skill to establish framework-wide cohesion in requirement elicitation patterns.

### Business Value
- 67% reduction in incomplete stories
- 9% token efficiency improvement (10K savings per story)
- 52% reduction in iteration cycles
- Improved user onboarding and experience

---

## 2. Stakeholders

| Role | Name | Responsibility |
|------|------|----------------|
| **Primary Users** | DevForgeAI Users | Consume effective-prompting-guide.md for better input |
| **Framework Maintainers** | Dev Team | Maintain guidance documents, integrate into skills |
| **Quality Assurance** | QA Team | Validate 85%+ success rate improvement |
| **Product Owner** | Framework Lead | Approve impact report, decide on rollout |

---

## 3. Functional Requirements

### FR-001: User-Facing Prompting Guide
**Priority:** CRITICAL
**Feature:** 1

**Description:**
Create comprehensive markdown guide teaching users how to provide clear, complete input to DevForgeAI commands.

**Acceptance Criteria:**
- [ ] Document created at `src/claude/memory/effective-prompting-guide.md`
- [ ] Covers all major commands (/ideate, /create-story, /create-context, /dev, /qa, /release)
- [ ] Contains 20-30 before/after examples
- [ ] Includes quick reference checklists for each command
- [ ] Documents 10-15 common pitfalls to avoid
- [ ] Cross-references user-input-guidance.md and claude-code-terminal-expert
- [ ] Size: 3,000-4,000 lines
- [ ] Format: Markdown with clear sections, scannable headers

**Success Metrics:**
- Users report clearer understanding of framework expectations
- 30% reduction in "I don't know what to provide" questions

---

### FR-002: Framework-Internal Guidance Reference
**Priority:** CRITICAL
**Feature:** 2

**Description:**
Create internal reference for Claude executing skills, providing patterns for eliciting complete requirements from users.

**Acceptance Criteria:**
- [ ] Document created at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`
- [ ] Contains 10-15 elicitation patterns (functional, NFR, edge cases, integration)
- [ ] Includes 20-30 AskUserQuestion templates
- [ ] Provides NFR quantification table (vague term → measurable target)
- [ ] Documents integration points for 5 skills
- [ ] Cross-references effective-prompting-guide.md and claude-code-terminal-expert
- [ ] Size: 2,000-3,000 lines
- [ ] Format: Structured sections with clear examples

**Success Metrics:**
- Skills using guidance show 52% reduction in subagent re-invocations
- 9% token savings measured across 10 test stories

---

### FR-003: claude-code-terminal-expert Enhancement
**Priority:** HIGH
**Feature:** 3

**Description:**
Add "How DevForgeAI Skills Work with User Input" section to claude-code-terminal-expert skill for framework cohesion.

**Acceptance Criteria:**
- [ ] New section added to `src/claude/skills/claude-code-terminal-expert/SKILL.md`
- [ ] Section explains "Ask, Don't Assume" principle
- [ ] Contains 5-10 quick examples of effective communication
- [ ] Cross-references both guidance documents
- [ ] Positioned after features overview, before detailed sections
- [ ] Size: 100-200 lines
- [ ] Maintains skill's existing structure and organization

**Success Metrics:**
- Framework components reference consistent guidance source
- No conflicting advice across skills

---

### FR-004: devforgeai-ideation Integration
**Priority:** HIGH
**Feature:** 4

**Description:**
Integrate user-input-guidance.md into devforgeai-ideation skill Phase 1.

**Acceptance Criteria:**
- [ ] Phase 1 Step 0 added to `src/claude/skills/devforgeai-ideation/SKILL.md`
- [ ] Step 0 loads user-input-guidance.md before discovery
- [ ] Guidance patterns used throughout Phase 1-2 questions
- [ ] Documentation updated to explain integration
- [ ] No breaking changes to existing workflow

**Success Metrics:**
- Ideation generates more complete requirements on first pass
- Fewer clarifying questions needed post-ideation

---

### FR-005: devforgeai-story-creation Integration
**Priority:** CRITICAL
**Feature:** 5

**Description:**
Integrate user-input-guidance.md into devforgeai-story-creation skill Phase 1.

**Acceptance Criteria:**
- [ ] Phase 1 Step 0 added to `src/claude/skills/devforgeai-story-creation/SKILL.md`
- [ ] Step 0 loads user-input-guidance.md before feature capture
- [ ] Guidance patterns used before invoking requirements-analyst subagent
- [ ] Documentation updated to explain integration
- [ ] No breaking changes to existing workflow

**Success Metrics:**
- 85%+ single-pass success rate (up from 40%)
- 2.5 → 1.2 average subagent re-invocations

---

### FR-006: Additional Skill Integrations
**Priority:** MEDIUM
**Feature:** 6

**Description:**
Integrate guidance into devforgeai-architecture, devforgeai-ui-generator, devforgeai-orchestration.

**Acceptance Criteria:**
- [ ] devforgeai-architecture: Phase 1 Step 0 added
- [ ] devforgeai-ui-generator: Phase 2 Step 0 added
- [ ] devforgeai-orchestration: Phase 4A Step 0 and Phase 3 Step 0 added
- [ ] All integrations follow same pattern (Step 0: Load guidance)
- [ ] Documentation updated for each skill
- [ ] No breaking changes to existing workflows

**Success Metrics:**
- Framework-wide consistency in requirement elicitation
- All user-input skills show improved question quality

---

### FR-007: Documentation Updates
**Priority:** MEDIUM
**Feature:** 7

**Description:**
Update framework documentation to reference new guidance system.

**Acceptance Criteria:**
- [ ] `src/CLAUDE.md`: "Learning DevForgeAI" section added
- [ ] `src/claude/memory/commands-reference.md`: Cross-refs added for 11 commands
- [ ] `src/claude/memory/skills-reference.md`: Cross-refs added for 13 skills
- [ ] All cross-references use correct file paths (src/ tree)
- [ ] Progressive disclosure principle maintained
- [ ] Links are discoverable by users and framework

**Success Metrics:**
- Users find guidance documents easily
- Framework components reference guidance correctly

---

### FR-008: Validation & Testing Suite
**Priority:** HIGH
**Feature:** 8

**Description:**
Create comprehensive test suite validating guidance system impact.

**Acceptance Criteria:**
- [ ] Test suite created in `tests/user-input-guidance/`
- [ ] 10 test fixtures (feature descriptions of varying quality)
- [ ] Baseline tests (without guidance) measure current performance
- [ ] Enhanced tests (with guidance) measure improvement
- [ ] Token savings validation script (Python)
- [ ] Success rate measurement script (Python)
- [ ] Sync validation script (Bash)
- [ ] Impact report generated in `.devforgeai/specs/enhancements/`

**Success Metrics:**
- All tests pass
- Impact report shows 85%+ success rate, 9%+ token savings
- Baseline vs enhanced comparison validates hypothesis

---

### FR-009: Operational Sync
**Priority:** MEDIUM
**Feature:** 9

**Description:**
Sync source files to operational folders for runtime use.

**Acceptance Criteria:**
- [ ] Sync script copies `src/claude/` → `.claude/`
- [ ] Sync script copies `src/CLAUDE.md` → `CLAUDE.md`
- [ ] Validation confirms operational files match source
- [ ] Sync is non-destructive (preserves operational-only files)
- [ ] Documentation explains sync workflow

**Success Metrics:**
- Operational folders match source distribution
- No sync-related issues during runtime

---

## 4. Non-Functional Requirements

### NFR-001: Performance
**Priority:** HIGH

- **Token Efficiency:** Net 9% savings per story (10K tokens)
- **Load Time:** Guidance documents load in <500ms
- **No Runtime Impact:** Command execution time unchanged

**Acceptance:**
- [ ] Token savings measured at 9%+ on 10 test stories
- [ ] Load time <500ms for all Read operations
- [ ] No measurable increase in command execution time

---

### NFR-002: Maintainability
**Priority:** HIGH

- **Single Source of Truth:** All guidance in `src/` tree
- **Cross-References:** Clear links between documents
- **Markdown Format:** Easy to update, version control friendly
- **Sync Automation:** Operational folders updated automatically

**Acceptance:**
- [ ] No duplicate guidance across documents
- [ ] All cross-references resolve correctly
- [ ] Markdown lints pass
- [ ] Sync script runs without errors

---

### NFR-003: Usability
**Priority:** HIGH

- **Scannable Format:** Checklists, headers, tables
- **Concrete Examples:** 20-30 before/after examples
- **Progressive Disclosure:** Users read as needed
- **Discoverability:** Linked from CLAUDE.md and memory/

**Acceptance:**
- [ ] Users report documents are easy to navigate
- [ ] Examples are clear and helpful
- [ ] Checklists are actionable
- [ ] Documents are easy to find

---

### NFR-004: Quality
**Priority:** CRITICAL

- **Success Rate:** 85%+ single-pass story creation
- **Incomplete Stories:** <15% (down from 40%)
- **Framework Cohesion:** All skills use same terminology
- **Consistency:** No conflicting advice across documents

**Acceptance:**
- [ ] 10 test stories show 85%+ single-pass success
- [ ] Incomplete story rate <15%
- [ ] Terminology audit shows consistency
- [ ] No conflicting patterns found

---

### NFR-005: Testability
**Priority:** MEDIUM

- **Automated Tests:** All validation scripts executable
- **Reproducible:** Same inputs → same results
- **Measurable:** Metrics clearly defined
- **Evidence-Based:** Impact report with data

**Acceptance:**
- [ ] All test scripts run successfully
- [ ] Results are reproducible
- [ ] Metrics match targets (85% success, 9% savings)
- [ ] Impact report contains evidence

---

## 5. Data Models

### 5.1 Guidance Document Structure

```markdown
# [Document Title]

## Purpose
[Why this document exists]

## Core Principles
[Framework principles this reinforces]

## By [Category] (User Guide)
### [Category 1]
[Guidance for this category]

## [Pattern Type] (Framework Guide)
### Pattern 1: [Name]
[Pattern details]

## Cross-References
[Links to related documents]
```

### 5.2 Test Fixture Format

```json
{
  "fixture_id": "feature-001",
  "description": "Login feature description",
  "quality": "poor|good|excellent",
  "input": "Feature description text",
  "expected_questions": 15,
  "expected_iterations": 2.5,
  "expected_tokens": 115000
}
```

### 5.3 Impact Report Format

```yaml
---
report_id: USER-INPUT-GUIDANCE-IMPACT
date: 2025-01-20
version: 1.0
---

## Baseline Metrics (Without Guidance)
- Single-pass success rate: 40%
- Average iterations: 2.5
- Average tokens per story: 115K

## Enhanced Metrics (With Guidance)
- Single-pass success rate: 85%
- Average iterations: 1.2
- Average tokens per story: 105K

## Improvements
- Success rate: +112% (40% → 85%)
- Iterations: -52% (2.5 → 1.2)
- Tokens: -9% (115K → 105K)

## Evidence
[10 test stories with results]
```

---

## 6. Integration Points

### 6.1 Skill Integration Pattern

**All skills follow same pattern:**

```markdown
### Phase N: [Phase Name]

**Step 0: Load User Input Guidance (NEW)**

Before [phase activity], load requirement elicitation patterns:

Read(file_path="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md")

Use patterns to:
- [Specific application 1]
- [Specific application 2]
- [Specific application 3]

**Step 1: [Existing Step] (EXISTING)**

[Continue with existing workflow...]
```

### 6.2 Cross-Reference Pattern

**All documents cross-reference consistently:**

```markdown
## Cross-References

**For users:**
- Getting started: src/CLAUDE.md
- Effective prompting: src/claude/memory/effective-prompting-guide.md

**For framework:**
- Requirement patterns: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
- Claude Code capabilities: claude-code-terminal-expert skill

**For maintainers:**
- Source tree: src/
- Tests: tests/user-input-guidance/
```

---

## 7. Constraints

### 7.1 Technical Constraints

- **File Format:** Markdown only (no HTML, no binary)
- **File Location:** `src/` tree (not operational folders)
- **Size Limits:** effective-prompting-guide.md <5K lines, user-input-guidance.md <3K lines
- **Dependencies:** No external dependencies (framework self-contained)

### 7.2 Compatibility Constraints

- **Backward Compatibility:** All skill integrations must not break existing workflows
- **Framework Version:** Works with current DevForgeAI version
- **Claude Code Version:** Compatible with current terminal version

### 7.3 Process Constraints

- **Source Tree Alignment:** All deliverables in `src/` tree
- **Testing Required:** All features must pass validation tests
- **Documentation Required:** All changes must update relevant docs
- **Review Required:** Impact report must show positive results

---

## 8. Assumptions

1. **User Willingness:** Users willing to read guidance documents
2. **Framework Compliance:** Skills will load guidance when integrated
3. **Token Availability:** 2-3K token load doesn't exhaust budgets
4. **Measurability:** Success rate and token savings are measurable
5. **Maintenance:** Team commits to quarterly guidance reviews

---

## 9. Dependencies

### 9.1 Internal Dependencies

- DevForgeAI framework operational (.claude/ and .devforgeai/ exist)
- 5 skills to integrate with (ideation, story-creation, architecture, ui-generator, orchestration)
- claude-code-terminal-expert skill exists
- Source tree structure established (src/ directory)

### 9.2 External Dependencies

- None (framework enhancement is self-contained)

---

## 10. Success Metrics

### 10.1 Quantitative Metrics

| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| **Single-pass success rate** | 40% | 85% | Test 10 stories with/without guidance |
| **Average iterations** | 2.5 | 1.2 | Count subagent re-invocations |
| **Token usage per story** | 115K | 105K | Measure total tokens from start to completion |
| **Incomplete stories** | 40% | <15% | Count stories requiring revision |
| **Time to first story** | 15-20 min | 10-12 min | Time from /create-story to completion |

### 10.2 Qualitative Metrics

- **User Feedback:** Positive feedback on guidance clarity
- **Framework Cohesion:** No conflicting advice detected
- **Discoverability:** Users find guidance documents easily
- **Maintainability:** Team reports guidance is easy to update

---

## 11. Risks & Mitigation

### Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Guidance not used | Low | High | Mandatory Step 0 in skills (automatic load) |
| Token overhead negates savings | Low | Medium | Progressive disclosure, measure actual impact |
| Guidance becomes outdated | Medium | Medium | Quarterly reviews, versioning |
| Source/operational sync issues | Medium | Medium | Automated validation script |
| Users don't read guide | Medium | Low | Framework still asks questions (optional enhancement) |

---

## 12. Timeline

**Sprint 1 (2 weeks):**
- Week 1: Features 1-3 (Documents + enhancement)
- Week 2: Features 4-9 (Integration + testing + sync)

**Total Duration:** 2 weeks (1 sprint)

---

## 13. Acceptance

### 13.1 Definition of Done

- [ ] All 9 features implemented
- [ ] All source files in `src/` tree
- [ ] All tests passing
- [ ] Impact report shows positive results
- [ ] Documentation updated
- [ ] Operational sync validated
- [ ] User feedback collected

### 13.2 Sign-Off

- [ ] Product Owner approves impact report
- [ ] QA validates 85%+ success rate
- [ ] Framework Maintainers approve integration
- [ ] Users report positive experience

---

**Requirements Status:** Complete
**Next Action:** Create sprint plan with `/create-sprint`
