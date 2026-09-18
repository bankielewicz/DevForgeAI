"""Append a V3 artifact manifest without replacing the earlier V2 manifest."""
import hashlib
import json
from pathlib import Path
RUN=Path(__file__).resolve().parent
output=RUN/'artifact-manifest-v3.json'
assert not output.exists()
rows={p.relative_to(RUN).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(RUN.rglob('*')) if p.is_file() and p!=output and '__pycache__' not in p.parts}
output.write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps({'files':len(rows),'manifest':str(output)}))
