# /create-incident-from-rca — Extended Reference Documentation

Supplementary documentation for the `/create-incident-from-rca` command. The command file contains core orchestration logic; this file contains detailed help, error templates, business rules, and recovery patterns.

---

## Full Help Text

```
/create-incident-from-rca — Convert RCA recommendations into GitHub issues

USAGE:
    /create-incident-from-rca RCA-NNN [--threshold HOURS]
    /create-incident-from-rca --help | help

ARGUMENTS:
    RCA-NNN         Required. RCA document ID (e.g., RCA-049). Case-insensitive.

OPTIONS:
    --threshold N   Filter recommendations with effort >= N hours
    --help, help    Display this help message

PROCESS:
    1. Parse RCA document and extract recommendations (delegates to spec-driven-stories --RCA)
    2. Filter by effort threshold and sort by priority
    3. Display summary table for interactive selection
    4. Multi-select recommendations to convert
    5. Delegate drafting + preview + approval + posting to github-incident-from-rca skill
    6. Skill posts approved drafts via `gh issue create`
    7. Update RCA document with Issue-NNN references for posted issues

REPO:
    Hardcoded to bankielewicz/DevForgeAI (per template line 1).
    Multi-repo support is out of scope.

RELATED COMMANDS:
    /rca                    Create new RCA document
    /create-stories-from-rca  Create user stories from RCA recs (instead of issues)
    /create-story           Create individual story
    /dev                    Start story implementation
```

---

## Error Message Templates

```
ERROR_MISSING_RCA_ID:
    "❌ RCA ID required"
    "Usage: /create-incident-from-rca RCA-NNN"
    "Available RCAs:"

ERROR_RCA_NOT_FOUND:
    "❌ RCA not found: ${RCA_ID}"
    "Available RCAs:"

ERROR_INVALID_FORMAT:
    "❌ Invalid RCA format"
    "Expected: RCA-NNN (where NNN are digits)"

ERROR_GH_NOT_AUTHENTICATED:
    "❌ gh CLI not authenticated"
    "Run: gh auth login"
    "Then re-invoke: /create-incident-from-rca ${RCA_ID}"

ERROR_GH_NOT_INSTALLED:
    "❌ gh CLI not found on PATH"
    "Install: https://cli.github.com"
    "Then re-invoke: /create-incident-from-rca ${RCA_ID}"

ERROR_REPO_INACCESSIBLE:
    "❌ Cannot access bankielewicz/DevForgeAI"
    "Check: gh repo view bankielewicz/DevForgeAI"
    "Possible causes: token lacks permission, network down, repo renamed"

ERROR_NO_RECOMMENDATIONS:
    "❌ No recommendations found in ${RCA_ID}"
    "Cannot create issues from an RCA with zero recommendations."
    "Verify the RCA has '### REC-N:' sections."

ERROR_ALL_FILTERED:
    "❌ All recommendations filtered out by --threshold ${HOURS}"
    "Lower the threshold or run without --threshold."
```

---

## Phase Orchestration Overview

```
┌─────────────────────────────────────────────────────────────────┐
│              /create-incident-from-rca Workflow                  │
│                  (4 Main Orchestration Phases)                   │
└─────────────────────────────────────────────────────────────────┘

Phase 1-5: RCA PARSING (delegated to spec-driven-stories --RCA)
  ├─ Input: RCA ID (e.g., RCA-049)
  ├─ Process: Parse document, extract recommendations
  ├─ Output: Structured recommendation list
  └─ Reference: parsing-workflow.md

       ↓

Phase 6-9: INTERACTIVE SELECTION
  ├─ Input: Parsed recommendations
  ├─ Process: Multi-select prompt, build selection array
  ├─ Output: selected_recommendations
  └─ Reference: selection-workflow.md

       ↓

Phase 10: DRAFT + APPROVE + POST (delegated to github-incident-from-rca skill)
  ├─ Input: selected_recommendations, RCA_ID, repo
  ├─ Process: Skill runs 6 internal phases (Setup, Drafting, Summary,
  │           Drill-down approval, Post, Result)
  ├─ Output: results array (rec_id, issue_number, issue_url, status)
  └─ Reference: issue-creation-workflow.md (contract)
                + ../../../skills/github-incident-from-rca/SKILL.md (skill)

       ↓

Phase 11: RCA-ISSUE LINKING
  ├─ Input: results array (from skill)
  ├─ Process: Update RCA file with Issue-NNN refs for successful posts
  ├─ Output: Updated RCA with traceability
  └─ Reference: linking-workflow.md
```

| Phase | Component | Owner | Role |
|-------|-----------|-------|------|
| 1-5 | RCA Parser | spec-driven-stories skill (--RCA) | Parse RCA and extract recommendations |
| 6-9 | Selection | This slash command | Interactive recommendation selection |
| 10 | Issue Creator | github-incident-from-rca skill | Draft, preview, approve, post issues |
| 11 | Linker | This slash command | Link issues back to RCA document |

---

## Business Rules & Constraints

| Rule | Constraint | Implementation | Phase |
|------|-----------|-----------------|-------|
| BR-001: Effort Threshold | Filter recommendations with effort ≥ threshold hours | Applied in parsing phase | Parsing |
| BR-002: Priority Sorting | Sort recommendations by priority: CRITICAL > HIGH > MEDIUM > LOW | Applied in parsing phase | Parsing |
| BR-003: Slash command never calls gh | All `gh` invocations live in `github-incident-from-rca` skill | Architecture constraint | Phase 10 |
| BR-004: Failure Isolation | Continue processing remaining items on individual failures | Applied throughout | All Phases |
| BR-005: Approval Required | NO `gh issue create` may execute before user approves at skill Phase 4 | Enforced inside skill | Phase 10 |
| BR-006: Case Normalization | Accept case-insensitive RCA IDs (rca-049 → RCA-049) | Applied in argument parsing | Parsing |
| BR-007: File Existence | Verify RCA file exists before processing | Check in argument parsing | Parsing |
| BR-008: Hardcoded Repo | bankielewicz/DevForgeAI is locked | In skill | Phase 10 |
| BR-009: Idempotency | Detect already-linked recs; prompt user before duplicating | Skill Phase 1.5 | Phase 10 |

---

## Open Questions Handling

When the embedded template detects a recommendation that can't be translated into a concrete issue without inventing scope, the skill records the issue under "Open Questions" instead of fabricating content. Examples:

- **Recommendation says "explore options for caching"** — too vague for a concrete issue. Skill records: "REC-N specifies 'explore caching options' — too vague to translate. Specify: which caching layer (request, query, response)? Eviction policy? Time-to-live target?"
- **Recommendation lists no files** — issue would have empty "Files to change". Skill records: "REC-N has no file list. Add concrete file paths to RCA before reposting."
- **Subjective acceptance criterion** — e.g., "code is more maintainable". Skill strips it and records: "Subjective AC stripped. Replace with measurable criterion (cyclomatic complexity ≤ N, test coverage ≥ X%)."

**The user can choose at the approval gate (skill Phase 4):**
- Inspect drafts to read the open questions, decide whether to address them in the RCA before posting
- Cancel the run, edit the RCA, re-run
- Post anyway (issues with unresolved open questions get a warning in the body)

---

## Recovery Patterns

### Mid-batch posting failure

**Scenario:** 7 of 10 issues posted, then `gh` rate-limited. Remaining 3 fail.

**State after run:**
- RCA file has 7 issues linked (Phase 11 processed only successful posts)
- `tmp/${RCA_ID}/drafts/` retains all 10 drafts (BR-008: drafts persist)
- Result array shows 7 success, 3 failed (with rate-limit error messages)

**Recovery:**
1. Wait for rate-limit reset (usually shown in the error message — `X-RateLimit-Reset` header).
2. Re-run `/create-incident-from-rca ${RCA_ID}`.
3. Skill Phase 1.5 (idempotency) detects the 7 already-linked recs and prompts: "7 of 10 selected recs are already linked to issues. Skip them and post only the remaining 3? (Recommended)"
4. Pick "Skip already-linked". Skill posts only the 3 unlinked recs.

### gh authentication expired mid-batch

Same pattern as rate-limit. Run `gh auth refresh`, re-invoke, skip already-linked.

### Issue body too long (HTTP 422)

GitHub limits issue bodies to ~64KB. If a draft exceeds this, posting fails with HTTP 422.

**Recovery:**
1. Inspect the failing draft: `Read(file_path="tmp/${RCA_ID}/drafts/draft-${REC_ID}.md")`
2. Trim the source recommendation in the RCA file (e.g., move long evidence sections to the RCA's Evidence section, leaving only a summary in the recommendation).
3. Re-run. Skill Phase 1.5 will offer to skip the already-linked items; pick that. The trimmed rec re-drafts shorter and posts.

### Label doesn't exist on repo

The skill caches `gh label list` once per invocation. If a recommendation needed a label not on the repo, the draft's `## Labels` section is empty AND an Open Question is logged: "Label '<name>' doesn't exist. Create with `gh label create '<name>'` or remove from this issue."

**Recovery options:**
- Create the missing label: `gh label create '<name>' -R bankielewicz/DevForgeAI -d "Description" -c hexcolor`
- Re-run the workflow; the new label will be in the cache and applied
- OR post without the label (skill posts with the empty `## Labels` line; user can add the label manually on the issue afterward)

### User cancels in the middle of inspection (Phase 4.3)

If the user has been inspecting drafts and changes their mind, picking "Cancel — post nothing" returns the result array with all entries marked `status: "cancelled"`. Phase 11 (linking) sees zero successful posts and HALTs gracefully — RCA is untouched.

### RCA file edit fails in Phase 11

Edge case: the RCA file has been modified since Phase 1 (e.g., another agent edited it). The exact-string `Edit` would fail because the line "before" image no longer matches.

**Behavior:** Edit tool returns an error. The slash command surfaces it: "RCA file changed during workflow. Issue posted (Issue-NNN) but RCA not updated. Manual link needed: `- [ ] REC-N: See Issue-NNN`"

The issue is already on GitHub (irreversible) — the failure is in the linking step only. The user adds the link manually.

---

## Edge Cases

| Edge Case | Behavior |
|-----------|----------|
| Missing frontmatter | Extract ID from filename, log warning |
| No recommendations | HALT — cannot create issues from zero recs |
| All filtered out | HALT — "No recommendations meet threshold" |
| Invalid REC ID in selection | Log warning, ignore that selection |
| Single recommendation in RCA | Still display selection prompt (allow cancel) |
| User selects "Other" with custom REC IDs | Parse comma-separated list |
| All selected recs already linked | Skill Phase 1.5 prompt; user picks repost / skip / cancel |
| User cancels at approval gate | All selected recs marked status: cancelled; RCA untouched |
| Network drops mid-post | Successful posts linked; failed retried via re-run |

---

## Implementation Reference Files

All detailed phase workflows are documented in dedicated reference files for maintainability and modularity.

### Phase Reference Files

| Phase | Component | File | Purpose |
|-------|-----------|------|---------|
| 1-5 | RCA Parser | `references/create-incident-from-rca/parsing-workflow.md` | RCA parsing, extraction, filtering algorithm (delegates to spec-driven-stories) |
| 6-9 | Selection | `references/create-incident-from-rca/selection-workflow.md` | Interactive user selection process |
| 10 | Issue Creator | `references/create-incident-from-rca/issue-creation-workflow.md` | Skill delegation contract (slash command → github-incident-from-rca skill) |
| 11 | Linker | `references/create-incident-from-rca/linking-workflow.md` | RCA document update with Issue-NNN refs |

**Note:** All reference files are located at: `.claude/commands/references/create-incident-from-rca/`

---

## Cross-references

- **Skill that owns Phase 10:** `.claude/skills/github-incident-from-rca/SKILL.md`
- **Embedded template prompt:** `.claude/skills/github-incident-from-rca/assets/templates/Github-incident-template.md`
- **Sister command:** `/create-stories-from-rca` (same parsing + selection mechanics, different downstream artifact)
- **Constitutional context:** `devforgeai/specs/context/architecture-constraints.md` (Layer 1/2/3 rules — this command is Layer 3, the skill is Layer 1)

---

**Version:** 1.0 - Lean Orchestration Reference | **Created:** 2026-05-05
