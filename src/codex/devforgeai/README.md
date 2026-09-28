# DevForgeAI for Codex

Source package containing Brainstorm, Architecture and Documents Updater. The plugin manifest is
version 0.3.0; this directory is not an installation or marketplace registration.

| Skill | Purpose | Source and evaluation report |
|---|---|---|
| Brainstorm (SKL-001 v7) | Explore ideas and record user-confirmed decisions in BRN documents | [Brainstorm import report](IMPORT-REPORT.md) |
| Architecture (SKL-003 v4) | Resolve PRD architecture questions with accepted decisions, bounded evidence and per-requirement readiness | [Architecture import report](ARCHITECTURE-IMPORT-REPORT.md) |
| Documents Updater (SKL-005 v2) | Update README files, changelogs and guides from verified repository changes, or prepare exact proposals | [Documents Updater import report](DOCUMENTS-UPDATER-IMPORT-REPORT.md) |

## Using the source

After enabling the plugin in Codex, select the skill or invoke it explicitly:

```text
$brainstorm ways our dental clinic could reduce appointment no-shows
$devforgeai:architecture PRD-001
$documents-updater update the documentation for my uncommitted changes
$documents-updater v1.0.0..HEAD propose
```

Natural-language requests can also select these skills. Questions use native
`request_user_input` when the current host mode permits it; otherwise the skill asks
in plain text. Resources resolve from the loaded skill directory. No connector,
credentials, MCP server or background hook is required by these skills.

Documents Updater preserves published release sections, staging choices and unrelated
work. It runs only when requested or matched to a documentation request. Repository
templates take priority over its twelve fallback templates. Its Python Markdown checker
uses the standard library and cannot determine whether a documentation claim is true.

Architecture reads PRD documents under `docs/specs/prd/`, writes ARCH and ADR documents,
and asks before inspecting code outside the approved scope. Organizational policy comes
from `docs/specs/policy/`; local configuration uses `.codex/devforgeai.local.md`.
The package does not yet include the PRD or Epic skills; Architecture can consume an
existing PRD and names Epic as the planned next step. Runtime question availability is
host-dependent; unanswered decisions remain open.

## Local checks

Run from this package directory with Python 3:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 -B skills/documents-updater/scripts/check_docs.py /path/to/project/README.md
python3 -B skills/brainstorm/scripts/validate_brn.py /path/to/project/docs/specs/brainstorm/BRN-001.md
```

The [Documents Updater evaluation guide](evals/documents-updater/README.md) explains
fixture generation and native Codex evaluations. The
[Architecture evaluation guide](evals/architecture/README.md) documents its separate
14-case matrix, manual obligations and source-to-SPEC comparison. Tests and import evidence are development
resources; only the manifest and skills are needed at runtime.

Existing skills and historical evaluation evidence are preserved. Importing Architecture
does not install the package or establish owner acceptance. Its report distinguishes
static checks, native evaluations and unrun manual obligations. Unknown authoring
model/session identifiers are recorded honestly.
