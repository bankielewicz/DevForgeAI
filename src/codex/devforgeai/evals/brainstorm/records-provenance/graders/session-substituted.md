---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
\$\{(?:CLAUDE_SESSION_ID|CODEX_THREAD_ID)\}|\b(?:model|session):[ \t]*"unknown"
