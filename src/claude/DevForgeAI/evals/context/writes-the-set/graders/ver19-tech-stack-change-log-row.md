---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
session:[ \t]*["']?([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})["']?[\s\S]*\n\|[^\n]*\|[ \t]*claude-code \(session \1\)[ \t]*\|[^|\n]*Policy resolution: interview\.max_calls=8 \(default\); architecture\.mandated_platforms=none \(default\); quality\.required_categories=floor only \(default\); testing\.method=tdd \(default\); testing\.coverage_metric=line \(default\); testing\.coverage_threshold=none \(default\); testing\.coverage_scope=code roots \(default\); testing\.coverage_exclusions=generated,tests,fixtures roots \(default\); testing\.exception_approvers=story owner \(default\)[ \t]*\|
