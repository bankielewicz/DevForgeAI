# This package's phase refactor: old-to-new mapping

What moved where when this package's inline workflow became `phases/`, and every sentence whose behaviour was omitted or changed. Read it if you are reviewing the refactor, reconciling an older finding against the current file layout, or looking for an instruction that used to be in `SKILL.md`.

## Contents

- The frozen baseline this maps from
- Section-to-file mapping
- Behaviour omitted or changed
- Identities and references preserved
- Phase 06 classification: a proposal, not an adoption
- `phases/` and the authoring contract

## The frozen baseline this maps from

The prior `SKILL.md`, 122 lines, SHA-256 `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9`, at commit `8d2f22b82a08a25731c1be05e91f55247d1026ad`. Those bytes remain reachable at that commit; nothing here replaces them. `references/derivation.json` records the chain.

## Section-to-file mapping

Line ranges are the baseline's.

| Old section (lines) | New location | Omitted or changed |
| --- | --- | --- |
| Frontmatter `name` (1-4) | `SKILL.md` frontmatter | None. Unchanged bytes. |
| Frontmatter `description` (3) | `SKILL.md` frontmatter | Changed. Adds the framework workflow skill target and the refactor-into-phases trigger; "the pinned dependency versions" reads "the pinned versions" and "the real code layout" gains "the governing contracts", for length. Every existing exclusion, including the three named sibling skills and the role-titles clause, is retained verbatim. 988 characters. |
| Preamble, "A project expert is not a persona" (6-8) | `SKILL.md`, preamble | Changed. Generalised from a project expert to any expert this skill authors: "this project decided" reads "that were decided", "the code that already exists" reads "the code or contracts that already exist". No obligation altered. |
| Three failure modes (10-14) | `SKILL.md`, preamble | Changed by addition. The three are retained with the same meaning, with "the project never made" reading "nobody made" and "carries nothing this project decided" reading "carries nothing anyone decided". A fourth, "Reporting instead of delivering", is added for the presentation requirement. |
| What this skill does and does not own (16-22) | `SKILL.md`, same heading | Changed by addition. The CLI's ownership is stated in full - phase state and transitions, gates, validators, mutation permission, acceptance - and one sentence is added saying that the phase files here, and any this skill authors, describe obligations and do not enforce progression. "the expert" reads "the skill" twice. Nothing removed. |
| Two roots (24-26) | `SKILL.md`, same heading | Changed. `phases/` is added to the package's own resource list. Otherwise verbatim. |
| Required inputs (28-42) | `SKILL.md`, same heading | Changed. Row 1 accepts "an accepted requirement" as well as a story, task or goal. Rows 2 and 3 are marked "Required for a project expert" instead of "Required for production expertise" and "Required". One row is added for accepted framework requirements, contracts and provider conventions. The two paragraphs after the table are verbatim. |
| (new) | `SKILL.md`, "Two kinds of target" | Added. The project-expert and framework-workflow-skill grounding split, with the rule that a framework skill needs no production application or application architecture document. |
| 1. Intake (44-50) | [`phases/phase-01-intake.md`](../phases/phase-01-intake.md) | Changed by addition. All three baseline paragraphs are retained. "Recover what already exists before asking anyone anything" is now the opening rule "Recover before you ask", with the same reasoning sentence verbatim. The `devforge expert prepare` paragraph is retained verbatim but placed under the project-expert branch, because the command is a project-expertise command; the framework branch says so instead of recording a blocked step. |
| 2. Selection (52-60) | [`phases/phase-02-selection.md`](../phases/phase-02-selection.md) | Changed by addition. All four baseline paragraphs are retained. The comparison list gains "provider" and "behaviour". Two paragraphs are added: same-provider reuse candidacy, and cross-provider equivalents being intentional implementations rather than duplicates. |
| 3. Design (62-72) | [`phases/phase-03-design.md`](../phases/phase-03-design.md) | Changed. The opening "Write the specification before the skill" paragraph is condensed into the phase's Purpose, keeping the reason it exists; see the omissions list. Everything else is retained. Added: grouping questions, carrying accepted classifications forward, capturing optional-versus-required for a genuinely new item, the phase map for a multi-step target, the no-forced-phase-count rule, and planning the old-to-new mapping for a refactor. |
| 4. Authoring (74-86) | [`phases/phase-04-authoring.md`](../phases/phase-04-authoring.md) | Changed by addition. All six baseline paragraphs are retained. "Add assets, scripts or extra references only for an actual need" now also names phase files. Added: how to author a multi-step workflow skill, how to carry out and record a refactor mapping, and the sentence that applying a change does not close a finding (also retained in `validator-handoff.md`). |
| 5. Prepared transfer (88-98) | [`phases/phase-05-prepared-transfer.md`](../phases/phase-05-prepared-transfer.md) | Changed by addition. All five baseline paragraphs are retained verbatim except "in Design" reading "in design". Added: the produced outputs must be saved and read back before the summary phase. |
| When an evaluator sends findings back (100-106) | [`phases/phase-01-intake.md`](../phases/phase-01-intake.md), "When the input is an evaluator's findings" | Changed by relocation. The first two paragraphs are verbatim. The third is not repeated there; see the omissions list. |
| When something is missing or a check cannot run (108-112) | `SKILL.md`, same heading | None. Verbatim. |
| Stopping (114-122) | `SKILL.md`, same heading | Changed. The completion condition's last clause, "and the next task is explicit and real", is replaced by the summary's contents; the hand-back paragraph gains a clause distinguishing an honestly reported blocked outcome from one presented as success. The reuse paragraph and the final paragraph are verbatim. |
| (new) | [`phases/phase-06-completion-summary.md`](../phases/phase-06-completion-summary.md) | Added. The final reporting phase: save first, then a short terminal summary. |
| (new) | `SKILL.md`, "Phase map" and "Conditional references" | Added. Navigation only: one line per phase and per reference, with when it is needed. No instruction lives only here. |

## Behaviour omitted or changed

Three items, named rather than left to be discovered:

1. **Condensed, not dropped.** Baseline line 64, "Write the specification before the skill. This is the ordering that stops an expert from becoming a description of whatever got written; the expectations exist first, independently stated, and the candidate is then written against them." Phase 03's Purpose now reads "State the expectations before the candidate exists, so the specification is not a description of whatever got written." The ordering obligation is unchanged; "independently stated" survives in the phase's produced outputs and in the acceptance-expectation rows it feeds.
2. **Relocated.** Baseline line 106, "Applying a change means the source was edited. It does not mean the finding is closed. The evaluator has to evaluate the new bytes, and prior passing observations do not transfer to changed ones." It is not in phase 01's repair-intake section; it is in phase 04's enhancement section, where the edit actually happens, and it was already carried in `references/validator-handoff.md`.
3. **Replaced.** Baseline line 116's closing clause "and the next task is explicit and real" is replaced by the summary's required contents, which include one next action and its owner. The obligation is preserved and made specific; the wording is gone.

Nothing else was removed. Every other baseline sentence appears in the new layout with its meaning intact.

One obligation is **added** rather than relocated, and is named here because it is new: every route must save its record to the assigned durable location and read it back before the completion summary. Phase 05 already did this for a full run. Phase 02 now says it for a reuse recommendation, and the stop-and-hand-back branch of phases 01, 03 and 04 says it for a partial or blocked result. The baseline's stopping section required a reuse recommendation to record its search limits but never said where that record was written, and the completion summary makes the gap operative: it must link a path that resolves.

## Identities and references preserved

The five phase identities - Intake, Selection, Design, Authoring, Prepared transfer - keep their names, their order and their Enforced classification. Every link that existed in the baseline still resolves, re-pointed only for depth: `assets/…` and `references/…` from `SKILL.md` become `../assets/…` and `../references/…` from a phase file, and each is also linked directly from `SKILL.md` so that no reference sits more than one level from the file the client always loads. Eval case IDs, fixtures and the trigger split are unchanged; new cases take new IDs.

## Phase 06 classification: a proposal, not an adoption

The authoring contract classifies five creator phases as Enforced and does not classify a sixth. This package cannot classify one, and does not. The proposal put to that contract's owner, with the fact that decides it:

An Enforced item, by this package's own interview guide, needs observable completion evidence: what could be inspected, where it lives, who writes it, and what makes it stale. Phase 06 has two halves with different answers. **Saving the detailed record and reading it back** has that evidence - files at assigned paths with final digests. **Presenting a short terminal summary** has none: a terminal response is not retained, not addressable and not inspectable, and routing it to an outbox to make it inspectable would reintroduce exactly the bookkeeping the requirement removes.

The saving half sits in the Enforced phases, not in phase 06, on every route. Phase 05 carries it for a full run. It is also carried by phase 02 for a reuse recommendation, and by the stop-and-hand-back branch of phases 01, 03 and 04 for a partial or blocked result - the routes that never reach phase 05. That placement is deliberate: phase 06 produces presentation only, and moving an evidence obligation into it would make the phase both the producer and the presenter of its own evidence.

- **Option A - Enforced.** Classify phase 06 Enforced on the strength of the save-and-read-back precondition its inputs require, and accept that the presentation half carries no completion evidence. Honest only if the classification says which half the evidence covers.
- **Option B - Optional presentation step over Enforced obligations.** Classify phase 06 Optional. Its retained-evidence obligations stay where they already are, inside the Enforced phases that produce each route's record, and the summary is a presentation convention with no evidence claim.

Option B matches the evidence rule this package applies to everyone else. It is put as a proposal either way; the owner decides. **No runtime check exists for phase 06, and none is proposed by this change.** Markdown does not enforce progression; if the owner wants one, it is a compiled DevForge CLI requirement routed to the integration owner.

## `phases/` and the authoring contract

The contract's per-skill structure lists `SKILL.md`, `references/`, `assets/`, `scripts/`, `agents/openai.yaml` and `evals/`. `phases/` is not in that list. Two facts about that:

- The contract also records that the Agent Skills specification permits additional directories, and the compiled installer and exporter select files by exclusion - `evals/`, `history/`, `__pycache__/`, `*.pyc`, `provenance.json` - rather than by an allowlist. `phases/` therefore installs and exports with the rest of the runtime package.
- This package uses `phases/` as a package-local structure. It is **proposed** for the contract's per-skill structure list and is not yet in it. That proposal belongs to the contract owner; this package does not edit `docs/mvp/` and makes no claim that the addition has been accepted.
