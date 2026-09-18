from trial_support import *

receipt=EVIDENCE/'routing-classification-receipt.json'
original=receipt.read_bytes()
(EVIDENCE/'routing-classification-receipt-original.json').write_bytes(original)
value=json.loads(original)
value['prompt']="""While final binding is held, perform a separate routing classification task using the loaded builder's actual entrypoint and raw requests at forward-inputs/routing-requests.jsonl under 20260912-build-v2. For each request, emit one observed JSONL row {case_id,route}, selecting from import/spec_build/revision/explanation/specification_authoring/installation/unrelated based on the request. Save routing-observed.jsonl in your disposable project's evidence (outside generated package), include actual prompt/request source and manifest currently observed in a separate receipt. Do not read root expected classifications or tests, and do not execute any of those seven requests. Report this as classification, not native implicit activation. Still complete the original spec build when I send the final digest."""
value.pop('prompt_note')
write_json(receipt,value)
log(dict(cwd=str(ROOT),action='Corrected routing receipt to exact parent prompt punctuation and possessives',before_sha256=sha(original),after_sha256=sha(receipt.read_bytes()),preserved_original='routing-classification-receipt-original.json',interpretation='Metadata transcription correction only; observed routes and request digests unchanged'))
print(json.dumps(dict(receipt=str(receipt),sha256=sha(receipt.read_bytes()),observed_sha256=value['observed_sha256'])))
