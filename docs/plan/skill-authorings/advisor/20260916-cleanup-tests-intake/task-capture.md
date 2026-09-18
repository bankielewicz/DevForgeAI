# User request
Add focused tests for the uncovered cleanup and failure paths, while keeping the current coverage policy unchanged.
- Exercise real failure handling with meaningful assertions.
- Keep production code unchanged unless a test demonstrates a defect.
- Run existing regressions to check compatibility.
- Preserve the current >=95% aggregate line requirement; report branch and per-file gaps transparently.

Scope remains development source only. Operational promotion was performed by the user previously;
it does not authorize this task to edit .agents. This is explicitly authorized test maintenance,
not independent skill validation or a live Claude review. The user's test request takes precedence
over the skill-builder authoring-only test restriction. Existing policy denominator is scripts/ plus
evals/ Python executable lines; report branch coverage separately without adding a branch/per-file gate.
Tests first exercise unchanged production code. If behavior is already correct, preserve it and do
not invent a red phase. Retain any genuine failures and only repair demonstrated defects.
