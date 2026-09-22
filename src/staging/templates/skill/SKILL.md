---
name: skill-name
description: Does X to Y and produces Z. Use when the user asks to A, mentions B or C, or is working with D files.
argument-hint: "[topic]"
metadata:
  devforgeai-id: "SKL-000"
  devforgeai-version: "1"
---

# <Skill title>

<!-- Delete every comment in this file when filling it in. One sentence: the outcome
     this skill produces, and the artifact it writes. -->

## Inputs

- `$ARGUMENTS`: <what the user passes; what to do when it is empty>
- <files or context the skill reads, with paths>

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. <step>
- [ ] 2. <step>
- [ ] 3. Validate the output
- [ ] 4. Report and hand off
```

### 1. <step>

<!-- Imperative instructions. Match freedom to fragility: exact commands for fragile
     steps, heuristics for judgment steps. Offer one default and an escape hatch. -->

### 2. <step>

### 3. Validate the output

<!-- A validate → fix → repeat loop. Name the exact check, and say what "passing" means. -->

1. <check>
2. If it fails, fix the reported problem and check again. Continue only when it passes.

### 4. Report and hand off

<!-- What to tell the user, and the next step or skill in the chain. -->

## Decisions that need the user

<!-- Every judgment the skill must NOT make on its own. The implementing SPEC has a BEH or AC for each. -->

- <decision>: propose options and wait for explicit confirmation.

## Output contract

<!-- The exact artifact: path pattern, template, schema it must satisfy. -->

## References

<!-- One line per file, stating WHEN to read it. Link directly; never chain references. -->

- [<topic>](references/<topic>.md): read when <condition>.
