---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\ngenerated_by:[ \t]*\n[ \t]+tool:[ \t]*\"?codex\"?[ \t]*\n[ \t]+model:[ \t]*\"?[A-Za-z0-9][^\"\s]*\"?[ \t]*\n[ \t]+session:[ \t]*\"?[A-Za-z0-9][^\"\s]*\"?
