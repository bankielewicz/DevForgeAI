# Saving and resuming discovery briefs

Read this reference when saving discovery output or resuming a saved brief. Conversation-only discovery creates no files. Saved output may be partial with `NEEDS_INPUT`, complete enough for `READY_FOR_PRD`, or an explicitly requested reuse handoff with `REUSE_EXISTING`; a reuse handoff references the existing artifact without rewriting it.

## Destination and revision

Reuse the selected root, existing brief ID on resume, authorized persistence scope and project conventions. Resolve any ambiguity before dependent filesystem actions. Unless the user or project conventions select another destination, use:

`docs/plan/discovery/<brief-id>/brainstorm-brief-rNNN.md`

`brief-id` is a local artifact identifier matching `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`. For a new brief derive a short safe topic identifier plus UTC timestamp, shortening the topic to fit 64 characters; check for collisions. This is not a project UUID or binding identity. A first saved revision is integer 1; every saved successor increments the selected previous revision. Format the filename revision with at least three digits (`r001`, `r002`, ..., `r1000`). Keep frontmatter revision numeric.

Inspect selected lineage and occupied paths before choosing a successor. If a competing successor or destination collision exists, reconcile the actual lineage or choose another safe unused destination within the authorized convention; do not skip a revision silently, overwrite unknown work or change scope to evade a denial. If the selected previous revision or its objective was superseded, identify the current selected work before resuming it.

## Artifact contract

Fill the [template](../assets/discovery-brief-template.md). Replace its drafting placeholders with observed information, attributed proposals or explicit unknowns; do not invent answers. Emit exactly these six frontmatter fields:

| Field | Value |
| --- | --- |
| `format_version` | `brainstorm-brief-v1` |
| `brief_id` | The safe local identifier |
| `revision` | Integer >=1 |
| `updated_at_utc` | Actual RFC3339 UTC timestamp, ending in `Z` |
| `disposition` | `READY_FOR_PRD`, `NEEDS_INPUT` or `REUSE_EXISTING`, selected by SKILL.md |
| `supersedes` | Prior brief's project-relative path, or YAML null for the first revision |

Keep substantive content in all nine template sections. Include the attributed request and source inventory; problem/users/outcomes; MVP/exclusions/later ideas; meaningful options and decision origin; constraints and architecture questions with reasons for inapplicability; evidence and experimental states; identified decisions/questions with stage impact; disposition/reason/next consumer/reused paths/manual next request; and follow-up/change notes. Empty applicable lists are stated explicitly, including “none selected” for experiments when applicable. A partial brief names gaps rather than dropping sections. Do not duplicate a PRD, epic, story or policy pack inside it.

## Preserve, write and read back

1. Prepare intended content from the currently selected inputs. Before every write, recheck their identities and the destination state. Resolve the literal output path within the selected output scope; inspect existing ancestors and the leaf without following symlinks/junctions/reparse escapes. Reject any traversal or link that escapes the selected scope. If the available tools cannot establish safe resolution, report the missing capability and do not perform the dependent write.
2. Create only required directories under the authorized scope. Use exclusive creation for the new brief: opening an existing path for truncating write is not acceptable. Use terminal filesystem operations with literal arguments and an exclusive create mode; never interpolate user content as executable shell text. No packaged helper, network service or GUI is required. Recheck the path after directory creation and immediately before creating the file.
3. Preserve all older briefs and source documents. Read the new file back completely against the intended bytes, metadata and substantive section contract. Recheck source identities to detect drift during writing. A stale or incomplete artifact cannot be announced as the current successfully delivered brief merely because a write command exited successfully.
4. Report the actual path and saved revision only after successful readback. If creation, writing, source recheck or readback fails, report the actual destination/error and observed partial artifact state. Separate “file absent”, “partial file present”, “bytes differ” and “state unknown” when applicable. State what remains incomplete; do not claim delivery or silently clean up unrelated files.

These are ordinary filesystem preservation steps, not an atomic framework transaction or protected acceptance gate. If interrupted, inspect the actual file and its lineage before any retry. A prior successful-looking message is not evidence of a completed write. Preserve partial attempts; reconcile their state and use a safe new destination only within the selected scope. Permissions still apply; never silently choose an outside destination to avoid them.

## Resume with current evidence

Read the selected prior brief and relevant governing sources. Compare the prior inventory's identities and decision origins with current inputs, using [evidence and decisions](evidence-and-decisions.md). Retain unaffected supported observations; revise only affected claims and record changed or unavailable inputs and their implications. A clarification updates the selected objective's constraints; an explicit objective replacement names what it supersedes.

If saving is authorized, create a new revision, retaining the brief ID and linking the prior project-relative path in `supersedes`. Record change notes and current source identities. Never edit the old revision to make its evidence appear current. If saving is not selected, return the revised discussion and disposition without a successor file or invented path.
