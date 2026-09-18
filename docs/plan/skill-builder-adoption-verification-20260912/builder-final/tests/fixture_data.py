"""Construct bounded synthetic evidence; never import or convert a project skill."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


PACKAGE = Path(__file__).resolve().parents[1]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, data: bytes | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def file_ref(root: Path, path: Path) -> dict:
    return {"path": path.relative_to(root).as_posix(), "sha256": sha(path.read_bytes())}


def files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def baseline_entries(root: Path) -> list[dict]:
    return [{"path": path, "sha256": sha(data)} for path, data in files(root).items()]


def revision_rows(baseline: dict, current: dict, candidate: dict, required: list[str]) -> list[dict]:
    """Fixture oracle expresses the specification's ordered byte comparisons."""
    rows = []
    for path in sorted(set(baseline) | set(current) | set(candidate)):
        b, c, n = baseline.get(path), current.get(path), candidate.get(path)
        owned = path in baseline
        if path in candidate and path in current and not owned:
            action, reason = "CONFLICT", "Proposed path is occupied and unowned."
        elif c == b:
            action, reason = "USE_NEW", "Current equals the previous generated baseline."
        elif c == n:
            action, reason = "KEEP_CURRENT", "Current equals the candidate."
        elif n == b:
            action, reason = "KEEP_CURRENT", "Candidate generation is unchanged."
        else:
            action, reason = "CONFLICT", "Current and candidate both differ from baseline."
        selected = n if action == "USE_NEW" else c
        if path in required and selected is None:
            action, reason = "CONFLICT", "Result would omit a required artifact."
        rows.append({
            "path": path,
            "ownership": "generated" if owned or path in candidate else "retained_user",
            "b_sha256": None if b is None else sha(b),
            "c_sha256": None if c is None else sha(c),
            "n_sha256": None if n is None else sha(n),
            "action": action,
            "reason": reason,
        })
    return rows


def build_revision(root: Path, baseline: dict[str, bytes] | None = None,
                   current: dict[str, bytes] | None = None,
                   candidate: dict[str, bytes] | None = None,
                   *, status: str = "APPLIED", required: list[str] | None = None,
                   advance: bool = False) -> dict:
    baseline = {"SKILL.md": b"Old generated skill.\n"} if baseline is None else baseline
    current = dict(baseline, **{"personal.txt": b"User-owned note.\n"}) if current is None else current
    candidate = {"SKILL.md": b"New generated skill.\n"} if candidate is None else candidate
    required = ["SKILL.md"] if required is None else required
    rows = revision_rows(baseline, current, candidate, required)
    if any(row["action"] == "CONFLICT" for row in rows):
        status = "CONFLICT"
    after = dict(current)
    if status == "APPLIED":
        for row in rows:
            if row["action"] == "USE_NEW":
                if row["path"] in candidate:
                    after[row["path"]] = candidate[row["path"]]
                else:
                    after.pop(row["path"], None)
    directories = {"baseline": baseline, "current": current, "candidate": candidate, "after": after}
    for name, content in directories.items():
        destination = root / "revision" / name
        destination.mkdir(parents=True, exist_ok=True)
        for path, data in content.items():
            write(destination / path, data)
    previous_input = b"Synthetic previous generation: retain the supplied baseline bytes.\n"
    write(root / "revision/previous-input.md", previous_input)
    previous_contract = {
        "schema_version": "1", "mode": "spec_build", "target_name": "synthetic-total",
        "inputs": [{"id": "previous-input", "path": "revision/previous-input.md",
                    "resolved_path": str((root / "revision/previous-input.md").resolve()), "role": "spec",
                    "bytes": len(previous_input), "sha256": sha(previous_input)}],
        "authorization": {"instruction": "Construct the bounded previous-generation byte fixture.",
                          "inputs": [{"id": "previous-input", "sha256": sha(previous_input)}]},
        "purpose": "Exercise historical byte accounting, including empty ownership boundary fixtures.",
        "activation": {"positive": ["Construct the fixture."], "excluded": ["Install a skill."]},
        "requirements": [{"id": "previous-requirement", "origin": "source", "text": previous_input.decode("utf-8").strip(),
                          "source_refs": [{"input_id": "previous-input", "start_byte": 0,
                                           "end_byte": len(previous_input), "sha256": sha(previous_input)}],
                          "artifact_paths": sorted(baseline),
                          "verification": [{"method": "Compare supplied fixture bytes.", "expected": "Baseline byte equality."}]}] if baseline else [],
        "artifacts": [{"path": path, "role": "fixture", "requirement_ids": ["previous-requirement"],
                       "purpose": "Carry the supplied previous-generation bytes."} for path in sorted(baseline)],
        "workers": [], "dependencies": [],
    }
    write_json(root / "revision/previous-contract.json", previous_contract)
    previous_observation = {"schema_version": "1", "run_id": "previous-synthetic-run", "target_name": "synthetic-total",
                            "outputs": baseline_entries(root / "revision/baseline"),
                            "command": "tests/fixture_data.py build_revision",
                            "observations": ["Synthetic fixture construction recorded the supplied previous baseline bytes."]}
    write_json(root / "revision/previous-observation.json", previous_observation)
    prior_provenance = {
        "schema_version": "1", "run_id": "previous-synthetic-run", "result": "COMPLETE",
        "mode": "spec_build", "target_name": "synthetic-total",
        "builder_manifest_sha256": sha((PACKAGE / "evals/build-manifest.json").read_bytes()),
        "contract_sha256": sha((root / "revision/previous-contract.json").read_bytes()),
        "inputs": [{"id": "previous-input", "sha256": sha(previous_input)}], "dependencies": [],
        "outputs": [{"path": path, "ownership": "generated", "sha256": sha(data),
                     "baseline_path": "revision/baseline/" + path, "baseline_sha256": sha(data)}
                    for path, data in sorted(baseline.items())],
        "mappings": [{"requirement_id": "previous-requirement", "artifact_paths": sorted(baseline),
                      "evidence_ids": ["previous-observation"]}] if baseline else [],
        "evidence": [{"id": "previous-observation", **file_ref(root, root / "revision/previous-observation.json")}],
        "prior_build": None,
    }
    write_json(root / "revision/previous-provenance.json", prior_provenance)
    previous = {"schema_version": "1", "run_id": "previous-synthetic-run", "result": "COMPLETE",
                "baseline": baseline_entries(root / "revision/baseline"),
                "provenance": file_ref(root, root / "revision/previous-provenance.json")}
    write_json(root / "revision/previous-build.json", previous)
    pointer = {"run_id": "previous-synthetic-run", "baseline": previous["baseline"]}
    write_json(root / "revision/pointer-before.json", pointer)
    if advance:
        pointer = {"run_id": "synthetic-revision", "baseline": baseline_entries(root / "revision/candidate")}
    write_json(root / "revision/pointer-after.json", pointer)
    plan = {
        "schema_version": "1", "run_id": "synthetic-revision", "status": status,
        **{name: "revision/" + name for name in directories},
        "required_paths": required, "owned_paths": sorted(baseline), "rows": rows,
        "applied_paths": sorted(path for path in set(current) | set(after) if current.get(path) != after.get(path)),
        "baseline_advanced": advance,
        "readback_passed": status == "APPLIED", "evaluation_passed": status == "APPLIED",
        "prior_build": file_ref(root, root / "revision/previous-build.json"),
        "baseline_before": file_ref(root, root / "revision/pointer-before.json"),
        "baseline_after": file_ref(root, root / "revision/pointer-after.json"),
    }
    write_json(root / "revision/revision-plan.json", plan)
    return plan


def build_candidate(root: Path, builder_digest: str) -> dict[str, dict]:
    """Create five-grader inputs and return grader-ID to params mappings.

    The current manifest digest is supplied after the builder is bound. This
    avoids embedding a self-referential digest in the distributed fixture.
    The construction is synthetic evidence, not a model forward trial.
    """
    root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(PACKAGE / "evals/fixtures/portable", root / "portable")
    source = b"# Synthetic requirement\nReturn decimal totals as JSON strings.\n"
    write(root / "trace/input.md", source)
    generated = {
        "SKILL.md": b"---\nname: synthetic-total\ndescription: Report fixture decimal totals.\n---\n\nRead [schema](schema.json).\n",
        "schema.json": b'{"type":"object","required":["total"],"properties":{"total":{"type":"string"}}}\n',
    }
    for path, data in generated.items():
        write(root / "trace/destination" / path, data)
        write(root / "trace/baseline" / path, data)
    input_record = {"id": "spec", "path": "trace/input.md", "resolved_path": str((root / "trace/input.md").resolve()),
                    "role": "spec", "bytes": len(source), "sha256": sha(source)}
    contract = {
        "schema_version": "1", "mode": "spec_build", "target_name": "synthetic-total",
        "inputs": [input_record],
        "authorization": {"instruction": "Build the synthetic fixture capability from the selected input.",
                          "inputs": [{"id": "spec", "sha256": sha(source)}]},
        "purpose": "Exercise byte-accounting evidence using fabricated data.",
        "activation": {"positive": ["Report fixture decimal totals."], "excluded": ["Install a skill."]},
        "requirements": [{"id": "req-0001", "origin": "source", "text": "Return decimal totals as JSON strings.",
                          "source_refs": [{"input_id": "spec", "start_byte": 0, "end_byte": len(source), "sha256": sha(source)}],
                          "artifact_paths": list(generated),
                          "verification": [{"method": "Read generated fixture schema.", "expected": "total is a required string."}]}],
        "artifacts": [{"path": path, "role": "entrypoint" if path == "SKILL.md" else "schema",
                       "requirement_ids": ["req-0001"], "purpose": "Express the synthetic total contract."} for path in generated],
        "workers": [], "dependencies": [],
    }
    write_json(root / "trace/evidence/build-contract.json", contract)
    output_entries = [{"path": path, "sha256": sha(data)} for path, data in generated.items()]
    observation = {"schema_version": "1", "run_id": "synthetic-build", "target_name": "synthetic-total",
                   "outputs": output_entries, "command": "tests/fixture_data.py build_candidate",
                   "observations": ["Synthetic construction recorded the generated fixture bytes; no model conversion was performed."]}
    write_json(root / "trace/evidence/construction-observation.json", observation)
    provenance = {
        "schema_version": "1", "run_id": "synthetic-build", "mode": "spec_build", "target_name": "synthetic-total",
        "builder_manifest_sha256": builder_digest,
        "contract_sha256": sha((root / "trace/evidence/build-contract.json").read_bytes()),
        "inputs": [{"id": "spec", "sha256": sha(source)}], "dependencies": [],
        "outputs": [{**entry, "ownership": "generated", "baseline_path": "trace/baseline/" + entry["path"],
                     "baseline_sha256": entry["sha256"]} for entry in output_entries],
        "mappings": [{"requirement_id": "req-0001", "artifact_paths": list(generated), "evidence_ids": ["construction"]}],
        "evidence": [{"id": "construction", **file_ref(root, root / "trace/evidence/construction-observation.json")}],
        "prior_build": None, "result": "COMPLETE",
    }
    write_json(root / "trace/evidence/build-provenance.json", provenance)
    build_revision(root)
    routes = ["import", "spec_build", "revision", "explanation", "specification_authoring", "installation", "unrelated"]
    records = [{"case_id": "synthetic-route-" + route, "route": route, "request": "Synthetic route fixture: " + route} for route in routes]
    for name in ("expected", "observed"):
        write(root / "routing" / (name + ".jsonl"), "".join(json.dumps(record) + "\n" for record in records))
    return {
        "package_links": {"path": "trace/destination"},
        "manifest_accounting": {"source": "portable/source", "destination": "portable/destination", "evidence": "portable/evidence"},
        "build_traceability": {"evidence": "trace/evidence", "destination": "trace/destination"},
        "revision_consistency": {"path": "revision/revision-plan.json"},
        "routing_outcomes": {"expected": "routing/expected.jsonl", "observed": "routing/observed.jsonl"},
    }
