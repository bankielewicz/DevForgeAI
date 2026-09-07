# Skill-builder evaluation requirements

Selected from the user's explicit requirements in this Codex task, recovered 2026-09-07 before measurement. This is an evaluation input, not a newly accepted complete builder design and not a modification of the skill.

## Source and scope
The current user invokes skill-validator on skill-builder. Prior user requests specify an MVP authoring-only builder, followed by a DevForgeAI-specific enhancement and a separate validator. No populated standalone design of the enhanced builder was found in the searched docs/research/Skills and framework docs/skill-authoring paths. The blank asset template is not that missing design. Full conformance to an unprovided original design cannot be asserted; the explicit requirements below can be reviewed independently.

## Explicit user requirements
- SB01: Take user input and brainstorm through focused Q&A to determine the workflow and needs.
- SB02: Search for similar existing skills before creating a duplicate; recommend enhancing an appropriate existing skill or create when none suitable is found. Scope the claim to searched sources.
- SB03: Populate the skill specification template and build or enhance the selected skill.
- SB04: For each workflow, phase and task, ask Optional versus Enforced when unclassified. Preserve an explicit named-group decision.
- SB05: For enforced items, propose a hook design.
- SB06: Builder authors only; validation/testing belongs to skill-validator. Do not validate the target or activate the proposed hooks during builder work.
- SB07: The builder is the entry point for DevForgeAI custom framework skill creation/enhancement and contains intrinsic DevForgeAI knowledge, with concrete current capabilities.
- SB08: Include the reusable skill-design-spec.md template.
- SB09: Consume validator repair/enhancement recommendations to edit the selected skill. Validator evaluates and hands off; builder owns target edits.
- SB10: Make workflows concrete with appropriate references and explicit unresolved facts; do not represent aspirations as implemented or tested capabilities.

## Selected governing sources
Evaluate the candidate's selected preserved authoring contract revision 2 and the paired source/installed mapping. A concurrent revision 3 is a separately reported refresh consideration, not a retroactive requirement. Framework AGENTS.md supplies provider ownership and canonical-source rules. Exact inputs and source hashes are in input-manifest.json.
The Agent Skills format specification preserved at docs/research/Skills/specification.md supplies structural name/description constraints. New style preferences or new framework behavior are proposals, not accepted requirements.

## Evaluation limits
No original standalone enhanced-builder design is supplied. Independent AI review is scoped to SB01-SB10 and the selected contracts. Native C/B/A results require actual observed isolation, subscribed runtime and a frozen budget; static inspection or a fresh subagent is insufficient. These limits cannot be converted into target defects without a controlling requirement and concrete evidence.

