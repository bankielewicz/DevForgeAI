---
name: github-incident-from-feedback
description: Convert selected AI-analysis recommendations from `devforgeai/feedback/ai-analysis/${STORY_ID}/...ai-analysis.json` files into GitHub issues in bankielewicz/DevForgeAI via gh issue create. Owns drafting, summary preview, drill-down approval flow, and posting. Consumes the embedded Github-incident-template.md as the issue-body schema and AI prompt. Use this skill whenever the user runs /create-incident-from-feedback, asks to convert ai_analysis recommendations into GitHub issues, asks to "post issues from feedback", asks to "create incidents from framework-analyst recommendations", or wants to turn AI-analysis findings into actionable GitHub work-orders. The skill is the only place in the framework that calls `gh issue create` for ai_analysis-derived work — slash commands and other skills MUST delegate here rather than calling gh directly.
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(gh:*), AskUserQuestion
---

# github-incident-from-feedback — Skill Definition

This skill converts an array of `ai_analysis` recommendations (already parsed and selected upstream from a `devforgeai/feedback/ai-analysis/${STORY_ID}/...ai-analysis.json` file) into GitHub issues posted to `bankielewicz/DevForgeAI`. It owns drafting, preview, approval, and posting. The slash command `/create-incident-from-feedback` delegates here for any work that touches `gh issue create`.

**Sibling skills:** `github-incident-from-rca` (RCA-derived recs) and `github-incident-from-recommendations` (QA-derived recs). Same posting pipeline, different input shape — `ai_analysis` recs are leaner than QA recs (no `file`/`line`/`before_code`/`after_code`/`verification` fields; have `description`/`affected_files[]`/`implementation_notes`/`priority`/`feasible_in_claude_code` instead). Drafting therefore looks closer to the RCA path than the QA path.

**Embedded asset (the AI prompt that defines the issue body schema, quality bar, prohibited language, and DevForgeAI house rules):**
- `assets/templates/Github-incident-template.md` — read this in Phase 1; it's the authoritative drafting prompt. Byte-identical to the two sibling skills' templates (a framework-wide invariant, not source-specific).

**Why a separate skill instead of inline command logic?** GitHub-issue creation has irreversible side effects (issues leave audit trails on the public repo). The framework's anti-pattern guidance treats irreversible-side-effect logic as a Layer-1 concern. Centralizing `gh issue create` in this skill (and its RCA and QA-recs siblings) gives one place to audit, version, and harden the posting path.

**Authorizing ADR:** ADR-077.

---

## When this skill is invoked

The slash command `/create-incident-from-feedback STORY-NNN` invokes this skill in Phase 10 of its workflow:

```
Skill(command="github-incident-from-feedback", args="--batch")
```

For eval/test runs that must NOT post real issues:

```
Skill(command="github-incident-from-feedback", args="--batch --eval")
```

Inputs the slash command provides (via shared context, since `args` is just a flag):

| Variable | Type | Source | Example |
|----------|------|--------|---------|
| `${ENTRY_ID}` | string | parsed from `/create-incident-from-feedback STORY-661` or `EPIC-081` | `STORY-661` or `EPIC-081` |
| `${SOURCE_FILE}` | path | resolved by slash command from `Glob("devforgeai/feedback/ai-analysis/${ENTRY_ID}/*ai-analysis*.json")` | `devforgeai/feedback/ai-analysis/EPIC-081/2026-02-22-epic-creation-ai-analysis.json` |
| `selected_recommendations` | array | output of slash command Phase 0 (multi-select AskUserQuestion) | see schema below |
| `repo` | string | hardcoded constant (template line 1) | `bankielewicz/DevForgeAI` |

`selected_recommendations` schema (each element — derived from `ai_analysis.recommendations[]`):

```json
{
  "id": "REC-FB-EPIC-081-M-001",
  "description": "<full description text from ai_analysis.recommendations[].description>",
  "affected_files": [".claude/skills/..."],
  "implementation_notes": "<free-text implementation guidance>",
  "priority": "high|medium|low",
  "feasible_in_claude_code": true,
  "source_operation": "epic-creation|/dev|/qa|sprint-retro|...",
  "source_timestamp": "2026-02-22T00:00:00Z"
}
```

**Note on `id`:** The source `ai_analysis.recommendations[]` does NOT carry an `id` field. The slash command's Phase 0 synthesizes one before delegating: `REC-FB-${ENTRY_ID}-${P}-${seq:03d}` where `P` is the first letter of priority (H/M/L) uppercased. The skill validates the synthesized id matches `^REC-FB-[A-Z0-9-]+-[HML]-\d{3}$`.

Outputs the slash command receives back (used by its Phase 11 linking step):

```json
[
  {
    "rec_id": "REC-FB-EPIC-081-M-001",
    "issue_number": 42,
    "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
    "status": "success",
    "error_message": null
  }
]
```

---

## Constants (locked)

```
REPO                   = bankielewicz/DevForgeAI
ISSUES_URL             = https://github.com/bankielewicz/DevForgeAI/issues
TEMPLATE_PATH          = assets/templates/Github-incident-template.md   # relative to this skill
DRAFTS_DIR             = tmp/${ENTRY_ID}/drafts/                        # per Rule 2 (operational-safety.md)
EVAL_MOCK_DIR          = tmp/eval-mock/                                 # only when --eval set
EVAL_POSTED_PATH       = tmp/eval-mock/posted.json                       # canonical mock-post log
EVAL_SKIPPED_PATH      = tmp/eval-mock/skipped.json                      # idempotency-skip diagnostics
SKIPPED_PATH           = tmp/${ENTRY_ID}/skipped.json                    # idempotency-skip in REAL mode
GH_BIN                 = gh                                              # PATH-resolved
ISSUE_NUMBER_HASH_BITS = 28                                              # sha256[:7] hex → mod 100000 deterministic
ID_PATTERN             = ^REC-FB-[A-Z0-9-]+-[HML]-\d{3}$
```

`tmp/${ENTRY_ID}/drafts/` is the per-invocation scratch directory. Per `.claude/rules/workflow/operational-safety.md` Rule 2, never write to system `/tmp/`. The `draft_path` field in posted entries always uses this project-relative path — never the eval-workspace-specific path. Drafts persist after the run for inspection and re-run.

**Skipped diagnostics live in their own file** (`skipped.json`), separate from `posted.json`. Rationale: `posted.json` should remain URL-clean (no real github.com URLs) so a `grep -E "github\\.com" posted.json` audit catches accidental leaks. Skipped entries (idempotency hits) often carry real-issue URLs from prior posts — keeping them out of `posted.json` preserves the audit invariant. Pattern identical to the QA-recs sibling.

---

## Eval Mode (`--eval` argument)

When invoked with `args="--batch --eval"`, Phase 5 substitutes `gh issue create` with a mock that:
- Returns a deterministic mock URL: `https://example.invalid/issue/<n>` where `<n>` is SHA-256-hash-derived from `rec.id` (reproducible across runs)
- Writes the mock-posting record to `tmp/eval-mock/posted.json` (single JSON file, stable schema — see "Posted schema" below)
- Routes idempotency-skip diagnostics to `tmp/eval-mock/skipped.json` (separate from posted.json)
- Does NOT invoke the real `gh` CLI (no network call, no real issue)

The user has parallel Claude sessions in OTHER repos; test runs must never accidentally interact with any GitHub repo. The `--eval` flag is the safety harness.

### Posted schema (stable — every entry has every field, even null)

```json
{
  "mode": "MOCKED",
  "repo": "bankielewicz/DevForgeAI",
  "note": "Eval mock posts — no real GitHub interaction. .invalid TLD is RFC-2606-reserved.",
  "generated_at": "<iso UTC>",
  "posted": [
    {
      "recommendation_id": "REC-FB-EPIC-081-M-001",
      "issue_number": 47312,
      "issue_url": "https://example.invalid/issue/47312",
      "title": "Add constitutional compliance pre-check to requirements elicitation",
      "labels": ["priority:medium", "origin:ai-analysis-feedback", "feasible:claude-code", "category:framework-improvement"],
      "draft_path": "tmp/EPIC-081/drafts/draft-REC-FB-EPIC-081-M-001.md",
      "ts": "2026-05-20T19:42:11Z",
      "status": "success",
      "error_message": null,
      "mock": true,
      "priority": "medium",
      "feasible_in_claude_code": true,
      "source_operation": "epic-creation"
    }
  ],
  "skipped": []
}
```

**Field rules:**
- **`recommendation_id`** — verbose form (matches sibling skills). NEVER abbreviate to `rec_id` in the file (the slash-command-returned summary array DOES use `rec_id`, but the on-disk audit log uses the verbose form).
- **`labels`** — array of strings, `key:value` namespaced. Standard set: `priority:{lower}`, `origin:ai-analysis-feedback`, `category:framework-improvement`. Plus `feasible:claude-code` when `feasible_in_claude_code == true`. Bare tokens are forbidden — they collide with org-level labels on other repos.
- **`draft_path`** — ALWAYS rooted at `tmp/${ENTRY_ID}/drafts/...` per operational-safety.md Rule 2.
- **`error_message`** — `null` when `status == "success"`, populated string otherwise. ALWAYS present.
- **`mock`** — `true` when this file is the eval-mock posted log.
- **`status`** — one of `success | failed | skipped | cancelled`.
- **`priority`/`feasible_in_claude_code`/`source_operation`** — copied from input rec for downstream filtering without label-string-splitting.
- **Top-level `posted`/`skipped` arrays** — ALWAYS emitted (`[]` for empty).

### Skip routing (separate file)

When idempotency check (Phase 1.5) detects an already-linked rec, the skill writes a structured skip record to `tmp/eval-mock/skipped.json` (in --eval) or `tmp/${ENTRY_ID}/skipped.json` (in REAL):

```json
{
  "mode": "MOCKED",
  "repo": "bankielewicz/DevForgeAI",
  "skipped": [
    {
      "recommendation_id": "REC-FB-EPIC-081-L-002",
      "reason": "already_posted",
      "existing_marker": "\"posted_as\": { \"issue_number\": 42, \"issue_url\": \"https://github.com/bankielewicz/DevForgeAI/issues/42\", ... }",
      "existing_issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
      "detected_in_phase": "idempotency_check",
      "ts": "<iso>"
    }
  ]
}
```

### Linking markers (source ai-analysis.json update)

After a successful post, the skill updates the source `ai_analysis.json` in place by adding a `posted_as` object to the recommendation:

```json
{
  "description": "Add constitutional compliance pre-check...",
  "affected_files": [".claude/skills/..."],
  "implementation_notes": "...",
  "priority": "medium",
  "feasible_in_claude_code": true,
  "posted_as": {
    "rec_id": "REC-FB-EPIC-081-M-001",
    "issue_number": 47312,
    "issue_url": "https://example.invalid/issue/47312",
    "posted_at": "2026-05-20T19:42:11Z",
    "mock": true,
    "fingerprint": "sha256:abc123..."
  }
}
```

In REAL mode, `mock` is `false` and the URL is a real `github.com` URL. In eval mode, `mock` is `true` and the URL is `https://example.invalid/...`. The idempotency check in Phase 1.5 grep-matches the `"posted_as"` substring under the matching `description` text to detect prior posts.

### Deterministic issue numbers

Mock issue numbers are SHA-256-hash-derived from `rec.id`, NOT timestamp or random:

```python
import hashlib
issue_number = int(hashlib.sha256(rec_id.encode("utf-8")).hexdigest()[:7], 16) % 100000
```

Same `rec_id` always yields the same `issue_number` across runs. Identical to the sibling skills.

---

## Phase 1 — Setup

**Goal:** Validate inputs, confirm `gh` is authenticated (skipped in `--eval` mode), load the template, detect prior runs.

### 1.1 Validate inputs

Read `selected_recommendations` from caller context. For each element, confirm these required fields are non-empty:
- `id` (matches `ID_PATTERN`)
- `description` (non-empty string, ≥20 chars)
- `priority` (one of `high`, `medium`, `low` — lowercase, matching the source `ai_analysis` schema)
- `affected_files` (array of paths; may be empty if the recommendation is framework-wide rather than file-specific — emit an Open Question if empty)

`implementation_notes` and `feasible_in_claude_code` are recommended but not required.

If any element fails validation, HALT with:
```
ERROR: Invalid recommendation in batch input: <details>
       This is an upstream contract violation — the slash command's Phase 0
       selection should have filtered or rejected this entry.
```

### 1.2 Confirm `gh` authentication (SKIPPED in --eval mode)

If `--eval` is set, skip 1.2 and 1.3. Otherwise:

```bash
gh auth status
```

| Exit code | Action |
|-----------|--------|
| 0 (authenticated) | Continue to 1.3 |
| Non-zero (not authenticated) | HALT. Emit: "gh CLI not authenticated. Run `gh auth login` and re-invoke `/create-incident-from-feedback`." Return all-failed results. |
| `gh` not on PATH | HALT. Emit: "gh CLI not installed. Install from https://cli.github.com and re-invoke." |

### 1.3 Confirm repo accessibility (SKIPPED in --eval mode)

```bash
gh repo view bankielewicz/DevForgeAI --json name 2>&1
```

If this fails, HALT with the gh error message. Do not attempt drafting if posting will fail.

### 1.4 Load the template

```
Read(file_path="assets/templates/Github-incident-template.md")
```

Bind the file content to context as the **drafting prompt**. Phase 2 applies its rules (quality bar, prohibited language, body schema, DevForgeAI house rules) to each recommendation.

### 1.5 Idempotency check

Read the source ai-analysis JSON:

```
Read(file_path="${SOURCE_FILE}")
```

For each recommendation in `selected_recommendations`, search the source JSON for an existing `posted_as` marker by description match. Because ai-analysis recs have no stable `id` in the source file, the match uses the rec's `description` substring (first 80 chars after the leading verb) AND the synthesized `rec.id` if it was written into the source on a prior run:

```
Grep(pattern="\"description\".*${description_first_80_chars_escaped}.*\"posted_as\"", path="${SOURCE_FILE}")
```

If a match exists for any rec, build a list of `already_linked_recs` and present them via `AskUserQuestion`:

- "Re-post anyway (creates duplicates) — proceed with all selected"
- "Skip already-linked (Recommended)"
- "Cancel — let me reconcile manually"

In `--eval` mode, default to "Skip already-linked" (deterministic behavior for evals).

**Skip routing:** Already-linked recs do NOT enter `posted.json`. Write structured skip records to a SEPARATE file (`skipped.json` per the schema above). The selected_recommendations array passed to Phase 2 excludes the skipped recs.

### 1.5.5 Remote duplicate check (ISSUE-797)

Before drafting, record a **remote duplicate scan** so the `pre-gh-incident-template-guard`
hook can verify the step ran and block `gh issue create` if the scan was skipped.

```bash
devforgeai-validate dup-scan ${ENTRY_ID} --query "<3-5 keywords from the recommendation>" --project-root=.
```

Read `tmp/${ENTRY_ID}/dup-scan.json` for the results list. If any result matches the same
defect/enhancement surface it in the approval loop BEFORE Phase 2:

```
AskUserQuestion →
    question: "Possible remote duplicate: #${number} '${title}' (${state}, ${url}). Proceed?"
    options:  ["Skip — record as duplicate (recommended)", "File anyway", "Cancel"]
```

Then record the human disposition so the hook gate can pass:

```bash
# on Skip:
devforgeai-validate dup-scan ${ENTRY_ID} --disposition "skipped-duplicate:#${number}" --project-root=.
# on File anyway:
devforgeai-validate dup-scan ${ENTRY_ID} --disposition "filed-anyway:user-confirmed" --project-root=.
# on no match found:
devforgeai-validate dup-scan ${ENTRY_ID} --disposition "no-match" --project-root=.
# on Cancel: return without proceeding to Phase 2
```

In `--eval` mode, skip the gh network scan and write disposition deterministically:
`devforgeai-validate dup-scan ${ENTRY_ID} --disposition "no-match" --project-root=.`
The remote scan is mandatory in REAL mode. **Batch-level design:** one scan per batch (keyed on `ENTRY_ID`) is by design — the hook passes for all recs in this batch once the batch-level `dup-scan.json` is recorded.

### 1.6 Create the drafts directory

```bash
mkdir -p tmp/${ENTRY_ID}/drafts/
[ -n "${EVAL_MODE}" ] && mkdir -p tmp/eval-mock/
```

---

## Phase 2 — Drafting

**Goal:** For each selected recommendation, produce a complete GitHub issue draft in markdown. AI-analysis recs are LESS structured than QA recs (no `before_code`/`after_code`/`verification`), so drafting carries more inference per Open Question.

### 2.1 Title synthesis

The source schema has no `title` field. Synthesize one from `description`:

```python
def synthesize_title(description: str) -> tuple[str, str]:
    """Returns (title, residual_description).

    Title: first sentence, ≤80 chars, verb-first imperative.
    If first sentence > 80 chars, truncate at last word boundary ≤77, add "…".
    Strip any leading "Add ", "Implement ", "Update " — and keep as the imperative verb.
    Residual: the full description minus the title text (becomes the `## Context` body).
    """
    first_sentence = description.split(".")[0].strip()
    if len(first_sentence) <= 80:
        return first_sentence, description
    # Truncate at word boundary
    truncated = first_sentence[:77].rsplit(" ", 1)[0] + "…"
    return truncated, description
```

If the synthesized title does not start with an imperative verb (Add/Update/Fix/Replace/Remove/Refactor/etc.), prepend an inferred verb based on the description. If inference is ambiguous, leave as-is and append an Open Question: "Title verb-first check — verify '${title}' reads as imperative; consider rewrite."

### 2.2 Direct field mapping

For each `rec` in `selected_recommendations`:

| AI-analysis rec field | → | Issue body section |
|-----------------------|---|--------------------|
| synthesized `title` | → | `# <Title>` (verb-first imperative, ≤80 chars) |
| `description` (residual) | → | `## Context` |
| `affected_files[]` | → | `## Files to change` (e.g., `- .claude/skills/foo/SKILL.md — see implementation notes`) |
| `implementation_notes` | → | `## Required behavior` (free-text guidance) |
| (derived from `affected_files` + `description`) | → | `## Acceptance criteria` (synthesized) |
| (derived) | → | `## Test plan` (see 2.3) |

### 2.3 Acceptance criteria + Test plan synthesis

AI-analysis recs do NOT carry verification commands. Synthesize ACs and a Test plan:

**Acceptance criteria** (default 2-3 items):
- `[ ] Change documented in PR description with reference to ${ENTRY_ID}`
- `[ ] Affected files updated per implementation notes: ${affected_files_count} file(s)`
- `[ ] Manual verification of behavior described in '## Context'`

If `affected_files[]` is empty, add an Open Question: "Acceptance criteria — affected_files[] is empty; downstream implementor must scope file targets."

**Test plan** (default):
- `Verify the change by inspecting: ${affected_files_joined_with_comma}` (if files present)
- `For framework-config changes: run \`devforgeai-validate validate-context\` after applying.`
- `For skill/agent file changes: confirm the consuming workflow still completes (smoke test the relevant slash command).`

Better-than-default ACs/Test plan: when `implementation_notes` contains a verifiable claim (e.g., "Update status from 'Proposed' to 'Accepted'"), derive a concrete AC for it.

### 2.4 Label assembly (array form, full namespacing)

```python
labels = [
    f"priority:{rec['priority'].lower()}",                # priority:high | priority:medium | priority:low
    "origin:ai-analysis-feedback",                        # origin marker
    "category:framework-improvement",                     # ai-analysis recs are framework-improvement by design
]

# Feasibility marker — preserves the framework-analyst's self-assessment
if rec.get("feasible_in_claude_code") is True:
    labels.append("feasible:claude-code")
elif rec.get("feasible_in_claude_code") is False:
    labels.append("feasible:requires-human")
```

**Before assuming a label exists on the repo** (REAL mode only), run `gh label list -R bankielewicz/DevForgeAI` ONCE per skill invocation and cache the result. Drop any label not on the repo and append an Open Question per affected draft: "Label '<X>' not on repo. Create with `gh label create '<X>'` or remove?"

In `--eval` mode, skip the `gh label list` call and emit ALL inferred labels.

### 2.5 Write each draft to disk (with mandatory `## Labels` body section)

The draft body MUST contain ALL 10 sections from the embedded template, in this exact order:

1. `# <Title>` (imperative, ≤80 chars, no prefix)
2. `## Context`
3. `## Current behavior` (often "Not yet implemented" or "Documented in implementation notes" for ai-analysis recs)
4. `## Required behavior`
5. `## Files to change`
6. `## Acceptance criteria`
7. `## Test plan`
8. `## Out of scope` (always emit — usually a one-line "Implementation scope only; no broader refactoring.")
9. `## Dependencies` (always emit — "None" for ai-analysis recs unless implementation_notes explicitly references another REC)
10. `## Labels` ← **MANDATORY — emit unconditionally**

The `## Labels` body section is mandatory even when the labels also appear in `posted.json`. Two reasons:
1. **Template fidelity** — the embedded `Github-incident-template.md` explicitly specifies a `## Labels` section.
2. **Audit trail** — humans reading the issue body shouldn't have to cross-reference the JSON file.

**Format and order:** Comma-separated string, order MUST match the JSON `labels[]` array exactly. `", ".join(labels_array)` does both.

```
Write(file_path="tmp/${ENTRY_ID}/drafts/draft-${rec.id}.md",
      content=f"""# {title}

## Context
{context_paragraph}

## Current behavior
{current_behavior}

## Required behavior
{required_behavior}

## Files to change
{files_to_change_list}

## Acceptance criteria
{ac_checklist}

## Test plan
{test_plan}

## Out of scope
Implementation scope only; no broader refactoring outside the affected_files set.

## Dependencies
{dependencies_text}

## Labels
{', '.join(labels_array)}
""")
```

If a draft has open questions, also:
```
Write(file_path="tmp/${ENTRY_ID}/drafts/open-questions-${rec.id}.md",
      content="<list of unresolved questions>")
```

### 2.6 Per-draft validation gate

Before recording a draft as ready, verify:

- [ ] Title is ≤80 chars, imperative verb-first, no prohibited language (per template line 59)
- [ ] All 10 template body sections populated
- [ ] **`## Labels` section is present and non-empty**
- [ ] **Body `## Labels` line matches `", ".join(labels_array)` exactly**
- [ ] At least 1 acceptance criterion in the checklist
- [ ] Test plan non-empty
- [ ] `affected_files[]` array reflected in body, OR an Open Question explaining the absence

If any check fails, append to Open Questions. Never silently drop validation failures.

---

## Phase 3 — Summary Preview

**Goal:** Show a compact, scrollable overview before approval.

### 3.1 Emit summary table

```
| #  | REC ID                       | Priority | Title                                | Labels                               | Open-Qs |
|----|------------------------------|----------|--------------------------------------|--------------------------------------|---------|
| 1  | REC-FB-EPIC-081-M-001        | medium   | Add constitutional compliance pre-… | priority:medium, origin:ai-analysis…| 0       |
| 2  | REC-FB-EPIC-081-L-002        | low      | Accept ADR-012 formally              | priority:low, origin:ai-analysis-f… | 0       |
```

Columns:
- `#` — sequential index in the batch
- `REC ID` — full synthesized ID
- `Priority` — high/medium/low (lowercase — matches source)
- `Title` — truncated to 36 chars
- `Labels` — truncated to 36 chars
- `Open-Qs` — count of bullets in the rec's open-questions file (`0` if no file)

### 3.2 Aggregate signals

After the table, emit per-category lines as applicable:
- `⚠ N drafts have unresolved Open Questions — inspect before posting.`
- `ℹ M drafts are marked feasible_in_claude_code:false — these will need human implementation.`
- `ℹ Drafts saved to tmp/${ENTRY_ID}/drafts/ for inspection.`

---

## Phase 4 — Drill-down Approval Loop

**Goal:** Let the user inspect drafts before committing to posting.

### 4.1 Initial prompt

```
AskUserQuestion(
  questions=[{
    question: "Approve posting? ${N} draft issues are ready (see summary table above).",
    header: "Approve",
    multiSelect: false,
    options: [
      {label: "Post all ${N} issues (Recommended)", description: "..."},
      {label: "Inspect a draft in detail", description: "..."},
      {label: "Post a subset", description: "..."},
      {label: "Cancel — post nothing", description: "..."}
    ]
  }]
)
```

### 4.2 Branch on user response

- **Post all** → `to_post = selected_recommendations`. Goto Phase 5.
- **Inspect** → Run 4.3 sub-loop. Then loop back to 4.1.
- **Post subset** → Run 4.4 multiselect. Then Phase 5 with chosen subset.
- **Cancel** → Return early with all `status: "cancelled"`.

### 4.3 Inspection sub-loop

Show full body of one draft, then re-prompt. Loop until user picks "Back to approval".

### 4.4 Subset selection

```
AskUserQuestion(multiSelect=true, options=<one per draft>)
```

Recs not chosen receive `status: "skipped"` with `error_message: "user excluded from subset post"`.

In `--eval` mode, default to "Post all" deterministically.

---

## Phase 5 — Post

**Goal:** Run `gh issue create` for each approved draft. Continue on per-issue failure.

### 5.1 Per-rec post invocation (REAL mode)

When `--eval` is NOT set, run the real `gh issue create` and capture the response into the stable-schema posted.json envelope:

```python
import subprocess
from datetime import datetime, timezone

posted_envelope = {
    "mode": "REAL",
    "repo": "bankielewicz/DevForgeAI",
    "note": "Real GitHub issues posted via gh issue create.",
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "posted": [],
    "skipped": []
}

for rec in to_post:
    title       = <synthesized imperative title — Phase 2.1, NO prefix>
    body_file   = f"tmp/{entry_id}/drafts/draft-{rec['id']}.md"
    labels_arr  = <array from Phase 2.4 — namespaced strings>

    Display: f"[{index+1}/{len(to_post)}] Posting: {rec['id']} — {title}"

    # ── Recurrence check (Issue #934) — MANDATORY before this rec's post ──
    # pre-gh-incident-template-guard Step 9 create-gate blocks gh issue create
    # unless a fresh recurrence-check artifact exists for the exact draft body
    # (keyed by the same bytes). It also detects an exact recurrence of an OPEN
    # issue so a +1 is recorded as a comment instead of filing a duplicate.
    # Provenance-only gate — it does NOT verify the OccurrenceInput is truthful.
    occurrence_file = f"tmp/{entry_id}/drafts/occurrence-{rec['id']}.json"
    # Write occurrence_file = OccurrenceInput JSON with the 12 fields the check
    # validates: source_kind, source_id, kind, provenance, title, description,
    # affected_files, evidence_refs, category, severity_or_priority,
    # producer_record_id, repo_identity. Set source_kind="ai_analysis",
    # source_id=rec['id'], repo_identity="bankielewicz/DevForgeAI".
    subprocess.run(["devforgeai-validate", "incident-recurrence", "check",
                    "--occurrence", occurrence_file, "--body-file", body_file,
                    "--verb", "create", "--project-root", "."])
    # Read disposition, fingerprint, matched_issue_number from the printed
    # artifact (tmp/incident-recurrence/checks/<body_sha256>.json).
    # IF disposition == "exact_open_match":
    #   AskUserQuestion → "REC {rec['id']}: exact recurrence of OPEN issue
    #     #{matched_issue_number}. Record a +1 recurrence comment instead of
    #     filing a new issue?" options ["Record +1 comment (recommended)",
    #     "File new anyway", "Cancel"].
    #   Record +1 comment → write tmp/{entry_id}/drafts/recurrence-comment-{rec['id']}.md
    #     = a "<!-- recurrence -->" marker line then exactly ONE line
    #     "repo_identity | fingerprint | run_id"
    #     (repo_identity=bankielewicz/DevForgeAI, fingerprint=<artifact fingerprint>, run_id=rec['id']);
    #     mint the comment artifact and post the comment, then continue (skip gh issue create):
    #       devforgeai-validate incident-recurrence check --occurrence {occurrence_file} --body-file <comment> --verb comment --project-root=.
    #       gh issue comment {matched_issue_number} --repo bankielewicz/DevForgeAI --body-file <comment>
    #     append _build_entry(..., status="recurrence-recorded"); continue
    #   File new anyway → fall through to gh issue create (the --verb create artifact satisfies Step 9).
    #   Cancel → append _build_entry(..., status="cancelled"); continue

    cmd = ["gh", "issue", "create",
           "--repo", "bankielewicz/DevForgeAI",
           "--title", title,
           "--body-file", body_file]
    if labels_arr:
        cmd.extend(["--label", ",".join(labels_arr)])
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        issue_url = result.stdout.strip()
        issue_number = int(issue_url.rsplit("/", 1)[1])
        entry = _build_entry(rec, issue_number, issue_url, title, labels_arr,
                             body_file, status="success", error_message=None, mock=False)
    else:
        entry = _build_entry(rec, None, None, title, labels_arr, body_file,
                             status="failed", error_message=result.stderr.strip(), mock=False)
    posted_envelope["posted"].append(entry)
```

**CRITICAL — Cross-repo guard:** `--repo bankielewicz/DevForgeAI` is hardcoded in EVERY invocation. The user has parallel Claude sessions in other repositories; without the explicit `--repo`, gh would default to the current directory's git remote, which could be ANY repo. The flag is non-negotiable.

### 5.2 Per-rec post invocation (--eval mode)

When `--eval` is set, substitute the gh command with a deterministic mock:

```python
import hashlib
from datetime import datetime, timezone

posted_envelope = {
    "mode": "MOCKED",
    "repo": "bankielewicz/DevForgeAI",
    "note": "Eval mock posts — no real GitHub interaction. .invalid TLD is RFC-2606-reserved.",
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "posted": [],
    "skipped": []
}

for rec in to_post:
    issue_number = int(hashlib.sha256(rec["id"].encode("utf-8")).hexdigest()[:7], 16) % 100000
    issue_url = f"https://example.invalid/issue/{issue_number}"
    draft_path = f"tmp/{entry_id}/drafts/draft-{rec['id']}.md"

    entry = {
        "recommendation_id": rec["id"],
        "issue_number": issue_number,
        "issue_url": issue_url,
        "title": title,
        "labels": labels_array,
        "draft_path": draft_path,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "success",
        "error_message": None,
        "mock": True,
        "priority": rec["priority"],
        "feasible_in_claude_code": rec.get("feasible_in_claude_code"),
        "source_operation": rec.get("source_operation"),
    }
    posted_envelope["posted"].append(entry)
    Display: f"  ✓ MOCK posted: Issue-mock-{issue_number} — {issue_url}"

Path("tmp/eval-mock/posted.json").write_text(json.dumps(posted_envelope, indent=2))
```

### 5.3 Source-file link-back (BOTH modes)

After each successful post (real or mock), update the source `ai_analysis.json` in place by adding `posted_as` to the matching recommendation:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

source = json.loads(Path(source_file).read_text())
for src_rec in source["ai_analysis"]["recommendations"]:
    # Match by description-first-80 prefix (recs in source have no id)
    if src_rec["description"][:80] == rec["description"][:80]:
        src_rec["posted_as"] = {
            "rec_id": rec["id"],
            "issue_number": issue_number,
            "issue_url": issue_url,
            "posted_at": entry["ts"],
            "mock": entry["mock"],
            "fingerprint": hashlib.sha256(f"{ENTRY_ID}::{rec['id']}::{title}".encode("utf-8")).hexdigest(),
        }
        break

Path(source_file).write_text(json.dumps(source, indent=2))
```

The fingerprint feeds the next-run idempotency check. Format identical to the QA-recs sibling's link-back pattern.

### 5.4 Per-failure error templates (REAL mode)

When `gh` returns non-zero, common causes:

| stderr signature | Likely cause | Surface to user |
|------------------|--------------|-----------------|
| `could not add label: 'X' not found` | Label missing | `Run gh label create '${X}' and re-run for the failed REC.` |
| `HTTP 401` / `Bad credentials` | Token expired | `Run gh auth refresh and re-run for failed RECs.` |
| `HTTP 403` / `rate limit exceeded` | Rate-limited | `Wait ${reset_minutes}m, re-run for failed RECs.` |
| `HTTP 422` / `validation failed` | Body too long, bad label | `Inspect tmp/${ENTRY_ID}/drafts/draft-${rec.id}.md and fix.` |
| Network error / timeout | Transient | `Retry after a moment.` |

Do NOT auto-retry. Surface and let user re-invoke.

---

## Phase 6 — Result

**Goal:** Print final summary and return result list.

### 6.1 Final summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GitHub Incident Creation Summary — ${ENTRY_ID} ${EVAL_MODE_BANNER}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Posted:   ${success_count}
   • REC-FB-NNN → Issue-NNN — <URL>
   • ...

❌ Failed:   ${failure_count}
   • REC-FB-NNN: ${error_message}

⏭ Skipped:  ${skip_count}
   • REC-FB-NNN: user excluded from subset

Drafts available at: tmp/${ENTRY_ID}/drafts/
${EVAL_MOCK_NOTE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

`${EVAL_MODE_BANNER}` is `"(EVAL MOCK)"` when `--eval` is set, else empty.
`${EVAL_MOCK_NOTE}` is `"Mock posts logged to tmp/eval-mock/posted.json"` when `--eval`, else empty.

### 6.2 Return value

Return `results` array to caller. The slash command's Phase 11 step consumes this for any further reporting (the in-place source-file link-back already happened in Phase 5.3).

---

## Business Rules (locked)

| Rule | Implementation |
|------|----------------|
| BR-001: Label assembly (array, namespaced) | Labels are an ARRAY of strings. Always include: `priority:{lower}`, `origin:ai-analysis-feedback`, `category:framework-improvement`, `feasible:claude-code\|requires-human` (when known). Drop labels not on repo (REAL mode); Open Question per draft. |
| BR-002: Title quality (no prefix) | Synthesized imperative verb-first, ≤80 chars, no prohibited language. NO `[FB-{PRIORITY}]` prefix — priority surfaced via `priority:*` label. |
| BR-003: Files-to-change honesty | AI-analysis recs carry `affected_files[]`. Empty arrays trigger an Open Question; the skill does NOT invent file targets. |
| BR-004: Failure isolation | A `gh issue create` failure on rec N does NOT block posting of rec N+1. |
| BR-005: Approval required | NO `gh issue create` (real or mock) before Phase 4 user approval (or default-Post-all in `--eval` mode). |
| BR-006: No system /tmp use | Drafts go to `tmp/${ENTRY_ID}/drafts/` per project root. |
| BR-007: Hardcoded repo + cross-repo guard | `bankielewicz/DevForgeAI` locked. EVERY `gh issue create` line has `--repo bankielewicz/DevForgeAI`. |
| BR-008: Drafts persist | Do not auto-delete drafts. Re-runs use them via idempotency check. |
| BR-009: Idempotency awareness | Phase 1.5 detects already-linked recs via `posted_as` substring under matching description. Skip records routed to `skipped.json`, NEVER mixed into `posted.json`. |
| BR-010: Source-file link-back | Phase 5.3 writes `posted_as` into the source JSON in place. Match key: `description` first-80-char prefix (since source recs have no stable id). |
| BR-011: Stable posted schema | `posted.json` is a SINGLE JSON object with top-level metadata + always-present `posted: []` + `skipped: []` arrays. Every entry has every field (use `null` for empty). Field name `recommendation_id` (verbose) in the file — `rec_id` only in the returned slash-command summary. |
| BR-012: Deterministic issue numbers | Mock issue numbers are `int(sha256(rec_id)[:7], 16) % 100000` — reproducible across runs. |
| BR-013: ID synthesis | Slash command Phase 0 mints `REC-FB-${ENTRY_ID}-${P}-${seq:03d}`. Source ai-analysis recommendations DO NOT carry stable ids; the synthesized form is the skill's idempotency key and stays in the `posted_as` block of the source file across runs. |
| BR-014: Feasibility-aware labels | When `feasible_in_claude_code` is True, add `feasible:claude-code`. When False, add `feasible:requires-human`. When absent, omit. Feasibility informs triage routing but does NOT block posting. |
| BR-015: `## Labels` body section is mandatory | Every draft body MUST end with a `## Labels` section containing the comma-joined label array. Order MUST match the JSON `labels[]` field exactly. |

---

## Edge Cases

| Edge case | Behavior |
|-----------|----------|
| `selected_recommendations` empty | Return empty results. Emit: "No recommendations to process." |
| `gh` not authenticated (REAL mode) | HALT in Phase 1.2. All-failed results with auth error. |
| `gh` not installed (REAL mode) | HALT in Phase 1.2. Install instructions. |
| Repo unreachable (REAL mode) | HALT in Phase 1.3. |
| All recs already linked | Phase 1.5 prompt. Default skip in --eval. |
| Empty `affected_files[]` | Open Question on the draft; proceed to Phase 3. Phase 4 lets user cancel. |
| `feasible_in_claude_code: false` for all recs | Proceed normally — label `feasible:requires-human` flags downstream triage. |
| All drafts have open questions | Proceed to Phase 3 summary. Phase 4 lets user cancel. |
| Mid-batch network failure (REAL) | Successes recorded; failures recorded per-rec. User re-runs for failures. |
| `gh label list` call fails | Cache empty list. Drop inferred labels; one Open Q per draft. |
| Issue body exceeds 64KB (REAL) | HTTP 422. User trims rec.description/implementation_notes, re-runs. |
| User cancels in Phase 4.3 mid-inspection | Treat as "Cancel" — all recs `status: "cancelled"`. |
| `--eval` mode (mock posts) | No `gh` calls. `tmp/eval-mock/posted.json` records mocks. Source-file link-back still happens (with `mock: true`). |
| Source ai-analysis JSON not writable | Posting proceeds; link-back fails silently with a log line. Idempotency check on next run will not detect prior post — duplicate posting risk. Surface as: "⚠ Source JSON link-back failed: ${error}. Re-runs will not detect this rec as already posted." |

---

## Integration

| Aspect | Value |
|--------|-------|
| **Invoked by** | `/create-incident-from-feedback` slash command (Phase 10) |
| **Invokes** | `gh` CLI via Bash (REAL mode only); `AskUserQuestion`; `Read`/`Write`/`Grep`/`Glob` for file ops; embedded `assets/templates/Github-incident-template.md` |
| **Reads** | `${SOURCE_FILE}` (idempotency check + link-back source-of-truth), `${TEMPLATE_PATH}` (drafting prompt) |
| **Writes** | `tmp/${ENTRY_ID}/drafts/draft-${REC_ID}.md`, `tmp/${ENTRY_ID}/drafts/open-questions-${REC_ID}.md` (when present), `tmp/eval-mock/posted.json` (--eval only) OR `tmp/${ENTRY_ID}/posted.json` (REAL), `${SOURCE_FILE}` (in-place `posted_as` link-back) |
| **Posts** | GitHub issues to `bankielewicz/DevForgeAI` (REAL mode) |
| **Returns** | Result array to caller |

---

## Naming Note (intentional deviation from ADR-017)

ADR-017 prescribes the `spec-driven-*` prefix for skills. This skill's name `github-incident-from-feedback` is a deliberate, user-confirmed deviation matching the sibling `github-incident-from-rca` and `github-incident-from-recommendations`: the skill is tightly coupled to the GitHub provider and to the AI-analysis feedback source artifact, not a generalized cross-cutting framework concern. A future framework analysis pass may consolidate all three siblings under a single `spec-driven-incidents` umbrella.

---

**Version:** 1.0 | **Created:** 2026-05-20 | **Pattern:** Skill owns external-side-effect logic; slash command orchestrates only. | **Authorizing ADR:** ADR-077.
