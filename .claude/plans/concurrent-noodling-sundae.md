# DevForgeAI CLI Landscape Inventory

## Context

The user wants to understand the CLI entry points in the project before the new Rust binary (`./bin/devforgeai`) replaces the existing ones. Three CLIs exist today, with the Rust binary being a prototype under development in a separate project.

---

## CLI Inventory

| # | CLI | Type | Invocation | Status |
|---|-----|------|------------|--------|
| 1 | `devforgeai` (Node.js) | npm package bin | `devforgeai <command>` | **Installed** globally via npm. Currently permission-denied (likely needs `npm link` refresh). Limited to `install` command. |
| 2 | `devforgeai-validate` | Python (pip editable install) | `devforgeai-validate <command>` | **Broken** — `PackageNotFoundError` means the editable install is stale. Needs `pip install -e ./.claude/scripts/`. Has 16 subcommands (phase management, DoD validation, context validation, hooks, ast-grep, feedback). |
| 3 | `./bin/devforgeai` (Rust) | Compiled ELF binary | `./bin/devforgeai <command>` | **Prototype** — not ready. Being developed in a separate project. Replicates Python CLI commands (phase, validate, check-git, hooks, install, ast-grep, feedback-reindex) plus `approve-bypass`. |

### Supporting scripts (not primary CLIs)
- `./bin/devforgeai.js` — Node.js entry point for the npm `devforgeai` package
- `./bin/act` — GitHub Actions local runner (utility, not DevForgeAI-specific)
- `scripts/validate_deferrals.py` — Standalone deferral format validator
- `.claude/scripts/devforgeai-validate` — Bash shim wrapper for the Python CLI

---

## Key Observations

1. **Node.js CLI** (`devforgeai`) — Thin wrapper; only does `install`. Delegates to Python for actual work.
2. **Python CLI** (`devforgeai-validate`) — The workhorse. All 16 validation/phase commands live here. Currently broken due to stale pip metadata.
3. **Rust binary** (`./bin/devforgeai`) — Future replacement. Prototype stage, developed externally. Mirrors Python CLI command surface + adds `approve-bypass`.

## No action needed — this is an inventory/reference document.
