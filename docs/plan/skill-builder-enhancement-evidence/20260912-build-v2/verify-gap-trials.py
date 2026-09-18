"""Check actual model gap-trial artifacts; no model calls or package mutation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "forward/import-project"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def confined(value, boundary):
    path = Path(value).resolve()
    assert path.is_relative_to(boundary.resolve()), str(path)
    return path


expected = {
    "gaps-missing": ("MISSING_INPUT", {"REQ-02"}),
    "gaps-contradictory": ("CONTRADICTORY_REQUIREMENT", {"REQ-02", "REQ-03"}),
    "gaps-capability": ("UNSUPPORTED_CAPABILITY", {"REQ-02", "REQ-03"}),
}
trials = json.loads((PROJECT / "gap-trial-results.json").read_text(encoding="utf-8"))["trials"]
assert len(trials) == len(expected) and {row["target"] for row in trials} == set(expected)
observations = []
for row in trials:
    code, ids = expected[row["target"]]
    evidence = confined(row["evidence"], PROJECT)
    source = confined(row["input"], ROOT / "forward-inputs")
    source_bytes = source.read_bytes()
    contract = json.loads((evidence / "build-contract.json").read_text(encoding="utf-8"))
    inputs = {value["id"]: value for value in contract["inputs"]}
    assert len(inputs) == 1
    value = next(iter(inputs.values()))
    assert value["bytes"] == len(source_bytes) and value["sha256"] == sha(source_bytes)
    snapshot_input = confined(evidence / "evaluation-snapshot" / value["path"], evidence)
    assert snapshot_input.read_bytes() == source_bytes
    gaps = json.loads((evidence / "spec-gaps.json").read_text(encoding="utf-8"))
    assert gaps["schema_version"] == "1" and len(gaps["gaps"]) == 1
    gap = gaps["gaps"][0]
    assert set(gap) == {"id", "reason_code", "source_refs", "requirement_ids", "affected_outputs", "description", "required_resolution"}
    assert gap["reason_code"] == code and set(gap["requirement_ids"]) == ids
    assert gap["id"] and gap["description"] and gap["required_resolution"] and gap["affected_outputs"]
    assert gap["source_refs"]
    for ref in gap["source_refs"]:
        assert ref["input_id"] in inputs
        start, end = ref["start_byte"], ref["end_byte"]
        assert type(start) is int and type(end) is int and 0 <= start < end <= len(source_bytes)
        assert sha(source_bytes[start:end]) == ref["sha256"]
    # Inspect actual paths instead of accepting candidate_created/report flags.
    paths = [evidence / "candidate", evidence / "evaluation-snapshot/destination",
             PROJECT / "src/agents/skills" / row["target"]]
    assert all(not path.exists() for path in paths)
    assert not list(evidence.rglob("SKILL.md"))
    assert row["status"] == "BLOCKED"
    observations.append({"case_id": row["target"], "status": "PASS", "reason_code": code,
                         "input_sha256": sha(source_bytes),
                         "spec_gaps_sha256": sha((evidence / "spec-gaps.json").read_bytes()),
                         "absent_paths_observed": [str(path) for path in paths]})

result = {"schema_version": "1", "authority": "NONE", "observations": observations,
          "limit": "Checks actual retained trial artifacts and current absence; does not predict future model behavior."}
with (ROOT / "gap-trial-observations.json").open("x", encoding="utf-8", newline="\n") as output:
    output.write(json.dumps(result, indent=2) + "\n")
print(json.dumps({"gap_trials": len(observations), "status": "PASS", "authority": "NONE"}))
