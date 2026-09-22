# BRN output rules

## Contents

- When to use this
- Frontmatter
- Item blocks
- Collections and fields
- Leftovers
- Self-check list

## When to use this

Read this before writing a BRN file, and check the written file against the **Self-check list**
when `devforgeai check --json` is unavailable (not on PATH, a non-zero exit, or output that isn't
JSON). These rules restate the brainstorm schema. A file that breaks any of them is invalid.

## Frontmatter

The YAML between the first two whole `---` lines. Allowed keys, and **no others**:

| Key | Rule |
|---|---|
| `id` | `BRN-NNN`: three digits, for example `BRN-001` |
| `type` | exactly `brainstorm` |
| `title` | quoted string |
| `status` | `draft`, `converged` or `archived` |
| `version` | integer, at least 1 |
| `created`, `updated` | `YYYY-MM-DD` |
| `owner` | quoted string |
| `authors` | list of strings |
| `generated_by` | map with only `tool`, `model`, `session`, each a quoted string |
| `reviewed_by` | list of strings (`[]` when the skill writes the file) |
| `approved_by` | quoted string (`""`) |
| `approved_on` | `YYYY-MM-DD` or `null` |
| `upstream` | list of link records (usually `[]`) |
| `supersedes` | list of document IDs |
| `superseded_by` | document ID or `null` |
| `blocked_by` | list of `DOC-NNN` or `DOC-NNN#ITEM-NN` strings |
| `participants` | list of strings |
| `sources` | list of strings |

Required: every key above except `generated_by`, `reviewed_by`, `approved_by`, `approved_on`,
`participants` and `sources`. The skill writes all of them anyway.

A link record has only `id` (a document ID), optional `item`, `relation`, `version` (integer),
`hash` and optional `note`. **`hash` is always `null`.** Only the checker writes hashes.

## Item blocks

- An item block is a fence whose info string is exactly `yaml items`.
- Each fence has **exactly one top-level key**: `problems`, `ideas` or `assumptions`.
- Inside a fence, use only `#` comments. `<!-- -->` never goes inside a fence.
- **Quote every free-text value** with `"…"`. Unquoted text starting with `>`, `|`, `*`, `&`, `!`,
  `@`, `%` or a backtick, or containing `: ` or ` #`, changes meaning. Words like `no` and `yes`
  change type.
- Enum values (`status`, `severity`, `disposition`, `state`) and item IDs stay unquoted.
- Lists of prose use block sequences (`- "…"`), never flow lists (`[a, b]`).
- Items are never deleted or renumbered. Retire one with `status: deprecated` (and
  `superseded_by: IDEA-NN` if something replaced it).

## Collections and fields

These are the only collections and fields. Every item may also carry `superseded_by` (an item ID
or `null`) and `upstream` (a list of link records).

**`problems`**: IDs `PRB-01`, `PRB-02`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `PRB-NN` |
| `status` | yes | `active` or `deprecated` |
| `statement` | yes | quoted string |
| `who` | no | quoted string |
| `evidence` | no | quoted string |
| `severity` | no | `high`, `medium` or `low` |

**`ideas`**: IDs `IDEA-01`, `IDEA-02`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `IDEA-NN` |
| `status` | yes | `active` or `deprecated` |
| `idea` | yes | quoted string |
| `addresses` | no | block list of `PRB-NN` IDs that exist in the file |
| `value`, `effort`, `risk` | no | quoted string or `null` |
| `score` | no | number, quoted string or `null` |
| `disposition` | yes | `open`, `promoted`, `parked` or `rejected` |
| `reason` | no | quoted string or `null` |

**`assumptions`**: IDs `ASM-01`, `ASM-02`, …

| Field | Required | Rule |
|---|---|---|
| `id` | yes | `ASM-NN` |
| `status` | yes | `active` or `deprecated` |
| `statement` | yes | quoted string |
| `validation` | no | quoted string |
| `state` | yes | `open`, `validated` or `invalidated` |

Anything else, such as a framework's own scores, goes in the prose of section 5 (Evaluation method)
or section 6 (Convergence), never as a new key.

## Leftovers

None of these may remain in the written file:

- template placeholders: `BRN-000`, `YYYY-MM-DD`, or any `<…>` text such as `<topic>`, `<persona>` or `<signal>`;
- `<!-- -->` author comments;
- an empty `title` or `owner`, or an empty `generated_by` value.

Unknowns are written as `[NEEDS CLARIFICATION: <question>]`, with the question filled in, never as a guess.

## Self-check list

Read the written file back, then confirm each line:

1. The file name is `BRN-NNN-<slug>.md` and matches the frontmatter `id`.
2. The frontmatter has only the allowed keys, with the types above.
3. `generated_by` has non-empty `tool`, `model` and `session`. `reviewed_by` is `[]`. Every `hash` is `null`.
4. Every `yaml items` fence has exactly one top-level key, from the three collections.
5. Every item has its required fields, uses only allowed fields, and has an ID in the right pattern, with no duplicates.
6. Every free-text value is quoted. Enum values are from the allowed lists.
7. Every `addresses` entry names a `PRB-NN` that exists in the file.
8. Every heading from the template is still present.
9. No leftovers from the list above remain.
