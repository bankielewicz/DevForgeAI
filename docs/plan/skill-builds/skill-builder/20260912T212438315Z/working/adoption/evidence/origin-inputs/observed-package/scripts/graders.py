"""Deterministic observations only; no DevForgeAI state or acceptance authority."""

import hashlib
import json
import math
import re
import stat
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

VERSION = "2.0.0"
GRADER_IDS = ("package_links", "manifest_accounting", "build_traceability", "revision_consistency", "routing_outcomes",
              "adoption_consistency", "build_traceability_v2", "revision_consistency_v2", "routing_outcomes_v2")
BUILD_MANIFEST_SHA256 = None  # Injected only after the runner verifies these bytes.
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


def result(problems, files):
    return {
        "status": "FAIL" if problems else "PASS",
        "observations": problems or ["No discrepancy in the measured properties."],
        "candidate_digests": {name: digest(data) for name, data in sorted(files.items())},
    }


def package_links(root, params):
    if set(params) != {"path"}:
        raise ValueError("package_links requires only path")
    folder = bounded_path(root, params["path"], allow_dot=True)
    files = snapshot(folder)
    problems = []
    if "SKILL.md" not in files:
        problems.append("Missing SKILL.md")
    for name, data in files.items():
        if not name.lower().endswith(".md"):
            continue
        content = data.decode("utf-8-sig")
        # This grader covers ordinary Markdown links, not HTML or code examples.
        content = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", content)
        content = re.sub(r"`[^`\n]*`", "", content)
        definitions = dict(re.findall(r"(?m)^\s*\[([^\]]+)\]:\s*<?([^\s>]+)>?", content))
        definitions = {key.casefold(): value for key, value in definitions.items()}
        links = re.findall(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", content)
        for label, reference in re.findall(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", content):
            key = (reference or label).casefold()
            if key not in definitions:
                problems.append(name + ": undefined reference " + key)
            else:
                links.append(definitions[key])
        links.extend(definitions.values())
        for raw in links:
            url = urlsplit(raw.strip("<>"))
            if url.scheme in ("http", "https", "mailto") or (not url.path and not url.netloc):
                continue
            if url.scheme or url.netloc:
                problems.append(name + ": unsupported link " + raw)
                continue
            relative = unquote(url.path)
            if "\\" in relative or ":" in relative or relative.startswith("/"):
                problems.append(name + ": unsafe link " + raw)
                continue
            target = (folder / PurePosixPath(name).parent / relative).resolve()
            if not target.is_relative_to(folder.resolve()):
                problems.append(name + ": escaping link " + raw)
            elif target.relative_to(folder.resolve()).as_posix() not in files:
                problems.append(name + ": missing file link " + raw)
    prefix = "" if params["path"] == "." else params["path"] + "/"
    return result(problems, {prefix + key: value for key, value in files.items()})


def manifest_entries(value):
    if not isinstance(value, dict) or value.get("schema_version") != "1" or not isinstance(value.get("files"), list):
        raise ValueError("manifest requires schema_version 1 and files array")
    entries = {}
    for entry in value["files"]:
        name = entry["path"]
        if not isinstance(name, str) or name in entries:
            raise ValueError("invalid or duplicate manifest path")
        if type(entry["bytes"]) is not int or entry["bytes"] < 0:
            raise ValueError("invalid manifest byte count")
        if not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            raise ValueError("invalid manifest digest")
        entries[name] = (entry["bytes"], entry["sha256"])
    return entries


def manifest_accounting(root, params):
    if set(params) != {"source", "destination", "evidence"}:
        raise ValueError("manifest_accounting requires source, destination, evidence")
    folders = {key: bounded_path(root, value) for key, value in params.items()}
    resolved = list(folders.values())
    if any(a == b or a.is_relative_to(b) or b.is_relative_to(a) for i, a in enumerate(resolved) for b in resolved[i + 1:]):
        raise ValueError("source, destination and evidence must be disjoint")
    inventories = {key: snapshot(path) for key, path in folders.items()}
    evidence = inventories["evidence"]
    before = manifest_entries(strict_json(evidence["source-manifest.json"].decode("utf-8-sig")))
    destination = manifest_entries(strict_json(evidence["destination-manifest.json"].decode("utf-8-sig")))
    dispositions = strict_json(evidence["file-dispositions.json"].decode("utf-8-sig"))
    if not isinstance(dispositions, dict) or dispositions.get("schema_version") != "1" or not isinstance(dispositions.get("files"), list):
        raise ValueError("dispositions require schema_version 1 and files array")
    problems = []
    for key, expected in (("source", before), ("destination", destination)):
        actual = {name: (len(data), digest(data)) for name, data in inventories[key].items()}
        if actual != expected:
            problems.append(key + " bytes or file set differs from manifest")
    seen = set()
    for entry in dispositions["files"]:
        name = entry["source_path"]
        if name in seen or name not in before:
            problems.append("duplicate or unknown disposition: " + str(name))
            continue
        seen.add(name)
        if entry["source_sha256"] != before[name][1]:
            problems.append("disposition source digest mismatch: " + name)
        action, targets = entry["disposition"], entry["target_paths"]
        if action not in ("PRESERVE", "REWRITE", "CONSOLIDATE", "OMIT", "DEFER"):
            raise ValueError("unknown disposition")
        if not isinstance(targets, list) or any(not isinstance(t, str) for t in targets) or len(targets) != len(set(targets)):
            raise ValueError("target_paths must contain unique strings")
        if bool(targets) != (action not in ("OMIT", "DEFER")):
            problems.append("disposition target count mismatch: " + name)
        for target in targets:
            if target not in destination:
                problems.append("disposition target absent: " + target)
            elif action == "PRESERVE" and before[name] != destination[target]:
                problems.append("PRESERVE byte mismatch: " + name + " -> " + target)
    if seen != set(before):
        problems.append("source files missing dispositions")
    all_files = {params[key] + "/" + name: data for key, files in inventories.items() for name, data in files.items()}
    return result(problems, all_files)


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


def build_traceability(root, params, _version="1"):
    fields(params, {"evidence", "destination"})
    evidence_dir = bounded_path(root, params["evidence"])
    destination_dir = bounded_path(root, params["destination"])
    if evidence_dir == destination_dir or evidence_dir.is_relative_to(destination_dir) or destination_dir.is_relative_to(evidence_dir):
        raise ValueError("evidence and destination must be disjoint")
    files = snapshot(root)
    contract_path = params["evidence"] + "/build-contract.json"
    provenance_path = params["evidence"] + "/build-provenance.json"
    contract = read_snapshot_json(root, files, contract_path)
    provenance = read_snapshot_json(root, files, provenance_path)
    fields(contract, {"schema_version", "mode", "target_name", "inputs", "authorization", "purpose", "activation", "requirements", "artifacts", "workers", "dependencies"})
    origin_fields = {"prior_build"} if _version == "1" else {"prior_origin", "adoption_origin"}
    fields(provenance, {"schema_version", "run_id", "mode", "target_name", "builder_manifest_sha256", "contract_sha256", "inputs", "dependencies", "outputs", "mappings", "evidence", "result"} | origin_fields)
    if contract["schema_version"] != "1" or provenance["schema_version"] != _version or contract["mode"] not in ("import", "spec_build") or provenance["result"] not in ("COMPLETE", "INCOMPLETE"):
        raise ValueError("unsupported contract/provenance version, mode or result")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", nonempty(contract["target_name"])) or len(contract["target_name"]) > 64:
        raise ValueError("invalid target_name")
    nonempty(provenance["run_id"])
    nonempty(contract["purpose"])
    fields(contract["activation"], {"positive", "excluded"})
    strings(contract["activation"]["positive"], False)
    strings(contract["activation"]["excluded"])
    objects(contract["workers"])
    objects(contract["dependencies"])
    problems = []
    if provenance["mode"] != contract["mode"] or provenance["target_name"] != contract["target_name"]:
        problems.append("provenance identity differs from contract")
    if sha(provenance["contract_sha256"]) != digest(files[contract_path]):
        problems.append("contract digest mismatch")
    if BUILD_MANIFEST_SHA256 is not None and sha(provenance["builder_manifest_sha256"]) != BUILD_MANIFEST_SHA256:
        problems.append("builder manifest digest differs from running evaluator")
    else:
        sha(provenance["builder_manifest_sha256"])
    if provenance["dependencies"] != contract["dependencies"]:
        problems.append("dependency recording differs from contract")
    inputs = indexed(contract["inputs"], "id")
    if not inputs:
        raise ValueError("contract requires at least one input")
    input_bytes, input_hashes = {}, {}
    for ident, row in inputs.items():
        fields(row, {"id", "path", "resolved_path", "role", "bytes", "sha256"})
        nonempty(row["resolved_path"])
        nonempty(row["role"])
        path = bounded_path(root, row["path"])
        if path.is_relative_to(destination_dir):
            raise ValueError("input cannot be inside destination")
        if type(row["bytes"]) is not int or row["bytes"] < 0:
            raise ValueError("invalid input byte count")
        input_bytes[ident] = files[row["path"]]
        input_hashes[ident] = sha(row["sha256"])
        if (len(input_bytes[ident]), digest(input_bytes[ident])) != (row["bytes"], row["sha256"]):
            problems.append("input bytes changed: " + ident)
    fields(contract["authorization"], {"instruction", "inputs"})
    nonempty(contract["authorization"]["instruction"])
    for label, rows in (("authorization", contract["authorization"]["inputs"]), ("provenance", provenance["inputs"])):
        recorded = {}
        for ident, row in indexed(rows, "id").items():
            fields(row, {"id", "sha256"})
            recorded[ident] = sha(row["sha256"])
        if recorded != input_hashes:
            problems.append(label + " input identity/digest mismatch")
    requirements = indexed(contract["requirements"], "id")
    artifacts = indexed(contract["artifacts"], "path")
    if not requirements or not artifacts or "SKILL.md" not in artifacts:
        raise ValueError("nonempty requirements and artifacts including SKILL.md required")
    for ident, row in requirements.items():
        fields(row, {"id", "origin", "text", "source_refs", "artifact_paths", "verification"}, {"rationale"})
        nonempty(row["text"])
        if row["origin"] not in ("source", "derived"):
            raise ValueError("unknown requirement origin")
        if row["origin"] == "derived":
            nonempty(row.get("rationale"))
        refs = objects(row["source_refs"])
        if row["origin"] == "source" and not refs:
            raise ValueError("source requirement lacks source reference")
        for ref in refs:
            fields(ref, {"input_id", "start_byte", "end_byte", "sha256"})
            if ref["input_id"] not in input_bytes:
                problems.append("unknown source input: " + str(ref["input_id"]))
                continue
            start, end = ref["start_byte"], ref["end_byte"]
            data = input_bytes[ref["input_id"]]
            if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(data):
                problems.append("invalid source byte range: " + ident)
            elif sha(ref["sha256"]) != digest(data[start:end]):
                problems.append("source excerpt digest mismatch: " + ident)
        for path in strings(row["artifact_paths"], False):
            bounded_path(destination_dir, path)
            if path not in artifacts:
                problems.append("requirement references unknown artifact: " + path)
        if not objects(row["verification"]):
            raise ValueError("requirement verification is empty")
        for verification in row["verification"]:
            fields(verification, {"method", "expected"})
            nonempty(verification["method"])
            nonempty(verification["expected"])
    for path, row in artifacts.items():
        fields(row, {"path", "role", "requirement_ids", "purpose"})
        bounded_path(destination_dir, path)
        nonempty(row["role"])
        nonempty(row["purpose"])
        declared = set(strings(row["requirement_ids"], False))
        reverse = {ident for ident, req in requirements.items() if path in req["artifact_paths"]}
        if declared != reverse:
            problems.append("artifact requirement mapping mismatch: " + path)
    prefix = params["destination"] + "/"
    actual_outputs = {path[len(prefix):]: digest(data) for path, data in files.items() if path.startswith(prefix)}
    output_rows = indexed(provenance["outputs"], "path")
    output_hashes = {}
    for path, row in output_rows.items():
        fields(row, {"path", "sha256", "ownership", "baseline_path", "baseline_sha256"})
        bounded_path(destination_dir, path)
        output_hashes[path] = sha(row["sha256"])
        if row["ownership"] == "generated":
            bounded_path(root, row["baseline_path"])
            if row["baseline_path"].startswith(prefix):
                raise ValueError("generated baseline must be separate from destination")
            if row["baseline_path"] not in files or digest(files[row["baseline_path"]]) != sha(row["baseline_sha256"]):
                problems.append("generated baseline digest mismatch: " + path)
        elif row["ownership"] != "retained_user" or row["baseline_path"] is not None or row["baseline_sha256"] is not None:
            raise ValueError("invalid ownership or retained-user baseline")
    if actual_outputs != output_hashes:
        problems.append("destination output set or digests differ from provenance")
    if not set(artifacts) <= set(actual_outputs):
        problems.append("required artifact is missing")
    if any(output_rows.get(path, {}).get("ownership") != "generated" for path in artifacts):
        problems.append("required artifact lacks generated ownership")
    evidence = indexed(provenance["evidence"], "id")
    evidence_outputs = {}
    for ident, row in evidence.items():
        fields(row, {"id", "path", "sha256"})
        data = read_snapshot_json(root, files, row["path"])
        if sha(row["sha256"]) != digest(files[row["path"]]):
            problems.append("cited evidence digest mismatch: " + ident)
        if not isinstance(data, dict) or data.get("schema_version") != "1":
            raise ValueError("cited evidence requires schema version 1 object")
        if data.get("run_id") != provenance["run_id"] or data.get("target_name") != contract["target_name"]:
            problems.append("cited evidence run/package mismatch: " + ident)
        evidence_outputs[ident] = hash_rows(data["outputs"])
        for path, expected in evidence_outputs[ident].items():
            if actual_outputs.get(path) != expected:
                problems.append("cited evidence output digest mismatch: " + path)
    mappings = indexed(provenance["mappings"], "requirement_id")
    if set(mappings) != set(requirements):
        problems.append("provenance requirement mapping set mismatch")
    for ident, row in mappings.items():
        fields(row, {"requirement_id", "artifact_paths", "evidence_ids"})
        paths = set(strings(row["artifact_paths"], False))
        evidence_ids = strings(row["evidence_ids"], False)
        if ident in requirements and paths != set(requirements[ident]["artifact_paths"]):
            problems.append("provenance artifact mapping mismatch: " + ident)
        covered = set()
        for evidence_id in evidence_ids:
            if evidence_id not in evidence_outputs:
                problems.append("unknown evidence ID: " + evidence_id)
            else:
                covered.update(evidence_outputs[evidence_id])
        if not paths <= covered:
            problems.append("requirement artifacts lack cited observation: " + ident)
    if _version == "2":
        if contract["mode"] != "spec_build":
            raise ValueError("adoption lineage supports spec_build only")
        plan = read_snapshot_json(root, files, params["evidence"] + "/revision-plan.json")
        origin, baseline = revision_origin(root, files, plan, problems)
        if provenance["prior_origin"] != plan["prior_origin"] or provenance["adoption_origin"] != plan["adoption_origin"]:
            problems.append("provenance and plan origin references disagree")
        if origin["target_name"] != contract["target_name"] or provenance["run_id"] != plan["run_id"]:
            problems.append("revision origin/contract/run identity mismatch")
        candidate_prefix = plan["candidate"] + "/"
        candidate = {p[len(candidate_prefix):]: digest(d) for p, d in files.items() if p.startswith(candidate_prefix)}
        generated = {p: row["baseline_sha256"] for p, row in output_rows.items() if row["ownership"] == "generated"}
        if generated != candidate or set(candidate) != set(artifacts):
            problems.append("generated candidate ownership is not exactly justified by build contract")
        if provenance["result"] == "COMPLETE" and (plan["status"] != "APPLIED" or not plan["readback_passed"] or not plan["evaluation_passed"]):
            problems.append("COMPLETE provenance lacks delivered revision checks/readback")
        after_prefix = plan["after"] + "/"
        after = {p[len(after_prefix):]: digest(d) for p, d in files.items() if p.startswith(after_prefix)}
        if after != actual_outputs:
            problems.append("delivered output differs from revision after snapshot")
    elif provenance["prior_build"] is not None:
        ref = fields(provenance["prior_build"], {"path", "sha256"})
        prior = read_snapshot_json(root, files, ref["path"])
        prior_provenance_record(prior)
        if sha(ref["sha256"]) != digest(files[ref["path"]]) or prior["target_name"] != contract["target_name"]:
            problems.append("prior successful provenance mismatch")
    return result(problems, files)


def revision_action(owned, b, c, n, required):
    """Compare digest-or-None values; never mutate files."""
    if not owned and n is not None and c is not None:
        return "CONFLICT", c
    if not owned and n is None:
        action, selected = "KEEP_CURRENT", c
    elif c == b:
        action, selected = "USE_NEW", n
    elif c == n or n == b:
        action, selected = "KEEP_CURRENT", c
    else:
        action, selected = "CONFLICT", c
    if required and selected is None:
        return "CONFLICT", c
    return action, selected


def revision_consistency(root, params, _version="1"):
    fields(params, {"path"})
    files = snapshot(root)
    plan = read_snapshot_json(root, files, params["path"])
    origin_fields = {"prior_build"} if _version == "1" else {"prior_origin", "adoption_origin"}
    fields(plan, {"schema_version", "run_id", "status", "baseline", "current", "candidate", "after", "required_paths", "owned_paths", "rows", "applied_paths", "baseline_advanced", "readback_passed", "evaluation_passed", "baseline_before", "baseline_after"} | origin_fields, {"retry_of"})
    if plan["schema_version"] != _version or plan["status"] not in ("CONFLICT", "PLANNED", "APPLIED", "PARTIAL"):
        raise ValueError("unsupported revision version or status")
    nonempty(plan["run_id"])
    for key in ("baseline_advanced", "readback_passed", "evaluation_passed"):
        if type(plan[key]) is not bool:
            raise ValueError("revision state fields must be booleans")
    roots = {key: bounded_path(root, plan[key]) for key in ("baseline", "current", "candidate", "after")}
    pairs = list(roots.values())
    if any(a == b or a.is_relative_to(b) or b.is_relative_to(a) for i, a in enumerate(pairs) for b in pairs[i + 1:]):
        raise ValueError("revision snapshot directories must be disjoint")
    snapshots = {}
    for key, folder in roots.items():
        if not folder.is_dir():
            raise ValueError("revision snapshot directory missing: " + key)
        prefix = plan[key] + "/"
        snapshots[key] = {name[len(prefix):]: digest(data) for name, data in files.items() if name.startswith(prefix)}
    b, c, n, after = [snapshots[key] for key in ("baseline", "current", "candidate", "after")]
    owned = set(strings(plan["owned_paths"]))
    required = set(strings(plan["required_paths"], False))
    applied = set(strings(plan["applied_paths"]))
    for path in owned | required | applied:
        bounded_path(root, path)
    problems = []
    if owned != set(b):
        problems.append("owned path set differs from previous baseline")
    if not required <= set(n):
        problems.append("candidate omits a required artifact")
    refs = {}
    for key in (("prior_build",) if _version == "1" else ()) + ("baseline_before", "baseline_after"):
        ref = fields(plan[key], {"path", "sha256"})
        value = read_snapshot_json(root, files, ref["path"])
        if not isinstance(value, dict):
            raise ValueError("baseline reference requires object")
        if digest(files[ref["path"]]) != sha(ref["sha256"]):
            problems.append("revision reference digest mismatch: " + key)
        refs[key] = value
    if _version == "2":
        prior, previous_generated = revision_origin(root, files, plan, problems)
        if previous_generated != b:
            problems.append("previous origin does not bind baseline bytes")
    else:
        prior = refs["prior_build"]
        if prior.get("result") != "COMPLETE" or hash_rows(prior["baseline"]) != b:
            problems.append("missing or inconsistent previous successful baseline")
        prior_provenance_ref = fields(prior["provenance"], {"path", "sha256"})
        prior_provenance = read_snapshot_json(root, files, prior_provenance_ref["path"])
        previous_generated = prior_provenance_record(prior_provenance)
        if digest(files[prior_provenance_ref["path"]]) != sha(prior_provenance_ref["sha256"]) or prior_provenance.get("result") != "COMPLETE" or prior_provenance.get("run_id") != prior.get("run_id") or previous_generated != b:
            problems.append("previous provenance does not bind the generated baseline")
    if "retry_of" in plan:
        retry_ref = fields(plan["retry_of"], {"path", "sha256"})
        retry = read_snapshot_json(root, files, retry_ref["path"])
        if not isinstance(retry, dict):
            raise ValueError("retry reference must be a revision plan")
        origin_key = "prior_build" if _version == "1" else "prior_origin"
        retry_prior = fields(retry[origin_key], {"path", "sha256"} | ({"kind"} if _version == "2" else set()))
        same_origin = (sha(retry_prior["sha256"]) == plan[origin_key]["sha256"] if _version == "1"
                       else retry_prior == plan[origin_key] and retry.get("schema_version") == "2")
        if digest(files[retry_ref["path"]]) != sha(retry_ref["sha256"]) or retry.get("status") not in (("PARTIAL", "CONFLICT") if _version == "2" else ("PARTIAL",)) or not same_origin or retry.get("baseline_advanced") is not False:
            problems.append("retry does not retain the previous successful baseline")
    before_pointer, after_pointer = refs["baseline_before"], refs["baseline_after"]
    if before_pointer.get("run_id") != prior.get("run_id") or hash_rows(before_pointer["baseline"]) != b:
        problems.append("previous active baseline pointer mismatch")
    actual_advanced = files[plan["baseline_before"]["path"]] != files[plan["baseline_after"]["path"]]
    if actual_advanced != plan["baseline_advanced"]:
        problems.append("baseline advancement claim differs from pointer bytes")
    if actual_advanced and (after_pointer.get("run_id") != plan["run_id"] or hash_rows(after_pointer["baseline"]) != n):
        problems.append("advanced baseline pointer does not identify generated candidate")
    if _version == "2":
        pointer_record(root, files, after_pointer, problems)
        if actual_advanced:
            if after_pointer["origin"]["kind"] != "generated":
                problems.append("advanced pointer must identify generated provenance")
            else:
                published = reference_json(root, files, after_pointer["origin"], problems, typed=True)
                baseline = generated_origin_record(root, files, published, plan["adoption_origin"], problems,
                                                   after_pointer["origin"]["path"])
                if baseline != n or published["run_id"] != plan["run_id"] or published["prior_origin"] != plan["prior_origin"]:
                    problems.append("published generated origin differs from revision")
    rows = indexed(plan["rows"], "path")
    paths = set(b) | set(c) | set(n)
    if set(rows) != paths:
        problems.append("revision rows do not exactly cover B/C/N paths")
    expected, actions = dict(c), {}
    for path in sorted(paths):
        action, selected = revision_action(path in owned, b.get(path), c.get(path), n.get(path), path in required)
        actions[path] = action
        if selected is None:
            expected.pop(path, None)
        else:
            expected[path] = selected
        if path not in rows:
            continue
        row = fields(rows[path], {"path", "ownership", "b_sha256", "c_sha256", "n_sha256", "action", "reason"})
        nonempty(row["reason"])
        for key in ("b_sha256", "c_sha256", "n_sha256"):
            if row[key] is not None:
                sha(row[key])
        if row["action"] not in ("USE_NEW", "KEEP_CURRENT", "CONFLICT") or row["ownership"] not in (("adopted", "generated", "retained_user") if _version == "2" else ("generated", "retained_user")):
            raise ValueError("invalid revision action or ownership")
        expected_ownership = "generated" if path in owned or path in n else "retained_user"
        if _version == "2" and path in owned and plan["prior_origin"]["kind"] == "adopted":
            expected_ownership = "adopted"
        if (row["b_sha256"], row["c_sha256"], row["n_sha256"], row["action"], row["ownership"]) != (b.get(path), c.get(path), n.get(path), action, expected_ownership):
            problems.append("revision classification mismatch: " + path)
    changed = {path for path in set(c) | set(after) if c.get(path) != after.get(path)}
    if changed != applied:
        problems.append("applied path set differs from observed destination delta")
    has_conflict = "CONFLICT" in actions.values()
    if has_conflict and plan["status"] != "CONFLICT":
        problems.append("conflicted proposal has incompatible status")
    if plan["status"] in ("CONFLICT", "PLANNED") and c != after:
        problems.append("conflicted/planned run changed destination")
    if plan["status"] == "APPLIED":
        if after != expected:
            problems.append("applied result differs from computed revision")
        if not plan["readback_passed"] or not plan["evaluation_passed"]:
            problems.append("applied status lacks successful readback/evaluation")
    if plan["status"] == "PARTIAL":
        if any(actions.get(path) != "USE_NEW" or after.get(path) != expected.get(path) for path in changed):
            problems.append("partial result contains unrelated or unplanned mutation")
        if plan["readback_passed"]:
            problems.append("partial run claims successful readback")
    if actual_advanced and (plan["status"] != "APPLIED" or not plan["readback_passed"] or not plan["evaluation_passed"] or has_conflict or after != expected):
        problems.append("baseline advanced before successful application/evaluation/readback")
    return result(problems, files)


def routing_outcomes(root, params, _version="1"):
    fields(params, {"expected", "observed"})
    files = snapshot(root)
    routes = {"import", "spec_build", "revision", "explanation", "specification_authoring", "installation", "unrelated"}
    if _version == "2":
        routes.add("adoption")
    parsed = {}
    for key in ("expected", "observed"):
        bounded_path(root, params[key])
        data = files[params[key]]
        lines = data.decode("utf-8-sig").splitlines()
        if len(data) > 1024 * 1024 or not 1 <= len(lines) <= 1000:
            raise ValueError("routing input requires 1-1000 JSONL records and at most 1 MiB")
        rows = indexed([strict_json(line) for line in lines], "case_id")
        parsed[key] = {}
        for ident, row in rows.items():
            fields(row, {"case_id", "route"}, {"request"})
            if row["route"] not in routes:
                raise ValueError("unknown routing outcome")
            if "request" in row:
                nonempty(row["request"])
            parsed[key][ident] = row["route"]
    if set(parsed["expected"]) != set(parsed["observed"]):
        raise ValueError("routing observation IDs missing or unknown")
    problems = ["route mismatch: " + ident for ident, route in parsed["expected"].items() if parsed["observed"][ident] != route]
    return result(problems, files)


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


def adoption_consistency(root, params):
    fields(params, {"evidence", "destination"})
    evidence = bounded_path(root, params["evidence"])
    destination = bounded_path(root, params["destination"])
    if evidence == destination or evidence.is_relative_to(destination) or destination.is_relative_to(evidence):
        raise ValueError("adoption evidence and destination must be disjoint")
    files = snapshot(root)
    problems = []
    record = read_snapshot_json(root, files, params["evidence"] + "/adoption-record.json")
    adoption_record(root, files, record, problems)
    if not bounded_path(root, record["snapshot_root"]).is_relative_to(evidence):
        raise ValueError("adoption snapshot must be inside selected evidence directory")
    for key in ("snapshot_manifest", "managed_manifest", "origin_spec", "source_readback"):
        if not bounded_path(root, record[key]["path"]).is_relative_to(evidence):
            raise ValueError("adoption inputs must be inside selected evidence directory")
    source_prefix = record["snapshot_root"] + "/"
    after_prefix = params["destination"] + "/"
    before = {p[len(source_prefix):]: d for p, d in files.items() if p.startswith(source_prefix)}
    after = {p[len(after_prefix):]: d for p, d in files.items() if p.startswith(after_prefix)}
    if before != after:
        problems.append("adoption mutated target bytes or file set")
    return result(problems, files)


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


def grade(grader_id, root, params):
    if not isinstance(params, dict):
        raise ValueError("grader params must be an object")
    if grader_id == "package_links":
        return package_links(root, params)
    if grader_id == "manifest_accounting":
        return manifest_accounting(root, params)
    if grader_id == "build_traceability":
        return build_traceability(root, params)
    if grader_id == "revision_consistency":
        return revision_consistency(root, params)
    if grader_id == "routing_outcomes":
        return routing_outcomes(root, params)
    if grader_id == "adoption_consistency":
        return adoption_consistency(root, params)
    if grader_id == "build_traceability_v2":
        return build_traceability(root, params, "2")
    if grader_id == "revision_consistency_v2":
        return revision_consistency(root, params, "2")
    if grader_id == "routing_outcomes_v2":
        return routing_outcomes(root, params, "2")
    raise ValueError("unknown grader: " + str(grader_id))
