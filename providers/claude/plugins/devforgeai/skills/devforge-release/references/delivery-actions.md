# Delivery actions: authority, commands, and what each one proves

Read this at Recheck, before any external action, and whenever an external outcome is about to be recorded.

The user initiates each skill and each command. This package schedules nothing, invokes no other skill, and holds no credentials. Authoring, review, evaluation and integration are distinct responsibilities, and a user authorizing several of them in one assignment does not merge them.

## Five actions, five authorities

PR drafting, PR creation, merge, deployment and release acceptance are separate actions. Execute an external one only within an authorization the user already has - something they said in this task, or a standing delegation whose scope actually reaches this action and this target. Ask only when the required authority is missing, and ask for the specific one.

| Action | What it changes | What has to be true first |
| --- | --- | --- |
| Draft PR material and release notes | Nothing outside the artifact destination | The candidate identity rechecked; the applicable architecture requirements read |
| Push a branch | A remote ref | Authorization covering this remote and branch; the branch is not another writer's |
| Create a PR | A review request others will act on | Authorization for this repository; the draft exists; the target branch is current |
| Merge | The target branch's history | Separate authorization; the PR's own required checks in whatever state they are actually in |
| Tag, publish or deploy | A release others will run | Separate authorization; the migration and recovery steps recorded; a rollback path |
| Communicate externally | Someone's inbox or a public channel | Separate authorization; this skill sends nothing on its own initiative |

Three things that look like permission and are not:

- **A readiness recommendation.** A review-report saying "ready for the stated next step" is a reviewer's judgement about the candidate. It is not the user authorizing publication, and the review-report's own `decision_ref` records a decision about that document, not an adoption here.
- **An `accepted` status upstream.** A document's status records drafting and adoption of that document.
- **Working tooling.** That a CLI is installed and authenticated says only that the action would succeed, never that it is permitted.

Where the authority is genuinely absent, the correct result is a complete draft, the action recorded `NOT_RUN`, the specific authority named, and its owner named. That is a finished result.

## What the DevForge CLI actually covers

The companion DevForge CLI is a separate compiled program. Use absolute paths for the project, policy and state directories; the operator supplies them. Inspect the selected executable's own `--help` before relying on any of this - the rows below state what each command proves, which is always narrower than the phase it supports.

| Owner and action | Command | What it proves, and what it does not |
| --- | --- | --- |
| Operator verifies a candidate against its accepted snapshot | `devforge verify --project <abs-project> --policy <abs-policy> --state <abs-state>` | Compares bytes and modes between the accepted archive and the current candidate tree. It proves those two trees agree. It has never read a review-report, does not know what a QA identity is, and says nothing about semantic correctness or release readiness. |
| Operator checks structural policy and provenance | `devforge check --project <abs-project> --policy <abs-policy>` | Checks approved dependencies, layout, tooling pins and expert provenance against the external policy. Its own help text says it does not certify semantic behavior. It does not check this skill's workflow. |
| Operator inspects durable phase state | `devforge status --project <abs-project> --policy <abs-policy> --state <abs-state>` | Reports the recorded phase state in the external state directory. It reports what was recorded; it does not re-derive it and does not judge it. |

These accept their flags at the leaf subcommand, as their own `--help` output shows. A missing binary, a missing policy, a missing state directory or a stale lock means `COULD_NOT_RUN` with that cause - not a skipped check quietly recorded as fine, and never an auto-recovery. There is no force-unlock and no gate-skip; a stale lock or a leftover interrupted transition is inspected by a person.

## What has no integration at all

**No DevForge subcommand creates a pull request, pushes, merges, tags, publishes or deploys.** That capability does not exist in the CLI surface. Do not name one, and do not describe a suggested `git` or hosting command as a gate - a command someone might run and an exit status nobody reads are both advisory.

External actions therefore run through the user's own Git tooling and their own hosting interface, under the permission settings they already have. This package declares no `allowed-tools` in its frontmatter, so it grants nothing; every tool call is governed by the user's existing settings exactly as it would be without this skill loaded.

Record that as a capability gap when it matters to the result, rather than working around it. If a requirement genuinely needs a dependent action blocked - no merge without an authorization reference, say - record it as a requirement, naming the action, the evidence to check and the intended allow or refuse behaviour, and route it to the integration owner who owns the check and its wiring. Recording a requirement is design input. It is not evidence that any client supports, enables or honours such a check.

## CI and verification evidence

Hosted CI, a local test run and a structural check are three different observations and never one status.

- **A local run** is evidence about this machine and this moment. Record it with the exact revision it ran against and where its output lives. It is not hosted GREEN.
- **Hosted CI** is evidence only when you have a result locator and the exact revision it ran on. Unavailable, unreachable, or simply not yet run for this revision is `COULD_NOT_RUN` or `NOT_RUN` with the actual cause.
- **A structural check** proves which inputs were referenced and that a layout holds. It never proves that behaviour is correct.

This framework uses no model API key anywhere, so a model-driven CI action that requires one is outside its scope; record it as `NOT_APPLICABLE` with that reason rather than as a missing check. Ordinary CI that runs deterministic builds, tests and artifact checks is unaffected and is the thing to cite when it exists.

A passing suite is evidence for the behaviour it tested. It is not proof of all requirement semantics, and it is not a human release decision.

## After the fact

Reading back what was created is part of the action, not a separate courtesy. A PR that was created has a URL that resolves; a merge has a commit; a deployment has a reference in whatever system performed it. Cite what you read, with when you read it.

A tooling failure during an authorized action is a failure. Record it as one, preserve the partial state for inspection, and do not retry indefinitely. Two successive attempts at the same blocker with no new evidence means stop and report the concrete alternative.

Operational failure after a real release becomes a change request or the project's existing incident process. It is not a correction to a frozen release record: that record described what was true when it was written, and rewriting it destroys the only account of what actually happened.

## Ownership and concurrency

Every writing session has one writer, an assigned worktree and branch, and a declared fence. Worktrees share Git metadata; they reduce working-file collisions and do not isolate refs, configuration, credentials or external services.

If an assignment record gives the worktree, branch or destination to another writer, stop the dependent writes and report the collision - naming the record you saw and where you read it. Preserve both sessions' work. Do not delete, reset, revert, stash, clean, force or switch anything, and do not relocate to an unassigned path.

A worker-authored session ID is not proof of ownership, and the absence of a session record does not establish that you are the single writer. Record the task authorization actually held, inspect for collision evidence, and proceed only within an observable scope.
