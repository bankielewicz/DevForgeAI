"""Read existing authoring custody only; no skill-quality or product execution."""
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
PROJECT = Path(r"C:\Projects\DevForgeAI")
sys.path.insert(0, str(PROJECT / ".agents/skills/skill-builder/scripts"))
import authoring as custody

RUN = Path(__file__).parent
PRIOR = PROJECT / "docs/plan/skill-authorings/qa/20260914T193851Z"


def main():
    request_path = PRIOR / "validation-request.json"
    request = custody.parse(custody.read_bytes(request_path))
    record = custody.parse(custody.referenced(request["authoring_record"]))
    contract = custody.parse(custody.read_bytes(PRIOR / "contract.json"))
    baseline_ref = custody.reference(PRIOR / "authoring-baseline.json")
    prior_contract = dict(contract, prior=baseline_ref)
    origin, baseline_hashes = custody.origin(prior_contract)
    publication = custody.parse(custody.read_bytes(PRIOR / "publication-readback.json"))
    if publication["request"] != custody.reference(request_path):
        raise ValueError("Existing request no longer matches publication readback")
    manifest = custody.parse(custody.referenced(request["target_manifest"]))
    current = custody.manifest(custody.files(Path(request["target_root"])))
    if current != manifest or current["package_digest"] != request["package_digest"]:
        raise ValueError("Development source differs from published delivery")
    if {row["path"]: row["sha256"] for row in current["files"]} != baseline_hashes:
        raise ValueError("Development source differs from authored baseline")
    references = request["specification_refs"] + record["inputs"]
    for reference in references:
        custody.referenced(reference)
    selected_specs = [custody.reference(PROJECT / "docs/specs" / name) for name in
                      ("qa-skill-postmvp-spec.md", "qa-skill-spec.md")]
    for reference in selected_specs:
        if reference not in request["specification_refs"]:
            raise ValueError("Current selected specification is not bound by request")
    result = {
        "record_kind": "existing_authoring_readback",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "request": "$skill-builder C:\\Projects\\DevForgeAI\\docs\\specs\\qa-skill-postmvp-spec.md",
        "disposition": "EXISTING_AUTHORED_DELIVERY_UNCHANGED",
        "project_root": str(PROJECT),
        "target_root": request["target_root"],
        "prior_origin": origin,
        "selected_specs": selected_specs,
        "package_manifest": current,
        "validation_request": custody.reference(request_path),
        "bound_references_read": len(references),
        "changed_package_paths": [],
        "omissions": [],
        "review": "Read entry, four references, three templates, UI metadata and existing requirement mapping. Requested post-MVP instructions already present; no new authoring delta identified. This records byte custody, not skill quality.",
        "validation": "NOT_PERFORMED",
        "testing": "NOT_PERFORMED",
        "framework_acceptance": "NOT_EVALUATED",
        "command": "python -B -X utf8 docs/plan/skill-authorings/qa/20260914T2000129113921Z-readback/readback.py",
        "cwd": str(Path.cwd()),
        "python": sys.version,
        "host": platform.platform(),
        "script": custody.reference(Path(__file__)),
    }
    output = RUN / "readback.json"
    custody.save(output, result)
    if custody.parse(custody.read_bytes(output)) != result:
        raise ValueError("Receipt readback differs")
    print(json.dumps({"receipt": custody.reference(output), "disposition": result["disposition"],
                      "package_digest": current["package_digest"],
                      "validation_request": result["validation_request"]}, indent=2))


if __name__ == "__main__":
    main()
