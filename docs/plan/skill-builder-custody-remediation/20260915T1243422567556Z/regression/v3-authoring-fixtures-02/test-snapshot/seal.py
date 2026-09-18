"""Inventory final external regression artifacts without rewriting old evidence."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[4]
def manifest(root):
    return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='artifact-manifest.json'}
dependencies={name:importlib.metadata.version(name) for name in ('coverage','PyYAML','jsonschema')}
(RUN/'dependencies.json').write_text(json.dumps({'python':sys.version,'executable':sys.executable,'dependencies':dependencies,'installation':'Used existing dependencies; no installation'},indent=2),encoding='utf-8')
audit=ROOT/'docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures'
external={str(audit/name):manifest(audit/name) for name in ('extended-04','followup-02')}
(RUN/'retained-fixture-manifest.json').write_text(json.dumps(external,indent=2),encoding='utf-8')
(RUN/'artifact-manifest.json').write_text(json.dumps(manifest(RUN),indent=2),encoding='utf-8')
print(json.dumps({'external_roots':len(external),'artifacts':len(manifest(RUN))}))
