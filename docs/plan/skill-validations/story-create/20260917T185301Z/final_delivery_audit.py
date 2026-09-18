"""Read the delivered packet, source identities and executed evidence before reporting."""
import hashlib
import json
from pathlib import Path
import re

RAW=Path(__file__).resolve().parent
ROOT=RAW.with_name(RAW.name+'-records')
SUPPLEMENT=RAW.with_name(RAW.name+'-supplemental')
PROJECT=RAW.parents[4]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False)
        stream.write('\n')

def main():
    # Report text was completed after native outputs; refresh its own handoff binding.
    handoff=json.loads((ROOT/'handoff.json').read_bytes())
    handoff['report']['sha256']=digest(ROOT/'validation-report.md')
    (ROOT/'handoff.json').write_text(json.dumps(handoff,indent=2)+'\n',encoding='utf-8')
    required=['source-manifest.json','source-after-manifest.json','origin-record.json','sources.json','rule-set.json','workflow-map.json','checks.jsonl','findings.json','validation-report.md','enforcement-recommendations.md','handoff.json','command-log.md','assessment.json','metrics.json','input-readback.json','operational-readback.json']
    for name in required:assert (ROOT/name).is_file(),name
    manifest=json.loads((ROOT/'source-manifest.json').read_bytes())
    target=PROJECT/'src/agents/skills/story-create'
    for row in manifest['files']:
        assert digest(target/row['path'])==row['sha256']
        assert digest(ROOT/'source'/row['path'])==row['sha256']
    assert {p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}=={r['path'] for r in manifest['files']}
    inputs=json.loads((RAW/'inputs/index.json').read_bytes())
    for row in inputs:assert digest(Path(row['original_path']))==row['sha256']
    source_dev=PROJECT/'.agents/skills/dev'
    captured_dev=RAW/'trials/N12/project/.agents/skills/dev'
    dev_paths=[p.relative_to(captured_dev).as_posix() for p in captured_dev.rglob('*') if p.is_file()]
    assert set(dev_paths)=={p.relative_to(source_dev).as_posix() for p in source_dev.rglob('*') if p.is_file()}
    for relative in dev_paths:assert digest(source_dev/relative)==digest(captured_dev/relative)
    bundle=json.loads((RAW/'evaluation-bundle-manifest.json').read_bytes())
    for row in bundle['files']:assert digest(RAW/row['path'])==row['sha256'],row['path']
    family=json.loads((SUPPLEMENT/'inputs/authoring-family-assessment.json').read_bytes())
    for key in ('request','baseline','authoring_record','intake','assessment'):
        assert digest(Path(family[key]['path']))==family[key]['sha256']
    assert family['target_digest']==manifest['package_digest'] and family['outcome']=='INCOMPLETE'
    native=json.loads((RAW/'native-assessment.json').read_bytes())
    assert len(native)==15 and sum(row['result']=='PASS' for row in native)==8
    for row in native:
        if row['case_id']!='N13':assert row['cleanup']=='VERIFIED' and row['input_unchanged']
    metrics=json.loads((ROOT/'metrics.json').read_bytes())
    assert metrics['Windows']['required_pass']==52 and metrics['Windows']['required_total']==62
    assert metrics['overall_declared_target_cases']['passing']==83 and metrics['overall_declared_target_cases']['required']==93
    assert json.loads((ROOT/'assessment.json').read_bytes())['overall_assessment']=='INCOMPLETE'
    links=[]
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)',(ROOT/'validation-report.md').read_text(encoding='utf-8')):
        link=match[1]
        if link.startswith('https://'):continue
        destination=(ROOT/link).resolve()
        assert destination.exists(),link
        links.append(link)
    report_hash=digest(ROOT/'validation-report.md')
    write(RAW/'final-delivery-audit.json',dict(schema_version='story-delivery-audit-v1',target_digest=manifest['package_digest'],target_files_unchanged=len(manifest['files']),original_inputs_unchanged=len(inputs),consumer_operational_files_unchanged=len(dev_paths),evaluation_bundle_files_unchanged=len(bundle['files']),required_packet_files_present=required,local_report_links_checked=links,report_sha256=report_hash,handoff_sha256=digest(ROOT/'handoff.json'),custom_authoring_supplement_refs_checked=5,native_case_count=15,native_complete=8,active_native_handles=0,active_handles_basis='Every launched case has a final receipt with VERIFIED process cleanup; orchestration sessions were polled to completion.',assessment='INCOMPLETE',framework_acceptance='NOT_EVALUATED',result='MATCH',limitation='Delivery integrity and arithmetic only; does not upgrade semantic or native coverage.'))
    print(json.dumps({'result':'MATCH','target_files':len(manifest['files']),'originals':len(inputs),'consumer_operational_files':len(dev_paths),'bundle_files':len(bundle['files']),'local_report_links':len(links),'assessment':'INCOMPLETE'}))

if __name__=='__main__':main()
