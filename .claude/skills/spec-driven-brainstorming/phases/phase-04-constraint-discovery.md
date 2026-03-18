# Phase 04: Constraint Discovery

## Contract

| Attribute | Value |
|-----------|-------|
| PURPOSE | Understand WHAT LIMITS the solution space through budget, timeline, resource, and organizational constraints. |
| REFERENCE | `.claude/skills/spec-driven-brainstorming/references/constraint-discovery-workflow.md` |
| STEP COUNT | 5 mandatory steps |
| MINIMUM QUESTIONS | 3 |

---

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Budget range identified (even if "TBD")
- [ ] Timeline identified
- [ ] Resource availability assessed
- [ ] Technical constraints documented
- [ ] Organizational constraints documented
- [ ] Checkpoint updated with phase data

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 05.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/constraint-discovery-workflow.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 4.1: Budget Constraints

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "What budget range is available for this initiative?"
      header: "Budget"
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

**VERIFY:**
- User response is non-empty
- Response maps to one of the six options
- Store in `session.constraints.budget.range`

**FOLLOW-UP (conditional -- only if budget is defined):**
```
IF response != "Not defined yet":
  AskUserQuestion:
    questions:
      - question: "Is this budget flexible or fixed?"
        header: "Flexibility"
        multiSelect: false
        options:
          - label: "Fixed - cannot exceed"
            description: "Hard budget limit"
          - label: "Somewhat flexible"
            description: "Can adjust with justification"
          - label: "Very flexible"
            description: "Budget can grow if value proven"

  Store in session.constraints.budget.flexibility

  AskUserQuestion:
    questions:
      - question: "Is there budget for ongoing operational costs?"
        header: "Ongoing"
        multiSelect: false
        options:
          - label: "Yes - included in budget"
            description: "Operating costs considered"
          - label: "Separate budget"
            description: "OpEx is different from CapEx"
          - label: "Not considered yet"
            description: "Need to discuss"

  Store in session.constraints.budget.ongoing_costs

ELSE:
  session.constraints.budget.flexibility = "TBD"
  session.constraints.budget.ongoing_costs = "TBD"
```

**RECORD:**
- `session.constraints.budget` = {range, flexibility, ongoing_costs}
- Increment question counter by 1 (if TBD) or 3 (if defined with follow-ups)
- Update checkpoint: `checkpoint.completed_outputs.constraints.budget = session.constraints.budget`

---

### Step 4.2: Timeline Constraints

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "When does this need to be done?"
      header: "Timeline"
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

**VERIFY:**
- User response is non-empty
- Response maps to one of the five options
- Store in `session.constraints.timeline.target`

**FOLLOW-UP (conditional -- only if urgent):**
```
IF response in ["ASAP (< 1 month)", "This quarter"]:
  AskUserQuestion:
    questions:
      - question: "Is this deadline negotiable?"
        header: "Fixed?"
        multiSelect: false
        options:
          - label: "Fixed - regulatory/contractual"
            description: "Cannot miss this date"
          - label: "Fixed - business event"
            description: "Tied to launch/event"
          - label: "Preferred but flexible"
            description: "Can adjust if needed"

  Store in session.constraints.timeline.flexibility

  AskUserQuestion:
    questions:
      - question: "What happens if the deadline is missed?"
        header: "Consequence"
        multiSelect: false
        options:
          - label: "Significant penalties"
            description: "Financial or legal impact"
          - label: "Missed opportunity"
            description: "Business impact but no penalty"
          - label: "Minor inconvenience"
            description: "Not critical"

  Store in session.constraints.timeline.consequence

ELSE:
  session.constraints.timeline.flexibility = "Flexible"
  session.constraints.timeline.consequence = "N/A"
```

**RECORD:**
- `session.constraints.timeline` = {target, flexibility, consequence}
- Increment question counter by 1 (if not urgent) or 3 (if urgent with follow-ups)
- Update checkpoint: `checkpoint.completed_outputs.constraints.timeline = session.constraints.timeline`

---

### Step 4.3: Resource Constraints

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "What team or resources are available for this initiative?"
      header: "Resources"
      multiSelect: false
      options:
        - label: "Dedicated team available"
          description: "Have people assigned"
        - label: "Shared resources"
          description: "People split across projects"
        - label: "Need to hire/contract"
          description: "No current resources"
        - label: "Not sure"
          description: "Resource plan unclear"
```

**VERIFY:**
- User response is non-empty
- Response maps to one of the four options
- Store in `session.constraints.resources.availability`

**FOLLOW-UP (conditional -- team size if resources exist):**
```
IF response in ["Dedicated team available", "Shared resources"]:
  AskUserQuestion:
    questions:
      - question: "Approximately how many people?"
        header: "Team Size"
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

  Store in session.constraints.resources.team_size

ELSE:
  session.constraints.resources.team_size = "TBD"
```

**FOLLOW-UP (unconditional -- skill gaps):**
```
AskUserQuestion:
  questions:
    - question: "Are there any skill gaps that would need to be filled?"
      header: "Skill Gaps"
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

Store in session.constraints.resources.skill_gaps
```

**RECORD:**
- `session.constraints.resources` = {availability, team_size, skill_gaps}
- Increment question counter by 2 (if no team) or 3 (if team exists with size follow-up)
- Update checkpoint: `checkpoint.completed_outputs.constraints.resources = session.constraints.resources`

---

### Step 4.4: Technical Constraints

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "Are there technical constraints we need to work within?"
      header: "Tech Limits"
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

**VERIFY:**
- Response captured (may be single selection or multiple)
- Store in `session.constraints.technical.requirements`

**FOLLOW-UP (conditional -- integration systems):**
```
IF "Must integrate with existing systems" selected:
  AskUserQuestion:
    questions:
      - question: "Which systems must be integrated?"
        header: "Systems"
        multiSelect: false
        options:
          - label: "Let me list them"
            description: "I'll name the systems"

  Capture system names from user input
  Store in session.constraints.technical.systems[]
```

**FOLLOW-UP (conditional -- security standards):**
```
IF "Must meet security standards" selected:
  AskUserQuestion:
    questions:
      - question: "Which security or compliance standards apply?"
        header: "Standards"
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

  Store in session.constraints.technical.security_standards[]
```

**RECORD:**
- `session.constraints.technical` = {requirements, systems (if applicable), security_standards (if applicable)}
- Increment question counter by 1 + number of conditional follow-ups triggered
- Update checkpoint: `checkpoint.completed_outputs.constraints.technical = session.constraints.technical`

---

### Step 4.5: Organizational Constraints

**EXECUTE:**
```
AskUserQuestion:
  questions:
    - question: "Are there organizational or political constraints?"
      header: "Org Limits"
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

**VERIFY:**
- Response captured (may be single selection or multiple)
- Store in `session.constraints.organizational.requirements`

**FOLLOW-UP (conditional -- change resistance):**
```
IF "Change resistance expected" selected:
  AskUserQuestion:
    questions:
      - question: "Where is the resistance likely to come from?"
        header: "Source"
        multiSelect: true
        options:
          - label: "End users"
            description: "People who use current system"
          - label: "IT department"
            description: "Technical teams"
          - label: "Management"
            description: "Middle management"
          - label: "Executive leadership"
            description: "Senior leaders"

  Store in session.constraints.organizational.resistance_sources[]

  AskUserQuestion:
    questions:
      - question: "What's driving the resistance?"
        header: "Cause"
        multiSelect: true
        options:
          - label: "Fear of job loss"
            description: "Automation concerns"
          - label: "Comfort with current system"
            description: "Change fatigue"
          - label: "Previous bad experiences"
            description: "Past failures"
          - label: "Unclear benefits"
            description: "Don't see the value"

  Store in session.constraints.organizational.resistance_causes[]

ELSE:
  session.constraints.organizational.resistance_sources = []
  session.constraints.organizational.resistance_causes = []
```

**RECORD:**
- `session.constraints.organizational` = {requirements, resistance_sources, resistance_causes}
- Increment question counter by 1 (if no resistance) or 3 (if resistance with follow-ups)
- Update checkpoint: `checkpoint.completed_outputs.constraints.organizational = session.constraints.organizational`

---

## Phase 04 Checkpoint Update

After all steps complete, write the following to the checkpoint:

```json
{
  "progress": {
    "current_phase": 5,
    "phases_completed": [..., 4],
    "completion_percentage": "updated"
  },
  "completed_outputs": {
    "constraints": {
      "budget": { "range": "...", "flexibility": "...", "ongoing_costs": "..." },
      "timeline": { "target": "...", "flexibility": "...", "consequence": "..." },
      "resources": { "availability": "...", "team_size": "...", "skill_gaps": [...] },
      "technical": { "requirements": [...], "systems": [...], "security_standards": [...] },
      "organizational": { "requirements": [...], "resistance_sources": [...], "resistance_causes": [...] }
    }
  }
}
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 04 checkpoint was NOT saved."

---

## Phase Transition Display

```
Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 4 Complete: Constraint Discovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Budget: {range} ({flexibility})
Timeline: {target} ({flexibility})
Resources: {team_size} ({availability})
Technical: {count} constraints
Organizational: {count} constraints

Proceeding to Phase 5: Hypothesis Formation...
"
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Budget unknown | "Not defined yet" | Note as TBD, emphasize importance |
| All constraints "flexible" | No real limits | Probe for hidden constraints |
| Too many constraints | 20+ items | Group by category, prioritize blockers |
| Conflicting constraints | Budget vs timeline | Highlight tradeoff for prioritization |
