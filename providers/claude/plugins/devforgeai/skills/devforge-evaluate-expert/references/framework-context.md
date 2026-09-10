# Framework context

This package is the Claude implementation of SKILL-008, `devforge-evaluate-expert`, in the DevForgeAI roster. DevForgeAI is an adaptive, spec-driven software engineering framework in local POC development. Nothing in this package establishes that the framework, this skill, or anything it evaluates has itself been evaluated.

This is a narrowed restatement of the framework's shared contracts, selected for the situations this skill actually meets. Where it and the packaged contracts differ, the contracts govern; `derivation.json` records what each file was distilled from.

## Who owns what

DevForgeAI owns conversational methodology, skills and project expertise. The companion DevForge CLI - a separate compiled Rust program - owns the protected runtime, the deterministic gates, structural checks and installation.

The split decides what may be written into a skill. Rust owns phase state, phase transitions and the mechanical checks that must pass before a dependent action is permitted. The skill owns the reasoning inside a phase: selecting context, designing the experiment, reading the evidence and judging the result. An AI judgement is evidence for a decision; it is not the decision.

The consequence is a prohibition, not a style preference. No repeated phase acknowledgements, no self-issued PASS labels, no simulated advance or complete sequences, and no instruction presented as enforcement when nothing blocks anything. A suggested command is not a gate, and an exit status nobody reads is not one either.

Everything substantive stays: the task instructions, the accepted requirements, scope, user decisions, source grounding, output formats, decision criteria, the relevant command and the real handoffs.

## The evaluation exception, and its limit

The framework's language policy assigns every phase, gate, validator, mutation broker and acceptance decision to compiled Rust, with one exception: a Python JSONL evaluation runner and deterministic graders are required build artifacts. They produce raw outputs and metrics. They cannot hold framework authority, mutate a candidate or its gates, or declare acceptance.

`scripts/run_cases.py` and `scripts/graders.py` are that exception and stay inside it. [The runner interface](runner-interface.md) states the boundary precisely and explains why some grader assertions look like checks a gate would perform while remaining evidence.

Two capabilities this workflow would otherwise use are absent from the compiled CLI:

- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.**
- **Protected-manifest custody for the evaluation runner** - binding the runner, grader, runtime and case identities outside evaluated-agent write access and verifying them before acceptance criteria apply - **is not implemented in the DevForge CLI.**

Both are evaluation prerequisites owned by the DevForge integration owner. [Missing DevForge CLI capabilities](missing-rust-capabilities.md) has the procedure for working without them and the labelling that keeps the gap visible.

## Roles that stay separate

The creator authors. This skill evaluates and returns bounded findings. The user initiates each skill and each command. An integration owner handles installation, export, hooks and shared contract changes.

An author cannot supply an independent judgement of its own candidate, and a user authorising several responsibilities in one assignment does not merge them. Package identity, structural binding, behavioural evidence, human acceptance and operational installation are five separate facts; establishing one says nothing about the others.

## Resolving paths

This package's resources resolve against the directory holding the loaded `SKILL.md`, wherever the client installed it. The candidate, the consuming project, the evidence directory and the external authority resolve separately from the assignment. The shell's working directory is none of them, and Markdown links imply no working directory.

Claude exposes `${CLAUDE_SKILL_DIR}` and, for plugin skills, `${CLAUDE_PLUGIN_ROOT}`. They exist and may be useful, but derive the root from the loaded `SKILL.md` path rather than depending on them. Never hard-code a developer's home directory, and never require the DevForgeAI repository - or its `docs/mvp` tree - to be present at runtime. That is why the templates this skill needs are copied into `assets/`.

## Result vocabulary

Fixed, and never blended into a score or a percentage.

| Term | Means |
| --- | --- |
| `NOT_EVALUATED` | Behaviour nobody has evaluated. |
| `NOT_RUN` | Planned, unattempted. |
| `COULD_NOT_RUN` | A required observation was blocked; the actual cause is recorded. |
| `NOT_APPLICABLE` | Excluded from the stated scope, with the reason. |
| `NOT_VALIDATED` / `NOT_OBSERVED` | Contract-header states for admission and for native activation or delivery. |

The absence of an error is not a pass. A hash binding or a package check proves which inputs were referenced, never that behaviour is correct. Preserve earlier reports' original labels; explaining a later reclassification is fine, rewriting their history is not.

## Historical identities

The DevForge managed-runtime workflow IDs `skill-builder` and `skill-validator` belong to an older protocol on the Codex side, as do the managed `advance` / `resume` / `complete` helper sequence, the Codex `--manual-experts-only --manual-evidence` installation mode, its adoption-evidence predicate, and the accepted Routine/Full validation policy for manual mode. They are preserved history in the Codex packages, not aliases or capabilities of this one, and no Claude adoption path is established by any of them. Automated scheduling, automatic receiver invocation, and retry or repair loops remain deferred, with their recorded failures preserved rather than resolved by this port.

## Bounded delivery

State the finish line that matches the request and stop there. For this skill the finish line is a saved evaluation with an honest account of what was and was not observed - not a growing chain of prerequisites, and not a second campaign to close a gap that belongs to another owner.

Carry settled decisions forward instead of asking again. When two successive attempts address the same blocker with no new evidence, stop that remedy and report the concrete alternative. Never call a required observation "ceremony" in order to finish cheaply: the way to reduce scope is an accepted scope change, not a quietly weakened expectation.
