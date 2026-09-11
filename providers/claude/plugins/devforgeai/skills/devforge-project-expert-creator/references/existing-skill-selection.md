# Existing-skill selection

Discovery decides between reuse, enhancement and creation. Inspect instructions and resources only. Do not run a candidate, test its behaviour, or install anything to find out what it does.

## Where to look in a Claude environment

Start with the catalogue the environment actually exposes and with any target the user named directly. For framework work, search the assigned provider's canonical source inventory before interpreting an installed match, because an installed copy tells you a skill is present but not where it may be edited.

Skills reach a Claude session from several places, and they are not equivalent:

| Location | Scope | Notes for selection |
| --- | --- | --- |
| `<project>/.claude/skills/<name>/SKILL.md` | This repository's sessions | Loaded from the starting directory and every parent up to the repository root. |
| `<subdir>/.claude/skills/<name>/SKILL.md` | Sessions at or below that subdirectory | Loads when work touches files there. A nested skill can share a name with a root one; both stay available. |
| `~/.claude/skills/<name>/SKILL.md` | Every project on this machine | Personal, outside any repository. Easy to forget and easy to shadow with. |
| A plugin's `skills/<name>/SKILL.md` | Wherever the plugin is enabled | Generated or distributed; the plugin source is the thing to edit, not the installed plugin. |
| Managed settings directory | Organisation-wide | May be present and unreadable. Record it as an unsearched location rather than assuming it is empty. |
| An `--add-dir` directory | That session only | Present for this session and gone in the next. |

A `.claude/skills/<name>` entry can be a symlink to a directory elsewhere; resolve it rather than treating the link and its target as two capabilities. A generated copy and its canonical source are one candidate lineage. Windows and WSL can carry separate inventories - resolve actual locations instead of assuming shared storage.

Include authorised repository or catalogue sources the user supplies. Do not install plugins to inspect them and do not expand into an open-ended internet search.

## Comparing candidates

Read filenames and the `name`/`description` metadata first to shortlist, then read the plausible candidates' instructions and only the resources you need.

| Dimension | What to compare |
| --- | --- |
| Purpose | The job it does and the outcome it intends. |
| Activation | The requests and situations that should select it. |
| Scope | Work included, work excluded, and who owns each. |
| Inputs and outputs | Required context and access; the artifacts actually delivered. |
| Process | The essential steps, decisions and rules. |
| Behaviour | What it actually does with a representative request, read from its instructions - not run. |
| Runtime | Provider, tools, environment, dependencies. |
| Authority | Governing specification, durable source, assignment and integration owner. |

A shared name, role or toolset does not establish duplication. A general-purpose creator skill is relevant when the requested target is an authoring workflow, and is not a duplicate of every skill it could produce. A framework utility can be genuinely distinct from a roster skill when their outcomes, scope or authority differ - which does not authorise adding it to the accepted roster or changing a sibling gate.

**Cross-provider equivalents are not duplicates.** The Claude and Codex packages of the same framework skill are intentional provider implementations with separately tracked behaviour, and the authoring contract gives them separate canonical sources. A Codex package existing is not a reason to delete, merge or re-point the Claude one, nor evidence that the Claude one is redundant - and it is not yours to edit unless you were assigned that provider. Compare within your assigned provider to decide reuse, enhancement or creation; record the other provider's equivalent as context, with its path, and leave it alone. Where the two have diverged, that is a fact for the report, not a defect to fix here.

For a project expert specifically, the comparison that matters is whether an existing expert already carries the decisions and versions this story needs. Overlapping subject matter is not enough: an expert for the same subsystem built against a superseded architecture rule is a refresh candidate, not a reuse candidate. For a framework workflow skill, the equivalent question is whether an existing skill in the same provider's roster already owns this workflow and could absorb the gap without blurring its activation.

## Choosing

- **Reuse.** An existing capability already meets the need. Recommend it, say what it covers, and stop. This is a successful outcome, not a failure to deliver.
- **Enhance.** A candidate owns the same workflow and can absorb the gap without confusing its scope or activation. Name the durable source and what must be preserved.
- **Create.** Nothing suitable was found in the searched inventory, or a meaningfully distinct boundary warrants a separate skill. Explain the distinction in terms of activation and scope, not subject matter.
- **Resolve first.** Several candidates fit, or a source you cannot read would change the answer. Put the relevant differences in front of the user as a focused question.

Find the durable editable source for any generated, bundled, cached or read-only candidate before proposing changes to it. For Claude framework work that is this repository's `providers/claude/plugins/devforgeai/skills/<name>`; project-local `.claude/skills` copies and exported plugins are generated. If the durable source or the assignment is unavailable, preserve the enhancement as a proposal and record the gap. Never silently edit a cache, pick an unrelated destination, or create a duplicate because the real one is out of reach.

Inspect the destination for a collision before writing. A collision requires inspection and reconciliation; it is not permission to overwrite. Preserve unrelated existing behaviour, resources, dependencies, identity and invocation policy.

## During a bounded repair

A frozen evaluator handoff already identifies a target, and it normally implies enhancing that same source. Keep the prior search and decision rather than repeating the inventory. Refresh only the comparison that new findings actually affect - a finding that changes purpose, ownership, scope or destination.

Compare the current source against the supplied frozen manifest before applying anything. If it drifted, identify which files and requirements are affected and reconcile with current ownership before proceeding. Do not apply stale findings blindly and do not overwrite concurrent edits.

A report with no native activation evidence does not prove a duplicate selection or a source defect. Record the missing observation as an evaluation prerequisite unless other evidence supports a bounded authoring change.

## What to record

In the design specification:

- Locations actually searched, locations excluded or unreachable, and the limits of the comparison.
- Candidate paths, provider and source identity, the overlap and the gap.
- The chosen action and why.
- The canonical target and its generated installation or export mapping.
- For an enhancement, the intended changes and the behaviour being preserved.
- Contract, ownership or integration gaps, and any unresolved decision.

Use "No suitable skill found in the searched inventory" when that is what happened. Candidate inspection is not validation: do not report testing, and never claim global uniqueness from a bounded search.
