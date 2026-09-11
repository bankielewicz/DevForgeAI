---
name: fixture-scope-note
description: Produce a short scope note: Goal, Included work, Excluded work and Open questions, from supplied project facts.
---

# Fixture scope note

The description is an unquoted plain scalar containing a colon followed by a
space. YAML reads that colon as a mapping indicator rather than as text, so the
line is not a scalar the restricted subset can store.

Declining to parse it is a limit of this reader, not a defect established here.
A client loader may accept the same bytes and present the whole description. The
grader's only honest answer is that it did not establish the value, which is why
this fixture expects INDETERMINATE in both directions rather than a defect.
