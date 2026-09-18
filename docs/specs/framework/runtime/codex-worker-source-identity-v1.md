---
id: DFF-WORKER-SOURCE-IDENTITY-01
version: 1.0.0
status: selected-bounded-implementation
updated: 2026-09-16
---

# Reviewed plugin-cache junction identity

The user approved the [bounded proposal](../../../plan/framework-worker-native-continuation/20260916T013303Z/source-inventory-proposal.md). This companion amends only the source-inventory reparse rule and inventory schema in [preflight v1](codex-worker-preflight-v1.md), and the corresponding profile-source clause of [native readiness](codex-worker-native-readiness-v1.md). The old documents and their evidence remain unchanged. All other [base worker](codex-worker-feasibility-v1.md) requirements remain mandatory.

## SI-01: Closed, machine-specific identity

Compile `src/plugin-source-identity.json` as data in Rust, with a closed object containing `schema_version:1`, `adapter:"codex-0.154.0-stdio"`, and `junctions`. Each closed junction has `path`, `target`, and integer `reparse_tag`. The sole selected mapping is:

| Logical directory | Physical target | Required tag |
| --- | --- | --- |
| `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest` | `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816` | `2684354563` (`0xa0000003`, Windows directory junction) |

The discovery evidence is under `docs/plan/framework-worker-source-identity/20260916T021843Z-dev/discovery/`. At the fixed cache/provider/plugin/version levels it found three providers, seventeen plugin directories, and this one junction. Pinned [Codex 0.154.0 store source](https://raw.githubusercontent.com/openai/codex/rust-v0.154.0/codex-rs/core-plugins/src/store.rs) selects version entries for which `DirEntry::file_type().is_dir()` is true. The retained native Rust metadata probe reports false for this junction and true for physical `26.908.70816`. Thus this link obstructs strict inventory collection but is not used as the active version by that pinned lookup. The [loader](https://raw.githubusercontent.com/openai/codex/rust-v0.154.0/codex-rs/core-plugins/src/loader.rs) consumes the selected physical version root. Record the junction as membership; do not infer that Codex reads through it. Discovery is not runtime qualification.

No runtime argument, environment override, review, inventory field, alternate user root or user-provided mapping can expand this record. Do not search for a replacement, refresh a version, follow another junction, or change installed files. Standard Windows extended-prefix normalization and case-insensitive comparison identify this exact local path; parent components, UNC/device paths, relative targets, symbolic links and other reparse types are not admitted. The target must be an ordinary, existing sibling version directory with no reparse component anywhere in its path. The logical parent must also pass the strict resolver. When the fixed derived cache root contains the compiled mapping, a missing or replaced mapping fails closed. Preserve existing collection under other derived user roots: no mapping applies there, and every reparse is rejected, including an identically named relative cache link. This is not a relocated exception or a change to root derivation.

## SI-02: Observe the link; read physical sources

Only the plugin version-selector level can recognize the selected junction. All other selected locations retain strict reparse rejection. Query the link itself for directory attributes and its tag, and read its target without following it; compare both against the compiled record. Verify before and after collection. Resolve and traverse the physical directory with existing strict rules. Never open a source through the logical alias.

Keep complete membership indices for every directory already inspected by the preflight contract, including the plugin directory containing both the alias and physical version. Distinguish a verified junction member from an ordinary directory with kind byte `j` in the existing name/length index encoding (`f` and `d` remain unchanged). Read each physical source once; do not create duplicate physical file bindings by traversing the alias. Hash the existing selected control inputs and their bytes. This does not claim recursive byte coverage of plugin payloads outside the existing control-source inventory; effective-state checks must still establish inactivity before work.

## SI-03: Inventory and review binding

Inventory becomes closed schema **2**. Retain `fixture_cwd`, `roots` and `entries` with their previous meanings and bounds, and require `source_identity_sha256` (SHA-256 of the exact compiled record bytes) and `junctions` (the observed closed path/target/tag records). The emitted mapping paths are normalized absolute paths. Verification requires the compiled digest, exact applicable mapping set (the sole mapping under its pinned cache root; empty under a disjoint derived root), and fresh collection from fixed actual roots. Missing, unknown, duplicate, null and wrong-type fields fail. Schema-1 inventories cannot qualify this candidate's schema-2 native reviews. Historical schema-1 evidence remains historical.

The review itself remains schema 2: its inventory digest binds the new inventory, and `profile_sources` exactly covers physical file paths and hashes. A caller-supplied mapping never grants permission. Changed link/tag/target, physical bytes, directory membership, source identity digest, omitted/extra mappings, or stale inventory/review prevents qualification. Existing 1 MiB/file, 8 MiB aggregate, 2,048-entry, 1,024-member and depth limits, credential exclusions and fixed source roots remain unchanged.

## SI-04: Freshness before effects

Recheck the complete review/inventory at initial qualification and immediately before process creation, after argument and spawn-intent preparation. Also recheck the pinned executable identity at that final boundary. Fail before spawn on either identity failure. Existing runtime checks remain required before any thread/turn. A failed source review uses `profile_unqualified`; `profile-sources` emits exit 3 and no inventory for an invalid mapping. Do not emit a successful spawn observation when no process was created.

This experiment does not prevent a same-user hostile filesystem replacement in the interval between checks and process creation. It establishes bounded observation and rejection of observed drift, not a protected filesystem or acceptance authority.

## SI-05: Required verification and boundaries

Windows x64 is the selected platform; default package configuration has no optional features. Required cases are counted once, with subfixtures conjunctive:

| Case | Independent expected behavior |
| --- | --- |
| SI-T01 | Exact selected directory junction succeeds; inventory binds mapping, physical hashes and membership without duplicate file bindings. |
| SI-T02 | Same-byte replacement at another target, changed target, escaping target and missing target all reject. |
| SI-T03 | Directory symlink, wrong tag, ordinary directory substituted for the expected junction and missing junction reject. |
| SI-T04 | Unlisted alias, loop, additional reparse in target/ancestor/control source and alias outside plugin selector depth reject. |
| SI-T05 | Physical byte or complete indexed membership changes invalidate the retained inventory. |
| SI-T06 | Old inventory schema, stale/forged identity digest, omitted/extra mapping, unknown/duplicate/malformed fields reject. |
| SI-T07 | Review binds physical sources; stale review/inventory and review paths through the alias reject. |
| SI-T08 | Drift after initial qualification is rejected by the final check before process creation, with no child spawn. |
| SI-T09 | Existing source limits, credential exclusions, strict non-plugin paths, executable identity, policy and all WF/F-01/F-02 regressions remain valid. |
| SI-T10 | Final source/installed mapping readback shows only selected development changes; old evidence/specification bytes are retained. |

Use real Windows junction fixtures under owned test roots; injection of synthetic mapping values is permitted only through private test seams, never production APIs. Keep each stimulus, expected result and real outcome. Do not claim a synthetic fixture proves actual Codex startup. Run all affected regressions, formatting, Clippy and full first-party executed-line coverage with both 95% floors and existing stop conditions. Fresh independent QA must preserve the frozen candidate and audit test integrity.

Only after independent QA PASS may compiled source collection be attempted on the installed profile with this candidate. A complete inventory is a prerequisite, not proof of an inactive effective profile. Compiled preflight and independently supported human operator findings still precede the already-selected one-shot WN-01/WN-02 trials. Never generate all-true findings to unblock them. Launcher/policy/model/effort/fixture/deadline/no-retry selections are unchanged. Authority implementation/provisioning is outside this amendment; protected framework acceptance remains NOT_EVALUATED unless a separately qualified authority issues a decision.
