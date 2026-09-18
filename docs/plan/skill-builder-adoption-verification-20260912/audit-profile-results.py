"""Read back every final deterministic case and every measured candidate byte."""
import hashlib
import json
from pathlib import Path
import sys

evidence = Path(__file__).resolve().parent
suffix = "-release" if "--release" in sys.argv else ""
batch = evidence / ("profile-checks-release" if suffix else "profile-checks-final-bound")
package = evidence.parents[2] / "src/agents/skills/skill-builder"
def sha(data):
    return hashlib.sha256(data).hexdigest()
manifest_digest = sha((package / "evals/build-manifest.json").read_bytes())
records, measured = [], 0
for output in sorted(batch.glob("*/evaluation.jsonl")):
    candidate = output.parent / "candidate"
    cases = output.parent / "cases.jsonl"
    for line in output.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        assert record["build_manifest_sha256"] == manifest_digest
        assert record["cases_sha256"] == sha(cases.read_bytes())
        assert record["expectation_met"] is True
        for path, digest in record["candidate_digests"].items():
            selected = (candidate / path).resolve()
            assert selected.is_relative_to(candidate.resolve())
            assert sha(selected.read_bytes()) == digest, path
            measured += 1
        records.append(record)
summary = {"builder_manifest_sha256": manifest_digest, "evaluations": len(list(batch.glob("*/evaluation.jsonl"))),
           "observations": len(records), "pass_observations": sum(r["status"] == "PASS" for r in records),
           "expected_fail_observations": sum(r["status"] == "FAIL" for r in records),
           "all_expectations_matched": True, "measured_candidate_hashes_reverified": measured, "case_hashes_reverified": True}
(evidence / ("profile-readback-audit" + suffix + ".json")).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary))
