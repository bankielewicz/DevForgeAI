# Phase 02: Discovery & Problem Understanding

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Deeply understand the business problem, identify users, define goals, assess complexity, and establish scope boundaries |
| **REFERENCE** | `.claude/skills/spec-driven-ideation/references/discovery-workflow.md` (357 lines), `.claude/skills/spec-driven-ideation/references/user-interaction-patterns.md` (491 lines) |
| **STEP COUNT** | 8 mandatory steps |
| **MINIMUM QUESTIONS** | 5 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] problem_statement captured (non-empty, specific -- not vague like "make things better")
- [ ] user_types identified (at least 1 with volume estimate)
- [ ] personas documented (at least 1 with name/role, goals, pain_points)
- [ ] business_goals captured (at least 1 with measurable target)
- [ ] success_metrics quantified (at least 1 per business goal)
- [ ] scope_boundaries defined (in_scope and out_of_scope each have 1+ items)
- [ ] complexity_assessment completed (all 4 dimensions scored with reasoning)
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 03.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-ideation/references/discovery-workflow.md")
Read(file_path=".claude/skills/spec-driven-ideation/references/user-interaction-patterns.md")
```

IF either Read fails: HALT -- "Phase 02 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 2.1: Capture Business Problem

**Condition:** Skip the initial question if `session.problem_statement` is already set from brainstorm handoff.

```
IF session.problem_statement is NOT null AND session.problem_statement != "":
  Display: "Problem statement pre-populated from brainstorm: '{session.problem_statement}'"
  Display: "We'll validate this later in this phase. Proceeding to Step 2.2."
  SKIP to Step 2.2
```

EXECUTE (Initial Prompt):
```
AskUserQuestion:
  questions:
    - question: "What business problem are you trying to solve?"
      header: "Business Problem"
      multiSelect: false
      options:
        - label: "Let me describe it"
          description: "I'll explain the problem in detail"
        - label: "I have a solution in mind"
          description: "I know what I want to build"
        - label: "I need help articulating it"
          description: "I have a rough idea but can't pin it down"
```

Decision Logic:
```
IF response == "Let me describe it":
  Capture user's free-form problem description
  session.problem_statement = captured_description
  session.problem_source = "user_described"

ELSE IF response == "I have a solution in mind":
  # Reverse-engineer the problem from the solution
  AskUserQuestion:
    questions:
      - question: "What solution do you have in mind? We'll work backward to the problem."
        header: "Proposed Solution"
        multiSelect: false
        options:
          - label: "Let me describe my solution"
            description: "I'll explain what I want to build"

  Capture user's solution description
  Store in session.proposed_solution

  # Now extract the problem
  AskUserQuestion:
    questions:
      - question: "What's happening now that makes this solution necessary? What's the gap between current state and desired state?"
        header: "The Gap"
        multiSelect: false
        options:
          - label: "Let me explain the current situation"
            description: "I'll describe what's happening now"

  Capture user's gap description
  session.problem_statement = "Current: {current_situation}. Desired: {proposed_solution}. Gap: {user_gap_description}"
  session.problem_source = "reverse_engineered"

ELSE IF response == "I need help articulating it":
  # Guided discovery through sub-questions
  AskUserQuestion:
    questions:
      - question: "What's happening now that frustrates you or your users?"
        header: "Current Frustration"
        multiSelect: false
        options:
          - label: "Let me describe it"
            description: "I'll explain the frustration"

  Capture current_frustration

  AskUserQuestion:
    questions:
      - question: "What should be happening instead?"
        header: "Desired State"
        multiSelect: false
        options:
          - label: "Let me describe it"
            description: "I'll explain the ideal outcome"

  Capture desired_state

  AskUserQuestion:
    questions:
      - question: "What's preventing the desired state from happening?"
        header: "Blocker"
        multiSelect: false
        options:
          - label: "Let me explain"
            description: "I'll describe the blocker"
          - label: "I don't know"
            description: "That's what I need help figuring out"

  IF response == "Let me explain":
    Capture blocker
  ELSE IF response == "I don't know":
    blocker = "Unknown -- to be investigated during requirements elicitation"

  session.problem_statement = "Users experience {current_frustration}. The desired state is {desired_state}. Blocker: {blocker}."
  session.problem_source = "guided_discovery"
```

VERIFY: `session.problem_statement` is non-empty and specific.
Specificity check:
```
IF session.problem_statement contains ONLY vague terms like
   ["make things better", "improve everything", "fix issues", "be faster"]:
  HALT -- "Step 2.1: Problem statement too vague. Contains no specific problem description. Re-ask with more probing questions."

IF len(session.problem_statement) < 20:
  HALT -- "Step 2.1: Problem statement too short ({len} chars). Minimum 20 characters for a meaningful statement."
```
IF `session.problem_statement` is null or empty: HALT -- "Step 2.1: Business Problem not captured."

RECORD: Update checkpoint: `session.phases["02"].questions_answered += {count of questions asked in this step}`; `session.completed_outputs.problem_statement = session.problem_statement`; `session.completed_outputs.problem_source = session.problem_source`

---

### Step 2.2: Identify User Types

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who are the primary users or beneficiaries of the solution?"
      header: "User Types"
      multiSelect: true
      options:
        - label: "End customers/consumers"
          description: "People who buy or use your product/service"
        - label: "Internal employees"
          description: "Staff within the organization"
        - label: "Business partners/vendors"
          description: "Third-party business relationships"
        - label: "Administrators/operators"
          description: "People who manage and maintain the system"
```

Follow-Up (Volume per user type):
```
FOR each selected user_type:
  AskUserQuestion:
    questions:
      - question: "How many {user_type} would use this solution?"
        header: "User Volume"
        multiSelect: false
        options:
          - label: "1-10"
            description: "Small group"
          - label: "10-100"
            description: "Department level"
          - label: "100-1,000"
            description: "Company-wide"
          - label: "1,000-10,000"
            description: "Large scale"
          - label: "10,000+"
            description: "Mass market"

  Store in session.user_types[]:
    {
      type: user_type,
      volume: selected_volume
    }
```

VERIFY: At least 1 user type selected with volume estimate.
```
IF session.user_types is empty OR len(session.user_types) < 1:
  HALT -- "Step 2.2: No user types identified. At least 1 required."

FOR each user_type in session.user_types:
  IF user_type.volume is null or empty:
    HALT -- "Step 2.2: Volume not captured for user type '{user_type.type}'."
```

RECORD: Update checkpoint: `session.phases["02"].questions_answered += (1 + len(session.user_types))`; `session.completed_outputs.user_types = session.user_types`

---

### Step 2.3: Build User Personas

EXECUTE:
```
FOR each user_type in session.user_types:

  # Question 1: What do they need?
  AskUserQuestion:
    questions:
      - question: "What does a typical {user_type.type} need to accomplish with this solution?"
        header: "Persona: {user_type.type} - Goals"
        multiSelect: false
        options:
          - label: "Let me describe their goals"
            description: "I'll explain what they need to do"

  Capture persona_goals from user response

  # Question 2: What frustrates them?
  AskUserQuestion:
    questions:
      - question: "What frustrates a typical {user_type.type} most about the current situation?"
        header: "Persona: {user_type.type} - Pain Points"
        multiSelect: false
        options:
          - label: "Let me describe their frustrations"
            description: "I'll explain their pain points"

  Capture persona_pain_points from user response

  # Question 3: What does success look like?
  AskUserQuestion:
    questions:
      - question: "What would success look like for a typical {user_type.type}?"
        header: "Persona: {user_type.type} - Success"
        multiSelect: false
        options:
          - label: "Let me describe success"
            description: "I'll explain their ideal outcome"

  Capture persona_success from user response

  # Build persona object
  persona = {
    name: "{user_type.type} Persona",
    role: user_type.type,
    volume: user_type.volume,
    goals: persona_goals,
    pain_points: persona_pain_points,
    success_definition: persona_success
  }

  session.personas.append(persona)
```

VERIFY: At least 1 persona documented with name/role, goals, and pain_points.
```
IF session.personas is empty OR len(session.personas) < 1:
  HALT -- "Step 2.3: No personas documented. At least 1 required."

FOR each persona in session.personas:
  IF persona.goals is null or empty:
    HALT -- "Step 2.3: Goals not captured for persona '{persona.name}'."
  IF persona.pain_points is null or empty:
    HALT -- "Step 2.3: Pain points not captured for persona '{persona.name}'."
```

RECORD: Update checkpoint: `session.phases["02"].questions_answered += (3 * len(session.user_types))`; `session.completed_outputs.personas = session.personas`

---

### Step 2.4: Define Business Goals

EXECUTE (Initial Selection):
```
AskUserQuestion:
  questions:
    - question: "What are the top 3 business goals for this initiative?"
      header: "Business Goals"
      multiSelect: true
      options:
        - label: "Increase revenue"
          description: "Generate more income or sales"
        - label: "Reduce costs"
          description: "Lower operational or infrastructure expenses"
        - label: "Improve efficiency"
          description: "Do more with less time or resources"
        - label: "Enhance user experience"
          description: "Make it easier and more pleasant for users"
        - label: "Enable new capabilities"
          description: "Do something not currently possible"
        - label: "Compliance/regulatory requirement"
          description: "Meet legal or regulatory obligations"
        - label: "Reduce risk"
          description: "Mitigate business, technical, or security risks"
        - label: "Other"
          description: "I'll describe a different goal"
```

Decision Logic:
```
IF "Other" in selected_goals:
  AskUserQuestion:
    questions:
      - question: "Describe your business goal:"
        header: "Custom Goal"
        multiSelect: false
        options:
          - label: "Let me describe it"
            description: "I'll explain the goal"

  Capture custom_goal, add to selected_goals
```

EXECUTE (Measurable Targets per Goal):
```
FOR each goal in selected_goals:
  AskUserQuestion:
    questions:
      - question: "For the goal '{goal}', what is a measurable target? (How much improvement? By when?)"
        header: "Measurable Target"
        multiSelect: false
        options:
          - label: "Let me specify"
            description: "I have a specific target in mind"
          - label: "Help me define a target"
            description: "I need guidance on what's realistic"
          - label: "Can't quantify yet"
            description: "I'll revisit this after more discovery"

  IF response == "Let me specify":
    Capture measurable_target from user
    Store in session.business_goals[]:
      {
        goal: goal,
        measurable_target: measurable_target,
        quantified: true
      }

  ELSE IF response == "Help me define a target":
    # Suggest reasonable targets based on goal type
    Display: "Typical targets for '{goal}':"
    IF goal == "Increase revenue":
      Display: "  - 10-20% revenue increase within 12 months"
      Display: "  - $X additional monthly recurring revenue"
    ELSE IF goal == "Reduce costs":
      Display: "  - 15-30% cost reduction within 6 months"
      Display: "  - $X savings per month"
    ELSE IF goal == "Improve efficiency":
      Display: "  - 50% reduction in time-to-complete for key process"
      Display: "  - X hours saved per week per employee"
    ELSE IF goal == "Enhance user experience":
      Display: "  - NPS improvement from X to Y"
      Display: "  - Task completion rate increase to 95%"
    ELSE:
      Display: "  - Specific percentage improvement"
      Display: "  - Specific timeline for achievement"

    AskUserQuestion:
      questions:
        - question: "Based on these examples, what target works for you?"
          header: "Guided Target"
          multiSelect: false
          options:
            - label: "Let me specify my target"
              description: "I'll provide a specific number"

    Capture guided_target
    Store in session.business_goals[]:
      {
        goal: goal,
        measurable_target: guided_target,
        quantified: true
      }

  ELSE IF response == "Can't quantify yet":
    Store in session.business_goals[]:
      {
        goal: goal,
        measurable_target: "To be determined during requirements elicitation",
        quantified: false
      }
```

VERIFY: At least 1 business goal captured with a measurable target (quantified: true).
```
IF session.business_goals is empty OR len(session.business_goals) < 1:
  HALT -- "Step 2.4: No business goals captured. At least 1 required."

quantified_goals = [g for g in session.business_goals WHERE g.quantified == true]
IF len(quantified_goals) < 1:
  HALT -- "Step 2.4: No business goals have measurable targets. At least 1 must be quantified."
```

RECORD: Update checkpoint: `session.phases["02"].questions_answered += (1 + len(session.business_goals))`; `session.completed_outputs.business_goals = session.business_goals`

---

### Step 2.5: Define Success Metrics

EXECUTE:
```
Display:
"Now let's define how you'll measure success. For each business goal,
 we'll identify 1-2 Key Performance Indicators (KPIs)."

FOR each goal in session.business_goals:

  AskUserQuestion:
    questions:
      - question: "How will you measure success for '{goal.goal}'? What KPI(s) should we track?"
        header: "KPI for: {goal.goal}"
        multiSelect: false
        options:
          - label: "Let me define the KPI"
            description: "I have a specific metric in mind"
          - label: "Suggest KPIs for me"
            description: "Help me identify the right metrics"

  IF response == "Let me define the KPI":
    Capture user_kpi from user
    Store in session.success_metrics[]:
      {
        goal: goal.goal,
        kpi: user_kpi,
        source: "user_defined"
      }

  ELSE IF response == "Suggest KPIs for me":
    # Generate KPI suggestions based on goal type
    IF goal.goal == "Increase revenue":
      suggested_kpis = [
        "Monthly Recurring Revenue (MRR)",
        "Average Revenue Per User (ARPU)",
        "Conversion Rate (%)",
        "Customer Lifetime Value (CLV)"
      ]
    ELSE IF goal.goal == "Reduce costs":
      suggested_kpis = [
        "Cost per transaction",
        "Operational cost per month",
        "Time spent on manual tasks (hours/week)",
        "Infrastructure cost per user"
      ]
    ELSE IF goal.goal == "Improve efficiency":
      suggested_kpis = [
        "Task completion time (minutes)",
        "Throughput (units processed per hour)",
        "Error rate (%)",
        "Automation coverage (%)"
      ]
    ELSE IF goal.goal == "Enhance user experience":
      suggested_kpis = [
        "Net Promoter Score (NPS)",
        "Task completion rate (%)",
        "Average session duration",
        "Support ticket volume (per week)"
      ]
    ELSE:
      suggested_kpis = [
        "Custom metric aligned to goal",
        "Percentage improvement over baseline",
        "Time-to-achieve target"
      ]

    AskUserQuestion:
      questions:
        - question: "Which KPI(s) best measure success for '{goal.goal}'?"
          header: "Select KPI"
          multiSelect: true
          options: [format each suggested_kpi as option with description]

    Capture selected_kpis
    FOR each kpi in selected_kpis:
      Store in session.success_metrics[]:
        {
          goal: goal.goal,
          kpi: kpi,
          source: "suggested"
        }

  # Quantify the KPI
  AskUserQuestion:
    questions:
      - question: "What is the target value for this KPI? (e.g., 'reduce from 10 min to 2 min', 'achieve 95% uptime')"
        header: "KPI Target"
        multiSelect: false
        options:
          - label: "Let me specify the target"
            description: "I have a specific number in mind"
          - label: "I don't know the baseline yet"
            description: "Need to measure current state first"

  IF response == "Let me specify the target":
    Capture kpi_target
    Update latest session.success_metrics entry: target_value = kpi_target
  ELSE IF response == "I don't know the baseline yet":
    Update latest session.success_metrics entry: target_value = "Baseline TBD -- measure current state first"
```

VERIFY: At least 1 quantified success metric per business goal.
```
FOR each goal in session.business_goals:
  metrics_for_goal = [m for m in session.success_metrics WHERE m.goal == goal.goal]
  IF len(metrics_for_goal) < 1:
    HALT -- "Step 2.5: No success metric defined for business goal '{goal.goal}'. At least 1 required per goal."

total_metrics = len(session.success_metrics)
IF total_metrics < 1:
  HALT -- "Step 2.5: No success metrics captured. At least 1 required."
```

RECORD: Update checkpoint: `session.phases["02"].questions_answered += (2 * len(session.business_goals))`; `session.completed_outputs.success_metrics = session.success_metrics`

---

### Step 2.6: Establish Scope Boundaries

EXECUTE (In Scope):
```
AskUserQuestion:
  questions:
    - question: "What should be IN scope for this project? What must the first release include?"
      header: "In Scope"
      multiSelect: false
      options:
        - label: "Let me list the in-scope items"
          description: "I'll describe what must be included"
        - label: "I need help defining scope"
          description: "Help me determine what's essential"
```

Decision Logic (In Scope):
```
IF response == "Let me list the in-scope items":
  Capture in_scope_items from user (free text, parse into list)
  Store in session.scope_boundaries.in_scope = in_scope_items

ELSE IF response == "I need help defining scope":
  # Derive scope suggestions from problem statement and personas
  Display:
  "Based on your problem statement and user personas, here are likely in-scope items:"
  Display: "  - Core workflow to address '{session.problem_statement}'"
  FOR each persona in session.personas:
    Display: "  - Features for {persona.name}: {persona.goals}"

  AskUserQuestion:
    questions:
      - question: "Which of these should definitely be in scope?"
        header: "Confirm Scope"
        multiSelect: false
        options:
          - label: "All of these are in scope"
            description: "Include everything listed"
          - label: "Let me adjust"
            description: "I'll modify the list"

  IF response == "All of these are in scope":
    session.scope_boundaries.in_scope = derived_items
  ELSE IF response == "Let me adjust":
    Capture user adjustments
    session.scope_boundaries.in_scope = adjusted_items
```

EXECUTE (Out of Scope):
```
AskUserQuestion:
  questions:
    - question: "What should be explicitly OUT of scope? What are you NOT building in the first release?"
      header: "Out of Scope"
      multiSelect: false
      options:
        - label: "Let me list exclusions"
          description: "I'll describe what's out of scope"
        - label: "Suggest common exclusions"
          description: "Help me think about what to exclude"
```

Decision Logic (Out of Scope):
```
IF response == "Let me list exclusions":
  Capture out_of_scope_items from user
  Store in session.scope_boundaries.out_of_scope = out_of_scope_items

ELSE IF response == "Suggest common exclusions":
  Display:
  "Common out-of-scope items for first releases:"
  Display: "  - Advanced analytics and reporting"
  Display: "  - Multi-language/internationalization"
  Display: "  - Mobile-native apps (if web-first)"
  Display: "  - Third-party marketplace integrations"
  Display: "  - Advanced admin/configuration tools"
  Display: "  - Performance optimization beyond baseline"

  AskUserQuestion:
    questions:
      - question: "Which of these are out of scope? Add any others."
        header: "Confirm Exclusions"
        multiSelect: false
        options:
          - label: "Let me confirm and add"
            description: "I'll finalize the exclusions list"

  Capture user's confirmed exclusions
  session.scope_boundaries.out_of_scope = confirmed_exclusions
```

EXECUTE (Future Scope):
```
AskUserQuestion:
  questions:
    - question: "Anything to defer to a future phase or release?"
      header: "Future Scope"
      multiSelect: false
      options:
        - label: "Yes, let me list deferred items"
          description: "Some things should wait for Release 2+"
        - label: "No, everything is either in or out"
          description: "Nothing deferred"
        - label: "Move some out-of-scope to future"
          description: "I want to eventually build some excluded items"
```

Decision Logic (Future Scope):
```
IF response == "Yes, let me list deferred items":
  Capture future_items from user
  session.scope_boundaries.future = future_items

ELSE IF response == "No, everything is either in or out":
  session.scope_boundaries.future = []

ELSE IF response == "Move some out-of-scope to future":
  Display: "Current out-of-scope items:"
  FOR each item in session.scope_boundaries.out_of_scope:
    Display: "  - {item}"

  AskUserQuestion:
    questions:
      - question: "Which out-of-scope items should move to future releases?"
        header: "Defer to Future"
        multiSelect: false
        options:
          - label: "Let me select"
            description: "I'll identify which to defer"

  Capture items_to_defer
  # Move selected items from out_of_scope to future
  session.scope_boundaries.future = items_to_defer
  session.scope_boundaries.out_of_scope = [remove deferred items from out_of_scope]
```

VERIFY: in_scope has at least 1 item, out_of_scope has at least 1 item.
```
IF session.scope_boundaries.in_scope is null OR len(session.scope_boundaries.in_scope) < 1:
  HALT -- "Step 2.6: No in-scope items defined. At least 1 required."

IF session.scope_boundaries.out_of_scope is null OR len(session.scope_boundaries.out_of_scope) < 1:
  HALT -- "Step 2.6: No out-of-scope items defined. At least 1 required to prevent scope creep."
```

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 3`; `session.completed_outputs.scope_boundaries = session.scope_boundaries`

---

### Step 2.7: Complexity Assessment (Chain-of-Thought)

EXECUTE (Multi-Dimensional Scoring):
```
Display:
"Now I'll assess the project complexity across 4 dimensions.
 This helps calibrate the depth of requirements elicitation in later phases."

<thinking>
Score each of the 4 dimensions below with explicit reasoning:

1. SCOPE (1-5): How many features, entities, or user flows?
   - Consider: number of in-scope items from Step 2.6
   - Consider: number of user types from Step 2.2
   - Consider: number of personas from Step 2.3
   - 1 = Single feature, 1 user type
   - 2 = 2-3 features, 1-2 user types
   - 3 = 4-6 features, 2-3 user types
   - 4 = 7-10 features, 3-4 user types
   - 5 = 10+ features, 5+ user types
   Score: {N} because {reasoning}

2. TECHNICAL RISK (1-5): How novel or uncertain is the technology?
   - Consider: problem statement novelty
   - Consider: whether existing solutions exist
   - Consider: performance/security requirements implied by goals
   - 1 = Well-known patterns, standard CRUD
   - 2 = Minor technical challenges, common integrations
   - 3 = Some novel elements, moderate complexity
   - 4 = Significant unknowns, advanced patterns
   - 5 = Cutting-edge tech, research-grade problems
   Score: {N} because {reasoning}

3. INTEGRATION SURFACE (1-5): How many external systems or touchpoints?
   - Consider: user types that imply external systems
   - Consider: business goals that require data from other systems
   - Consider: scope items mentioning APIs or integrations
   - 1 = Self-contained, no external dependencies
   - 2 = 1-2 simple integrations (e.g., email, auth)
   - 3 = 3-4 integrations with moderate complexity
   - 4 = 5-7 integrations including real-time data
   - 5 = 8+ integrations, complex orchestration
   Score: {N} because {reasoning}

4. DOMAIN NOVELTY (1-5): How familiar is the problem domain?
   - Consider: how well the user articulated the problem (strong = familiar domain)
   - Consider: industry-specific regulations or standards
   - Consider: whether personas are well-defined (well-defined = familiar domain)
   - 1 = Very familiar, standard business domain
   - 2 = Mostly familiar, minor domain learning
   - 3 = Moderately familiar, some domain expertise needed
   - 4 = Unfamiliar domain, significant learning curve
   - 5 = Highly specialized, requires deep domain expertise
   Score: {N} because {reasoning}

TOTAL = Scope + Technical Risk + Integration Surface + Domain Novelty

Tier mapping:
  Tier 1 (4-8):   Simple       -- Minimal requirements elicitation needed
  Tier 2 (9-12):  Moderate     -- Standard requirements process
  Tier 3 (13-16): Complex      -- Deep elicitation with multiple rounds
  Tier 4 (17-20): Enterprise   -- Extensive discovery, multiple stakeholder rounds
</thinking>
```

EXECUTE (Present Assessment to User):
```
complexity_assessment = {
  scope: { score: N, reasoning: "..." },
  technical_risk: { score: N, reasoning: "..." },
  integration_surface: { score: N, reasoning: "..." },
  domain_novelty: { score: N, reasoning: "..." },
  total: sum_of_all_scores,
  tier: derived_tier,
  tier_label: derived_tier_label
}

Display:
"Complexity Assessment:
  Scope:               {score}/5 - {reasoning}
  Technical Risk:      {score}/5 - {reasoning}
  Integration Surface: {score}/5 - {reasoning}
  Domain Novelty:      {score}/5 - {reasoning}
  ────────────────────────────────
  Total:               {total}/20
  Tier:                {tier} ({tier_label})

  Impact: {tier_impact_description}"

AskUserQuestion:
  questions:
    - question: "Does this complexity assessment seem accurate?"
      header: "Validate Assessment"
      multiSelect: false
      options:
        - label: "Yes, that's accurate"
          description: "Proceed with this assessment"
        - label: "It's more complex than shown"
          description: "Complexity is underestimated"
        - label: "It's simpler than shown"
          description: "Complexity is overestimated"
```

Decision Logic:
```
IF response == "Yes, that's accurate":
  session.complexity_assessment = complexity_assessment
  session.complexity_validated = true

ELSE IF response == "It's more complex than shown":
  AskUserQuestion:
    questions:
      - question: "Which dimension(s) are underestimated? What am I missing?"
        header: "Adjust Upward"
        multiSelect: false
        options:
          - label: "Let me explain"
            description: "I'll describe the additional complexity"

  Capture user's explanation
  Adjust relevant dimension scores upward (recalculate total and tier)
  session.complexity_assessment = adjusted_assessment
  session.complexity_validated = true

ELSE IF response == "It's simpler than shown":
  AskUserQuestion:
    questions:
      - question: "Which dimension(s) are overestimated?"
        header: "Adjust Downward"
        multiSelect: false
        options:
          - label: "Let me explain"
            description: "I'll clarify what's simpler"

  Capture user's explanation
  Adjust relevant dimension scores downward (recalculate total and tier)
  session.complexity_assessment = adjusted_assessment
  session.complexity_validated = true
```

VERIFY: complexity_assessment has all 4 dimensions scored with reasoning.
```
IF session.complexity_assessment is null:
  HALT -- "Step 2.7: Complexity assessment not generated."

FOR dimension in ["scope", "technical_risk", "integration_surface", "domain_novelty"]:
  IF session.complexity_assessment[dimension] is null:
    HALT -- "Step 2.7: Dimension '{dimension}' not scored."
  IF session.complexity_assessment[dimension].score < 1 OR session.complexity_assessment[dimension].score > 5:
    HALT -- "Step 2.7: Dimension '{dimension}' score out of range (1-5). Got: {score}."
  IF session.complexity_assessment[dimension].reasoning is null or empty:
    HALT -- "Step 2.7: Dimension '{dimension}' missing reasoning."

IF session.complexity_assessment.total is null:
  HALT -- "Step 2.7: Total score not calculated."

IF session.complexity_assessment.tier is null:
  HALT -- "Step 2.7: Tier not derived from total score."
```

RECORD: Update checkpoint: `session.phases["02"].questions_answered += 1`; `session.completed_outputs.complexity_assessment = session.complexity_assessment`

---

### Step 2.8: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session Management"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 3 (Requirements Elicitation)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit -- resume with /ideate --resume {IDEATION_ID}"

  IF response == "Save and continue later":
    Write updated checkpoint with all Phase 02 data
    Display: "Session saved. Resume with: /ideate --resume {IDEATION_ID}"
    EXIT skill

ELSE:
  Display: "Context window healthy. Proceeding to Phase 3."
```

VERIFY: Context window check was performed (either threshold check or healthy confirmation).
IF check was skipped: HALT -- "Step 2.8: Context Window Check not performed."

RECORD: Update checkpoint: `session.phases["02"].context_check_completed = true`

---

## Phase Exit Verification

Before transitioning to Phase 03, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.problem_statement is non-empty and len(session.problem_statement) >= 20
    IF FAIL: HALT -- "Exit blocked: Problem statement not captured or too vague."

  CHECK: len(session.user_types) >= 1
    IF FAIL: HALT -- "Exit blocked: No user types identified."

  CHECK: ALL user_types have volume (user_type.volume is not null for each)
    IF FAIL: HALT -- "Exit blocked: User type '{type}' missing volume estimate."

  CHECK: len(session.personas) >= 1
    IF FAIL: HALT -- "Exit blocked: No personas documented."

  CHECK: ALL personas have goals AND pain_points (non-empty for each)
    IF FAIL: HALT -- "Exit blocked: Persona '{name}' missing goals or pain_points."

  CHECK: len(session.business_goals) >= 1 AND at least 1 has quantified == true
    IF FAIL: HALT -- "Exit blocked: No business goals captured or none are quantified."

  CHECK: len(session.success_metrics) >= 1
    IF FAIL: HALT -- "Exit blocked: No success metrics defined."

  CHECK: FOR each goal in session.business_goals: at least 1 metric exists for that goal
    IF FAIL: HALT -- "Exit blocked: Business goal '{goal}' has no success metric."

  CHECK: session.scope_boundaries.in_scope is not null AND len(session.scope_boundaries.in_scope) >= 1
    IF FAIL: HALT -- "Exit blocked: No in-scope items defined."

  CHECK: session.scope_boundaries.out_of_scope is not null AND len(session.scope_boundaries.out_of_scope) >= 1
    IF FAIL: HALT -- "Exit blocked: No out-of-scope items defined."

  CHECK: session.complexity_assessment is not null AND all 4 dimensions scored
    IF FAIL: HALT -- "Exit blocked: Complexity assessment incomplete."

  CHECK: session.phases["02"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."

  CHECK: session.phases["02"].questions_answered >= 5
    IF FAIL: HALT -- "Exit blocked: Minimum 5 questions required, only {count} answered."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 3
checkpoint.progress.phases_completed.append("02")
checkpoint.progress.completion_percentage = round(2/7 * 100)

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: Checkpoint file updated on disk with `current_phase = 3`.
IF write fails: HALT -- "Phase 02 exit checkpoint not saved."

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 2 Complete: Discovery & Problem Understanding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem Statement:
  \"{session.problem_statement}\"

User Types: {len(session.user_types)} identified
  {FOR each user_type: '- {type} ({volume} users)'}

Personas: {len(session.personas)} documented
  {FOR each persona: '- {name}: {goals_summary}'}

Business Goals: {len(session.business_goals)} defined
  {FOR each goal: '- {goal} (Target: {measurable_target})'}

Scope:
  In:  {len(session.scope_boundaries.in_scope)} items
  Out: {len(session.scope_boundaries.out_of_scope)} items

Complexity: Tier {tier} ({tier_label}) -- {total}/20
  Scope: {score}/5 | Risk: {score}/5 | Integration: {score}/5 | Novelty: {score}/5

Proceeding to Phase 3: Requirements Elicitation...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
