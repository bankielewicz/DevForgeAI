"""Hash readback and evidence indexing only, never framework acceptance."""
import json
import os
from pathlib import Path
import record

def readback(filename):
    expected = json.loads((record.ROOT/filename).read_text(encoding='utf-8-sig'))
    values = []
    for entry in expected:
        path = Path(entry['path'])
        actual = record.sha(path) if path.is_file() else None
        values.append({**entry,'actual_sha256':actual,'matches':actual==entry['sha256']})
    return values

for source, output in [('candidate-manifest.json','post-qa-source-readback.json'),('inputs-manifest.json','post-qa-inputs-readback.json')]:
    values = readback(source)
    record.write(output,values)
    print(json.dumps({'record':output,'entries':len(values),'mismatches':sum(not e['matches'] for e in values)}))

files = []
reparses = []
def scan(directory):
    for entry in sorted(os.scandir(directory),key=lambda e:e.name):
        path = Path(entry.path)
        info = entry.stat(follow_symlinks=False)
        if getattr(info,'st_file_attributes',0)&0x400:
            reparses.append({'path':str(path),'target':os.readlink(path)})
        elif entry.is_dir(follow_symlinks=False):
            if entry.name != 'target':
                scan(path)
        elif path.name != 'evidence-manifest.json':
            files.append({'path':str(path),'bytes':info.st_size,'sha256':record.sha(path)})
scan(record.ROOT)
record.write('evidence-manifest.json',{'files':files,'reparses_not_followed':reparses,'excluded':'target build output is retained in place; independent QA owns its raw coverage bindings'})
print(json.dumps({'evidence_files':len(files),'evidence_manifest_sha256':record.sha(record.ROOT/'evidence-manifest.json')}))
