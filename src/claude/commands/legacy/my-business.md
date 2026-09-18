---
description: Display your aggregated business journey dashboard with profile, milestones, streak, and next steps
argument-hint: "[optional: section to focus on, e.g. milestones, streak, tasks]"
---

# My Business Dashboard

Display an aggregated, read-only dashboard of the user's business coaching journey.

## Step 1: Load Business Artifacts

Read all available business artifacts:

```
Read(file_path="devforgeai/specs/business/profile.md")
Read(file_path="devforgeai/specs/business/milestones.md")
Read(file_path="devforgeai/specs/business/sessions.md")
Read(file_path="devforgeai/specs/business/tasks.md")
```

Check if `$ARGUMENTS` specifies a section focus (e.g., "milestones", "streak", "tasks"). If so, display only that section. Otherwise display the full dashboard.

## Step 2: Handle Empty State

IF none of the business artifact files exist (profile not found, no milestones, no sessions):

Display the welcome onboarding message:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Welcome to Your Business Journey!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  It looks like you haven't started yet.
  Let's get started on your first step!

  Run /assess-me to begin your business
  assessment and create your profile.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

STOP here. Do not render the full dashboard.

## Step 3: Render Aggregated Dashboard

When business artifacts are present, render the full ASCII dashboard:

```
┌─────────────────────────────────────────────┐
│         YOUR BUSINESS JOURNEY               │
├─────────────────────────────────────────────┤
│                                             │
│  Profile & Adaptation Level                 │
│  ─────────────────────────────              │
│  Name: {business_name}                      │
│  Stage: {current_stage}                     │
│  Adaptation Level: {level}                  │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Streak: {streak_count} days                │
│  ─────────────────────────────              │
│  Keep the momentum going!                   │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Milestones                                 │
│  ─────────────────────────────              │
│                                             │
│  Completed milestones (checkmark):          │
│  [x] Milestone 1 - Done                    │
│  [x] Milestone 2 - Done                    │
│                                             │
│  Current milestone in progress:             │
│  [ ] Milestone 3 - In Progress (60%)       │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Next Recommended Task                      │
│  ─────────────────────────────              │
│  Task: {next_task_name}                     │
│  Estimated time: {duration}                 │
│  Why: {rationale}                           │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Encouraging Quote                          │
│  ─────────────────────────────              │
│  "{motivation_quote}"                       │
│  Select a quote based on current progress   │
│  to provide encouragement and motivation.   │
│                                             │
└─────────────────────────────────────────────┘
```

## Step 4: Populate Dashboard Data

For each section, extract data from the loaded artifacts:

1. **Profile summary** - From `devforgeai/specs/business/profile.md`: business name, stage, adaptation level
2. **Streak count** - From `devforgeai/specs/business/sessions.md`: count consecutive session days
3. **Completed milestones** - From `devforgeai/specs/business/milestones.md`: items marked complete (checkmark indicator)
4. **Current milestone in progress** - From milestones: first incomplete item
5. **Next recommended task** - From `devforgeai/specs/business/tasks.md`: highest priority incomplete task with estimated time
6. **Encouraging quote** - Select a motivation quote appropriate to the user's current progress stage

## Constraints

- This command is READ-ONLY. It aggregates and displays data only.
- If a specific artifact file is missing but others exist, show available sections and note missing ones gracefully.
- If the user has no profile yet, guide them to run `/assess-me` to begin.
