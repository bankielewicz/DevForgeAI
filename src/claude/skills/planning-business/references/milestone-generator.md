---
id: milestone-generator
title: Milestone Generator Reference
version: "1.0"
story: STORY-532
created: 2026-03-04
status: Published
phase: milestone-generation
---

# Milestone Generator Reference

Defines the milestone generation phase for the planning-business skill. Generates 10 sequential milestones from user-profile.yaml data, producing milestones.yaml output.

---

## Prerequisites

Before generating milestones, validate that `user-profile.yaml` exists in the project workspace. If missing, HALT with error message:

```
Error: User profile not found
Action: Run the user-profile phase first before milestone generation.
Do not create milestones — user profile is required.
```

Do not create milestones.yaml without a valid user-profile.yaml.

---

## Milestone Schema

Each milestone requires exactly 6 fields. All fields are mandatory.

```yaml
milestone_schema:
  - name: string           # Short identifier (2-5 words)
  - definition: string     # What "done" means for this milestone
  - soft_timeframe: string  # Estimated duration (e.g., "7-14 days")
  - micro_tasks: list      # 3-7 concrete sub-tasks
  - validation_gate: string # Binary pass/fail criterion
  - celebration: string     # Reward action on completion
```

---

## Guard Rails: Timeframe Constraints

The following guard rails govern timeframe assignment:

1. **Minimum duration:** All milestones must have minimum 7-day duration. Clamp any computed soft_timeframe below 7 days to 7.
2. **Maximum total duration:** 180 days total across all 10 milestones combined.
3. **Recalibration trigger:** When total milestone duration exceeds 180 days, halt generation and recalibrate the plan.

```yaml
guard_rails:
  min_days_per_milestone: 7
  max_total_days: 180
  recalibration_trigger:
    condition: "total_days > 180"
    action: "Halt generation and recalibrate plan"
```

---

## Idempotent Re-generation

Milestone generation is idempotent. Re-running the generator overwrites existing output.

**Backup before overwrite:** Before any overwrite of milestones.yaml, create a backup copy at `milestones.yaml.bak`. This preserves previous milestone data.

Procedure:
1. Check if milestones.yaml exists
2. If yes, copy to milestones.yaml.bak (backup prior to overwrite)
3. Regenerate milestones.yaml from current user-profile.yaml
4. Write new milestones.yaml (overwrite)

The backup before overwrite order ensures no data loss during regeneration.

---

## Validation Gate Rules

All validation_gate values must be concrete, binary, pass-fail criteria. Each gate must be verifiable and measurable — done or not done.

**Prohibited vague terms in validation gates:**
- "feels ready" — too subjective
- "good enough" — not measurable
- "ready enough" — vague
- "probably done" — not binary

Every validation_gate must answer a yes/no question with observable evidence.

---

## Milestone Definitions

### Milestone 1: Problem Validated

```yaml
- name: "Problem Validated"
  definition: "Target customer problem is confirmed through direct evidence"
  soft_timeframe: "7-14 days"
  micro_tasks:
    - Conduct 5 problem discovery interviews
    - Document top 3 pain points with quotes
    - Identify existing alternatives customers use
    - Write problem hypothesis statement
  validation_gate: "5 interviews completed with documented pain points"
  celebration: "Share problem statement with one trusted advisor"
```

### Milestone 2: Customer Defined

```yaml
- name: "Customer Defined"
  definition: "Ideal customer profile documented with demographic and behavioral traits"
  soft_timeframe: "7-10 days"
  micro_tasks:
    - Create ideal customer persona document
    - List 3 demographic filters
    - List 3 behavioral indicators
    - Identify where target customers congregate online
  validation_gate: "Customer persona document exists with 3+ demographic and 3+ behavioral traits"
  celebration: "Print persona card and pin to workspace wall"
```

### Milestone 3: Solution Sketched

```yaml
- name: "Solution Sketched"
  definition: "Core solution concept articulated in a one-page brief"
  soft_timeframe: "7-14 days"
  micro_tasks:
    - Draft one-page solution brief
    - Map solution to top 3 pain points
    - Identify key differentiator vs alternatives
    - Sketch user flow (3-5 steps)
  validation_gate: "One-page solution brief exists mapping to validated pain points"
  celebration: "Walk a friend through the solution sketch in under 2 minutes"
```

### Milestone 4: Prototype Built

```yaml
- name: "Prototype Built"
  definition: "Functional or visual prototype ready for user testing"
  soft_timeframe: "14-21 days"
  micro_tasks:
    - Select prototyping tool or framework
    - Build core user flow (happy path)
    - Add 1-2 secondary flows
    - Internal walkthrough with notes
    - Fix critical usability issues
  validation_gate: "Prototype demonstrates core user flow end-to-end without assistance"
  celebration: "Demo the prototype to 3 people and collect reactions"
```

### Milestone 5: User Tested

```yaml
- name: "User Tested"
  definition: "Prototype tested with real target users and feedback documented"
  soft_timeframe: "10-14 days"
  micro_tasks:
    - Recruit 5 target users for testing
    - Create test script with 3-5 tasks
    - Conduct moderated test sessions
    - Document findings per user
    - Prioritize top 3 changes needed
  validation_gate: "5 user test sessions completed with documented findings and prioritized changes"
  celebration: "Write a summary post about what users taught you"
```

### Milestone 6: MVP Scoped

```yaml
- name: "MVP Scoped"
  definition: "Minimum viable product feature set defined with cut list"
  soft_timeframe: "7-10 days"
  micro_tasks:
    - List all potential features
    - Apply MoSCoW prioritization
    - Define must-have feature set (max 5)
    - Document explicit cut list (not-in-MVP)
    - Estimate build effort per feature
  validation_gate: "Feature list exists with 5 or fewer must-haves and explicit cut list documented"
  celebration: "Delete one feature you were attached to — freedom in focus"
```

### Milestone 7: MVP Built

```yaml
- name: "MVP Built"
  definition: "Working MVP deployed to a testable environment"
  soft_timeframe: "21-30 days"
  micro_tasks:
    - Set up development environment
    - Implement must-have features
    - Write basic automated tests
    - Deploy to staging environment
    - Conduct internal smoke test
    - Fix critical bugs
  validation_gate: "MVP deployed to staging with all must-have features functional and smoke test passing"
  celebration: "Take a full day off — you built something real"
```

### Milestone 8: Early Adopters Acquired

```yaml
- name: "Early Adopters Acquired"
  definition: "First 10 real users actively using the MVP"
  soft_timeframe: "14-21 days"
  micro_tasks:
    - Create onboarding flow or guide
    - Reach out to 30 potential early adopters
    - Offer early access with feedback agreement
    - Track activation metrics
    - Conduct 3 follow-up interviews
  validation_gate: "10 users signed up and completed onboarding with at least 3 returning after day 1"
  celebration: "Send a personal thank-you message to each early adopter"
```

### Milestone 9: Metrics Baselined

```yaml
- name: "Metrics Baselined"
  definition: "Key business metrics tracked with 2-week baseline data"
  soft_timeframe: "14-21 days"
  micro_tasks:
    - Define 3-5 key metrics (retention, activation, revenue)
    - Instrument analytics tracking
    - Collect 2 weeks of baseline data
    - Create metrics dashboard
    - Identify top metric to improve
  validation_gate: "Dashboard shows 2 weeks of tracked data for 3+ key metrics"
  celebration: "Share your metrics dashboard publicly — transparency builds trust"
```

### Milestone 10: Launch Ready

```yaml
- name: "Launch Ready"
  definition: "Product ready for public launch with go-to-market plan"
  soft_timeframe: "14-21 days"
  micro_tasks:
    - Create landing page with clear value proposition
    - Write launch announcement
    - Prepare support documentation
    - Set up payment or signup flow
    - Plan launch day distribution (3+ channels)
    - Conduct final end-to-end test
  validation_gate: "Landing page live, payment flow tested, launch announcement drafted, 3+ distribution channels identified"
  celebration: "Launch day — hit publish and tell everyone you know"
```
