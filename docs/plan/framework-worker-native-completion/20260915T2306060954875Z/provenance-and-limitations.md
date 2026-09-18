# Evidence and source limitations

Final independent QA stopped on `QA-F-COV-01`: 2,852/3,103 executed lines, 91.91105381888495%. No native work followed that stop. The initial context's NTFS label is not independently substantiated; final environment reporting identifies the local Windows C: location and records filesystem type as unverified after a denied volume query.

The independent QA candidate is frozen at 48 files: manifest SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`. Selected input manifest SHA-256 `3fafe784e180b37cabaf8e276c8f324ea464fd568dcfa9a05688a55db9e88288`. Candidate snapshot is adjacent. No source/test/specification edits are permitted during that independent campaign.

## Development evidence

Root command recorder and the policy, review, source and integration slices preserve separate raw streams, native exit codes, command arguments, cwd, timing and source identities for their recorded Cargo attempts. Setup-only failures and evolving-candidate attempts remain distinct from behavioral Red and final candidate QA. The initial source collector blocked on a real plugin-cache reparse; it did not launch Codex.

Two development formatting/setup invocations in the integration slice did not retain separate native raw stdout/stderr, individual exit codes or durations. The original tool-returned response is retained at `integration-dev/pre-final-policy-setup-failure-tool-response.json`; its limitations are explicit. One formatting invocation returned no text before the recorded rate-limit Red. These are evidence-retention gaps, not product failures or complete raw command receipts. This development run does not claim complete raw retention of every attempt. Fresh independent QA must provide complete qualification-command capture. The root's final whole-package formatting correction and earlier full Clippy command were separately recorded.

The effective-profile validator slice used a separate selected destination:
`C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2310034070895Z-effective-dev`.
Its final focused Cargo test and Clippy invocations used `--locked` but not `--offline`; they are not relabeled as offline commands. Final independent QA uses the selected locked/offline commands. No dependency installation is claimed.

## Pinned sources

The retained 0.154.0 protocol schemas and actual feature-list baseline bind names and schema definitions. Feature baseline SHA-256 is `10e096f2fdf3dd3546065097bb3eadccb1336d91160586fb4a5b0a6eeb577ec9`; ConfigReadResponse schema SHA-256 is `bd72c94e2c7d49ead6a20bcf54afedc8db11044bf8cadb387e42135dd5d1e342`. These reside in the earlier retained schema/profile discovery roots referenced by context.md.

Research consulted the upstream [version-tagged feature registry](https://raw.githubusercontent.com/openai/codex/rust-v0.154.0/codex-rs/features/src/lib.rs) and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference). The web retrieval's raw source body/digest was not retained; a direct source download was blocked. This is source guidance, not a digest-proven correspondence between upstream source and the installed executable. The actual effective disabled-feature state still needs native preflight evidence.

The child console change follows [Microsoft process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags) and the retained held-job process-image observations. It preserves atomic job membership and explicit inherited stdio handles. Fresh original process-tree/cancellation regressions remain mandatory.

## Native prerequisites

There is no established source call-chain proving that disabling plugins makes every cached control file irrelevant before and after initialize. Consequently, the cache is not excluded and the observed `chrome/latest` reparse remains a blocker. No operational link/configuration is edited. The conservative provider checks plus operator review do not prove an undocumented internal endpoint selection; unknown provider behavior cannot qualify native execution.

No native app-server inspection or WN-01/WN-02 model trial has been launched in this run. Model/effort selection remains `gpt-6-astra`/`high`, one attempt each after prerequisites, with no automatic retry. Protected authority remains outside this component; framework acceptance is NOT_EVALUATED.
