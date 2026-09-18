# Phase 03: Prescription (Tactical Mode Only)

**Purpose:** Generate ranked hypotheses with confidence scores and produce fix prescriptions for the invoking dev workflow.
**Applies to:** Tactical mode only. Strategic mode skips this phase entirely.

---

## Reference Loading [MANDATORY]

```
# No required references for this phase. Phase 03 is tactical-mode only;
# it generates hypotheses, prescriptions, and the rca-prescription.json
# envelope using artifacts already loaded by Phases 01-02 (capture data,
# diagnostic-analyst output, investigation report). The pre-rca-prescription-
# write.sh hook validates the emitted JSON schema at Write time.
```

---

## Step 03.1: Generate Hypotheses [MANDATORY]

### EXECUTE

Based on Phase 02 investigation findings and diagnostic-analyst output, generate 2-5 hypotheses:

```
HYPOTHESIS RANKING
==================
H1: {description} [Confidence: {0.0-1.0}]
    Evidence: {supporting evidence from Phase 02}
    Category: {spec-drift | test-assertion | import-dependency | coverage | anti-pattern | dod-validation}
    Affected Files: {list}

H2: {description} [Confidence: {0.0-1.0}]
    Evidence: {supporting evidence}
    Category: {category}
    Affected Files: {list}
```

**Confidence Scoring Criteria:**

| Score | Meaning | Criteria |
|-------|---------|----------|
| 0.9-1.0 | Near certain | Direct evidence in error output + code trace confirms |
| 0.7-0.8 | High confidence | Strong evidence, one minor ambiguity |
| 0.5-0.6 | Moderate | Multiple possible causes, evidence supports this one |
| 0.3-0.4 | Low | Indirect evidence only |
| 0.0-0.2 | Speculative | No direct evidence, pattern-based guess |

**Failure Categories (from investigation-patterns.md):**

| Category | Description |
|----------|-------------|
| spec-drift | Implementation diverges from context file constraints |
| test-assertion | Test expects X but implementation produces Y |
| import-dependency | Missing modules, wrong versions, circular imports |
| coverage | Test coverage below thresholds |
| anti-pattern | Code matches forbidden patterns |
| dod-validation | DoD format errors or autonomous deferral |

### VERIFY

- At least 2 hypotheses generated
- At least 1 hypothesis has confidence >= 0.5
- Each hypothesis has evidence, category, and affected files

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.1
```

---

## Step 03.2: Validate Top Hypothesis [MANDATORY]

### EXECUTE

For the top hypothesis (highest confidence):

1. Verify it explains ALL observed symptoms from Phase 01 capture
2. Verify it is consistent with Phase 02 investigation findings
3. Verify the root location matches the hypothesis
4. Verify the diagnostic-analyst spec compliance findings align

If hypothesis does not explain all symptoms:
```
Re-rank hypotheses
Promote next candidate to top
Re-validate
```

### VERIFY

- Top hypothesis explains all observed symptoms
- No contradictions with investigation findings
- Root location and hypothesis are consistent

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.2
```

---

## Step 03.3: Generate Fix Prescription [MANDATORY]

### EXECUTE

For each hypothesis (starting with highest confidence):

```
PRESCRIPTION
============
Target Hypothesis: H{n} [{confidence}]
Root Cause: {one-line summary}

Fix Actions:
1. File: {absolute_path}
   Line: {line_number or range}
   Action: {Edit | Write | Delete | Add}
   Change: {specific description of what to change}
   Rationale: {why this fixes the root cause}

2. File: {absolute_path}
   Line: {line_number or range}
   Action: {Edit | Write | Delete | Add}
   Change: {specific description}
   Rationale: {why this helps}

Verification:
  Command: {test command to verify fix}
  Expected: {expected output after fix}
```

### VERIFY

- At least one prescription has specific file paths
- Each fix action has a concrete change description (not vague)
- Verification command specified

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.3
```

---

## Step 03.4: Risk Assessment [MANDATORY]

### EXECUTE

For each prescribed fix:

| Dimension | Assessment |
|-----------|------------|
| **Scope** | How many files affected? |
| **Regression Risk** | Could this break other tests? |
| **Reversibility** | Can this be undone easily? |
| **Side Effects** | What else might change? |

### VERIFY

- Risk assessment completed for primary prescription
- No unacknowledged high-risk changes

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.4
```

---

## Step 03.5: Fix Ordering [MANDATORY]

### EXECUTE

If multiple fixes are required, specify execution order:

1. Fixes that address **root cause FIRST**
2. Fixes that address **symptoms SECOND**
3. Fixes that are **preventive LAST**

### VERIFY

- Ordering is logical (root cause before symptoms)
- Dependencies between fixes are noted

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.5
```

---

## Step 03.6: Produce Final Report and Handoff [MANDATORY]

### EXECUTE

Produce the final tactical diagnosis report:

```
ROOT CAUSE DIAGNOSIS REPORT
============================
Story: {STORY_ID}
Phase: {workflow_phase}
Timestamp: {current date/time}

CAPTURE:
  Error: {error summary}
  Phase State: {current phase}
  Fix Attempts: {count}

INVESTIGATION:
  Spec Compliance: {PASS/FAIL}
  Context Violations: {list or "None"}
  Root Location: {file:line}

HYPOTHESES:
  H1: {description} [{confidence}]
  H2: {description} [{confidence}]

PRESCRIPTION:
  Primary Fix: {description}
  Files: {list of files to modify}
  Verification: {test command}
  Risk: {scope assessment}
  Order: {execution order}

STATUS: {DIAGNOSED | ESCALATED | INCONCLUSIVE}
```

**STATUS Determination:**
- DIAGNOSED: Top hypothesis confidence >= 0.7 and prescription is actionable
- ESCALATED: Top hypothesis confidence < 0.5 or all prescriptions failed
- INCONCLUSIVE: Evidence insufficient for diagnosis

Return prescription to invoking workflow phase for execution.

### VERIFY

- Final report contains all sections
- STATUS is one of DIAGNOSED, ESCALATED, INCONCLUSIVE
- Prescription is actionable (specific file paths and changes)

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.6
```

---

## Step 03.7: Emit Structured Prescription JSON [MANDATORY]

**Added by ADR-074.** Writes `tmp/${STORY_ID}/rca-prescription.json` so that `spec-driven-dev` Phase 03 can read the prescription on retry and apply it through the existing remediation-step interpreter. Without this artifact, the tactical loop relies on the human to translate the prose report into edits.

### EXECUTE

Construct the prescription envelope from the data already produced in Steps 03.1–03.6:

```json
{
  "session_id": "${SESSION_ID}",
  "story_id": "${STORY_ID}",
  "status": "DIAGNOSED",
  "generated_at": "<ISO-8601 UTC timestamp>",
  "top_hypothesis": {
    "n": 1,
    "description": "<H1 description from Step 03.1>",
    "confidence": <H1 confidence, decimal 0..1>,
    "category": "<failure category>",
    "affected_files": ["<absolute path>", "..."]
  },
  "ranked_hypotheses": [
    { "n": 1, "description": "...", "confidence": 0.0, "category": "..." },
    { "n": 2, "description": "...", "confidence": 0.0, "category": "..." }
  ],
  "prescription": [
    {
      "file": "<absolute file path from Step 03.3>",
      "line": <line or line range start>,
      "action": "Edit",
      "change": "<one-line description of the change>",
      "rationale": "<why this fixes the root cause>"
    }
  ],
  "verification_command": "<verification command from Step 03.3>",
  "next_action": "resume-phase-03"
}
```

Then write the artifact:

```
Write(
  file_path="tmp/${STORY_ID}/rca-prescription.json",
  content=<the JSON envelope above, prettified>
)
```

**`next_action` selection:**

| STATUS (from 03.6) | next_action |
|---|---|
| DIAGNOSED + top hypothesis confidence ≥ 0.7 | `resume-phase-03` |
| ESCALATED OR top hypothesis confidence in [0.5, 0.7) | `escalate` |
| INCONCLUSIVE OR top hypothesis confidence < 0.5 | `halt` |

The `pre-rca-prescription-write.sh` hook (ADR-074) validates the schema before the Write lands: `status` enum, `next_action` enum, and — when `status=DIAGNOSED` — `top_hypothesis.confidence ≥ 0.5`, non-empty `ranked_hypotheses`, and non-empty `prescription`. A schema violation is blocked with exit 2.

### VERIFY

- File exists: `Read(file_path="tmp/${STORY_ID}/rca-prescription.json")` succeeds
- JSON parses (re-run the hook's `jq -e .` check mentally if needed)
- `next_action` matches the STATUS Determination table above
- For DIAGNOSED: prescription array is non-empty and each entry has `file`, `line`, `action`, `change`, `rationale`

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=03 --step=03.7
```

---

## Downstream Hand-off

After Step 03.7 lands the prescription file, the tactical-mode flow ends. The user re-invokes `/dev` for the same story; `spec-driven-dev/phases/phase-03-implementation.md` detects `tmp/${STORY_ID}/rca-prescription.json` and applies the prescription on its retry path (per ADR-074), then unlinks the file. If `next_action=escalate` or `halt`, /dev re-displays the diagnosis to the user and HALTs without auto-applying.
