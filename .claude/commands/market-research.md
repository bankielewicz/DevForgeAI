---
description: Conduct structured market research (sizing, competitive analysis, interviews)
argument-hint: <phase> (market-sizing | competitive-analysis | customer-interviews | full)
model: opus
allowed-tools: AskUserQuestion, Read, Skill
execution-mode: immediate
---

# /market-research - Market Research Workflow

Invoke the researching-market skill to conduct structured market research. This command validates arguments and delegates all business logic to the skill.

---

## ARGUMENTS

The command accepts a single required phase argument.

**Valid options:**
- `market-sizing` - Run market sizing analysis
- `competitive-analysis` - Run competitive landscape analysis
- `customer-interviews` - Generate hypothesis-driven discovery prompts for customer conversations
- `full` - Run all three phases sequentially

---

## Phase 0: Argument Validation

```
PHASE_ARG = null

FOR arg in arguments:
    IF arg matches "market-sizing|competitive-analysis|customer-interviews|full":
        PHASE_ARG = arg

IF PHASE_ARG is empty or invalid:
    Display: "Invalid argument. Valid options are:"
    Display: "  - market-sizing"
    Display: "  - competitive-analysis"
    Display: "  - customer-interviews"
    Display: "  - full"
    Display: ""
    Display: "Usage: /market-research <phase>"
    Display: "The phase argument must be one of the valid options listed above."
    HALT
```

---

## Phase 1: Invoke Skill

Delegate to the researching-market skill with the validated phase argument.

```
Display: ""
Display: "============================================="
Display: "  Market Research Workflow"
Display: "============================================="
Display: "**Phase:** ${PHASE_ARG}"
Display: "Delegating to researching-market skill..."

Skill(command="researching-market", args="${PHASE_ARG}")
```

---

## Phase 2: Display Results

Display the skill's formatted result directly. No processing or business logic in this command. All research logic is handled by the researching-market skill.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No argument provided | Show valid options and usage |
| Invalid phase argument | Show valid options and usage |
| Skill not found | Check: src/claude/skills/researching-market/SKILL.md exists |
