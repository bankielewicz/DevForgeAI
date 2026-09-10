# SKILL-004 requirement mapping — devforge-prototype

Every row of `docs/mvp/specifications/skill-004-devforge-prototype.md` (revision 2, sha256 `e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c`) mapped to the file and section that carries it and, where a case exists, to its eval identifier.

Paths are relative to `providers/claude/plugins/devforgeai/skills/devforge-prototype/`. `XB-n` is a tier-B case id in `evals/evals.json`; `XP-*` is a deterministic case id in `evals/cases.jsonl`; `A*` is a query id in `evals/triggers/trigger-queries.json`.

A mapping shows which requirement was addressed where. It is not evidence that the addressing works.

## User goal and use-case inventory

| Spec row | Carried by | Cases |
|---|---|---|
| User goal — bounded experiment, recorded result, explicit disposition of prototype code | `SKILL.md` opening; phases 1 and 4; `references/experiment-boundaries.md` "Disposition of the prototype code" | XB-1, XB-4 |
| Direct request — "prototype the risky part before we commit" | `SKILL.md` frontmatter description, direct clause | XB-1, A2a |
| Indirect request — "Can this approach support the interaction or performance we need?" | description, indirect clause; `SKILL.md` phase 1 | XB-2, A3a, A3b |
| Expected result — experiment-plan; prototype-report plus a standardized handoff | `SKILL.md` phases 1 and 4; `assets/experiment-plan.md`, `assets/prototype-report.md`, `assets/handoff.md` | XB-1, XP-C-001 |
| Required context — concrete uncertainty, relevant drafts or accepted constraints, permitted workspace | `SKILL.md` "Required inputs" table | XB-1, XB-2 |
| Plugin capability — approved local runtime tools, no model API service | `references/framework-context.md` "What the CLI actually offers"; frontmatter carries no `allowed-tools`; `references/sources.md` states this explicitly | — |
| State/action boundary — cannot silently become production code or override an accepted architecture decision | `SKILL.md` failure mode 2 and phase 4; `references/experiment-boundaries.md` disposition table | XB-4, XP-C-006 |
| MVP support decision — conditional; skip when inspection or existing evidence resolves it | description closing clause; `SKILL.md` phase 1 "if it is sufficient, that is the correct answer" | A7a, A7b |
| Does not activate for — a fully specified production behaviour belongs to develop | description exclusion 1; `SKILL.md` is silent by design, the routing lives in the description | XB-5, XP-A-001, A4a, A4b |

## Inputs and provenance

| Spec row | Carried by | Cases |
|---|---|---|
| product-brief / design-spec / architecture-contract — at least one; identify the uncertain requirement and whether its source is draft or accepted | `SKILL.md` inputs table row 1; `references/recording-rules.md` "Upstream references" | XB-1, XB-7 |
| Experiment constraints — required; permitted paths, tools, time/resource bound, observable measures | inputs table row 3; `references/experiment-boundaries.md` "The fence" | XB-2, XB-11 |
| prototype-report — optional; earlier experiment and what this iteration changes | inputs table row 4 | XB-10 |
| Artifact contract — exact revisions, hashes, stable section IDs, decisions, source evidence | `references/recording-rules.md` "The envelope" and "Digests, and the order of the writes" | XB-7 |
| A proposed source cannot become an accepted production constraint by being copied downstream | `SKILL.md` inputs note; `references/recording-rules.md` draft-versus-accepted paragraph | XB-1, XB-7 |
| Reuse valid current artifacts rather than replaying earlier phases | `references/recording-rules.md` "Upstream references", final paragraph | — |
| Execution contract — owner and fence per session; distinct worktrees and branches | `SKILL.md` inputs table row 5; `references/experiment-boundaries.md` "Concurrency and ownership" | XB-6 |

## Workflow and phase exits

| Phase | Work carried by | Exit condition carried by | Cases |
|---|---|---|---|
| 1. Specify | `SKILL.md` §1 | "the plan exists, and it exists before its measurements and its result are known" | XB-1, XB-2, XP-C-001 |
| 2. Build | `SKILL.md` §2 | "prototype files and reproduction steps are identified, and nothing was written outside the fence" | XP-C-002, XP-C-006 |
| 3. Observe | `SKILL.md` §3 | "every planned case carries an observation, a failure, or an explicit unavailability with its cause" | XB-3, XB-9, XP-A-002 |
| 4. Decide | `SKILL.md` §4 | "the report separates observation from recommendation, names the exact prototype identity and the limits of what was measured, and states a disposition whose adoption is still the user's" | XB-4, XP-B-001 |
| Phases are not CLI subcommands; only documented, implemented commands may be named as gates | `SKILL.md` closing line of §4; `references/framework-context.md` CLI table and missing-integration list | — |
| On interruption, preserve the current phase and evidence; resume by rechecking identities and the assignment | `references/experiment-boundaries.md` "Stopping", final paragraph | XB-6 |

## Outputs and standardized templates

| Spec row | Carried by | Cases |
|---|---|---|
| experiment-plan, prefix XPLAN, hypothesis / measurement method / constraints / stop conditions before execution | `assets/experiment-plan.md` (byte-identical copy); `references/recording-rules.md` "Filling the plan" | XB-1, XB-10 |
| prototype-report, prefix XREPORT, observed results / exact prototype identity / limitations / disposition | `assets/prototype-report.md` (byte-identical copy); `references/recording-rules.md` "Filling the report" | XB-4, XP-C-001, XP-C-004 |
| Consumer coverage — experiment-plan to prototype and review; prototype-report to define-product, design, architect, plan, change | `assets/handoff.md` "Continuation directory" paragraph | XB-4 |
| Every result includes a handoff with output identities, observed checks, unresolved decisions, next owner, one copyable task | `assets/handoff.md` throughout | XB-1 |
| Follow an existing authorized continuation; a handoff recommendation is not authority for unrelated external actions | `assets/handoff.md` closing line | XB-11 |

## Validation and behavioral acceptance

| Spec case | Required observation | Carried by | Eval |
|---|---|---|---|
| Direct activation | Creates a plan, prototype and result tied to the original uncertainty | `SKILL.md` §1–§4 | **XB-1** |
| Indirect activation | Defines a measurement before claiming a result | `SKILL.md` §1 | **XB-2** |
| Unavailable runtime | Records COULD_NOT_RUN and makes no performance claim | `SKILL.md` §3 and "When something is missing"; `references/experiment-boundaries.md` "When a measurement cannot be taken" | **XB-3** |
| Failed hypothesis | Preserves the failure and recommends a revision rather than moving the threshold | `SKILL.md` §4 and failure mode 1; `references/experiment-boundaries.md` "Measurement before result" | **XB-4**, XP-B-001 |
| Out of scope | Routes to develop | description exclusion 1 | **XB-5**, XP-A-001 |

## Additional common cases

| Spec case | Carried by | Eval |
|---|---|---|
| A concurrent writer claims this session's worktree or branch — stop dependent writes, report without deleting or resetting | `SKILL.md` "When something is missing", bullet 3; `references/experiment-boundaries.md` "Concurrency and ownership" | **XB-6** |
| A relevant upstream revision, installed skill, base commit or candidate changes — mark prior evidence stale, route a new check | `SKILL.md` bullet 2; `references/recording-rules.md` "When the upstream has moved on" | **XB-7** |
| A template placeholder remains in a required result field — the result stays a draft | `SKILL.md` bullet 4; `references/recording-rules.md` "Placeholders" | **XB-8**, XP-C-004 |
| A requested check cannot execute — record COULD_NOT_RUN and its actual cause; absence of an error is not PASS | `SKILL.md` bullet 5; `references/experiment-boundaries.md` "When a measurement cannot be taken" | **XB-9**, XP-C-005, XP-A-002 |
| Acceptance requires real outputs from representative requests in each terminal claimed | `evals/evals.json` `execution_boundary`; nothing in the package claims a terminal observation | all NOT_RUN |

## Rework, stopping, and recovery

| Spec item | Carried by | Eval |
|---|---|---|
| A new hypothesis or changed threshold requires a new plan revision | `references/experiment-boundaries.md` "Measurement before result", second paragraph | **XB-10** |
| Findings return to the owning product/design/architecture skill; production adoption becomes a planned story | `SKILL.md` §4; `references/experiment-boundaries.md` disposition table | XB-4 |
| Stop at the resource bound or when the work needs authority beyond the declared fence; preserve partial observations | `SKILL.md` "Stopping"; `references/experiment-boundaries.md` "The fence" and "Stopping" | **XB-11** |
| Preserve accepted versions and observed failures; do not force-unlock, overwrite another session's result, change external gates, or retry indefinitely | `SKILL.md` bullet 3; `references/experiment-boundaries.md` "Concurrency and ownership" and "Stopping" | XB-6 |
| If the worktree or active run changes, re-establish the baseline before resuming | `references/experiment-boundaries.md` "Stopping", final paragraph | XB-7 |

## Native creator authoring prompt

| Spec instruction | How it was followed |
|---|---|
| Use the operator-supplied worktree, provider, write fence and base | Worktree, branch and base verified before writing; fence honoured — `git status` confirms no file outside it was touched |
| Read skill-authoring-contract.md at the selected revision | Read at base; digest in `references/derivation.json` |
| Create or improve devforge-prototype to satisfy SKILL-004 | Created; no prior package existed |
| Read this specification, its named templates, and only the relevant sections of the shared contracts | Sections actually used are recorded per-derivation in `references/derivation.json` |
| A focused skill in the assigned provider source, its needed runtime resources, reproducible eval cases/fixtures, separate A/B/C observations | Package as authored; A/B/C reported separately and all `NOT_RUN` |
| Record the real installation mode and candidate/baseline identities | No installation was performed; recorded as such. No baseline existed |
| Do not claim implicit activation from a run explicitly supplied SKILL.md | `evals/evals.json` `tier_note` states tier B can never evidence activation; explicit-invocation trigger entries are recorded separately |
| Preserve user scope and existing approval; keep DevForge authority external; respect the assigned worktree; report unavailable checks truthfully | No gate, policy or sibling was modified; the only command named in the package is `devforge isolate`, with its actual limit stated |
| Move lengthy conditional procedures into references; keep the trigger description precise; use scripts only for real deterministic operations | Three references carry the conditional material; no `scripts/` was authored |
| Copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path | Both output templates and the shared handoff are in `assets/`; all seven local links verified to resolve inside the package; no `docs/mvp` path and no developer home path appears in the package |

## Completion handoff

| Spec item | Carried by |
|---|---|
| Completion means the specified artifacts exist, declared inputs resolve, required observations are recorded, the next task is explicit | `SKILL.md` "Stopping" |
| A document's accepted status and an external gate's passing result are separate facts | `references/framework-context.md` "Result vocabulary"; `references/recording-rules.md` `status` and `decision_ref` rows |

## Coverage summary

Every SKILL-004 acceptance row and every additional common case has a tier-B eval case. Nine of the eleven cases also have at least one deterministic assertion, and two spec behaviours — threshold integrity (XP-B-001) and the semantic reading of an untrusted embedded instruction — are deliberately left with no deterministic grader and routed to independent review rather than approximated by one.

No case has been executed. Tiers A, B and C are `NOT_RUN`.
