import json
from pathlib import Path
RUN=Path(__file__).resolve().parent
final=RUN/'final-combined'
grade=json.loads((final/'independent-grade.json').read_text())
report=json.loads((final/'coverage.json').read_text())
scope=json.loads((final/'scope.json').read_text())
lines=['# Windows skill-builder regression and coverage','',
'Final development-source Python regression: **318/318 required cases PASS (100%)**. All-source executed-line coverage: **2201/2299 = 95.73727707699%**. All eight shipped Python modules are measured, including the runtime asset; zero line exclusions. Branch coverage is reported separately below. This is executed maintenance evidence, not framework acceptance, installation, or native skill activation.','',
'## Source and execution','',
'The final three batches bind identical V2 package bytes, and each batch and combination verified source readback. `final-combined/scope.json` records every source hash. The authoring helper SHA-256 is `'+scope['source']['scripts/authoring.py']+'`.','',
'Native Windows; PowerShell launched `C:\\Program Files\\Python310\\python.exe` 3.10.11 with `-B -X utf8`; cwd `C:\\Projects\\DevForgeAI`, Windows C: filesystem. Existing coverage.py 7.9.0, PyYAML 6.0.2, jsonschema 4.24.0. No dependencies were installed.','',
'| Final batch | Required / passed | Wall seconds | Exit |','| --- | --- | --- | --- |']
for name in scope['inputs']:
    g=json.loads((RUN/name/'grade.json').read_text());p=json.loads((RUN/(name+'-process.json')).read_text())
    lines.append(f"| {name} | {g['required']} / {g['passed']} | {p['elapsed_seconds']:.3f} | {p['exit_code']} |")
lines += ['', 'Each batch had a 120-second ceiling. The case sets are disjoint, with no retries or inherited base-case duplicates added to the denominator. `final-combined/expected.json`, `results.jsonl`, and `independent-grade.json` bind the inventory, observed results, and independent reduction. `result.schema.json` validates each result row. No required cases failed, errored, skipped, or remained unexecuted in the final V2 collection.', '', '## Coverage denominator and missing lines','', '| Shipped module | Executed / statements | Missing executable lines |','| --- | --- | --- |']
for name,data in report['files'].items():
    s=data['summary'];missing=', '.join(map(str,data['missing_lines'])) or 'None'
    lines.append(f"| {name.replace(chr(92),'/')} | {s['covered_lines']} / {s['num_statements']} | {missing} |")
total=report['totals'];lines += ['',f"Branches: {total['covered_branches']}/{total['num_branches']} = {grade['branch_percent']:.11f}%. This separate measure does not replace the required executed-line floor.", '', '## Earlier attempts retained','',
'- qa-01, V1: 286 required cases, 262 passed. 105.844 seconds, no timeout. Coverage instrumentation changed direct-script import semantics; copied tests also initially lacked helper fixture search paths. Three retained assertions needed explicit adaptation for the newly earlier rejection boundary. These were harness/contract mismatches, not evidence of an unaffected product passing.',
'- qa-02, V1: 120.031-second collection timeout, incomplete coverage finalization. Most observed cases passed after instrumentation corrections. One real recovery-guidance defect remained: changed-origin rejection returned BLOCKED but omitted the required fresh-run instruction. Parent repaired that error message in V2. This failed assertion is retained as red evidence.',
'- qa-03-stage, V1: 30/30 focused cases passed in 15.735 seconds. This earlier source is not included in the final combined V2 coverage or pass denominator.',
'- Final V2 batches above re-execute every declared case against final source. No V1 coverage is included.','',
'## Test integrity and limits','',
'Retained historical tests and fixtures remain at their original paths; copied tests, source hashes and adaptations are recorded in retained-test-receipts.json, adaptations.md, each final batch test-snapshot/, scope.json, and retained-fixture-manifest.json. Fixtures are synthetic local trees. Assertions inspect real return values, destinations, byte preservation, stale-history rejection, schema/intake results, and publication readback. Existing Windows-only checks executed on Windows. The optional jsonschema dependency was available; the junction case executed instead of skipping.',
'Mocks inject explicit filesystem errors, capture limits, or competing-writer changes. They do not replace the acceptance oracle or produce canned passing authoring results. Runtime-original tests execute the actual shipped runtime asset, while the retained adaptive suite separately exercises copied runtime fixtures. No tests assert implementation source text. Diagnostic and output-format assertions supplement observable effects.',
'The coverage runner wraps genuine CLI execution with coverage_driver.py solely to preserve direct-script sys.path semantics under tracing. It records real command receipts and return codes. Executed-line coverage includes all first-party shipped Python files even when unimported; no uncovered module or line is omitted.',
'This report establishes Windows deterministic helper coverage and regression only. Linux coverage, native implicit activation, generated-skill outcomes and complete end-to-end workflow qualification are separate evidence owned by the parent task. Operational skill copies and source packages were not edited by this regression task.','']
(RUN/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
print(str(RUN/'REPORT.md'))
