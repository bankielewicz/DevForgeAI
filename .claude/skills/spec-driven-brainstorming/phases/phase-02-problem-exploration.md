# Phase 02: Problem Exploration

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Deep dive into WHAT the actual problem is using root cause analysis |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/problem-exploration-workflow.md` |
| **STEP COUNT** | 6 mandatory steps (with substeps 2.1.1 and 2.1.2) |
| **MINIMUM QUESTIONS** | 5 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Current state documented (session.current_state.type is set)
- [ ] At least 3 levels of 5 Whys completed (session.root_causes has >= 3 entries)
- [ ] At least 1 pain point identified with severity (session.pain_points.length >= 1)
- [ ] Problem statement generated and user-validated (session.problem_statement is non-empty and validated)
- [ ] Checkpoint updated with phase data

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/problem-exploration-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
```

IF either Read fails: HALT -- "Phase 02 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 2.1: Current State Assessment

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "How is this task or process currently being done?"
      header: "Current State"
      multiSelect: false
      options:
        - label: "Manual process"
          description: "Done by humans with little automation"
        - label: "Semi-automated"
          description: "Mix of manual and automated steps"
        - label: "Automated but broken"
          description: "System exists but has issues"
        - label: "No process exists"
          description: "Currently not being done at all"
```

Decision Logic:
```
IF response == "Manual process" OR response == "Semi-automated":
  session.current_state.type = response
  GOTO Step 2.1.1 (Process Details)

ELSE IF response == "Automated but broken":
  session.current_state.type = "automated_broken"
  GOTO Step 2.1.2 (System Issues)

ELSE IF response == "No process exists":
  session.current_state.type = "none"
  SKIP substeps 2.1.1 and 2.1.2, GOTO Step 2.2
```

VERIFY: User response captured and non-empty. `session.current_state.type` is set.
IF response is null or empty: HALT -- "Step 2.1: Current State Assessment response not captured."

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 1`; `session.completed_outputs.current_state.type = response`

---

### Step 2.1.1: Process Details (Manual/Semi-Automated)

**Condition:** Only execute if `session.current_state.type` is "Manual process" or "Semi-automated".

```
IF session.current_state.type NOT IN ["Manual process", "Semi-automated"]:
  SKIP to Step 2.2
```

EXECUTE (Duration):
```
AskUserQuestion:
  questions:
    - question: "How long does the current process take per instance?"
      header: "Duration"
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

EXECUTE (Volume):
```
AskUserQuestion:
  questions:
    - question: "How many times per day/week is this process executed?"
      header: "Volume"
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

EXECUTE (Error Rate):
```
AskUserQuestion:
  questions:
    - question: "How often does the current process fail or produce errors?"
      header: "Error Rate"
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

VERIFY: All three sub-questions (Duration, Volume, Error Rate) captured and non-empty.
IF any response is null or empty: HALT -- "Step 2.1.1: Process Details incomplete. Missing: {duration|volume|error_rate}."
Store in `session.current_state.duration`, `session.current_state.volume`, `session.current_state.error_rate`

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 3`; `session.completed_outputs.current_state = {type, duration, volume, error_rate}`

---

### Step 2.1.2: System Issues (Automated but Broken)

**Condition:** Only execute if `session.current_state.type` is "automated_broken".

```
IF session.current_state.type != "automated_broken":
  SKIP to Step 2.2
```

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "What are the main issues with the current system?"
      header: "Issues"
      multiSelect: true
      options:
        - label: "Reliability problems"
          description: "System crashes or fails"
        - label: "Performance issues"
          description: "Too slow"
        - label: "Missing features"
          description: "Doesn't do what we need"
        - label: "Hard to use"
          description: "Poor user experience"
```

VERIFY: User response captured and non-empty. At least 1 issue selected.
IF response is null or empty: HALT -- "Step 2.1.2: System Issues response not captured."
Store in `session.current_state.system_issues[]`

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 1`; `session.completed_outputs.current_state.system_issues = session.current_state.system_issues`

---

### Step 2.2: 5 Whys Root Cause Analysis

Introduction Display:
```
Display:
"Now let's explore WHY this problem exists using the 5 Whys technique.
 We'll ask 'why' repeatedly to find the root cause."
```

EXECUTE (Why Level 1):
```
current_problem = session.topic

AskUserQuestion:
  questions:
    - question: "Why does {current_problem} happen?"
      header: "Why 1"
      multiSelect: false
      options:
        - label: "Let me explain"
          description: "I'll describe the cause"
        - label: "I don't know"
          description: "The cause is unclear"
```

Decision Logic (Why 1):
```
IF response == "Let me explain":
  Capture user's free-form explanation
  Store in session.root_causes[0]
  current_problem = session.root_causes[0]
ELSE IF response == "I don't know":
  session.root_causes[0] = "Unknown - needs investigation"
  Ask from different angle: "What do people blame when this problem occurs?"
  IF user provides answer: update session.root_causes[0], continue loop
  ELSE: SKIP remaining whys
```

EXECUTE (Why Levels 2-5 Loop):
```
FOR level in [2, 3, 4, 5]:
  IF current_problem == "Unknown" OR user_says_stop:
    BREAK

  AskUserQuestion:
    questions:
      - question: "Why does {current_problem} happen?"
        header: "Why {level}"
        multiSelect: false
        options:
          - label: "Let me explain"
            description: "I'll describe the cause"
          - label: "That's the root cause"
            description: "We've found the fundamental issue"
          - label: "I don't know"
            description: "Unsure of deeper cause"

  IF response == "Let me explain":
    Capture user's free-form explanation
    Store explanation in session.root_causes[level-1]
    current_problem = session.root_causes[level-1]
  ELSE IF response == "That's the root cause":
    Mark session.root_cause_found = true
    session.root_cause_level = level - 1
    BREAK
  ELSE IF response == "I don't know":
    session.root_causes[level-1] = "Unknown"
    session.root_cause_level = level - 1
    BREAK
```

VERIFY: At least 3 levels of 5 Whys completed (session.root_causes has >= 3 non-null entries) OR user explicitly declared root cause found at an earlier level.
IF `len(session.root_causes) < 3` AND `session.root_cause_found != true`: HALT -- "Step 2.2: Minimum 3 Why levels required. Only {count} completed."
Store `session.root_cause_level` and `session.root_cause_found`

RECORD: Update checkpoint: `session.phases["02"].questions_answered += len(session.root_causes)`; `session.completed_outputs.root_causes = session.root_causes`; `session.completed_outputs.root_cause_level = session.root_cause_level`; `session.completed_outputs.root_cause_found = session.root_cause_found`

---

### Step 2.3: Pain Point Inventory

EXECUTE (Initial Prompt):
```
AskUserQuestion:
  questions:
    - question: "What are the top 3-5 pain points caused by this problem?"
      header: "Pain Points"
      multiSelect: false
      options:
        - label: "Let me list them"
          description: "I'll describe each pain point"
```

EXECUTE (Pain Point Loop -- 1 through 5):
```
FOR i in [1..5]:
  Capture pain_point description from user

  IF pain_point is empty OR user says done:
    BREAK

  # Get impact type for this pain point
  AskUserQuestion:
    questions:
      - question: "What type of business impact does '{pain_point}' cause?"
        header: "Impact Type"
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

  # Get severity for this pain point
  AskUserQuestion:
    questions:
      - question: "How severe is '{pain_point}' for your business?"
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

  Store in session.pain_points[]:
    {
      description: pain_point,
      impact_types: [selected impacts],
      severity: selected severity
    }
```

VERIFY: At least 1 pain point captured with both impact type and severity.
IF `session.pain_points.length < 1`: HALT -- "Step 2.3: At least 1 pain point required. None captured."
IF any pain point is missing `impact_types` or `severity`: HALT -- "Step 2.3: Pain point '{description}' missing impact type or severity."

RECORD: Update checkpoint: `session.phases["02"].questions_answered += (1 + 2 * pain_point_count)`; `session.completed_outputs.pain_points = session.pain_points`

---

### Step 2.4: Impact Quantification

**Condition:** Only execute for pain points with severity "Critical" or "High".

```
critical_high_pains = [p for p in session.pain_points WHERE p.severity in ["Critical", "High"]]

IF len(critical_high_pains) == 0:
  Display: "No Critical/High pain points to quantify. Proceeding to Step 2.5."
  SKIP to Step 2.5
```

EXECUTE:
```
FOR each pain_point in critical_high_pains:
  AskUserQuestion:
    questions:
      - question: "Can you estimate the cost of '{pain_point.description}' per month?"
        header: "Cost"
        multiSelect: false
        options:
          - label: "< $1,000/month"
            description: "Minor cost"
          - label: "$1,000 - $10,000/month"
            description: "Moderate cost"
          - label: "$10,000 - $100,000/month"
            description: "Significant cost"
          - label: "> $100,000/month"
            description: "Major cost"
          - label: "Can't estimate"
            description: "Unknown or hard to quantify"

  Store in pain_point.estimated_cost
```

VERIFY: Each Critical/High pain point has an estimated_cost value (including "Can't estimate" as valid).
IF any Critical/High pain point is missing `estimated_cost`: HALT -- "Step 2.4: Impact quantification incomplete for '{pain_point.description}'."

RECORD: Update checkpoint: `session.phases["02"].questions_answered += len(critical_high_pains)`; `session.completed_outputs.pain_points = session.pain_points` (updated with costs)

---

### Step 2.5: Failed Solution History

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Have you tried solving this problem before?"
      header: "History"
      multiSelect: false
      options:
        - label: "Yes - it failed"
          description: "We tried but it didn't work"
        - label: "Yes - partially worked"
          description: "Some success but not complete"
        - label: "No - first attempt"
          description: "Haven't tried before"
        - label: "Not sure"
          description: "Before my time or don't know"
```

Conditional Follow-Up:
```
IF response IN ["Yes - it failed", "Yes - partially worked"]:

  # What was tried
  AskUserQuestion:
    questions:
      - question: "What was tried before?"
        header: "Previous"
        multiSelect: false
        options:
          - label: "Let me describe"
            description: "I'll explain what we tried"

  Capture description from user.
  Store in session.failed_solutions[].what

  # Why it failed
  AskUserQuestion:
    questions:
      - question: "Why didn't it work?"
        header: "Why Failed"
        multiSelect: true
        options:
          - label: "Too expensive"
            description: "Cost exceeded budget"
          - label: "Too complex"
            description: "Solution was too complicated"
          - label: "Poor adoption"
            description: "People didn't use it"
          - label: "Didn't solve the problem"
            description: "Wrong solution for the issue"
          - label: "Other factors"
            description: "External circumstances"

  Store in session.failed_solutions[].why

ELSE IF response == "No - first attempt":
  session.failed_solutions = []
  Note: Greenfield opportunity -- no prior failures to learn from.

ELSE IF response == "Not sure":
  session.failed_solutions = "unknown"
```

VERIFY: User response captured and non-empty. Failed solution history is recorded (even if empty list or "unknown").
IF response is null or empty: HALT -- "Step 2.5: Failed Solution History response not captured."
Store in `session.failed_solutions`

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 1` (+ 2 if follow-ups triggered); `session.completed_outputs.failed_solutions = session.failed_solutions`

---

### Step 2.6: Generate Problem Statement

EXECUTE (Synthesis):
```
# Build problem statement from collected data
primary_stakeholder = session.stakeholders.primary[0].name
primary_pain = session.pain_points[0].description
root_cause = session.root_causes[-1]  # Deepest root cause identified
impact = session.pain_points[0].impact_types[0]

problem_statement = "{primary_stakeholder} experiences {primary_pain} because {root_cause}, resulting in {impact}."
```

EXECUTE (User Validation):
```
Display:
"Based on our discussion, here's the problem statement:

  \"{problem_statement}\"
"

AskUserQuestion:
  questions:
    - question: "Does this accurately capture the problem?"
      header: "Validate"
      multiSelect: false
      options:
        - label: "Yes, that's accurate"
          description: "Proceed with this statement"
        - label: "Needs adjustment"
          description: "I'll refine it"
        - label: "Let me rewrite it"
          description: "I have a better version"
```

Decision Logic:
```
IF response == "Yes, that's accurate":
  session.problem_statement = problem_statement
  session.problem_statement_validated = true

ELSE IF response == "Needs adjustment":
  Ask user for specific adjustments
  Apply adjustments to problem_statement
  session.problem_statement = adjusted_statement
  session.problem_statement_validated = true

ELSE IF response == "Let me rewrite it":
  Capture user's rewritten problem statement
  session.problem_statement = user_rewrite
  session.problem_statement_validated = true
```

VERIFY: Problem statement is non-empty AND user has validated it (`session.problem_statement_validated == true`).
IF `session.problem_statement` is null or empty: HALT -- "Step 2.6: Problem statement not generated."
IF `session.problem_statement_validated != true`: HALT -- "Step 2.6: Problem statement not validated by user."

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 1`; `session.completed_outputs.problem_statement = session.problem_statement`; `session.completed_outputs.problem_statement_validated = true`

---

## Phase Exit Verification

Before transitioning to Phase 03, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.current_state.type is not null
    IF FAIL: HALT -- "Exit blocked: Current state not documented."

  CHECK: len(session.root_causes) >= 3 OR session.root_cause_found == true
    IF FAIL: HALT -- "Exit blocked: Less than 3 Why levels completed without root cause found."

  CHECK: session.pain_points.length >= 1
    IF FAIL: HALT -- "Exit blocked: No pain points identified."

  CHECK: ALL pain points have severity set
    IF FAIL: HALT -- "Exit blocked: Pain point '{description}' missing severity."

  CHECK: session.problem_statement is non-empty AND session.problem_statement_validated == true
    IF FAIL: HALT -- "Exit blocked: Problem statement not generated or not validated."

  CHECK: session.phases["02"].questions_answered >= 5
    IF FAIL: HALT -- "Exit blocked: Minimum 5 questions required, only {count} answered."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 3
checkpoint.progress.phases_completed.append("02")
checkpoint.progress.completion_percentage = round(2/7 * 100)

Write(file_path="devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: Checkpoint file updated on disk with `current_phase = 3`.
IF write fails: HALT -- "Phase 02 exit checkpoint not saved."

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 2 Complete: Problem Exploration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem Statement:
  \"{problem_statement}\"

Root Cause (Level {root_cause_level}):
  {deepest_root_cause}

Pain Points: {count} identified
  - {pain_1} (Severity: {severity})
  - {pain_2} (Severity: {severity})

Previous Attempts: {count}

Proceeding to Phase 3: Opportunity Mapping...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
