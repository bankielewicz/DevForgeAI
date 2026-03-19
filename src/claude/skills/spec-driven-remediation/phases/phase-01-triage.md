# Phase 01: Finding Triage + Classification

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=remediation --from=00 --to=01
# Exit 0: proceed | Exit 1: Phase 00 incomplete
```

## Contract

PURPOSE: Classify each finding into one of four categories based on safety conditions from fix-actions-catalog.md.
REQUIRED SUBAGENTS: None (all work is inline — classification requires reading evidence fields)
REQUIRED ARTIFACTS: Classification map, Fix Plan Summary display
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 1: Load Reference — fix-actions-catalog.md (Fresh Per-Phase Load)

EXECUTE: Load the fix actions catalog fresh for this phase. Do NOT rely on the copy loaded in Phase 00. Per-phase reference loading prevents "already covered" rationalization.
```
Read(file_path="{SKILL_DIR}/references/fix-actions-catalog.md")
```

VERIFY: Content loaded and contains "Classification Matrix" heading AND "Automated Fix Safety Rules" heading.
```
Grep(pattern="## Classification Matrix", path="{SKILL_DIR}/references/fix-actions-catalog.md")
Grep(pattern="## Automated Fix Safety Rules", path="{SKILL_DIR}/references/fix-actions-catalog.md")
# Both must return matches
```

RECORD: Reference load confirmed.

---

### Step 2: Classify Each Finding

EXECUTE: For each finding (skip those marked "previously_fixed"), evaluate three safety conditions from the fix-actions-catalog.md to determine classification.

**Three-condition safety test:**
```
FOR each finding (skip previously_fixed):

    condition_1_deterministic = (
        old_value AND new_value are exactly derivable
        from finding.Evidence AND finding.Remediation fields
        — no judgment needed
    )

    condition_2_single_file = (
        only one file is affected
        OR it is a batch of identical single-file edits to non-context files
    )

    condition_3_not_context_file = (
        target file is NOT one of the 6 constitutional context files:
        - devforgeai/specs/context/tech-stack.md
        - devforgeai/specs/context/source-tree.md
        - devforgeai/specs/context/dependencies.md
        - devforgeai/specs/context/coding-standards.md
        - devforgeai/specs/context/architecture-constraints.md
        - devforgeai/specs/context/anti-patterns.md
    )

    IF all three conditions met:
        classification = "automated"
    ELIF finding.Type mentions ADR or finding.Evidence references ADR:
        classification = "adr_required"
    ELIF no fix procedure exists in fix-actions-catalog.md for this finding type:
        classification = "advisory"
    ELSE:
        classification = "interactive"
```

Also consult the Classification Matrix table in fix-actions-catalog.md to cross-check the classification against the canonical type-to-classification mapping.

VERIFY: Every non-previously-fixed finding has a classification in {automated, interactive, adr_required, advisory}.
```
FOR each finding:
    IF finding.status != "previously_fixed":
        ASSERT finding.classification in ["automated", "interactive", "adr_required", "advisory"]
```

RECORD:
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=remediation --phase=01 --step=classify
```

---

### Step 3: Display Fix Plan Summary

EXECUTE: Count findings by classification and display the Fix Plan Summary box.
```
count_auto        = count findings where classification == "automated"
count_interactive = count findings where classification == "interactive"
count_adr         = count findings where classification == "adr_required"
count_advisory    = count findings where classification == "advisory"
count_fixed       = count findings where status == "previously_fixed"

Display:

+------------------------------------------+
|           Fix Plan Summary               |
+------------------------------------------+
|  Automated (safe):   {count_auto}        |
|  Interactive:        {count_interactive}  |
|  Requires ADR:       {count_adr}         |
|  Advisory only:      {count_advisory}    |
|  Previously fixed:   {count_fixed}       |
+------------------------------------------+
```

VERIFY: Summary contains all 5 count categories. Total of all categories equals total findings count.
```
ASSERT (count_auto + count_interactive + count_adr + count_advisory + count_fixed) == total_findings
```

RECORD: Update checkpoint with classification results.
```
Update checkpoint file: devforgeai/temp/.remediation-checkpoint-${SESSION_ID}.yaml

  current_phase: 1
  findings:
    - finding_id: "F-001"
      classification: "{classification}"
      status: "pending"
      ...
  phase_completion:
    phase_00: true
    phase_01: true
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=remediation --phase=01 --checkpoint-passed
# Exit 0: proceed to Phase 02 | Exit 1: phase incomplete
```
