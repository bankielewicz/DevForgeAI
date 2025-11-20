# Migration Report - STORY-042

**Generated:** Wed Nov 19 09:09:54 EST 2025

## Summary

- **Total Files Processed:** 953
- **Files Copied:** 953
- **Files Skipped:** 0 (already present with matching checksums)
- **Files Excluded:** 237 (backup/artifact patterns)
- **Files Failed:** 0

## Directories Copied

### .claude/ → src/claude/
- Status: Complete
- Files: 765

### .devforgeai/ → src/devforgeai/
- Status: Complete
- Files: 187
- Excluded: qa/reports/, RCA/, adrs/, feedback/imported/, logs/

### CLAUDE.md → src/CLAUDE.md
- Status: Complete
- Size: 40875 bytes
- Template Marker: Added

## Validation Results

### Checksums
- Total: 953
- Format: SHA256 <filepath>
- Verifiable: Yes

### Original Directories
- .claude: 1002 files (unchanged)
- .devforgeai: 1003 files (unchanged)

## Exclusions

Patterns excluded: .coverage, .coverage, 

Total excluded: 237 files

## Errors Encountered

None

## Next Steps

1. Review this report for any errors
2. Run: `git status` to verify file staging
3. Commit with: `git commit -m 'feat(STORY-042): Migrate framework files to src/'`
4. Verify: `/dev --help` and `/qa --help` still work

