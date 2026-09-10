---
- name: fixture-scope-note
- description: Produce a short scope note from supplied project facts.
---

# Fixture scope note

The frontmatter root is a YAML sequence. It cannot carry mapping keys at all,
so "name and description are populated" is determinably false rather than merely
unreadable.
