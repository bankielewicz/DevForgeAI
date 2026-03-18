# Phase 06: Prioritization

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Rank opportunities and solutions using MoSCoW and Impact-Effort analysis |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/prioritization-workflow.md` |
| **STEP COUNT** | 5 mandatory steps |
| **MINIMUM QUESTIONS** | 2 |

## Phase Exit Criteria

- [ ] All opportunities classified with MoSCoW
- [ ] At least 1 Must Have identified
- [ ] Impact-Effort assessed for Must/Should Have items
- [ ] Recommended sequence generated
- [ ] User validated sequence
- [ ] Checkpoint updated

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/prioritization-workflow.md")
```

IF Read fails: HALT -- "Phase 06 cannot proceed without reference file."

---

## Mandatory Steps

### Step 6.1: Compile Items for Prioritization

```
EXECUTE:
  items_to_prioritize = []

  # Opportunities from Phase 3
  FOR each opportunity in session.opportunities:
    items_to_prioritize.append({
      id: "OPP-{index}",
      description: opportunity.description,
      source: opportunity.source,
      type: "opportunity"
    })

  # Must-have capabilities from success vision
  FOR each capability in session.success_vision.metrics:
    items_to_prioritize.append({
      id: "CAP-{index}",
      description: capability,
      source: "success_vision",
      type: "capability"
    })

  # Adjacent problems from Phase 3
  FOR each adjacent in session.adjacent_opportunities:
    items_to_prioritize.append({
      id: "ADJ-{index}",
      description: adjacent.problem,
      source: "adjacent",
      type: "adjacent"
    })

  session.prioritization_items = items_to_prioritize

  Display:
    "We have {len(items)} items to prioritize:

    Opportunities:
      - OPP-1: {description}
      - OPP-2: {description}

    Capabilities:
      - CAP-1: {description}

    Adjacent Problems:
      - ADJ-1: {description}

    Let's classify each one."

VERIFY:
  - At least 1 item compiled for prioritization
  - Each item has id, description, source, and type fields
  - Items drawn from Phase 3 outputs and success vision

RECORD:
  session.prioritization_items = items_to_prioritize
  Update checkpoint: { phase: 6, step: "6.1", status: "complete" }
```

---

### Step 6.2: MoSCoW Classification

```
EXECUTE:
  FOR each item in session.prioritization_items:
    AskUserQuestion:
      questions:
        - question: "How would you classify '{item.description}'?"
          header: "Priority"
          multiSelect: false
          options:
            - label: "Must Have"
              description: "Critical - project fails without it"
            - label: "Should Have"
              description: "Important but can work around"
            - label: "Could Have"
              description: "Nice to have if time/budget allows"
            - label: "Won't Have (this time)"
              description: "Explicitly out of scope"

    item.moscow = response

  # Categorize results
  session.moscow = {
    must_have: [items where moscow == "Must Have"],
    should_have: [items where moscow == "Should Have"],
    could_have: [items where moscow == "Could Have"],
    wont_have: [items where moscow == "Won't Have (this time)"]
  }

  # Validation Check: 0 Must Haves
  IF len(must_have) == 0:
    Display: "No Must Haves identified. Are you sure nothing is critical?"
    AskUserQuestion:
      questions:
        - question: "Is there truly nothing that's absolutely required?"
          header: "Confirm"
          multiSelect: false
          options:
            - label: "Correct - all flexible"
              description: "Everything is negotiable"
            - label: "Let me reconsider"
              description: "I'll upgrade some items"

    IF response == "Let me reconsider":
      Re-present items for reclassification

  # Validation Check: 5+ Must Haves
  IF len(must_have) > 5:
    Display: "Many Must Haves identified. This may exceed constraints."
    AskUserQuestion:
      questions:
        - question: "Can we reduce the Must Haves to focus on the most critical?"
          header: "Reduce"
          multiSelect: false
          options:
            - label: "Yes, let me reconsider"
              description: "I'll downgrade some items"
            - label: "All are truly critical"
              description: "Keep as is"

    IF response == "Yes, let me reconsider":
      Re-present Must Have items for reclassification

VERIFY:
  - Every item has a moscow classification
  - At least 1 Must Have identified (or explicit user override via "Correct - all flexible")
  - Must Have count validated (warning given if > 5)

RECORD:
  session.moscow = { must_have, should_have, could_have, wont_have }
  Update checkpoint: { phase: 6, step: "6.2", status: "complete" }
```

---

### Step 6.3: Impact-Effort Matrix

```
EXECUTE:
  Display:
    "Now let's assess impact and effort for each Must Have and Should Have item.

    This will help determine the optimal sequence.

         HIGH IMPACT
              |
      Major   |   Quick
     Projects |   Wins
    ----------+-----------
      Avoid   |  Fill-ins
              |
         LOW IMPACT
       HIGH EFFORT   LOW EFFORT
    "

  FOR each item in [must_have + should_have]:
    # Impact assessment
    AskUserQuestion:
      questions:
        - question: "What is the expected impact of '{item.description}'?"
          header: "Impact"
          multiSelect: false
          options:
            - label: "High impact"
              description: "Significant business value"
            - label: "Medium impact"
              description: "Moderate business value"
            - label: "Low impact"
              description: "Minor business value"

    item.impact = response

    # Effort assessment
    AskUserQuestion:
      questions:
        - question: "How much effort do you estimate '{item.description}' would require?"
          header: "Effort"
          multiSelect: false
          options:
            - label: "Low effort"
              description: "Days to a week"
            - label: "Medium effort"
              description: "Weeks to a month"
            - label: "High effort"
              description: "Months of work"

    item.effort = response

  # Categorize by quadrant
  session.impact_effort = {
    quick_wins:     [items where impact in ["High","Medium"] AND effort == "Low"],
    major_projects: [items where impact in ["High","Medium"] AND effort == "High"],
    fill_ins:       [items where impact == "Low" AND effort == "Low"],
    avoid:          [items where impact == "Low" AND effort == "High"]
  }

VERIFY:
  - Every Must Have and Should Have item has impact AND effort ratings
  - Items categorized into exactly one quadrant
  - No items left uncategorized

RECORD:
  session.impact_effort = { quick_wins, major_projects, fill_ins, avoid }
  Update checkpoint: { phase: 6, step: "6.3", status: "complete" }
```

---

### Step 6.4: Generate Recommended Sequence

```
EXECUTE:
  sequence = []
  order = 1

  # 1. Quick Wins that are Must Have (do first)
  FOR item in quick_wins WHERE item.id in must_have_ids:
    sequence.append({
      order: order,
      item: item,
      rationale: "Quick Win + Must Have = Do first"
    })
    order += 1

  # 2. Quick Wins that are Should Have
  FOR item in quick_wins WHERE item.id in should_have_ids:
    sequence.append({
      order: order,
      item: item,
      rationale: "Quick Win + Should Have = Do early"
    })
    order += 1

  # 3. Major Projects that are Must Have
  FOR item in major_projects WHERE item.id in must_have_ids:
    sequence.append({
      order: order,
      item: item,
      rationale: "Major Project + Must Have = Plan carefully"
    })
    order += 1

  # 4. Major Projects that are Should Have
  FOR item in major_projects WHERE item.id in should_have_ids:
    sequence.append({
      order: order,
      item: item,
      rationale: "Major Project + Should Have = If time allows"
    })
    order += 1

  # 5. Fill-ins
  FOR item in fill_ins:
    sequence.append({
      order: order,
      item: item,
      rationale: "Fill-in = When bandwidth available"
    })
    order += 1

  session.recommended_sequence = sequence

  Display:
    "Based on MoSCoW and Impact-Effort analysis, here's the recommended sequence:

    1. {item_1} - Quick Win + Must Have
    2. {item_2} - Quick Win + Should Have
    3. {item_3} - Major Project + Must Have
    ...

    Items to avoid or defer:
    - {avoid_item} (Low impact, high effort)"

VERIFY:
  - Sequence contains all Must Have and Should Have items
  - Sequence follows the algorithm order: QW+Must > QW+Should > MP+Must > MP+Should > Fill-ins
  - Avoid items listed separately (not in sequence)

RECORD:
  session.recommended_sequence = sequence
  Update checkpoint: { phase: 6, step: "6.4", status: "complete" }
```

---

### Step 6.5: Validate Sequence

```
EXECUTE:
  AskUserQuestion:
    questions:
      - question: "Does this sequence look right? Any adjustments needed?"
        header: "Validate"
        multiSelect: false
        options:
          - label: "Yes, looks good"
            description: "Proceed with this sequence"
          - label: "Adjust order"
            description: "I'd like to change the priority"
          - label: "Add dependencies"
            description: "Some items depend on others"

  IF response == "Adjust order":
    AskUserQuestion:
      questions:
        - question: "What would you like to move?"
          header: "Move"
          multiSelect: false
          options:
            - label: "Move {item_1} higher"
              description: "Should be done earlier"
            - label: "Move {item_2} lower"
              description: "Can wait"
            - label: "Other changes"
              description: "Let me explain"

    Apply adjustments to sequence
    Re-display updated sequence

  IF response == "Add dependencies":
    AskUserQuestion:
      questions:
        - question: "Which item depends on another?"
          header: "Dependency"
          multiSelect: false
          options:
            - label: "{item_2} depends on {item_1}"
              description: "Must complete {item_1} first"
            # ... other dependency options dynamically generated

    Record dependencies
    Re-sort sequence respecting dependency order

VERIFY:
  - User explicitly validated the final sequence
  - If adjustments made, updated sequence re-displayed and re-validated
  - Dependencies recorded (if any)

RECORD:
  session.recommended_sequence = [final validated sequence]
  session.dependencies = [recorded dependencies]
  Update checkpoint: { phase: 6, step: "6.5", status: "complete", phase_complete: true }
```

---

## Phase 6 Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 6 Complete: Prioritization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MoSCoW Classification:
  Must Have: {count}
  Should Have: {count}
  Could Have: {count}
  Won't Have: {count}

Impact-Effort Analysis:
  Quick Wins: {count}
  Major Projects: {count}
  Fill-ins: {count}
  Avoid: {count}

Recommended Start:
  1. {first_item}

Proceeding to Phase 7: Handoff Synthesis...
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Everything is Must Have | 10+ Must Haves | Force rank top 3-5 |
| Everything is Quick Win | Underestimating effort | Probe for hidden complexity |
| Nothing is Must Have | All items optional | Ask about project success criteria |
| Circular dependencies | A depends on B depends on A | Identify minimum viable scope |
