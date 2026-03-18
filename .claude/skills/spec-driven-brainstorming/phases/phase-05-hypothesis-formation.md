# Phase 05: Hypothesis Formation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Create TESTABLE assumptions that need validation before committing to a solution |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/hypothesis-formation-workflow.md` |
| **STEP COUNT** | 7 mandatory steps |
| **MINIMUM QUESTIONS** | 2 |

## Phase Exit Criteria

- [ ] Implicit assumptions extracted from previous phases
- [ ] Critical assumptions identified by user
- [ ] At least 1 hypothesis formulated as IF-THEN statement
- [ ] Success criteria defined for each hypothesis
- [ ] Validation methods identified
- [ ] Risk levels assessed
- [ ] Context window check completed
- [ ] Checkpoint updated

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/hypothesis-formation-workflow.md")
```

IF Read fails: HALT -- "Phase 05 cannot proceed without reference file."

---

## Mandatory Steps

### Step 5.1: Extract Implicit Assumptions

```
EXECUTE:
  Review all previous phase outputs for implicit assumptions:

  # From Problem Statement (Phase 2)
  IF session.problem_statement contains claims without evidence:
    Add assumption: { source: "problem_statement", type: "problem_validity" }

  # From Root Cause Analysis (Phase 2)
  FOR each root_cause in session.root_causes:
    IF root_cause is a causal claim:
      Add assumption: { source: "root_cause", type: "causation" }

  # From Opportunity Mapping (Phase 3)
  FOR each opportunity in session.opportunities:
    Add assumption: "{opportunity.description} will solve the problem"
    { source: "opportunity", type: "solution_effectiveness" }

  # From Constraints (Phase 4)
  FOR each constraint in session.constraints:
    IF constraint.flexibility != "Fixed":
      Add assumption: "{constraint} is negotiable"
      { source: "constraint", type: "constraint_flexibility" }

  Display:
    "Based on our discussion, I've identified these implicit assumptions:

    1. {assumption_1}
    2. {assumption_2}
    3. {assumption_3}
    ...

    Let's validate which ones are critical to test."

VERIFY:
  - At least 1 assumption extracted
  - Each assumption has source and type fields
  IF 0 assumptions found: Ask user directly about risky beliefs

RECORD:
  session.assumptions = [extracted assumptions]
  Update checkpoint: { phase: 5, step: "5.1", status: "complete" }
```

---

### Step 5.2: Prioritize Assumptions

```
EXECUTE:
  AskUserQuestion:
    questions:
      - question: "Which of these assumptions are most critical to validate before proceeding?"
        header: "Critical"
        multiSelect: true
        options:
          - label: "{assumption_1}"
            description: "From: {source}"
          - label: "{assumption_2}"
            description: "From: {source}"
          - label: "{assumption_3}"
            description: "From: {source}"
          - label: "None are critical"
            description: "All assumptions are safe"

  FOR each selected assumption:
    assumption.priority = "critical"
    assumption.validation_required = true

VERIFY:
  - User responded with selection
  - IF "None are critical" selected: Probe with "what if wrong" scenarios before accepting
  - At least 1 critical assumption identified (or explicit user override)

RECORD:
  session.critical_assumptions = [selected assumptions]
  Update checkpoint: { phase: 5, step: "5.2", status: "complete" }
```

---

### Step 5.3: Formulate Hypotheses

```
EXECUTE:
  FOR each critical_assumption:
    # Convert to IF-THEN statement
    hypothesis = {
      id: "H{index}",
      statement: "IF {condition}, THEN {expected_outcome}",
      source: critical_assumption.source,
      type: critical_assumption.type
    }

    Display:
      "Hypothesis {id}:
       IF {condition}, THEN {expected_outcome}

       Based on assumption: {original_assumption}"

    AskUserQuestion:
      questions:
        - question: "Is this hypothesis correctly stated?"
          header: "Validate"
          multiSelect: false
          options:
            - label: "Yes, correct"
              description: "Proceed with this hypothesis"
            - label: "Needs adjustment"
              description: "I'll refine it"

    IF response == "Needs adjustment":
      Capture user's refined hypothesis text
      Update hypothesis.statement with refinement

VERIFY:
  - At least 1 hypothesis formulated as IF-THEN statement
  - Each hypothesis has: id, statement, source, type
  - User validated each hypothesis

RECORD:
  session.hypotheses = [formulated hypotheses]
  Update checkpoint: { phase: 5, step: "5.3", status: "complete" }
```

---

### Step 5.4: Define Success Criteria

```
EXECUTE:
  FOR each hypothesis:
    AskUserQuestion:
      questions:
        - question: "How would we know if '{hypothesis.statement}' is true? What's the success metric?"
          header: "Metric"
          multiSelect: false
          options:
            - label: "Let me specify"
              description: "I'll define the metric"
            - label: "Suggest options"
              description: "Help me think of metrics"

    IF response == "Suggest options":
      # Provide relevant metric options based on hypothesis type
      IF hypothesis.type == "solution_effectiveness":
        Suggest: ["Time reduction %", "Error rate reduction %", "Cost savings $"]
      ELSE IF hypothesis.type == "causation":
        Suggest: ["Before/after comparison", "A/B test results", "Correlation analysis"]
      ELSE IF hypothesis.type == "problem_validity":
        Suggest: ["User survey results", "Support ticket volume", "Process observation"]
      ELSE IF hypothesis.type == "constraint_flexibility":
        Suggest: ["Stakeholder approval", "Budget reallocation", "Timeline extension"]

    hypothesis.success_criteria = user_input

VERIFY:
  - Each hypothesis has a measurable success criteria string
  - Success criteria is specific (not vague like "it works")
  IF criteria is vague: Ask user to quantify

RECORD:
  Update each hypothesis with success_criteria
  Update checkpoint: { phase: 5, step: "5.4", status: "complete" }
```

---

### Step 5.5: Identify Validation Methods

```
EXECUTE:
  FOR each hypothesis:
    AskUserQuestion:
      questions:
        - question: "How could we validate '{hypothesis.statement}'?"
          header: "Validation"
          multiSelect: false
          options:
            - label: "Proof of concept"
              description: "Build a small test"
            - label: "User research"
              description: "Talk to users/stakeholders"
            - label: "Data analysis"
              description: "Analyze existing data"
            - label: "Expert consultation"
              description: "Ask domain experts"
            - label: "Market research"
              description: "Research similar solutions"

    hypothesis.validation_method = response

VERIFY:
  - Each hypothesis has a validation_method assigned
  - validation_method is one of the 5 options above

RECORD:
  Update each hypothesis with validation_method
  Update checkpoint: { phase: 5, step: "5.5", status: "complete" }
```

---

### Step 5.6: Assess Risk Level

```
EXECUTE:
  FOR each hypothesis:
    AskUserQuestion:
      questions:
        - question: "What happens if '{hypothesis.statement}' turns out to be wrong?"
          header: "Risk Level"
          multiSelect: false
          options:
            - label: "Project fails"
              description: "Critical dependency"
            - label: "Major rework needed"
              description: "Significant impact but recoverable"
            - label: "Minor adjustments"
              description: "Can adapt without major changes"
            - label: "No real impact"
              description: "Hypothesis isn't critical"

    hypothesis.risk_level = response

    IF response == "Project fails":
      hypothesis.blocking = true
      hypothesis.validate_first = true

VERIFY:
  - Each hypothesis has a risk_level assigned
  - Blocking hypotheses flagged with blocking=true and validate_first=true
  - validation_priority list generated (blocking first, then by risk)

RECORD:
  session.hypothesis_register = {
    hypotheses: [all hypotheses with full metadata],
    validation_priority: [ordered by risk: "Project fails" first],
    assumptions_validated: count,
    assumptions_remaining: 0
  }
  Update checkpoint: { phase: 5, step: "5.6", status: "complete" }
```

---

### Step 5.7: Context Window Check

```
EXECUTE:
  IF estimated_context_usage > 70%:
    AskUserQuestion:
      questions:
        - question: "Context window is approximately {PERCENT}% full. Would you like to:"
          header: "Session"
          multiSelect: false
          options:
            - label: "Continue in this session"
              description: "Proceed to Phase 6 (Prioritization)"
            - label: "Save and continue later"
              description: "Create checkpoint and exit"

    IF response == "Save and continue later":
      Save checkpoint with all session data
      Display checkpoint confirmation
      EXIT session

  ELSE:
    # Context is fine, proceed automatically
    No user question needed

VERIFY:
  - Context usage assessed
  - IF > 70%: User chose to continue or save
  - IF save chosen: Checkpoint written and verified on disk

RECORD:
  Update checkpoint: { phase: 5, step: "5.7", status: "complete", phase_complete: true }
```

---

## Phase 5 Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 5 Complete: Hypothesis Formation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hypotheses Formed: {count}
  - H1: {statement} (Risk: {risk_level})
  - H2: {statement} (Risk: {risk_level})

Blocking Hypotheses: {count}
  Must validate before proceeding: {blocking_ids}

Proceeding to Phase 6: Prioritization...
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| No assumptions found | Analysis finds nothing | Ask directly about risky beliefs |
| All assumptions "safe" | User says none critical | Probe with "what if wrong" scenarios |
| Cannot formulate IF-THEN | Assumption is vague | Ask for specific expected outcome |
| No validation method | User unsure how to test | Suggest appropriate methods from the 5 options |
