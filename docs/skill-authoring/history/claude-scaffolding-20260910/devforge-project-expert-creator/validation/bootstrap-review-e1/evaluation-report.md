---
schema_version: "devforge.artifact/v1"
artifact_id: "SEVAL-E1-001"
artifact_type: "skill-evaluation-report"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T18:56:07Z"
producer:
  skill: "independent evaluator (bootstrap, source-loaded rubric)"
  skill_revision: "unknown; no evaluator skill was installed or loaded. The Claude devforge-evaluate-expert package does not exist at this revision, so the contract's bootstrap route was used: the Codex evaluator's rubric and structural-check references were read by absolute path as source-loaded review instructions."
execution_ref: null
upstream:
  - artifact: "SKILL-007"
    revision: 3
    store: "project"
    path: "docs/mvp/specifications/skill-007-devforge-project-expert-creator.md"
    sha256: "983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c"
    sections_used: ["User goal and use-case inventory", "Inputs and provenance", "Workflow and phase exits", "Outputs and standardized templates", "Validation and behavioural acceptance", "Rework, stopping, and recovery", "F01-F08 manual promotion contract"]
  - artifact: "skill-authoring-contract"
    revision: 3
    store: "project"
    path: "docs/mvp/skill-authoring-contract.md"
    sha256: "371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53"
  - artifact: "ai-review-rubric (source-loaded from the Codex evaluator)"
    store: "project"
    path: "providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/references/ai-review-rubric.md"
    role: "R01-R10 criterion meanings, applied to a Claude package"
  - artifact: "structural-checks (source-loaded from the Codex evaluator)"
    store: "project"
    path: "providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert/references/structural-checks.md"
    role: "S001-S013 rule meanings"
evidence:
  - kind: "command log"
    path: "commands.log"
    note: "Every command with evidentiary weight or observable side-effects, with UTC time and exit status. Plain file reads into the reviewer's context are not individually listed; the files read are identified by digest in the manifest below."
  - kind: "legacy structural report"
    path: "legacy-inspect-source.json"
    note: "LEGACY, non-authoritative. Produced by the unchanged Codex helper inspect_skill.py."
  - kind: "findings"
    path: "findings.json"
  - kind: "bounded builder-return specification"
    path: "repair-spec.md"
supersedes: null
decision_ref: null
missing_inputs:
  - "Native tier A/B/C observations: no evaluation execution was allocated to this review, and the Claude devforge-evaluate-expert runner/graders do not exist at this revision."
  - "Independent second reviewer: not obtained. This is a single-reviewer static review."
---

# Skill authoring evaluation

Bootstrap route, recorded honestly: the Claude evaluator skill does not exist. This review was performed
by reading the authoring contract, SKILL-007 and the Codex evaluator's rubric and structural-check
references **as source-loaded review instructions, not as an installed skill**. No evaluator skill was
discovered, loaded, activated or invoked, and nothing here may be read as evidence that one was.

- Skill/provider: `devforge-project-expert-creator`, provider **claude**
- Source package: `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator`, 25 files
- Candidate commit: `69b6090bde458f48cae0f5751035be65fdb4593c` (verified; worktree clean apart from this review's own output fence)
- Worktree: `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`
- Branch: `author/claude-devforge-project-expert-creator-scaffold-20260910`
- Installed package: **none**. No installation or export was performed or observed.
- Selected specification: SKILL-007 revision 3, sha256 `983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c` (recomputed by this review)
- Baseline: **old_skill** — the same package at base commit `c17e758417da64928a0f47fc2600304465ac3f3c`, 3 files (static read only; no baseline arm was executed)
- Runtime and installation mode: not applicable; static source review only
- Context/assignment: independent evaluator (worker E1) under coordinator dispatch; did not author the candidate
- Prior evaluation: none

## Candidate identity — file manifest computed by this review

Computed independently with `sha256sum` over the package tree, not copied from the author's records.
This manifest is the identity to which every line reference below is bound.

| Path | SHA-256 |
| --- | --- |
| `SKILL.md` | `1e9929a5713de1df05e2b0bbafdc49de388e74104e584f4ec77c237c35362a0e` |
| `assets/evaluation-cases.md` | `46439049d859c65245c26f7427a99f97277b05f6244d7fcae8f25a4c12ff4e99` |
| `assets/expert-package.md` | `678cb91253a36a2ebf1e370d96858ed6a27206dffedc62cb90658cdcffdf890d` |
| `assets/expert-skill.md` | `1626481317b0a798dd02f8cca55716b8dce7b4c613765799568eecdd7db614f5` |
| `assets/expert-spec.md` | `4b380c265c7135b9248740aa1e2fb2adb0d3ff4ec420031945bd159d89706157` |
| `assets/handoff.md` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` |
| `assets/skill-design-spec.md` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` |
| `evals/evals.json` | `64de1a96299fd36da983f4aed320c349776a976422bda69c917497544223b1f4` |
| `evals/fixtures/assignment-record.md` | `9bf426d2a3758db50a434c30b750eb041ae6f7f263e808d7407d79b0f5a0391e` |
| `evals/fixtures/draft-xspec-with-placeholder.md` | `935ab781ff6b144a1843982933c2df867273c87363288487bba9bfca47671694` |
| `evals/fixtures/evaluator-handoff.md` | `79d046d82889f77fda7b99ce0f3e718565ccd5c0019f9c1b6db8a243c85d6275` |
| `evals/fixtures/existing-expert/SKILL.md` | `14615e93f9cf02ec4b643a2d8bd5b4441c35dfd06b8323e1fd71c5e8ab2289ad` |
| `evals/fixtures/expertise-map.md` | `79a03a25ec27af5bc36a66f6a4560a6da793bbb1c5a3148d128037f5eb375974` |
| `evals/fixtures/project.md` | `99c9c082a4354dccd9112fc412af8c89e9e94a28bfe93b7de9d579d54bea514b` |
| `evals/fixtures/stale/ARCH-001.md` | `d30ce790d5be2d5c493672c5e5568f4eeecc824e52d71e9b68ef9103ef33648b` |
| `evals/fixtures/stale/XPKG-001.md` | `a437f858371ec2d10c0a98845456b7133ac2155f385b41a2f4f448cf2a6f6c52` |
| `evals/fixtures/stale/preserved/ARCH-001.r1.md` | `65d99ab516b5fb2bca9e0d45dc5587c27d692fc426957329173a6d357ad70314` |
| `evals/triggers/trigger-queries.json` | `29a4fe7f9b93394c47942f794a70025dd9ea2a4d27557b0f8b5682cdd4972d39` |
| `references/derivation.json` | `06f951797e720415c7fdc085ab7682067e21edd6f0cf6ff03b524cbf4b595b01` |
| `references/existing-skill-selection.md` | `89a070c3fbee10a8bce513101a0dd50bbfaec431fd3056fddc8d3113e5b933df` |
| `references/framework-context.md` | `884d915f6b65f11540283ee3ed241d2e33cd54c24d22d93e51e3496d49501c66` |
| `references/interview-guide.md` | `0157e51472cbf206b73d818e0243708906496ab8d72a9b1cbefd7cfab3134d76` |
| `references/manual-operation.md` | `3b3eb092033239bd8f20f0eb1d087b810cbd87fd641225531b15abc02b3b572c` |
| `references/sources.md` | `c4b749085a2187ca97f188debdb47e9b720182b28fc6d592fafb9d84cdf11eac` |
| `references/validator-handoff.md` | `0cb2975c440d5df14e14d3b5f875393254eeeb72537684e421a5b740d0945f7f` |

The package contains no symlinks and no `scripts/`. The author's `file-manifest.json` was compared against
this manifest **after** it was computed: 25 entries, 0 mismatches, 0 missing, no unmanifested files on disk.

## Checks actually run

Commands with evidentiary weight are logged with exit statuses in `commands.log` (its header states the convention). Nothing in the candidate or any governing input was
modified; the only writes are inside this fence.

| # | Check | Command (abridged) | Result |
| --- | --- | --- | --- |
| 1 | Frozen commit verification | `git rev-parse HEAD` | `69b6090b…` matches the packet |
| 2 | Worktree cleanliness | `git status --porcelain` | Clean except this review's own fence |
| 3 | Independent file manifest | `find -type f \| xargs sha256sum` | 25 files, table above |
| 4 | Governing input identity | `sha256sum` spec-007, authoring contract | Both match the packet exactly |
| 5 | Derivation destination digests | all 24 `destination_sha256` vs actual bytes | **24/24 match**; no drift |
| 6 | Derivation source digests @ base | `git show c17e758:<path> \| sha256sum` | All match, incl. shared templates and 18 Codex port-source files |
| 7 | Template drift since base | base vs current worktree for 8 governing docs | No drift; base selection still current |
| 8 | Byte-identical template copies | 3 assets vs `docs/mvp` templates | expert-spec / expert-package / expert-skill all byte-identical as claimed |
| 9 | Markdown link resolution | custom resolver, SKILL.md rel root, references rel own dir | 16 local destinations, **0 broken, 0 escaping** |
| 10 | Path hygiene | grep `/home/`, `~/`, `/Users/`, `docs/mvp` | No developer home path; no runtime `docs/mvp` dependency |
| 11 | Codex-only concepts in shipped files | grep `$skill`, `.agents/skills`, `openai.yaml` | None outside the provenance record |
| 12 | Claude shell-injection syntax | grep `` `! `` and leading `!` in SKILL.md | None present |
| 13 | Frontmatter | parsed | Keys exactly `name`, `description`; name == folder (31 chars) |
| 13b | `SKILL.md` length | `wc -l < SKILL.md` | **118** lines. Line counts in this report use the `wc -l` newline-count convention, matching the author's records; a count-of-lines convention yields 119. Line *references* below are one-based file lines and are unaffected. |
| 14 | Description budget | measured | 869 chars vs documented 1,536 truncation limit |
| 15 | evals.json integrity | parsed; `files[]` existence and containment | 10 cases; all `files[]` exist; none escapes `evals/` |
| 16 | Spec case coverage | `spec_case` back-references | 5 acceptance + 4 common + 1 rework = all covered |
| 17 | Trigger inventory | parsed and counted | **21** queries, 10 positive / 11 negative, **6** negative categories — see F-001 |
| 18 | Stale-fixture reproducibility | digest cross-check | `XPKG-001.md` cites `65d99ab5…`, the real digest of `preserved/ARCH-001.r1.md`, while the cited path holds `d30ce790…`. Mismatch genuinely reproducible |
| 19 | Fixture labelling | grep | All 9 fixtures self-labelled synthetic |
| 20 | LEGACY structural helper | `inspect_skill.py --mode source` | exit 0; S001–S013 all PASS (PyYAML 6.0.3 present, so S004 ran) |
| 21 | DevForge CLI surface | `devforge --help`, `expert --help`, `expert prepare\|bind\|status --help`, `check --help` | Every command named in the package exists; flags accepted at the leaf subcommand exactly as the package claims |
| 22 | Installer script existence | `ls scripts/install_framework.py` | Present in the companion repository |
| 23 | Claude client facts | WebFetch `https://code.claude.com/docs/en/skills`, retrieved **2026-09-10** | Every provider claim in the package verified — see area 4 |
| 24 | Baseline recovery | `git show c17e758:…` for 3 baseline files | Read; preservation claims verified |
| 25 | Author manifest cross-check | recomputed vs `file-manifest.json` | 25/25 exact |

## Per-area results

### 1. Structure and resolution — PASS

Frontmatter carries `name` and `description` only, and `name` equals the folder name. All 16 local Markdown
destinations resolve to files inside the package; none escapes it, and `SKILL.md` links only into `assets/`
and `references/` — never into `evals/`, which is correctly source-only. No dependency on `docs/mvp`, on the
Codex package, or on any developer home path exists in the shipped instructions; the only `~/` occurrences
are the *documented* Claude personal-skills discovery location `~/.claude/skills/`, which the Selection
phase must search, and which the fetched documentation confirms.

Derivation verification exceeded the requested spot-check: **all 24** `destination_sha256` entries were
recomputed and match, and every source-side digest was verified at the stated base revision `c17e758…`,
including the three shared templates, the shared handoff template and all 18 Codex port-source files.
No governing template has drifted since base, so the author's selected input set is still current.
`references/derivation.json` correctly does not carry its own digest, and my manifest confirms no entry
anywhere records a digest of that record.

`evals/evals.json` parses, all `files[]` entries exist, and none escapes the `evals` directory.
`trigger-queries.json` has a fixed, author-assigned train/validation split with explicit-invocation,
direct-domain and indirect positives plus near-miss negatives across six categories — the substance the
contract requires. Its recorded *count* is wrong (F-001).

### 2. Requirement coverage vs SKILL-007 — PASS

The author's `spec-mapping.md` was checked against actual file content rather than trusted. All five named
phases appear as workflow content in `SKILL.md` §1–§5 with their specification exits represented, and the
package states explicitly (`references/manual-operation.md` §"What these commands do not cover") that the
phases are not CLI subcommands and that no command intercepts them — matching spec-007's requirement.

The inputs table (`SKILL.md` lines 30–38) carries all six specification inputs with their conditionality.
The three outputs XSPEC / XPKG / NATIVE ship as `assets/expert-spec.md`, `assets/expert-package.md` and
`assets/expert-skill.md`, each verified byte-identical to its governing `docs/mvp` template, and the handoff
is a faithful bounded adaptation of the shared template retaining its envelope and every substantive rule.
All five acceptance cases and all four additional common cases are materialised as graded eval cases, plus a
tenth for the rework path. Rework/stop conditions appear at `SKILL.md` lines 98–104 and 112–118.

One spec-mapping claim is inaccurate: line 136's trigger counts (F-001). Every other mapping row I sampled
resolved to real content at the cited section.

### 3. Builder requirements — PASS with two contained defects

Discovery-before-creation is operative: §2 requires searching before creating, forbids running candidates to
find out what they do, and demands the searched *and* unreachable locations be recorded, with the honest
phrasing rule "No suitable skill found in the searched inventory" versus the unsupportable "No such skill
exists". Specification-driven design is ordered correctly — §3 requires the specification before the
candidate, explicitly so expectations do not merely describe whatever got written. Focused Q&A is bounded to
one-to-three questions per round, only where the answer changes the design, with an explicit rule against
replaying settled decisions and against a newer source reopening one.

Author/evaluator separation is one of the package's strongest properties, stated in the opening failure modes
("Grading your own work"), at line 22, and enforced through `assets/handoff.md`'s fixed
**Validation status: Not performed.** and **Behavioural status: NOT_EVALUATED.** lines. Provenance is
retrievable and exact.

Two contained defects sit in the completion boundary: the working design document is required in §3 but
omitted from the stopping condition and the prepared-transfer output list (F-002), and a `reuse` outcome —
a valid and successful Selection result — has no satisfiable completion path in the Stopping rule (F-003).

### 4. Provider correctness — PASS

Verified against `https://code.claude.com/docs/en/skills`, retrieved **2026-09-10**. Every provider claim
the package makes is accurate:

- Description truncation at **1,536 characters combined with `when_to_use`** — `references/sources.md` states
  exactly this; the candidate's own description is 869 characters, well inside it.
- Invocation `/<skill-name>`, plugin-namespaced `/<plugin-name>:<skill-name>`, bare when no name collides —
  matches the documentation, and `references/manual-operation.md` line 16 correctly labels both *illustrative*
  and requires confirming what is actually installed before naming one.
- All six discovery locations in `references/existing-skill-selection.md` (project root with parent-directory
  discovery, nested subdirectory, personal `~/.claude/skills`, plugin `skills/`, managed settings directory,
  `--add-dir`) appear in the documentation, as does symlink resolution.
- Progressive loading in three phases and the ≤500-line body recommendation are both documented; `SKILL.md`
  is 118 lines (`wc -l`).

No Codex-only concept leaks into a shipped file: no `$skill` syntax, no `agents/openai.yaml`, no
`.agents/skills` path, no Codex hook event. No `!` shell-injection syntax appears in `SKILL.md`.
Every DevForge command the package names exists in the built binary, and the claim at
`references/manual-operation.md` line 42 that the flags are accepted at the leaf subcommand was confirmed
against actual `--help` output for `expert bind`, `expert status` and `check`.

### 5. Authority boundaries — PASS

The Rust CLI retains bind/gates/acceptance. The baseline had the *creator* run `devforge expert bind` and
`devforge check`; the candidate reassigns both to the operator/integration owner, correctly grounded in
spec-007's Authoring exit ("no target tests, binding or installation by creator"), and preserves rather than
deletes the commands by documenting them with owners in `references/manual-operation.md`.

No ceremonial enforcement: `references/framework-context.md` line 13 prohibits phase acknowledgements,
self-issued PASS labels and simulated advance/complete sequences as a stated prohibition rather than a style
note, and `references/interview-guide.md` line 68 repeats it for the authored expert. No self-issued PASS
appears anywhere. `SKILL.md` line 46 forbids seeking a more permissive policy or editing a gate to make a
candidate pass, and line 84 forbids an expert restating a gate as something it enforces.

Prompt-injection posture is substantively present as an *authority* boundary — a proposal cannot become an
accepted constraint by being copied downstream (line 40), a newer source does not reopen a settled decision
(line 66), a severity label is not authority (line 102). What is missing is the explicit statement that
directives embedded in supplied material are data rather than instructions, which eval case 3 nonetheless
grades (F-004).

### 6. Instruction clarity and usefulness — PASS

This is substantive draft functionality a Claude session could follow, not scaffolding. It opens with three
concrete failure modes rather than a role preamble, distinguishes the two path roots explicitly, and closes
with a finite stopping condition plus a stop-and-hand-back branch. Error and dependency behaviour is real:
the fixed vocabulary is stated with its meanings, "the absence of an error is not a pass" recurs, and line 94
requires checking what is actually installed before naming a next task — explicitly warning that
`devforge-evaluate-expert` may be absent and that a plain-language task must be given instead of an
unconfirmed slash command. No unresolved placeholder exists in any required output field of the shipped
instructions; the `{{…}}` markers in `assets/` are template placeholders, which the structural contract
treats as intentional content. I found no unnecessary ceremony.

### 7. Baseline comparison (old_skill, static) — no useful behaviour lost

The baseline is a 32-line `SKILL.md` plus two assets. Each of the seven `preserved_behaviors` claims in
`derivation.json` was checked against the baseline bytes and holds. The removed
`assets/expert-spec-template.md` is the only content deletion, and its preservation claim is **true**: all
eight contract rows (Responsibility, Activation, Knowledge, Inputs, Decisions, Output, Evaluation, Refresh)
and the AI-proposal-versus-user-decision rule are carried into `references/interview-guide.md` lines 45–56,
and the original bytes remain reachable at the base commit. All seven baseline evaluation cases survive in
`assets/evaluation-cases.md` items 1–7 with their meanings intact, plus two optional additions.

Two baseline behaviours were deliberately reassigned rather than lost — creator-run binding/checking, and
creator-run evaluation — both correctly grounded in spec-007 revision 3's author/evaluator separation. The
baseline description ended "evaluate it with project-specific cases"; dropping that and routing evaluation to
`devforge-evaluate-expert` is a correctness improvement, not a regression.

## R01–R10 review criteria

Static, scoped results bound to commit `69b6090b…` and the file manifest above. No score, average or
percentage is derived from these.

| ID | Applicability | Outcome | Evidence and rationale | Finding |
| --- | --- | --- | --- | --- |
| R01 Task identity and scope | Applicable | **PASS** | `SKILL.md` lines 2–3: description states the capability and the selecting conditions, and discriminates three adjacent workflows by name plus the "list of role titles" near-miss. Body task matches spec-007 "User goal". 869 chars, inside the documented 1,536 limit. Cannot prove native activation. | — |
| R02 Inputs, outputs, completion | Applicable | **FAIL** | Inputs (lines 30–40) and missing-input behaviour are complete and consequential. But the working design document required at line 64 is absent from the completion rule (line 114) and from the §5 prepared-transfer record list (lines 88–90); the declared completion rule can be satisfied without it ever being transferred, while `references/manual-operation.md` line 11 lists "design and XSPEC" as the creator exit. | F-002 |
| R03 Authority, ownership, accepted decisions | Applicable | **PASS** | Lines 22, 40, 46, 84, 92; `references/framework-context.md` lines 11–17, 21–23, 81. Authoring-only boundary held; bind/check ownership reassigned with a cited specification basis; proposals kept distinct from decisions; no self-granted approval. | — |
| R04 Workflow decisions and failure paths | Applicable | **FAIL** | Failure handling is otherwise strong (lines 106–110: fixed vocabulary, unavailable-dependency behaviour, collision handling with no delete/reset/force and no quiet relocation). But `reuse` — named at line 56 as a valid Selection outcome and called "a successful outcome" at `existing-skill-selection.md` line 44 — satisfies neither branch of Stopping: line 114 requires an authored candidate, line 116 covers only blockers. | F-003 |
| R05 Runtime dependencies and resource delivery | Applicable | **PASS** | 16/16 local links resolve inside the package; the two roots are distinguished at lines 24–26 and `framework-context.md` lines 27–31; no runtime `docs/mvp` or home-path dependency; `evals/` is not linked from `SKILL.md`; every named command verified present in the built binary and the installer script exists. No candidate code was run. | — |
| R06 Instructions versus supplied data | Applicable (reads project docs, code, pasted snippets, evaluator reports) | **PASS** | The authority boundary is present and repeated — lines 40, 46, 66, 102 — so supplied material cannot silently become authority, which is the criterion's PASS anchor. Residual gap: no shipped instruction states that directives embedded in supplied material are data, although eval case 3 grades exactly that. | F-004 |
| R07 Framework semantics and artifact provenance | Applicable | **PASS** | All 24 destination digests and every source digest verified exact at the stated revision; no artifact carries its own digest, and the rule is stated at `framework-context.md` lines 61–67; draft/adopted, structural freshness and behavioural evaluation kept separate at lines 92–93; prior bytes preserved at the base commit. No digest, receipt or lineage claim is fabricated. Scoped exception: a count in a provenance *narrative* field is wrong (F-001); it meets no R07 FAIL anchor because no identity, digest or lineage is affected. | F-001 |
| R08 Prompt organization and decision-relevant detail | Applicable | **PASS** | 118-line body (`wc -l`) with conditional detail in five linked references, each linked at the phase that needs it. No conflicting duplicate rule was found; the "second design document" prohibition (line 118) is an over-delivery bound, consistent with `manual-operation.md` line 7's "do not maintain a second *independent* design". Task-specific rather than generic content throughout. | — |
| R09 Observable checks and honest outcome reporting | Applicable | **PASS** | Fixed vocabulary with meanings (lines 106–110); "the absence of an error is not a pass" recurs; line 94 separates what is suggested, what is installed and what was actually invoked; line 104 states an applied change is not a closed finding. The skill correctly refuses to run validation within an authoring scope, which this criterion explicitly does not penalise. | — |
| R10 Enforcement and handoff boundaries | Applicable | **PASS** | Enforcement requirements are recorded and routed to the integration owner with the status fixed at "no gate implemented by this skill" (`interview-guide.md` lines 58–72; `framework-context.md` line 17). Handoff carries next owner, real limits, finding-ID and severity preservation (`validator-handoff.md` lines 37–50) and one copyable task conditioned on actual installation. The evaluator does not repair; the creator does not evaluate. | — |

**Outcome counts:** PASS 8, FAIL 2, COULD_NOT_RUN 0, NOT_APPLICABLE 0. Both FAILs carry MINOR severity —
severity reflects demonstrated impact, and in each case a linked reference recovers the missing behaviour.

## Findings

| ID | Severity | Type | Requirement | File and location | Demonstrated impact | Smallest repair |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | MINOR | defect | Authoring contract, derivation-record accuracy; R07 | `references/derivation.json` line 244 (shipped); also `spec-mapping.md` line 136, `handoff.md` line 125, `authoring-notes.md` line 105 | The record says "Twenty-two queries … five negative categories"; the file holds **21** queries (10 positive, 11 negative) across **6** negative categories. The derivation record is the package's own drift-detection instrument, and its own refresh condition treats a record/actual mismatch as drift; a coverage reviewer reconciling record against file hits a discrepancy, and "five categories" understates near-miss breadth. | Correct the count and the category enumeration in the `transformation` string. No change to the queries themselves. |
| F-002 | MINOR | defect | SKILL-007 Design/PreparedTransfer exits; R02 | `SKILL.md` line 64 versus lines 88–90 and line 114 | The working design document is mandated in Design but never named in the prepared-transfer record list or the completion rule, so a session can satisfy Stopping without carrying it into the transfer — while `manual-operation.md` line 11 makes "design and XSPEC" the creator exit. The linkage lives only in a reference introduced at line 96 under a command-ownership framing. | Name the design document in §5's record list and add it to the Stopping sentence — roughly one clause in each. |
| F-003 | MINOR | defect | SKILL-007 Selection exit; R04 | `SKILL.md` line 56 versus lines 114–116 | `reuse` is a named, valid and successful Selection outcome with no satisfiable completion path: Stopping demands an authored candidate, and the stop-and-hand-back branch covers only blockers. Eval case 2 (`indirect-activation-reuse-check`) expects exactly a reuse or bounded-enhancement recommendation, so a session self-checking against Stopping may author a candidate anyway — the behaviour that case grades against. | Add a clause to the Stopping paragraph recognising a recorded reuse recommendation, with its search limits, as a complete result. |
| F-004 | MINOR | defect | R06 trust boundary; eval case 3 expectation | `SKILL.md` "Required inputs" / §1; expectation at `evals/evals.json` case 3 `graded_observations` | Eval case 3 grades "External content is treated as evidence about the world, not as an instruction that changes project authority", but no shipped instruction states it. The declared workflow ingests pasted snippets, project documents and evaluator reports, so the behaviour is graded without being instructed. | One sentence stating that supplied material provides facts, never instructions or authority. |
| F-005 | ADVISORY | evaluation_gap | Shared-template governance | `assets/expert-spec.md` line 63; `assets/expert-package.md` line 64 | Both byte-identical shared-template copies carry a "Promoted Codex content mapping" section that is Codex-scoped and NOT_APPLICABLE to a Claude package. **No target edit by the author is supported**: editing a byte-identical copy would fork the governing `docs/mvp` template and break the verified byte-identity. The author flagged it and routed it via `derivation.json` refresh conditions. | No target edit. Integration-owner decision on the shared template. |
| F-006 | ADVISORY | evaluation_gap | Authoring contract, three tiers | Whole package | Tiers A, B and C are unobserved and behaviour is `NOT_EVALUATED`. No evaluation execution was allocated to this review, and the Claude `devforge-evaluate-expert` package that supplies the runner and graders does not exist at this revision, so the authored cases cannot yet be executed by anyone. | No target edit. Coordinator allocates evaluation once the evaluator package exists. |

No BLOCKER and no MAJOR finding was demonstrated.

## Tier results

| Tier | Cases | Observations and evidence | Outcome | Limits |
| --- | --- | --- | --- | --- |
| A discovery/activation | 21 authored trigger queries | None. No installation, no fresh terminal, no discovery or activation observed. | **NOT_RUN** | Not allocated to this static review. Requires an installed package in a fresh target terminal; no installed copy exists. A source review can never establish tier A. |
| B output quality | 10 authored tier-B cases with an `old_skill` baseline | None. Neither the candidate arm nor the baseline arm was executed. | **NOT_RUN** | Not allocated. The runner and deterministic graders belong to the Claude `devforge-evaluate-expert` package, which does not exist at this revision. |
| C installed resources | Installed-resource resolution | None. No install or export was performed. Static link resolution was checked in source and is **not** tier C evidence. | **NOT_RUN** | Not allocated. Requires an actual exported or project-local installation in a consuming project. |

- Run manifests/transcripts/grades: none produced; no run occurred. `commands.log` records this review's own commands only.
- Human feedback: not obtained.
- Resource measurements: not observable in a static review.
- **Proposed disposition: revise (bounded).** The package is otherwise suitable for its stated scope — an
  authored, unevaluated draft candidate. Four MINOR repairs are recommended; none of them blocks allocating
  the evaluation. F-003 is the one worth applying *before* a tier-B run, because it interacts directly with
  what eval case 2 grades.
- **Behavioural status: NOT_EVALUATED.**
- Unavailable or excluded observations: all native tiers (F-006); independent second reviewer not obtained.
- Required refresh and next owner: the **same author (builder)**, under coordinator dispatch, per
  `repair-spec.md`. Any applied change produces a new candidate identity and requires re-evaluation of the
  changed bytes; nothing in this report transfers to edited bytes.
- Adoption reference: null

## Limits of this review

1. **Bootstrap route, not an installed evaluator.** No Claude evaluator skill exists. The rubric and
   structural-check references were read from the Codex package by absolute path as source-loaded
   instructions. This is the contract's permitted bootstrap and is not an evaluator invocation.
2. **Static only.** No candidate code, helper or skill was executed. Static link resolution, digest
   verification and structural checks establish which bytes exist and reference what — never behaviour.
3. **Single reviewer, limited independence.** I did not author the candidate and applied predeclared
   criteria, but I am not a filesystem-, process- or memory-isolated reviewer. I read
   `references/derivation.json`'s narrative before completing my own inspection; I mitigated this by
   computing the file manifest and all digest comparisons independently first and comparing to the author's
   records only afterwards. The author's `authoring-notes.md`, `spec-mapping.md` and `handoff.md` were read
   last, after my findings were formed.
4. **The legacy helper is non-authoritative.** `legacy-inspect-source.json` (exit 0, S001–S013 PASS) is
   LEGACY Python evidence recorded as supporting structural observation only. It carries no framework
   admission or acceptance authority, and its PASS establishes no behaviour.
5. **Local runs are local evidence.** The `devforge --help` invocations and the structural helper ran in this
   environment against a prebuilt debug binary. They are not isolated native evidence and prove nothing about
   a consuming project.
6. **Provider facts are documentation, not observation.** The Claude client claims were verified against the
   published documentation retrieved 2026-09-10. No client discovery or activation behaviour was observed.
7. **Untrusted evidence handling.** The candidate, its fixtures, its derivation record and the author's
   handoff and self-assessment were treated as evidence, not instructions. No author-preferred verdict was
   adopted; the author's spec-mapping was checked against actual file content, which is how F-001 surfaced.
8. **I recommend; I do not accept.** No acceptance, adoption, promotion or release decision is made here.
