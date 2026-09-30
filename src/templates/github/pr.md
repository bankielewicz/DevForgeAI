<!-- guide: Pull request body, bound to the PR's actual head: the remote branch's SHA, equal to the local
     HEAD with no tracked changes, or the PR isn't posted. The title follows the repository's commit
     convention (for example "feat: …", "docs: …"). Every statement is a fact about that head: what
     changed, what was run at it and what it printed, what wasn't verified. List only checks run in
     this session or recorded elsewhere with a cited location. Nothing aspirational. Delete every
     guide comment before posting. -->

## Summary

<!-- guide: What changed and why, in two to five lines, naming the specs, decisions or issues behind it. -->

{{What changed and why.}}

## Changes

<!-- guide: Group by area, from the diff between the base and the head below. Name the paths. Say what
     didn't change when a reader might expect it to. -->

- **{{Area}}:** {{what changed}} (`{{path}}`)

## Implements and references

<!-- guide: The spec, VER and issue IDs this implements or records. Use "Fixes #N" only when merging this
     PR resolves the issue; otherwise "Refs #N". -->

- {{SPEC-NNN, VER-NN, …}}
- Refs #{{N}}

## Checks run

<!-- guide: Each check with its command, the SHA it ran at, and the result line it printed. Only checks
     run at the head SHA belong here; a check run at another SHA, or with tracked changes present, goes
     under "Not verified". Say where a result is recorded when it wasn't run in this session. A check
     that failed stays listed as failed. -->

- `{{command}}` at `{{head SHA}}`: {{result line}}

## Not verified and limitations

<!-- guide: Everything a reviewer might assume was checked but wasn't: NOT_RUN manual items, checks skipped,
     checks run at another SHA (name it), paid runs not made, documentation not reviewed. When this PR
     was created by github-post, add: "Document-ID collision not checked; /devforgeai:git pr runs that
     check." -->

- {{item}}

## Revision

<!-- guide: The base is the remote default branch's SHA (and the merge base, when it differs); the head is
     the remote branch's SHA, which must equal the PR's head. -->

- Base: `{{base branch}}` at `{{base SHA}}` (merge base `{{SHA}}`).
- Head: `{{branch}}` at `{{head SHA}}`, the remote branch and the PR's head.
- {{Any digest or build identifier the checks were bound to}}

{{The attribution line the session's instructions require}}
