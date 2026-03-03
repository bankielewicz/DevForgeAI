---
id: EPIC-050
title: Installation Process Improvements
status: Planning
start_date: 2026-01-25
target_date: 2026-03-31
total_points: 18
completed_points: 0
created: 2026-01-25
owner: DevForgeAI Team
tech_lead: Claude
team: DevForgeAI
priority: P1 - Critical
source_analysis: /home/bryan/.claude/plans/idempotent-dazzling-petal.md
---

# Epic: Installation Process Improvements

## Business Goal

Improve the DevForgeAI installation process from its current grade of **C+ (72/100)** to **B+ (85/100)** by addressing 7 friction points that make onboarding unnecessarily difficult.

The installation system has enterprise-grade features (offline support, rollback, validation) but these are buried under layers of friction including binary name mismatches, undocumented prerequisites, and fragmented configuration.

**Value Statement:** Reduce installation time from 10-15 minutes (with troubleshooting) to 3-5 minutes, and eliminate common causes of installation failures.

## Success Metrics

- **Metric 1:** Reduce average installation time from 10-15 min to 3-5 min
- **Metric 2:** Eliminate Phase 01 preflight failures due to CLI detection (currently ~30% of failures)
- **Metric 3:** Reduce installation support requests by 50%
- **Metric 4:** Achieve 100% first-run success rate for documented installation path

**Measurement Plan:**
- Track via user feedback and RCA documents
- Baseline: C+ (72/100) installation grade
- Target: B+ (85/100) installation grade
- Review frequency: After each sprint

## Scope

### In Scope

#### Feature 1.1: Fix Binary Name Mismatch (CRITICAL)
- **Points:** 2
- **RCA:** RCA-026
- **Problem:** setup.py registers `devforgeai-validate` but cli.py uses prog='devforgeai', causing Phase 01 preflight CLI detection to fail
- **Solution:** Align binary name across setup.py, cli.py, and reference files
- **Business Value:** Eliminates ~30% of installation failures

#### Feature 1.2: Document Python CLI Installation Step (CRITICAL)
- **Points:** 1
- **Problem:** INSTALL.md missing explicit `pip install -e .claude/scripts/` instruction
- **Solution:** Add explicit step to prerequisites section
- **Business Value:** Prevents silent failures from missing CLI

#### Feature 2.1: Consolidate PYTHONPATH Settings (HIGH)
- **Points:** 2
- **Problem:** 5 different PYTHONPATH patterns in settings.local.json
- **Solution:** Consolidate to single canonical path pattern
- **Business Value:** Reduces configuration confusion and debugging time

#### Feature 2.2: Create TARGET-PROJECT-QUICK-START.md (HIGH)
- **Points:** 3
- **Problem:** No quick-start guide for external projects
- **Solution:** Create 5-minute guide: Prerequisites -> Install -> First Command -> Verify
- **Business Value:** Enables self-service onboarding without reading 700+ line INSTALL.md

#### Feature 2.3: Document Hook Setup Prerequisites (HIGH)
- **Points:** 2
- **Problem:** Hook configuration not documented as installation prerequisite
- **Solution:** Add hook setup section to INSTALL.md
- **Business Value:** Prevents silent hook failures

#### Feature 3.1: Consolidate Triple Mirror Pattern (MEDIUM)
- **Points:** 5
- **Problem:** Code exists in /src/, .claude/, AND /bundled/ requiring 3x maintenance
- **Solution:** Make /src/claude/ single source of truth with build-time sync
- **ADR Required:** Yes - Triple Mirror Consolidation Strategy
- **Business Value:** Reduces maintenance burden and sync errors

#### Feature 3.2: Add Post-Install Validation Command (MEDIUM)
- **Points:** 3
- **Problem:** No command for users to verify installation worked
- **Solution:** Create `devforgeai-validate validate-installation` command
- **Business Value:** Enables self-service troubleshooting

### Out of Scope

- Simplifying the installer architecture (100+ Python modules) - future epic
- GUI installer improvements - separate initiative
- Pure npm distribution (eliminating Python dependency) - architectural decision needed
- Repository bloat cleanup (1000s of backup files) - maintenance task

## Target Sprints

### Sprint 1: Critical Fixes + Documentation Foundation
**Goal:** Eliminate blocking issues and improve documentation
**Estimated Points:** 8
**Features:**
- Feature 1.1: Fix Binary Name Mismatch (2 pts)
- Feature 1.2: Document Python CLI Installation Step (1 pt)
- Feature 2.2: Create TARGET-PROJECT-QUICK-START.md (3 pts)
- Feature 2.3: Document Hook Setup Prerequisites (2 pts)

**Key Deliverables:**
- Phase 01 preflight no longer fails due to CLI detection
- Complete quick-start guide for external projects
- INSTALL.md updated with all prerequisites

### Sprint 2: Configuration + Validation
**Goal:** Consolidate configuration and add validation tools
**Estimated Points:** 5
**Features:**
- Feature 2.1: Consolidate PYTHONPATH Settings (2 pts)
- Feature 3.2: Add Post-Install Validation Command (3 pts)

**Key Deliverables:**
- Single canonical PYTHONPATH pattern
- Working `devforgeai-validate validate-installation` command

### Sprint 3: Architecture Improvement
**Goal:** Consolidate triple mirror pattern
**Estimated Points:** 5
**Features:**
- Feature 3.1: Consolidate Triple Mirror Pattern (5 pts)

**Key Deliverables:**
- ADR approved and implemented
- Sync script created and integrated
- CI verification in place

## User Stories

### Sprint 1 Stories (8 points)
| ID | Title | Type | Points | Depends On | Status |
|----|-------|------|--------|------------|--------|
| STORY-308 | Fix Binary Name Mismatch in Python CLI | bugfix | 2 | - | Backlog |
| STORY-309 | Document Python CLI Installation as Required Prerequisite | documentation | 1 | STORY-308 | Backlog |
| STORY-311 | Create TARGET-PROJECT-QUICK-START.md Guide | documentation | 3 | STORY-308, STORY-309 | Backlog |
| STORY-312 | Document Hook Setup as Installation Prerequisite | documentation | 2 | STORY-309 | Backlog |

### Sprint 2 Stories (5 points)
| ID | Title | Type | Points | Depends On | Status |
|----|-------|------|--------|------------|--------|
| STORY-310 | Consolidate PYTHONPATH Configuration Patterns | refactor | 2 | - | Backlog |
| STORY-314 | Add Post-Install Validation Command | feature | 3 | STORY-308, STORY-310 | Backlog |

### Sprint 3 Stories (5 points)
| ID | Title | Type | Points | Depends On | Status |
|----|-------|------|--------|------------|--------|
| STORY-313 | Consolidate Triple Mirror Pattern to Single Source of Truth | refactor | 5 | - | Backlog |

### User Value Statements

1. **As a** new user, **I want** the Python CLI to be automatically detected, **so that** Phase 01 preflight doesn't fail
2. **As a** new user, **I want** clear installation prerequisites, **so that** I don't miss required steps
3. **As a** new user, **I want** a quick-start guide, **so that** I can set up DevForgeAI in 5 minutes
4. **As a** developer, **I want** a single source of truth for framework code, **so that** changes only need to be made once
5. **As a** user, **I want** a validation command, **so that** I can verify my installation is correct

## Technical Considerations

### Architecture Impact
- Feature 3.1 requires build process changes (sync script)
- Feature 3.2 adds new CLI command to devforgeai_cli
- No database or API changes

### Technology Decisions
- Python CLI continues as validation tool
- Build-time copy preferred over symlinks (Windows compatibility)
- No new dependencies required

### Security & Compliance
- No security implications (documentation and tooling changes only)
- No new sensitive data handling

### Performance Requirements
- Validation command should complete in < 5 seconds
- No runtime performance impact

## Dependencies

### Internal Dependencies
- [x] **RCA-026:** Binary name mismatch analysis - Complete
- [ ] **ADR-XXX:** Triple Mirror Consolidation - Required for Feature 3.1

### External Dependencies
- None

## Risks & Mitigation

### Risk 1: Triple mirror consolidation breaks existing workflows
- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Create ADR, extensive testing, phased rollout
- **Contingency:** Rollback to current pattern if issues arise

### Risk 2: PYTHONPATH changes break CI/CD
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Test in isolated environment before merging
- **Contingency:** Keep backward compatibility patterns temporarily

### Risk 3: Binary name change breaks existing scripts
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Create backward compatibility alias during transition
- **Contingency:** Document migration path for affected users

### Risk 4: Documentation updates don't cover all use cases
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** User testing with fresh project before release
- **Contingency:** Iterate based on user feedback

## Stakeholders

### Primary Stakeholders
- **Product Owner:** DevForgeAI Team
- **Tech Lead:** Claude
- **Users:** All DevForgeAI adopters

### Additional Stakeholders
- **Contributors:** Framework developers
- **Support:** Users experiencing installation issues

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1-2:  Sprint 1 - Critical fixes + Documentation
Week 3-4:  Sprint 2 - Configuration + Validation
Week 5-6:  Sprint 3 - Architecture (Triple Mirror)
════════════════════════════════════════════════════
Total Duration: 6 weeks
Target Release: 2026-03-31 (Q1 2026)
```

### Key Milestones
- [ ] **Milestone 1:** Week 2 - Phase 01 preflight working, quick-start guide published
- [ ] **Milestone 2:** Week 4 - Validation command available
- [ ] **Milestone 3:** Week 6 - Triple mirror consolidated
- [ ] **Final Release:** 2026-03-31 - All 7 features complete, B+ grade achieved

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 8 | 4 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 5 | 2 | 0 | 0 | 0 |
| Sprint 3 | Not Started | 5 | 1 | 0 | 0 | 0 |
| **Total** | **0%** | **18** | **7** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 18
- **Completed:** 0
- **Remaining:** 18
- **Velocity:** TBD after Sprint 1

## Technical Assessment Summary

**Complexity Score:** 6/10 (Moderate-High)
**Estimated Duration:** 3 sprints (6 weeks)
**ADRs Required:** 1 (Triple Mirror Consolidation)
**Key Risks:** 4 identified with mitigations

### Implementation Order
1. Features 1.1, 1.2, 2.3 (CRITICAL + HIGH documentation) - Sprint 1
2. Feature 2.2 (Quick Start guide) - Sprint 1
3. Feature 2.1 (PYTHONPATH) - Sprint 2
4. Feature 3.2 (Validation command) - Sprint 2
5. Feature 3.1 (Triple Mirror - ADR first) - Sprint 3

---

**Epic Template Version:** 1.0
**Created:** 2026-01-25
**Analysis Source:** Installation Process Grade Analysis
