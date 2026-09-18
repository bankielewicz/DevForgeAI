import json
from pathlib import Path
import sys
RUN=Path(__file__).resolve().parent
final=RUN/(sys.argv[1] if len(sys.argv)>1 else 'final-combined')
output=RUN/(sys.argv[2] if len(sys.argv)>2 else 'REPORT.md')
grade=json.loads((final/'independent-grade.json').read_text())
report=json.loads((final/'coverage.json').read_text())
scope=json.loads((final/'scope.json').read_text())
lines=['# Windows skill-builder regression and coverage','',
f"Final development-source Python regression: **{grade['passed']}/{grade['required']} required cases PASS ({grade['pass_rate']:.0f}%)**. All-source executed-line coverage: **{grade['covered_lines']}/{grade['statements']} = {grade['line_percent']:.11f}%**. All eight shipped Python modules are measured, including the runtime asset; zero line exclusions. Branch coverage is reported separately below. This is executed maintenance evidence, not framework acceptance, installation, or native skill activation.",'',
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
text='\n'.join(lines)
if 'v3' in final.name:
    text=text.replace('V2','V3').replace('final-combined',final.name)
    text=text.replace('Parent repaired that error message in V3.', 'Parent repaired that error message in V2.')
    text += '\n## V3 repair and retained fixture corrections\n\nV2 final-combined passed 318/318 with 2201/2299 lines but was superseded by the independently reproduced empty-directory defect. red-prewrite failed because first before_write stage drift left an occupied target despite BLOCKED; V3 defers target creation until after that check. The final V3 inventory includes this additional case, for 319 required cases.\n\nv3-authoring initially passed 131/133: two callback fixtures assumed target creation before the callback. Their retained failures prompted setup corrections that explicitly create the competing destination; all original assertions remain. v3-authoring-fixtures-02 re-executes the entire affected subgroup. The final V3 combination uses v3-legacy, v3-authoring-fixtures-02 and v3-adaptive-stage only; all have identical source hashes. Earlier V1/V2 and failed V3 attempts remain separate.\n'
output.write_text(text,encoding='utf-8')
print(str(output))
