# PRD output rules

## Contents

- When to use this
- Frontmatter
- Links
- Item blocks
- Collections and fields
- Markers
- Change Log and resolution line
- Leftovers
- Self-check list

## When to use this

Read this before writing a PRD, and check the written file against the **Self-check list** when
`devforgeai check --json` is unavailable (not on PATH, or output that isn't JSON). These rules restate
the PRD schema. A file that breaks any of them is invalid.

## Frontmatter

The YAML between the first two whole `---` lines. Allowed keys, and **no others**:

| Key | Rule |
|---|---|
| `id` | `PRD-NNN`: three digits, for example `PRD-001` |
| `type` | exactly `prd` |
| `title` | quoted string naming the product or release |
| `status` | `draft`, `in-review`, `approved`, `superseded` or `deprecated`. The skill writes only `draft`, or `in-review` when extending an approved PRD. **Never `approved`** |
| `version` | integer, at least 1 |
| `created`, `updated` | `YYYY-MM-DD` |
| `owner` | quoted string |
| `authors` | list of strings |
| `generated_by` | map with only `tool`, `model`, `session`, each a quoted non-empty string |
| `reviewed_by` | `[]` when the skill writes the file |
| `approved_by` | quoted string (`""` unless a person approved it) |
| `approved_on` | `YYYY-MM-DD` or `null` |
| `upstream` | list of link records |
| `supersedes` | list of document IDs |
| `superseded_by` | document ID or `null` |
| `blocked_by` | list of `DOC-NNN` or `DOC-NNN#ITEM-NN` strings |
| `target_release` | quoted string, the name of the release `current` items belong to |
| `stage` | `prototype`, `mvp`, `evolution` or `null` |
| `operating_context` | `local`, `internal`, `pilot`, `production` or `null` |
| `stakeholders` | list of strings |

`stage` and `operating_context` are written only when the user supplied or confirmed them. Otherwise
they are `null`. The template's `#` comments after them may be deleted.

## Links

A link record has only `id` (a document ID), optional `item`, `relation`, `version` (integer),
`hash` and optional `note`. Write every link record in **flow style, keys in this order**:

```yaml
- {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

- **`hash` is always `null`.** Only the checker writes hashes.
- `version` is the upstream document's current `version`.
- A link lives in exactly one place: on the item that owns it, or in the frontmatter when the whole
  PRD owns it. Never repeat a link in prose; prose uses the qualified reference `BRN-001#PRB-01`.

Which links go where:

| Source | Where | Relation |
|---|---|---|
| BRN problem | frontmatter `upstream` | `derives` |
| promoted BRN idea | the FR's (or SM's) `upstream` | `derives` |
| BRN assumption | the ASM's `upstream` | `derives` |
| accepted ADR that applies | frontmatter `upstream` | `constrains` |
| another PRD's constraint or cross-cutting NFR (BEH-15) | frontmatter `upstream`, with `item` | `constrains` |
| policy `architecture.mandated_platforms` setting | the `upstream` of the constraint NFR it produced, **never also in frontmatter** | `constrains` |
| `interview.max_calls` or `quality.required_categories` setting that applied | frontmatter `upstream`, with `item: SET-NN` and the policy `version` | `informed_by` |

Never cite an open, parked or rejected idea, anywhere: not in a link, not in prose, not as
`IDEA-NN` text. Describe a parked or rejected idea in words when it becomes a non-goal. Never link a
proposed, rejected or superseded ADR.

## Item blocks

- An item block is a fence whose info string is exactly `yaml items`.
- Each fence has **exactly one top-level key**: `success_metrics`, `functional_requirements`,
  `non_functional_requirements` or `assumptions`.
- Inside a fence, use only `#` comments. `<!-- -->` never goes inside a fence.
- **Quote every free-text value** with `"…"`. Unquoted text starting with `>`, `|`, `*`, `&`, `!`,
  `@`, `%` or a backtick, or containing `: ` or ` #`, changes meaning. Words like `no` and `yes`
  change type.
- Enum values (`status`, `category`, `priority`, `release`, `state`), `null` and item IDs stay unquoted.
- Lists of prose use block sequences (`- "…"`), never flow lists.
- Items are never deleted or renumbered. Retire one with `status: deprecated` (and `superseded_by`).
- A collection with no items is written as `success_metrics: []` (or the matching key), never omitted.

## Collections and fields

Every item may also carry `superseded_by` (an item ID or `null`) and `upstream` (link records).
Write the keys in the order shown.

**`success_metrics`**: IDs `SM-01`, `SM-02`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `SM-NN` |
| `status` | yes | `active` or `deprecated` |
| `metric` | yes | quoted string |
| `baseline` | no | quoted string |
| `target` | yes | quoted string; `"[NEEDS CLARIFICATION: target for <metric>]"` when unknown |
| `measured_by` | no | quoted string |

**`functional_requirements`**: IDs `FR-001`, `FR-002`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `FR-NNN` |
| `status` | yes | `active` or `deprecated` |
| `statement` | yes | quoted, starts `"The system shall` |
| `priority` | yes | `must`, `should`, `could`, `wont` or `null` |
| `release` | yes | `current`, `later` or `null` |
| `notes` | no | quoted string or `null` |
| `upstream` | yes (skill rule) | at least one `derives` link to a promoted BRN idea |

**`non_functional_requirements`**: IDs `NFR-001`, `NFR-002`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `NFR-NNN` |
| `status` | yes | `active` or `deprecated` |
| `category` | yes | `performance`, `security`, `privacy`, `accessibility`, `reliability`, `compliance`, `observability`, `usability`, `maintainability`, `constraint` or `other` |
| `statement` | yes | quoted string, measurable where possible |
| `priority` | yes | as for FRs |
| `release` | yes | as for FRs |

Write NFR keys in the order `id`, `status`, `category`, `statement`, `priority`, `release`, then `upstream` if any.

**`category: constraint`** records a fixed external condition: a mandated platform, a required
integration, data residency, an existing system or a regulatory mandate. Its statement names the
condition, not a design, and ends with where it applies, for example `"… (applies to the whole
product)"`, `"… (applies to online payments)"` or `"… (applies to production)"`. An architecture style,
a framework or any other design preference is never a constraint unless the user said it is a hard
constraint; otherwise it goes to open questions (see Markers).

**`assumptions`**: IDs `ASM-01`, `ASM-02`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `ASM-NN` |
| `status` | yes | `active` or `deprecated` |
| `statement` | yes | quoted string |
| `validation` | no | quoted string |
| `state` | yes | `open`, `validated` or `invalidated` |

**Null decisions.** `stage`, `operating_context`, every `priority` and every `release` are `null` unless
the user supplied or confirmed the value. A suggestion the user did not confirm is never written. A PRD
with any of them `null` can't be approved; that is expected for a draft.

**`priority: wont` with `release: current`** is an explicit exclusion from the current release ("won't have
this time"). The current release delivers only `release: current` items with `must`, `should` or `could`.
Downstream, no epic is written for a `wont` item.

## Markers

Each marker is one bullet in section 12 (Open questions) unless it sits inside a quoted item value.

- Unknown: `[NEEDS CLARIFICATION: <question>]`, with the question written out.
- Required quality category not answered (BEH-03), exactly:
  `[NEEDS CLARIFICATION: <category> requirements for <context>]`, for example
  `[NEEDS CLARIFICATION: compliance requirements for production]`. `<context>` is the established
  operating context, or `production` when it was resolved as the fail-safe. Never write a placeholder
  NFR for an unanswered category.
- Open architecture decision (BEH-16), exactly:
  `[NEEDS ADR: <decision>; affects FR-NNN, FR-NNN]`, naming every requirement whose epics it blocks.
  It doesn't block approval of the PRD; it blocks epics for the named requirements.
- Design preference that is not a hard constraint (BEH-07): a plain bullet
  `Design preference for a future ADR: <preference> (not a requirement)`.

## Change Log and resolution line

The Change Log table has columns Version, Date, Author, Change, Items affected. Each row the skill
adds has today's date and author `claude-code`. The **Change** cell of that row ends with the policy
resolution line, as one line with no line break:

`Policy resolution: <entry>; <entry>; …`

The entry forms and their order are in `policy.md` (Resolution line). A `|` never appears inside the
cell; write the line exactly as `policy.md` specifies.

## Leftovers

None of these may remain in the written file:

- template placeholders: `PRD-000`, `BRN-000`, `YYYY-MM-DD`, or any `<…>` text such as `<outcome>`,
  `<metric>` or `<capability>`;
- `<!-- -->` author comments, **except** the GENERATED comment under `## 13. Epic map`, which stays;
- an empty `title` or `owner`, an empty `generated_by` value, or an empty Change Log date or author cell;
- the template's example items (the `BRN-000` links, `"<p95 latency …>"`).

## Self-check list

Read the written file back, then confirm each line:

1. The file is `docs/specs/prd/PRD-NNN.md`, and `NNN` matches the frontmatter `id`.
2. The frontmatter has only the allowed keys, with the types above. `status` is not `approved`.
3. `generated_by` has non-empty `tool`, `model` and `session`, and no `${` text remains anywhere.
   `reviewed_by` is `[]`. Every `hash` is `null`.
4. Every `yaml items` fence has exactly one top-level key, from the four collections.
5. Every item has its required fields, uses only allowed fields, and has an ID in the right pattern,
   with no duplicates and no gaps introduced by this run.
6. Every free-text value is quoted. Enum values are from the allowed lists, or `null` where allowed.
7. Every FR has a `derives` link to a promoted idea of the BRN. No open, parked or rejected idea ID
   appears anywhere in the file.
8. Every link record has `id`, `relation` and `version`; relations and placements follow Links.
9. Markers use the exact forms in Markers. Each required category left unanswered has its marker.
10. Every heading from the template is still present, including `## 13. Epic map` with its GENERATED comment.
11. The newest Change Log row carries one `Policy resolution:` line.
12. No leftovers from the list above remain.
