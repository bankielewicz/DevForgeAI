"""Maintenance-only consolidation of newly authored schemas; no legacy edits."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5] / 'src/agents/skills/skill-builder/schemas'
names = ['project-evidence-v1', 'adaptation-proposal-v1', 'adaptation-selection-v1', 'set-authoring-v1', 'set-validation-request-v1', 'adaptive-skill-v1', 'project-binding-v1', 'adaptive-observation-v1', 'binding-observation-v1']
documents = {name: json.loads((ROOT / (name + '.schema.json')).read_text(encoding='utf-8')) for name in names}
definitions = documents[names[0]]['$defs']
assert all(value['$defs'] == definitions for value in documents.values())
common = ROOT / 'adaptive-common.schema.json'
with common.open('x', encoding='utf-8') as stream:
    json.dump({'$schema': 'https://json-schema.org/draft/2020-12/schema', '$defs': definitions}, stream, indent=2)
for name, value in documents.items():
    del value['$defs']
    text = json.dumps(value, indent=2).replace('#/$defs/', 'adaptive-common.schema.json#/$defs/') + '\n'
    (ROOT / (name + '.schema.json')).write_text(text, encoding='utf-8')
