---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document. These are all the facts its author was given. From the user: the tool has 400 open GitHub issues, most never triaged; two people maintain the tool in their spare time. From the project file docs/contributor-survey.md: 12 of 20 contributors said they gave up on an issue because nobody answered; 3 of 20 said the labels helped them find an issue to work on. PASS if no `evidence` value in the problems block states a number or a finding other than these. A value that is only a [NEEDS CLARIFICATION: ...] marker is fine. FAIL if any evidence value states another number, study or finding, and quote it.
