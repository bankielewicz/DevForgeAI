# User-supplied documentation and design applications

Retrieved 2026-09-04 through the official OpenAI documentation tools. These are concise research notes and a [structured source inventory](sources.json), not immutable archives of the full web pages. Provider behavior can change; certify the actual terminal version used for each evaluation.

## SRC-001: Brainstorm plugin use cases

Source: [Brainstorm plugin use cases](https://developers.openai.com/plugins/plan/use-case).

Application to this package: Each skill has a user goal, direct and indirect requests, required context, expected output, capability choice, action boundary, support decision, and behavioral cases.

## SRC-002: Build skills for plugins

Source: [Build skills for plugins](https://developers.openai.com/plugins/build/skills).

Application to this package: Use focused native skills and creator-assisted authoring; supporting resources are package-local. Skills can operate without an MCP server.

## SRC-003: Package your plugin

Source: [Package your plugin](https://developers.openai.com/plugins/build/plugins).

Application to this package: Packaging and installation remain distinct from skill behavior. Native manifests, marketplace distribution, installed copies, and hook trust need their own verification.

## SRC-004: Prompting

Source: [Prompting](https://learn.chatgpt.com/docs/prompting).

Application to this package: The authoring and handoff prompts name the goal, relevant context, output, consequential boundaries, and observable verification; they avoid scripting every reasoning step.

## SRC-005: Build skills

Source: [Build skills](https://learn.chatgpt.com/docs/build-skills).

Application to this package: Keep activation descriptions discriminating and load detailed references progressively. Test actual skill discovery and updates in the target terminal.

## SRC-006: Hooks

Source: [Hooks](https://learn.chatgpt.com/docs/hooks).

Application to this package: Non-managed hook trust, concurrent matching hooks, and unavailable/error MCP hook behavior prevent treating hook presence as conclusive acceptance. External checks remain authoritative.

## SRC-007: Worktrees

Source: [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees).

Application to this package: Each concurrent writer gets a distinct checkout/branch or recorded detached base. Git metadata remains shared. Desktop-managed handoff and ignored-file copying are not assumed in manual CLI worktrees.

## SRC-008: Codex GitHub Action

Source: [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action).

Application to this package: The documented Action lists an API key as a prerequisite. Defer this model CI path under the user's subscription-only constraint; deterministic GitHub Actions remain in scope.

## User requirements and interpretation

The user's request supplies the lifecycle, project-specific expert creation and refresh, separate DevForge enforcement repository, no required model API billing, and concurrent-session worktree requirement. The 12-skill partition and document names are proposed design decisions, not facts asserted by OpenAI documentation.

Git worktrees are an execution primitive shared by the terminal workflows; the linked page's desktop UI operations are not prescribed as CLI operations. Hooks are optional integration adapters. A listed marketplace plugin or a frontmatter-valid skill still needs observed installation and behavior in each terminal.

Claude behavior must be evaluated independently. These OpenAI sources do not establish Claude command names, hook schemas, authentication behavior, or feature parity. The POC's existing Claude package remains an unevaluated input until exercised in its native runtime.

## Scope decisions resulting from the sources

- A core skill exists only when it completes a recognizable user goal.
- General skill/package authoring can reuse native creators; the project expert workflow adds project-specific evidence and evaluation requirements.
- Worktree allocation, artifact verification, and external acceptance are tooling/operator responsibilities rather than extra conversational roles.
- Full model automation inside GitHub CI is deferred because the cited setup does not satisfy the requested subscription-only baseline.
- Source revisions and actual runtime observations belong in provenance. Documentation alone is not runtime acceptance evidence.


## Agent Skills authoring refresh, 2026-09-05 UTC

SRC-009 through SRC-015 in sources.json identify the seven Agent Skills topics, their URLs, retrieval times, cached web-tool responses, SHA-256, and design applications. Direct HTTPS download was blocked by the shell network policy; the browser tool provided the saved rendered responses. These may be excerpts and are not raw HTTP/full-page snapshots.

The review separates open-format requirements, provider extensions, DevForgeAI conventions, and native runtime observations. Separate provider sources, filtered runtime exports, three result tiers, and synthetic B7 conflicts are explicit project choices. No native behavior or protected gate is established by those conventions.

The script guide's relative-command assumptions need actual terminal verification: Markdown resource paths do not change shell CWD. The host guide's suggested duplicate precedence and context retention are implementation guidance, not Codex/Claude guarantees. A native creator's run_loop.py needs inspection for installed-source selection, consultation detection, version, and authentication. Manual subscribed terminal runs remain a valid MVP method.
