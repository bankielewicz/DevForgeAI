# Tracing impact

Read this at Trace impact, and again at Route and verify when you write the refresh plan.

The output of this phase is a table of things that are actually affected, each with an identity, a path from the changed source, an expected impact, an owner action, and an honest statement of where the analysis stops. The table is only worth having if that last column is true.

## Resolve a reference before you trust it

An `upstream` entry in a `devforge.artifact/v1` envelope carries an `artifact_id`, a `revision`, a `store`, a `path`, a `sha256`, and the stable section IDs the artifact actually relied on. Resolving it means finding those bytes and checking they hash to that digest.

Four things you can find, and they mean different things:

- **The bytes resolve and match the digest.** The reference is sound. Whatever it says about the dependency is current.
- **The bytes resolve and do not match.** The upstream moved after the dependent was written. The dependent's reasoning was done against bytes you no longer have at that path, and the dependent is a candidate for review regardless of what this change does.
- **The path resolves to nothing.** Look for a preserved copy - a project archive convention, a sibling revision file, a frozen snapshot named in an evidence entry. If you find one that hashes correctly, the reference is repairable and you say where the preserved bytes are. If you do not, the edge is unresolved.
- **There is no envelope at all.** Plenty of real project files are just files. Record it as raw-file evidence with its native locator and digest; do not invent an artifact ID for it.

An unresolved edge is a coverage limit and it belongs in the change-request. It is not an absent dependency, and writing it as one turns a hole in the analysis into a claim that nothing is there.

How to write a repaired locator, and where the preserved bytes go, is in [Recording the change-request honestly](recording-rules.md).

Repairing a broken locator to preserved bytes is mechanical and changes nothing about what has been adopted. Adopting a newer revision is a decision and needs authority. Keep those two acts separate in the record: a reader who cannot see both cannot tell an authorized update from an invented one.

## What belongs in the graph

Documents are the easy part. These are the ones a change assessment usually misses:

| Kind of dependent | Why it is affected | What identifies it |
| --- | --- | --- |
| Stories and acceptance criteria written against the changed rule | The criteria may now describe behaviour the project no longer wants | Artifact ID, revision, the section citing the change |
| Generated project expert sources | An expert carries the decisions and versions it was written against | Source package path and its file manifest |
| Installed and exported copies of those experts and skills | A copy is generated; refreshing the source does not refresh the copy | Installation path, installation mode, and the source it was generated from |
| Evaluation plans and reports bound to a superseded candidate | A report is evidence about the exact bytes it examined | Report identity, and the candidate manifest it bound |
| Recorded expert bindings | A binding records which policy and document digests were referenced | The project's expert directory provenance record |
| Open runs, worktrees and branches | In-flight work proceeding under the old rule | Assignment record, worktree path, base commit |
| Prior change-requests touching the same artifacts | A declined or deferred proposal may now be live again, or this one may duplicate it | Artifact ID and revision |

No command reports any of this. [What the CLI can and cannot tell you](cli-boundaries.md) says which freshness facts the DevForge CLI actually establishes - one bound expert against its own recorded binding - and which of the rows above have no implemented check at all.

A refresh is not complete when only a source `SKILL.md` changed. The installed copies generated from it, and every evaluation bound to the previous bytes, are part of the same refresh, and each gets its own row with its own owner.

## Which skill owns which artifact

The roster's provenance edges say where a revision of each artifact starts. The change-request routes to the owning skill; it does not perform the revision.

| Affected artifact | Owning skill for the first revision |
| --- | --- |
| Idea ledger, early intent | `devforge-brainstorm` |
| Product brief, adopted requirements | `devforge-define-product` |
| Design specification, interaction contracts | `devforge-design` |
| Experiment plan or prototype report | `devforge-prototype` |
| Architecture contract, rules, pinned versions | `devforge-architect` |
| Epics, stories, acceptance criteria | `devforge-plan` |
| Project expert specification and package | `devforge-project-expert-creator` |
| Expert evaluation plan or report | `devforge-evaluate-expert` |
| Implementation of an accepted, unchanged story | `devforge-develop` |
| Review of a candidate | `devforge-review` |
| Release record | `devforge-release` |

**Check what is installed before naming one.** That table is the specified roster, and most of it is specified rather than implemented - reading a name off it is not evidence a user can invoke it. Look at what the session actually has. At the time this package was authored, the Claude provider source carried draft `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator` and `devforge-review` and nothing else, and a provider source directory by itself is not a discovered installation.

Where the owner is absent, say so as a capability gap: name the capability, say it is not installed, and give a next task the user can actually act on - a plain-language task with resolvable absolute paths. A gap reported honestly is a useful result; a plausible-looking slash command for a skill nobody has confirmed is not.

## Semantic impact versus a reference edge

The edges tell you where to look. They do not tell you what is affected.

An artifact can cite the changed section and be untouched by this particular change - the rule it relied on was a different clause, or the change is additive in a direction it does not care about. Another can be broken without citing anything, because it encoded an assumption that was true and is now not. Version-pinned examples inside an expert are the classic case: nothing references them and a dependency upgrade invalidates every one.

So read what the change actually means for each dependent, and record the confidence per row. Three honest values, and they are not the same:

- **Affected** - you read the dependent and the change reaches it. Say how.
- **Not affected** - you read the dependent and the change does not reach it. Say why, briefly; a bare "no" is not reviewable.
- **Uncertain** - you could not read it, could not resolve it, or could not tell. Say which, and what would settle it.

Do not collapse uncertain into either neighbour. A dependent nobody could read is not a dependent nobody needs to check.

## External triggers

For a new release, a changed API or a vendor announcement, verify the specific claim before building a graph on it. Record the source URL, the retrieval date, the applicable package version, and exactly what you verified. Where you could not verify, the claim stays a missing input rather than becoming confident prose.

Discovery of a newer version is not approval to upgrade. The proposal says what upgrading would invalidate and what it would cost; the decision belongs to the user, and the project's pinned dependency stays pinned until they make it.

## Recording the limit

Every impact table gets a stated boundary. At minimum: which stores and directories you actually searched, which you could not reach and why, whether installed copies and active runs were inspected or only inferred, and which edges did not resolve.

"No further dependents were found in the searched inventory" is an honest result. "Nothing else is affected" is a claim a bounded search cannot support. The difference matters to whoever reads this next, because one of them invites a second look and the other closes the question.
