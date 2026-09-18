---
description: Audit the framework for wiring rot, silos, and dead code (orphans + dangling references)
argument-hint: "[--audits=agents,hooks,skills,commands,code,retired] [--retired-registry=<path>] [--strict]"
model: opus
allowed-tools: Read, Skill, AskUserQuestion
---

# /audit-rot

Pure orchestrator. ALL logic — engine invocation (`devforgeai-validate audit-wiring`),
dead-code orchestration, GROUNDED-vs-INCONCLUSIVE classification, and report synthesis —
lives in the framework-rot-audit skill.

No scanning, no grep, no classification, no display logic here. The skill handles everything,
and the deterministic CLI engine (never the LLM) is the source of every wiring finding.

```
Skill(command="framework-rot-audit")
```
