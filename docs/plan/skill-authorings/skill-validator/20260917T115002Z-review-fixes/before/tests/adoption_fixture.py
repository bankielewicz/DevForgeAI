"""Synthetic custody fixtures, explicitly separate from independent task trials."""
from pathlib import Path
import json

from fixture_data import build_candidate, files, sha, write, write_json, file_ref, revision_rows


def rows(values):
    return [{"path": p, "bytes": len(d), "sha256": sha(d)} for p, d in sorted(values.items())]


def build_adoption(root, content=None, managed=None):
    content = {"SKILL.md": b"An existing skill with a known missing frontmatter defect.\n",
               "notes.txt": b"User-maintained notes.\n"} if content is None else content
    managed = ["SKILL.md"] if managed is None else managed
    evidence = root / "adoption/evidence"
    for path, data in content.items():
        write(evidence / "snapshot" / path, data)
        write(root / "adoption/destination" / path, data)
    spec = b"# Reviewed origin\nRecord the observed existing capability; history is unknown.\n"
    write(evidence / "origin.md", spec)
    write_json(evidence / "snapshot-manifest.json", {"schema_version": "1", "files": rows(content)})
    write_json(evidence / "managed-manifest.json", {"schema_version": "1", "files": rows({p: content[p] for p in managed})})
    target = str((root / "project/src/agents/skills/synthetic-total").resolve())
    readback = {"schema_version": "1", "run_id": "synthetic-adoption", "target_root": target,
                "before": rows(content), "after": rows(content), "spec_before_sha256": sha(spec),
                "spec_after_sha256": sha(spec), "outcome": "UNCHANGED"}
    write_json(evidence / "source-readback.json", readback)
    write_json(evidence / "quality.json", {"quality": "FAILED", "observations": ["Synthetic known defect; custody is separate."]})
    record = {"schema_version": "1", "record_kind": "adoption", "run_id": "synthetic-adoption",
              "target_name": "synthetic-total", "target_root": target, "project_root": str((root / "project").resolve()),
              "captured_at_utc": "2026-09-12T14:00:00Z", "historical_origin": "unknown",
              "snapshot_root": "adoption/evidence/snapshot", "snapshot_manifest": file_ref(root, evidence / "snapshot-manifest.json"),
              "managed_manifest": file_ref(root, evidence / "managed-manifest.json"),
              "managed_paths": sorted(managed), "retained_user_paths": sorted(set(content) - set(managed)),
              "origin_spec": file_ref(root, evidence / "origin.md"),
              "origin_spec_input": {"resolved_path": str((root / "reviewed-origin.md").resolve()), "bytes": len(spec), "sha256": sha(spec)},
              "authorization": {"instruction": "Adopt this synthetic development target using the reviewed origin and selected managed manifest; preserve all bytes and unknown history.",
                                "target_root": target, "managed_manifest_sha256": sha((evidence / "managed-manifest.json").read_bytes()), "origin_spec_sha256": sha(spec)},
              "prior_evidence": [], "quality_evidence": [file_ref(root, evidence / "quality.json")],
              "source_readback": file_ref(root, evidence / "source-readback.json"), "recording_state": "ADOPTED"}
    write_json(evidence / "adoption-record.json", record)
    ref = file_ref(root, evidence / "adoption-record.json")
    pointer = {"schema_version": "2", "run_id": record["run_id"], "target_name": record["target_name"],
               "origin": {"kind": "adopted", **ref}, "baseline": [{"path": p, "sha256": sha(content[p])} for p in sorted(managed)]}
    write_json(evidence / "pointer.json", pointer)
    return record


def build_v2(root, builder_digest, *, current=None, candidate=None, status="APPLIED", advance=False):
    build_candidate(root, builder_digest)
    new = files(root / "trace/baseline") if candidate is None else candidate
    old = dict(new)
    old["SKILL.md"] = b"---\nname: synthetic-total\ndescription: Existing fixture.\n---\nOld behavior.\n"
    content = {**old, "notes.txt": b"User-maintained notes.\n"}
    adoption = build_adoption(root, content, sorted(old))
    current = dict(content) if current is None else current
    # Clean only synthetic files created above, for alternate candidate fixtures.
    for base in (root / "trace/destination", root / "trace/baseline"):
        for path in list(base.rglob("*")):
            if path.is_file():
                path.unlink()
    for p, d in new.items():
        write(root / "trace/baseline" / p, d)
    delta = revision_rows(old, current, new, sorted(new))
    for row in delta:
        if row["path"] in old:
            row["ownership"] = "adopted"
    if any(r["action"] == "CONFLICT" for r in delta):
        status = "CONFLICT"
    after = dict(current)
    if status == "APPLIED":
        for row in delta:
            if row["action"] == "USE_NEW":
                if row["path"] in new:
                    after[row["path"]] = new[row["path"]]
                else:
                    after.pop(row["path"], None)
    for folder, values in (("revision2/baseline", old), ("revision2/current", current), ("trace/destination", after)):
        (root / folder).mkdir(parents=True, exist_ok=True)
        for p, d in values.items():
            write(root / folder / p, d)
    adoption_ref = file_ref(root, root / "adoption/evidence/adoption-record.json")
    prior = {"kind": "adopted", **adoption_ref}
    before = file_ref(root, root / "adoption/evidence/pointer.json")
    write(root / "trace/evidence/pointer-after.json", (root / before["path"]).read_bytes())
    plan = {"schema_version": "2", "run_id": "synthetic-build", "status": status, "baseline": "revision2/baseline",
            "current": "revision2/current", "candidate": "trace/baseline", "after": "trace/destination",
            "required_paths": sorted(new), "owned_paths": sorted(old), "rows": delta,
            "applied_paths": sorted(p for p in set(current) | set(after) if current.get(p) != after.get(p)),
            "baseline_advanced": advance, "readback_passed": status == "APPLIED", "evaluation_passed": status == "APPLIED",
            "prior_origin": prior, "adoption_origin": adoption_ref, "baseline_before": before,
            "baseline_after": file_ref(root, root / "trace/evidence/pointer-after.json")}
    provenance_path = root / "trace/evidence/build-provenance.json"
    provenance = json.loads(provenance_path.read_text())
    provenance.pop("prior_build")
    provenance.update(schema_version="2", prior_origin=prior, adoption_origin=adoption_ref,
                      result="COMPLETE" if status == "APPLIED" else "INCOMPLETE")
    provenance["outputs"] = [{"path": p, "sha256": sha(d), "ownership": "generated" if p in new else "retained_user",
                              "baseline_path": "trace/baseline/" + p if p in new else None,
                              "baseline_sha256": sha(new[p]) if p in new else None} for p, d in sorted(after.items())]
    observation_path = root / "trace/evidence/construction-observation.json"
    observation = json.loads(observation_path.read_text())
    observation["outputs"] = [{"path": p, "sha256": sha(d)} for p, d in sorted(after.items())]
    write_json(observation_path, observation)
    provenance["evidence"][0].update(file_ref(root, observation_path))
    write_json(provenance_path, provenance)
    if advance:
        write_json(root / "trace/evidence/pointer-after.json", {"schema_version": "2", "run_id": plan["run_id"], "target_name": "synthetic-total",
                   "origin": {"kind": "generated", **file_ref(root, provenance_path)}, "baseline": [{"path": p, "sha256": sha(d)} for p, d in sorted(new.items())]})
        plan["baseline_after"] = file_ref(root, root / "trace/evidence/pointer-after.json")
    write_json(root / "trace/evidence/revision-plan.json", plan)
    return plan
