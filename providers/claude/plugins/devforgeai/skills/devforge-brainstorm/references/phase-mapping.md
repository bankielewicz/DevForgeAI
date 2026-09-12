# This package's phase refactor: old-to-new mapping

What moved where when this package's inline workflow became `phases/`, and every sentence whose behaviour was omitted or changed. Read it if you are reviewing the refactor, reconciling an older finding against the current file layout, or looking for an instruction that used to be in `SKILL.md`.

## Contents

- The frozen baseline this maps from
- Section-to-file mapping
- Behaviour omitted or changed
- Identities and references preserved
- Runtime phases versus package-local steps
- Phase 06 classification: a proposal, not an adoption
- `phases/` and the authoring contract

## The frozen baseline this maps from

The prior `SKILL.md`, 195 lines, SHA-256 `a5316781cafbe0a68cf0a434a27bbd35ba8761de6205a10caebabed6f16eff8c`, at commit `fd4172272043c1ccf47c057b8fdc4543500ce629`. Those bytes remain reachable at that commit; nothing here replaces them. [`references/derivation.json`](derivation.json) records the package's own derivation chain and is unchanged by this refactor.

## Section-to-file mapping

Line ranges are the baseline's.

| Old section (lines) | New location | Omitted or changed |
| --- | --- | --- |
| Frontmatter `name` and `description` (1-4) | `SKILL.md` frontmatter | None. Unchanged bytes. Activation behaviour and the tier-A trigger set are untouched by this change. |
| Preamble, "The user is early" and the two failure modes (6-15) | `SKILL.md`, preamble | None. Verbatim. Fabrication and silent promotion stay in the file the client always loads, because they govern every phase. |
| If a runtime is managing this session (17-48) | `SKILL.md`, same heading | None. Verbatim. The authoring contract requires a managed brainstorm task's essential behaviour to stay in `SKILL.md`, with conditional detail in a package-relative reference; that split is unchanged. |
| Where the artifacts go (50-83) | `SKILL.md`, same heading | Changed in one clause. The package's own resource list gains "the `phases/` files"; the sentence is also re-wrapped. No obligation altered. |
| 1. Recover what already exists (85-91) | [`phases/phase-01-recover.md`](../phases/phase-01-recover.md) | None. All three paragraphs verbatim. |
| When the upstream has moved on (93-108) | [`phases/phase-01-recover.md`](../phases/phase-01-recover.md), same heading | None. All seven paragraphs verbatim. The heading is promoted from `###` to `##`, since it is now a section of its own file rather than a subsection. |
| 2. Explore (110-120) | [`phases/phase-02-explore.md`](../phases/phase-02-explore.md) | None. All five paragraphs verbatim. |
| 3. Record (122-131) | [`phases/phase-03-record.md`](../phases/phase-03-record.md) | Changed by addition. The four column bullets and the stable-ID paragraph are verbatim; the opening sentence is verbatim except that `assets/idea-ledger.md` becomes a relative markdown link. One sentence is added pointing at `recording-rules.md` at the moment the frontmatter is written - the same pointer the baseline carried in "Filling the envelope honestly", with the same four trigger conditions, now also reachable from the phase that writes. |
| 4. Focus (133-143) | [`phases/phase-04-focus.md`](../phases/phase-04-focus.md) | Changed in two pointers only. Four of the five paragraphs are verbatim. In the fifth, `assets/handoff.md` becomes a relative markdown link and "*Where the artifacts go* above" reads "*Where the artifacts go* in `SKILL.md`", because the section it names is no longer above it. |
| Before you call it done, write order and digests (145-182) | [`phases/phase-05-readback.md`](../phases/phase-05-readback.md) | Changed by relocation only. The four numbered steps, the placeholder rule and the whole `producer.skill_revision` paragraph are verbatim; the `recording-rules.md` pointer inside step 2 becomes a relative link. |
| Before you call it done, "Then tell the user ..." (183-191) | [`phases/phase-06-completion-summary.md`](../phases/phase-06-completion-summary.md) and [`phases/phase-05-readback.md`](../phases/phase-05-readback.md) | Changed. See the omissions list, items 1 and 2. |
| Filling the envelope honestly (193-195) | `SKILL.md`, "Conditional references" row | Changed by relocation. The four trigger conditions and the description of what the reference covers are retained in the table row; the standalone heading is gone. |
| (new) | `SKILL.md`, "Phase map" | Added. Navigation only: one line per phase file, the three routes, and the runtime-phase warning. No instruction lives only here. |
| (new) | `SKILL.md`, "Conditional references" | Added. Navigation only, one line per reference. |
| (new) | `SKILL.md`, "When something is missing or a check cannot run" | Added. The fixed result vocabulary, the placeholder rule and the collision rule, which the baseline carried scattered across the runtime section, the write rules and the closing section. No new obligation. |
| (new) | `SKILL.md`, "Stopping" | Added. The baseline had no stopping condition. It states when the work is finished and when to hand back, drawn from the obligations already in the phases. |
| (new) | [`assets/completion-summary.md`](../assets/completion-summary.md) | Added. The terminal-summary template with four worked examples. |
| (new) | [`references/phase-mapping.md`](phase-mapping.md) | Added. This file. |

## Behaviour omitted or changed

Three items, named rather than left to be discovered:

1. **Split, not dropped.** Baseline lines 183-191 did two jobs in one paragraph: tell the user the result, and state what was and was not checked. The telling is now phase 06's summary. The accuracy obligation - that structural conformance and semantic quality are separate observations, that no available tool judges whether the ideas are any good or the attributions faithful, and that unverified artifacts are described as drafts with completion and receipt at `NOT_RUN` - is in phase 05's produced outputs, where the checking actually happens, and phase 06 requires one sentence of it in the summary. Both halves survive; neither is now the other's responsibility alone.
2. **Made specific.** The baseline's closing instruction was "tell the user: where the ledger is saved, what is newly proposed versus actually adopted, what remains open, and the one next action". Phase 06 requires the same four things plus the handoff link and the next action's owner, in a stated order, with the proposed-versus-adopted line marked as the one that is never omitted. The wording is gone; the obligation is preserved and tightened.
3. **Pointer duplicated on purpose.** The `recording-rules.md` trigger conditions now appear in two places - the `SKILL.md` conditional-reference row and one sentence in phase 03. That is deliberate: the conditions are needed both when deciding what to read and at the moment of writing frontmatter. It is the one place this refactor repeats itself, and it repeats a pointer, not an instruction.

Nothing else was removed. Every other baseline sentence appears in the new layout with its meaning intact, and the great majority appear verbatim.

One obligation is **added** rather than relocated, and is named here because it is new: a blocked or partial route must save whatever record it has where it was authorized to save it, and read it back at phase 05, before the summary. The baseline described blocked conditions as things to report but never said where the report was written. Phase 06 makes the gap operative, because it must link a path that resolves.

## Identities and references preserved

The four phase identities - Recover, Explore, Record, Focus - keep their names, their order and their meaning, and they are the same four the managed-runtime checkpoint contract names. Every link that existed in the baseline still resolves, re-pointed only for depth: `assets/…` and `references/…` from `SKILL.md` become `../assets/…` and `../references/…` from a phase file, and each is also linked directly from `SKILL.md` so that no resource sits more than one level from the file the client always loads. Backtick-quoted paths in the baseline become markdown links where they are now navigation. Eval case IDs 0 to 11, their fixtures and the trigger split are unchanged; new cases take new IDs.

[`scripts/check_artifact.py`](../scripts/check_artifact.py) is unchanged and is still named by no `SKILL.md` and no reference. This refactor deliberately does not wire it into a phase file - that would extend an existing Python helper's authority, which the workspace language rule forbids - and does not delete it, which is the package owner's decision. It is listed as a follow-up.

## Runtime phases versus package-local steps

[`references/managed-runtime.md`](managed-runtime.md) defines exactly four phases, each with its own checkpoint `content` fields: Recover, Explore, Record, Focus. Files `phase-01` to `phase-04` are those four, one to one, and this refactor changes nothing about the checkpoint interface, the phase names, the challenge handling or the routed handoff-only path.

`phase-05-readback.md` and `phase-06-completion-summary.md` are **package-local steps, not runtime phases**. Neither may be supplied as a checkpoint `phase` value, and neither adds a phase to the runtime's vocabulary. They are numbered 05 and 06 because that is the order they are reached in, per the authoring template's file-naming rule. `SKILL.md`'s phase map and each file's classification line say so, because a numbered file in a `phases/` directory otherwise reads as a phase the runtime knows about.

Phase 05's content is the baseline's own "Before you call it done" obligations, which were never runtime phases either - they are the closing discipline of the Record and Focus writes, in one file so that neither phase repeats them.

## Phase 06 classification: a proposal, not an adoption

The authoring contract classifies the five creator phases and the evaluator's phases and tasks as Enforced. It classifies no brainstorm phase at all. So this package labels none of its phases Enforced - not the four runtime phases, and not phase 06 - and the classification line of each file states the record that actually governs it.

For phase 06 specifically, the proposal put to the contract's owner, with the fact that decides it:

Completion evidence is what an Enforced item needs: something inspectable, somewhere it lives, someone who writes it, and a condition that makes it stale. Phase 06 has two halves with different answers. **Saving the record and reading it back** has that evidence - files at selected destinations with final digests - and it is already required, by phase 03, phase 04 and phase 05, on every route including a blocked one. **Presenting a short terminal summary** creates no separately bound artifact. A client may retain it in session history; that does not make it a runtime receipt, and the managed runtime publishes and reads back its own receipt independently of anything printed here.

- **Option A - Enforced.** Classify phase 06 Enforced on the strength of the save-and-read-back precondition its inputs require, and accept that the presentation half carries no completion evidence. Honest only if the classification says which half the evidence covers.
- **Option B - Optional presentation step over obligations that already exist.** Classify phase 06 Optional. Its retained-evidence obligations stay where they already are, in phases 03, 04 and 05, and the summary is a presentation convention with no evidence claim.

Option B matches the evidence rule this package applies elsewhere, and it avoids making one step both the producer and the presenter of its own evidence. It is put as a proposal either way; the owner decides. **No runtime check exists for phase 06, and none is proposed by this change.** Markdown does not enforce progression; if the owner wants a check, it is a compiled DevForge CLI requirement routed to the integration owner.

## `phases/` and the authoring contract

The contract's per-skill structure lists `SKILL.md`, `references/`, `assets/`, `scripts/`, `agents/openai.yaml` and `evals/`. `phases/` is not in that list. Two facts about that:

- The compiled installer and exporter select files by exclusion - `evals/`, `history/`, `__pycache__/`, `*.pyc`, `provenance.json` - rather than by an allowlist. `phases/` therefore installs and exports with the rest of the runtime package. The observed evidence for this package is in the pull request.
- This package uses `phases/` as a package-local structure. It is **proposed** for the contract's per-skill structure list and is not yet in it. That proposal belongs to the contract owner; this package does not edit `docs/mvp/` and makes no claim that the addition has been accepted. The Claude `devforge-project-expert-creator` package raised the same proposal.
