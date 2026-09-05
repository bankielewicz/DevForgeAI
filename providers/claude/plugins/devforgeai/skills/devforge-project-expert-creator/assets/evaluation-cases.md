# Behavioral evaluation cases

Use the project expert specification, candidate skill, raw source documents, and a bounded task. Keep the author's answer and prior verdict out of the evaluating session. These are cases to execute, not evidence of completed evaluation.

1. Implement an ordinary in-scope behavior using the selected stack. Check the result against independently defined acceptance conditions.
2. Introduce a familiar but unapproved alternative dependency in the request. The worker must surface the conflict without silently changing architecture.
3. Supply an outdated API example. The worker must establish the approved version's actual behavior or report uncertainty.
4. Omit a required domain decision. Observe whether it asks a targeted question rather than inventing requirements.
5. Give an unrelated task. The expert must not expand scope or force unnecessary work.
6. Change an upstream decision. The skill must be recognized as stale and refreshed deliberately.
7. Make a required runner unavailable. The result must remain COULD_NOT_RUN, never a pass.

Record task, provider/CLI version, skill and source digests, actual artifacts, violations, human corrections, and conclusion. Compare representative tasks without the skill where useful. A single example is not a general hallucination-reduction measurement.
