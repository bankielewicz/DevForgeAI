"""Inventory retained evidence without following fixture reparse points."""
import datetime as dt
import json
import os
from pathlib import Path
import record

root = Path(__file__).resolve().parent
destination = root/'artifact-manifest.json'
if destination.exists():
    raise SystemExit('Refusing to replace sealed artifact manifest')
entries = []
excluded_build_files = 0
def visit(directory):
    global excluded_build_files
    for entry in sorted(os.scandir(directory),key=lambda item:item.name.casefold()):
        path = Path(entry.path)
        if path == destination:
            continue
        stat = entry.stat(follow_symlinks=False)
        relative = path.relative_to(root).as_posix()
        if int(getattr(stat,'st_file_attributes',0)) & 0x400:
            entries.append({'path':relative,'kind':'reparse','target':os.readlink(path)})
        elif entry.is_dir(follow_symlinks=False):
            visit(path)
        elif entry.is_file(follow_symlinks=False):
            in_build = any(part.startswith('target') for part in path.relative_to(root).parts[:-1])
            if in_build and path.suffix not in {'.profraw','.profdata'}:
                excluded_build_files += 1
                continue
            entries.append({'path':relative,'kind':'file','bytes':stat.st_size,'sha256':record.sha256(path)})
visit(root)
external = []
begin = dt.datetime(2026,9,16,0,38,40,tzinfo=dt.timezone.utc).timestamp()
for directory in sorted((record.WORKSPACE/'docs/plan/framework-worker-trials').glob('RT-source-type-*')):
    if directory.stat().st_ctime < begin:
        continue
    for path in sorted(directory.rglob('*')):
        if path.is_file():
            external.append({'path':str(path),'bytes':path.stat().st_size,'sha256':record.sha256(path)})
value = {'schema_version':1,'created_utc':record.utc_now(),'entries':entries,
    'external_rt_source_fixture_files':external,
    'scope':'All evidence-root files except disposable compiler intermediates; raw profraw/profdata retained and included. Fixture reparse targets are recorded, never followed. Manifest excludes itself.',
    'excluded_disposable_build_files':excluded_build_files}
record.atomic_json(destination,value)
print(json.dumps({'entries':len(entries),'external_fixture_files':len(external),'artifact_manifest_sha256':record.sha256(destination),'excluded_build_files':excluded_build_files}))
