"""Retain final source and handoff byte observations; no acceptance authority."""
import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
sys.path.insert(0, str(PROJECT / "src/agents/skills/skill-builder/scripts"))
import authoring as custody


def load(path):
    return json.loads(path.read_bytes())


def ref(path):
    return {"path": str(path.resolve()), "sha256": custody.digest(path.read_bytes())}


def main():
    validation = PROJECT / "docs/plan/skill-validations/dev" / ROOT.name
    authoring = PROJECT / "docs/plan/skill-authorings/dev" / ROOT.name
    receipt = load(validation / "FINAL-RECEIPT.json")
    if receipt.get("assessment_completed") is not True:
        raise ValueError("Independent assessment has not completed")
    for key in ("artifact_readback", "validation_report", "bundle", "handoff"):
        bound = receipt[key]
        path = (validation / bound["path"]).resolve()
        if not path.is_relative_to(validation.resolve()) or ref(path)["sha256"] != bound["sha256"]:
            raise ValueError("Validator receipt reference mismatch: " + key)
    validation_files = load(validation / "final-artifact-manifest.json")["files"]
    for row in validation_files:
        path = (validation / row["path"]).resolve()
        if not path.is_relative_to(validation.resolve()):
            raise ValueError("Validator artifact outside declared readback scope")
        raw = path.read_bytes()
        if len(raw) != row["bytes"] or custody.digest(raw) != row["sha256"]:
            raise ValueError("Validator delivered artifact changed: " + row["path"])
    prior = load(ROOT / "implementation-readback.json")
    observations = {}
    for name, expected in prior["packages"].items():
        current = custody.manifest(custody.files(PROJECT / "src/agents/skills" / name))
        operational = custody.manifest(custody.files(PROJECT / ".agents/skills" / name))
        if current["package_digest"] != expected["after_digest"] or current["files"] != expected["files"]:
            raise ValueError("Development source drift: " + name)
        if operational["package_digest"] != expected["operational_package_digest"]:
            raise ValueError("Operational source drift: " + name)
        observations[name] = {"development": current, "operational_digest": operational["package_digest"],
                              "changed_paths": expected["changed_paths"], "unchanged_since_readback": True}
    if receipt["target_package_digest"] != observations["dev"]["development"]["package_digest"]:
        raise ValueError("Assessment target differs from delivery")
    fixed = {
        PROJECT / "docs/specs/dev-skill-spec.md": "b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265",
        PROJECT / "docs/plan/dev-qa-remediation-plan.md": "9c551929df6c1023b1922663b407a9f9428e682f2ae7cd8a414ce4abe608cec7",
        PROJECT / "docs/plan/skill-validations/dev/20260913T2310456388212Z/validation-report.md": "88297dbba18fdc04f31f1d9b3d56e817d0f71ccc9ce0fde8ad2a0dbab6726c64",
        PROJECT / "docs/plan/skill-validations/dev/20260913T2310456388212Z/revision-spec.md": "d4fdb404ebf3e869d4d2b6f99756cf70d54a460a369a74bd3f645f5cb9cfe1b9",
        authoring / "validation-request.json": "034887a39a8b5f12e0ca3bb27e2f87cba48b4f0f74335071ef2baf6b77d525af",
    }
    for path, expected_hash in fixed.items():
        if ref(path)["sha256"] != expected_hash:
            raise ValueError("Pinned input changed: " + str(path))
    records = [authoring / name for name in ("authoring-record.json", "authoring-baseline.json", "validation-request.json", "publication-readback.json")]
    records += [validation / name for name in ("validation-report.md", "assessment.json", "FINAL-RECEIPT.json", "final-artifact-manifest.json", "bundle/artifact-manifest.json")]
    records += [ROOT / name for name in ("remediation-result.md", "implementation-summary.md", "requirement-resource-map.md", "builder-qa/final-result.json", "builder-qa/evaluation-bundle/manifest-v2.json", "builder-qa/evaluation-bundle/FINAL-RECEIPT.json")]
    result = {
        "schema_version": "dev-remediation-closeout-v1",
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "implementation": "DELIVERED",
        "assessment": receipt["assessment"],
        "scenario_counts": receipt["scenario_counts"],
        "package_digest": receipt["target_package_digest"],
        "source_readback": observations,
        "validator_delivered_files_read_back": len(validation_files),
        "pinned_inputs": [ref(path) for path in fixed],
        "records": [ref(path) for path in records],
        "testing": "PERFORMED_WITH_GAPS",
        "installation": "NOT_PERFORMED",
        "framework_acceptance": "NOT_EVALUATED",
        "interpretation": "Both source corrections delivered. Independent assessment outcome and gaps remain authoritative only as evaluation evidence, not framework acceptance. Historical authoring-stage NOT_PERFORMED labels remain unchanged."
    }
    custody.save(ROOT / "FINAL-RESULT.json", result)
    if load(ROOT / "FINAL-RESULT.json") != result:
        raise ValueError("Final result readback mismatch")
    print(json.dumps({"result": ref(ROOT / "FINAL-RESULT.json"), "assessment": result["assessment"], "scenario_counts": result["scenario_counts"], "package_digest": result["package_digest"]}, indent=2))


if __name__ == "__main__":
    main()
