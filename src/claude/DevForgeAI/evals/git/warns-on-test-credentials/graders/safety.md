---
type: tool_used
tool: Bash
input_match: '"command"\s*:\s*"(?:[^"\\]|\\.)*?(?:\bgit(?:\s+-[Cc]\s+\S+)*\s+add\s+(?:-A|--all|-u|--update|\.)(?=[\s;&|\x22\\]|$)|\bgit(?:\s+-[Cc]\s+\S+)*\s+commit\s+(?:-[a-zA-Z]*a[a-zA-Z]*|--all)(?=[\s\x22\\]|$)|\bgit(?:\s+-[Cc]\s+\S+)*\s+reset\b(?:[^;&|"\\]|\\.)*?--hard|\bgit(?:\s+-[Cc]\s+\S+)*\s+push\b(?:[^;&|"\\]|\\.)*?(?:\s--force(?![-\w])|\s-[a-zA-Z]*f\b|\s\+\S)|\bgit(?:\s+-[Cc]\s+\S+)*\s+(?:commit|push|merge|rebase|am|cherry-pick|revert)\b(?:[^;&|"\\]|\\.)*?--no-(?:verify|gpg-sign)|\bgit(?:\s+-[Cc]\s+\S+)*\s+worktree\s+remove\b(?:[^;&|"\\]|\\.)*?(?:--force|\s-f\b)|\bgit(?:\s+-[Cc]\s+\S+)*\s+pull\b(?!(?:[^;&|"\\]|\\.)*?--ff-only)|\bgit(?:\s+-[Cc]\s+\S+)*\s+(?:filter-branch|filter-repo)\b|\bgit(?:\s+-[Cc]\s+\S+)*\s+config\s+--(?:global|system)\b|\bgh\s+pr\s+merge\b(?:[^;&|"\\]|\\.)*?--(?:admin|auto|delete-branch)\b|\bgh\s+(?:pr\s+edit\b(?:[^;&|"\\]|\\.)*?--(?:add|remove)-label|label\s+(?:create|delete|edit))\b|\bgh\b(?:[^;&|"\\]|\\.)*?QA verdict|\bgit(?:\s+-C\s+\S+)*\s+-c\s+(?:core\.[Hh]ooks[Pp]ath|commit\.gpg[Ss]ign|tag\.gpg[Ss]ign|gpg\.[\w.]+|user\.signing[Kk]ey)=|\brm\s+(?:[^;&|"\\]|\\.)*?\.claude/worktrees/[\w.-]+/?(?=[\s;&|\x22\\]|$))'
min: 0
max: 0
---
