"""Read actual artifacts and retain delivery/traceability. Evidence only."""
import datetime, hashlib, json, pathlib, re
from html.parser import HTMLParser
RUN=pathlib.Path(__file__).resolve().parent
ROOT=RUN.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,text): (RUN/name).write_text(text,encoding='utf-8')
inputs=json.loads((RUN/'inputs.json').read_text())
for entry in inputs:
    assert digest(pathlib.Path(entry['path']))==entry['sha256'],f"Input drift: {entry['path']}"
candidate=RUN/'attempts/085-windows-final-coverage/candidate.json'
for entry in json.loads(candidate.read_text()):
    assert digest(ROOT/entry['path'])==entry['sha256'],f"Candidate drift: {entry['path']}"
grammar=json.loads((ROOT/'devforgeai/grammar-manifest.json').read_text())
for entry in grammar['grammars']:assert digest(ROOT/'devforgeai'/entry['license_path'])==entry['sha256']
for entry in grammar['queries']:assert digest(ROOT/'devforgeai'/entry['path'])==entry['sha256']
assert digest(ROOT/'devforgeai'/grammar['lockfile'])==grammar['lockfile_sha256']
page=ROOT/'docs/plan/index-service-validation-playbook.html'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
parser=Links();parser.feed(page.read_text(encoding='utf-8'))
assert len(parser.ids)==len(set(parser.ids))
for link in parser.links:
    if not link.startswith(('https:','http:','#')):assert (page.parent/link).is_file(),link
cases=json.loads(re.search(r'<script id="caseData" type="application/json">(.*?)</script>',page.read_text(encoding='utf-8'),re.S)[1])
assert len(cases)==19
for case in cases:
    suite=case['suite'].split()
    if suite[0]!='ALL':
        source=ROOT/'devforgeai/tests'/f'{suite[0]}.rs'
        assert source.is_file(),str(source)
        if len(suite)>1:assert f'fn {suite[1]}(' in source.read_text(),case['id']
windows=json.loads((RUN/'windows-coverage-004.json').read_text())['data'][0]['totals']['lines']
wsl=json.loads((RUN/'wsl-coverage-002.json').read_text())['data'][0]['totals']['lines']
qualified='DEVFORGEAI-INDEX-SERVICE-001'
implementation={
1:'src/bin, lib.rs; compiled component entry points',2:'service.rs, storage.rs; staged records and shared client',3:'platform.rs, host.rs, tray.rs; platform adapters',4:'platform.rs, host.rs; private ownership and native IPC',5:'cli.rs; WSL argument-vector relay',6:'cli.rs, tray.rs; running-distribution inventory and poll policy',7:'platform.rs, source_file.rs, index.rs; canonical roots and handle-based capture',8:'service.rs; indexing/coverage/freshness and activity fields',9:'cli.rs, host.rs; detached Start and foreground run',10:'service.rs; pause writer guard and Resume reconciliation',11:'service.rs, host.rs, cli.rs; cancellation, flush and stop confirmation',12:'service.rs; job conflicts, cancellation and retention',13:'service.rs; registration/configuration and cache-only removal',14:'index.rs; exclusion and encoding rules',15:'index.rs, queries; bundled language adapters and source ranges',16:'service.rs; watch coalescing, debounce, root-failure backoff',17:'index.rs; two workers, bounded admission and parser cancellation',18:'storage.rs; SQLite FTS5 and schema refusal',19:'storage.rs; immutable publication and two-generation retention',20:'service.rs; counts, coverage, freshness and diagnostics',21:'service.rs; logs and explicit corrupt-cache quarantine',22:'protocol.rs, host.rs, client.rs; strict typed framing',23:'cli.rs, protocol.rs; management commands',24:'protocol.rs, cli.rs; envelopes and exit mapping',25:'tray_windows.rs; native asynchronous management UI',26:'tray.rs, tray_windows.rs, packaging; opt-in startup and exit behavior'}
trace='# Requirement traceability at manual handoff\n\nAll selected source-qualified requirements are accounted for. Implemented source and executed support are listed below; full-platform qualification remains incomplete. No editable note is framework acceptance.\n\n'
trace+='| Requirement | Implemented artifact (under devforgeai/) | Acceptance evidence / remaining qualification | State |\n| --- | --- | --- | --- |\n'
for number in range(1,27):
    req=f'DS-{number:03}'
    mapped=[c['id'] for c in cases if req in c['requirements']]
    trace+=f'| {qualified}/{req} | {implementation[number]} | '+', '.join(mapped)+f'; attempts 085/086 contain current focused tests; see playbook for missing subchecks | PARTIAL |\n'
trace+='\n| Acceptance scenario | Current evidence and limit | Whole required-platform result |\n| --- | --- | --- |\n'
for case in cases:
    trace+=f"| {qualified}/{case['id']} | {case['gap']} See [playbook](../../index-service-validation-playbook.html), attempts 085/086 and [platform status](platform-status.md). | {'FAIL: coverage below floor' if case['id']=='DS-A19' else 'NOT_RUN: complete required-platform scenario remains unqualified'} |\n"
trace+='\n| Additional obligation | Evidence/result |\n| --- | --- |\n| Section 1.4 engineering | Retained attempts 001–089; Windows/WSL line coverage FAIL (<95%); full required-case matrix incomplete. |\n| Section 9 benchmark | Attempt 069: three measured Windows repetitions plus CPU/RAM samples; query/idle/per-platform gaps remain. |\n| Section 10 delivery | Source, Cargo.lock, grammars/licenses, schemas/examples, fixtures, unit example, user docs and native release builds 087/089 delivered as a development candidate. |\n| Section 10 evidence destination | Original literal context-bound run root retained; readback.json verifies promised files and input/candidate hashes. |\n\n26 requirements, 19 scenarios and 4 unnumbered obligations are accounted for. None is promoted to whole-product acceptance. The companion query extension, installation, operational skills and protected enforcement remain outside the selected implementation changes.\n'
write('traceability.md',trace)
with (RUN/'slices.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## Executed lineage and handoff\n\nS01: protocol red 002, green 003. S02: platform red 011, native green 013; IPC red 017, native green 019. S03: capture red 006, green 007; worker/cancellation refinements 028–031; directory-link defect red 058, green 059/060. S04: storage red 008, green 010; service red 014, green 016; Resume defect 027→029; debounce 042→043; root failure 068/070→071; negative/reader QA 073. S05: CLI red 020, green 021; process failures 035/036/038 and fixes 039/040. S06: tray red 022, green 024; native harness corrections 050–053, native pass 054; readable status 061→062; WSL bridge 066. S07: final candidate tests/coverage 085/086, Windows Clippy 088, native release builds 087/089, WSL final checks 089; full qualification remains PARTIAL.\n\nThe user requested the HTML manual playbook and explicit WSL-tested/standalone-Linux-untested note. Playbook logic defect 075→076 is retained; live browser preview was policy-blocked. Further platform/manual results should be evaluated against the exact submitted candidate.\n')
checkpoint=f'''# Manual qualification handoff checkpoint

User-selected implementation: docs/plan/devforgeai-index-service-mvp-spec.md. Latest steering requested an offline HTML playbook and a note that WSL is tested while standalone Linux is untested. The user proposed Ubuntu 26.04.1 LTS; it is supported as an explicitly labeled compatibility campaign, while the specified standalone Ubuntu 24.04 target remains NOT_RUN. The selected specification was not rewritten.

Overall application development status: PARTIAL. Source foundation, CLI, native IPC, storage/indexing, WSL bridge and native tray are implemented, but mandatory coverage and scenario qualification remain incomplete. Candidate: attempts/085-windows-final-coverage/candidate.json, SHA-256 {digest(candidate)}. Attempts 085–089 bind the same candidate. Attempt 083 retained a new Rust 1.98 Clippy lint failure; the mechanical iterator refactor in 084 resolved it. Readback independently checks all manifest entries against current bytes.

Windows: 38/38 automated cases; {windows['covered']}/{windows['count']} executed lines ({windows['percent']}%). WSL: 36/36 automated cases; {wsl['covered']}/{wsl['count']} executed lines ({wsl['percent']}%). Both coverage commands exit 1 because neither meets 95%. Branch coverage NOT_RUN. Standalone Ubuntu 24.04 and 26.04.1 NOT_RUN. No installation/startup changes or operational skill edits were made.

Retained negative results include expected red failures, harness compile/setup errors, sandbox denials, an initial benchmark timeout, a lost benchmark stdout run, and corrected GUI text-reading assumptions. Exact commands, stream hashes and manifests remain in executions.jsonl/attempts. Successful retries do not erase them.

Delivered manual organizer: ../../index-service-validation-playbook.html. Platform summary: platform-status.md. Browser local-file policy denied preview; do not work around that restriction. Node unit/static checks passed, but browser visual/import/download interactions remain unperformed.

Unresolved implementation/qualification work: coverage below 95%; full cross-account IPC denials, Windows path-replacement/junction stress, installed-stopped WSL and mixed-environment tray scenarios, controlled crash/publication and watcher overflow injection, sustained resource/idle and per-platform benchmarks, schema/runtime matrix, native startup/systemd scenarios. Additional reviewed risks to probe: WSL canonical aliases to mounted Windows roots; bridge stdin deadline/envelope validation; oversized-response handling; root/watcher diagnostics completeness; effective file accounting; log retention/concurrent rotation; complete adapter constructs. Do not treat focused tests as proof these gaps are closed.

Next safe action: evaluate the user's exported playbook JSON together with exact source/tool/platform manifests and raw evidence, then reproduce and repair failures through TDD. Independent code/coverage work may resume from the current candidate after checking input/source drift. Do not restore old candidates over newer work, install components to simulate acceptance, or merge WSL results into standalone Linux.
'''
checkpoint += '\nFormal QA is PENDING. QA must independently verify specification conformance, executed-line coverage >=95%, and the required unit-test pass rate >=95% per platform. Any mock decorator or test that games results is a QA failure. Reject vacuous assertions, fabricated outputs, weakened expectations, skipped required cases counted as passes, unjustified coverage exclusions and duplicate retry counts. Failed QA returns this candidate for remediation; the current coverage already fails both measured platforms.\n\nThe focused test-integrity review found a setup-only assertion in devforgeai/tests/harness.rs (size_of::<u32>() == 4). It supplies no product evidence and receives no required-case credit. Raw runner totals of 38 Windows / 36 WSL include it; removing that setup count leaves 37 / 35 executed non-setup cases, not a complete required-case denominator. The absent-distribution WSL probe does not establish installed-stopped behavior. No mock decorator was found in the scoped Rust source/tests/examples scan. This scan is not a completed anti-gaming audit. The HTML Node checker uses minimal DOM/storage substitutes and supplies only helper logic evidence, never native browser or product qualification.\n'
write('checkpoint-manual-handoff.md',checkpoint)
delivery=f'''# Development delivery

Selected scope: application implementation from DEVFORGEAI-INDEX-SERVICE-001, plus the user-requested offline HTML manual-validation playbook. Overall application status: **PARTIAL**. The playbook and platform note are delivered; full product/platform qualification is not complete.

Source: `C:\\Projects\\DevForgeAI\\devforgeai`. Candidate manifest: [085 candidate](attempts/085-windows-final-coverage/candidate.json), SHA-256 `{digest(candidate)}`. No Git metadata is present. Source input hashes remain unchanged. All 26 requirements, 19 scenarios and four additional obligations are accounted for in [traceability.md](traceability.md).

Actual outputs: Rust CLI, daemon, shared protocol/client/index/storage/platform modules and native Windows tray; Cargo.lock; bundled queries and five license files with grammar manifest; request/response schemas and examples; synthetic tests and deterministic benchmark fixture; README and optional systemd unit example. Windows release binaries are under `devforgeai/target/release/`; Linux binaries were built inside WSL at `/tmp/devforgeai-index-20260914T0727264112301Z/release/`. They are development artifacts, not installed or fully qualified releases.

User-facing handoff: [HTML playbook](../../index-service-validation-playbook.html), [platform note](platform-status.md), [continuation checkpoint](checkpoint-manual-handoff.md). The HTML is offline, covers all 19 scenarios, separates platform/release results, retains attempt history and exports JSON evidence references. Ubuntu 26.04.1 is an additional compatibility target; standalone Ubuntu 24.04 remains untested.

| Check | Actual result |
| --- | --- |
| Windows regression / native smoke | 38/38 implemented cases PASS (085), including native tray and isolated WSL bridge. This is not all required acceptance subchecks. |
| WSL regression | 36/36 implemented cases PASS (086). Standalone Linux NOT_RUN. |
| Windows coverage | FAIL: {windows['covered']}/{windows['count']} = {windows['percent']}%, required >=95%. |
| WSL coverage | FAIL: {wsl['covered']}/{wsl['count']} = {wsl['percent']}%, required >=95%. |
| Branch coverage | NOT_RUN; no branch instrumentation. |
| Formatting / Clippy | Windows Clippy PASS (088); source formatted (084); WSL final format/Clippy and binary hashes PASS (089). |
| Native release builds | Windows PASS (087); WSL Linux CLI/daemon PASS (089). No standalone Ubuntu execution implied. |
| Windows benchmark | Three repetitions completed (069); baseline and limitations in platform-status.md. |
| HTML logic/static | Node checks PASS (076 and final readback); links/IDs/command-reference/input-manifest checks in readback.json. |
| HTML browser preview | NOT_RUN: browser security policy blocked local file access. |
| Startup / installation / full native scenario matrix | NOT_RUN or incomplete as detailed per playbook card. |

The raw suite pass rates are 100% for the implemented suites, with each case counted once and zero failures/ignored cases in 085/086. These are not complete required-scenario pass rates. No scenario is claimed fully qualified across all required hosts while standalone Linux and other mandatory subchecks are missing. Numeric coverage floors fail independently. Earlier failures, timeouts and corrections remain in the append-only execution receipts.

Original evidence selection: `docs/plan/index-service-implementation/20260914T0727264112301Z`; resolved root `C:\\Projects\\DevForgeAI\\docs\\plan\\index-service-implementation\\20260914T0727264112301Z`. The HTML destination was bound before first write in context.md. [readback.json](readback.json) lists each required actual path, current SHA-256 and presence observation. Old evidence is retained.

External protected Rust-framework acceptance: **NOT_EVALUATED**. This index service and Python/HTML evidence helpers cannot issue that decision. No operational skill, startup configuration or installation was changed. Remaining work and next safe action are in the checkpoint; evaluate the user's returned evidence before making further qualification claims.
'''
delivery += '\nFormal QA is PENDING. QA must independently verify specification conformance, executed-line coverage >=95%, and the required unit-test pass rate >=95% per platform. Any mock decorator or test that games results is a QA failure. Reject vacuous assertions, fabricated outputs, weakened expectations, skipped required cases counted as passes, unjustified coverage exclusions and duplicate retry counts. Failed QA returns this candidate for remediation; the current coverage already fails both measured platforms.\n\nThe focused test-integrity review found a setup-only assertion in devforgeai/tests/harness.rs (size_of::<u32>() == 4). It supplies no product evidence and receives no required-case credit. Raw runner totals of 38 Windows / 36 WSL include it; removing that setup count leaves 37 / 35 executed non-setup cases, not a complete required-case denominator. The absent-distribution WSL probe does not establish installed-stopped behavior. No mock decorator was found in the scoped Rust source/tests/examples scan. This scan is not a completed anti-gaming audit. The HTML Node checker uses minimal DOM/storage substitutes and supplies only helper logic evidence, never native browser or product qualification.\n'
write('delivery.md',delivery)
expected=[RUN/n for n in ['context.md','inputs.json','traceability.md','slices.md','executions.jsonl','checkpoint-manual-handoff.md','delivery.md','platform-status.md','windows-coverage-004.json','wsl-coverage-002.json','build_playbook.py','check_playbook.cjs','finalize_notes.py','test-integrity-review.md','attempts/085-windows-final-coverage/candidate.json','attempts/089-wsl-final-checks/stdout.txt']]+[page]
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'docs/plan/index-service-implementation/20260914T0727264112301Z','resolved_root':str(RUN),'input_hash_readback':'PASS','candidate_hash_readback':'PASS','grammar_license_query_lock_hashes':'PASS','html_links_ids_test_references':'PASS','html_browser_visual':'NOT_RUN: browser URL policy blocked local file','outputs':[{'required_path':str(p),'actual_path':str(p.resolve()),'sha256':digest(p),'bytes':p.stat().st_size} for p in expected],'windows_binaries':[{'path':str(p),'sha256':digest(p)} for p in (ROOT/'devforgeai/target/release').glob('devforgeai*.exe')]}
write('readback.json',json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
