# Framework context

This package is the Claude implementation of SKILL-007, `devforge-project-expert-creator`, in the DevForgeAI roster. DevForgeAI is an adaptive, spec-driven software engineering framework in local POC development. Nothing in this package establishes that the framework, this skill, or anything it produces has been evaluated.

Everything below is a narrowed restatement of the framework's shared contracts, selected for the situations this skill actually meets. It restates; it does not extend or waive them. Where the two differ, the contracts govern. `derivation.json` records the exact sources and sections this was distilled from.

## Who owns what

DevForgeAI owns conversational methodology, skills, and project expertise. The companion DevForge CLI - a separate compiled Rust program - owns the protected runtime, the deterministic gates, structural checks and installation.

The split is worth stating precisely, because it decides what may be written into a skill. Rust owns phase state, phase transitions, and the mechanical checks that must pass before a dependent action is permitted. The skill owns the reasoning inside a phase: the questions, the context selection, the authoring, and the semantic judgement about the result. An AI judgement is evidence for a decision the CLI makes; it is not the decision.

The consequence for skill content is a prohibition, not a style preference. Do not write repeated phase acknowledgements, self-issued PASS labels, simulated advance or complete sequences, or instructions presented as enforcement when nothing blocks anything. A suggested command is not a gate, and an exit status nobody reads is not a gate either. Prompt instructions guide behaviour and can be missed or overridden by other context, which is exactly why real enforcement lives in code.

What to keep is everything substantive: task instructions, accepted requirements, scope, user decisions, source grounding, output formats, explanations, decision criteria, the relevant command, and real handoffs. The requirement is to move real enforcement into code, not to strip explanation out of skills.

When a design genuinely needs a dependent action blocked, record it as a requirement - name the action, the evidence to be checked, and the intended allow/refuse behaviour - and route it to the integration owner, who owns the Rust check and the provider wiring that invokes it. Recording the requirement is design input. It is not evidence that any client supports, enables or honours such a check.

## Roles that stay separate

The creator authors. An independent evaluator evaluates and returns bounded findings. The user initiates each skill and each command. An integration owner handles installation, export, hooks and shared contract changes.

An author cannot supply an independent judgement of its own candidate, and a user authorising several responsibilities in one assignment does not merge them. Package identity, structural binding, behavioural evidence, human acceptance and operational installation are five separate facts. Establishing one says nothing about the others.

## Resolving paths

Two roots, and conflating them is how a lookup quietly fails.

This package's own resources resolve against the directory holding the loaded `SKILL.md`, wherever the client installed it. The consuming project's inputs and outputs resolve against the project root supplied for the task. The shell working directory is neither by default. Markdown links imply no working directory.

Prefer absolute paths for project inputs and outputs in tool calls. Never hard-code a developer's home directory into a package, and never require the DevForgeAI repository - or its `docs/mvp` tree - to be present at runtime. That is why the templates this skill needs are copied into `assets/` rather than linked upstream.

## Grounding expertise

Ground a project expert in the actual goal or story, the accepted architecture, the real code, and the pinned dependencies. Keep the decisions and source versions the project actually made.

Record source URLs, the applicable version, the retrieval date, the specific claim supported, and the conditions that would make it stale. An unverified API claim stays a missing input rather than becoming confident guidance. A newer library release is a proposal for a controlled refresh; it is never permission to replace an approved stack.

Keep AI proposals separate from user decisions, and keep each at the strength it was actually given. A proposal recorded as a decision becomes a production constraint two skills later, and by then nobody can tell where it came from.

## The artifact envelope

Framework artifacts - the expert specification, the package record, the handoff - carry a `devforge.artifact/v1` YAML envelope. The `assets/` templates already contain it; these are the fields whose meaning matters when filling one in.

| Field | Meaning |
| --- | --- |
| `schema_version` | `devforge.artifact/v1`. A proposed schema for these documents, not the CLI's policy schema. |
| `artifact_id` / `artifact_type` / `project_id` | Stable identity, one of the declared types, and the project whose facts the document describes. |
| `revision` / `status` | Positive integer; `draft`, `in_review`, `accepted`, `superseded` or `retired`. |
| `created_at_utc` | Actual UTC creation time for this revision. |
| `producer` | Skill name and the exact loaded skill revision or digest. |
| `execution_ref` | The authority-selected session record and revision. Use `null` plus `missing_inputs` in pre-assignment bootstrap; its absence does not establish ownership. |
| `upstream` | Causal inputs: `artifact_id`, `revision`, `store`, `path`, `sha256`, and the stable section IDs actually relied on. |
| `evidence` | Locators for actual observations, source checks and external receipts. |
| `supersedes` | Prior artifact ID, revision and digest, or `null`. Retain the prior bytes. |
| `decision_ref` | The user's actual adoption or previously delegated authority; `null` while none exists. |
| `missing_inputs` | Explicit unresolved required information. |

Three rules about digests, because this is where these documents most often go wrong.

No artifact contains its own complete-byte digest. Hash a file only after its bytes are final, then put that digest in the document that references it - never in the file itself. A handoff does not list itself among its own outputs, and its own digest belongs in an external receipt or the terminal response.

A digest is only true while the bytes behind it are still reachable. If you are about to overwrite a file whose digest you cite, preserve the old bytes at a stable authorised location first and point the reference at the preserved copy. If you cannot preserve them, record that in `missing_inputs` and cite only what exists.

Every reference must resolve after your last write. Digests get repeated - the same file often appears in an output table, an upstream entry and an invalidation condition - and a stale copy in any one of them is the same defect as a wrong primary reference, just harder to notice. Read them all back, not only the first.

`producer.skill_revision` is the digest of the installed `SKILL.md` file's bytes: one file. It is not a digest of the package and not the plugin version, which can be identical across two different drafts and therefore identifies nothing. Say which one you have. Where nothing observable gives you the value, `unknown` is the honest entry.

A template placeholder left in a required field means the result is a draft and cannot be presented as ready. A missing fact goes in `missing_inputs`, never into template filler.

## Package shape and packaging rules

A skill package is `SKILL.md` plus optional `references/`, `assets/`, `scripts/` and `evals/`. Create optional resources only when they are useful, and link each at the point that needs it rather than loading everything by default.

`evals/` stays in the authored source and is omitted from installed copies and runtime exports. `assets/` and `references/` do ship - which is why reusable evaluation instructions for a generated expert belong in `assets/`, while the tests of this skill itself belong in `evals/`. Eval fixtures must be reproducible from source, and paths inside `evals/evals.json` resolve relative to that `evals` directory and must stay within it.

Canonical Claude framework sources live under this repository's `providers/claude/plugins/devforgeai/skills/<name>`. Project-local installations and exported plugins are generated copies, never alternative authoring sources. A provider source directory by itself is not a discovered installation. Edit only the assigned provider and skill; a project-specific expert needs its own explicit source-to-installation mapping rather than an inferred one.

For every shared template or contract copied into a package, record the source path and exact revision or preserved location and digest, the package-relative destination and digest, any transformation, and the refresh conditions. One maintenance record - `references/derivation.json` - is sufficient. Missing derivation metadata is a package correction; it is not permission to redesign the shared template.

Do not modify sibling gates, shared contracts, installer policy, the accepted roster, or another skill so that this candidate passes. Report a contract or integration gap to its owner and continue the independent work.

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

State the finish line that matches the request and stop there. For this skill the finish line is a candidate authored against a specification, with its identities recorded and an honest account of what remains unobserved - not a growing chain of prerequisites, and not a second design document.

Carry settled decisions forward instead of asking again. When two successive attempts address the same blocker with no new evidence, stop that remedy and report the concrete alternative. Put optional improvements outside the delivery path, and never call a required check "ceremony" in order to finish cheaply: the way to reduce scope is an accepted scope change, not a quietly weakened gate.
