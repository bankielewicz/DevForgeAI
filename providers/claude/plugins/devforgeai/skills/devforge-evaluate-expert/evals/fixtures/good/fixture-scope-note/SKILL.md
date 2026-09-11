---
name: fixture-scope-note
description: Produce a short scope note from supplied project facts when the user asks for a scope summary.
---

# Fixture scope note

Read the supplied facts and the governing specification, then write the requested
scope note with the sections Goal, Included work, Excluded work and Open questions.

Use only the supplied facts. Record a missing consequential fact as an open
question rather than inventing it. Preserve explicitly excluded work.

See [the required format](references/required-format.md) before writing the note.

Save the note at the consuming project's assigned output path. Do not modify
governing inputs, source skills, credentials or global state. This skill does not
validate or adopt its own output.
