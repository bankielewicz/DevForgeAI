# DevForgeAI POC

This repository owns conversational workflows, skills, agent definitions, examples, and project expertise. Its companion repository is https://github.com/bankielewicz/DevForge and owns the Rust CLI, policy, tests, and GitHub workflows.

Work from the user's task and applicable skill. Capture brainstorming suggestions as proposals; preserve accepted project decisions and their source revisions. Use project-specific facts and verified library references when authoring expert skills. A provenance binding is not evidence of expert behavior.

When working on this framework or a generated project, do not change sibling DevForge gates or policy to make a candidate pass. Report a contract defect to its owner. Framework maintenance explicitly requested by the user may change framework sources; application work may not silently change its governing framework.

Canonical framework skill sources are provider-specific: providers/claude/plugins/devforgeai/skills and providers/codex/plugins/devforgeai/skills. Work only in the provider and skill named by your assignment. Claude plugin agents are in providers/claude/plugins/devforgeai/agents; Codex subagent templates remain in providers/codex/agents. Per-skill agents/openai.yaml is optional Codex metadata, not a subagent. Installed copies and exported plugins are generated artifacts, never alternative canonical sources.

For skill authoring, read docs/mvp/skill-authoring-contract.md and the relevant specification/templates. Shared contracts and installer integration have one integration owner; report ambiguities rather than changing them from a skill-only assignment. Authored eval inputs live under the skill's evals directory, while run outputs live in the assigned provider evaluation workspace. No package or file-hash check certifies native activation or behavioral quality.

The POC is Linux/WSL2 and local-only. Read docs/POC.md for commands, actual guarantees, and remaining evaluation work.
