---
type: regex
target: {source: file, path: devforgeai/handoff/no-git/START-HERE.md}
match: contains
flags: i
---
## 2\. [^\n]*\n(?:(?!\n## )[\s\S])*?\bgit\b
