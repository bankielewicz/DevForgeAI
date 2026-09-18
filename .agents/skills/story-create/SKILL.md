---
name: story-create
description: Create specification-driven user stories from feature requests, selected epic outcomes, architecture seeds, QA or RCA recommendations, and deferred-work gaps. Produce source-grounded acceptance criteria, technical and applicable UI specifications, dependencies, and verification obligations in one file per story. Use for story authoring and selected story batches; implementation, product QA, existing-story audits, epic creation, and sprint planning are separate tasks.
metadata:
  version: "0.1.0"
---

# Story Create

Turn the selected outcome into a story a fresh implementation or assessment session can use. Preserve its requirement sources, canonical shared contracts, open decisions and acceptance obligations. Authoring a story does not implement its behavior or qualify it for release.

## Runtime prerequisite

This is an adaptive **core** package. Its [descriptor](assets/devforgeai-skill.json) and [contract](references/adaptive-contract.md) define the responsibility. Resolve the selected project and the actually loaded skill directory. Discover Python 3.10+ and run the bundled read-only observation **before product actions**, on resume, and after binding/package changes:

```text
python -B -X utf8 <loaded-package>/scripts/check_project_binding.py --project-root <selected-project> --skill-root <loaded-package>
```

Use native shell quoting or an argument vector so paths remain data. Continue only for exit **0**, status **MATCH**, reason **BOUND**. Any other result stops story writes and downstream workflow calls: report its sanitized reason and the separately owned installation/rebinding prerequisite. Missing Python is unavailable, not a match. Do not install dependencies or create a binding here. Read-only explanation remains possible.

The result observes project/root/package/role consistency. It grants no permission, protected approval, or acceptance. A previous match cannot qualify changed bytes. Honor current user scope and actual host permissions throughout.

## Select and author

1. Read [intake and scope](references/intake-and-scope.md). Resolve selected inputs, applicable project rules, literal destinations, identity and metadata. Reuse supplied answers; ask only about missing decisions that change the story. An existing specification supplies context without selecting all its deliverables.
2. Load the branch that matches the request:

   | Selected input | Resource |
   | --- | --- |
   | One feature, defect, refactor or documentation outcome | Continue from intake |
   | Epic outcomes, several stories, coverage gaps or shared prerequisites | [Batch and dependencies](references/batch-and-dependencies.md) |
   | QA/RCA recommendations or deferred-work findings | [Recommendations and gaps](references/recommendations-and-gaps.md) |
   | Architecture document or selected story seed | [Architecture seeds](references/architecture-seeds.md) |

3. Draft the user outcome, scope, provenance and acceptance criteria using [acceptance criteria](references/acceptance-criteria.md). Consult [domain patterns](references/domain-patterns.md) only for relevant behaviors. Resolve requirement ownership and dependencies before presenting dependent work as ready.
4. Use [technical specification](references/technical-specification.md) to define applicable interfaces, components, constraints and test mappings. Read [UI specification](references/ui-specification.md) when the selected behavior has an interface; record why it is inapplicable otherwise. Ground design in the actual project and selected sources.
5. Assemble the [story template](assets/templates/story-template.md) using [its contract](references/story-contract.md). One story is one complete `.story.md` file, including its technical/UI content. Shared canonical specifications remain external references; do not copy them into competing sources of truth.
6. Follow [delivery and resume](references/delivery-and-resume.md) for content review, safe writes, complete readback, selected link updates and the final handoff. Finish the authorized batch, continuing independent work after a local failure and explicitly blocking its dependents.

The primary owns all file writes. Do the analysis directly. When delegation is explicitly allowed by the current request or applicable host policy and has a concrete benefit, provide a bounded content-only or read-only task with the selected sources, expected content, exclusions and return format. No named agent profile is required. A delegated response is evidence to inspect, not proof of correctness or independence.

## Effects and limits

Create the requested story files, an external session record when useful for a batch/interruption, and authorized links in the explicitly selected related documents. Do not overwrite a different existing story, alter governing specifications to hide a conflict, or mark implementation/QA obligations complete while planning them.

No fixed language, architecture, story count, phase count, numeric product threshold, agent roster, Git repository, browser, MCP server or external service is required. Terminal file operations are sufficient for authoring. Use actual project-mandated authority interfaces for protected operations; if such an authority is unavailable, report the affected operation as blocked. Do not simulate it with prose, checkboxes or Python.

Deliver exact written paths and unresolved requirements. Development, independent product QA, skill-package evaluation, installation and deployment remain separately selected work. A manual handoff does not invoke its consumer.
