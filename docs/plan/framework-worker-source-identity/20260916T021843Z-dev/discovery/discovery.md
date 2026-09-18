# Plugin-cache junction discovery

Observation time: 2026-09-16T02:22:52.8085204Z  
Host scope: native Windows checkout at `C:\Projects\DevForgeAI`  
Selected proposal: `docs/plan/framework-worker-native-continuation/20260916T013303Z/source-inventory-proposal.md`, SHA-256 `7832f32fcc1a0a4be59458b8c1202937fcfdcecda18a944612f51e6b7a7b63e2`.

This was read-only discovery of installed plugin-cache metadata and package bytes. It did not modify links, cache content, configuration, credentials, accounts, or startup state. Enumeration descended only into non-reparse provider and plugin directories. The only followed reparse was the already identified exact `chrome/latest` mapping for a one-file equality check.

## Exact mapping result

The fixed cache/provider/plugin/version enumeration found 3 providers, 17 plugin directories, and 23 immediate plugin members. Exactly one immediate member was a reparse point:

| Field | Observed value |
| --- | --- |
| Logical path | `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest` |
| PowerShell type | `Directory, ReparsePoint`; `LinkType=Junction` |
| Reparse tag | `0xa0000003` (`Microsoft`, `Name Surrogate`, `Mount Point`) |
| Substitute target | `\??\C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816` |
| Print target | `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816` |
| Physical target type | ordinary directory, not a reparse point |

All provider and plugin directories were ordinary directories. Every other immediate version or install-record member was non-reparse. No wildcard mapping or second exception is supported by this observation.

The physical Chrome package contains 64 directories, 381 files, 14,489,799 file bytes, and no nested reparse points. The largest immediate directory membership is 45. Three payload files exceed 1 MiB and the largest is 4,084,148 bytes. These payload figures characterize the package; the selected companion contract does not claim recursive payload-byte coverage.

The physical `.codex-plugin/plugin.json` declares `name=chrome`, `version=26.908.70816`, has 3,294 bytes, and SHA-256 `30cecefd335796f68e1e8501f28ffb81af414dd409284d5e4f188e32f11c90cb`. The same file read through the known logical mapping had the same digest and length.

## Pinned Codex 0.154.0 role

Primary source is the OpenAI `rust-v0.154.0` tag:

- `store.rs`: <https://raw.githubusercontent.com/openai/codex/rust-v0.154.0/codex-rs/core-plugins/src/store.rs>
- `loader.rs`: <https://raw.githubusercontent.com/openai/codex/rust-v0.154.0/codex-rs/core-plugins/src/loader.rs>
- Retrieved through the web reader on 2026-09-16 after the local metadata observation.

`store.rs` lines 23-25 and 100-129 define the cache as `plugins/cache` and the package layout as `<marketplace>/<plugin>/<version>`. Lines 157-181 enumerate the plugin directory, retain only entries for which `DirEntry::file_type().is_dir()` is true, validate and sort their names, and select `local` or the greatest version. The decisive source fragment is `entry.file_type().ok().filter(std::fs::FileType::is_dir)?;`.

The native Rust probe in this directory used the same standard-library file-type observation and returned:

```text
name=26.908.70816;is_dir=true;is_file=false;is_symlink=false;attrs=0x00000010
name=latest;is_dir=false;is_file=false;is_symlink=true;attrs=0x00000410
```

Therefore the pinned Codex implementation excludes this Windows junction from its discovered version directories and selects the ordinary `26.908.70816` directory. `loader.rs` lines 245-252, 311-346, and 357-430 use the store's active version/root for installed plugin reconciliation and curated cache refresh.

The evidence does not support calling `latest` a Codex selection alias. Its role in this candidate is narrower: it is an installed cache member that blocks the worker's complete directory inventory. The bounded amendment should record and verify this exact member and target without traversing the junction or treating it as a profile source. The physical `26.908.70816` directory remains separately inventoried through its ordinary path.

The retained 0.154.0 generated `PluginListResponse.json` additionally describes local assets as resolved from the installed plugin package and `localVersion` as the locally materialized package version. It does not document a `latest` alias. Its path is `docs/plan/framework-worker-contract/20260915T151300Z/codex-schema/v2/PluginListResponse.json`, SHA-256 `a405d2514d6236df75130c87c749e0e070b946a889f143a0448bbcd27d1d8501`.

## Commands and observed results

All commands ran from `C:\Projects\DevForgeAI` in PowerShell. Relevant successful commands exited 0.

1. Fixed-level enumeration used `Get-Item -Force -LiteralPath` and `Get-ChildItem -Force -LiteralPath`, descending only when `Attributes` did not include `ReparsePoint`. Result: 3 providers, 17 plugins, 23 immediate members, 1 reparse member.
2. `fsutil reparsepoint query 'C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest'` returned tag `0xa0000003` and the exact substitute/print targets above.
3. A queue-based physical-tree metadata walk enqueued only non-reparse directories. Result: 64 directories, 381 files, 14,489,799 bytes, 0 nested reparses, maximum immediate membership 45.
4. `Get-FileHash -Algorithm SHA256 -LiteralPath <logical-plugin-json>,<physical-plugin-json>` returned the same `30CECEFD...F11C90CB` digest for both paths.
5. `rustc --edition 2024 discovery/rust-file-type-probe.rs -o discovery/rust-file-type-probe.exe` followed by the executable produced the two file-type rows above.

Retained attempt note: an initial PowerShell formatting command exited 1 with `ParserError: An empty pipe element is not allowed`; the corrected in-memory enumeration exited 0. The first Rust probe compile exited 1 because stable `MetadataExt` has no `reparse_tag()` method. The source was narrowed to `file_attributes()` plus `DirEntry::file_type()` and the second compile/run exited 0. `fsutil` supplies the authoritative reparse tag independently.

