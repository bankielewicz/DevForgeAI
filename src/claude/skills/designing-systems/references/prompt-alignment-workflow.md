# Prompt Alignment Workflow

Reference file for Phase 5.5 of the designing-systems skill. Loaded on demand during /create-context execution.
Progressive disclosure — loaded on-demand only when Phase 5.5 executes, not at skill startup.

## Purpose

Validate that newly created context files do not contradict existing configuration layers
(CLAUDE.md, system-prompt-core.md). Detect gaps, contradictions, and ADR propagation drift
before Phase 6 (Epic Creation). Ensures prompt-layer alignment so AI agents receive
consistent, non-conflicting instructions.

## Preconditions

- Phase 5 (Validate Spec Against Context) completed successfully
- All 6 context files exist in `devforgeai/specs/context/`
- alignment-auditor subagent available in `.claude/agents/`

## Postconditions

- Zero HIGH contradictions unresolved (or overridden with ACCEPTED_RISK + justification)
- All findings logged to `devforgeai/feedback/ai-analysis/phase-5.5-alignment.json`

---

## Graceful Degradation

If the alignment-auditor subagent times out, errors, or returns malformed output:

- Display WARNING: "alignment-auditor did not complete — Phase 5.5 findings unavailable"
- Phase 6 is NOT blocked by alignment-auditor failure
- Treat result as "zero findings" (no contradictions, no gaps, no drift detected)
- Log the failure reason to the alignment JSON under `"error"` key
- Continue to Step 6 (Report) with degraded status noted; logging present in report

---

## Step 1: Detect Configuration Layers

**Inputs:** Project root path, file system access

**Actions:**

1. Check for CLAUDE.md using `Read(file_path="CLAUDE.md")`.
   - If found: record as configuration layer source.
   - If missing: note absence (informational only, non-blocking).

2. Check for system-prompt-core.md using `Glob(pattern=".claude/memory/system-prompt-core.md")`.
   - If found: record as configuration layer source.
   - If missing: note absence gracefully (non-blocking).

3. If NEITHER file exists:
   - Record informational note: "No prompt configuration layers detected. Consider adding CLAUDE.md for project-level AI guidance."
   - Proceed to Phase 6 normally (non-blocking).

4. If one or both exist: record paths for Step 2 context injection.

**Tools:** Read, Glob

**Outputs:** `detected_layers` list (may be empty). Informational note if neither file present.

---

## Step 2: Invoke alignment-auditor

**Inputs:** `detected_layers` from Step 1, paths to all 6 context files in `devforgeai/specs/context/`

**Actions:**

1. Assemble context payload including detected configuration layer file contents
   and all 6 context file paths.

2. Invoke alignment-auditor subagent:

```
Task(
  subagent_type="alignment-auditor",
  description="Validate configuration layer alignment after context file creation",
  prompt="""
  Analyze alignment between configuration layers and context files.
  Configuration layers: CLAUDE.md ({content_or_absent}), system-prompt-core.md ({content_or_absent}).
  Context files: all 6 in devforgeai/specs/context/.
  Return structured JSON output:
  {
    "contradictions": [{"severity": "HIGH|MEDIUM|LOW", "description": "...", "layer": "...", "context_file": "..."}],
    "gaps": [{"section": "...", "missing_content": "...", "suggested_addition": "..."}],
    "adr_drift": [{"adr_id": "...", "context_file": "...", "drift_description": "..."}],
    "claude_md_gaps": [{"section": "...", "draft": "..."}]
  }
  """
)
```

3. Parse the structured JSON output. If parsing fails, apply Graceful Degradation (see above).

**Tools:** Task

**Outputs:** Structured JSON report with `contradictions`, `gaps`, `adr_drift`, `claude_md_gaps` arrays.

---

## Step 3: Process Contradictions

**Inputs:** `contradictions` array from Step 2 JSON output

**Actions:**

1. Separate contradictions by severity: HIGH, MEDIUM, LOW.

2. For each HIGH contradiction (blocking):
   - Present via AskUserQuestion:
     ```
     Contradiction detected (HIGH severity):
     Layer: {layer}
     Context file: {context_file}
     Issue: {description}

     Options:
     A) Apply fix — update the conflicting file automatically
     B) Skip — leave as-is (requires written justification)
     C) Edit manually — open file for manual correction
     D) ACCEPTED_RISK — override with justification

     Select A, B, C, or D:
     ```
   - BLOCK Phase 6 until all HIGH contradictions are resolved or overridden.

3. For MEDIUM and LOW contradictions (deferrable):
   - Display summary to user.
   - Prompt: "Accept and defer MEDIUM/LOW contradictions with justification? [Y/n]"
   - Record justification in alignment log if deferred.
   - Phase 6 is NOT blocked by MEDIUM or LOW contradictions.

4. ACCEPTED_RISK override (for HIGH contradictions):
   - Allow user to override with ACCEPTED_RISK.
   - Require non-empty justification (reject blank entries).
   - Ask: "Provide justification for accepting this risk (required):"
   - Record override in `devforgeai/feedback/ai-analysis/phase-5.5-alignment.json` under `"accepted_risks"`.
   - Unblock Phase 6 once all HIGH contradictions are resolved, skipped, or overridden.

**Tools:** AskUserQuestion

**Outputs:** Resolution decisions per contradiction. Updated alignment log. Phase 6 gate status.

---

## Step 4: Process Gaps

**Inputs:** `gaps` array and `claude_md_gaps` array from Step 2 JSON output

**Actions:**

1. For context file gaps (missing sections or constraints):

   Synthesize gap context using `<project_context>` template:

   4 required sections: Platform Constraint, Build System Routing, Subagent Routing, Current State
   ```xml
   <project_context>
     <!-- Platform: tech-stack.md runtime, OS, cloud targets -->
     <Platform_Constraint>{extracted from tech-stack.md}</Platform_Constraint>
     <!-- Build System: source-tree.md tool, test runner, output paths -->
     <Build_System_Routing>{extracted from source-tree.md}</Build_System_Routing>
     <!-- Subagent: architecture-constraints.md layer assignments -->
     <Subagent_Routing>{extracted from architecture-constraints.md}</Subagent_Routing>
     <!-- Current: coding-standards.md + dependencies.md libraries, patterns -->
     <Current_State>{extracted from coding-standards.md and dependencies.md}</Current_State>
   </project_context>
   ```

   Present suggestions for approval via AskUserQuestion:
   ```
   Gap detected in {section}:
   Suggested addition: {missing_content}

   Apply? [Y/n/Edit]:
   ```

   Gaps are non-blocking — Phase 6 proceeds if user declines.

2. For CLAUDE.md gaps (`claude_md_gaps` array):

   - Draft missing sections using context file content.
   - Present for approval via AskUserQuestion:
     ```
     CLAUDE.md gap: section "{section}" missing or incomplete.

     Suggested draft:
     {draft}

     Apply to CLAUDE.md? [Y/n/Edit]:
     ```
   - Apply only if user approves.
   - Note declined gaps in alignment log without modification.

**Tools:** AskUserQuestion, Edit

**Outputs:** Applied gap fixes (if approved). CLAUDE.md updates (if approved). Non-blocking gap log.

---

## Step 5: Process ADR Propagation Drift

**Inputs:** `adr_drift` array from Step 2 JSON output, ADR files in `devforgeai/specs/adrs/`

**Actions:**

1. Read referenced ADR file to confirm decision:
   ```
   Read(file_path="devforgeai/specs/adrs/{adr_id}.md")
   ```

2. Compare ADR decision against context file reference to identify divergence.

3. Prompt user: "Apply update? [Y/n]".
   - If approved: use Edit to update context file section.
   - If declined: log drift as deferred in alignment report.

4. ADR drift is non-blocking for Phase 6 — track for future remediation.

**Tools:** Read

**Outputs:** ADR drift remediation decisions. Updated context files (if approved). Drift log entries.

---

## Step 6: Report

**Inputs:** All resolution decisions from Steps 3-5, graceful degradation status from Step 2

**Actions:**

1. Compile Phase 5.5 alignment summary:
   - Contradictions: found / resolved / deferred / overridden
   - Gaps: found / applied / declined
   - ADR drift: found / remediated / deferred
   - ACCEPTED_RISK overrides with justifications
   - Graceful degradation events (if any)

2. Write report to:
   `devforgeai/feedback/ai-analysis/phase-5.5-alignment.json`

3. Display summary: contradictions (resolved/deferred), gaps (applied/declined), ADR drift
   (remediated/deferred), ACCEPTED_RISK count, Phase 6 gate status.

4. Set completion status: COMPLETE or DEGRADED (if graceful degradation occurred).

**Tools:** Display (built-in)

**Outputs:** Phase 5.5 completion status. Alignment report file written. Phase 6 gate status.
