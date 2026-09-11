# Synthetic project authority

Synthetic fixture. This is the project owner's supplied decision record for an
evaluation case; it is not a claim about any real project.

## Goal and accepted constraints

A local notes tool on Python 3.11. Accepted constraints: the standard-library
`json` module and `pathlib` only. No third-party dependency, no database, no
network. The existing public `load` and `save` names are preserved.

## The story that needs expertise

The current story needs focused persistence expertise that recognises these
constraints and distinguishes a missing input file from an empty note list.

Saved JSON is a list of `{id, text}` objects. `id` is a non-empty unique string.
Unknown fields present in a stored record are preserved across edits. A read
error is surfaced to the caller without overwriting the input file.

## Placement and fence

The expert source is `project/experts/notes-storage`. Its proposed installation
is the consuming project's `.claude/skills/notes-storage`. The user-authorised
write fence is the expert source and the allocated report outbox, and nothing
else. Existing code and public behaviour outside the requested change are
preserved.

Use the local code and documents as evidence. Do not infer a different stack.
