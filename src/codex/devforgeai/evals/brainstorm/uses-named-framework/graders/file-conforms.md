---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm (BRN) document. Its item blocks are the fenced blocks whose
info string is "yaml items". The allowed fields per collection are:
- problems: id, status, superseded_by, upstream, statement, who, evidence, severity
- ideas: id, status, superseded_by, upstream, idea, addresses, value, effort, risk,
  score, disposition, reason
- assumptions: id, status, superseded_by, upstream, statement, validation, state
No other collections are allowed.
PASS if every item block uses only its own collection's fields, and section 5
(Evaluation method) names diverge-converge and explains how value, effort, risk and
score were assigned.
FAIL otherwise. When failing, quote the offending passage or field and name the
requirement it violates.
