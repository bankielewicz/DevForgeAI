---
name: devforge-project-expert-creator
description: Create or refresh a dedicated expert skill for a project's concrete goals, approved architecture, selected APIs, and recurring work; evaluate it with project-specific cases.
---

Produce useful project expertise rather than a generic expert persona. The same core workflow must adapt to projects with different approved stacks. This skill authors expertise; the external DevForge CLI records structural provenance and gates development candidates.

## Establish the task and authority

Identify the candidate project, the externally selected policy file, the DevForge executable, the required role, and the goal/story needing it. Use the owner's supplied paths. Do not locate a more permissive policy or modify the validator to get a pass.

Run `devforge expert prepare --project <project> --policy <external-policy>` and inspect its context. Read the named upstream documents, actual relevant code, and approved dependencies. If the project is new or required policy is absent, draft the missing decisions and surface them to the user rather than inventing approval.

Read assets/expert-spec-template.md when specifying a new expert. Write the capability specification before the skill, with independently stated expected outcomes. Reuse existing expertise when it covers the work.

## Author project expertise

Write `SKILL.md` under the declared expert directory. Include valid name and description frontmatter, precise activation, project-specific decision guidance, required inputs, deliverables, verification, and handling of uncertainty. Supply focused references for architecture, version-specific APIs, and verified examples. Load these progressively; do not duplicate all project documents.

Research the selected version using official sources. Record the source URL, retrieval date, relevant package version, and actual verification. Missing evidence stays unresolved. A newer available version is a proposal to investigate, not permission to replace the approved stack.

Skills do not grant tool permissions. Put executable control logic in the external DevForge project. Local expert references may explain the gate but must not redefine it.

## Bind, evaluate, and refresh

Run `devforge expert bind --project <project> --policy <external-policy> --expert <declared-relative-expert-directory>` then `devforge check` with the same project/policy. Binding covers exact policy, upstream documents, and all expert files except binding history. It explicitly leaves behavior NOT_EVALUATED.

Exercise the skill on realistic tasks using assets/evaluation-cases.md. Preserve actual results and the exact skill/input versions. Use a separately initiated evaluation session when independent behavioral review is needed. Do not provide the author’s desired solution to the evaluator. Do not claim evaluation was run if only structure was checked.

When policy, upstream content, or expert files change, `devforge expert status` reports STALE. Review the semantic changes, update the skill/references, repeat affected evaluations, and bind the revised content. Prior bindings are retained by digest. Start a new gate run when its governing policy or expertise changes; existing evidence cannot be carried forward silently.

Close with specification and skill paths, sources used, structural status, behavioral status, remaining gaps, and the next human-owned decision. Never silently mark a skill as a proven expert because it passed structural validation.
