# ADR-011: Triple Mirror Consolidation Strategy

**Status:** Accepted
**Date:** 2026-01-27
**Story:** STORY-313
**Epic:** EPIC-050

## Context

DevForgeAI maintains framework files in three locations:

1. **`src/`** - Distribution source for installer deployment
2. **`.claude/`** - Operational directory used by Claude Code Terminal
3. **`devforgeai/`** - Project specifications and context files

This "triple mirror" pattern creates maintenance burden:
- Changes must be made in all three locations
- Risk of drift between mirrors
- 3x effort for any framework modification
- Potential for inconsistency causing bugs

The friction point was identified in EPIC-050 as "FP-4: Triple mirror pattern" with MEDIUM priority.

## Decision

**We will implement a build-time sync approach with `src/` as the single source of truth.**

### Selected Approach: Build-Time Copy Script

A shell script (`scripts/sync-mirrors.sh`) will:
1. Copy files from `src/claude/` to `.claude/`
2. Copy files from `src/devforgeai/` to `devforgeai/`
3. Use `rsync -a` to preserve file permissions and timestamps
4. Report sync status for visibility

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| **Symlinks** | Windows compatibility issues with Git and symlinks. Many Windows Git configurations don't handle symlinks correctly, causing checkout failures. |
| **Git Submodules** | Unnecessary complexity for an internal repository. Submodules add cognitive overhead and complicate the developer workflow. |
| **Single Directory** | Would break Claude Code Terminal's discovery mechanism which expects `.claude/` directory structure. |
| **Manual Sync** | Error-prone and unsustainable. Human error guaranteed. |

### CI Enforcement

A GitHub Actions workflow (`.github/workflows/sync-verification.yml`) will:
1. Run on every PR that touches mirror directories
2. Use `diff -r` to compare source and target directories
3. Fail the PR if mirrors are out of sync
4. Provide clear error messages about drift

## Consequences

### Positive

- **Single source of truth:** All edits happen in `src/`, eliminating confusion
- **Automated enforcement:** CI catches drift before merge
- **Cross-platform:** Bash script works on Windows (Git Bash/WSL), macOS, and Linux
- **Visibility:** Sync status clearly reported
- **Reduced maintenance:** 66% reduction in edit locations

### Negative

- **Script maintenance:** Need to maintain the sync script
- **Build step required:** Developers must run sync after changes
- **Learning curve:** Contributors need to understand the pattern

### Neutral

- **No runtime impact:** Sync happens at build/commit time, not runtime
- **Existing structure preserved:** No changes to how Claude Code Terminal discovers files

## Implementation

1. Create `scripts/sync-mirrors.sh` with rsync-based sync
2. Create `.github/workflows/sync-verification.yml` for CI enforcement
3. Update `CONTRIBUTING.md` to document sync workflow
4. Update `scripts/release.sh` to run sync before release

## References

- STORY-313: Consolidate Triple Mirror Pattern
- EPIC-050: Installation Process Improvements
- source-tree.md: Dual-Location Architecture section
