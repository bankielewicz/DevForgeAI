---
type: regex
target: {source: file, path: devforgeai/handoff/feat-export/START-HERE.md}
match: not_contains
---
### Decided[^\n]*(?:(?!\n###? )[\s\S])*?\n[-*+] [^\n]*(--delimiter|config\.toml)
