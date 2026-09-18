"""Readback and bind final maintenance evidence; no authority or source mutation."""
import hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
TARGET=ROOT/'src/agents/skills/skill-validator'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2),encoding='utf-8')
files=json.loads((RUN/'delivery-003/source-manifest.json').read_text())
assert all(sha(TARGET/path)==digest for path,digest in files.items()),'Final source drift'
protected=json.loads((RUN/'preservation.json').read_text())
assert all(sha(Path(row['path']))==row['sha256'] for row in protected),'Protected file drift'
for name in ('README.md','implementation-report.md'):
    doc=RUN/name
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
        parsed=urlsplit(target)
        if not parsed.scheme and parsed.path:
            assert (doc.parent/unquote(parsed.path)).exists(),f'Broken report link: {target}'
package_digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
coverage=json.loads((RUN/'coverage-final-003/measurement.json').read_text())
write(RUN/'delivery-summary.json',dict(implementation='DELIVERED',qualification=sys.argv[1],
      source_file_count=len(files),source_package_digest=package_digest,
      package_digest_definition='SHA256 of sorted compact JSON path-to-sha256 mapping in delivery-003/source-manifest.json',
      regression=json.loads((RUN/'regression-005-grading.json').read_text()),
      line_coverage={k:coverage[k] for k in ('covered_lines','statements','line_percent')},
      branch_coverage={k:coverage[k] for k in ('covered_branches','branches','branch_percent')},
      protected_files_unchanged=len(protected),framework_acceptance='NOT_EVALUATED',linux_native='NOT_RUN'))
manifest={p.relative_to(RUN).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(RUN.rglob('*'))
          if p.is_file() and p.name!='bundle-manifest.json' and '__pycache__' not in p.parts}
write(RUN/'bundle-manifest.json',dict(schema_version='maintenance-bundle-v1',files=manifest,
      limitation='Editable evidence integrity inventory; not protected provenance or framework acceptance'))
print(json.dumps(dict(files=len(manifest),source_file_count=len(files),source_package_digest=package_digest,
                     bundle_manifest_sha256=sha(RUN/'bundle-manifest.json'))))
