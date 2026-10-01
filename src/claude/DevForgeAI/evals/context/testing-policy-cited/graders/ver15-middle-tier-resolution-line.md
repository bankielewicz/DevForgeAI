---
type: regex
target: {source: file, path: docs/specs/context/middle-tier.md}
match: contains
---
\n\|[^\n]*\|[ \t]*claude-code \(session [^)\n]*\)[ \t]*\|[^|\n]*Policy resolution: interview\.max_calls=8 \(default\); architecture\.mandated_platforms=none \(default\); quality\.required_categories=floor only \(default\); testing\.method=tdd \(default\); testing\.coverage_metric=line \(default\); testing\.coverage_threshold=90 \(POL-001#SET-01\); testing\.coverage_scope=code roots \(default\); testing\.coverage_exclusions=generated,tests,fixtures roots \(default\); testing\.exception_approvers=story owner \(default\)[ \t]*\|
