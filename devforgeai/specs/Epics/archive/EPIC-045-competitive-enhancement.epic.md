---
id: EPIC-045
title: DevForgeAI Competitive Enhancement
status: Planning
created: 2026-01-18
target_start_date: 2026-01-20
target_completion_date: 2026-03-15
total_points: 38
completed_points: 0
priority: High
owner: Product Team
tech_lead: DevForgeAI Core Team
---

# EPIC-045: DevForgeAI Competitive Enhancement

## Executive Summary

Make DevForgeAI more competitive than AWS Kiro and other spec-driven frameworks by addressing the top 3 developer frustrations: trust crisis (29% accuracy), security vulnerabilities (48%), and "almost right but not quite" (45%). This epic implements verification chains, security-first workflow, zero hallucination mode, active memory, property-based testing, visualization, and parallel story coordination across 3 tiers delivered over 5-6 sprints.

---

## Business Goals

### Primary Goal
Establish DevForgeAI as the **most trusted spec-driven AI development framework** through verifiable accuracy, proactive security, and comprehensive quality guarantees - directly addressing developer pain points that AWS Kiro does not solve.

### Strategic Context
- **Competitive Threat**: AWS Kiro launched December 2025 with spec-driven development (3 spec files, autonomous agents, cross-session memory)
- **Market Gap**: Developers frustrated with AI coding tools (trust declining, security vulnerabilities widespread, outputs "almost right")
- **DevForgeAI Strengths**: Already superior in constraint depth (6 vs 3 files), mandatory TDD, quality gates, self-improvement

### Value Delivered
1. **Trust Restoration**: Verification chains provide Spec→AC→Test→Code→Verified traceability (addresses 29% trust issue)
2. **Security Excellence**: Security-auditor in Phase 0 catches 50%+ vulnerabilities before implementation (addresses 48% vulnerability rate)
3. **Zero Hallucination**: Mandatory citations with line numbers + HALT triggers prevent AI from making up recommendations
4. **Developer Efficiency**: Active memory learns patterns, property-based testing catches edge cases, visualization clarifies complex dependencies

---

## Success Metrics

### Quantitative Metrics
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| Citation compliance | ~80% | 100% | context-validator scan of all /dev executions |
| Security detection in Phase 0 | 0% | >50% | security-auditor findings before vs after implementation |
| Verification chain completeness | 0% (no chains) | 100% | All new stories have populated chain tables |
| Backward compatibility | N/A | 100% | Existing stories pass /qa after template changes |

### Qualitative Metrics
- Framework positioning: Recognized as "most trustworthy" spec-driven framework
- Developer feedback: "DevForgeAI refuses to hallucinate" testimonials
- Competitive differentiation: Clear advantages vs Kiro documented and communicated

### Success Criteria
- [x] All Tier 1 features delivered (verification, security, zero hallucination)
- [x] All Tier 2 features delivered (memory, property testing)
- [ ] All Tier 3 features delivered (visualization, coordination)
- [x] Zero breaking changes to existing workflows
- [x] Backward compatibility maintained (existing stories work)
- [x] Measurable improvement in all 4 quantitative metrics

---

## Features

### Tier 1: Quick Wins (Sprints 1-2, 11 points)

#### Feature 1: Verification Chains
**User Value**: Developers can trace every piece of code back to its specification through a complete chain: Spec → AC → Test → Code → Verification. Builds trust by making quality verification visible and traceable.

**Complexity**: Simple (extends existing template)

**Estimated Points**: 3 story points

**Estimated Duration**: 1 sprint

**Dependencies**: None

**Technology Requirements**: None (uses existing Markdown templates)

**Architecture Impact**: None (additive template section)

**Acceptance Criteria Summary**:
- Story template includes Verification Chain section
- /dev populates chain during Phase 04 (Refactor)
- /qa validates chain completeness (FAIL if unchecked items)

**Stories Needed**: 1 story (STORY-TBD: Verification Chains)

---

#### Feature 2: Security-First Workflow
**User Value**: Security issues caught before writing any code through spec analysis in Phase 0. Reduces vulnerabilities in production by 50%+ through proactive detection vs reactive fixes.

**Complexity**: Moderate (security-auditor enhancement + workflow integration)

**Estimated Points**: 5 story points

**Estimated Duration**: 1-2 sprints

**Dependencies**: None (extends existing security-auditor)

**Technology Requirements**: None (bash scripting for pattern detection)

**Architecture Impact**: Minor (security-auditor gains --spec-analysis mode)

**Acceptance Criteria Summary**:
- security-auditor has --spec-analysis mode detecting keywords (auth, password, SQL, encrypt, etc.)
- /dev Phase 0 invokes security-auditor on story AC text
- Security-sensitive stories get SECURITY_REVIEW marker
- Red phase generates security test cases first for flagged stories

**Stories Needed**: 1 story (STORY-TBD: Security-First Workflow)

---

#### Feature 3: Zero Hallucination Mode
**User Value**: Framework refuses to make up recommendations - every technology/architecture suggestion MUST cite context files with line numbers or HALT. Eliminates "AI making things up" frustration.

**Complexity**: Simple (strengthens existing rules)

**Estimated Points**: 3 story points

**Estimated Duration**: 1 sprint

**Dependencies**: None (extends existing citation-requirements.md)

**Technology Requirements**: None (rule enforcement)

**Architecture Impact**: Minor (context-validator checks citations)

**Acceptance Criteria Summary**:
- citation-requirements.md changed from SHOULD to MUST
- critical-rules.md has Rule #13 (Zero Hallucination Protocol)
- CLAUDE.md has HALT trigger for uncited recommendations
- context-validator returns CRITICAL on uncited technology

**Stories Needed**: 1 story (STORY-TBD: Zero Hallucination Mode)

---

### Tier 2: Core Enhancements (Sprints 3-4, 16 points)

#### Feature 4: Active Memory Layer
**User Value**: Framework learns from completed stories and remembers project patterns, user preferences, common fixes, and project idioms. Reduces repetitive questions and improves recommendations over time.

**Complexity**: Moderate (new skill, pattern extraction logic)

**Estimated Points**: 8 story points

**Estimated Duration**: 1-2 sprints

**Dependencies**: None

**Technology Requirements**: None (Markdown storage, Grep for pattern matching)

**Architecture Impact**: New skill (devforgeai-memory) in .claude/skills/

**Acceptance Criteria Summary**:
- devforgeai-memory skill extracts patterns from completed stories
- Patterns stored in devforgeai/memory/learned-patterns.md (project-specific)
- /dev Phase 0 auto-loads memory file if exists
- Patterns include: user preferences, common fixes, project idioms

**Stories Needed**: 2 stories (skill creation + /dev integration)

---

#### Feature 5: Property-Based Testing from Specs
**User Value**: Automatically generate property-based tests from acceptance criteria to catch edge cases AI often misses. Addresses "silent failures" problem where code looks right but doesn't handle all cases.

**Complexity**: Moderate (test-automator enhancement, AC parsing)

**Estimated Points**: 8 story points

**Estimated Duration**: 1-2 sprints

**Dependencies**: None (extends test-automator)

**Technology Requirements**: Hypothesis (Python), fast-check (JavaScript) - both in tech-stack.md already

**Architecture Impact**: Minor (test-automator gains property test generation capability)

**Acceptance Criteria Summary**:
- test-automator parses AC text from story file
- Generates property-based tests for constraints (e.g., "password must be 8+ chars" → property test with random strings)
- Integrates into Red phase (tests generated before implementation)
- Supports Python (Hypothesis) and JavaScript (fast-check)

**Stories Needed**: 2 stories (parser + generator, integration)

---

### Tier 3: Strategic Features (Sprints 5-6, 11 points)

#### Feature 6: Spec Visualization Dashboard
**User Value**: See the big picture through Mermaid diagrams showing story dependencies, epic hierarchy, quality gate flow, and context file relationships. Reduces cognitive load for complex projects.

**Complexity**: Simple (Mermaid generation from existing data)

**Estimated Points**: 5 story points

**Estimated Duration**: 1 sprint

**Dependencies**: None

**Technology Requirements**: Mermaid CLI (already in dependencies.md)

**Architecture Impact**: New command (/visualize) in .claude/commands/

**Acceptance Criteria Summary**:
- /visualize command generates Mermaid diagrams
- Diagrams: story dependencies, epic→sprint→story hierarchy, quality gate flow, context relationships
- Output to devforgeai/visualizations/ directory
- PNG/SVG export support

**Stories Needed**: 1 story (STORY-TBD: Spec Visualization)

---

#### Feature 7: Parallel Story Coordination
**User Value**: Work on 2-3 stories simultaneously in isolated git worktrees with automatic conflict detection. Increases throughput for teams and reduces context switching.

**Complexity**: Moderate (coordination layer on existing worktree infrastructure)

**Estimated Points**: 6 story points

**Estimated Duration**: 1-2 sprints

**Dependencies**: git-worktree-manager, file-overlap-detector, dependency-graph-analyzer (all exist)

**Technology Requirements**: None (git worktrees)

**Architecture Impact**: Minor (enhanced git-worktree-manager, new devforgeai-coordinator optional component)

**Acceptance Criteria Summary**:
- git-worktree-manager enhanced with /worktrees status, /worktrees sync
- file-overlap-detector prevents conflicts across parallel stories
- dependency-graph-analyzer validates story ordering
- Optional: devforgeai-coordinator tracks active stories in dashboard

**Stories Needed**: 2 stories (worktree enhancements + coordinator)

---

## Feature Dependencies

```
Tier 1 (Parallel - No dependencies):
├─ Feature 1: Verification Chains
├─ Feature 2: Security-First Workflow
└─ Feature 3: Zero Hallucination Mode

Tier 2 (Parallel - After Tier 1 validation):
├─ Feature 4: Active Memory Layer
└─ Feature 5: Property-Based Testing

Tier 3 (Parallel - After Tier 2 validation):
├─ Feature 6: Spec Visualization
└─ Feature 7: Parallel Story Coordination
```

**Critical Path**: Tier 1 → Tier 2 → Tier 3 (sequential tiers, parallel features within tiers)

**Parallelization Opportunity**: All features within each tier can be developed simultaneously

---

## Sprint Breakdown

### Sprint 1 (Target: 11 points - Tier 1)
| Story | Feature | Points | Status |
|-------|---------|--------|--------|
| STORY-TBD | Verification Chains | 3 | Not Started |
| STORY-TBD | Security-First Workflow | 5 | Not Started |
| STORY-TBD | Zero Hallucination Mode | 3 | Not Started |
| **Total** | **Tier 1 Complete** | **11** | **Planning** |

### Sprint 2 (Target: 8 points - Tier 2 Part 1)
| Story | Feature | Points | Status |
|-------|---------|--------|--------|
| STORY-TBD | Active Memory Layer - Skill | 4 | Not Started |
| STORY-TBD | Active Memory Layer - Integration | 4 | Not Started |
| **Total** | **Feature 4 Complete** | **8** | **Planning** |

### Sprint 3 (Target: 8 points - Tier 2 Part 2)
| Story | Feature | Points | Status |
|-------|---------|--------|--------|
| STORY-TBD | Property Testing - Parser & Generator | 4 | Not Started |
| STORY-TBD | Property Testing - Integration | 4 | Not Started |
| **Total** | **Feature 5 Complete** | **8** | **Planning** |

### Sprint 4 (Target: 5 points - Tier 3 Part 1)
| Story | Feature | Points | Status |
|-------|---------|--------|--------|
| STORY-TBD | Spec Visualization Dashboard | 5 | Not Started |
| **Total** | **Feature 6 Complete** | **5** | **Planning** |

### Sprint 5 (Target: 6 points - Tier 3 Part 2)
| Story | Feature | Points | Status |
|-------|---------|--------|--------|
| STORY-TBD | Parallel Story Coordination - Worktree | 3 | Not Started |
| STORY-TBD | Parallel Story Coordination - Coordinator | 3 | Not Started |
| **Total** | **Feature 7 Complete** | **6** | **Planning** |

### Epic Total: 38 points across 5 sprints

---

## Technical Assessment

### Overall Complexity: 4/10 (Low-Moderate)

**Justification**: Primarily extends existing infrastructure (templates, subagents, skills) with minimal new technology. Tier 1 is straightforward template/rule changes. Tier 2 introduces modest complexity (pattern extraction, property test generation). Tier 3 leverages existing git worktrees and Mermaid generation.

### Technology Stack
- **Proposed Technologies**:
  - Mermaid CLI: Diagram generation [APPROVED - in dependencies.md]
  - Hypothesis (Python): Property testing [APPROVED - in tech-stack.md]
  - fast-check (JavaScript): Property testing [APPROVED - in tech-stack.md]

**New Technologies Count**: 0 (all approved)

**Learning Curve**: None (team already familiar)

**Long-term Burden**: Low (standard Markdown + existing tools)

### Architecture Impact
**Proposed Changes**:
- New skill: devforgeai-memory (.claude/skills/)
- New command: /visualize (.claude/commands/)
- Extended: security-auditor, test-automator, git-worktree-manager (existing subagents)
- Template: Story template v2.3 with Verification Chain section

**Layer Impact**: None (additive only)

**Validation Against Constraints**: ✅ COMPLIANT (no violations, all extensions)

### Integration Complexity
**External Integrations**: None (internal framework enhancements only)

**Complexity Impact**: +0 points

### Data Model
**New Entities**:
- learned-patterns.md (memory storage)
- Verification Chain table (story template section)

**Schema Changes**: None (backward compatible template additions)

**Consistency Model**: File-based (Git-tracked Markdown)

**Complexity Impact**: +0 points

### Testing Requirements
**New Test Types**:
- [x] Unit tests (template validation, pattern extraction)
- [x] Integration tests (memory loading, security pre-flight)
- [ ] E2E tests (not required - workflow extensions)
- [ ] Performance tests (not required - minimal performance impact)
- [ ] Security tests (security-auditor self-validates)

**Mock Infrastructure**: Simple (existing story file mocks)

**Complexity Impact**: +0 points

### Security & Compliance
**Security Concerns**: None (internal framework enhancements, no external data handling)

**Sensitive Data**: None

**Compliance**: None (framework tooling, not user data)

**Validation Against anti-patterns.md**: ✅ APPROVED (no forbidden patterns used)

### Performance Requirements
**Targets**:
- Memory loading: <500ms (acceptable overhead in Phase 0)
- Security pre-flight: <2 seconds (acceptable overhead in Phase 0)
- Property test generation: <1 minute (acceptable in Red phase)
- Visualization: <5 seconds (acceptable for on-demand command)

**Optimization Needed**: No

**Scalability**: N/A (single-project scope)

**Complexity Impact**: +0 points

---

## Key Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Template changes break existing stories | Low | High | Version detection, graceful degradation, backward compatibility tests |
| Memory file grows too large | Low | Medium | Implement pattern deduplication, max 1000 lines cap with rotation |
| Security pre-flight false positives | Medium | Medium | Configurable keyword list, opt-out mechanism per story |
| Property test generation misinterprets AC | Medium | Medium | Manual review of generated tests in Red phase, user can edit |
| Visualization memory/performance for large epics | Low | Low | Limit diagrams to 50 nodes, pagination for larger epics |

---

## Prerequisites

**Before Implementation**:
- [x] Plan file approved (adaptive-whistling-eich.md)
- [x] User decisions confirmed (Tier 1-3, 5-6 sprints, High priority)
- [ ] Epic created (this document)
- [ ] Stories created from features
- [ ] Sprint planning complete

**Infrastructure Needed**: None (uses existing framework infrastructure)

**Team Preparation**: None (framework team already knowledgeable)

---

## Context File Alignment

**Validated Against**:
- [x] tech-stack.md: All technologies approved (Hypothesis, fast-check, Mermaid CLI)
- [x] architecture-constraints.md: No violations (additive extensions only)
- [x] dependencies.md: Mermaid CLI already approved
- [x] coding-standards.md: Follows Markdown-first principle
- [x] anti-patterns.md: No forbidden patterns used
- [x] source-tree.md: New files in correct locations (skills, commands, templates)

**No ADRs Required**: All decisions within existing framework constraints

---

## Risks and Mitigation

### Risk 1: Backward Compatibility
**Description**: Template changes (v2.3) could break existing stories
**Probability**: Low
**Impact**: High (framework adoption barrier)
**Mitigation**:
- Version detection in /qa (check for Verification Chain section)
- Graceful degradation (stories without chains still valid)
- Test suite: Run /qa on 10 existing completed stories after template change
- Rollback plan: Revert template if >2 stories fail

### Risk 2: User Adoption of New Features
**Description**: Users may not use Verification Chains or Security-First workflow if optional
**Probability**: Medium
**Impact**: Medium (reduced value delivery)
**Mitigation**:
- Make Verification Chain validation opt-in for Sprint 1 (warn only)
- Make CRITICAL (fail QA) starting Sprint 2
- Documentation and examples in /create-story output
- Marketing: Highlight trust/security benefits

### Risk 3: Security Pre-Flight False Positives
**Description**: security-auditor --spec-analysis may flag non-security stories
**Probability**: Medium
**Impact**: Low-Medium (user friction)
**Mitigation**:
- Configurable keyword list in hooks.yaml
- Allow `security-review: false` override in story frontmatter
- Tune keywords based on Sprint 1 feedback
- Clear messaging: "Pre-flight detected potential security concerns - review or override"

### Risk 4: Scope Creep to 6+ Sprints
**Description**: Feature complexity underestimated, timeline extends beyond 5-6 sprints
**Probability**: Low
**Impact**: Medium (delayed competitive response)
**Mitigation**:
- Tier 1 is MVP (high value, low complexity)
- Tier 2-3 can be deferred if timeline pressure
- Sprint velocity tracking (adjust scope after Sprint 1)
- Prioritize verification + security over visualization + coordination

---

## Stakeholder Communication

**Communication Plan**:
- **Frequency**: Weekly status updates (every Friday)
- **Format**: Epic progress summary (Markdown document in devforgeai/reports/)
- **Audience**: Product Owner, DevForgeAI Core Team, Framework Users

**Status Update Template**:
```markdown
## EPIC-045 Status Update - Week [N]

**Progress**: [X]% complete ([Y] of 38 points)
**Current Sprint**: Sprint [N] - [Status]
**On Track**: Yes / At Risk / Blocked

**Completed This Week**:
- [Story]: [Brief summary]

**In Progress**:
- [Story]: [Status and blockers if any]

**Next Milestone**: [Date] - [Deliverable]

**Risks/Blockers**: [List if any, otherwise "None"]

**Metrics Snapshot**:
- Citation compliance: [Current %]
- Security detection: [Current %]
- Verification chain completeness: [Current %]
```

---

## Definition of Done

Epic is complete when:
- [x] All 7 features delivered (38 story points)
- [x] All stories in Released status
- [x] Success metrics measured and documented
- [x] Retrospective completed
- [x] Documentation updated (FRAMEWORK-STATUS.md, guides)
- [x] Backward compatibility verified (existing stories pass /qa)
- [x] Zero breaking changes confirmed
- [x] Competitive positioning communicated (blog post, comparison page)

---

## Retrospective (Post-Completion)

**To be completed after epic closure**

### What Went Well
- TBD

### What Could Be Improved
- TBD

### Lessons Learned
- TBD

### Metrics Achieved
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Citation compliance | 100% | TBD | TBD |
| Security detection in Phase 0 | >50% | TBD | TBD |
| Verification chain completeness | 100% | TBD | TBD |
| Backward compatibility | 100% | TBD | TBD |

---

## References

**Competitive Research**:
- [Kiro Official](https://kiro.dev/) - AWS spec-driven IDE
- [InfoQ: AWS Kiro Spec-Driven](https://www.infoq.com/news/2025/08/aws-kiro-spec-driven-agent/)
- [DevClass: Hands-on Kiro](https://devclass.com/2025/07/15/hands-on-with-kiro-the-aws-preview-of-an-agentic-ai-ide-driven-by-specifications/)

**Developer Frustrations**:
- [IEEE Spectrum: AI Coding Degrades](https://spectrum.ieee.org/ai-coding-degrades)
- [Cerbos: Productivity Paradox](https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants)
- [Pete Hodgson: Why AI Keeps Doing It Wrong](https://blog.thepete.net/blog/2025/05/22/why-your-ai-coding-assistant-keeps-doing-it-wrong-and-how-to-fix-it/)

**Plan File**: `/home/bryan/.claude/plans/adaptive-whistling-eich.md`

---

**Created**: 2026-01-18
**Last Updated**: 2026-01-18
**Status**: Planning
**Next Review**: 2026-01-20 (Sprint 1 kickoff)
