# Stakeholder Matrix - Quick Reference

## Stakeholder Groups at a Glance

### Primary Stakeholders (Decision Authority)

| Stakeholder | Role | Key Metric | Influence | Veto Power |
|---|---|---|---|---|
| **Framework Maintainers** | Architecture, quality gates, ADR approval | Zero architectural violations | HIGH | YES - Can block releases |
| **Product Manager** | Prioritization, roadmap, epic planning | Value delivered per sprint | HIGH | YES - Controls sprint plan |
| **Release Lead** | Version management, compatibility | Uptime, successful upgrades | MEDIUM-HIGH | YES - Can delay release |

### Secondary Stakeholders (Users & Beneficiaries)

| Stakeholder | Role | Key Metric | Influence | Engagement |
|---|---|---|---|---|
| **End Users** (Dev teams) | Daily framework users | Time saved, quality gates | MEDIUM | Feature requests, feedback |
| **Claude Community** | Potential adopters | Adoption rate, market share | MEDIUM | Market evaluation |
| **Subagent Developers** | Extension creators | Ecosystem tools, plugins | MEDIUM | Open source contributions |

### Tertiary Stakeholders (Affected Parties)

| Stakeholder | Role | Key Metric | Influence | Mode |
|---|---|---|---|---|
| **Documentation Team** | Tutorials, guides, migration docs | Doc currency, user adoption | LOW-MEDIUM | Proactive updates |
| **QA/Testing** | Validation, regression detection | Coverage %, test quality | MEDIUM | Quality gates |
| **Security Officers** | Vulnerability prevention, audits | Security reviews, compliance | MEDIUM | Architecture reviews |
| **Support/Onboarding** | User help, troubleshooting | Time to first story, NPS | LOW-MEDIUM | UX recommendations |
| **Community Contributors** | OSS contributions, proposals | Contribution volume | LOW | Pull requests |
| **Educators** | Training, certifications, courses | Market adoption | LOW | Course materials |

---

## Conflict Summary (8 Major Conflicts)

| # | Conflict | Primary Party | Secondary Party | Severity | Status |
|---|---|---|---|---|---|
| 1 | Innovation vs. Stability | PM wants features | Release Lead wants stability | HIGH | Active |
| 2 | Constraints vs. Flexibility | Maintainers enforce rules | Users want shortcuts | HIGH | Active |
| 3 | Generalist vs. Specialized | Meta-framework design | Stack-specific requests | MEDIUM | Active |
| 4 | Complexity vs. Usability | Feature-rich skills | New user confusion | MEDIUM | Active |
| 5 | Token Budget vs. Features | Size constraints (1000 lines) | Skill completeness | MEDIUM | Active |
| 6 | Speed vs. Documentation | Fast iteration | Doc falls out-of-date | MEDIUM | Active |
| 7 | Tool Privilege vs. Utility | Security/least privilege | Subagent functionality | MEDIUM | Active |
| 8 | Compatibility vs. Debt Cleanup | Breaking changes | Fixing architectural issues | HIGH | Emerging |

---

## Stakeholder Needs by Category

### Pain Points (What's Broken)
- **End Users**: Learning curve too steep; quality gate failures unclear
- **New Adopters**: Setup process complex (Python 3.10, Node.js, Git required)
- **Documentation Team**: Docs fall out-of-sync with releases
- **Subagent Devs**: Unclear tool privilege requirements
- **QA**: Complex skill interactions hard to test

### Desires (What's Wanted)
- **Product Manager**: Clearer ROI metrics; feature prioritization framework
- **Release Lead**: Backward compatibility guarantees; smooth upgrade paths
- **End Users**: Stack-specific optimizations; debugging guides
- **Support Team**: Simplified command set; interactive wizard
- **Educators**: Framework stability; certification program recognition

### Constraints (What's Required)
- **Maintainers**: Architectural integrity; immutable context files; zero tech debt
- **Security**: No hardcoded secrets; least privilege tool access; audit trails
- **Framework**: Token budget limits (skills < 1000 lines); context windows
- **Quality**: 95% coverage (business logic); no Critical/High violations
- **Users**: No manual CLAUDE.md merges required; automated migrations

---

## Decision Matrix: Who Decides What?

```
Feature Request
    ↓
User Proposes → Support/PM gather requirements
    ↓
Does it fit framework philosophy? → Maintainers decide YES/NO
    ↓ YES
Is it new core skill or enhancement? → PM prioritizes in roadmap
    ↓ FEATURE SELECTED
Create story in sprint → Development team implements
    ↓
Does it pass quality gates? → QA/Security approve
    ↓ APPROVED
Release in next version → Release Lead coordinates
    ↓
Document changes → Documentation team updates guides
```

---

## Communication Plan Template

| Stakeholder Group | Communication Frequency | Format | Message Type |
|---|---|---|---|
| Maintainers | Weekly sync | Architecture review | Technical decisions, ADRs |
| Product Manager | Daily standup | Metrics, roadmap | Progress, blockers, priorities |
| Release Lead | Release-time | Version plan | Breaking changes, migration path |
| End Users | Monthly newsletter | Email, changelog | New features, tips, examples |
| QA/Testing | Per story | Acceptance criteria | Test requirements, coverage goals |
| Support Team | Weekly meeting | Feedback loop | Common issues, documentation gaps |
| Community | Quarterly update | Blog, forum | Roadmap, contribution process |
| Security | Per release | Audit report | Compliance, vulnerability fixes |

---

## Escalation Path for Conflicts

**Level 1: Disagreement Between Team Members**
- Documented positions (1 page each)
- Discussion in their respective working groups
- Attempt consensus

**Level 2: Escalation to Group Leads**
- Maintainer lead
- Product manager
- Release lead
- Discuss alternatives
- Vote if no consensus (majority + maintainer can veto)

**Level 3: Escalation to Stakeholder Board**
- Create ADR if architectural impact
- Advisory board review (user reps, contributor rep, educator rep)
- Document decision and rationale
- Implement with monitoring plan

**Level 4: External Resolution** (if needed)
- Request community feedback (GitHub discussion)
- Evaluate market impact
- Revisit decision in next quarter

---

## Stakeholder Health Checks

### Quarterly Review Questions

**For Maintainers**:
- Are we maintaining architectural integrity? (Yes/No)
- Is technical debt increasing? (Defer trends up/down?)
- Are quality gates being respected? (% HALT violations?)

**For Product Manager**:
- Are we delivering business value? (Stories completed vs. planned?)
- Is roadmap visible and trusted? (Stakeholder alignment score?)
- Are we balancing innovation and stability? (Feature:bugfix ratio)

**For End Users**:
- Is framework saving time? (Quantify: time before/after)
- Are quality gates helping or hindering? (Perception: helpful/restrictive)
- Are we addressing top pain points? (Feature request trends)

**For QA/Testing**:
- Are we catching regressions? (Bugs found in testing vs. production)
- Is coverage sustainable? (Coverage trends over time)
- Are acceptance criteria clear? (% stories requiring clarification)

**For Support/Onboarding**:
- How many teams reach "first story"? (Conversion rate)
- What's the most common blocker? (Support ticket analysis)
- Are quality gate HALT messages helpful? (User feedback on clarity)

**For Documentation**:
- Is documentation current? (Date last verified vs. actual release date)
- What docs get most views? (Analytics on tutorial/guide popularity)
- Are examples working? (User reports on outdated examples)

---

## Stakeholder Engagement Model

### How to Involve Each Stakeholder Group

**Maintainers**:
- ADR reviews for architectural changes
- Architecture decision board meetings
- Code review on critical PRs

**Product Manager**:
- Sprint planning sessions
- Roadmap review meetings
- Feature proposal evaluations

**End Users**:
- Monthly feature feedback survey
- Quarterly user interviews
- Beta testing new features

**QA/Testing**:
- Acceptance criteria reviews
- Test plan reviews
- Post-release regression testing

**Support Team**:
- Weekly issue triage
- Documentation review before releases
- User feedback synthesis

**Documentation Team**:
- Part of release planning (what needs docs?)
- Example code reviews for accuracy
- Migration guide creation for breaking changes

**Community Contributors**:
- Contribution guidelines in README
- Good first issue tracking
- Recognition program (contributor hall of fame)

---

**Last Updated**: 2025-12-22
**Review Cycle**: Quarterly (next: 2026-01-22)
