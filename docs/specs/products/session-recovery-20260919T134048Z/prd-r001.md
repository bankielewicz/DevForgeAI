---
format_version: product-requirements-v1
prd_id: session-recovery-20260919T134048Z
revision: 1
updated_at_utc: "2026-09-19T13:40:48Z"
disposition: READY_FOR_REVIEW
supersedes: null
---

# DevForgeAI native Windows session recovery

## Document context and sources

This PRD specifies a Rust-owned capability for recovering named Codex and Claude
Code conversations after interruption or restart. The operator sees a recovery
list at Windows sign-in and chooses which conversations to reopen. It does not
automatically resume engineering work.

Bryan requested this PRD using `prd-create`, following the session-recovery
discussion. The selected root is `C:\Projects\DevForgeAI`. Repository delivery
uses branch `docs/session-recovery-prd` in its separate task worktree, based on
`4109846f3f792e13814c9366689d5c868e012450`. This authoring request selects
documentation and its draft PR, not implementation, provider-session launches,
hook installation, login registration, or independent review. The separately
requested local Codex worktree-approval rule is not part of this product.

This is a feature PRD, not a replacement for the index specifications or a
framework phase specification. MUST/MUST NOT describe the future implementation;
they do not claim existing functionality. `READY_FOR_REVIEW` is an authoring
disposition, not approval, implementation readiness, or framework acceptance.

### Conversation inputs

| Source | Origin and selected meaning |
| --- | --- |
| SRC-001 | Bryan supplied an anecdote about naming Claude sessions, recording IDs/names/directories with lifecycle hooks, and reopening them after restart; requested equivalent usefulness for Codex and Claude through the Rust CLI. The anecdote's 19 sessions in 30 seconds is motivation, not verified evidence or an agreed performance target. |
| SRC-002 | Bryan's answer during this authoring session: “Show a recovery list; I choose what opens (Recommended).” The question expressly described reopening conversations without instructions to continue work. |
| SRC-003 | Bryan's answer during this authoring session: “Native Windows first (Recommended).” WSL/Linux/macOS remain later scope. |

The earlier assistant's recommendations are design proposals, not additional
stakeholder approvals. Requirements below identify where they derive from the
selected outcome and governing constraints. Conversation has no fabricated file
digest.

### Bound local sources

Each SHA256 was computed from the same raw-byte buffer used to interpret that
source in the task checkout. The clause column limits the selected use; linking a
whole framework document does not select its entire implementation.

| Source | Locator | Selected clauses | Raw-byte SHA256 |
| --- | --- | --- | --- |
| SRC-004 | [AGENTS.md](../../../../AGENTS.md) | Framework authority; development/QA floors; terminal access; source/operational ownership | `cc0ed8bc550bf6cb0c82b6040b6d3c561c8ff494d76ee2a5f80e4e5c3a46c242` |
| SRC-005 | [docs/specs/framework/knowledge-and-continuity.md](../../../../docs/specs/framework/knowledge-and-continuity.md) | DFF-10: inputs/checkpoints; retrieval/resumption rules 3–6; existing assets/open decisions | `557b007099481746691921328d7644e0bac437ca9385a91f3c869f562170d4da` |
| SRC-006 | [docs/specs/framework/runtime/architecture.md](../../../../docs/specs/framework/runtime/architecture.md) | DFF-RUNTIME-01: progress/lifetime; persistence; protection/readiness | `f6751c356f7e161ef7d40773c4d2129be07055cdd055cecfafd20fb84657d7fc` |
| SRC-007 | [docs/specs/framework/installation-and-integrations.md](../../../../docs/specs/framework/installation-and-integrations.md) | DFF-11: lifecycle; worktree compatibility; integration surfaces | `2ee95ad58bb25694e156eafa479f68227bfd905a88761e85643ab1209681e1c6` |
| SRC-008 | [docs/specs/framework/guardrails-and-rust-runtime.md](../../../../docs/specs/framework/guardrails-and-rust-runtime.md) | DFF-07: protected behavior; host adapters; implementation readiness | `3df344a0a0b682d3e738e3a029415555bb058f91730365e07b1fec4cff236685` |
| SRC-009 | [docs/plan/devforgeai-codex-rust-enforcement-design.md](../../../../docs/plan/devforgeai-codex-rust-enforcement-design.md) | Sections 1 and 7: compiled Rust ownership and event adapter boundaries | `284f36e622a0d067b0417879eed32f239a4a01b86bb5ef8f45a65a64855ac9ed` |
| SRC-010 | [docs/plan/devforgeai-index-query-cli-spec.md](../../../../docs/plan/devforgeai-index-query-cli-spec.md) | Sections 1–1.2: query scope, index dependency and evidence-only boundary | `65097f0bbd73869fca9e70c872e4ea27b30ed71ce5cb6db0a4ff095aaf16d702` |
| SRC-011 | [docs/plan/devforgeai-index-service-mvp-spec.md](../../../../docs/plan/devforgeai-index-service-mvp-spec.md) | Sections 1–1.4: index lifecycle, authority separation and engineering policy | `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4` |
| SRC-012 | [devforgeai/Cargo.toml](../../../../devforgeai/Cargo.toml) | Current package identity and dependency baseline | `f6301a2d01e04ac66192c38269679b38e80aee0a20d901d86a4fdd4a42bc1e53` |
| SRC-013 | [devforgeai/src/cli.rs](../../../../devforgeai/src/cli.rs) | Cli/Command/Daemon declarations: current public command groups | `6b802c6c4c8dc6d7aec38c75f4fc49401ec87d47b81c0578839e9e7a0bbe51a9` |

### External interface research

Accessed 2026-09-19. These are changing official documents, not version-pinned
native qualification evidence.

| Source | Locator and inspected section | Use |
| --- | --- | --- |
| SRC-014 | [Codex hooks](https://learn.chatgpt.com/docs/hooks): common input, SessionStart, SessionEnd, trust and concurrent handlers | Event adapter assumptions and missing-event limitations |
| SRC-015 | [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference): codex resume | Exact-session and working-directory resume surface |
| SRC-016 | [Claude hooks](https://code.claude.com/docs/en/hooks): common input, SessionStart input, SessionEnd | Event/title differences and advisory end events |
| SRC-017 | [Claude CLI reference](https://code.claude.com/docs/en/cli-reference): --name, --resume, --no-session-persistence | Naming, native resumption and unavailable history |

Read-only local help reported Codex CLI 0.155.0 and Claude Code 2.1.278.
Help/version calls did not open a conversation or establish compatible behavior.
Codex also reported an access-denied warning for its temporary alias cleanup;
this observation is not a successful native acceptance trial.

## Problem, actors and outcomes

A restart closes working terminals. Remembering which conversation belongs to
which task and checkout creates avoidable manual reconstruction (SRC-001).
The selected user is a Windows developer operating several Codex/Claude CLI
sessions, including sessions in distinct Git worktrees.

The existing public CLI command groups in SRC-013 manage indexing and related
lifecycle; its `daemon resume` resumes indexing, not an AI conversation. SRC-012
identifies the current Rust index package. This scoped inspection does not claim
an exhaustive absence of session experiments elsewhere. DFF-10 and runtime
architecture describe continuity as planned work, not a qualified installed
session recovery service (SRC-005/006).

| Outcome | Observable result | Basis |
| --- | --- | --- |
| OUT-001 | Recover the intended conversation and its checkout without guessing from the most recent chat. | SRC-001 |
| OUT-002 | At sign-in, inspect saved sessions and open only the chosen conversations. | SRC-002/003 |
| OUT-003 | Retain useful recovery information after missing end hooks, crashes, or partial launch failures, while stating uncertainty. | SRC-001; SRC-005 resumption rules; SRC-006 progress/lifetime |
| OUT-004 | Operate and inspect recovery through the Rust CLI without transferring policy authority to scripts, hooks, or editable session notes. | SRC-004/008/009 |

Actors are the operator, the two provider CLIs, the Windows sign-in entry point,
and the Rust recovery component. No model is needed to list sessions or decide
whether a launch request satisfies deterministic prerequisites.

## Scope and exclusions

First-version scope is native Windows interactive Codex and Claude Code sessions
observed after the recovery integration is explicitly enabled. It includes
capture, display naming, list/detail inspection, manual selection, exact-session
launch in the recorded checkout, and an opt-in sign-in entry point that opens the
list. Manual CLI access remains available without login integration. Both
providers are required for the complete selected feature (SRC-001–003).

Automatic import of all historical conversations is not required. Missing hook
observations must be disclosed; the product cannot recover a session it never
recorded or reconstruct provider history that was not saved.

Excluded from this version:

- Automatic reopening of a saved set or automatic execution of unfinished work.
- WSL, standalone Linux/macOS, remote sessions, cross-machine synchronization,
  and resuming a Codex conversation inside Claude or vice versa.
- Recreating/moving worktrees, switching branches, restoring source snapshots,
  stashing/resetting/cleaning files, or replaying interrupted commands.
- Provider authentication management, credential copying, API fallback, automatic
  provider upgrades, or overriding permissions to make resumption succeed.
- Background subagent restoration, workflow scheduling, full transcript backup,
  AI-generated task summaries, new GUI/tray design, and desktop-window layout
  reconstruction.
- Installing the broader framework, implementing its protected authority,
  replacing the index daemon, or changing existing project-binding schemas.

These exclusions bound SRC-001 to the choices in SRC-002/003 and preserve
SRC-004–011. Exclusion of automatic engineering continuation does not imply that
a provider starts without any internal activity; qualification must examine
provider hooks, pending turns and persisted automation (REQ-006).

## Scenarios and interactions

1. **Normal recovery:** hooks record a session while it runs. After Windows
   sign-in, the enabled integration opens the recovery list. Nothing is selected
   for launch until the operator chooses entries and confirms the displayed
   provider, session and directory. Each selected entry receives its own result.
2. **Manual recovery:** the operator invokes the same list from PowerShell 5.1
   or PowerShell 7. An empty list explains that no sessions have been recorded;
   it offers integration diagnostics rather than launching a new conversation.
3. **Interrupted session:** the machine stops before SessionEnd. The last
   committed record remains. The list describes its lifecycle as uncertain until
   reconciled; it does not declare the task completed or cancelled.
4. **Unavailable checkout/history:** the row remains visible with the precise
   missing prerequisite. Recovery does not substitute the project root, another
   worktree, a similarly named chat, or the most recent conversation.
5. **Mixed results:** one selected session opens, another cannot authenticate,
   and another is already active. The summary reports all three separately.
   Reopening the list or retrying after uncertainty does not duplicate the first.
6. **Changed context:** branch, directory identity or effective launch policy
   differs from the recorded observation. The operator sees the difference;
   unresolved or incompatible identity/security changes prevent that launch.
   No recovery action silently repairs or overrides the changed context.

The required UI is a keyboard-operable terminal list/detail/confirmation flow,
with readable rows, explicit prompts, and errors that do not depend on color.
A GUI is not required. A future operator-console menu may call the Rust
operations; it must not implement a second store, policy, or recovery algorithm.

## Functional requirements

“Derived” identifies an engineering consequence proposed for review under the
cited outcome/constraint, rather than an extra claimed user decision. All
requirements are future normative obligations within this PRD.

| ID | Trigger, conditions and required observable behavior | Basis / outcome | Acceptance |
| --- | --- | --- | --- |
| REQ-001 | On a supported provider event, the Rust adapter MUST validate its provider-specific envelope and persist session identity, observed directory, event kind and observation time. Session identity MUST include provider and local user/host/store namespace plus the native ID; a title is never a unique key. Invalid or unsupported input MUST return a classified diagnostic without creating a launchable record. | Derived: SRC-001, SRC-004/006/014/016; OUT-001/003/004 | AC-001, AC-002 |
| REQ-002 | Capture MUST commit during session life, starting with SessionStart, rather than depending on shutdown. Repeated events MUST NOT duplicate logical sessions. Concurrent/resumed lifetimes and delayed end events MUST NOT make an older observation overwrite a newer lifetime. Missing, unorderable or conflicting observations MUST remain visibly uncertain. End events MUST NOT mark work complete, cancelled, or disposable. | SRC-005 rules 3–6, SRC-006 lifetime; provider differences; OUT-003 | AC-003, AC-004 |
| REQ-003 | List/detail MUST show provider, display label or native-ID fallback, exact recorded directory/checkout, last observation, lifecycle confidence, and restore availability/reason. The operator MUST be able to set a framework display label without changing native identity or silently renaming provider history. An observed provider title and an operator label MUST remain distinguishable. Unknown task/branch information MUST be shown as unknown. | SRC-001; derived usability under SRC-005/006; OUT-001/002 | AC-005 |
| REQ-004 | Sign-in, when separately enabled, MUST open the recovery list in that user's interactive Windows session, with zero provider launches before explicit selection and confirmation. The same recovery flow MUST be callable manually. Cancel/empty selection MUST launch nothing. Repeated activation while a recovery UI is active MUST not produce competing launch owners. | SRC-002/003; SRC-004 terminal access; OUT-002 | AC-006, AC-007 |
| REQ-005 | Before each selected launch, Rust MUST recheck the provider executable/profile, exact native-session availability, recorded directory and checkout identity, current activity, and effective supported permission context. Invalid IDs, missing history, unsupported versions, ambiguous ownership or incompatible directory/policy changes MUST block the affected launch with a reason. A branch/HEAD change MUST be disclosed; the operator can review the current checkout, but recovery MUST NOT alter it or infer that old work remains valid. | Derived: SRC-005/006/007/008; OUT-001/003/004 | AC-008, AC-009 |
| REQ-006 | A successful restore MUST reopen the selected native conversation in its validated directory, without a supplied task prompt, synthetic “continue,” automatic turn submission, --last selection, or fork/new-session fallback. The qualified adapter MUST account for pending turns, hooks and persisted automation that could resume work without a new prompt. If it cannot establish the selected conversation-only mode, it MUST block managed launch and explain the limitation, not silently change provider settings. | SRC-002; SRC-005 rule 6; SRC-015/017; OUT-001/002/004 | AC-010, AC-011 |
| REQ-007 | Repeated/concurrent requests for the same session MUST share a serialized launch decision. An already active session MUST not be launched again by this component. After a crash between process creation and acknowledgement, the next request MUST reconcile actual state; uncertainty MUST not authorize a blind retry. A saved PID alone MUST not establish liveness or session ownership. | Derived: SRC-006 progress/lifetime; SRC-008 request identity; OUT-003 | AC-012, AC-013 |
| REQ-008 | Each batch MUST retain per-session selected, not-attempted, blocked, launch-requested, opened/confirmed, failed or uncertain outcomes as applicable. OS process creation alone MUST not be reported as a confirmed resumed conversation. A failed entry MUST not erase successful entries. Cancellation MUST stop future dispatch after cancellation is observed and disclose any in-flight/previous launches; it MUST not kill an existing conversation or repeat an uncertain attempt. | Derived: SRC-002, SRC-005/006; OUT-002/003 | AC-014, AC-015 |
| REQ-009 | On list/restore/storage operations, Rust MUST preserve committed records through interruption and reject unreadable or unsupported stored formats without resetting the store. Missing/corrupt history or referenced evidence MUST yield a concrete gap. Record removal/expiry MUST NOT follow from SessionEnd or a universal timer. Dismissal, deletion and retention policy are subject to Q-004; no automatic purge is selected. | SRC-004 preservation; SRC-005/006 persistence; OUT-003 | AC-016 |
| REQ-010 | Inspect/plan integration MUST be read-only. Enable/update/disable of hook and Windows sign-in integration MUST require the selected concrete effects, preserve unrelated configuration, track owned entries, and report partial changes/readback. Hook trust review MUST use native controls. Disable MUST stop future owned activation without deleting native conversations or project files. | SRC-004/007 lifecycle; SRC-009 hooks; OUT-004 | AC-017 |

## Quality and operational requirements

| ID | Required behavior and measurement obligation | Basis / outcome | Acceptance |
| --- | --- | --- | --- |
| REQ-011 | Framework capture, persistence, checks and launch coordination MUST be compiled Rust. Declarative configuration or an optional PowerShell menu only dispatches it. Session metadata, provider output and model notes MUST NOT authorize protected work or grant acceptance. Recovery MUST NOT require indexing or broaden its observation-only service into an authority. | SRC-004/008/009/010/011; OUT-004 | AC-018 |
| REQ-012 | Recovery data MUST remain within the selected Windows user's local boundary. It MUST exclude credentials, tokens and raw prompt/transcript content by default. Names, directories and references are untrusted data, never executable shell fragments. Diagnostic output MUST identify the failed operation without dumping provider payloads/secrets. Existing provider authentication and permission controls remain in force. | Derived: SRC-005 privacy, SRC-006 protection, SRC-007 integration; OUT-003/004 | AC-019 |
| REQ-013 | Hook work MUST be bounded, local and independent of model/network calls. A record MUST not be acknowledged as durable before commit. Contention, disk errors and timeout MUST produce truthful capture limitations; hook failure cannot promise to stop the host. Payload, latency, storage and launch-concurrency bounds MUST be defined in the implementation contract (Q-003), respecting the qualified provider's timeout. No “19 in 30 seconds” target is inherited. | SRC-001 anecdote limitation; SRC-006 bounded operations; SRC-014/016; OUT-003 | AC-020 |
| REQ-014 | Native Windows terminal operation MUST work from Windows PowerShell 5.1 and PowerShell 7 without requiring Bash/WSL. Support claims MUST identify Windows build, shell/terminal, provider version/install form/profile, integration configuration and limitations. A new provider version MUST not silently inherit prior native qualification. Text and structured results MUST carry equivalent status and reasons; actual grammar/schema is Q-001. | SRC-003; SRC-004 Windows/terminal policy; SRC-007 compatibility; OUT-002/004 | AC-007, AC-021 |
| REQ-015 | Implementation MUST follow red -> green -> refactor -> QA and retain per-platform evidence. Executed-line coverage MUST be >=95% of declared first-party executable framework scope; required-case pass rate MUST be >=95%, with skipped/blocked/errored/unexecuted cases in the denominator and no below-threshold rounding. Failed mandatory scenarios, unresolved regressions and authority/security invariants cannot be waived by either floor. | SRC-004 and SRC-009 section 1; OUT-004 | AC-022 |

REQUIRED platform coverage for this feature is native Windows; both selected
PowerShell hosts and both provider adapters must be exercised. Shared Rust unit
evidence may be reported once with its scope; shell/provider integration results
must remain attributable and cannot qualify an untested profile. Source exclusions,
case denominators, tool versions, commands, exit codes and artifacts are declared
before execution. Branch coverage is reported separately where available.

No service uptime SLA, cloud synchronization, compliance certification, or web UI
is selected. Hook responsiveness and multi-session capacity need measured
qualification, not an invented savings estimate. The hook-timeout and launch
bounds are implementation blockers in Q-003, not measured results in this PRD.

## Data, interfaces and dependencies

### Logical data and ownership

These are requirements on meaning, not a new finalized persistence schema.

| Entity | Required meaning and owner |
| --- | --- |
| Session reference | Rust recovery store owns provider/native ID plus local namespace, display label and last validated directory/checkout association. Provider owns the native conversation and its history. |
| Lifecycle observation | Provider event and source/reason, locally observed time, provider/profile identity and capture result; distinguish receipt order from actual lifecycle ordering. |
| Checkout observation | Resolved directory and, when Git exists, checkout/repository identity plus observed branch/HEAD and observation time. Non-Git sessions are not silently made into repositories. |
| Recovery request/result | Explicit selection, request identity, per-session attempt/outcome and confirmed versus uncertain effects. It is not a framework run acceptance record. |
| Optional context reference | An operator-supplied task/specification or next-action reference may be displayed with its source; absent information stays absent. Reading or presenting it does not dispatch work or certify freshness. |
| Integration ownership | Selected hook/sign-in entries, version and prior state needed for bounded update/disable. Existing provider configuration remains owned by its original owner. |

Do not copy transcript bodies to explain a title. An optional transcript locator
is only a reference with missing-file behavior, not a stable provider database API.
No transcript parser or direct provider-database writer is selected.

Lifecycle confidence (observed/uncertain), current liveness, restore eligibility,
operator selection and task completion are separate concepts. A close event only
updates an observation. A resumed lifetime can produce another start for the same
native conversation. No clock timestamp alone resolves delayed/conflicting events.

### Provider contract differences

- Codex supplies common session/cwd/event fields. SessionStart distinguishes
  startup/resume/clear/compact. SessionEnd is main-thread only and can occur on
  normal closure, archive/delete or delayed idle cleanup; its documented reason
  is currently `other`. It is advisory, not a completion signal. Codex resume
  accepts a session selector; explicit directory selection matters.
  (SRC-014/015)
- Claude supplies common session/cwd/event fields and may supply
  `session_title` at SessionStart. SessionEnd reasons distinguish, among others,
  clear, interactive resume, logout and prompt exit; end hooks cannot prevent
  termination. Naming and native resume are exposed by the CLI; sessions without
  persistence are not recoverable history. (SRC-016/017)

Adapters MUST be qualified separately. Neither identical hook names nor successful
help output proves identical fields, ordering, availability, or startup behavior.
A provider title missing from an event is not an excuse to scrape undocumented
internal storage. Hook stdout must not inject arbitrary stored notes into agent
instructions; diagnostics belong on the provider-supported diagnostic channel.

### Terminal operations and dependencies

| Required operation | Inputs and result | Dependencies / limits |
| --- | --- | --- |
| Capture event | Provider selector + native event on stdin -> recorded/rejected/failed observation | Qualified event adapter, bounded durable writer; no terminal launch |
| List / inspect | Optional provider/project/session selector -> records, confidence and reasons | Store available; no provider launch or index dependency |
| Set display label | Exact framework session reference + operator label -> updated display metadata | Identity remains unchanged; no provider-history write |
| Preview restore | Explicit session selection -> exact candidate launches, prerequisites and differences | Read-only native/provider/checkout inspection where supported |
| Restore selection | Confirmed selection/request identity -> per-session outcomes | Recheck immediately before effect; exact argument vector, current supported profile |
| Inspect / plan integration | Selected host/provider -> missing capabilities and concrete owned changes | No writes |
| Enable / disable integration | Authorized plan -> actual owned changes and readback | DFF-11 ownership/trust contract; no implicit enrollment from ordinary list commands |

These names describe capabilities; they are not copyable CLI commands. Candidate
placement under a `devforgeai session` group is a proposal for Q-001 review.
Existing index `daemon resume` MUST retain its meaning. The new feature consumes
no index database/IPC protocol by assumption and needs no active project binding
to list its own local recovery records. Reopening a conversation does not assert
that binding-required skills are activated in that checkout.

## Architecture and decisions

| ID | Decision and origin | Consequence |
| --- | --- | --- |
| DEC-001 | User-selected: list and explicit operator choice at sign-in (SRC-002). | Automatic reopening is excluded. |
| DEC-002 | User-selected: native Windows first (SRC-003). | WSL/Linux/macOS and remote cross-host storage are excluded. |
| DEC-003 | Governing: compiled Rust ownership; advisory storage does not become protected authority (SRC-004/006/008/009). | Hooks and shells invoke one Rust implementation; ordinary session recovery cannot grant workflow acceptance. |
| DEC-004 | Derived for review: native conversation IDs are identity; mutable titles are display (SRC-001/014–017). | Duplicate names and renames cannot redirect recovery. |
| DEC-005 | Derived for review: persist before shutdown, reconcile uncertain launches (SRC-005/006). | End-only capture and PID-only duplicate detection are insufficient. |

The smallest candidate architecture is a Rust recovery module/adapter boundary
exposed through the CLI, local persistence and a per-user sign-in launcher.
Whether it belongs in the current crate or a sibling crate, and whether durable
writes need a dedicated process, remain Q-001/Q-002 decisions. Do not quietly
reuse the index daemon as a workflow controller. SQLite is a candidate already
mentioned in SRC-006, not a selected database layout.

A flat-file registry offers simple inspection but needs explicit concurrent-write
and crash semantics. SQLite provides local transactions but does not solve process
launch atomicity, authorization or provider state by itself. Review must select
the simpler design that meets REQ-002/007/009/013, rather than introduce a service
solely because a registry is needed.

No native recovery experiment was executed during authoring. A later disposable
qualification should observe whether resuming an idle, interrupted, goal-bearing
or hook-enabled conversation can perform work without a new prompt. Its method,
permissions and effects need a selected test contract; a contrary result blocks
managed conversation-only launch for that profile, not a silent scope rewrite.

## Acceptance and traceability

The following are planned oracles, not results. Each applies to both providers
where meaningful; provider-specific variants remain separate required cases.

| ID | Conditions and observable expected result | Requirement backlinks |
| --- | --- | --- |
| AC-001 | Valid start events with the same native ID in different providers/namespaces produce distinct correctly attributed records. Same-identity retries yield one logical session. | REQ-001 |
| AC-002 | Missing ID/cwd, invalid JSON, unsupported event/version and oversized input return precise errors; no executable or launchable record is synthesized. | REQ-001, REQ-013 |
| AC-003 | After a committed start and forced termination without an end hook, a fresh recovery process reads the record and shows uncertain/currently reconciled lifecycle, not task completion or cancellation. | REQ-002 |
| AC-004 | Concurrent starts, repeated resume/compact events and a delayed end from an older lifetime do not lose acknowledged records or close a newer lifetime. If ordering cannot be proved, uncertainty is visible. | REQ-002 |
| AC-005 | Duplicate names, absent titles, Unicode labels and renamed sessions remain selectable by exact identity; operator labels do not modify native history. Missing task/branch data stays unknown. | REQ-003 |
| AC-006 | Enabled sign-in opens the list only. Cancel, no selection, repeated UI activation and a disabled integration create zero provider sessions. Confirmation opens only explicitly selected eligible entries. | REQ-004 |
| AC-007 | Empty/loading/error/partial-result states and selection/cancellation are keyboard operable in native PowerShell 5.1 and 7; status remains understandable without color. Manual access works without startup registration. | REQ-004, REQ-014 |
| AC-008 | Missing/renamed/replaced directory, removed worktree, unavailable provider, missing/nonpersistent session and ambiguous identity each block that entry with no fallback launch or source/configuration repair. | REQ-005 |
| AC-009 | Changed branch/HEAD or effective security context is disclosed before launch. Concurrent changes are rechecked; incompatible/unresolved context is not launched. No branch switch, reset, stash or permission bypass occurs. | REQ-005 |
| AC-010 | A supported selection opens the same native ID in the validated checkout. It supplies no task prompt, --last, fork, or new-session substitution; the operator sees the expected conversation. | REQ-006 |
| AC-011 | Profiles with pending/automatic continuation or startup-hook activity are tested against the conversation-only contract. An unsafe or unverifiable profile is reported unsupported for managed launch; no configuration is silently altered. | REQ-006 |
| AC-012 | Two simultaneous requests for one session produce at most one managed launch; a session already active through a supported external launch path is not duplicated. Ambiguous external liveness is blocked with its limitation. | REQ-007 |
| AC-013 | Interrupt immediately before/after process creation and before confirmation; on retry, reconcile existing/absent/uncertain effects. A reused PID or delayed acknowledgement does not trigger a second launch. | REQ-007 |
| AC-014 | In a mixed successful/blocked/failed batch, all per-session outcomes persist. Spawn without verified resume remains unconfirmed. Reopening the list does not retry any launch. | REQ-008 |
| AC-015 | Cancel while one launch is in flight: no later dispatch after cancellation is observed; retain the in-flight result or uncertainty, leave already-open sessions intact, and do not auto-retry. | REQ-008 |
| AC-016 | Crash during write, disk full, denied read and corrupt/unknown stored version preserve prior committed information or report a concrete inaccessible-state failure. No store reset, end-triggered deletion or fabricated recovery occurs. | REQ-009 |
| AC-017 | In disposable Windows/provider configuration, inspect/plan writes nothing; authorized enable/update/disable preserves unrelated entries. Interrupted changes report partial effects. Trust denial remains denied, and disable leaves sessions/source intact. | REQ-010 |
| AC-018 | The feature works with indexing stopped/unavailable and follows one Rust decision path. Forged session notes cannot advance a protected phase; disabling hooks cannot manufacture capture or acceptance. Existing index/lifecycle meaning is unchanged. | REQ-011 |
| AC-019 | Quotes, spaces, shell metacharacters and malformed identities cannot execute injected commands or select a different checkout. Secret-bearing payloads do not enter stored diagnostics; no credential export or permission widening occurs. | REQ-012 |
| AC-020 | Under the predeclared payload/concurrency/storage workload, measure capture latency and completion against the selected provider budget; contention/timeouts are bounded and reported. Uncommitted capture is never acknowledged as durable. | REQ-013; Q-003 |
| AC-021 | Record native Windows/shell/provider/profile identities and actual results. A provider upgrade or unsupported profile does not reuse the old qualification as its own. Text/structured outputs agree on per-session state. | REQ-014 |
| AC-022 | Retained red/green/refactor/regression/native evidence includes all declared cases and first-party source scope; both >=95% floors are met without waiving mandatory failures. Independent QA assesses the exact candidate. | REQ-015 |

### Source/outcome coverage

| Selected obligation | Disposition / outcome -> requirement -> criterion |
| --- | --- |
| SRC-001: recognizable saved sessions and native recovery | OUT-001 -> REQ-001/003/005/006 -> AC-001/002/005/008–011 |
| SRC-001: recovery after restart | OUT-003 -> REQ-002/007/008/009/013 -> AC-003/004/012–016/020 |
| SRC-001: anecdotal automated restore/speed | Automatic reopen superseded for this version by SRC-002; 19/30-second claim excluded as an unsupported target. |
| SRC-002: sign-in list and explicit choice, without continuation instructions | OUT-002 -> REQ-004/006/008 -> AC-006/007/010/011/014/015 |
| SRC-003: native Windows | OUT-002/004 -> REQ-004/010/014 -> AC-006/007/017/021; other hosts excluded. |
| SRC-004/009: Rust, terminal, preservation, implementation quality | OUT-004 -> REQ-010–015 -> AC-007/017–022 |
| SRC-005: recover actual obligations, no blind replay, private-data limits | OUT-003/004 -> REQ-002/005–009/012 -> AC-003/004/008–016/019; broader context service excluded. |
| SRC-006: distinct identities, durable observations, launch uncertainty, unprotected memory | OUT-001/003/004 -> REQ-001/002/005/007–009/011–013 -> linked ACs above; database/process topology Q-002. |
| SRC-007: explicit lifecycle effects, host-specific support, worktree binding limitation | OUT-004 -> REQ-005/010/014 -> AC-008/009/017/021; complete installer/binding writer excluded. |
| SRC-008: one authority, truthful availability, idempotent effects | OUT-003/004 -> REQ-007/008/011 -> AC-012–015/018; protected authority implementation excluded. |
| SRC-010/011: index ownership and companion boundaries | OUT-004 -> REQ-011 -> AC-018; indexing/query/tray implementation and their other-host matrices not selected here. |
| SRC-012/013: observed current package/CLI | Baseline context for Q-001 and AC-018, not business policy or a claim of broad feature absence. |
| SRC-014–017: provider contracts | OUT-001/003 -> REQ-001/002/005/006/013/014 -> AC-001–004/008–011/020/021; version qualification Q-005. |

## Risks, assumptions and questions

Product choices for list-first recovery and native Windows are resolved. The
following explicit design/qualification questions are transferred to PRD review
and the architecture owner (person not yet assigned); they block dependent
implementation or release, not authoring of the selected outcomes.

| ID | Exact question / risk and alternatives | Owner / affected scope / blocking stage |
| --- | --- | --- |
| Q-001 | What Rust package/module owns recovery, and what exact CLI grammar, versioned result schema and exit-code mapping implements the operation table without changing index contracts? | PRD reviewer + architecture owner; REQ-001/004–011/014; blocks dependent implementation contract. |
| Q-002 | Which local store/location, writer ownership, transaction/durability and migration contract handles concurrent hooks and interrupted launches? Evaluate flat-file vs SQLite; choose lifecycle/order correlation and external liveness evidence without relying only on PID/timestamps. | Architecture owner; REQ-001/002/007–009/012/013; blocks persistence/launch implementation. |
| Q-003 | What supported workload, payload/label size, hook deadline, contention/retry limit, launch concurrency and cancellation deadline can native measurement qualify? Propose values with evidence; do not inherit the anecdote's rate. | Architecture owner proposes; Bryan selects product limits; REQ-002/008/013; blocks bounded implementation and AC-020 qualification. |
| Q-004 | What retention/storage-budget and explicit dismissal/deletion behavior should recovery metadata have? No automatic purge is selected; native transcripts, project files and required evidence remain outside registry cleanup authority. | Bryan with DFF-10/policy owner; REQ-009/012/013; blocks any cleanup feature or operational retention claim. Core capture/list/restore can proceed without adding deletion. |
| Q-005 | Which exact installed Windows/provider profiles support session discovery, trustworthy liveness and confirmed conversation-only resume, including persisted goals/pending turns/hooks? What observable acknowledgement proves the requested ID/directory opened? | Provider adapter owner + independent QA; REQ-005–008/014; blocks native support/release claim and any unsupported launch path. |
| Q-006 | Which per-user Windows sign-in mechanism and terminal host presents one usable list, supports paths with spaces/Unicode, and has explicit enable/disable ownership? | Windows integration owner; REQ-004/010/014; blocks activation implementation/native sign-in qualification. |

RISK-001: a provider update can change events/resume behavior; source basis
SRC-014–017, mitigated by Q-005 and REQ-014. RISK-002: shutdown can omit events
and process creation cannot be atomically committed with local records; basis
SRC-005/006, addressed by REQ-002/007. RISK-003: user-writable recovery records
cannot serve as protected approval; basis SRC-006/008, constrained by REQ-011/012.
RISK-004: names/directories may themselves be sensitive; basis SRC-005, subject
to REQ-012 and Q-004. Each risk remains with the respective question owner;
none is marked resolved by this document.

## Review handoff

Source action: **CREATED**. Disposition: **READY_FOR_REVIEW**. Identity:
`session-recovery-20260919T134048Z`, revision 1, at
`docs/specs/products/session-recovery-20260919T134048Z/prd-r001.md`.
The final whole-file SHA256 is supplied in the authoring delivery/PR, outside
this file to avoid a self-referential digest.

Next responsibility is **prd-review**, manually selected. Review the precise
candidate digest from delivery against SRC-001–017 and the local source identities
above. Focus on whether the planned oracles expose missing hooks, late events,
duplicate launch races, uncertain external effects, changed checkout identities,
and provider-side automatic work. Resolve Q-001–006 with their named owners;
an implementation contract must settle its dependent blockers before coding.

Copyable continuation request (the reviewer must first verify the delivery digest):

> Independently review revision 1 of
> docs/specs/products/session-recovery-20260919T134048Z/prd-r001.md
> (PRD session-recovery-20260919T134048Z), using the exact SHA256 in its
> authoring delivery/PR and bound SRC-004–013 local sources, SRC-001–003
> decisions, and SRC-014–017 provider references. Select native Windows
> Codex/Claude capture, list-first sign-in recovery and explicitly chosen
> conversation-only resumption. Assess contradictions, missing behavior,
> architecture sufficiency, feasibility, quality obligations and AC-001–022.
> Focus on Q-001–006, especially no automatic work, liveness/duplicate races
> and crash recovery. Return findings to the PRD author; do not implement,
> launch provider sessions, install hooks, register startup tasks, or treat
> this authoring disposition as review approval.

Independent PRD review, implementation tests, native recovery/sign-in trials,
installation and framework acceptance are **NOT_PERFORMED / NOT_EVALUATED**
as appropriate. This PRD does not close prior worker diagnostic or QA findings.

## Revision and follow-up notes

Revision 1 adds OUT-001–004, REQ-001–015, AC-001–022, DEC-001–005,
Q-001–006 and RISK-001–004. It has no predecessor and retires no existing
framework requirement. The source buffer identities above are the authoring
baseline; delivery rechecks them before saving and at final readback. A changed
source requires semantic reconciliation, not a hash-only refresh.

Possible later selections are automatic reopening of an explicitly saved set,
WSL/other hosts, historical-session import, an operator-console shortcut and
richer context references. None is selected by this revision, and none authorizes
autonomous resumption of unfinished work.
