# DevForgeAI Brainstorm for Codex

Source port of the Claude Brainstorm skill, SKL-001 v5, implementing the planning workflow
in SPEC-001 v10 with the provider adaptations described in [IMPORT-REPORT.md](IMPORT-REPORT.md).
This Codex variant is SKL-001 v6 and the plugin manifest version is 0.1.0.

The package contains `.codex-plugin/plugin.json`, `skills/brainstorm/`, and eight imported
evaluation definitions. The skill includes its BRN template, framework catalog, default
framework, output rules, Python validator, and `agents/openai.yaml` for implicit invocation.
It writes into the consuming project's `docs/specs/brainstorm/`; plugin resources resolve
relative to the loaded skill. It never decides dispositions or convergence for the user.

## Using the source

This directory is source, not an installation or marketplace registration. After enabling
the plugin in Codex, select **DevForgeAI Brainstorm**, or use `$brainstorm` in Codex CLI:

```text
$brainstorm ways our dental clinic could reduce appointment no-shows
```

Natural-language brainstorming requests may also select it. The PRD skill is not included;
the handoff names that missing workflow and the BRN ID without invoking Claude commands.
No connector, credentials, MCP server, or background hook is needed.

## Local checks

Run from this package directory with Python 3:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 skills/brainstorm/scripts/validate_brn.py /path/to/project/docs/specs/brainstorm/BRN-001.md
```

The validator uses the standard library; PyYAML, when available, adds YAML parsing. It is
a partial structural check and cannot prove user consent or complete schema conformance.
The session-aware validator tests are distinct from the native skill evaluations described
in [evals/README.md](evals/README.md), which remain NOT_RUN.

The import retains source hashes and changes in [import-evidence/](import-evidence/).
Provider edits do not approve the specification, install the plugin, or qualify native
behavior. The exact authoring model was not exposed, so the port provenance states unknown.

Packaging follows the supported plugin-creator compatibility layout:
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).
Invocation and metadata follow [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills).
