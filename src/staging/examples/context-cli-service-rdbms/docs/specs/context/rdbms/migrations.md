> Part of CTX-015 (rdbms.md), version 1. A change here raises that document's version.

# Relational database: migration rules

- **Convention:** one revision per story, named `<story id>_<what>`, for example `story_012_add_break`.
- **Convention:** a revision that has reached `main` is never edited; a correction is a new revision.
- **Convention:** every revision has a working downgrade, tested by `pytest tests/db -k downgrade`.

Back to [rdbms.md](../rdbms.md).
