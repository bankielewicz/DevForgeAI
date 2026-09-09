# Synthetic project authority

Goal: a Python 3.11 local notes tool. Accepted constraints: use the standard-library json module and pathlib; no third-party dependency, database or network. Preserve existing public load/save names. This fixture is the project owner's supplied decision record, not a real project claim.

The current story needs a focused persistence expert that recognizes these constraints and distinguishes missing input from an empty note list. Saved JSON is a list of {id, text} objects; id is a nonempty unique string. Unknown fields are preserved by edits. A read error must be surfaced without overwriting the input.

The expert source is project/experts/notes-storage. Its proposed installation is .agents/skills/notes-storage. User-authorized write fence is only the expert source and the allocated report outbox. Existing skill code/public behavior outside the requested change is preserved. Use local code/docs as evidence; do not infer a new stack.
