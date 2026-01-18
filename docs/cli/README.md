# DevForgeAI CLI Reference

**Version:** Node.js CLI v1.0.0 | Python CLI v0.1.0
**Last Updated:** 2025-01-12

---

## Overview

DevForgeAI provides **two complementary CLI packages**:

| CLI | Purpose | Installation |
|-----|---------|--------------|
| **Node.js CLI** | Framework installation wizard | `npm install -g .` |
| **Python CLI** | Workflow validators & phase tracking | `pip install -e .claude/scripts/` |

Both use the command name `devforgeai`. The Python CLI takes precedence when both are installed.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User's Terminal                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  npm install -g .          pip install -e .claude/scripts/  │
│        ↓                            ↓                       │
│  ┌─────────────────┐      ┌─────────────────────────────┐  │
│  │ Node.js CLI     │      │ Python CLI                  │  │
│  │ (v1.0.0)        │      │ (v0.1.0)                    │  │
│  ├─────────────────┤      ├─────────────────────────────┤  │
│  │ • install       │      │ • validate-dod              │  │
│  │ • --version     │      │ • check-git                 │  │
│  │ • --help        │      │ • validate-context          │  │
│  │                 │      │ • check-hooks               │  │
│  │ Routes to ──────┼──────│ • invoke-hooks              │  │
│  │ Python installer│      │ • phase-* (6 commands)      │  │
│  │                 │      │ • ast-grep (3 subcommands)  │  │
│  └─────────────────┘      └─────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### How the CLIs Interact

The Node.js CLI routes the `install` command to the Python installer:

```
User runs: devforgeai install /path/to/project
         ↓
Node.js CLI (bin/devforgeai.js)
         ↓
Spawns: python -m installer --mode=fresh --target /path/to/project
         ↓
Python installer (installer/install.py)
         ↓
Framework deployed to target project
```

All validation commands (`validate-dod`, `phase-*`, `ast-grep`) are Python-only and run directly without Node.js involvement.

### Building from Source

```bash
# Node.js CLI
npm install                     # Install dependencies
npm install -g .                # Install CLI globally

# Python CLI
pip install -e .claude/scripts/ # Install in editable mode

# Verify both work
devforgeai --version            # Node.js CLI (shows vX.X.X)
devforgeai validate-dod --help  # Python CLI
```

**Source Code Locations:**
| Component | Location |
|-----------|----------|
| Node.js entry point | `bin/devforgeai.js` |
| Node.js CLI logic | `lib/cli.js` |
| Wizard modules | `src/cli/wizard/` |
| Python CLI | `.claude/scripts/devforgeai_cli/` |

See [docs/BUILD.md](../BUILD.md) for comprehensive build documentation.

---

## Quick Start

### Install Both CLIs

```bash
# Navigate to DevForgeAI project root
cd /path/to/DevForgeAI

# 1. Install Node.js CLI (installation wizard)
npm install -g .

# 2. Install Python CLI (workflow validators)
pip install --break-system-packages -e .claude/scripts/

# 3. Verify installation
devforgeai --version
```

### Common Workflows

```bash
# Install framework to a new project
devforgeai install /path/to/project

# Validate story Definition of Done
devforgeai validate-dod devforgeai/specs/Stories/STORY-001.story.md

# Check hook configuration before feedback
devforgeai check-hooks --operation=dev --status=success

# Track TDD phase progress
devforgeai phase-status STORY-001
```

---

## Node.js CLI Reference

**Location:** `bin/devforgeai.js` → `lib/cli.js`
**Installation:** `npm install -g .`

### Commands

#### `devforgeai install <path>`

Install DevForgeAI framework to a target directory.

```bash
devforgeai install .              # Current directory
devforgeai install /path/to/project
devforgeai install . --yes        # Non-interactive (use defaults)
devforgeai install . --quiet      # Suppress non-error output
```

**Options:**
| Flag | Description |
|------|-------------|
| `--yes`, `-y` | Non-interactive mode, accept all defaults |
| `--quiet` | Suppress spinners, progress bars, info messages |

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Installation failed |
| 130 | Cancelled by user (Ctrl+C) |

**Behavior:**
- Routes to Python installer (`python -m installer`)
- Validates Python 3.10+ before proceeding
- Shows interactive wizard prompts (unless `--yes`)

#### `devforgeai --version`

Display CLI version.

```bash
devforgeai --version
devforgeai -v
```

**Output:** `devforgeai v1.0.0`

#### `devforgeai --help`

Display help message with usage examples.

```bash
devforgeai --help
devforgeai -h
```

### Wizard Features

The installation wizard provides:

- **Interactive prompts** (Inquirer.js)
  - Target directory selection
  - Installation mode (minimal/standard/full)
  - CLAUDE.md merge strategy
- **Progress feedback** (Ora spinners, CLI-Progress bars)
- **Colored output** (Chalk - respects `NO_COLOR` env var)
- **Graceful shutdown** (Ctrl+C cleanup)
- **CI Detection** (`CI=true` auto-enables `--yes --quiet`)

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| chalk | 4.1.2 | Terminal colors |
| cli-progress | ^3.12.0 | Progress bars |
| commander | ^11.0.0 | CLI argument parsing |
| inquirer | ^8.2.6 | Interactive prompts |
| ora | 5.4.1 | Spinners |

---

## Python CLI Reference

**Location:** `src/claude/scripts/devforgeai_cli/cli.py`
**Installation:** `pip install --break-system-packages -e .claude/scripts/`

### Validation Commands

#### `devforgeai validate-dod <story-file>`

Validate Definition of Done completion in a story file.

```bash
devforgeai validate-dod devforgeai/specs/Stories/STORY-001.story.md
devforgeai validate-dod STORY-001.story.md --format=json
devforgeai validate-dod STORY-001.story.md --project-root=/path/to/project
```

**Options:**
| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--format` | text, json | text | Output format |
| `--project-root` | path | . | Project root directory |

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Valid (all DoD items complete or properly justified) |
| 1 | Violations found |
| 2 | Error (file not found, invalid format) |

**What it validates:**
- All DoD `[x]` items have Implementation Notes entry
- Deferred items have user approval markers
- Referenced stories/ADRs exist
- **Blocks:** Autonomous deferrals (DoD `[x]` + Impl `[ ]` without approval)

#### `devforgeai check-git`

Check if directory is a Git repository.

```bash
devforgeai check-git
devforgeai check-git --directory=/path/to/project
devforgeai check-git --format=json
```

**Options:**
| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--directory` | path | . | Directory to check |
| `--format` | text, json | text | Output format |

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Git available |
| 1 | Git not available |
| 2 | Error (Git not installed) |

#### `devforgeai validate-context`

Validate all 6 DevForgeAI context files exist.

```bash
devforgeai validate-context
devforgeai validate-context --directory=/path/to/project
devforgeai validate-context --format=json
```

**Context files checked:**
- `tech-stack.md`
- `source-tree.md`
- `dependencies.md`
- `coding-standards.md`
- `architecture-constraints.md`
- `anti-patterns.md`

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | All files valid |
| 1 | Missing or empty files |
| 2 | Error |

### Hook Commands

#### `devforgeai check-hooks`

Check if feedback hooks should trigger for an operation.

```bash
devforgeai check-hooks --operation=dev --status=success
devforgeai check-hooks --operation=qa --status=failure
devforgeai check-hooks --operation=release --status=partial --config=custom-hooks.yaml
```

**Required Options:**
| Flag | Values | Description |
|------|--------|-------------|
| `--operation` | dev, qa, release, etc. | Operation name |
| `--status` | success, failure, partial | Operation result |

**Optional:**
| Flag | Default | Description |
|------|---------|-------------|
| `--config` | devforgeai/config/hooks.yaml | Custom config path |

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Trigger feedback hook |
| 1 | Don't trigger (safe default) |
| 2 | Error (invalid arguments) |

**Configuration:** `devforgeai/config/hooks.yaml`
```yaml
enabled: true
trigger_on: all  # all, failures-only, none
operations:
  dev:
    trigger_on: all
  qa:
    trigger_on: failures-only
```

#### `devforgeai invoke-hooks`

Invoke devforgeai-feedback skill for retrospective feedback.

```bash
devforgeai invoke-hooks --operation=dev
devforgeai invoke-hooks --operation=qa --story=STORY-001
devforgeai invoke-hooks --operation=release --verbose
```

**Options:**
| Flag | Values | Description |
|------|--------|-------------|
| `--operation` | dev, qa, release, etc. | Operation name (required) |
| `--story` | STORY-NNN | Story ID (optional) |
| `--verbose` | flag | Enable verbose logging |

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Success (feedback captured) |
| 1 | Failure (logged, gracefully handled) |

**Features:**
- Extracts context (todos, errors, timing)
- Sanitizes secrets (54 patterns)
- 30-second timeout protection
- Circular invocation detection

### Phase State Commands

#### `devforgeai phase-init <story-id>`

Initialize phase state file for TDD workflow tracking.

```bash
devforgeai phase-init STORY-001
devforgeai phase-init STORY-001 --project-root=/path/to/project
devforgeai phase-init STORY-001 --format=json
```

**Output:** Creates `devforgeai/workflows/STORY-001-phase-state.json`

#### `devforgeai phase-check`

Check if phase transition is allowed.

```bash
devforgeai phase-check STORY-001 --from=01 --to=02
devforgeai phase-check STORY-001 --from=02 --to=03 --format=json
```

**Required Options:**
| Flag | Description |
|------|-------------|
| `--from` | Source phase (01-10) |
| `--to` | Target phase (01-10) |

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Transition allowed |
| 1 | Transition blocked (sequential order violation) |
| 2 | Error |

#### `devforgeai phase-complete`

Mark a phase as complete.

```bash
devforgeai phase-complete STORY-001 --phase=02
devforgeai phase-complete STORY-001 --phase=03 --checkpoint-passed
devforgeai phase-complete STORY-001 --phase=04 --checkpoint-failed
```

**Options:**
| Flag | Description |
|------|-------------|
| `--phase` | Phase ID to complete (01-10) |
| `--checkpoint-passed` | Mark checkpoint as passed (default) |
| `--checkpoint-failed` | Mark checkpoint as failed |

#### `devforgeai phase-status <story-id>`

Display current phase status and workflow progress.

```bash
devforgeai phase-status STORY-001
devforgeai phase-status STORY-001 --format=json
```

**Output Example:**
```
STORY-001 Phase Status
======================
Current Phase: 03 (Implementation)
Completed: 01, 02
Progress: 20%

Phase Details:
  01 Preflight     [✓] Complete
  02 Test-First    [✓] Complete
  03 Implementation [→] In Progress
  04 Refactoring   [ ] Pending
  ...
```

#### `devforgeai phase-record`

Record subagent invocation for a phase.

```bash
devforgeai phase-record STORY-001 --phase=02 --subagent=test-automator
devforgeai phase-record STORY-001 --phase=03 --subagent=backend-architect
```

**Options:**
| Flag | Description |
|------|-------------|
| `--phase` | Phase ID (01-10) |
| `--subagent` | Subagent name that was invoked |

**Behavior:** Appends to `subagents_invoked` list (idempotent - won't duplicate).

#### `devforgeai phase-observe`

Record workflow observation during TDD execution.

```bash
devforgeai phase-observe STORY-001 --phase=02 --category=friction --note="Test setup slow"
devforgeai phase-observe STORY-001 --phase=03 --category=success --note="Clean implementation"
devforgeai phase-observe STORY-001 --phase=04 --category=gap --note="Missing refactoring tool" --severity=high
```

**Options:**
| Flag | Values | Description |
|------|--------|-------------|
| `--phase` | 01-10 | Phase ID |
| `--category` | friction, gap, success, pattern | Observation type |
| `--note` | text | Observation description |
| `--severity` | low, medium, high | Severity level (default: medium) |

### AST-Grep Commands

#### `devforgeai ast-grep scan <path>`

Scan directory for code violations using semantic analysis.

```bash
devforgeai ast-grep scan ./src
devforgeai ast-grep scan ./src --category=security
devforgeai ast-grep scan ./tests --language=python --format=json
devforgeai ast-grep scan ./src --fallback  # Force grep mode
```

**Options:**
| Flag | Values | Description |
|------|--------|-------------|
| `--category` | security, anti-patterns, complexity, architecture | Filter by category |
| `--language` | python, csharp, typescript, javascript | Filter by language |
| `--format` | text, json, markdown | Output format |
| `--fallback` | flag | Force grep-based analysis |

**Detection:**
- SQL injection (string concatenation)
- Hardcoded secrets (API keys, passwords, tokens)
- AWS credentials
- Anti-patterns per `anti-patterns.md`

**Accuracy:**
- With ast-grep: 90-95%
- With grep fallback: 60-75%

#### `devforgeai ast-grep init`

Initialize ast-grep configuration directory.

```bash
devforgeai ast-grep init
devforgeai ast-grep init --force
devforgeai ast-grep init --project-root=/path/to/project
```

**Options:**
| Flag | Description |
|------|-------------|
| `--force` | Overwrite existing configuration |
| `--project-root` | Target project directory |

**Creates:** `devforgeai/ast-grep/sgconfig.yml` and rule directories.

#### `devforgeai ast-grep validate-config`

Validate ast-grep configuration file.

```bash
devforgeai ast-grep validate-config
devforgeai ast-grep validate-config --config=custom-sgconfig.yml
devforgeai ast-grep validate-config --format=json
```

**Exit Codes:**
| Code | Meaning |
|------|---------|
| 0 | Configuration valid |
| 1 | Configuration invalid |

---

## Pre-Commit Integration

The Python CLI integrates with Git pre-commit hooks.

### Installation

```bash
bash .claude/scripts/install_hooks.sh
```

### Workflow

```bash
# Developer stages story file
git add devforgeai/specs/Stories/STORY-042.story.md

# Commit triggers validation
git commit -m "feat: Implement feature"

# Output:
# DevForgeAI Validators Running...
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   Validating: STORY-042.story.md
#      ✅ Passed
# ✅ All validators passed - commit allowed
```

### Bypass (Not Recommended)

```bash
git commit --no-verify
```

---

## Environment Variables

| Variable | Effect |
|----------|--------|
| `CI=true` | Auto-enables `--yes --quiet` for Node.js CLI |
| `NO_COLOR` | Disables colored output |
| `TERM=dumb` | Uses ASCII symbols instead of Unicode |
| `DEBUG_CLI` | Enables debug logging for Python detection |
| `DEVFORGEAI_HOOK_ACTIVE` | Prevents circular hook invocation |

---

## Troubleshooting

### "command not found: devforgeai"

**Cause:** CLI not in PATH

**Fix (Node.js):**
```bash
export PATH="$PATH:$(npm config get prefix)/bin"
```

**Fix (Python):**
```bash
export PATH="$PATH:$(python3 -m site --user-base)/bin"
```

### "Python 3.10+ required"

**Cause:** Python version too old

**Fix:**
```bash
# Check version
python3 --version

# Install Python 3.10+ (Ubuntu/Debian)
sudo apt install python3.10
```

### Permission denied during npm install

**Fix:**
```bash
sudo npm install -g .
# Or fix npm permissions: https://docs.npmjs.com/resolving-eacces-permissions-errors
```

### "AUTONOMOUS DEFERRAL DETECTED"

**Cause:** DoD marked `[x]` but Implementation Notes shows `[ ]` without user approval

**Fix Option 1 - Add approval marker:**
```markdown
- [ ] Item - Deferred to STORY-XXX
  **User approved:** YES (via AskUserQuestion 2025-01-12)
  **Rationale:** [user-provided reason]
```

**Fix Option 2 - Complete the work:**
```markdown
- [x] Item - Completed: [description]
```

---

## Story Traceability

| Story | CLI | Feature |
|-------|-----|---------|
| STORY-020 | Slash commands | `/feedback`, `/feedback-config`, `/feedback-search`, `/export-feedback` |
| STORY-021 | Python | `check-hooks` command |
| STORY-022 | Python | `invoke-hooks` command |
| STORY-068 | Node.js | Global CLI entry point |
| STORY-071 | Node.js | Wizard interactive UI |
| STORY-115 | Python | `ast-grep scan` command |
| STORY-116 | Python | `ast-grep init`, `ast-grep validate-config` |
| STORY-129 | Both | CLI availability check (preflight) |
| STORY-148 | Python | Phase state commands (init, check, complete, status) |
| STORY-149 | Python | `phase-record` command |
| STORY-188 | Python | `phase-observe` command |
| STORY-247 | Node.js | CLI wizard installer |

---

## File Locations

| Component | Path |
|-----------|------|
| Node.js entry point | `bin/devforgeai.js` |
| Node.js CLI logic | `lib/cli.js` |
| Wizard modules | `src/cli/wizard/` |
| Python CLI | `src/claude/scripts/devforgeai_cli/cli.py` |
| Python validators | `src/claude/scripts/devforgeai_cli/validators/` |
| Python commands | `src/claude/scripts/devforgeai_cli/commands/` |
| Hooks configuration | `devforgeai/config/hooks.yaml` |
| Phase state files | `devforgeai/workflows/STORY-*-phase-state.json` |
| AST-grep config | `devforgeai/ast-grep/sgconfig.yml` |

---

## See Also

- [Existing Python CLI README](../../src/claude/scripts/devforgeai_cli/README.md)
- [Hook Integration Pattern](../../devforgeai/protocols/hook-integration-pattern.md)
- [AST-grep Rule Authoring](../ast-grep/rule-authoring-guide.md)
- [Feedback System Guide](../guides/feedback-overview.md)
