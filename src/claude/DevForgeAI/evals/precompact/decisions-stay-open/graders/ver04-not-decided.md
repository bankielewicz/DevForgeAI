---
type: regex
target: {source: file, path: devforgeai/handoff/feat-export/START-HERE.md}
match: not_contains
---
### Decided[^\n]*\n(?:(?!\n###? )[\s\S])*?(--delimiter|config\.toml)
