---
type: regex
target: {source: file, path: .git/info/exclude}
match: contains
flags: m
---
^/?\.claude/worktrees/?[ \t]*$
