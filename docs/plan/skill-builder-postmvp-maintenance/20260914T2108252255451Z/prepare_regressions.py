"""Copy a retained adaptive suite into fresh maintenance evidence."""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
source = ROOT / 'docs/plan/skill-adaptive-implementations/skill-builder/20260913T083452607505Z/test_adaptive.py'
text = source.read_text(encoding='utf-8')
text = text.replace('PROJECT = RUN.parents[4]', 'PROJECT = RUN.parents[3]')
text = text.replace("if row['path'].startswith('schemas/') or row['path'].startswith('scripts/'):",
    "if (row['path'].startswith('schemas/') or row['path'].startswith('scripts/')) and row['path'] != 'scripts/authoring.py':")
(RUN / 'test_builder_adaptive.py').write_text(text, encoding='utf-8')
before = json.loads((RUN / 'before-manifest.json').read_bytes())
(RUN / 'builder-before.json').write_text(json.dumps({'files': [{'path': p, 'sha256': h} for p, h in before.items()]}, indent=2))
(RUN / 'regression-adaptation.md').write_text('''# Retained adaptive tests

Copied the prior 20260913T083452607505Z test_adaptive.py, preserved at its source.
Changed only project ancestry for this new evidence location and the byte-preservation
test to exclude scripts/authoring.py, whose changes SBP-010/011 explicitly require.
The byte baseline is the captured pre-maintenance package, never historical bytes.
All previous schemas and other scripts remain in its preservation assertion.
ADAPTIVE_TEST_ROOT selects a new per-attempt fixture root. All functional cases remain.
This is maintenance regression evidence, not independent skill-validator evaluation.
''')
