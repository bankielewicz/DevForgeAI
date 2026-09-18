"""Final preservation and artifact-link checks; append evidence without replay."""
import json
import re
from pathlib import Path
from harness import RUN, ROOT, TARGET, LOADED, PRIOR, CHECKER, SPECS, EXPECTED, read, write, save, ref, sha, inventory, now

for name,p in [('target',TARGET),('loaded-evaluator',LOADED),('companion',ROOT/'src/agents/skills/skill-builder')]:
    actual=inventory(p)
    before=json.loads(read(RUN/'inputs'/f'{name}-before.json'))
    assert actual['files']==before['files'] and actual['excluded_boundaries']==before['excluded_boundaries']
for name,digest in SPECS.items(): assert sha(read(ROOT/'docs/plan'/name))==digest
prior=json.loads(read(RUN/'inputs/prior-selected-before.json'))
assert all(sha(read(Path(r['path'])))==r['sha256'] for r in prior)
assert inventory(RUN/'source')['package_digest']==EXPECTED
assert sha(read(ROOT/'AGENTS.md'))==sha(read(RUN/'inputs/AGENTS.md'))
assert sha(read(CHECKER))==json.loads(read(RUN/'inputs/checker-identity.json'))['sha256']

links=[]
for name in ('finding-validation-report.md','command-log.md'):
    for dest in re.findall(r'\]\(([^)]+)\)',read(RUN/name).decode()):
        if dest.startswith(('https://','http://')): continue
        path=RUN/dest.split('#',1)[0]
        assert path.exists(), (name,dest)
        links.append({'document':name,'target':dest,'exists':True})
save(RUN/'final-link-audit.json',{'local_links':links,'manual_citation_review':'Governing section 6/7 support duplicate/application reductions; section 3.2 supports protocol candidates and outside-fence resource parsing. Current anchors verified against unchanged target. F08 content checked, not just exit status. External CommonMark identity retained separately.'})

commands=[]
for d in sorted((RUN/'commands').iterdir()):
    if (d/'receipt.json').exists(): commands.append(json.loads(read(d/'receipt.json')))
save(RUN/'command-log-final.json',commands)
append=['\n## Final evidence-record verification\n']
for cid in ('LEGACY-RECORDS','ADAPTIVE-RECORDS'):
    rec=json.loads(read(RUN/'commands'/cid/'receipt.json'))
    assert rec['exit']==0 and not rec['timed_out']
    append += [f'### {cid}\n','```json',json.dumps(rec['argv']),'```',f"\nCwd: `{rec['cwd']}`. Start: {rec['start']}; end: {rec['end']}; elapsed: {rec['elapsed_seconds']:.3f}s; exit 0; no timeout.",f'[stdout](commands/{cid}/stdout.txt) · [stderr](commands/{cid}/stderr.txt) · [receipt](commands/{cid}/receipt.json)\n']
with (RUN/'command-log.md').open('ab') as f: f.write(('\n'.join(append)+'\n').encode())
write(RUN/'preparation-log.md','# Preparation and scope notes\n\nThe conversational plan was executed as a focused validator-only assessment. All created files are within this fresh run. Setup used harness.py, case preparation used probes.py prepare, then probes.py run. H11 was separately planned before its execution. audit_fixtures.py verified 42 record shapes and 180 reference occurrences; support_checks.py ran the installed structural checker, 27 affected regressions and source readback. Each candidate subprocess is recorded under commands/.\n\nRead-only exploration also used PowerShell Get-Content/Get-ChildItem/Get-FileHash and rg. One exploratory rg invocation with a literal tests/test_*.py argument failed on Windows with OS error 123. It was corrected to directory plus -g filtering; this was a search syntax error, not a candidate failure or a TDD red result. Some long tool readouts were truncated; focused follow-up reads supplied relevant source sections. Tool-call transcript retains those exploratory outputs; they are not falsely represented as subprocess receipts here.\n\nNo candidate process timed out, no retry was needed, and no target edits were attempted. Extra generated empty.jsonl in H11 is an unused setup artifact; it is not a supplied checks record. Previous implementation/QA reports remain historical claims except the exact bytes and four replays verified here. No dependency installation, WSL execution, model task or operational binding was performed.\n')
save(RUN/'final-receipt.json',{'completed_at':now(),'task':'Focused confirmation and remediation planning for QA-01 through QA-04','assessment_completed':True,'finding_verification':'4 CONFIRMED, 0 REFUTED, 0 UNRESOLVED','implementation_conformity':'FAIL for assessed behavior','repair_status':'NOT_PERFORMED','target_digest':EXPECTED,'target_files':75,'target_readback':'UNCHANGED','loaded_evaluator_readback':'UNCHANGED','companion_readback':'UNCHANGED','selected_prior_evidence_readback':'UNCHANGED','fresh_cases':{'total':33,'matched':22,'mismatched':11},'original_replays':{'total':4,'reproduced_failures':4},'affected_regression':{'passing':27,'total':27},'record_integrity':{'legacy':'PASS (self-review)','adaptive':'PASS (self-review)'},'full_regression':'NOT_RUN in this focused run; previously reported 229 not recertified','line_coverage':'NOT_RUN','branch_coverage':'NOT_RUN','native_qualification':'NOT_RUN','installation':'NOT_PERFORMED','rust_qualification':'NOT_RUN','report':ref(RUN/'finding-validation-report.md'),'matrix':ref(RUN/'finding-matrix.json'),'revision_spec':ref(RUN/'revision-spec.md'),'command_log':ref(RUN/'command-log.md'),'commands':ref(RUN/'command-log-final.json'),'input_readback':ref(RUN/'final-input-readback.json'),'handoff':ref(RUN/'authoring-handoff-supplement.json'),'evidence_link_audit':ref(RUN/'final-link-audit.json'),'remaining_work':'Review and separately authorize selected repairs, verify supported custody basis, implement through skill-creator using red/green/refactor, then fresh skill-validator QA and independently reported broader acceptance gaps.'})
print(json.dumps({'report':str(RUN/'finding-validation-report.md'),'proposal_sha256':sha(read(RUN/'revision-spec.md')),'receipt':str(RUN/'final-receipt.json'),'candidate_commands':len(commands),'target':'UNCHANGED','findings':'4 CONFIRMED'}))
