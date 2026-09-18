---
name: create-incident-from-rca
description: Create GitHub incidents from RCA recommendations
argument-hint: "RCA-NNN [--threshold HOURS] [--help]"
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite
---

# /create-incident-from-rca - Create GH Incidents from RCA Recommendations

Parse RCA documents, select recommendations interactively, draft and post GitHub issues to bankielewicz/DevForgeAI via the `github-incident-from-rca` skill, then link the posted issues back into the RCA file.

**Component Orchestration:** Parse → Select → Draft+Approve+Post (skill) → Link

**Reference:** `references/create-incident-from-rca/incident-reference.md` for detailed docs.

**Architectural constraint:** This command never calls `gh` directly. All GitHub-issue logic is owned by the `github-incident-from-rca` skill. The slash command is a thin orchestrator.

---

## Usage

```bash
/create-incident-from-rca RCA-NNN [--threshold HOURS]
/create-incident-from-rca --help
```

---

## Argument Parsing

```
ARG = first argument from $ARGUMENTS

IF ARG == "--help" OR ARG == "help":
    Display abbreviated help:
    "Usage: /create-incident-from-rca RCA-NNN [--threshold HOURS]
     See: references/create-incident-from-rca/incident-reference.md for full help"
    HALT

RCA_ID = extract from arguments matching "RCA-[0-9]+" (case-insensitive)

IF RCA_ID empty:
    Display: "❌ RCA ID required"
    Display: "Usage: /create-incident-from-rca RCA-NNN"
    Display: "Available RCAs:"
    FOR rca in Glob("devforgeai/RCA/*.md"):
        Display: "  • ${rca_id}"
    HALT

RCA_ID = uppercase(RCA_ID)  # rca-049 → RCA-049

IF Glob("devforgeai/RCA/${RCA_ID}*.md") not found:
    Display: "❌ RCA not found: ${RCA_ID}"
    Display: "Available RCAs:"
    FOR rca in Glob("devforgeai/RCA/*.md"):
        Display: "  • ${rca_id}"
    HALT

# Optional: --threshold flag
THRESHOLD = parse_int(--threshold value) OR 0  # 0 = no filter
```

---

## Phase 1-5: RCA Parsing

**See:** `references/create-incident-from-rca/parsing-workflow.md`

Delegate parsing to the existing tested entry point in spec-driven-stories. This is a deliberate reuse — both /create-stories-from-rca and /create-incident-from-rca consume identical RCA structure, so parsing logic is shared.

```
IF RCA_ID ISNOT empty:
    Skill(command="spec-driven-stories", args="--RCA")
```

The skill returns:
1. **Locate RCA File**: `Glob(pattern="devforgeai/RCA/${RCA_ID}*.md")`
2. **Parse Frontmatter**: Extract id, title, severity, status
3. **Extract Recommendations**: Parse `### REC-N:` sections with priority, description, effort, success criteria
4. **Filter/Sort**: Apply effort threshold (if --threshold provided) and priority sort
5. **Display Results**: Show recommendations with effort estimates

The result is a parsed `rca_document` with a `recommendations` array, available to the next phase.

---

## Phase 6-9: Interactive Selection

**See:** `references/create-incident-from-rca/selection-workflow.md`

```
AskUserQuestion(
    question: "Which recommendations to convert into GitHub issues?",
    header: "Select",
    multiSelect: true,
    options: [
        "All recommendations (Recommended)",
        "REC-1: <title>",
        "REC-2: <title>",
        ...
        "None - cancel"
    ]
)
```

Capture `selected_recommendations` array. If empty / "None - cancel", HALT gracefully.

---

## Phase 10: Issue Drafting + Approval + Posting (DELEGATE TO SKILL)

**See:** `references/create-incident-from-rca/issue-creation-workflow.md`

This phase is delegated entirely to the `github-incident-from-rca` skill. The slash command does NOT format issue bodies, does NOT call `gh issue create`, does NOT manage approval prompts. The skill owns all of that.

```
Skill(command="github-incident-from-rca", args="--batch")
```

**Inputs the skill consumes** (via shared context):
- `${RCA_ID}`, `${RCA_FILE}` — from argument parsing
- `selected_recommendations` — from Phase 6-9
- `repo` — hardcoded constant `bankielewicz/DevForgeAI` (in skill itself)

**Outputs the skill returns** (used by Phase 11 below):
```
results = [
  { rec_id: "REC-1", issue_number: 42, issue_url: "https://...", status: "success", error_message: null },
  { rec_id: "REC-2", issue_number: null, issue_url: null, status: "failed", error_message: "label X missing" },
  { rec_id: "REC-3", issue_number: null, issue_url: null, status: "skipped", error_message: "user excluded from subset" }
]
```

The skill internally runs 6 phases:
1. Setup (validate inputs, gh auth check, idempotency detection)
2. Drafting (apply embedded template to each rec)
3. Summary preview (compact table)
4. Drill-down approval loop (user picks: post-all / inspect / subset / cancel)
5. Post (gh issue create per approved draft, continue-on-error)
6. Result (return to caller)

The slash command treats this as a single black-box delegation.

---

## Phase 11: RCA-Issue Linking

**See:** `references/create-incident-from-rca/linking-workflow.md`

For each entry in `results` with `status == "success"`, update the RCA file to record the issue link. This is a simple file edit — no GitHub API calls.

```
FOR result in results where status == "success":
    rec_id       = result.rec_id            # e.g., "REC-1"
    issue_number = result.issue_number      # e.g., 42
    issue_url    = result.issue_url         # e.g., "https://github.com/bankielewicz/DevForgeAI/issues/42"

    # 1. Update implementation checklist line
    Edit(
        file_path="${RCA_FILE}",
        old_string="- [ ] ${rec_id}",
        new_string="- [ ] ${rec_id}: See Issue-${issue_number} (${issue_url})"
    )

    # 2. Add inline reference under section header
    Edit(
        file_path="${RCA_FILE}",
        old_string="### ${rec_id}:",
        new_string="### ${rec_id}:\n**Implemented in:** Issue-${issue_number} — ${issue_url}\n"
    )
```

If the RCA frontmatter `status: OPEN` and ALL recommendations now have `Issue-NNN` links (no failures or skips), update status to `IN_PROGRESS`. Otherwise leave it.

---

## Error Handling

Validation errors, gh auth failures, label-missing errors, network failures, and per-issue failures are all handled with **failure isolation** — a failure on issue N does NOT block issue N+1. The `github-incident-from-rca` skill's Phase 5 handles posting errors and Phase 6 reports them. The slash command's Phase 11 only links successful posts.

See `references/create-incident-from-rca/incident-reference.md` for detailed error templates and recovery guidance.

---

## Success Criteria

- [ ] RCA document parsed correctly (Phase 1-5 via spec-driven-stories)
- [ ] Recommendations extracted and displayed
- [ ] User selection honored (Phase 6-9)
- [ ] Issues drafted with full template fidelity (skill Phase 2)
- [ ] User approval explicitly captured before any post (skill Phase 4)
- [ ] Issues posted via `github-incident-from-rca` skill (skill Phase 5)
- [ ] RCA document updated with `Issue-NNN` links for successful posts (Phase 11)
- [ ] Failure isolation: per-issue failures don't block batch
- [ ] Idempotency: re-runs detect already-linked RECs and prompt before duplicating

---

## Integration

**Invoked by:** User via `/create-incident-from-rca RCA-NNN`
**Invokes:**
- `spec-driven-stories` skill (Phase 1-5: RCA parsing — reuse)
- `github-incident-from-rca` skill (Phase 10: drafting + posting)

**Updates:** RCA document (issue links via Edit), GitHub issues (created via skill)

**Reference Files:** `references/create-incident-from-rca/` directory contains:
- `parsing-workflow.md` — Phase 1-5 detailed workflow
- `selection-workflow.md` — Phase 6-9 detailed workflow
- `issue-creation-workflow.md` — Phase 10 skill-delegation contract
- `linking-workflow.md` — Phase 11 RCA-update workflow
- `incident-reference.md` — Extended documentation, error templates, business rules

---

**Version:** 1.0 - Lean Orchestration | **Pattern:** Command delegates issue creation to skill
