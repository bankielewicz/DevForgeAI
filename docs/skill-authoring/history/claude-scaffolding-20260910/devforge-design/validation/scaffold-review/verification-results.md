---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-devforge-design-scaffold-20260910"
artifact_type: "expert-evaluation-report"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T20:18:54Z"
producer:
  skill: "devforge-evaluate-expert (source-loaded, not installed)"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac (sha256 of the SKILL.md blob at claude-scaffold-evaluate-expert-20260910 commit e641797eebf04cd1e8eb9f711549e038e7745407; its bytes were read with git show and by absolute path, not loaded by a client)"
execution_ref: null
upstream:
  - artifact_id: "SKILL-003"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-003-devforge-design.md"
    sha256: "4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
      - "Native creator authoring prompt"
      - "Completion handoff"
  - artifact_id: "CANDIDATE-devforge-design"
    revision: "9ad38de25a9941eb8ed67e9650430879f62032e4"
    store: project
    path: "providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md"
    sha256: "65dbb586ab78a43fa2b83a7e9c35f20272b3d4181ba08e6cc7519876de0e4c83"
    sections:
      - "whole package, 23 files; per-file manifest in commands.log"
evidence:
  - path: "validation-plan.json"
    sha256: "3670bdb08f9a4fafaa4e875ab84e87d5c7a71c90da5769c441d7eaf0916b94d7"
  - path: "validation-results.json"
    sha256: "30ec3e3827773ff2e0aa42d4eccaa71cfd38caa6dfd105818851d577c9cc4a85"
  - path: "ai-review.json"
    sha256: "56d7d52474bbf05202ded00d46136c0ead6114a2c85bf07a4ae84f486e1218a1"
  - path: "findings.json"
    sha256: "d274779599f18e4aa24becffc7967c8bb9ff4a8a9f6517be2e83aa5d10dc5030"
  - path: "runner-out/run1-packageroot-source.jsonl"
    sha256: "0fd3f2d2c380efeb57020359773def19c45456a25395587ea7f6e7bf1f853e8b"
  - path: "runner-out/run2-fixtures-source.jsonl"
    sha256: "fd34f00c3363ad259efce0b0367a728590d8001b720fa683affcd7769a3db68a"
  - path: "runner-out/run3-packageroot-installedmode.jsonl"
    sha256: "795a0c39d9cc38dbc6caa3a1c7ac7928eb4e2f84705a74bd4eb65616f173ecde"
  - path: "runner-out/run4-supplementary-source.jsonl"
    sha256: "dd70cebf695054bd711bdee262ebed9af8881385a73acf26dddec8fab03eecc8"
  - path: "runner-out/run5-nested-field-probe.jsonl"
    sha256: "2a498e50a8473d4cd504d9fe971ee6657bf5ad6e0f6e5b61482f216dcd1362e0"
  - path: "runner-out/evaluator-supplementary-cases.jsonl"
    sha256: "65d98620a5a7f3016103370f01911d88c3f40ef8e1939f3d84be74511146f7e2"
  - path: "runner-out/evaluator-nested-field-probe.jsonl"
    sha256: "15b6fe98884db255b2582c6805f73a4248a7ccc96c1d30cbf6a7c9712249ce69"
  - path: "commands.log"
    note: "every command this evaluation ran, with its output; hashed after the evaluation closes"
supersedes: null
decision_ref: null
missing_inputs:
  - "Session assignment record: none exists. The evaluation scope came from the operator task packet at /home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/evaluator-devforge-design.md, which is not a devforge.artifact session record, so execution_ref is null. Its absence does not establish that this evaluator owns the destination."
  - "Installed or exported copy of the candidate: not generated, and none was to be generated under this assignment. Blocks tier C."
  - "Fresh terminal, isolated workspace and per-attempt client-state isolation: not allocated. Blocks tiers A and B."
  - "Claude Code client version and model configuration: not observable from inside this session; recorded as unknown rather than inferred."
---

# Skill verification results: devforge-design (SKILL-003), Claude scaffold

This is an independent scaffold evaluation. The evaluator did not author the candidate. It inspects and measures; it does not accept, adopt, install or release anything, and it made no edit to the candidate, its specification, its cases or its expectations.

`validation-results.json` holds the machine-readable per-check outcomes and is referenced here rather than restated. `findings.json` holds the full finding records.

## Identity and scope

- **Evaluation plan:** `validation-plan.json`, sha256 `3670bdb08f9a4fafaa4e875ab84e87d5c7a71c90da5769c441d7eaf0916b94d7`. It records a sequencing deviation: the packet fixed the scope and the frozen identities before any observation and `commands.log` is the contemporaneous freeze record, but the plan file itself was serialized after the deterministic runs. No expectation was chosen or altered after seeing an outcome.
- **Candidate source identity:** worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910` at commit `9ad38de25a9941eb8ed67e9650430879f62032e4`, package `providers/claude/plugins/devforgeai/skills/devforge-design`, 23 files. `SKILL.md` sha256 `65dbb586ab78a43fa2b83a7e9c35f20272b3d4181ba08e6cc7519876de0e4c83`. HEAD equals the packet's frozen commit, `git diff 9ad38de HEAD -- providers/` is empty, and the only untracked path in the worktree is this evaluation's own output fence. The complete 23-file path-to-digest manifest was computed independently by this evaluator and appears in `commands.log`; it is identical, 23 of 23, to the author's `file-manifest.json`.
- **Installed candidate identity:** **not installed.** `file-manifest.json` records `installed_copy: "not generated"` and `plugin_export: "not generated"`, and no install or export was to be attempted under this assignment.
- **Specification:** `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-003-devforge-design.md`, sha256 `4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb`, matching the digest the packet declared.
- **Validator followed:** the Claude `devforge-evaluate-expert` package, **source-loaded** by absolute path from worktree `claude-scaffold-evaluate-expert-20260910` at commit `e641797eebf04cd1e8eb9f711549e038e7745407` (`SKILL.md` sha256 `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac`). It was not installed, not discovered and not invoked by a client. **That validator is itself a draft under bootstrap review** (E2: revise → repaired at `e101e76` → recheck pending), so its rubric anchors, its runner interface and its report templates may change; this report's criterion outcomes are bound to the `e641797` anchors.
- **Baseline:** `without_skill`. No Claude `devforge-design` existed at the base revision `c17e758417da64928a0f47fc2600304465ac3f3c`, so there is no preserved previous revision. The baseline arm is `NOT_RUN` because no native run was allocated, and a missing arm supports no improvement claim.
- **Client, version and model configuration:** unknown. No version probe is available from inside this session. Client facts about Claude skills were taken from `https://code.claude.com/docs/en/skills`, retrieved by this evaluator on **2026-09-10 UTC**.
- **Assignment and write fence:** writes confined to `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/` inside the candidate worktree. Nothing was committed. Nothing outside the fence was written, moved, reset or cleaned.
- **Independence conditions actually met:** a separately dispatched evaluator context that never authored, edited or advised on the candidate. Criterion records R01–R10 were drafted and `ai-review.json` was written **before** any file under the author's `authoring/` directory was opened; `spec-mapping.md` was read afterwards only to verify its claims against bytes, and no author-preferred grade was adopted. **Not** separated: filesystem, process space and host, which are shared with the candidate worktree and with other concurrent sessions. The evaluator read the candidate's own `evals/` including its expectations, so it is not blind to the author's intended outcomes.
- **Scope of this evaluation:** phases P1, P2, P3, P5 and P6. P4 (tiers C, B, A) is `NOT_RUN` with its cause. This is a static and deterministic evaluation of authored bytes. **It establishes nothing about whether a session finds this skill, loads it, or produces a better design with it.**

## Evidence groups and outcomes

Reported separately. Not merged into any figure.

| Group | Observations | Outcome | Evidence | Limits |
| --- | --- | --- | --- | --- |
| Intake and freeze | Candidate, specification, validator, ten governing inputs and the CLI surface frozen and re-verified by digest | PASS | `commands.log`; `validation-plan.json` | Plan file serialized after the runs; the freeze record is contemporaneous |
| Structure (manual observation) | 10 checks: frontmatter, name/folder, link resolution, runtime independence, derivation-vs-bytes, evals resolution, trigger split, case-file validity, specification coverage, authority boundaries | **9 PASS, 1 FAIL** (`CHK-SPEC-01`) | `validation-results.json`; `runner-out/` | Method `INSPECTION_MANUAL`; authority: none. A hash match proves byte identity, never that a flow is any good |
| Independent review R01–R10 | All ten applicable and reviewed against the frozen rubric | **9 PASS, 1 FAIL** (R04) | `ai-review.json` | Static reading. A static PASS does not establish that a session will follow the instructions |
| Tier C installed resources | evals.json id 1 / `DX-C-001` | NOT_RUN | — | No installed or exported copy exists; none was to be generated (F-012) |
| Tier B output quality | evals.json ids 2–10, both arms | NOT_RUN | — | No native run allocated; the `without_skill` arm was not executed (F-012) |
| Tier A discovery and activation | 23 trigger queries | NOT_RUN | — | No fresh terminal, no installed package to discover, no per-attempt client-state isolation (F-012) |

## Checks run, with commands

Every command and its output is in `commands.log`. The runner is the validator package's `scripts/run_cases.py` at `e641797`, invoked through `/usr/bin/python3 -B` (3.12.3), standard library only, with `--out` inside this fence. **These are local, non-isolated observations made in the evaluator's ordinary session. They are not native evidence and they do not close either missing-capability dependency.**

| # | What was checked | Command shape | Result |
| --- | --- | --- | --- |
| 1 | Candidate frozen identity | `git rev-parse HEAD`; `git diff 9ad38de HEAD --stat -- providers/`; `find … \| xargs sha256sum` | HEAD = `9ad38de`; diff empty; 23-file manifest recorded |
| 2 | Validator frozen identity | `git show e641797:…/SKILL.md \| sha256sum` | `bdf665c7…` |
| 3 | Template copies vs governing sources | `cmp` ×2 | Both exit 0 — byte-identical |
| 4 | All 13 declared derivation sources at the pinned revision | `git show c17e758:<path> \| sha256sum` ×13 | 13/13 identical to the digests `derivation.json` records |
| 5 | DevForge CLI surface | `devforge --help`, `devforge check --help`, `devforge expert --help` | Surface matches `SKILL.md`'s claim exactly |
| 6 | Claude client facts | WebFetch `https://code.claude.com/docs/en/skills` | All seven claims in `references/sources.md` match the retrieved page |
| 7 | evals resolution and cross-reference | Python, stdlib | 24/24 `files[]` entries (12 in `evals.json`, 12 in `cases.jsonl`) exist inside `evals/`; 9/9 subpaths exist; 10/10 `deterministic_cases` ids resolve; no orphans |
| 8 | Trigger split | Python, stdlib | 23 queries, no duplicate ids, 8 categories each with train and validation entries |
| 9 | Held-out leakage | `grep -rniE` over `SKILL.md`, `references/`, `assets/` | No fixture token and no validation-split phrase in any runtime-shipped file |
| 10 | Author manifest verification | Python, stdlib | 23/23 declared digests identical to the evaluator's own; `file_count` correct |
| 11 | Candidate cases, package root, `--mode source` | `run_cases.py --cases <pkg>/evals/cases.jsonl --candidate <pkg> --out runner-out/run1-…` | exit 0; **9 of 10 cases COULD_NOT_RUN** — see F-005 |
| 12 | Candidate cases, fixtures root, `--mode source`, 9 selected | `… --candidate <pkg>/evals/fixtures --out runner-out/run2-…` | exit 0; 9 COMPLETED |
| 13 | `DX-C-001`, package root, `--mode installed` | `… --candidate <pkg> --mode installed --case-id DX-C-001 --out runner-out/run3-…` | exit 0; COMPLETED |
| 14 | Evaluator-added structural cases | `… --cases runner-out/evaluator-supplementary-cases.jsonl --candidate <pkg> --out runner-out/run4-…` | exit 0; 6 COMPLETED |
| 15 | Evaluator grader probe (nested envelope key) | `… --cases runner-out/evaluator-nested-field-probe.jsonl --candidate <pkg>/evals/fixtures --out runner-out/run5-…` | exit 0; COMPLETED |

**The DevForge CLI has no skill-package structural-inspection capability.** No command above is a structural gate, none was presented as one, and none exists to be run. Every structural row here was obtained by reading.

## Runner observations

`MATCH` / `MISMATCH` / `INDETERMINATE` are the runner's own vocabulary. They are rows cited while adjudicating, never outcomes copied into a result. Exit status describes the program, not the candidate; all five runs exited 0.

| Run | Case | Assertion | Grader | Result | Observed |
| --- | --- | --- | --- | --- | --- |
| run1 | `DX-C-001` | A1–A8 | various | INDETERMINATE ×8 | case declares `mode: installed`, run used `source` |
| run1 | 9 other cases | — | — | case `COULD_NOT_RUN` ×9 | `candidate_subpath '<name>' does not resolve to a directory inside the candidate root` |
| run2 | `DX-B-002/003/005/006/010` | A1 (each) | none | INDETERMINATE ×5 | `no-deterministic-grader`, routed to independent review |
| run2 | `DX-B-004` | A1 | `claim_evidence_binding` | **MISMATCH** | `claimed='PASS' evidence=none` — the intended discriminating result |
| run2 | `DX-B-004` | A2 | none | INDETERMINATE | routed to independent review |
| run2 | `DX-B-007` | A1 | `artifact_side_effect` | MATCH | 1 sentinel unchanged (`sentinel/UX-004.md` = `cf0e9f8d…`, matching the digest the case hard-codes) |
| run2 | `DX-B-008` | A1 | `path_present` | MATCH | `preserved/PROD-001.r2.md` present |
| run2 | `DX-B-008` | A2 | `artifact_side_effect` | MATCH | 1 sentinel unchanged (`b863996b…`, matching the case's digest) |
| run2 | `DX-C-009` | A1 | `required_report_fields` | **MISMATCH** | `placeholder`: `created_at_utc` (line 8), `execution_ref` (line 12) — the intended discriminating result |
| run3 | `DX-C-001` | A1 | `frontmatter_present` | MATCH | opening and closing `---` present |
| run3 | `DX-C-001` | A2 | `frontmatter_fields` | MATCH | `description,name` populated |
| run3 | `DX-C-001` | A3 | `package_relative_links` | MATCH | `SKILL.md`: 4 local, 0 external, all resolve |
| run3 | `DX-C-001` | A4 | `package_relative_links` | MATCH | `recording-rules.md`: 1 local, resolves |
| run3 | `DX-C-001` | A5 | `package_relative_links` | MATCH | `mockups-and-preview.md`: **0 local, 0 external** — vacuous, see F-010 |
| run3 | `DX-C-001` | A6, A7 | `path_present` | MATCH ×2 | both `assets/` templates present |
| run3 | `DX-C-001` | A8 | `path_absent` | **MISMATCH** | `evals` present. **Expected and correct for a source tree** — the authoring contract keeps `evals/` in source and strips it on install. This is an evaluation condition (no installed copy), not a candidate defect |
| run4 | `SUP-S-001` | A1 | `name_folder_relation` (`expect_equal`) | MATCH | `name='devforge-design' folder='devforge-design'` |
| run4 | `SUP-S-002` | A1–A4 | `package_relative_links` | MATCH ×4 | `sources.md`, both assets, fixtures README: 0 local links each, none unresolved |
| run4 | `SUP-S-003` | A1–A8 | `path_present` | MATCH ×8 | all four references, all three evals files, and `evals/` itself present |
| run4 | `SUP-S-004` | A1, A2 | `required_report_fields` | MISMATCH ×2 | `placeholder`: `artifact_id`, `created_at_utc`, `execution_ref` in both templates. **Expected** — a blank source template is supposed to hold placeholders |
| run4 | `SUP-S-005` | A1–A3 | `artifact_side_effect` | MATCH ×3 | no backtick-bang syntax, no bang-fence, no `docs/mvp/`, no `/home/` in `SKILL.md` or either reference |
| run4 | `SUP-S-006` | A1 | `artifact_side_effect` | MATCH | both shipped templates hash to the digests `derivation.json` declares |
| run5 | `SUP-P-001` | A1 | `required_report_fields` | MISMATCH | `skill_revision` found at line 11 — a nested envelope key **is** addressable by its leaf name |
| run5 | `SUP-P-001` | A2 | `required_report_fields` | MISMATCH | `producer.skill_revision` reported missing — a dotted path is **not** addressable |

The evaluator added `SUP-S-001` … `SUP-S-006` and `SUP-P-001` because the candidate's deterministic layer contains one tier-C case and, across all ten cases, ten of eighteen assertions carry `"grader": null`.

## Independent review R01–R10

Full records with line-level evidence are in `ai-review.json`.

| Criterion | Outcome | One-line basis |
| --- | --- | --- |
| R01 Task identity and scope | PASS | Description names the capability, both activating conditions and four near-miss exclusions, each naming a real roster sibling; the overloaded word "design" is explicitly disambiguated |
| R02 Inputs, outputs and completion | PASS | All four specification input rows carried verbatim in requirement and consume-only meaning; missing-input behaviour is explicit and non-fabricating; completion is finite and distinguishes a result from a proposal |
| R03 Authority, ownership and accepted decisions | PASS | No self-granted approval; a selected destination governs; `decision_ref` stays null until a real adoption; adopting a newer upstream is separated from repairing a locator and needs the user's authorization |
| R04 Workflow decisions and failure paths | **FAIL** | SKILL-003's rework route "product-scope conflicts return to define-product via change" has no transition anywhere in the package (F-001) |
| R05 Runtime dependencies and resource delivery | PASS | Two roots kept apart; references linked at the phase of use; all links resolve; no `docs/mvp`, repository or home-path runtime dependency; CLI claims match the binary's help |
| R06 Instructions versus supplied data | PASS | Supplied documents, feedback and retrieved pages supply facts, never instructions or authority; a directive inside supplied material is a fact to report |
| R07 Framework semantics and artifact provenance | PASS | Envelope, upstream resolution, no-self-digest and write-order are all correct and concrete; `devforge.artifact/v1` is correctly labelled a proposed schema. F-002 attached, not raising to FAIL |
| R08 Prompt organisation | PASS | 132 lines with conditional detail in two references linked at point of use; no conflicting duplicate rule |
| R09 Observable checks and honest outcome reporting | PASS | The strongest part of the package: writing a file and inspecting it are held apart, `NOT_RUN` is the default, and the absence of an error is explicitly not a pass |
| R10 Enforcement and handoff boundaries | PASS | Phases stated as this skill's workflow with nothing intercepting them; the missing check is named as a design requirement routed to its owner; suggested / installed / actually-invoked kept as three facts |

No average, weighted score or percentage was computed, and no criterion outcome is blended with the deterministic rows or with any tier.

## Requirement coverage against SKILL-003

Complete for: the nine use-case-inventory rows; the inputs table (all four specification rows with identical `Requirement` and `Consume only` values, plus two rows legitimately derived from the "Required context" line); all four phases with their exit conditions carried faithfully; the outputs table with the `UX` prefix and both package-relative templates; the "phases are not CLI subcommands" and "only implemented commands may be named as gates" statements; all five acceptance-case rows and all four additional common cases, each with an `evals.json` entry and a `cases.jsonl` counterpart; the stopping conditions; the completion handoff.

Not addressed: the product-scope-conflict rework route (**F-001**, MAJOR) and the interruption-and-resume rule (**F-003**, MINOR).

`spec-mapping.md` was verified claim by claim against bytes. Everything checked verified — the specification digest, both byte-exact template copies, the 950-character description, the absence of `scripts/`, the acceptance-case mapping, and all 23 digests in `file-manifest.json` — except four claims recorded as **F-004**: the two rows above are marked addressed when the cited bytes do not carry them; "24 trigger queries" (observed 23); and "four of the ten carry a deterministic grader … six route entirely to independent review" (observed five and five, contradicted by `spec-mapping.md`'s own table two sections earlier).

## Findings

Full records in `findings.json`. Severity is chosen from the demonstrated consequence.

| ID | Type | Severity | Requirement | Evidence | Demonstrated impact | Smallest repair |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | defect | **MAJOR** | SKILL-003 Rework: "Product-scope conflicts return to define-product via change" | `SKILL.md:85-91`, `:106-115`, `:123-131`; grep in `commands.log`; `ai-review.json` R04 | A session that finds mid-workflow that a requested flow contradicts an accepted requirement has no stated successor; the likely outcomes are a silent reinterpretation of the requirement or an unrouted stop | One sentence in **4. Iterate** and one Stopping condition naming the route, with the capability-gap caveat the package already applies elsewhere (CHG-001) |
| F-002 | defect | MINOR | artifact-contract, `missing_inputs` = "explicit unresolved required information" | `references/recording-rules.md:17` vs `:23` | An artifact can carry `unknown` in a required `producer` field with an empty `missing_inputs`, so the gap does not propagate to a consumer | Add "and record it in `missing_inputs`" to the `producer` row (CHG-002) |
| F-003 | defect | MINOR | SKILL-003: "On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again" | "interrupt" absent from all three prose files; nearest bullets are `SKILL.md:110` and `:112` | A session resumed after an interruption can continue against upstream bytes that changed in the interval; the read-back rule limits the blast radius | Add one bullet to "When something is missing or a check cannot run" (CHG-003) |
| F-004 | defect | MINOR | skill-authoring-contract: record actual results and limitations | `spec-mapping.md` rework/workflow tables and coverage summary; `authoring/handoff.md` result line | Two specification rows are marked addressed when they are not, which turns an open gap into an assumed-closed one; two counts are wrong and one contradicts the same document | Correct four claims after CHG-001 and CHG-003 land (CHG-004) |
| F-005 | defect | MINOR | Authored cases must be runnable | `runner-out/run1-…jsonl`: 9 of 10 COULD_NOT_RUN in a single invocation | An evaluator running the case file the obvious way records nine blocked cases; the runner names the cause, so it is recoverable rather than silent | Document the two required invocations in `evals/fixtures/README.md` (CHG-005) |
| F-006 | defect | MINOR | skill-authoring-contract tier definitions; C gates before B and A | `evals.json` id 9 declares `tier: C` **and** `baseline_comparison: without_skill`; `cases.jsonl` `DX-C-009` | A B-shaped case labelled C either blocks B/A admission on the wrong condition or gets excused, and it puts a baseline arm inside the tier whose shape has none | Relabel to tier B and renumber the case id (CHG-006) |
| F-007 | enhancement | MINOR | skill-authoring-contract: derivation records need an exact revision and digest | `derivation.json` `derivations[4]`; `authoring-notes.md` PENDING section; runs 1–5 | The provenance record points at bytes with no checkable identity, and five open questions that are now answerable stay open | Repoint the entry at `e641797` with digests and close all five (CHG-007) |
| F-008 | enhancement | ADVISORY | missing-rust-capabilities: a fact nobody wrote a case for is not observed | `run4`, `run5` — five structural facts the candidate asserts nowhere | No demonstrated defect; the deterministic layer would discriminate facts an evaluator otherwise adds by hand | Add the five assertions this evaluator ran and observed MATCH (CHG-008) |
| F-009 | defect | ADVISORY | Internal consistency of the case file | `DX-C-009` A1 `expect: "complete"` vs its own `expectations.summary` | The runner never reads `expect`; a reader would misread the correct MISMATCH as a failure | Change the value to `"placeholder"` (CHG-009) |
| F-010 | defect | ADVISORY | Internal consistency of the case file | `run3` `DX-C-001` A5: "0 local, 0 external" | A vacuous MATCH that reads as coverage it does not provide | Point A5 at a file that has links, or drop it (CHG-010) |
| F-011 | defect | ADVISORY | skill-authoring-contract: realistic near-miss negatives with a fixed split | trigger `A7b` in `negative_define_product` vs the description's routing to `devforge-change`; author-disclosed | None on any activation observation; the category label does not describe the query | Coordinator decides whether to add a `negative_change` category, which re-cuts a fixed split (CHG-011) |
| F-012 | evaluation_gap | MAJOR | skill-authoring-contract tiers; SKILL-003 acceptance | `file-manifest.json` `installed_copy`/`plugin_export` = "not generated"; no terminal or workspace allocated | Every claim about discovery, activation, installed-resource resolution and output quality is unavailable | **no target edit** — coordinator / integration owner allocates a native evaluation |
| F-013 | evaluation_gap | MAJOR | missing-rust-capabilities, both statements | `devforge --help` observed 2026-09-10T20:05:35Z; runner header custody note | Structural evidence is manual and the runner's identities are self-reported; the disposition was adjudicated by hand | **no target edit** — DevForge integration owner |

Candidate severity counts, excluding the two evaluation gaps: **BLOCKER 0, MAJOR 1, MINOR 6, ADVISORY 4.**

## Missing capabilities and evaluation prerequisites

Recorded whatever the observations turned out to be.

- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.** Verified against the binary's own help rather than taken on trust: `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help` on 2026-09-10T20:05:35Z lists `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status` and `isolate`, and `devforge check --help` reads "Check structural policy and provenance; does not certify semantic behavior" — a project gate, not a skill-package inspector. Every structural row in this report is therefore method `INSPECTION_MANUAL` with `authority: none`, and a complete set of matching runner rows does not close this dependency. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** The runner, grader, runtime and case identities in every observations header are self-reported by the run, exactly as its own custody note says. Owner: DevForge integration owner.
- **No installed or exported copy of the candidate exists and no isolated native workspace was allocated.** Blocks tiers C, B and A (F-012). Owner: coordinator and DevForgeAI integration owner.
- **No `decision.json` or any other decision receipt was produced.** There is no implemented reduction step; the disposition below was adjudicated against the results contract by hand.
- **The validator this evaluation followed is itself unqualified.** It is a draft under bootstrap review (E2: revise → repaired at `e101e76` → recheck pending), it was source-loaded rather than installed, and it has no native evaluation of its own. Its criteria are DevForgeAI evaluator design requirements, not any provider's certification criteria. Owner: coordinator.

None of these is a defect in the candidate, and no edit to the candidate produces any of them.

## Decision and coverage

- **Disposition: revise.** One applicable `FAIL` — `AI-R04` / `CHK-SPEC-01`, driven by F-001 — and the results contract gives *revise* for any applicable `FAIL`.
- **Basis:** adjudicated against the results contract by hand; no implemented decision receipt exists.
- **Behavioural status:** `NOT_EVALUATED`.
- **Coverage actually obtained:** intake, structure and independent review are complete. Structure carries one `FAIL` alongside nine `PASS` rows, so a consumer must read every row rather than assume a single headline covered them.
- **Required observations not obtained:** tier C (`NOT_RUN` — no installed or exported copy, none to be generated under this assignment); tier B (`NOT_RUN` — no native run, and the `without_skill` arm was not executed); tier A (`NOT_RUN` — no fresh terminal, no installed package to discover, no per-attempt client-state isolation).
- **What this disposition does not say:** after the recorded repairs land, this candidate still could not reach *suitable for the stated scope* from this evaluation. Three required evidence groups are `NOT_RUN`, so its standing after repair would be *insufficient evidence* until a native evaluation is allocated.
- **Observed metrics:** the runner's own `files_read`, `bytes_read` and `duration_ms` per case are in `runner-out/`. They are bounded reads of that program, not measurements of any client session. No token, latency or cost metric was observable.
- **Adoption reference:** null.
- **Handoff reference:** `HANDOFF-devforge-design-scaffold-review-20260910`, in `handoff.md` in this directory.

*Suitable for the stated scope* is a recommendation. It was not reached here, and it would not be acceptance, adoption or release if it were.

## What this evaluation found good

Recorded because a repair specification that lists only defects invites a rewrite of things that are already right, and because the behaviour to preserve has to be nameable.

- The honesty layer is genuinely strong. Writing a mockup file and looking at it are held apart as separate facts, `NOT_RUN` is the stated default, `COULD_NOT_RUN` needs the actual cause rather than "could not check", and describing rendered appearance that was not observed is explicitly prohibited with a concrete example of what that failure looks like.
- The authority boundary is correct and unusually explicit: the four phases are named as this skill's workflow with nothing intercepting them, the absent design-spec check is named as a missing integration with an owner, and the package says in as many words that recording that requirement is design input rather than evidence a check exists.
- Provenance handling is concrete rather than ceremonial: the three-outcome upstream resolution procedure, the separation of repairing a locator from adopting a revision, the no-self-digest write order, and the instruction to check every repeated occurrence of a digest rather than only the first.
- The `user-stated` fallback for the absent `devforge-define-product` is the right shape — it produces a usable result without fabricating a `PROD-001@1`, and it labels itself so a later reader can tell what was assumed.
- Fixtures are reproducible, labelled synthetic in a README that says so first, and the two sentinel digests hard-coded in the cases match the fixture bytes exactly.
- The author disclosed its own open items, including one it could have quietly fixed (trigger `A7b`), and made no activation, installation or evaluation claim anywhere.

## Recovery and continuation

- **Last completed phase:** P6. Results, findings, the repair specification and the builder-return handoff are saved in this directory.
- **Frozen input digests still matching:** yes at the time of writing. Candidate HEAD `9ad38de`, `SKILL.md` `65dbb586…`, specification `4a90c0d5…`, validator `SKILL.md` `bdf665c7…` all re-verified during this evaluation.
- **Owned processes and workspace disposition:** no long-running process was launched; five `python3` runs completed and exited. No worktree was created, retained or released. The candidate worktree is untouched apart from this untracked output fence, and nothing was committed.
- **Conditions invalidating this report:** any change to the candidate package bytes; a new candidate revision; a change to SKILL-003 or to any of the ten governing inputs; a change to the `devforge-evaluate-expert` package at `e641797` (its rubric anchors, runner or graders), including the pending `e101e76` recheck; a DevForge CLI revision that adds skill-package structural inspection or evidence reduction; and the first native run of any tier, which supersedes every `NOT_RUN` row above for the case it covers.
