# ADR-018: Installer Python Exception to Markdown-Only Constraint

**Date**: 2025-12-05
**Status**: Accepted
**Deciders**: Framework Architect
**Related**: ADR-001 (Markdown-only constraint), STORY-078 (Upgrade mode)

## Context

ADR-001 established that **all framework documentation must be in Markdown** to ensure language-agnosticism and optimal token efficiency for Claude Code Terminal integration.

However, STORY-078 introduces the `installer/` directory - a Python distribution tooling package for:
- Backup and restore operations
- Version management and upgrades
- Migration script execution
- Installation lifecycle management (EPIC-012, EPIC-013, EPIC-014)

The `installer/` package:
- Is **operational infrastructure**, not a framework component
- Requires **Python implementation** (cannot be Markdown-only)
- Operates **outside Claude Code Terminal** (no skill invocation)
- Has its own **test suite** (`installer/tests/`)

**The question**: Should `installer/` be exempt from the Markdown-only constraint in ADR-001?

## Decision

**YES** - `installer/` receives an **explicit exception** to the Markdown-only constraint.

**Reasoning**:

1. **Location & Scope**
   - Framework components: `.claude/`, `.devforgeai/` (MUST be Markdown)
   - Distribution tooling: `installer/` at repo root (CAN be Python)
   - Distinction: `installer/` is **infrastructure**, not **framework**

2. **Separate Concerns**
   - Framework: Provides instructions to Claude Code Terminal (Markdown)
   - Installer: Executes on user machines independently (Python implementation)
   - No conflict: They don't execute in the same context

3. **Technical Necessity**
   - Backup/restore requires file I/O operations
   - Version comparison needs semantic versioning logic
   - Migration execution requires subprocess management
   - These operations cannot be expressed in Markdown documentation

4. **Clear Documentation**
   - Exception is explicit and bounded (only `installer/`)
   - Rationale documented in source-tree.md
   - Anti-pattern scanner can be configured to exclude `installer/`

## Consequences

### Positive
- Installer works as independent Python package
- Can be distributed separately (pip install devforgeai)
- Enables robust backup/restore/upgrade operations
- No impact on framework's Markdown constraint
- Clear separation of concerns

### Negative
- Adds Python dependency to project (currently Markdown-only in framework)
- Installer requires its own testing/maintenance outside framework
- Anti-pattern scanner may flag `installer/` unless explicitly excluded

### Mitigations
1. Document exception clearly in source-tree.md
2. Keep `installer/` code quality high (same standards as framework)
3. Configure anti-pattern scanner to exclude `installer/`
4. Treat `installer/` as separate package (version independently if needed)

## Alternatives Considered

### Alternative 1: No Python - Markdown-only installer scripts

**Rejected because**:
- Shell scripts wouldn't work across platforms (Windows, Mac, Linux)
- Cannot reliably implement backup/restore/upgrade in bash/sh
- Would violate principle of "write once, run anywhere"

### Alternative 2: Keep installer as separate GitHub repository

**Rejected because**:
- Complicates deployment (two repos to manage)
- Makes version management harder (sync challenges)
- Users need installer + framework in single package
- Testing becomes fragmented

### Alternative 3: Use a different language (Go, Rust)

**Rejected because**:
- Adds build complexity (need compile step)
- Harder for community contributions
- Python already used elsewhere in project (scripts/)
- Python has excellent cross-platform support

## Implementation

### Phase 1: Current (STORY-078)
- ✅ `installer/` contains Python implementation
- ✅ Exception documented in source-tree.md via ADR-018
- ✅ Tests in `installer/tests/` for all components

### Phase 2: Future
- Configure anti-pattern scanner to exclude `installer/`
- Document installer API separately in `installer/API.md`
- Maintain consistent code quality standards

## Enforcement

**This exception applies ONLY to**:
```
installer/
├── *.py                # Python implementation (allowed)
├── tests/              # Python tests (allowed)
└── *.md                # Documentation (follows Markdown standard)
```

**NOT allowed elsewhere**:
```
.claude/
└── skills/
    └── devforgeai-**/
        ├── *.py        # ❌ FORBIDDEN (violates ADR-001)
```

## Related Decisions

- **ADR-001**: Markdown for all framework documentation
- **STORY-048**: Dual-location architecture (operational vs distribution)
- **STORY-078**: Upgrade mode with migration scripts
- **EPIC-012/013/014**: Version management & installation lifecycle

## References

- [source-tree.md](../../.devforgeai/context/source-tree.md) - "EXCEPTION - installer/ Distribution Tooling"
- [ADR-001](./ADR-001-markdown-for-documentation.md) - Markdown constraint
- [STORY-078 Implementation Notes](.../../devforgeai/specs/Stories/STORY-078-upgrade-mode-migration-scripts.story.md)

## Revision History

- **2025-12-05**: Initial decision - Python exception for installer/ package
