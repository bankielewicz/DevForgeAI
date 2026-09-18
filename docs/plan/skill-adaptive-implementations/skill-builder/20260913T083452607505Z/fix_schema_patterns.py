"""Fix inspected overescaped new-schema regexes only."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[5] / 'src/agents/skills/skill-builder/schemas'
path = root / 'adaptive-common.schema.json'
doc = json.loads(path.read_text())
doc['$defs']['RelPath']['pattern'] = '^(?!/)(?!.*[' + chr(92) * 2 + ':' + chr(0) + '])(?!(?:.*/)?[.]{1,2}(?:/|$))[^/]+(?:/[^/]+)*$'
path.write_text(json.dumps(doc, indent=2) + '\n', encoding='utf-8')
path = root / 'project-binding-v1.schema.json'
doc = json.loads(path.read_text())
doc['properties']['updated_at_utc']['pattern'] = '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:[.][0-9]+)?Z$'
path.write_text(json.dumps(doc, indent=2) + '\n', encoding='utf-8')
