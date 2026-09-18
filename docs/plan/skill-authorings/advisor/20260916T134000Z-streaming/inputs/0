# Selected advisor progress integration

User request: "perhaps, the advisor skill needs a powershell harness such as the one provided by claude as an example. how to we integrate it into the advisor skill?"
User selection after the concrete integration proposal: "proceed".

Approved scope: develop src/agents/skills/advisor with a thin PowerShell 5.1/7 launcher and optional streaming progress in the existing Python runner, then independent skill-validator evaluation. Preserve operational .agents/skills/advisor, advisor-test.ps1, historical evidence and the Rust worker. Do not call Claude for the exhausted historical review. No installation or new paid model call is part of this deterministic implementation/validation.

The selected proposal keeps auth, attempt/budget limits, evidence and response validation in Python; uses stream-json --verbose for optional progress; keeps progress on stderr and final JSON on stdout; retains raw streams plus final result and response; versions new streaming receipts while reading v1; bounds execution through EOF/process exit/cleanup; rejects missing/duplicate/malformed terminal output; records costs even on budget failures without claiming independent billing enforcement. Distinguish process completion, structurally valid advice and reviewer verdict.

History inspected: initial skill-creator build and direct auth fix exist, but no compatible builder baseline or custody history. Contract history_review=no_known_history denotes that precise builder fact, not absence of known origin. Source and installed package matched 16/16 before this task. This is a focused observed edit, not whole-package adoption.

TDD and independent skill evaluation are explicitly selected together. Authoring records remain authoring-only; separate validation evidence binds exact resulting bytes. Python and PowerShell are skill support resources, never protected framework authority.
