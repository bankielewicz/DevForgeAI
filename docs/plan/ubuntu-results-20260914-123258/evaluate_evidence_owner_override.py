"""Evaluate supplied artifacts; does not issue protected framework acceptance."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import tarfile

base = Path(__file__).resolve().parent
root = base.parents[2]
raw = base / 'manual-index-20260914T162437-7915'
out = base / ('evaluation-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
out.mkdir()
sha = lambda b: hashlib.sha256(b).hexdigest()
def one(pattern):
    paths = list(raw.glob(pattern))
    assert len(paths) == 1, (pattern, paths)
    return paths[0]
def read(pattern):
    return one(pattern).read_text(encoding='utf-8')

inventory = [{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(raw.iterdir()) if p.is_file()]
attempts = []
for p in sorted(raw.glob('*.command.txt')):
    prefix = p.name[:-len('.command.txt')]
    parts = {suffix:raw/(prefix+'.'+suffix+'.txt') for suffix in ['stdout','stderr','exit','cwd']}
    assert all(p.is_file() for p in parts.values()), prefix
    text = parts['stdout'].read_text()
    cases = re.findall(r'^test (\S+) \.\.\. (ok|FAILED|ignored)', text, re.M)
    attempts.append({'id':prefix,'command':p.read_text(),'cwd':parts['cwd'].read_text().strip(),
                     'exit':int(parts['exit'].read_text()),'cases':[{'name':n,'result':r} for n,r in cases]})
regression = next(a for a in attempts if a['id'].startswith('regression-'))
coverage_attempt = next(a for a in attempts if a['id'].startswith('coverage-') and not a['id'].startswith('coverage-tool-'))
assert len(regression['cases']) == len({c['name'] for c in regression['cases']}) == 36
assert all(c['result']=='ok' for c in regression['cases'])
assert {c['name'] for c in coverage_attempt['cases']} == {c['name'] for c in regression['cases']}
assert all(c['result']=='ok' for c in coverage_attempt['cases'])

manifest = {}
for line in read('candidate-after-build-*.stdout.txt').splitlines():
    match = re.fullmatch(r'([a-f0-9]{64})  (.+)', line)
    assert match, line
    assert match[2] not in manifest
    manifest[match[2]] = match[1]
with tarfile.open(root/'devforgeai-ubuntu-source-20260914.tar.gz', 'r:gz') as tar:
    bundled = {m.name[len('DevForgeAI/devforgeai/'):]:sha(tar.extractfile(m).read())
               for m in tar.getmembers() if m.isfile() and m.name.startswith('DevForgeAI/devforgeai/')}
assert manifest == bundled, 'Submitted source manifest differs from packaged source'
local_drift = [name for name,digest in manifest.items() if sha((root/'devforgeai'/name).read_bytes()) != digest]
assert not local_drift, local_drift
assert len(read('candidate-before.sha256').splitlines()) == 3
integrity = read('bundle-integrity-*.stdout.txt').splitlines()
assert len(integrity) == 365 and all(line.endswith(': OK') for line in integrity)

coverage = json.loads((raw/'coverage.json').read_text())['data'][0]
lines = coverage['totals']['lines']
assert lines['covered'] == 2066 and lines['count'] == 2786
assert all('/devforgeai/src/' in f['filename'] for f in coverage['files'])
assert sum(f['summary']['lines']['count'] for f in coverage['files']) == lines['count']
files = [{'path':f['filename'].split('/devforgeai/')[1], **f['summary']['lines']} for f in coverage['files']]
bench = [json.loads(line) for line in read('benchmark-2026*.stdout.txt').splitlines() if line.startswith('{')]
assert len(bench) == 4 and len(bench[-1]['repetitions']) == 3
assert bench[-1]['fixture_manifest_sha256'] == sha((raw/'benchmark-fixture-manifest.json').read_bytes())
assert bench[-1]['files']==10000 and bench[-1]['bytes']==104857600
assert all(b['coverage']['text_count']==10000 and b['coverage']['structural_count']==8000 for b in bench[:3])
summary = {'evaluation_kind':'supplied_evidence_review','authority':'evidence_only_NOT_EVALUATED',
    'platform':read('os-*.stdout.txt'),'kernel':read('host-*.stdout.txt'),
    'rustc':read('rustc-*.stdout.txt'),'coverage_tool':read('coverage-tool-*.stdout.txt'),
    'source_manifest_files':len(manifest),'source_matches_bundle_and_local':'PASS',
    'bundle_integrity_reported_ok':len(integrity),'initial_manifest':'INCOMPLETE: 3 entries; retained',
    'full_manifest_capture':'After build and initial DS-A01; before later regression/coverage/benchmark. No final source manifest supplied.',
    'regression_raw':{'passed':36,'failed':0,'ignored':0,'percent':100},
    'product_evidence_count':35,'excluded_setup_case':'rust_test_harness_executes',
    'required_specification_case_pass_rate':'NOT_ESTABLISHED: full required scenario denominator incomplete',
    'line_coverage':lines,'line_coverage_result':'FAIL','branch_coverage':'NOT_RUN',
    'per_file_coverage':files,'attempts':attempts,'benchmark':bench[-1],
    'overall_evidence_disposition':'FAIL: coverage below mandatory floor; further acceptance evidence incomplete',
    'formal_independent_QA':'PENDING; this is review of supplied execution artifacts',
    'evaluation_specification_sha256':'52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4',
    'original_bundle_specification_sha256':'b1886c7bf237f823b2f83a8b37c1288ca26880ecfc58771568b38750e8855897',
    'required_standalone_target':'Ubuntu 26.04.1 LTS x64','target_override':'Repository owner, 2026-09-14; supersedes standalone Ubuntu 24.04 only','manual_playbook_export':'NOT_SUPPLIED',
    'received_artifact_manifest':inventory}
(out/'evaluation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
report = f'''# Standalone Ubuntu evidence evaluation

Result: **FAIL against the coverage requirement; full qualification remains incomplete.** This is an evidence review, not protected Rust-framework acceptance or a completed independent anti-gaming audit.

The received files establish execution on Ubuntu 26.04.1 LTS, VMware host me-VMware-Virtual-Platform, Linux 7.0.0-31-generic x86_64. Rust 1.93.1 uses LLVM 21.1.8; cargo-llvm-cov is 0.9.1. Standalone Ubuntu is now tested at this release. The repository owner explicitly replaced the standalone Ubuntu 24.04 target with Ubuntu 26.04.1 LTS on 2026-09-14. This campaign now matches the required standalone target. Windows and Ubuntu 24.04 WSL2 requirements remain unchanged.

| Check | Result |
| --- | --- |
| Source identity | All {len(manifest)} files in the corrected manifest match the packaged candidate and current local application bytes. Bundle check reports 365 files OK. |
| Release build, formatting, Clippy | PASS: each command exited 0. |
| Regression | 36/36 raw cases passed, none failed or ignored. Includes one trivial setup-only assertion; 35 non-setup cases passed. |
| Coverage run tests | Same 36 unique cases passed; repeated execution adds no required-case credit. |
| Executed-line coverage | FAIL: 2066/2786 = {lines['percent']}%; required >=95%. Coverage command exited 1 after successfully writing its report. |
| Branch coverage | NOT_RUN: branch instrumentation absent. Zero branch entries do not constitute measured coverage. |
| Detailed required-case pass rate | NOT_ESTABLISHED. Implemented regression success does not cover all required acceptance subchecks. |
| Benchmark | Three release repetitions completed, fixture digest verified; external time/RSS observations retained. |
| Manual scenarios / formal independent QA | INCOMPLETE / PENDING. No exported playbook observations or complete manual evidence supplied. |

## Coverage remediation evidence

Denominator: 13 first-party executable source files compiled for Linux, including the Linux unsupported-tray entry path. Tests, examples, fixtures and dependencies were excluded by the recorded command; no further source exclusions were introduced in this review.

| Source | Covered / executable lines | Percent |
| --- | ---: | ---: |
'''
for f in files:
    report += f"| {f['path']} | {f['covered']}/{f['count']} | {f['percent']}% |\n"
report += '''
The CLI has 339 uncovered lines, service 127, platform 66, index 60 and shared tray logic 59. These are priorities for requirement-based tests and implementation review, not permission to exclude code or add vacuous assertions.

## Test integrity and scenario limits

The source still contains tests/harness.rs with only size_of::<u32>() == 4. It is setup evidence only and must receive no product-required-case credit. A scoped search found no mock decorators or coverage-bypass attributes in application source/tests/examples. This does not finish the required anti-gaming audit or prove every oracle is independent. The two Windows-only ignored WSL tests are not compiled on this Linux target and their scenarios receive no standalone Linux pass credit.

DS-A01 was run twice; both attempts remain retained, counted once when considering its supporting test. DS-A07 and DS-A15 reuse the protocol tests; DS-A02 and DS-A17 reuse one lifecycle test. Those repetitions are not additional unique passing cases. Every copied test command executed at least one test, but focused support does not qualify the whole scenario. In particular DS-A04 does not prove an OS crash at commit; DS-A07 lacks cross-account denial; DS-A11 lacks overflow and full convergence evidence; DS-A16's portable preferences test does not prove Linux systemd installation; DS-A18's fixture test alone is not a benchmark, although a separate benchmark was subsequently run. DS-A05 and DS-A06 are Windows-controller scenarios, NOT_APPLICABLE for this standalone campaign.

The user encountered two playbook usability defects: a missing rg produced a partial manifest without stopping preparation, and copy buttons supplied explanatory prose as executable commands for Windows-only scenarios. Preserve these as playbook defects; the resulting shell errors are not product runtime failures. They were shown in conversation, not captured by run_case. The initial 3-file manifest is retained. The corrected manifest and bundle verification were recorded after build/initial DS-A01 but before later tests. No final after-campaign source manifest or remote evidence-file checksum inventory was supplied; this review hashes received bytes and does not claim end-to-end remote attestation.

## Benchmark observations

| Repetition | Cold ms | Warm ms | 100-file edit ms | Status p95 microseconds |
| --- | ---: | ---: | ---: | ---: |
'''
for b in bench[:3]:
    report += f"| {b['repetition']} | {b['cold_ms']} | {b['warm_ms']} | {b['edit_100_ms']} | {b['status_p95_us']} |\n"
report += '''
Fixture: 10,000 files / 104,857,600 bytes, seed 20260913, four concurrent management-status readers, 10,000 text and 8,000 structural files in each repetition. GNU time reports 38.39 seconds user CPU, 14.49 seconds system CPU, 54.44 seconds wall time and 52,988 KiB maximum resident set size. The example's internal NOT_MEASURED resource field is supplemented by these external measurements. CPU model, total assigned VM RAM and sustained idle CPU are not supplied. This is management-status concurrency, not the companion code-query workload. It does not fully qualify DS-A18 or establish a cross-platform speed comparison.

## Disposition

Retain all submitted artifacts unchanged. Return the candidate for coverage and test-quality remediation; review missing behavior against the selected specification through red/green/refactor and fresh per-platform QA. No rerun of this unchanged candidate can be presumed to satisfy 95%. Apply the owner-authorized standalone Ubuntu 26.04.1 target; no separate standalone Ubuntu 24.04 run is required for this revised contract. The per-attempt ledger and received-file SHA-256 inventory are in evaluation.json.
'''
(out/'evaluation.md').write_text(report,encoding='utf-8')
assert all(sha((raw/e['path']).read_bytes())==e['sha256'] for e in inventory)
print(json.dumps({'report':str(out/'evaluation.md'),'details':str(out/'evaluation.json'),
                  'source_files':len(manifest),'attempts':len(attempts),'received_files':len(inventory),
                  'coverage':lines,'result':'FAIL','raw_evidence_unchanged':True},indent=2))
