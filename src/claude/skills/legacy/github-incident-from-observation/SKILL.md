---
name: github-incident-from-observation
description: Draft and post a single GitHub issue to bankielewicz/DevForgeAI from an inline spontaneous observation — a bug or enhancement discovered live during active work, with no upstream source document. Owns drafting, summary preview, drill-down approval flow, and posting. Consumes the embedded Github-incident-template.md as the issue-body schema and AI prompt. Use this skill whenever the user runs /create-incident, asks to "file a bug from something I just noticed", asks to "create an incident from this observation", wants to turn a spontaneous finding into a GitHub work-order, or an agent finds a framework defect live and needs to file it through the template pipeline. The skill is the only place in the framework that calls `gh issue create` for observation-derived work — slash commands and other skills MUST delegate here rather than calling gh directly.
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(gh:*), AskUserQuestion
---

# github-incident-from-observation — Skill Definition

This skill converts a single **inline observation** (a free-text description of a bug or
enhancement the user or an agent discovered live during active work) into one GitHub issue
posted to `bankielewicz/DevForgeAI`. It owns drafting, preview, approval, and posting. The
slash command `/create-incident` delegates here for any work that touches `gh issue create`.

**The on-ramp it fills.** The other four incident pathways are all source-document-driven —
`github-incident-from-rca` (an RCA doc), `github-incident-from-recommendations` (a QA-recs
file), `github-incident-from-feedback` (an ai-analysis JSON), and `create-incident-from-queue`
(an aggregated queue JSON). A bug or enhancement found **while working** has no such source,
so before this skill existed there was no pathway to invoke — forcing a freehand
`gh issue create` that bypassed the template (this happened with #399). This skill is the
inline-description on-ramp into the same template + preview-approval pipeline.

**Sibling skills:** `github-incident-from-rca`, `github-incident-from-recommendations`,
`github-incident-from-feedback`. Same posting pipeline, different input shape — those consume
a structured upstream artifact; this consumes a single free-text `observation_text` string.
Drafting therefore synthesizes every issue-body section from the one description rather than
mapping pre-structured fields.

**Embedded asset (the AI prompt that defines the issue body schema, quality bar, prohibited
language, and DevForgeAI house rules):**
- `assets/templates/Github-incident-template.md` — read this in Phase 1; it is the
  authoritative drafting prompt. Byte-identical to the three sibling skills' templates (a
  framework-wide invariant, not source-specific).

**Why a separate skill instead of inline command logic?** GitHub-issue creation has
irreversible side effects (issues leave audit trails on the public repo). The framework's
anti-pattern guidance treats irreversible-side-effect logic as a Layer-1 concern. Centralizing
`gh issue create` in this skill (and its three siblings) gives one place to audit, version,
and harden the posting path. The thin `/create-incident` command never calls `gh` directly.

**Authorizing ADR:** ADR-077 (governs all `github-incident-from-*` skills).

---

## When this skill is invoked

The slash command `/create-incident "<observation>"` invokes this skill after parsing its
arguments:

```
Skill(command="github-incident-from-observation")
```

For eval/test runs that must NOT post real issues:

```
Skill(command="github-incident-from-observation", args="--eval")
```

Inputs the slash command provides (via shared context, since `args` is just a flag):

| Variable | Type | Source | Example |
|----------|------|--------|---------|
| `observation_text` | string | command args, or AskUserQuestion when empty | "When /create-story runs without a STORY_ID arg, it silently creates a file named .story.md instead of halting." |
| `label_type` | `"bug"` \| `"enhancement"` | command `--type=` flag, or AskUserQuestion when absent | `"bug"` |
| `severity` | `"critical"` \| `"high"` \| `"medium"` \| `"low"` | command `--severity=` flag, or AskUserQuestion when absent | `"high"` |
| `originating_work` | string (optional) | command `--work=` flag | `"STORY-661 /dev run, Phase 04"` |
| `related` | string (optional) | command `--related=` flag | `"ADR-077, #399"` |
| `repo` | string | hardcoded constant (template line 1) | `bankielewicz/DevForgeAI` |

There is **no upstream id** for an observation — the skill derives a stable one from the text
(see Constants → `OBS_ID`). Single observation in, single issue out.

Outputs the slash command receives back (used by its final summary step):

```json
[
  {
    "obs_id": "OBS-1a2b3c4d",
    "issue_number": 412,
    "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/412",
    "status": "success",
    "error_message": null
  }
]
```

`status` ∈ `success` | `failed` | `cancelled` | `skipped`. The result is always a
single-element array (wrapped for parity with the batch siblings' return contract).

---

## Constants (locked)

```
REPO                   = bankielewicz/DevForgeAI
ISSUES_URL             = https://github.com/bankielewicz/DevForgeAI/issues
TEMPLATE_PATH          = assets/templates/Github-incident-template.md   # relative to this skill
OBS_ID                 = CLI-derived via devforgeai-validate derive-obs-id (stdin=observation_text bytes)
DRAFTS_DIR             = tmp/${OBS_ID}/drafts/                          # per Rule 2 (operational-safety.md)
POSTED_PATH            = tmp/${OBS_ID}/posted.json                      # canonical post log (REAL mode)
SKIPPED_PATH           = tmp/${OBS_ID}/skipped.json                     # idempotency-skip in REAL mode
EVAL_MOCK_DIR          = tmp/eval-mock/                                 # only when --eval set
EVAL_POSTED_PATH       = tmp/eval-mock/posted.json                      # canonical mock-post log
GH_BIN                 = gh                                             # PATH-resolved
MOCK_ISSUE_RANGE       = [0, 99999]                                     # eval issue_number = int(sha256(OBS_ID)[:7],16) % 100000
ID_PATTERN             = ^OBS-[0-9a-f]{8}$
LABEL_TYPES            = {bug, enhancement}
```

`OBS_ID` is the per-observation identity and idempotency key:
`OBS_ID = "OBS-" + sha256(observation_text.encode("utf-8")).hexdigest()[:8]`. The same
observation text always resolves to the same `OBS_ID`, so a re-run lands in the same
`tmp/${OBS_ID}/drafts/` directory and the idempotency check (Phase 1.5) can detect a prior
post. Per `.claude/rules/workflow/operational-safety.md` Rule 2, never write to system
`/tmp/`.

**Skipped diagnostics live in their own file** (`skipped.json`), separate from `posted.json`,
so a `grep -E "github\.com" posted.json` audit catches accidental real-URL leaks. Pattern
identical to the siblings.

---

## Eval Mode (`--eval` argument)

When invoked with `args="--eval"`, Phase 5 substitutes `gh issue create` with a mock that:
- Returns a deterministic mock URL `https://example.invalid/issue/<n>` where `<n>` is
  SHA-256-derived from `OBS_ID` (reproducible across runs)
- Writes the mock-posting record to `tmp/eval-mock/posted.json` (single JSON file, stable
  schema — see "Posted schema" below)
- Does NOT invoke the real `gh` CLI (no network call, no real issue)
- Skips the Phase 1.3 `gh auth status` and Phase 1.4 `gh repo view` checks
- Defaults `label_type` to `bug` if absent (no interactive prompt in eval), and defaults the
  Phase 4 approval to "Post" deterministically

The user runs parallel Claude sessions in OTHER repos; test runs must never accidentally
interact with any GitHub repo. The `--eval` flag is the safety harness. The `.invalid` TLD is
RFC-2606-reserved and never resolves.

### Posted schema (stable — every entry has every field, even null)

The same envelope is written in both modes; only three field *values* differ by mode (shown in
the comments). In **REAL** mode: `mode="REAL"`, `mock=false`, `issue_url` is a real
`github.com` URL. In **EVAL** mode: `mode="MOCKED"`, `mock=true`, `issue_url` is an
`example.invalid` URL (this preserves the `grep github.com tmp/eval-mock/posted.json` audit
invariant — an eval log must never carry a real URL). The example below shows the REAL-mode
values.

```json
{
  "mode": "REAL",
  "repo": "bankielewicz/DevForgeAI",
  "generated_at": "<iso UTC>",
  "obs_id": "OBS-1a2b3c4d",
  "posted": [
    {
      "obs_id": "OBS-1a2b3c4d",
      "issue_number": 412,
      "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/412",
      "title": "Halt /create-story when STORY_ID argument is absent",
      "labels": ["type:bug", "origin:spontaneous-observation", "category:framework", "severity:high"],
      "draft_path": "tmp/OBS-1a2b3c4d/drafts/draft-OBS-1a2b3c4d.md",
      "label_type": "bug",
      "ts": "<iso UTC>",
      "status": "success",
      "error_message": null,
      "mock": false,
      "fingerprint": "sha256:..."
    }
  ]
}
```

In EVAL mode the corresponding fields are `"mode": "MOCKED"`, `"mock": true`, and
`"issue_url": "https://example.invalid/issue/<n>"`.

`fingerprint = sha256(f"{OBS_ID}::{title}".encode()).hexdigest()` — the idempotency match key
re-runs check in Phase 1.5.

---

## Phase 1 — Setup

### 1.1 Validate inputs

```
IF observation_text is empty OR len(observation_text.strip()) < 20:
    HALT → "Observation text is required and must be at least 20 characters describing the
            bug or enhancement." (The command guarantees this via a pre-delegation prompt, but
            the skill validates independently — defense in depth.)

IF label_type not in {"bug", "enhancement"}:
    IF --eval: label_type = "bug"            # deterministic, no prompt in eval
    ELSE: AskUserQuestion →
        question: "What type of issue is this?"
        header:   "Type"
        options:  ["bug — something is broken or wrong",
                   "enhancement — a new gate, lint, or capability"]
    label_type = (mapped to "bug" | "enhancement")

IF severity not in {"critical", "high", "medium", "low"}:
    IF --eval: severity = "medium"           # deterministic, no prompt in eval
    ELSE: AskUserQuestion →
        question: "What is the severity of this issue?"
        header:   "Severity"
        options:  ["critical — system broken / data loss",
                   "high — significant impact, workaround painful",
                   "medium — moderate impact, workaround exists",
                   "low — minor / cosmetic"]
    severity = (mapped to "critical" | "high" | "medium" | "low")
```

### 1.2 Derive OBS_ID

EXECUTE: Pipe `observation_text` bytes to `devforgeai-validate derive-obs-id` and bind stdout as `OBS_ID`:
```bash
printf '%s' "${observation_text}" | devforgeai-validate derive-obs-id
```
VERIFY: `OBS_ID` matches `^OBS-[0-9a-f]{8}$`. If the CLI exits non-zero → HALT → AskUserQuestion.

`OBS_ID` MUST match `ID_PATTERN` (`^OBS-[0-9a-f]{8}$`). It scopes every `tmp/` path below.

### 1.3 Confirm gh authentication (SKIPPED in `--eval`)

```bash
gh auth status
```
HALT on non-zero → "gh CLI not authenticated. Run `gh auth login` and re-invoke
`/create-incident`." HALT if `gh` is not on PATH.

### 1.4 Confirm repo accessibility (SKIPPED in `--eval`)

```bash
gh repo view bankielewicz/DevForgeAI --json name
```
HALT on failure (no repo access / network).

### 1.5 Idempotency check

```
IF Glob("tmp/${OBS_ID}/posted.json") AND its posted[0].status == "success":
    AskUserQuestion →
        question: "This observation was already posted as Issue-${issue_number}
                   (${issue_url}). Re-post anyway?"
        options:  ["Skip (recommended)", "Re-post (creates a duplicate)", "Cancel"]
    Skip   → return [{obs_id, status: "skipped",
                      error_message: "already posted as Issue-${issue_number}"}]
    Cancel → return [{obs_id, status: "cancelled"}]
    Re-post→ continue

IF Glob("tmp/${OBS_ID}/drafts/draft-${OBS_ID}.md") exists (a prior draft):
    # If posted.json exists with status "failed", surface that the prior POST attempt failed
    # (not merely "a draft exists") so the user is not misled into thinking nothing was tried.
    prefix = ("A prior post attempt FAILED (${posted[0].error_message}); a draft exists"
              if posted.json status == "failed"
              else "A draft already exists for this observation")
    AskUserQuestion →
        question: "${prefix} (OBS_ID=${OBS_ID}). How to proceed?"
        options:  ["Re-use existing draft — go straight to preview",
                   "Regenerate — overwrite with a fresh draft",
                   "Cancel — inspect tmp/${OBS_ID}/drafts/ manually"]
    Re-use → load the draft, skip Phase 2, jump to Phase 3
    Regen  → continue to Phase 2 (overwrite)
    Cancel → return [{obs_id, status: "cancelled"}]
```
In `--eval` mode, default to "Regenerate" deterministically (always a fresh draft).

### 1.5.5 Remote duplicate check (ISSUE-797)

Before drafting, record a **remote duplicate scan** so the `pre-gh-incident-template-guard`
hook can verify the step ran and block `gh issue create` if the scan was skipped.

```bash
devforgeai-validate dup-scan ${OBS_ID} --query "<3-5 keywords from the observation>" --project-root=.
```

Read `tmp/${OBS_ID}/dup-scan.json` for the results list. If any result matches the same
defect/enhancement — over **BOTH open and closed** states — surface it in the approval loop
BEFORE Phase 2:

```
AskUserQuestion →
    question: "Possible remote duplicate: #${number} '${title}' (${state}, ${url}). Proceed?"
    options:  ["Skip — record as duplicate (recommended)", "File anyway", "Cancel"]
```

Then record the human disposition so the hook gate can pass:

```bash
# on Skip:
devforgeai-validate dup-scan ${OBS_ID} --disposition "skipped-duplicate:#${number}" --project-root=.
# → return [{obs_id, status: "skipped", error_message: "remote duplicate #${number}"}]
# on File anyway:
devforgeai-validate dup-scan ${OBS_ID} --disposition "filed-anyway:user-confirmed" --project-root=.
# → continue to Phase 2
# on no match found:
devforgeai-validate dup-scan ${OBS_ID} --disposition "no-match" --project-root=.
# → continue to Phase 2
# on Cancel: return [{obs_id, status: "cancelled"}] without recording disposition
```

In `--eval` mode, skip the gh network scan and write disposition deterministically:
`devforgeai-validate dup-scan ${OBS_ID} --disposition "no-match" --project-root=.`
The remote scan is mandatory in REAL mode.

### 1.6 Create the drafts directory

```bash
mkdir -p tmp/${OBS_ID}/drafts/
```
(Bash `mkdir`/`echo >>` into `tmp/` is permitted per operational-safety.md Rule 2.)

---

## Phase 2 — Drafting

Load the template (`Read(file_path="assets/templates/Github-incident-template.md")`) and use
it as the authoritative drafting prompt. Compose the issue body with **all ten** template
sections in order: `## Context`, `## Current behavior`, `## Required behavior`,
`## Files to change`, `## Acceptance criteria`, `## Test plan`, `## Out of scope`,
`## Dependencies`, `## Provenance`, `## Labels`.

### 2.1 Title synthesis

- Take the first sentence of `observation_text`; render it imperative, verb-first
  (Fix / Add / Halt / Replace / Remove / Update / Enforce / Gate / …), ≤80 chars.
- Strip leading framing ("When …", "I noticed …", "It seems …") and convert to a direct
  imperative describing the change.
- If the first sentence exceeds 80 chars, truncate at the last word boundary ≤77 and append
  `…`.
- If no imperative verb can be derived, prepend one consistent with `label_type` (bug → a
  corrective verb; enhancement → "Add"/"Enforce"), then rewrite to a clean imperative.

### 2.2 Section mapping (single observation → ten sections)

| Source | → | Issue section |
|--------|---|---------------|
| synthesized title | → | `# <Title>` |
| observation_text (the "what is wrong / missing" framing) | → | `## Context` + `## Current behavior` |
| inferred corrected state (what SHOULD happen instead) | → | `## Required behavior` |
| file paths extracted from observation_text | → | `## Files to change` (Open Question if none) |
| derived objectively-verifiable checklist | → | `## Acceptance criteria` |
| derived proof commands / test names | → | `## Test plan` |
| default `- None` unless the text names adjacent excluded work | → | `## Out of scope` |
| default `None` unless the text names prerequisites | → | `## Dependencies` |
| constructed from invocation context (see 2.3) | → | `## Provenance` |
| `label_type` + repo label reconciliation (2.4) | → | `## Labels` |

Unlike the siblings there is no structured `affected_files[]` input — extract candidate paths
from the free text (`.claude/…`, `src/…`, `devforgeai/…`, `tests/…`, or any `path/to/file.ext`
token). If none can be grounded, write `## Files to change` as an Open Question rather than
inventing targets (BR-003).

### 2.3 Provenance section (the distinguishing requirement)

The `## Provenance` section MUST carry four sub-bullets; `**Source**` and `**Chain**` are
mandatory and gate-checked by `pre-gh-incident-template-guard.sh` (#400):

```markdown
## Provenance
- **Source**: spontaneous-observation
- **Originating work**: ${originating_work OR "active session — see conversation context"}
- **Chain**: discovered → grounded → filed
- **Related**: ${related OR "None"}
```

`**Source**` MUST be the literal `spontaneous-observation` (this is what distinguishes an
observation-derived issue from an RCA/QA/feedback one). `**Chain**` MUST be non-empty; the
default `discovered → grounded → filed` records the on-ramp causal chain. If the observation
cites issues / ADRs / commits, fold them into `**Related**` and extend `**Chain**` with the
originating link (e.g. `#399 freehand-filing → template bypassed → this on-ramp → filed`).

### 2.4 Label assembly

```python
labels = [
    f"type:{label_type}",              # type:bug | type:enhancement
    "origin:spontaneous-observation",  # origin marker
    "category:framework",              # observation-derived issues are framework issues
    f"severity:{severity}",            # severity:critical | high | medium | low
]
```
In REAL mode, run `gh label list -R bankielewicz/DevForgeAI` ONCE, cache it, drop any label
not present on the repo, and emit one Open Question per dropped label (BR-001). In `--eval`
mode, emit all inferred labels without checking. The `## Labels` body line is mandatory and
MUST match the labels array exactly (BR-015).

### 2.5 Write the draft

```
Write(file_path="tmp/${OBS_ID}/drafts/draft-${OBS_ID}.md", content=<full body>)
IF open_questions: Write("tmp/${OBS_ID}/drafts/open-questions-${OBS_ID}.md", <list>)
```

### 2.6 Per-draft validation gate

Reject (and fix) the draft unless ALL hold:
- title ≤80 chars, imperative, no prohibited language (template line 65 list)
- **the ENTIRE body** (title + every section, not just the title) is free of the prohibited
  terms — `pre-gh-incident-template-guard.sh` greps the whole `--body-file` case-insensitively
  and `exit 2`s on any match, so a synthesized AC/Test-plan line containing "improve" /
  "robust" / "leverage" / "streamline" would hard-block the post. Scan the full body here.
- all ten template sections present, in order (the skill's own check; the guard hook gate-checks
  nine of them — see the Integration table note on `## Labels`)
- `## Provenance` contains `**Source**` and `**Chain**` (guard-hook requirement)
- `## Labels` present and equal to the labels array
- ≥1 acceptance criterion; `## Test plan` non-empty

If the observation contains prohibited language ("consider", "improve", "streamline", …),
translate it to concrete language in the body and add an Open Question noting the translation
(do not embed the prohibited term in the posted body).

---

## Phase 3 — Summary Preview

Single observation → one draft, so emit the full preview inline (no batch table):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Draft Preview — ${OBS_ID}   ${"[EVAL — no real post]" if --eval else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Title:   ${title}
  Type:    ${label_type}
  Labels:  ${", ".join(labels)}
  Open-Qs: ${count}   (${"none" if 0 else "see below"})
  Draft:   tmp/${OBS_ID}/drafts/draft-${OBS_ID}.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Then emit any Open Questions (separate from the body — these are blockers for the user, not
issue content).

---

## Phase 4 — Drill-down Approval Loop

```
AskUserQuestion →
    question: "Approve posting this issue to bankielewicz/DevForgeAI?"
    header:   "Approve"
    options:
      - "Post issue (Recommended)"        → Phase 5
      - "Inspect full draft body"         → Read draft, emit full body, re-prompt (loop)
      - "Edit observation and regenerate" → AskUserQuestion for new text → re-derive OBS_ID →
                                            re-run Phase 2
      - "Cancel — post nothing"           → return [{obs_id, status: "cancelled"}]
                                            (draft stays in tmp/${OBS_ID}/drafts/)
```
NO `gh issue create` happens before this approval (BR-005). In `--eval` mode, default to "Post
issue" deterministically. If the user edits the observation text, the SHA-256 changes, so a
new `OBS_ID` and a new `tmp/` directory result — the original draft is preserved.

---

## Phase 5 — Post

### 5.0 Recurrence check (Issue #934)

MANDATORY before posting in REAL mode. The `pre-gh-incident-template-guard` **Step 9
create-gate** blocks `gh issue create` unless a fresh recurrence-check artifact exists for the
exact draft body — so this step runs against the finalized Phase 2 draft, keyed by the same
body bytes Phase 5.1 posts. It also detects an exact recurrence of an OPEN issue so a +1 is
recorded as a comment instead of filing a duplicate.

1. Construct an `OccurrenceInput` JSON at `tmp/${OBS_ID}/occurrence.json` with the 12 fields
   `incident-recurrence check` validates: `source_kind`, `source_id`, `kind`, `provenance`,
   `title`, `description`, `affected_files`, `evidence_refs`, `category`,
   `severity_or_priority`, `producer_record_id`, `repo_identity`. Set
   `source_kind: "observation"`, `source_id: "${OBS_ID}"`, and
   `repo_identity: "bankielewicz/DevForgeAI"`.
2. Run the check against the draft, before posting:

```bash
devforgeai-validate incident-recurrence check --occurrence tmp/${OBS_ID}/occurrence.json --body-file tmp/${OBS_ID}/drafts/draft-${OBS_ID}.md --verb create --project-root=.
```

3. Read `disposition`, `fingerprint`, and `matched_issue_number` from the artifact the command
   prints (`tmp/incident-recurrence/checks/<body_sha256>.json`).

If `disposition == "exact_open_match"` (a GROUNDED, recipe_confidence-HIGH recurrence of an
OPEN issue), offer the recurrence-comment path instead of filing a new issue:

```
AskUserQuestion →
    question: "Exact recurrence of OPEN issue #${matched_issue_number}. Record a +1 recurrence comment instead of filing a new issue?"
    options:  ["Record +1 comment (recommended)", "File new anyway", "Cancel"]
```

- **Record +1 comment** → write the comment body to
  `tmp/${OBS_ID}/drafts/recurrence-comment-${OBS_ID}.md` as a `<!-- recurrence -->` marker line
  followed by exactly ONE structured line `repo_identity | fingerprint | run_id`
  (`repo_identity` = `bankielewicz/DevForgeAI`, `fingerprint` = the artifact's `fingerprint`,
  `run_id` = `${OBS_ID}`). Mint the comment artifact, then post the comment:

  ```bash
  devforgeai-validate incident-recurrence check --occurrence tmp/${OBS_ID}/occurrence.json --body-file tmp/${OBS_ID}/drafts/recurrence-comment-${OBS_ID}.md --verb comment --project-root=.
  gh issue comment ${matched_issue_number} --repo bankielewicz/DevForgeAI --body-file tmp/${OBS_ID}/drafts/recurrence-comment-${OBS_ID}.md
  ```
  Then SKIP Phase 5.1 (no new issue) → return `[{obs_id, status: "recurrence-recorded", matched_issue: ${matched_issue_number}}]`.
- **File new anyway** → continue to Phase 5.1 (the `--verb create` artifact this step wrote satisfies the Step 9 create-gate).
- **Cancel** → return `[{obs_id, status: "cancelled"}]`.

For any non-`exact_open_match` disposition, continue to Phase 5.1.

In `--eval` mode, SKIP this entire step: Phase 5.2 mocks the post (no real `gh issue create`
runs, so the create-gate never fires) and no comment is posted.

This step enforces artifact provenance only — it does NOT verify the `OccurrenceInput` is
semantically truthful; that remains a review concern.

### 5.1 REAL mode

```bash
gh issue create \
  --repo bankielewicz/DevForgeAI \
  --title "${title}" \
  --body-file "tmp/${OBS_ID}/drafts/draft-${OBS_ID}.md" \
  --label "${labels_csv}"
```
- `--repo bankielewicz/DevForgeAI` is hardcoded on EVERY invocation (cross-repo guard —
  BR-007; the user has parallel sessions in other repos and `gh` otherwise defaults to the
  CWD's git remote).
- stdout is the issue URL → parse `issue_number = int(issue_url.rsplit("/", 1)[1])`.
- On non-zero exit: `status = "failed"`, capture stderr; surface a per-failure recovery hint
  (label missing / HTTP 401 auth / rate-limit / HTTP 422 body / network) — NO auto-retry.

### 5.2 EVAL mode

```python
issue_number = int(hashlib.sha256(OBS_ID.encode("utf-8")).hexdigest()[:7], 16) % 100000
issue_url    = f"https://example.invalid/issue/{issue_number}"
```
No `gh` call; write the mock record to `tmp/eval-mock/posted.json`.

### 5.3 Write posted.json (both modes)

Write the stable-schema envelope (see "Posted schema") to `POSTED_PATH` (REAL) or
`EVAL_POSTED_PATH` (eval). `fingerprint = sha256(f"{OBS_ID}::{title}")` — the Phase-1.5
idempotency key.

---

## Phase 6 — Result Summary + Return

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GitHub Incident Summary — ${OBS_ID}   ${"[EVAL]" if --eval else ""}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Posted:  Issue-${issue_number} — ${issue_url}
  (or ❌ Failed: ${error_message} / ⏭ Skipped: ${reason} / Cancelled)
  Draft at: tmp/${OBS_ID}/drafts/draft-${OBS_ID}.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Return the single-element result array (see "When this skill is invoked → Outputs").

---

## Business Rules (locked)

| Rule | Implementation |
|------|----------------|
| BR-001 Label assembly | `type:{bug\|enhancement}`, `origin:spontaneous-observation`, `category:framework`, `severity:{critical\|high\|medium\|low}`. Drop labels absent from the repo; Open Question per drop. |
| BR-002 Title quality | Imperative verb-first, ≤80 chars, no prohibited language. |
| BR-003 Files honesty | Extract paths from observation_text; if none, Open Question — never invent targets. |
| BR-004 Single issue | One observation → one issue. No batch loop, no multi-rec selection. |
| BR-005 Approval required | NO `gh issue create` before the Phase 4 approval. |
| BR-006 No system /tmp | Drafts under `tmp/${OBS_ID}/drafts/` (project-relative). |
| BR-007 Hardcoded repo | `--repo bankielewicz/DevForgeAI` on every invocation (cross-repo guard). |
| BR-008 Drafts persist | Drafts are not auto-deleted; re-runs reuse the idempotency check. |
| BR-009 Idempotency | Phase 1.5 detects a prior post via `posted.json` and a prior draft via the draft file. |
| BR-010 Provenance mandatory | `## Provenance` with `**Source**: spontaneous-observation` and a non-empty `**Chain**` — gate-checked by `pre-gh-incident-template-guard.sh`. |
| BR-011 Stable posted schema | `posted.json` always carries `mode`, `repo`, `generated_at`, `obs_id`, `posted: []`. |
| BR-012 Deterministic mock | eval `issue_number = int(sha256(OBS_ID)[:7], 16) % 100000` — reproducible. |
| BR-013 Stable id | `OBS_ID = OBS-<sha256(observation_text)[:8]>`; same text → same id. |
| BR-014 Eval safety | `--eval` skips auth/repo/post; mock URL on the RFC-2606 `.invalid` TLD. |
| BR-015 Labels body line | The `## Labels` section is mandatory and equals the labels array. |

---

## Edge Cases

| Case | Behavior |
|------|----------|
| `observation_text` empty or <20 chars | HALT in Phase 1.1. |
| `label_type` missing | AskUserQuestion (Phase 1.1); `--eval` defaults to `bug`. |
| `severity` missing | AskUserQuestion (Phase 1.1); `--eval` defaults to `medium`. |
| No file paths extractable | `## Files to change` is an Open Question; proceed. |
| Draft already exists for OBS_ID | Phase 1.5 AskUserQuestion: re-use / regenerate / cancel. |
| Already posted (posted.json success) | Phase 1.5 AskUserQuestion: skip / re-post / cancel. |
| `gh` not authenticated | HALT Phase 1.3. |
| Repo unreachable | HALT Phase 1.4. |
| All synthesized labels absent from repo | Open Question per label; proceed; user can cancel at Phase 4. |
| Prohibited language in observation | Translate to concrete terms in the body; Open Question noting the translation. |
| "Edit and regenerate" changes the text | Re-derive OBS_ID; fresh `tmp/` dir; original draft preserved. |
| Observation > ~500 chars | `## Context` = first ~4 sentences; full text quoted in `## Current behavior`. |
| `--eval` mode | No `gh`; deterministic mock; `tmp/eval-mock/posted.json`. |

---

## Integration

| Caller | Mechanism |
|--------|-----------|
| `/create-incident "<observation>" [--type=] [--work=] [--related=] [--eval]` | parses args, delegates `Skill(command="github-incident-from-observation")` |
| `pre-gh-incident-template-guard.sh` (#400) | gate-checks the posted body: **nine** required `##` sections (Context, Current behavior, Required behavior, Files to change, Acceptance criteria, Test plan, Out of scope, Dependencies, Provenance) + `## Provenance` `**Source**`/`**Chain**` non-empty + no prohibited language anywhere in the body. `## Labels` is mandatory per BR-015 but enforced by this skill's own Phase 2.6 gate, NOT by the hook. |
| `Github-incident-template.md` | the byte-identical drafting prompt, shared with the three siblings |

**Naming note (ADR-017 deviation).** ADR-017 mandates gerund-form skill names with the
`spec-driven-*` prefix. This skill — like its three `github-incident-from-*` siblings — is
provider-tightly-coupled (its entire purpose is `gh issue create` against one repo), so it
follows the established sibling naming rather than the generic gerund convention. It is the
fourth member of that family.

---

**Version:** 1.0 | **Created:** 2026-06-12 | **Source:** Issue #401 | **ADR:** ADR-077
