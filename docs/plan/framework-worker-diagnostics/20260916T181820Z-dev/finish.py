"""Read back and summarize this bounded development delivery, not acceptance."""
from record import ROOT, REPO, PACKAGE, digest, manifest, write
from pathlib import Path
import datetime
import json
import re

def md(name, content):
    path = ROOT/name
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(content)
    assert path.read_text(encoding='utf-8') == content

candidate = json.loads((ROOT/'candidate-v2-manifest.json').read_text())
assert candidate == manifest()
candidate_sha = digest(ROOT/'candidate-v2-manifest.json')
for entry in candidate:
    assert digest(ROOT/'candidate-v2-snapshot'/entry['path']) == entry['sha256']
bindings = json.loads((ROOT/'input-bindings.json').read_text())
for entry in bindings:
    assert digest(Path(entry['path'])) == entry['sha256'], entry['path']
coverage = json.loads((ROOT/'final-coverage-analysis.json').read_text())
assert coverage['floor_met']
inventory = json.loads((ROOT/'final-test-inventory.json').read_text())
assert inventory['required_test_count'] == 133
attempt_ids = ['19-final-clippy','20-final-inventory','21-final-offline','22-final-coverage',
               '23-final-fmt-check','24-final-doc-tests','25-final-build']
receipts = {name:json.loads((ROOT/'attempts'/name/'receipt.json').read_text()) for name in attempt_ids}
for name, receipt in receipts.items():
    assert receipt['exit_code'] == 0, name
    assert receipt['candidate_sha256'] == candidate_sha, name
    for stream in ['stdout','stderr']:
        assert digest(ROOT/'attempts'/name/f'{stream}.txt') == receipt[f'{stream}_sha256']
assert 'running 40 tests' in (ROOT/'attempts/21-final-offline/stdout.txt').read_text()
assert '40 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out' in (ROOT/'attempts/21-final-offline/stdout.txt').read_text()

baseline = {e['path']:e['sha256'] for e in json.loads((ROOT/'baseline-manifest.json').read_text())}
for path in ['Cargo.toml','Cargo.lock','src/launch_policy.rs','src/restrictive-launch-policy.json',
             'src/native-executable-identity.json','src/plugin-source-identity.json',
             'src/native_identity.rs','src/profile_sources.rs','src/request.rs','src/journal.rs',
             'tests/fixtures/task.json','tests/fixtures/prompt.txt','tests/fixtures/expected.json',
             'tests/fixtures/output-schema.json','tests/fixtures/schema-command.json']:
    assert digest(PACKAGE/path) == baseline[path], path

exe = ROOT/'target/debug/devforgeai-codex-worker-probe.exe'
exe_sha = digest(exe)
rows = '\n'.join(f"| {name} | `cargo {' '.join(r['arguments'])}` | 0 | {r['seconds']:.3f} s |"
                 for name,r in receipts.items())
changed = '\n'.join('- `'+p+'`' for p in inventory['changed_files'])
percentage = coverage['percentage']
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

md('delivery.md',f'''# Rust native-denial diagnostic development delivery

Development status: **COMPLETE for the selected bounded implementation and independent offline QA handoff**. Independent QA is **NOT_RUN**. No native Codex preflight/trial or installed source collection was launched. Framework acceptance is **NOT_EVALUATED**. The original native failure remains unexplained until a separately selected diagnostic launch.

## Candidate and environment

- Package: `{PACKAGE}`.
- Final 58-file manifest: `{ROOT / 'candidate-v2-manifest.json'}`, SHA256 `{candidate_sha}`. The corresponding candidate-v2-snapshot contains the exact source/test/config/README bytes.
- Original 56-file candidate was preserved in baseline-snapshot and verified against historical manifest `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`. The initial diagnostic candidate and attempts remain preserved separately; only candidate-v2 is delivered for QA.
- Native Windows x64 10.0.26200, PowerShell 7.6.6, C: NTFS; Rust/Cargo 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4. No Git metadata. No WSL or alternate checkout.
- Built diagnostic executable: `{exe}`, SHA256 `{exe_sha}`, {exe.stat().st_size} bytes. This is a development artifact, not an approved native-launch selection or installation.

## Implemented behavior and traceability

| Requirement | Implementation and evidence | Development result |
| --- | --- | --- |
| D1 / handoff 1: derive closed non-sensitive contract before implementation | diagnostic-contract-initial.md; final diagnostic-contract.md; typed Rust enums in diagnostic.rs | PASS |
| D2a / handoff 2: post-spawn source verification stage | runner/Session source_review observations at post_spawn and post_preflight; real missing-review verifier tests and dispatch wiring | PASS, offline scope |
| D2b / handoff 2: initialize/config process accounting | one existing held-job query returns total/active; exact 1/1 success, 2/1 exited-descendant rejection, 1/0 stopped-worker rejection; initialize/config/checkpoint tags | PASS |
| D2c / handoff 2: closed config rejection categories | same validator, same predicate order/values; section/predicate markers; 22 literal mutation cases, missing/duplicate session-layer and path/precedence subfixtures | PASS |
| D2d / handoff 2: privacy and failed RPC stage | closed serialized events; sentinel/unknown-field tests for config, layer, origin, RPC errors and server requests; no untrusted values in diagnostic constructors | PASS |
| D3a / handoff 1,3: preserve denial, all-false review, fixed launch, identities, cleanup and no-work behavior | unchanged protected source/data bindings; all original 123 tests plus ten diagnostic tests; source checks fail closed; actual local process and journal tests | PASS |
| D3b / handoff 3: regression, negative paths, format, Clippy, full first-party coverage and both floors | final attempts listed below, all bound to final manifest | PASS |
| D4 / current user: independent offline QA handoff and exact readback | qa-handoff.md, final-readback.json, artifact-index.json | Prepared; independent QA NOT_RUN |
| Deferred / handoff 4,5 | fresh native fixture/request/review/inventory digests, separate single no-work launch selection, then use observed predicate to classify issue | NOT_RUN; requires separate selection after independent QA PASS |

Changed/added package files (nine existing files, two new files):

{changed}

No policy, source/executable identity record, Cargo manifest/lock, request/review predicate, baseline fixture, journal schema, operational installation, credential setting, startup setting or qualification threshold was changed. Final pre-spawn ordering and terminal cleanup/error mapping remain intact. The diagnostic label correction RC-01 does not change result strings.

## Exact validation

All commands ran from `{PACKAGE}` using `C:\\Users\\bryan\\.cargo\\bin\\cargo.exe`. Attempts record scoped CARGO_TARGET_DIR, per-attempt CARGO_LLVM_COV_TARGET_DIR and WF_TEST_EVIDENCE; all other environment variables were inherited, and no credential values were collected or changed. The final normal and coverage campaigns used separate targets/fixtures and overlapped; both completed without failures.

| Attempt | Exact Cargo command | Exit | Elapsed |
| --- | --- | ---: | ---: |
{rows}

- Required complete suite: **133/133 (100%)**, including **40/40 unit tests**, original WF-01..WF-20 and subfixtures, offline NI/SI cases, F-01/F-02 and ten added diagnostic tests. Zero failed/errored/skipped/ignored/unexecuted required tests in the final candidate campaign. The instrumented campaign independently executed the same 133/133; it does not double the denominator.
- Full first-party executed-line coverage: **{coverage['covered']}/{coverage['count']} = {percentage}%**, floor 95%. All 13 src/*.rs files are accounted for, lib.rs 0/0; zero first-party exclusions. Raw final-coverage.json and final-coverage-analysis.json bind each file/count.
- Branch coverage: **NOT_RUN**; no branch floor was selected. Documentation tests: command passed with **0 discovered**, not invented documentation coverage.
- Red/Green: attempts 01/03 demonstrate initial absent diagnostics then the corrected exact-count Green; 16/17 demonstrate the misleading generic RPC label then its correction. Refactor was rustfmt only; current all-target campaigns reran affected code. Initial 02 and 05 fixture/oracle mistakes remain documented in review-notes.md, not concealed as product defects or successful Red results.
- Final code/test review found no ignored/should_panic/mock framework/coverage-suppression additions. Config/identity/launch predicate comparison and literal output oracles support preservation; this is developer review, not independent QA.

## Limits and remaining work

Independent offline QA must use fresh, disjoint evidence and assess the final frozen bytes. Native installed-profile behavior, Pro authentication, gpt-6-astra/high availability, hooks/plugins/apps/MCP/network isolation and custom-provider runtime behavior remain unqualified. WN-01/WN-02 remain 0/2 NOT_RUN here. Local synthetic peers are not Codex trials. Accounting-query OS failure is handled with null counts/query_failed but was not forcibly induced; private source-boundary tests do not claim end-to-end native runner execution. No authoritative framework decision was requested or issued.

Only after independent offline QA PASS may a separate task prepare exact fresh fixture/request/all-false review/inventory digests and select one bounded no-work native diagnostic launch. Refresh source bindings after any host permission change. Preserve each attempt; dispatch no thread/turn and generate no true operator findings. Any resulting repair, policy/contract amendment or operational change needs its own selection.

Output destination is the original context-selected `{ROOT}`. Final-readback.json verifies the promised files at this root, 58/58 current/snapshot candidate bindings, all bound input/historical evidence files, and unchanged fixed policy/identity/request sources. Artifact-index.json supplies external report bindings without a self-hash. These Python records summarize observations only; they grant no mutation, phase or framework acceptance authority.
''')

md('qa-handoff.md',f'''# Independent offline QA handoff

Select only independent offline QA of the bounded diagnostic changes in `{PACKAGE}` on native Windows x64. This is a handoff, not a QA execution or launch authorization.

Candidate: `{ROOT / 'candidate-v2-manifest.json'}`, SHA256 `{candidate_sha}`; exact bytes in candidate-v2-snapshot. Preserve this 58-file candidate. Read the original selected handoff at `{REPO / 'docs/plan/framework-worker-native-continuation/20260916T034357Z-source-identity/native-diagnostic-handoff.md'}`, applicable AGENTS.md, diagnostic-contract.md, delivery.md, review-notes.md and the four worker companion contracts in input-bindings.json. Baseline and both prior diagnostic snapshots/evidence remain in place.

Use the QA skill in a new independent session; write a fresh disjoint QA root. Do not modify this candidate or prior evidence. Verify manifests and tool/platform identity before tests. Developer results are context only: final 133/133 tests and {coverage['covered']}/{coverage['count']} executed lines ({percentage}%). Framework acceptance NOT_EVALUATED.

Required QA scope:

1. Independently audit every changed production predicate against baseline. Verify no changes to fixed argv, identities, review/all-false behavior, launch limits, cleanup/cancellation/deadlines or dispatch authority. Preserve strict profile_unqualified/protocol_error and existing terminal codes.
2. Independently author negative stimuli/oracles that distinguish post-spawn source review, initialize/config RPC process-count checks and config validation. Confirm total and active come from the same guard query and exited children remain counted. Include absent/malformed/unknown/active config, exact session-layer keys and cardinality, origin/source coverage and first-failure ordering.
3. Verify closed field sets and privacy using unique canaries in unknown nested config/layer/origin/server-error fields. Ensure neither success nor denial diagnostics retain them; no unknown value supplies a diagnostic label. Review the bounded other_rpc_failure fallback without interpreting it as a transport cause.
4. Demonstrate that diagnostics cannot authorize work, create operator findings or bypass the all-false review rejection for run. Audit public runner wiring as well as private test seams. Check evidence-write failure precedence, cancellation, deadlines, process cleanup and no thread/turn in synthetic preflight traces. No OS accounting-query failure was induced in development; assess that error projection independently where feasible.
5. Run the full original-plus-added 133-case Rust inventory with all subfixtures, negative/recovery/F-01/F-02 tests, format, Clippy -D warnings, build, docs and full first-party executed-line coverage. Denominator: every executable line under src/ (13 files including lib.rs 0/0), no first-party exclusions. Require both >=95% floors and every mandatory invariant; no skips counted as passes. Run actual tests, not just --list. Keep branch coverage separately reported.
6. Audit test integrity and sensitivity. Test helpers generate local synthetic peers only. Preserve failed attempts; distinguish fixture/oracle/setup failures from product failures. Do not overwrite/reuse native evidence or count retries twice. Read back final candidate/input hashes before issuing a scoped QA result.

Useful commands are listed exactly in delivery.md; use QA-owned target/coverage/evidence directories. Build --bins before a standalone --lib run, because private process tests require the built protocol-peer.exe beside the test target. The all-target campaign builds those peers itself. Allow the production 120-second WF-16 watchdog plus suite overhead. The developer recorder is optional evidence tooling, not framework authority.

Prohibitions: no native Codex preflight/trial, installed-profile source collection, installed configuration/cache/skill changes, alternate CODEX_HOME, login, credential edits, junction refresh, authority provisioning, predicate relaxation, or true operator findings. No WN-01/WN-02 credit from peers.

After independent offline QA PASS, return a separately selected native-diagnostic preparation/launch handoff. Do not launch as part of this QA task. The next selection must bind fresh exact fixture/request/all-false review/inventory digests, refresh after host permission changes, and authorize one bounded no-work attempt with no thread/turn. The resulting predicate decides defect versus prerequisite versus contract gap; no allowlist relaxation is preselected.
''')

md('checkpoint.md',f'''# Development delivery checkpoint

Time: {now}. Selected project/evidence destination remain exactly those in context.md. Candidate-v2 manifest SHA256 {candidate_sha}; 58 files read back and identical. Bounded diagnostic development, Red/Green/refactor, final regression/static/build/coverage checks and independent QA handoff are complete. Initial candidate and all failed attempts remain preserved.

Final campaign results: 133/133 complete suite, 40/40 units, {coverage['covered']}/{coverage['count']} executed lines ({percentage}%); branch coverage NOT_RUN. Independent QA NOT_RUN, native diagnostic launch NOT_RUN, WN-01/WN-02 NOT_RUN, framework acceptance NOT_EVALUATED.

All recorded build/test/coverage subprocess receipts are terminal. No native Codex process was started. Next safe action is a separately selected independent offline QA session using qa-handoff.md. Reverify current source/spec/tool and path identities before resuming; do not restore snapshots over current source or rerun a native attempt. After QA PASS, select a bounded native diagnostic launch separately. This handoff grants no launch or operational authority.
''')

required = ['context.md','diagnostic-contract.md','diagnostic-contract-initial.md','input-bindings.json',
            'baseline-manifest.json','baseline-comparison.json','candidate-v2-manifest.json',
            'final-candidate.diff','executions.jsonl','final-test-inventory.json',
            'final-coverage.json','final-coverage-analysis.json','review-notes.md',
            'delivery.md','qa-handoff.md','checkpoint.md']
readback = {'at':now,'selected_evidence_value':str(ROOT),'resolved_evidence_root':str(ROOT),
            'candidate_files_checked':len(candidate),'candidate_manifest_sha256':candidate_sha,
            'input_and_historical_files_checked':len(bindings),'historical_native_files_checked':91,
            'changed_paths':inventory['changed_files'],'all_input_hashes_unchanged':True,
            'outputs':[{'required_path':str(ROOT/name),'actual_path':str((ROOT/name).resolve()),
                        'sha256':digest(ROOT/name),'bytes':(ROOT/name).stat().st_size} for name in required],
            'executable':{'path':str(exe),'sha256':exe_sha,'bytes':exe.stat().st_size},
            'source_manifests_agree':candidate == manifest(),'framework_acceptance':'NOT_EVALUATED'}
write(ROOT/'final-readback.json',readback)
paths = [p for p in ROOT.iterdir() if p.is_file()]
for child in (ROOT/'attempts').iterdir():
    paths.extend(p for p in child.iterdir() if p.is_file())
for snapshot in ['baseline-snapshot','candidate-snapshot','candidate-v2-snapshot']:
    paths.extend(p for p in (ROOT/snapshot).rglob('*') if p.is_file())
write(ROOT/'artifact-index.json', {'scope':'Top-level artifacts, attempt receipts/streams/manifests and exact source snapshots; retained test fixtures and build outputs excluded except executable binding in final-readback.',
      'entries':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(paths)]})
print(json.dumps({'candidate_sha256':candidate_sha,'coverage':percentage,'candidate_files':len(candidate),
                  'bound_inputs':len(bindings),'handoff':str(ROOT/'qa-handoff.md'),'readback_sha256':digest(ROOT/'final-readback.json')}))
