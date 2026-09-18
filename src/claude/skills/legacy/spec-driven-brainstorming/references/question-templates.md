---
description: Centralized AskUserQuestion shape templates referenced from all 11 phase files. Phase files name a template ID and supply only the question text + header; the canonical option set + descriptions live here.
version: "1.0"
created: 2026-05-13
type: reference
---

# Question Templates for spec-driven-brainstorming

The 11 phase files each contain multiple `AskUserQuestion` invocations. Across the skill, ~50 such calls cluster into 5 recurring shapes. Each phase references a template by ID (`QT-1`..`QT-5`) and supplies the unique parameters (question text, header label, and any per-call option text overrides). This file is the canonical source for the shapes.

## How phase files reference these templates

A phase file step that previously inlined a full AskUserQuestion block:

```
EXECUTE:
  AskUserQuestion:
    questions:
      - question: "How severe is the issue?"
        header: "Severity"
        multiSelect: false
        options:
          - label: "Critical"
            description: "Business cannot function properly"
          - label: "High"
            description: "Significant negative impact"
          - label: "Medium"
            description: "Noticeable but manageable"
          - label: "Low"
            description: "Minor inconvenience"
```

Now references the template + supplies only the unique pieces:

```
EXECUTE:
  AskUserQuestion: template=QT-2
    question_text: "How severe is the issue?"
    header: "Severity"
```

The orchestrator MUST expand `template=QT-2` to the canonical block below at runtime. Custom override of any single option label or description is allowed by adding an `overrides:` block — see §"Override Conventions" at the bottom.

---

## QT-1 — Binary / Trinary Decision

**Purpose:** Yes/No/Skip choice. Used when the user needs to opt into a workflow, decide whether to continue, or pick between two distinct paths.

**Parameters required from phase file:**
- `question_text` (string): The full question to display
- `header` (string): Short ≤12-char label for the chip
- `option_overrides` (optional): Replace any of the 3 default labels/descriptions

**Canonical block:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Yes (Recommended)"
          description: "Proceed with this option"
        - label: "No"
          description: "Decline this option"
        - label: "Skip / Defer"
          description: "Postpone this decision"
```

**Example sites:**
- `phase-01-ba-planning.md` Step 1.3 (research opt-in)
- `phase-03-problem-current-state.md` Step 3.6 (failed solution history gate)
- `phase-11-synthesis-handoff.md` Step 11.8 (project artifact generation gate)

**Variant: 2-option (Yes/No only) — drop "Skip / Defer" via `option_overrides: { remove: ["Skip / Defer"] }`.**

---

## QT-2 — Severity / Priority Ranking (4-tier)

**Purpose:** Capture an ordinal severity or priority on a 4-tier scale. Used for pain-point severity, MoSCoW classification, risk levels.

**Parameters required from phase file:**
- `question_text` (string)
- `header` (string)
- `scale_type` (optional, default `"severity"`): one of `severity` (Critical/High/Medium/Low), `moscow` (Must/Should/Could/Won't), `risk` (High/Medium/Low/Negligible)
- `option_overrides` (optional): Replace any option label or description

**Canonical block — `scale_type: severity` (default):**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Critical"
          description: "Business cannot function properly without resolution"
        - label: "High"
          description: "Significant negative impact on operations"
        - label: "Medium"
          description: "Noticeable but manageable impact"
        - label: "Low"
          description: "Minor inconvenience, not blocking"
```

**Canonical block — `scale_type: moscow`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Must Have"
          description: "Critical — project fails without it"
        - label: "Should Have"
          description: "Important but can work around"
        - label: "Could Have"
          description: "Nice to have if time/budget allows"
        - label: "Won't Have (this time)"
          description: "Explicitly out of scope for this iteration"
```

**Canonical block — `scale_type: risk`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "High"
          description: "Likely to occur with major consequences"
        - label: "Medium"
          description: "Possible occurrence with moderate consequences"
        - label: "Low"
          description: "Unlikely but consequences would be notable"
        - label: "Negligible"
          description: "Very unlikely or trivial consequences"
```

**Example sites:**
- `phase-03-problem-current-state.md` Step 3.4 — pain-point severity (`scale_type: severity`)
- `phase-09-prioritization-roadmap.md` Step 9.2 — MoSCoW classification (`scale_type: moscow`)
- `phase-05-business-case-feasibility.md` Step 5.5 — feasibility rating (`scale_type: risk`)

---

## QT-3 — Range Selection (Tiered)

**Purpose:** Capture a value from a tiered range (budget brackets, time windows, durations, team sizes).

**Parameters required from phase file:**
- `question_text` (string)
- `header` (string)
- `range_type` (string): one of `budget`, `timeline`, `duration`, `volume`, `team_size`, `error_rate`
- `option_overrides` (optional)

**Canonical block — `range_type: budget`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "< $10K"
          description: "Small project / proof of concept"
        - label: "$10K - $50K"
          description: "Modest investment"
        - label: "$50K - $200K"
          description: "Significant project"
        - label: "$200K - $1M"
          description: "Major initiative"
        - label: "> $1M"
          description: "Enterprise transformation"
        - label: "Not defined yet"
          description: "Budget TBD"
```

**Canonical block — `range_type: timeline`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "ASAP (< 1 month)"
          description: "Urgent need"
        - label: "This quarter"
          description: "Within 3 months"
        - label: "This half"
          description: "Within 6 months"
        - label: "This year"
          description: "Within 12 months"
        - label: "No hard deadline"
          description: "Flexible timing"
```

**Canonical block — `range_type: duration`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Minutes (< 30 min)"
          description: "Quick task"
        - label: "Hours (30 min - 4 hrs)"
          description: "Significant time investment"
        - label: "Days (4+ hrs)"
          description: "Multi-day process"
        - label: "Weeks or longer"
          description: "Extended timeline"
```

**Canonical block — `range_type: volume`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Occasionally (< 10/week)"
          description: "Infrequent task"
        - label: "Regularly (10-50/week)"
          description: "Common task"
        - label: "Frequently (50-200/week)"
          description: "High-volume task"
        - label: "Constantly (200+/week)"
          description: "Critical path"
```

**Canonical block — `range_type: team_size`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "1-2 people"
          description: "Small team"
        - label: "3-5 people"
          description: "Medium team"
        - label: "6-10 people"
          description: "Large team"
        - label: "10+ people"
          description: "Enterprise scale"
```

**Canonical block — `range_type: error_rate`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Rarely (< 5%)"
          description: "Errors are uncommon"
        - label: "Sometimes (5-15%)"
          description: "Noticeable error rate"
        - label: "Often (15-30%)"
          description: "Frequent problems"
        - label: "Very often (> 30%)"
          description: "Major reliability issues"
```

**Example sites:**
- `phase-07-constraints-solution-scope.md` Step 7.1 — budget (`range_type: budget`)
- `phase-07-constraints-solution-scope.md` Step 7.2 — timeline (`range_type: timeline`)
- `phase-07-constraints-solution-scope.md` Step 7.3 follow-up — team size (`range_type: team_size`)
- `phase-03-problem-current-state.md` Step 3.1.1 — process duration (`range_type: duration`), volume (`range_type: volume`), error rate (`range_type: error_rate`)

---

## QT-4 — Multi-Select Impact / Category

**Purpose:** Capture multiple selections from a fixed taxonomy (business impact types, technical constraints, security standards, skill gaps).

**Parameters required from phase file:**
- `question_text` (string)
- `header` (string)
- `category` (string): one of `business_impact`, `success_metrics`, `technical_constraint`, `security_standard`, `skill_gap`, `org_constraint`
- `option_overrides` (optional)

**Canonical block — `category: business_impact`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: true
      options:
        - label: "Revenue loss"
          description: "Directly affects income"
        - label: "Cost increase"
          description: "Increases operational costs"
        - label: "Customer impact"
          description: "Affects customer satisfaction/retention"
        - label: "Employee impact"
          description: "Affects productivity or morale"
        - label: "Risk/Compliance"
          description: "Creates legal or regulatory exposure"
```

**Canonical block — `category: success_metrics`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: true
      options:
        - label: "Time saved"
          description: "Reduce hours/days on tasks"
        - label: "Money saved"
          description: "Reduce operational costs"
        - label: "Revenue increased"
          description: "Generate more income"
        - label: "Errors reduced"
          description: "Improve accuracy/quality"
        - label: "Customer satisfaction"
          description: "Improve NPS or retention"
```

**Canonical block — `category: technical_constraint`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: true
      options:
        - label: "Must integrate with existing systems"
          description: "Legacy system requirements"
        - label: "Must use specific technology"
          description: "Technology mandates"
        - label: "Must meet security standards"
          description: "Security/compliance requirements"
        - label: "Must work on-premise"
          description: "No cloud allowed"
        - label: "No major constraints"
          description: "Greenfield opportunity"
```

**Canonical block — `category: security_standard`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: true
      options:
        - label: "SOC 2"
          description: "Security trust principles"
        - label: "HIPAA"
          description: "Healthcare data"
        - label: "PCI-DSS"
          description: "Payment card data"
        - label: "GDPR"
          description: "EU data protection"
        - label: "Internal security policy"
          description: "Company-specific"
```

**Canonical block — `category: skill_gap`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: true
      options:
        - label: "Technical skills"
          description: "Programming, architecture, etc."
        - label: "Domain expertise"
          description: "Industry/business knowledge"
        - label: "Project management"
          description: "Planning and execution"
        - label: "No significant gaps"
          description: "Team is capable"
```

**Canonical block — `category: org_constraint`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: true
      options:
        - label: "Requires executive approval"
          description: "C-level sign-off needed"
        - label: "Union considerations"
          description: "Labor agreements to consider"
        - label: "Change resistance expected"
          description: "Cultural barriers"
        - label: "Regulatory requirements"
          description: "Industry regulations"
        - label: "None significant"
          description: "Organization is supportive"
```

**Example sites:**
- `phase-03-problem-current-state.md` Step 3.4 — impact type per pain point (`category: business_impact`)
- `phase-04-future-state-opportunity.md` Step 4.4 — success metrics (`category: success_metrics`)
- `phase-07-constraints-solution-scope.md` Step 7.4 — technical (`category: technical_constraint`)
- `phase-07-constraints-solution-scope.md` Step 7.4 follow-up — security standards (`category: security_standard`)
- `phase-07-constraints-solution-scope.md` Step 7.5 — organizational (`category: org_constraint`)

---

## QT-5 — Free-Form Capture

**Purpose:** Open-ended capture where structured options would constrain useful responses. The user picks a single intent option and then provides free text.

**Parameters required from phase file:**
- `question_text` (string)
- `header` (string)
- `intent` (string, default `"describe"`): one of `describe`, `explain`, `rewrite`, `list`

**Canonical block — `intent: describe` (default):**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Let me describe"
          description: "I'll explain in my own words"
        - label: "Help me brainstorm"
          description: "Guide me with follow-up questions"
        - label: "Skip this question"
          description: "I don't have an answer right now"
```

**Canonical block — `intent: explain`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Let me explain"
          description: "I have specific reasons to share"
        - label: "I'm not sure"
          description: "I don't have a clear answer"
        - label: "Skip"
          description: "Move on without this detail"
```

**Canonical block — `intent: rewrite`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Yes, that's accurate"
          description: "Proceed with this version"
        - label: "Needs minor adjustment"
          description: "I'll refine it slightly"
        - label: "Let me rewrite it"
          description: "I have a better version"
```

**Canonical block — `intent: list`:**
```yaml
AskUserQuestion:
  questions:
    - question: "{question_text}"
      header: "{header}"
      multiSelect: false
      options:
        - label: "Let me list them"
          description: "I'll name each one"
        - label: "Done — no more to add"
          description: "List is complete"
```

**Example sites:**
- `phase-03-problem-current-state.md` Step 3.7 — problem statement rewrite (`intent: rewrite`)
- `phase-04-future-state-opportunity.md` Step 4.2 — ideal state (`intent: describe`)
- `phase-03-problem-current-state.md` Step 3.6 follow-up — prior attempt description (`intent: describe`)
- `phase-02-stakeholder-analysis.md` Step 2.1 follow-up — list decision makers (`intent: list`)
- `phase-04-future-state-opportunity.md` Step 4.6 follow-up — technology rationale (`intent: explain`)

---

## Override Conventions

When a phase needs to customize a specific option for a single call (not pollute the template), use an `overrides:` block:

```yaml
AskUserQuestion: template=QT-2
  question_text: "How urgent is this?"
  header: "Urgency"
  scale_type: severity
  overrides:
    "Critical":
      description: "Must address this hour"
    remove:
      - "Low"
```

Override semantics:
- A key matching a default label replaces ONLY the named fields in that option's record
- `remove: [list]` drops the named options from the rendered output
- No new options can be added via overrides — if a phase needs a 5th option, use a different template or define a new shape and add it here

---

## When NOT to use a template

Use an inline `AskUserQuestion` block (not a template) when ALL of the following are true:
1. The question is one-off — no other phase asks anything structurally similar
2. The options are wholly unique to this question
3. The question is ≤10 lines including options

Inline blocks are still valid; templates are an optimization for repeated shapes, not a mandate.
