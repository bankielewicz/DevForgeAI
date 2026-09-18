"""Resolve first-party ownership and report retained full-collection evidence."""
import json
from decimal import Decimal
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
raw = ROOT/'full-coverage/coverage.json'
coverage = json.loads(raw.read_text(encoding='utf-8'))
source = json.loads((ROOT/'source-denominator.json').read_text(encoding='utf-8'))['source_files']
selected = {str(Path(entry['path']).resolve()).casefold():entry for entry in source}
files, excluded, seen = [], [], set()
for dataset in coverage['data']:
    for entry in dataset['files']:
        path = Path(entry['filename']).resolve()
        key = str(path).casefold()
        if key not in selected:
            excluded.append(str(path))
            continue
        if key in seen:
            raise SystemExit('Duplicate first-party source in raw coverage:' + str(path))
        seen.add(key)
        if record.sha256(path) != selected[key]['sha256']:
            raise SystemExit('Source drift:' + str(path))
        files.append({'path':str(path),'sha256':record.sha256(path), 'lines':entry['summary']['lines'],
                      'branches':entry['summary'].get('branches')})
missing = [entry['path'] for key,entry in selected.items() if key not in seen]
if any(Path(path).name != 'lib.rs' for path in missing):
    raise SystemExit('Missing executable source in raw JSON:' + str(missing))
covered = sum(entry['lines']['covered'] for entry in files)
count = sum(entry['lines']['count'] for entry in files)
result = {'raw':str(raw),'raw_sha256':record.sha256(raw),'covered_lines':covered,'executable_lines':count,
          'percent':str(Decimal(covered)*100/Decimal(count)), 'threshold_percent':95,
          'meets_threshold':covered*100 >= count*95,'files':files,'declared_files_without_executable_lines':missing,
          'excluded_resolved_paths':excluded,'first_party_exclusions':[],
          'branch_status':'NOT_RUN unless raw JSON contains instrumented branches'}
record.atomic_json(ROOT/'coverage-analysis.json',result)
print(json.dumps({key:result[key] for key in ['covered_lines','executable_lines','percent','meets_threshold','raw_sha256']}))
