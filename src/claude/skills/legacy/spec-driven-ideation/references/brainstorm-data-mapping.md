---
id: brainstorm-data-mapping
title: Brainstorm to Ideation Data Mapping Reference
version: "3.0"
created: 2025-12-21
updated: 2026-05-17
status: Published
---

# Brainstorm to Ideation Data Mapping

Complete field mapping between brainstorm output and ideation input.

## Table of Contents

- [Section 1: Field Mapping Table](#section-1-field-mapping-table)
- [Section 2: Mapping Details](#section-2-mapping-details)
- [Section 3: Phase Behavior Summary](#section-3-phase-behavior-summary)
- [Section 4: Question Reduction Matrix](#section-4-question-reduction-matrix)
- [Section 5: Transformation Rules](#section-5-transformation-rules)
- [Section 6: Edge Cases](#section-6-edge-cases)
- [Section 7: Markdown Body Extraction](#section-7-markdown-body-extraction)
- [Section 8: Extended Field Mapping Table](#section-8-extended-field-mapping-table)
- [Section 9: Brainstorm Schema 2.0 (HTML Data Island) Mapping](#section-9-brainstorm-schema-20-html-data-island-mapping)

---

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

### 1.5 Visual Design Context Fields

| Brainstorm Field | Type | Ideation Field | Phase | Effect |
|------------------|------|----------------|-------|--------|
| `design_artifacts.has_mockup` | bool/null | `session.ui_context.has_mockup` | 1 | Detect UI presence |
| `design_artifacts.mockup_path` | string/null | `session.ui_context.mockup_path` | 1 | Path to existing mockup code |
| `design_artifacts.design_source_of_truth` | string/null | `session.ui_context.design_doc_path` | 1 | Path to design.md if exists |
| `design_artifacts.aesthetic_vibe` | string/null | `session.ui_context.aesthetic_vibe` | 2 | Aesthetic direction for UI |
| `design_artifacts.ui_complexity` | enum/null | `session.ui_context.complexity` | 2 | Estimated UI complexity |

**Extraction rules for design_artifacts:**
- All fields are OPTIONAL (graceful degradation if absent)
- If `design_artifacts` key is missing entirely: set all ui_context fields to null
- If `has_mockup` is null: UI decision was deferred — ask during ideation Phase 2
- If `has_mockup` is true AND `design_source_of_truth` is not null: design.md is available for downstream skills
- If `has_mockup` is true AND `design_source_of_truth` is null: mockup exists but design.md not yet generated

### 1.6 Visual Capture Fields

| Brainstorm Field | Type | Ideation Field | Phase | Effect |
|------------------|------|----------------|-------|--------|
| `design_artifacts.screenshots.desktop` | string/null | `session.ui_context.screenshots.desktop` | 1 | Path to desktop screenshot |
| `design_artifacts.screenshots.tablet` | string/null | `session.ui_context.screenshots.tablet` | 1 | Path to tablet screenshot |
| `design_artifacts.screenshots.mobile` | string/null | `session.ui_context.screenshots.mobile` | 1 | Path to mobile screenshot |
| `design_artifacts.suggested_extract_command` | string/null | `session.ui_context.extract_command` | 1 | Pre-built /create-design command with --origin |

**Extraction rules:**
- All fields are OPTIONAL (graceful degradation if absent)
- Screenshots populated only when /create-design --extract --url was previously run
- suggested_extract_command includes --origin for return routing

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

## Section 7: Markdown Body Extraction

**Version:** 2.0 (STORY-292)
**Purpose:** Extract structured data from markdown body sections (in addition to YAML frontmatter).

All markdown body fields are **OPTIONAL** - graceful degradation when section missing.

---

### 7.1 Stakeholder Analysis Table Extraction [OPTIONAL]

**Brainstorm Location:** Section 1: Stakeholder Analysis
**Ideation Field:** `session.stakeholder_analysis` array (ideation stakeholder mapping)

**Input Pattern (markdown table):**
```markdown
| Stakeholder | Influence | Goals | Concerns | Pain Points | Success Criteria | Conflicts |
|-------------|-----------|-------|----------|-------------|------------------|-----------|
| Order Clerk | High | Speed | Complexity | Manual data entry | < 5 min per order | Manager oversight |
| Operations Manager | High | Accuracy | Cost | Error rates | < 1% error rate | Clerk pushback |
```

**Extraction Pattern:**
```
1. Search for "## Section 1: Stakeholder Analysis" OR "## Stakeholder Analysis"
2. Find markdown table (lines starting with "|")
3. Parse header row for column names
4. Required columns: Stakeholder, Influence, Goals, Concerns
5. Optional columns: Pain Points, Success Criteria, Conflicts
6. Parse each data row into structured object
```

**Ideation Session Mapping:**
```yaml
session:
  stakeholder_analysis:
    columns: ["Stakeholder", "Influence", "Goals", "Concerns", "Pain Points", "Success Criteria", "Conflicts"]
    rows:
      - stakeholder: "Order Clerk"
        influence: "High"
        goals: "Speed"
        concerns: "Complexity"
        pain_points: "Manual data entry, repetitive tasks"
        success_criteria: "Process orders in under 5 minutes"
        conflicts: "Manager oversight"
        source: "brainstorm"
      - stakeholder: "Operations Manager"
        influence: "High"
        goals: "Accuracy"
        concerns: "Cost"
        pain_points: "Error rates, training overhead"
        success_criteria: "Reduce error rate below 1%"
        conflicts: "Clerk pushback"
        source: "brainstorm"
    source: "brainstorm:BRAINSTORM-001"
```

**Phase 1 Behavior:**
- Skip "Who are the stakeholders?" questions
- Display: "Stakeholder analysis from brainstorm: {count} stakeholders"
- Ask only: "Any stakeholders to add?" (optional)

**Missing Section Pattern:**
```yaml
# If section not found in brainstorm
session:
  stakeholder_analysis:
    status: "needs_discovery"
    source: null
```

---

### 7.2 Root Cause Analysis (5 Whys) Extraction [OPTIONAL]

**Brainstorm Location:** Section 2: Problem Analysis > Root Cause Analysis
**Note:** Root cause extraction is optional for backward compatibility

**Input Pattern:**
```markdown
### Root Cause Analysis (5 Whys)

**Why 1:** Why do orders take 45 minutes?
→ Manual data entry from multiple sources

**Why 2:** Why is data entry manual?
→ No API integration between systems

**Why 3:** Why no API integration?
→ Legacy systems predate modern integration

**Why 4:** Why haven't legacy systems been updated?
→ Budget constraints and risk aversion

**Why 5:** Why budget constraints?
→ ROI unclear without pilot program

**Root Cause:** Lack of demonstrated ROI for system modernization
```

**Extraction Pattern:**
```
1. Search for "### Root Cause Analysis" OR "5 Whys"
2. Extract patterns: "**Why N:**" followed by question
3. Extract arrow patterns: "→" or "->" followed by answer
4. Preserve order (1-5)
5. Find "**Root Cause:**" for final conclusion
```

**Ideation Session Mapping:**
```yaml
session:
  root_cause_analysis:
    whys:
      - level: 1
        question: "Why do orders take 45 minutes?"
        answer: "Manual data entry from multiple sources"
      - level: 2
        question: "Why is data entry manual?"
        answer: "No API integration between systems"
      - level: 3
        question: "Why no API integration?"
        answer: "Legacy systems predate modern integration"
      - level: 4
        question: "Why haven't legacy systems been updated?"
        answer: "Budget constraints and risk aversion"
      - level: 5
        question: "Why budget constraints?"
        answer: "ROI unclear without pilot program"
    root_cause: "Lack of demonstrated ROI for system modernization"
    source: "brainstorm:BRAINSTORM-001"
```

**Phase 1 Behavior:**
- Skip "What's the root cause?" question
- Display: "Root cause from brainstorm: {root_cause}"
- Ask only: "Is this root cause still accurate?" (validation)

**Missing Section Pattern:**
```yaml
session:
  root_cause_analysis:
    status: "needs_discovery"
    source: null
```

---

### 7.3 Pain Points Extraction [OPTIONAL]

**Brainstorm Location:** Section 2: Problem Analysis > Pain Point Inventory

**Input Pattern:**
```markdown
### Pain Point Inventory

| Pain Point | Severity | Business Impact |
|------------|----------|-----------------|
| 45-minute processing time | High | Lost productivity |
| 8% error rate | Critical | Customer complaints |
| Manual reconciliation | Medium | Overtime costs |
```

**Extraction Pattern:**
```
1. Search for "### Pain Point" OR "Pain Points"
2. Parse markdown table OR bullet list
3. Extract: Pain Point, Severity (if present), Business Impact (if present)
```

**Ideation Session Mapping:**
```yaml
session:
  pain_points:
    - description: "45-minute processing time"
      severity: "High"
      business_impact: "Lost productivity"
      source: "brainstorm"
    - description: "8% error rate"
      severity: "Critical"
      business_impact: "Customer complaints"
      source: "brainstorm"
    - description: "Manual reconciliation"
      severity: "Medium"
      business_impact: "Overtime costs"
      source: "brainstorm"
```

**Phase 1 Behavior:**
- Pre-populate pain points list
- Display: "Pain points from brainstorm: {count}"
- Ask: "Any pain points to add or prioritize?"

**Missing Section Pattern:**
```yaml
session:
  pain_points:
    status: "needs_discovery"
    source: null
```

---

### 7.4 Failed Solutions Extraction [OPTIONAL]

**Brainstorm Location:** Section 2: Problem Analysis > What Has Already Been Tried

**Input Pattern:**
```markdown
### What Has Already Been Tried (Failed Solutions)

| Solution | Why It Failed | Lessons Learned |
|----------|---------------|-----------------|
| Offshore data entry | Quality issues, time zone delays | Need local control |
| Excel macros | Maintenance nightmare | Avoid custom scripts |
| Part-time hires | Training costs exceeded savings | Automation preferred |
```

**Extraction Pattern:**
```
1. Search for "Failed Solutions" OR "What Has Already Been Tried"
2. Parse markdown table OR bullet list
3. Extract: Solution, Why It Failed, Lessons Learned
```

**Ideation Session Mapping:**
```yaml
session:
  failed_solutions:
    - solution: "Offshore data entry"
      failure_reason: "Quality issues, time zone delays"
      lessons_learned: "Need local control"
      source: "brainstorm"
    - solution: "Excel macros"
      failure_reason: "Maintenance nightmare"
      lessons_learned: "Avoid custom scripts"
      source: "brainstorm"
    - solution: "Part-time hires"
      failure_reason: "Training costs exceeded savings"
      lessons_learned: "Automation preferred"
      source: "brainstorm"
```

**Phase 2 Behavior:**
- Skip solutions that have already failed
- Display: "Failed approaches from brainstorm: {count}"
- Inform epic structure: avoid similar patterns

**Missing Section Pattern:**
```yaml
session:
  failed_solutions:
    status: "needs_discovery"
    source: null
```

---

### 7.5 Hypothesis Register Extraction [OPTIONAL]

**Brainstorm Location:** Section 4: Hypothesis Register
**Note:** Hypothesis extraction is optional for backward compatibility
**Fields:** ID, hypothesis statement text, Validation Method, Success Criteria

**Input Pattern:**
```markdown
## Section 4: Hypothesis Register

| ID | Hypothesis | Validation Method | Success Criteria |
|----|------------|-------------------|------------------|
| H1 | IF we automate order entry THEN processing time will drop below 5 minutes | Pilot with 100 orders | < 5 min avg |
| H2 | IF we add validation rules THEN error rate will drop below 1% | A/B test | < 1% error rate |
```

**Extraction Pattern:**
```
1. Search for "## Section 4: Hypothesis" OR "Hypothesis Register"
2. Parse markdown table
3. Extract: ID, Hypothesis, Validation Method, Success Criteria
4. Support IF-THEN pattern: Extract condition and expected outcome
```

**Ideation Session Mapping:**
```yaml
session:
  hypotheses:
    - id: "H1"
      hypothesis: "IF we automate order entry THEN processing time will drop below 5 minutes"
      condition: "we automate order entry"
      expected_outcome: "processing time will drop below 5 minutes"
      validation_method: "Pilot with 100 orders"
      success_criteria: "< 5 min avg"
      status: "pending"
      source: "brainstorm"
    - id: "H2"
      hypothesis: "IF we add validation rules THEN error rate will drop below 1%"
      condition: "we add validation rules"
      expected_outcome: "error rate will drop below 1%"
      validation_method: "A/B test"
      success_criteria: "< 1% error rate"
      status: "pending"
      source: "brainstorm"
```

**Phase 4 Behavior:**
- Inform epic structure around hypothesis validation
- Display: "Hypotheses from brainstorm: {count}"
- Suggest: Create validation stories for each hypothesis

**Missing Section Pattern:**
```yaml
session:
  hypotheses:
    status: "needs_discovery"
    source: null
```

---

### 7.6 Impact-Effort Matrix Extraction [OPTIONAL]

**Brainstorm Location:** Section 5: Impact-Effort Matrix
**Note:** Matrix extraction is optional, prioritization optional for backward compatibility

**Input Pattern:**
```markdown
## Section 5: Impact-Effort Matrix

### Quick Wins (High Impact, Low Effort)
- API integration for order lookup
- Auto-fill customer data

### Major Projects (High Impact, High Effort)
- Full workflow automation
- Legacy system replacement

### Fill-ins (Low Impact, Low Effort)
- UI improvements
- Report generation

### Thankless Tasks (Low Impact, High Effort)
- Full audit trail
- Complete data migration
```

**Extraction Pattern:**
```
1. Search for "## Section 5: Impact-Effort" OR "Impact-Effort Matrix"
2. Identify quadrant headers: Quick Wins, Major Projects, Fill-ins, Thankless Tasks
3. Extract bullet list items under each quadrant
4. Alternative: Support MoSCoW format (Must/Should/Could/Won't)
```

**Ideation Session Mapping:**
```yaml
session:
  impact_effort_matrix:
    quick_wins:  # High Impact, Low Effort
      - name: "API integration for order lookup"
        impact_score: 8
        effort_score: 2
      - name: "Auto-fill customer data"
        impact_score: 7
        effort_score: 3
    major_projects:  # High Impact, High Effort
      - name: "Full workflow automation"
        impact_score: 9
        effort_score: 8
      - name: "Legacy system replacement"
        impact_score: 10
        effort_score: 9
    fill_ins:  # Low Impact, Low Effort
      - name: "UI improvements"
        impact_score: 3
        effort_score: 2
      - name: "Report generation"
        impact_score: 4
        effort_score: 3
    thankless_tasks:  # Low Impact, High Effort
      - name: "Full audit trail"
        impact_score: 3
        effort_score: 7
      - name: "Complete data migration"
        impact_score: 4
        effort_score: 9
    source: "brainstorm:BRAINSTORM-001"
```

**Alternative MoSCoW Mapping:**
```yaml
session:
  prioritization:
    method: "MoSCoW"
    must_have: [...]
    should_have: [...]
    could_have: [...]
    wont_have: [...]
    source: "brainstorm"
```

**Phase 4 Behavior:**
- Pre-prioritize epic features
- Display: "Prioritization from brainstorm: {quick_wins_count} quick wins identified"
- Suggest: Start with Quick Wins for early value

**Missing Section Pattern:**
```yaml
session:
  impact_effort_matrix:
    status: "needs_discovery"
    source: null
```

---

### 7.7 Recommended Sequence Extraction [OPTIONAL]

**Brainstorm Location:** Section 6: Recommended Sequence
**Output Format:** `implementation_sequence` as ordered list/array with rationale

**Input Pattern:**
```markdown
## Section 6: Recommended Sequence

### Recommended Implementation Order

1. **API Integration** - Quick win, enables other features
   - Rationale: Foundation for automation
   - Dependencies: None

2. **Validation Rules** - Addresses critical error rate
   - Rationale: Immediate quality improvement
   - Dependencies: API Integration

3. **Workflow Automation** - Major impact, needs foundation
   - Rationale: Full productivity gains
   - Dependencies: API Integration, Validation Rules
```

**Extraction Pattern:**
```
1. Search for "## Section 6: Recommended" OR "Recommended Sequence"
2. Extract numbered list items
3. Parse: Step name (bold), description, rationale, dependencies
4. Preserve order (1, 2, 3...)
```

**Ideation Session Mapping:**
```yaml
session:
  recommended_sequence:
    - order: 1
      name: "API Integration"
      description: "Quick win, enables other features"
      rationale: "Foundation for automation"
      dependencies: []
      source: "brainstorm"
    - order: 2
      name: "Validation Rules"
      description: "Addresses critical error rate"
      rationale: "Immediate quality improvement"
      dependencies: ["API Integration"]
      source: "brainstorm"
    - order: 3
      name: "Workflow Automation"
      description: "Major impact, needs foundation"
      rationale: "Full productivity gains"
      dependencies: ["API Integration", "Validation Rules"]
      source: "brainstorm"
```

**Phase 4 Behavior:**
- Pre-sequence epic features
- Display: "Implementation sequence from brainstorm: {count} phases"
- Ask: "Follow this sequence or adjust?"

**Missing Section Pattern:**
```yaml
session:
  recommended_sequence:
    status: "needs_discovery"
    source: null
```

---

### 7.8 Problem Refinement Extraction [OPTIONAL]

**Brainstorm Location:** Section 3: Problem Refinement (or similar)
**Note:** Problem refinement extraction is optional for backward compatibility
**Fields:** original_problem, refined_problem, refinement_rationale

**Input Pattern:**
```markdown
## Problem Refinement

### Original Problem Statement
Operations team spends 45 minutes per order on manual data entry, resulting in 8% error rate.

### Refined Problem Statement
Manual order processing creates productivity bottleneck and quality issues due to lack of system integration.

### Refinement Rationale
The original problem focused on symptoms (time, errors). The refined problem identifies root cause (lack of integration) which enables better solution targeting.
```

**Extraction Pattern:**
```
1. Search for "## Problem Refinement" OR "### Problem Refinement"
2. Find "Original Problem" subsection or labeled text
3. Find "Refined Problem" subsection or labeled text
4. Find "Rationale" or "Refinement Rationale" subsection
5. Extract text content from each subsection
```

**Ideation Session Mapping:**
```yaml
session:
  problem_refinement:
    original_problem: "Operations team spends 45 minutes per order on manual data entry, resulting in 8% error rate."
    refined_problem: "Manual order processing creates productivity bottleneck and quality issues due to lack of system integration."
    refinement_rationale: "The original problem focused on symptoms (time, errors). The refined problem identifies root cause (lack of integration) which enables better solution targeting."
    source: "brainstorm:BRAINSTORM-001"
```

**Phase 1 Behavior:**
- Use refined problem as primary problem statement
- Display: "Problem refined from brainstorm"
- Show: "Original: {original_problem}"
- Show: "Refined: {refined_problem}"
- Ask only: "Is this refined problem accurate?" (validation)

**Missing Section Pattern:**
```yaml
session:
  problem_refinement:
    status: "needs_discovery"
    source: null
```

---

### 7.9 Backward Compatibility

**Existing Brainstorms (BRAINSTORM-001 through BRAINSTORM-006):**

All markdown body extraction fields are **OPTIONAL**. When processing existing brainstorms:

1. **If section exists:** Extract and map to ideation session
2. **If section missing:** Set `status: "needs_discovery"`, continue processing
3. **Never fail:** Graceful degradation for all sections

**Version Detection:**
```yaml
# Detect brainstorm version from content
IF frontmatter contains all Section 7 fields:
    brainstorm_version = "2.0"
ELIF frontmatter contains core fields only:
    brainstorm_version = "1.0"
    # All Section 7 fields will be "needs_discovery"
```

**Processing Order:**
1. Extract YAML frontmatter (Section 1-6 fields) - REQUIRED
2. Attempt markdown body extraction (Section 7 fields) - OPTIONAL
3. Set `needs_discovery` for any missing sections
4. Continue to ideation with available data

---

## Section 8: Extended Field Mapping Table

### 8.1 Markdown Body Fields (NEW in v2.0)

| Brainstorm Section | Type | Ideation Field | Phase | Effect |
|--------------------|------|----------------|-------|--------|
| Stakeholder Analysis table | table | `session.stakeholder_analysis` | 1 | Skip stakeholder discovery |
| Root Cause Analysis (5 Whys) | list | `session.root_cause_analysis` | 1 | Skip root cause questions |
| Pain Point Inventory | table/list | `session.pain_points` | 1 | Pre-populate pain points |
| Problem Refinement | text | `session.problem_refinement` | 1 | Use refined problem statement |
| Failed Solutions | table/list | `session.failed_solutions` | 2 | Inform solution avoidance |
| Hypothesis Register | table | `session.hypotheses` | 4 | Guide validation stories |
| Impact-Effort Matrix | lists | `session.impact_effort_matrix` | 4 | Pre-prioritize features |
| Recommended Sequence | list | `session.recommended_sequence` | 4 | Pre-sequence implementation |

### 8.2 Questions Saved per Markdown Body Field

| Field Present | Questions Saved | Phase |
|---------------|-----------------|-------|
| `stakeholder_analysis` | 3-5 | 1 |
| `root_cause_analysis` | 2-3 | 1 |
| `pain_points` | 2-4 | 1 |
| `problem_refinement` | 2-3 | 1 |
| `failed_solutions` | 1-2 | 2 |
| `hypotheses` | 2-4 | 4 |
| `impact_effort_matrix` | 3-5 | 4 |
| `recommended_sequence` | 2-3 | 4 |

**Total additional savings (v2.0):** 17-29 questions

---

## Section 9: Brainstorm Schema 2.0 (HTML Data Island) Mapping

**Applies to:** `.brainstorm.html` documents produced by `spec-driven-brainstorming`
(ADR-065). Their machine-readable data lives in an embedded JSON island
(`<script type="application/json" id="brainstorm-data">`) validated by
`brainstorm.schema.json` **v2.0**.

> **Terminology note:** "v2.0" here means the *brainstorm data-island schema*
> (`brainstorm.schema.json` v2.0). It is **not** the Section 7/8 "v2.0" — that older
> label referred to STORY-292 Markdown-body extraction for legacy `.md` documents.
> Sections 1-8 above remain authoritative for legacy `.brainstorm.md` inputs; Section 9
> is authoritative for `.brainstorm.html` inputs. The
> `brainstorm-handoff-workflow.md` §2.1a extractor branches on file extension and
> produces the context variable described here.

### 9.1 Core Field Mapping (v2.0 data island -> ideation session)

| v2.0 data-island path | Ideation session field | Phase | Notes |
|-----------------------|-------------------------|-------|-------|
| `id`, `title` | `session.brainstorm_id`, `session.brainstorm_title` | All | Reference tracking |
| `confidence_level` | `session.brainstorm_input.confidence_level` | 1 | HIGH/MEDIUM = skip discovery |
| `problem_statement` | `session.problem_statement` | 1 | Skip problem elicitation |
| `opportunity.target_outcome` | `session.business_goals[0]` | 1 | Pre-populate goals |
| `handoff.recommended_approach` | `session.solution_hints` | 4 | Inform epic structure |
| `handoff.critical_assumptions` | `session.assumptions` | 5 | Risk assessment input |
| `handoff.open_questions` | `session.open_questions` | 5-6 | Carried into validation / output |
| `stakeholders.primary_stakeholder` | `session.primary_user` | 1 | Skip user identification |
| `stakeholders.registry[]` | `session.stakeholder_registry` | 1-2 | influence / interest / RACI -- see 9.5 |
| `constraints_scope.budget_range` | `session.feasibility.budget` | 5 | Pre-populate feasibility |
| `constraints_scope.timeline` | `session.feasibility.timeline` | 5 | Pre-populate feasibility |
| `constraints_scope.hard_constraints` | `session.constraints` | 5 | Skip constraint discovery |
| `constraints_scope.out_of_scope[]` | `session.scope_boundaries.out_of_scope` | 2 | `{item, rationale}` objects |
| `requirements.functional[]` | `session.must_have_requirements` (seed) | 2-3 | `FR-NNN` with `priority` |
| `requirements.nfrs[]` | `session.nfr_requirements` (seed) | 3 | `NFR-NNN` with `category`, `metric` |
| `requirements.glossary[]` | `session.glossary` | 3 | `{term, definition}` |
| `requirements.assumptions[]` | `session.assumptions_register` | 3-5 | Phase-08 assumptions register |
| `risk_analysis.risks[]` | `session.risk_register` (seed) | 3-5 | `RISK-NNN` -- see 9.3 |
| `prioritization.deferred_ideas[]` | `session.idea_backlog` (seed) | 2-5 | `DEF-NNN` -- see 9.2 |
| `prioritization.release_roadmap[]` | `session.milestone_roadmap` (seed) | 3-5 | see 9.4 |
| `prioritization.must_have_capabilities` | `session.moscow_priority.must` | 3 | MoSCoW |
| `prioritization.should_have` / `could_have` / `wont_have` | `session.moscow_priority.*` | 3 | MoSCoW |
| `prioritization.recommended_sequence[]` | `session.recommended_sequence` | 4 | Pre-sequence implementation |
| `design_artifacts.*` | `session.ui_context.*` | 1-2 | Same rules as Section 1.5 |

### 9.2 Deferred Ideas Register Mapping (DEF-NNN -> idea backlog)

Each `prioritization.deferred_ideas[]` item maps **1:1** into the ideation idea backlog.
This is the structural fix for the data-loss defect: ideas the brainstorm intentionally
kept out of the MVP MUST survive into ideation rather than being dropped at the handoff.

| v2.0 field | Idea-backlog field | Carried |
|------------|--------------------|---------|
| `id` (`DEF-NNN`) | `id` | Verbatim |
| `description` | `description` | Verbatim |
| `why_deferred` | `why_deferred` | Verbatim |
| `business_value` | `business_value` | Verbatim |
| `mvp_dependency` | `mvp_dependency` | Verbatim |
| `revisit_when` | `revisit_when` | Verbatim |
| `source_phase` | `source` | Prefixed: `brainstorm:{brainstorm_id}:{source_phase}` |
| `status` | `status` | Verbatim (`open`/`promoted`/`rejected`) |

Ideation writes these to `devforgeai/specs/ideation/{project}-idea-backlog.md` in
Phase 05 (see `assets/templates/idea-backlog-template.md`). Ideation MUST NOT discard
any `deferred_ideas[]` item.

### 9.3 Risk Register Mapping (RISK-NNN)

Each `risk_analysis.risks[]` item maps 1:1 into the ideation risk register:
`id` (`RISK-NNN`), `description`, `likelihood`, `impact`, `severity`, `mitigation`,
`owner` are carried verbatim. The register is rendered into the PM-plan output. When no
brainstorm is present, the risk register is elicited during Phase 03 instead.

### 9.4 Release Roadmap Mapping

`prioritization.release_roadmap[]` (phased releases -- MVP / Release 2 / Future) maps
into `session.milestone_roadmap`, rendered into the PM-plan output. When no brainstorm is
present, the roadmap is derived from MoSCoW priority + `scope.future` during Phase 03.

### 9.5 Stakeholder Registry Mapping

`stakeholders.registry[]` carries `{id, name_or_role, category, influence, interest,
raci, goals, concerns}`. Ideation keeps the full registry as `session.stakeholder_registry`
AND derives lightweight personas (`derive_personas()`) for backward compatibility with
phases that consume `session.user_personas`.

### 9.6 Empty or Absent v2.0 Fields

All v2.0 fields are OPTIONAL. When a field is absent or its array is empty:
- Set the corresponding ideation register to an empty list (do NOT fail).
- The register is then populated by ideation's own elicitation steps.
- Legacy `.brainstorm.md` (v1.0) inputs have no `deferred_ideas`, `risks`, or
  `release_roadmap` at all -- those registers always start empty for v1.0 inputs.

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Persona parse fails | Invalid format | Ask as new question |
| Budget parse fails | Non-standard format | Ask for clarification |
| Empty must-haves | No requirements | Run full Phase 2 |
| Conflicting data | User contradicts | Prompt to choose |
| Table parse fails | Malformed markdown | Set `needs_discovery`, continue |
| 5 Whys incomplete | Less than 5 levels | Use available, note gap |
| Matrix section missing | No quadrant headers | Set `needs_discovery`, continue |
| Sequence incomplete | Missing rationale | Extract names only, continue |

---

**Version:** 3.0 | **Status:** Published | **Created:** 2025-12-21 | **Updated:** 2026-05-17 (ADR-065 -- brainstorm schema 2.0 HTML data-island mapping)
