# Development language policy

Owner decision: 2026-09-09, with the phase/hook clarification of 2026-09-10 recorded below. This policy applies to framework-owned implementation in DevForge and DevForgeAI. It is the approved framework architecture, not a claim that Claude, Codex or their tools universally require Python.

## Rust framework authority and required Python evaluation

Compiled Rust in the DevForge CLI must implement every DevForgeAI phase, gate, validator, mutation broker and acceptance decision. Framework runtime, tooling, installers/exporters, hooks, helpers, tests and executable examples must use Rust, except for the specific required Python evaluation artifacts below. Other programming languages and convenience, temporary, provider or embedded-script exceptions are forbidden.

Skill evaluation must include a Python JSONL runner and deterministic graders as required build artifacts. They produce raw outputs and metrics. They cannot own trusted framework authority, mutate the candidate or its gates, or declare framework acceptance. Rust validates their evidence and owns acceptance; a Python grade is evidence, not an acceptance decision. The exception does not authorize implementing framework phases, validators, mutation brokers or gate logic in Python.

Bind the exact Python runner and grader files, Python/runtime and dependency selection, case inputs and grading criteria in a protected manifest alongside candidate/specification identities. Keep these selected artifacts outside evaluated-agent write access. Record machine-readable case identities, actual outputs, metrics, diagnostics and execution statuses; missing results are not zero or success, and prose is not an executed benchmark. Before applying accepted criteria, Rust must check selected identities, output format and required coverage. Missing, changed, malformed or incomplete evidence cannot authorize acceptance.

Conversational instructions, documentation, data and declarative configuration may use Markdown, JSON, YAML and TOML. These formats do not permit hiding non-Rust framework logic in code blocks, command strings, hook declarations or configuration. Reading another project's source, describing an external technology stack, or retaining historical source/evidence does not turn that material into framework-owned implementation.

Standard command invocations that run existing tools are operational use. Invoking Cargo or an unchanged existing check is allowed within the task's authority. This does not permit implementing framework logic in shell commands, Python snippets or another language under the label of an invocation.

## Phases, hooks and skill content

Owner clarification: 2026-09-10. "Rust implements phases" means that Rust owns phase state, phase transitions and the mechanical checks required before a dependent action is permitted. The skill performs the reasoning inside a phase: questions and answers, context selection, authoring, and semantic review of the result. AI judgments are evidence for a Rust decision. Rust checking a review record's identity, format and required coverage validates evidence; it does not make Rust a semantic reviewer.

The integration chain is: a supported provider hook event (Claude or Codex) or a GitHub event invokes the selected Rust CLI, the CLI executes the check, and its result allows or refuses the dependent operation. Provider hook declarations and direct command invocations are wiring; the logic they invoke must be Rust. GitHub workflow checks run on GitHub events and block a merge only where a branch rule requires them. Local Git hooks run on a developer machine, are not distributed through the repository, and can be bypassed; name each surface accurately. A hook declaration alone does not show that a client supports, enables or honors the event. Verify each provider's actual interception and blocking behavior before describing it as enforcement, and report an unavailable integration as unavailable. A suggested command or an ignored exit status is not a gate.

Prompt instructions guide behavior and can be missed or overridden by other context, so they are not a dependable enforcement boundary on their own. This is not a claim that models always ignore instructions. Skills therefore must not contain ceremonial enforcement: repetitive mandatory status narration, simulated advance/complete sequences, self-attested PASS labels, or instructions presented as enforcement without an actual blocking mechanism behind them.

Preserve useful skill content: task instructions, accepted requirements, scope, user decisions, source grounding, output formats, explanations, decision criteria, the relevant command, and real handoffs. The requirement is to move real enforcement into code, not to turn every sentence, optional task or administrative convention into a Rust gate. A gate is added only to protect a concrete accepted requirement at an actual transition; name the action it controls, the input or evidence it checks, and its observable allow/refuse behavior, and use the smallest existing mechanism. Event-triggered checks are within MVP scope. Scheduling, automatic receiver invocation and background repair or orchestration remain post-MVP.

The language boundary above is unchanged: the Python JSONL runner and deterministic graders remain required evaluation artifacts that produce evidence and metrics, framework authority remains Rust, and existing nonconforming framework Python remains a scoped migration obligation. This section records the approved architecture; it does not claim that every provider hook or phase interception is implemented or observed.

## Protect the trusted implementation

Keep the trusted Rust executable and its source, selected revision and build inputs outside evaluated-agent write access. Digest-pin the selected actual binary and its source identity/build inputs in a trusted location outside the writable candidate. Validate evidence against that selection and reject mismatches, substituted binaries or rebuilt weakened binaries even if they report the same version. Protecting only the executable while allowing the evaluated agent to change its source or rebuild inputs is insufficient. Compilation alone does not protect the trusted boundary.

Protect governing policy, expected digests and acceptance records from evaluated-agent writes as well. The trusted path must verify selected binary/source and governing identities before authority-bearing execution and acceptance, rejecting a mismatch. A candidate cannot edit the expected hash or approve a replacement binary. Only the authorized integration owner may review and select a new identity, preserving the previous evidence.

## Required migration and preserved evidence

Existing Python framework logic must be ported into the DevForge CLI in Rust. Existing non-Rust implementation outside the approved runner/grader scope, including the Python POC fixture applications, is legacy/noncompliant and requires Rust migration. See the [POC scope](POC.md) for the current implementation. Preserve source, tests and evidence; the policy does not claim the legacy implementation has become Rust. Running unchanged existing tools and checks remains allowed within the task's authority while migration is outstanding. Do not add or extend non-Rust framework logic.

Migration is mandatory but requires its own authorized implementation scope, owner and acceptance criteria. This documentation task does not perform migration, delete legacy code, remove or weaken tests/gates, edit frozen specifications or acceptance evidence, or change installed packages. Report language compliance separately from test results, native behavior and acceptance. The policy is an implementation requirement; prose alone is not automatic CI or runtime enforcement.

## Selected contracts and frozen work

The [skill authoring contract](mvp/skill-authoring-contract.md) preserves each assignment's selected revisions and bytes. An older instruction assigning trusted framework logic to Python conflicts with this policy. Stop the affected new implementation and report the conflict to the integration owner for an explicitly selected correction or migration scope. Continue unaffected authorized work and unchanged existing checks. Do not silently refresh contracts, repin a running acceptance campaign, or reinterpret historical results.
