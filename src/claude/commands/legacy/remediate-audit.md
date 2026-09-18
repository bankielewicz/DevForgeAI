---
description: Remediate a validated DevForgeAI enterprise audit run through the shared deterministic CLI
argument-hint: <run-id> [--finding <id>] [--dry-run] [--resume]
allowed-tools: Read, Skill, AskUserQuestion, Bash(devforgeai-validate:*)
---

# /remediate-audit

Validate the explicit run ID with `devforgeai-validate audit-findings-status`
before invoking the skill. Reject a Markdown path or absent durable register.

Skill(command="remediating-devforgeai-audit", args="{user_args}")
