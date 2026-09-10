---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-E2-001"
artifact_type: "skill-enhancement-spec"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T19:40:00Z"
producer:
  skill: "independent evaluator (bootstrap, source-loaded rubric)"
  skill_revision: "no skill was installed, discovered or activated"
execution_ref: "worker E2, bootstrap review of the Claude devforge-evaluate-expert candidate"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "Tiers A, B and C are NOT_RUN, so no change below is motivated by observed session behaviour."
---

# Bounded repair specification

**Target:** `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/` at commit
`e52ac596cbf790dfa156d883852d392c512fdbcc`, in
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910`.

**Next owner:** `devforge-project-expert-creator` - the validator's author - under coordinator dispatch.

**This evaluator made no edit to the candidate.** The package byte manifest is identical before and after every
run performed during this review. Each change below is justified by a defect demonstrated on frozen bytes or on
an observed run recorded in `evaluation-report.md` and `commands.log`. Nothing here is a style preference.

## Behaviour to preserve across every change

These are the candidate's strongest properties. They were verified under adversarial probing and must survive
any repair unchanged:

1. **No aggregate verdict, anywhere.** No `overall`, `coverage_complete`, count, percentage or summary field in
   any runner output. Verified absent across six observations files.
2. **Exit status describes the program, not the candidate.** 0 = complete output written; 1 = unusable input;
   2 = internal fault. A run full of MISMATCH rows exits 0.
3. **Assertion vocabulary stays `MATCH` / `MISMATCH` / `INDETERMINATE`**, disjoint from the framework's
   PASS/FAIL vocabulary, so a row cannot be pasted into a results record as an authority outcome.
4. **`INDETERMINATE` is never softened to MATCH and never hardened into an invented MISMATCH.**
5. **Nothing is written inside `--candidate`**, ever; `--out` must be new, absolute and outside the candidate.
6. **No aggregation, import or execution of candidate code, no subprocess, no network, standard library only,
   `/usr/bin/python3`.**
7. **The two missing-DevForge-CLI-capability statements** appear in `SKILL.md`, `framework-context.md`,
   `missing-rust-capabilities.md`, `validation-results.json` and `verification-results.md`, and no run closes
   either dependency.
8. **The evaluator never repairs the candidate**, never accepts, adopts, installs or releases, and hands off to
   `devforge-project-expert-creator`.
9. **`graders.py` has no command interface.** There must remain exactly one executable.
10. **`SKILL.md` carries `name` and `description` only**, no `!` shell-injection syntax, ```text fences,
    no developer home path, no runtime dependency on `docs/mvp` or the Codex package.
11. **The name-versus-folder rule stays a recorded observation**, asserted as equality only when a case says so.

## Forbidden scope

- Do not add a rule catalogue, an aggregate field, a decision receipt, or anything that would make the Python
  scripts a gate or an acceptance decision. The two missing capabilities are the DevForge integration owner's
  work and must stay reported rather than implemented here.
- Do not port `inspect_skill.py` or `assess_evidence.py`, and do not reintroduce PyYAML or any third-party
  dependency. CHG-002, CHG-003 and CHG-004 are all satisfiable with the standard library.
- Do not rewrite `SKILL.md` prose, restructure the six phases, or compress any reference. CHG-001 adds links.
- Do not edit the Codex package, `docs/mvp`, the DevForge CLI, or any other Claude skill.
- Do not edit or refresh the three verbatim `docs/mvp` template copies. Their bytes are correct and verified;
  CHG-008(d) concerns only how they are introduced, not their contents.
- Do not treat any finding here as authority to run, install or accept anything.

## Changes

### CHG-001 - route the eight unreachable runtime files (F-001)

**Finding:** F-001. **Severity:** MAJOR. **Files:** `SKILL.md` only.

**Evidence and reproduction:** extract every Markdown link from every non-`evals` package file and take the
transitive closure from `SKILL.md`. Eight runtime files are in no one's link set and are named in no `SKILL.md`
prose: `references/evaluation-boundaries.md`, `references/framework-context.md`,
`references/contracts/{artifact,execution,skill-authoring}-contract.md`,
`assets/expert-evaluation-plan.md`, `assets/expert-evaluation-report.md`, `assets/test-cases.json`.

**Bounded desired change:** add package-relative Markdown links at the phase that needs each file. A minimal
routing that closes the gap without changing any existing sentence:

| File | Suggested phase | Why there |
| --- | --- | --- |
| `references/evaluation-boundaries.md` | §Non-negotiable boundaries **and** P2 | It holds the permission matrix and the command-boundaries table; both are entry-level constraints. |
| `references/framework-context.md` | §Two roots or §What the DevForge CLI does not implement | It holds the Rust-authority ownership split and the bounded-delivery finish line. |
| `references/contracts/*.md` | P1 and P3 | P1 freezes contract references; P3 tells the reviewer to use "the applicable contracts" without saying where they are. |
| `assets/test-cases.json` | P1 | It is the frozen human-authored case record `results-contract.md` sequences at position 2. |
| `assets/expert-evaluation-plan.md`, `assets/expert-evaluation-report.md` | P6, with the one-line mapping | SKILL-008 names EVPLAN and EVREPORT; the package delivers them as `validation-plan.json` and `verification-results.md`. Say so once, in `SKILL.md`, and link the two shipped templates as the envelope reference. |

**Acceptable alternative:** if the author judges a file genuinely redundant at runtime, remove it from the
package and record the removal in `derivation.json` rather than leaving it shipped and unrouted. Removing
`assets/expert-evaluation-plan.md` / `assets/expert-evaluation-report.md` is **not** acceptable while
`spec-mapping.md` cites them as the SKILL-008 output templates - route them or restate the mapping.

**Acceptance condition:** the transitive link closure from `SKILL.md` reaches every runtime file, or every file
outside it is deliberately removed with a `derivation.json` record. `SKILL.md` stays under 500 lines.

**Reruns:** re-extract the link graph; re-run `EX-GOOD-001` and this review's `E2-GOOD-001` to confirm
`package_relative_links` still reports every local destination resolving inside the package.

### CHG-002 - make `grade_required_report_fields` fence-aware (F-002)

**Finding:** F-002. **Severity:** MAJOR. **File:** `scripts/graders.py`, `grade_required_report_fields`.

**Evidence and reproduction:** `scratch/synthetic/fenced-report/report.md` has no `Disposition` field; its only
`Disposition:` line is inside a ```text fence. Case `E2-RPT-001` returns MATCH, `1 fields`, "every required
field is present and populated", in both modes.

**Bounded desired change:** before the per-field scan, compute the set of line numbers inside a fenced block
using the module's existing `FENCE` regex and the same open/close discipline `grade_package_relative_links`
already implements, and skip those lines. Do not change the placeholder rule, the `-* \t` stripping, the
`**field:**` form, the first-match-wins rule, or the returned `observed`/`reason` shapes.

**Preserve:** a field still holding a `{{placeholder}}` stays MISMATCH `placeholder`; a genuinely populated
field stays MATCH; a missing field stays MISMATCH `incomplete`.

**Acceptance condition:** `E2-RPT-001` returns MISMATCH `incomplete`; `EX-GOOD-002` (the populated report
fixture) still returns MATCH unchanged.

**Reruns:** the full author case file in both modes, plus this review's `scratch/cases/e2-cases.jsonl`.
Add a fenced-example fixture to `evals/fixtures/` so the regression is permanent.

### CHG-003 - stop `grade_transcript_completion` counting a mention as a consultation (F-003)

**Finding:** F-003. **Severity:** MAJOR. **Files:** `scripts/graders.py`, `grade_transcript_completion`;
`references/runner-interface.md`, the grader table row.

**Evidence and reproduction:** `scratch/synthetic/mention-only/transcript.json` completes without consulting
anything; its only mention of the target is a prompt saying *not* to use it. Case `E2-NEG-002` returns MATCH,
`completed consulted=True`, "the run completed and consulted 'devforge-evaluate-expert'".

**Bounded desired change:** restrict the consultation search to declared consultation-bearing fields of the
synthetic transcript shape - for example an event whose `type` is in an explicit consultation allowlist, or a
dedicated `skill` / `resource` / `loaded` field - and never match against free-text `prompt` or message bodies.
Where the shape cannot establish the fact, return INDETERMINATE with the reason, consistent with this grader's
existing treatment of a non-conforming transcript. Document the exact field contract in the
`references/runner-interface.md` grader table row and in the fixture README.

**Preserve:** absence of a terminal completion event still yields INDETERMINATE with `blocks_case=True` and
`execution_status: COULD_NOT_RUN`; a real client transcript still yields INDETERMINATE rather than an inference;
`expect: no_target_consultation` semantics are unchanged for genuinely conforming inputs.

**Acceptance condition:** `E2-NEG-002` no longer reports `consulted=True`; `EX-GOOD-003`
(`negative-complete.json`) and `EX-DEF-007` (the timeout transcript) keep their current outcomes exactly.

**Reruns:** both author modes and this review's case file; add a mention-only fixture to `evals/fixtures/`.

### CHG-004 - make the documented unknown-key rejection real (F-004)

**Finding:** F-004. **Severity:** MINOR. **Files:** `scripts/run_cases.py`, `load_cases`; or
`references/runner-interface.md` §Case file.

**Evidence and reproduction:** `scratch/cases/typo.jsonl` uses `"assertion"` for `"assertions"`. Exit 0;
the case is emitted as `COMPLETED` with an empty `assertions` list. A separate probe embedding
`"bogus_unknown_key"` in an otherwise valid case is likewise accepted.

**Bounded desired change (preferred):** add a module-level allowlist of permitted top-level case keys
(`case_id`, `tier`, `title`, `prompt`, `files`, `candidate_subpath`, `mode`, `expectations`, `assertions`, and
any other key the shipped `evals/cases.jsonl` actually uses) and raise `InputError` naming the file, the line
number and the offending key - matching the existing error style. Consider the same treatment for assertion
keys. **Alternative, if the author prefers permissiveness:** delete the sentence "Unknown keys and duplicate
keys within a line are rejected" from `references/runner-interface.md` and state the actual behaviour. Do not
leave the documentation and the code disagreeing.

**Preserve:** exit 1 remains "unusable input"; every existing rejection (duplicate JSON key, non-object line,
missing/duplicate `case_id`, non-list assertions, unknown grader) is unchanged; the shipped
`evals/cases.jsonl` must still load without error.

**Acceptance condition:** `scratch/cases/typo.jsonl` exits 1 naming `assertion` (preferred branch), or the
reference no longer claims a rejection that does not happen. The author's 13-case file still exits 0.

### CHG-005 - stop writing bytecode into the skill package (F-005)

**Finding:** F-005. **Severity:** MINOR. **Files:** `scripts/run_cases.py`; `references/runner-interface.md`;
`SKILL.md` §P2 invocation block.

**Evidence and reproduction:** copy `scripts/` elsewhere and run the documented form without `-B`;
`__pycache__/graders.cpython-312.pyc` appears beside the copy. The frozen worktree already contains
`scripts/__pycache__/graders.cpython-312.pyc` from the author's own runs.

**Bounded desired change:** add `sys.dont_write_bytecode = True` on the line immediately before
`sys.path.insert(...)` / `import graders`, and add `-B` to the invocation shown in `SKILL.md` §P2 and in
`references/runner-interface.md` §Interface. Either alone fixes the observable behaviour; both together also
protect a caller who copies the command by hand.

**Preserve:** the import mechanism, the "exactly one file at `--out`" guarantee (which then becomes true), and
every existing path validation.

**Do not** delete the existing `scripts/__pycache__/` from the frozen commit as part of this change; it is
evidence for this finding. Removing it is the coordinator's call.

**Acceptance condition:** running the documented form against a fresh copy of `scripts/` creates no
`__pycache__` directory.

### CHG-006 - correct the Claude discovery-location enumeration (F-006)

**Finding:** F-006. **Severity:** MINOR. **Files:** `references/sources.md` (Claude skills row);
`references/native-evaluation.md` (the discovery-location inventory step).

**Evidence:** `https://code.claude.com/docs/en/skills`, retrieved 2026-09-10, documents eight locations in
precedence order: Enterprise managed settings, Personal `~/.claude/skills`, Project `.claude/skills`, Nested
`<subdir>/.claude/skills`, Additional directory via `--add-dir`, Plugin `<plugin>/skills`, claude.ai
account-synced skills, Bundled skills. The package omits the last two and places plugin before `--add-dir`.

**Bounded desired change:** add the two missing locations to both enumerations and correct the order so
`--add-dir` precedes plugin. Keep the existing retrieval-date and refresh-condition discipline; update the
retrieval date only if the source is re-fetched.

**Preserve:** the surrounding requirement that a `without_skill` arm must lack the target in **every** location
and that an `old_skill` arm must expose only the selected preserved copy - the requirement is right, only its
enumeration is short.

**Acceptance condition:** both files list all eight locations in the documented precedence order.

### CHG-007 - coordinator decision on non-mapping frontmatter (F-007)

**Finding:** F-007. **Severity:** ADVISORY. **Files:** `scripts/graders.py`, `read_frontmatter`;
`references/runner-interface.md`, the `frontmatter_fields` row.

**This is a decision request, not a prescribed patch.** A top-level YAML sequence cannot carry a `name` key, so
"required fields are populated" is determinably false, yet the grader answers INDETERMINATE. Two defensible
positions exist and the choice is the coordinator's:

- **(a)** Return MISMATCH for a top-level sequence specifically, since no mapping key can exist. Narrower and
  more informative; slightly widens the set of defects the restricted parser is willing to assert.
- **(b)** Keep INDETERMINATE and add "top-level sequences" to the disclosed INDETERMINATE list in
  `references/runner-interface.md`. Preserves the "never invent a defect" posture exactly.

**Either way**, the disclosure gap in `references/runner-interface.md` should be closed. Do not implement (a)
without the coordinator's answer; the current behaviour is not wrong, only conservative.

**Acceptance condition:** the disclosed limits list matches the implemented classification.

### CHG-008 - four contained documentation corrections (F-008)

**Finding:** F-008. **Severity:** ADVISORY.

- **(a)** `scripts/graders.py`, `read_frontmatter` docstring: add `'duplicate'` to the list of returned statuses.
- **(b)** `scripts/run_cases.py` module docstring: scope the disjointness claim to *assertion results*, since
  case-level `execution_status` deliberately uses `COULD_NOT_RUN` per the coordinator's decision. One clause.
- **(c)** `references/derivation.json`: add `references/sources.md` to `new_in_this_package` with its digest and
  rationale. Every other declared digest was independently verified and is correct; do not touch them.
- **(d)** Once CHG-001 settles how `assets/expert-evaluation-plan.md` and `assets/expert-evaluation-report.md`
  are introduced, add a one-line note where they are linked saying that their inherited "Promoted Codex content
  mapping" paragraph refers to a `decision.json` this package does not produce, and why. **Do not edit the
  template bytes** - they are verified byte-identical to `docs/mvp` and their derivation record depends on that.

**Acceptance condition:** each statement matches the behaviour or bytes it describes.

### CHG-009 - reconcile two partially honored coordinator decisions (F-009)

**Finding:** F-009. **Severity:** ADVISORY. **Files:** `references/results-contract.md`; the author's
`authoring/handoff.md` (outside the candidate fence).

**(a) Run-manifest extension count.** The coordinator named four native extensions; the shipped
`assets/run-manifest.json` adds 17 keys to the shared v1 base (22 → 39, none removed). The four named ones are
present, and no VPR-2 field exists anywhere. Most of the other 13 trace to authoring-contract requirements
(installation mode **and path**; distinguishing worker-visible from operator-only inputs), so the *fields* look
right and the *documentation* does not: `references/results-contract.md` still says "the extensions `case_id`,
`attempt_id`, `arm` and `transcript_sha256`".

- **Bounded change:** update that sentence to describe the actual extension set, grouping the `*_ref` boundary
  fields, or trim the template to what the decision named. **This is a coordinator call**, because the extra
  fields are contract-grounded and trimming them would lose contract-required content.
- **Preserve:** the four named extensions, the `devforge.skill-run/v1` schema id, and the absence of every
  VPR-2 / Routine-Full / adoption-evidence field.
- **Acceptance condition:** `results-contract.md` and `assets/run-manifest.json` describe the same record shape.

**(b) Missing capabilities in the handoff.** `grep -c 'not implemented in the DevForge CLI'` over the author's
`handoff.md` returns 0. The handoff refers to "the two missing-DevForge-CLI-capability statements" and "the two
missing CLI capabilities becoming available" without ever naming them.

- **Bounded change:** state both sentences verbatim in `handoff.md`, as the package already does in five places.
- **No target edit.** `handoff.md` is author evidence outside the candidate package fence. Nothing in the
  candidate needs to change for this item, and the package half of the decision is fully honored.

## Where the evidence supports no target edit

- **The Rust-authority boundary needs no change.** The scripts implement no rule catalogue, emit no aggregate,
  and never present a Python result as admission or acceptance. `missing-rust-capabilities.md` names both absent
  capabilities, explains why the Codex helpers were deliberately not ported, tells the reader to verify the gap
  from `devforge --help` rather than trust the file, and confines any operator-supplied legacy helper to
  `authority: none`. No edit.
- **`derivation.json` needs no correction beyond F-008(c).** 16/16 destination digests and 18/18 declared source
  digests were recomputed and match, including the three verbatim `docs/mvp` template copies. No edit.
- **The trigger set needs no change.** 22 queries, 7 categories, 8 negatives including four near-miss
  "evaluate" senses, split across train and validation, with an installation-mode note. No edit.
- **`evals/` needs no change for reachability.** Every `files[]` entry resolves inside the `evals` directory and
  exists. No edit.
- **Provider ceremony needs no change.** No `!` syntax in any form, 143 lines, no home paths, no runtime
  `docs/mvp` dependency, every named `devforge` command present in `devforge --help`, and the
  directory-name-versus-frontmatter-`name` rule stated correctly against the documentation. No edit.
- **Nothing in the untrusted-input posture, the missing-evidence vocabulary or the handoff boundary requires an
  edit.** These are the package's strongest sections and are listed above as behaviour to preserve.
- **The two missing DevForge CLI capabilities are not repairable here.** They belong to the DevForge
  integration owner. No candidate edit produces them, and no finding above should be read as asking for one.

## Reruns after any change

1. `run_cases.py --cases <pkg>/evals/cases.jsonl --candidate <pkg>/evals/fixtures --out <new> --mode source`
2. the same with `--mode installed`
3. this review's `scratch/cases/e2-cases.jsonl` against `scratch/synthetic/` in both modes
4. the seven error probes in `commands.log`, including the `typo.jsonl` probe
5. the full package link-graph extraction (CHG-001)
6. a before/after `sha256sum` manifest of the package, and a `__pycache__` check (CHG-005)

A changed candidate is a new evaluation identity. These findings close only against new matching evidence;
preserve this report and its observations files rather than overwriting them.
