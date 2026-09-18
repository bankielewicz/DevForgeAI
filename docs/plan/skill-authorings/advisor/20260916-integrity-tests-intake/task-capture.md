# Selected maintenance request
The user requested five validate_prior_attempt rejection-path tests for these listed guards:
receipt versus raw output; launch record versus receipt; final envelope versus raw output;
unexpected extracted response; invalid stream receipt format. Each fixture must first be
accepted as pristine, mutate one semantic field (updating a dependent hash only when necessary
to reach the intended comparison), and assert the specific ValueError. Mutant guard removal
must be detected rather than relying on an unrelated earlier hash error.

Also fix the ResourceWarning from the flood-reader test instead of documenting it, and provide
an entry-point-excluded coverage view. Preserve the existing all-first-party baseline separately
so the requested exclusion does not alter or hide the >=95% aggregate-line requirement.
Reconcile evaluator scope by retaining unit-only coverage before appending the standalone JSONL run.
Do not chase unrelated streaming parser/type/timing coverage gaps. Development-only scope persists.
No live Claude call, operational installation, budget change, or production behavior change is requested.
Tests and retained evidence are explicitly authorized; independent skill validation remains separate.
