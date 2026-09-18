# Native capability observation

The installed `codex exec --help` command exited 0 during intake, but emitted these diagnostics (transcribed from the retained conversation tool result; not a second execution):

```
WARNING: failed to clean up stale arg0 temp dirs: Access is denied. (os error 5)
WARNING: proceeding, even though we could not create PATH aliases: Access is denied. (os error 5) at path "C:\Users\bryan\.codex\tmp\arg0\codex-arg0t36Iwu"
```

The CLI supports `--ephemeral`, `--sandbox`, `--skip-git-repo-check`, `--json`, and `--output-last-message`. Ephemeral session persistence does not establish containment of global startup effects. Read-only configuration inspection observed model gpt-6-astra and node_repl/openaiDeveloperDocs MCP sections. No credentials were inspected or copied. No config, authentication, model, hook, permission, or installation changes were made. CLI version was not queried after the startup-side-effect warning.

Current user scope prohibits external mutation. Native positive, invalid-input and implicit-discovery cases remain NOT_RUN because native host side effects cannot be established as contained using current permissions/configuration. This is an evaluator capability limitation, not a ledger-c defect. No native attempt was launched, and none was retried.
