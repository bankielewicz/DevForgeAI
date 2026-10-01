---
type: regex
target: {source: file, path: docs/specs/context/rdbms/migrations.md}
match: contains
---
^> Part of CTX-015 \(rdbms\.md\), version 1\. A change here raises that document's version\.\n\n# Relational database: migration rules\n\n- \*\*Convention:\*\* one revision per story, named `<story id>_<what>`, for example `story_012_add_break`\.\n- \*\*Convention:\*\* a revision that has reached `main` is never edited; a correction is a new revision\.\n- \*\*Convention:\*\* every revision has a working downgrade, tested by `pytest tests/db -k downgrade`\.\n\nBack to \[rdbms\.md\]\(\.\./rdbms\.md\)\.\n$
