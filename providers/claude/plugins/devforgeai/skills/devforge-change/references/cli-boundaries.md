# What the CLI can and cannot tell you about a change

Read this before naming any `devforge` command in a change-request, and before writing a refresh-plan row that assumes something will be checked.

DevForgeAI owns the conversation. The companion DevForge CLI is a separate compiled Rust program that owns the mechanical checks. This skill needs both kinds of fact and must never present one as the other: a command's result says exactly what its own predicate says, which is always narrower than the phase it supports.

## Before relying on any row here

Inspect the selected executable's own `--help` first. The rows below were read from a specific build at authoring time and are recorded so a later reader can tell a description from an observation; they are not a guarantee about the binary in front of you. A subcommand that has been added, renamed or removed since makes the row wrong, and the `--help` output is the authority.

Use absolute paths for `--project` and `--policy`. The assignment supplies them. Every
command below takes that shape:

```text
devforge <subcommand> --project <abs-project> --policy <abs-policy> [--state <abs-state>]
```

These are illustrations of an operator's invocation, not something this skill runs. Do not go looking for a more permissive policy, and never edit a policy, a gate or its pins so that something passes - a check that refuses is telling you something, and it goes to its owner.

## Commands that exist

This is the subset a change assessment has any reason to cite. The binary exposes others - `init`, `red`, `green`, `accept`, `isolate` and the `delivery` group - which belong to the TDD gate and the managed runtime and are not part of this workflow. Their absence from this table means they are out of scope here, never that they do not exist.

| Owner and action | Command | What it proves, and what it does not |
| --- | --- | --- |
| Operator or worker recovers grounding context | `devforge expert prepare --project <abs-project> --policy <abs-policy>` | Loads the external policy and project and returns grounding inputs. Read-only. Invalid or missing input refuses. It is not proof that any phase completed and it reports nothing about a change. |
| Operator checks a bound expert's freshness | `devforge expert status --project <abs-project> --policy <abs-policy>` | Reports `MISSING`, `CURRENT` or `STALE` **against the recorded binding for that one expert directory**, plus a separate behavioural status that stays `NOT_EVALUATED` until a real terminal evaluation is recorded. This is the only staleness predicate the CLI implements, and its scope is one bound expert, not a project's artifacts. |
| Integration owner records a binding | `devforge expert bind --project <abs-project> --policy <abs-policy> --expert <declared-relative-expert-dir>` | Records the exact policy, upstream document and package digests plus binding history in the project's expert directory. It explicitly leaves behaviour `NOT_EVALUATED`. Missing input or a collision refuses. Not this skill's command, and not the change author's. |
| Operator gates a project candidate | `devforge check --project <abs-project> --policy <abs-policy>` | Checks approved dependencies, layout, tooling pins and expert provenance against the external policy. Its own help says it does not certify semantic behavior. It does not read a change-request, and it knows nothing about this workflow. |
| Operator inspects durable phase state | `devforge status --project <abs-project> --policy <abs-policy> --state <abs-state>` | Reports the recorded state of an open RED/GREEN run. Useful to this skill only as a way to find out whether an in-flight run exists that a change would invalidate. It does not evaluate the change. |
| Operator verifies an accepted snapshot | `devforge verify --project <abs-project> --policy <abs-policy> --state <abs-state>` | Compares bytes and modes of the current tree against the accepted snapshot. It establishes that a candidate did or did not drift from what was accepted. It says nothing about whether the accepted thing is still correct after a governing change. |

Each of these accepts its flags at the leaf subcommand, as its own `--help` output shows. All of them are the operator's or integration owner's to run. This skill reads their recorded results when an owner supplies them; preparing a proposal is not authority to run them, and a command you did not run is not evidence.

## What has no implemented check

These are the parts of this workflow that nothing currently enforces. Each is a real requirement of the specification and each is missing an integration, so record it as a requirement with its evidence and its owner rather than describing it as a gate.

| Requirement | Missing integration |
| --- | --- |
| Walk an artifact's declared `upstream` edges and enumerate direct and transitive dependents | No command reads the `devforge.artifact/v1` envelope or resolves its `upstream` entries. The graph in a change-request is produced by reading documents, and its coverage is exactly as good as the reading. |
| Mark an affected artifact, evaluation or installed copy stale when a governing source changes | `devforge expert status` covers one bound expert against its own recorded binding. Nothing marks a story, contract, report or candidate stale, and nothing propagates staleness along an edge. |
| Block a dependent action until the change-request's required new evidence exists | Nothing reads a change-request. The refresh plan's `State` column is a record of intent; it permits and refuses nothing. |
| Detect that an installed or exported copy has diverged from the source it was generated from | Installation and export are generated copies. No command compares an installed skill copy against its provider source, so "the installed copy still needs refreshing" is an assertion to verify by reading bytes, not a reported status. |
| Detect a concurrent writer on a worktree, branch or destination | There is no lease service and no ownership check. Collision detection here means reading the assignment record and the destination and reporting what you find. |

Route each of these to the integration owner as a recorded requirement: the action that must wait, the evidence to be checked, where that evidence lives and what invalidates it, and the intended allow-or-refuse behaviour. Recording the requirement is design input. It is not evidence that any client supports, enables or honours such a check, and feasibility stays unknown until that owner confirms it.

Do not substitute prose for the missing check. A phase acknowledgement, a self-issued PASS, or a simulated command sequence written into a proposal is worse than the honest gap, because it reads as enforcement to everyone downstream.

## Observation recorded at authoring time

`devforge --help`, `devforge expert --help`, `devforge delivery --help` and the five leaf `--help` outputs above were read on 2026-09-10 UTC from a locally built development binary reporting `devforge 0.1.0`. That build is a fact about one machine at one moment: it is not a released identity, and it is not evidence that any consuming project has that binary, that policy, or any binary at all. Where the executable is unavailable, every row above is `COULD_NOT_RUN` for that project with the cause recorded - not `NOT_APPLICABLE`, and certainly not a pass.
