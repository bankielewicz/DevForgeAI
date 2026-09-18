# /create-incident-from-recommendations — Extended Reference Documentation

Supplementary documentation for the `/create-incident-from-recommendations` command. The command file contains core orchestration logic; this file contains detailed help, error templates, business rules, and recovery patterns.

---

## Full Help Text

```
/create-incident-from-recommendations — Convert QA recommendations into GitHub issues

USAGE:
    /create-incident-from-recommendations STORY-NNN
    /create-incident-from-recommendations STORY-NNN --rec-ids=ID1,ID2
    /create-incident-from-recommendations STORY-NNN --severity=MEDIUM
    /create-incident-from-recommendations STORY-NNN --include-blocking
    /create-incident-from-recommendations --help | help

ARGUMENTS:
    STORY-NNN                   Required. STORY ID (e.g., STORY-661). Case-insensitive.

OPTIONS:
    --rec-ids=ID1,ID2,ID3       Skip the multi-select prompt; post exactly the listed recs.
                                Format: REC-STORY-NNN-{C|H|M|L}-NNN per ID.
    --severity=SEVERITY         Filter to one severity level. CRITICAL|HIGH|MEDIUM|LOW.
    --include-blocking          Include the ## Blocking Recommendations section
                                (default: Advisory only).
    --help, help                Display this help message.

PROCESS:
    1. Read devforgeai/qa/recommendations/STORY-NNN-qa-recommendations.md
    2. Validate against qa-recommendations-schema.json
    3. Apply filters (--severity, --include-blocking) — Advisory section is default
    4. Honor --rec-ids OR show interactive multi-select
    5. Delegate drafting + preview + approval + posting to
       github-incident-from-recommendations skill
    6. Skill posts approved drafts via the gh CLI (--repo bankielewicz/DevForgeAI hardcoded)
    7. Update QA recs file with **Posted as:** Issue-NNN markers per successful post

REPO:
    Hardcoded to bankielewicz/DevForgeAI per BR-007. Multi-repo support is out of scope.

RELATED COMMANDS:
    /qa STORY-NNN                          Generate the QA recommendations file consumed here
    /create-incident-from-rca RCA-NNN      Sibling command; same target repo, different source format
    /create-stories-from-rca RCA-NNN       Convert RCA recs to user stories (different artifact)
    /create-story                          Create individual story
    /dev STORY-NNN                         Implement a story
```

---

## Error Message Templates

```
ERROR_MISSING_STORY_ID:
    "❌ STORY ID required"
    "Usage: /create-incident-from-recommendations STORY-NNN"
    "Available QA recs files:"

ERROR_QA_RECS_NOT_FOUND:
    "❌ QA recommendations file not found: ${QA_RECS_FILE}"
    "Run /qa ${STORY_ID} first to generate QA recommendations."
    "Available QA recs files:"

ERROR_INVALID_STORY_FORMAT:
    "❌ Invalid STORY format"
    "Expected: STORY-NNN (where NNN are digits)"

ERROR_INVALID_REC_ID_FORMAT:
    "❌ Invalid --rec-ids entry: ${rec_id}"
    "Expected format: REC-STORY-NNN-{C|H|M|L}-NNN (e.g., REC-STORY-661-M-001)"

ERROR_INVALID_SEVERITY:
    "❌ Invalid --severity: ${SEVERITY_FILTER}"
    "Expected: CRITICAL | HIGH | MEDIUM | LOW"

ERROR_REC_IDS_NOT_FOUND:
    "❌ Requested rec IDs not found in ${QA_RECS_FILE}: ${missing_ids}"

ERROR_GH_NOT_AUTHENTICATED:
    "❌ gh CLI not authenticated"
    "Run: gh auth login"
    "Then re-invoke: /create-incident-from-recommendations ${STORY_ID}"

ERROR_GH_NOT_INSTALLED:
    "❌ gh CLI not found on PATH"
    "Install: https://cli.github.com"

ERROR_REPO_INACCESSIBLE:
    "❌ Cannot access bankielewicz/DevForgeAI"
    "Check: gh repo view bankielewicz/DevForgeAI"
    "Possible causes: token lacks permission, network down, repo renamed"

ERROR_NO_RECS_AFTER_FILTER:
    "❌ No recommendations match current filters"
    "Tip: re-run without --severity or pass --include-blocking"

ERROR_SCHEMA_VIOLATION:
    "❌ Schema violations in ${rec.id}:"
    "   • ${each violation}"
    "   File: ${QA_RECS_FILE}"
    "Fix the QA recs file (or regenerate with /qa ${STORY_ID}) and retry."
```

---

## Phase Orchestration Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│        /create-incident-from-recommendations Workflow                │
│                  (4 Main Orchestration Phases)                       │
└─────────────────────────────────────────────────────────────────────┘

Phase 1-5: QA RECS PARSING (inline, NOT delegated)
  ├─ Input: STORY ID (e.g., STORY-661)
  ├─ Process: Read file, validate schema, parse YAML blocks across 3 sections
  ├─ Output: qa_recs_document with full schema per rec
  └─ Reference: parsing-workflow.md

       ↓

Phase 6-9: FILTER + INTERACTIVE SELECTION
  ├─ Input: Parsed recommendations
  ├─ Process: Apply --severity, --include-blocking, --rec-ids filters;
  │           multi-select prompt if --rec-ids absent
  ├─ Output: selected_recommendations
  └─ Reference: selection-workflow.md

       ↓

Phase 10: DRAFT + APPROVE + POST (delegated to skill)
  ├─ Input: selected_recommendations, STORY_ID, QA_RECS_FILE, repo
  ├─ Process: Skill runs 6 internal phases (Setup, Drafting, Summary,
  │           Drill-down approval, Post, Result + audit trail)
  ├─ Output: results array (rec_id, issue_number, issue_url, status, error_message)
  └─ Reference: issue-creation-workflow.md (contract)
                + ../../../skills/github-incident-from-recommendations/SKILL.md (skill)

       ↓

Phase 11: QA-RECS LINKING
  ├─ Input: results array (from skill)
  ├─ Process: Add **Posted as:** Issue-NNN markers to QA recs file for successful posts
  ├─ Output: QA recs file with traceability markers
  └─ Reference: linking-workflow.md
```

| Phase | Component | Owner | Role |
|-------|-----------|-------|------|
| 1-5 | QA Recs Parser | This slash command (inline) | Read + validate + parse YAML |
| 6-9 | Selection | This slash command | Filters + interactive selection |
| 10 | Issue Creator | github-incident-from-recommendations skill | Draft, preview, approve, post, audit |
| 11 | Linker | This slash command | Add Issue-NNN markers to QA recs file |

---

## Business Rules & Constraints

| Rule | Constraint | Implementation | Phase |
|------|-----------|-----------------|-------|
| BR-001: Schema Validation | Every rec must satisfy `qa-recommendations-schema.json` | HALT on violation | Parsing |
| BR-002: Default Visibility | Advisory section is default; Blocking opt-in via `--include-blocking`; Deferred explicit-only via `--rec-ids` | Filter logic | Selection |
| BR-003: Slash command never invokes gh | All gh-CLI invocations live in the skill | Architecture constraint | Phase 10 |
| BR-004: Failure Isolation | Continue processing remaining items on individual failures | Applied throughout | All phases |
| BR-005: Approval Required | NO posting may execute before user approves at skill Phase 4 (real or mock) | Enforced inside skill | Phase 10 |
| BR-006: Project-Scoped Drafts | Drafts written to `tmp/${STORY_ID}/drafts/` per operational-safety.md Rule 2 | Skill Phase 1 | Phase 10 |
| BR-007: Hardcoded Repo + Cross-Repo Guard | `bankielewicz/DevForgeAI` locked. EVERY gh-CLI invocation hardcodes `--repo bankielewicz/DevForgeAI`. Cross-repo confusion guard for parallel Claude sessions | In skill | Phase 10 |
| BR-008: Drafts Persist | No auto-cleanup of `tmp/${STORY_ID}/drafts/` — stay for inspection | Skill Phase 1 | Phase 10 |
| BR-009: Idempotency | Skill detects already-linked recs (real `Issue-N` OR mock `Issue-mock-N`) and routes to a SEPARATE `skipped.json` file (NEVER mixed into `posted.json`) | Skill Phase 1.5 | Phase 10 |
| BR-010: Classification Namespacing | REGRESSION → `classification:regression` label; PRE_EXISTING → `classification:pre-existing`. Always namespaced; bare tokens forbidden | Skill Phase 2.2 | Phase 10 |
| BR-011: Stable posted-mock Schema | `posted.json` is a SINGLE JSON object with always-present `posted: []` + `skipped: []` arrays; every entry has every field (use `null` for empty); `recommendation_id` (verbose, never `rec_id`) | Skill Phase 5 | Phase 10 |
| BR-012: Deterministic Issue Numbers (eval) | Mock issue numbers via `int(sha256(rec_id)[:7], 16) % 100000` — reproducible across eval runs | Skill Phase 5 (eval mode) | Phase 10 |
| BR-013: Always Preserve Section Structure | qa-recs-update output ALWAYS preserves all 3 canonical sections; empty sections get `_None._` | Skill Phase 6 | Phase 10 |
| BR-014: Audit Trail | Skill adds `last_posted_at` frontmatter + `## Posting Audit Trail` section per cycle. Append-only across cycles | Skill Phase 6 | Phase 10 |
| BR-015: ## Labels Body Section Mandatory | Every draft body MUST end with `## Labels` section; line content equals `", ".join(labels[])` byte-for-byte | Skill Phase 2.4 | Phase 10 |

---

## Open Questions Handling

When the embedded template detects a recommendation that can't be translated into a concrete issue without inventing scope, the skill records the issue under "Open Questions" instead of fabricating content. With QA recs (which are pre-structured by `/qa`), open questions are RARE — most fields are required by the schema and filled by the QA generator. Examples that DO trigger open questions:

- **Title exceeds 80 chars** — Skill rewrites to imperative ≤80 chars; the original is logged for the author's review
- **`category=anti_pattern` without `classification`** — Should be caught at parsing (BR-001), but if it slips through, skill flags it
- **`remediation_steps` empty AND no `before_code`/`after_code`** — Schema requires one or the other; if both absent, draft has empty AC checklist and skill logs the gap
- **Subjective verification.expected** — e.g., "behavior looks reasonable". Skill keeps the value but flags: "Replace with measurable assertion"

The user can choose at the approval gate (skill Phase 4): inspect drafts, cancel + edit QA recs file + re-run, or post anyway with the warnings in the body.

---

## Recovery Patterns

### Mid-batch posting failure (gh rate-limited)

**Scenario:** 7 of 10 issues posted, then gh rate-limit hits. Remaining 3 fail.

**State after run:**
- QA recs file has 7 `**Posted as:**` markers (Phase 11 processed only successful posts)
- `tmp/${STORY_ID}/drafts/` retains all 10 drafts (BR-008)
- Result array shows 7 success, 3 failed (with rate-limit error messages)

**Recovery:**
1. Wait for rate-limit reset.
2. Re-run `/create-incident-from-recommendations ${STORY_ID}`.
3. Skill Phase 1.5 (idempotency) detects the 7 already-linked recs and routes them to `skipped.json` per BR-009.
4. The 3 unlinked recs are drafted and posted.

### gh authentication expired mid-batch

Same pattern as rate-limit. Run `gh auth refresh`, re-invoke, idempotency handles the rest.

### Issue body too long (HTTP 422)

GitHub limits issue bodies to ~64KB. If a draft exceeds this, posting fails with HTTP 422.

**Recovery:**
1. Inspect the failing draft: `Read(file_path="tmp/${STORY_ID}/drafts/draft-${REC_ID}.md")`
2. Trim the rec in the QA recs file (e.g., shorten `before_code`/`after_code` blocks; move long evidence to `references[].url`).
3. Re-run. Skill Phase 1.5 idempotency routes already-linked items to `skipped.json`; the trimmed rec re-drafts shorter and posts.

### Label doesn't exist on repo

The skill caches `gh label list` once per invocation. If a recommendation needed a label not on the repo, the draft's `## Labels` section keeps the label string AND posting fails with "label X not found".

**Recovery options:**
- Create the missing label: `gh label create '<name>' -R bankielewicz/DevForgeAI -d "Description" -c hexcolor`
- Re-run; new label is in the cache.
- OR remove the failing label from the rec's classification/severity/category mapping — out of scope for in-flight runs.

### User cancels at approval gate

Picking "Cancel — post nothing" returns the result array with all entries marked `status: "cancelled"`. Phase 11 sees zero successful posts and HALTs gracefully — QA recs file is untouched.

### QA recs file edit fails in Phase 11

Edge case: QA recs file modified mid-workflow (e.g., another agent regenerated it).

**Behavior:** Edit returns an error. Slash command surfaces: "QA recs file changed during workflow. Issue posted (Issue-NNN) but file not updated. Manual marker needed: `**Posted as:** Issue-NNN — URL` under the rec's `id:` line."

The issue is already on GitHub (irreversible) — only the linking step failed. User adds the marker manually.

### Schema mismatch after upstream `/qa` upgrade

If `/qa` evolves the QA recs schema (new fields, renamed fields), this command's parser may surface "schema violations" for files generated under the new format.

**Recovery:**
1. Update `qa-recommendations-schema.json` reference and re-validate.
2. If a transitional period is needed, the skill's `schema_version` warning is non-blocking — the parser degrades gracefully.

---

## Edge Cases

| Edge Case | Behavior |
|-----------|----------|
| Missing QA recs file | HALT with hint to run `/qa STORY-NNN` first |
| Empty Advisory section, no `--include-blocking` | HALT with "no recs match filters" |
| User selects single rec via `--rec-ids` | Bypasses prompt; posts directly (still passes through skill approval gate) |
| Already-linked rec selected | Skill Phase 1.5 routes to `skipped.json`; no duplicate post |
| Rec with `source_rca:` pointer | Phase 11 also updates the RCA file with cross-reference |
| `category=documentation` rec (no `file`/`line`) | Allowed; whole-file scope; `## Files to change` reads "(documentation rec — no specific file)" |
| `remediation_steps` instead of `before_code`/`after_code` | Each step becomes one AC checklist item; `## Current behavior`/`## Required behavior` populated from rec narrative |
| Multiple QA cycles for same STORY | QA recs file is regenerated per cycle; `qa_cycle` frontmatter increments; skill Phase 1.5 handles cross-cycle idempotency |

---

## Implementation Reference Files

All detailed phase workflows are documented in dedicated reference files for maintainability and modularity.

| Phase | Component | File | Purpose |
|-------|-----------|------|---------|
| 1-5 | Parser | `references/create-incident-from-recommendations/parsing-workflow.md` | YAML loading + schema validation against `qa-recommendations-schema.json` |
| 6-9 | Selection | `references/create-incident-from-recommendations/selection-workflow.md` | Filter logic (--severity, --include-blocking, --rec-ids) + multi-select prompt |
| 10 | Issue Creator | `references/create-incident-from-recommendations/issue-creation-workflow.md` | Skill delegation contract |
| 11 | Linker | `references/create-incident-from-recommendations/linking-workflow.md` | QA recs file mutation: add `**Posted as:**` markers |

**Note:** All reference files are located at: `.claude/commands/references/create-incident-from-recommendations/`

---

## Cross-references

- **Skill that owns Phase 10:** `.claude/skills/github-incident-from-recommendations/SKILL.md`
- **Embedded template prompt:** `.claude/skills/github-incident-from-recommendations/assets/templates/Github-incident-template.md` (byte-identical to the RCA-pathway sibling's template)
- **Authoritative schema:** `src/claude/skills/spec-driven-qa/assets/schemas/qa-recommendations-schema.json`
- **Sibling command:** `/create-incident-from-rca` (same target repo, RCA-markdown source format, shared issue-body template)
- **Upstream producer:** `/qa STORY-NNN` (generates the QA recs file consumed here)
- **Constitutional context:** `devforgeai/specs/context/architecture-constraints.md` (Layer 1/2/3 rules — this command is Layer 3, the skill is Layer 1)

---

**Version:** 1.0 — Lean Orchestration Reference | **Created:** 2026-05-09
