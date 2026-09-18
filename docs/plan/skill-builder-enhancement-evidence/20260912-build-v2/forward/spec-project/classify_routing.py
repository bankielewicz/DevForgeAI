from trial_support import *

routes = {
    'route-01':'import',
    'route-02':'spec_build',
    'route-03':'revision',
    'route-04':'explanation',
    'route-05':'specification_authoring',
    'route-06':'installation',
    'route-07':'unrelated',
}
source=INPUTS/'routing-requests.jsonl'
requests=[json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]
assert {row['case_id'] for row in requests}==set(routes)
observed=EVIDENCE/'routing-observed.jsonl'
with observed.open('x',encoding='utf-8') as stream:
    for row in requests:
        stream.write(json.dumps(dict(case_id=row['case_id'],route=routes[row['case_id']]))+'\n')
prompt='While final binding is held, perform a separate routing classification task using the loaded builder actual entrypoint and raw requests at forward-inputs/routing-requests.jsonl under 20260912-build-v2. For each request, emit one observed JSONL row {case_id,route}, selecting from import/spec_build/revision/explanation/specification_authoring/installation/unrelated based on the request. Save routing-observed.jsonl in your disposable project evidence (outside generated package), include actual prompt/request source and manifest currently observed in a separate receipt. Do not read root expected classifications or tests, and do not execute any of those seven requests. Report this as classification, not native implicit activation. Still complete the original spec build when I send the final digest.'
receipt=dict(schema_version='1',run_id=RUN,captured_at_utc=stamp(),task='Independent routing classification by the forward specification agent',prompt=prompt,prompt_note='Parent task text transcribed with apostrophes omitted; exact parent message is in the conversation.',request_source=str(source),request_source_sha256=sha(source.read_bytes()),request_snapshot='routing-source-routing-requests.jsonl',requests=requests,entrypoint=str(BUILDER/'SKILL.md'),entrypoint_sha256=sha((BUILDER/'SKILL.md').read_bytes()),entrypoint_snapshot='routing-source-SKILL.md',manifest_currently_observed_path=str(BUILDER/'evals/build-manifest.json'),manifest_currently_observed_sha256=sha((BUILDER/'evals/build-manifest.json').read_bytes()),manifest_status='Digest observation only during parent binding hold; no final package-binding evaluator result claimed',observed_path=str(observed),observed_sha256=sha(observed.read_bytes()),classification_method='Agent read actual entrypoint and raw requests, then selected route by requested operation; mapping persisted without executing requests.',requests_executed=False,expected_classifications_read=False,tests_read=False,native_implicit_activation='NOT_PERFORMED',rationales={'route-01':'Selected local Claude package conversion requests import.','route-02':'Selected approved Markdown requests specification build.','route-03':'Authorized existing generated output update requests revision with prior evidence.','route-04':'Explanation alone explicitly forbids mutation.','route-05':'The specification is the only requested deliverable.','route-06':'Already-built package installation is separate from development authoring.','route-07':'Application README spelling edit requests no skill changes.'})
write_json(EVIDENCE/'routing-classification-receipt.json',receipt)
log(dict(cwd=str(ROOT),tool='apply_patch and Python persistence',action='Persisted agent routing classifications and receipt',output=str(observed),observed=routes,interpretation='Classification only; no request execution or native implicit activation'))
print(observed.read_text(encoding='utf-8'))
print(json.dumps(dict(receipt=str(EVIDENCE/'routing-classification-receipt.json'),sha256=sha((EVIDENCE/'routing-classification-receipt.json').read_bytes()),manifest=receipt['manifest_currently_observed_sha256'])))
