# Independent description-only routing observation

Reviewer: /root/dev_validation/routing_review. No tools or files were permitted. The description and prompts below were the complete task data; expected labels were not supplied. This is description classification, not native implicit discovery. No numerical activation score is inferred after the fact.

Description: Implement, extend, or finish software from explicitly selected specification documents, including dependent multi-document contracts; resume user-selected implementation work or checkpoints through product TDD, integration, and QA. Do not use for specification drafting, architecture research alone, skill authoring/evaluation, installation, deployment, or review-only requests.

| ID | Raw prompt | Actual classification |
| --- | --- | --- |
| P1 | Implement the library described in the selected api.md in this empty project through tests. | applicable |
| P2 | Resume the implementation checkpoint I selected and finish the dependent specs api.md and client.md. | applicable |
| P3 | Write a specification for a payment service. | not_applicable |
| P4 | Compare possible database architectures without code changes. | not_applicable |
| P5 | Author a new Codex development skill from this specification. | not_applicable |
| P6 | Audit this skill package's instructions and run quality trials. | not_applicable |
| P7 | Install the operational skill and enable startup. | not_applicable |
| P8 | Deploy our existing build to production. | not_applicable |
| P9 | Review this commit for bugs without modifying it. | not_applicable |
| P10 | Build the application; I have not selected any specifications yet. | needs_input |
| P11 | Use selected api.md to prepare an implementation plan only; do not code. | not_applicable |
| P12 | Extend the supplied parser specification implementation with its new cases and run QA. | applicable |

Actual reviewer rationale: selected implementation/resume prompts match; specification drafting, architecture-only research, skill authoring/evaluation, installation, deployment and review-only work are excluded; missing explicit specs need input; plan-only expressly prohibits implementation. P11 is a description-routing limit, while explicitly invoked plan-only handling is separately assessed by DV14.
