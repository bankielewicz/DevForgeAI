# Held-out expectations

These files record what each authored case expects. They are **not** given to an evaluated
worker, and neither is `../withheld/`. An evaluated worker receives only the raw task request and
the files listed in that case's `files` array in `../evals.json`.

Graders may receive these expectations, together with the task facts, applicable rules and the
actual outputs. They must not receive the candidate author's preferred solution or private
deliberation.

These expectations were authored before any execution, by the same session that authored the
candidate. They therefore support scoped review only. They are not independently held-out
criteria and do not constitute independent acceptance.
