# Source-inventory requirement and case matrix

All cases derive from `codex-worker-preflight-v1.md` lines 22-30 and NI-T08/NI-T10: closed typed inventory, fixed bounds, explicit absence, strict source grammar, no credential reads, and fail-closed source identity.

| Case | Requirement-derived expected result | Test level | Independent oracle |
| --- | --- | --- | --- |
| SI-E01 | Every state tuple follows the closed schema; wrong version or invalid nullable-field combinations reject. | Private Rust unit | Literal schema version, 1 MiB file cap, and 1,024 item cap from the specification. |
| SI-E02 | The 2,049th entry rejects; eight real 1 MiB files accumulate successfully and a further byte rejects with `profile_source_limit`. | Private Rust unit with real files | Literal 2,048-entry, 1 MiB file and 8 MiB aggregate limits from the specification. |
| SI-E03 | Nine nested rule directories and more than 32 scoped ancestors reject with `profile_source_limit`; a leaf outside the root rejects scope. | Private Rust unit with real directories | Literal eight rule-directory and 32 ancestor-level limits. |
| SI-E04 | A directory with 1,025 children rejects; a selected source with directory type where a file is required rejects. | Private Rust unit with real directories | Literal 1,024 member cap and the required file/directory state distinction. |
| SI-E05 | Files in provider/plugin positions and unknown plugin-control members reject; recognized remote-install/control inputs are inventoried while unrelated version payload files are not read as controls. | Private Rust unit with real plugin trees | Closed source-tree grammar stated by the contract and existing selected implementation documentation. |
| SI-E06 | Credential-like names, including non-Unicode names that cannot be safely compared, reject before content access. | Private Rust unit | Contract prohibition on credential reads and fail-closed unknown names. |
| SI-E07 | Hash length drift and reads beyond 1 MiB reject; relative/parent paths reject. | Private Rust unit with real files | Literal file bound, strict absolute-path contract, and complete typed source identity. |
| SI-E08 | Missing descendants remain explicit resolved absences and directory observations have stable case-insensitive ordering. | Private Rust unit with real directories | Explicit absence and deterministic membership requirements. |

Required-case denominator for this slice: 8 cases, counted once each. This is developer characterization evidence, not the final full-suite or coverage denominator; independent QA owns the qualifying retest.
