---
name: devforge-develop
description: Implement a bounded project story using current project expert skills and the external DevForge RED-to-GREEN acceptance workflow.
---

Read the story, approved policy, relevant expert skills, and actual baseline. Resolve absent or stale expertise using devforge-project-expert-creator before starting the development run. The current POC runner supports Python unittest; do not imply support for other runners.

The human-controlled authority terminal initializes the run with `devforge init --project <candidate> --policy <external-policy> --state <external-state>`. The agent edits only the candidate. Use the recorded state path, never a newly invented substitute.

1. Add the behavioral test while production code stays at the initialized baseline.
2. Have the authority runner execute `devforge red` with the same three paths. A valid RED has an assertion failure and no runner errors, skipped tests, or empty suite. This is observed test order, not evidence of private drafting order.
3. Implement only the declared production scope. Preserve the exact RED tests.
4. Obtain `devforge green` evidence. Fix failures within scope; changes to tests or upstream decisions require a new run rather than weakening the gate.
5. Prepare the candidate and report for review. The authority terminal runs `devforge accept` and `devforge verify` against the exact candidate after the required human/semantic review.

A normal session may invoke the CLI for convenience, but strong separation uses the external authority terminal and the tested filesystem boundary. Never claim the presence of these instructions prevents writes. No privileged actions, release, push, or merge are implied by a local accepted snapshot.

Close with exact candidate identity, phase, evidence location, unresolved findings, and the next action. If a required check cannot run, preserve the failure and stop the dependent transition.
