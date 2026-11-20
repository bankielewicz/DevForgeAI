# BRN output rules

## Contents

- When to use this
- File and IDs
- Frontmatter
- Item blocks
- Collections and fields
- Project kind, sources and sections 3 and 8
- First release cut and risk ranking
- Unknowns
- Change Log
- Validation checklist
- Example item blocks

## When to use this

Read this before writing a BRN document, and use the validation checklist after writing it. The
rules exist because the PRD workflow and the `devforgeai check` validator parse these documents
mechanically. A document that reads well but breaks a rule here breaks everything downstream.

## File and IDs

| What | Pattern | Rule |
|---|---|---|
| Document ID | `BRN-NNN` (three digits, e.g. `BRN-007`) | Next free number in `docs/specs/brainstorm/` |
| File path | `docs/specs/brainstorm/BRN-NNN.md` | Named by the ID only; the topic goes in `title` |
| Problem ID | `PRB-NN` (e.g. `PRB-01`) | Unique in the document |
| Idea ID | `IDEA-NN` (e.g. `IDEA-03`) | Unique in the document |
| Assumption ID | `ASM-NN` (e.g. `ASM-02`) | Unique in the document |

Number items from `01` in each collection, in order. IDs are never reused, renumbered or deleted.
When referring to an item in prose, use the qualified form `BRN-001#IDEA-03`.

## Frontmatter

Keep exactly these keys, in this order. Unknown or misspelled keys are errors.

| Key | Value |
|---|---|
| `id` | `BRN-NNN`, equal to the file name |
| `type` | `brainstorm` |
| `title` | Quoted descriptive topic, never empty |
| `status` | `draft`, `converged` or `archived` |
| `version` | Integer, `1` for a new BRN |
| `created`, `updated` | Unquoted `YYYY-MM-DD` dates |
| `owner` | Quoted name of the accountable human |
| `authors` | List of quoted names, e.g. `["Bryan", "claude-code"]` |
| `generated_by` | Map with quoted `tool`, `model` and `session`, all non-empty |
| `reviewed_by` | `[]` (only humans who reviewed it; never filled by the AI) |
| `approved_by` | `""` |
| `approved_on` | `null` |
| `upstream` | `[]`, or link records (usually `relation: informed_by`); in a brownfield BRN, one per document read |
| `supersedes` | `[]` |
| `superseded_by` | `null` |
| `blocked_by` | `[]` |
| `participants` | List of quoted names, or `[]` |
| `sources` | `[]`, or one quoted `"<kind>: <reference>"` string per input used (*Project kind, sources and sections 3 and 8*) |

Keep the `# --- brainstorm-specific ---` comment line before `participants`.

A link record is written in flow form, one per line:

```yaml
upstream:
  - {id: BRN-001, relation: informed_by, version: 1, hash: null, note: "optional"}
```

`hash` is always `null`. Only the validator writes hashes; a typed hash is wrong by definition.

## Item blocks

- An item block is a fenced block whose info string is exactly `yaml items`.
- Each fence holds **exactly one top-level key**: `problems`, `ideas` or `assumptions`.
- Inside a fence use `#` comments only. `<!-- -->` notes may not appear inside a fence (and none
  remain in a finished BRN).
- **Quote every free-text value** with double quotes. Unquoted text that starts with `>`, `|`,
  `*`, `&`, `!`, `@`, `%` or a backtick, or that contains `: ` or ` #`, silently changes meaning.
  Unquoted `yes`, `no` or `3.10` change type.
- For lists of IDs or prose, use block sequences (`- PRB-01`), never flow lists (`[PRB-01, PRB-02]`).
- IDs, enum values, `null` and numbers are not quoted.

## Collections and fields

Each item has `id` and `status` (`active` or `deprecated`), and may have `superseded_by` (an item
ID) and `upstream` (a list of link records). Besides those, only these fields are allowed:

**`problems`**

| Field | Value |
|---|---|
| `statement` | Quoted, one sentence, from the user's side |
| `who` | Quoted persona, with no vertical bar in it, spelled the same way in every problem |
| `evidence` | Quoted fact that ends with one `sources` entry in parentheses, or `"[NEEDS CLARIFICATION: …]"`. In a BRN without the project-kind line: quoted source or data |
| `severity` | `high`, `medium` or `low` |

**`ideas`**

| Field | Value |
|---|---|
| `idea` | Quoted idea; the user's own words when the idea came from the user |
| `addresses` | Block list of one or more `PRB-NN` IDs that exist in this document |
| `value`, `effort`, `risk` | `null`, or a quoted string per the framework: a rating such as `"high"`, or a number written in quotes such as `"800"` |
| `score` | `null` or a number, per the framework |
| `disposition` | `open`, `promoted`, `parked` or `rejected`; anything but `open` only when user-confirmed |
| `reason` | `null` while `open`; otherwise a quoted reason the user confirmed |

**`assumptions`**

| Field | Value |
|---|---|
| `statement` | Quoted, phrased "We believe that …" |
| `validation` | Quoted experiment, interview or data that would confirm it |
| `state` | `open`, `validated` or `invalidated` |

No other collections and no other fields. Put method-specific reasoning in the prose sections.

## Project kind, sources and sections 3 and 8

These rules hold for a BRN that has the project-kind line (a *new-shape* BRN): a line after the
frontmatter and outside every fenced block that starts with `Project kind:`. A BRN without it keeps
its earlier shape, also when extended, and is checked by the other rules only.
[intake.md](intake.md) says how to fill each part.

| Part | Form |
|---|---|
| Project kind | The first line under `## 1. Context`, followed by a blank line: `Project kind: greenfield`, `Project kind: brownfield` or `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]`. With the third, and only then, section 7 holds one bullet `- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]`, or the same with `worked as brownfield` |
| `sources` | Each entry `"<kind>: <reference>"`, the kind one of `document`, `data`, `ticket`, `interview`, `url`, `note`; no vertical bar; no entry twice |
| A cited fact: an active problem's `evidence`, a section 8 baseline | One `[NEEDS CLARIFICATION: …]` marker and nothing else, or text that ends with one `sources` entry, without its quotes, in parentheses after a space |
| Section 3 | Only the table `\| Persona \| Job to be done \| Current workaround \| Pain \|`: one row per distinct `who` value of the active problems, in the order the values first appear, the Persona cell equal to the `who` value; four non-empty cells in each row |
| Section 8 | One bullet `- IDEA-NN: <outcome>; baseline <cited fact>` for each active idea whose row in section 6's *First release cut* table says `yes`, in ID order; with none, the single line `- None.` |

A BRN whose kind is `brownfield` also holds the four parts below; a `greenfield` BRN holds none of
them; while the kind is not decided it holds all four when the run worked as brownfield and none
when it worked as greenfield. [brownfield.md](brownfield.md) says how to fill each.

| Part | Form |
|---|---|
| `### Existing product`, in section 1 after the context prose | The table `\| Document \| Version \| What it already covers \|`, one row per document read (a BRN, PRD, EPIC or ARCH ID, never this BRN; its version), or the line `No document was found in the project.`; then any `Skipped: <path> (<reason>)` lines. Each row's document has an `upstream` record `{id: <ID>, relation: informed_by, version: <version>, hash: null}` and the `sources` entry `"document: docs/specs/<folder>/<ID>.md v<version>"` |
| `### Already covered`, in section 6 | The table `\| Suggestion \| Covered by \|`, `Covered by` being `PRD-NNN#FR-NNN`, `PRD-NNN#NFR-NNN`, `EPIC-NNN#DW-NN` or `ARCH-NNN#CMP-NN` of a document Existing product lists; or the line `None.` |
| `### Previously decided`, in section 6 | The table `\| Idea \| Decision \| Where \|`, `Decision` being `rejected` or `parked` and `Where` `BRN-NNN#IDEA-NN` of a BRN Existing product lists, each once; or the line `None.` An idea of this BRN that carries an item-level `upstream` link to such an idea is not listed |
| `### Assumption updates`, last in section 6 | The table `\| Earlier assumption \| Change \| Evidence \| Status \|`: `BRN-NNN#ASM-NN` of a BRN Existing product lists, or of this BRN, each once; `open to validated` or `open to invalidated`; a fact ending with one `sources` entry in parentheses; `proposed, not confirmed` or `confirmed on YYYY-MM-DD`. Or the line `None.` |

Section 6's subsections stand in this order: First release cut, Already covered, Previously
decided, Assumption updates.

## First release cut and risk ranking

Two prose tables carry the path to a first release. [mvp-path.md](mvp-path.md) defines every cell; the
validator checks them (MV-01 to MV-12) in a BRN that has the `Project kind:` line.

| Where | Heading | Holds |
|---|---|---|
| Section 7, after the `assumptions` block and before the bullets | `### Assumption risk ranking` | One row per active assumption whose `state` is `open`: `Rank`, `Assumption`, `If wrong`, `Confidence`, `Cheapest test`. `None.` when there is no such assumption |
| Section 6, after the convergence prose | `### First release cut` | The status line, then one row per active idea that is promoted or proposed for promotion: `Idea`, `In first release` (`yes` or `no`), `Why`. `No idea is promoted or proposed for promotion.` when there is no such idea |

The status line is `First release cut: proposed, not confirmed` until the user confirms the cut, then
`First release cut: confirmed on YYYY-MM-DD`, with that day's date and no name. A cell never holds a
`|`. Section 8 lists exactly the ideas whose row says `yes` (see *Collections and fields* for its bullets).

## Unknowns

Never guess. Write `[NEEDS CLARIFICATION: <question>]` where the answer is unknown, in prose or
inside a quoted value. Section 7 also lists open questions as `- [NEEDS CLARIFICATION: …]` bullets;
if there are none, write `- None.`

## Change Log

Add one row per version: version, date, author, what changed. When you write the row, the author
is `claude-code (session <session ID>)`, with the same ID as `generated_by.session`:

```markdown
| 2 | 2026-09-27 | claude-code (session 7b7b72c0-8b14-4b7d-aba5-f21cdbadc51f) | Added IDEA-13 to IDEA-22 |
```

The session ID is the name of that conversation's transcript, so `claude --resume <ID>` can reopen
it. Never edit earlier rows: they record the sessions that wrote earlier versions.

## Validation checklist

Check each item; fix and re-check anything that fails.

1. The file path is `docs/specs/brainstorm/BRN-NNN.md` and `id` equals `BRN-NNN`.
2. The frontmatter has exactly the keys in the Frontmatter table, with valid values.
   `generated_by` has non-empty `tool`, `model` and `session`, `reviewed_by` is `[]`, and every
   `hash` is `null`.
3. Every item ID matches its pattern, is unique, and is numbered in order.
4. Every `yaml items` fence holds exactly one top-level key: `problems`, `ideas` or `assumptions`.
5. Every item has only allowed fields, and every enum value is in its list.
6. Every free-text value is double-quoted, and no flow lists are used for IDs or prose.
7. Every `addresses` entry names a `PRB-NN` that exists in the document.
8. `disposition` is not `open`, and `status` is `converged`, only where the user confirmed it.
9. All eight numbered section headings and `## Change Log` are present.
10. No leftovers remain: no `<!--`, no `<…>` placeholders, no `BRN-000`, no `YYYY-MM-DD`, and no
    empty `title`.
11. The last Change Log row's author is `claude-code (session <ID>)` with the ID in
    `generated_by.session`, unless a person wrote that row.
12. In a BRN with the project-kind line: that line is exact, first under `## 1. Context` and
    followed by a blank line; while it is the NEEDS CLARIFICATION line, and only then, section 7
    holds the one bullet that says which kind the run worked as; every `sources` entry has the form `"<kind>: <reference>"` and stands
    once; every active problem's `evidence` and every section 8 baseline is one marker or ends with
    a `sources` entry in parentheses; section 3 is the Target users table with one row per `who`
    value; section 8 has one bullet per first-release idea, or the line `- None.`
13. In a brownfield BRN: `### Existing product` in section 1 and `### Already covered`,
    `### Previously decided` and `### Assumption updates` in section 6, in that order, each
    holding its table or its replacement line; every document of Existing product has its
    `upstream` record and its `sources` entry; every `Covered by` and `Where` cites a listed
    document; every Evidence cell ends with a `sources` entry; and every `confirmed on` status is
    one the user confirmed. A greenfield BRN has none of the four headings.
14. In a BRN with the `Project kind:` line: section 7 holds `### Assumption risk ranking` and section 6
    holds `### First release cut`, each cell as [mvp-path.md](mvp-path.md) defines it; the cut's status
    line says `confirmed` only where the user confirmed the cut.

## Example item blocks

````markdown
```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Patients forget appointments booked weeks ahead."
    who: "Returning patient"
    evidence: "[NEEDS CLARIFICATION: current no-show rate]"
    severity: high
```

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Text a reminder two days before, with a one-tap reschedule link."
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: 4
    disposition: open
    reason: null
```
````
