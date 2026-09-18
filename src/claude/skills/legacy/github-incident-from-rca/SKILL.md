---
name: github-incident-from-rca
description: Convert selected RCA recommendations into GitHub issues in bankielewicz/DevForgeAI via gh issue create. Owns drafting, summary preview, drill-down approval flow, and posting. Consumes the embedded Github-incident-template.md as the issue-body schema and AI prompt. Use this skill whenever the user runs /create-incident-from-rca, asks to convert RCA recommendations into GitHub issues, asks to "post issues from RCA", asks to "create incidents from RCA recommendations", or wants to turn analysis findings into actionable GitHub work-orders. The skill is the only place in the framework that calls `gh issue create` for RCA-derived work — slash commands and other skills MUST delegate here rather than calling gh directly.
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(gh:*), AskUserQuestion
---

# github-incident-from-rca — Skill Definition

This skill converts an array of RCA recommendations (already parsed and selected upstream) into GitHub issues posted to `bankielewicz/DevForgeAI`. It owns drafting, preview, approval, and posting. The slash command `/create-incident-from-rca` delegates here for any work that touches `gh issue create`.

**Embedded asset (the AI prompt that defines the issue body schema, quality bar, prohibited language, and DevForgeAI house rules):**
- `assets/templates/Github-incident-template.md` — read this in Phase 1; it's the authoritative drafting prompt.

**Why a separate skill instead of inline command logic?** GitHub-issue creation has irreversible side effects (new issues are not silently deletable; they leave audit trails on the public repo). The framework's anti-pattern guidance treats irreversible-side-effect logic as a Layer-1 concern. Keeping `gh issue create` exclusively in this skill gives one place to audit, version, and harden the posting path.

---

## When this skill is invoked

The slash command `/create-incident-from-rca RCA-NNN` invokes this skill in Phase 10 of its workflow, with the call:

```
Skill(command="github-incident-from-rca", args="--batch")
```

Inputs the slash command provides (via shared context, since `args` is just a flag):

| Variable | Type | Source | Example |
|----------|------|--------|---------|
| `${RCA_ID}` | string | parsed from `/create-incident-from-rca RCA-049` | `RCA-049` |
| `${RCA_FILE}` | path | resolved from `Glob("devforgeai/RCA/${RCA_ID}*.md")` | `devforgeai/RCA/RCA-049-batch-creation.md` |
| `selected_recommendations` | array | output of slash command Phase 6-9 (multi-select AskUserQuestion) | see schema below |
| `repo` | string | hardcoded constant (template line 1) | `bankielewicz/DevForgeAI` |

`selected_recommendations` schema (each element) — per ADR-074 tiered contract (`spec-driven-rca/references/recommendation-contract.md`):

```json
{
  "id": "REC-1",
  "priority": "CRITICAL|HIGH|MEDIUM|LOW",
  "title": "<one-line title>",
  "description": "<full text from RCA section>",
  "addresses_why": "Why #N — \"<exact quoted text from 5 Whys answer>\"",
  "evidence_files": "<comma-separated list of evidence file paths>",
  "test_specification": "<markdown table content from REC Test Specification section>",
  "conditional": { "type": "Unconditional|Conditional", "condition": "<trigger or null>" },
  "effort_hours": 6,
  "effort_points": null,
  "success_criteria": ["<bullet>", "<bullet>"]
}
```

**Tier obligations (ADR-074):**
- **Required tier** (`id`, `title`, `priority`, `description`, `addresses_why`, `evidence_files`): MUST be ingested and rendered verbatim into the issue body. `addresses_why` and `evidence_files` carry 5-Whys traceability — without them the resulting issue is unprovenanced.
- **Rendered tier** (`test_specification`, `success_criteria`, `effort_hours`, `effort_points`, `conditional`): MUST be rendered into the issue body. Phase 2 maps them to specific sections (see 2.1).

Outputs the slash command receives back (used by its Phase 11 linking step):
```json
[
  {
    "rec_id": "REC-1",
    "issue_number": 42,
    "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
    "status": "success",
    "error_message": null
  },
  {
    "rec_id": "REC-2",
    "issue_number": null,
    "issue_url": null,
    "status": "failed",
    "error_message": "label 'priority:critical' does not exist on this repo"
  }
]
```

---

## Constants (locked)

```
REPO            = bankielewicz/DevForgeAI
ISSUES_URL      = https://github.com/bankielewicz/DevForgeAI/issues
TEMPLATE_PATH   = assets/templates/Github-incident-template.md   # path relative to this skill
DRAFTS_DIR      = tmp/${RCA_ID}/drafts/                          # project-relative per operational-safety.md Rule 2
GH_BIN          = gh                                             # PATH-resolved
```

`tmp/${RCA_ID}/drafts/` is the per-invocation scratch directory. Per `.claude/rules/workflow/operational-safety.md` Rule 2, never write to system `/tmp/`. The skill cleans up only on explicit user request — drafts are kept for re-run / audit by default.

---

## Phase 1 — Setup

**Goal:** Validate inputs, confirm `gh` is authenticated, load the template, detect prior runs.

### 1.1 Validate inputs

Read `selected_recommendations` from caller context. For each element, confirm these fields are non-empty:
- `id` (matches `^REC-\d+$`)
- `title` (non-empty string)
- `priority` (one of CRITICAL, HIGH, MEDIUM, LOW)
- `description` (non-empty string)

If any element fails validation, HALT and emit:
```
ERROR: Invalid recommendation in batch input: <details>
       This is an upstream contract violation — the slash command's Phase 6-9
       selection should have filtered or rejected this entry.
```

### 1.2 Confirm `gh` authentication

```bash
gh auth status
```

Three outcomes:

| Exit code | Action |
|-----------|--------|
| 0 (authenticated) | Continue to 1.3 |
| Non-zero (not authenticated) | HALT. Emit: "gh CLI not authenticated. Run `gh auth login` and re-invoke `/create-incident-from-rca`." Return empty result list with status `failed` for all recs and `error_message: "gh not authenticated"`. |
| `gh` not on PATH | HALT. Emit: "gh CLI not installed. Install from https://cli.github.com and re-invoke." |

### 1.3 Confirm repo accessibility

```bash
gh repo view bankielewicz/DevForgeAI --json name 2>&1
```

If this fails (repo not accessible, network down, token lacks permission), HALT with the gh error message. Do not attempt drafting if posting will fail.

### 1.4 Load the template

```
Read(file_path="assets/templates/Github-incident-template.md")
```

Bind the file content to context as the **drafting prompt**. Phase 2 applies its rules (quality bar, prohibited language, body schema, DevForgeAI house rules) to each recommendation.

### 1.5 Idempotency check (BR-009)

Read the RCA file:
```
Read(file_path="${RCA_FILE}")
```

For each recommendation in `selected_recommendations`, search the RCA file for an existing issue link:
```
pattern = "${rec.id}.*Issue-\d+"
Grep(pattern=pattern, path="${RCA_FILE}")
```

If a match exists for any rec, that rec was already posted previously. **Do not silently skip.** Build a list of `already_linked_recs` and present them to the user via `AskUserQuestion`:

```
options = [
  { label: "Re-post anyway (creates duplicates) — proceed with all selected",
    description: "Each rec will get a new Issue-NNN; the RCA will accumulate multiple links per rec." },
  { label: "Skip already-linked (Recommended)",
    description: "Drop the ${len(already_linked)} already-linked recs from this batch; post the rest." },
  { label: "Cancel — let me reconcile manually",
    description: "Exit. The user resolves the duplication intent before re-running." }
]
```

Apply the user's choice. If "Skip already-linked", remove those recs from `selected_recommendations` and continue with the remainder. If "Cancel", return early with status `cancelled` for all selected recs.

### 1.5.5 Remote duplicate check (ISSUE-797)

Before drafting, record a **remote duplicate scan** so the `pre-gh-incident-template-guard`
hook can verify the step ran and block `gh issue create` if the scan was skipped.

```bash
devforgeai-validate dup-scan ${RCA_ID} --query "<3-5 keywords from the recommendation>" --project-root=.
```

Read `tmp/${RCA_ID}/dup-scan.json` for the results list. If any result matches the same
defect/enhancement surface it in the approval loop BEFORE Phase 2:

```
AskUserQuestion →
    question: "Possible remote duplicate: #${number} '${title}' (${state}, ${url}). Proceed?"
    options:  ["Skip — record as duplicate (recommended)", "File anyway", "Cancel"]
```

Then record the human disposition so the hook gate can pass:

```bash
# on Skip:
devforgeai-validate dup-scan ${RCA_ID} --disposition "skipped-duplicate:#${number}" --project-root=.
# on File anyway:
devforgeai-validate dup-scan ${RCA_ID} --disposition "filed-anyway:user-confirmed" --project-root=.
# on no match found:
devforgeai-validate dup-scan ${RCA_ID} --disposition "no-match" --project-root=.
# on Cancel: return without proceeding to Phase 2
```

In `--eval` mode, skip the gh network scan and write disposition deterministically:
`devforgeai-validate dup-scan ${RCA_ID} --disposition "no-match" --project-root=.`
The remote scan is mandatory in REAL mode. **Batch-level design:** one scan per batch (keyed on `RCA_ID`) is by design — the hook passes for all recs in this batch once the batch-level `dup-scan.json` is recorded.

### 1.6 Create the drafts directory

```
mkdir -p tmp/${RCA_ID}/drafts/
```

(This is `mkdir -p` via Bash, permitted under operational-safety.md Rule 2 because `tmp/` is the project-scoped scratch dir.)

---

## Phase 2 — Drafting

**Goal:** For each selected recommendation, produce a complete GitHub issue draft in markdown, plus an Open Questions list per rec (blockers/uninferable scope).

### 2.1 Apply the template's drafting rules per recommendation

For each `rec` in `selected_recommendations`:

1. **Title** (one line, ≤80 chars, imperative verb-first per template lines 22-25)
   - Translate `rec.title` from RCA-recommendation phrasing to issue-actionable phrasing.
   - Example: `rec.title = "Add structural fidelity agent"` → issue title: `Add structural-fidelity agent to /create-story-team workflow`
   - **Reject and rewrite** any title containing prohibited language (template line 59): "consider", "explore", "improve where appropriate", "modernize", "leverage", "streamline", etc. If the source can't be rewritten without invention, flag in Open Questions and use a neutral placeholder title (e.g., `[REC-N: <original title> — open question(s) block draft]`).

2. **Body sections** — populate verbatim from the template structure (template lines 22-55). Field sources per ADR-074 tier are noted:
   - `## Context` — 2-4 sentences. Pull from `rec.description` first paragraph + the RCA's title/severity. **Then append the 5-Whys provenance line: `> Addresses ${rec.addresses_why}` (Required-tier field; verbatim, including the `Why #N — "..."` shape).** No marketing language.
   - `## Current behavior` — exact description with file paths and line ranges. Pull from `rec.description` if it specifies files; otherwise list under Open Questions.
   - `## Required behavior` — exact post-change behavior. Pull from `rec.description` second paragraph or RCA "Recommended Action" subsection.
   - `## Files to change` — exact `path/to/file.ext` with one-line description per file. **PRIMARY SOURCE: `rec.evidence_files` (Required-tier).** Parse the comma-separated list and render one bullet per file. The rec's `Current Code Context` section (when present in `rec.description`) provides per-file context for the one-line description. If `rec.evidence_files` is `N/A — documentation-only change` OR empty, fall back to `rec.description` parsing. If still none, list under Open Questions — but the Required-tier contract states `evidence_files` SHOULD be present for any code-touching rec; an empty value flags an upstream RCA defect.
   - `## Acceptance criteria` — checklist. Map `rec.success_criteria` directly. Each item must be objectively verifiable (e.g., "passes test X", "function returns Y", "exit code is 0"). Strip subjective items ("code is cleaner") and flag them in Open Questions.
   - `## Test plan` — **PRIMARY SOURCE: `rec.test_specification` (Rendered-tier).** Render the markdown table verbatim under this section. If `rec.test_specification` is missing or empty, fall back to deriving from acceptance criteria — and add an Open Question noting the upstream RCA defect (`test_specification` is a Rendered-tier contract field per ADR-074).
   - `## Out of scope` — adjacent items NOT in this issue. Derive from rec body. If `rec.conditional.type == "Conditional"`, surface the trigger: `This issue is conditional — implement only when: ${rec.conditional.condition}`. If unconditional or unclear, list as: `- (none specified by recommendation)`.
   - `## Dependencies` — prerequisite issues, branches, decisions. Default: `None`. If the rec mentions another REC-N in the same RCA, note: `Depends on Issue posted for REC-N (link: <to-be-set-on-post>)`. If `rec.conditional.type == "Conditional"`, also include the conditional trigger as a dependency clause: `Conditional dependency: only post/implement when ${rec.conditional.condition} is true.`

3. **Labels** (template line 53) — comma-separated. Build by:
   - Map `rec.priority` → priority label:
     - CRITICAL → `priority:critical`
     - HIGH → `priority:high`
     - MEDIUM → `priority:medium`
     - LOW → `priority:low`
   - Add area label inferred from rec title/description keywords (e.g., "skill", "command", "agent" → `area:framework`; "test", "QA" → `area:qa`; "ci", "github actions" → `area:ci`). If no clear area, omit.
   - Add type label inferred from rec content:
     - Bug fix language ("fix", "broken", "regression") → `bug`
     - Doc-only ("update docs", "add reference") → `documentation`
     - Refactor language ("extract", "rename", "split") → `refactor`
     - New capability → `enhancement`
   - Before assuming a label exists, run `gh label list -R bankielewicz/DevForgeAI` ONCE per skill invocation (cache result). If a label is not in the list, leave it off and add an Open Question: `Label '<name>' does not exist on the repo. Create it (gh label create '<name>') or remove?`.

4. **Open Questions** — separate from the issue body (template lines 60-61). Capture every:
   - Vague-language clean-up that couldn't be translated without invention
   - File path the rec didn't specify
   - Subjective acceptance criterion stripped
   - Missing test plan detail
   - Missing label that was needed but doesn't exist on the repo

### 2.2 Write each draft to disk

```
Write(file_path="tmp/${RCA_ID}/drafts/draft-${rec.id}.md",
      content="<full issue body markdown — sections 1-9 of the template>")

Write(file_path="tmp/${RCA_ID}/drafts/open-questions-${rec.id}.md",
      content="<list of unresolved questions>")
```

If a draft has zero open questions, do NOT create the open-questions file (its absence signals "ready to post"). If it has any, the file's existence is a flag for Phase 3.

### 2.3 Per-draft validation gate

Before recording a draft as ready, verify:
- [ ] Title is ≤80 chars, imperative verb-first, no prohibited language
- [ ] All 7 body sections populated (Context, Current behavior, Required behavior, Files to change, Acceptance criteria, Test plan, Out of scope, Dependencies)
- [ ] At least 1 acceptance criterion in the checklist
- [ ] At least 1 file in "Files to change" (or all such items captured in Open Questions)
- [ ] Labels line is non-empty OR open-question explicitly notes label gap
- [ ] **Context section contains the verbatim `> Addresses Why #N — "..."` line from `rec.addresses_why`** (ADR-074 Required-tier rendering)
- [ ] **Files-to-change section was populated from `rec.evidence_files` (not invented)** OR the upstream rec defect was noted in Open Questions (ADR-074 Required-tier rendering)

If any check fails AND the failure isn't already in Open Questions, append to Open Questions. Never silently drop validation failures.

---

## Phase 3 — Summary Preview

**Goal:** Show the user a compact, scrollable overview before approval. No full draft bodies emitted at this phase — that's reserved for inspect drill-down.

### 3.1 Emit summary table

Use markdown table (renders well in chat). Columns:

```
| #  | REC ID  | Title                                    | Labels                            | Open-Qs |
|----|---------|------------------------------------------|-----------------------------------|---------|
| 1  | REC-1   | Add structural-fidelity agent to /create | priority:high, enhancement, area:framework | 0       |
| 2  | REC-2   | Wire phase-skip prevention hooks         | priority:critical, bug            | 1       |
| 3  | REC-3   | Update tech-stack.md ESM/CJS versions    | priority:medium, documentation    | 0       |
```

- Title column: truncate to 40 chars (append `…` if cut). Use the issue title (post-rewrite), not the original `rec.title`.
- Labels column: truncate to 35 chars.
- Open-Qs column: count of bullets in `tmp/${RCA_ID}/drafts/open-questions-${rec.id}.md`. `0` if file doesn't exist.

### 3.2 Surface aggregate signals

After the table, emit one line per category if applicable:
- `⚠ N drafts have unresolved Open Questions — inspect before posting.`
- `ℹ M drafts share priority:critical — posting these will likely create high-visibility issues.`
- `ℹ Drafts saved to tmp/${RCA_ID}/drafts/ for inspection.`

---

## Phase 4 — Drill-down Approval Loop

**Goal:** Let the user inspect drafts in detail before committing to posting, and let them post a subset if some look wrong.

### 4.1 Initial prompt

```
AskUserQuestion(
  questions=[{
    question: "Approve posting? ${N} draft issues are ready (see summary table above). Drafts with open questions: ${M}.",
    header: "Approve",
    multiSelect: false,
    options: [
      {
        label: "Post all ${N} issues (Recommended)",
        description: "Post every draft to ${REPO} in REC-ID order. Failures isolated per BR-004."
      },
      {
        label: "Inspect a draft in detail",
        description: "Show full body of one draft, then re-prompt for approval."
      },
      {
        label: "Post a subset",
        description: "Pick which drafts to post (multiselect)."
      },
      {
        label: "Cancel — post nothing",
        description: "Exit. Drafts remain in tmp/${RCA_ID}/drafts/ for the next run."
      }
    ]
  }]
)
```

### 4.2 Branch on user response

| Response | Action |
|----------|--------|
| **Post all** | Set `to_post = selected_recommendations`. Goto Phase 5. |
| **Inspect** | Run 4.3 (inspection sub-loop). Loop back to 4.1 after. |
| **Post subset** | Run 4.4 (subset selection). Then Phase 5 with selected subset. |
| **Cancel** | Return early. Skill output: `[{rec_id, status: "cancelled", ...} for rec in selected_recommendations]`. |

### 4.3 Inspection sub-loop

```
AskUserQuestion(
  questions=[{
    question: "Which draft to inspect?",
    header: "Inspect",
    multiSelect: false,
    options: [
      { label: "Draft 1 — ${title-truncated}",  description: "${labels}" },
      ...
      { label: "Back to approval prompt",       description: "Stop inspecting, return to summary." }
    ]
  }]
)
```

When user picks a draft N:
1. `Read(file_path="tmp/${RCA_ID}/drafts/draft-${rec.id}.md")` — emit full body to chat.
2. If `tmp/${RCA_ID}/drafts/open-questions-${rec.id}.md` exists, emit its content under heading `## Open Questions for REC-N`.
3. Loop back to 4.3 (let user inspect another draft) until they pick "Back to approval prompt".
4. Then loop back to 4.1.

### 4.4 Subset selection

```
AskUserQuestion(
  questions=[{
    question: "Select drafts to post (multiselect):",
    header: "Subset",
    multiSelect: true,
    options: [
      { label: "REC-1: ${title-truncated}", description: "${labels} | open-qs: ${count}" },
      { label: "REC-2: ${title-truncated}", description: "${labels} | open-qs: ${count}" },
      ...
    ]
  }]
)
```

Set `to_post` to the chosen subset. Recs not chosen receive `status: "skipped"` in the result (with `error_message: "user excluded from subset post"`). Goto Phase 5.

---

## Phase 5 — Post

**Goal:** Run `gh issue create` for each draft in `to_post`. Continue on per-issue failure (BR-004 isolation). Emit progress in real time.

### 5.1 Per-rec post invocation

```
FOR each rec in to_post:
    title       = <rewritten issue title from Phase 2.1>
    body_file   = "tmp/${RCA_ID}/drafts/draft-${rec.id}.md"
    labels      = <comma-separated label string from Phase 2.1>

    # Emit progress before the call
    Display: "[${index+1}/${len(to_post)}] Posting: ${rec.id} — ${title}"

    # ── Recurrence check (Issue #934) — MANDATORY before this rec's post ──
    # The pre-gh-incident-template-guard Step 9 create-gate blocks this gh issue
    # create unless a fresh recurrence-check artifact exists for the exact draft
    # body. Run it against body_file (same bytes the post sends). It also detects
    # an exact recurrence of an OPEN issue so a +1 is recorded as a comment
    # instead of filing a duplicate. Provenance-only gate — it does NOT verify
    # the OccurrenceInput is semantically truthful (a review concern).
    occurrence_file = "tmp/${RCA_ID}/drafts/occurrence-${rec.id}.json"
    Write occurrence_file = OccurrenceInput JSON with the 12 fields
        incident-recurrence check validates: source_kind, source_id, kind,
        provenance, title, description, affected_files, evidence_refs, category,
        severity_or_priority, producer_record_id, repo_identity. Set
        source_kind="rca", source_id="${rec.id}", repo_identity="bankielewicz/DevForgeAI".
    Bash: devforgeai-validate incident-recurrence check --occurrence ${occurrence_file} --body-file ${body_file} --verb create --project-root=.
    Read disposition, fingerprint, matched_issue_number from the printed artifact
        (tmp/incident-recurrence/checks/<body_sha256>.json).

    IF disposition == "exact_open_match":
        AskUserQuestion →
            question: "REC ${rec.id}: exact recurrence of OPEN issue #${matched_issue_number}. Record a +1 recurrence comment instead of filing a new issue?"
            options:  ["Record +1 comment (recommended)", "File new anyway", "Cancel"]
        Record +1 comment →
            Write tmp/${RCA_ID}/drafts/recurrence-comment-${rec.id}.md =
                a "<!-- recurrence -->" marker line, then exactly ONE line
                "repo_identity | fingerprint | run_id"
                (repo_identity=bankielewicz/DevForgeAI, fingerprint=<artifact fingerprint>, run_id=${rec.id}).
            Bash: devforgeai-validate incident-recurrence check --occurrence ${occurrence_file} --body-file tmp/${RCA_ID}/drafts/recurrence-comment-${rec.id}.md --verb comment --project-root=.
            Bash: gh issue comment ${matched_issue_number} --repo bankielewicz/DevForgeAI --body-file tmp/${RCA_ID}/drafts/recurrence-comment-${rec.id}.md
            results.append({rec_id: rec.id, issue_number: ${matched_issue_number}, status: "recurrence-recorded", error_message: null})
            CONTINUE   # skip gh issue create for this rec
        File new anyway → fall through to gh issue create below (the --verb create artifact satisfies Step 9).
        Cancel → results.append({rec_id: rec.id, status: "cancelled", ...}); CONTINUE
    # Non-exact_open_match dispositions fall through to gh issue create below.
    # In a no-network/eval mode, skip this step — a mocked post does not trigger the create-gate.

    # Construct gh command
    cmd = gh issue create
            --repo bankielewicz/DevForgeAI
            --title "${title}"
            --body-file "${body_file}"
            <only if labels non-empty:> --label "${labels}"

    # Run via Bash. Capture stdout (issue URL) and stderr (errors).
    result = Bash(command=cmd, ...)

    IF result.exit_code == 0:
        # gh prints the issue URL on success
        issue_url    = trim(result.stdout)                       # e.g., https://github.com/bankielewicz/DevForgeAI/issues/42
        issue_number = extract_int(issue_url, after="/issues/")  # 42
        Display: "  ✓ Posted: Issue-${issue_number} — ${issue_url}"
        results.append({
            rec_id: rec.id,
            issue_number: issue_number,
            issue_url: issue_url,
            status: "success",
            error_message: null
        })

    ELSE:
        Display: "  ✗ FAILED: ${result.stderr}"
        results.append({
            rec_id: rec.id,
            issue_number: null,
            issue_url: null,
            status: "failed",
            error_message: trim(result.stderr)
        })
        # BR-004: do not break the loop; continue to next rec
        CONTINUE
```

### 5.2 Per-failure error templates

When a `gh` call fails, common causes and how to surface them:

| stderr signature | Likely cause | What to surface to user |
|-----------------|--------------|-------------------------|
| `could not add label: 'X' not found` | Label doesn't exist on repo | "Label '${X}' missing. Run `gh label create '${X}'` and re-run /create-incident-from-rca for the failed REC." |
| `HTTP 401` / `Bad credentials` | Token expired mid-batch | "gh token expired. Run `gh auth refresh` and re-run for failed RECs." |
| `HTTP 403` / `rate limit exceeded` | Hit GitHub rate limit | "Rate-limited. Wait `${reset_minutes}` min, then re-run for failed RECs. (Successful posts already saved.)" |
| `HTTP 422` / `validation failed` | Body too long, title too long, or invalid label | "Validation failed: ${gh_message}. Inspect tmp/${RCA_ID}/drafts/draft-${rec.id}.md and fix before re-run." |
| Network error / timeout | Transient connectivity | "Network error. Retry after a moment." |

Do NOT auto-retry. Surface the error and let the user re-invoke if appropriate.

---

## Phase 6 — Result

**Goal:** Print a final summary and return the result list to the caller (the slash command's Phase 11 linking step).

### 6.1 Final summary

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  GitHub Incident Creation Summary — ${RCA_ID}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

success_count = count(results where status == "success")
failure_count = count(results where status == "failed")
skip_count    = count(results where status == "skipped")

Display: ""
Display: "✅ Posted:   ${success_count}"
FOR r in results where status == "success":
    Display: "   • ${r.rec_id} → Issue-${r.issue_number} — ${r.issue_url}"
Display: ""
IF failure_count > 0:
    Display: "❌ Failed:   ${failure_count}"
    FOR r in results where status == "failed":
        Display: "   • ${r.rec_id}: ${r.error_message}"
    Display: ""
IF skip_count > 0:
    Display: "⏭ Skipped:  ${skip_count}"
    FOR r in results where status == "skipped":
        Display: "   • ${r.rec_id}: ${r.error_message}"
    Display: ""

Display: "Drafts available at: tmp/${RCA_ID}/drafts/"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

### 6.2 Return value

Return `results` array to caller. The slash command's Phase 11 linking workflow consumes this — only success entries trigger RCA file updates with `Issue-NNN` references.

---

## Business Rules (locked)

| Rule | Implementation |
|------|----------------|
| BR-001: Priority → Label Mapping | CRITICAL→`priority:critical`, HIGH→`priority:high`, MEDIUM→`priority:medium`, LOW→`priority:low`. Skip if label missing on repo (record under Open Questions). |
| BR-002: Title Quality | Imperative verb-first, ≤80 chars, no prohibited language (template line 59). |
| BR-003: Files-to-change Honesty | Never invent file paths. If rec doesn't specify, list under Open Questions and surface as a draft validation flag. |
| BR-004: Failure Isolation | A `gh issue create` failure on rec N does NOT block posting of rec N+1. Each post is independent. |
| BR-005: Approval Required | NO `gh issue create` call may execute before Phase 4 user approval (post-all OR subset). Phase 1's `gh auth status` and `gh repo view` and `gh label list` are read-only and permitted. |
| BR-006: No System /tmp Use | Drafts go to `tmp/${RCA_ID}/drafts/` per project root. Per `.claude/rules/workflow/operational-safety.md` Rule 2. |
| BR-007: Hardcoded Repo | `bankielewicz/DevForgeAI` is locked (template line 1). Multi-repo support is explicitly out of scope. |
| BR-008: Drafts Persist | Do not auto-delete `tmp/${RCA_ID}/drafts/` on success or failure. The user may want to inspect or re-post. Cleanup is the user's choice. |
| BR-009: Idempotency Awareness | Phase 1.5 detects already-linked recs and asks the user how to handle (skip / repost / cancel). Default behavior: skip already-linked. |

---

## Edge Cases

| Edge case | Behavior |
|-----------|----------|
| `selected_recommendations` is empty | Return empty results array. Emit: "No recommendations to process." |
| `gh` not authenticated | HALT in Phase 1.2. Return all-failed results with auth error. |
| `gh` not installed | HALT in Phase 1.2. Return all-failed results with install instructions. |
| Repo unreachable | HALT in Phase 1.3. Same handling. |
| All recs already linked (BR-009) | Phase 1.5 prompt. If user picks "Skip", return all-skipped results with `error_message: "already linked, skipped per user choice"`. |
| All drafts have unresolved open questions | Still proceed to Phase 3 summary table. Phase 4 lets user choose "Cancel" to handle the questions before posting. |
| Mid-batch network failure | Posts that succeeded before failure are recorded. Posts after are recorded as failed. User re-invokes for the failures. No partial-state recovery — `tmp/${RCA_ID}/drafts/` persists for re-use. |
| Label list call fails | Cache empty list. All inferred labels go to Open Questions. User can post without labels OR cancel to fix label conventions first. |
| Issue body exceeds GitHub size limit (~64KB) | `gh` returns HTTP 422. Surface error; user must trim the rec's `description` and retry. |
| User cancels mid-inspection (Phase 4.3) | Treat as "Cancel" — return all selected recs as `status: "cancelled"`. |

---

## Reference Files

This skill keeps everything inline (under the 1000-line max for skills, on track at ~500 lines). If extraction becomes necessary in the future:

- `references/posting-error-recovery.md` — extended error templates, retry patterns
- `references/label-management.md` — interactive label creation flow

These are not yet authored. The current SKILL.md is self-contained.

---

## Integration

| Aspect | Value |
|--------|-------|
| **Invoked by** | `/create-incident-from-rca` slash command (Phase 10) |
| **Invokes** | `gh` CLI via Bash; `AskUserQuestion` tool; `Read`, `Write`, `Grep`, `Glob` for file ops; `assets/templates/Github-incident-template.md` (embedded asset, Phase 1.4) |
| **Reads** | `${RCA_FILE}` (idempotency check), `${TEMPLATE_PATH}` (drafting prompt) |
| **Writes** | `tmp/${RCA_ID}/drafts/draft-${REC_ID}.md`, `tmp/${RCA_ID}/drafts/open-questions-${REC_ID}.md` |
| **Posts** | GitHub issues to `bankielewicz/DevForgeAI` |
| **Returns** | Result array to caller |

---

## Naming Note (intentional deviation from ADR-017)

ADR-017 prescribes the `spec-driven-*` prefix for skills (e.g., `spec-driven-stories`, `spec-driven-rca`). This skill's name `github-incident-from-rca` is a deliberate, user-confirmed deviation: the skill is tightly coupled to the GitHub provider and to the RCA-incident workflow (it's not a generalized cross-cutting framework concern). A future framework analysis pass may consolidate this back under the `spec-driven-incidents` umbrella; for now, the literal name signals intent unambiguously.

---

**Version:** 1.0 | **Created:** 2026-05-05 | **Pattern:** Skill owns external-side-effect logic; slash command orchestrates only.
