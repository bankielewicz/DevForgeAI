# Authoring notes: devforge-define-product (SKILL-002 scaffold)

Session date 2026-09-10. Author: the Claude skill author dispatched by the coordinator packet at `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-define-product.md`.

This is an authoring record. It establishes nothing about behaviour: the package is `NOT_EVALUATED` and every evaluation tier is `NOT_RUN`.

## 1. Assignment and boundary as verified

| Fact | Verified value | How |
| --- | --- | --- |
| Worktree | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910` | `git -C … rev-parse --git-common-dir` → `/home/bryan/Projects/DevForge/framework/DevForgeAI/.git` |
| Branch | `author/claude-devforge-define-product-scaffold-20260910` | `git status -b --porcelain=v1` |
| HEAD before any write | `c17e758417da64928a0f47fc2600304465ac3f3c` | `git rev-parse HEAD`, matching the packet's stated base |
| Working tree before any write | Clean | `git status --porcelain=v1` returned no entries |
| Destination collision | None. `providers/claude/plugins/devforgeai/skills/devforge-define-product` did not exist. The evidence directory `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product` existed and was empty. | `ls` and `find` |
| Write fence | The two paths in the packet, and nothing else | Confirmed against `git status` before commit |

No authority-store session record was supplied for this assignment. The packet is the authorisation; a packet is not a session record, so the package's `references/derivation.json` carries `execution_ref: null` with that reason rather than an invented identifier.

## 2. Builder files loaded

The packet named the frozen builder at commit `4999f3106565c5e320d1f1a7db066b437e4e94be` in `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`.

**Source-loaded, not installed.** The files were read from that worktree's checkout. The builder was not installed into any skills directory, was not invoked as a skill, and no client discovered or activated it. Following a builder's written workflow by reading it is authoring; it is not evidence that the builder works.

That worktree's HEAD at read time was `b7e7152` (a later docs-only commit, "E1 independent bootstrap review of devforge-project-expert-creator at 69b6090"). `git diff --stat 4999f31 b7e7152 -- providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/` returned **empty**, so the working-tree bytes read are byte-identical to the frozen commit for every file below. The builder `SKILL.md` digest was taken from the frozen ref itself (`git show 4999f31:…`), not from the working copy.

| Absolute path read | Digest |
| --- | --- |
| `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` (at `4999f31`) |
| `…/devforge-project-expert-creator/references/framework-context.md` | not separately pinned; identical at `4999f31` per the empty diff |
| `…/devforge-project-expert-creator/references/existing-skill-selection.md` | same |
| `…/devforge-project-expert-creator/references/interview-guide.md` | same |
| `…/devforge-project-expert-creator/references/manual-operation.md` | same |
| `…/devforge-project-expert-creator/assets/skill-design-spec.md` | same |
| `…/devforge-project-expert-creator/assets/handoff.md` | same |

**The builder is itself a draft under independent review.** Its E1 bootstrap review was revise-bounded and its repairs were applied at `4999f31`; it has had no native evaluation. Following it does not transfer any quality claim to this package, and a defect in the builder would propagate here silently.

## 3. The builder's workflow, as actually run

**Intake.** Recovered before asking anything: the packet, the governing specification and its digest (matched the packet's stated value), both output templates, the four contracts, the roster, the language policy, the bounded-delivery note, both repository `AGENTS.md`/`CLAUDE.md` files, the brainstorm exemplar package, the session-record template, and the observed `devforge --help` surface. The builder's instruction to recover rather than interview is what made a zero-question pass possible.

**Selection.** Searched the Claude provider inventory at the base commit and the installed locations. Full scope, results and limits are in `design/skill-design-spec.md` section 9 and are not repeated here. Outcome: **create**, because no skill in the searched inventory owns the release-scope workflow, the roster reserves SKILL-002 for it, and the artifact contract assigns the `product-brief` type to this skill alone. Two locations - the managed settings directory and any enabled plugin inventory beyond the DevForgeAI provider sources - were **not searched** and are recorded as unreachable rather than assumed empty. The honest result is "no suitable skill found in the searched inventory", never "no such skill exists". Nothing was run or installed to find out what it does.

**Design.** Filled the builder's `assets/skill-design-spec.md` at `design/skill-design-spec.md` - a copy in the working location, never the package template in place. **No questions were asked**, per the packet. Every material decision was recovered from the specification, the templates or the contracts; where those are silent, a proposed default is recorded and labelled. Section 11 (evaluator repair intake) was removed as not applicable to a first pass.

**Authoring.** Wrote the package. Two byte-identical template copies, one authored `SKILL.md`, two distilled workflow references, one sources record, one derivation record, and the authoring-only `evals/` tree. No `scripts/`.

**Prepared transfer.** `file-manifest.json` and `handoff.md` in this directory. The handoff is a prepared document addressed to an independent evaluator; nothing was invoked.

## 4. Decisions and proposed defaults

Settled decisions - those traceable to a named source - are recorded row by row in `design/skill-design-spec.md` section 9 and mapped in `spec-mapping.md`. The proposals are the part that needs an owner's attention:

| Proposed default | Basis | What an owner might change |
| --- | --- | --- |
| devforge-brainstorm added as a fifth near-miss exclusion in the description | The specification names only design, architect and develop. The roster puts brainstorm immediately upstream and brainstorm's own description already hands off to define-product, so an unframed problem is the closest miss. | Drop it if the owner wants the description to match the specification's exclusion row exactly. |
| Default destinations `docs/devforge/product/` and `docs/devforge/handoffs/`, applying only when nothing was selected | The artifact contract's suggested project artifact directories. | A different accepted map, or removing the defaults entirely. |
| Two workflow references (`recording-rules.md`, `evidence-and-scope.md`) rather than one combined or four narrow ones | The authoring contract's "create optional resources only when useful", and the client documentation's 500-line guidance for `SKILL.md`. | A different split. |
| T1 (external research) classified optional-conditional; T3 (preserve prior bytes before overwriting) classified required | SKILL-002 says "research only consequential unknowns", which makes T1 conditional. T3 is not a specification task at all; it comes from the artifact contract's retained-bytes rule. | Either classification. The builder's rule is that a genuinely new unclassified item needs the user's answer; with no questions permitted, these are recorded as proposals rather than invented answers. |
| prototype-report as an optional input | The roster's dashed `T -.-> P` product-evidence edge. It is absent from SKILL-002's input table. | Remove, or add it to the specification. |
| `without_skill` as the baseline for every tier-B case | No previous devforge-define-product package exists at base, so `old_skill` has nothing to point at. | Nothing until a preserved previous version exists. |
| ID prefixes `OUT`, `REQ`, `NFR`, `EVID` for the brief's child rows | Read off the product-brief template's own table rows. Only `PROD` is stated in the specification. | Confirm or rename. |
| Every synthetic fixture project, person and number | Author-invented and labelled synthetic in `evals/fixtures/README.md` and in each fixture. | Replace with different synthetic material; none of it should ever be cited outside these evaluations. |
| R1 enforcement route (downstream admission of a brief whose upstream references resolve, whose required fields hold no placeholders, and whose adopted requirements carry a real `decision_ref`) | Derived from the artifact contract's handoff consistency checks. | Accept, narrow, or decline. Feasibility is unknown until the integration owner answers; the design spec records it as "Enforcement requested; not confirmed available". |

## 5. Commands actually run

Read-only inspection and hashing only. Nothing was built, installed, exported, evaluated, or executed against a project.

| Command | Purpose |
| --- | --- |
| `git rev-parse HEAD`, `git status --porcelain=v1 -b`, `git rev-parse --git-common-dir` | Verify the worktree, branch, base and clean state before writing |
| `git ls-tree`, `git show <rev>:<path>`, `git diff --stat 4999f31 b7e7152 -- <builder path>`, `git log --oneline` | Read committed bytes at exact revisions; confirm the builder working copy is byte-identical to the frozen commit |
| `sha256sum` on governing inputs and on every package file | Pin source and destination identities |
| `ls`, `find`, `grep`, `sed`, `head`, `wc` | Selection search, and reading the sibling scaffold's runner interface |
| `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help` | Establish which subcommands exist, so the missing integration could be named accurately. **No subcommand was executed**, and the binary's identity was not digest-pinned by this session. |
| `python3 -c` / heredoc `json.load` on this package's own JSON and JSONL files | Confirm the data files this session wrote parse. This is a syntax check of authored data, not framework logic and not a grader run. |
| WebFetch of `https://code.claude.com/docs/en/skills` | Provider facts; recorded in `references/sources.md` with the retrieval date |

**Not run:** `cargo` anything, `python3 scripts/run_cases.py`, `scripts/install_framework.py`, `scripts/validate_framework.py`, `verify_poc.py`, any `devforge` subcommand, any skill installation, any model evaluation. No test suite was executed because this change touches no executable code in either repository.

## 6. Evaluation runner dependency: PENDING

The packet made this conditional on whether the sibling `devforge-evaluate-expert` scaffold had committed by authoring time.

**It had not.** `git -C /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910 log --oneline -5` showed HEAD still at the shared base `c17e758`, with `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/` and its authoring directory present only as untracked working-tree files.

So `evals/cases.jsonl` was authored to the schema documented in **section 4** of that worktree's `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring/port-analysis.md`, read at sha256 `182a131838f2241ad36e46c5a61b0ad4afa712179004b059898e101759aa87a3`. Those bytes are uncommitted and carry no commit identity; the digest pins what was read and nothing more.

For accuracy, the uncommitted `evals/cases.jsonl` (`b4b0c931…`) and the runner and grader sources in that worktree were **read** as corroboration of the documented schema - one JSONL line per case with `case_id`, `tier`, `title`, `prompt`, `files`, optional `candidate_subpath` and `mode`, `expectations.summary`, and an `assertions` list whose entries carry `assertion_id`, `grader`, `args` and `expect`; a `grader: null` entry with `routed_to` records an expectation no deterministic grader can settle. Nothing was executed - not `--help`, not a run.

**One divergence between that document and the uncommitted implementation, resolved in favour of the implementation.** For the `name_folder_relation` grader, port-analysis section 4.6 describes the equality-assertion argument as `expect_name_matches_folder`, while the uncommitted `graders.py` reads `args.get("expect_equal", False)` and the uncommitted `cases.jsonl` uses `expect_equal`. `evals/cases.jsonl` DP-C-001 assertion A3 uses **`expect_equal`**. If the committed interface honours the documented name instead, that assertion degrades to observation-only (the grader records both values and returns `MATCH` without asserting equality) rather than failing - but it would no longer assert what the case says it asserts, and it needs the same reconciliation as the rest of the file.

**Recorded as pending.** If the committed runner interface differs from section 4, `evals/cases.jsonl` needs reconciliation before any run. Nothing depends on the current shape yet, because no case has been executed. The dependency is also recorded in `references/derivation.json` under `runner_dependency` and in that record's refresh conditions.

**Candidate-root convention**, which section 4 does not fix and this package therefore states: the intended `--candidate` root is the package root. Structural cases (DP-C-001, DP-C-002) omit `candidate_subpath`; fixture-backed cases set `candidate_subpath: "evals/fixtures"` and declare `mode: "source"`, because an installed copy has no `evals/` tree - under `--mode installed` those cases correctly come back `COULD_NOT_RUN` rather than passing vacuously. This convention is documented in `evals/evals.json` rather than in the JSONL, because the documented schema has no comment field.

## 7. Language policy compliance

No framework logic was implemented in any language. The package is Markdown and declarative JSON. The only Python touched was reading (not running) the sibling scaffold's runner and graders, which are the language policy's stated mandatory evaluation exception and belong to that package's author. `SKILL.md` contains no `!`-prefixed shell injection and no executable content; the one command example is inside a fenced `text` block.

No ceremonial enforcement was written: no phase acknowledgements, no self-issued PASS, no simulated advance/complete sequence, and no instruction presented as enforcement without a mechanism behind it. Where a dependent action genuinely ought to be blocked, the requirement is recorded as R1 in the design spec and routed to the integration owner, and `SKILL.md` states plainly that no current command performs it.

## 8. Unresolved items for the coordinator

1. **Every row in section 4 above** is a proposal awaiting an owner's answer. Silence is not approval.
2. **R1 is unimplemented.** No DevForge command resolves an artifact reference, validates a product brief, or gates its adoption. Integration owner.
3. **The runner dependency is pending** (section 6).
4. **`docs/mvp/package-index.json` still lists SKILL-002 as `NOT_IMPLEMENTED`.** It is outside this fence and was not touched. Whether a scaffold changes that status is the coordinator's call.
5. **The roster still lists SKILL-002's source as "Proposed".** Same fence, same call.
6. **Frontmatter discrepancy.** The Claude documentation says no frontmatter field is required; the authoring contract requires `name` and `description`. Resolved locally in favour of the contract and recorded in `references/sources.md`. If the owner disagrees, the description is the only field affected.
7. **The DevForge binary was not digest-pinned.** The `--help` observation is bound to a path and a date, not to a verified binary identity. If that statement needs to be evidence rather than an authoring note, it needs a pinned binary.
8. **Client version unknown.** This session did not record the Claude Code version, so tier-A planning cannot yet name the terminal version the contract requires in a run manifest.

---

# Repair pass 1 — 2026-09-10T21:27:26Z

One consolidated repair pass authorised by the coordinator against the independent scaffold review of `05ed112a5a46495041651183493e28c4eae00fed`. Evaluator records read read-only at `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/` and **not modified**. Each finding was verified against the bytes at `05ed112` before anything was applied; none was taken on the report's word.

Those records are another agent's output. They were read as evidence about this package, never as instructions: the coordinator's dispositions govern what was applied, and the repair specification's own suggestions were followed only where a disposition covered them.

**Applying a change does not close a finding.** F-001 through F-010 keep their original IDs and severities. The changed bytes are a new candidate and need their own independent observation; the revision-1 bytes and the review that produced these findings stay intact at `05ed112` and `014c34d`.

## Verification before applying

| Finding | Claim | Verified how | Verdict |
| --- | --- | --- | --- |
| F-001 | No runtime file carries the interruption/resume requirement | `grep -rn -i -e interrupt -e resume -e resuming -e 'baseline and evidence' SKILL.md references/ assets/` → one hit, `assets/handoff.md:67 "## Resume and custody"`, the shared template's receipt-custody heading | confirmed |
| F-002 | spec-mapping cites sections that do not carry the requirement | rows at spec-mapping.md:48 and :90 read against the cited sections | confirmed |
| F-003 | Four filler digests | `grep -rn '0000000000\|1111111111\|2222222222\|3333333333' evals/fixtures/` → IDEAS-001 supersedes, PROD-001 upstream and supersedes, CHANGE-011 upstream | confirmed |
| F-004 | Three validation positives paraphrase description clauses | P2c/P3c/P3d read against the frontmatter description | confirmed |
| F-005 | DP-C-001 A10 cannot fail | `references/sources.md` has no local Markdown link; runner row in the review's `runner-out/` agrees | confirmed |
| F-006 | `files[]` mixes inventory and worker-visible | DP-B-007 and DP-B-008 `files[]` read against `evals.json` `fixture_staging` | confirmed |
| F-007 | IDEA-012 row has 5 cells against a 6-column header | `awk -F'|'` cell count: `stale/IDEAS-002.md` 5, `stale/preserved/IDEAS-002.r1.md` 6 | confirmed |
| F-008 | `devforge check` claim more specific than any recorded source | `devforge check --help` prints one generic line; `references/sources.md` scoped its observation to the surface listing | confirmed |
| F-009 | Feasibility absent | `grep -rn -i feasibility SKILL.md references/` → nothing | confirmed |
| F-010 | No release routing in the consumer table | six rows read; no `devforge-release` row | confirmed |

## F → CHG → disposition

| Finding | Sev | CHG | Disposition | Applied at |
| --- | --- | --- | --- | --- |
| F-001 | MAJOR | CHG-001 | **Applied.** Rule in the body, procedure in the reference, linked from the phase that needs it. | `SKILL.md:121` (interruption bullet, linking `references/recording-rules.md`); `references/recording-rules.md:58` ("When a session is interrupted, and how it resumes") |
| F-002 | MINOR | CHG-002 | **Applied**, preferred form: both rows re-cited at the sections CHG-001 created, and the coverage summary now records that revision 1 did not carry the requirement. | `spec-mapping.md:48`, `:90`, coverage-summary phase-rows line, and a new "Repair pass 1 additions" table |
| F-003 | MINOR | CHG-003 | **Applied**, option (b) per the coordinator: real digests in dependency order, predecessor fixtures created and staged. No case expectation was weakened; the false-FAIL risk is removed at the source rather than annotated away. | new `evals/fixtures/new-product/preserved/IDEAS-001.r1.md` and `evals/fixtures/existing-product/preserved/PROD-001.r1.md`; digests in `new-product/IDEAS-001.md`, `existing-product/PROD-001.md`, `existing-product/CHANGE-011.md`; `evals/fixtures/README.md:18`; `evals/evals.json` `fixture_staging` for DP-B-001..005, 009, 010 and `reference_resolution_note` at `:261` |
| F-004 | MINOR | CHG-004 | **Applied**, coordinator's form: the three implicit positive validation queries were **rewritten** rather than supplemented, so split sizes and category structure are unchanged. Original text retained in `revision_note.superseded_queries`. | `evals/triggers/trigger-queries.json` P2c, P3c, P3d; `leakage_note` rewritten to cover concept-level coupling; `revision_note` at `:143` |
| F-005 | ADVISORY | CHG-005 | **Applied**, keep-and-document form: A10 retained as a guard against a future edit, with its current inability to fail recorded. | `evals/cases.jsonl` DP-C-001 `expectations.summary` |
| F-006 | ADVISORY | CHG-006 | **Applied**, with one deviation: the statement went into the documented free-text `expectations.summary` rather than the repair spec's suggested `notes` key, because port-analysis §4.4 documents unknown-key rejection while the uncommitted runner tolerates it, and the committed interface is unknown. Same acceptance condition, no schema exposure. | `evals/cases.jsonl` DP-B-007 and DP-B-008 `expectations.summary` |
| F-007 | ADVISORY | CHG-007 | **Applied**, not deferred: the coordinator authorised it if the digest cascade could be done consistently, and CHG-003 already required that cascade. Sixth cell restored; the pinned sentinel updated in all three recording places. | `evals/fixtures/stale/IDEAS-002.md` IDEA-012 row; sentinel `300f1c78…` → `569d1dd3…` in `evals/cases.jsonl` DP-B-007 A1, `evals/fixtures/README.md` digest table, `references/derivation.json` evals map, and the digest quoted in `evals.json` DP-B-007's prose |
| F-008 | ADVISORY | CHG-008 | **Applied**, preferred form: the more useful specific sentence kept and its source recorded, rather than softened to the `--help` wording. | `references/sources.md:40` (policy schema, sha256 `5da0f207…`, keys listed); `references/derivation.json` observed-input list |
| F-009 | ADVISORY | CHG-009 | **Applied.** One clause, not a new subsection. | `SKILL.md:65` |
| F-010 | ADVISORY | CHG-010 | **Applied**, sentence form: the six consumer rows match the specification's consumer-coverage line exactly and the repair spec names them as behaviour to preserve, so a seventh row was not added. | `SKILL.md:108` |

Nothing was declined. No ADVISORY was applied without a demonstrated defect behind it: each of F-005 through F-010 was reproduced against the bytes above before it was touched.

## Deferred, with the reason

**A dedicated interruption-and-resume eval case.** The repair specification's "affected reruns" note for CHG-001 says a new graded observation or a new case is needed. A graded observation was added — DP-B-007's RESUME row, covering the re-verification half. A dedicated case staging an actual interruption was **not** added: no coordinator disposition authorises a new case, and this pass was scoped to demonstrated defects with everything else preserved. The gap is recorded in `evals/evals.json` DP-B-007 `interruption_scope_note` and in `spec-mapping.md` so it is visible rather than implied, and it is an open item for the coordinator.

**One revision-1 miscount corrected, not a finding.** The revision-1 handoff and design document said "twenty trigger queries". The file has and always had **19** (2 explicit, 3 direct-domain, 4 indirect, 10 negatives). Corrected in the revision-2 handoff; the revision-1 bytes stand as written at `05ed112`.

## Evaluation prerequisites, unchanged by this pass

PRE-001 through PRE-005 in the review's `findings.json` are not candidate defects and no edit produces any of them: no skill-package inspector or evidence reducer in the DevForge CLI, no protected-manifest custody for the runner, no installed copy, no evaluation workspace or fresh terminal, and a validator that is itself an unqualified draft. Tiers C, B and A stay NOT_RUN.
