---
description: Start a coaching session with the business coaching-entrepreneur skill
argument-hint: "[topic or challenge to discuss, e.g. pricing strategy, customer acquisition]"
---

# Coach Me

Invoke the coaching-entrepreneur skill to start a personalized business coaching session.

## Step 1: Validate Arguments

Check if `$ARGUMENTS` contains a topic or challenge the user wants to discuss. If empty, the skill will begin with a general check-in.

## Step 2: Invoke Coaching Skill

```
Skill(command="coaching-entrepreneur", args="$ARGUMENTS")
```

The coaching-entrepreneur skill handles all session logic, including:
- Assessing the user's current emotional state
- Adapting coaching style to the user's profile
- Providing actionable next steps
- Recording session progress

## Step 3: Post-Session

After the coaching-entrepreneur skill completes, the session artifacts are automatically saved. The user can review their progress anytime with `/my-business`.
