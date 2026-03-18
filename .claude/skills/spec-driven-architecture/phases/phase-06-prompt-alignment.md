# Phase 06: Prompt Alignment

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Validate CLAUDE.md and system-prompt-core.md alignment with context files; detect contradictions and gaps |
| **REFERENCES** | `.claude/skills/spec-driven-architecture/references/prompt-alignment-workflow.md` |
| **STEP COUNT** | 6 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] Configuration layers detected and loaded
- [ ] alignment-auditor subagent invoked (or graceful degradation applied)
- [ ] All HIGH contradictions resolved (zero remaining)
- [ ] Gaps processed and user-approved additions applied
- [ ] ADR drift items recorded
- [ ] Alignment report written to `devforgeai/feedback/ai-analysis/`
**IF any criterion is unmet: HALT. Do NOT proceed to Phase 07.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-architecture/references/prompt-alignment-workflow.md")
```

Do NOT rely on memory of previous reads. Load fresh every time.

---

## Mandatory Steps

### Step 6.1: Detect Configuration Layers

**EXECUTE:**
```
Glob(pattern="CLAUDE.md")
Glob(pattern=".claude/system-prompt-core.md")
```
For each file found:
```
Read(file_path="CLAUDE.md")
Read(file_path=".claude/system-prompt-core.md")
```

**VERIFY:**
- At least CLAUDE.md exists and was read successfully
- system-prompt-core.md existence recorded (may not exist in all projects)
- Content is non-empty for each file found

**RECORD:**
```json
checkpoint.phase_06.step_6_1 = {
  "claude_md_exists": true,
  "claude_md_lines": <count>,
  "system_prompt_exists": <boolean>,
  "system_prompt_lines": <count_or_null>,
  "layers_detected": ["CLAUDE.md", "system-prompt-core.md"]
}
```

---

### Step 6.2: Invoke alignment-auditor Subagent

**EXECUTE:**
```
Task(
  subagent_type="alignment-auditor",
  prompt="Perform pairwise comparison across configuration layers:
    - CLAUDE.md
    - .claude/system-prompt-core.md
    - All 6 context files in devforgeai/specs/context/

    For each pair, detect:
    1. CONTRADICTIONS — Layer A says X, Layer B says NOT-X (severity: HIGH)
    2. GAPS — Layer A references concept not defined anywhere (severity: MEDIUM)
    3. ADR_DRIFT — ADR decision not reflected in context files (severity: MEDIUM)
    4. REDUNDANCY — Same rule stated in 3+ places verbatim (severity: LOW)

    Return structured JSON: { findings: [{ type, severity, layer_a, layer_b, evidence, line_a, line_b }] }"
)
```
This is a BLOCKING task with graceful degradation.

**VERIFY:**
- Task returned a result with structured findings
- IF Task failed (error or timeout):
  - Display: `WARNING: alignment-auditor subagent unavailable. Phase will complete with degraded status.`
  - Set `alignment_status = "degraded"`
  - Skip to Step 6.6 (Write Alignment Report with degraded flag)

**RECORD:**
```json
checkpoint.phase_06.step_6_2 = {
  "subagent_invoked": true,
  "subagent_result_received": <boolean>,
  "alignment_status": "complete" | "degraded",
  "findings_count": { "CONTRADICTION": <n>, "GAP": <n>, "ADR_DRIFT": <n>, "REDUNDANCY": <n> },
  "raw_findings": [ ... ]
}
```

---

### Step 6.3: Process HIGH Contradictions (BLOCKING)

**EXECUTE:**
- Filter findings where `severity == "HIGH"` and `type == "CONTRADICTION"`
- For each HIGH contradiction:
  ```
  AskUserQuestion(
    question="HIGH contradiction detected:\n  Layer A: <layer_a> (line <line_a>)\n  Layer B: <layer_b> (line <line_b>)\n  Evidence: <evidence>\n\nWhich layer is authoritative?",
    options=[
      { "label": "Layer A is correct", "description": "Update <layer_b> to match" },
      { "label": "Layer B is correct", "description": "Update <layer_a> to match" },
      { "label": "Both need updating", "description": "Provide new wording for both" }
    ]
  )
  ```
- Apply approved resolution via `Edit(file_path=..., old_string=..., new_string=...)`

**VERIFY:**
- Every HIGH contradiction has a user decision recorded
- Every approved edit applied successfully
- Zero HIGH contradictions remain unresolved
- IF unresolved HIGHs remain after processing: HALT immediately

**RECORD:**
```json
checkpoint.phase_06.step_6_3 = {
  "high_contradictions_found": <count>,
  "high_contradictions_resolved": <count>,
  "high_contradictions_remaining": 0,
  "resolutions": [{ "finding_id": <n>, "decision": "<choice>", "edit_applied": true }]
}
```

---

### Step 6.4: Process Gaps

**EXECUTE:**
- Filter findings where `type == "GAP"`
- For each gap, synthesize project context to determine if the gap is meaningful
- Draft CLAUDE.md additions or context file clarifications as needed
- Present batch to user:
  ```
  AskUserQuestion(
    question="The following gaps were detected between configuration layers and context files:\n<gap_list>\n\nShould these be addressed?",
    options=[
      { "label": "Address all gaps", "description": "Apply all suggested additions" },
      { "label": "Select individually", "description": "Review each gap separately" },
      { "label": "Defer all to stories", "description": "Create future work items" }
    ]
  )
  ```
- Apply approved additions via `Edit`

**VERIFY:**
- User decision recorded for each gap (addressed, deferred, or dismissed)
- Approved edits applied without error
- Deferred gaps have justification text

**RECORD:**
```json
checkpoint.phase_06.step_6_4 = {
  "gaps_found": <count>,
  "gaps_addressed": <count>,
  "gaps_deferred": <count>,
  "gaps_dismissed": <count>,
  "edits_applied": [{ "file": "<path>", "change": "<summary>" }]
}
```

---

### Step 6.5: Process ADR Drift

**EXECUTE:**
- Filter findings where `type == "ADR_DRIFT"`
- For each drift item:
  ```
  Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
  ```
  Read the referenced ADR to confirm the drift is genuine
- Record each confirmed drift item with: ADR number, decision text, affected context file, missing content

**VERIFY:**
- Each ADR drift item confirmed by reading the actual ADR file
- False positives filtered out (ADR decision already reflected but auditor missed it)
- Confirmed drift items recorded for future propagation

**RECORD:**
```json
checkpoint.phase_06.step_6_5 = {
  "drift_items_reported": <count>,
  "drift_items_confirmed": <count>,
  "drift_items_false_positive": <count>,
  "confirmed_drift": [{ "adr": "ADR-<NNN>", "decision": "<text>", "missing_in": "<file>" }]
}
```

---

### Step 6.6: Write Alignment Report

**EXECUTE:**
```
Write(
  file_path="devforgeai/feedback/ai-analysis/phase-6-alignment.json",
  content=<JSON report containing:
    timestamp, alignment_status, layers_analyzed,
    contradictions (found, resolved, remaining),
    gaps (found, addressed, deferred),
    adr_drift (reported, confirmed),
    phase_result ("PASS" | "PASS_WITH_DEGRADATION" | "FAIL")
  >
)
```

**VERIFY:**
```
Glob(pattern="devforgeai/feedback/ai-analysis/phase-6-alignment.json")
```
- File exists at expected path
- File is valid JSON (parseable)

**RECORD:**
```json
checkpoint.phase_06.step_6_6 = {
  "report_path": "devforgeai/feedback/ai-analysis/phase-6-alignment.json",
  "report_written": true,
  "phase_result": "PASS" | "PASS_WITH_DEGRADATION"
}
```

---

## Phase Transition Display

```
============================================================
  PHASE 06 COMPLETE: Prompt Alignment
============================================================
  Layers analyzed:         <N>
  Alignment status:        [COMPLETE/DEGRADED]
  HIGH contradictions:     <N> found, <N> resolved
  Gaps:                    <N> addressed, <M> deferred
  ADR drift items:         <N> confirmed
  Report:                  devforgeai/feedback/ai-analysis/phase-6-alignment.json
------------------------------------------------------------
  Proceeding to Phase 07: Domain References
============================================================
```
