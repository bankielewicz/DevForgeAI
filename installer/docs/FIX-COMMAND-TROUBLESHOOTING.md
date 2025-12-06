# DevForgeAI Fix Command Troubleshooting Guide

**Story:** STORY-079 - Fix/Repair Installation Mode
**Version:** 1.0
**Last Updated:** 2025-12-06

---

## Common Issues and Solutions

### Issue 1: Exit Code 1 (Missing Source)

**Symptoms:**
```
Error: Source package not found. Cannot repair.
Exit code: 1
```

**Cause:** Fix command cannot locate source package to restore missing files.

**Solutions:**

**A. Provide source path explicitly:**
```bash
python -m installer fix /path/to/project --source /path/to/devforgeai-source
```

**B. Ensure source in standard location:**
- Check: `/path/to/project/src/` directory exists
- Check: `/path/to/project/bundled/` directory exists
- Source should contain `claude/` and `devforgeai/` subdirectories

**C. Reinstall DevForgeAI:**
```bash
python -m installer install /path/to/project --force
```

---

### Issue 2: Exit Code 2 (Permission Denied)

**Symptoms:**
```
Error: Permission denied writing to .claude/commands/
Exit code: 2
```

**Cause:** Insufficient permissions to write to installation directories.

**Solutions:**

**A. Check file permissions:**
```bash
ls -la /path/to/project/.claude/
ls -la /path/to/project/.devforgeai/
```

**B. Fix permissions:**
```bash
chmod -R u+w /path/to/project/.claude/
chmod -R u+w /path/to/project/.devforgeai/
```

**C. Run as appropriate user:**
- If installed as root: `sudo python -m installer fix /path/to/project`
- If installed as user: Run as that user

---

### Issue 3: Exit Code 3 (Partial Repair)

**Symptoms:**
```
Fixed 5 issues. 2 user-modified files require manual attention.
Exit code: 3
```

**Cause:** Some issues fixed successfully, but some were skipped (user chose "keep my version").

**Solutions:**

**A. Review skipped files:**
```bash
cat .devforgeai/logs/fix-{timestamp}.log
```

**B. Decide on skipped files:**
- Keep user modifications → No action needed
- Want original → Run fix again, choose "restore" for those files

**C. Force repair all files:**
```bash
python -m installer fix /path/to/project --force
```
⚠️ Warning: This overwrites all user modifications

---

### Issue 4: Exit Code 4 (Post-Repair Validation Failed)

**Symptoms:**
```
Post-repair validation found 2 remaining issues
Exit code: 4
```

**Cause:** After repair, validation still detects issues. Possible reasons:
- Source package is corrupted
- File restoration failed
- Disk errors during repair

**Solutions:**

**A. Run fix again:**
```bash
python -m installer fix /path/to/project --verbose
```

**B. Check source package integrity:**
```bash
# Verify source files exist
ls -R /path/to/source/claude/
ls -R /path/to/source/devforgeai/
```

**C. Reinstall from scratch:**
```bash
python -m installer install /path/to/project --force
```

---

### Issue 5: Exit Code 5 (Manual Merge Needed)

**Symptoms:**
```
3 user-modified files require manual attention
Exit code: 5
```

**Cause:** User-modified files detected, but no automatic repair requested.

**Solutions:**

**A. Review user-modified files:**
Run fix in interactive mode and choose action for each file:
```bash
python -m installer fix /path/to/project
```

**B. Show diffs to decide:**
When prompted, choose option 3 (Show diff) to see changes before deciding

**C. Backup and restore:**
When prompted, choose option 4 to preserve your version while restoring original

---

### Issue 6: Manifest Missing

**Symptoms:**
```
Manifest file (.devforgeai/.install-manifest.json) not found.

Options:
  1. Regenerate manifest from current files
  2. Reinstall DevForgeAI
  3. Abort
```

**Cause:** Installation manifest was deleted or never created.

**Solutions:**

**A. Regenerate if files are correct:**
Choose option 1 - Treats current files as source of truth

**B. Reinstall if files are corrupted:**
Choose option 2, then run:
```bash
python -m installer install /path/to/project
```

**C. Manual manifest creation:**
Create `.devforgeai/.install-manifest.json` manually (not recommended)

---

### Issue 7: Validation Takes Too Long (>30 seconds)

**Symptoms:**
Validation process seems stuck or takes excessive time.

**Cause:** Very large installation or slow disk I/O.

**Solutions:**

**A. Check installation size:**
```bash
find .claude/ .devforgeai/ -type f | wc -l
```
Should be ~450 files for standard installation

**B. Check disk performance:**
```bash
time dd if=/dev/zero of=test.tmp bs=1M count=100
rm test.tmp
```

**C. Exclude extra files:**
Remove unnecessary files from `.claude/` and `.devforgeai/` directories

---

### Issue 8: Security Constraint Violated

**Symptoms:**
```
SecurityError: Cannot modify files outside DevForgeAI scope.
Path: user_project/data.csv
```

**Cause:** Manifest contains files outside allowed directories (`.claude/`, `.devforgeai/`, `CLAUDE.md`).

**Solutions:**

**A. Check manifest integrity:**
```bash
cat .devforgeai/.install-manifest.json | grep "user_project"
```

**B. Regenerate manifest:**
```bash
# Remove corrupted manifest
rm .devforgeai/.install-manifest.json

# Run fix to regenerate
python -m installer fix /path/to/project
# Choose option 1 (Regenerate)
```

**C. Reinstall if manifest is compromised:**
```bash
python -m installer install /path/to/project --force
```

---

### Issue 9: All Files Show as Corrupted

**Symptoms:**
Every file in manifest shows checksum mismatch.

**Cause:** Manifest is from different installation or source.

**Solutions:**

**A. Verify installation version:**
```bash
cat .devforgeai/.version.json
```

**B. Use correct source package:**
```bash
# Match source version to installation version
python -m installer fix /path/to/project --source /path/to/source-v1.0.1
```

**C. Regenerate manifest:**
If files are actually correct, regenerate manifest from current state

---

### Issue 10: Disk Space Errors During Repair

**Symptoms:**
```
OSError: [Errno 28] No space left on device
```

**Cause:** Insufficient disk space for repair operations.

**Solutions:**

**A. Check available space:**
```bash
df -h /path/to/project
```

**B. Clean old backups:**
```bash
rm -rf .devforgeai/install-backup-*
```

**C. Free up space:**
- Remove unnecessary files
- Clean package caches
- Expand disk if needed

---

## Debug Mode

**Enable detailed logging:**
```bash
export DEVFORGEAI_DEBUG=1
python -m installer fix /path/to/project --verbose
```

**Check installation logs:**
```bash
tail -f .devforgeai/logs/install.log
```

---

## Common Workflows

### Workflow 1: Recover from Incomplete Upgrade

```bash
# 1. Run fix to detect issues
python -m installer fix /path/to/project

# 2. Review issues
cat .devforgeai/logs/fix-{timestamp}.log

# 3. Repair with appropriate source
python -m installer fix /path/to/project --source /path/to/new-version
```

---

### Workflow 2: Restore Default Configuration

```bash
# 1. Backup current config
cp -r .devforgeai/context/ .devforgeai/context.backup/

# 2. Run fix with force (restores defaults)
python -m installer fix /path/to/project --force

# 3. Merge back customizations if needed
diff -u .devforgeai/context.backup/ .devforgeai/context/
```

---

### Workflow 3: Validate Installation Health

```bash
# Run fix in validation-only mode (no source)
python -m installer fix /path/to/project

# If exit code 0: Installation is healthy
# If exit code 1: Missing files (needs source to repair)
# If exit code 5: User files modified (not an error)
```

---

## FAQ

**Q: Will fix command delete my user files?**
A: No. Fix only modifies files in `.claude/`, `.devforgeai/`, and `CLAUDE.md`. Your project files are safe.

**Q: What happens if I choose "Keep my version"?**
A: The file is skipped. Your modifications are preserved. The issue remains in the report.

**Q: Can I undo a repair?**
A: If you chose "Backup and restore", your version is in `.backups/install-backup-{timestamp}/`. Restore manually if needed.

**Q: How do I know which files are user-modifiable?**
A: Files in `.ai_docs/` and `.devforgeai/context/` are considered user-modifiable. `CLAUDE.md` is also user-modifiable.

**Q: What if source package is corrupted?**
A: Download fresh source from official repository or use a verified backup.

**Q: Can I run fix on a fresh installation?**
A: Yes, but it will report no issues (exit code 0).

---

## Getting Help

**Check logs:**
```bash
cat .devforgeai/logs/fix-{timestamp}.log
cat .devforgeai/logs/install.log
```

**Verify installation:**
```bash
python -m installer validate /path/to/project
```

**Reinstall if all else fails:**
```bash
# Backup user files first
cp -r .ai_docs/ .ai_docs.backup/
cp -r .devforgeai/context/ .devforgeai/context.backup/

# Reinstall
python -m installer install /path/to/project --force

# Restore user files
cp -r .ai_docs.backup/* .ai_docs/
cp -r .devforgeai/context.backup/* .devforgeai/context/
```

---

**For additional support, consult:**
- STORY-079 technical specification
- `installer/docs/API.md`
- `installer/docs/ERROR-HANDLING-API.md`
