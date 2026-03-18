# Technical Assessment Guide

Guide for evaluating technical complexity, architecture impact, and risk assessment of epics and features.

---

## Overview

Technical assessment evaluates architecture impact, technology requirements, integration complexity, and risk factors. This guide helps the architect-reviewer subagent and technical leads systematically assess epics before implementation.

**Key Principle:** Assessment validates alignment with existing architecture, identifies required ADRs, and flags risks early.

---

## Complexity Scoring Reference

For the **unified complexity scoring system**, see complexity-assessment-workflow.md (scoring procedure) and complexity-assessment-matrix.md (detailed rubric with examples and legacy scale mapping).

The unified system uses a **0-60 scale** with **5 tiers** (Trivial, Low, Moderate, High, Critical) and **4 dimensions** (Functional, Technical, Team/Org, NFR).

---

## Quick Reference

See complexity-assessment-matrix.md for full tier definitions and scoring ranges.

---

## Assessment Dimensions

### Dimension 1: Technology Stack Impact

**Questions to Ask:**
1. Are new technologies required? (Y/N)
2. How many new technologies? (0, 1-2, 3+)
3. Are proposed technologies in approved tech-stack.md? (Y/N/Needs ADR)
4. Learning curve for team? (None, Low, Medium, High)
5. Long-term maintenance burden? (Low, Medium, High)

**Framework Integration - MUST Check tech-stack.md:**

```markdown
IF technology in tech-stack.md:
  ✅ APPROVED (no action)

IF technology NOT in tech-stack.md:
  ⚠️ REQUIRES ADR
  Action: Flag in assessment, require ADR creation

IF multiple new technologies (3+):
  🛑 MAJOR DECISION
  Action: Require full architecture review
```

---

### Dimension 2: Architecture Changes

**Questions to Ask:**
1. New services/layers required? (Y/N)
2. Changes to existing architecture? (Y/N)
3. Impact on architecture-constraints.md rules? (None/Minor/Major)
4. Violates layer boundaries? (Y/N)
5. Creates circular dependencies? (Y/N)

**Framework Integration - MUST Check architecture-constraints.md:**

```markdown
IF violates layer boundaries:
  🛑 BLOCK - Cannot proceed

IF creates circular dependencies:
  🛑 BLOCK - Cannot proceed

IF extends existing boundaries:
  ⚠️ FLAG - May need ADR

IF respects all constraints:
  ✅ APPROVED - Continue
```

---

### Dimension 3: Integration Complexity

**Questions to Ask:**
1. External systems to integrate? (Y/N)
2. Number of integrations? (1, 2-3, 4+)
3. Integration type? (REST API, SOAP, gRPC, webhooks, real-time)
4. Data transformation required? (Y/N)
5. Error handling complexity? (Standard, Custom, Very complex)

---

### Dimension 4: Data Modeling Complexity

**Questions to Ask:**
1. New entity types required? (0, 1-2, 3-5, 6+)
2. Entity relationships? (Simple 1:1/1:M, Complex M:M, Graph/Network)
3. Schema changes to existing data? (None, Minor, Major, Migration required)
4. Data consistency requirements? (Eventual, Strong, ACID)

---

### Dimension 5: Testing Complexity

**Questions to Ask:**
1. New test types needed? (Unit, Integration, E2E, Performance, Security, Chaos)
2. Mock/stub complexity? (Simple mocks, Complex async mocks, Distributed mocks)
3. Test infrastructure required? (None, Minimal, Significant, Complex)

---

### Dimension 6: Security Considerations

**Questions to Ask:**
1. Handles authentication/authorization? (Y/N)
2. Handles sensitive data? (PII, financial, health)
3. Compliance requirements? (GDPR, PCI DSS, HIPAA, SOC 2)
4. Cryptography required? (Y/N, what type)

**Framework Integration - MUST Check anti-patterns.md:**

```markdown
FORBIDDEN: Hardcoded secrets → Use environment variables
FORBIDDEN: SQL concatenation → Use parameterized queries
FORBIDDEN: Weak cryptography → Use SHA256+, AES-256+
FORBIDDEN: Direct instantiation → Use Dependency Injection
```

---

## Risk Identification Matrix

### Technology Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Unproven technology | Low-Medium | High | Proof-of-concept phase, fallback plan |
| Vendor lock-in | Medium | High | Multi-vendor evaluation, contract review |
| Learning curve | Medium | Medium | Team training, pair programming |

### Integration Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Third-party API instability | Medium | High | SLA monitoring, circuit breakers |
| Rate limiting | Medium | Medium | Request queuing, backoff strategy |
| Webhook delivery failures | Medium | Medium | Retry with exponential backoff, DLQ |

### Data Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Data loss during migration | Low | Critical | Backup strategy, dry-run before cutover |
| Data inconsistency | Low-Medium | High | Consistency checks, reconciliation |
| Data privacy violations | Low | Critical | Data classification, encryption, audit trail |

---

## Context File Validation Process

**IF context files exist in `devforgeai/specs/context/`:**

1. Read all 6 context files
2. For each proposed technology/architecture:
   - VALIDATE against tech-stack.md
   - VALIDATE against architecture-constraints.md
   - VALIDATE against dependencies.md
   - VALIDATE against anti-patterns.md
3. If any validation FAILS:
   - FLAG in assessment as "REQUIRES ADR" or "BLOCKED"
   - Do NOT proceed with assumption of approval

---

## Output Format for Architect-Reviewer

```markdown
## Technical Assessment: [Epic/Feature Name]

### Overall Complexity Score
**Overall**: [Score]/60 ([Tier]: Trivial/Low/Moderate/High/Critical)
**Justification**: [1-2 sentences explaining score]

### Key Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|

### Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

### Recommendations
[Based on complexity tier]

### Approval Status
**Ready to Proceed**: [Y/N]
```

---

## Self-Validation Checklist

**Before finalizing assessment:**
- [ ] Complexity score justified by assessment dimensions
- [ ] All technologies checked against tech-stack.md
- [ ] All architecture changes checked against architecture-constraints.md
- [ ] All integrations checked against dependencies.md
- [ ] Security patterns checked against anti-patterns.md
- [ ] All risks documented with probability/impact/mitigation
- [ ] Prerequisites clearly listed
- [ ] ADRs identified for all significant decisions

---

**Last Updated:** 2026-02-17
**Version:** 2.0
**Framework:** DevForgeAI Orchestration
