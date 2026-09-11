# Phase 03: Design

**Classification:** Enforced, per the skill-authoring contract. **Applies:** whenever a candidate will be authored or enhanced; skipped only by a reuse result.

## Purpose

State the expectations before the candidate exists, so the specification is not a description of whatever got written.

## Needed inputs

The intake record and the selection decision from phases [01](phase-01-intake.md) and [02](phase-02-selection.md), the grounding sources for the target kind, and - for an enhancement - the accepted specification and the frozen baseline already recovered.

## Substantive work

Derive the working design document from [assets/skill-design-spec.md](../assets/skill-design-spec.md) - copy it to the project's artifact location and fill it there. Never fill the package template in place. Populate it from the sources you recovered in intake; Q&A is for the material gaps that remain, not for facts already on disk.

Ask one to three related questions per round, only where the answer changes the design. Group related questions rather than sending them one at a time. Keep supplied requirements, your own proposed defaults and unresolved choices visually distinct - silence is not approval, and a default you invented is not a requirement the user gave you. Carry accepted classifications and settled decisions forward instead of reopening them; do not reopen a settled decision because a newer source appeared, note the conflict and let the user resolve it. For a genuinely new, undecided workflow item, capture whether it is optional or whether its completion is required before its dependent action. [Interview guide](../references/interview-guide.md) has the question set, the expert-spec content checklist, and how to record an enforcement requirement without claiming enforcement exists.

### Shape of the workflow you are designing

Decide, from the work itself, whether the target is a multi-step workflow or a single body of guidance:

- **A multi-step workflow skill** gets a phase map in its design: one row per phase with the package-relative phase file it will live in, when that phase applies, the inputs it needs, the artifacts it produces, and the one immediate continuation from it. State the explicit start phase and the finish phase, and make the finish a reporting and handoff phase that saves the detailed record and then presents a short summary. [assets/phase-file.md](../assets/phase-file.md) is the shape of each produced phase file.
- **A reference-only expert** - a body of decision guidance with no ordered steps - gets no phases at all. Do not invent ceremony to reach a phase count, and do not force a count in either direction: the right number is the number of distinct pieces of work with distinct inputs and outputs.

For an enhancement of a skill whose workflow is currently inline, plan the mapping now: every existing section to the phase file that will carry it, what stays in the entry point, and any sentence whose behaviour is omitted or changed. That mapping is authored in the next phase and recorded in the change record; behaviour, accepted decisions, stable IDs and the meaning of every reference are preserved unless a change is explicitly authorised and explicitly identified.

### Formal outputs of the design

The expert specification (XSPEC, from [assets/expert-spec.md](../assets/expert-spec.md)) and the proposed acceptance cases that go with it. [assets/evaluation-cases.md](../assets/evaluation-cases.md) is the starting set of cases for the skill you are about to write - carry them into the specification's acceptance-expectation rows and, later, into the evaluator handoff. You propose them. You do not run them, and a proposed case is not an observation.

For factual API guidance, research the version the project actually approved and record the source URL, the retrieval date, the applicable package version and what you specifically verified. Where you could not verify, the claim stays unresolved rather than becoming confident prose.

## Produced outputs

The filled working design document at the project's artifact location, the expert specification with independently stated acceptance expectations, the phase map for the target when it has one, and the recorded classification answers and open questions.

## Next phase

Continue to [phase 04, authoring](phase-04-authoring.md) once the activation boundary, the inputs, the output, the core process and its branches, the material constraints and the destination are settled. An unanswered non-blocking question stays open and does not hold up the independent work; a consequential rule that needs an approval nobody has given stops the dependent part of the design and goes to [phase 06](phase-06-completion-summary.md) as a blocker.
