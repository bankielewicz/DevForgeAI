---
name: create-incident
description: Create a GitHub incident from a spontaneous observation — a bug or enhancement discovered live during active work
argument-hint: "<observation text> [--type=bug|enhancement] [--severity=critical|high|medium|low] [--work=<context>] [--related=<refs>] [--eval] [--help]"
model: opus
allowed-tools: AskUserQuestion, Skill, Bash(devforgeai-validate:parse-incident-args)
---

# /create-incident — Create a GH Incident from a Spontaneous Observation

File a single, template-conformant GitHub issue in bankielewicz/DevForgeAI from an **inline
description** of a bug or enhancement you found while working — the case the four
source-document-driven pathways (`/create-incident-from-{rca,recommendations,feedback,queue}`)
cannot serve, because a live observation has no upstream document. This command parses the
observation and delegates drafting + preview + approval + posting to the
`github-incident-from-observation` skill.

**Component Orchestration:** Parse → Confirm → Draft+Approve+Post (skill)

**Architectural constraint:** This command never calls `gh` directly. All GitHub issue-creation
logic is owned by the `github-incident-from-observation` skill. The slash command is a thin
orchestrator (this is a locked three-layer rule: commands delegate to skills; only the skill
touches the posting path).

**Sibling pathways:** `/create-incident-from-rca`, `/create-incident-from-recommendations`,
`/create-incident-from-feedback`, `/create-incident-from-queue`. All share the byte-identical
`Github-incident-template.md` asset but consume different inputs; this one consumes a free-text
observation.

**Authorizing ADR:** ADR-077.

---

## Usage

```bash
/create-incident "When /create-story runs without a STORY_ID arg it silently writes .story.md instead of halting" --type=bug
/create-incident "Add a Phase-03 exit gate that blocks completion unless a worktree exists for the issue" --type=enhancement
/create-incident "<observation>" --type=bug --work="STORY-661 /dev Phase 04" --related="#399, ADR-077"
/create-incident "<observation>" --type=enhancement --eval        # dry run, no real posting
/create-incident --help
```

`--type=` is the issue label class (`bug` | `enhancement`). `--work=` records the originating
work for the issue's Provenance. `--related=` records cited issues/ADRs/commits. `--eval` runs
the skill in mock mode (no authentication, no real issue, deterministic mock URL on the
RFC-2606 `.invalid` TLD) for safe testing.

---

## Phase 1 — Help gate

```
# Run the deterministic arg parser ONCE (issue #712) — do NOT inline $ARGUMENTS into prose.
PARSED = JSON from: printf '%s' "$ARGUMENTS" | devforgeai-validate parse-incident-args
IF PARSED.help == true OR trim($ARGUMENTS) == "" OR trim($ARGUMENTS) == "help":
    Display: "Usage: /create-incident \"<observation text>\" [--type=bug|enhancement] [--work=<context>] [--related=<refs>] [--eval]"
    Display: "  <observation text>  Free-text description of the bug or enhancement (>= 20 chars)."
    Display: "  --type=             bug | enhancement (prompted if omitted)."
    Display: "  --work=             Originating work for the issue's Provenance (optional)."
    Display: "  --related=          Issues / ADRs / commits the observation cites (optional)."
    Display: "  --eval              Dry run — no gh auth, no real issue, deterministic mock."
    HALT
```

(An empty invocation falls through to the Phase 3 prompt rather than HALTing only when the
user explicitly wants interactive entry; `--help`/`help`/bare-empty show usage and stop.)

---

## Phase 2 — Argument parsing

```
# Consume the parser JSON (issue #712). The former emulated prose parsing was the leak source:
# a long or multiline $ARGUMENTS was substituted verbatim into every pseudocode line.
PARSED = JSON from: printf '%s' "$ARGUMENTS" | devforgeai-validate parse-incident-args
EVAL_MODE     = PARSED.eval            # bool
TYPE_FLAG     = PARSED.type            # "bug" | "enhancement" | ""
SEVERITY_FLAG = PARSED.severity        # "critical" | "high" | "medium" | "low" | ""
WORK_FLAG     = PARSED.work            # optional free text (quoted values unquoted by the helper)
RELATED_FLAG  = PARSED.related         # optional free text
OBSERVATION_TEXT = PARSED.observation_text   # residual free text; newlines/length preserved verbatim
```

The helper uses a trailing-flags, byte-preserving tokenizer: only a contiguous trailing run of
`--type=`/`--severity=`/`--work=`/`--related=`/`--eval`/`--help` tokens is parsed; everything before it is
`observation_text`, preserved byte-for-byte (a `--type=` inside the body is retained, not extracted).

---

## Phase 3 — Observation + type resolution

```
IF OBSERVATION_TEXT is empty:
    AskUserQuestion →
        question: "What did you observe? Describe the bug or enhancement you found (>= 20 chars)."
        # Map the free-text answer to OBSERVATION_TEXT.

IF TYPE_FLAG not empty AND TYPE_FLAG not in {"bug", "enhancement"}:
    Display: "❌ Invalid --type: ${TYPE_FLAG}. Expected: bug | enhancement"
    HALT

IF TYPE_FLAG is empty:
    AskUserQuestion →
        question: "What type of incident is this?"
        header:   "Type"
        options:
          - "bug — something is broken, wrong, or crashing"
          - "enhancement — a new gate, lint, or capability to add"
    TYPE_FLAG = (mapped to "bug" | "enhancement")
```

---

## Phase 4 — Confirmation display

```
Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "  /create-incident — filing a ${TYPE_FLAG} observation"
  "  Observation: ${OBSERVATION_TEXT[:100]}${'…' if len > 100 else ''}"
  IF WORK_FLAG:    "  Work context: ${WORK_FLAG}"
  IF RELATED_FLAG: "  Related: ${RELATED_FLAG}"
  IF EVAL_MODE:    "  Mode: EVAL (no real GitHub interaction)"
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Phase 5 — Delegate to the skill

```
Skill(command="github-incident-from-observation", args="${'--eval' if EVAL_MODE else ''}")
```

Inputs passed via shared context:
- `observation_text`  = OBSERVATION_TEXT
- `label_type`        = TYPE_FLAG
- `severity`          = SEVERITY_FLAG (or empty → skill prompts via AskUserQuestion / defaults medium in --eval)
- `originating_work`  = WORK_FLAG (or empty → skill defaults to "active session")
- `related`           = RELATED_FLAG (or empty → skill writes "None")

The skill owns drafting, the full preview, the approval gate (nothing posts before explicit
approval), and the posting path. It returns a single-element `results` array.

---

## Phase 6 — Final summary

```
r = results[0]
IF r.status == "success":
    Display: "✅ Issue filed: Issue-${r.issue_number} — ${r.issue_url}"
ELIF r.status == "cancelled":
    Display: "Cancelled. Draft saved to tmp/${r.obs_id}/drafts/ for later."
ELIF r.status == "skipped":
    Display: "⏭ Skipped: ${r.error_message}"
ELSE:
    Display: "❌ Failed: ${r.error_message}"
```

---

## Success Criteria

- The observation is parsed (or interactively gathered) and a `bug`/`enhancement` type is
  resolved before any delegation.
- The skill is invoked exactly once via `Skill(command="github-incident-from-observation")`;
  this command performs no file I/O and no posting itself.
- No posting occurs before the skill's explicit-approval gate.
- The command never calls `gh` directly (only the skill does) — the locked three-layer rule.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No observation text | Phase 3 AskUserQuestion gathers it interactively. |
| Invalid `--type` value | HALT in Phase 3 with the expected values. |
| `gh` not authenticated | The skill HALTs in its Phase 1.3 → run `gh auth login`. |
| Observation already filed | The skill's Phase 1.5 idempotency check offers skip / re-post / cancel. |
| Want a dry run | Pass `--eval` — the skill mocks the post (no real GitHub interaction). |
