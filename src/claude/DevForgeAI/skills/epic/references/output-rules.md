# Epic output rules

## Contents

- When to use this
- Frontmatter
- Links
- Sections
- The done-when block
- Change Log
- Leftovers
- Self-check list

## When to use this

Read this before writing an epic (step 7), and check every epic written against the **Self-check list**
(step 8). These rules restate `epic.schema.json` and the template. A file that breaks any of them is invalid.
Never call a `devforgeai` command to validate.

## Frontmatter

The YAML between the first two whole `---` lines. Allowed keys, in the template's order, and **no others**:

| Key | Rule |
|---|---|
| `id` | `EPIC-NNN`: three digits, matching the file name |
| `type` | exactly `epic` |
| `title` | quoted: the capability, for example `"Members manage their own bookings"` |
| `status` | `draft`. **Never anything else**: only the user approves an epic |
| `version` | `1` |
| `created`, `updated` | today, `YYYY-MM-DD` |
| `owner` | quoted: the user's name, else the PRD's `owner` |
| `authors` | list: the user's name (if known) and `claude-code`. Never invent a name |
| `generated_by` | map with only `tool` (`"claude-code"`), `model` (your model ID) and `session` (`"${CLAUDE_SESSION_ID}"`, substituted), each quoted and non-empty |
| `reviewed_by` | `[]` |
| `approved_by`, `approved_on` | `""` and `null` |
| `upstream` | link records (Links) |
| `supersedes` | `[]` |
| `superseded_by` | `null` |
| `blocked_by` | `[]` |
| `priority` | `must`, `should` or `could` (SKILL.md step 6, and `selection.md`, Priority and numbering) |
| `target_release` | the PRD's `target_release`, quoted. If the PRD has none, `""` and a marker in section 8 |

## Links

The whole epic owns its links, so they all go in the frontmatter `upstream`, in flow style with the keys in
this order:

```yaml
upstream:
  - {id: PRD-004, item: FR-021, relation: refines, version: 3, hash: null}
  - {id: PRD-004, item: NFR-004, relation: refines, version: 3, hash: null, note: "partial: booking pages only"}
  - {id: PRD-004, item: SM-02, relation: informed_by, version: 3, hash: null, note: "raises the share of online bookings"}
  - {id: ARCH-002, relation: informed_by, version: 5, hash: null}
```

- **One `refines` link for every requirement the epic groups**, and for no other requirement, at the PRD's
  `version`. An attached NFR that is shared or applies only in part carries `note: "partial: <which part>"`.
- **One `informed_by` link to the ARCH** the readiness came from, with no `item`, at **the ARCH's own
  `version`** (not the PRD's).
- Optionally, one `informed_by` link for each PRD success metric the epic moves, with a note saying how.
- Never link a left-out or covered requirement, an ADR, a DEC or a policy setting.
- `hash` is always `null`. Only the checker writes hashes.
- Prose uses qualified references such as `PRD-004#FR-021` or `ARCH-002#DEC-11`, never another link record.
- Done-when items carry no `upstream`: stories satisfy them later.

## Sections

Keep every heading of `${CLAUDE_SKILL_DIR}/assets/epic.md`, in order, with the title line
`# EPIC-NNN — <capability name>`. Delete every author comment, except the GENERATED comment under
`## 7. Story map`, which stays exactly as it is.

| Section | Content |
|---|---|
| 1. Goal | One paragraph: what users can do when this epic is done that they can't do today. If the PRD or the ARCH is a draft, it starts with the proposal line (below) |
| 2. Business value | Prose: why it matters, naming the success metrics it moves as qualified references |
| 3. Scope | **In scope:** one bullet per requirement the epic refines, `PRD-NNN#FR-NNN: <short statement>`. **Out of scope:** related requirements left out or in other epics, each with its reason or epic ID, or `- Not planned.` |
| 4. Done when | The `done_when` block (below) |
| 5. Dependencies and risks | Prose: the other epics written in this run it depends on, and the ARCH decisions it relies on, as qualified references (`ARCH-002#DEC-11`). Hard blockers would go in `blocked_by`, which stays `[]` because only ready requirements are included |
| 6. Technical notes (optional) | High-level constraints from the ARCH, such as components, or `None.` |
| 7. Story map | Only the template's GENERATED comment. Never list stories |
| 8. Open questions | One `- [NEEDS CLARIFICATION: <question>]` bullet per unknown, or `- None.` |

**The proposal line.** When the PRD or the ARCH has `status: draft`, the first line of section 1 is:
`**Proposal:** <ID> is a draft, so this epic is a proposal until its inputs are approved.` Name each draft input.

**The unconfirmed grouping.** When no one confirmed the grouping (SKILL.md step 6), section 8 contains exactly:
`- [NEEDS CLARIFICATION: grouping proposed by the skill; not confirmed by the user]`

## The done-when block

- One fence whose info string is exactly `yaml items`, with the single top-level key `done_when`.
- At least one item. IDs `DW-01`, `DW-02`, … in order. Each item has only `id`, `status: active`,
  `criterion` and `evidence_method`.
- `criterion` is an integrated outcome that can only be checked once several stories are done, broader than a
  story's acceptance criteria. `evidence_method` says how it is shown: an end-to-end test, a demo or a metric.
- Quote every free-text value with `"…"`. No `#` comments and no `<!-- -->` inside the fence.

```yaml
done_when:
  - id: DW-01
    status: active
    criterion: "A member books, cancels and rebooks a class place on a phone without staff help"
    evidence_method: "End-to-end test on the staging site"
```

## Change Log

Keep the template's table (Version, Date, Author, Change) with one row: `1`, today, `claude-code`, and
`Initial draft from PRD-NNN vN and ARCH-NNN vM`.

## Leftovers

None of these may remain in a written epic:

- `EPIC-000`, `PRD-000`, `YYYY-MM-DD`, or any `<…>` placeholder such as `<capability name>`, `<item>` or
  `<integrated outcome>`;
- any `<!-- -->` comment other than the story map's GENERATED comment;
- the template's example links and the example marker `[NEEDS CLARIFICATION: <question>]`;
- a trailing `#` comment on any frontmatter line (such as `# draft | in-review | …` or `# must | should | could`);
- an empty `title`, `owner` or `generated_by` value, or an empty Change Log date or author cell.

## Self-check list

Read each epic written back, then confirm each line.

1. The path is `docs/specs/epic/EPIC-NNN.md`, `NNN` matches the frontmatter `id`, and the number was free.
2. The frontmatter has only the allowed keys. `status: draft`, `version: 1`, `reviewed_by: []`,
   `approved_by: ""`, `approved_on: null`, and `target_release` is the PRD's.
3. `generated_by` has non-empty `tool`, `model` and `session`, and no `${` text remains anywhere. Every
   `hash` is `null`.
4. `upstream` has one `refines` link, at the PRD's version, for each requirement in the confirmed grouping for
   this epic and no other, with the partial note where shared; and one `informed_by` link to the ARCH at the
   ARCH's version. Every link is in flow style with the keys in order.
5. Every requirement refined is eligible. No eligible FR is in two new epics, and none is left out of all of
   them. No covered FR appears.
6. `priority` is the highest priority among the FRs it refines (an NFR-only epic: its NFRs' highest), and
   the epics are numbered Must, then Should, then Could.
7. The `done_when` fence has exactly one top-level key, and at least one DW item with a quoted criterion and
   evidence method.
8. Every heading from the template is present, section 7 holds only the GENERATED comment, and section 8
   holds the unconfirmed-grouping marker when the grouping wasn't confirmed.
9. If the PRD or the ARCH is a draft, section 1 starts with the proposal line.
10. No leftovers remain.
11. No existing file changed: every earlier epic, the PRD, the ARCH, the ADRs and the policy documents are as
    they were.
