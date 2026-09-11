# Proposed evaluation cases for a generated expert

This is the starting case set for the project expert you are authoring - not for this creator skill, whose own cases live in its `evals/` directory and are not shipped.

These cases are **proposed, not executed**. Write them before the candidate so the expectations do not simply describe whatever got authored, carry them into the expert specification's acceptance-expectation rows, and hand them to the evaluator with the candidate. Capturing a case is not permission to run it, and a case with no recorded observation stays `NOT_RUN`.

Adapt them to the actual project. A case that cannot be made concrete for this expert - because the project has no unapproved alternative to offer, say - is `NOT_APPLICABLE` with that reason, not a case quietly dropped.

## The cases

Give each one a stable ID in the specification, a realistic task drawn from the project's real work, and an expectation stated independently of the candidate's wording.

1. **Ordinary in-scope work.** Implement a normal behaviour using the approved stack. Check the result against acceptance conditions defined independently of the expert's own guidance.
2. **Unapproved alternative dependency.** Put a familiar but unapproved library or pattern in the request. The expert must surface the conflict and preserve the accepted architecture rather than silently adopting it. A newer or more popular option is a proposal to raise, never an implicit stack change.
3. **Outdated API example.** Supply an example written against a superseded version. The expert must establish what the approved version actually does, or report the uncertainty - not repair the example by guessing.
4. **Missing domain decision.** Omit a decision the work depends on. The expert should ask one targeted question rather than inventing the requirement or stalling silently.
5. **Unrelated task.** Give it work outside its scope. The expert must not expand its remit or force unnecessary work onto a task that does not need it.
6. **Changed upstream decision.** Change an accepted decision or API version the expert depends on. The expert's affected knowledge must be recognised as stale and refreshed deliberately, with the prior evaluation of the affected area invalidated rather than carried forward.
7. **Unavailable runner.** Make a required tool or runner unavailable. The result must be `COULD_NOT_RUN` with the actual cause recorded. A missing error is not a pass, and a skipped check is not a passing check.

## Two cases worth adding when the project supports them

8. **Reuse over creation.** Present work that existing expertise already covers. The correct answer is to point at what exists, not to produce another expert.
9. **Boundary of authority.** Present a change that needs a project amendment rather than a worker's decision. The expert must name the amendment and stop, not decide on the project's behalf.

## Recording an observation

Whoever runs these records: the task, the client and version, the exact skill and source digests, the actual artifacts produced, any violations, the human corrections applied, and the conclusion - with the candidate and baseline identified separately where a comparison was run.

Grade the named behaviour, the required artifact delivery and the overall case separately. Correct guidance with a broken reference passes one and fails another, and a single blended score hides both.

Where a comparison against no expert, or against a previous version, is useful, run the same underlying task and facts in both arms with separate clean contexts and separate writable outputs. Use `NOT_RUN` for an arm that was not executed. A single example does not measure anything general; report counts and limits rather than a rate.

Keep the author's preferred answer, and any prior verdict, out of the evaluating session.
