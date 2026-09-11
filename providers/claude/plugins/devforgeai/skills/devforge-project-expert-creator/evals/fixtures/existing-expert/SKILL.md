---
name: notes-storage
description: Read and write the notes JSON store for this project. Use when a task loads, saves, migrates or repairs notes records, or asks how records are persisted. Not for CLI output formatting, which belongs to notes-cli-formatting.
---

# Notes storage

Synthetic fixture, revision 1. Illustrative content for an evaluation case.

## Accepted constraints

Python 3.11, standard library only: `json` and `pathlib`. No third-party
dependency, database or network. The public `load` and `save` names are fixed.

## Guidance

The store is a JSON list of `{id, text}` objects at the path the caller supplies.
`id` is a non-empty unique string; a duplicate id is a caller error and is
reported, not silently resolved.

A missing store file and an empty note list are different results. A missing file
means the store has not been created yet; an empty list means it exists and holds
nothing. Do not collapse them into one empty return.

## Known gap

This revision does not state what happens to fields present in a stored record
that this version does not recognise.
