# PRD Review skill authoring handoff

The new [prd-review development package](../../src/agents/skills/prd-review/SKILL.md)
implements the authored instructions for independent PRD assessment, architecture
sufficiency review, findings, source drift, selected retest and a manual handoff
to work planning. Source action: **CREATED**. Authoring: **AUTHORED**. Publication
and complete byte readback: **PUBLISHED**. These are custody observations.

Validation: **NOT_PERFORMED**. Testing: **NOT_PERFORMED**. All 32 mandatory
evaluation cases and their required subcases remain unexecuted. Evaluated-build
completion is incomplete; installation and framework acceptance are unperformed.
No operational package, other skill, specification or prior evidence was edited.

## Candidate and original requirements

- Original contract: [DFF-WF-03](../specs/framework/workflows/phase-3-prd-review-spec.md),
  SHA256 `f0a43675fe3a2bfe0fef7f8c8a9a672e8e58d6bdd41b43133b001dc04992f1cf`.
- Actual worktree: `C:\Projects\DevForgeAI\worktrees\git\prd-review-skill`.
- Actual target: `src/agents/skills/prd-review` in that worktree.
- Branch: `feat/prd-review-skill`; authoring base:
  `c68dacdf21509a032bebb046b322d34739f5f2fb` (`origin/main`).
- Package digest: `0b4f2fba6c9adb9f353578665dd798e411488ad413c1a274bc4a315d0d89c336`.
  This is SHA256 of compact UTF-8 JSON of sorted `{path, bytes, sha256}` manifest
  rows, unescaped Unicode and that key order, excluding root and timestamps.

| Created runtime file | Bytes | SHA256 |
| --- | ---: | --- |
| SKILL.md | 5468 | 44abf01ed921fca1cd9ea94ddaa792984d0eb918978ca9ee2a47ff521b2d174a |
| agents/openai.yaml | 244 | 8c7d9536dd2fabec16c7109afc7adb427811a0160478f7e7f079a88e85719bbb |
| assets/prd-review-template.md | 4291 | 391b9dbbf33f6c46f46069e98f4bfb738c5c97c689e0691b0af7521d97f027d3 |
| references/assessment-and-retest.md | 6470 | 523d7b7ff0a51529957b43ef0d965b439110b9247e726891d7ebd487d63a3e15 |
| references/intake-and-evidence.md | 6380 | 2c08a359f60121d799ae31655053145fdada90657ca7567d55544b4c3a9f5555 |
| references/report-and-delivery.md | 7045 | 034e1e7d1848bb6e169708b658f9a74b1deadf4ddbc8c57821ab321cee0840cb |
| references/review-and-findings.md | 5981 | 9f3d3cb9db89db06f535fe5fce3fdebe5702b407a141f410df8a6e60fc2d81fd |

## Design and retained custody

The [external authored design](skill-authoring-inputs/prd-review/20260919T143056Z/authoring-design.json)
maps PRR-001 through PRR-020 individually to observable completion, resources,
consumers and adverse conditions. SHA256:
`c653ac850bae7e7994c7b5d1709a290cb437fd3e0360d797d5897a9f842fdf07`.
The [selected request](skill-authoring-inputs/prd-review/20260919T143056Z/request.md)
records the user's worktree/draft-PR selection. No unresolved behavior questions
were introduced; there are no executable runtime helpers or required runtime
timeouts. Design expectations are untested and do not supply independent oracles.

The following custody files remain in the retained local task worktree. They bind
actual absolute roots and are not relocatable validator packets. Raw snapshots
and candidate/baseline copies stay local; the authored design, original contract,
source manifest above and this usable manual handoff are published for review.

Local run prefix:
`C:\Projects\DevForgeAI\worktrees\git\prd-review-skill\docs\plan\skill-authorings\prd-review\20260919T143056Z\`

| Local artifact below prefix | SHA256 or observation |
| --- | --- |
| authoring-record.json | aa2a003f72b0e8adadddbffaeaa4ef24dce5c96df6693b6599c998247206f7e9 |
| authoring-baseline.json | 0dd95a0ea01844ed31faac19f79d65601cc338335480dc7141bc2f2e8439d450 |
| design-capture.json | ebb52ed1500bc024a862310911db69f9ecd401ddb0c4f76d0cd0913a82cf8485 |
| validation-request.json | 22a6cec7b2bd6f8f0d1aa69ddd71e3d03b86690722483e61f0742961df011a05 |
| publication-readback.json | PUBLISHED; binds record, baseline, request and package digest |
| validator-request.md | Generated digest-bound invocation and design/source references |

Use this retained worktree for the local packet. A consumer on another host can
review the published source, specification, design and manifest, but must obtain
accessible original custody inputs or establish a new permitted validation intake;
do not rewrite sealed path-bound records or pretend remote paths are locally valid.

## Manual validator request

This is the next user's conversation request, not an invocation performed during
authoring:

```text
$skill-validator Validate and test the prd-review development skill at
C:\Projects\DevForgeAI\worktrees\git\prd-review-skill\src\agents\skills\prd-review.
Use project C:\Projects\DevForgeAI\worktrees\git\prd-review-skill and read
docs\plan\skill-authorings\prd-review\20260919T143056Z\validation-request.json
(SHA256 22a6cec7b2bd6f8f0d1aa69ddd71e3d03b86690722483e61f0742961df011a05).
Reject stale package, authoring, design or source bindings.

Original requirements: docs\specs\framework\workflows\phase-3-prd-review-spec.md
(SHA256 f0a43675fe3a2bfe0fef7f8c8a9a672e8e58d6bdd41b43133b001dc04992f1cf),
plus its governing companion contracts. Read the packet's original external
specification identity as recorded. The worktree copy had identical raw bytes.
Read docs\plan\skill-authoring-inputs\prd-review\20260919T143056Z\authoring-design.json
(SHA256 c653ac850bae7e7994c7b5d1709a290cb437fd3e0360d797d5897a9f842fdf07).
The design is authored expectation, not observed behavior. Open questions: none.

Independently construct fixtures and oracles from PRR-001 through PRR-020 and
execute PRV-01 through PRV-32, including every required subcase, initially on
native Windows/PowerShell. Cover explicit/natural activation and near misses,
standalone and legacy formats, complete/focused scopes, original-source authority,
architecture/planning boundaries, finding quality, all assessment/completeness
combinations, real independence limits, source drift, safe persistence and retest.

Observe paired source acquisition at its actual boundary. Exercise prewrite and
postwrite candidate/governing drift with semantic reassessment, not hash refresh.
Observe an actual failed full readback after a successful report write for PRV-27;
do not replace it with a mistimed failure or actor-written assertion. Exercise
collision, traversal/reparse escape, actual permission denial, interrupted writes,
resume, historical-source review, conversation-only/reuse and all retest states.
Check repeated statements, contradictory acceptance, unauthorized scope deletion,
regressions, untargeted findings and focused-result limits. Preserve all attempts.

Supply the independent Python JSONL evaluation runner, deterministic graders,
fixtures, expected results, schema, runtime/dependencies and digest manifests.
Freeze cases and subcases before running; candidate judgments are not their oracle.
Report routing, structural/artifact grading and semantic/native evidence separately.
Use independent artifact-grader negative controls. Identify controller/fixture
effects separately from skill effects and respect actual host restrictions.

All 32 mandatory cases and required subcases must pass. Count each case once;
failed/errored/skipped/blocked/unexecuted cases remain in the denominator and
retries cannot inflate it. The 95% floor cannot waive any mandatory failure.
Record cwd, versions, exact commands, exit codes, raw outputs, candidate/source/
report identities and independent adjudication. This seven-file package has zero
executable files: package coverage is NOT_APPLICABLE, never 100%. Report evaluator
or helper coverage separately and missing measurements as NOT_RUN. Other hosts
remain unqualified. Do not install, repair the package, review a real product,
invoke another workflow or claim protected framework acceptance.
```

## Authoring observations and limits

Execution used native Windows PowerShell in the task worktree. Discovered tools:
Python 3.10.11, Git 2.53.0.windows.3 and GitHub CLI 2.92.0. The installed builder
was invoked by absolute path at
`C:\Projects\DevForgeAI\.agents\skills\skill-builder\scripts\authoring.py`.

Commands executed for input preparation and custody, all exit 0:

```powershell
python -B -X utf8 docs/plan/skill-authoring-inputs/prd-review/20260919T143056Z/prepare-inputs.py
python -B -X utf8 C:/Projects/DevForgeAI/.agents/skills/skill-builder/scripts/authoring.py begin --contract C:/Projects/DevForgeAI/worktrees/git/prd-review-skill/docs/plan/skill-authoring-inputs/prd-review/20260919T143056Z/authoring-contract.json --run-root C:/Projects/DevForgeAI/worktrees/git/prd-review-skill/docs/plan/skill-authorings/prd-review/20260919T143056Z --design C:/Projects/DevForgeAI/worktrees/git/prd-review-skill/docs/plan/skill-authoring-inputs/prd-review/20260919T143056Z/authoring-design.json
python -B -X utf8 C:/Projects/DevForgeAI/.agents/skills/skill-builder/scripts/authoring.py publish --run-root C:/Projects/DevForgeAI/worktrees/git/prd-review-skill/docs/plan/skill-authorings/prd-review/20260919T143056Z
```

Begin returned STAGED. Publish returned AUTHORED, seven applied paths and no
publication issues; publication-readback records PUBLISHED. No candidate checker,
grader, sample execution or native trial was run. Authoring inspection and
whitespace review are not skill validation. Prior upstream PRD-create results do
not qualify these bytes.

`git diff --cached --check` completed with exit 0. The staged scope contains only
the seven new package files, this handoff, the selected request and external
design. `python -B -X utf8 docs/plan/skill-authorings/prd-review/20260919T143056Z/delivery-custody.py`
completed with exit 0 and recorded 20 matching byte observations in the local
`delivery-custody.json`: all seven working/staged source files match the delivered
manifest, ten original inputs are unchanged, and three publication references
still match. This is Git/source custody, not a structural or behavioral skill test.

Git worktree creation initially failed to write its branch lock in the sandbox;
the host-approved retry created the selected worktree. Final fetch similarly
required host approval for task-worktree FETCH_HEAD. Neither failure changed the
selected base or weakened restrictions. No cleanup or rollback was performed.
