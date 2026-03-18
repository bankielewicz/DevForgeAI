# Phase 02: Workflow Dispatch

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=01 --to=02 ${WORKFLOW_FLAG}
# Exit 0: proceed | Exit 1: Phase 01 incomplete | Exit 127: CLI not installed (continue)
```

## Contract

PURPOSE: Resolve the workflow-specific phase list based on WORKFLOW_TYPE determined in Phase 01. Set the phase sequence for the orchestration loop. Display workflow plan.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: PHASE_LIST set, EXPECTED_COUNT set, workflow plan displayed
STEP COUNT: 3 mandatory steps

---

## Mandatory Steps

### Step 2.1: Resolve Phase List

EXECUTE: Select the phase sequence based on WORKFLOW_TYPE.
```
IF WORKFLOW_TYPE == "generation":
    PHASE_LIST = ["G03", "G04", "G05", "G06", "G07", "G08", "G09", "G10"]
    EXPECTED_COUNT = 10  # Including phases 01, 02
    Display: "Generation workflow selected: 10 phases (01, 02, G03-G10)"

ELIF WORKFLOW_TYPE == "audit":
    PHASE_LIST = ["A03", "A04", "A05", "A06", "A07"]
    EXPECTED_COUNT = 7  # Including phases 01, 02
    Display: "Audit workflow selected: 7 phases (01, 02, A03-A07)"

ELIF WORKFLOW_TYPE == "fix":
    PHASE_LIST = ["F03", "F04", "F05", "F06", "F07", "F08"]
    EXPECTED_COUNT = 8  # Including phases 01, 02
    Display: "Fix workflow selected: 8 phases (01, 02, F03-F08)"

ELSE:
    HALT: "Unknown WORKFLOW_TYPE: {WORKFLOW_TYPE}. Expected: generation, audit, or fix."
```
VERIFY: PHASE_LIST is a non-empty array. EXPECTED_COUNT is a positive integer.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=02 --step=2.1 ${WORKFLOW_FLAG}`

---

### Step 2.2: Resolve Documentation Types (Generation Only)

EXECUTE: If generation workflow, resolve which documentation types to generate.
```
IF WORKFLOW_TYPE == "generation":
    IF $DOC_TYPE == "all" OR $DOC_TYPE == "module":
        TYPES = ["api", "architecture", "developer-guide", "troubleshooting", "roadmap"]
        Display: "Documentation types: all ({len(TYPES)} types)"
    ELSE:
        TYPES = [$DOC_TYPE]
        Display: "Documentation type: {$DOC_TYPE}"

    # Resolve output strategy (section-level consolidation)
    OUTPUT_MAP = {
        "api": "docs/api/API.md",
        "architecture": "docs/architecture/ARCHITECTURE.md",
        "developer-guide": "docs/guides/DEVELOPER-GUIDE.md",
        "troubleshooting": "docs/guides/TROUBLESHOOTING.md",
        "roadmap": "docs/guides/ROADMAP.md"
    }
    Display: "Output strategy: section-level consolidation into framework files"

ELIF WORKFLOW_TYPE == "audit":
    Display: "Audit workflow: No documentation types to resolve"

ELIF WORKFLOW_TYPE == "fix":
    Display: "Fix workflow: Types determined by findings in audit file"
```
VERIFY: If generation, TYPES array is populated and OUTPUT_MAP is defined. If audit/fix, step acknowledged.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=02 --step=2.2 ${WORKFLOW_FLAG}`

---

### Step 2.3: Display Workflow Plan

EXECUTE: Display the complete plan for the selected workflow.
```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Workflow Plan: {WORKFLOW_TYPE}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""

IF WORKFLOW_TYPE == "generation":
    Display: "  Phase G03: Discovery & Analysis"
    Display: "  Phase G04: Content Generation (documentation-writer subagent)"
    Display: "  Phase G05: Template Application & Customization"
    Display: "  Phase G06: Section-Level Integration"
    Display: "  Phase G07: Post-Generation Integration"
    Display: "  Phase G08: Validation & Quality Check (coverage >= 80%)"
    Display: "  Phase G09: Export & Finalization"
    Display: "  Phase G10: Completion Summary"

ELIF WORKFLOW_TYPE == "audit":
    Display: "  Phase A03: Audit Discovery"
    Display: "  Phase A04: Audit Analysis (4 dimensions)"
    Display: "  Phase A05: Audit Prioritization"
    Display: "  Phase A06: Audit Output (doc-audit.json)"
    Display: "  Phase A07: Audit Display"

ELIF WORKFLOW_TYPE == "fix":
    Display: "  Phase F03: Load Findings"
    Display: "  Phase F04: Classify Findings"
    Display: "  Phase F05: Preview Changes"
    Display: "  Phase F06: Execute Fixes"
    Display: "  Phase F07: Verify Fixes"
    Display: "  Phase F08: Fix Report"

Display: ""
Display: "  Total phases: {EXPECTED_COUNT}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
```
VERIFY: Workflow plan displayed with correct phase count matching EXPECTED_COUNT.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=02 --step=2.3 ${WORKFLOW_FLAG}`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=02 --checkpoint-passed ${WORKFLOW_FLAG}
```

## Phase Transition Display

```
Display: ""
Display: "Phase 02 complete: Workflow Dispatch"
Display: "  Proceeding to Phase {PHASE_LIST[0]}: {first phase name}"
Display: ""
```
