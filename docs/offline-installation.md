# Offline Installation Guide

Complete guide for installing DevForgeAI in air-gapped networks, secure data centers, and environments with restricted internet access.

## Overview

DevForgeAI supports **full offline installation** after the initial npm package download. This enables deployment in:
- Air-gapped networks (no internet connectivity)
- Secure data centers with network restrictions
- Organizations with strict network policies
- Environments behind restrictive firewalls/proxies

## Prerequisites

**On the machine with internet access:**
- Node.js 18+ and npm 8+
- Internet connectivity (one-time download)

**On the air-gapped machine:**
- Node.js 18+ and npm 8+
- Git (required for framework initialization)
- Python 3.8+ (optional, for CLI validation tools)

## Step-by-Step Installation

### Step 1: Download Package (Online Machine)

```bash
# Create a directory for the package
mkdir devforgeai-offline && cd devforgeai-offline

# Download the package as a tarball
npm pack devforgeai

# This creates: devforgeai-1.0.0.tgz (or current version)
```

### Step 2: Transfer to Air-Gapped Machine

Transfer the `.tgz` file using your approved method:
- USB drive
- Secure file transfer
- Air-gap data diode
- Approved network path

### Step 3: Install Globally (Offline Machine)

```bash
# Navigate to where you transferred the file
cd /path/to/transferred/files

# Install globally from the local tarball
npm install -g devforgeai-1.0.0.tgz

# Verify installation
devforgeai --version
```

### Step 4: Initialize Project (Offline)

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run the installer (no network required)
devforgeai install .

# The installer will display:
# ✓ Network Status: Offline - Air-gapped mode
#   Using bundled files only (no internet connection required)
```

## What Gets Installed

### Framework Files
- `.claude/agents/` - 20+ specialized subagents
- `.claude/commands/` - 11 slash commands
- `.claude/skills/` - 8 DevForgeAI skills
- `.claude/memory/` - Reference documentation
- `.claude/scripts/` - CLI validators

### Template Files
- `devforgeai/context/` - 6 context file templates
- `devforgeai/protocols/` - Workflow protocols
- `devforgeai/specs/` - Specification templates

### Documentation
- `CLAUDE.md` - Framework instructions (merged with existing)
- `README.md` - Project documentation

## Bundle Integrity Verification

All bundled files are verified using SHA256 checksums:

```
✓ Bundle integrity verified: 707 files
  All checksums match
```

### Checksum Failure Handling

If checksums don't match:

```
⚠ Checksum mismatch detected: 2 files
  - bundled/claude/agents/test-automator.md
  - bundled/devforgeai/context/tech-stack.md

✗ Installation halted: 3+ checksum failures detected
  This may indicate file corruption or tampering.

  Resolution:
  1. Re-download the npm package from trusted source
  2. Verify file transfer completed without errors
  3. Check target disk for errors
```

## Optional Dependencies

### Python CLI (Optional)

The Python CLI provides validation commands:
- `devforgeai-validate validate-dod` - DoD validation
- `devforgeai-validate check-git` - Git status
- `devforgeai-validate validate-context` - Context file validation

**If Python is unavailable:**

```
⚠ Python 3.8+ not detected
  Skipping optional CLI installation

  Skipped features:
  - devforgeai-validate CLI commands
  - Pre-commit hook validation

  Impact: Manual validation required (slash commands still work)

  To enable later:
  1. Install Python 3.8+
  2. Run: pip install -e .claude/scripts/
```

A `MISSING_FEATURES.md` file documents skipped features.

## Troubleshooting

### "Network Status: Online" When Expected Offline

The installer checks connectivity by attempting to reach `8.8.8.8:53` (Google DNS).

**If you're behind a proxy that allows DNS:**
- The installer may detect as "Online"
- Installation still works (uses bundled files)
- No external downloads are made regardless

### Checksum Errors

**Cause:** File corruption during transfer

**Resolution:**
1. Verify the source `.tgz` file checksum
2. Re-transfer using a different method
3. Check disk health on target machine

### Permission Denied

**Cause:** Insufficient permissions for global install

**Resolution:**
```bash
# Option 1: Use npm prefix
npm install -g devforgeai-1.0.0.tgz --prefix ~/.local

# Option 2: Use nvm (no sudo required)
nvm use 18
npm install -g devforgeai-1.0.0.tgz
```

### Git Not Available

**Cause:** Git not installed on air-gapped machine

**Resolution:**
1. Git is required for DevForgeAI
2. Install Git from offline media
3. Run installer again

### Python Wheel Installation Fails

**Cause:** Python version mismatch or pip issues

**Resolution:**
```bash
# Manual installation (if needed)
cd /path/to/project/.claude/scripts
pip install -e . --no-index --find-links=../../bundled/python-cli/wheels/
```

## Verification Commands

After installation, verify everything works:

```bash
# Check DevForgeAI version
devforgeai --version

# Check installed files
ls -la .claude/
ls -la devforgeai/

# Verify CLAUDE.md exists
cat CLAUDE.md | head -20

# Test CLI (if Python available)
devforgeai-validate check-git
```

## Network-Dependent Features

These features are disabled in offline mode:

| Feature | Offline Behavior |
|---------|-----------------|
| Version update check | Skipped (uses installed version) |
| Telemetry | Disabled |
| GitHub API | Not available |
| npm registry lookup | Not available |

**To update when online later:**
```bash
# Check for updates
npm outdated -g devforgeai

# Update if available
npm update -g devforgeai
```

## Security Considerations

### Checksum Verification
- All 707+ bundled files have SHA256 checksums
- Checksums stored in `bundled/checksums.json`
- Installation halts on 3+ verification failures

### No External Calls
- Zero HTTP/HTTPS requests during offline installation
- No CDN dependencies
- No GitHub API calls
- No npm registry lookups

### Tamper Detection
- Modified files detected via checksum mismatch
- Clear error messages identify affected files
- Installation blocked until resolved

## Bundle Contents

```
bundled/
├── claude/
│   ├── agents/          # 20+ subagent definitions
│   ├── commands/        # 11 slash commands
│   ├── memory/          # Reference documentation
│   ├── scripts/         # CLI source code
│   └── skills/          # 8 skill definitions
├── devforgeai/
│   ├── context/         # 6 context file templates
│   ├── protocols/       # Workflow protocols
│   └── specs/           # Specification templates
├── python-cli/
│   └── wheels/          # Python wheel files
├── checksums.json       # SHA256 manifest
├── version.json         # Version metadata
├── CLAUDE.md            # Framework instructions
└── README.md            # Documentation
```

## Support

For issues with offline installation:
1. Check this troubleshooting guide
2. Review [installer/TROUBLESHOOTING.md](../installer/TROUBLESHOOTING.md)
3. Submit issue at https://github.com/anthropics/devforgeai/issues

---

**Last Updated:** 2025-11-29
**Applies to:** DevForgeAI v1.0.0+
