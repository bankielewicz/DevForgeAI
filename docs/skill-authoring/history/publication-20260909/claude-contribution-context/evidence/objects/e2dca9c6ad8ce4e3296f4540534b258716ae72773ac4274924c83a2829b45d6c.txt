# Authored evaluation inputs

These files are authoring source. They are excluded from any runtime export or installed copy of
this package, per the skill authoring contract: an installed skill ships SKILL.md, references,
assets and scripts only.

## Layout

| Path | Contents | Reaches an evaluated worker? |
| --- | --- | --- |
| `evals.json` | Case index: raw prompt, declared mode, scenario role/provider, worker-visible file list | No |
| `fixtures/` | Synthetic contribution records | Only the files listed for that case |
| `expectations/` | Required observations and material failures per case | No |
| `withheld/` | Records deliberately unreachable inside a case's permitted boundary | No |
| `triggers/triggers.json` | Authored activation queries with a fixed train/validation split | No |
| `coverage-matrix.md` | Provider/role/variant/mode/arm accounting | No |

An evaluated worker receives its case's raw prompt and the files listed in that case's `files`
array. Nothing else in this directory is supplied to it. A grader may receive the relevant
`expectations/` file together with the task facts, applicable rules and the actual output.

## Path resolution

Every path in a case's `files` array is relative to **this directory** and stays within it, per
the DevForgeAI skill authoring contract revision 2. The generic skill-creator schema note about
skill-root-relative paths does not apply here; the project contract governs.

## Fixture design

Records are synthetic, derived from real failure shapes rather than copied from live control
files. Session IDs are in a 9xx range and worktree paths sit under a fictional
`/srv/devforgeai-fixture/` root, so no fixture can be confused with a real assignment or used as
a writable target.

Where a case pins a digest, that digest is genuine: the bytes were written first and hashed, and
the record citing the digest was written afterwards. Two digests are deliberately wrong in a
specific, documented way, and both are labelled in `expectations/`:

- CCX-06 pins the digest of a record kept in `withheld/` and never shipped into the worker-visible
  tree, so the record is genuinely unresolvable while its expected identity is real.
- CCX-08 ships a historical receipt carrying a 12-character truncation of a real digest. It is a
  preserved historical omission, not an error to repair.

## Execution status

NOT_RUN. SESSION-004 allocates exactly 0 model calls, concurrency 0 and retries 0. No case, arm
or trigger query has been executed, and no native activation, loading or behavior has been
observed for this package.
