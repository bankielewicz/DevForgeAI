# Intake

**Purpose:** Recover the actual assignment and authority before selecting work.

**Inputs:** Request, selected source and specification, provider, ownership/write fence; supplied findings if remediation.

**Work (Enforced):**

## Recover framework authority and the target

Read [framework context](../references/framework-context.md) and the selected [skill-authoring contract](../references/contracts/skill-authoring-contract.md). Resolve each package link relative to its containing file within the loaded skill root, independently of the shell working directory. Resolve the consuming project and its artifact destinations separately; do not require the framework checkout at runtime.

Recover the current request, concrete workflow or project goal, assignment scope, provider, accepted specification and source revisions, and applicable project/framework instructions. Recover approved architecture, actual relevant code and pinned dependencies when the target expertise depends on them. Preserve source URLs, retrieval dates, applicable API versions, claims and refresh conditions. A newer API version is a proposal, never an implicit stack change. Record actual source paths and revision or preserved-byte identities, contract/template SHA-256 values, and any missing inputs. A missing value remains unknown with a reason; do not fabricate a revision, hash, owner, or approval. Preserve the selected prior inputs when newer conflicting sources appear. Reconcile only the affected authoring before proceeding.

For a framework skill, the canonical Codex source is `providers/codex/plugins/devforgeai/skills/<name>` in the selected framework checkout. `.agents/skills/<name>` and exported plugin packages are generated runtime copies, not alternative authoring sources. Work only in the assigned provider and skill. Project-specific skills need an explicit source-to-installation mapping; do not assume a personal or installed path is canonical.

Do not modify sibling DevForge gates, shared contracts, installer policy, the accepted roster, or another skill to make this candidate pass. Report a contract or integration gap to its owner. Authoring completion is not framework adoption, release, native activation, or behavioral certification.

## Choose the entry path

Use the conversation and supplied materials before asking questions. Establish the workflow, typical request, result, and target environment. Distinguish design-only work from authorization to create or enhance files. Once the necessary decisions and authoring scope are settled, proceed without adding a blanket approval checkpoint.

- For a new idea or ordinary enhancement, continue to Selection; load its discovery guide there and the interview guide when Design begins.
- For findings from `devforge-evaluate-expert` or another supplied validation report, start with its handoff and named evidence sections, then read [the validator handoff guide](../references/validator-handoff.md). Preserve its frozen target/specification, finding IDs, expected behavior, evidence, and prior results. The validator evaluates; this builder owns edits. Do not restart settled Q&A or execute the validator.

## Outputs and continuation

Save actual authority, source/provider mapping, write fence, accepted decisions and missing inputs in the working specification. Framework workflows need the concrete workflow goal and applicable framework contracts; application architecture/code/API versions are required only when the target guidance depends on them. Do not demand application architecture to reorganize framework instructions.

Continue to [Selection](02-selection.md) when the assignment permits discovery. Missing required source or ownership blocks dependent authoring; preserve the gap and continue unaffected discovery. Load remediation details only when supplied findings apply.
