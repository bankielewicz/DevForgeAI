# Proposed next selection: bounded plugin-cache source identity

**PROPOSED ONLY — not an amendment, implementation, or launch authorization.** Current specifications and candidate bytes are unchanged.

## Observed problem

The newly qualified 53-file candidate's compiled `profile-sources` operation exits 3 at `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest`. Current Windows metadata identifies this as a directory junction to `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816`. The strict contract correctly rejects it. Source collection therefore cannot produce the complete inventory needed for effective-profile inspection and WN-01/WN-02.

The adopted repair handoff explicitly excludes source-inventory exceptions. The preflight contract also says no configuration edits, reparse removal or policy relaxation is implied. A new selection is required to change this rule.

## Proposed selected scope

Amend the worker source-identity contract, implement the bounded rule in compiled Rust, and independently QA the changed candidate. Preserve the old contract versions/evidence. Select these constraints together:

1. Discover the exact applicable cache junction mappings and their version-matched role before changing code. The observed chrome mapping is a known blocker, not proof that it is the only mapping or source.
2. Permit only an explicitly enumerated, compiled-in reviewed mapping with the expected Windows directory-junction tag, exact logical path and exact physical target. No caller-controlled allowlist, wildcard alias, general `canonicalize` bypass, symlink substitution, additional junction or automatic version refresh.
3. Bind mapping identity, physical source bytes and complete directory membership in the inventory/review contract. Recheck mapping and source identities during review validation and immediately before process creation. Drift fails closed.
4. Keep credential exclusions, fixed roots, inventory limits and every other path rejection. Do not omit plugin inputs merely because a disabling flag exists; actual effective-state checks still must prove inactivity.
5. Leave installed links, caches, configuration, credentials, accounts and startup state unchanged. This is a source-observation amendment, not an operational cleanup.
6. Preserve the physical Codex identity, fixed restrictive policy, immutable fixtures, model/effort, one-shot trial limits and all protected-authority boundaries.
7. Use requirement-derived Red/Green tests for exact mapping success and rejection of changed tag/target/bytes, unlisted mapping, loops, extra reparse components, escaping targets and stale inventory/review. Re-run all affected regressions and full first-party coverage with both 95% floors; stop under existing QA rules.
8. Only after independent QA passes, retry the source collection on the new candidate. A complete inventory still precedes compiled preflight and the separate human operator findings; no all-true findings or native success is assumed.

This proposal cannot guarantee that source collection or native Codex qualification will then pass: another installed-source or effective-state predicate may fail. Preserve each distinct outcome and do not silently broaden the mapping set.

Alternative: retain strict rejection and leave native trials blocked until the host/source prerequisites change through a separately reviewed operational action. No such operational action is proposed or authorized here.

Authority implementation/provisioning remains separately deferred. Its existing first-policy adapter binds an older candidate and cannot be applied unchanged to the current worker.
