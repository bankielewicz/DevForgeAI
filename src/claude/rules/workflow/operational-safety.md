---
name: operational-safety
description: Rules for safe file operations and project-scoped temporary directories
version: "1.0"
created: 2026-02-27
---

# Operational Safety Rules

## Rule 1: Use Native Tools for File Operations

All file read, write, search, and edit operations MUST use the built-in native tools (`Read`, `Write`, `Edit`, `Glob`, `Grep`) rather than shell commands such as `cat`, `echo`, `sed`, `awk`, or `find`. Native tools provide significant token savings and structured error handling that Bash-based file manipulation cannot match.

Agents must not fall back to Bash for convenience. If a native tool exists for the operation, it must be used unconditionally.

See also:
- `devforgeai/specs/context/anti-patterns.md` — Category 1 (Tool Usage Violations) defines forbidden Bash file operation patterns and their native tool replacements.
- `.claude/rules/core/critical-rules.md` — Rule 2 (File Operations) mandates native tools for 40-73% token efficiency gains.

---

## Rule 2: Project-Scoped Temporary Files

Use of the system `/tmp/` directory is **FORBIDDEN** for any workflow artifact, scratch file, or intermediate output.

All temporary files MUST be written under the project root using the pattern:

```
{project-root}/tmp/{story-id}/
```

### Wrong Example

```
/tmp/STORY-505/output.txt
/tmp/build-cache/result.json
```

### Correct Example

```
tmp/STORY-505/output.txt
tmp/STORY-505/intermediate.json
```

The correct relative path `tmp/STORY-505/` resolves from the current working directory, which must be the project root.

### Rationale

**Portability:** The `/tmp/` path is not reliably shared between WSL, Windows, and Linux environments. Files written to `/tmp/` on WSL may be invisible from Windows tooling and vice versa. Using a project-relative directory ensures cross-platform consistency.

**Traceability:** Naming temporary directories by story-id (e.g., `tmp/STORY-505/`) makes it clear which workflow produced each artifact. System `/tmp/` provides no such association, making cleanup and debugging difficult.

### Working Directory Verification

Before writing temporary files, verify that the current working directory is the project root. A simple check is to confirm that `CLAUDE.md` or `package.json` exists at the CWD. If the working directory is incorrect, resolve the project-root path before creating temporary directories.
