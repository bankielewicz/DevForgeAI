---
type: llm
focus:
  source: file
  path: docs/specs/brainstorm/BRN-001.md
---

The input is the complete brainstorm (BRN) document Claude wrote. Check only these two requirements.

R1. Collection-specific fields. Every fenced block whose info string is `yaml items` has exactly one top-level key: `problems`, `ideas` or `assumptions`. Each item uses only the fields allowed for its own collection:
- problems: id, status, superseded_by, upstream, statement, who, evidence, severity
- ideas: id, status, superseded_by, upstream, idea, addresses, value, effort, risk, score, disposition, reason
- assumptions: id, status, superseded_by, upstream, statement, validation, state
A field allowed in one collection is not allowed in another: for example `state` on an idea, or `disposition` on a problem, violates R1. The keys inside an `upstream` link record (id, item, relation, version, hash, note) are not item fields.

R2. Method explanation. Section 5 (Evaluation method) names the diverge-converge framework and explains how the ideas were evaluated: which criteria were rated and how the ratings became the score. A heading, the framework's name alone, or a table of scores without that explanation does not satisfy R2.

Ignore everything else: frontmatter, other sections, writing quality and the merit of the ideas.

PASS if R1 and R2 both hold.
FAIL if either is violated. When you fail it, quote the offending passage or name the offending item and field, and state which requirement (R1 or R2) it violates.
