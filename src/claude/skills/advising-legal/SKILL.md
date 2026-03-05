---
name: advising-legal
description: "Use when providing educational legal structure guidance for entrepreneurs. Covers business entity selection, liability considerations, and professional referral triggers. Educational only - not legal advice."
---

# Advising Legal Skill

Educational legal guidance for entrepreneurs navigating business structure decisions in the terminal.

---

## Core Workflow

### Step 1: Read User Profile at Session Start

At the beginning of each session, read the user profile file to adapt explanation depth based on experience level:

```
Read(file_path="user-profile.yaml")
```

- The user profile is **read-only** - this skill must **not write to** or **mutate** user profile data
- The user profile is **profile optional** - if missing, apply graceful fallback with **no error** produced
- Extract the experience level dimension from the user profile path to determine verbosity

### Step 2: Determine Experience Level and Adjust Verbosity

This skill supports three experience levels for adaptive pacing. The verbosity and explanation depth adjust based on the detected level:

| Experience Level | Verbosity | Behavior |
|-----------------|-----------|----------|
| **beginner** | High verbosity - full explanations with definitions of legal terms, examples for every concept, and step-by-step walkthroughs | Adjust pacing to be slower and more thorough |
| **intermediate** | Moderate verbosity - concise explanations assuming basic business knowledge, focused on decision-relevant details | Standard detail level for most users |
| **advanced** | Low verbosity - brief summaries, direct recommendations, skip foundational explanations | Adjust pacing to be faster and more direct |

**Fallback behavior:** When user profile is absent or experience level is not specified, **fallback to intermediate** as the default experience level. This ensures a silent fallback with no error message displayed to the user.

### Step 3: Load Business Structure Decision Tree

Load the canonical reference for entity selection guidance:

```
Read(file_path=".claude/skills/advising-legal/references/business-structure-guide.md")
```

This reference file is the sole authoritative source for entity descriptions, decision factors, and professional referral triggers.

### Step 4: Guide User Through Decision Factors

Walk the user through the sequential decision factors defined in the business structure guide:

1. Revenue expectations
2. Partners/co-founders
3. Liability exposure
4. Tax preferences

Present each factor sequentially, using adaptive pacing from Step 2.

### Step 5: Generate Recommendation Output

Based on user responses, generate the recommendation artifact to the output path specified in the business structure guide.

Include disclaimer header, entity recommendation with rationale, and decision path summary.

---

## Output

The skill produces a business structure recommendation artifact. See `references/business-structure-guide.md` for output format, disclaimer template, and artifact path specification.

---

## References

| Reference | Path | Purpose |
|-----------|------|---------|
| Business Structure Guide | `references/business-structure-guide.md` | Decision tree, entity descriptions, referral triggers |

---

## Constraints

- This skill provides **educational only** guidance, never prescriptive legal advice
- All recommendations use "consider" language, never "you should" or "you must"
- Professional referral triggers halt the branch when complexity exceeds educational scope
- User profile access is strictly read-only with no mutation permitted
