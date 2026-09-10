# Version evidence and existing stacks

Read this in Resolve, whenever a decision turns on how a specific package version actually behaves, and whenever the project already has a stack.

## The version you remember is not the version pinned

Model knowledge of an API is an average over versions, and an architecture contract is the one document where that average is dangerous: the version it pins is the version every later session is governed by. A familiar example that does not match the pinned version is a signal to verify, never a licence to move the pin so the example fits.

So when a claim about API behaviour would change a decision:

1. Read what the project has actually pinned - the manifest and, where one exists, the lockfile. Record the path where you observed it, because "the version in the lockfile" and "the version someone mentioned" are different facts.
2. Check the claim against a primary source for that exact version.
3. Record what you verified, not that you looked.

## What a verified claim records

| Field | Content |
| --- | --- |
| Source | The URL, or the reference the user supplied. |
| Applicable version | The exact package version the claim holds for. |
| Retrieval date | When you actually read it, in UTC. |
| Claim supported | The specific statement it supports - not the page's subject. |
| Limitations | What the source does not establish, and what would make it stale. |

A source that supports "this API exists in 8.0" does not support "this API behaves the same in 6.0". Keep the claim no wider than the evidence.

## When you cannot verify

The claim stays unresolved. Record it as an open question with the observation that would settle it, put the affected decision in `proposed` state, and name what it blocks. Do not convert an unverified recollection into confident prose, and do not select a version because it is the one you could find documentation for.

Where an execution risk cannot be settled by reading at all - performance under the project's real load, an integration whose behaviour is undocumented, a migration whose cost is unknown - that is a prototype question. Name it, route it, and leave the decision open. Check what is actually installed before naming a skill as the next step.

## An existing stack is a decision already made

On an established project most of the contract already exists in the repository, and the observed state is evidence about the project.

- **Preserve what the user has retained.** If the repository uses a package and the user has said they are keeping it, that is an adopted decision. Record it as such, with the manifest path where you observed the version.
- **An alternative you prefer is a proposal, and only when it was asked for.** Where the user explicitly requests a comparison, record the alternative as an explicitly requested proposal with its rationale, its migration cost and its decision state - never as a rule, never as the default, and never by editing the retained decision's row.
- **Do not replace a stack by describing a better one.** Writing a different package into the contract does not migrate anything; it just makes the contract false about the code.
- **Prohibited substitutions are worth writing down.** Where two packages solve the same problem and the project chose one, record the exclusion explicitly so a later session does not add the other for one convenient feature.

The inventory is the deliverable for an existing project: what is actually depended on, at which versions, recorded where, with which rules already in force and which gaps genuinely unresolved.

## A newer release is a research trigger, not an upgrade

A new version of an approved dependency is something to raise. It is never by itself authorization to change the stack, and neither is a security advisory, a deprecation notice, or the fact that the newer version is obviously better.

Record it as observed context: the release, what it changes that matters here, and which ADR or RULE IDs it would affect. Then route the proposal to `devforge-change`, which owns amendments to accepted contracts - and, because much of the roster is specified but not implemented, say plainly whether that skill is actually installed and give the user a next step they can act on if it is not.

The one thing not to do is apply the upgrade in the contract and mention it afterwards. That is adoption with an undo button: it puts the user in the position of having to notice and reverse a commitment they never made.

## Research is bounded

Research the claims that change a decision. An architecture contract does not need a citation for every sentence, and a survey of an ecosystem is not what the user asked for. Where a claim does not change a decision, the honest record is that it was not investigated.
