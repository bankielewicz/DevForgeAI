---
type: llm
focus:
  source: file
  path: docs/specs/brainstorms/BRN-001-onboarding-drop-off.md
---

The input is the brainstorm document Claude wrote.

PASS if every fenced block whose info string is `yaml items` has exactly one top-level key, which is `problems`, `ideas` or `assumptions`; problem items use only the fields id, status, superseded_by, upstream, statement, who, evidence and severity; idea items use only id, status, superseded_by, upstream, idea, addresses, value, effort, risk, score, disposition and reason; assumption items use only id, status, superseded_by, upstream, statement, validation and state; and the evaluation method section names diverge-converge.
FAIL if any `yaml items` block has another top-level key or more than one, or any item has a field not listed above (for example a framework-specific key such as `phase`, `cluster`, `votes` or `impact`).
