# ARCH and ADR output rules

## Contents

- When to use this
- ARCH frontmatter
- Links
- Item blocks
- ARCH collections
- ARCH sections
- Amending an ARCH
- Recording a review
- ADRs
- Change Log and resolution line
- Leftovers
- Self-check list

## When to use this

Read this before writing an ARCH or an ADR (step 9) or recording a review (step 4), and check every file
written against the **Self-check list** when `devforgeai check --json` is unavailable (not on PATH, or output
that isn't JSON). These rules restate the ARCH and ADR schemas. A file that breaks any of them is invalid.

## ARCH frontmatter

The YAML between the first two whole `---` lines. Allowed keys, and **no others**:

| Key | Rule |
|---|---|
| `id` | `ARCH-NNN`: three digits, for example `ARCH-001`, matching the file name |
| `type` | exactly `arch` |
| `title` | quoted string, for example `"Studio booking platform architecture"` |
| `status` | `draft` for a new ARCH; `in-review` after amending an approved one. **Never set to `approved`**. A review record leaves it as it was (Recording a review) |
| `version` | integer, at least 1 |
| `created`, `updated` | `YYYY-MM-DD` |
| `owner` | quoted string: the user's name, else the PRD's owner |
| `authors` | list: the user's name (if known) and `claude-code`. Never invent a name |
| `generated_by` | map with only `tool` (`"claude-code"`), `model` (your model ID) and `session` (`"${CLAUDE_SESSION_ID}"`, substituted), each quoted and non-empty |
| `reviewed_by` | `[]` |
| `approved_by`, `approved_on` | `""` and `null` for a new or amended ARCH. A review record leaves them as they were |
| `upstream` | list of link records (Links) |
| `supersedes` | `[]` |
| `superseded_by` | `null` |
| `blocked_by` | `[]` |
| `system` | quoted string naming the system or product the ARCH covers |
| `outcome` | `reuse`, `amend`, `create` or `null`. **`null` unless the user confirmed the outcome** |
| `inspection_scope` | list of quoted strings, exactly as the user named them; `[]` if none |

## Links

A link record has only `id`, optional `item`, `relation`, `version`, `hash` and optional `note`. Write
every link in **flow style, keys in this order**:

```yaml
- {id: PRD-001, item: FR-001, relation: informed_by, version: 3, hash: null}
```

- **`hash` is always `null`.** Only the checker writes hashes.
- A link added in this run uses the linked document's current `version`: the PRD version examined, the
  policy version. Links on existing items keep their versions and are never updated (Amending an ARCH): an
  older version is how a suspect link shows up for review.
- A link lives in exactly one place: on the item that owns it, or in the frontmatter when the whole ARCH
  owns it. Never repeat a link in prose; prose uses the qualified reference, such as `PRD-001#FR-001`.

| Source | Where | Relation |
|---|---|---|
| the input PRD (whole document) | ARCH frontmatter `upstream` | `informed_by` |
| each requirement a question affects | that DEC's `upstream`, one link per requirement | `informed_by` |
| each NFR (quality driver or constraint) a component serves | that CMP's `upstream` | `informed_by` |
| an applied `architecture.mandated_platforms` setting | the `upstream` of the CMP that provides the capability; if no CMP does, the DEC it resolves. **Never also in the frontmatter** | `constrains` |
| an applied `interview.max_calls` or `quality.required_categories` setting | ARCH frontmatter `upstream`, with `item: SET-NN` | `informed_by` |

Never link a default, a local value, a deprecated or not-applicable setting, an ignored policy document,
or an ADR that isn't accepted. `resolved_by` entries are IDs, not links.

## Item blocks

- An item block is a fence whose info string is exactly `yaml items`, with **exactly one top-level key**:
  `components`, `decisions` or `evidence`.
- Inside a fence, never `<!-- -->`. Delete the template's inline `# …` hints (such as
  `# open | resolved`); write no trailing comment on an item line.
- **Quote every free-text value** with `"…"`. Enum values (`status`, `state`, `kind`, `classification`),
  booleans, `null` and IDs stay unquoted.
- Lists of prose use block sequences (`- "…"`), never flow lists.
- Items are never deleted or renumbered. Retire one with `status: deprecated` (and `superseded_by`).
- A collection with no items is written as `evidence: []` (or the matching key), never omitted.

## ARCH collections

Write the keys in the order shown. Every item may also carry `superseded_by` (an item ID or `null`)
before `upstream`.

**`components`**: IDs `CMP-01`, `CMP-02`, …

| Field | Required | Rule |
|---|---|---|
| `id`, `status` | yes | `CMP-NN`; `active` or `deprecated` |
| `name`, `responsibility` | yes | quoted strings |
| `owns_data` | no | block list of quoted strings |
| `interacts_with` | no | block list of quoted strings: `CMP-NN` IDs or external systems |
| `deployment` | no | quoted string: the deployment unit |
| `upstream` | yes (skill rule) | the NFRs it serves; the mandated-platform setting it obeys |

**`decisions`**: IDs `DEC-01`, `DEC-02`, …

| Field | Required | Rule |
|---|---|---|
| `id`, `status` | yes | `DEC-NN`; `active` or `deprecated` |
| `question` | yes | quoted string, one question |
| `blocking` | yes | `true` or `false` |
| `state` | yes | `open` or `resolved` |
| `resolved_by` | yes | flow list of IDs: `[]` when `open`; one or more `ADR-NNN` or `POL-NNN#SET-NN` when `resolved`, for example `[POL-001#SET-01]` |
| `notes` | yes (skill rule) | quoted string or `null`: options considered, conflicts, why it is still open |
| `upstream` | yes | at least one link: every affected requirement, `informed_by`, at the PRD version examined |

**`evidence`**: IDs `EVD-01`, `EVD-02`, …; the rules for each field are in `inspection.md`.

| Field | Required | Rule |
|---|---|---|
| `id`, `status` | yes | `EVD-NN`; `active` or `deprecated` |
| `source` | yes | quoted string, with the version and status examined where applicable |
| `kind` | yes | `code`, `document`, `adr`, `policy` or `prd` |
| `finding` | yes | quoted string |
| `classification` | yes | `observed`, `policy`, `decided` or `context` |

Example decision, open, and one resolved by a mandate:

```yaml
decisions:
  - id: DEC-01
    status: active
    question: "Which identity provider signs members in?"
    blocking: true
    state: resolved
    resolved_by: [POL-001#SET-01]
    notes: "Mandated platform for identity and authentication"
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
  - id: DEC-02
    status: active
    question: "How are member sessions revoked?"
    blocking: true
    state: open
    resolved_by: []
    notes: "The mandate names the platform, not how sessions are revoked"
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
```

## ARCH sections

Keep every heading of `${CLAUDE_SKILL_DIR}/assets/arch.md`, in order, with the `ARCH-NNN — <system> architecture` title line.

| Section | Content |
|---|---|
| 1. Context and scope | What the system is for, what's inside and outside it, and the PRD ID, version and status examined. If the PRD is a draft, say the ARCH is a proposal |
| 2. Quality drivers | Prose naming the NFRs and constraints that shape the design, as qualified references |
| 3. Components | A Mermaid `flowchart` with one node per active CMP, then the `components` block |
| 4. Architectural questions | The `decisions` block |
| 5. Evidence inspected | The `evidence` block |
| 6. Deployment | Prose: deployment units, environments, what runs where. Unknowns are markers in §8 |
| 7. Requirement changes proposed to the PRD owner | One bullet per proposal, or `- None.` |
| 8. Open questions | One `[NEEDS CLARIFICATION: <question>]` bullet per unknown, or `- None.` |

A §7 bullet names the requirement, the finding and the proposed change, and addresses the PRD owner, for example:
`- PRD-001#NFR-002 conflicts with the mandate POL-001#SET-01 (Org A Identity Platform). Proposed change for Priya Nair (PRD owner): replace "sign in with Google accounts" with sign-in through the mandated platform, or obtain a policy exception.`

## Amending an ARCH

- Bump `version` by one and set `updated` to today. Add a Change Log row.
- Leave every existing CMP, DEC and EVD **byte-identical**, except a DEC's `state` and `resolved_by` when it
  moves between open and resolved. Log each such transition, with its reason, in the new Change Log row.
- When the user explicitly approves superseding an ADR that a DEC cites, and decides that DEC in this run, the
  DEC stays resolved and `resolved_by` changes from `[ADR-old]` to `[ADR-new]` (replace, don't append), logged
  in one Change Log row, for example `DEC-01 resolved_by ADR-001 → ADR-002: ADR-001 superseded by ADR-002`.
- New items continue the numbering. Update the frontmatter PRD link to the version examined, or add it if
  this PRD isn't linked yet. New items' links use current versions; links on existing items keep their versions and are never updated.
- `outcome` records the outcome for the PRD version examined: set it only when the user confirmed it in this
  run, and otherwise set it to `null`.
- If `status` was `approved`, set it to `in-review`, `approved_by: ""` and `approved_on: null`.
- A confirmed reuse is not an amendment: follow Recording a review instead.

## Recording a review

When the user confirms **reuse** and the ARCH's frontmatter PRD link (the link to the PRD with no `item`) has
a `version` older than the PRD's `version`, record the review. Make exactly these three changes:

1. That frontmatter link's `version` becomes the PRD's current `version`. Nothing else in the link changes.
2. `outcome` becomes `reuse`.
3. Add one Change Log row: the ARCH's current `version` (unchanged), today's date, author `claude-code`, Change
   `Reviewed against PRD-NNN vN: reuse confirmed, no architectural change.` followed by the policy
   resolution line, and Items affected `frontmatter`. For example:
   `| 2 | 2026-09-24 | claude-code | Reviewed against PRD-001 v3: reuse confirmed, no architectural change. Policy resolution: … | frontmatter |`

Everything else stays **byte-identical**: `version`, `updated`, `status`, `approved_by`, `approved_on`, every
section, and every CMP, DEC and EVD, including their links, which keep their older versions and still show as
suspect for review. A review is a relink, not an amendment: no version bump, no change to `updated`, and an
approved ARCH stays approved.

- If the frontmatter PRD link already equals the PRD's `version`, confirming reuse writes nothing.
- With no one to confirm reuse, nothing is confirmed and nothing is written.

## ADRs

Write each ADR to `docs/specs/adr/ADR-NNN.md`, the next free number (highest existing `ADR-NNN` plus one),
from `${CLAUDE_SKILL_DIR}/assets/adr.md`.

| Key | Rule |
|---|---|
| `id`, `type` | `ADR-NNN`, matching the file name; `adr` |
| `title` | quoted: the decision stated as a result, for example `"Revoke sessions with short-lived tokens and a revocation list"` |
| `status` | `accepted` only for the user's explicit decision; `proposed` for a deferred one. Never anything else |
| `version` | `1` |
| `created`, `updated` | today |
| `owner`, `authors`, `generated_by`, `reviewed_by` | as for the ARCH |
| `approved_by`, `approved_on` | accepted: the deciding user's name and today. Proposed: `""` and `null` |
| `upstream` | the requirements its DEC cites, `informed_by`, at the PRD version examined |
| `supersedes` | `[ADR-old]` when this ADR supersedes one (a supersession the user explicitly approved), otherwise `[]` |
| `superseded_by`, `blocked_by` | `null`, `[]` |
| `consulted`, `informed` | lists of names, `[]` when none |

- Say in the context section which question it answers, as a qualified reference: `Answers ARCH-001#DEC-02.`
- Fill every section: the options you presented with their trade-offs, the chosen option (or "not decided"
  for a proposed ADR), consequences, and how the decision will be confirmed.
- The Status history table has one row: today, the status, and who decided.
- **Never modify an existing ADR**, except to record a supersession the user explicitly approved: then
  set the old ADR's `status: superseded` and `superseded_by` (the accepted ADR written in this run), and add
  one Status history row. Everything else in the old ADR stays byte-identical, including `version` and `updated`.

## Change Log and resolution line

The ARCH Change Log table has columns Version, Date, Author, Change, Items affected. Each row the skill adds
has the new version (a review record's row keeps the current one), today's date and author `claude-code`. Its
**Change** cell summarizes the change (for example `Initial draft for PRD-001 v2` or
`DEC-01 resolved → open: ADR-002 superseded by ADR-003`) and **ends with the policy resolution line**, as one line:

`Policy resolution: <entry>; <entry>; …`

The entry forms and their order are in `policy.md` (Resolution line). A `|` never appears inside the cell.

## Leftovers

None of these may remain in a written file:

- `ARCH-000`, `ADR-000`, `PRD-000`, `YYYY-MM-DD`, or any `<…>` placeholder such as `<system>`, `<component>`,
  `<question>` or `<option A>`;
- any `<!-- -->` author comment;
- the template's example items and links (`"<component>"`, `PRD-000`);
- an empty `title`, `owner`, `system` or `generated_by` value, or an empty Change Log date or author cell.

## Self-check list

Read each written file back, then confirm each line.

**ARCH** (new or amended; a review record uses its own list below)

1. The path is `docs/specs/arch/ARCH-NNN.md`, and `NNN` matches the frontmatter `id`.
2. The frontmatter has only the allowed keys, with the types above. `status` is not `approved`.
3. `generated_by` has non-empty `tool`, `model` and `session`, and no `${` text remains anywhere.
   `reviewed_by` is `[]`. Every `hash` is `null`.
4. `outcome` is `null` unless the user confirmed it.
5. Every `yaml items` fence has exactly one top-level key: `components`, `decisions` or `evidence`.
6. Every item has its required fields, only allowed fields, and an ID in the right pattern, with no
   duplicates and no renumbering.
7. Every DEC: `state: open` has `resolved_by: []`; `state: resolved` has at least one entry, each an ADR
   that is accepted and not superseded, or an effective policy setting. `upstream` has at least one link.
8. Every `[NEEDS ADR]` marker in the PRD has a DEC citing every requirement it names.
9. Every EVD `classification` follows `inspection.md`, and the input PRD has an EVD with `kind: prd`.
10. Every link record follows Links: flow style, key order, placement and relation. Links added in this run use
    current versions; links on existing items keep their versions and must not be updated. An older version
    is how a suspect link shows up.
11. Every free-text value is quoted. Every heading from the template is present.
12. The newest Change Log row ends with one `Policy resolution:` line.
13. No leftovers remain, and no item line carries a trailing `#` comment.

**Each new ADR**

1. The path is `docs/specs/adr/ADR-NNN.md`, `NNN` matches `id`, and the number was free.
2. The frontmatter has only the keys of the ADR template, `status` is `accepted` or `proposed`, and
   `approved_by` is non-empty exactly when it is `accepted`.
3. Provenance as for the ARCH; every `hash` is `null`.
4. It names the one DEC it answers, and only that DEC lists it in `resolved_by`.
5. No leftovers remain.
6. `supersedes` is `[ADR-old]` when this run supersedes an ADR, otherwise `[]`.

**Each existing ADR marked superseded**

1. The user explicitly approved the supersession in this run.
2. Only these changed: `status: superseded`, `superseded_by` (an accepted ADR written in this run, whose
   `supersedes` names this ADR) and one new Status history row. Everything else is byte-identical.

**A review record**

1. The user confirmed reuse, and before this run the frontmatter PRD link was older than the PRD's `version`.
2. Only these changed: that link's `version` (now the PRD's), `outcome: reuse`, and one new Change Log row
   with the unchanged ARCH version, starting `Reviewed against PRD-NNN vN` and ending with one
   `Policy resolution:` line.
3. `version`, `updated`, `status`, `approved_by` and `approved_on` are as they were, and every item and its
   links are byte-identical.
