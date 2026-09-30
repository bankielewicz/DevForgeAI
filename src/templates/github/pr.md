<!-- guide: Pull request body. The title follows the repository's commit convention (for example
     "feat: …", "docs: …"). Every statement is a fact about this branch: what changed, what was run
     and what it printed, what wasn't verified. List only checks actually run in this session or
     recorded elsewhere with a cited location. Nothing aspirational. Delete every guide comment
     before posting. -->

## Summary

<!-- guide: What changed and why, in two to five lines, naming the specs, decisions or issues behind it. -->

{{What changed and why.}}

## Changes

<!-- guide: Group by area. Name the paths. Say what didn't change when a reader might expect it to. -->

- **{{Area}}:** {{what changed}} (`{{path}}`)

## Implements and references

<!-- guide: The spec, VER and issue IDs this implements or records. Use "Fixes #N" only when merging this
     PR resolves the issue; otherwise "Refs #N". -->

- {{SPEC-NNN, VER-NN, …}}
- Refs #{{N}}

## Checks run

<!-- guide: Each check with its command and the result line it printed. Say where a result is recorded when
     it wasn't run in this session. A check that failed stays listed as failed. -->

- `{{command}}`: {{result line}}

## Not verified and limitations

<!-- guide: Everything a reviewer might assume was checked but wasn't: NOT_RUN manual items, checks skipped,
     paid runs not made, documentation not reviewed. When this PR was created by github-post, add:
     "Document-ID collision not checked; /devforgeai:git pr runs that check." -->

- {{item}}

## Revision

- Base `{{base branch}}` at `{{short SHA}}`; head `{{short SHA}}`.
- {{Any digest or build identifier the checks were bound to}}

{{The attribution line the session's instructions require}}
