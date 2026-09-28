# DevForgeAI for Codex

Source package containing Brainstorm and Documents Updater. The plugin manifest is
version 0.2.0; this directory is not an installation or marketplace registration.

| Skill | Purpose | Source and evaluation report |
|---|---|---|
| Brainstorm (SKL-001 v7) | Explore ideas and record user-confirmed decisions in BRN documents | [Brainstorm import report](IMPORT-REPORT.md) |
| Documents Updater (SKL-005 v2) | Update README files, changelogs and guides from verified repository changes, or prepare exact proposals | [Documents Updater import report](DOCUMENTS-UPDATER-IMPORT-REPORT.md) |

## Using the source

After enabling the plugin in Codex, select the skill or invoke it explicitly:

```text
$brainstorm ways our dental clinic could reduce appointment no-shows
$documents-updater update the documentation for my uncommitted changes
$documents-updater v1.0.0..HEAD propose
```

Natural-language requests can also select either skill. Questions use native
`request_user_input` when the current host mode permits it; otherwise the skill asks
in plain text. Resources resolve from the loaded skill directory. No connector,
credentials, MCP server or background hook is required by either skill.

Documents Updater preserves published release sections, staging choices and unrelated
work. It runs only when requested or matched to a documentation request. Repository
templates take priority over its twelve fallback templates. Its Python Markdown checker
uses the standard library and cannot determine whether a documentation claim is true.

## Local checks

Run from this package directory with Python 3:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 -B skills/documents-updater/scripts/check_docs.py /path/to/project/README.md
python3 -B skills/brainstorm/scripts/validate_brn.py /path/to/project/docs/specs/brainstorm/BRN-001.md
```

The [Documents Updater evaluation guide](evals/documents-updater/README.md) explains
fixture generation and native Codex evaluations. Tests and import evidence are development
resources; only the manifest and skills are needed at runtime.

Brainstorm source and historical evaluation evidence are preserved. Adding Documents
Updater does not qualify, install or approve either skill. The new port's provenance
records unknown authoring model/session identifiers rather than inventing them.
