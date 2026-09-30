# DevForgeAI for Codex

Source package containing Brainstorm, PRD, Architecture and Documents Updater. The plugin manifest is
version 0.5.0; this directory is not an installation or marketplace registration.

| Skill | Purpose | Source and evaluation report |
|---|---|---|
| Brainstorm (SKL-001 v7) | Explore ideas and record user-confirmed decisions in BRN documents | [Brainstorm import report](IMPORT-REPORT.md) |
| PRD (SKL-002 v2, SPEC-002 v2) | Turn promoted BRN ideas into user-owned requirements and scope | [Current contract update](contract-update-evidence/20260929/REPORT.md); [historical import](PRD-IMPORT-REPORT.md) |
| Architecture (SKL-003 v6, SPEC-003 v4) | Classify shared components and resolve PRD architecture questions with accepted decisions, bounded evidence and per-requirement readiness | [Current contract update](contract-update-evidence/20260929/REPORT.md); [historical import](ARCHITECTURE-IMPORT-REPORT.md) |
| Documents Updater (SKL-005 v2) | Update README files, changelogs and guides from verified repository changes, or prepare exact proposals | [Documents Updater import report](DOCUMENTS-UPDATER-IMPORT-REPORT.md) |

## Using the source

After enabling the plugin in Codex, select the skill or invoke it explicitly:

```text
$brainstorm ways our dental clinic could reduce appointment no-shows
$devforgeai:prd BRN-001
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
PRD implements SPEC-002 v2; Architecture implements SPEC-003 v4. The current contract
report separates source authoring, static checks, native behavior, manual obligations and
qualification. The campaign stopped at a native usage limit: 111 automated trials completed,
four were interrupted and 155 remain NOT_RUN. The closing audit also found mixed Codex executable
versions and primary-checkout drift. Exact identity and recorded behavior failures remain open;
this candidate is not qualified. The package does not yet include Epic; Architecture names it as
the planned next step. Runtime question availability is host-dependent; unanswered decisions remain
open.

Architecture remains a draft port. Its import report records native evaluation
failures, specification discrepancies and unrun manual acceptance checks.

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
16-case matrix, manual obligations and source-to-SPEC comparison. Tests and import evidence are development
resources; only the manifest and skills are needed at runtime.

The [PRD evaluation guide](evals/prd/README.md) preserves the 29-case, 174-trial
plugin/baseline denominator and all 32 mandatory VER obligations. Source presence and
structural checks do not establish PRD qualification.

Existing skills and historical evaluation evidence are preserved. Importing Architecture
does not install the package or establish owner acceptance. Its report distinguishes
static checks, native evaluations and unrun manual obligations. Unknown authoring
model/session identifiers are recorded honestly.

The 2026-09-29 approved contract update is recorded in [contract update report](contract-update-evidence/20260929/REPORT.md).
Historical import reports and proposals describe their original candidates and remain unchanged.
