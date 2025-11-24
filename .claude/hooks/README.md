# DevForgeAI Pre-Tool-Use Hook

**Purpose:** Auto-approve safe bash commands to reduce user approval friction while blocking dangerous operations.

**Effectiveness:** >95% of commands auto-approved (RCA-015 REC-01 + REC-02)

---

## How It Works

### Approval Flow

```
Bash command requested
    ↓
Hook intercepts (pre-tool-use.sh)
    ↓
Check against 69 SAFE_PATTERNS
    ├─ Match found → AUTO-APPROVE (exit 0)
    ↓
Check against BLOCKED_PATTERNS
    ├─ Match found → BLOCK with error (exit 2)
    ↓
No match → ASK USER for approval (exit 1)
```

### Pattern Matching

**Safe Patterns:** Prefix matching (`"$COMMAND" == "$pattern"*`)
- Command must START with safe pattern
- Example: `git status | grep modified` matches `"git status"`

**Blocked Patterns:** Regex contains (`"$COMMAND" =~ pattern`)
- Pattern can appear ANYWHERE in command
- Example: `cd /tmp && rm -rf test` blocked by `rm -rf` even though starts with `cd`

**Multi-Layer Defense:**
- Safe patterns checked FIRST (auto-approve common safe commands)
- Blocked patterns checked SECOND (catch dangerous operations even if start looks safe)
- Unknown commands ASK USER (safe default)

---

## Safe Patterns (69 Total)

### Original Patterns (54)

**DevForgeAI Workflows:**
- `npm run test`, `npm run build`, `npm run lint`
- `dotnet test`, `dotnet build`
- `python3 -m pytest`, `pytest`
- `bash tests/`, `bash .claude/scripts/`, `bash .devforgeai/`

**Git Operations (Read-Only):**
- `git status`, `git diff`, `git log`
- `git add`, `git commit` (write but safe - framework operations)

**File Operations (Read-Only):**
- `wc -`, `grep -E`, `grep -r`
- `head -`, `tail -`
- `cat tests/`, `cat .devforgeai/`, `cat src/`, `cat installer/`
- `ls -la`, `ls -lh`, `ls -1`
- `find installer`, `find /mnt/c/Projects/DevForgeAI2/{src,tests,installer}`

**Utilities:**
- `echo`, `cat >`, `cat <<`, `cat << 'EOF'`
- `cp`, `mkdir -p`, `chmod +x`, `dos2unix`
- `sed -i`, `python3 -m json.tool`, `python3 <<`, `sort -`

### RCA-015 Additions (15)

**Added:** 2025-11-24
**Rationale:** Empirical analysis of 3,517 unknown command entries showed these patterns used frequently by Claude during DevForgeAI workflows.

**Command Composition:**
- `cd ` - Directory changes (always safe)
- `python3 -c ` - Inline Python scripts (safe, no file modification)
- `python3 << 'EOF'` - Python HERE-documents (safe, read-only analysis)
- `python << 'EOF'` - Python 2 HERE-documents

**DevForgeAI CLI:**
- `devforgeai ` - Framework's own CLI tools (always safe, we control them)

**Git Introspection (Read-Only):**
- `git rev-parse` - Parse git refs (read-only)
- `git branch` - List/show branches (read-only)
- `git --version` - Version check (read-only)
- `git rev-list` - List commits (read-only)

**Shell Utilities (Read-Only):**
- `which ` - Find command location
- `command -v` - Check if command exists
- `type ` - Show command type
- `stat ` - File statistics
- `file ` - File type detection
- `basename ` - Extract filename from path

---

## Blocked Patterns (6 Total)

**Always Blocked (Exit 2):**
- `rm -rf` - Recursive forced deletion (data loss risk)
- `sudo` - Privilege escalation (system modification)
- `git push` - Remote operations (unintended deployment)
- `npm publish` - Package publishing (unintended release)
- `curl` - Network requests (security risk)
- `wget` - Network downloads (security risk)

**Why blocked patterns use regex:**
- Catches dangerous operations anywhere in command
- Example: `cd /tmp && rm -rf test` blocked even though starts with safe `cd`

---

## Pattern Addition Criteria

### Safe Pattern Checklist

Add pattern if command is:
- ✅ **Read-only** - Doesn't modify files (git status, ls, grep, cat)
- ✅ **Framework-internal** - DevForgeAI operations we control (devforgeai CLI, pytest, npm test)
- ✅ **Navigation-only** - Changes context but no side effects (cd, which, type)
- ✅ **Logging/temp** - Writes to logs or temp dirs (echo, mkdir -p .devforgeai/logs)

Do NOT add if command:
- ❌ **Modifies source** - Changes production files
- ❌ **Network access** - External requests
- ❌ **Privilege** - Requires sudo or root
- ❌ **Deletion** - Removes files (except safe temp dirs)

### Before Adding Pattern

**Check:**
1. Is command genuinely safe? (review what it does)
2. Is it used frequently? (check logs or run analysis tool)
3. Could it be misused? (consider edge cases)
4. Does it pass all 4 safety criteria above?

**Test:**
1. Add pattern to array
2. Run `bash -n .claude/hooks/pre-tool-use.sh` (syntax check)
3. Test command auto-approves
4. Test dangerous variant still blocks (e.g., if adding `git`, ensure `git push` still blocked)
5. Monitor logs for 24 hours

---

## Maintenance Process

### Monthly Pattern Review

**Run pattern analysis tool:**
```bash
python3 .devforgeai/scripts/analyze-hook-patterns.py
# Outputs top 20 safe pattern candidates
# Shows frequency and impact percentage
```

**Review suggestions:**
1. Check each pattern against safety criteria
2. Validate pattern is genuinely safe
3. Add to SAFE_PATTERNS if passes criteria
4. Test with sample commands
5. Commit with rationale: `chore(hooks): Add pattern '{pattern}' (used {count}× per analysis)`

### Weekly Unknown Command Review

**Check what's requiring approval:**
```bash
tail -100 .devforgeai/logs/hook-unknown-commands.log | \
  sed 's/.*APPROVAL: //' | \
  sort | uniq -c | sort -rn | head -10
```

**If pattern appears >10 times:**
- High-frequency safe pattern
- Add immediately (don't wait for monthly review)

### Quarterly Effectiveness Audit

**Calculate metrics:**
```bash
# Total invocations
TOTAL=$(wc -l < .devforgeai/logs/pre-tool-use.log)

# Auto-approved
AUTO=$(grep -c "AUTO-APPROVE" .devforgeai/logs/pre-tool-use.log)

# Approval rate
echo "scale=2; $AUTO * 100 / $TOTAL" | bc
# Target: >95%
```

**If approval rate <90%:**
- Run pattern analysis
- Review top unknown commands
- Add high-frequency safe patterns
- Re-audit in 1 week

---

## Troubleshooting

### Issue: Commands Still Requiring Approval

**Symptoms:**
- Frequent user approval prompts
- Same command pattern logged multiple times in hook-unknown-commands.log

**Diagnosis:**
```bash
# Find most frequent unknown commands
tail -500 .devforgeai/logs/hook-unknown-commands.log | \
  sed 's/.*APPROVAL: //' | \
  awk '{print $1" "$2}' | \
  sort | uniq -c | sort -rn | head -10
```

**Resolution:**
- Review top 10 unknown command prefixes
- Validate each is safe
- Add to SAFE_PATTERNS
- Commit and test

### Issue: Unsafe Command Auto-Approved

**Symptoms:**
- File deleted unexpectedly
- System modified without approval
- Command that should have been blocked was auto-approved

**Diagnosis:**
```bash
# Find what pattern matched
tail -50 .devforgeai/logs/pre-tool-use.log | grep -B 5 "AUTO-APPROVE"
# Shows which pattern matched
```

**Resolution:**
1. Identify problematic pattern
2. Make pattern more specific:
   - `"cd "` → `"cd /mnt/c/Projects/DevForgeAI2"` (restrict to project)
   - Or remove pattern if too risky
3. Add command to BLOCKED_PATTERNS if genuinely dangerous
4. Test fix
5. Document in this README why pattern was restricted/removed

### Issue: Hook Not Running

**Symptoms:**
- No entries in pre-tool-use.log
- ALL commands requiring approval (or none)

**Diagnosis:**
```bash
# Check hook is executable
ls -la .claude/hooks/pre-tool-use.sh
# Should show execute permission (x)

# Check bash syntax
bash -n .claude/hooks/pre-tool-use.sh
# Should exit 0
```

**Resolution:**
```bash
# Make executable
chmod +x .claude/hooks/pre-tool-use.sh

# Fix syntax if errors
# Review bash -n output for line numbers
```

### Issue: Hook Performance Slow

**Symptoms:**
- Commands take long to execute
- Noticeable delay before approval prompt

**Diagnosis:**
```bash
# Time hook execution
time bash .claude/hooks/pre-tool-use.sh <<< '{"tool_input":{"command":"git status"}}'
# Target: <100ms
```

**Resolution:**
- If >100ms: Review loop efficiency
- Consider compiling patterns to single regex
- Optimize jq extraction
- Profile with `set -x` to find bottleneck

---

## Related Documentation

**RCA Documents:**
- RCA-015: Pre-Tool-Use Hook Friction analysis

**Framework Protocols:**
- CLAUDE.md: Hook integration overview
- .devforgeai/protocols/: Framework patterns

**Scripts:**
- .devforgeai/scripts/analyze-hook-patterns.py: Pattern analysis tool (when created per REC-4)

---

## Changelog

### 2025-11-24: RCA-015 REC-02 - Pipe/Redirect Support
- **Added:** Quote-aware base command extraction (43-line function)
- **Feature:** Auto-approve safe commands with pipes (`git status | grep`) and redirects (`pytest > file`)
- **Safety:** Two-layer check: blocked patterns in full command + system directory redirect blocks
- **Quote Handling:** Preserves pipes/redirects inside quotes (`python3 -c "print('|')"`)
- **System Protection:** Blocks redirects to /etc, /usr, /sys, /boot, /root
- **Impact:** Additional 5-10% friction reduction (pipes/redirects now auto-approved)
- **Testing:** 23 test scenarios documented in test-rec-02.sh
- **Reference:** RCA-015-pre-tool-use-hook-friction-remains.md REC-02

### 2025-11-24: RCA-015 REC-01 - Pattern Expansion
- Added 15 common command composition patterns
- Patterns: cd, python3 -c, HERE-docs, devforgeai CLI, git introspection, shell utilities
- Impact: 90% reduction in approval friction (3,517 unknown commands → target <350)
- Reference: .devforgeai/RCA/RCA-015-pre-tool-use-hook-friction-remains.md

### Initial: Hook Creation
- 54 safe patterns for DevForgeAI workflows
- 6 blocked patterns for dangerous operations
- Prefix matching for safe, regex for blocked

---

## Quick Reference

**Check logs:**
```bash
# Recent unknown commands
tail -50 .devforgeai/logs/hook-unknown-commands.log

# Hook execution log
tail -100 .devforgeai/logs/pre-tool-use.log

# Pattern match successes
grep "MATCHED safe pattern" .devforgeai/logs/pre-tool-use.log | tail -20
```

**Test hook:**
```bash
# Test safe command
cd /tmp && echo "test"
# Should auto-approve

# Test blocked command
echo "testing" # This line just shows syntax, DON'T RUN: rm -rf /tmp/test
# Should block with error
```

**Metrics:**
```bash
# Approval rate
AUTO=$(grep -c "AUTO-APPROVE" .devforgeai/logs/pre-tool-use.log)
TOTAL=$(wc -l < .devforgeai/logs/pre-tool-use.log)
echo "Approval rate: $(echo "scale=1; $AUTO * 100 / $TOTAL" | bc)%"
# Target: >95%
```

---

**Hook Version:** 2.0 (post-RCA-015)
**Pattern Count:** 69 safe, 6 blocked
**Last Updated:** 2025-11-24
