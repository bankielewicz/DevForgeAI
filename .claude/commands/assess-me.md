---
description: Run a guided self-assessment questionnaire to generate an adaptive coaching profile
argument-hint: "[--recalibrate]"
---

# /assess-me

Run a guided self-assessment to generate a personalized adaptive coaching profile stored at `devforgeai/specs/business/user-profile.yaml`.

## Usage

```
/assess-me [--recalibrate]
```

## What It Does

Invokes the `assessing-entrepreneur` skill to guide you through a 6-dimension work-style questionnaire. Your responses are synthesized into a 7-dimension adaptive profile saved to `devforgeai/specs/business/user-profile.yaml`.

```
Skill("assessing-entrepreneur")
```

## Arguments

### Default (no arguments)

Runs a full assessment and creates a new `user-profile.yaml`. Use this for first-time setup.

### --recalibrate

Runs a recalibration flow when your work style has changed. Pass this flag to regenerate your adaptive profile.

**Business Rule BR-002:** Only `user-profile.yaml` is modified. Coaching history and session log remain untouched.

## Recalibration Flow

Steps when this mode runs:

1. Claude reads the existing `user-profile.yaml` and displays current settings
2. You complete the assessing-entrepreneur questionnaire again
3. Results are written to `user-profile.yaml` (profile file only)
4. Coaching session history is preserved — the session log is not touched
5. The `last_calibrated` timestamp in `user-profile.yaml` is updated

## Output

The command overwrites the existing profile at `devforgeai/specs/business/user-profile.yaml`.

The profile captures 7 adaptive dimensions: `task_chunk_size`, `session_length`, `check_in_frequency`, `progress_visualization`, `celebration_intensity`, `reminder_style`, and `overwhelm_prevention`.
