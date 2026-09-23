# Policy resolution (configuration contract v1)

## Contents

- When to use this
- Layers and precedence
- R1. Load and validate
- R2. Resolve unconditional settings
- R3. Establish the operating context
- R4. Evaluate conditional settings
- R5. Record
- Local preferences
- Stop message
- Resolution line

## When to use this

Read this at the start of every run, before selecting a BRN. Follow R1 to R5 in order: R1 and R2 run
first, so the interview budget and any policy error are known before the first question and before
anything is written. R3 and R4 run once the operating context is established. R5 runs when writing.

## Layers and precedence

From general to specific:

1. **Framework defaults**: `defaults.md`.
2. **Organization policy**: an approved `docs/specs/policy/POL-NNN.md` with `scope: organization`.
3. **Project policy**: an approved `docs/specs/policy/POL-NNN.md` with `scope: project`.
4. **Local preference**: `.claude/devforgeai.local.md` (Local preferences, below). Interaction defaults only.

- **Which value wins:** the most specific layer that is *allowed* to set it.
- **Who may override:** the `overridable_by` list of the setting being overridden. A lower layer that sets a
  value the higher layer's setting doesn't allow it to override is an error (stop), except for local
  preferences, which are ignored and reported instead.
- The quality floor (`interview.md`) is a framework requirement: policy only adds to it.

## R1. Load and validate

1. Glob `docs/specs/policy/POL-*.md`. None, or no directory: every key takes its default; go to R2.
2. Read each file's frontmatter. If `status` is not `approved`, skip the file and record
   `ignored <path> (status <status>)` (SV-06). It never applies, whatever its settings say.
3. For each approved file, read the frontmatter and every `yaml items` fence with the key `settings`.
   Check the **schema rules** and then the **semantic rules** below. The first violation stops the run
   (Stop message). Never repair a policy file, never guess what it meant, and never fall back silently to defaults.

**Schema rules** (restating `policy.schema.json`):

- Frontmatter has exactly these keys, and no others: `id` (`POL-NNN`), `type` (`policy`), `title`, `status`,
  `version` (integer ≥ 1), `created`, `updated` (`YYYY-MM-DD`), `owner`, `authors`, `upstream`, `supersedes`,
  `superseded_by`, `blocked_by`, `scope`, `source`, and optionally `generated_by`, `reviewed_by`,
  `approved_by`, `approved_on`.
- `scope` is `organization` or `project`. With `organization`, `source` is a map with exactly `repository`
  and `ref`. With `project`, `source` is `null`.
- Each setting has `id` (`SET-NN`), `status` (`active` or `deprecated`), `key`, `class`, `value` and
  `overridable_by`, and may have `superseded_by`, `upstream`, `applies_when` and `rationale`. No other field.
- `overridable_by` is a list of distinct values from `project` and `local`.
- `key` is one of the three v1 keys, with these rules:

| Key | `class` | `value` | `applies_when` | `overridable_by` may contain |
|---|---|---|---|---|
| `quality.required_categories` | `organizational_policy` | non-empty list of distinct NFR categories (`performance`, `security`, `privacy`, `accessibility`, `reliability`, `compliance`, `observability`, `usability`, `maintainability`, `constraint`, `other`) | **required**: `{operating_context: [...]}`, a non-empty list of `local`, `internal`, `pilot`, `production` | `project` only |
| `architecture.mandated_platforms` | `organizational_policy` | map with exactly `capability`, `platform`, `source`, all strings | **forbidden** | `project` only |
| `interview.max_calls` | `interaction_default` | integer from 1 to 20 | **forbidden** | `project`, `local` |

An unknown key, a class that doesn't match the key, an out-of-range or wrongly typed value, a missing or
empty `applies_when` where required, an `applies_when` where forbidden, and `local` on an organizational-policy
key are all schema violations.

**Semantic rules** (ADR-003 A4):

| Rule | Check | On violation |
|---|---|---|
| SV-01 | Setting IDs are unique within a document | stop |
| SV-02 | At most one approved document per scope (`organization`, `project`) | stop; name both files |
| SV-03 | `interview.max_calls` appears at most once per document | stop |
| SV-04 | At most one active `architecture.mandated_platforms` setting per capability per document; across layers, see R2 | stop |
| SV-05 | Only `status: active` settings take part. Skip `deprecated` settings entirely: no link, no constraint, no value | skip |
| SV-06 | Only approved documents take part (step 2) | skip and report |
| SV-07 | Local preference entries follow the local format (Local preferences) | ignore and report |

Capabilities are the same when their `capability` strings match ignoring case and surrounding spaces.

## R2. Resolve unconditional settings

Take only active settings from approved documents.

**`interview.max_calls`**

1. Start from the default (8, `overridable_by: [project, local]`).
2. If the organization policy sets it, that setting replaces the default.
3. If the project policy sets it: when the current effective setting's `overridable_by` includes `project`,
   it replaces it; otherwise **stop** (override not allowed), naming both settings.
4. Apply a valid local entry only if the effective setting's `overridable_by` includes `local`; otherwise
   ignore and report it (Local preferences).
5. The result is the interview budget: at most that many AskUserQuestion calls.

**`architecture.mandated_platforms`**

1. Collect every active setting from the organization and project policies.
2. For each capability mandated by both: if the organization setting's `overridable_by` includes `project`,
   the project setting replaces it; otherwise **stop** with SV-04, naming both settings.
3. Each remaining setting is a mandate that applies to this PRD (BEH-16).

## R3. Establish the operating context

Take the operating context from the request, then the BRN, then the first framing question (`interview.md`).
It counts as established only when the user stated or confirmed it. If none of these gives it (for example,
the request says to proceed without questions), it stays unknown and `operating_context` stays `null`.

## R4. Evaluate conditional settings

1. The evaluation context is the established operating context, or `production` when it is unknown.
2. For each active `quality.required_categories` setting in the organization and project policies: if its
   `applies_when.operating_context` includes the evaluation context, add its categories to the required set;
   otherwise record it as not applicable. Settings from both layers add up; none removes a category.
3. Required categories = the floor for the evaluation context (`interview.md`) plus every added category.
   Ask each of them in the quality round, and mark each unanswered one (`output-rules.md`, Markers).

## R5. Record

1. For each applied policy setting, add an upstream link carrying the policy's current `version`:
   - `architecture.mandated_platforms`: `constrains`, placed as `output-rules.md` (Links) says;
   - every other key: `informed_by`, in the frontmatter, for example
     `{id: POL-001, item: SET-02, relation: informed_by, version: 3, hash: null}`.
2. Never link a default, a local value, a deprecated setting, a not-applicable setting or an ignored document.
3. Write the resolution line (below) into the Change Log row this run adds.

## Local preferences

`.claude/devforgeai.local.md`, if it exists. Its entire content is YAML frontmatter:

```yaml
---
devforgeai_local: 1
interview.max_calls: 5
---
```

- `devforgeai_local` must be `1`. If it is missing or different, or the YAML doesn't parse, ignore the whole
  file and record `ignored .claude/devforgeai.local.md (<reason>)`.
- Each other entry is used only if the key is an interaction default (v1: only `interview.max_calls`), its
  value passes the schema rule for that key, and the effective setting's `overridable_by` includes `local`.
- Otherwise ignore the entry and record `ignored .claude/devforgeai.local.md#<key> (<reason>)`, where the
  reason is one of `unknown key`, `organizational-policy key`, `out of range`, `wrong type` or
  `not overridable by local`.
- A local file never stops the run.

## Stop message

On a schema, SV-01 to SV-04 or override violation, write nothing, create no directory, and reply with:

```
Policy error: <path> <SET-NN or frontmatter key> (<setting key>): <rule> — <what is wrong>.
No PRD was written. Fix the policy document and run /devforgeai:prd again.
```

- `<rule>` is `schema` or the rule ID (`SV-01` … `SV-04`), or `override not allowed`.
- For a cross-layer violation, name both settings as `POL-NNN#SET-NN`, with their files.
- Example: `Policy error: docs/specs/policy/POL-001.md SET-01 (interview.max_calls): schema — value 50 is outside 1–20.`

## Resolution line

One line, in the Change Log row's Change cell, entries separated by `; `, in this order:

1. `interview.max_calls=<n> (<source>)`, where `<source>` is `POL-NNN#SET-NN`, `default` or `local`.
2. Mandated platforms: one `architecture.mandated_platforms=<platform> for <capability> (POL-NNN#SET-NN)`
   per applied setting, or `architecture.mandated_platforms=none (default)`.
3. Required categories: one `quality.required_categories=+<cat>,+<cat> (POL-NNN#SET-NN)` per applied
   setting, or `quality.required_categories=floor only (default)` when none applied.
4. One `POL-NNN#SET-NN not applicable (<evaluation context>)` per conditional setting that didn't apply.
5. `operating context unknown, resolved as production`, only when R4 used the fail-safe.
6. One `ignored <file or local entry> (<reason>)` per skipped document or local entry.

Example: `Policy resolution: interview.max_calls=5 (local); architecture.mandated_platforms=none (default); quality.required_categories=+compliance (POL-001#SET-02); operating context unknown, resolved as production`.
