# Framework context

This package is the Claude implementation of SKILL-005, `devforge-architect`, in the DevForgeAI roster. DevForgeAI is an adaptive, spec-driven software engineering framework in local POC development. Nothing in this package establishes that the framework, this skill, or anything it produces has been evaluated.

Everything below is a narrowed restatement of the framework's shared contracts, selected for the situations this skill actually meets. It restates; it does not extend or waive them. Where the two differ, the contracts govern. `derivation.json` records the exact sources this was distilled from.

## Who owns what

DevForgeAI owns conversational methodology, skills, and project expertise. The companion DevForge CLI - a separate compiled Rust program - owns the protected runtime, the deterministic gates, structural checks and installation.

The split is worth stating precisely, because it decides what may be written into a skill or into a contract this skill produces. Rust owns phase state, phase transitions, and the mechanical checks that must pass before a dependent action is permitted. The skill owns the reasoning inside a phase: the questions, the context selection, the comparison of alternatives, the authoring, and the semantic judgement about the result. An AI judgement is evidence for a decision the CLI makes; it is not the decision.

The consequence is a prohibition, not a style preference. Do not write repeated phase acknowledgements, self-issued PASS labels, simulated advance or complete sequences, or instructions presented as enforcement when nothing blocks anything. A suggested command is not a gate, and an exit status nobody reads is not a gate either. Prompt instructions guide behaviour and can be missed or overridden by other context, which is exactly why real enforcement lives in code.

What to keep is everything substantive: task instructions, accepted requirements, scope, user decisions, source grounding, output formats, explanations, decision criteria, the relevant command, and real handoffs. The requirement is to move real enforcement into code, not to strip explanation out of skills or contracts.

## Recording an enforcement requirement

An architecture contract routinely contains rules that should block something - a forbidden dependency direction, a required test before a merge, a prohibited package substitution. Recording such a rule is design input. It is not evidence that anything checks it.

For each rule that must block a dependent action, record:

| Field | Content |
| --- | --- |
| Covered rules | The RULE, ADR or API IDs this route protects. |
| Requirement and protected action | The precise condition, and the action that must wait for it. |
| Observable evidence | What could actually be inspected. Distinguish proof of completion from a self-reported marker. |
| State and freshness | Where the evidence lives, who writes it, how it binds to this contract revision, and what invalidates it. |
| Intended allow or refuse behaviour | The exact conditions for permitting or refusing. A warning is advisory, not a refusal. |
| Missing evidence and errors | Intended behaviour for missing or stale evidence, timeouts and unavailable dependencies. |
| Owner | Integration owner. The check itself is compiled into the DevForge CLI and invoked by whatever wiring that owner selects. |
| Feasibility | Unknown until the integration owner confirms it, or their recorded answer. |
| Status | Requirement recorded. No gate is implemented, activated or executed by this skill. |

Where a requirement cannot be met in the target environment, record "Enforcement requested; not confirmed available" and propose a feasible alternative for discussion. Do not silently downgrade a required rule into advisory prose, and do not write phase narration or a simulated command sequence into the contract as a substitute.

## Roles that stay separate

The architect authors a proposed contract and records the user's actual decisions. The user adopts. An external policy owner makes an adopted revision effective as DevForge policy. An integration owner handles installation, export, hooks and shared contract changes. An independent evaluator evaluates skills and returns bounded findings.

A user authorising several responsibilities in one assignment does not merge them. Document adoption, structural freshness, behavioural evidence, external policy effectiveness and human acceptance are separate facts. Establishing one says nothing about the others.

## Command boundaries

Use absolute paths for the project and the policy; the assignment supplies them. Inspect the selected executable's own `--help` before relying on any of this. Each row states what the command actually proves, which is always narrower than the phase it supports.

| Owner and action | Command | What it proves, and what it does not |
| --- | --- | --- |
| Operator gates a project candidate | `devforge check --project <abs-project> --policy <abs-policy>` | Checks approved dependencies, layout, tooling pins and expert provenance against the external policy file. The current POC dependency check is a synthetic contract check, not a NuGet or npm adapter; it resolves no real package graph and certifies no semantic behaviour. |
| Operator recovers grounding context | `devforge expert prepare --project <abs-project> --policy <abs-policy>` | Loads the external policy and project and returns grounding inputs. Read-only. Invalid or missing input refuses. It is not proof that any phase completed. |
| Operator checks expertise freshness | `devforge expert status --project <abs-project> --policy <abs-policy>` | Reports `MISSING`, `CURRENT` or `STALE` against a recorded binding, plus a separate behavioural status that stays `NOT_EVALUATED` until a real terminal evaluation is recorded. |
| Operator runs the TDD gate | `devforge init`, `red`, `green`, `accept`, `verify`, `status` | Observe baseline, an actual test-only assertion failure, passing tests with the exact RED tests, and byte and mode integrity against an accepted snapshot. They are the story-level gate, not an architecture check. Not this skill's commands. |
| Integration owner installs or exports | The companion DevForge repository's installer script | Generates project-local copies or a plugin export. Installation is not activation, not evaluation and not acceptance. |

The four phases in `SKILL.md` are the workflow this skill performs. They are not CLI subcommands and no command above intercepts them. Do not present any of these as universal enforcement, and do not simulate a transition that no command performed.

## Missing integrations to name rather than assume

Two gaps are load-bearing for an architecture contract, and a contract that depends on either should say so:

- **Real stack and test adapters.** The POC's dependency and tooling checks are synthetic pins in a policy JSON. A rule asserting a package version, a lockfile state or a test command for a real ecosystem has no implemented adapter behind it.
- **Making an adopted contract effective as policy.** The external policy file is operator-owned. This skill does not write it, and an adopted contract revision does not become an active gate by being adopted. Hand the exact revision to the policy owner and record that step as pending until they confirm it.

Report a contract or integration gap to its owner and continue the independent work. Never modify a gate, a policy, a sibling skill or the accepted roster so that a candidate passes.

## Two roots

This package's own resources resolve against the directory holding the loaded `SKILL.md`, wherever the client installed it. The consuming project's inputs and outputs resolve against the project root supplied for the task. The shell working directory is neither by default, and Markdown links imply no working directory.

Prefer absolute paths for project inputs and outputs in tool calls. Never hard-code a developer's home directory into a package, and never require the DevForgeAI repository - or its `docs/mvp` tree - to be present at runtime. That is why the templates this skill needs are copied into `assets/` rather than linked upstream.

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

## Bounded delivery

State the finish line that matches the request and stop there. For this skill the finish line is a contract authored against the accepted requirements, with its identities and evidence recorded and an honest account of what remains unresolved - not a growing chain of prerequisites, and not a generalized platform for slices nobody asked about.

Carry settled decisions forward instead of asking again. When two successive attempts address the same blocker with no new evidence, stop that remedy and report the concrete alternative. Put optional improvements outside the delivery path, and never call a required check "ceremony" in order to finish cheaply: the way to reduce scope is an accepted scope change, not a quietly weakened gate.
