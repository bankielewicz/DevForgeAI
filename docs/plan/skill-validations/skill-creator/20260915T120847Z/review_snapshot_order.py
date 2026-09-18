"""Correct the reviewer ordering error without rerunning any product trial."""
import datetime,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
expected=json.loads((ROOT/"source-manifest.json").read_text())["files"]
for case in ("create","update"):
    trial=ROOT/"trials"/case
    observed=sorted([{"path":p.relative_to(trial/"skill-creator").as_posix(),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in (trial/"skill-creator").rglob("*") if p.is_file()],key=lambda r:r["path"])
    assert observed==expected
    with (trial/"snapshot-readback.json").open("x",encoding="utf-8") as f:json.dump({"files":observed,"matches":True,"sort":"relative POSIX path, case-sensitive; matches source manifest contract"},f,indent=2)
    previous=json.loads((trial/"primary-review.json").read_text())
    revised={**previous,"checks":{**previous["checks"],"skill_creator_snapshot_unchanged":True}}
    revised["result"]="PASS" if all(revised["checks"].values()) else "FAIL"
    revised["reviewed_at_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    revised["prior_review"]="primary-review.json"
    revised["harness_correction"]="Original reviewer compared case-insensitive Windows Path enumeration order to case-sensitive manifest order. All path/size/hash mappings were identical. Corrected by sorting relative path strings; original failure retained. No product task was retried or modified."
    with (trial/"primary-review-002.json").open("x",encoding="utf-8") as f:json.dump(revised,f,indent=2)
    print(case,revised["result"])

