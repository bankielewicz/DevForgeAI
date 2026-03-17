# Phase 01: Stakeholder Discovery

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Identify WHO is involved in the problem space and WHAT they want |
| **REFERENCE** | `.claude/skills/brainstorming/references/stakeholder-discovery-workflow.md` |
| **STEP COUNT** | 8 mandatory steps |
| **MINIMUM QUESTIONS** | 5 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] At least 1 primary stakeholder identified (session.stakeholders.primary.length >= 1)
- [ ] At least 1 secondary stakeholder identified (session.stakeholders.secondary.length >= 1)
- [ ] Goals captured for each primary stakeholder
- [ ] Concerns captured for each primary stakeholder
- [ ] Conflicts identified or explicitly marked "none detected"
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/brainstorming/references/stakeholder-discovery-workflow.md")
Read(file_path=".claude/skills/brainstorming/references/user-interaction-patterns.md")
```

IF either Read fails: HALT -- "Phase 01 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 1.1: Get Initial Topic

**Condition:** Only execute if `session.topic` is null (topic not provided in command arguments).

```
IF session.topic is NOT null:
  Display: "Topic already set: {session.topic}"
  SKIP to Step 1.2
```

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "What business problem or opportunity would you like to explore?"
      header: "Topic"
      multiSelect: false
      options:
        - label: "I have a specific problem"
          description: "Something isn't working well"
        - label: "I see an opportunity"
          description: "Something could be better"
        - label: "I'm not sure yet"
          description: "Help me discover it"
```

Decision Logic:
```
IF response == "I have a specific problem":
  Ask for problem description
  Set session.topic_type = "problem"
ELSE IF response == "I see an opportunity":
  Ask for opportunity description
  Set session.topic_type = "opportunity"
ELSE IF response == "I'm not sure yet":
  Set session.topic_type = "discovery"
  Skip detailed description, proceed to stakeholder questions
```

VERIFY: User response captured and non-empty.
IF response is null or empty: HALT -- "Step 1.1: Get Initial Topic response not captured."
Store in `session.topic` and `session.topic_type`

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1`; `session.topic = response`; `session.topic_type = derived_type`

---

### Step 1.2: Identify Primary Decision Maker

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who has the authority to approve or reject solutions for this problem?"
      header: "Decision Maker"
      multiSelect: false
      options:
        - label: "I am the decision maker"
          description: "I have budget and approval authority"
        - label: "Someone else"
          description: "I'll need to get approval from others"
        - label: "Multiple people"
          description: "It's a committee or shared decision"
        - label: "Not sure"
          description: "Decision authority is unclear"
```

Follow-Up Logic:
```
IF response == "Someone else" OR response == "Multiple people":
  AskUserQuestion:
    questions:
      - question: "Who are the key decision makers?"
        header: "Who"
        multiSelect: false
        options:
          - label: "Let me list them"
            description: "I'll name the people/roles"

  Capture names/roles from user.
  Store in session.stakeholders.primary[]

ELSE IF response == "I am the decision maker":
  Store "User (self)" in session.stakeholders.primary[]

ELSE IF response == "Not sure":
  Ask about budget/approval process to infer decision maker.
  Store inferred decision maker in session.stakeholders.primary[]
```

VERIFY: User response captured and non-empty. `session.stakeholders.primary.length >= 1`.
IF response is null or empty: HALT -- "Step 1.2: Identify Primary Decision Maker response not captured."
IF `session.stakeholders.primary` is empty after processing: HALT -- "Step 1.2: No primary stakeholder captured."

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1`; `session.completed_outputs.stakeholders.primary = session.stakeholders.primary`

---

### Step 1.3: Identify End Users

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who will actually use the solution on a daily basis?"
      header: "End Users"
      multiSelect: true
      options:
        - label: "Internal employees"
          description: "Staff within the organization"
        - label: "External customers"
          description: "Paying customers or clients"
        - label: "Partners/vendors"
          description: "Third-party business relationships"
        - label: "The general public"
          description: "Anyone can access it"
```

Follow-Up Logic:
```
FOR each selected user_type:
  AskUserQuestion:
    questions:
      - question: "How many {user_type} would use this solution?"
        header: "Count"
        multiSelect: false
        options:
          - label: "1-10"
            description: "Small team"
          - label: "10-100"
            description: "Department level"
          - label: "100-1000"
            description: "Company-wide"
          - label: "1000+"
            description: "Large scale"
```

VERIFY: User response captured and non-empty. At least 1 user type selected.
IF response is null or empty: HALT -- "Step 1.3: Identify End Users response not captured."
Store in `session.stakeholders.secondary[]` with count per user type.

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1`; `session.completed_outputs.stakeholders.secondary = session.stakeholders.secondary`

---

### Step 1.4: Identify Affected Parties

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who else will be impacted by this change, even if they don't use the solution directly?"
      header: "Affected"
      multiSelect: true
      options:
        - label: "IT/Operations team"
          description: "Those who maintain systems"
        - label: "Finance/Accounting"
          description: "Those who handle budgets and reporting"
        - label: "Compliance/Legal"
          description: "Those who ensure regulatory compliance"
        - label: "Customer Support"
          description: "Those who help users with issues"
```

VERIFY: User response captured and non-empty.
IF response is null or empty: HALT -- "Step 1.4: Identify Affected Parties response not captured."
Store in `session.stakeholders.tertiary[]`

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1`; `session.completed_outputs.stakeholders.tertiary = session.stakeholders.tertiary`

---

### Step 1.5: Map Stakeholder Goals

EXECUTE:
```
FOR each stakeholder in session.stakeholders.primary:
  AskUserQuestion:
    questions:
      - question: "What does {stakeholder.name} want to achieve from this initiative?"
        header: "Goals"
        multiSelect: true
        options:
          - label: "Reduce costs"
            description: "Save money on operations"
          - label: "Increase revenue"
            description: "Generate more income"
          - label: "Improve efficiency"
            description: "Do more with less"
          - label: "Reduce risk"
            description: "Prevent problems or losses"

  Store response in stakeholder.goals[]
```

Optional Subagent Enhancement:
```
# For deeper stakeholder analysis, invoke subagent (OPTIONAL - not blocking)
Task(
  subagent_type="stakeholder-analyst",
  prompt="Analyze stakeholders for: {session.topic}.
          Primary: {session.stakeholders.primary}
          Secondary: {session.stakeholders.secondary}
          Identify goals, concerns, and potential conflicts."
)
```

VERIFY: User response captured and non-empty for each primary stakeholder. Every primary stakeholder has at least 1 goal.
IF response is null or empty for any stakeholder: HALT -- "Step 1.5: Map Stakeholder Goals response not captured for {stakeholder.name}."
IF any `stakeholder.goals` is empty: HALT -- "Step 1.5: Goals not captured for {stakeholder.name}."

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1` (per stakeholder loop iteration); `session.completed_outputs.stakeholders.goals = {stakeholder.name: stakeholder.goals for each}`

---

### Step 1.6: Map Stakeholder Concerns

EXECUTE:
```
FOR each stakeholder in session.stakeholders.primary:
  AskUserQuestion:
    questions:
      - question: "What concerns or fears does {stakeholder.name} have about this initiative?"
        header: "Concerns"
        multiSelect: true
        options:
          - label: "Budget overruns"
            description: "It might cost too much"
          - label: "Timeline delays"
            description: "It might take too long"
          - label: "Disruption"
            description: "It might disrupt current operations"
          - label: "Adoption issues"
            description: "People might not use it"

  Store response in stakeholder.concerns[]
```

VERIFY: User response captured and non-empty for each primary stakeholder. Every primary stakeholder has at least 1 concern.
IF response is null or empty for any stakeholder: HALT -- "Step 1.6: Map Stakeholder Concerns response not captured for {stakeholder.name}."
IF any `stakeholder.concerns` is empty: HALT -- "Step 1.6: Concerns not captured for {stakeholder.name}."

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1` (per stakeholder loop iteration); `session.completed_outputs.stakeholders.concerns = {stakeholder.name: stakeholder.concerns for each}`

---

### Step 1.7: Identify Conflicts

EXECUTE (Analysis):
```
conflicts = []

FOR each pair (stakeholder_a, stakeholder_b) in session.stakeholders.primary:
  IF stakeholder_a.goals CONFLICTS_WITH stakeholder_b.goals:
    conflict = {
      stakeholders: [stakeholder_a.name, stakeholder_b.name],
      nature: describe_conflict(stakeholder_a.goals, stakeholder_b.goals),
      resolution: null  # Will be addressed in prioritization
    }
    conflicts.append(conflict)
```

Conflict Detection Rules:
- "Reduce costs" vs "Increase features" = Resource conflict
- "ASAP timeline" vs "High quality" = Speed vs quality
- "Minimal disruption" vs "Complete overhaul" = Scope conflict

EXECUTE (User Confirmation):
```
IF len(conflicts) > 0:
  Display: "I've identified potential conflicts:"
  FOR each conflict:
    Display: "- {stakeholder_a.name} wants {goal_a} but {stakeholder_b.name} wants {goal_b}"

  AskUserQuestion:
    questions:
      - question: "Are these conflicts accurate? Any others?"
        header: "Validate"
        multiSelect: false
        options:
          - label: "Yes, accurate"
            description: "These conflicts are real"
          - label: "Some corrections needed"
            description: "I'll clarify"
          - label: "No conflicts"
            description: "They're actually aligned"

ELSE:
  Display: "No conflicts detected between stakeholder goals."
  Set session.conflicts = "none detected"
```

VERIFY: Conflicts either confirmed by user OR explicitly marked "none detected".
IF conflict analysis was not performed: HALT -- "Step 1.7: Identify Conflicts was not executed."
Store in `session.conflicts`

RECORD: Update checkpoint: `session.phases["01"].questions_answered += 1`; `session.completed_outputs.stakeholders.conflicts = session.conflicts`

---

### Step 1.8: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 2 (Problem Exploration)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit"

  IF response == "Save and continue later":
    Write updated checkpoint with all Phase 01 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill

ELSE:
  Display: "Context window healthy. Proceeding to Phase 2."
```

VERIFY: Context window check was performed (either threshold check or healthy confirmation).
IF check was skipped: HALT -- "Step 1.8: Context Window Check not performed."

RECORD: Update checkpoint: `session.phases["01"].context_check_completed = true`

---

## Phase Exit Verification

Before transitioning to Phase 02, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.stakeholders.primary.length >= 1
    IF FAIL: HALT -- "Exit blocked: No primary stakeholder identified."

  CHECK: session.stakeholders.secondary.length >= 1
    IF FAIL: HALT -- "Exit blocked: No secondary stakeholder identified."

  CHECK: ALL primary stakeholders have goals (stakeholder.goals.length >= 1 for each)
    IF FAIL: HALT -- "Exit blocked: Goals missing for primary stakeholder {name}."

  CHECK: ALL primary stakeholders have concerns (stakeholder.concerns.length >= 1 for each)
    IF FAIL: HALT -- "Exit blocked: Concerns missing for primary stakeholder {name}."

  CHECK: session.conflicts is not null (either list of conflicts OR "none detected")
    IF FAIL: HALT -- "Exit blocked: Conflict analysis not completed."

  CHECK: session.phases["01"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."

  CHECK: session.phases["01"].questions_answered >= 5
    IF FAIL: HALT -- "Exit blocked: Minimum 5 questions required, only {count} answered."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 2
checkpoint.progress.phases_completed.append("01")
checkpoint.progress.completion_percentage = round(1/7 * 100)

Write(file_path="devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: Checkpoint file updated on disk with `current_phase = 2`.
IF write fails: HALT -- "Phase 01 exit checkpoint not saved."

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 1 Complete: Stakeholder Discovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stakeholders Identified:
  Primary: {count} decision maker(s)
  Secondary: {count} user group(s)
  Tertiary: {count} affected parties

Conflicts: {count} potential conflicts identified

Proceeding to Phase 2: Problem Exploration...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
