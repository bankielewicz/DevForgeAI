"""Retain actual runner observations; synthetic cases are not forward trials."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
evidence = Path(__file__).resolve().parent
project = evidence.parents[2]
package = project / "src/agents/skills/skill-builder"
sys.path.insert(0, str(package / "tests"))
from adoption_fixture import build_adoption, build_v2
from fixture_data import build_candidate, sha, write, write_json

batch = evidence / ("profile-checks-release" if "--release" in sys.argv else "profile-checks-final-bound" if "--final" in sys.argv else "profile-checks-first-bound")
batch.mkdir(exist_ok=False)
builder_digest = sha((package / "evals/build-manifest.json").read_bytes())
observed = [json.loads(line) for line in (evidence.parent / "skill-builder-adoption-verification-20260912-independent-build-trials/routing-observed.jsonl").read_text().splitlines()]
expected_routes = {"r1": "adoption", "r2": "unrelated", "r3": "specification_authoring", "r4": "installation", "r5": "import", "r6": "spec_build", "r7": "revision", "r8": "explanation", "r9": "unrelated", "r10": "explanation"}
receipts = []

def routes(root, legacy=False, negative=False):
    selected = [r for r in observed if not legacy or r["case_id"] != "r1"]
    expected = [{"case_id": r["case_id"], "route": expected_routes[r["case_id"]], "request": r["request"]} for r in selected]
    for name, values in (("expected", expected), ("observed", selected)):
        values = [dict(r) for r in values]
        if name == "observed" and negative:
            values[0]["route"] = "installation"
        write(root / "routing" / (name + ".jsonl"), "".join(json.dumps(r) + "\n" for r in values))

def evaluate(name, profile, params, negative=()):
    candidate = batch / name / "candidate"
    case_path = batch / name / "cases.jsonl"
    cases = [{"case_id": name + "-" + g, "grader_id": g, "params": p, "expected": "FAIL" if g in negative else "PASS"} for g, p in params.items()]
    write(case_path, "".join(json.dumps(c) + "\n" for c in cases))
    output = batch / name / "evaluation.jsonl"
    command = [sys.executable, "-B", "-X", "utf8", str(package / "scripts/run_evaluation.py"), "--package-root", str(package),
               "--candidate-root", str(candidate), "--cases", str(case_path), "--output", str(output), "--run-id", name, "--profile", profile]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
    write(batch / name / "stdout.txt", result.stdout)
    write(batch / name / "stderr.txt", result.stderr)
    records = [json.loads(line) for line in output.read_text().splitlines()] if output.exists() else []
    receipt = {"name": name, "profile": profile, "command": command, "exit_code": result.returncode,
               "builder_manifest_sha256": builder_digest, "cases_sha256": sha(case_path.read_bytes()),
               "results": [{k: r.get(k) for k in ("grader_id", "status", "expected", "expectation_met", "observations", "error")} for r in records]}
    write_json(batch / name / "command.json", receipt)
    receipts.append(receipt)
    print(json.dumps({"name": name, "exit_code": result.returncode, "results": receipt["results"]}))

root = batch / "builder-v2-positive/candidate"
params = build_candidate(root, builder_digest)
routes(root, legacy=True)
evaluate("builder-v2-positive", "builder-v2", params)
for negative in (False, True):
    suffix = "negative" if negative else "positive"
    name = "adoption-" + suffix
    root = batch / name / "candidate"
    build_adoption(root)
    if negative:
        write(root / "adoption/destination/notes.txt", "Unauthorized mutation of retained user bytes.\n")
    evaluate(name, "adoption-v1", {"adoption_consistency": {"evidence": "adoption/evidence", "destination": "adoption/destination"}},
             ("adoption_consistency",) if negative else ())
    name = "revision-v2-" + suffix
    root = batch / name / "candidate"
    plan = build_v2(root, builder_digest, advance=True)
    if negative:
        plan["readback_passed"] = False
        write_json(root / "trace/evidence/revision-plan.json", plan)
    evaluate(name, "revision-spec-v2", {"package_links": {"path": "trace/destination"}, "build_traceability_v2": {"evidence": "trace/evidence", "destination": "trace/destination"},
              "revision_consistency_v2": {"path": "trace/evidence/revision-plan.json"}}, ("build_traceability_v2", "revision_consistency_v2") if negative else ())
    name = "routing-adoption-" + suffix
    root = batch / name / "candidate"
    routes(root, negative=negative)
    evaluate(name, "routing-adoption-v1", {"routing_outcomes_v2": {"expected": "routing/expected.jsonl", "observed": "routing/observed.jsonl"}},
             ("routing_outcomes_v2",) if negative else ())
write_json(batch / "summary.json", receipts)
if any(r["exit_code"] != 0 for r in receipts):
    sys.exit(1)
