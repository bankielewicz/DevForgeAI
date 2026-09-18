"""Fresh corrected legacy evidence layout; preserve failed original attempt."""
import json
import shutil
from capture import RUN

source=RUN/'self-review'
target=RUN/'self-review-records-003'
target.mkdir()
for path in source.iterdir():
    if path.name=='observations':
        continue
    if path.is_dir():
        shutil.copytree(path,target/path.name)
    else:
        shutil.copyfile(path,target/path.name)
shutil.copytree(source/'observations',target/'inputs/observations')
def rebase(value):
    if isinstance(value,dict):
        for key,item in value.items():
            if key=='path' and isinstance(item,str) and item.startswith('observations/'):
                value[key]='inputs/'+item
            else:
                rebase(item)
    elif isinstance(value,list):
        for item in value:
            rebase(item)
for path in target.iterdir():
    if path.suffix not in ('.json','.jsonl'):
        continue
    lines=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()] if path.suffix=='.jsonl' else [json.loads(path.read_bytes())]
    previous=json.dumps(lines,ensure_ascii=False)
    for value in lines:
        rebase(value)
    if json.dumps(lines,ensure_ascii=False)!=previous:
        path.write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in lines) if path.suffix=='.jsonl' else json.dumps(lines[0],ensure_ascii=False,indent=2),encoding='utf-8')
(target/'layout-correction.md').write_text('Fresh evidence-layout attempt. The original self-review/ and failed legacy-records-001 output remain intact. Raw native/helper JSON now lives under inputs/observations so the unchanged schema-1 reader treats it as input bytes, not evaluator-owned records. References retain their run-relative base and actual byte digests.\n',encoding='utf-8')
print(str(target))
