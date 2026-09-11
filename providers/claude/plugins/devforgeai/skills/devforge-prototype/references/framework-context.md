# Framework context

This package is the Claude implementation of SKILL-004, `devforge-prototype`, in the DevForgeAI roster. DevForgeAI is an adaptive, spec-driven software engineering framework in local POC development. Nothing in this package establishes that the framework, this skill, or anything it produces has been evaluated.

Everything below is a narrowed restatement of the framework's shared contracts, selected for the situations this skill actually meets. It restates; it does not extend or waive them. Where the two differ, the contracts govern. `derivation.json` records the exact sources and sections this was distilled from.

## Who owns what

DevForgeAI owns conversational methodology, skills, and project expertise. The companion DevForge CLI - a separate compiled Rust program - owns the protected runtime, the deterministic gates, structural checks and installation.

Stated precisely, because it decides what may be written into a skill: Rust owns phase state, phase transitions, and the mechanical checks that must pass before a dependent action is permitted. The skill owns the reasoning inside a phase - the framing, the context selection, the measurement design and the semantic judgement about a result. An AI judgement is evidence for a decision the CLI makes; it is not the decision.

The consequence for skill content is a prohibition, not a style preference. Do not write repeated phase acknowledgements, self-issued PASS labels, simulated advance or complete sequences, or instructions presented as enforcement when nothing blocks anything. A suggested command is not a gate, and an exit status nobody reads is not a gate either.

What to keep is everything substantive: task instructions, accepted requirements, scope, user decisions, source grounding, output formats, explanations, decision criteria, the relevant command, and real handoffs. The requirement is to move real enforcement into code, not to strip explanation out of skills.

## What the CLI actually offers this workflow today

Confirmed present in `devforge --help` on the companion repository's debug build, observed 2026-09-10. Inspect the selected executable's own `--help` before relying on any row - a command's existence here is a description of the current integration route, not evidence it was run.

| Command | What it does, and its limit for an experiment |
| --- | --- |
| `devforge isolate --project <abs-project> --runtime claude -- claude` | Runs a client with `/` mounted read-only and only `--project` writable. It bounds writes to the **whole project**, not to an experiment subpath, so it does not implement an experiment fence. It is the closest existing containment and worth naming as that. |
| `devforge check --project <abs-project> --policy <abs-policy>` | Checks approved dependencies, layout, tooling pins and expert provenance against an external policy. It says nothing about an experiment, a plan, a threshold or a measurement. |
| `devforge init` / `red` / `green` / `accept` / `verify` / `status` | The story-development test gate: baseline, an observed test-only assertion failure, passing tests with the exact RED test bytes, and an accepted snapshot. These belong to `devforge-develop` and to hardening work **after** a prototype is adopted. Running them against experiment code is not part of this workflow, and prototype code is precisely the code that has not earned them. |
| `devforge expert prepare / bind / status` | Project expertise grounding and freshness. Unrelated to an experiment except as a source of project context. |

## Integrations this workflow would need and does not have

Record these as requirements for the integration owner. None of them exists, and none of them is implemented by this skill.

- **A sub-project experiment fence.** No command restricts writes to a declared experiment subpath, or refuses a write outside it. `isolate` bounds the project; the fence inside it is currently observed by the person doing the work, not enforced.
- **A pre-execution plan freeze.** No command records an XPLAN's bytes before measurement in a location the evaluated agent cannot rewrite. Hashing the plan yourself records which bytes you had; it does not establish that they preceded the evidence to anyone who does not already trust you.
- **A promotion check.** Nothing refuses a prototype file that appears under a policy source root, and nothing ties a prototype-report's disposition to whether hardening actually happened.
- **Threshold immutability.** Nothing detects a threshold that changed between the plan and the report. That comparison is currently a reader's job.

Recording a requirement is design input. It is not evidence that any client supports, enables or honours such a check, and the honest status of every row above is that the gap is open.

## Resolving paths

Two roots, and conflating them is how a lookup quietly fails.

This package's own resources resolve against the directory holding the loaded `SKILL.md`, wherever the client installed it. The consuming project's inputs, prototype and outputs resolve against the project root supplied for the task. The shell working directory is neither by default, and Markdown links imply no working directory.

Prefer absolute paths for project inputs and outputs in tool calls. Never hard-code a developer's home directory into a package, and never require the DevForgeAI repository - or its `docs/mvp` tree - to be present at runtime. That is why the templates this skill needs are copied into `assets/` rather than linked upstream.

## Roles that stay separate

The user initiates each skill and each command. This skill runs the experiment and reports it. The skills that own the affected documents - define-product, design, architect, plan, change - decide what the finding means for their artifacts. An integration owner handles installation, export, hooks and shared contract changes. Hardening a prototype into production code is `devforge-develop`'s work under a planned story, behind the real gate.

A user authorising several responsibilities in one assignment does not merge them. An experimenter cannot supply the independent judgement that the experiment's own design was sound, and running a measurement is not accepting its consequence.

## Result vocabulary

Fixed, and never blended into a single score or percentage.

| Term | Means |
| --- | --- |
| `NOT_EVALUATED` | Behaviour nobody has evaluated. |
| `NOT_RUN` | Planned, unattempted. |
| `COULD_NOT_RUN` | A required observation was blocked; the actual cause is recorded. |
| `NOT_APPLICABLE` | Excluded from the stated scope, with the reason. |
| `NOT_VALIDATED` / `NOT_OBSERVED` | Contract-header states for admission and for native activation or delivery. |

The absence of an error is not a pass. A hash binding or package check proves which inputs were referenced, never that behaviour is correct. Preserve earlier reports' original labels; explaining a later reclassification is fine, rewriting their history is not.

## Package shape and packaging rules

A skill package is `SKILL.md` plus optional `references/`, `assets/`, `scripts/` and `evals/`. Create optional resources only when they are useful, and link each at the point that needs it rather than loading everything by default.

`evals/` stays in the authored source and is omitted from installed copies and runtime exports; `assets/` and `references/` do ship. Eval fixtures must be reproducible from source, and paths inside `evals/evals.json` resolve relative to that `evals` directory and stay within it.

Canonical Claude framework sources live under this repository's `providers/claude/plugins/devforgeai/skills/<name>`. Project-local installations and exported plugins are generated copies, never alternative authoring sources. For every shared template or contract copied into a package, record the source path and exact revision, the destination and digest, the transformation and the refresh condition; `references/derivation.json` is that record.

Do not modify sibling gates, shared contracts, installer policy, the accepted roster, or another skill so that this candidate passes. Report a contract or integration gap to its owner and continue the independent work.

## Bounded delivery

State the finish line that matches the request and stop there. For this skill the finish line is a bounded experiment with its plan, its observations and an honest account of what remains unmeasured - not a growing chain of follow-on experiments, and not a hardening pass nobody asked for.

Carry settled decisions forward instead of asking again. When two successive attempts address the same blocker with no new evidence, stop that remedy and report the concrete alternative. Put optional improvements outside the delivery path, and never call a required observation "ceremony" in order to finish cheaply - the way to reduce scope is an accepted scope change, not a quietly weakened threshold.
