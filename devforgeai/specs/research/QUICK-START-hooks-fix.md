# Claude Code Hooks - Quick Start Fix Guide

## The Problem (In Plain English)

Your hook script is fine and your JSON is valid, but Claude Code has a bug that prevents hooks configured in `settings.json` files from being recognized. The error "Found 0 hook matchers in settings" means the settings file is being read but the hooks section is being skipped.

**Solution:** Use the interactive `/hooks` command instead of editing JSON directly.

---

## 5-Minute Fix

### Step 1: Backup Your Settings (Optional)
```bash
cp .claude/settings.json .claude/settings.json.backup
```

### Step 2: Open Claude Code and Run the Command
```
/hooks
```

### Step 3: Follow the Interactive Menu
- Select "Add new hook"
- Event: "PreToolUse"
- Matcher: "Bash"
- Command: `$CLAUDE_PROJECT_DIR/.claude/hooks/pre-tool-use.sh`
- Storage: "Project settings"
- Press Esc to exit menu

### Step 4: Verify It Worked
```
/hooks
```
You should now see your PreToolUse hook listed.

### Step 5: Test It
```bash
# This should auto-approve (safe command)
git status

# This should be blocked (dangerous command)
rm -rf test/
```

---

## What Just Happened?

When you use `/hooks` command:
1. Claude Code performs proper validation
2. Hook gets registered in the hook system
3. Same settings are saved to `settings.json`
4. **But** the `/hooks` command also triggers initialization that file edits don't

The bug is that direct JSON edits don't trigger hook registration, but the `/hooks` command does. So you're using the same file format, but `/hooks` ensures it's properly activated.

---

## Why Your Current Config Isn't Working

**File:** `.claude/settings.json`
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/mnt/c/Projects/DevForgeAI2/.claude/hooks/pre-tool-use.sh"
          }
        ]
      }
    ]
  }
}
```

**Issues:**
1. ✗ File-based configuration has parsing bug in Claude Code v1.0.51+
2. ✗ Absolute path (`/mnt/c/Projects/...`) breaks if working directory changes
3. ✗ Settings are read but hooks section not registered

**Fixes Applied by `/hooks` Command:**
1. ✓ Forces proper hook registration
2. ✓ Can use environment variables like `$CLAUDE_PROJECT_DIR`
3. ✓ Triggers initialization that file edits skip

---

## Alternative: Manual Fix (If You Prefer)

If you want to keep the file-based approach, update your settings.json:

**Before:**
```json
"command": "/mnt/c/Projects/DevForgeAI2/.claude/hooks/pre-tool-use.sh"
```

**After:**
```json
"command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-tool-use.sh"
```

Then still run `/hooks` command to register it properly.

---

## Testing Your Hook

Once registered via `/hooks`, test each scenario:

### Test 1: Safe Command (Should Auto-Approve)
```bash
git status
# Should execute without asking
# Check: Debug logs show hook exit code 0
```

### Test 2: Blocked Command (Should Block)
```bash
rm -rf test/
# Should fail with error message
# Check: Debug logs show hook exit code 2
```

### Test 3: Unknown Command (Should Ask)
```bash
curl https://example.com
# Should show prompt asking for approval
# Check: Debug logs show hook exit code 1
```

---

## Check if It's Working

Run in Claude Code:
```
/hooks
```

**If Working:**
```
PreToolUse Events
├─ Matcher: Bash
│  Command: $CLAUDE_PROJECT_DIR/.claude/hooks/pre-tool-use.sh
│  ✓ Registered
```

**If Not Working:**
```
No hooks configured yet
```

If you see "No hooks configured yet" after running `/hooks` command, try:
1. Restart Claude Code
2. Try `/hooks` command again
3. See "Troubleshooting" section in research document

---

## Files Involved

- **Hook Script:** `.claude/hooks/pre-tool-use.sh` (no changes needed)
- **Settings:** `.claude/settings.json` (minor path update optional)
- **Registration:** `/hooks` command (what we're using to fix it)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `/hooks` shows "No hooks configured" | Restart Claude Code, try `/hooks` again |
| Hook not executing | Check debug logs with `claude --debug` |
| Script permission denied | Run `chmod +x .claude/hooks/pre-tool-use.sh` |
| Hook blocks all commands | Your regex patterns in script might be too broad |

---

## Success Indicators

✓ You'll know it's working when:
- `/hooks` command shows your PreToolUse hook
- Safe commands (git status, npm test) execute without prompting
- Blocked commands (rm -rf, git push) show error message
- Debug logs show "Found 1 hook matchers in settings"

---

## Next Steps

1. **Run `/hooks` command** (main fix)
2. **Test with safe/blocked/unknown commands**
3. **Check debug logs:** `claude --debug`
4. **If still issues:** See "Troubleshooting" section in RESEARCH-001

---

**Research Report:** RESEARCH-001-claude-code-hooks-configuration.md
**Issue:** GitHub anthropics/claude-code #11544
**Tested Solutions:** 5 working examples from production
