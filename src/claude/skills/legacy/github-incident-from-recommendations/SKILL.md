---
name: github-incident-from-recommendations
description: Convert selected QA recommendations from devforgeai/qa/recommendations/STORY-NNN-qa-recommendations.md into GitHub issues in bankielewicz/DevForgeAI via gh issue create. Owns drafting, summary preview, drill-down approval flow, and posting. Consumes the embedded Github-incident-template.md as the issue-body schema and AI prompt. Use this skill whenever the user runs /create-incident-from-recommendations, asks to convert QA recommendations into GitHub issues, asks to "post issues from QA recs", asks to "create incidents from STORY-NNN findings", or wants to turn QA-validated findings into actionable GitHub work-orders. The skill is the only place in the framework that calls `gh issue create` for QA-recs-derived work — slash commands and other skills MUST delegate here rather than calling gh directly.
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(gh:*), AskUserQuestion
---

# github-incident-from-recommendations — Skill Definition

This skill converts an array of QA recommendations (already parsed from `devforgeai/qa/recommendations/STORY-NNN-qa-recommendations.md` and selected upstream) into GitHub issues posted to `bankielewicz/DevForgeAI`. It owns drafting, preview, approval, and posting. The slash command `/create-incident-from-recommendations` delegates here for any work that touches `gh issue create`.

**Sibling skill:** `github-incident-from-rca` (RCA-derived recs). Same posting pipeline, different input shape — QA recs are pre-structured (file, line, before_code, after_code, verification.command, classification) so drafting needs far fewer "Open Questions" inferences than the RCA path.

**Embedded asset (the AI prompt that defines the issue body schema, quality bar, prohibited language, and DevForgeAI house rules):**
- `assets/templates/Github-incident-template.md` — read this in Phase 1; it's the authoritative drafting prompt. Identical byte-for-byte to the sibling RCA skill's template.

**Why a separate skill instead of inline command logic?** GitHub-issue creation has irreversible side effects (issues leave audit trails on the public repo). The framework's anti-pattern guidance treats irreversible-side-effect logic as a Layer-1 concern. Centralizing `gh issue create` in this skill (and its RCA sibling) gives one place to audit, version, and harden the posting path.

---

## When this skill is invoked

The slash command `/create-incident-from-recommendations STORY-NNN` invokes this skill in Phase 10 of its workflow:

```
Skill(command="github-incident-from-recommendations", args="--batch")
```

For eval/test runs that must NOT post real issues:

```
Skill(command="github-incident-from-recommendations", args="--batch --eval")
```

Inputs the slash command provides (via shared context, since `args` is just a flag):

| Variable | Type | Source | Example |
|----------|------|--------|---------|
| `${STORY_ID}` | string | parsed from `/create-incident-from-recommendations STORY-661` | `STORY-661` |
| `${QA_RECS_FILE}` | path | `devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md` | `devforgeai/qa/recommendations/STORY-661-qa-recommendations.md` |
| `selected_recommendations` | array | output of slash command Phase 6-9 (multi-select AskUserQuestion) | full QA-recs schema (see below) |
| `repo` | string | hardcoded constant (template line 1) | `bankielewicz/DevForgeAI` |

`selected_recommendations` schema (each element — full QA-recs schema per `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`):

```json
{
  "id": "REC-STORY-661-M-001",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "provenance": "GROUNDED|DERIVED|INCONCLUSIVE",
  "title": "<imperative one-line summary, 10-120 chars>",
  "file": "src/claude/scripts/...",
  "line": 623,
  "line_range": [421, 431],
  "category": "correctness|security|performance|test_quality|coverage|anti_pattern|documentation",
  "blocking_release": false,
  "before_code": "<exact current source>",
  "after_code": "<exact proposed source>",
  "remediation_steps": ["step 1", "step 2"],
  "verification": {"command": "<shell/pytest cmd>", "expected": "<exit/output>"},
  "estimated_effort_minutes": 15,
  "dependencies": ["REC-STORY-661-M-002"],
  "references": [{"source": "RCA-066", "url": "...", "line_range": [10, 20]}],
  "classification": "REGRESSION|PRE_EXISTING",
  "cycle_first_seen": 2
}
```

Only one of (`before_code`+`after_code`) OR `remediation_steps` is populated per rec — schema guarantees this via oneOf constraint.

Outputs the slash command receives back (used by its Phase 11 linking step):

```json
[
  {
    "rec_id": "REC-STORY-661-M-001",
    "issue_number": 42,
    "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
    "status": "success",
    "error_message": null
  },
  {
    "rec_id": "REC-STORY-661-M-002",
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
REPO                   = bankielewicz/DevForgeAI
ISSUES_URL             = https://github.com/bankielewicz/DevForgeAI/issues
TEMPLATE_PATH          = assets/templates/Github-incident-template.md   # relative to this skill
DRAFTS_DIR             = tmp/${STORY_ID}/drafts/                        # per Rule 2 (operational-safety.md)
EVAL_MOCK_DIR          = tmp/eval-mock/                                 # only when --eval set
EVAL_POSTED_PATH       = tmp/eval-mock/posted.json                       # canonical mock-post log
EVAL_SKIPPED_PATH      = tmp/eval-mock/skipped.json                      # idempotency-skip diagnostics (separate file — keeps posted.json URL-clean)
SKIPPED_PATH           = tmp/${STORY_ID}/skipped.json                    # idempotency-skip in REAL mode
GH_BIN                 = gh                                              # PATH-resolved
ISSUE_NUMBER_HASH_BITS = 28                                              # sha256[:7] hex → 28 bits → mod 100000 = deterministic 0..99999
```

`tmp/${STORY_ID}/drafts/` is the per-invocation scratch directory. Per `.claude/rules/workflow/operational-safety.md` Rule 2, never write to system `/tmp/`. The `draft_path` field in posted-mock entries always uses this project-relative path — never the eval-workspace-specific path. Drafts are kept after the run for inspection and re-run.

**Skipped diagnostics live in their own file** (`skipped.json`), separate from `posted.json`. Rationale: `posted.json` should remain URL-clean (no real github.com URLs) so a `grep -E "github\\.com" posted.json` audit catches accidental leaks. Skipped entries (idempotency hits) often carry real-issue URLs from prior posts — keeping them out of `posted.json` preserves the audit invariant.

---

## Eval Mode (`--eval` argument)

When the skill is invoked with `args="--batch --eval"`, Phase 5 substitutes `gh issue create` with a mock that:
- Returns a deterministic mock URL: `https://example.invalid/issue/<n>` where `<n>` is a SHA-256-hash-derived issue number (reproducible across runs for the same `recommendation_id`)
- Writes the mock-posting record to `tmp/eval-mock/posted.json` (a single JSON file with stable schema — see "Posted-mock schema" below)
- Routes idempotency-skip diagnostics to `tmp/eval-mock/skipped.json` (SEPARATE from posted.json — see "Skip routing" below)
- Does NOT invoke the real `gh` CLI (no network call, no real issue)

**Why this matters:** The full skill-creator eval/iteration loop spawns subagents that run this skill end-to-end. Without a mock mode, those evals would post real issues to `bankielewicz/DevForgeAI`. The user has parallel Claude sessions in OTHER repos (e.g., `nexu-io/open-design`); test runs must never accidentally interact with any GitHub repo. The `--eval` flag is the safety harness.

### Posted-mock schema (stable — every entry has every field, even null)

The `posted.json` file is a single JSON object with a top-level metadata block AND an always-present `posted` array. Stable schema across all runs (no field renames, no omit-when-empty):

```json
{
  "mode": "MOCKED",
  "repo": "bankielewicz/DevForgeAI",
  "note": "Eval mock posts — no real GitHub interaction. .invalid TLD is RFC-2606-reserved.",
  "generated_at": "<iso UTC>",
  "posted": [
    {
      "recommendation_id": "REC-STORY-661-M-001",
      "issue_number": 47312,
      "issue_url": "https://example.invalid/issue/47312",
      "title": "Replace sys.exit(1) with return 1 for consistent CLI exit-code contract",
      "labels": ["severity:medium", "category:anti_pattern", "classification:regression", "origin:qa-recommendation", "provenance:grounded", "effort:small"],
      "draft_path": "tmp/STORY-661/drafts/draft-REC-STORY-661-M-001.md",
      "ts": "2026-05-08T19:42:11Z",
      "status": "success",
      "error_message": null,
      "mock": true,
      "severity": "MEDIUM",
      "category": "anti_pattern",
      "provenance": "GROUNDED",
      "blocking_release": false
    }
  ],
  "skipped": []
}
```

**Field rules:**
- **`recommendation_id`** — verbose form (matches QA-recs schema field names). NEVER abbreviate to `rec_id`.
- **`labels`** — array of strings, NOT comma-string. EVERY label uses `key:value` namespacing (no bare tokens). Standard set: `severity:{lower}`, `category:{cat}`, `origin:qa-recommendation`, `provenance:{lower}`, `effort:small|medium|large`. Classification triage: `classification:regression` or `classification:pre-existing` (iteration-3 namespacing — was bare `regression` / `pre-existing` before). Blocking flag: `release:blocking` (iteration-3 — was bare `blocking-release`). Bare tokens are forbidden because they collide with org-level labels of the same name on other repos.
- **`draft_path`** — ALWAYS rooted at `tmp/${STORY_ID}/drafts/...` per operational-safety.md Rule 2. NEVER use the workspace-specific path (e.g., `src/claude/skills/.../iteration-1/...`). The draft_path field's job is to point a downstream consumer to the production draft location.
- **`error_message`** — `null` when `status == "success"`, populated string otherwise. ALWAYS present (don't omit when empty).
- **`mock`** — `true` always when this file is the eval-mock posted log. Allows downstream parsers to distinguish without checking the URL.
- **`status`** — one of `success | failed | skipped | cancelled`. (Skipped recs never appear here; they go to skipped.json. But the field is preserved for schema stability.)
- **`severity`/`category`/`provenance`/`blocking_release`** — copied from input rec for downstream filtering without label-string-splitting.
- **Top-level `posted`/`skipped` arrays** — ALWAYS emitted (use `[]` for empty). Downstream consumers can rely on key presence.

### Skip routing (separate file)

When idempotency check (Phase 1.5) detects an already-linked rec, the skill writes a structured skip record to `tmp/eval-mock/skipped.json` (in --eval) or `tmp/${STORY_ID}/skipped.json` (in REAL):

```json
{
  "mode": "MOCKED",
  "repo": "bankielewicz/DevForgeAI",
  "skipped": [
    {
      "recommendation_id": "REC-STORY-660-L-001",
      "reason": "already_posted",
      "existing_marker": "**Posted as:** Issue-42",
      "existing_issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
      "detected_in_phase": "idempotency_check",
      "ts": "<iso>"
    }
  ]
}
```

**Why a separate file:** Skip records often carry pre-existing real-issue URLs (e.g., Issue-42's full github.com URL). Putting them in `posted.json` would defeat the audit invariant `grep -E "github\\.com" posted.json → empty`. Routing skips to their own file lets a downstream auditor enforce different policies per file.

### Linking markers (qa-recs-update.md)

Idempotency markers in the QA recs file use `Issue-mock-<n>` (eval mode) or `Issue-<n>` (real mode). The `mock-` prefix is the only fast textual signal a downstream tool has to tell "this rec was posted in eval mode" vs "real". Don't drop the prefix in --eval mode.

### Deterministic issue numbers

Mock issue numbers are SHA-256-hash-derived from the recommendation_id, NOT timestamp or random. Algorithm:

```python
import hashlib
issue_number = int(hashlib.sha256(rec_id.encode("utf-8")).hexdigest()[:7], 16) % 100000
# Reproducible: same rec_id always yields the same issue_number across runs.
```

Why hash-derived rather than monotonic-from-base: sequence-from-fixture-state requires reading the QA recs file's existing `Issue-N` markers and starting at max+1, which is more state-dependent and harder to reproduce in isolated subagent contexts. Hash-derivation is purely a function of input → output, perfect for eval reproducibility.

---

## Phase 1 — Setup

**Goal:** Validate inputs, confirm `gh` is authenticated (skipped in `--eval` mode), load the template, detect prior runs.

### 1.1 Validate inputs

Read `selected_recommendations` from caller context. For each element, confirm these required fields are non-empty:
- `id` (matches `^REC-STORY-\d+-[CHML]-\d{3}$`)
- `severity` (one of CRITICAL, HIGH, MEDIUM, LOW)
- `title` (non-empty string)
- `file` (non-empty path)
- `line` OR `line_range` (at least one — the generator now fail-fast validates this; trust the input)
- `category` (one of correctness, security, performance, test_quality, coverage, anti_pattern, documentation)
- `verification.command` AND `verification.expected` (both non-empty)

For category=anti_pattern, also confirm `classification` is one of REGRESSION or PRE_EXISTING (the generator validates this; trust but verify here too).

If any element fails validation, HALT with:
```
ERROR: Invalid recommendation in batch input: <details>
       This is an upstream contract violation — the qa_recommendations_generator
       should fail-fast on this. Re-run /qa to regenerate the QA recs file.
```

### 1.2 Confirm `gh` authentication (SKIPPED in --eval mode)

If `--eval` is set, skip 1.2 and 1.3. Otherwise:

```bash
gh auth status
```

| Exit code | Action |
|-----------|--------|
| 0 (authenticated) | Continue to 1.3 |
| Non-zero (not authenticated) | HALT. Emit: "gh CLI not authenticated. Run `gh auth login` and re-invoke `/create-incident-from-recommendations`." Return all-failed results. |
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

### 1.5 Idempotency check (BR-009 + skipped.json routing)

Idempotency has two evidence sources, checked in order:

**Source A (primary, post-fix): the posting manifest.** `/create-incident-from-recommendations` Phase 11 writes `tmp/${STORY_ID}/posting-manifest.json` after each successful posting run. This is the canonical durable link-back record — the QA recs file is never mutated by Phase 11 (the original Edit-based design was silently blocked by `feedback-artifact-write-gate.sh` ADR-062 D2 during active workflows).

**Source B (legacy fallback): inline `**Posted as:** Issue-N` markers in the QA recs file.** Stories posted before the manifest fix landed may carry the original inline markers. Phase 1.5 still detects those for backward compatibility.

```
manifest_path = f"tmp/{STORY_ID}/posting-manifest.json"
manifest_linked_rec_ids = set()
IF file_exists(manifest_path):
    manifest = json.parse(Read(file_path=manifest_path))
    manifest_linked_rec_ids = { link["rec_id"] for link in manifest.get("links", []) }

# Legacy fallback: grep the QA recs file for inline markers
Read(file_path="${QA_RECS_FILE}")
legacy_linked_rec_ids = set()
FOR rec in selected_recommendations:
    real_pattern = f"{rec.id}.*Issue-\\d+"
    mock_pattern = f"{rec.id}.*Issue-mock-\\d+"
    IF Grep(pattern=real_pattern + "|" + mock_pattern, path="${QA_RECS_FILE}") found:
        legacy_linked_rec_ids.add(rec.id)

already_linked_rec_ids = manifest_linked_rec_ids | legacy_linked_rec_ids
already_linked_recs = [rec for rec in selected_recommendations if rec.id in already_linked_rec_ids]
```

If any recs are already linked, present them via `AskUserQuestion`:

- "Re-post anyway (creates duplicates) — proceed with all selected"
- "Skip already-linked (Recommended)"
- "Cancel — let me reconcile manually"

In `--eval` mode, default to "Skip already-linked" (deterministic behavior for evals).

**Skip routing (BR-009 + BR-011):** When the user picks "Skip already-linked" (or it defaults in --eval), the skipped recs do NOT enter `posted.json`. Instead, write structured skip records to a SEPARATE file:

```python
skipped_envelope = {
    "mode": "MOCKED" if EVAL_MODE else "REAL",
    "repo": "bankielewicz/DevForgeAI",
    "skipped": []
}
for rec in already_linked_recs:
    # Source preference: manifest first (post-fix), legacy marker as fallback.
    IF rec["id"] in manifest_linked_rec_ids:
        manifest_entry = next(l for l in manifest["links"] if l["rec_id"] == rec["id"])
        existing_marker = f"manifest:posting-manifest.json#{manifest_entry['issue_number']}"
        existing_issue_url = manifest_entry["issue_url"]
        source = "posting-manifest"
    ELSE:
        # Legacy inline marker in QA recs file
        existing_marker = <full match line, e.g., "**Posted as:** Issue-42 — https://...">
        existing_issue_url = <URL extracted from marker>
        source = "qa-recs-inline-marker"

    skip_record = {
        "recommendation_id": rec["id"],
        "reason": "already_posted",
        "existing_marker": existing_marker,
        "existing_issue_url": existing_issue_url,
        "evidence_source": source,
        "detected_in_phase": "idempotency_check",
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    skipped_envelope["skipped"].append(skip_record)

skipped_path = "tmp/eval-mock/skipped.json" if EVAL_MODE else f"tmp/{story_id}/skipped.json"
Path(skipped_path).write_text(json.dumps(skipped_envelope, indent=2))
```

**Why a separate file:** Skip records often carry pre-existing real-issue URLs (e.g., the `https://github.com/bankielewicz/DevForgeAI/issues/42` URL embedded in the existing `**Posted as:** Issue-42` marker). If those URLs landed in `posted.json`, a downstream auditor running `grep -E "github\\.com" posted.json` (the canonical "did we leak a real URL?" check) would fail, even though the skill did everything right. Routing skips to their own file lets the audit invariant hold without losing diagnostic context.

**The selected_recommendations array passed to Phase 2** now excludes the skipped recs (it's filtered down to only recs the user approved for posting).

### 1.5.5 Remote duplicate check (ISSUE-797)

Before drafting, record a **remote duplicate scan** so the `pre-gh-incident-template-guard`
hook can verify the step ran and block `gh issue create` if the scan was skipped.

```bash
devforgeai-validate dup-scan ${STORY_ID} --query "<3-5 keywords from the recommendation>" --project-root=.
```

Read `tmp/${STORY_ID}/dup-scan.json` for the results list. If any result matches the same
defect/enhancement surface it in the approval loop BEFORE Phase 2:

```
AskUserQuestion →
    question: "Possible remote duplicate: #${number} '${title}' (${state}, ${url}). Proceed?"
    options:  ["Skip — record as duplicate (recommended)", "File anyway", "Cancel"]
```

Then record the human disposition so the hook gate can pass:

```bash
# on Skip:
devforgeai-validate dup-scan ${STORY_ID} --disposition "skipped-duplicate:#${number}" --project-root=.
# on File anyway:
devforgeai-validate dup-scan ${STORY_ID} --disposition "filed-anyway:user-confirmed" --project-root=.
# on no match found:
devforgeai-validate dup-scan ${STORY_ID} --disposition "no-match" --project-root=.
# on Cancel: return without proceeding to Phase 2
```

In `--eval` mode, skip the gh network scan and write disposition deterministically:
`devforgeai-validate dup-scan ${STORY_ID} --disposition "no-match" --project-root=.`
The remote scan is mandatory in REAL mode. **Batch-level design:** one scan per batch (keyed on `STORY_ID`) is by design — the hook passes for all recs in this batch once the batch-level `dup-scan.json` is recorded.

### 1.6 Create the drafts directory

```bash
mkdir -p tmp/${STORY_ID}/drafts/
# In --eval mode, also create the mock dir:
[ -n "${EVAL_MODE}" ] && mkdir -p tmp/eval-mock/
```

---

## Phase 2 — Drafting

**Goal:** For each selected recommendation, produce a complete GitHub issue draft in markdown. QA recs are pre-structured, so most fields map directly to issue template sections without inference.

### 2.1 Direct field mapping (the QA-recs advantage)

For each `rec` in `selected_recommendations`:

| QA rec field | → | Issue body section |
|--------------|---|-------------------|
| `title` | → | `# <Title>` (verify imperative + ≤80 chars; rewrite if needed per template line 22) |
| `file` + `line` (or `line_range`) | → | `## Files to change` (e.g., `- src/foo.py:42 — fix off-by-one`) |
| `before_code` (when present) | → | `## Current behavior` (with code block) |
| `after_code` (when present) | → | `## Required behavior` (with code block) |
| `remediation_steps` (alt path) | → | `## Acceptance criteria` (each step → checklist item) |
| `verification.command` + `verification.expected` | → | `## Test plan` (verbatim command + expected output) |
| `dependencies` (REC-IDs) | → | `## Dependencies` (e.g., "Depends on REC-STORY-661-M-002") |
| `references` | → | `## References` footer (URLs, source citations) |

### 2.2 Label assembly (array form, full namespacing)

Labels are emitted as a **JSON array** of strings (not a comma-separated string). Every applicable label uses `key:value` namespacing for consistent triage. Per BR-001 and BR-010:

```python
labels = [
    f"severity:{rec.severity.lower()}",        # severity:critical | severity:high | severity:medium | severity:low
    f"category:{rec.category}",                # category:correctness | category:security | category:anti_pattern | etc.
    f"provenance:{rec.provenance.lower()}",    # provenance:grounded | provenance:derived | provenance:inconclusive
    "origin:qa-recommendation",                # origin marker — distinguishes from manually-filed issues
]

# Effort tier — derived from estimated_effort_minutes
em = rec.get("estimated_effort_minutes", 0)
if em <= 30:
    labels.append("effort:small")
elif em <= 120:
    labels.append("effort:medium")
else:
    labels.append("effort:large")

# Classification → namespaced label (consistent with all other namespaced labels above).
# Iteration-3 fix: previously the bare forms `regression` / `pre-existing` were used, which
# diverged from the namespaced convention used by every other label. Bare tokens are also
# more likely to collide with org-level labels of the same name on other repos. Always
# emit the `classification:` namespace prefix so a single grep over the labels array
# produces a clean classification axis.
if rec.classification == "REGRESSION":
    labels.append("classification:regression")
elif rec.classification == "PRE_EXISTING":
    labels.append("classification:pre-existing")

# Blocking release — presence-as-signal, namespaced for consistency
if rec.blocking_release:
    labels.append("release:blocking")
```

**Before assuming a label exists on the repo** (REAL mode only), run `gh label list -R bankielewicz/DevForgeAI` ONCE per skill invocation and cache the result. Drop any label not on the repo and append an Open Question per affected draft: "Label '<X>' not on repo. Create with `gh label create '<X>'` or remove?"

**In `--eval` mode**, skip the `gh label list` call and emit ALL inferred labels (the eval grades drafting, not label-existence handshaking; missing labels would cause spurious Open Questions that pollute the eval signal).

### 2.2a Title rules (no prefix)

Issue titles are **verb-first imperative, ≤80 chars, no prefix**. Severity is surfaced via the `severity:*` label, not the title — modern GitHub workflows rely on labels for triage, and prefixes consume ~7 chars of the title budget without adding info that labels don't already carry.

| RIGHT | WRONG |
|-------|-------|
| `Replace sys.exit(1) with return 1 for CLI exit-code contract` | `[QA-MEDIUM] Replace sys.exit(1) with return 1` |
| `Guard Windows fcntl WARNING behind once-per-session flag` | `[QA-LOW]: fcntl warning fix` |

### 2.3 Per-draft Acceptance Criteria construction

If `before_code` + `after_code` are present:
- Phase 2 derives ACs from the verification: `[ ] Run \`${verification.command}\` and observe \`${verification.expected}\``
- Add 1-2 ACs from the diff if obvious (e.g., "Function X returns Y instead of Z")

If `remediation_steps` are present (alt path):
- Each step becomes an AC: `[ ] ${step}`

Open Questions are reserved for genuinely uninferable scope — and with QA recs that's rare. Most drafts will have an empty Open Questions list. Don't manufacture them.

### 2.4 Write each draft to disk (with mandatory `## Labels` body section)

The draft body MUST contain ALL 10 sections from the embedded template, in this exact order:

1. `# <Title>` (imperative, ≤80 chars, no prefix)
2. `## Context`
3. `## Current behavior`
4. `## Required behavior`
5. `## Files to change`
6. `## Acceptance criteria`
7. `## Test plan`
8. `## Out of scope`
9. `## Dependencies`
10. `## Labels` ← **MANDATORY — emit unconditionally** (iteration-3 enforcement)

The `## Labels` body section is mandatory even when the labels also appear in `posted-mock.json`. Two reasons:
1. **Template fidelity** — the embedded `Github-incident-template.md` (line 53) explicitly specifies a `## Labels` section. Skipping it violates the template contract.
2. **Audit trail** — humans reading the issue body shouldn't have to cross-reference the JSON file to see the triage labels. The body is the human-readable artifact.

**Format and order of body labels:**
- Comma-separated string (NOT a YAML/JSON array — that's how GitHub renders the section in markdown)
- **Order MUST match the JSON `labels[]` array exactly.** No re-sorting. The skill builds the array once in Phase 2.2, then serializes that same array for both the JSON entry's `labels` field AND the body's `## Labels` section. A simple `", ".join(labels_array)` does both.
- No leading/trailing whitespace. No bullet points. Just `key:value, key:value, key:value` on a single line under the `## Labels` heading.

```
Write(file_path="tmp/${STORY_ID}/drafts/draft-${rec.id}.md",
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
{out_of_scope_list}

## Dependencies
{dependencies_text}

## Labels
{', '.join(labels_array)}
""")
```

If a draft has any open questions (rare), also:

```
Write(file_path="tmp/${STORY_ID}/drafts/open-questions-${rec.id}.md",
      content="<list of unresolved questions>")
```

### 2.5 Per-draft validation gate

Before recording a draft as ready, verify:

- [ ] Title is ≤80 chars, imperative verb-first, no prohibited language (per template line 59)
- [ ] All 10 template body sections populated (Context, Current behavior, Required behavior, Files to change, Acceptance criteria, Test plan, Out of scope, Dependencies, **Labels**)
- [ ] **`## Labels` section is present and non-empty** (iteration-3 enforcement — was the most common omission)
- [ ] **Body `## Labels` line matches `", ".join(labels_array)` exactly** — same order, same content as the JSON `labels[]` field. No re-sorting between the two emission sites.
- [ ] Files to change contains at least one `path:line` reference
- [ ] At least 1 acceptance criterion in the checklist
- [ ] Test plan command non-empty
- [ ] No bare `regression` or `pre-existing` token in any label slot — both must be `classification:regression` / `classification:pre-existing` (iteration-3 namespacing fix)

If any check fails, append to Open Questions. Never silently drop validation failures.

---

## Phase 3 — Summary Preview

**Goal:** Show a compact, scrollable overview before approval.

### 3.1 Emit summary table

Markdown table — 5 columns (severity column added vs RCA path):

```
| #  | REC ID                  | Severity | Title                                | Labels                            | Open-Qs |
|----|-------------------------|----------|--------------------------------------|-----------------------------------|---------|
| 1  | REC-STORY-661-M-001     | MEDIUM   | Replace sys.exit(1) with return 1    | severity:medium, classification:r…| 0       |
| 2  | REC-STORY-661-M-002     | MEDIUM   | Silence Windows fcntl WARNING noise  | severity:medium, classification:p…| 0       |
```

Columns:
- `#` — sequential index in the batch
- `REC ID` — full ID
- `Severity` — CRITICAL/HIGH/MEDIUM/LOW
- `Title` — truncated to 36 chars
- `Labels` — truncated to 35 chars
- `Open-Qs` — count of bullets in `tmp/${STORY_ID}/drafts/open-questions-${rec.id}.md`. `0` if file doesn't exist.

### 3.2 Aggregate signals

After the table, emit per-category lines as applicable:
- `⚠ N drafts have unresolved Open Questions — inspect before posting.`
- `ℹ M drafts share severity:critical — these will likely get triage attention.`
- `ℹ Drafts saved to tmp/${STORY_ID}/drafts/ for inspection.`

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

In `--eval` mode for evals that don't drive interactive prompts, default to "Post all" deterministically.

---

## Phase 5 — Post

**Goal:** Run `gh issue create` for each approved draft. Continue on per-issue failure.

### 5.1 Per-rec post invocation (REAL mode)

When `--eval` is NOT set, run the real `gh issue create` and capture the response into the stable-schema posted.json envelope:

```python
import subprocess
from datetime import datetime, timezone

# At skill start, build the envelope (REAL mode):
posted_envelope = {
    "mode": "REAL",
    "repo": "bankielewicz/DevForgeAI",
    "note": "Real GitHub issues posted via gh issue create.",
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "posted": [],
    "skipped": []
}

# Per-rec:
for rec in to_post:
    title       = <rewritten imperative title — Phase 2.1, NO prefix>
    body_file   = f"tmp/{story_id}/drafts/draft-{rec['id']}.md"
    labels_arr  = <array from Phase 2.2 — namespaced strings>

    Display: f"[{index+1}/{len(to_post)}] Posting: {rec['id']} — {title}"

    # ── Recurrence check (Issue #934) — MANDATORY before this rec's post ──
    # pre-gh-incident-template-guard Step 9 create-gate blocks gh issue create
    # unless a fresh recurrence-check artifact exists for the exact draft body
    # (keyed by the same bytes). It also detects an exact recurrence of an OPEN
    # issue so a +1 is recorded as a comment instead of filing a duplicate.
    # Provenance-only gate — it does NOT verify the OccurrenceInput is truthful.
    occurrence_file = f"tmp/{story_id}/drafts/occurrence-{rec['id']}.json"
    # Write occurrence_file = OccurrenceInput JSON with the 12 fields the check
    # validates: source_kind, source_id, kind, provenance, title, description,
    # affected_files, evidence_refs, category, severity_or_priority,
    # producer_record_id, repo_identity. Set source_kind="qa-recommendation",
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
    #   Record +1 comment → write tmp/{story_id}/drafts/recurrence-comment-{rec['id']}.md
    #     = a "<!-- recurrence -->" marker line then exactly ONE line
    #     "repo_identity | fingerprint | run_id"
    #     (repo_identity=bankielewicz/DevForgeAI, fingerprint=<artifact fingerprint>, run_id=rec['id']);
    #     mint the comment artifact and post the comment, then continue (skip gh issue create):
    #       devforgeai-validate incident-recurrence check --occurrence {occurrence_file} --body-file <comment> --verb comment --project-root=.
    #       gh issue comment {matched_issue_number} --repo bankielewicz/DevForgeAI --body-file <comment>
    #     append _build_entry(..., status="recurrence-recorded"); continue
    #   File new anyway → fall through to gh issue create (the --verb create artifact satisfies Step 9).
    #   Cancel → append _build_entry(..., status="cancelled"); continue

    # gh CLI accepts comma-separated --label; we serialize the array at the boundary.
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

(`_build_entry` returns the same stable-schema dict shape used in --eval mode — see Posted-mock schema in the Eval Mode section. The on-disk schema is identical except `mock: false` and the URL is real.)

**CRITICAL — Cross-repo guard (BR-007):** `--repo bankielewicz/DevForgeAI` is hardcoded in EVERY invocation. The user has parallel Claude sessions in other repositories (e.g., `nexu-io/open-design`); without the explicit `--repo`, gh would default to the current directory's git remote, which could be ANY repo. The flag is non-negotiable and verified by the slash command's static smoke test:

```bash
grep -nE "gh issue create" SKILL.md | grep -v -- "--repo bankielewicz/DevForgeAI"
# (must return empty — every gh issue create line must have the --repo flag)
```

### 5.2 Per-rec post invocation (--eval mode)

When `--eval` is set, substitute the gh command with a deterministic mock that writes to the **stable-schema posted.json** (single JSON file with top-level metadata + always-present arrays):

```python
import hashlib
from datetime import datetime, timezone

# At skill invocation start, build the posted.json envelope once:
posted_envelope = {
    "mode": "MOCKED",
    "repo": "bankielewicz/DevForgeAI",
    "note": "Eval mock posts — no real GitHub interaction. .invalid TLD is RFC-2606-reserved.",
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "posted": [],
    "skipped": []  # populated separately if Phase 1.5 detects already-linked recs
}

# Per-rec, in Phase 5:
for rec in to_post:
    # Deterministic issue number — hash of recommendation_id, NOT timestamp.
    issue_number = int(hashlib.sha256(rec["id"].encode("utf-8")).hexdigest()[:7], 16) % 100000
    issue_url = f"https://example.invalid/issue/{issue_number}"

    # draft_path is project-relative per Rule 2 — never workspace-specific
    draft_path = f"tmp/{story_id}/drafts/draft-{rec['id']}.md"

    entry = {
        "recommendation_id": rec["id"],          # verbose form
        "issue_number": issue_number,
        "issue_url": issue_url,
        "title": title,                          # post-rewrite imperative title (no prefix)
        "labels": labels_array,                  # array, namespaced per Phase 2.2
        "draft_path": draft_path,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "success",
        "error_message": None,                   # always present
        "mock": True,
        "severity": rec["severity"],             # for downstream filtering
        "category": rec["category"],
        "provenance": rec["provenance"],
        "blocking_release": rec.get("blocking_release", False),
    }
    posted_envelope["posted"].append(entry)
    Display: f"  ✓ MOCK posted: Issue-mock-{issue_number} — {issue_url}"

# At end of Phase 5, write the envelope as a single JSON object (NOT JSONL):
Path("tmp/eval-mock/posted.json").write_text(json.dumps(posted_envelope, indent=2))
```

**Key invariants:**
- The mock NEVER invokes `gh`. The audit trace `tmp/eval-mock/posted.json` is the ground truth.
- `posted.json` is a SINGLE JSON object with top-level metadata + arrays — NOT JSONL. This stable schema is parseable by any JSON consumer with one `json.load()`.
- `posted` is always emitted (use `[]` for empty). Same for `skipped`.
- `error_message` is always present (use `null` for success). Same shape regardless of status.
- `recommendation_id` is verbose (NOT abbreviated to `rec_id`) for schema-match with the QA recs YAML.
- Issue numbers are reproducible: re-running on the same rec_id yields the same number.

### 5.3 Per-failure error templates (REAL mode)

When `gh` returns non-zero, common causes:

| stderr signature | Likely cause | Surface to user |
|-----------------|--------------|-----------------|
| `could not add label: 'X' not found` | Label missing | `Run gh label create '${X}' and re-run for the failed REC.` |
| `HTTP 401` / `Bad credentials` | Token expired | `Run gh auth refresh and re-run for failed RECs.` |
| `HTTP 403` / `rate limit exceeded` | Rate-limited | `Wait ${reset_minutes}m, re-run for failed RECs.` |
| `HTTP 422` / `validation failed` | Body too long, bad label | `Inspect tmp/${STORY_ID}/drafts/draft-${rec.id}.md and fix.` |
| Network error / timeout | Transient | `Retry after a moment.` |

Do NOT auto-retry. Surface and let user re-invoke.

---

## Phase 6 — Result

**Goal:** Print final summary and return result list.

### 6.1 Final summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GitHub Incident Creation Summary — ${STORY_ID} ${EVAL_MODE_BANNER}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Posted:   ${success_count}
   • REC-NNN → Issue-NNN — <URL>
   • ...

❌ Failed:   ${failure_count}
   • REC-NNN: ${error_message}

⏭ Skipped:  ${skip_count}
   • REC-NNN: user excluded from subset

Drafts available at: tmp/${STORY_ID}/drafts/
${EVAL_MOCK_NOTE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

`${EVAL_MODE_BANNER}` is `"(EVAL MOCK)"` when `--eval` is set, else empty.
`${EVAL_MOCK_NOTE}` is `"Mock posts logged to tmp/eval-mock/posted.json"` when `--eval`, else empty.

### 6.2 Return value

Return `results` array to caller. The slash command's Phase 11 linking workflow consumes this — only success entries trigger QA-recs file updates with `Issue-NNN` (real) or `Issue-mock-NNN` (eval) references.

---

## Business Rules (locked)

| Rule | Implementation |
|------|----------------|
| BR-001: Label assembly (array, namespaced) | Labels are an ARRAY of strings (not comma-separated). Always include: `severity:{lower}`, `category:{cat}`, `provenance:{lower}`, `origin:qa-recommendation`, `effort:small\|medium\|large` (derived from estimated_effort_minutes). Drop labels not on repo (REAL mode); Open Question per draft. |
| BR-002: Title quality (no prefix) | Imperative verb-first, ≤80 chars, no prohibited language (template line 59). NO `[QA-{SEV}]` prefix — severity is surfaced via `severity:*` label. Modern label-based triage; preserves character budget. |
| BR-003: Files-to-change honesty | QA recs CARRY `file` + `line`/`line_range` (post-fidelity-fix, generator fail-fast validates). Phase 2 maps these directly. |
| BR-004: Failure isolation | A `gh issue create` failure on rec N does NOT block posting of rec N+1. |
| BR-005: Approval required | NO `gh issue create` (real or mock) before Phase 4 user approval (or default-Post-all in `--eval` mode). |
| BR-006: No system /tmp use | Drafts go to `tmp/${STORY_ID}/drafts/` per project root. The `draft_path` field in posted-mock entries ALWAYS uses this project-relative path — never the eval-workspace-specific path. |
| BR-007: Hardcoded repo + cross-repo guard | `bankielewicz/DevForgeAI` locked. EVERY `gh issue create` line has `--repo bankielewicz/DevForgeAI`. |
| BR-008: Drafts persist | Do not auto-delete drafts. Re-runs use them via idempotency check. |
| BR-009: Idempotency awareness | Phase 1.5 detects already-linked recs via two evidence sources, in order: (A) **primary** — `tmp/${STORY_ID}/posting-manifest.json` written by `/create-incident-from-recommendations` Phase 11 (the post-PR-#81 link-back artifact); (B) **legacy fallback** — inline `**Posted as:** Issue-N` / `Issue-mock-N` markers grep'd from `${QA_RECS_FILE}` for stories posted before PR #81 landed. The skill asks the user how to handle the union of both sources. Skip records routed to a SEPARATE file (`skipped.json`), NEVER mixed into `posted.json`. The QA recs file is never mutated by this skill or by Phase 11 (sidesteps `feedback-artifact-write-gate.sh` ADR-062 D2). |
| BR-010: Classification → namespaced label (any category) | REGRESSION → `classification:regression`, PRE_EXISTING → `classification:pre-existing`. **Always namespaced** (iteration-3) — bare tokens are forbidden because they collide with org-level labels. Allowed on ANY category (iteration-2 broadening). None when classification absent. |
| BR-015: `## Labels` body section is mandatory | Every draft body MUST end with a `## Labels` section containing the comma-joined label array. Order MUST match the JSON `labels[]` field exactly (single source of truth, two emission sites — body markdown + JSON). Iteration-3 enforcement after iter-1/iter-2 drafts inconsistently omitted it. |
| BR-011: Stable posted-mock schema | `posted.json` is a SINGLE JSON object with top-level `mode`/`repo`/`note`/`generated_at` + always-present `posted: []` + `skipped: []` arrays. Every entry has every field (use `null` for empty values). Field name `recommendation_id` (verbose) — never abbreviated to `rec_id`. |
| BR-012: Deterministic issue numbers | Mock issue numbers are `int(sha256(rec_id)[:7], 16) % 100000` — reproducible across runs. Same `recommendation_id` always yields the same number. NO `time.time()` or `random` derivations. |
| BR-013: Always preserve section structure | Output qa-recs-update.md ALWAYS preserves all canonical sections (`## Blocking Recommendations`, `## Advisory Recommendations`, `## Deferred Recommendations`) even when empty. Empty sections get `_None._` body — never the section header alone, never an omitted section. |
| BR-014: Audit trail in qa-recs-update.md | Each posting cycle adds: (a) `last_posted_at: <iso>` to frontmatter (next to `generated_at`), (b) a `## Posting Audit Trail` section with a per-cycle table of `\| REC ID \| Severity \| Action \| Issue / URL \|`. Append-only across cycles. |

---

## Edge Cases

| Edge case | Behavior |
|-----------|----------|
| `selected_recommendations` empty | Return empty results. Emit: "No recommendations to process." |
| `gh` not authenticated (REAL mode) | HALT in Phase 1.2. All-failed results with auth error. |
| `gh` not installed (REAL mode) | HALT in Phase 1.2. Install instructions. |
| Repo unreachable (REAL mode) | HALT in Phase 1.3. |
| All recs already linked (BR-009) | Phase 1.5 prompt. Default skip in --eval. |
| `tmp/${STORY_ID}/posting-manifest.json` malformed or unreadable | Phase 1.5 falls back to the legacy inline-marker grep on `${QA_RECS_FILE}` only. Surface as: "⚠ posting-manifest.json read failed: ${error}. Falling back to inline-marker idempotency only — recs posted via PR #81's manifest pattern may not be detected as already-linked; re-runs may duplicate. Manual fix: delete the corrupt manifest and re-run." Does not HALT. |
| All drafts have open questions | Proceed to Phase 3 summary. Phase 4 lets user cancel. |
| Mid-batch network failure (REAL) | Successes recorded; failures recorded per-rec. User re-runs for failures. |
| `gh label list` call fails | Cache empty list. Drop inferred labels; one Open Q per draft. |
| Issue body exceeds 64KB (REAL) | HTTP 422. User trims rec.before_code/after_code, re-runs. |
| User cancels in Phase 4.3 mid-inspection | Treat as "Cancel" — all recs `status: "cancelled"`. |
| `--eval` mode (mock posts) | No `gh` calls. `tmp/eval-mock/posted.json` records mocks. Idempotency markers use `Issue-mock-N`. |

---

## Integration

| Aspect | Value |
|--------|-------|
| **Invoked by** | `/create-incident-from-recommendations` slash command (Phase 10) |
| **Invokes** | `gh` CLI via Bash (REAL mode only); `AskUserQuestion`; `Read`/`Write`/`Grep`/`Glob` for file ops; embedded `assets/templates/Github-incident-template.md` |
| **Reads** | `tmp/${STORY_ID}/posting-manifest.json` (Phase 1.5 idempotency — **primary**, post-PR-#81), `${QA_RECS_FILE}` (legacy inline `**Posted as:**` marker fallback for stories posted pre-PR-#81), `${TEMPLATE_PATH}` (drafting prompt) |
| **Writes** | `tmp/${STORY_ID}/drafts/draft-${REC_ID}.md`, `tmp/${STORY_ID}/drafts/open-questions-${REC_ID}.md` (when present), `tmp/${STORY_ID}/posted.json` (REAL) OR `tmp/eval-mock/posted.json` (--eval), `tmp/${STORY_ID}/skipped.json` (when idempotency-skips occur). **Does NOT write to `${QA_RECS_FILE}`** — that path is gated by `feedback-artifact-write-gate.sh` (ADR-062 D2); the cross-run link-back lives in `tmp/${STORY_ID}/posting-manifest.json` written by `/create-incident-from-recommendations` Phase 11, not by this skill. |
| **Posts** | GitHub issues to `bankielewicz/DevForgeAI` (REAL mode) |
| **Returns** | Result array to caller |

---

## Naming Note (intentional deviation from ADR-017)

ADR-017 prescribes the `spec-driven-*` prefix for skills. This skill's name `github-incident-from-recommendations` is a deliberate, user-confirmed deviation matching the sibling `github-incident-from-rca`: the skill is tightly coupled to the GitHub provider and to the QA-recs source artifact, not a generalized cross-cutting framework concern. A future framework analysis pass may consolidate both (and the RCA sibling) under a single `spec-driven-incidents` umbrella.

---

**Version:** 1.0 | **Created:** 2026-05-08 | **Pattern:** Skill owns external-side-effect logic; slash command orchestrates only.
