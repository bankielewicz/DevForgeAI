# Framework POC scope

This slice makes project-specific expert creation concrete through a maintained creator skill, a specification template, behavioral evaluation cases, two distinct example experts, and executable provenance/freshness checks in the companion Rust CLI.

It also provides a brainstorming workflow and a minimal development/review handoff. Mockup generation, SaaS architecture automation, epic/story semantic derivation, sprint planning, deployment, and production release control remain future capabilities. Their absence does not become an implicit claim of implementation.

The example expert skills were authored during this POC implementation using the stated synthetic project contracts and official Python references. The scripted demo copies those authored artifacts; it does not call a terminal model to generate or evaluate them. Use the expert creator in an interactive subscribed session to exercise that separate behavior.

## Repository boundary

| Repository | Owns |
| --- | --- |
| DevForgeAI | Skills, plugin manifests, subagent definitions, expert specs, project examples, and conversational methodology. |
| DevForge | CLI, external policy, deterministic gates, fixed test runner, installation/validation scripts, and GitHub workflows. |

The [external runbook](../../DevForge/docs/POC.md) explains how the worker's filesystem boundary and the human-controlled acceptance terminal implement the POC separation. Simply opening the two repositories in one unrestricted AI session does not impose that boundary.

## Sources checked on 2026-09-04

- [Codex skills](https://learn.chatgpt.com/docs/build-skills): project-local `.agents/skills` discovery and progressive loading.
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): standalone TOML definitions and session configuration.
- [Codex authentication](https://learn.chatgpt.com/docs/auth): subscription sign-in differs from API-key use.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks): useful integration points with documented enforcement limits.
- [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference) and [subagents](https://code.claude.com/docs/en/sub-agents): native packaging and agent definitions.
- [Claude subscription use](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan): interactive subscription access and limits.
- [Python 3.12 sqlite3](https://docs.python.org/3.12/library/sqlite3.html) and [json](https://docs.python.org/3.12/library/json.html): APIs used by the two fixture implementations.

Local provider packaging was checked with the installed plugin/skill validators. See companion validation evidence for the installed versions and actual outcomes. No unsupported claim of general hallucination reduction, independent model review, or hosted CI acceptance is made.


## Provider migration and current pilot

Canonical sources are providers/claude/plugins/devforgeai and providers/codex/plugins/devforgeai. See the [shared authoring contract](mvp/skill-authoring-contract.md). Core sources are separate; --include-experts still explicitly installs the portable synthetic expert fixtures. That fixture convenience is not proof that arbitrary provider-specific skills are interchangeable.

The companion installer now filters authored evals from runtime copies and can export a runtime-only plugin. The four skills per provider remain drafts requiring the expanded specifications. Native behavioral acceptance is pending. The immediate continuation is SKILL-001 C/B/A evaluation under assigned provider worktrees, then SKILL-002 consuming its ledger.
