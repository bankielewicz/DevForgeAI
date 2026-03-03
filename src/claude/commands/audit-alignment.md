---
description: "Validate configuration layer alignment across CLAUDE.md, system prompt, context files, rules, and ADRs"
argument-hint: "[--layer=all|claudemd|prompt|context|rules|adrs] [--fix] [--generate-refs] [--output=console|file]"
model: opus
allowed-tools: Read, Glob, Grep, Task, AskUserQuestion, Edit, Write
---

# /audit-alignment - Configuration Layer Alignment Audit

Detect contradictions, gaps, and ADR drift between configuration layers. Delegates all analysis to alignment-auditor subagent.

---

## Quick Reference

- `/audit-alignment` — Full audit, all layers, console output
- `/audit-alignment --layer=context` — Audit context files only
- `/audit-alignment --layer=adrs --fix` — Audit ADRs with fix proposals
- `/audit-alignment --output=file` — Write report to devforgeai/qa/
- `/audit-alignment --fix --generate-refs` — Regenerate domain reference files

---

## Phase 0: Argument Parsing

```
PARSE $ARGUMENTS:
  --layer          = $LAYER          (default: "all")
  --fix            = $FIX            (default: false)
  --generate-refs  = $GENERATE_REFS  (default: false)
  --output         = $OUTPUT         (default: "console")

IF $GENERATE_REFS == true AND $FIX != true:
  Display: "❌ --generate-refs requires --fix (regeneration is a fix action)"
  HALT

VALID_LAYERS = [all, claudemd, prompt, context, rules, adrs]

IF $LAYER not in VALID_LAYERS:
  AskUserQuestion:
    question: "Invalid --layer value. Which layer to audit?"
    header: "Layer"
    options:
      - { label: "all", description: "Audit all layers (Recommended)" }
      - { label: "claudemd", description: "CLAUDE.md only" }
      - { label: "context", description: "6 context files only" }
      - { label: "adrs", description: "ADR files only" }
    multiSelect: false
  SET $LAYER = user_selection

SET report_path = "devforgeai/qa/alignment-audit-{YYYY-MM-DD}.md"

Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  Configuration Layer Alignment Audit"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  Layer: {$LAYER} | Fix: {$FIX} | Output: {$OUTPUT}"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Phase 1: Invoke Alignment Auditor

**Zero business logic here. All analysis delegated to subagent.**

```
Task(
  subagent_type="alignment-auditor",
  description="Audit configuration layer alignment",
  prompt="""
  Perform pairwise alignment audit across configuration layers.

  Layer filter: ${LAYER}

  Return structured findings as JSON array:
  [
    {
      "id": "CHK-NNN",
      "type": "contradiction|gap|adr_drift",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "layer_a": "source layer name",
      "layer_b": "target layer name",
      "description": "what is misaligned",
      "line_a": N,
      "line_b": N,
      "resolution": "proposed fix"
    }
  ]

  Also return summary:
  {
    "contradictions": N,
    "gaps": N,
    "adr_drift": N,
    "total": N,
    "status": "PASS|WARN|FAIL"
  }
  """
)

SET findings = subagent_result.findings
SET summary = subagent_result.summary
```

---

## Phase 2: Severity-Based Display Formatting

**Group findings by severity in descending order: CRITICAL > HIGH > MEDIUM > LOW.**

```
FOR severity IN [CRITICAL, HIGH, MEDIUM, LOW]:
  filtered = findings WHERE severity == current_severity

  IF filtered is not empty:
    Display:
    "### {severity_badge} {severity} ({count})"
    ""
    "| Check ID | Layer A | Layer B | Description | Lines |"
    "|----------|---------|---------|-------------|-------|"

    FOR finding IN filtered:
      Display: "| {finding.id} | {finding.layer_a} | {finding.layer_b} | {finding.description} | {finding.line_a}-{finding.line_b} |"

severity_badges:
  CRITICAL: "🔴"
  HIGH: "🟠"
  MEDIUM: "🟡"
  LOW: "🔵"
```

---

## Phase 3: Conditional Fix Proposals (--fix)

```
IF $FIX == true:
  Display: "## Fix Proposals"
  Display: ""

  FOR finding IN findings:
    DETERMINE layer mutability:

    # MUTABLE layers — propose edits via AskUserQuestion
    IF finding.layer_b == "CLAUDE.md":
      AskUserQuestion:
        question: "Apply fix to CLAUDE.md? {finding.resolution}"
        header: "Fix"
        options:
          - { label: "Apply edit", description: "Edit CLAUDE.md" }
          - { label: "Skip", description: "Do not modify" }
      IF user selects "Apply edit":
        Edit(file_path="CLAUDE.md", ...)

    # MUTABLE — system prompt additions
    ELIF finding.layer_b matches "system-prompt":
      AskUserQuestion:
        question: "Add to system prompt? {finding.resolution}"
        header: "Fix"
        options:
          - { label: "Add content", description: "Append to system prompt" }
          - { label: "Skip", description: "Do not modify" }

    # IMMUTABLE — context files (6) — never edit, ADR only
    ELIF finding.layer_b matches "context files":
      Display: "⚠️ IMMUTABLE: {finding.layer_b} cannot be edited directly"
      Display: "  → Recommendation: Create ADR to authorize change"
      Display: "  → Run: /create-context to update via proper workflow"
      # Never call Edit() on context files

    # MUTABLE — rules files
    ELIF finding.layer_b matches "rules":
      AskUserQuestion:
        question: "Apply fix to rule? {finding.resolution}"
        header: "Fix"
        options:
          - { label: "Apply edit", description: "Edit rule file" }
          - { label: "Skip", description: "Do not modify" }

    # APPEND-ONLY — ADRs — recommend new ADR, never edit existing
    ELIF finding.layer_b matches "adrs":
      Display: "📝 APPEND-ONLY: Cannot edit existing ADR"
      Display: "  → Recommendation: Create new ADR superseding {finding.id}"
      # Never call Edit() on existing ADRs

ELSE:
  Display: "(Run with --fix to see fix proposals)"
```

---

## Phase 3.5: Domain Reference Regeneration (--generate-refs)

**Overwrite project-*.md, remove stale. Delegated via Task().**

```
IF $GENERATE_REFS == true AND $FIX == true:
  Display: "🔄 Regenerating domain reference files..."

  Task(
    subagent_type="general-purpose",
    description="Regenerate domain references via Phase 5.7",
    prompt="""
    Execute Phase 5.7 Domain Reference Generation per:
    .claude/skills/designing-systems/references/domain-reference-generation.md

    1. Re-evaluate ALL 4 heuristics (DH-01, DH-02, DH-03, DH-04) against context files
    2. Overwrite existing project-*.md files (not append), update auto-generation header with date
    3. Detect stale files (heuristic no longer triggers) — AskUserQuestion before deletion:
       options: "Remove stale file" | "Keep file (manual override)"
    """
  )

  Display: "✓ Domain reference regeneration complete"
```

---

## Phase 4: Output Handling

```
IF $OUTPUT == "file":
  # Build markdown report
  report_content = """
  # Configuration Layer Alignment Audit Report
  **Generated:** {YYYY-MM-DD}
  **Layer:** {$LAYER}
  **Status:** {summary.status}

  ## Executive Summary
  {summary_table}

  ## Detailed Findings
  {severity_grouped_findings}

  ## Fix Proposals
  {fix_proposals_if_any}
  """

  Write(file_path=report_path, content=report_content)
  Display: "Report written to: {report_path}"

# Always display to terminal (both console and file modes)
```

---

## Phase 5: Executive Summary Table

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  Executive Summary"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
""
"| Category      | CRITICAL | HIGH | MEDIUM | LOW | Total |"
"|---------------|----------|------|--------|-----|-------|"
"| Contradictions| {c_crit} | {c_hi}| {c_med}| {c_lo}| {summary.contradictions} |"
"| Gaps          | {g_crit} | {g_hi}| {g_med}| {g_lo}| {summary.gaps} |"
"| ADR Drift     | {d_crit} | {d_hi}| {d_med}| {d_lo}| {summary.adr_drift} |"
"| **Total**     |          |      |        |     | **{summary.total}** |"

Per-category counts show findings broken down by type and severity level.
""
"**Overall Status:** {summary.status}"
""

STATUS_RULES:
  PASS = 0 findings
  WARN = findings exist but 0 CRITICAL
  FAIL = any CRITICAL finding exists

Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Error Handling

```
IF alignment-auditor subagent not found:
  Display: "❌ alignment-auditor subagent not available"
  Display: "   Ensure .claude/agents/alignment-auditor.md exists"
  Display: "   See STORY-473 for subagent creation"
  HALT

IF 6 context files not all present:
  Display: "❌ Missing context files in devforgeai/specs/context/"
  Display: "   Run /create-context to generate"
  HALT

IF findings is empty (fully aligned):
  Display: "✅ PASS — All configuration layers aligned. 0 findings."
```

---

## Integration

**Invoked by:** Framework maintainers, after /create-context, after ADR acceptance
**Generates:** `devforgeai/qa/alignment-audit-{YYYY-MM-DD}.md` (if --output=file)
**Updates:** None by default (read-only audit); --fix may edit MUTABLE layers with user approval
**Uses:** alignment-auditor subagent via Task()

**Related commands:**
- `/audit-orphans` — Orphaned file detection
- `/audit-budget` — Command character budget audit
- `/audit-deferrals` — Deferred work audit
