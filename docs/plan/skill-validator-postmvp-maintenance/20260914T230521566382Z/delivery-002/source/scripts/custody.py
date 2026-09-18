"""Legacy custody and record readers extracted from builder 2.0.0. No quality grader or dispatcher."""

import hashlib

import json

import math

import re

import stat

from pathlib import Path, PurePosixPath

from urllib.parse import unquote, urlsplit

VERSION = "2.0.0"

MAX_BYTES = 32 * 1024 * 1024

MAX_FILES = 2000

def digest(data):
    return hashlib.sha256(data).hexdigest()

def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    def constant(value):
        raise ValueError("non-finite JSON value: " + value)

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("non-finite JSON value: " + value)
        return number

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant, parse_float=finite_float)

def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400
    )

def bounded_path(root, relative, allow_dot=False):
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise ValueError("expected a forward-slash relative path")
    parts = PurePosixPath(relative).parts
    if relative == "." and allow_dot:
        return root
    if not parts or any(p in ("..", ".") for p in relative.split("/")) or relative.startswith("/"):
        raise ValueError("unsafe relative path: " + relative)
    current = root
    for part in parts:
        if part.casefold() in ("backup", "backups"):
            raise ValueError("excluded backup boundary: " + relative)
        current = current / part
        if current.exists() or current.is_symlink():
            if is_link(current):
                raise ValueError("link/reparse boundary: " + relative)
    if not current.resolve().is_relative_to(root.resolve()):
        raise ValueError("path escapes root: " + relative)
    return current

def snapshot(root):
    if not root.is_dir() or is_link(root):
        raise ValueError("snapshot root must be a regular directory")
    files = {}
    total = 0

    def walk(directory):
        nonlocal total
        for item in sorted(directory.iterdir(), key=lambda p: p.name):
            rel = item.relative_to(root).as_posix()
            if item.name.casefold() in ("backup", "backups"):
                raise ValueError("excluded backup boundary: " + rel)
            if is_link(item):
                raise ValueError("link/reparse boundary: " + rel)
            if item.is_dir():
                walk(item)
            elif item.is_file():
                size = item.stat().st_size
                if len(files) >= MAX_FILES or total + size > MAX_BYTES:
                    raise ValueError("snapshot exceeds 2000 files or 32 MiB")
                data = item.read_bytes()
                total += len(data)
                if total > MAX_BYTES:
                    raise ValueError("snapshot exceeds 32 MiB")
                files[rel] = data
            else:
                raise ValueError("non-regular snapshot entry: " + rel)

    walk(root)
    return files


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= set(value) or set(value) - set(required) - set(optional):
        raise ValueError("invalid object fields; required: " + ", ".join(sorted(required)))
    return value

def nonempty(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected nonempty string")
    return value

def sha(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("expected lowercase SHA-256")
    return value

def strings(value, allow_empty=True):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value) or len(set(value)) != len(value) or (not allow_empty and not value):
        raise ValueError("expected unique nonempty strings")
    return value

def objects(value):
    if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
        raise ValueError("expected object array")
    return value

def indexed(rows, key):
    result = {}
    for row in objects(rows):
        ident = nonempty(row[key])
        if ident in result:
            raise ValueError("duplicate " + key + ": " + ident)
        result[ident] = row
    return result

def read_snapshot_json(root, files, path):
    bounded_path(root, path)
    return strict_json(files[path].decode("utf-8-sig"))

def hash_rows(rows):
    result = {}
    for row in objects(rows):
        fields(row, {"path", "sha256"})
        path = nonempty(row["path"])
        if path in result:
            raise ValueError("duplicate output path")
        result[path] = sha(row["sha256"])
    return result

def prior_provenance_record(value, _version="1"):
    """Check one historical record without rebasing paths or following history."""
    fields(value, {"schema_version", "run_id", "mode", "target_name", "builder_manifest_sha256",
                   "contract_sha256", "inputs", "dependencies", "outputs", "mappings", "evidence",
                   "result"} | ({"prior_build"} if _version == "1" else {"prior_origin", "adoption_origin"}))
    if value["schema_version"] != _version or value["mode"] not in ("import", "spec_build") or value["result"] != "COMPLETE":
        raise ValueError("previous provenance requires selected schema and a complete supported build mode")
    nonempty(value["run_id"])
    target = nonempty(value["target_name"])
    if len(target) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", target):
        raise ValueError("invalid previous provenance target_name")
    sha(value["builder_manifest_sha256"])
    sha(value["contract_sha256"])
    objects(value["dependencies"])

    def historical_path(path):
        # These strings refer to the preceding snapshot. No historical root
        # locator exists in schema 1, so do not resolve them in the new root.
        nonempty(path)
        if "\\" in path or ":" in path or path.startswith("/") or any(part in ("", ".", "..") for part in path.split("/")):
            raise ValueError("unsafe previous provenance path")
        if any(part.casefold() in ("backup", "backups") for part in path.split("/")):
            raise ValueError("excluded previous provenance path")
        return path

    def reference(row):
        fields(row, {"path", "sha256"})
        historical_path(row["path"])
        sha(row["sha256"])

    inputs = indexed(value["inputs"], "id")
    if not inputs:
        raise ValueError("previous provenance requires input records")
    for row in inputs.values():
        fields(row, {"id", "sha256"})
        sha(row["sha256"])

    generated = {}
    for path, row in indexed(value["outputs"], "path").items():
        fields(row, {"path", "sha256", "ownership", "baseline_path", "baseline_sha256"})
        historical_path(path)
        sha(row["sha256"])
        if row["ownership"] == "generated":
            historical_path(row["baseline_path"])
            generated[path] = sha(row["baseline_sha256"])
        elif row["ownership"] != "retained_user" or row["baseline_path"] is not None or row["baseline_sha256"] is not None:
            raise ValueError("invalid previous provenance ownership or baseline fields")

    evidence = indexed(value["evidence"], "id")
    for row in evidence.values():
        fields(row, {"id", "path", "sha256"})
        historical_path(row["path"])
        sha(row["sha256"])
    mappings = indexed(value["mappings"], "requirement_id")
    if generated and not mappings:
        raise ValueError("previous generated outputs require provenance mappings")
    for row in mappings.values():
        fields(row, {"requirement_id", "artifact_paths", "evidence_ids"})
        paths = strings(row["artifact_paths"], False)
        for path in paths:
            historical_path(path)
        if not set(paths) <= set(generated):
            raise ValueError("previous provenance mapping references an unknown generated output")
        if not set(strings(row["evidence_ids"], False)) <= set(evidence):
            raise ValueError("previous provenance mapping references unknown evidence")
    if _version == "2":
        reference(value["adoption_origin"])
        typed = fields(value["prior_origin"], {"kind", "path", "sha256"})
        if typed["kind"] not in ("adopted", "generated"):
            raise ValueError("unknown previous origin kind")
        reference({k: typed[k] for k in ("path", "sha256")})
    elif value["prior_build"] is not None:
        reference(value["prior_build"])
    return generated

def reference_json(root, files, ref, problems, typed=False):
    fields(ref, {"path", "sha256"} | ({"kind"} if typed else set()))
    if typed and ref["kind"] not in ("adopted", "generated"):
        raise ValueError("unknown origin kind")
    value = read_snapshot_json(root, files, ref["path"])
    if sha(ref["sha256"]) != digest(files[ref["path"]]):
        problems.append("reference digest mismatch: " + ref["path"])
    return value

def observed_rows(root, rows):
    """Strict, normalized, sorted size/hash manifest rows."""
    entries = {}
    for row in objects(rows):
        fields(row, {"path", "bytes", "sha256"})
        path = nonempty(row["path"])
        bounded_path(root, path)
        if PurePosixPath(path).as_posix() != path or path in entries:
            raise ValueError("duplicate or non-normalized observed path")
        if type(row["bytes"]) is not int or row["bytes"] < 0:
            raise ValueError("invalid observed byte count")
        entries[path] = (row["bytes"], sha(row["sha256"]))
    if list(entries) != sorted(entries):
        raise ValueError("observed rows must be sorted")
    return entries

ADOPTION_FIELDS = {"schema_version", "record_kind", "run_id", "target_name", "target_root", "project_root",
                   "captured_at_utc", "historical_origin", "snapshot_root", "snapshot_manifest",
                   "managed_paths", "retained_user_paths", "origin_spec", "authorization", "prior_evidence",
                   "quality_evidence", "source_readback", "recording_state", "managed_manifest", "origin_spec_input"}

def adoption_record(root, files, record, problems):
    fields(record, ADOPTION_FIELDS, {"known_defects", "handoff"})
    if record["schema_version"] != "1" or record["record_kind"] != "adoption" or record["historical_origin"] != "unknown":
        raise ValueError("adoption requires typed schema 1 and unknown historical origin")
    if record["recording_state"] not in ("ADOPTED", "INCOMPLETE"):
        raise ValueError("invalid adoption recording state")
    for key in ("run_id", "target_name", "target_root", "project_root", "captured_at_utc"):
        nonempty(record[key])
    # Original paths identify custody but never become filesystem read locators.
    project = record["project_root"].replace("\\", "/").rstrip("/")
    target = record["target_root"].replace("\\", "/").rstrip("/")
    name = record["target_name"]
    if any(part in ("", ".", "..") for part in name.split("/")) or "/" in name or "\\" in name or ":" in name:
        raise ValueError("invalid observed target identity")
    if target != project + "/src/agents/skills/" + name or not (Path(record["project_root"]).is_absolute()):
        raise ValueError("adoption target must identify the selected development directory")
    from datetime import datetime
    stamp = datetime.fromisoformat(record["captured_at_utc"].replace("Z", "+00:00"))
    if stamp.utcoffset() is None or stamp.utcoffset().total_seconds() != 0:
        raise ValueError("capture timestamp must be UTC")
    folder = bounded_path(root, record["snapshot_root"])
    if not folder.is_dir():
        raise ValueError("adoption snapshot directory missing")
    prefix = record["snapshot_root"] + "/"
    actual = {p[len(prefix):]: (len(d), digest(d)) for p, d in files.items() if p.startswith(prefix)}
    manifest = reference_json(root, files, record["snapshot_manifest"], problems)
    fields(manifest, {"schema_version", "files"})
    managed_manifest = reference_json(root, files, record["managed_manifest"], problems)
    fields(managed_manifest, {"schema_version", "files"})
    if manifest["schema_version"] != "1" or managed_manifest["schema_version"] != "1":
        raise ValueError("unsupported adoption manifest schema")
    if observed_rows(root, manifest["files"]) != actual:
        problems.append("adoption snapshot manifest differs from observed bytes")
    managed = strings(record["managed_paths"], False)
    retained = strings(record["retained_user_paths"])
    for paths in (managed, retained):
        if paths != sorted(paths):
            raise ValueError("adoption path partition must be sorted")
        for path in paths:
            bounded_path(root, path)
    if set(managed) & set(retained) or set(managed) | set(retained) != set(actual):
        problems.append("managed/retained paths do not partition the snapshot")
    measured_managed = {p: actual[p] for p in managed if p in actual}
    if observed_rows(root, managed_manifest["files"]) != measured_managed:
        problems.append("managed manifest does not match authorized observed subset")
    spec = fields(record["origin_spec"], {"path", "sha256"})
    bounded_path(root, spec["path"])
    if sha(spec["sha256"]) != digest(files[spec["path"]]):
        problems.append("origin specification digest mismatch")
    metadata = fields(record["origin_spec_input"], {"resolved_path", "bytes", "sha256"})
    nonempty(metadata["resolved_path"])
    if type(metadata["bytes"]) is not int or metadata["bytes"] < 0:
        raise ValueError("invalid origin specification byte count")
    if (metadata["bytes"], sha(metadata["sha256"])) != (len(files[spec["path"]]), spec["sha256"]):
        problems.append("origin specification input metadata mismatch")
    auth = fields(record["authorization"], {"instruction", "target_root", "managed_manifest_sha256", "origin_spec_sha256"})
    nonempty(auth["instruction"])
    if auth["target_root"] != record["target_root"] or sha(auth["managed_manifest_sha256"]) != record["managed_manifest"]["sha256"] or sha(auth["origin_spec_sha256"]) != spec["sha256"]:
        problems.append("adoption authorization identity/selection/digest mismatch")
    for key in ("prior_evidence", "quality_evidence"):
        seen = set()
        for ref in objects(record[key]):
            fields(ref, {"path", "sha256"})
            bounded_path(root, ref["path"])
            if ref["path"] in seen:
                raise ValueError("duplicate evidence reference")
            seen.add(ref["path"])
            if sha(ref["sha256"]) != digest(files[ref["path"]]):
                problems.append(key + " digest mismatch")
    readback = reference_json(root, files, record["source_readback"], problems)
    fields(readback, {"schema_version", "run_id", "target_root", "before", "after", "spec_before_sha256", "spec_after_sha256", "outcome"})
    if readback["schema_version"] != "1":
        raise ValueError("unsupported source readback schema")
    if readback["run_id"] != record["run_id"] or readback["target_root"] != record["target_root"]:
        problems.append("source readback identity mismatch")
    if observed_rows(root, readback["before"]) != actual or observed_rows(root, readback["after"]) != actual:
        problems.append("SOURCE_CHANGED: source readback differs from snapshot")
    if sha(readback["spec_before_sha256"]) != spec["sha256"] or sha(readback["spec_after_sha256"]) != spec["sha256"] or readback["outcome"] != "UNCHANGED":
        problems.append("SOURCE_CHANGED: specification/readback mismatch")
    if record["recording_state"] != "ADOPTED":
        problems.append("adoption recording is incomplete")
    if "known_defects" in record:
        strings(record["known_defects"])
    if "handoff" in record:
        verify_handoff(root, files, record["handoff"], record, problems)
    return {p: value[1] for p, value in measured_managed.items()}

def verify_handoff(root, files, ref, record, problems):
    """A selected input packet is byte-bound evidence, never repair authority."""
    packet = reference_json(root, files, ref, problems)
    fields(packet, {"schema_version", "target_root", "target_manifest_sha256", "managed_manifest_sha256",
                    "origin_spec_sha256", "review_policy", "review_state", "selected_references", "builder_readiness"})
    if packet["schema_version"] != "1" or packet["review_policy"] != "review-before-repair":
        raise ValueError("unsupported handoff schema or review policy")
    nonempty(packet["builder_readiness"])
    if packet["review_state"] != "reviewed" or packet["target_root"] != record["target_root"]:
        problems.append("handoff review/target identity mismatch")
    for key, expected in (("target_manifest_sha256", record["snapshot_manifest"]["sha256"]),
                          ("managed_manifest_sha256", record["managed_manifest"]["sha256"]),
                          ("origin_spec_sha256", record["origin_spec"]["sha256"])):
        if sha(packet[key]) != expected:
            problems.append("handoff selected digest mismatch: " + key)
    if not objects(packet["selected_references"]):
        raise ValueError("handoff must select its report/findings/specification references")
    for selected in packet["selected_references"]:
        fields(selected, {"path", "sha256"})
        bounded_path(root, selected["path"])
        if sha(selected["sha256"]) != digest(files[selected["path"]]):
            problems.append("handoff selected reference digest mismatch")

def pointer_record(root, files, pointer, problems):
    fields(pointer, {"schema_version", "run_id", "target_name", "origin", "baseline"})
    if pointer["schema_version"] != "2":
        raise ValueError("origin pointer requires schema 2")
    nonempty(pointer["run_id"])
    nonempty(pointer["target_name"])
    origin = reference_json(root, files, pointer["origin"], problems, typed=True)
    if origin["run_id"] != pointer["run_id"] or origin["target_name"] != pointer["target_name"]:
        problems.append("pointer origin identity mismatch")
    rows = hash_rows(pointer["baseline"])
    for path in rows:
        bounded_path(root, path)
    return origin, rows

def generated_origin_record(root, files, origin, adoption_ref, problems, origin_path):
    fields(origin, {"schema_version", "run_id", "mode", "target_name", "builder_manifest_sha256", "contract_sha256",
                    "inputs", "dependencies", "outputs", "mappings", "evidence", "prior_origin", "adoption_origin", "result"})
    if origin["schema_version"] != "2" or origin["mode"] != "spec_build" or origin["result"] != "COMPLETE":
        raise ValueError("generated adoption lineage requires COMPLETE schema 2 spec_build provenance")
    fields(origin["prior_origin"], {"kind", "path", "sha256"})
    if origin["prior_origin"]["kind"] not in ("adopted", "generated"):
        raise ValueError("unknown previous origin kind")
    fields(origin["adoption_origin"], {"path", "sha256"})
    if origin["adoption_origin"] != adoption_ref:
        problems.append("generated lineage changed its original adoption reference")
    generated = prior_provenance_record(origin, "2")
    preceding = reference_json(root, files, origin["prior_origin"], problems, typed=True)
    if preceding.get("target_name") != origin["target_name"]:
        problems.append("generated prior-origin target identity mismatch")
    if origin["prior_origin"]["kind"] == "adopted":
        if {k: origin["prior_origin"][k] for k in ("path", "sha256")} != adoption_ref:
            problems.append("generated first revision changed adopted origin")
    else:
        prior_provenance_record(preceding, "2")
        if preceding["adoption_origin"] != adoption_ref:
            problems.append("preceding generated origin changed adoption lineage")
    contract_path = (PurePosixPath(origin_path).parent / "build-contract.json").as_posix()
    contract = read_snapshot_json(root, files, contract_path)
    if digest(files[contract_path]) != origin["contract_sha256"] or contract.get("schema_version") != "1" or contract.get("mode") != "spec_build" or contract.get("target_name") != origin["target_name"]:
        problems.append("historical generated contract identity/digest mismatch")
    auth = fields(contract["authorization"], {"instruction", "inputs"})
    nonempty(auth["instruction"])
    authorized_inputs = {i: sha(r["sha256"]) for i, r in indexed(auth["inputs"], "id").items()}
    captured_inputs = {}
    for ident, row in indexed(contract["inputs"], "id").items():
        fields(row, {"id", "path", "resolved_path", "role", "bytes", "sha256"})
        bounded_path(root, row["path"])
        data = files[row["path"]]
        captured_inputs[ident] = sha(row["sha256"])
        if type(row["bytes"]) is not int or (len(data), digest(data)) != (row["bytes"], row["sha256"]):
            problems.append("historical generated input byte mismatch")
    if not captured_inputs or captured_inputs != authorized_inputs or captured_inputs != {r["id"]: r["sha256"] for r in origin["inputs"]}:
        problems.append("historical generated authorization/input selection mismatch")
    if set(indexed(contract["artifacts"], "path")) != set(generated):
        problems.append("historical generated ownership not justified by contract")
    for row in origin["outputs"]:
        if row["ownership"] == "generated":
            bounded_path(root, row["baseline_path"])
            if digest(files[row["baseline_path"]]) != row["baseline_sha256"]:
                problems.append("historical generated baseline bytes changed")
    for row in origin["evidence"]:
        data = reference_json(root, files, {k: row[k] for k in ("path", "sha256")}, problems)
        measured = hash_rows(data["outputs"])
        outputs = {r["path"]: r["sha256"] for r in origin["outputs"]}
        if data.get("schema_version") != "1" or data.get("run_id") != origin["run_id"] or data.get("target_name") != origin["target_name"] or any(outputs.get(p) != d for p, d in measured.items()):
            problems.append("historical generated observation identity/output mismatch")
    return generated

def revision_origin(root, files, plan, problems):
    if plan.get("schema_version") != "2":
        raise ValueError("adoption revision requires schema 2 plan")
    adopted = reference_json(root, files, plan["adoption_origin"], problems)
    adopted_baseline = adoption_record(root, files, adopted, problems)
    origin = reference_json(root, files, plan["prior_origin"], problems, typed=True)
    if plan["prior_origin"]["kind"] == "adopted":
        if {k: plan["prior_origin"][k] for k in ("path", "sha256")} != plan["adoption_origin"]:
            problems.append("first revision origin differs from adoption origin")
        baseline = adopted_baseline
    else:
        baseline = generated_origin_record(root, files, origin, plan["adoption_origin"], problems, plan["prior_origin"]["path"])
    before = reference_json(root, files, plan["baseline_before"], problems)
    pointer_origin, pointer_baseline = pointer_record(root, files, before, problems)
    if before["origin"] != plan["prior_origin"] or pointer_baseline != baseline or origin["target_name"] != adopted["target_name"]:
        problems.append("published-before pointer does not bind selected origin/target/baseline")
    return origin, baseline
