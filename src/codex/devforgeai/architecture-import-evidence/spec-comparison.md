# Architecture Port — SPEC-003 Comparison

## Scope and denominator

This comparison binds the Codex `architecture` skill revision 4 to approved `SPEC-003` v1. The
native v4 campaign binds candidate SHA-256
`002672e3f614de13d5268e6d34a71f95d52202f212f06d97de9388f9ceb3da92`, definitions SHA-256
`050863b32468d45437425116e5ce4868ff928cb37ece9f66bfc130d2b0c18323`, and checkpoint
`5e041cced955ea817fd113a4d44353201cf55426`. The frozen
denominator is **41 named obligations**: BEH-01–16 (16), ERR-01–06 (6), QR-01–03 (3), and
VER-01–16 (16). Static correspondence below establishes instruction coverage only; it does not
establish runtime behavior.

SPEC-003 defines 14 automated/e2e verifications and two manual verifications. The automated cases
are: VER-01 `creates-arch`; VER-02 `org-a-policy`; VER-03 `org-b-policy`; VER-04 `unrelated-adr`;
VER-05 `superseded-adr`; VER-06 `no-acceptance-without-user`; VER-07
`existing-arch-not-duplicated`; VER-08 `insufficient-evidence`; VER-09
`prd-change-handed-back`; VER-10 `hands-off-to-epic`; VER-11 `ignores-unrelated-request`;
VER-14 `records-provenance`; VER-15 `reuse-records-review`; and VER-16
`reuse-review-idempotent`. VER-12 is an eleven-part interactive/manual obligation; VER-13 is the
operator immutability check.

VER-12's sub-denominator is: (a) explicit per-decision acceptance; (b) bounded inspection, with
separate yes/no out-of-scope runs; (c) draft-PRD warning timing; (d) stopped-session draft offer;
(e) invalid-policy stop; (f) PRD/Architecture shared-reference byte identity; (g) unknown-PRD
listing; (h) skill-size limits; (i) ERR-05 restoration after an accepted decision; (j) versioned
amendment link preservation; and (k) an explicitly approved ADR supersession. VER-13 separately
requires the same deployed-plugin digest before, between, and after the Organization A/B runs, plus
a clean `git diff src/`.

## Static obligation mapping

| Obligation | Codex instruction coverage | Verification route |
|---|---|---|
| BEH-01 | PRD selection, ID-only input, and no-argument question | VER-12 manual |
| BEH-02 | PRD reading, draft warning, immutable PRD, product-question boundary | VER-01 |
| BEH-03 | R1–R5 policy resolution and stop-on-invalid rules | VER-02, VER-14; VER-13 manual |
| BEH-04 | Existing ARCH selection, reuse/amend gate, next free ID | VER-01, VER-07 |
| BEH-05 | Named-scope-only inspection and classified EVD records | VER-08; VER-12 manual |
| BEH-06 | Shared architectural questions, DEC links, and components | VER-01 |
| BEH-07 | Only policy, confirmed accepted ADR, or explicit user decision resolves a DEC | VER-02–04, VER-06 |
| BEH-08 | Separately confirmed reuse/amend/create outcome | VER-02, VER-06, VER-15–16 |
| BEH-09 | New, amended, and review-record write rules | VER-01, VER-15–16; VER-12 manual |
| BEH-10 | CMP items, Mermaid view, and NFR/constraint links | VER-01 |
| BEH-11 | Decision-specific readiness with live resolver status | VER-02–05 |
| BEH-12 | PRD-owner handback without editing the PRD | VER-09 |
| BEH-13 | Provider provenance, dates, hashes, and templates | VER-14; VER-12 manual |
| BEH-14 | Read-back self-check, three attempts, and validation-failure handling | VER-01; VER-12 manual |
| BEH-15 | Complete readiness report and final epic handoff | VER-01, VER-10 |
| BEH-16 | PRD/BRN/policy immutability and constrained ADR supersession | VER-09; VER-12 manual |
| ERR-01 | Unknown PRD lists available PRDs and writes nothing | VER-12 manual |
| ERR-02 | Invalid policy stops before writes with file, setting, and rule | VER-12 manual |
| ERR-03 | Out-of-scope inspection asks first or records the unknown | VER-12 manual |
| ERR-04 | Several applicable ARCHs are listed for user selection | VER-07 claims coverage; see D-02 |
| ERR-05 | After three failed checks, restore only unsafe acceptance state | VER-12 manual |
| ERR-06 | A stopped session offers a draft with open decisions and null outcome | VER-12 manual |
| QR-01 | Frozen v4 `SKILL.md` is 371 lines and its 638-character description is within the 500/1024 limits | Static; VER-12 manual |
| QR-02 | Frontmatter is limited to the specified fields; skill/provenance versions match | Static; VER-11 is trigger-only |
| QR-03 | Fourteen tagged cases correspond one-for-one with automated VER items | Evaluation campaign plus baseline |

## Provider adaptations

These differences from the literal Claude paths and commands preserve the workflow contract:

| ID | SPEC-003 / Claude form | Codex form | Assessment |
|---|---|---|---|
| A-01 | SPEC-003:165 uses `AskUserQuestion` | `SKILL.md:75-81` and `references/readiness.md:71-77` use native `request_user_input` within its three-question/three-option limits, with a plain-text fallback that retains all choices | Required by the import request |
| A-02 | SPEC-003:214,220 uses `${CLAUDE_SKILL_DIR}` / `${CLAUDE_PLUGIN_ROOT}` | `SKILL.md:36-40,246,266,309-319` resolves assets and sibling skills relative to the loaded Codex skill | Required provider adaptation |
| A-03 | SPEC-003:163 names `.claude/devforgeai.local.md` | `SKILL.md:31-40` and the shared policy reference use `.codex/devforgeai.local.md`, read-only during Architecture | Provider-specific project preference path |
| A-04 | SPEC-003:214 and the Claude source use Claude provenance | `SKILL.md:248-261` and `references/output-rules.md:52-56,168-177` require `codex` plus actual host identity; unavailable identity stays explicitly unresolved | Honest provider provenance |
| A-05 | SPEC-003:38-39,220 uses Claude slash commands | `SKILL.md:28-30,309-319` and `agents/openai.yaml` use namespaced Codex skill mentions | Avoids presenting Claude commands as Codex commands |
| A-06 | SPEC-003:31,70-84 defines the Claude layout | `src/codex/devforgeai/skills/architecture/` adds Codex agent metadata while retaining the two templates and five references | Required Codex plugin layout |
| A-07 | SPEC-003:153 includes Claude's `argument-hint` field | Codex frontmatter omits that unsupported provider field and carries the input hint in the default prompt and skill body | Required frontmatter adaptation; QR-02 is evaluated against Codex's schema |

## Discrepancies and limits

| ID | Finding | Consequence |
|---|---|---|
| D-01 | SPEC-003:290-292 still says the skill is not built and automated verification is not run, although the Claude source and its 14 cases now exist. | Treat that table as stale historical status. Codex evaluation results must be reported separately and must not be inferred from the source suite. |
| D-02 | SPEC-003:362-369 claims VER-07 covers ERR-04, but `existing-arch-not-duplicated/scaffold.sh:167-196` creates only ARCH-001. ERR-04 requires several potentially applicable ARCH documents. | The source automated suite still does not exercise the multiple-ARCH branch. The separate v4 `ERR-04` supplemental probe closes that bounded behavior gap: protocol line 364 sends a real `request_user_input` naming ARCH-001 and ARCH-002, then stops unanswered without writes. This supplemental PASS does not repair or replace source VER-07. |
| D-03 | SPEC-003:100-102 and VER-12(f) at 405-407 require Architecture `policy.md` and `defaults.md` to be byte-identical to the PRD skill's copies. | Cross-worktree static correspondence passes against committed PRD candidate `fb8bc29f5adf2db07f2694b989bf4ecce82d95c3`: policy SHA-256 `6318353443a49d5d607948833fa087a08d5b9e210a0524e70010263586b75847`; defaults `58e578242a06031fef08de7b8e5c907791bbb14739717085a34ebecde68b5dab`. Same-package and deployed integration remain `NOT_RUN` because this branch does not contain that Codex PRD skill. |
| D-04 | VER-12(a–k) at SPEC-003:405-407 and VER-13 at 424-431 are manual by specification. | Automated case success cannot waive them; each must be reported PASS, FAIL, or NOT_RUN separately. |
| D-05 | Static presence of a rule, a passing helper, or model-authored output does not establish the behavior. | Runtime qualification requires retained native Codex trials, independent grading, and a no-plugin baseline. |
| D-06 | VER-14 at SPEC-003:432-440 requires actual current-run model and session identity. An honest `unknown` fallback avoids invented provenance but does not satisfy VER-14; `references/output-rules.md:279-281,305-309` enforces this boundary. | Regex acceptance of non-empty placeholder text must not be reported as full provenance qualification. |
| D-07 | Native loading from a source root, installation, and VER-13's deployed-plugin immutability check are separate states. | A successful source-root evaluation does not establish installation or the deployed operator check. |
| D-08 | VER-07's source prompt says `Proceed without questions`, while SPEC-003:185-187 and VER-07 require the skill to recommend reuse/amend and ask the user to choose. The retained smoke and fresh v4 `existing-arch-not-duplicated--plugin--1` honored the literal user instruction, recommended amend, wrote nothing, and asked no question. | VER-07 remains `FAIL`: the required source-case choice request is absent. The v4 ERR-04 supplemental probe confirms that `request_user_input` works when the prompt permits a question, but it cannot waive this source-case contradiction or failure. |
| D-09 | In that retained smoke, `protocol.jsonl:87-89` starts `pwd && rg --files` with broad patterns at the repository root concurrently with loading `SKILL.md`. | This violates SPEC-003:188-190 / BEH-05's fixed-path, no-root-listing rule. Because the scan started before the skill completed loading, record it as a native activation-order/runtime failure, not an omission from the static port. |
| D-10 | Historical v3 supplemental VER-12(e) named `POL-001.md`, `SET-03`, `interview.max_calls`, value 50, allowed range 1–20 and ERR-02, but omitted the exact `schema` label required by `references/policy.md:194-203`; its frozen helper therefore reported `FAIL`. | The v4 VER-12(e) probe resolves this exact-format gap. Its protocol line 162 names the file, setting, key, invalid value, schema range and ERR-02, stops, and says nothing was written. Independent v4 review records `PASS`; retain the v3 failure as historical evidence only. |
| D-11 | Claude `references/output-rules.md:170-172` requires every newly written Change Log row to identify the current session and limits equality with `generated_by.session` to a new or amended ARCH. A review record deliberately preserves historical `generated_by` byte-for-byte (`:197-211`; SPEC-003 BEH-09 at 200-202). Codex v3 instead required the row session to equal `generated_by.session` unconditionally. Retained v3 VER-15 `reuse-records-review--plugin--1/protocol.jsonl:517,800` consequently added `codex (session fixture-session)`, copying the historical fixture identity although the actual current thread was `01a0e9f9-d4be-7122-8886-b8c163865de6`; its line 514 self-check explicitly asserted that incorrect equality before claiming PASS. | This was an introduced provider-port regression and a real v3 BEH-09 / VER-15 failure that the structural grader missed. Candidate v4 corrects the rule at `references/output-rules.md:170-174,305-309`: the new row uses the current Codex host session/thread ID (or an honest unresolved `unknown`), equality to `generated_by.session` applies only for new/amended ARCHs, and a review record retains historical `generated_by`. V3 results do not qualify v4; the v4-bound VER-15/16 runs must demonstrate the correction. |
| D-12 | V4 VER-15 `reuse-records-review--plugin--1/protocol.jsonl:719,723` correctly preserves historical `generated_by` and writes `codex (session unknown)` rather than copying the fixture identity. The final answer discloses that the current session ID was unavailable, but calls the read-back `PASS` and does not mark current-run provenance incomplete or validation unresolved. The actual protocol thread is `01a0ea02-fb36-7653-ae42-6954b752ccb2`. | This is a native runtime-conformance failure against the v4 unresolved-provenance boundary in `references/output-rules.md:170-174,305-309`. Structural three-change custody may pass, but the review cannot be reported fully validated when its current-run audit identity is unknown. VER-15 remains failed for complete contract conformance even if a structure-only grader accepts it. |
| D-13 | V4 VER-05 `superseded-adr--plugin--1/protocol.jsonl:374` first amends the approved ARCH correctly to version 2, `status: in-review`, with cleared approval fields. Lines 395 and 530 retain three failed provenance checks. Line 532 then applies ERR-05 by restoring `status: approved`, `approved_by: "Priya Nair"`, and the old `approved_on` date while retaining the version-2 amendment. ARCH-001 changes from SHA-256 `9cf67270f4c8ae9a2536e6f00fc1992ce44fabc427194a1e293e57622f80eccc` to `f4dda212fdfc5c9552d237ceac889685cff554cf71ca223b421af29783f94a0f`; PRD and ADR hashes remain unchanged. Section 8, the audit row, and the final answer at line 749 explicitly warn that those historical fields do not approve the amendment and withhold readiness, but the document's normative metadata still presents version 2 as approved. | This is an inherited contract tension for owner clarification, not a demonstrated unauthorized provider change. BEH-09 / `references/output-rules.md:182-188` define the normal amended state as `in-review` with cleared approval fields; ERR-05 at SPEC-003:252-254 / `references/output-rules.md:258-264` explicitly defines a different failure state by restoring every changed status and approval field while retaining other content. The trace complies with that exception. The retained metadata can still mislead downstream consumers, so the rollback contract should state how historical approval applies after a failed amended write. The trial's concrete failures remain unresolved exact provenance and the missing required readiness report. |

## Retained evaluation boundary

Candidate v3 (`9b60b259dc26720d3cd5797a4fe7b6a7800746482e9897d5fece0bd8e8e36e7d`)
was interrupted after D-11 was confirmed. Its `interruption.json` records **24 completed, 4
interrupted and 56 NOT_RUN** trials out of 84. The interrupted VER-05 arms are ungraded. The
independently reviewed v3 VER-07 plugin and baseline trials both fail the required user-choice gate,
and the v3 supplemental probes are retained historical evidence only. None qualifies revision 4.

Revision 4's `native-evaluation-20260928-v4/evaluation-summary.json` records **84 of 84 trials
completed with no harness errors** under `codex-cli 0.158.0` and `gpt-6-astra`. The plugin mean is
`0.8426587302` versus baseline `0.3035714286`; plugin threshold passes are 36/42, strict passes are
7/42, and activation passes are 42/42 in both arms. Artifact-schema checks pass for all 33 plugin
artifacts authored or modified; the baseline authors 52 artifacts, with 3 passing and 49 failing.
Only VER-11 and VER-16 pass their complete frozen case obligations. VER-01–10 and VER-14–15 fail;
VER-12 and VER-13 remain NOT_RUN. Aggregate means and threshold counts do not waive
any failed case or mandatory manual obligation.

The independent v4 semantic adjudication required for VER-05 and VER-07 is complete: **12 of 12
reviews are FAIL**. All six VER-07 arm/repeat reviews identify the same missing contract element:
the output points to ARCH-001 and generally recommends amendment, but never asks the user to choose.
All six VER-05 arm/repeat reviews omit the required complete final readiness mapping for FR-001,
FR-002, and NFR-001. The plugin runs correctly reopen DEC-01 and retain DEC-02, but exact-provenance
failure causes them to withhold the readiness handoff; that is still a FAIL under the frozen
`readiness-mapping` rubric. Each retained trial has a schema-checked `semantic-review.json` using the
grader's exact top-level key.

## Manual and supplemental status

The v4 supplemental set is independently reviewed as **4 PASS, 0 FAIL, 0 REVIEW_REQUIRED** for its
narrow obligations: VER-12(c) draft-warning timing, VER-12(e) exact invalid-policy stop,
VER-12(g) unknown-PRD listing, and the separate ERR-04 multi-ARCH native question. Candidate hashes
match before and after every probe.

Complete VER-12 remains **NOT_RUN**. Subcases (c), (e), (g), and (h) pass. Subcase (f) has static
cross-worktree byte parity, but same-package integration is not run, so the subcase remains NOT_RUN.
Subcases (a), (b), (d), (i), (j), and (k) are NOT_RUN. VER-13 also remains **NOT_RUN** because no
installed/deployed plugin underwent the required before/between/after Organization A/B digest check.
These mandatory gaps cannot be waived by the automated matrix or supplemental percentage.

## Result boundary

The final static audit found no unadapted Claude runtime token. The two asset templates remain
byte-identical to the Claude source. D-11 records an unintended v3 semantic change in review-record
provenance and its v4 correction; only a v4-bound campaign can qualify the correction. Final
behavioral status belongs to the retained Codex evaluation record; this document does not convert
other static correspondence into a pass.
