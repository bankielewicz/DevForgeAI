# Profile-source identity development handoff

Scope: the inventory schema, compiled plugin-source identity, exact Windows junction observation, physical-source traversal, and focused SI-T01 through SI-T07 tests. Runner SI-T08 and integrated package qualification are owned by the parent development run.

## Implemented behavior

- Compiled `src/plugin-source-identity.json` contains the sole selected Chrome `latest` directory-junction mapping and tag `0xa0000003`.
- Inventory schema 2 requires the exact compiled-record digest and observed junction records. Review source bindings remain physical paths only.
- The selected mapping applies only when the fixed derived plugin-cache root is the selected installed root. Disjoint synthetic roots retain strict collection with no applicable exception; an identical relative junction there rejects.
- Collection verifies the selected mapping before traversal and again after physical hashing/membership collection. It records the alias as index kind `j`, requires the ordinary sibling physical version, and never traverses the alias.
- All other reparse locations remain rejected. The existing public request resolver is unchanged.
- Native executable junction helpers are crate-private for reuse; the public launcher-verification API is unchanged.

## TDD and focused results

- `red-001/`: retained fixture setup failure. Forward separators reached `cmd.exe` as switches, so this is not product Red.
- `red-002/`: valid behavioral Red. A real test-owned NTFS junction was created and independently read back; the existing collector rejected exact `chrome\\latest` with `profile_source_reparse`. Native exit 101; candidate before/after digest `a551455a00d782c8f7e37c1b80d1776f37e6b31c196ee50e49c905e791cf77d0`.
- `green-t01-001/`: original focused SI-T01 Green.
- `focused-profile-final/`: 20/20 profile-source unit tests passed, including SI-T01 through SI-T06 and prior strict-source regressions. Candidate stayed unchanged during the run.
- `focused-review-final/`: 6/6 closed-review tests passed, including SI-T07 reparse paths. Candidate stayed unchanged during the run.
- `focused-cli-final/`: the compiled source-inventory CLI case passed with schema 2, exact compiled-record digest, and empty applicable junction set for the disjoint synthetic user root. Candidate stayed unchanged during the run.
- `focused-lib-001/`: retained nonqualifying setup failure: 36/37 passed, while the parent-owned SI-T08 unit required a peer binary not built by the lib-only command. The qualifying all-target campaign must build the peer.

The post-collection retarget test was added within the same collector slice after the original SI-T01 Red. It has passing evidence; no separate historical Red is claimed for that subfixture.

## Focused test integrity

The positive test uses a real Windows junction, verifies the reparse attribute and `read_link`, compares a literal SHA-256 for known physical control bytes, and compares the independently encoded `d`/`j` directory-index digest. Negative subfixtures cover same-byte alternate targets, escape/missing targets, symlink/wrong tag, ordinary/missing junction, unlisted and loop links, nested and wrong-depth reparses, physical byte and membership drift, post-collection retargeting, old/forged/omitted/extra schema data, malformed fields, and reparse review/inventory/source paths.

## Pending parent checks

The parent run is applying lint-only refactors after source freeze, then owns package rustfmt, Clippy, all-target regressions, full first-party coverage, final candidate binding, and separate independent QA. These focused receipts do not establish native Codex qualification or framework acceptance.
