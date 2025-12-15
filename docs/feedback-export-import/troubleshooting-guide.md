# Troubleshooting Guide

Common issues and solutions for feedback export/import operations.

---

## Export Issues

### Issue: "No sessions match date range"

**Symptoms:**
```
ERROR: No feedback sessions found for date range: last-7-days

Searched: .devforgeai/feedback/sessions/
Found: 0 sessions in range (2025-11-04 to 2025-11-11)
```

**Causes:**
- No feedback created in selected time period
- Feedback directory empty
- Date range too narrow

**Solutions:**
1. **Use broader date range:**
   ```bash
   /export-feedback --date-range last-30-days
   /export-feedback --date-range all
   ```

2. **Check if feedback exists:**
   ```bash
   ls .devforgeai/feedback/sessions/
   ```

3. **Generate feedback first:**
   ```bash
   # Run DevForgeAI commands to create feedback
   /dev STORY-001
   /qa STORY-001
   ```

---

### Issue: "Export size exceeds 100MB limit"

**Symptoms:**
```
ERROR: Export would exceed 100MB limit

Estimated size: 142 MB (uncompressed)
Sessions: 2,847
Date range: all
```

**Causes:**
- Too many sessions selected
- Very long feedback files
- Date range too broad

**Solutions:**
1. **Use narrower date range:**
   ```bash
   /export-feedback --date-range last-30-days  # Instead of "all"
   /export-feedback --date-range last-7-days   # Even narrower
   ```

2. **Calculate size before export:**
   ```bash
   du -sh .devforgeai/feedback/sessions/
   ```

3. **Split into multiple exports:**
   ```bash
   /export-feedback --date-range last-30-days --output ~/exports/recent/
   /export-feedback --date-range last-90-days --output ~/exports/quarter/
   ```

---

### Issue: "Permission denied writing to output directory"

**Symptoms:**
```
ERROR: Cannot write to output directory

Path: /root/exports/
Error: [Errno 13] Permission denied
```

**Causes:**
- Directory doesn't exist
- No write permissions
- Read-only filesystem

**Solutions:**
1. **Use writable directory:**
   ```bash
   /export-feedback --output ~/Documents/
   /export-feedback --output ~/Desktop/
   ```

2. **Create output directory:**
   ```bash
   mkdir -p ~/exports
   chmod 755 ~/exports
   /export-feedback --output ~/exports/
   ```

3. **Check permissions:**
   ```bash
   ls -ld ~/exports
   # Should show: drwxr-xr-x (write permission)
   ```

---

### Issue: "Feedback directory not found"

**Symptoms:**
```
ERROR: Feedback directory does not exist

Expected: .devforgeai/feedback/sessions/
Found: Directory not found
```

**Causes:**
- Fresh project (no feedback collected yet)
- Feedback directory deleted
- Wrong working directory

**Solutions:**
1. **Generate feedback:**
   ```bash
   # Run commands to create feedback
   /dev STORY-001
   /qa STORY-001
   ```

2. **Check working directory:**
   ```bash
   pwd
   # Should be in DevForgeAI project root
   ```

3. **Initialize feedback system:**
   ```bash
   # Feedback created automatically by framework commands
   # No manual initialization needed
   ```

---

## Import Issues

### Issue: "File not found"

**Symptoms:**
```
ERROR: Archive file not found

Path: export.zip
Error: [Errno 2] No such file or directory
```

**Causes:**
- Wrong file path
- Typo in filename
- File in different directory

**Solutions:**
1. **Use absolute path:**
   ```bash
   /import-feedback ~/Downloads/export.zip
   ```

2. **Verify file exists:**
   ```bash
   ls -la export.zip
   find . -name "*export*.zip"
   ```

3. **Use correct relative path:**
   ```bash
   /import-feedback ./exports/export.zip
   ```

---

### Issue: "Not a valid ZIP archive"

**Symptoms:**
```
ERROR: Not a valid ZIP archive

File: export.zip
Error: File is not a zip file
```

**Causes:**
- File corrupted during download
- Incomplete download
- Wrong file type

**Solutions:**
1. **Re-download file:**
   - Download again from source
   - Verify download completed

2. **Verify file type:**
   ```bash
   file export.zip
   # Should show: Zip archive data
   ```

3. **Check file size:**
   ```bash
   ls -lh export.zip
   # Compare with expected size
   ```

4. **Test ZIP manually:**
   ```bash
   unzip -t export.zip
   # Tests archive integrity
   ```

---

### Issue: "Missing required files in archive"

**Symptoms:**
```
ERROR: Archive missing required files

Found in archive:
  - feedback-sessions/ ✅
  - index.json ✅
  - manifest.json ❌ MISSING

Expected: index.json, manifest.json, feedback-sessions/
```

**Causes:**
- Incomplete export
- Manually modified archive
- Corrupted during transfer

**Solutions:**
1. **Request re-export from source:**
   - Ask sender to re-export
   - Verify all files present before sharing

2. **Don't manually modify archives:**
   - Don't unzip, modify, re-zip
   - Use export command to create valid archives

---

### Issue: "Framework version incompatible"

**Symptoms:**
```
WARNING: Framework version mismatch

Exported with: Framework 0.9.0
Current version: Framework 1.0.1
Min required: 1.0.0

Status: Import will proceed but may encounter issues
```

**Causes:**
- Export from older framework version
- Framework upgraded since export

**Solutions:**
1. **Proceed with warning:**
   - Import usually works (backward compatible)
   - Review imported content for issues

2. **Upgrade framework:**
   ```bash
   # Update to newer framework version
   # Re-export with newer version
   ```

3. **Request re-export:**
   - Ask sender to upgrade framework
   - Re-export with compatible version

---

### Issue: "Duplicate IDs - import proceeded with -imported-N suffix"

**Symptoms:**
```
⚠️ Duplicate Session IDs Resolved

3 duplicate IDs detected and auto-resolved:
  - ...440000 → ...440000-imported-1
  - ...550111 → ...550111-imported-1
  - ...660222 → ...660222-imported-1

All conflicts logged: conflict-resolution.log
```

**This is not an error - it's expected behavior!**

**Causes:**
- Importing same package twice
- Importing packages with overlapping sessions
- Re-importing after deletion

**Actions:**
- ✅ Review conflict log if needed
- ✅ Both versions preserved (no data loss)
- ✅ Continue normally

**See:** `conflict-resolution-guide.md` for details

---

### Issue: "Permission denied creating import directory"

**Symptoms:**
```
ERROR: Cannot create import directory

Path: .devforgeai/feedback/imported/2025-11-11T14-30-00/
Error: [Errno 13] Permission denied
```

**Causes:**
- No write permission to .devforgeai/
- Parent directory doesn't exist
- Filesystem read-only

**Solutions:**
1. **Check permissions:**
   ```bash
   ls -ld .devforgeai/feedback/
   chmod 755 .devforgeai/feedback/
   ```

2. **Create parent directory:**
   ```bash
   mkdir -p .devforgeai/feedback/imported
   ```

3. **Check disk space:**
   ```bash
   df -h .
   ```

---

## Performance Issues

### Issue: "Export taking longer than 5 seconds"

**Symptoms:**
```
Export running... (8 seconds elapsed)
Export running... (12 seconds elapsed)
```

**Causes:**
- Large number of sessions (500+)
- Very large session files
- Slow disk I/O

**Solutions:**
1. **Use narrower date range:**
   ```bash
   /export-feedback --date-range last-7-days  # Fewer sessions
   ```

2. **Check disk speed:**
   ```bash
   # May be normal for slow disks
   # SSDs export faster than HDDs
   ```

3. **Wait for completion:**
   - Exports up to 1000 sessions: May take 10-20 seconds
   - Still within acceptable range

---

### Issue: "Import slower than expected"

**Symptoms:**
```
Import running... (5 seconds elapsed)
Import running... (8 seconds elapsed)
```

**Causes:**
- Large archive (50+ MB)
- Many sessions (500+)
- Slow extraction

**Solutions:**
1. **Wait for completion:**
   - Large imports: Up to 10 seconds normal
   - Progress indication not shown for imports < 10s

2. **Check archive size:**
   ```bash
   ls -lh export.zip
   # >20MB may take longer
   ```

---

## Data Integrity Issues

### Issue: "Checksum mismatch warning"

**Symptoms:**
```
⚠️ WARNING: Checksum mismatch detected

File: feedback-sessions/2025-11-07T10-00-00-command-dev-success.md
Expected SHA-256: abc123def456...
Actual SHA-256:   789ghi012jkl...

Import will proceed. Review file for corruption.
```

**Causes:**
- File modified after export
- Corruption during transfer
- Encoding issues

**Solutions:**
1. **Review imported file:**
   ```bash
   cat .devforgeai/feedback/imported/*/feedback-sessions/2025-11-07*.md
   # Check for corruption or unexpected content
   ```

2. **Request re-export:**
   - If multiple files corrupted, ask for fresh export

3. **Continue if minor:**
   - Import proceeds (not blocking)
   - Single file corruption may be acceptable

---

### Issue: "Session count mismatch"

**Symptoms:**
```
ERROR: Session count mismatch

index.json lists: 50 sessions
feedback-sessions/ contains: 48 files

Archive may be incomplete or corrupted.
```

**Causes:**
- Export process interrupted
- Manual modification of archive
- Corruption during transfer

**Solutions:**
1. **Request re-export:**
   - Ask sender to export again
   - Verify count before sharing

2. **Don't use corrupted archive:**
   - Incomplete data may cause issues
   - Wait for valid export

---

## Unicode and Encoding Issues

### Issue: "Invalid characters in filenames"

**Symptoms:**
```
ERROR: Invalid character in filename

File: 2025-11-07T10-00-00-�-command.md
Error: Encoding issue detected
```

**Causes:**
- Non-UTF-8 encoding
- Special characters in original filenames
- Platform encoding differences

**Solutions:**
1. **Re-export with UTF-8:**
   - Framework should handle automatically
   - Report if issue persists

2. **Check locale settings:**
   ```bash
   locale
   # Should show UTF-8 encoding
   ```

---

### Issue: "Emoji or Unicode content corrupted"

**Symptoms:**
- Emoji appear as `?` or boxes
- Chinese/Arabic characters corrupted
- Text encoding issues

**Causes:**
- Wrong character encoding during export/import
- Terminal doesn't support Unicode

**Solutions:**
1. **Use UTF-8 aware terminal:**
   - Modern terminals support Unicode
   - Check terminal encoding settings

2. **Re-export:**
   - Framework uses UTF-8 by default
   - Should not require manual intervention

---

## Common User Errors

### Error: Using Wrong Command

**Wrong:**
```bash
/import-feedback --file export.zip  # Flag syntax ❌
/export-feedback STORY-017          # Wrong parameter ❌
```

**Correct:**
```bash
/import-feedback export.zip         # Direct path ✅
/export-feedback --date-range last-30-days  # Correct flag ✅
```

---

### Error: Expecting Unsanitized Export

**Expectation:** "I'll export and see my real story IDs"

**Reality:** All user exports are sanitized (secure by default)

**Solution:** Original feedback remains in `.devforgeai/feedback/sessions/` for local use

---

### Error: Re-Importing Same Package

**Situation:** User imports same package twice thinking it was different

**Result:** All sessions duplicated with -imported-1 suffix

**Solution:**
1. Check import directory before importing:
   ```bash
   ls .devforgeai/feedback/imported/
   ```

2. Delete duplicate import:
   ```bash
   rm -rf .devforgeai/feedback/imported/2025-11-11T14-30-00/
   /feedback-reindex
   ```

---

## Getting Help

### Self-Diagnosis Steps

1. **Check error message carefully:**
   - Error messages include suggestions
   - Follow remediation guidance

2. **Verify preconditions:**
   - File exists (exports)
   - Archive valid (imports)
   - Permissions correct (both)

3. **Review logs:**
   ```bash
   # Export/import operations are logged
   grep "export\|import" .devforgeai/logs/*.log
   ```

4. **Check framework version:**
   ```bash
   # Ensure framework up to date
   cat devforgeai/context/tech-stack.md | grep version
   ```

### Reporting Bugs

**If issue persists:**

1. **Gather diagnostic info:**
   ```bash
   # Framework version
   # Error message (full text)
   # Steps to reproduce
   # Archive size and session count
   ```

2. **Create minimal reproduction:**
   - Smallest export that reproduces issue
   - Sanitized (safe to share)

3. **Report to maintainers:**
   - GitHub issues
   - Include diagnostic info
   - Attach sanitized export if relevant

---

## Related Documentation

- **Export Guide:** `export-feedback-guide.md`
- **Import Guide:** `import-feedback-guide.md`
- **Archive Format:** `archive-format-spec.md`
- **Conflict Resolution:** `conflict-resolution-guide.md`

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
