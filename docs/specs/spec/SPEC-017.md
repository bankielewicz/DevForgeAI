---
id: SPEC-017
type: spec
title: "UI skill (MVP): record a release's screen designs from committed boards"
status: draft          # draft | in-review | approved | superseded | deprecated
version: 1
created: 2026-10-09
updated: 2026-10-09
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-sonnet-5-5"
  session: "7637882f-b2ec-465e-988a-9602340d1023"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 13, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 13, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 13, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "the workflow chain, which ADR-007 extends with this step"}
  - {id: ADR-007, relation: informed_by, version: 1, hash: null, note: "proposed: the chain step, the DSN and the committed boards this skill implements; becomes constrains when ADR-007 is accepted (SPEC-009 v1 handled ADR-004 the same way)"}
  - {id: ADR-004, relation: informed_by, version: 2, hash: null, note: "D2: front-end.md keeps the conventions and the design system, ui-mockups.md indexes approved story designs; a CLI is a user interface; D6: suspect links"}
  - {id: PRD-001, item: FR-023, relation: informed_by, version: 13, hash: null, note: "the requirement this skill implements; no story specifies it yet"}
  - {id: PRD-001, item: FR-003, relation: informed_by, version: 13, hash: null, note: "decisions stay the user's: every mapping and the approval"}
  - {id: PRD-001, item: FR-004, relation: informed_by, version: 13, hash: null, note: "the hand-off names the next step and says when it is not available"}
  - {id: SPEC-001, relation: informed_by, version: 17, hash: null, note: "the BRN this skill reads: its item blocks and the promoted disposition"}
  - {id: SPEC-002, relation: informed_by, version: 5, hash: null, note: "the create-or-extend gate, the unconverged-BRN gate, the null-until-confirmed rule and the validation loop this skill follows"}
  - {id: SPEC-004, relation: informed_by, version: 4, hash: null, note: "§2: no policy resolution while PRD-001 FR-012 is later; this skill follows"}
  - {id: SPEC-009, relation: informed_by, version: 3, hash: null, note: "story-level design stays with the story skill (BEH-11, BEH-12)"}
  - {id: SPEC-013, relation: informed_by, version: 28, hash: null, note: "BEH-02: a plugin skill is tracked unless its metadata says otherwise; this skill is tracked, by ticks only"}
supersedes: []
superseded_by: null
blocked_by: [ADR-007]
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/ui", "src/tests/ui", "src/claude/DevForgeAI/evals/ui", "src/schemas/design.schema.json"]
---

# SPEC-017 — UI skill (MVP): record a release's screen designs from committed boards

> **Version 1, draft, 2026-10-09.** Cycle A of four (ADR-007): documents only. Drafted from Bryan's decisions of 2026-10-08
> and 2026-10-09 and the Krepion session's spec page "A UI Skill for DevForgeAI" (version 6), which §13 lists. It implements
> ADR-007, which is proposed, so this spec is blocked until ADR-007 is accepted. Nothing is built. Every choice that the
> page or Bryan's words don't settle is in §13, for his accept or challenge.

## 1. Overview

The `ui` skill ships in the `devforgeai` plugin and is invoked as `/devforgeai:ui [BRN-NNN]`. It records a release's screen
designs, graphical and terminal alike, as one **design document** (DSN) at `docs/specs/design/DSN-NNN.md`. The user draws the
boards in Claude Design and copies them into the repository; the skill reads the committed copy, never the canvas. It sits
after the brainstorm and before the PRD (ADR-007 D1):

- it reads the converged brainstorm (BRN) and its **promoted ideas**;
- it reads the boards by contract: `docs/specs/design/DSN-NNN/boards/canvas.json`, then each board file it names;
- it drafts which board belongs to which **flow**, which **surface** (`web`, `desktop`, `mobile` or `terminal`) and which
  promoted ideas it shows, asks the user to confirm every mapping, and writes the DSN;
- it checks the DSN with a bundled script and reports;
- it hands off to the PRD, whose section 8 links the DSN instead of a raw canvas URL.

A second run for the same brainstorm **amends** the DSN: boards changed, were added or removed, or a PRD requirement, an
accepted ADR's consequence or the brainstorm itself now names a screen (the four Krepion cases, ADR-007). The three triggers,
each with a worked example, are in §6 ("The amend path"). An amend run bumps the DSN's version, which makes it a suspect
upstream for the documents that cite it (§2). In every case the user draws in Claude Design and copies the boards into the
repository again: the skill sees only the committed copy, so a board changed on the canvas and not copied again never reaches
it.

Four rules shape everything else:
- **It decides nothing the user didn't.** A flow, a surface, an idea mapping and a canvas fact are written only when the
  user supplied or confirmed them; otherwise they are `null` with a marker. Approval needs the user's explicit words and a
  named approver (BEH-16).
- **It reads files, not the canvas.** No network, no `/design`, and no interface to Claude Design (SPEC-009 §2). A
  missing, unreadable or unknown-format copy stops the run with a clear message (ERR-03 to ERR-06).
- **One slot, re-runnable.** One active DSN per brainstorm; the amend path is the second look (ADR-007 D4).
- **It writes only its own document.** The PRD, the architecture description (ARCH), the context documents, the stories
  and the boards are read-only (BEH-19). A bumped DSN is a suspect upstream, and each owning skill re-reviews it
  (ADR-007 D5); this skill names who, and starts none of them.

The skill is recorded as `SKL-013` in its `provenance.yaml`.

Bryan, 2026-10-08: "release-design-ui-mockups is too long. stick with ui-mockups or ui", then "ui (Recommended)". Bryan,
2026-10-09: "UI will cover terminal screens such as CLI as i previously found it more useful than claude designing without
claude design. claude design is so much nicer. our command will be /devforgeai:ui not /design". `/design` is Claude Code's
built-in command and is not this skill.

## 2. Constraints

- **PRD-001 NFR-001 to NFR-003** (v13): a `SKILL.md` of at most 500 lines and a description of at most 1024 characters,
  spec-only frontmatter with provenance in the sidecar, and an eval suite at 0.8 per case over 3 runs against the
  no-plugin baseline (QR-01 to QR-04), unless Bryan records a waiver in §9.
- **ADR-001** (v4): built in a worktree from `src/claude/DevForgeAI/`; the owner deploys; evals run from a plain terminal.
- **ADR-007 (proposed):** the chain step (D1), the DSN (D2), the boards read by contract (D3), one slot with an amend path
  (D4), the suspect-upstream duty (D5), story-level design left to SPEC-009 (D6) and the user's decisions (D7).
- **ADR-004 D2:** `front-end.md` keeps the conventions, including the design system and, for a CLI, "command structure, flags,
  output formats"; `ui-mockups.md` holds the design-system reference and the index of approved story designs. The DSN holds
  the screen designs and no tokens (§13, a).
- **No policy resolution.** PRD-001 FR-006 to FR-008 cover only the prd and Architecture Definition workflows, and FR-012
  (release later) covers the rest; SPEC-004 §2 and SPEC-009 §2 already decline to resolve policy for the same reason. This
  skill resolves no policy (no R1 to R5, no resolution line), copies neither `policy.md` nor `defaults.md`, and has no
  `interview.max_calls`: the interview is bounded by its structure (BEH-09). §13 (f) records the alternative.
- **Decisions stay the user's** (PRD-001 FR-003): the mappings and the approval (BEH-09, BEH-16).
- **The progress tracker** (SPEC-013 v28, BEH-02): the skill is tracked like prd, epic and context: no
  `devforgeai-tracked` key, no manifest (manifests for the other skills are SPEC-012 §11's later work), so its runs are
  tracked by ticks only. Its numbered checklist in `SKILL.md` is what the tracker reads (§5).
- **Standard library only** for the bundled script, which runs under `python3 -S` (like `validate_brn.py`, `find_spec.py` and
  `check_handoff.py`). It needs no PyYAML or jsonschema (IF-01 to IF-03).
- **Out of scope:**
  - drawing a board, calling `/design`, or fetching from the canvas;
  - story-level design: the story skill's gate and design record (SPEC-009 BEH-11, BEH-12);
  - editing any PRD, ARCH, ADR, context document, story or spec (BEH-19);
  - the neighbours' changes (the brainstorm hand-off, the PRD's section 8, the architecture evidence and report, the context
    re-review), which are cycle C and specified in SPEC-001, SPEC-002, SPEC-003 and SPEC-011 (§10);
  - the research step: the user said the research "will be slated for another skill";
  - sizing the design work, rendering a board, or reviewing a board's look.

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/ui/
├── SKILL.md                    # the checklist (BEH-01 to BEH-20), the user's decisions, the output contract
├── provenance.yaml             # SKL-013, implements SPEC-017
├── scripts/
│   └── dsn_check.py            # IF-01 next, IF-02 boards, IF-03 check; standard library only
├── references/
│   ├── interview.md            # what is asked, in what batches, with which options (BEH-09)
│   ├── boards.md               # the canvas.json contract and how a board file is read (DM-04, BEH-06)
│   └── output-rules.md         # frontmatter, board items, the coverage table, the self-check list (§4)
└── assets/
    └── dsn.md                  # the DSN template (DM-01)
src/schemas/design.schema.json                  # the DSN's JSON Schema (this change, cycle A)
src/claude/DevForgeAI/evals/ui/<case>/          # one case per automated VER item (§9), generated in cycle B
src/tests/ui/                                   # test_dsn_check.py, test_structure.py, make_evals.py; not deployed
```

```mermaid
flowchart LR
    A[Argument BEH-02] --> R[Read the BRN BEH-03]
    R --> C[Create or amend BEH-04]
    C --> N[ID and boards folder BEH-05]
    N --> B[Read the boards BEH-06]
    B --> M[Amend inputs BEH-07 BEH-08]
    M --> Q[Draft, then confirm BEH-09 to BEH-11]
    Q --> W[Write BEH-12 to BEH-14]
    W --> V[Check with dsn_check.py BEH-15]
    V --> K[Approval, explicit only BEH-16]
    K --> H[Report and hand off BEH-17 BEH-18]
```

## 4. Data model

**The project root** is the folder the session started in. Every path below is relative to it.

**Inputs,** all read by contract. None is edited except the DSN this skill writes:
- **The BRN:** `docs/specs/brainstorm/BRN-NNN.md`: its `status`, `version`, `owner` and `title`, its `ideas` item block (only
  `disposition: promoted` ideas count) and, for context, its `problems` and `assumptions`.
- **The existing DSNs:** `docs/specs/design/DSN-*.md`, for create or amend (BEH-04), the next free number (IF-01) and, in an
  amend run, the document being amended.
- **The boards:** `docs/specs/design/DSN-NNN/boards/`, where `DSN-NNN` is the DSN's own ID (DM-04). The skill reads
  `canvas.json` and each board file it names, and nothing else in the folder.
- **In an amend run only:** the PRDs in `docs/specs/prd/` (requirements that name a screen, a flow or a user interface),
  the accepted ADRs in `docs/specs/adr/` (consequences that do), and the documents under `docs/specs/` whose `upstream`
  cites the DSN (BEH-07), all read-only.

**Outputs:** `docs/specs/design/DSN-NNN.md`, from `${CLAUDE_SKILL_DIR}/assets/dsn.md`. Nothing else is written.

**The ID.** A create run's ID is the next free number: one more than the highest number among the `DSN-NNN.md` files in
`docs/specs/design/` of any status, `DSN-001` when there is none (IF-01 prints it). The user copies the boards into the
folder of that number before the run (ERR-03 names it). A folder under `docs/specs/design/` whose number has no `DSN-NNN.md`
is a **pending boards folder**; it matters only when it isn't the next free number (ERR-03 lists it).

**DM-01. The DSN document.** Frontmatter, in this order: the common keys (`id`, `type: design`, `title`, `status`, `version`,
`created`, `updated`, `owner`, `authors`, `generated_by`, `reviewed_by`, `approved_by`, `approved_on`, `upstream`,
`supersedes`, `superseded_by`, `blocked_by`), then the design-specific keys:

| Key | Holds |
|---|---|
| `canvas` | The Claude Design canvas URL (`https://…`) the boards were copied from, or `null` until the user gives it |
| `canvas_version` | The canvas version identifier of the copy now in `boards/`, as the user gives it (for example `1791493650-acf3`), or `null`. Never carried over from an earlier copy (BEH-10) |
| `canvas_format` | The `v` of the copied `canvas.json` (an integer; DM-04), read by the script, never asked |
| `boards_root` | `docs/specs/design/DSN-NNN/boards/` for this document's own ID |

Frontmatter values the skill sets:
- **`title`:** the BRN's title followed by `: release design`, unless the user gives another. **`owner`:** the BRN's owner, unless
  the user names another. **`authors`:** the owner and `"claude-code"`.
- **`status`:** `draft` for a new document; the rules of BEH-13 and BEH-16 otherwise. The skill never sets `superseded` or
  `deprecated`: those are the user's.
- **`generated_by`:** the tool, model and session as the host provides them (BEH-20). **`reviewed_by`:** `[]`.
  **`approved_by`:** `""` and **`approved_on`:** `null` until BEH-16. **`supersedes`:** `[]`, **`superseded_by`:** `null`,
  **`blocked_by`:** `[]`. Every `hash` is `null`.
- **`upstream`:** one `derives` link to the BRN, with no `item`, at the BRN's version; and one `derives` link with `item:
  IDEA-NN` to the same BRN and version for each distinct idea that an active board names (§13, o). It holds no link to a PRD or
  an ADR (§13, w).

The body, in this order, with these headings (the template `assets/dsn.md` holds them):

| Heading | Holds |
|---|---|
| `## 1. Scope` | Two to four sentences: the product or release the design covers (from the BRN's title and context), the flows and the surfaces that appear. No claim the user didn't confirm |
| `## 2. Boards` | The `yaml items` block `boards:` (DM-02) |
| `## 3. Idea coverage` | The table of DM-03 |
| `## 4. Canvas` | Where the boards were copied from (the `canvas` and `canvas_version` values, or the marker), the date of the copy when the user gave it, and the re-copy rule: a new copy means a new run, which amends this document |
| `## 5. Open questions` | One `[NEEDS CLARIFICATION: …]` bullet for each marker the document holds outside a board's `notes`, or `None.` |
| `## Change Log` | Rows `Version \| Date \| Author \| Change \| Items affected`, one at least for each version |

**DM-02. A board item,** in the `boards:` block, one for each board `canvas.json` names, in its order, then (after an amend) any
board added later, appended:

| Field | Holds |
|---|---|
| `id` | `BRD-NN`, two digits, allocated in order from `BRD-01`, never renumbered or reused |
| `status` | `active`, or `deprecated` for a board that left the canvas (never deleted) |
| `superseded_by` | Optional: the `BRD-NN` of the board that replaces a deprecated one, when the user says so |
| `file` | The board's file name, as `canvas.json` names it: a plain name, no `/`, `\` or `..` |
| `title` | A short name for the screen: the name the user confirmed (proposed from the board, BEH-06), else the board's file name without its extension |
| `flow` | The user's flow for the board, a lowercase slug (`day-to-day`), or `null` until confirmed |
| `surface` | `web`, `desktop`, `mobile` or `terminal`, or `null` until confirmed (BEH-11) |
| `ideas` | The promoted BRN ideas the board shows, as `IDEA-NN`: a list, `[]` when the user confirmed none, `null` until confirmed |
| `answers` | The PRD requirements and accepted ADRs the board answers, written `PRD-NNN#FR-NNN`, `PRD-NNN#NFR-NNN` or `ADR-NNN`: a list, `[]` when none. Plain text, not links: no version, and nothing in `upstream` (§13, w). Written only for a candidate the user confirmed (BEH-07, BEH-09) or a reference the user states |
| `sha256` | The SHA-256 of the board file's bytes at the run that wrote the item, from the script (IF-02) |
| `notes` | Free text, or `null`; it holds the marker for each `null` field of the item |

**DM-03. The idea coverage table** (section 3): `| Idea | Boards | Status |`, one row for each promoted idea of the BRN, in idea
ID order, the `Boards` cell listing the active `BRD-NN` items that name it (or `none`), and `Status` one of:
- `designed`: the BRN promotes the idea and at least one active board names it;
- `not a screen`: the user confirmed that no board is needed (the idea names no screen, flow or user interface);
- `no board yet`: the idea names a screen, a flow or a user interface and no board shows it; section 5 holds a marker for it;
- `withdrawn`: the idea was promoted when an earlier version listed it and the BRN's disposition for it no longer is (BEH-08);
  its `Boards` cell lists the active boards that still name it, or `none`.

**DM-04. The copied canvas: `canvas.json` and the board files.** The script (IF-02) reads, and the skill relies on, only
this part of Claude Design's undocumented format:
- `canvas.json` is a UTF-8 JSON object. Its member **`v`** is an integer, and **3** is the only value this spec supports (the
  copy of canvas version `1791493650-acf3` that the Krepion session made had `v` 3; ERR-05).
- Its member **`boards`** is an object whose keys are the board file names, in the order the file writes them; each value is
  ignored. That order is the canvas order.
- Every other member (`attachments`, a board's `expand` or `h`) is ignored, and nothing is inferred from it.
- The folder is a snapshot. The skill never learns that the canvas changed: a board edited on the canvas and not copied into
  `boards/` again is invisible to it, and the version the report prints is the copy's, never the canvas's current one.
- Each board file named lies in the same folder as `canvas.json`, is a regular file (not a symbolic link) and is readable. A
  `boards/README.md` that lists digests, or any file `canvas.json` doesn't name, is never read (§13, b).
- A board file is read as text with Read, its first 150 lines, which is enough for its heading and structure (§13, m). The
  title is proposed from the first `<title>`, `<h1>` or `<h2>` text in those lines, else from the file name without its
  extension, and the proposal is written only when the user confirms it (DM-02).

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: ui
description: Records a DevForgeAI project's screen designs as a design document (DSN) in docs/specs/design/, from a converged brainstorm and design boards the user has committed as files, for graphical and terminal or command-line screens alike. Maps each board to a flow and to the brainstorm ideas it shows, asks the user to confirm every mapping, never fetches from the design canvas, and amends the DSN when a later change names a screen. Use after the brainstorm and before the PRD when ideas name a screen, a flow or a user interface, when the user asks to record, add or update the UI design, mockups, boards or screens of a release, or when a PRD requirement or an ADR names a screen the design lacks. Not for one story's design, drawing boards, or general UI advice.
argument-hint: "[BRN-NNN]"
metadata:
  devforgeai-id: "SKL-013"
  devforgeai-version: "<SKL-013's provenance.yaml version, quoted>"
```

- **The name must be exactly `ui`,** lowercase, so the command is `/devforgeai:ui`. It is not `/design`, which is Claude Code's
  built-in command, and not `ui-mockups`, which collides with `ui-mockups.md` (CTX-017). The skill takes no `devforgeai-tracked`
  key: it is tracked (§2).
- **The version isn't fixed here.** `metadata.devforgeai-version` must equal `provenance.yaml`'s `version`.
- **Arguments:** `$ARGUMENTS` is one BRN ID (`BRN-NNN`) or empty (BEH-02). A file path is refused (ERR-02).
- **Tools:**
  - **reading:** Read, plus Glob and Grep when available; otherwise `ls` on explicit paths under `docs/specs/`. Never the
    whole repository, and no code inspection;
  - **writing:** Write for a new DSN and Edit for an existing one, only `docs/specs/design/DSN-NNN.md`;
  - **Bash:** only `python3 ${CLAUDE_SKILL_DIR}/scripts/dsn_check.py` with the subcommands below, and that `ls`;
  - **AskUserQuestion:** at most 4 questions per call, 2 to 4 options each, the recommended option first and marked
    "(Recommended)". When it isn't available, ask in plain text and end the turn.
- **"Proceed without questions":** a request that says so asks nothing in the run (BEH-09); it never answers the gates (BEH-02,
  BEH-03, ERR-07, ERR-10).
- **The checklist** in `SKILL.md`'s Workflow section, which the tracker reads (SPEC-012 §1):

  ```
  - [ ] 1. Select the BRN; create when no DSN cites it, amend when one does
  - [ ] 2. Read the BRN and the boards (amend: the PRD and the ADRs too)
  - [ ] 3. Interview: confirm each mapping
  - [ ] 4. Write DSN-NNN (amend: version +1, a Change Log row)
  - [ ] 5. Validate (at most three repair cycles)
  - [ ] 6. Approval, only on the user's explicit words
  - [ ] 7. Report and hand off to /devforgeai:prd BRN-NNN
  ```

- **`scripts/dsn_check.py`** is standard library only and runs under `python3 -S`. It writes no file and opens no network
  connection, follows no symbolic link, and reads only the paths each subcommand names. Output is on standard output; exit 0
  is success, 1 a problem it reports, and 2 that it can't run (no or wrong arguments, a project root it can't read, or a BRN
  it can't read), with `Cannot run: <reason>.` and nothing else.

  | Item | Command | Behaviour |
  |---|---|---|
  | IF-01 | `dsn_check.py next [--root DIR]` | Prints `next: DSN-NNN` (§4: one more than the highest `docs/specs/design/DSN-NNN.md` number, `DSN-001` with none) and `pending boards folders: <DSN-NNN, …> \| none`. Reads only the names in `docs/specs/design/`. Exit 0 |
  | IF-02 | `dsn_check.py boards [--root DIR] DSN-NNN` | Checks `docs/specs/design/DSN-NNN/boards/` against DM-04 and prints, on success, `canvas.json: v<N>, <n> boards`, one line `board <k> <file> <bytes> <sha256>` for each board in canvas order, and `boards: ok` (exit 0). On a problem it stops at the first failing of ERR-03, ERR-04, ERR-05 and ERR-12, in that order, and prints one line `ERR-NN: <message>`; otherwise it prints one such line for every board that fails ERR-06; then `boards: <n> problem(s)` (exit 1). The ERR-03 message holds the folder's path |
  | IF-03 | `dsn_check.py check [--root DIR] DSN-NNN` | Applies the rules below to `docs/specs/design/DSN-NNN.md`, with the BRN it cites and, for the digests, the boards folder. Prints one line `<file>:<line>: <part>: <message> (<rule>)` for each error and `warning: …` for each suspect link, then `OK <file>` (exit 0) or `INVALID: <n> error(s) in <file>` (exit 1) |

  The rules `check` applies, by the label it prints:
  - `frontmatter`: the keys of DM-01 in order and no others; `id` equals the file name; `type` is `design`; `status` is one of
    `draft`, `in-review`, `approved`, `superseded`, `deprecated`; `version` an integer of 1 or more; `created` and `updated`
    valid dates, `updated` not before `created`; `boards_root` equals `docs/specs/design/<id>/boards/`; `canvas` an `https://`
    URL or `null`; `canvas_version` a non-empty string or `null`; `canvas_format` equal to the `v` in `canvas.json`;
  - `boards`: each item has the fields of DM-02, `answers` included, and no others; item IDs are `BRD-NN` and unique; every board `canvas.json`
    names has exactly one active item with that `file`, and every active item's `file` is named by `canvas.json`; a
    deprecated item's file is named by no active item; each active item's `sha256` equals the file's digest;
  - `mapping`: `flow` matches the slug form; `surface` is one of the four or `null`; `ideas` is a list of `IDEA-NN` without
    repeats, `[]` or `null`; an item with a `null` `flow`, `surface` or `ideas` has `[NEEDS CLARIFICATION` in its `notes`; each
    idea named is a promoted idea of the BRN, or one with a `withdrawn` row in section 3; each `answers` entry has the form of
    DM-02, and the PRD item (an `FR` or `NFR` of `docs/specs/prd/PRD-NNN.md`) or the ADR it names exists, else an error; a
    PRD item that is deprecated, or an ADR that is not `accepted` or has a `superseded_by`, is a `warning:` (a suspect
    reference), never an error;
  - `links`: `upstream` holds exactly one `derives` link without an `item`, to a BRN, and one `derives` link with an `item`
    for each distinct idea an active board names and no other; all at one version. A version below the BRN's current one is
    a `warning:` (a suspect link), never an error;
  - `coverage`: section 3 lists each promoted idea of the BRN once, with `Status` one of DM-03's four, and a row with `Status`
    `withdrawn` for each idea the BRN no longer promotes that an earlier version listed, all in ID order; a promoted idea is
    `designed` exactly when an active board names it, with `Boards` listing those items, and `not a screen` or `no board yet`
    when none does; `no board yet` also needs a marker in section 5 that names the idea; a `withdrawn` row's `Boards` lists the
    active boards that still name the idea, or `none`;
  - `approval`: `status: approved` has a non-empty `approved_by`, an `approved_on` date and no `[NEEDS CLARIFICATION` anywhere
    outside a code span; every other status has `approved_by: ""` and `approved_on: null`;
  - `changelog`: the Change Log has a row for the document's `version`, in version order, with a date not after `updated`;
  - `placeholder`: no HTML comment and no `[[fill:` outside a code span.

  The script can't decide whether a mapping says what the user confirmed, whether a Change Log row describes the run, or
  whether section 1 claims more than the user confirmed: these stay in the self-check list in `references/output-rules.md`
  (BEH-15).
- **Downstream contract** (read by the neighbours, specified in their own specs in cycle C): the DSN's ID, `version` and
  `status`; the active board items with `file`, `title`, `flow`, `surface` and `ideas`; `canvas` and `canvas_version`; and
  `boards_root`. A reader cites the DSN by ID and version, and treats an `in-review` or `draft` DSN's content as a proposal.

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Run when the user types /devforgeai:ui or asks to record, add or update the screen designs, mockups or boards of a release from a brainstorm. Work through the checklist of §5 in order, in the main conversation, copying it into the reply and ticking it off. Ask only what the behaviours below name. Use only the tools of §5. Never crawl the repository or the codebase, never run a devforgeai command (that CLI doesn't exist and a program of that name on PATH can't be trusted, SPEC-004 §2), and never resolve policy."
  - id: BEH-02
    status: active
    rule: "Select the BRN. If $ARGUMENTS is a BRN ID, or the user stated one, read docs/specs/brainstorm/<ID>.md. If it is empty, list each BRN that has at least one promoted idea, with its title, status, number of promoted ideas and the DSN that cites it (BEH-04) or none, and ask which to use; never guess, even when only one is listed. With no BRN that has a promoted idea, apply ERR-16. Never take a file path (ERR-02), and write nothing until the BRN is chosen."
  - id: BEH-03
    status: active
    rule: "Read the BRN's frontmatter status, version, owner and title and its ideas item block (and its problems and assumptions for context). Use only ideas with disposition promoted, and never cite an open, parked or rejected idea anywhere in the DSN. When the BRN is not converged, warn that some ideas may not be decided and continue only on the user's explicit yes (ERR-07). With no promoted idea, stop (ERR-08). If an item block can't be read, report which block and stop (ERR-09). Never repair or modify a BRN."
  - id: BEH-04
    status: active
    rule: "Create or amend, decided by the files, never asked. A DSN cites the BRN when its upstream holds a link with the BRN's ID, at any version. Among docs/specs/design/DSN-*.md, a superseded or deprecated DSN is never amended and doesn't count. With no active DSN citing the BRN, create one. With exactly one, amend it. With more than one, ask which to amend and write nothing until the user answers (ERR-10). A request for a second DSN for a BRN that one already cites amends the first; to start over, the user deprecates the old DSN, which this skill never does. A DSN that fails dsn_check.py check before the run changes it is reported and amended only on the user's confirmation (ERR-15)."
  - id: BEH-05
    status: active
    rule: "Find the boards folder. For a create run, run python3 ${CLAUDE_SKILL_DIR}/scripts/dsn_check.py next (IF-01) as a command of its own: the new DSN's ID is the one it prints, and the boards must be in docs/specs/design/<that ID>/boards/. For an amend run the folder is the DSN's own. Then run dsn_check.py boards <ID> (IF-02) as a command of its own and act on its exit code: 0 continue; 1 stop with the ERR the script names (ERR-03 to ERR-06, ERR-12), writing nothing; 2 or python3 unavailable, ERR-14. Never take a folder or a file name from the user."
  - id: BEH-06
    status: active
    rule: "Read the boards from the committed copy only, as DM-04 says: the script's list of board files in canvas order, then the first 150 lines of each with Read. Take nothing from boards/README.md or any file the script doesn't list, never read a path outside the boards folder, and never fetch from the canvas, open a URL or call /design. Propose each board's title from its first <title>, <h1> or <h2> text, else from its file name without the extension; the proposal is written only when the user confirms it (BEH-09). Draw nothing and edit no board file."
  - id: BEH-07
    status: active
    rule: "In an amend run, also read the existing DSN, and compare each active item's sha256 with the script's digest for its file: a board is unchanged when they are equal, changed when they differ, new when canvas.json names a file with no active item, and removed when an active item's file is no longer named. Read the PRDs in docs/specs/prd/ and the accepted ADRs in docs/specs/adr/ (read-only, no superseded one), and propose as candidates the active requirements and the consequences that name a screen, a flow or a user interface and that no active board's answers or notes already covers, each with its citation (file, item and version). These are proposals for the user's decision; a candidate the user confirms for a board is recorded in that board's answers (BEH-09), and the document and version read go into the Change Log row (BEH-13). Warn, in the report, of each answers entry whose PRD item is now deprecated or whose ADR is no longer accepted. Search docs/specs/ (with Grep, or ls and grep on that folder) for the documents whose upstream cites this DSN at a lower version than the DSN's new one, to name them in the report (BEH-17); read only their frontmatter."
  - id: BEH-08
    status: active
    rule: "In an amend run, when the BRN's version is higher than the version of the DSN's links to it, treat those links as suspect: re-read the BRN at its current version, add a coverage row for each promoted idea the table lacks (to be asked about), mark a row withdrawn for an idea that is no longer promoted (and ask what to do with the boards that name only it: keep the mapping, drop the idea from it, or deprecate the board), move the DSN's links to the BRN's current version in this same run, and say so in the Change Log row. The run raises the DSN's version once, not twice."
  - id: BEH-09
    status: active
    rule: "Draft before asking: from the boards and the promoted ideas, propose each board's title, flow, surface and ideas, and each promoted idea's coverage, without writing any of it. Interview only for what the request doesn't answer, in batches of at most 4 questions per call: first, when the request doesn't state them, the canvas URL and the canvas version copied (BEH-10); then one question for each proposed flow, showing its boards with the proposed title, surface and ideas of each, so the user confirms or changes the group; then one question for the promoted ideas that no board shows (not a screen, or no board yet); in an amend run, one question for each group of changed, new or removed boards, showing the candidates of BEH-07 that could bear on each so the user can name the board that answers a candidate, or decline it. Offer 2 to 4 options with the recommended first, and let the user answer in their own words. Write a flow, surface, idea list, title or coverage status only when the user supplied or confirmed it; otherwise write null (the file name without its extension for a title; no board yet for an idea that names a screen) with a [NEEDS CLARIFICATION: …] marker, in the item's notes or in section 5. Answers stated in the request count. Under 'proceed without questions', ask nothing."
  - id: BEH-10
    status: active
    rule: "Record the canvas facts the user gives: canvas (the URL) and canvas_version, as the user states them, and the date of the copy when the user gives it. Read canvas_format from the script's output, never from the user. A fact the user doesn't give is null, with a [NEEDS CLARIFICATION: canvas URL and version copied] marker in section 4. Never take the version from a file in the boards folder and never infer it. In an amend run in which a board changed, was added or was removed, the recorded canvas_version describes the copy that was in boards/ before: ask for the new one with the canvas facts, and when the user gives none write canvas_version null with the marker, never the old value, which would name a copy the skill no longer holds. When no board changed, keep it."
  - id: BEH-11
    status: active
    rule: "Treat graphical and terminal screens alike. Every board gets a surface of web, desktop, mobile or terminal, confirmed by the user (a terminal screen is a command-line or other text-mode screen, designed in Claude Design like any other board); a board whose surface the user hasn't confirmed has surface null and a marker. A terminal board is mapped to flows and ideas, counted and reported exactly as the others are."
  - id: BEH-12
    status: active
    rule: "Write a new DSN with Write from ${CLAUDE_SKILL_DIR}/assets/dsn.md: delete every author comment and fill DM-01 to DM-03. The ID is the one BEH-05 gave, version 1, status draft, created and updated today. One board item for each board canvas.json names, in canvas order, BRD-01 upward, each with its file, the confirmed or null mapping and the script's sha256. Section 3 follows DM-03, section 4 the canvas facts, section 5 the markers. One Change Log row, authored claude-code (session ${CLAUDE_SESSION_ID}), saying the document was created from the BRN and the boards and ending with the number of markers left. The write is a revision of no earlier document: it overwrites nothing."
  - id: BEH-13
    status: active
    rule: "Amend an existing DSN only with Edit, starting from its current text. Raise version by one whatever the status, a draft DSN's amend included (as SPEC-002 BEH-09 and SPEC-011 BEH-13 do), set updated to today, and add one Change Log row, authored claude-code (session ${CLAUDE_SESSION_ID}), naming the boards changed, added or removed, the canvas_version now recorded, the ideas, requirements and ADRs considered with the document versions read, and any link moved (BEH-08). Update canvas_version as BEH-10 says. Change only what the user confirmed or what a script fact requires (a digest, a canvas_format, a link version): keep every other line, never delete or renumber an item, deprecate a removed board's item with status deprecated, append a new board's item with the next free BRD number, add the confirmed answers entries (never to upstream), and update sha256 for every changed board. If the DSN was approved, set status to in-review and clear approved_by and approved_on, so the change is reviewed explicitly; a draft or in-review DSN keeps its status. Keep the existing authors (adding the tool if missing), reviewed_by and every Change Log row."
  - id: BEH-14
    status: active
    rule: "Keep section 3 equal to DM-03 after every write: one row for each promoted idea of the BRN at the version read, the Boards cell from the active items, and the Status the user confirmed (no board yet, with a section 5 marker, for an idea that names a screen the user has not placed). Never add a row for an idea that is not promoted, other than withdrawn, and never record an idea as not a screen unless the user said so."
  - id: BEH-15
    status: active
    rule: "Validate after writing: run python3 ${CLAUDE_SKILL_DIR}/scripts/dsn_check.py check <ID> (IF-03) as a command of its own, then read the DSN back against the self-check list in references/output-rules.md for what the script can't decide (§5). Run one initial check, then at most three repair-and-readback cycles, so at most four checks; a repair changes the file to address a reported error, and an error that can't be repaired (for example one in a file this skill may not edit) stops the loop and is reported. Record each check and repair in the reply, quoting the script's lines. A suspect-link warning is named in the reply, never repaired by editing another document. Problems left after the loop: ERR-11."
  - id: BEH-16
    status: active
    rule: "Record approval only on the user's explicit words in this run that approve the named DSN (for example 'approve DSN-001'), after the check passed and the DSN holds no [NEEDS CLARIFICATION marker: otherwise say which markers remain and leave the status as it is. approved_by is the name the user gives; when none is given, ask who is approving, offering the document's owner first, and when no answer can arrive don't approve and say the approver wasn't named. On approval, with Edit, set status approved, approved_by, approved_on to today and add a Change Log row 'Approved' authored by the approver, without raising version; then run the check again. Never infer approval from silence, from an earlier run, from a request to write or amend the DSN, or from the DSN being cited by another document."
  - id: BEH-17
    status: active
    rule: "When the run wrote or checked a DSN, open the final reply with this block, then the findings, then the next step. Block lines: 'Design document: <ID> (v<N>, <status>; new | amended)'; 'Boards: <boards_root> · <number of active boards> · version <canvas_version, or unknown>', always, in a create and in an amend run, naming the copy in boards/ that the run read; 'Flows: <flow> (<count>), … | none', with each hyphen of a flow shown as a space and 'unconfirmed (<count>)' last for boards with a null flow; 'Boards with no idea: <file>, … | none' (active boards whose ideas and answers are both []); 'Ideas with no board: IDEA-NN (<the idea shortened to 60 characters>), … | none' (no board yet); 'Markers left: <ID>: <count> | none'; then the script's last line, 'OK docs/specs/design/<ID>.md'. Findings follow: the suspect-link warnings, the documents that cite the DSN at an older version (amend, BEH-07), the candidates the user declined, and the unconfirmed mappings. A run that stops before writing (ERR-01 to ERR-10, ERR-12, ERR-14, ERR-16, ERR-17) has no block."
  - id: BEH-18
    status: active
    rule: "Name the next step last, as its own paragraph outside any code block, starting with the words Next step, with nothing after it. After a create run: tell the user to run /devforgeai:prd with the BRN's ID, and that the PRD's section 8 links the DSN, when ${CLAUDE_SKILL_DIR}/../prd/SKILL.md exists; otherwise say the PRD workflow isn't built yet. After an amend run, name each document found by BEH-07 that cites the DSN at an older version and the skill that owns it, in chain order and checking its SKILL.md the same way: the PRD, /devforgeai:prd with the BRN's ID; an architecture description, /devforgeai:architecture with its PRD's ID; a context document, /devforgeai:context with the document's name; and say they re-review the DSN as a suspect upstream. When none cites it, say so. Never start another workflow and never edit those documents."
  - id: BEH-19
    status: active
    rule: "Write only docs/specs/design/<ID>.md. Never modify a BRN, PRD, ARCH, ADR, policy document, context document, epic, story or spec, a board file, canvas.json or boards/README.md; never fetch from the canvas, open a URL or call /design; never run git, or run, build or test project code; never delete a file; never write a policy setting or an ADR."
  - id: BEH-20
    status: active
    rule: "Fill the frontmatter provenance with the actual authoring tool, model and session, as the host provides them (§4). Never guess, copy or fabricate them; when the host can't provide one, write unavailable and disclose it in this write's Change Log row and in the report. A new DSN: authors the owner and the tool, reviewed_by empty. An amend: keep the existing authors, reviewed_by and rows, and say in the Change Log row and the report that the new version hasn't been reviewed. Every hash null."
```

### The amend path: three triggers, each with a worked example

An amend run starts the same way whatever prompted it. The user draws in Claude Design, copies `canvas.json` and the boards into
the DSN's `boards/` folder again, and runs `/devforgeai:ui BRN-NNN`. The skill finds the one active DSN that cites the BRN
(BEH-04), compares each board's digest with the one the DSN recorded (BEH-07), reads the PRDs and accepted ADRs for candidates,
asks about each group (BEH-09) and edits the DSN (BEH-13). It draws no board and fetches none, and nothing starts it: the user
runs it, usually after the prd or architecture skill's report names it (cycle C, §10). A run in which nothing changed writes
nothing (ERR-17). The canvas versions below are made up.

**(a) A revision right after the brainstorm, before any PRD.**
- *Start:* DSN-001 is version 1, draft, written from BRN-001 (version 1); no PRD exists. The user redraws the Report board.
- *The user:* copies the boards again (canvas version `1791580000-c3d4`) and runs `/devforgeai:ui BRN-001`.
- *The skill:* amends DSN-001. Only `Report.dc.html`'s digest differs, and no PRD or ADR bears on it. It asks for the new canvas
  version and whether Report's mapping stands; the user gives the version and says it does.
- *Result:* DSN-001 is version 2 and **still draft**: an amend raises the version of a draft too (§13, u), and a draft keeps its
  status. Report's `sha256` and `canvas_version` are updated, and one Change Log row says so. No document cites DSN-001, so the
  report says that and the next step is `/devforgeai:prd BRN-001`. Had the user given no new canvas version, `canvas_version`
  would be `null` with its marker (BEH-10), not the old value.

**(b) A new or changed screen from a PRD extension.**
- *Start:* DSN-001 is version 2, approved, and PRD-001 (version 1) cites it in section 8. The prd skill extends PRD-001 to
  version 2 with FR-024, "The system shall let an administrator set the retention period on a settings screen", and its report
  (cycle C) says DSN-001 is suspect and names `/devforgeai:ui BRN-001`.
- *The user:* draws a Settings board, copies the boards again (`1791670000-e5f6`) and runs the skill.
- *The skill:* amends DSN-001. `Settings.dc.html` is new and the other digests are equal. It reads PRD-001 (version 2), proposes
  FR-024 as a candidate that names a screen, and asks for Settings' flow, surface and ideas, whether it answers FR-024, and the
  canvas version.
- *Result:* DSN-001 is version 3, **in-review**, with `approved_by` and `approved_on` cleared. BRD-05 is Settings, with
  `answers: ["PRD-001#FR-024"]` and its flow and surface as confirmed. DSN-001's `upstream` still holds only its BRN links (§13,
  w). The Change Log row names PRD-001 version 2. The report finds PRD-001 citing DSN-001 at version 2 and names
  `/devforgeai:prd BRN-001`, which re-reviews the DSN as a suspect upstream.

**(c) An accepted ADR's consequence.**
- *Start:* DSN-001 is version 3, in-review; PRD-001 and ARCH-001 (its evidence record) cite it at version 3. The architecture
  skill accepts ADR-009, whose consequence reads "the CLI must print a sync conflict and offer to keep the local copy", and its
  report (cycle C) says DSN-001 is suspect and names `/devforgeai:ui BRN-001`.
- *The user:* redraws the List board, a terminal screen, copies the boards again (`1791750000-a7b8`) and runs the skill.
- *The skill:* amends DSN-001. `List.dc.html`'s digest differs. It reads the accepted ADRs and proposes ADR-009's consequence as a
  candidate. The user says List answers ADR-009 and its flow and ideas stand.
- *Result:* DSN-001 is version 4 and stays in-review. BRD-02 (List) has `answers: ["ADR-009"]`, a new `sha256` and the new canvas
  version in the document. The report finds PRD-001 and ARCH-001 citing DSN-001 at version 3 and names `/devforgeai:prd BRN-001`
  and then `/devforgeai:architecture PRD-001`.

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The BRN ID given does not exist"
    handling: "Say so, list the BRN IDs that do exist with their titles, and write nothing"
    user_result: "The list of BRNs; nothing written"
  - id: ERR-02
    status: active
    condition: "$ARGUMENTS, or the request, gives a file path or a boards folder instead of a BRN ID"
    handling: "Write nothing. Say that the skill takes a BRN ID, never a path, and ask for the ID (listing the BRNs that have a promoted idea)"
    user_result: "A request for the ID; nothing written"
  - id: ERR-03
    status: active
    condition: "The boards folder docs/specs/design/<ID>/boards/ is missing, empty or without a canvas.json, or canvas.json names no board"
    handling: "Write nothing. Give the exact folder, say that the boards are copied there by the user (or by a session at the user's request) before the run, from the canvas, and that the skill never fetches them. For a create run say that the next free number is <ID> and list any pending boards folder under another number (IF-01), saying which number to use. Name canvas.json and the board files as what the folder must hold"
    user_result: "The exact path to copy the boards into, and nothing written"
  - id: ERR-04
    status: active
    condition: "canvas.json is not readable as a UTF-8 JSON object, or has no boards member that is an object"
    handling: "Write nothing. Quote the script's message, say the copy may be damaged or from another tool, and ask the user to copy it again. Never repair, reformat or guess at the file"
    user_result: "The reason and a request to copy again; nothing written"
  - id: ERR-05
    status: active
    condition: "canvas.json's v is not a value this spec supports (DM-04: 3), or is not an integer"
    handling: "Write nothing. Say which value the file holds and which are supported, and that Claude Design's format is not documented, so the skill doesn't guess what another version means. Tell the user a spec change must be approved for the new version"
    user_result: "The version found and the versions supported; nothing written"
  - id: ERR-06
    status: active
    condition: "A board file canvas.json names is absent, is not a regular file or is unreadable, or its name is not a plain file name (it holds /, \\ or .. or is empty)"
    handling: "Write nothing. Name each such board as the script reports it, and ask the user to copy the boards again"
    user_result: "Each board that fails and why; nothing written"
  - id: ERR-07
    status: active
    condition: "The selected BRN's status is not converged"
    handling: "Warn that some ideas may not be decided, and continue only after the user confirms. Without confirmation, as in a non-interactive run, write nothing"
    user_result: "A warning and a question, or nothing written"
  - id: ERR-08
    status: active
    condition: "The selected BRN has no promoted idea"
    handling: "Stop and write nothing. Say there is nothing to map the boards to, and point the user back to /devforgeai:brainstorm to converge it"
    user_result: "A handback to the brainstorm step; nothing written"
  - id: ERR-09
    status: active
    condition: "The BRN's item blocks can't be read (malformed YAML or a missing ideas collection)"
    handling: "Report which block failed and the BRN's path, and stop. Never repair the BRN"
    user_result: "The failing block; nothing written"
  - id: ERR-10
    status: active
    condition: "More than one active DSN cites the BRN"
    handling: "List them with their versions and statuses, say that ADR-007 D4 allows one active DSN for each BRN, and ask which to amend. With no answer, write nothing"
    user_result: "A question; nothing written without the answer"
  - id: ERR-11
    status: active
    condition: "Validation still fails after the initial check and three repair cycles, or an error can't be repaired"
    handling: "Stop. A new DSN stays draft. An amended DSN keeps the status BEH-13 gave it and is never set to approved. List the checks, the repairs and the unresolved errors, and don't hand off to the PRD or name the DSN as ready"
    user_result: "A validation-failure report"
  - id: ERR-12
    status: active
    condition: "canvas.json names more than 99 boards (BRD-NN has two digits)"
    handling: "Write nothing. Say that the DSN's board IDs hold 99 boards, give the count, and ask the owner to split the canvas or change the spec"
    user_result: "The count and the limit; nothing written"
  - id: ERR-13
    status: active
    condition: "The user stops before the interview ends"
    handling: "Offer to save the DSN with every unanswered mapping null and marked (a create run) or unchanged (an amend run). If yes, write it and validate and report it as any other write. With no answer to the offer, write nothing and say how to resume: run the skill again with the BRN ID"
    user_result: "A draft DSN with markers, or nothing written"
  - id: ERR-14
    status: active
    condition: "dsn_check.py can't run: exit 2, python3 is missing, or a BRN it needs can't be read"
    handling: "Stop before writing: say the check couldn't run, quote its Cannot run line, and write nothing. If it exits 2 after the run has written, name the file as written and not checked, leave its status as it is, approve nothing, and say so in the report"
    user_result: "The reason; nothing written, or the DSN left unchecked"
  - id: ERR-15
    status: active
    condition: "The DSN to amend fails dsn_check.py check before the run changes it, for example after a hand edit"
    handling: "Report its errors. Amend it only when the user confirms in this run; the amend then also repairs them, and the Change Log row says so. Without confirmation, leave it unchanged and stop"
    user_result: "The errors and a question, or the DSN left as it was"
  - id: ERR-16
    status: active
    condition: "No argument was given and no BRN can be selected: docs/specs/brainstorm/ holds no BRN, or none has a promoted idea"
    handling: "Write nothing. With no BRN at all, say that no brainstorm exists yet and point to /devforgeai:brainstorm. Otherwise list each BRN with its status, say that none has a promoted idea, and point to /devforgeai:brainstorm to converge one"
    user_result: "The reason and a handback to the brainstorm step; nothing written"
  - id: ERR-17
    status: active
    condition: "An amend run finds nothing to change: no board changed, new or removed, the DSN's links to the BRN are current, no candidate of BEH-07 bears on a screen without an answering board, and the request names no change"
    handling: "Write nothing and raise no version. Say that the DSN is current, give its version and the canvas_version it records, and say that a board changed on the canvas must be copied into the boards folder again before the skill can see it"
    user_result: "A statement that the DSN is current; nothing written"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds only the checklist, the user's decisions and the output contract; the interview, the board-reading contract and the output rules live in references/, the template in assets/. SKILL.md stays under about 200 lines, and each reference is read only when its step needs it"
    measured_by: "src/tests/ui/test_structure.py: SKILL.md line count (at most 500) and description length (at most 1024 characters, no < or >)"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 13, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted, with devforgeai-version equal to the provenance version; no devforgeai-tracked key"
    measured_by: "src/tests/ui/test_structure.py, against skill-frontmatter.schema.json and skill.schema.json, comparing the two version values"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 13, hash: null}
  - id: QR-03
    status: active
    response: "Every automated e2e VER item is graded in an eval case run against the no-plugin baseline, tagged ui and ver-NN; the trigger cases are tagged trigger and ver-NN, without ui, and run without a baseline arm (a run without the plugin can't fire the skill)"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs, unless Bryan records a waiver in §9"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 13, hash: null}
  - id: QR-04
    status: active
    response: "The skill fires on requests to record, add or update a release's UI design, screens, mockups or boards, whether or not they name the DSN, and on a PRD or ADR report that a change names a screen; it doesn't fire on requests about one story's design, drawing a screen, general UI advice or the PRD"
    measured_by: "VER-22, per model: every trigger case meets --threshold 0.8 over 3 runs, so a binary case needs 3 of 3. Required on sonnet and opus; haiku is measured and reported (§13)"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 13, hash: null}
  - id: QR-05
    status: active
    response: "The skill and its script read the boards only from committed files: no network connection, no write outside the DSN (the script writes no file), no symbolic link followed, and no path outside the ones each step names"
    measured_by: "src/tests/ui/test_dsn_check.py: each subcommand run with socket creation made to fail and over a folder tree compared byte for byte before and after, with a symbolic link as a board file; and the eval cases' whole-content graders on the neighbours and the boards"
    upstream:
      - {id: ADR-007, relation: informed_by, version: 1, hash: null, note: "D3: the boards are committed files, read by contract; the skill never fetches"}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: this spec against `spec.schema.json` | Passes, with every BEH, ERR and QR item covered by a VER item (checked 2026-10-09, version 1 draft; `coverage.py`) |
| Structural: `src/schemas/design.schema.json` | A DSN of two boards (one confirmed, one with `null` mapping and a marker) validates; a DSN with a bad ID, status, boards_root, file name and surface fails with one error each (checked 2026-10-09) |
| Build (SKL-013 v1) | Not built. Cycle B |
| Behavioural: automated VER items | Not run: the skill isn't built |
| Behavioural: manual VER items (VER-27, VER-28, VER-29) | Not run |
| Qualification (QR-03) | The bar is 0.8 per case over 3 runs, unless Bryan records a waiver here |

**Fixtures.** `src/tests/ui/make_evals.py` (cycle B) builds every case; it validates each seeded document against `src/schemas/`
(the BRN against `brainstorm.schema.json`, the DSN against `design.schema.json`) with a format checker, except a document a
case marks as expected to be invalid. An eval run starts in an empty workspace with no earlier conversation
(`.claude/rules/evals.md`), so each scaffold builds what the case needs.
- **Shared fixture:** `docs/specs/brainstorm/BRN-001.md`, `status: converged`, version 1, owner Example Owner, title "Shiftlog:
  record shifts"; its ideas IDEA-01 "Add a shift from the terminal", IDEA-02 "List shifts in a table", IDEA-03 "A weekly report
  page", IDEA-04 "Export shifts as CSV" and IDEA-06 "A dark theme for the report page" are promoted, IDEA-05 "Sync to a
  server" is parked. Four boards in `docs/specs/design/DSN-001/boards/`: `canvas.json` (`{"v": 3, "attachments": {}, "boards":
  {"Home.dc.html": {…}, "List.dc.html": {…}, "Add.dc.html": {…}, "Report.dc.html": {…}}}`) and four small HTML files with a
  `<title>`; `List` and `Add` show terminal output and prompts, `Home` and `Report` web pages. There is no DSN, no PRD, no ARCH
  and no policy.
- **The shared prompt,** unless a case gives its own: "Record the UI design for BRN-001. The canvas is
  https://claude.ai/artifact/EXAMPLE, version 17-example. Home and Report are web screens in the flow report-and-home; List and
  Add are terminal screens in the flow shifts. Home shows IDEA-02; List shows IDEA-02; Add shows IDEA-01; Report shows IDEA-03.
  IDEA-04 names no screen. IDEA-06 has no board yet. Proceed without questions." It confirms every mapping, so only IDEA-06 leaves
  a marker.
- **Case limits:** `max_turns: 60` and `timeout_seconds: 900` for a case that writes, `15` and `300` for the stop cases and the
  trigger cases; a pilot run confirms them.
- **Digests:** `make_evals.py` computes the SHA-256 of each board file and puts it into the graders. Every seeded board item
  carries `answers: []` unless a case says otherwise.
- **Documents that cite a DSN** (the PRD-001 of VER-10): until cycle C adds `DSN` to the document ID pattern (§10), such a
  document fails `prd.schema.json` on that one pattern, so the generator marks it as expected to be invalid for that reason
  alone and checks the rest of it.
- **The script on the fixtures:** the generator runs `dsn_check.py boards` and `check` over every seeded boards folder and DSN
  except one marked as expected to be invalid.

No story specifies this skill yet, so the VER items have no `upstream` link.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture and prompt. docs/specs/design/DSN-001.md exists with type design, status draft, version 1, approved_by empty, approved_on null, owner Example Owner, title 'Shiftlog: record shifts: release design', canvas and canvas_version as the prompt gives them, canvas_format 3 and boards_root docs/specs/design/DSN-001/boards/; its boards block has four active items BRD-01 to BRD-04 in canvas order (Home, List, Add, Report) with the files, flows, surfaces (web, terminal, terminal, web) and ideas the prompt states, and each sha256 equal to the board file's digest (computed by make_evals.py); upstream holds one derives link to BRN-001 at version 1 without an item and one with an item for each of IDEA-01, IDEA-02 and IDEA-03; generated_by holds tool, model and a session that is a UUID (not the text ${CLAUDE_SESSION_ID}); one Change Log row for version 1. Eval case writes-dsn: regex on the file, file_exists. Graders ver01-."
    level: e2e
    covers:
      - BEH-04
      - BEH-05
      - BEH-06
      - BEH-10
      - BEH-11
      - BEH-12
      - BEH-20
  - id: VER-02
    status: active
    obligation: "In writes-dsn, section 3 has the header and exactly five rows, IDEA-01, IDEA-02, IDEA-03, IDEA-04 and IDEA-06 (no IDEA-05, which is parked), with IDEA-01 to IDEA-03 designed and their Boards cells, IDEA-04 not a screen and IDEA-06 no board yet; section 5 holds one [NEEDS CLARIFICATION marker naming IDEA-06; the reply opens with the block (Design document: DSN-001 (v1, draft; new); Boards with the folder, 4 and the version; Flows: report and home (2), shifts (2); Boards with no idea: none; Ideas with no board: IDEA-06; Markers left: DSN-001: 1; OK docs/specs/design/DSN-001.md), and its last paragraph, outside any code block, starts with Next step, names /devforgeai:prd BRN-001, says the PRD's section 8 links DSN-001 and has nothing after it; the graders read the reply, never whether the prd skill exists. Eval case coverage-and-report: regex on the file and last_message. Graders ver02-."
    level: e2e
    covers:
      - BEH-03
      - BEH-14
      - BEH-17
      - BEH-18
  - id: VER-03
    status: active
    obligation: "Shared fixture; the prompt is 'Record the UI design for BRN-001. Proceed without questions.' (no canvas facts, no mapping). The DSN is written as draft; every item has flow, surface and ideas null and a [NEEDS CLARIFICATION marker in its notes, and each title equals the board's file name without its extension (a proposed title is written only when confirmed); canvas and canvas_version are null with a marker in section 4; section 3 lists every promoted idea as no board yet or not a screen only when the prompt said so (here, no board yet for all five); the reply's Flows line is 'unconfirmed (4)' and Markers left is not none. Eval case unconfirmed-stays-null: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-09
      - BEH-10
  - id: VER-04
    status: active
    obligation: "Shared fixture without the boards folder. No docs/specs/design/ file is written; the reply names docs/specs/design/DSN-001/boards/ as the folder, says the user copies canvas.json and the board files there, and that the skill never fetches from the canvas. Eval case no-boards-stops: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-03
  - id: VER-05
    status: active
    obligation: "Shared fixture with an existing docs/specs/design/DSN-001.md (draft, version 1, citing a different BRN, BRN-002) and the boards in docs/specs/design/DSN-001/boards/ only; the prompt records BRN-001. No new DSN is written and DSN-001.md is unchanged (whole-content grader); the reply says the next free number is DSN-002 and to copy the boards into docs/specs/design/DSN-002/boards/. Eval case boards-at-wrong-number: regex on last_message and the file."
    level: e2e
    covers:
      - ERR-03
      - BEH-05
  - id: VER-06
    status: active
    obligation: "Shared fixture with canvas.json holding the text 'not json {'. Nothing is written; the reply says canvas.json can't be read and asks the user to copy it again. Eval case canvas-unreadable: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-04
  - id: VER-07
    status: active
    obligation: "Shared fixture with canvas.json's v set to 4. Nothing is written; the reply names version 4 and the supported version 3 and says the format isn't documented. Eval case unknown-canvas-format: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-05
  - id: VER-08
    status: active
    obligation: "Shared fixture with canvas.json also naming 'Gone.dc.html' (not in the folder) and '../outside.dc.html'. Nothing is written; the reply names both boards; no file outside the boards folder is read (the trace has no Read of a path outside docs/specs/design/DSN-001/boards/, checked manually with --keep-temp; no shipped grader checks Read calls). Eval case board-file-absent: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-06
  - id: VER-09
    status: active
    obligation: "Shared fixture with a canvas.json that names 100 board files (small stubs). Nothing is written; the reply gives the count 100 and the limit 99. Eval case too-many-boards: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-12
  - id: VER-10
    status: active
    obligation: "Shared fixture plus an approved DSN-001 (version 1, approved_by Example Owner, four boards matching the folder), a PRD-001 citing DSN-001 at version 1, then Report.dc.html's content changed and a fifth board Settings.dc.html added to canvas.json and the folder; the prompt confirms Report's mapping is unchanged, that Settings is a web screen in the flow report-and-home showing IDEA-06, and 'proceed without questions'. DSN-001 is version 2, status in-review, approved_by empty, approved_on null; BRD-01 to BRD-04 keep their fields except Report's sha256, which equals the new digest; BRD-05 is Settings, active; IDEA-06's row is designed; the Change Log keeps its version 1 rows and has a version 2 row; PRD-001, BRN-001 and the board files are unchanged (whole-content graders); the reply says 'amended', names PRD-001 as citing DSN-001 at version 1 and its last paragraph starts with Next step, names /devforgeai:prd BRN-001 and says it re-reviews the DSN. Eval case amend-changed-board: regex on the files and last_message. Graders ver10-."
    level: e2e
    covers:
      - BEH-07
      - BEH-13
      - BEH-18
  - id: VER-11
    status: active
    obligation: "Shared fixture plus a DSN-001 version 1 (draft) and canvas.json no longer naming Add.dc.html (file removed). The prompt confirms the removal. BRD-03 (Add) is still in the file with status deprecated; no item is deleted or renumbered; the active board count in the reply is 3; IDEA-01's row is no board yet with a marker. Eval case amend-removed-board: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-13
      - BEH-14
  - id: VER-12
    status: active
    obligation: "Shared fixture plus a DSN-001 version 1 whose links cite BRN-001 at version 1, and BRN-001 now version 2 with a newly promoted idea IDEA-07 'Dark theme for List' and IDEA-02 now parked; the prompt says IDEA-07 has no board yet and the board that named IDEA-02 keeps its mapping. DSN-001 is version 2 (raised once); its links cite BRN-001 at version 2; section 3 has a row for IDEA-07 (no board yet, with a marker) and a withdrawn row for IDEA-02; the Change Log row says the links were moved. Eval case amend-brn-moved: regex on the file."
    level: e2e
    covers:
      - BEH-08
  - id: VER-13
    status: active
    obligation: "The shared fixture with the prompt 'Record the UI design for BRN-009.' (no such BRN). Nothing is written; the reply lists BRN-001. Eval case unknown-brn: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-01
  - id: VER-14
    status: active
    obligation: "The prompt is 'Record the UI design from docs/specs/brainstorm/BRN-001.md.' Nothing is written; the reply asks for the BRN ID and says paths aren't accepted. Eval case path-refused: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-02
  - id: VER-15
    status: active
    obligation: "Shared fixture with BRN-001's status draft and the prompt 'Record the UI design for BRN-001. Proceed without questions.' Nothing is written, and the reply warns that some ideas may not be decided. Eval case unconverged-brn: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-07
  - id: VER-16
    status: active
    obligation: "Shared fixture with BRN-001's ideas all open or parked. Nothing is written; the reply points to /devforgeai:brainstorm. Eval case no-promoted-idea: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-08
  - id: VER-17
    status: active
    obligation: "Shared fixture with BRN-001's ideas block holding malformed YAML. Nothing is written; the reply names the ideas block and BRN-001's path; BRN-001 is unchanged (whole-content grader). Eval case malformed-brn: file_exists false and regex on last_message and the file."
    level: e2e
    covers:
      - ERR-09
  - id: VER-18
    status: active
    obligation: "Shared fixture plus two draft DSNs, DSN-001 and DSN-002, both citing BRN-001. Nothing is written or changed; the reply lists both and asks which to amend. Eval case two-dsns-cite: regex on last_message and whole-content graders on both."
    level: e2e
    covers:
      - ERR-10
  - id: VER-19
    status: active
    obligation: "Shared fixture and prompt followed by 'I'm Example Owner, and I approve DSN-001, with IDEA-06 left as it is.' While the marker for IDEA-06 remains, the DSN stays draft and the reply says the marker remains; then the same with a fifth board, Settings.dc.html, in the fixture and the prompt placing IDEA-06 on it (every mapping confirmed): status approved, approved_by Example Owner, approved_on a date, a Change Log row Approved authored by Example Owner, version still 1. The prompt without any approval words leaves status draft in both fixtures. Eval cases approve-blocked-by-marker, approve-on-explicit-words and no-approval-without-words: regex on the file."
    level: e2e
    covers:
      - BEH-16
  - id: VER-20
    status: active
    obligation: "In writes-dsn and amend-changed-board, with a PRD-001, an ARCH-001, context documents and a STORY-001 seeded, each of them, BRN-001 and every board file and canvas.json is byte-identical to its seeded content (whole-content graders written ^…$ without the m flag, as the context suite does), and nothing is written under docs/specs/ but docs/specs/design/DSN-001.md. Eval case neighbours-unchanged (graders ver20-): regex and file_exists."
    level: e2e
    covers:
      - BEH-19
  - id: VER-21
    status: active
    obligation: "Two BRNs, BRN-001 with a promoted idea cited by DSN-001 and BRN-002 with one and no DSN, and the prompt 'Record the UI design.' Nothing is written; the reply lists both BRNs with their titles and which DSN cites each, and asks which to use; with no BRN, the reply says no brainstorm exists and points to /devforgeai:brainstorm; with only a draft BRN whose ideas are all open, the reply lists it with its status, says none has a promoted idea and points to /devforgeai:brainstorm. Eval cases lists-brns, no-brainstorm-yet and no-brn-with-promoted-idea: regex on last_message and file_exists false."
    level: e2e
    covers:
      - BEH-02
      - ERR-16
  - id: VER-22
    status: active
    obligation: "Trigger cases (§9 fixtures without a boards folder), every grader a tool_used Skill with input_match naming ui, min 1 for a positive case and max 0 for a negative: Positive: 'Record the screen designs for BRN-001 from the boards we copied.'; 'Add the UI design step for our release before the PRD.'; 'Update the UI design: the PRD now names a settings screen.'; 'Turn our Claude Design boards into a design document.'; 'Run the UI design step for BRN-001.'. Negative: 'Write the PRD for BRN-001.'; 'What UI framework should I use for a CLI?'; 'Draw a login screen for me.'; 'Record the approved design for STORY-001.'; 'Make the button on the report page blue.' Cases trigger-01 to trigger-10, run with --case 'trigger-*' --ablation none --runs 3, once each with --model haiku, sonnet and opus."
    level: e2e
    covers:
      - QR-04
      - BEH-01
  - id: VER-23
    status: active
    obligation: "src/tests/ui/test_dsn_check.py, subcommands next and boards, every case normally and under python3 -S. next: no design folder gives next: DSN-001 and none; DSN-001.md and DSN-003.md give next: DSN-004; a deprecated DSN counts; a boards folder with no document is listed as pending. boards: a valid folder of four boards exits 0 and prints canvas.json: v3, 4 boards, one line per board in canvas order with its byte count and the SHA-256 that hashlib gives, and boards: ok; each of a missing folder, an empty folder, a folder without canvas.json and a canvas.json with an empty boards object exits 1 with an ERR-03 line holding the folder; invalid UTF-8, JSON that is not an object, a missing boards member and boards that is a list each exit 1 with ERR-04; v 4, v '3' and v missing each exit 1 with ERR-05 naming the value found; an absent board file, a directory, a symbolic link as a board file, an unreadable file, and the names '', '..', 'a/b' and 'a\\\\b' each give an ERR-06 line for that board and every failing board is listed; 100 boards exits 1 with ERR-12; members other than v and boards, and extra files such as README.md, are ignored. Both subcommands write no file (the tree is byte-identical before and after), open no socket (creating one is made to fail) and give a missing --root or an unknown argument exit 2 with Cannot run. Tests are written before the script (§11)."
    level: unit
    covers:
      - IF-01
      - IF-02
      - ERR-03
      - ERR-04
      - ERR-05
      - ERR-06
      - ERR-12
      - QR-05
  - id: VER-24
    status: active
    obligation: "src/tests/ui/test_dsn_check.py, subcommand check, every case normally and under python3 -S, with and without PyYAML installed (the verdict is the same). A valid DSN (created, amended, approved, and with null mappings plus markers) exits 0 and prints OK <file>. One failing fixture for each rule label and each part of §5's rules exits 1 with the expected '<file>:<line>: <part>: <message> (<rule>)' line and INVALID: <n> error(s): frontmatter (wrong id for the file name, bad boards_root, canvas_format differing from canvas.json, canvas without https), boards (a duplicate BRD ID, a board in canvas.json with no active item, an active item with a file canvas.json doesn't name, a stale sha256, an extra field), mapping (a bad flow slug, surface cli, a null field without a marker, an idea that is not promoted), links (no document-level derives link, a missing or extra item link, mixed versions), coverage (a missing row, a designed idea with no board, a withdrawn row for an idea still promoted, no board yet without a section 5 marker), approval (approved with a marker, approved with empty approved_by, draft with approved_by set), changelog (no row for the version), placeholder (a comment). A links version below the BRN's current gives a warning and exit 0. Mapping cases for answers: a malformed entry ('FR-006', 'ADR-9') and an entry naming a PRD item or ADR that doesn't exist each exit 1; an entry naming a deprecated PRD item, or an ADR that is not accepted, gives a warning and exit 0; a board item without answers exits 1. A BRN it can't read exits 2. No file is written and no socket is opened."
    level: unit
    covers:
      - IF-03
      - BEH-15
      - QR-05
  - id: VER-25
    status: active
    obligation: "src/tests/ui/test_structure.py: SKILL.md has at most 500 lines; its frontmatter has exactly name, description, argument-hint and metadata (devforgeai-id, devforgeai-version), quoted and with no devforgeai-tracked key; the description has at most 1024 characters and no < or >; devforgeai-version equals provenance.yaml's version; provenance.yaml records SKL-013 implementing SPEC-017 and validates against skill.schema.json; the checklist has the seven numbered items of §5; every reference and asset SKILL.md names exists; assets/dsn.md holds DM-01's headings in order and validates, filled in, against design.schema.json; the skill's folder holds what §3 lists; SKILL.md, the references and the template hold no absolute path, no /home/ and no person's name."
    level: unit
    covers:
      - QR-01
      - QR-02
  - id: VER-26
    status: active
    obligation: "QR-03: every automated e2e case (VER-01 to VER-21 and VER-30 to VER-33) at 0.8 or above over 3 runs against the no-plugin baseline, and every VER item's graders at 0.8 or above, unless Bryan's waiver in §9 sets another bar"
    level: e2e
    covers:
      - QR-03
  - id: VER-27
    status: active
    obligation: "Manual, interactive, one fixture copy per check: (a) the questions come in batches of at most 4 with 2 to 4 options and the recommended first, one question for each flow showing its boards; (b) a mapping the user changes is written as changed, and one the user leaves is written null with a marker; (c) stopping mid-interview offers the draft and writes nothing without an answer (ERR-13); (d) 'approve DSN-001' without a name asks who is approving, with the owner first; (e) an amend run asks about each group of changed, new and removed boards and about each PRD or ADR candidate, and the candidates carry their citations; (f) an amend of a DSN that fails the check asks before changing it (ERR-15); (g) a BRN that is draft asks before continuing (ERR-07)."
    level: manual
    covers:
      - BEH-09
      - BEH-16
      - ERR-07
      - ERR-13
      - ERR-15
  - id: VER-28
    status: active
    obligation: "Manual, live, in Bryan's worker1 tab with --plugin-dir on the build, on a copy of the Krepion project's brainstorm and its sixteen committed boards: (a) /devforgeai:ui BRN-001 writes a DSN whose Flows line groups the boards into the four flows Bryan confirms and that lists the idea that never reached the canvas under Ideas with no board; (b) the first 150 lines of the real boards are enough for a title and a mapping proposal, and the run's context use is acceptable (§13, m); (c) after a hand-made change to one board file, a second run amends the DSN to version 2, in-review, and names the PRD that cites version 1; (d) the tracker opens a run for the skill with no manifest and says it is tracked by ticks only (SPEC-013 BEH-10), and the seven checklist items tick."
    level: manual
    covers:
      - BEH-01
  - id: VER-29
    status: active
    obligation: "Manual, in fixture copies: (a) a PostToolUse hook that corrupts one frontmatter field of the DSN after every Edit makes the run end with the validation-failure report after at most four checks, with the DSN kept as draft and not presented as ready (ERR-11); (b) with dsn_check.py made unrunnable (renamed in a copy of the skill), and separately with python3 missing from the path, the run stops before writing (ERR-14)."
    level: manual
    covers:
      - ERR-11
      - ERR-14
  - id: VER-30
    status: active
    obligation: "Trigger (a). Shared fixture plus a draft DSN-001 version 1 written from it (four boards matching the folder, board items with answers empty, no PRD), then Report.dc.html's content changed and canvas.json unchanged; the prompt gives the new canvas version 1791580000-c3d4, says Report's mapping stands and says to proceed without questions. DSN-001 is version 2 and still draft; BRD-04's sha256 equals the new digest and the other items are unchanged; canvas_version is 1791580000-c3d4; the Change Log keeps its version 1 row and has a version 2 row; the reply's Boards line ends 'version 1791580000-c3d4', it says no document cites DSN-001, and its last paragraph starts with Next step and names /devforgeai:prd BRN-001. A second case with the same fixture and a prompt that gives no canvas version: canvas_version is null with a [NEEDS CLARIFICATION marker in section 4, never the old value, and the Boards line ends 'version unknown'. Eval cases amend-draft-revision and amend-without-new-version: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-10
      - BEH-13
      - BEH-17
  - id: VER-31
    status: active
    obligation: "Trigger (b). Shared fixture plus an approved DSN-001 version 2 (four boards, canvas_version recorded), a PRD-001 version 2 that cites DSN-001 at version 2 in its frontmatter and holds FR-024 'The system shall let an administrator set the retention period on a settings screen', and Settings.dc.html added to the folder and to canvas.json; the prompt gives a new canvas version and says Settings is a web screen in the flow report-and-home that shows no idea and answers PRD-001 FR-024. DSN-001 is version 3, status in-review, approved_by empty, approved_on null; BRD-05 is Settings with answers exactly ['PRD-001#FR-024'], flow, surface web and ideas []; every other item has answers [] and its earlier fields; DSN-001's upstream holds only derives links to BRN-001 (no PRD or ADR link); the Change Log row names PRD-001 version 2; PRD-001, BRN-001 and the board files are byte-identical to their seeded content; the reply lists Settings under neither 'Boards with no idea' nor an error, names PRD-001 as citing DSN-001 at version 2, and its last paragraph starts with Next step and names /devforgeai:prd BRN-001. Eval case amend-prd-requirement: regex on the files and last_message. Graders ver31-."
    level: e2e
    covers:
      - BEH-07
      - BEH-09
      - BEH-13
      - BEH-18
  - id: VER-32
    status: active
    obligation: "Trigger (c). VER-31's start with an in-review DSN-001 version 3 that PRD-001 and ARCH-001 cite at version 3 (ARCH-001's frontmatter upstream, in this fixture's form), an accepted ADR-009 whose consequence reads 'the CLI must print a sync conflict and offer to keep the local copy', and List.dc.html's content changed; the prompt gives a new canvas version and says List answers ADR-009 and its mapping stands. DSN-001 is version 4, still in-review; BRD-02 (List) has answers exactly ['ADR-009'] and a new sha256; no other item changed; no upstream link to ADR-009; ADR-009, PRD-001, ARCH-001 and BRN-001 are byte-identical; the reply names PRD-001 and ARCH-001 as citing DSN-001 at version 3, and its last paragraph, outside any code block, starts with Next step, names /devforgeai:prd BRN-001 and then /devforgeai:architecture PRD-001, and has nothing after it. Eval case amend-adr-consequence: regex on the files and last_message."
    level: e2e
    covers:
      - BEH-07
      - BEH-13
      - BEH-18
  - id: VER-33
    status: active
    obligation: "Shared fixture plus a DSN-001 version 1 whose items match the folder (equal digests), a BRN-001 at the version its links cite, and no PRD or ADR; the prompt is 'Update the UI design for BRN-001. Proceed without questions.' Nothing is written and DSN-001 is byte-identical to its seeded content; the reply says DSN-001 is current, gives version 1 and the canvas version it records, and says a board changed on the canvas must be copied into the boards folder again first. Eval case amend-nothing-to-do: regex on the file and last_message."
    level: e2e
    covers:
      - ERR-17
```

## 10. Rollout, migration and rollback

- **New skill, nothing to migrate.** It ships in the next plugin version after approval and the build (0.31.0, the next free
  minor, set at the merge on Bryan's word). Rolling back is removing `skills/ui/`, `evals/ui/`, `src/tests/ui/`, the CLAUDE.md
  row, and `src/schemas/design.schema.json`.
- **Records.** CLAUDE.md's skill table gains a `ui` row (SKL-013, SPEC-017); `src/templates/README.md` gains the DSN rows in §1.2
  and §2.1 and a DSN → BRN `derives` pair in §2.4 (it lists `derives` for PRD → BRN only), as ADR-004's follow-up M2 did for `CTX`;
  the template moves into `assets/dsn.md` (`.claude/rules/skills.md`, "Building the next skill").
- **The ID patterns (deferred to cycle C, on purpose).** `common.schema.json`'s document ID pattern lacks `DSN` and its item ID
  pattern lacks `BRD`. They are not added in cycle A: `src/schemas/common.schema.json` is shared byte for byte with the
  prd, architecture and context skills' `references/schemas/` copies (`src/tests/prd/test_shared_files.py`), so changing it
  edits three built skills, which bumps and requalifies them (the shared-schema PR #25 did that for `CTX`). `design.schema.json`
  therefore holds its own `DSN` and `BRD` patterns until cycle C adds them, in the three copies and the inline copy of the
  document ID list in `brainstorm.schema.json` (`blocked_by`), together with the skills' bumps. A document that cites a DSN
  with an `id: DSN-NNN` link (the PRD's section 8, the ARCH, `ui-mockups.md`) needs that change, so it is a cycle C
  prerequisite.
- **The neighbours (cycle C, each with its spec bump, skill bump and requalification, and each needing Bryan's yes).** Stated
  here as dependencies, not specified here:
  - **SPEC-001 v18, SKL-001 v11:** the brainstorm's next-step text names `/devforgeai:ui BRN-NNN` first, then
    `/devforgeai:prd BRN-NNN`, when a promoted idea names a screen, a flow or a user interface and
    `${CLAUDE_SKILL_DIR}/../ui/SKILL.md` exists;
  - **SPEC-002 v6, SKL-002 v6:** the PRD template's section 8 links the DSN instead of a raw canvas URL; after an extension
    that adds a requirement naming a screen, a flow or a user interface, the report says the DSN section 8 links is suspect
    and names `/devforgeai:ui BRN-NNN`;
  - **SPEC-003 v12, SKL-003 v10:** the architecture step reads each DSN the PRD's section 8 links as evidence (one EVD item,
    `kind: document`, `classification: context`; a board decides nothing), and its report names `/devforgeai:ui BRN-NNN`
    when an accepted ADR's consequence names a screen or the user interface and the PRD links a DSN;
  - **SPEC-011 v4, SKL-010 v3:** the context step re-reviews a bumped DSN as a suspect upstream of `ui-mockups.md` section 2.
    `front-end.md` section 6 is not a suspect-link site (§13, a).
- **Cycle D:** SPEC-016 v4 (an eighth tile for the ui phase, SPEC-016 v3 is approved) and the dashboard pane. `chain_state.py`
  lists any Markdown file with a frontmatter `id` under `docs/specs/`, so `design/` needs no change there; a `boards/README.md` has
  no frontmatter and is counted among the files it leaves out.
- **Codex.** The Codex port isn't changed; a port is for Codex sessions to build.
- **This change (cycle A)** adds only documents and `design.schema.json`, so no plugin version changes and nothing deploys.

## 11. Implementation plan

After approval of ADR-007 and this spec, in cycle B, through `/plugin-dev:skill-development` (and `/plugin-dev:create-plugin`),
on a branch in `.claude/worktrees/ui-skill-build` (ADR-001):
1. Write `src/tests/ui/test_dsn_check.py` (VER-23, VER-24) and `test_structure.py` (VER-25), and see them fail.
2. Write `scripts/dsn_check.py` until VER-23 and VER-24 pass, normally and under `python3 -S`.
3. Write `assets/dsn.md` (DM-01), `references/interview.md`, `references/boards.md` and `references/output-rules.md`,
   `SKILL.md` from §5 and §6 (lean, imperative, the checklist first), and `provenance.yaml` as SKL-013 implementing SPEC-017;
   VER-25 passes. Run skill-reviewer.
4. Write `src/tests/ui/make_evals.py` with the fixtures and the cases of VER-01 to VER-22; check the graders offline with good and
   bad replies; run `--keep-temp` pilots of writes-dsn and amend-changed-board; generate the cases into `evals/ui/`.
5. Run plugin-validator and an adversarial review; take any finding that would refuse valid work to Bryan.
6. Evaluate cheapest first (CLAUDE.md, "Evaluating a skill"): a few cases with `--runs 1 --ablation none`, the trigger cases on
   the three models, then the suite. Then deploy, and run VER-27 to VER-29 by hand; record the results in §9.
7. Update CLAUDE.md's skill table, the templates README rows and `.claude/rules/skills.md`'s tracked-skill note as needed.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| The skill reads the boards from the canvas | The eval sandbox can't reach a private artifact, and the live canvas changes under a run (ADR-007 D3; Bryan, 2026-10-08) |
| The boards live in the spec or the DSN itself | The files are large and change often; the DSN records a digest and the mapping instead |
| One skill for graphical screens and another for terminal screens | Bryan: terminal screens are designed in Claude Design too, and one skill covers both (2026-10-09); `surface` tells them apart |
| A design-story skill, or a second slot after the PRD | ADR-007 options 4 and 5: SPEC-009 owns story-level design, and the amend path is the second look |
| The skill edits the PRD's section 8, the ARCH evidence and `ui-mockups.md` itself | Each belongs to another skill, which re-reviews the DSN as a suspect upstream (ADR-007 D5); a skill that edits a neighbour's document breaks the rule that every document has one writer |
| `tokens` in the DSN, copied into `front-end.md` section 6 | Two owners of one fact; `front-end.md` keeps the conventions (ADR-004 D2; §13, a) |
| Read `boards/README.md` for the canvas version and digests | The README's form is no one's contract, and a script computes digests more reliably (§13, b) |
| Resolve policy as the prd skill does (R1, R2, `interview.max_calls`) | FR-012 is later; SPEC-004 §2 and SPEC-009 §2 decline for the same reason; it would also make this skill a fourth member of the byte-identical shared files (§13, f) |
| Check the DSN by reading it back only | Anthropic's guidance, applied in SPEC-011: what a script can decide is decided by a script; reading stays for judgment (IF-03) |
| Ask the user for the folder or file name | Skills allocate IDs and never take a file name from the user (CLAUDE.md); the script prints the next free number |
| Hand off to the architecture step from the ui skill | The PRD comes first in the chain (ADR-007 D1); the PRD's section 8 links the DSN |

## 13. Open questions

**Decided by Bryan** (quotes in §1 and ADR-007): one release-design skill after the brainstorm and before the PRD, with
story-level design staying in the story skill (2026-10-08); the name `ui` (2026-10-08, "ui (Recommended)"); the boards as
committed files, read by contract and never fetched from the canvas (2026-10-08); one slot with an amend path (2026-10-09);
the terminal and CLI scope (2026-10-09); ADR-007 and four cycles A to D (2026-10-09: "Yes, add ADR-007 (Recommended)", "Four
cycles A–D (Recommended)"). The Krepion session's page also records, as decided with Bryan, the neighbours' costs (§10), the
user-owned decisions of §1 and the report block; this spec follows those. Its checklist differs from the page's in two places,
(f) and (t) below.

**Drafter's choices, for Bryan's accept or challenge** (everything below goes beyond his quoted words and the page's "Decided"
lines):
- **(a) Token ownership.** The page's DSN carried a `tokens` block that `front-end.md` section 6 would copy, while its scope says
  `front-end.md` keeps the conventions and the DSN holds the screen designs. Chosen: **the context documents own the look.**
  The DSN has no `tokens`; `front-end.md` section 6 and `ui-mockups.md` section 2 stay as ADR-004 D2 gives them. So
  `front-end.md` section 6 is **not** a suspect-link site: it cites no DSN. A DSN bump is re-reviewed at the three sites the page
  names (PRD section 8, the ARCH evidence record, `ui-mockups.md` section 2), and that re-review can lead the user to update the
  tokens by a context run. Not carried over: the `tokens` block. Alternative: the DSN owns the tokens, `front-end.md` section 6
  cites it, and `front-end.md` becomes a fourth suspect-link site with the values duplicated.
- **(b) The `canvas.json` contract** (DM-04). Read: `v` and the keys of `boards` in order. Ignored: `attachments`, every
  other member and every board's own members. An unknown `v` stops the run (ERR-05), as Claude Design's format is undocumented
  and nothing says what another version means; supported: 3, the only one seen. The `boards/README.md` with SHA-256 digests
  that the Krepion copy has is **provenance for people, not input:** the skill never reads it; the script computes each board's
  digest and the DSN records it per board (`sha256`), which is also how an amend finds a changed board. The canvas version and
  URL come from the user's words (or are `null` with a marker). Alternatives: read the README as an input for the canvas
  version; a digest of the folder rather than of each board.
- **(c) An amend run when the BRN has also moved on** (BEH-08). Re-read the BRN at its current version in the same run, move
  the DSN's links to it, ask about the ideas newly promoted or no longer promoted, raise the DSN's version once, and say so in
  the Change Log row. Alternative: two runs, one for the BRN's move (a relink with no version bump) and one for the boards.
- **(d) Tracked, by ticks only** (§2). Like prd, epic and context: no `devforgeai-tracked` key and no manifest; the seven-step
  checklist of the page is what the tracker reads. A manifest for it is SPEC-012 §11's later work.
- **(e) The look in the DSN against `ui-mockups.md` section 2** (with a). `ui-mockups.md` section 2 stays the design-system
  reference (ADR-004 D2) and the place that names the canvas; cycle C has the context step cite the DSN there (`informed_by`),
  so a bumped DSN is a suspect upstream of exactly that section. The DSN records the canvas URL and version, never tokens.
- **(f) No policy resolution.** The page's step 1, 'Resolve policy (R1, R2)' and 'at most interview.max_calls calls', is not
  carried over: FR-012 is later, and SPEC-004 §2 and SPEC-009 §2 decline for the same reason. The interview is bounded by its
  structure instead (BEH-09: the canvas facts, one question for each flow, one for the ideas with no board; in an amend run
  one for each group of boards and each candidate). Alternative: adopt R1 and R2 and make this skill the fourth member of the
  byte-identical shared files (`test_shared_files.py`), which cycle B would then extend.
- **(g) The ID and the boards folder** (§4, BEH-05). The boards are copied into `docs/specs/design/DSN-NNN/boards/` before the
  DSN exists, so the skill computes the next free number (IF-01), requires the boards there, and the stop message names the exact
  folder. The page's text didn't say how a create run knows `NNN`.
- **(h) An amended approved DSN is `in-review`** (BEH-13), as the prd skill treats an extended PRD (SPEC-002 BEH-09), with
  approval cleared. The context skill sets `draft` instead (SPEC-011 BEH-13).
- **(i) A bundled script, `dsn_check.py`** (IF-01 to IF-03), for what a script can decide: the next number, the boards' contract
  and the DSN's rules. The page's report shows an 'OK docs/specs/design/DSN-001.md' line, which implies a checker. Alternative:
  read the DSN back against the self-check list only, as the prd skill does.
- **(j) A `surface` field** (`web`, `desktop`, `mobile`, `terminal`) on each board, so Bryan's terminal and CLI scope is visible
  and testable. The page had none. `terminal` rather than `cli`, to cover a text-mode screen that isn't a command-line tool.
- **(k) The idea coverage table** (DM-03), with the four statuses. It makes 'Ideas with no board' a recorded, user-confirmed
  fact and spares an amend run from asking again about ideas the user already placed. The page reports the line but had no home
  for the decision that an idea needs no screen.
- **(l) One DSN covers one BRN,** and a second DSN for the same BRN is refused in favour of an amend (BEH-04). A design for two
  brainstorms is two DSNs. The skill never deprecates a DSN.
- **(m) Boards are read to their first 150 lines** (DM-04), and a title is proposed from a `<title>`, `<h1>` or `<h2>`. The 150 is a
  guess to bound the context use of sixteen HTML boards of unknown size; VER-28 (b) measures it on the real boards.
- **(n) The title and owner:** the BRN's title followed by `: release design`, and the BRN's owner. The page's example title was
  hand-chosen.
- **(o) The `upstream` shape:** one `derives` link to the BRN with no `item`, so every DSN cites its brainstorm, and one with an
  `item` for each idea a board shows. The page's example had one item link only.
- **(p) The amend hand-off** (BEH-18): it names each citing document and its owning skill, in chain order, and says they re-review
  the DSN. The page said 'name the documents that cite DSN-001 at the old version'.
- **(q) The step is not a gate:** the prd skill works with no DSN, and the brainstorm's hand-off only recommends the step when
  a promoted idea names a screen (cycle C).
- **(r) `design.schema.json` holds its own `DSN` and `BRD` patterns** until cycle C (§10). Cycle A does not edit
  `common.schema.json`: the byte-identical copies would change three built skills.
- **(s) A bounded set of stop errors for the boards** (ERR-03 to ERR-06, ERR-12): the page named missing or empty boards, an
  unreadable `canvas.json`, an unknown `v` and a named board file that is absent; the names that aren't plain file names and the
  100-board limit are added.
- **(t) The approval is a separate step** in the checklist (step 6), after the check, as the context skill's is.
- **(u) An amend of a draft DSN raises the version too** (BEH-13; §6, worked example a). The alternative, editing a draft in
  place, was refused for the precedent of SPEC-002 BEH-09 and SPEC-011 BEH-13 (a revision raises the version of a draft
  too) and because a draft DSN may already be cited by a PRD, whose link then shows as suspect. The cost is a version number
  for each revision before the PRD.
- **(v) The report always prints the canvas version of the copy it read** (BEH-17), and an amend never keeps a stale one
  (BEH-10): the version describes the copy in `boards/`, which the user states, since no file is read for it (b). So a board
  changed on the canvas and not copied again never reaches the skill (DM-04), and the Boards line shows which copy that was.
  Added at the lead's request, 2026-10-09.
- **(w) A board's references to requirements and ADRs are plain `answers` fields,** not `upstream` links (DM-02). Bryan asked
  (2026-10-09, relayed) how screens found during the PRD or architecture steps reach the design; a board added in an amend may
  answer a PRD requirement or an accepted ADR's consequence, not only a brainstorm idea. A link from the DSN to the PRD would
  make a loop: the PRD's section 8 links the DSN (cycle C), so each document's bump would make the other's link suspect for
  ever (SPEC-011 BEH-11 avoids such a loop). The references therefore carry no version and no suspect tracking. The Change Log
  row names the versions read, the check errors on a reference to nothing and warns on a deprecated PRD item or an ADR no
  longer accepted. Alternatives: `informed_by` links (the loop); a one-way link from the PRD only (what cycle C does).
- **(x) The amend path's three triggers** (§6): a revision before any PRD, a PRD extension and an accepted ADR's consequence,
  each with an example. No trigger starts the skill; the user does, after drawing and copying the boards (ADR-007 D4).

**Open questions:**
- [NEEDS CLARIFICATION: how large the real Claude Design boards are, and whether the first 150 lines of a board give its heading and
  structure; Bryan can decide after VER-28 (b)]
- [NEEDS CLARIFICATION: whether other `canvas.json` versions exist; Claude Design's format is not documented, so version 3 is the
  only one supported until a person checks another and a spec version adds it]
- [NEEDS CLARIFICATION: whether one DSN may cover several brainstorms (a release drawn from two), which §13 (l) refuses for now]
- [NEEDS CLARIFICATION: whether a draft or in-review DSN makes the PRD that links it a proposal, as ADR-004 D5 does for a draft
  context document; cycle C's SPEC-002 v6 decides]
- [NEEDS CLARIFICATION: whether the story skill's design brief should list the DSN's boards that bear on the story, as SPEC-009
  version 3 BEH-11 has it do (that spec's drafter's choice); Bryan decides there]
- [NEEDS CLARIFICATION: whether the framework should ask whoever copies the boards to leave a `boards/README.md` of digests, as the
  Krepion copy has; (b) treats such a file as provenance for people and never reads it]

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-10-09 | claude-code (session 7637882f-b2ec-465e-988a-9602340d1023) | Initial draft, cycle A of ADR-007 (proposed), from Bryan's decisions of 2026-10-08 and 2026-10-09 and the Krepion session's spec page 'A UI Skill for DevForgeAI' (version 6): the create and amend paths, the boards read by contract, the interview, the check and the hand-off. The page's tokens block and its policy step are not carried over; the drafter's choices are in §13 for Bryan's accept or challenge. Awaiting the drafts review and Bryan's decision; it can't be approved before ADR-007 is accepted | all |
| 1 | 2026-10-09 | claude-code (session 7637882f-b2ec-465e-988a-9602340d1023) | Before review, on the lead's additions of the same day (Bryan's question on how screens found during the PRD or architecture steps, and revisions after the brainstorm, reach the design): board items gain `answers` (PRD requirements and accepted ADRs, plain fields, not links; §13 w); the report always prints the canvas version of the copy it read, and an amend never keeps a stale one; §6 gains the amend path with three triggers and an example each (§13 u, x); a draft's amend raises the version; new ERR-17 (nothing to amend); new VER-30 to VER-33; the checker's `mapping` and `boards` rules cover `answers` | §1, DM-01, DM-02, DM-04, IF-03, BEH-07, BEH-09, BEH-10, BEH-13, BEH-17, ERR-17, VER-24, VER-26, VER-30 to VER-33, §6, §9, §13 |
