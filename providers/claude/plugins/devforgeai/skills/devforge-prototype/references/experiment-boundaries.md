# Experiment boundaries, evidence and disposition

Read this when you set the fence, when a measurement will not run, when a result misses its threshold, or when someone asks what should happen to the prototype code.

## The fence

The fence is the set of paths the experiment may write, the tools and services it may use, and the effort it may spend. It comes from the user or the assignment. It is not a formality: it is the thing that keeps an experiment from becoming an unreviewed change to the product.

Three properties matter.

- **It is declared before the work.** A fence written after the fact describes where you happened to write, which is not a constraint.
- **It is narrow.** The prototype gets its own directory. Where nothing was selected, `experiments/<XPLAN-ID>/` is this package's proposal - say that it is a proposal when you apply it, and prefer the project's own convention.
- **It is not yours to widen.** If answering the question honestly needs a credential, a production dataset, a paid service or a path outside the fence, that is a stop condition to report, not a boundary to move. Report what is blocked, what would unblock it, and who owns that.

`devforge isolate --project <abs-project> --runtime claude -- claude` mounts `/` read-only and rebinds only the project writable. That bounds the project. It does not bound a subpath inside it, so it is not an experiment fence and should not be described as one. No current DevForge command enforces the fence; see [framework context](framework-context.md) for the open integration requirements.

## Measurement before result

The plan's threshold exists so that the result can disagree with someone's hope. Write it before the measurement exists, freeze the plan, and do not touch the threshold afterwards.

Be exact about what that freeze establishes, because it is easy to overstate. A digest you computed yourself records which bytes you had when you computed it. It does not establish to anyone else that those bytes preceded the evidence, because nothing stopped you computing it afterwards - and no current DevForge command binds a plan's bytes outside the evaluated agent's reach, which is the second of the open integration requirements in [framework context](framework-context.md). Where something external does hold the identity - a commit in an authorised experiment worktree, an operator-held receipt - name it, and the ordering becomes checkable. Where nothing does, say that plainly and keep freezing anyway: a self-recorded freeze still fixes the threshold in front of you before the number arrives, which is the discipline the rest of this section depends on. What it does not do is prove that discipline to a reader who has no reason to take your word.

If a threshold turns out to have been wrong - the wrong metric, an impossible target, a condition nobody can observe - that is a real finding and it needs a **new plan revision** stating what changed and why, with the earlier revision preserved. What it is not is permission to edit the number in place. Editing in place destroys the only evidence that the original expectation existed, and the report then shows an experiment that met its target.

Related discipline while observing:

- Record the environment with the number. A latency without a machine, a dataset size and a configuration is not reproducible and supports no comparison.
- If you ran a check repeatedly, say so and say what varied. Reporting the best run as though it were the run is selection nobody can see.
- Distinguish "the prototype did X" from "the production system would do X". A probe with no error handling, no auth, no persistence and one warm cache is not the shipped path, and the gap belongs in the report's limits.
- Research is for factual claims that matter. When you use it, record the URL, the retrieval date, the applicable version and the specific claim it supports, and keep it distinguishable from your own inference. An unverified claim stays a missing input rather than becoming confident prose.

## When a measurement cannot be taken

Record `COULD_NOT_RUN` with the actual cause - the missing binary, the denied permission, the unavailable service, the timeout, the fixture that would not build. Then make no claim from it.

The failure modes here are specific and worth naming:

- **Absence of an error is not a pass.** A check that never executed produced no result at all.
- **A substitute is a new case.** Measuring something adjacent because the planned check would not run is legitimate work and dishonest reporting if it is presented as the planned case. Add it as a new case in a plan revision, or record it as an additional observation with its own limits.
- **An unavailable runtime is not a small result.** When the experiment as a whole cannot execute, the report says that, the disposition is unresolved, and nothing about feasibility, latency or cost has been established.
- **A partial run is partial.** Some cases observed and others blocked is a normal, reportable outcome. Blending them into an overall impression is not.

## Reading the result

The comparison to the threshold is an observation. What should follow is a recommendation. Every sentence in the report should be readable as one or the other, and a reader who cannot tell them apart will treat your recommendation as a finding.

- **Threshold met.** The hypothesis survived this test, under these conditions, with these limits. It did not become a guarantee, and it did not accept anything.
- **Threshold missed.** This is a result, and often the valuable one, because it stopped a commitment that would have been wrong. Preserve it exactly as observed and recommend the revision it implies - a changed requirement, a different approach, a further experiment - routed to the skill that owns the affected document. Preserving a failure means the bytes stay reachable, not just a summary of them.
- **Inconclusive.** Say so. An experiment that did not settle the question has still narrowed it, and naming what would settle it is a useful output.

## Disposition of the prototype code

Every report proposes one, and the user adopts it or does not.

| Disposition | What it means | What it does not authorise |
| --- | --- | --- |
| Discard | The question is answered; the code has served its purpose. Say where it was, so a later reader knows it existed. | - |
| Keep as reference | The code stays reachable as an illustration of what was tried, clearly marked as experiment code. | It is not on the build path, not imported by product code, and not a dependency. |
| Candidate for hardening | The approach is worth taking forward. | It is not production code. Hardening is a separate planned story with its own tests, review and gates, and it is `devforge-develop`'s work under the real gate - not a promotion that happens because the code already exists and appears to work. |

Two things a prototype can never do: silently become production code, and override an accepted architecture decision. A working experiment is evidence for revisiting a decision through the change workflow. It is not the revisit, and it is not the authority to make one.

The `Required production hardening` field is where the distance between the two is written down - error handling, tests, security, persistence, migration, observability, whatever this particular probe skipped. Filling it in honestly is what keeps "it worked in the prototype" from being read as "it is nearly done".

## Concurrency and ownership

Every writing session has an owner and a fence. Concurrent writers use distinct worktrees and branches from recorded commits; a shared worktree is not a concurrency mechanism.

If a record shows another session holds the worktree, branch or destination you were assigned, stop the dependent writes and report the collision - naming the record you saw and where you read it. Do not delete, reset, revert, stash, rebase or force anything, and do not quietly write somewhere else: relocating leaves the path someone is actually watching empty while producing an artifact nobody selected.

Historical authorship is not a current claim. Someone's name on an old commit does not make them the active writer, so compare actual assignment evidence rather than treating an old producer as a collision.

## Stopping

Stop at the resource bound in the plan, or when the work needs authority beyond the declared fence. Preserve the partial observations either way - a bounded experiment that ran out of budget with three of five cases observed is a real, reportable result.

Do not retry indefinitely, and do not keep going past the finish line. If the worktree, the upstream revision or the active run changed underneath you, re-establish the baseline and the evidence identities before resuming, rather than continuing on references that no longer resolve.
