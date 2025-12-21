# CLAUDE.md Conflict Resolution Instructions

This guide explains how to resolve conflicts when merging CLAUDE.md files during DevForgeAI installation.

## What is a Conflict?

A conflict occurs when you've significantly modified a DevForgeAI framework section (>30% changes). The system detects this using a 70% similarity threshold.

**No Conflict:** Your section is ≥70% similar to the framework version
**Conflict:** Your section is <70% similar (you changed >30% of content)

## When Conflicts Are Detected

During auto-merge, if conflicts are found:

1. **Auto-merge halts** - No changes are written
2. **Backup is created** - Your original file is safe
3. **Conflict details shown** - Section name, line numbers, content excerpts
4. **Resolution prompt appears** - You choose how to proceed

## Resolution Options

### Option 1: Keep Your Version

**Choose when:** Your modifications are intentional and important

**What happens:**
- Your modified section is preserved exactly as-is
- Framework section is NOT updated
- Other non-conflicting sections are merged normally

**Example:**
```
Your "Critical Rules" section has custom rules for your project.
Choosing "Keep your version" preserves those custom rules.
```

### Option 2: Use DevForgeAI Version

**Choose when:** You want the latest framework content

**What happens:**
- Your modifications are discarded
- Framework section replaces your version
- Your original is still in backup file

**Example:**
```
DevForgeAI updated "Critical Rules" with new security guidelines.
Choosing "Use DevForgeAI version" gets those updates.
```

### Option 3: Manual Resolution

**Choose when:** You want to manually merge both versions

**What happens:**
- Auto-merge stops completely
- `CLAUDE.mddevforgeai-template` is created
- You manually compare and merge the files

## Manual Resolution Steps

If you choose manual resolution (or have complex conflicts):

### Step 1: Locate Files

After choosing manual resolution, you'll have:
```
CLAUDE.md                        # Your original (unchanged)
CLAUDE.md.backup-YYYYMMDD-HHMMSS # Backup copy
CLAUDE.mddevforgeai-template    # DevForgeAI template
```

### Step 2: Compare Files

Use a diff tool to compare your CLAUDE.md with the template:

```bash
# Using diff
diff CLAUDE.md CLAUDE.mddevforgeai-template

# Using VS Code
code --diff CLAUDE.md CLAUDE.mddevforgeai-template

# Using vim
vimdiff CLAUDE.md CLAUDE.mddevforgeai-template
```

### Step 3: Identify Sections

Framework sections to update (from template):
- `## Repository Overview`
- `## Critical Rules - ALWAYS Follow`
- `## Development Workflow Overview`
- `## Common Commands`
- `## Key File Locations`
- `## What NOT to Do`

User sections to preserve (from your file):
- Any section NOT in the list above
- Custom project-specific instructions
- Your team's guidelines

### Step 4: Merge Content

1. **Copy framework sections** from `devforgeai-template` to your CLAUDE.md
2. **Keep your custom sections** in their original positions
3. **Resolve any overlaps** by deciding which content to keep

### Step 5: Validate

After manual merge, verify:
- [ ] All framework sections are present and updated
- [ ] Your custom sections are preserved
- [ ] No duplicate sections
- [ ] File is valid markdown

### Step 6: Clean Up

Remove temporary files:
```bash
rm CLAUDE.mddevforgeai-template
# Keep backup until you've verified everything works
```

## Conflict Prevention Tips

### 1. Use Custom Section Names

Instead of modifying framework sections, create your own:

**Don't do this:**
```markdown
## Critical Rules - ALWAYS Follow
[Your custom rules mixed with framework rules]
```

**Do this:**
```markdown
## Critical Rules - ALWAYS Follow
[Framework content - don't modify]

## My Project Rules
[Your custom rules here]
```

### 2. Append, Don't Replace

Add your content at the end of sections:

```markdown
## Critical Rules - ALWAYS Follow
[Framework content]

### Project-Specific Rules
[Your additions here]
```

### 3. Use Comments for Context

Mark your additions clearly:

```markdown
<!-- BEGIN PROJECT CUSTOMIZATION -->
Your custom content here
<!-- END PROJECT CUSTOMIZATION -->
```

## Troubleshooting

### "Multiple conflicts detected"

If auto-merge finds many conflicts, consider:
1. Using **Replace** strategy for clean start
2. Using **Manual** strategy for full control
3. Reviewing your CLAUDE.md for unnecessary framework modifications

### "Can't determine section type"

Some sections may be ambiguous. The system uses content similarity to classify them. If misclassified:
1. Choose **Manual** resolution
2. Explicitly organize your content into framework vs custom sections

### "Backup verification failed"

If backup integrity check fails:
1. Check disk space
2. Verify write permissions
3. Try again - transient I/O error

## Recovery

If something goes wrong:

### Restore from Backup
```bash
cp CLAUDE.md.backup-YYYYMMDD-HHMMSS CLAUDE.md
```

### Start Fresh
```bash
# Remove conflicted file
rm CLAUDE.md

# Re-run installer
devforgeai install
```

## See Also

- [Merge Strategy Guide](./claudemd-merge-guide.md)
- [DevForgeAI Installation Guide](../README.md)
