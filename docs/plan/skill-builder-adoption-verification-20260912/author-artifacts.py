"""One-time authoring receipt. --bind is run only after reviewing intentional edits."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
package = Path(__file__).resolve().parents[3] / "src/agents/skills/skill-builder"

def module(name):
    spec = importlib.util.spec_from_file_location(name, package / "scripts" / (name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

runner, graders = module("run_evaluation"), module("graders")

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if "--bind" in sys.argv:
    files = graders.snapshot(package)
    files.pop("evals/build-manifest.json")
    manifest = {"schema_version": "2", "graders": {g: runner.VERSION for g in runner.GRADER_IDS},
                "profiles": runner.PROFILES,
                "artifacts": {p: hashlib.sha256(d).hexdigest() for p, d in sorted(files.items())}}
    write(package / "evals/build-manifest.json", manifest)
    print(hashlib.sha256((package / "evals/build-manifest.json").read_bytes()).hexdigest())
    sys.exit(0)

write(package / "evals/profiles.json", {"schema_version": "1", "profiles": runner.PROFILES})
path = package / "evals/build-artifacts.schema.json"
schema = json.loads(path.read_text(encoding="utf-8"))
for key, values in (("graders", {g: runner.VERSION for g in runner.GRADER_IDS}), ("profiles", runner.PROFILES)):
    schema["properties"][key]["required"] = list(values)
    schema["properties"][key]["properties"] = {k: {"const": v} for k, v in values.items()}
write(path, schema)
path = package / "evals/evidence.schema.json"
schema = json.loads(path.read_text(encoding="utf-8"))
schema["properties"]["grader_id"]["enum"] = [*runner.GRADER_IDS, None]
write(path, schema)

string = {"type": "string", "minLength": 1}
sha = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
relative = {"type": "string", "pattern": r"^(?!/)(?!.*(?:^|/)\.{1,2}(?:/|$))[^\\:]+$"}
paths = {"type": "array", "uniqueItems": True, "items": relative}
def obj(properties, optional=()):
    return {"type": "object", "additionalProperties": False,
            "required": [p for p in properties if p not in optional], "properties": properties}
def arr(items):
    return {"type": "array", "items": items}
ref = obj({"path": relative, "sha256": sha})
typed = obj({"kind": {"enum": ["adopted", "generated"]}, "path": relative, "sha256": sha})
rows = arr(obj({"path": relative, "bytes": {"type": "integer", "minimum": 0}, "sha256": sha}))
record = {p: string for p in ("run_id", "target_name", "target_root", "project_root", "captured_at_utc")}
record.update(schema_version={"const": "1"}, record_kind={"const": "adoption"}, historical_origin={"const": "unknown"},
              snapshot_root=relative, snapshot_manifest=ref, managed_manifest=ref, managed_paths={**paths, "minItems": 1},
              retained_user_paths=paths, origin_spec=ref, origin_spec_input=obj({"resolved_path": string, "bytes": {"type": "integer", "minimum": 0}, "sha256": sha}),
              authorization=obj({"instruction": string, "target_root": string, "managed_manifest_sha256": sha, "origin_spec_sha256": sha}),
              prior_evidence=arr(ref), quality_evidence=arr(ref), source_readback=ref,
              recording_state={"enum": ["ADOPTED", "INCOMPLETE"]}, known_defects=arr(string), handoff=ref)
definitions = {
    "adoption_record": obj(record, ("known_defects", "handoff")),
    "manifest": obj({"schema_version": {"const": "1"}, "files": rows}),
    "source_readback": obj({"schema_version": {"const": "1"}, "run_id": string, "target_root": string, "before": rows, "after": rows,
                             "spec_before_sha256": sha, "spec_after_sha256": sha, "outcome": string}),
    "pointer": obj({"schema_version": {"const": "2"}, "run_id": string, "target_name": string, "origin": typed,
                    "baseline": arr(obj({"path": relative, "sha256": sha}))}),
    "handoff": obj({"schema_version": {"const": "1"}, "target_root": string, "target_manifest_sha256": sha, "managed_manifest_sha256": sha,
                    "origin_spec_sha256": sha, "review_policy": {"const": "review-before-repair"}, "review_state": string,
                    "selected_references": {**arr(ref), "minItems": 1}, "builder_readiness": string}),
}
provenance = obj({"schema_version": {"const": "2"}, "run_id": string, "mode": {"const": "spec_build"}, "target_name": string,
                  "builder_manifest_sha256": sha, "contract_sha256": sha,
                  "inputs": arr(obj({"id": string, "sha256": sha})), "dependencies": arr({"type": "object"}),
                  "outputs": arr(obj({"path": relative, "sha256": sha, "ownership": {"enum": ["generated", "retained_user"]},
                                      "baseline_path": {"anyOf": [relative, {"type": "null"}]},
                                      "baseline_sha256": {"anyOf": [sha, {"type": "null"}]}})),
                  "mappings": arr(obj({"requirement_id": string, "artifact_paths": paths, "evidence_ids": {"type": "array", "items": string, "uniqueItems": True, "minItems": 1}})),
                  "evidence": arr(obj({"id": string, "path": relative, "sha256": sha})),
                  "prior_origin": typed, "adoption_origin": ref, "result": {"enum": ["COMPLETE", "INCOMPLETE"]}})
plan_fields = {p: relative for p in ("baseline", "current", "candidate", "after")}
plan_fields.update(schema_version={"const": "2"}, run_id=string, status={"enum": ["CONFLICT", "PLANNED", "APPLIED", "PARTIAL"]},
                   required_paths={**paths, "minItems": 1}, owned_paths=paths, applied_paths=paths,
                   rows=arr(obj({"path": relative, "ownership": {"enum": ["adopted", "generated", "retained_user"]},
                                 **{p: {"anyOf": [sha, {"type": "null"}]} for p in ("b_sha256", "c_sha256", "n_sha256")},
                                 "action": {"enum": ["USE_NEW", "KEEP_CURRENT", "CONFLICT"]}, "reason": string})),
                   baseline_advanced={"type": "boolean"}, readback_passed={"type": "boolean"}, evaluation_passed={"type": "boolean"},
                   prior_origin=typed, adoption_origin=ref, baseline_before=ref, baseline_after=ref, retry_of=ref)
definitions.update(provenance_v2=provenance, revision_plan_v2=obj(plan_fields, ("retry_of",)))
write(package / "evals/adoption-evidence.schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema",
      "title": "Observed adoption custody and typed development origins; no acceptance authority",
      "$ref": "#/$defs/adoption_record", "$defs": definitions})
print("Authored profile and schema extensions; manifest not rebound.")
