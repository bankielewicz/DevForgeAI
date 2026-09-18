---
name: create-incident-from-recommendations
description: Create GitHub incidents from QA recommendations
argument-hint: "STORY-NNN [--rec-ids=ID1,ID2] [--severity=CRITICAL|HIGH|MEDIUM|LOW] [--include-blocking] [--help]"
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite
---

# /create-incident-from-recommendations — Create GH Incidents from QA Recommendations

Parse a QA recommendations file produced by `/qa STORY-NNN`, select recommendations interactively (or honor `--rec-ids`), draft and post GitHub issues to bankielewicz/DevForgeAI via the `github-incident-from-recommendations` skill, then link the posted issues back into the QA-recs file.

**Component Orchestration:** Parse → Filter+Select → Draft+Approve+Post (skill) → Link

**Reference:** `references/create-incident-from-recommendations/incident-reference.md` for detailed docs.

**Architectural constraint:** This command never calls `gh` directly. All GitHub-issue logic is owned by the `github-incident-from-recommendations` skill. The slash command is a thin orchestrator.

**Sibling pathway:** `/create-incident-from-rca RCA-NNN` is the RCA-source equivalent. The two pathways share the embedded `Github-incident-template.md` asset (byte-identical) but consume different upstream document formats — RCA markdown vs. QA-recs YAML.

---

## Usage

```bash
/create-incident-from-recommendations STORY-NNN
/create-incident-from-recommendations STORY-NNN --rec-ids=REC-STORY-NNN-M-001,REC-STORY-NNN-L-002
/create-incident-from-recommendations STORY-NNN --severity=MEDIUM
/create-incident-from-recommendations STORY-NNN --include-blocking
/create-incident-from-recommendations --help
```

By default, only **Advisory** recommendations are eligible (the QA recs file's `## Advisory Recommendations` section). Pass `--include-blocking` to also include `## Blocking Recommendations`. `## Deferred Recommendations` are never auto-included — they require explicit `--rec-ids=` selection.

---

## Argument Parsing

```
ARG = first argument from $ARGUMENTS

IF ARG == "--help" OR ARG == "help":
    Display abbreviated help:
    "Usage: /create-incident-from-recommendations STORY-NNN [--rec-ids=ID1,ID2] [--severity=...] [--include-blocking]
     See: references/create-incident-from-recommendations/incident-reference.md for full help"
    HALT

STORY_ID = extract from arguments matching "STORY-[0-9]+" (case-insensitive)

IF STORY_ID empty:
    Display: "❌ STORY ID required"
    Display: "Usage: /create-incident-from-recommendations STORY-NNN"
    Display: "Available QA recommendations files:"
    FOR f in Glob("devforgeai/qa/recommendations/STORY-*-qa-recommendations.md"):
        Display: "  • ${story_id}"
    HALT

STORY_ID = uppercase(STORY_ID)  # story-661 → STORY-661

QA_RECS_FILE = "devforgeai/qa/recommendations/${STORY_ID}-qa-recommendations.md"

IF Glob(QA_RECS_FILE) returns nothing:
    Display: "❌ QA recommendations file not found: ${QA_RECS_FILE}"
    Display: ""
    Display: "Run /qa ${STORY_ID} first to generate QA recommendations."
    Display: ""
    Display: "Available QA recs files:"
    FOR f in Glob("devforgeai/qa/recommendations/STORY-*-qa-recommendations.md"):
        Display: "  • ${story_id}"
    HALT

# Optional flags — parsed from $ARGUMENTS
REC_IDS_RAW       = parse_value_after("--rec-ids=")        # e.g., "REC-STORY-661-M-001,REC-STORY-661-L-002"
SEVERITY_FILTER   = parse_value_after("--severity=")       # e.g., "MEDIUM"; uppercased
INCLUDE_BLOCKING  = "--include-blocking" in $ARGUMENTS     # boolean

REC_IDS_LIST = REC_IDS_RAW.split(",") with whitespace stripped (or empty if not provided)

IF REC_IDS_LIST not empty:
    FOR rec_id in REC_IDS_LIST:
        IF NOT rec_id matches "^REC-STORY-\d+-[CHML]-\d{3}$":
            Display: "❌ Invalid --rec-ids entry: ${rec_id}"
            Display: "   Expected format: REC-STORY-NNN-{C|H|M|L}-NNN (e.g., REC-STORY-661-M-001)"
            HALT

IF SEVERITY_FILTER not empty AND SEVERITY_FILTER NOT IN {"CRITICAL", "HIGH", "MEDIUM", "LOW"}:
    Display: "❌ Invalid --severity: ${SEVERITY_FILTER}"
    Display: "   Expected: CRITICAL | HIGH | MEDIUM | LOW"
    HALT
```

---

## Phase 1-5: QA-Recs Parsing

**See:** `references/create-incident-from-recommendations/parsing-workflow.md`

QA recommendation files are structured YAML (each rec is a YAML block under one of three section headers), validated against `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`. There is NO shared parser with `/create-incident-from-rca` — that sibling pathway parses RCA markdown via a different skill, which does not apply here.

**Steps (executed inline by this command, NOT via a separate skill):**

1. **Read frontmatter** — Validate `schema_version` is recognized.
2. **Sanity-check `<!-- SECTION_MANIFEST -->`** — Confirms the file structure expected by the schema.
3. **Parse YAML blocks** under `## Blocking Recommendations`, `## Advisory Recommendations`, `## Deferred Recommendations`.
4. **Validate each entry** against `qa-recommendations-schema.json`. Mandatory fields per category — see parsing-workflow.md for the table. HALT on schema violation with file:line context.
5. **Return** a list of recommendation objects with all schema fields (`id`, `severity`, `provenance`, `title`, `file`, `line` or `line_range`, `category`, `blocking_release`, `before_code`, `after_code`, `verification.command`, `verification.expected`, `estimated_effort_minutes`, `dependencies`, `references`, optional `classification`, `cycle_first_seen`, optional `remediation_steps`).

The result is a parsed `qa_recs_document` with a `recommendations` array, available to the next phase.

---

## Phase 6-9: Filter + Interactive Selection

**See:** `references/create-incident-from-recommendations/selection-workflow.md`

```
# Step 6.1: Apply default visibility — Advisory only unless --include-blocking
candidate = []
FOR rec in qa_recs_document.recommendations:
    IF rec.section == "Deferred":
        # Deferred recs are never auto-included
        IF rec.id in REC_IDS_LIST:
            candidate.append(rec)
        ELSE:
            continue
    ELIF rec.section == "Blocking" AND NOT INCLUDE_BLOCKING AND rec.id NOT IN REC_IDS_LIST:
        continue
    ELSE:
        candidate.append(rec)

# Step 6.2: Apply --severity filter (only if provided)
IF SEVERITY_FILTER not empty:
    candidate = [r for r in candidate if r.severity == SEVERITY_FILTER]

# Step 6.3: Apply --rec-ids filter (only if provided) — exact match, skips prompt
IF REC_IDS_LIST not empty:
    selected_recommendations = [r for r in candidate if r.id in REC_IDS_LIST]

    # Validate every requested rec_id was found in the file
    missing = [id for id in REC_IDS_LIST if id NOT IN [r.id for r in selected_recommendations]]
    IF missing not empty:
        Display: "❌ Requested rec IDs not found in ${QA_RECS_FILE}: ${missing}"
        HALT

    # Skip the multi-select prompt — user already specified IDs
ELSE:
    # Step 6.4: Interactive multi-select via AskUserQuestion
    AskUserQuestion(
        question: "Which recommendations to convert into GitHub issues for ${STORY_ID}?",
        header: "Select",
        multiSelect: true,
        options: [
            "All ${len(candidate)} recommendations (Recommended)",
            # Per-rec rows showing severity, ID, title, file:line, effort
            "[${severity}] ${rec.id} — ${title} (${file}:${line}, ${effort}min)",
            ...
            "None — cancel"
        ]
    )

    selected_recommendations = (mapped from user choices)

IF selected_recommendations empty OR user chose "None — cancel":
    Display: "No recommendations selected; cancelling."
    HALT gracefully
```

---

## Phase 10: Issue Drafting + Approval + Posting (DELEGATE TO SKILL)

**See:** `references/create-incident-from-recommendations/issue-creation-workflow.md`

This phase is delegated entirely to the `github-incident-from-recommendations` skill. The slash command does NOT format issue bodies, does NOT invoke the gh CLI to post issues, does NOT manage approval prompts. The skill owns all of that.

```
Skill(command="github-incident-from-recommendations", args="--batch")
```

**Inputs the skill consumes** (via shared context):
- `${STORY_ID}`, `${QA_RECS_FILE}` — from argument parsing
- `selected_recommendations` — from Phase 6-9 (full QA-recs schema per entry)
- `repo` — hardcoded constant `bankielewicz/DevForgeAI` (in skill itself per BR-007)

**Outputs the skill returns** (used by Phase 11 below):
```
results = [
  { rec_id: "REC-STORY-661-M-001", issue_number: 42, issue_url: "https://github.com/bankielewicz/DevForgeAI/issues/42", status: "success", error_message: null },
  { rec_id: "REC-STORY-661-M-002", issue_number: null, issue_url: null,  status: "failed", error_message: "label X missing" },
  { rec_id: "REC-STORY-661-L-001", issue_number: null, issue_url: null,  status: "skipped", error_message: "already linked: Issue-37" }
]
```

The skill internally runs 6 phases:
1. Setup (validate inputs, gh auth check, idempotency detection from QA_RECS_FILE)
2. Drafting (apply embedded template; QA recs are richer than RCA — `file:line` directly populates `## Files to change`, `before_code`/`after_code` map to `## Current behavior`/`## Required behavior`, `verification.command`+`expected` populate `## Test plan`, `classification` maps to `classification:regression` or `classification:pre-existing` label)
3. Summary preview (compact table with severity column)
4. Drill-down approval loop (user picks: post-all / inspect / subset / cancel)
5. Post (the gh CLI invocation hardcodes `--repo bankielewicz/DevForgeAI` per BR-007 — continue-on-error per BR-004)
6. Result (return to caller)

The slash command treats this as a single black-box delegation.

---

## Phase 11: QA-Recs Linking

**See:** `references/create-incident-from-recommendations/linking-workflow.md`

For each entry in `results` with `status == "success"`, record the rec → issue link in `tmp/${STORY_ID}/posting-manifest.json`. The QA recs file is **not** mutated by this phase.

**Why a manifest, not an in-place Edit?** `feedback-artifact-write-gate.sh` (ADR-062 D2, PreToolUse[Edit|Write]) blocks any Edit/Write under `devforgeai/qa/recommendations/**` while a workflow is active. An in-place Edit silently failed during the normal /qa → /create-incident-from-recommendations flow and caused duplicate posts on re-runs (the skill's idempotency check missed the never-added markers). The manifest-link-back pattern mirrors the sibling `github-incident-from-feedback` skill (advisor catch, PR #76).

```
manifest_path = f"tmp/{STORY_ID}/posting-manifest.json"
mkdir -p "tmp/{STORY_ID}/"

IF file_exists(manifest_path):
    manifest = json.parse(Read(file_path=manifest_path))
ELSE:
    manifest = { "schema_version": "1.0", "story_id": STORY_ID,
                 "qa_recs_file": QA_RECS_FILE, "last_updated": null, "links": [] }

existing_rec_ids = { l["rec_id"] for l in manifest["links"] }

FOR result in results where status == "success":
    rec_id       = result.rec_id
    issue_number = result.issue_number
    issue_url    = result.issue_url

    IF rec_id in existing_rec_ids:
        Display: f"  ⚠ {rec_id} already linked in posting-manifest.json — skipping"
        continue

    manifest["links"].append({
        "rec_id":       rec_id,
        "issue_number": issue_number,
        "issue_url":    issue_url,
        "posted_at":    datetime.now(timezone.utc).isoformat(timespec="seconds")
    })

manifest["last_updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
Write(file_path=manifest_path, content=json.dumps(manifest, indent=2))
```

The QA-recs file's frontmatter `last_posted_at` and the `## Posting Audit Trail` section are owned and updated by the skill (BR-014), not by this slash command. Do NOT duplicate that bookkeeping here.

If a rec has a `source_rca:` pointer (rare — only for QA recs that originated from an earlier RCA), additionally update the linked RCA file. RCA files are under `devforgeai/RCA/` (not gated by ADR-062 D2), so Edit is safe there. See linking-workflow.md Step 4.

---

## Error Handling

Validation errors, gh auth failures, label-missing errors, network failures, and per-issue failures are all handled with **failure isolation** — a failure on issue N does NOT block issue N+1. The `github-incident-from-recommendations` skill's Phase 5 handles posting errors and Phase 6 reports them. The slash command's Phase 11 only links successful posts.

See `references/create-incident-from-recommendations/incident-reference.md` for detailed error templates and recovery guidance.

---

## Success Criteria

- [ ] QA recs file parsed and validated against schema (Phase 1-5)
- [ ] Filters applied (`--severity`, `--include-blocking`, default Advisory-only) (Phase 6.1-6.3)
- [ ] Recommendations selected (`--rec-ids` honored OR multi-select prompt) (Phase 6-9)
- [ ] Issues drafted with full template fidelity, including `## Labels` section (skill Phase 2 + BR-015)
- [ ] User approval explicitly captured before any post (skill Phase 4)
- [ ] Issues posted via `github-incident-from-recommendations` skill with `--repo bankielewicz/DevForgeAI` hardcoded (skill Phase 5 + BR-007)
- [ ] Posting manifest written at `tmp/${STORY_ID}/posting-manifest.json` with one `links[]` entry per successful post (Phase 11); QA recs file is NOT mutated (BR-005)
- [ ] Failure isolation: per-issue failures don't block batch (BR-004)
- [ ] Idempotency: re-runs detect already-linked recs and route to `skipped.json` (skill Phase 1.5 + BR-009)

---

## Integration

**Invoked by:** User via `/create-incident-from-recommendations STORY-NNN`
**Invokes:**
- `github-incident-from-recommendations` skill (Phase 10: drafting + posting + idempotency + audit trail)

**Note:** This command does NOT delegate to a separate parsing skill (the RCA-pathway sibling does, but RCA-format parsing is irrelevant here). QA recs parsing is inline-YAML per `parsing-workflow.md`.

**Updates:** `tmp/${STORY_ID}/posting-manifest.json` (per-rec link-back entries; Phase 11 owned), GitHub issues (created via skill). QA recs file is **not** modified by Phase 11 — see BR-005 in linking-workflow.md.

**Reference Files:** `references/create-incident-from-recommendations/` directory contains:
- `parsing-workflow.md` — Phase 1-5 detailed YAML parsing + schema validation
- `selection-workflow.md` — Phase 6-9 filter logic + multi-select prompt
- `issue-creation-workflow.md` — Phase 10 skill-delegation contract
- `linking-workflow.md` — Phase 11 QA-recs-update workflow
- `incident-reference.md` — Extended documentation, error templates, business rules

---

**Version:** 1.0 — Lean Orchestration | **Pattern:** Command delegates issue creation to skill (sibling: `/create-incident-from-rca`)
