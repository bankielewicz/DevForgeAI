---
id: brainstorm-data-mapping
title: Brainstorm to Ideation Data Mapping Reference
version: "1.0"
created: 2025-12-21
status: Published
---

# Brainstorm to Ideation Data Mapping

Complete field mapping between brainstorm output and ideation input.

## Overview

This document defines how each field from a brainstorm document maps to ideation session fields, which phases are affected, and what behavior changes occur.

---

## Section 1: Field Mapping Table

### 1.1 Core Fields

| Brainstorm Field | Type | Ideation Field | Phase | Effect |
|------------------|------|----------------|-------|--------|
| `id` | string | `session.brainstorm_id` | All | Reference tracking |
| `title` | string | `session.brainstorm_title` | All | Context display |
| `confidence_level` | enum | `session.skip_discovery` | 1 | HIGH/MEDIUM = skip discovery |
| `problem_statement` | string | `session.problem_statement` | 1 | Skip problem elicitation |
| `target_outcome` | string | `session.business_goals[0]` | 1 | Pre-populate goals |
| `recommended_approach` | string | `session.solution_hints` | 4 | Inform epic structure |

### 1.2 Stakeholder Fields

| Brainstorm Field | Type | Ideation Field | Phase | Effect |
|------------------|------|----------------|-------|--------|
| `primary_stakeholder` | string | `session.primary_user` | 1 | Skip user identification |
| `user_personas` | list | `session.user_personas` | 1 | Skip persona discovery |
| `user_personas[].role` | string | `persona.role` | 1 | Direct mapping |
| `user_personas[].goal` | string | `persona.primary_goal` | 1 | Direct mapping |

### 1.3 Constraint Fields

| Brainstorm Field | Type | Ideation Field | Phase | Effect |
|------------------|------|----------------|-------|--------|
| `budget_range` | string | `session.budget_constraint` | 5 | Pre-populate feasibility |
| `timeline` | string | `session.timeline_constraint` | 5 | Pre-populate feasibility |
| `hard_constraints` | list | `session.constraints` | 5 | Skip constraint discovery |

### 1.4 Requirement Fields

| Brainstorm Field | Type | Ideation Field | Phase | Effect |
|------------------|------|----------------|-------|--------|
| `must_have_capabilities` | list | `session.must_have_requirements` | 2 | Seed requirements list |
| `nice_to_have` | list | `session.should_have_requirements` | 2 | Seed requirements list |
| `critical_assumptions` | list | `session.assumptions` | 5 | Risk assessment input |

---

## Section 2: Mapping Details

### 2.1 Problem Statement Mapping

**Brainstorm:**
```yaml
problem_statement: "Operations team spends 45 minutes per order on manual data entry, resulting in 8% error rate"
```

**Ideation Session:**
```yaml
session:
  problem_statement: "Operations team spends 45 minutes per order on manual data entry, resulting in 8% error rate"
  problem_validated: true
  problem_source: "brainstorm:BRAINSTORM-001"
```

**Phase 1 Behavior:**
- Skip "What problem are you trying to solve?" question
- Display: "Problem from brainstorm: {problem_statement}"
- Ask only: "Is this still accurate?" (validation)

---

### 2.2 User Personas Mapping

**Brainstorm:**
```yaml
user_personas:
  - "Order Clerk: Data entry - Reduce time per order"
  - "Operations Manager: Oversight - Reduce error rate"
  - "Customer: Recipient - Faster order fulfillment"
```

**Ideation Session:**
```yaml
session:
  user_personas:
    - role: "Order Clerk"
      type: "primary_user"
      primary_goal: "Reduce time per order"
      source: "brainstorm"
    - role: "Operations Manager"
      type: "stakeholder"
      primary_goal: "Reduce error rate"
      source: "brainstorm"
    - role: "Customer"
      type: "end_beneficiary"
      primary_goal: "Faster order fulfillment"
      source: "brainstorm"
```

**Phase 1 Behavior:**
- Skip "Who will use this?" questions
- Skip "What are their goals?" questions
- Display: "{count} personas from brainstorm"
- Ask only: "Any personas to add?" (optional)

---

### 2.3 Constraints Mapping

**Brainstorm:**
```yaml
budget_range: "$50K - $200K"
timeline: "Q2 2025"
hard_constraints:
  - "Must integrate with SAP"
  - "Must use existing Oracle DB"
  - "Must comply with SOC 2"
```

**Ideation Session:**
```yaml
session:
  feasibility:
    budget:
      range: "$50K - $200K"
      source: "brainstorm"
    timeline:
      target: "Q2 2025"
      source: "brainstorm"
    constraints:
      - type: "integration"
        description: "Must integrate with SAP"
        source: "brainstorm"
      - type: "technical"
        description: "Must use existing Oracle DB"
        source: "brainstorm"
      - type: "compliance"
        description: "Must comply with SOC 2"
        source: "brainstorm"
```

**Phase 5 Behavior:**
- Skip "What's the budget?" question
- Skip "What's the timeline?" question
- Skip "Any technical constraints?" question
- Display: "Constraints from brainstorm: {count}"
- Ask only: "Any additional constraints?"

---

### 2.4 Requirements Mapping

**Brainstorm:**
```yaml
must_have_capabilities:
  - "API integration for order processing"
  - "Reduce processing time to <5 minutes"
  - "Error rate below 1%"
nice_to_have:
  - "Mobile app for order entry"
  - "Real-time dashboard"
```

**Ideation Session:**
```yaml
session:
  requirements:
    must_have:
      - id: "REQ-001"
        description: "API integration for order processing"
        priority: "MUST"
        source: "brainstorm"
      - id: "REQ-002"
        description: "Reduce processing time to <5 minutes"
        priority: "MUST"
        type: "performance"
        source: "brainstorm"
      - id: "REQ-003"
        description: "Error rate below 1%"
        priority: "MUST"
        type: "quality"
        source: "brainstorm"
    should_have:
      - id: "REQ-004"
        description: "Mobile app for order entry"
        priority: "SHOULD"
        source: "brainstorm"
      - id: "REQ-005"
        description: "Real-time dashboard"
        priority: "SHOULD"
        source: "brainstorm"
```

**Phase 2 Behavior:**
- Pre-populate requirements list
- Display: "Requirements from brainstorm: {must_count} must-have, {should_count} should-have"
- Ask: "Let's expand on these. What details can you add to {REQ-001}?"
- Focus on deepening, not discovering

---

### 2.5 Assumptions Mapping

**Brainstorm:**
```yaml
critical_assumptions:
  - "Users will adopt new system if trained"
  - "API integration is technically feasible"
```

**Ideation Session:**
```yaml
session:
  risk_assessment:
    assumptions:
      - id: "ASMP-001"
        statement: "Users will adopt new system if trained"
        validation_method: "User research"
        source: "brainstorm"
      - id: "ASMP-002"
        statement: "API integration is technically feasible"
        validation_method: "Proof of concept"
        source: "brainstorm"
```

**Phase 5 Behavior:**
- Pre-populate assumptions
- Display: "Assumptions from brainstorm: {count}"
- Ask: "Any assumptions to add or validate?"

---

## Section 3: Phase Behavior Summary

### 3.1 Phase 1: Discovery & Problem Understanding

| Without Brainstorm | With Brainstorm (HIGH) | With Brainstorm (MEDIUM) |
|-------------------|------------------------|--------------------------|
| 5-10 questions | 0 questions (skip) | 1-3 questions (validate) |
| Discover problem | Pre-populated | Validate problem |
| Discover users | Pre-populated | Confirm users |
| Discover goals | Pre-populated | Validate goals |

### 3.2 Phase 2: Requirements Elicitation

| Without Brainstorm | With Brainstorm |
|-------------------|-----------------|
| 15-25 questions | 10-20 questions |
| Start from scratch | Start from must-haves |
| Discover requirements | Deepen requirements |

### 3.3 Phase 3: Complexity Assessment

| Without Brainstorm | With Brainstorm |
|-------------------|-----------------|
| Standard scoring | Standard scoring |
| No change | Brainstorm confidence as input |

### 3.4 Phase 4: Epic & Feature Decomposition

| Without Brainstorm | With Brainstorm |
|-------------------|-----------------|
| Derive structure | Hint from recommended_approach |
| Standard decomposition | Influenced decomposition |

### 3.5 Phase 5: Feasibility & Constraints

| Without Brainstorm | With Brainstorm |
|-------------------|-----------------|
| 5-10 questions | 0-3 questions |
| Discover constraints | Validate constraints |
| Estimate budget/timeline | Use brainstorm values |

### 3.6 Phase 6: Documentation

| Without Brainstorm | With Brainstorm |
|-------------------|-----------------|
| Standard output | Include brainstorm reference |
| No change | Link to source brainstorm |

---

## Section 4: Question Reduction Matrix

### 4.1 Questions Skipped per Field

| Field Present | Questions Saved | Phase |
|---------------|-----------------|-------|
| `problem_statement` | 2-3 | 1 |
| `user_personas` | 3-5 | 1 |
| `target_outcome` | 1-2 | 1 |
| `must_have_capabilities` | 5-10 | 2 |
| `hard_constraints` | 2-3 | 5 |
| `budget_range` | 1-2 | 5 |
| `timeline` | 1-2 | 5 |
| `critical_assumptions` | 2-3 | 5 |

**Total potential savings:** 17-30 questions (out of 40-60 typical)

### 4.2 Confidence Level Effects

| Confidence | Discovery Skip | Validation Questions | Est. Savings |
|------------|----------------|----------------------|--------------|
| HIGH | Full | 1-2 | 8-10 questions |
| MEDIUM | Partial | 3-5 | 5-7 questions |
| LOW | None | Full discovery | 0 questions |

---

## Section 5: Transformation Rules

### 5.1 String to Persona Transformation

**Input (brainstorm):**
```
"Order Clerk: Data entry - Reduce time per order"
```

**Transformation:**
```
1. Split by ": " → ["Order Clerk", "Data entry - Reduce time per order"]
2. Extract role: "Order Clerk"
3. Split remainder by " - " → ["Data entry", "Reduce time per order"]
4. Extract function: "Data entry"
5. Extract goal: "Reduce time per order"
```

**Output (ideation):**
```yaml
persona:
  role: "Order Clerk"
  function: "Data entry"
  primary_goal: "Reduce time per order"
  type: "primary_user"  # Inferred from first position
```

### 5.2 Budget Range Normalization

**Input variations:**
- "$50K - $200K"
- "$50,000 - $200,000"
- "50-200K"
- "Between $50K and $200K"

**Normalized output:**
```yaml
budget:
  min: 50000
  max: 200000
  display: "$50K - $200K"
  currency: "USD"
```

### 5.3 Timeline Normalization

**Input variations:**
- "Q2 2025"
- "June 2025"
- "Within 6 months"
- "This year"

**Normalized output:**
```yaml
timeline:
  target_date: "2025-06-30"  # End of Q2
  flexibility: "quarter"  # Inferred precision
  display: "Q2 2025"
```

---

## Section 6: Edge Cases

### 6.1 Missing Fields

**If brainstorm field is null or empty:**
- Mark field as "needs_discovery"
- Ask standard Phase 1 question for that field
- Don't assume or skip

### 6.2 Conflicting Data

**If user provides different data during ideation:**
- Prompt for clarification
- Allow user to choose: brainstorm value or new value
- Document the change in requirements spec

### 6.3 Partial Brainstorm

**If only some fields populated:**
- Use what's available
- Ask for missing fields
- Note source for each field (brainstorm vs discovered)

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Persona parse fails | Invalid format | Ask as new question |
| Budget parse fails | Non-standard format | Ask for clarification |
| Empty must-haves | No requirements | Run full Phase 2 |
| Conflicting data | User contradicts | Prompt to choose |

---

**Version:** 1.0 | **Status:** Published | **Created:** 2025-12-21
