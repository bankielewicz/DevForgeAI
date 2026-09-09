---
name: notes-sqlite-persistence
description: Implement and test note persistence for notes-sqlite using its approved SQLite architecture; refresh when that architecture or story changes.
---

Read the current project story and architecture before changing src/store.py. Use references/stack.md for the selected API and scope. Work within this project's decisions; expertise from another project does not override them.

For STORY-001, save_and_list takes a string and returns a list containing that string after the SQLite round trip. Preserve apostrophes and Unicode. This experiment uses fresh storage per call and does not establish production durability.

Use sqlite3.connect with an in-memory database, bind user strings through ? parameters, retrieve row values as strings, and explicitly close the connection. Do not substitute an ORM or interpolate SQL values.

Add behavioral tests before production changes and request RED evidence from the external gate. Preserve the evaluated tests during GREEN. Report unavailable runners instead of claiming success.

If the policy, story, architecture, or reference changes, review the resulting stale binding and refresh the affected guidance. A binding marked CURRENT is structural evidence only; behavioral evaluation remains separate.
