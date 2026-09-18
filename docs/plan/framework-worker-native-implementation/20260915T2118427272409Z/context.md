# Selected native-readiness development

Destination: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
Evidence: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-implementation\20260915T2118427272409Z`.

User selected implementation of native readiness first; acceptance authority implementation and provisioning are deferred. Existing physical Codex 0.154.0, `gpt-6-astra` / `high`, one WN-01 and one WN-02 attempt after all prerequisites and independent QA. No automatic retry, model/provider/version substitution, installation, operational configuration or credential changes.

Inputs are bound in inputs-manifest.json. All 32 baseline package files match the selected independent-retest candidate (baseline-readback.json). No Git metadata; SHA-256 manifests bind source. Windows native C: checkout, PowerShell, standalone package Cargo.toml/Cargo.lock, no optional feature declarations. Separate fresh Cargo target and retained fixtures under this evidence root. No nested instructions apply to the package or selected evidence directories.

## Requirements matrix and denominators (before execution)

Windows x86_64 is the required platform. No Linux or tray acceptance is selected.

| Requirement | Expected result / level | Planned evidence | Initial status |
| --- | --- | --- | --- |
| NI-T01 | Exactly pinned two-junction mapping permits physical identity, no alias execution; Rust integration/unit | identity tests + mapping observation | NOT_RUN |
| NI-T02 | Changed target/tag and same bytes at another path rejected; Rust filesystem tests | synthetic junction cases | NOT_RUN |
| NI-T03 | Digest/file/adapter mismatch rejects without PATH fallback | negative identity cases | NOT_RUN |
| NI-T04 | All non-worker paths retain strict reparse rejection | regression + strict path tests | NOT_RUN |
| NI-T05 | Rechecking mapping/bytes catches drift before spawn | repeated-check fixtures + runner integration | NOT_RUN |
| NI-T06 | Original WF-01..20, 26 supplemental, 4 repair functions, 6 units remain valid | full cargo tests + old independent helper | NOT_RUN |
| NI-T07 | One exact native-only shell-free argv, no caller injection | policy tests after version verification | BLOCKED dependency |
| NI-T08 | Version/digest/source-inventory failures reject | policy review tests after verification | BLOCKED dependency |
| NI-T09 | Disabled integrations proven inactive before threads; managed/hooks unknown fails | pinned source/effective profile review | BLOCKED dependency |
| NI-T10 | Credentials/profile/model/effort/sandbox checks before turn | protocol regression + qualified native preflight | BLOCKED dependency |
| NI-T11 | WN-01 exact final output, no tools, immutable fixture, stopped tree | native trial after independent QA | BLOCKED dependency |
| NI-T12 | WN-02 interrupted turn and stopped tree, honest race outcome | native trial after independent QA | BLOCKED dependency |

Overall selected readiness denominator: 12 mandatory NI groups, including both native cases. Initial ready offline development denominator: NI-T01..06 (six groups), with original WF-01..20 and all existing regression functions retained separately. Policy/native groups cannot be passed by offline peers. Later reports must distinguish partial subcomponent checks from full NI completion.

First-party executable source denominator: every executable line under package `src/`, including new identity/policy code, Windows process and CLI branches; no uncovered first-party exclusions. Exclude tests/ (synthetic peer/drivers/fixtures) and third-party dependencies. lib.rs module declarations have no executable lines. The LLVM collector determines the line count; report exact numerator/denominator and separately branch data when available. Floors: >=95% required cases and >=95% executed lines; mandatory/security failures are never waived.

Python capture helpers retain evidence only and make no acceptance decisions. Development and independent QA results cannot establish protected framework acceptance.
