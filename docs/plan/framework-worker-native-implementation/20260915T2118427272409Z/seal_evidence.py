"""Integrity inventory only. Editable hashes are not a protected acceptance receipt."""
import datetime
import json
import os
from pathlib import Path
from record import ROOT, WORK, sha, write

entries=[]
reparses=[]
def visit(directory):
    for entry in sorted(os.scandir(directory), key=lambda e:e.name):
        path=Path(entry.path)
        info=entry.stat(follow_symlinks=False)
        if getattr(info,'st_file_attributes',0)&0x400:
            reparses.append({'path':str(path),'attributes':info.st_file_attributes,
                'target':os.readlink(path),'note':'retained fixture link; never traversed'})
        elif entry.is_dir(follow_symlinks=False):
            if path!=ROOT/'target': visit(path)
        elif path.name not in ('evidence-manifest.json','reparse-inventory.json','compiled-and-raw-coverage-manifest.json'):
            entries.append({'path':str(path),'bytes':info.st_size,'sha256':sha(path)})

visit(ROOT)
write('reparse-inventory.json',reparses)
entries.append({'path':str(ROOT/'reparse-inventory.json'),'bytes':(ROOT/'reparse-inventory.json').stat().st_size,'sha256':sha(ROOT/'reparse-inventory.json')})
write('evidence-manifest.json',entries)
artifacts=[]
for path in sorted((ROOT/'target').rglob('*')):
    if path.is_file() and (path.suffix in ('.profraw','.profdata') or path.suffix=='.exe'
            and path.name.startswith(('devforgeai_codex_worker_probe','devforgeai-codex-worker-probe','protocol_peer','protocol-peer','console_driver','console-driver','crash_driver','crash-driver'))):
        artifacts.append({'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path)})
write('compiled-and-raw-coverage-manifest.json',artifacts)
entries.append({'path':str(ROOT/'compiled-and-raw-coverage-manifest.json'),'bytes':(ROOT/'compiled-and-raw-coverage-manifest.json').stat().st_size,'sha256':sha(ROOT/'compiled-and-raw-coverage-manifest.json')})
write('evidence-manifest.json',entries)
print(json.dumps({'evidence_files':len(entries),'raw_and_binary_artifacts':len(artifacts),'reparse_points_not_traversed':len(reparses),
    'evidence_manifest_sha256':sha(ROOT/'evidence-manifest.json')}))
