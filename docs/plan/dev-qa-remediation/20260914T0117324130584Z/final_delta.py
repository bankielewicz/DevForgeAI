"""Final scoped byte/delta observations; no quality or authority decision."""
import datetime
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[3]
sys.path.insert(0,str(PROJECT/"src/agents/skills/skill-builder/scripts"))
import authoring as a
expected={
"skill-builder":{"scripts/authoring.py","references/authoring.md","references/evidence-format.md"},
"skill-validator":{"tests/test_authoring.py","tests/test_authoring_safeguards.py","evals/build-manifest.json"},
"dev":{"SKILL.md","references/context.md","references/evidence-resume.md","references/failure-delivery.md","assets/context.md","assets/delivery.md","assets/checkpoint.md","assets/traceability.md"}}
results={}
for name,allowed in expected.items():
    before=json.loads((ROOT/"before"/(name+"-manifest.json")).read_bytes())
    current=a.manifest(a.files(PROJECT/"src/agents/skills"/name))
    old={r["path"]:r for r in before["files"]}
    new={r["path"]:r for r in current["files"]}
    delta=sorted(p for p in old.keys()|new.keys() if old.get(p)!=new.get(p))
    if set(delta)!=allowed:
        raise ValueError("Unexpected source delta "+name+" "+str(delta))
    operational=a.manifest(a.files(PROJECT/".agents/skills"/name))
    results[name]={"before_digest":before["package_digest"],"after_digest":current["package_digest"],
                   "changed_paths":delta,"files":current["files"],
                   "operational_matches_prechange_development":operational["package_digest"]==before["package_digest"],
                   "operational_package_digest":operational["package_digest"]}
spec=PROJECT/"docs/specs/dev-skill-spec.md"
if a.digest(spec.read_bytes())!="b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265":
    raise ValueError("specification drift")
a.save(ROOT/"implementation-readback.json",{"recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"packages":results,
"specification_sha256":a.digest(spec.read_bytes()),"framework_acceptance":"NOT_EVALUATED",
"interpretation":"Scoped complete file-byte readback; no whole-machine or protected enforcement claim."})
print(json.dumps({name:{k:v for k,v in value.items() if k!="files"} for name,value in results.items()},indent=2))

