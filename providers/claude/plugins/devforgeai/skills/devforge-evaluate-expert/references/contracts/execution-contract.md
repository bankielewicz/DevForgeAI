# Packaged execution and authority contract

Operational derivation of DevForgeAI `docs/mvp/execution-contract.md`, draft revision 3, selected at base commit c17e758417da64928a0f47fc2600304465ac3f3c. Exact digests are in `../derivation.json`. These are requirements to observe, not a claim that a registry, a launcher or any hook is implemented.

## Authority and assignment

Use ordinary subscribed Claude Code sessions and the supported helpers. Human-operated transitions remain valid for existing gates. Native installation, discovery, activation, resource loading and output must each be demonstrated for the stated provider. Do not invent a slash command, a DevForge command or a callable skill for a capability that is not implemented.

A writing assignment names the actual owner, task, provider, permitted source paths, evaluation output area, protected paths, runtime configuration and integration owner. Git work also records the repository and common-directory identity, the worktree, the branch or detached state and the real base commit. Missing metadata does not prove exclusive ownership.

Concurrent writing sessions require separately assigned worktrees and unique branches or a recorded detached state. Worktrees share metadata and do not isolate credentials, client state, services, policy or acceptance. Never fabricate a base commit, and never commit another session's work to fill a template.

## Runtime and evidence

An evaluation assignment covers process control and client state as well as repository files. Give each arm and each retry a distinct attempt identity, writable output area and isolated history or memory store. A new conversation, worktree path or subagent is not sufficient on its own; verify the effective client-state mapping and the visible instructions, skills, plugins, tools and settings before relying on clean-context evidence. A retry must not inherit an earlier attempt's writable memory.

Keep writable client state inside the assigned evaluation area. Access to a terminal does not authorise deleting or modifying the user's global history, memory, configuration or credentials. Preserve contamination evidence and start a new isolated store rather than cleaning an unassigned one. Subscription sign-in and any read-only credential use need an explicit runtime arrangement; never copy credentials into an evidence bundle.

Record the processes a run launched and terminate only those, using verified identity and a private process group or PID namespace where available. Broad process-name termination can affect another author's work. Test filesystem and process boundaries with harmless probes before model execution, and if a required boundary cannot be established, preserve the cause and record `COULD_NOT_RUN` rather than falling back to an unconfined run.

## External acceptance

Installation, export, hook registration and adoption belong to the integration owner. Neither compatibility, source validation, installation nor export proves native admission, hook activation, terminal completion or rendered delivery. A hook declaration alone does not show that a client supports, enables or honours an event; verify actual interception before describing anything as enforcement, and report an unavailable integration as unavailable.

## Handoff and re-evaluation

A handoff identifies the changes, the checks actually run, the unresolved work and the next owner, with exact paths and SHA-256 bindings where the custody arrangement requires them. Preparing a handoff is not invoking a receiver and authorises no transition.

A changed candidate, installed copy, specification, fixture, baseline or material runtime setting invalidates the affected earlier conclusion and starts a new iteration. Retain the prior bytes and results.
