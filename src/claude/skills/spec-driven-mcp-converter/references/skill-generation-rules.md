# Skill Generation Rules for MCP-CLI Converter

**Purpose:** Rules and patterns for auto-generating Claude Code skills from MCP server analysis.

**Context:** When the MCP-CLI converter generates a CLI wrapper from an MCP server, it also generates a complementary skill (SKILL.md) so Claude Code understands how to use the CLI effectively. This document defines the rules for skill generation.

---

## Overview

The converter automatically generates skills following Anthropic's official skill specification and DevForgeAI best practices. The generated skill serves as an "onboarding guide" that transforms Claude from a general-purpose agent into a specialist equipped with knowledge of the specific CLI tool.

---

## Skill Anatomy for Generated CLIs

Every generated skill consists of:

```
<cli-name>-cli/
├── skill/
│   ├── SKILL.md (required) - Entry point with YAML frontmatter + markdown
│   ├── references/ (optional)
│   │   ├── cli_reference.md - Complete command reference
│   │   └── usage_examples.md - Pattern-specific examples
│   ├── scripts/ (optional)
│   │   └── setup.sh - Installation script
│   └── assets/ (optional)
│       └── error_codes.md - Error code reference
```

---

## SKILL.md Structure

### Required YAML Frontmatter

```yaml
---
name: <cli-name>-cli
description: <One-sentence description>. Use for: (1) <Primary>, (2) <Secondary>, (3) <Tertiary>. <Pattern guidance>.
---
```

**Frontmatter Rules:**
1. **name**: Must match CLI directory name, use kebab-case, end with `-cli`
2. **description**: Max 1024 characters, third-person voice, enumerate 3-5 use cases, include pattern-specific guidance

---

## Pattern-Specific Generation Rules

### Pattern 1: API Wrapper (Stateless)

**Template sections:** Direct Usage, Available Commands, Output Format, Examples, Error Handling

**Description pattern:**
```
<Service/API name> CLI for <domain>. Use for: (1) ..., (2) ..., (3) .... Each command is independent - no session needed.
```

### Pattern 2: State-Based (Stateful)

**Template sections:** Session Management, Session Commands, Available Commands, Session Lifecycle, Output Formats, Troubleshooting

**Description pattern:**
```
<Service name> CLI for <domain>. Use for: (1) ..., (2) ..., (3) .... Requires session management - create session before running commands.
```

### Pattern 3: Custom (Complex)

**Template sections:** Usage Overview, Commands, Special Features, Examples, Notes

**Description pattern:**
```
<Service name> CLI with <custom features>. Use for: (1) ..., (2) ..., (3) .... <Pattern-specific guidance>.
```

---

## Writing Style Rules

### Imperative/Infinitive Form (Required)

✅ **Correct:** "Create a session before running commands"
❌ **Incorrect:** "You should create a session"

### Progressive Disclosure

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<300 words recommended)
3. **Reference files** - As needed by Claude (unlimited)

### No Duplication

Information lives in ONE place:
- Quick reference in SKILL.md
- Detailed reference in `references/cli_reference.md`

---

## Quality Checklist for Generated Skills

- [ ] **Frontmatter complete**: name, description (< 1024 chars)
- [ ] **Description follows pattern**: "(1) ..., (2) ..., (3) ..."
- [ ] **Imperative language**: No "you should", "you can"
- [ ] **Pattern documented**: API-WRAPPER, STATE-BASED, or CUSTOM
- [ ] **Commands listed**: All MCP tools mapped to CLI commands
- [ ] **Session management**: Documented if state-based
- [ ] **Output formats**: JSON, text, base64 documented
- [ ] **Error handling**: Exit codes documented
- [ ] **Examples provided**: Real-world usage scenarios
- [ ] **Progressive disclosure**: Detailed content in references/
- [ ] **No duplication**: Content lives in one place
- [ ] **File structure**: SKILL.md, references/, scripts/, assets/

---

## Auto-Generation Logic

### Step 1: Analyze MCP Server

Extract from `mcp_analysis.json`:
- Detected pattern (api-wrapper, state-based, custom)
- Tool list with inputs/outputs
- State management requirements
- Async/sync characteristics

### Step 2: Generate Frontmatter

Build name from MCP type + "-cli" suffix.
Build description from top 3 tools + pattern guidance.

### Step 3: Generate Body Sections

Use pattern-specific template (api-wrapper, state-based, or custom).

### Step 4: Generate Reference Files

- `references/cli_reference.md` — Complete command reference
- `references/usage_examples.md` — Pattern-specific workflows
- `assets/error_codes.md` — Exit code reference

---

## Output Format Documentation

### JSON Format (Default)
```json
{"status": "success|error", "command": "<name>", "data": {...}, "error": "msg"}
```

### Text Format
Plain text output for single values or human-readable results.

### Base64 Format
For binary data (images, PDFs, files) — outputs base64-encoded string to stdout.

---

## Error Handling Documentation

### Standard Exit Codes

- **0** — Success
- **1** — General error
- **2** — Invalid arguments/usage
- **3** — Timeout
- **4** — Resource unavailable
- **5** — Authentication failed
- **6** — Rate limited
- **7** — Permission denied

**stderr** contains human-readable error messages with recovery hints.
