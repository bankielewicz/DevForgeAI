# Independent negative-fixture plan

## Isolation and provenance

No executable harness is created before freeze. After explicit freeze, QA will copy the frozen candidate into a QA-owned immutable snapshot/harness subtree and publish a copy manifest. Product source, product tests, specifications, installed cache/configuration, and old evidence stay unchanged. QA-only source additions or mutations exist only in the disposable copy and are recorded as deltas from the frozen manifest.

All filesystem cases use native Windows temporary roots under this QA evidence root or another explicit QA-owned path. Each junction/symlink setup is independently verified using Windows metadata and target readback before the product assertion. Cleanup removes only named QA-owned reparse entries and directories after verifying their resolved absolute paths remain inside the owned root. Retained fixtures are preferred when cleanup would weaken evidence.

## Public-entry controls

1. **Disjoint root, no exception:** set a QA-owned alternate `USERPROFILE`, create the existing allowed source layout with no reparse, and run the compiled `profile-sources` CLI. Expect exit 0, inventory schema 2, the compiled record digest, and an empty applicable `junctions` set.
2. **Disjoint root cannot relocate exception:** at the same relative `plugins/cache/openai-bundled/chrome/latest` path under the alternate root, create a real junction to a sibling physical version. Expect exit 3 and no successful inventory. The compiled absolute record must not adapt to `USERPROFILE`.
3. **Caller cannot inject mapping:** inspect CLI/request schemas and try unknown mapping/config arguments and inventory mapping mutations. Expect argument/schema rejection before collection/spawn.
4. **Public runner fixed check:** inspect the call graph and compiled surface to prove public `run`/`preflight` always invoke the fixed compiled final check. There must be no public callback, environment mapping, review field, or request field that substitutes it.

These controls do not run against the installed profile and do not start Codex.

## Private-seam real Windows matrix in the QA-owned copy

The source collector seam may accept a synthetic `Roots`/mapping only in test compilation. Each case uses real NTFS junction/symlink behavior and candidate production collector code.

| Fixture | Stimulus | Independent expected result |
| --- | --- | --- |
| Exact | One selected junction and ordinary physical sibling with source controls | Collect succeeds; `j` membership; normalized mapping; physical-only file paths; no duplicate binding. |
| Same bytes elsewhere | Copy identical source bytes to a different sibling target and repoint alias | Reject identity despite identical content. |
| Changed/escape/missing target | Repoint to another sibling, outside parent, or absent target | Reject before traversal. |
| Wrong type/tag | Directory symlink, ordinary directory, file reparse where creatable | Reject; setup proves actual OS type/tag. |
| Unlisted/loop/depth | Add unlisted alias, junction loop, alias at provider/plugin/control depth | Reject strict grammar/reparse policy. |
| Reparse in target chain | Add junction/symlink to target ancestor or control-source path | Reject; never read through alias. |
| Byte drift | Collect, alter one physical control byte, verify retained inventory | Reject stale inventory. |
| Membership drift | Collect, add/remove/rename a member at each indexed level | Reject even when retained file bytes are unchanged. |
| Schema/digest | Schema 1, wrong/invalid digest, omitted/extra/duplicate mapping, unknown/null/wrong-type fields | Reject closed schema/identity. |
| Review paths | Alias path, stale inventory digest, stale physical hash, omitted/extra physical binding | Reject review qualification. |

The oracle derives from the contract's absolute/sibling/type/schema rules and independently computed SHA-256/member lists. It does not copy the candidate's acceptance predicate.

## Final-boundary no-spawn control

Build `protocol-peer.exe` first. In the QA-owned test compilation, use the existing private final-check callback only to mutate a reviewed source after durable `spawn_intent` and argument preparation. Require exactly one final-check call, `profile_unqualified`, no `server_started`, null worker exit, stopped/empty owned tree, and no peer-side trace. Source inspection must confirm no callback or arbitrary checker reaches the public API and that no journal callback/argument construction intervenes between the final compiled check and `OwnedProcess::spawn`.

A separate negative sensitivity check in a disposable copy will deliberately bypass the final-check error or relabel junction membership; the independent assertions must fail. This demonstrates that the harness can detect the protected ordering/identity defect. The mutated copy never contributes passing product evidence or coverage.

## Integrity limits

Synthetic mapping values establish bounded collector logic only; they do not qualify actual Codex startup or installed-profile state. Deterministic protocol peers establish offline protocol/process behavior only. Setup failures are `ERROR`/harness gaps, never product failures or valid Red evidence. No retry follows a terminal integrity, metric, or critical-security stop.
