---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-ARCH-001"
artifact_type: "expert-evaluation-report"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:44:10Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
execution_ref: null
upstream:
  - artifact_id: "SKILL-005"
    revision: "2 (DRAFT MVP specification, refreshed 2026-09-05 UTC)"
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-005-devforge-architect.md"
    sha256: "b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
  - artifact_id: "devforge-architect candidate"
    revision: "61f6ef06fc61fa92d7a3714c54a5251cd9177a4f"
    store: "project"
    path: "/home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910/providers/claude/plugins/devforgeai/skills/devforge-architect"
    sha256: "SKILL.md cb51fead7d5bdd8ed6fcee17c3e6ae6a716efc0936108240e535fa0cca04b9e4; full 32-file manifest below"
    sections:
      - "entire package"
evidence:
  - path: "validation-plan.json"
    sha256: "2e499ea91c0579e5227e3a51f7998bbe9faf33adcfc8df5e72482a80fd0c698a"
  - path: "ai-review.json"
    sha256: "964c0ce8c6dbf780c50469d1045329735038b812daefb56ac089aeaed85cc2bb"
  - path: "findings.json"
    sha256: "18a031130e109e96070fdbb8c65221a12c7603459129d49db901bb1f1dca49e7"
  - path: "validation-results.json"
    sha256: "5c8ad6ee2a64d00643f06d9fc4ece74113a9c7cd530c3eed22dcf75dcc8bdf69"
  - path: "runner-out/"
    sha256: "nine observation files, each digested in the runner observations table below"
  - path: "commands.log"
    sha256: "digested in the handoff, after this report's bytes are final"
supersedes: null
decision_ref: null
missing_inputs:
  - "An installed or exported devforge-architect copy. Blocks every tier C observation."
  - "A fresh Claude Code terminal with an observable client version. Blocks every tier A observation."
  - "A permitted isolated evaluation workspace with per-attempt client state separation. Blocks every tier B observation and both arms of the without_skill comparison."
  - "A second separately dispatched reviewer context for P3. This session is the packet-designated fresh evaluator context and also ran P2; recorded as an independence limit rather than substituted."
---

# Skill verification results: devforge-architect (SKILL-005)

Independent scaffold evaluation. The evaluator did not author the candidate and has not edited it, its specification, its cases or its expectations.

## Identity and scope

- **Evaluation plan:** `validation-plan.json` in this directory, sha256 `2e499ea91c0579e5227e3a51f7998bbe9faf33adcfc8df5e72482a80fd0c698a`. Written after the deterministic runs; see the procedural limit in its own `_note` and in Limits below.
- **Candidate source identity:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910/providers/claude/plugins/devforgeai/skills/devforge-architect` at commit `61f6ef06fc61fa92d7a3714c54a5251cd9177a4f`. HEAD equals the frozen commit, `git diff 61f6ef06 HEAD --stat -- providers/` is empty and `git status --porcelain` is clean, so no coordinator evidence commit intervened. Manifest below, recomputed by this evaluator.
- **Installed candidate identity:** not installed. No installed or exported copy exists anywhere; this assignment authorised none and the packet directs that no install be attempted.
- **Specification:** `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-005-devforge-architect.md`, revision 2, sha256 `b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b` — recomputed, matches the packet.
- **Baseline:** `without_skill`. Verified rather than accepted: `git ls-tree -r c17e758417da64928a0f47fc2600304465ac3f3c -- providers/claude/plugins/devforgeai/skills/devforge-architect` returns nothing, so no previous revision exists and `old_skill` is unavailable. The baseline arm was `NOT_RUN`.
- **Builder the author followed:** `devforge-project-expert-creator` at `4999f3106565c5e320d1f1a7db066b437e4e94be`, source-loaded. The author's records say so explicitly and the commit exists with the subject "devforge-project-expert-creator repair pass 1 from E1 bootstrap review (F-001..F-004)". The author also records that the builder is itself a draft under independent review with no native evaluation, and that following it is following a draft methodology.
- **Client, version and model configuration:** unknown for any measured skill run, because no measured skill run occurred. The evaluator's own system prompt states model name **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`, and does mention a 1M context window.
- **Assignment and write fence:** independent scaffold evaluator under coordinator dispatch. Permitted writes: this directory only. Read-only on the candidate, the authoring evidence, both sibling worktrees and both framework repositories. No commit.
- **Independence conditions actually met:** separately dispatched from the author; fresh context holding only the packet, the frozen inputs and self-gathered evidence; the author's preferred disposition was checked for and none exists. **Not met:** the same session ran P2 and P3, there was no second reviewer, and the author's `evals/evals.json` graded observations — effectively the tier-B expected answers — were read during P2 orientation before R01–R10 were drafted. The author's narrative records were deliberately not opened until after R01–R10 were drafted, then read only to check their claims against bytes. Full list in `ai-review.json` under `reviewer.independence_limits`.
- **Scope of this evaluation:** structure, resolution and provenance; requirement coverage against SKILL-005; instruction clarity and usefulness; authority boundaries; Claude provider correctness; eval quality. It does **not** cover discovery, activation, instruction loading, installed-resource resolution or output quality — none of those was observed.

### The validator this evaluation followed

The workflow, rubric, runner and record templates are the Claude `devforge-evaluate-expert` package **source-loaded, not installed**, from `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910` at commit `e641797eebf04cd1e8eb9f711549e038e7745407`. Its `SKILL.md` is sha256 `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac`; `scripts/run_cases.py` is `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2` and `scripts/graders.py` is `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f`, both verified byte-identical between that worktree's working tree and the blobs at the frozen commit.

**That validator is itself a draft under bootstrap review.** Its E2 review returned *revise*; the repairs were applied at `e101e76162976f2414035bbe542f0a34f8cc51be` ("repair pass 1 from E2 bootstrap review (F-001..F-009)"), a focused recheck at `6916b60` closed F-001..F-009 and opened a new MINOR F-R01, and `e641797` is the commit that closed F-R01 by regenerating the derivation digests. `e101e76` is an ancestor of `e641797`, so this evaluation followed the post-repair, post-recheck bytes. It has had no native evaluation. Following it is following a draft methodology, and nothing in this report inherits validation from it.

### Candidate source manifest

Recomputed by this evaluator from the frozen tree, not copied from the author's manifest. 32 files. The author's `authoring/file-manifest.json` was then compared against it: all 32 digests match, no file on disk is missing from it and no entry in it is missing from disk.

| Path | SHA-256 |
| --- | --- |
| `SKILL.md` | `cb51fead7d5bdd8ed6fcee17c3e6ae6a716efc0936108240e535fa0cca04b9e4` |
| `assets/architecture-contract.md` | `38b4ec73345e05563fcffc0efe6a8165b9cfa2f32eca40254e90b53ae5ad1218` |
| `assets/handoff.md` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` |
| `references/derivation.json` | `69441df618eac3ae5727217ddbcab839abc04a9608556e6eba469f5a0b3cf6da` |
| `references/framework-context.md` | `1672462fcf118d6be9af08dca94d05efb4caeab128d9b671fd8419b52910ed19` |
| `references/recording-rules.md` | `5e828c935fed53e62000df883ea4cb3565ca7194909a687febb47401a024f18a` |
| `references/sources.md` | `61ed1720311c3b2370db1d3c578d2e3a1c5381b8490718a8788c7197bf205e37` |
| `references/version-evidence.md` | `d788578077654daaa8cae752d5142dfd88fa85042fa90128980df34981c48cad` |
| `evals/cases.jsonl` | `809a67baab4ed8fd7e967d750e76667761c7475d1e2fd685d98bff1cdd5a0eb1` |
| `evals/evals.json` | `dba8dd4530ced694f2ed37d2a1ec6f0ba9d88471522e1f1cc85fd1bf9ae0c947` |
| `evals/triggers/trigger-queries.json` | `0caa042650d002dcb5e8fe03067728cbab6842a6fadf81be0a2a42a92085aaf2` |
| `evals/fixtures/README.md` | `166a6cdbf72c8b00b208390f4bcd46a5899bc7faf42770e99663baf43330111b` |
| `evals/fixtures/collision/SESSION-042.md` | `355f792661a31179a41fa7db1c27c5fe57c900d7bcc8c4cd3cd62f162438ac42` |
| `evals/fixtures/collision/request-note.md` | `171199780302270054720b133ef3fa8bb76880289215f6e021e9ad34e0a73576` |
| `evals/fixtures/could-not-run/request-note.md` | `dcf154d5557ab3f25727a9e3eb65501f189f9af263f855063c8ed6c546e37c1f` |
| `evals/fixtures/drift/PB-002.md` | `38ca5f9d50672882c637794a063381e1f14c1d3a82c737dd60fb16c1d0909659` |
| `evals/fixtures/drift/note-from-the-lead.md` | `89e915c099713b87c0fc7d2a1dde59f0a8ec85c267e72de5367aad1c1f2c3c05` |
| `evals/fixtures/drift/observed-tree.txt` | `354067d90a180415eacc28680bffe817ff50cdc37ac7851204eb46cd066bb342` |
| `evals/fixtures/drift/package.json` | `fe505057b272ce403f74229e078121659c05c551bb2911be8257fa4dbb3dd6b8` |
| `evals/fixtures/existing-stack/Directory.Packages.props` | `f7274f78b8b6c4ddc6f2153c4977df127123e372d418175fbfccd93703345b18` |
| `evals/fixtures/existing-stack/note-from-the-user.md` | `9dd54d1d2a5fe8d00eb2b07e9bba82e4903cb54728236fa10f04952d3514330e` |
| `evals/fixtures/existing-stack/observed-tree.txt` | `9c39f8c71c355d3685b7b15b9b27e3701b01fed6fdc9c9702f3e979347db59ba` |
| `evals/fixtures/existing-stack/src/Notes.Api/Notes.Api.csproj` | `feb36264d3cebc78281de50af5b68aa8daa7b2000e6321fa2e7f9e58294b1104` |
| `evals/fixtures/greenfield/PB-001.md` | `776fb9bd9616ddaaaa6ec10db2608afec2c227ebfd4e6a227aa1d5d218373773` |
| `evals/fixtures/out-of-scope/docs/getting-started.md` | `abb76b894f05f4f31cfc116be345b2e471d50fc85b5118695916a6be3ea8d36b` |
| `evals/fixtures/out-of-scope/request-note.md` | `55b7323343bca9cadbb94c2521fc84a4417365ce40dc1fd3c4a762074ce02859` |
| `evals/fixtures/placeholder/ARCH-005.md` | `4d25f4be00ba47910727802e8ea0382817c8adbe7f12e4f477d8d97f26616fcc` |
| `evals/fixtures/stale/ARCH-004.md` | `b058798466a3d263aed1f5a97a60e942a44a8b455b6bc09fb5b64b07d9aa8982` |
| `evals/fixtures/stale/PB-003.md` | `327ac438fd3665e45a2fb0a8ecf8345a76506bf705965519f7d77e0de38801a3` |
| `evals/fixtures/stale/preserved/PB-003.r1.md` | `b6097c371bc88e64c41a77ee772d138e8173900614574649798f53f051ddc3b2` |
| `evals/fixtures/version-uncertainty/Directory.Packages.props` | `7bdb76205615f93a357980058690b0352db246cbdd9355046bd603c43132a7a3` |
| `evals/fixtures/version-uncertainty/proposed-snippet.md` | `7902ed106cf564195552844d8084fe1695cf6040f211d80aa247574d4dfde9a0` |

## Evidence groups and outcomes

Reported separately. They are not merged into a figure, and there is no score anywhere in this report.

| Group | Observations | Outcome | Evidence | Limits |
| --- | --- | --- | --- | --- |
| Intake and freeze | Candidate commit and cleanliness, specification digest, baseline existence, builder identity, validator identity, CLI surface, live client documentation | PASS (3 of 3 checks) | `validation-results.json` results[CHK-INTAKE-001..003]; `commands.log` | Frozen at 2026-09-10T21:23:15Z–21:35:45Z UTC; a later change to any input starts a new iteration |
| Structure (manual observation) | 18 rows: inventory, frontmatter, name-versus-folder, link resolution, declarative parsing, derivation verification, fixture completeness and reproducibility, injection and leak scans, trigger split, CLI command existence, grader discrimination | 18 of 18 observations obtained; 17 rows clean, and row M-11 (the interruption grep) supplies the evidence for the one FAIL, which is attributed to `CHK-AI-R04` in the ai_review group | `validation-results.json` structural_observations; nine files under `runner-out/` | **Method: INSPECTION_MANUAL; authority: none.** The DevForge CLI has no skill-package structural-inspection capability, so these are readings, not a gate result |
| Independent review R01–R10 | Ten applicable criteria against the frozen rubric | 9 PASS, 1 FAIL (R04) | `ai-review.json` revision 2, sha256 `964c0ce8c6dbf780c50469d1045329735038b812daefb56ac089aeaed85cc2bb` | Single-context review; the author's tier-B expected observations were in context before drafting. See F-008 |
| Tier C installed resources | ARCH-PKG-001, ARCH-PKG-002 as native observations | **NOT_RUN** | `findings.json` F-006 | No installed copy, no fresh terminal, no isolated workspace allocated in this assignment; the packet directs no install. Static link resolution does not establish tier C |
| Tier B output quality | ARCH-B-001..ARCH-B-009, candidate and `without_skill` arms | **NOT_RUN** | `findings.json` F-006 | Same cause. No boundary was established and no measured worker was launched. A missing arm supports no improvement claim |
| Tier A discovery and activation | A1a..A13a; explicit invocation kept separate from implicit | **NOT_RUN** | `findings.json` F-006 | Same cause. Inventory presence, session selection, instruction loading and task completion remain four unobserved facts |

## Checks actually run, with their commands

Every command is in `commands.log` with an observed `date -u` stamp and its exit status. The runner was invoked as the validator's `references/runner-interface.md` documents, through the interpreter, with `-B`, absolute paths and `--out` inside this fence.

1. **Intake.** `git rev-parse HEAD`, `git diff 61f6ef06… HEAD --stat -- providers/`, `git status --porcelain`, `git ls-tree -r c17e758… -- …/devforge-architect`, `git cat-file -t 4999f31…`, `git merge-base --is-ancestor e101e76 e641797`, `sha256sum` over the candidate tree and every governing input.
2. **CLI surface.** `devforge --help`, `devforge check --help`, `devforge expert --help`, `devforge delivery --help`, `devforge --version` against `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge`, sha256 `835c32639c0a7df270fe1b9182580f14fc7d0874d3aad1b4037ba7cf420b2b07`, version `devforge 0.1.0`.
3. **Client documentation.** `https://code.claude.com/docs/en/skills`, fetched 2026-09-10 UTC between the observed readings 21:27:14Z and 21:35:45Z. Used to check the candidate's own claims rather than to accept them: the page states the `description` (with `when_to_use`) is **truncated at 1,536 characters**, which is the figure `references/sources.md` records; the candidate's description measures **1,297 characters**, so nothing in it is lost to truncation. The page's account of slash-command derivation, discovery precedence, on-demand supporting-file loading, the 500-line `SKILL.md` guidance and the exclamation-prefixed shell-injection forms also matches what `sources.md` says it took from that page.
4. **Grader discrimination, before using the graders on the candidate.** The validator's own 17 cases against its own known-answer fixtures, in both modes.
5. **Candidate authored cases**, three invocations, plus a fourth deliberately mis-rooted one to observe the documented two-root behaviour.
6. **Evaluator-added structural cases**, two invocations. Ten cases authored in this fence because the candidate's own tier-C coverage omits `assets/`, fixture-reference completeness, fixture digest reproducibility and the injection-syntax scan.
7. **Manual scans**: shell-injection forms, absolute host paths, `docs/mvp` runtime dependency, Codex-only concepts, held-out fixture answers in `SKILL.md` and the references, `evals.json` `files[]` resolution, trigger-split stratification, and the `interrupt|resume` grep that produced F-001.

## Runner observations

Local, non-isolated evidence. `MATCH` / `MISMATCH` / `INDETERMINATE` are observations about single assertions; none is copied into a result. Every invocation exited 0 — including the one in which nine cases reported `COULD_NOT_RUN` — because the exit status describes the program, not the candidate. **There is no aggregate row anywhere in these files and none is computed here.**

| File | sha256 | Candidate root | Mode | What it observed |
| --- | --- | --- | --- | --- |
| `gradercheck-validator-fixtures-source.jsonl` | `76c67f18a7a4a8d0a755ee717c84d11e0d87f635f4bf2c17c37719024d9be807` | validator's `evals/fixtures` | source | 17 cases against known answers |
| `gradercheck-validator-fixtures-installed.jsonl` | `247e8431734678398ad95e7002cbd99e6d4f617eb66e53bd3be817af3f26181e` | validator's `evals/fixtures` | installed | same, mode-conditioned rows differ as designed |
| `candidate-pkg-source.jsonl` | `1a005cb24778c3337fe3e85534086999d6b8e7433b2ce2e4a311cb087dfb7b0f` | package root | source | ARCH-PKG-001, ARCH-PKG-002 |
| `candidate-pkg-installed.jsonl` | `530a653e97e518384371668fbac47bbd6c4ab1b263c548c831ef563dcbd0f87c` | package root | installed | same two, to observe the mode-conditioned assertion |
| `candidate-b-fixtures.jsonl` | `32edfab35ef6c5584cde5256d19696898c11ef448feb2ad764119a5dfbf5aa08` | `evals/fixtures` | source | ARCH-B-001..009 |
| `candidate-allcases-pkgroot.jsonl` | `1a90282dce0d57f701943f791766308ce94f2ec4fc1f78114d158f29f6380590` | package root | source | whole file at one root, deliberately |
| `evaluator-added-cases.jsonl` | `5b2db5f9f84bd12351e93b16b9c4f4a5b87831d0b4b7e63a016dfbc61b8371ce` | — | — | the ten evaluator-added cases themselves |
| `evaluator-added-pkgroot.jsonl` | `e9a3cc8d93005f4ec353f954d63f940b3a2a7eeca8c38e09fb794515d24f66b4` | package root | source | EV-ADD-PKG-001..005 |
| `evaluator-added-fixtures.jsonl` | `32df8426eeb8b913a5dcf5624d5d800726f9b4c6ff6e9d874c032dbabbb5c4e2` | `evals/fixtures` | source | EV-ADD-FIX-001..005 |

### Rows, and how each is to be read

| Case | Assertion | Grader | Result | Reading |
| --- | --- | --- | --- | --- |
| ARCH-PKG-001 | A1 | `frontmatter_present` | MATCH | Delimiters present |
| ARCH-PKG-001 | A2 | `frontmatter_fields` | MATCH | `description`, `name` both populated scalars |
| ARCH-PKG-001 | A3 | `name_folder_relation` | MATCH | `name='devforge-architect'`, `folder='devforge-architect'`. Equality asserted as a DevForgeAI convention the case declares, **not** as a Claude conformance rule |
| ARCH-PKG-001 | A4–A8 | `package_relative_links` | MATCH ×5 | SKILL.md 6 local / 0 external; the three procedural references 0 local each; `sources.md` 2 local resolving, 1 external counted and never fetched |
| ARCH-PKG-001 | A9–A10 | `path_present` | MATCH ×2 | Both output templates present |
| ARCH-PKG-002 | A1 | `path_absent` | INDETERMINATE (source) / MISMATCH (installed) | **Expected, not a defect.** The assertion is installed-mode-only. In source mode the grader declines. In installed mode it observes the source tree, where `evals/` is correctly present. No installed copy exists, so this is not a tier-C observation |
| ARCH-B-001..004, 006, 007 | sentinel assertions | `artifact_side_effect` | MATCH ×6 | Every fixture the cases pin still hashes to its authored bytes. Independently re-verified against the evaluator's own manifest in EV-ADD-FIX-002 |
| ARCH-B-006 A1, ARCH-B-007 A1 | | `path_present` | MATCH ×2 | Fixture sanity: the ownership record and the preserved revision-1 bytes are there |
| ARCH-B-008 | A1 | `required_report_fields` | MISMATCH | **Expected, and the case says so.** A fixture sanity check confirming `ARCH-005.md` really does still hold `{{project_id}}` and `{{ISO-8601-UTC-time}}` for a worker to find. A MATCH would have broken the case |
| ARCH-B-009 | A1 | `path_absent` | MATCH | Fixture sanity: `policies/shiftwell.json` really is absent, so the case's expected cause is real |
| ARCH-B-001..009 | routed assertions | `null` + `routed_to` | INDETERMINATE ×11 | **By design.** Each records an expectation no deterministic check can establish and names where it is routed. The runner emits INDETERMINATE with the routing, which is the honest answer and is deliberately visible |
| EV-ADD-PKG-001 | A1–A3 | `package_relative_links` | MATCH ×3 | Both copied templates and the fixtures README carry no local destination that escapes the package. This is the coverage the candidate's own case omits |
| EV-ADD-PKG-002 | A1–A7 | `path_present` | MATCH ×7 | Every reference and asset `derivation.json` binds is on disk |
| EV-ADD-PKG-003 | A1–A3 | `artifact_side_effect` | MATCH ×3 | No `` !` ``, no ` ```! `, no `/home/`, no `docs/mvp/`, no `${CLAUDE_*}` variable in `SKILL.md` or the two procedural references |
| EV-ADD-PKG-004 | A1–A2 | `required_report_fields` | MISMATCH ×2 | **Expected, and the correct result.** Both shipped templates still hold their placeholders, which a blank source template must. A MATCH here would have been the defect |
| EV-ADD-PKG-005 | A1–A3 | `path_absent` | MATCH ×3 | No `scripts/`, no `agents/openai.yaml`, no `hooks/` in the package |
| EV-ADD-FIX-001 | A1–A20 | `path_present` | MATCH ×20 | All twenty fixture paths named in `evals.json` `files[]` exist |
| EV-ADD-FIX-002 | A1–A2 | `artifact_side_effect` | MATCH ×2 | Ten fixtures hash to the evaluator's independently computed digests, including four that carry no sentinel of their own |
| EV-ADD-FIX-003 | A1 | `artifact_side_effect` | MATCH | `ARCH-004.md` cites `b6097c37…`, which is the real digest of `preserved/PB-003.r1.md`; the live revision-2 digest `327ac438…` appears nowhere in it. The fixture tests staleness, not a broken locator |
| EV-ADD-FIX-004 | A1–A3 | `path_absent` ×2, `path_present` | MATCH ×3 | The `COULD_NOT_RUN` fixture's stated cause is real |
| EV-ADD-FIX-005 | A1–A4 | `artifact_side_effect` | MATCH ×4 | No fixture note carries a shell-injection placeholder in either form |

**The mis-rooted run.** `candidate-allcases-pkgroot.jsonl` ran the whole case file against the package root and produced nine `COULD_NOT_RUN` rows for the tier-B cases. That is the documented behaviour, not a defect: `evals/fixtures/README.md` states plainly that the two case families have different candidate roots, gives both invocations, and says "A case run against the wrong root reports `COULD_NOT_RUN` for an unresolvable `candidate_subpath` rather than silently matching nothing." The run confirms the documentation is accurate.

**Grader discrimination.** Before any of this was used on the candidate, the validator's own cases were run against its own known-answer fixtures. Every conforming fixture matched; every deterministic defect fixture mismatched; the unparseable-frontmatter fixture returned INDETERMINATE and the incomplete-negative-transcript fixture set its case to COULD_NOT_RUN, both as designed; the two semantic-defect fixtures returned INDETERMINATE because they deliberately carry no deterministic assertion. That is a test of the graders, not an evaluation of anything, and it is the basis for citing their rows below.

## Independent review R01–R10

Full records with evidence locators in `ai-review.json` revision 2, sha256 `964c0ce8c6dbf780c50469d1045329735038b812daefb56ac089aeaed85cc2bb`. No average, weighted score or percentage is computed.

| Criterion | Applicable | Outcome | One-line basis |
| --- | --- | --- | --- |
| R01 Task identity and scope | yes | **PASS** | `name` equals folder; a 1,297-character description that states the capability, four discriminating situations matching the specification's request rows, and seven sibling exclusions all naming real roster skills; 239 characters clear of the measured truncation point. ADVISORY F-002 on the unnamed `devforge-review` boundary |
| R02 Inputs, outputs and completion | yes | **PASS** | All five specification input rows with their requirement levels; consume-only stated once for the table; missing-input behaviour explicit and non-fabricating; outputs, destinations, ID prefixes and a finite stopping condition all present |
| R03 Authority, ownership and accepted decisions | yes | **PASS** | Proposals and adoptions kept apart with `decision_ref` null while none exists; authority kept external; prior accepted bytes preserved; collision behaviour forbids delete, reset, revert, force and quiet relocation |
| R04 Workflow decisions and failure paths | yes | **FAIL** | Four phases with checkable exits and five failure branches matching the specification's common cases — but the specification's interruption-and-resume requirement is demonstrably omitted from the whole package. F-001 |
| R05 Runtime dependencies and resource delivery | yes | **PASS** | Two roots separated correctly; both templates copied in and verified byte-identical to their `docs/mvp` sources; every local link resolves in-package; no host path, no `docs/mvp` runtime dependency; every DevForge command named exists in the operator binary's help. ADVISORY F-003 |
| R06 Instructions versus supplied data | yes | **PASS** | One boundary statement covering documents, code, manifests, pasted snippets, retrieved pages and tool output, recognisable without any markup convention, and explicitly foreclosing the confident-phrasing escape |
| R07 Framework semantics and artifact provenance | yes | **PASS** | Envelope distillation compared field by field against the artifact contract and faithful on all eleven; stable non-reused IDs; no artifact carries its own digest, and none in the package does; `derivation.json`'s claims verified against bytes |
| R08 Prompt organisation and decision-relevant detail | yes | **PASS** | 120-line entrypoint holding every essential rule, with conditional detail routed from the phase that needs it; no conflicting duplicate rule; judgement left open where the specification leaves it open |
| R09 Observable checks and honest outcome reporting | yes | **PASS** | Fixed result vocabulary; self-issued PASS and phase-narration-as-check explicitly forbidden; `devforge check` described no more widely than it proves, matching the binary's own help text; the authored eval records carry `NOT_RUN` rather than a borrowed status |
| R10 Enforcement and handoff boundaries | yes | **PASS** | A nine-field enforcement-requirement record ending in a fixed "no gate is implemented, activated or executed by this skill" status; unmet requirements stay visible rather than being downgraded to advisory prose; the handoff forbids presenting a fictional command as runnable |

## Candidate and baseline comparison

| Case ID | Candidate evidence | Candidate outcome | Baseline evidence | Baseline outcome | Constraint violations |
| --- | --- | --- | --- | --- | --- |
| ARCH-B-001 … ARCH-B-009 | none — no measured run | NOT_RUN | none — arm not executed | NOT_RUN | not observable |

No comparison is made and none is possible. An incomplete baseline supports no improvement claim; here **both** arms are incomplete. Order sensitivity, identity leakage, effective tool assistance and sampling limits are all unmeasured because nothing was measured.

## Findings

Full records in `findings.json`, sha256 `18a031130e109e96070fdbb8c65221a12c7603459129d49db901bb1f1dca49e7`. Machine-readable per-check outcomes in `validation-results.json` revision 2, sha256 `5c8ad6ee2a64d00643f06d9fc4ece74113a9c7cd530c3eed22dcf75dcc8bdf69`.

| Finding ID | Type | Severity | Requirement | Evidence | Demonstrated impact | Affected cases |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | defect | **MINOR** | SKILL-005 "Workflow and phase exits" and "Rework, stopping, and recovery" | `SKILL.md` lines 103–120 (where the branch belongs); the specification sentences; `recording-rules.md` 356–383 (the two sections the author's mapping cites); exhaustive `interrupt\|resume` grep | A session interrupted mid-contract has no instruction to preserve the current phase's partial evidence or to re-read the session assignment before continuing. Contained: the unconditional pre-write identity rules still catch the highest-risk case, a silently stale upstream | ARCH-B-007, ARCH-PKG-001, EV-ADD-PKG-001 |
| F-002 | enhancement | ADVISORY | SKILL-005 use-case inventory | `SKILL.md` line 3; `trigger-queries.json` A12a and `owner_map.negative_review`; measured 1,297 of 1,536 characters | A near-miss review request is discriminated by the absence of an attractor rather than a stated boundary. Unmeasured — tier A did not run | A12a |
| F-003 | enhancement | ADVISORY | SKILL-005 "Only documented, implemented DevForge commands may be named" | `SKILL.md` line 93 versus `devforge --help` | None. No named command is fabricated; `includes` is non-exhaustive and the same sentence tells the reader to check the operator's binary | — |
| F-004 | enhancement | ADVISORY | SKILL-005 consumer-coverage line | `SKILL.md` lines 3 and 87; `spec-mapping.md` consumer row | None. The author disclosed the partial with a sound reason; `devforge-evaluate-expert` consumes an expert package, not the contract | — |
| F-005 | enhancement | ADVISORY | skill-authoring-contract "Three separately reported evaluation tiers" | `trigger-queries.json` stratification tally | None yet. Six negative routings sit in one split only, so a later description change tuned on train would have no held-out check for them | A5a, A6a, A7a, A8a, A9a, A10a, A11a, A12a, A13a |
| F-006 | **evaluation_gap** | MAJOR | SKILL-005 "Validation and behavioral acceptance" | the assignment | Every behavioural claim is unavailable. **Not a defect in the candidate** | all C, B and A cases |
| F-007 | **evaluation_gap** | MAJOR | the two missing CLI capabilities | `devforge --help` and subcommand help, run against the operator binary | Structural rows have no gate authority and runner identities are self-reported. **Not a defect in the candidate** | — |
| F-008 | **evaluation_gap** | MINOR | rubric "Preparing an independent review" | `ai-review.json` `reviewer.independence_limits` | Bounds the strength of R01–R10; does not invalidate them | — |

### Things considered and recorded as non-findings

So that a later reader can see they were checked rather than missed:

- `references/sources.md` is not reachable by Markdown link from `SKILL.md`. It is the package's provenance record in the sense of the authoring contract's "Record source URLs, applicable versions, retrieval dates, claims supported, and refresh conditions in the package's provenance record", carries no task instruction, and is the same class of file as `derivation.json`, which is likewise unlinked. **No target edit.**
- The one `/home`-family grep hit in the package is the string `~/.claude/skills/` inside `sources.md`. That is Claude's documented discovery location, verified against the live page; it is not a developer home path.
- The one `docs/mvp` mention is a prohibition against depending on `docs/mvp` at runtime.
- `AGENTS.md` appears once, named alongside `CLAUDE.md` as a project-convention file to check. That is provider-agnostic, not a Codex-only concept.
- Dapper and SQL Server appear in `recording-rules.md` as a teaching example about preferences versus decisions, and `existing-stack/` uses Dapper. The specification's own acceptance row names Dapper and Entity Framework, so this is specification-derived, not a held-out fixture answer leaking into the entrypoint. The reference's example is in fact the opposite framing to the fixture's.
- The eval cases depend on the sibling `devforge-evaluate-expert` package's `scripts/`. That dependency lives inside `evals/`, which is stripped from installed copies and exports; it is not a runtime dependency on another skill package.
- The two-root invocation requirement is documented in `evals/fixtures/README.md` with both commands. Not a defect.

## Missing capabilities and evaluation prerequisites

Both statements are recorded whatever the observations turned out to be, and they were verified against the operator binary's own help rather than taken on the validator's word.

- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.** Every structural fact in this report was obtained by reading and is labelled `INSPECTION_MANUAL` with `authority: none`. `devforge check` describes itself as "Check structural policy and provenance; does not certify semantic behavior", takes a project and a policy, and is not a skill-package inspector. No `decision.json` or equivalent receipt exists or was produced; the disposition below was adjudicated by hand. A complete set of matching runner rows does not close this dependency. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** The runner, grader, Python and case identities in every observations header are self-reported by the run, and a file describing itself is not a protected manifest. Owner: DevForge integration owner.
- **Native evaluation environment.** No installed copy, no fresh terminal, no isolated workspace, no per-attempt client state separation. Blocks tiers C, B and A and the whole baseline comparison. Owner: coordinator. See F-006.
- **A second independent reviewer context.** Bounds the R01–R10 records. Owner: coordinator. See F-008.

These are prerequisites, not defects in the candidate. Editing the candidate produces none of them.

## Decision and coverage

- **Disposition: revise.**
- **Basis:** adjudicated by hand against the frozen results contract, because evidence reduction is not implemented in the DevForge CLI and no decision receipt exists. The contract's precedence is that any applicable `FAIL` produces *revise*; `CHK-AI-R04` is an applicable `FAIL`. That rule is reached before the missing-observation rule, so the `NOT_RUN` tiers do not turn this into *insufficient evidence* — both facts are reported, and a reader must read every row rather than assume one headline covered them.
- **What *revise* does and does not mean here.** It rests on **one MINOR defect with a two-sentence repair**. It is not a judgement that the package is weak. Nine of ten rubric criteria pass, all eighteen structural observations were obtained with seventeen rows clean, every digest the package asserts about itself was independently verified and matched, and no BLOCKER or MAJOR defect was found. Had the interruption branch been present, the disposition would have been *insufficient evidence* on the unrun tiers — never *suitable for the stated scope*, which no evidence in this assignment could have supported.
- **Behavioural status: NOT_EVALUATED.**
- **Coverage actually obtained:** intake complete (3 of 3); structure complete (18 of 18 observations obtained); independent review complete (10 of 10 criteria).
- **Where the single defect is counted:** once. Structural row M-11 records the observation; the requirement application that makes it a `FAIL` is `CHK-AI-R04` in the ai_review group, because the omitted behaviour is a specification requirement assessed under rubric criterion R04 and no `CHK-STRUCT` check was planned for it. No `CHK-STRUCT` result row carries a `FAIL`. Counting it in both groups would double-count one defect.
- **Required observations not obtained:** tier C `NOT_RUN`; tier B `NOT_RUN`, both arms; tier A `NOT_RUN`. One cause for all three, recorded in F-006.
- **Observed metrics:** the runner's `metrics` fields are bounded reads of that program, not measurements of any client session, and no client session metric exists.
- **Adoption reference:** null. Nothing here adopts, installs, accepts or releases anything.
- **Handoff reference:** `handoff.md` in this directory.

*Suitable for the stated scope* is a recommendation and would not have been acceptance. This report recommends; it does not accept.

## Limits, including this evaluation's own

1. **The validator is unqualified for this use in a specific sense.** It is a draft under bootstrap review with no native evaluation of its own — E2 returned *revise*, repairs landed at `e101e76`, a focused recheck closed F-001..F-009 and opened F-R01, and `e641797` closed that. Its rubric anchors are DevForgeAI evaluator design requirements, not any provider's certification criteria. Applying a draft methodology does not make its outputs invalid, but it does mean a later revision of the validator could change which criteria apply or what their anchors demand, and this report would then need rechecking rather than amending.
2. **The plan record was written after the deterministic runs.** Nothing was chosen after seeing output — every candidate expectation was already frozen in the candidate's own case file at `61f6ef06`, and the evaluator-added expectations were written before their first execution — but the ordering is recorded rather than backdated.
3. **The independent review is single-context.** Same session as P2, no second reviewer, and the author's tier-B expected observations were in context before R01–R10 were drafted. F-001 rests on an exhaustive grep and a specification sentence, neither of which those observations could have anchored, but a contested criterion should go to a second fresh reviewer rather than be settled by weighting this one.
4. **Nothing behavioural was observed.** No discovery, no activation, no loading, no output. A static PASS on any criterion does not establish that a session will follow the instructions.
5. **Structural rows carry no authority.** They are readings, because the gate that would give them authority is not implemented.
6. **Runner evidence is local and non-isolated**, produced in the evaluator's own environment with self-reported identities.
7. **The author's records are untrusted evidence.** They were read after R01–R10 were drafted and only to check claims against bytes. The author states no preferred disposition anywhere — checked by grep — so none was available to adopt or resist. Where a claim overstated coverage, that is recorded inside F-001 rather than accepted.
8. **Two corrections were made to this evaluation's own records before delivery, and are disclosed rather than silently applied.** (a) `ai-review.json` revision 1 carried one-based line spans for `references/recording-rules.md` and `references/framework-context.md` that were offset by the header of a concatenated multi-file read - by +298 and +207 respectively. Every section name in every citation was correct, so the locators always resolved by section, but the numbers did not; revision 2 corrects them, verified against `grep -n '^## '` on both files. No criterion outcome, reason, finding or severity changed. (b) `validation-results.json` revision 1 recorded structural row M-11 as `FAIL` while every `CHK-STRUCT` result row was `PASS` or `NOT_APPLICABLE`, so one defect appeared to be attributed to two evidence groups; revision 2 adds an explicit attribution note and this report's prose was corrected to match. Both revision-1 states are described in the revision notes inside those records rather than erased. This is the same class of defect this evaluation raised against the candidate's own mapping row, found in the evaluator's own work by review before delivery.
9. **This report is a draft** (`status: draft`) and produces no acceptance. A document's status, external adoption, structural freshness and behavioural outcome are four separate facts, and only the third is established here.

## Recovery and continuation

- **Last completed phase:** P6, return. All six phases in scope completed.
- **Frozen input digests still matching:** yes at the time of writing — candidate `61f6ef06…` with a clean worktree, specification `b9dc3a5a…`, validator `e641797` with a clean worktree, binary `835c3263…`.
- **Owned processes and workspace disposition:** none retained. No background process, no worktree allocated, nothing installed, nothing committed. Writes confined to this directory.
- **Conditions invalidating this report:** any change to the candidate package bytes; a new commit touching `providers/` in the architect worktree; a change to `skill-005-devforge-architect.md`; a change to the validator's rubric, runner or graders; a different `devforge` binary; a change to any fixture; or the arrival of native C/B/A evidence, which would supersede the `NOT_RUN` rows rather than amend them.
