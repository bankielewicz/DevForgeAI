# Development language policy

Owner decision: 2026-09-09. This policy applies to framework-owned implementation in DevForge and DevForgeAI. It is the approved framework architecture, not a claim that Claude, Codex or their tools universally require Python.

## Rust framework authority and required Python evaluation

Compiled Rust in the DevForge CLI must implement every DevForgeAI phase, gate, validator, mutation broker and acceptance decision. Framework runtime, tooling, installers/exporters, hooks, helpers, tests and executable examples must use Rust, except for the specific required Python evaluation artifacts below. Other programming languages and convenience, temporary, provider or embedded-script exceptions are forbidden.

Skill evaluation must include a Python JSONL runner and deterministic graders as required build artifacts. They produce raw outputs and metrics. They cannot own trusted framework authority, mutate the candidate or its gates, or declare framework acceptance. Rust validates their evidence and owns acceptance; a Python grade is evidence, not an acceptance decision. The exception does not authorize implementing framework phases, validators, mutation brokers or gate logic in Python.

Bind the exact Python runner and grader files, Python/runtime and dependency selection, case inputs and grading criteria in a protected manifest alongside candidate/specification identities. Keep these selected artifacts outside evaluated-agent write access. Record machine-readable case identities, actual outputs, metrics, diagnostics and execution statuses; missing results are not zero or success, and prose is not an executed benchmark. Before applying accepted criteria, Rust must check selected identities, output format and required coverage. Missing, changed, malformed or incomplete evidence cannot authorize acceptance.

Conversational instructions, documentation, data and declarative configuration may use Markdown, JSON, YAML and TOML. These formats do not permit hiding non-Rust framework logic in code blocks, command strings, hook declarations or configuration. Reading another project's source, describing an external technology stack, or retaining historical source/evidence does not turn that material into framework-owned implementation.

Standard command invocations that run existing tools are operational use. Invoking Cargo or an unchanged existing check is allowed within the task's authority. This does not permit implementing framework logic in shell commands, Python snippets or another language under the label of an invocation.

## Protect the trusted implementation

Keep the trusted Rust executable and its source, selected revision and build inputs outside evaluated-agent write access. Digest-pin the selected actual binary and its source identity/build inputs in a trusted location outside the writable candidate. Validate evidence against that selection and reject mismatches, substituted binaries or rebuilt weakened binaries even if they report the same version. Protecting only the executable while allowing the evaluated agent to change its source or rebuild inputs is insufficient. Compilation alone does not protect the trusted boundary.

Protect governing policy, expected digests and acceptance records from evaluated-agent writes as well. The trusted path must verify selected binary/source and governing identities before authority-bearing execution and acceptance, rejecting a mismatch. A candidate cannot edit the expected hash or approve a replacement binary. Only the authorized integration owner may review and select a new identity, preserving the previous evidence.

## Required migration and preserved evidence

Existing Python framework logic must be ported into the DevForge CLI in Rust. Existing non-Rust implementation outside the approved runner/grader scope, including the Python POC fixture applications, is legacy/noncompliant and requires Rust migration. See the [POC scope](POC.md) for the current implementation. Preserve source, tests and evidence; the policy does not claim the legacy implementation has become Rust. Running unchanged existing tools and checks remains allowed within the task's authority while migration is outstanding. Do not add or extend non-Rust framework logic.

Migration is mandatory but requires its own authorized implementation scope, owner and acceptance criteria. This documentation task does not perform migration, delete legacy code, remove or weaken tests/gates, edit frozen specifications or acceptance evidence, or change installed packages. Report language compliance separately from test results, native behavior and acceptance. The policy is an implementation requirement; prose alone is not automatic CI or runtime enforcement.

## Selected contracts and frozen work

The [skill authoring contract](mvp/skill-authoring-contract.md) preserves each assignment's selected revisions and bytes. An older instruction assigning trusted framework logic to Python conflicts with this policy. Stop the affected new implementation and report the conflict to the integration owner for an explicitly selected correction or migration scope. Continue unaffected authorized work and unchanged existing checks. Do not silently refresh contracts, repin a running acceptance campaign, or reinterpret historical results.
