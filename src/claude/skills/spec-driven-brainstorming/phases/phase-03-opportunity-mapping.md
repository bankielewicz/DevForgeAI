# Phase 03: Opportunity Mapping

## Contract

| Attribute | Value |
|-----------|-------|
| PURPOSE | Explore WHAT COULD BE through blue-sky thinking, market research, and solution ideation. |
| REFERENCE | `.claude/skills/spec-driven-brainstorming/references/opportunity-mapping-workflow.md` |
| STEP COUNT | 8 mandatory steps |
| MINIMUM QUESTIONS | 3 |

---

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Research decision made (conducted or skipped)
- [ ] Ideal state described (session.ideal_state is non-empty)
- [ ] Success metrics identified (session.success_vision is non-empty)
- [ ] At least 1 opportunity identified (session.opportunities.length >= 1)
- [ ] Adjacent problems explored
- [ ] Opportunities compiled
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 04.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/opportunity-mapping-workflow.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 3.1: Research Option

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "Would you like to include market research in this brainstorm?"
      header: "Research"
      multiSelect: false
      options:
        - label: "Yes - Research competitors & trends (Recommended)"
          description: "I'll search for market data and competitor approaches"
        - label: "Skip - Use internal knowledge only"
          description: "Faster session, relies on what you know"
```

**VERIFY:**
- User response is non-empty
- Response maps to one of the two options

**DECISION LOGIC:**
```
IF response == "Yes - Research competitors & trends (Recommended)":
  session.research_enabled = true
  GOTO Step 3.2 (Conduct Market Research)
ELSE:
  session.research_enabled = false
  session.market_research = null
  SKIP Step 3.2, GOTO Step 3.3
```

**RECORD:**
- `session.research_enabled` = true or false
- Increment question counter
- Update checkpoint: `checkpoint.completed_outputs.research_decision = session.research_enabled`

---

### Step 3.2: Conduct Market Research [CONDITIONAL]

**CONDITION:** Only execute if `session.research_enabled == true`. If false, skip to Step 3.3.

**EXECUTE:**
```
Display: "Researching market solutions and competitor approaches..."

Task(
  subagent_type="internet-sleuth",
  prompt="Research market trends and competitor approaches for:
          Problem: {session.problem_statement}
          Find: competitors, available solutions, market trends, case studies.
          Return structured findings."
)
```

**VERIFY:**
Task returned result OR gracefully degraded.
```
IF task_result is null (timeout/failure):
  Display: "Research unavailable. Continuing with internal knowledge."
  session.research_enabled = false
  session.market_research = null
ELSE:
  Store in session.market_research
```

**Expected output structure (when successful):**
```yaml
session.market_research:
  competitors:
    - name: "Competitor A"
      approach: "description"
      pros: [...]
      cons: [...]
  trends: [...]
  technologies: [...]
  case_studies: [...]
```

**RECORD:**
- IF subagent invoked: record subagent execution
- `checkpoint.completed_outputs.market_research = session.market_research`
- `checkpoint.completed_outputs.research_conducted = (session.market_research != null)`

---

### Step 3.3: Blue-Sky Visioning

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "If you had unlimited resources, what would the ideal solution look like?"
      header: "Ideal State"
      multiSelect: false
      options:
        - label: "Let me describe it"
          description: "I have a vision to share"
        - label: "Help me brainstorm"
          description: "Guide me with questions"
```

**VERIFY:**
- User response is non-empty
- Response maps to one of the two options

**FOLLOW-UP PATH (if user selected "Help me brainstorm"):**
```
IF response == "Help me brainstorm":
  AskUserQuestion:
    questions:
      - question: "In an ideal world, how fast would this process be?"
        header: "Ideal Speed"
        multiSelect: false
        options:
          - label: "Instant"
            description: "Happens immediately"
          - label: "Minutes"
            description: "Done in a few minutes"
          - label: "Same day"
            description: "Completed within hours"

  AskUserQuestion:
    questions:
      - question: "In an ideal world, who would do this work?"
        header: "Ideal Actor"
        multiSelect: false
        options:
          - label: "Fully automated"
            description: "No human intervention"
          - label: "Minimal human oversight"
            description: "Humans review exceptions"
          - label: "Assisted by technology"
            description: "Humans do it faster with help"

  Synthesize user's speed + actor answers into session.ideal_state
```

**RECORD:**
- `session.ideal_state` = user description or synthesized ideal state
- Increment question counter (by 1 if "Let me describe it", by 3 if "Help me brainstorm")
- Update checkpoint: `checkpoint.completed_outputs.ideal_state = session.ideal_state`

---

### Step 3.4: Success Vision

**EXECUTE (Part A - Vision):**
```
AskUserQuestion:
  questions:
    - question: "What would change in your organization if this problem was completely solved?"
      header: "Vision"
      multiSelect: false
      options:
        - label: "Let me describe"
          description: "I'll paint the picture"
```

**VERIFY (Part A):**
- User response is non-empty
- Store description in `session.success_vision.description`

**EXECUTE (Part B - Metrics):**
```
AskUserQuestion:
  questions:
    - question: "How would you measure success for this initiative?"
      header: "Success Metrics"
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

**VERIFY (Part B):**
- At least 1 metric selected
- Store in `session.success_vision.metrics`

**RECORD:**
- `session.success_vision.description` = user vision description
- `session.success_vision.metrics` = selected metrics array
- Increment question counter by 2
- Update checkpoint: `checkpoint.completed_outputs.success_vision = session.success_vision`

---

### Step 3.5: Technology Opportunities

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "Are there any technologies you've heard about that might help?"
      header: "Tech Ideas"
      multiSelect: true
      options:
        - label: "AI/ML automation"
          description: "Artificial intelligence solutions"
        - label: "Process automation (RPA)"
          description: "Robotic process automation"
        - label: "Cloud migration"
          description: "Moving to cloud infrastructure"
        - label: "Integration/APIs"
          description: "Connecting existing systems"
        - label: "Mobile/Web apps"
          description: "New user interfaces"
        - label: "Data analytics"
          description: "Better insights and reporting"
```

**VERIFY:**
- Response captured (may be empty array if none selected -- that is valid)
- Store selections in `session.technology_ideas`

**FOLLOW-UP (for each selected technology):**
```
IF len(selected_technologies) > 0:
  FOR each technology in selected_technologies:
    AskUserQuestion:
      questions:
        - question: "Why do you think {technology} might help?"
          header: "Rationale"
          multiSelect: false
          options:
            - label: "Let me explain"
              description: "I have specific reasons"
            - label: "Just heard about it"
              description: "Worth exploring"

    Store rationale in session.technology_ideas[].rationale
```

**RECORD:**
- `session.technology_ideas` = array of {name, rationale} objects
- Increment question counter by 1 + number of follow-up rationale questions
- Update checkpoint: `checkpoint.completed_outputs.technology_ideas = session.technology_ideas`

---

### Step 3.6: Adjacent Opportunities

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "Are there related problems that could be solved at the same time?"
      header: "Related"
      multiSelect: false
      options:
        - label: "Yes, several"
          description: "Multiple related issues"
        - label: "Maybe one or two"
          description: "A few possibilities"
        - label: "No, this is isolated"
          description: "Problem is independent"
        - label: "Not sure"
          description: "Haven't thought about it"
```

**VERIFY:**
- User response is non-empty
- Response maps to one of the four options

**FOLLOW-UP (if adjacent problems exist):**
```
IF response in ["Yes, several", "Maybe one or two"]:
  FOR i in [1..3]:
    Capture related_problem from user input
    IF related_problem is empty: BREAK

    AskUserQuestion:
      questions:
        - question: "How is '{related_problem}' connected to the main problem?"
          header: "Connection"
          multiSelect: false
          options:
            - label: "Same root cause"
              description: "Both stem from same issue"
            - label: "Same stakeholders"
              description: "Affects same people"
            - label: "Same system"
              description: "Same technology involved"
            - label: "Same process"
              description: "Part of same workflow"

    Store in session.adjacent_opportunities[]
```

**RECORD:**
- `session.adjacent_opportunities` = array of {problem, connection} objects (may be empty)
- Increment question counter by 1 + number of follow-up connection questions
- Update checkpoint: `checkpoint.completed_outputs.adjacent_opportunities = session.adjacent_opportunities`

---

### Step 3.7: Compile Opportunities

**EXECUTE:**
```
opportunities = []

# From user vision
opportunities.append({
  source: "user_vision",
  description: session.ideal_state,
  type: "solution"
})

# From technology ideas
FOR tech in session.technology_ideas:
  opportunities.append({
    source: "technology",
    description: "Implement {tech.name}",
    rationale: tech.rationale
  })

# From market research (if available)
IF session.market_research:
  FOR competitor in session.market_research.competitors:
    opportunities.append({
      source: "competitor",
      description: "Adopt {competitor.approach}",
      pros: competitor.pros,
      cons: competitor.cons
    })

# From adjacent problems
FOR adjacent in session.adjacent_opportunities:
  opportunities.append({
    source: "adjacent",
    description: "Also solve: {adjacent.problem}",
    synergy: adjacent.synergy
  })

session.opportunities = opportunities
```

**Display to user:**
```
Display:
"I've identified {len(opportunities)} potential opportunities:

1. {opportunity_1.description}
2. {opportunity_2.description}
...

These will be prioritized in Phase 6."
```

**VERIFY:**
- `session.opportunities` array has at least 1 entry
- All sources aggregated (user_vision, technology, competitor if research conducted, adjacent if any)
- Summary displayed to user

**RECORD:**
- `session.opportunities` = compiled opportunity array
- Update checkpoint: `checkpoint.completed_outputs.opportunities = session.opportunities`

---

### Step 3.8: Context Window Check

**EXECUTE:**
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 4 (Constraint Discovery)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit"

  IF response == "Save and continue later":
    Write checkpoint with all Phase 03 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  # Context usage acceptable, continue automatically
```

**VERIFY:**
- Context usage estimated
- If over threshold: user decision captured
- If save requested: checkpoint written to disk, verified via Glob

**RECORD:**
- `checkpoint.progress.current_phase = 3` (completed)
- `checkpoint.progress.phases_completed` includes 3
- Increment `checkpoint.progress.completion_percentage`
- Write checkpoint to disk: `devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json`

---

## Phase 03 Checkpoint Update

After all steps complete, write the following to the checkpoint:

```json
{
  "progress": {
    "current_phase": 4,
    "phases_completed": [..., 3],
    "completion_percentage": "updated"
  },
  "completed_outputs": {
    "research_decision": true/false,
    "research_conducted": true/false,
    "market_research": { ... } or null,
    "ideal_state": "...",
    "success_vision": { "description": "...", "metrics": [...] },
    "technology_ideas": [ ... ],
    "adjacent_opportunities": [ ... ],
    "opportunities": [ ... ]
  }
}
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 03 checkpoint was NOT saved."

---

## Phase Transition Display

```
Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 3 Complete: Opportunity Mapping
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Research: {conducted/skipped}
{IF conducted: Competitors analyzed: {count}}

Opportunities Identified: {count}
  - {opp_1}
  - {opp_2}
  - {opp_3}

Adjacent Problems: {count}

Proceeding to Phase 4: Constraint Discovery...
"
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Research times out | Subagent takes too long | Skip research, continue |
| No technology ideas | User unfamiliar with options | Provide common suggestions |
| Ideal state too vague | "Make it better" | Ask for specific metrics |
| Too many opportunities | 20+ identified | Group similar ones, prioritize later |
