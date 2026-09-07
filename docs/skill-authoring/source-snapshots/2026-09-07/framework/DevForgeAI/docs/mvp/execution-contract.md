# Terminal, worktree, and external execution contract

Status: DRAFT MVP requirements, revision 3, 2026-09-07 UTC. This revision selects the managed brainstorm runtime interface and thin provider hook sources. The companion runtime has synthetic mechanical evidence; these shared/package sources remain an integration candidate. Native admission is NOT_VALIDATED, native hook activation and rendered receipt delivery are NOT_OBSERVED, and reviewed provider integration and combined install/export validation remain pending. This contract does not claim a worktree registry, general outbox, or full stack adapters.

## Terminal operating model

The target operating model is a normal subscribed Codex or Claude Code session. Native skills guide the work. The separate DevForge executable performs supported deterministic checks. Human-operated transitions remain a valid MVP path for existing gates; the managed brainstorm mode below assigns phase transitions and mechanical delivery to the protected runtime. A background agent service or model API is not required. The current production launcher refuses native admission until its launcher/authentication and effective hook-source contracts are established.

Each target terminal must separately demonstrate installation, discovery, activation, supporting-resource loading, and representative output. Native creator and plugin packaging helpers are authoring tools. Successful package validation or a CLI version probe does not establish runtime behavior.

Commands are thin entry points to skills. Do not invent a slash command or DevForge subcommand in a handoff: use the actual installed skill selector or a plain-language request naming the skill. The current Rust command surface is listed by its real --help output.

## Worktree assignment for concurrent sessions

User requirement: worktrees are important when multiple AI sessions work in one repository. For the MVP, each concurrent writing session must use its own declared worktree and unique branch, or a recorded detached commit when appropriate. One session is the writer for an assigned worktree; read-only reviewers may inspect a frozen snapshot.

Worktrees share Git metadata. They reduce working-file collisions but do not isolate shared refs, Git configuration, credentials, external services, or validator authority. The external control boundary must be tested separately. [OpenAI worktree guide](https://learn.chatgpt.com/docs/environments/git-worktrees).

The authority owner records a [session assignment](templates/shared/session-record.md) containing:
- Session ID, task/story, owner, provider, and ownership/lease state.
- Repository identity, Git common directory, absolute worktree path, branch or detached state, and base commit.
- Declared write fence, protected paths, installed skill identities, and required context revisions.
- External policy/runner/state references and report delivery path.
- Any shared port, database, service, or fixture allocation.
- Integration target and continuation owner.

Assignment records reside in the external authority store. A worker-authored session ID is not proof of ownership. The MVP may use a single human operator to serialize assignments and Git integration; an automated registry would require its own implementation and tests.

For an uncommitted greenfield idea, an observably assigned single writer may use bootstrap mode. Missing session metadata does not prove exclusive ownership; record the task authorization and inspect collision evidence before writes. Before concurrent Git work begins, an actual initial commit and recorded base are required. Do not invent a base SHA or automatically commit user work as a precondition.

Native Git supports manual allocation from a committed base. These are parameterized operator examples, not installed DevForge commands:

```bash
git -C "<repository>" worktree list --porcelain
git -C "<repository>" worktree add -b "<unique-task-branch>" "<new-worktree-path>" "<base-commit>"
```

Inspect current paths and branches first; do not reuse an occupied branch or overwrite a directory. The desktop app's automatic worktree setup, handoff, and ignored-file copying are not assumed for Git worktrees created manually in either terminal. Install required project skills in each task worktree using the accepted installation method; do not copy credentials merely because a setup file was ignored.

When protection makes the Git common directory read-only to the worker, the worker edits its assigned files and hands off the candidate; the operator performs commits and ref updates. Do not relax shared Git metadata permissions merely to make a worker command succeed.

## Per-session workflow

1. Allocate or verify the assignment before writes; capture the base and upstream identities.
2. Install and identify the actual skills needed in that worktree.
3. Complete allowed preparation before initializing a production candidate baseline.
4. Run the assigned bounded task; write reports through the declared delivery path.
5. Freeze the result and preserve external receipts before another session evaluates it.
6. Integrate under a single owner and test the combined candidate on its actual integration base.
7. Record completion and handoff before releasing ownership.

A rebase, conflict resolution, changed upstream context, or changed integration base creates a new candidate. Passing evidence from an earlier task branch is insufficient for the combined result. Cleanup is separate from completion: preserve dirty work and evidence, and never automatically delete a worktree used by another session.

## Concurrent story flow

```mermaid
flowchart TD
    BASE["Recorded Git base and external assignments"]
    BASE --> W1["Session A: worktree A / branch A"]
    BASE --> W2["Session B: worktree B / branch B"]
    W1 --> CA["Candidate A and gate receipts"]
    W2 --> CB["Candidate B and gate receipts"]
    CA --> INT["Single integration owner: new combined candidate"]
    CB --> INT
    INT --> CHECK["DevForge checks and QA on integration result"]
    CHECK --> REL["Authorized PR / release workflow"]
```

This describes permitted parallel sessions; it does not automatically launch subagents. A subagent receives only the task-relevant inputs and its declared scope. Read-only review and behavioral evaluation require the actual isolation conditions requested for that task.

## Managed brainstorm runtime

An external owner selects a devforge.brainstorm-session/v1 contract before task admission. It binds the task and assignment, immutable inputs, installed resource identities, original deadline, mutable-output baselines and retained archives, exact checkpoint destination, and separately bound external receipt destination. Mutable ledgers are outputs, not immutable inputs; preservation requires retained prior bytes. The runtime executable, selected inputs, state and receipt store must be protected from worker writes. A task contract supplies neither user authority nor permission to launch a model.

The ordinary phase order is Recover → Explore → Record → Focus. Only the external owner may select a handoff-only contract, with Recover → Focus and Explore/Record marked NOT_APPLICABLE. The worker cannot switch modes or destinations to escape a collision or a failed requirement. Runtime context supplies the current phase, fresh challenge, task identity, checkpoint destination and evidence shape; [SKILL-001](specifications/skill-001-devforge-brainstorm.md#managed-phase-evidence) defines the observable content. Accepted checkpoints and inspected bytes are preserved in the protected journal. Their acceptance establishes bounded evidence checks, not hidden reasoning, faithful adoption, or semantic quality.

A real blocking question produces awaiting_user evidence and preserves WAITING_USER without a new phase or receipt. UserPromptSubmit resumes the pending phase but does not prove the user answered the question or adopted an idea. Each phase allows one bounded correction. Missing, stale, replayed or out-of-order evidence, changed fixed inputs, missing retained archives, exhausted correction, unavailable authority, or deadline expiry prevents dependent completion. Runtime-generated instructions and callbacks retain runtime provenance; no new per-phase human approval is introduced.

The selected completion mode is managed-session. During the qualifying synchronous Stop after Focus reaches READY, the runtime rechecks actual artifact bytes, exclusively publishes the selected receipt, reads its complete bytes back, verifies its current targets, and returns its actual locator and full SHA-256 through systemMessage. This can occur while the owned client remains alive. Every Stop occurrence inspects current bytes; duplicate effective native hook sources must be excluded during admission. The model writes useful artifacts and supplied evidence; it does not invoke delivery advance/resume/complete/check/verify or package receipt helpers as a manual fallback.

Receipt publication, response transport, native turn completion and human delivery are separate observations. Managed mode records a protected task-result, a fresh delivery attempt before each verified response, and transport after the socket write. SOCKET_WRITE_COMPLETED does not establish rendering; rendered delivery remains NOT_OBSERVED without direct evidence. Re-emission rechecks and reuses the historical receipt. Later drift records current inapplicability, and a later process failure remains a failed process outcome while preserving any committed task result. Process-mode synthetic fixtures instead require READY phases and successful owned-process exit; that result cannot stand in for native managed-session completion.

The saved handoff records checks already observed and creation-time NOT_RUN for later receipt, readback and delivery operations. It excludes its own complete-byte digest and is not rewritten to claim the later receipt. The runtime reports its completion separately. Unmanaged discussion and draft artifacts remain possible, but cannot claim runtime-verified completion or manufacture a receipt. Human adoption, behavioral evaluation and acceptance remain separate requirements under the [artifact contract](artifact-contract.md).

## Hooks and runtime compatibility

The former no-hooks implementation choice is superseded for the selected managed brainstorm mode. Each provider package supplies hooks/hooks.json with exactly one unconditional synchronous command handler for each of SessionStart, UserPromptSubmit, Stop and SessionEnd. No async handler or conditional matcher is selected. The thin command is `"${DEVFORGE_DELIVERY_EXECUTABLE:-devforge}" delivery hook --provider codex`, with `claude` substituted only for the Claude package. The protected supervisor supplies the selected executable, socket and session-contract digest. Without an active socket the hook returns `{}` without an enforcement claim; with an active socket, malformed or unavailable transport fails explicitly.

Each package also supplies hooks/runtime-requirements.json with exactly these fields. The provider value is specific to that package; extra keys or alternate modes are not part of this version.

| Field | Required value |
| --- | --- |
| schema_version | devforge.runtime-requirement/v1 |
| runtime | devforge.delivery |
| protocol | devforge.delivery-runtime/v1 |
| provider | codex or claude, matching the package |
| completion_mode | managed-session |
| required_events | SessionStart, UserPromptSubmit, Stop, SessionEnd, in that order |

The companion installer requires an explicit absolute --runtime executable for a delivery-aware project installation. It checks delivery capabilities and binds the executable's bytes before writes; it does not discover a runtime through PATH. It merges owned Codex groups into .codex/hooks.json and Claude groups into .claude/settings.local.json, preserves unrelated settings and identical preexisting groups, and rejects edits to owned groups. Plugin export retains the hook component and runtime requirement while reporting the eventual host runtime as unverified. A compatible capability response or successful install does not prove native admission, trust, activation or rendering.

The target terminal's effective configuration must separately establish event coverage, trust, one managed callback per event occurrence, synchronous response handling, timeout/error behavior, actual continuation/denial, and receipt rendering. Source declarations alone cannot establish these facts. A skipped or failed hook is not a completed required check; a worker-writable hook configuration is not the protected execution boundary. External acceptance independently rechecks the exact candidate. This revision adds source declarations only; actual registration and native observation require their own recorded execution allocation.

## GitHub CI and the subscription-only boundary

Ordinary GitHub Actions can run DevForge's deterministic build/tests and artifact checks. Their workflow definitions belong to the separate DevForge repository, with selected authority revision and candidate revision recorded.

The documented Codex GitHub Action lists an OpenAI API key as a prerequisite. It is therefore deferred from this subscription-only MVP; no account session credentials are exported to CI. [Codex GitHub Action prerequisites](https://learn.chatgpt.com/docs/github-action).

The release skill can prepare a PR locally and use an existing authorized GitHub interface when available. PR creation, protected-branch configuration, hosted CI success, merge, and deployment require their own observed records. The existing local POC does not establish any of those hosted outcomes.

## Failure and recovery cases required before adoption

| Condition | Required result |
| --- | --- |
| Another writer owns the worktree/branch | Stop dependent writes; preserve both sessions' work. |
| Base commit or source revision changed | Re-evaluate scope and initialize the applicable new run. |
| Skill updated only in source | Reinstall safely, observe loaded identity, and repeat affected evaluation. |
| Hook disabled, skipped, failed, or unsupported | Do not claim enforcement; external required checks still control acceptance. |
| Authority policy/CLI writable by worker | The intended protected execution claim fails. |
| Conflicting changes from separate worktrees | Integration owner resolves a new candidate and reruns relevant QA/gates. |
| Agent cannot write the external report store | Use the declared outbox or operator-saved terminal record; no silent path substitution. |
| Target terminal or required check unavailable | Record COULD_NOT_RUN with the cause and block only the dependent claim/action. |

## Provider authoring and bootstrap evaluation

Use the [authoring contract](skill-authoring-contract.md) for canonical provider sources and A/B/C evidence. Every writing assignment names one worktree, branch/base, provider, skill paths, evaluation-output root, and integration owner. Shared specifications and sibling provider sources stay outside a skill-only write fence. Source ownership is organizational unless an independently verified filesystem boundary enforces it.

The integration owner may allocate assignments and perform local Git operations when the user's task authorizes that setup. This is different from a skill worker manufacturing a baseline or claiming ownership to escape a conflict. Initial commits contain only reviewed intended project files; keep credentials and disposable client/evaluation state out of Git. Record actual commit identities after creation. Git worktrees share metadata and do not isolate subscription caches or provider settings by themselves.

An author's worktree is not a clean evaluation context merely because it is a new directory. Stage candidate/baseline and raw fixtures into separate disposable consuming projects; record what other skills, project instructions, and tools are visible. For implicit tests, supply an ordinary user request and observe actual native consultation. For tier C, use a tested isolation boundary when claiming source docs were inaccessible. If it is unavailable, report the limitation and do not substitute a changed CWD for that evidence.

B7 uses an operator-authored synthetic assignment conflict in a disposable project, with protected-tree hashes before/after. It does not create two active writers or test an unimplemented lease service. The author has a real external session record; each evaluation run separately identifies its own context and permitted output. Operator-created fixtures are evidence, not authority to change real assignments.

A discovered sibling, a proposed continuation, and an invoked sibling are separate facts. The current pilot includes four draft skills per provider and no devforge-change implementation. Negative activation can be measured without installing nonexistent routing targets. Keep required provider checks distinct from checks excluded from an explicitly single-provider scope.
