# DevForgeAI Integration Guide

How `spec-driven-mcp-converter` skill integrates into the DevForgeAI framework ecosystem.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DevForgeAI Framework                     │
│                                                             │
│  /brainstorm → /ideate → /create-context → /dev → /qa     │
│                                                             │
│  Skills: spec-driven-dev, spec-driven-qa, etc.             │
│                                                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├─→ /convert-mcp [MCP]
                  │   │
                  │   └─→ Runs spec-driven-mcp-converter skill
                  │       ├─ Phase 01: Discovers MCP source
                  │       ├─ Phase 02: Detects pattern + confidence
                  │       ├─ Phase 03: Generates CLI wrapper
                  │       ├─ Phase 04: Generates skill docs
                  │       ├─ Phase 05: Validates + tests
                  │       ├─ Phase 06: Registers with framework
                  │       └─ Phase 07: Reports results
                  │
                  ├─→ Dev persona gets:
                  │   ├─ CLI tool ready to use
                  │   ├─ Skill documentation
                  │   └─ Tests/examples
                  │
                  └─→ QA persona validates:
                      ├─ CLI executes correctly
                      ├─ Skill matches CLI interface
                      └─ Tests pass
```

## Typical Workflow

### 1. Developer Discovers MCP

```
Dev: "I want to use the puppeteer-mcp for browser automation"
```

### 2. Trigger Conversion

```
/convert-mcp puppeteer-mcp --source npm:mcp-puppeteer@latest
```

### 3. 8-Phase Workflow Executes

The spec-driven-mcp-converter runs all 8 phases with anti-skip enforcement:
- Phase 00: Initialization (parameter extraction, checkpoint creation)
- Phase 01: Source Discovery (code-analyzer extracts tools)
- Phase 02: Pattern Detection (heuristic analysis, confidence scoring)
- Phase 03: CLI Generation (adapter, utilities, tests)
- Phase 04: Skill Generation (SKILL.md, references, assets)
- Phase 05: Validation (smoke tests, interface alignment)
- Phase 06: Registration (user approval, framework integration)
- Phase 07: Results (report, display, cleanup)

### 4. Dev Uses Generated CLI

```bash
SESSION=$(python puppeteer-cli/cli.py session create --name "test")
python puppeteer-cli/cli.py navigate --session $SESSION --url "https://example.com"
python puppeteer-cli/cli.py screenshot --session $SESSION --output /tmp/page.png
python puppeteer-cli/cli.py session destroy --session $SESSION
```

### 5. QA Validates

QA persona has skill documentation and validates:
- CLI commands match skill interface
- Error codes are correct
- Session management works
- Examples run successfully

---

## Slash Command Integration

### `/convert-mcp`

**Purpose**: Convert an MCP to CLI + skill

**Usage**:
```
/convert-mcp <mcp-name-or-package>
  [--source npm:package | --source ./local/path | --source ./schema.json]
  [--pattern api-wrapper|state-based|custom]
  [--adapter-script ./custom.py]
  [--output-dir ./output-path]
```

**Parameters**:

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| mcp-name | string | required | Name or npm package spec |
| --source | string | inferred | Where to find the MCP |
| --pattern | enum | auto | Force pattern (skips detection) |
| --adapter-script | path | - | Custom adapter for 'custom' pattern |
| --output-dir | path | ./<name>-cli | Output directory |

---

## CLI Output Formats

Generated CLIs normalize to standard formats for Claude consumption.

### JSON (Default)
```json
{"status": "success", "command": "navigate", "session": "abc123", "data": {"url": "...", "loaded": true}}
```

### Text (Human-readable)
```
/tmp/screenshot-abc123.png
```

### Base64 (Binary data)
```
iVBORw0KGgoAAAANSUhEUgAAAAEAAAA...
```

---

## Skill Registration

After conversion, if user approves registration:

1. Skill files copied to `.claude/skills/<cli-name>/`
2. SKILL.md, references, scripts, assets all copied
3. Skill available in future Claude Code conversations
4. Dev persona can use CLI commands immediately

---

## Error Handling & Recovery

Generated CLIs use standard Unix exit codes:

```
Exit 0   → Success, parse response
Exit 1   → General error, check stderr
Exit 2   → Bad arguments, review command syntax
Exit 3   → Timeout, retry or increase timeout
Exit 4   → Resource unavailable, check connectivity
Exit 5   → Auth failed, check credentials
Exit 6   → Rate limited, wait and retry
```

Skill documents these and provides recovery steps.

---

## Pattern-Specific Workflows

### API Wrapper Pattern
Stateless, direct 1:1 command mapping. No session management needed.

### State-Based Pattern
Session lifecycle: create → use → destroy. State persists between commands.

### Custom Pattern
User provides adapter code. Framework wraps it into CLI + skill.

---

## Troubleshooting Integration

### "Skill generated but Dev can't find it"
1. Check if user approved registration in Phase 06
2. Verify `.claude/skills/<cli-name>/SKILL.md` exists
3. Check YAML frontmatter is valid

### "CLI works but Skill docs are wrong"
Re-run Phase 04 (Skill Generation) or manually edit the generated SKILL.md.

### "Pattern detected wrong"
Use `--pattern` flag to override: `/convert-mcp my-mcp --pattern custom`
