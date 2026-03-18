# Treelint AST-Aware Search Integration

**AST-Powered Code Search:** Phases 02-04 invoke Treelint-enabled subagents for semantic code analysis, providing 40-80% token reduction compared to text-based search.

## Phase-to-Subagent Mapping

| Phase | Subagent | Treelint Feature |
|-------|----------|------------------|
| Phase 02 (Red) | test-automator | Pattern discovery for test generation |
| Phase 03 (Green) | backend-architect | Code structure analysis for implementation |
| Phase 04 (Refactor) | refactoring-specialist | Code smell detection and refactoring targets |
| Phase 04 (Refactor) | code-reviewer | Quality pattern validation |

## Automatic Fallback

Each subagent detects Treelint availability and falls back to Grep-based search when unavailable. No workflow changes required.

## Supported Languages

Python, TypeScript, JavaScript, Rust, Markdown

## Reference

See `.claude/agents/references/treelint-search-patterns.md` for AST query patterns and usage examples.
