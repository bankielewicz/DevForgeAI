---
type: regex
target: {source: file, path: README.md}
match: not_contains
---
[Ff]aster|[Qq]uicker|[Ss]peed|[Pp]erformance|[Ee]fficien|\d+ ?%|\b\d+(?:\.\d+)?x\b|\d ?×|times as fast|[Rr]un ?time|[Ww]all[- ]clock|[Tt]ests? pass|[Pp]assing tests
