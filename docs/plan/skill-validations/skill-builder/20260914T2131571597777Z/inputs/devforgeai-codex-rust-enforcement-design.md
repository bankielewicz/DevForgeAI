# DevForgeAI Codex CLI Enforcement: Compiled-Rust Design

Status: compiled-Rust enforcement design only. The companion skill build requires executable Python evidence artifacts; those artifacts do not implement this runtime, its hooks, or an acceptance path.
Recorded: 2026-09-11 America/New_York.

Requirements update: 2026-09-13 America/New_York. Mandatory TDD, quantitative quality floors, terminal compatibility, and non-ceremonial specification requirements are recorded below; this update does not implement or qualify the runtime.

## 1. Purpose and boundaries

Specify a fresh enforcement architecture for Codex CLI. Every DevForgeAI phase, gate, validator, mutation broker, and acceptance decision belongs in compiled Rust. A Python JSONL evaluation runner and deterministic graders are mandatory build artifacts and produce evidence only.

Rust is also mandatory for framework CLI/service logic, Codex hook handlers, and Git/GitHub hook handlers. Declarative host configuration may dispatch compiled Rust but must not become a separate policy implementation. Codex skills may use Python supporting resources; their Python evaluation bundle is required, not an optional alternative to Rust authority.

### Mandatory implementation and specification quality

Framework programming follows red -> green -> refactor -> QA. Retain a focused failing test before production changes, the minimum passing implementation result, post-refactor regression results, and final applicable QA evidence. Setup failures are not valid red tests. Documentation-only edits use factual and consistency checks rather than fabricated TDD evidence.

Require executed-line coverage >=95% for the declared first-party executable framework scope and test pass rate >=95% for the complete declared required-case suite, separately per required platform. Coverage excludes declared third-party/generated dependencies and fixtures, not inconvenient first-party branches or modules. Pass rate is passing required cases divided by all required cases; failed, errored, skipped, blocked, or unexecuted required cases are not passes. No rounding below the threshold, result cherry-picking, or denominator changes to manufacture a pass. Branch coverage, measurement limitations, counts, commands, tool versions, and evidence hashes are reported separately.

The compiled Rust gate design must validate the measurement reports and enforce both floors. A floor pass cannot override a failed mandatory acceptance scenario, unresolved regression, incomplete prerequisite, or authority/security invariant. The current document supplies requirements only; no numeric threshold is claimed to be enforced by an implemented service.

Do not create ceremonial gates, unexecuted PASS records, ambiguous contracts, placeholders presented as functionality, or aspirational framework claims. Each specified capability must have concrete inputs, outputs, ownership, failure semantics, terminal invocation, and observable acceptance evidence. Unresolved essential decisions are explicit blockers to implementation readiness.

All framework artifacts must work within Codex CLI terminal constraints: build, invoke, inspect, and validate through actual terminal-accessible capabilities. No MCP, browser, or GUI can be the sole required path. A Windows tray can provide optional human controls over equivalent CLI operations; native visual qualification remains distinct from terminal/integration evidence. This requirement does not turn proposed interfaces in this design into available commands.

This is a companion to the [importer specification](claude-to-codex-skill-import-spec.md) and [builder enhancement specification](skill-builder-enhancement-spec.md). The user separately authorized the development skill and required Python evidence tooling. That authorization does not implement or activate this Rust runtime, migrate legacy code, change operational configuration, or accept generated skills.

Do not copy or inspect legacy framework CLI or hook implementations, including `\\wsl$\Ubuntu\home\bryan\Projects\DevForgeAI2\.claude\scripts\devforgeai_cli`. Extract desired domain properties from allowed skill contracts and official host documentation. Treat legacy commands and model-written PASS flags as untrusted proposals, not architecture requirements.

## 2. Evidence informing the design

[Codex hooks documentation](https://learn.chatgpt.com/docs/hooks) describes synchronous interception, event-specific JSON contracts, reviewed/trusted configuration, concurrent handlers, and incomplete interception coverage. Background hooks cannot block operations. Post-tool events cannot reverse completed effects. Existing process input and specialized tool paths can bypass another pre-tool check. Unsupported hook responses and some hook failures do not necessarily deny operations.

Design consequence: hooks provide early feedback and interception for covered operations. They cannot be the sole protection of authoritative state or acceptance. Hook absence must not create authority.

[Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) supports outcome-based cases and calibration. [Python graders](https://developers.openai.com/api/docs/guides/graders) illustrate executable scoring. The required artifact/provenance and Rust authority boundaries below are project design decisions; they are not claimed as requirements or implementations supplied by OpenAI.

Observed host: Windows PowerShell with Codex CLI 0.154.0. Version/help succeeded with temporary alias access warnings. Hook execution, trust configuration, and permission isolation were not qualified.

## 3. Components and ownership

| Component | Language / owner | Allowed responsibility |
| --- | --- | --- |
| Imported skill | Agent-readable instructions | Domain reasoning, interaction, candidate work, and requests. |
| Control client | Compiled Rust | Typed terminal requests, responses, and diagnostics. |
| Authority service | Compiled Rust | All authoritative phase state, validation, gating, mutation, and acceptance. |
| Hook adapter | Compiled Rust | Parse Codex event JSON, call authority, map supported decisions to documented host output. |
| Evaluation runner | Python in restricted execution | Run pinned cases/graders and produce observations. |
| Deterministic graders | Python in restricted execution | Calculate reproducible metrics and identify evidence; never decide framework acceptance. |
| Skill Creator structural checker | Installed Python development tool | Check Codex skill packaging during authoring; no DevForgeAI validator, transition, or acceptance authority. |
| Qualification operator | Separate trusted principal | Approve installed authority/policy/build artifacts outside the evaluated agent's privileges. |

Use one authority implementation. CLI requests and hook requests must reach the same Rust validation and transition logic. Do not duplicate policy in hook scripts, Python, SKILL.md, or prompt evaluators.

The proposed future client executable name is `devforgeai-control`. It is not an existing command or a dependency of draft skills. Names below describe design interfaces only.

## 4. Authority protection on the target host

### Required deployment boundary

For the Windows target, use a Rust authority service under a dedicated service identity with protected storage and a local named-pipe interface. The agent identity may submit requests but cannot replace service binaries, policy, expected digests, authoritative state, or acceptance receipts. Provision these ACLs through a separately authorized installation step, not through the skill.

Run the evaluated agent without administrative rights. An administrator who can replace the service is outside this threat boundary; do not claim protection against that actor.

The client accepts untrusted proposals. Files under the project workspace remain candidate material even if named `accepted.json`. Service-owned storage is the sole source of authoritative status. Readback must come from the authority service, not from an arbitrary model-authored file.

Use a distinct trusted operator identity for build/policy approval. A JSON field or request arriving from the same agent identity cannot establish human approval. Do not put operator credentials into agent-accessible environment variables or files.

### Failures and unavailable protection

If the service, approved build, required graders, or protected storage is unavailable, issue no acceptance receipt. Report enforcement unavailable. Domain draft work can remain useful, but it cannot become accepted framework work.

A user-editable state file plus a hash is not protection: the agent could change both. Qualification must demonstrate actual denied writes under the evaluated identity. A future WSL/Linux target needs its own permission/IPC qualification; Windows results do not qualify it.

## 5. Control interfaces and phase semantics

### Proposed operations

- `run-start`: bind a new run to a workflow definition, approved policy, and immutable skill package digest.
- `run-status`: return authoritative state and unmet predicates.
- `artifact-submit`: register a candidate artifact for validation and snapshotting.
- `phase-request`: request transition to a named phase using the current revision and evidence references.
- `evaluation-request`: request execution of the approved evaluation bundle against pinned candidate artifacts.
- `acceptance-request`: ask Rust to evaluate final acceptance predicates and produce a receipt if satisfied.

The service assigns run identities. Requests cannot mint accepted run IDs or replace the governing policy. A missing workflow definition is an error, not a request to infer phase rules from prose.

### Request/response contract

Use versioned JSON over the local IPC interface. Required request fields are protocol version, operation, request ID, and run ID when applicable. Mutating requests include expected state revision. Artifact requests include logical artifact role and candidate reference. The authenticated peer identity is established by the OS transport, not a payload string.

Responses identify protocol version, request ID, outcome, authoritative revision, and diagnostics. Outcomes are `OK`, `REJECTED`, and `ERROR`. The terminal client uses exit 0, 2, and 3 respectively; invalid local usage uses exit 64. These client exit codes are separate from Codex hook exit semantics.

Return unmet predicates with required evidence and a concrete remediation. Never treat unknown operations, schema versions, or optional-looking required fields as permission to continue.

### State machine

An approved workflow definition supplies named phases, permitted transitions, artifact requirements, evaluation requirements, and acceptance predicates. Compiled Rust interprets and enforces that definition. Instructions may describe phases but cannot authoritatively advance them.

Reject phase skipping, absent prerequisite evidence, stale revisions, mismatched run identities, and attempts to substitute another skill package. Candidate edits invalidate evidence tied to older artifact hashes.

Serialize each run's mutating operations. Repeated identical request IDs return the original result; reusing an ID with different content is rejected. Persist transition state and its audit record atomically. A crash before commit must not leave an accepted status with missing evidence.

Resume reads the authoritative revision. Agent checkpoints preserve working context only; they cannot override service state. User corrections become new candidate evidence and trigger re-evaluation of affected predicates.

## 6. Artifacts, validators, and mutation broker

Rust validates the syntax, version, provenance, and required domain properties of submitted artifacts. File existence, a prior Read event, and `checkpoint-passed` are not sufficient predicates.

For acceptance, copy candidate bytes into an immutable service-owned snapshot and hash those bytes. Evaluate that snapshot, not a mutable workspace pathname. Path resolution rejects escapes and reparse-point traversal into excluded or protected areas; inaccessible candidates are reported without broadening permissions.

The mutation broker controls service-owned framework records and any explicitly managed accepted-artifact export. It does not claim to broker every draft file edit in the workspace. Ordinary shell writes cannot mint valid authority receipts.

The receipt includes run ID, final revision, workflow/policy/build identifiers, candidate/package digests, evidence references, acceptance outcome, and timestamp. Consumers obtain receipts from the service or verify a service signature against a separately trusted public key. Signing material is inaccessible to the agent and graders.

Do not let a Python helper perform schema validation that the framework treats as authoritative. Python may parse case files, report observed package/accounting properties, and run Skill Creator's packaging check. Rust independently applies every DevForgeAI structural/domain validator and acceptance rule. Calling a development check `quick_validate.py` does not grant it framework authority.

## 7. Hook design

Use a compiled Rust adapter launched through documented Codex command hooks. It consumes the host's event JSON on stdin and emits only supported event-specific output on stdout; diagnostics use stderr.

Design intent by event:

| Event | Role | Limit |
| --- | --- | --- |
| SessionStart | Report authority availability and run context. | Session start is not qualification. |
| PreToolUse | Intercept covered framework operations and reject known unauthorized requests. | Coverage is incomplete; authority protection remains external. |
| PostToolUse | Record observations and point out stale/invalid candidate results. | Cannot undo completed effects. |
| Stop | Provide bounded feedback about incomplete requested framework work. | Continuation is not acceptance; avoid repeated continuation loops. |
| Interrupt / compaction events | Preserve available run references and report recoverability. | Working context is not authoritative phase state. |

Use synchronous handlers for decisions. Do not configure a background handler as a gate. Do not grant broad permission through PermissionRequest hooks as part of this design.

For PreToolUse, map a Rust denial to the documented denial response or exit 2 with a reason. Do not reuse unsupported fields as if they denied execution. Handler failure must never be interpreted by the authority service as a successful operation, even when the host continues.

A disabled/skipped hook allows candidate activity but produces no authority result. Changed hooks need host trust review through normal controls. Do not use trust-bypass flags for qualification or installation.

Concurrent hook calls use the same idempotent service protocol and revision checks. Do not assume one matching hook prevents another handler from starting. Scope Stop behavior using run identity/state because a matcher is not a reliable filter for every event.

## 8. Required Python evaluation build artifacts

The development skill build is incomplete without the Python runner, deterministic graders, case/fixture data, their artifact binding, and executed evidence. The future Rust authority build must also bind that evaluation bundle to its own approved policy and build. Required artifacts are:

1. Evaluation runner and deterministic grader sources.
2. Grader definitions and stable IDs/versions.
3. Representative positive, negative, and adversarial cases.
4. Expected-result definitions and human review criteria where semantics require judgment.
5. JSONL evidence schema.
6. Supported Python runtime and dependency information, with a lock when external runner/grader dependencies exist.
7. Digests for the runner, graders, fixtures, and expected results.
8. Build manifest binding these artifacts to the Rust authority build and policy.

The development runner checks its local `evals/build-manifest.json` and emits execution errors for unavailable or changed required artifacts. This is a reproducibility check on agent-writable material, not a protected DevForgeAI build gate. The original builder evaluation reference was `src/agents/skills/skill-builder/references/evaluation.md`; that path is absent in the 2026-09-13 inspection. Current evaluator documentation is in the [validator evaluation reference](../../src/agents/skills/skill-validator/references/evaluation.md). Recheck the selected package's current contract before executing; the historical builder interface is not asserted to remain installed.

Rust build/qualification logic must independently verify required artifact completeness and permitted versions/digests. Its approved manifest is stored outside agent-write access and binds the Python bundle to the Rust build and policy. Missing artifacts cannot be waived by an agent-generated note. The local builder manifest cannot substitute for this approved manifest.

### Builder v2 evidence and future independent Rust validation

The enhanced local builder uses explicit evaluation profiles: `legacy-import-v1`, `import-v2`, `spec-v1`, `revision-import-v2`, `revision-spec-v1`, and `builder-v2`. Its version-2 package manifest binds profile definitions, grader versions, schemas, sources, fixtures, expected results, and tests. Every new runner result uses evidence schema 2 with profile identity/version. Historical schema-1 files remain historical evidence; selecting the legacy profile cannot satisfy enhanced-build requirements.

The original machine-evidence reference was `src/agents/skills/skill-builder/references/evaluator-contracts.md`; it is absent in the 2026-09-13 inspection. The current [validator machine evidence contracts](../../src/agents/skills/skill-validator/references/evaluator-contracts.md) document evaluator evidence. Earlier builder-profile descriptions here remain historical design context and require current package verification. These Python checks are evidence producers only. A future compiled Rust implementation must independently validate, against its protected approved build/policy:

- The operation's required profile and complete registered grader/case set, permitted versions, actual artifact digests, and result-schema version.
- Input identity, byte counts and SHA-256 values; zero-based end-exclusive source-reference intervals and their raw-byte digests; authorization origin through the actual operator boundary rather than a workspace instruction string.
- Requirement/artifact cross-references, complete output accounting, generated versus retained-user ownership, actual generated baselines, and matching candidate/output/evidence digests.
- Cited evidence run/package identity, dependency availability versus verified dependency bytes, and the completeness of actual required observations. A supplied hash or record of a dependency is not verification by itself.
- Prior successful immutable baseline identity, B/C/N consistency, actual mutation/readback evidence, and legitimate baseline advancement under Rust-owned mutation rules. Local snapshot equality does not prove chronological rechecks, successful protected mutation, or package-wide atomicity.
- Distinct structural, deterministic, script-execution, forward-trial, and routing evidence. Routing classification does not prove native implicit skill activation; byte accounting does not prove semantic fidelity.

Local provenance cites preceding structural/script observations; the final JSONL result is outside its candidate root and is linked by the final report. Rust must reject circular or nonexistent evidence references, stale digests, incomplete required trials, or a model-written COMPLETE value used as an acceptance predicate. Runtime policy supplies approved thresholds and required semantic observations; Python cannot waive them.

The local `build_evidence.py` helper performs bounded specification lookup, raw-byte metadata/source-reference calculation, and revision-plan proposals. It does not apply destination edits, publish authority state, or implement a mutation broker. Ordinary authorized terminal edits and editable development baseline pointers do not establish Rust acceptance. This section specifies future Rust validation responsibilities; no Rust runtime or runnable control command is delivered by it.

The service launches evaluation against immutable candidate snapshots under restricted permissions. Python may write only its assigned evidence output area, cannot contact external services by default, and cannot change the manifest, expected results, policy, or state. Runtime/resource bounds are part of the approved evaluation definition; exhausted bounds produce explicit incomplete evidence.

Each JSONL record identifies schema version, evaluation run ID, case ID, grader ID/version/digest, candidate digests, observations/metrics, referenced evidence, and execution error status. The runner does not emit an authoritative framework `accepted` field. Conflicting duplicates, missing required cases, malformed records, non-finite metrics, and mismatched digests are rejected by Rust.

Distinguish `NOT_RUN`, `ERROR`, and completed observations. An unexecuted case is not a passing case. The Python process exit code is not acceptance. Rust applies the approved thresholds and completeness rules after evidence validation.

The local development runner's `PASS`/`FAIL`/`ERROR` observations and expected-result comparison describe test outcomes only. A negative fixture may correctly observe `FAIL` and satisfy that fixture's expected result; this does not make the deliberately invalid candidate acceptable. Its caller-supplied run ID is a local evidence label, not an authority-issued run identity. The future service must supply and bind its own evaluation identity, immutable snapshots, execution limits, and approved case set.

Human assessments may supply signed/attributed observations through the operator boundary when required. Model judgment alone does not establish provenance or factual truth. Do not call a heuristic ceremony detector proof of semantic correctness.

## 9. Future qualification scenarios

Specify and run these only in a separately authorized implementation/qualification task:

- Valid transition and acceptance with complete pinned evidence.
- Skip a prerequisite or submit a model-written PASS without actual artifacts.
- Reuse evidence from another run, package, candidate revision, or grader build.
- Delete/modify a required grader, expected result, or evidence record.
- Bypass hooks, disable project hooks, or use a tool path outside hook coverage.
- Feed more commands into an already-running interactive shell.
- Submit simultaneous transitions against the same revision.
- Crash during a state/receipt write, then resume.
- Attempt agent writes to authority binaries, policy, state, and receipts.
- Attempt grader writes to state or expected results.
- Modify a candidate after snapshot creation and verify it does not change the accepted snapshot.
- Supply invalid hook output or simulate timeouts and missing service.
- Replay a request ID with different content.
- Forge operator approval or a receipt in the workspace.

The expected invariant is no unauthorized authoritative transition or receipt. Do not expand the claim to preventing every arbitrary action a user can authorize in Codex.

## 10. Delivery status

The Rust runtime remains design-only: no Rust control client, authority service, protected storage, hook configuration, or acceptance record is delivered by this design. The companion `skill-builder` development build requires the Python JSONL runner, deterministic graders, manifest, fixtures, and actual execution evidence. Their implementation and observed results are recorded in [the mandatory evaluation log](skill-builder-mandatory-evaluation-log.md).

Rust compilation, host qualification, protection tests, and operational installation remain `NOT_PERFORMED`. Report Python structural/deterministic checks from their execution evidence, and report semantic task evaluation separately. Successful development checks do not imply runtime acceptance or qualification.

The builder enhancement's implemented profiles, provenance checks, regression results, and synthetic forward trials are recorded in the [enhancement implementation log](skill-builder-enhancement-implementation-log.md). Those results remain development observations and do not implement this Rust runtime.
