#!/usr/bin/env python3
"""Bounded, read-only development observations; never framework acceptance.

Only snapshot creates files. Other commands print observations without mutation.
Python 3.10+; structure additionally requires an already installed PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from urllib.parse import unquote, urlsplit


MAX_FILES = 2000
MAX_BYTES = 32 * 1024 * 1024
DIGEST = re.compile(r"^[0-9a-f]{64}$")
DIMENSIONS = ("standards", "workflow", "instructions", "behavior")
DIMENSION_ALIASES = dict(zip(("standards_compliance", "workflow_correctness", "instruction_quality", "behavioral_evaluation"), DIMENSIONS))
LIMITATIONS = [
    "Development observations only; no semantic, native invocation, ownership, or framework acceptance claim.",
    "No links or junctions followed; excluded boundaries prevent a complete recovery snapshot.",
    "Static path and readback checks do not provide OS-enforced isolation against concurrent hostile replacement.",
]


class ObservationError(Exception):
    """An observation could not execute reliably."""


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def strict_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key: " + key)
        value[key] = item
    return value


def strict_json(data):
    def nonfinite(value):
        raise ValueError("non-finite JSON value: " + value)
    def finite_float(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError("non-finite JSON numeric value: " + value)
        return parsed
    return json.loads(data, object_pairs_hook=strict_object, parse_constant=nonfinite, parse_float=finite_float)


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def safe_path(value, must_exist=True):
    path = Path(value).expanduser()
    if ".." in path.parts:
        raise ObservationError("traversal component rejected: " + str(path))
    path = Path(os.path.abspath(path))
    # Inspect each existing ancestor before resolution can follow a junction.
    for ancestor in reversed((path, *path.parents)):
        if os.path.lexists(ancestor) and is_link(ancestor):
            raise ObservationError("link/junction boundary rejected: " + str(ancestor))
    if must_exist and not path.exists():
        raise ObservationError("missing path: " + str(path))
    return path


def within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def normalized_relative(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and all(part not in (".", "..", "") for part in value.split("/"))


def exclusion(name):
    lower = name.lower()
    if lower in ("devforgeai_cli", ".git"):
        return "excluded legacy implementation or repository metadata boundary"
    if (re.search(r"(?:^|[-_.])backups?(?:$|[-_.])", lower)
            or lower in ("backup", "backups", ".backup", ".backups", "__pycache__")
            or lower.startswith(("backup-", "backup_", "backups-", "backups_"))
            or lower.endswith((".bak", ".backup", "~"))):
        return "excluded backup or generated cache boundary"
    return None


def inventory(source, max_files=MAX_FILES, max_bytes=MAX_BYTES):
    if not source.is_dir():
        raise ObservationError("source is not a directory: " + str(source))
    pending = [source]
    files = []
    excluded = []
    total = 0
    while pending:
        current = pending.pop()
        # Enumerate one directory before deciding which children may be recursed.
        entries = sorted(current.iterdir(), key=lambda entry: entry.name)
        for entry in entries:
            relative = entry.relative_to(source).as_posix()
            reason = exclusion(entry.name)
            if reason:
                excluded.append({"path": relative, "reason": reason})
                continue
            info = entry.lstat()
            if is_link(entry):
                excluded.append({"path": relative, "reason": "link/junction not followed"})
            elif stat.S_ISDIR(info.st_mode):
                pending.append(entry)
            elif stat.S_ISREG(info.st_mode):
                if not normalized_relative(relative):
                    raise ObservationError("nonportable relative path: " + relative)
                total += info.st_size
                files.append((relative, entry, info))
                if len(files) > max_files or total > max_bytes:
                    raise ObservationError(f"snapshot ceiling exceeded: {len(files)} files, {total} bytes; limits {max_files} files/{max_bytes} bytes")
            else:
                raise ObservationError("special file rejected: " + relative)
    return sorted(files), sorted(excluded, key=lambda row: row["path"])


def read_stable(path, expected=None):
    safe_path(path)
    before = path.stat()
    if not stat.S_ISREG(before.st_mode):
        raise ObservationError("not a regular file: " + str(path))
    if before.st_size > MAX_BYTES:
        raise ObservationError("file exceeds read ceiling: " + str(path))
    if expected and (before.st_size, before.st_mtime_ns, before.st_ino) != (expected.st_size, expected.st_mtime_ns, expected.st_ino):
        raise ObservationError("source changed before read: " + str(path))
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    after = path.stat()
    if len(data) > MAX_BYTES or (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ObservationError("source changed or exceeded ceiling during read: " + str(path))
    return data


def make_manifest(source):
    permitted, excluded = inventory(source)
    rows = []
    for relative, path, info in permitted:
        data = read_stable(path, info)
        rows.append({"path": relative, "bytes": len(data), "sha256": sha256(data)})
    return {"schema_version": "1", "root": str(source),
            "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "files": rows, "excluded_boundaries": excluded, "complete": not excluded,
            "package_digest": sha256(compact(rows))}


def result(command, status, coverage, **extra):
    return {"schema_version": "1", "command": command, "status": status,
            "coverage": coverage, "limitations": list(LIMITATIONS), **extra}


def snapshot(args):
    source = safe_path(args.source)
    output = safe_path(args.output, must_exist=False)
    if os.path.lexists(output):
        raise ObservationError("snapshot output already exists: " + str(output))
    if within(output, source) or within(source, output):
        raise ObservationError("snapshot output overlaps source")
    # Finish bounded enumeration before creating anything.
    permitted, excluded = inventory(source)
    output.mkdir(parents=True, exist_ok=False)
    try:
        target = output / "source"
        target.mkdir()
        rows = []
        for relative, path, info in permitted:
            data = read_stable(path, info)
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(data)
            rows.append({"path": relative, "bytes": len(data), "sha256": sha256(data)})
        manifest = {"schema_version": "1", "root": str(source),
                    "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "files": rows, "excluded_boundaries": excluded, "complete": not excluded,
                    "package_digest": sha256(compact(rows))}
        after = make_manifest(source)
        if rows != after["files"] or excluded != after["excluded_boundaries"]:
            raise ObservationError("SOURCE_CHANGED during snapshot capture")
        with (output / "source-manifest.json").open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(manifest, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
        code = 0 if manifest["complete"] else 1
        return result("snapshot", "COMPLETE" if code == 0 else "INCOMPLETE", ["bounded inventory", "raw-byte copy", "source readback"],
                      output=str(output), manifest=manifest), code
    except Exception as exc:
        failure = result("snapshot", "PARTIAL", ["attempted snapshot"], output=str(output),
                         partial_output=str(output), complete=False, error=str(exc))
        # Preserve partial bytes, with an explicit incomplete marker; never a complete manifest.
        try:
            with (output / "snapshot-failure.json").open("x", encoding="utf-8") as stream:
                json.dump(failure, stream, ensure_ascii=False, indent=2)
        except OSError:
            pass
        return failure, 2


def validate_manifest(manifest):
    errors = []
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "1":
        return ["manifest must be schema version 1 object"]
    rows = manifest.get("files")
    if not isinstance(rows, list):
        return ["manifest files must be an array"]
    paths = []
    canonical = []
    for row in rows:
        if (not isinstance(row, dict) or not normalized_relative(row.get("path"))
                or type(row.get("bytes")) is not int or row["bytes"] < 0
                or not isinstance(row.get("sha256"), str) or not DIGEST.fullmatch(row["sha256"])):
            errors.append("invalid manifest file row")
            continue
        paths.append(row["path"])
        canonical.append({"path": row["path"], "bytes": row["bytes"], "sha256": row["sha256"]})
    if paths != sorted(set(paths)):
        errors.append("manifest files must be uniquely sorted by path")
    if manifest.get("package_digest") != sha256(compact(canonical)):
        errors.append("manifest package_digest mismatch")
    if not isinstance(manifest.get("excluded_boundaries"), list) or type(manifest.get("complete")) is not bool:
        errors.append("manifest requires excluded_boundaries and boolean complete")
    elif manifest["excluded_boundaries"] and manifest["complete"]:
        errors.append("manifest falsely claims complete with excluded boundaries")
    return errors


def readback(args):
    source = safe_path(args.source)
    path = safe_path(args.manifest)
    manifest = strict_json(read_stable(path).decode("utf-8"))
    if isinstance(manifest, dict) and isinstance(manifest.get("files"), list):
        if any(isinstance(row, dict) and not normalized_relative(row.get("path")) for row in manifest["files"]):
            raise ObservationError("unsafe manifest file path")
    errors = validate_manifest(manifest)
    if errors:
        return result("readback", "MISMATCH", ["manifest integrity"], errors=errors), 1
    actual = make_manifest(source)
    expected_rows = {row["path"]: row for row in manifest["files"]}
    actual_rows = {row["path"]: row for row in actual["files"]}
    added = sorted(actual_rows.keys() - expected_rows.keys())
    removed = sorted(expected_rows.keys() - actual_rows.keys())
    changed = sorted(path for path in actual_rows.keys() & expected_rows.keys() if actual_rows[path] != expected_rows[path])
    boundary_changed = actual["excluded_boundaries"] != manifest["excluded_boundaries"]
    drift = bool(added or removed or changed or boundary_changed)
    status = "SOURCE_CHANGED" if drift else "MATCH"
    return result("readback", status, ["permitted file set", "raw-byte sizes and hashes", "excluded boundaries"],
                  added=added, removed=removed, changed=changed, excluded_boundaries_changed=boundary_changed,
                  manifest=actual, complete=actual["complete"]), 1 if drift or not actual["complete"] else 0


def markdown_body(text):
    """Remove fenced code so sample links/headings are not reported as real links."""
    output = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            mark = match.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            output.append("")
        else:
            output.append(line if fence is None else "")
    return "\n".join(output)


def anchors(text):
    found = set()
    counts = {}
    for line in markdown_body(text).splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            heading = match.group(1).lower()
            heading = re.sub(r"<[^>]+>", "", heading)
            slug = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE).replace(" ", "-")
            ordinal = counts.get(slug, 0)
            counts[slug] = ordinal + 1
            found.add(slug if ordinal == 0 else f"{slug}-{ordinal}")
    return found


def structure(args):
    source = safe_path(args.source)
    permitted, excluded = inventory(source)
    observations = []
    required_mismatch = False
    def check(check_id, passed, detail, subject="SKILL.md", required=True):
        nonlocal required_mismatch
        observations.append({"check_id": check_id, "subject_path": subject,
                             "required": required, "result": "PASS" if passed else "FAIL", "reason": detail})
        required_mismatch |= required and not passed
    files = {relative: (path, info) for relative, path, info in permitted}
    if "SKILL.md" not in files:
        check("entrypoint", False, "required SKILL.md absent")
        return result("structure", "MISMATCH", ["entrypoint existence"], checks=observations, excluded_boundaries=excluded), 1
    try:
        import yaml
    except ImportError as exc:
        raise ObservationError("PyYAML unavailable; YAML structural checks NOT_RUN; no dependency installed") from exc
    from skill_format import yaml_mapping, metadata_checks, advisory_checks, SUPPORTED_FIELDS
    text = read_stable(*files["SKILL.md"]).decode("utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, flags=re.DOTALL)
    metadata = None
    check("frontmatter", bool(match), "frontmatter delimited at start" if match else "missing or unterminated YAML frontmatter")
    if match:
        try:
            metadata = yaml_mapping(match.group(1))
            check("yaml", isinstance(metadata, dict), "YAML must be a mapping")
        except (yaml.YAMLError, ValueError, TypeError) as exc:
            check("yaml", False, str(exc))
    if isinstance(metadata, dict):
        name = metadata.get("name")
        for check_id, passed, message in metadata_checks(metadata):
            check(check_id, passed, message)
        identity = source.name
        enclosing_manifest = source.parent / "source-manifest.json"
        if source.name == "source" and enclosing_manifest.exists():
            stored = strict_json(read_stable(safe_path(enclosing_manifest)).decode("utf-8"))
            manifest_errors = validate_manifest(stored)
            observed = make_manifest(source)
            if manifest_errors or stored["files"] != observed["files"]:
                check("snapshot_identity", False, "snapshot manifest invalid or does not bind actual source files")
            else:
                original = stored.get("root", "")
                identity = original.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        check("directory_identity", name == identity, "frontmatter name must match original skill directory name")
        for check_id, passed, message in advisory_checks(metadata):
            observations.append({"check_id": check_id, "subject_path": "SKILL.md", "required": False,
                                 "result": "NOT_RUN" if not passed else "PASS",
                                 "reason": "Recorded source divergence, not a defect: " + message})
        extra = sorted(set(metadata) - set(SUPPORTED_FIELDS))
        if extra:
            observations.append({"check_id": "additional_metadata", "subject_path": "SKILL.md", "required": False,
                                 "result": "NOT_RUN", "reason": "Applicability of extra host fields needs source-backed review: " + ", ".join(map(str, extra))})
    markdown = {}
    for relative, (path, info) in files.items():
        if path.suffix.lower() == ".md":
            markdown[relative] = read_stable(path, info).decode("utf-8")
    link_count = 0
    for relative, content in markdown.items():
        content = markdown_body(content)
        # Quoted inline code is example data, not live resource syntax.
        content = re.sub(r'(`+)([^\n]+?)\1', lambda match: ' ' * len(match[0]), content)
        # Deliberately limited to ordinary inline Markdown links/images.
        for match in re.finditer(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", content):
            target = match.group(1).strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            decoded = unquote(parsed.path)
            if not decoded:
                target_path = source / relative
            else:
                target_path = Path(os.path.abspath(source / Path(relative).parent / decoded))
            link_count += 1
            if not within(target_path, source):
                observations.append({"check_id": "external_resource_scope", "subject_path": relative, "required": False,
                                     "result": "NOT_RUN", "reason": "Outside package resource needs explicitly scoped inspection: " + target})
                continue
            target_relative = target_path.relative_to(source).as_posix()
            try:
                safe_path(target_path)
                exists = target_path.is_file() or target_path.is_dir()
            except ObservationError:
                exists = False
            check("resource_link", exists, target, relative)
            if exists and parsed.fragment:
                if target_relative in markdown:
                    check("resource_anchor", unquote(parsed.fragment) in anchors(markdown[target_relative]), target, relative)
                else:
                    observations.append({"check_id": "resource_anchor", "subject_path": relative, "required": False,
                                         "result": "NOT_RUN", "reason": "Anchor target not supported Markdown: " + target})
    # Claude Code reads no separate configuration file: invocation policy, tool grants
    # and every other host field live in the SKILL.md frontmatter checked above. A
    # package still carrying another host's configuration file is reported as dead
    # configuration rather than parsed against a contract this host does not read.
    for foreign in sorted(p for p in files if p.startswith("agents/") and p.endswith((".yaml", ".yml"))):
        observations.append({"check_id": "foreign_host_configuration", "subject_path": foreign, "required": False,
                             "result": "NOT_RUN",
                             "reason": "Claude Code reads no separate metadata file; this is unread configuration from another host and needs a disposition decision."})
    response = result("structure", "MISMATCH" if required_mismatch else ("INCOMPLETE" if excluded else "OBSERVED"),
                      ["required metadata", "selected optional metadata types and value domains", "ordinary inline links", "ATX heading anchors", "recorded source divergences"],
                      checks=observations, excluded_boundaries=excluded, links_checked=link_count,
                      parser={"yaml": getattr(yaml, "__version__", "unknown")})
    response["limitations"].extend([
        "Reference-style links, HTML anchors, Setext headings, renderer-specific slugs, and dynamic script paths require manual review.",
        "Extra host metadata keys require selected-source applicability review; installed checker compatibility is a separate observation.",
        "Advisory rows record disagreement between the Claude Code reference and the Agent Skills specification; they are never defects on their own.",
        "No optional folder, line count, keyword, or fixed workflow anatomy is required by these observations.",
    ])
    return response, 1 if required_mismatch or excluded else 0


def reduce_checks(checks):
    applicable = [row for row in checks if row.get("required") is True and row.get("applicability") != "not_applicable"]
    incomplete = [row.get("check_id") for row in applicable if row.get("applicability") == "unknown" or row.get("result") in ("NOT_RUN", "ERROR")]
    if any(row.get("applicability") == "applicable" and row.get("result") == "FAIL" for row in applicable):
        outcome = "FAIL"
    elif incomplete:
        outcome = "INCOMPLETE"
    elif applicable:
        outcome = "PASS"
    elif checks and any(row.get("applicability") == "applicable" for row in checks):
        outcome = "PASS"
    else:
        outcome = "NOT_APPLICABLE" if checks and all(row.get("applicability") == "not_applicable" and row.get("reason") for row in checks) else "INCOMPLETE"
    return {"outcome": outcome, "required_total": len(applicable),
            "required_evaluated": sum(row.get("applicability") == "applicable" and row.get("result") in ("PASS", "FAIL") for row in applicable),
            "incomplete_check_ids": incomplete}


def finding_identity(rule_id, subject_path, anchor, occurrence):
    identity = [rule_id, subject_path, anchor.replace("\r\n", "\n").replace("\r", "\n").strip(), occurrence]
    return "F-" + sha256(compact(identity)), identity


def records(args):
    root = safe_path(args.run_root)
    permitted, excluded = inventory(root)
    errors = []
    documents = {}
    raw = {}
    coverage = []
    for relative, path, info in permitted:
        raw[relative] = (path, info)
        if path.suffix.lower() not in (".json", ".jsonl"):
            continue
        # Source and captured fixture bytes are evidence, not validator records.
        if relative.startswith(("source/", "inputs/", "trials/")):
            continue
        try:
            text = read_stable(path, info).decode("utf-8")
            if path.suffix.lower() == ".jsonl":
                documents[relative] = [strict_json(line) for line in text.splitlines() if line.strip()]
            else:
                documents[relative] = strict_json(text)
        except (ValueError, UnicodeError, RecursionError) as exc:
            errors.append(relative + ": " + str(exc))
    if not documents:
        errors.append("no parseable machine records found")
    coverage.append("strict JSON/JSONL parsing of run records (excluding raw source, input, and trial fixtures)")
    reference_edges = {}
    references_checked = 0
    sources = documents.get("sources.json", {})
    source_rows = sources.get("sources", []) if isinstance(sources, dict) else []
    if not isinstance(source_rows, list):
        errors.append("sources must be an array")
        source_rows = []
    source_ids = {row.get("source_id") for row in source_rows if isinstance(row, dict) and isinstance(row.get("source_id"), str)}
    if len(source_ids) != len(source_rows):
        errors.append("source IDs must be unique strings")
    def inspect(value, owner, location="$"):
        nonlocal references_checked
        if isinstance(value, dict):
            if "path" in value and "sha256" in value:
                # A manifest file row describes source bytes; it is not run-relative reference.
                file_row = owner.endswith("manifest.json") and "bytes" in value
                if not file_row:
                    reference = value["path"]
                    digest = value["sha256"]
                    if not normalized_relative(reference) or not isinstance(digest, str) or not DIGEST.fullmatch(digest):
                        errors.append(f"{owner}:{location}: invalid path/digest reference")
                    elif reference == owner:
                        errors.append(f"{owner}:{location}: self-referential digest forbidden")
                    else:
                        reference_edges.setdefault(owner, set()).add(reference)
                        try:
                            destination = safe_path(root / reference)
                            if not destination.is_file():
                                raise ObservationError("reference is not a regular file")
                            data = read_stable(destination)
                            references_checked += 1
                            if sha256(data) != digest:
                                errors.append(f"{owner}:{location}: reference digest mismatch: {reference}")
                            if "source_id" in value and value["source_id"] not in source_ids:
                                errors.append(f"{owner}:{location}: unknown source_id")
                            if "start_byte" in value or "end_byte" in value:
                                start, end = value.get("start_byte"), value.get("end_byte")
                                if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(data):
                                    errors.append(f"{owner}:{location}: invalid byte locator")
                            if "start_line" in value or "end_line" in value:
                                start, end = value.get("start_line"), value.get("end_line")
                                if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(data.splitlines()):
                                    errors.append(f"{owner}:{location}: invalid line locator")
                            locator = value.get("locator")
                            if isinstance(locator, dict):
                                if "line_start" in locator or "line_end" in locator:
                                    start, end = locator.get("line_start"), locator.get("line_end")
                                    if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(data.splitlines()):
                                        errors.append(f"{owner}:{location}: invalid nested line locator")
                                if "start_byte" in locator or "end_byte" in locator:
                                    start, end = locator.get("start_byte"), locator.get("end_byte")
                                    if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(data):
                                        errors.append(f"{owner}:{location}: invalid nested byte locator")
                        except ObservationError as exc:
                            errors.append(f"{owner}:{location}: {exc}")
            for key, item in value.items():
                inspect(item, owner, location + "." + key)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                inspect(item, owner, location + f"[{index}]")
    for owner, document in documents.items():
        inspect(document, owner)
    for source_record in source_rows:
        if not isinstance(source_record, dict):
            errors.append("source record must be an object")
            continue
        if "snapshot_path" in source_record:
            inspect({"path": source_record["snapshot_path"], "sha256": source_record.get("sha256")}, "sources.json", "$.sources.snapshot_path")
    def visit(node, active, finished):
        if node in active:
            errors.append("cyclic digest references: " + node)
            return
        if node in finished:
            return
        active.add(node)
        for child in reference_edges.get(node, ()):
            visit(child, active, finished)
        active.remove(node)
        finished.add(node)
    finished = set()
    for name in reference_edges:
        visit(name, set(), finished)
    coverage.append("extant reference bytes, normalized paths, digests, supported locators, and reference cycles")
    identities = {}
    for name in ("source-manifest.json", "source-after-manifest.json"):
        if name in documents:
            errors.extend(name + ": " + message for message in validate_manifest(documents[name]))
    retained_manifest = documents.get("source-manifest.json")
    if isinstance(retained_manifest, dict) and not validate_manifest(retained_manifest):
        if (root / "source").exists():
            actual_snapshot = make_manifest(safe_path(root / "source"))
            if retained_manifest["files"] != actual_snapshot["files"]:
                errors.append("source-manifest.json does not match retained source bytes/file set")
    rule_set = documents.get("rule-set.json", {})
    rules = rule_set.get("rules", []) if isinstance(rule_set, dict) else []
    if not isinstance(rules, list):
        errors.append("rules must be an array")
        rules = []
    rule_ids = [row.get("rule_id") for row in rules if isinstance(row, dict) and isinstance(row.get("rule_id"), str)]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate rule_id in rule-set.json")
    checks = documents.get("checks.jsonl", [])
    if not isinstance(checks, list):
        checks = []
        errors.append("checks.jsonl must contain check objects")
    required_check_fields = {"schema_version", "run_id", "check_id", "rule_id", "subject_path", "method", "required", "applicability", "result", "reason", "evidence"}
    check_ids = set()
    for row in checks:
        if not isinstance(row, dict):
            errors.append("check row must be an object")
            continue
        if required_check_fields - row.keys():
            errors.append("check missing fields: " + ", ".join(sorted(required_check_fields - row.keys())))
        if row.get("schema_version") != "1" or type(row.get("required")) is not bool:
            errors.append("check schema_version/required invalid")
        if any(not isinstance(row.get(key), str) or not row.get(key) for key in ("run_id", "rule_id", "method", "reason")):
            errors.append("check run_id/rule_id/method/reason must be nonempty strings")
        check_id = row.get("check_id")
        if not isinstance(check_id, str) or not check_id or check_id in check_ids:
            errors.append("missing/duplicate check_id")
        if isinstance(check_id, str):
            check_ids.add(check_id)
        app, outcome = row.get("applicability"), row.get("result")
        if app not in ("applicable", "not_applicable", "unknown") or outcome not in ("PASS", "FAIL", "NOT_RUN", "ERROR", "NOT_APPLICABLE"):
            errors.append("invalid check applicability/result")
        if (app == "unknown" and outcome != "NOT_RUN") or (app == "not_applicable" and (outcome != "NOT_APPLICABLE" or not row.get("reason"))) or (app == "applicable" and outcome == "NOT_APPLICABLE"):
            errors.append("inconsistent check applicability/result")
        if rules and row.get("rule_id") not in rule_ids:
            errors.append("check references unknown rule_id")
        if not normalized_relative(row.get("subject_path")):
            errors.append("invalid check subject_path")
        if not isinstance(row.get("evidence"), list):
            errors.append("check evidence must be an array")
        elif any(not isinstance(ref, dict) or not {"path", "sha256"} <= ref.keys() for ref in row["evidence"]):
            errors.append("check evidence entries require path and sha256")
        if "dimension" in row and row["dimension"] not in (*DIMENSIONS, *DIMENSION_ALIASES):
            errors.append("unsupported check dimension")
    finding_document = documents.get("findings.json", {})
    finding_rows = finding_document.get("findings", []) if isinstance(finding_document, dict) else []
    if not isinstance(finding_rows, list):
        errors.append("findings must be an array")
        finding_rows = []
    finding_fields = {"finding_id", "rule_id", "category", "severity", "subject_path", "identity", "source_refs", "observation_refs", "description", "user_impact", "proposed_correction", "preserved_requirements", "verification_cases", "disposition"}
    for finding in finding_rows:
        if not isinstance(finding, dict):
            errors.append("finding must be an object")
            continue
        for canonical, alias in (("source_refs", "source_references"), ("observation_refs", "observation_references")):
            if canonical in finding and alias in finding and finding[canonical] != finding[alias]:
                errors.append("conflicting finding reference aliases")
            elif canonical not in finding and alias in finding:
                finding[canonical] = finding[alias]
        absent = finding_fields - finding.keys()
        if absent:
            errors.append("finding missing fields: " + ", ".join(sorted(absent)))
        identity = finding.get("identity")
        valid = (isinstance(identity, list) and len(identity) == 4 and isinstance(identity[0], str)
                 and normalized_relative(identity[1]) and isinstance(identity[2], str)
                 and type(identity[3]) is int and identity[3] >= 0)
        if not valid:
            errors.append("finding identity must be [rule_id, subject_path, normalized_anchor, occurrence]")
            continue
        expected, normalized = finding_identity(*identity)
        if identity != normalized or finding.get("finding_id") != expected or identity[0] != finding.get("rule_id") or identity[1] != finding.get("subject_path"):
            errors.append("finding identity/digest mismatch")
        if identity[2] == "MISSING_FILE" and identity[3] != 0:
            errors.append("MISSING_FILE finding occurrence must be zero")
        previous = identities.get(expected)
        if previous is not None:
            errors.append("duplicate finding identity; equal identities must deduplicate" if previous == identity else "finding digest collision with different identity")
        identities[expected] = identity
        if finding.get("severity") not in ("blocker", "major", "minor", "advisory") or finding.get("disposition") not in ("proposed", "selected", "deferred", "rejected"):
            errors.append("invalid finding severity/disposition")
        if rules and finding.get("rule_id") not in rule_ids:
            errors.append("finding references unknown rule_id")
    coverage.extend(["check schemas and applicability", "finding schemas and deterministic identity", "manifest digest accounting"])
    dimensions = {}
    for dimension in DIMENSIONS:
        selected = [row for row in checks if isinstance(row, dict) and DIMENSION_ALIASES.get(row.get("dimension"), row.get("dimension")) == dimension]
        if selected:
            dimensions[dimension] = reduce_checks(selected)
    all_required = reduce_checks([row for row in checks if isinstance(row, dict)])
    overall = ("FAIL" if any(row["outcome"] == "FAIL" for row in dimensions.values()) or all_required["outcome"] == "FAIL"
               else "INCOMPLETE" if len(dimensions) != len(DIMENSIONS) or any(row["outcome"] == "INCOMPLETE" for row in dimensions.values())
               else "PASS")
    origin = documents.get("origin-record.json", {})
    if not isinstance(origin, dict):
        errors.append("origin-record.json must be an object")
        origin = {}
    if isinstance(origin, dict):
        if origin.get("source_readback_state") in ("SOURCE_CHANGED", "changed") and overall != "FAIL":
            overall = "INCOMPLETE"
        if origin.get("history_kind") in ("adopted", "generated") and not origin.get("prior_evidence"):
            errors.append("adopted/generated history requires corresponding prior_evidence reference and manual verification")
    handoff = documents.get("handoff.json", {})
    if isinstance(handoff, dict) and handoff:
        selected = handoff.get("selected_finding_ids", [])
        deferred = handoff.get("deferred_finding_ids", [])
        if not isinstance(selected, list) or not isinstance(deferred, list):
            errors.append("handoff selected/deferred finding IDs must be arrays")
            selected, deferred = [], []
        for finding_id in selected + deferred:
            if not isinstance(finding_id, str) or finding_id not in identities:
                errors.append("handoff references unknown finding ID: " + str(finding_id))
        state = handoff.get("builder_readiness")
        review = handoff.get("proposal_review_state", handoff.get("review_state"))
        if "proposal_review_state" in handoff and "review_state" in handoff and handoff["proposal_review_state"] != handoff["review_state"]:
            errors.append("conflicting review-state aliases")
        if state not in ("NO_CHANGE", "REVIEW_REQUIRED", "READY", "BLOCKED"):
            errors.append("invalid builder_readiness")
        if review not in ("not_needed", "pending", "approved", "changes_requested"):
            errors.append("invalid handoff review_state")
        if state == "READY":
            if review != "approved" or not handoff.get("review_instruction"):
                errors.append("READY requires recorded approved review instruction")
            if not handoff.get("baseline_reference") and not (handoff.get("adoption_required") is True and handoff.get("adoption_capability") == "available" and handoff.get("managed_path_authorization")):
                errors.append("READY requires baseline or available adoption plus managed-path authorization")
            proposal = handoff.get("proposed_spec")
            authorization = handoff.get("review_authorization")
            if not isinstance(proposal, dict) or not isinstance(authorization, dict) or authorization.get("proposal_sha256") != proposal.get("sha256") or authorization.get("target_package_digest") != handoff.get("target_package_digest") or not authorization.get("target_package_digest"):
                errors.append("READY review authorization must bind proposal digest and target package digest")
            if origin.get("source_readback_state") not in ("UNCHANGED", "MATCH"):
                errors.append("READY requires matching source readback")
            manifest = documents.get("source-manifest.json", {})
            if not isinstance(manifest, dict) or handoff.get("target_package_digest") != manifest.get("package_digest"):
                errors.append("READY target digest must match retained source manifest")
        if state == "NO_CHANGE" and (selected or handoff.get("proposed_spec")):
            errors.append("NO_CHANGE contradicts proposed change")
        if state == "REVIEW_REQUIRED" and review not in ("pending", "changes_requested"):
            errors.append("REVIEW_REQUIRED must retain pending review or requested changes")
        if state in ("READY", "REVIEW_REQUIRED") and handoff.get("proposed_spec"):
            if not handoff.get("baseline_reference") and not (handoff.get("adoption_required") is True and handoff.get("adoption_capability") == "available" and handoff.get("managed_path_authorization")):
                errors.append("adoption-dependent execution without baseline/authorized available adoption must be BLOCKED")
        if state != "BLOCKED" and origin.get("source_readback_state") == "SOURCE_CHANGED":
            errors.append("changed source requires BLOCKED builder readiness")
    assessment = documents.get("assessment.json", {})
    if isinstance(assessment, dict) and assessment:
        if assessment.get("overall_assessment") != overall:
            errors.append("declared overall assessment contradicts computed check reduction")
        for name, expected in dimensions.items():
            declared_dimensions = assessment.get("dimensions", {})
            if not isinstance(declared_dimensions, dict):
                errors.append("assessment dimensions must be an object")
                declared_dimensions = {}
            declared = declared_dimensions.get(name)
            if declared is None:
                declared = next((value for key, value in declared_dimensions.items() if DIMENSION_ALIASES.get(key) == name), None)
            if isinstance(declared, dict):
                declared = declared.get("outcome")
            if declared != expected["outcome"]:
                errors.append("declared dimension contradicts computed reduction: " + name)
    coverage.append("status reductions when dimension-tagged checks exist; basic review-readiness consistency")
    response = result("records", "MISMATCH" if errors else ("INCOMPLETE" if excluded else "OBSERVED"), coverage,
                      errors=errors, records_checked=sorted(documents), references_checked=references_checked,
                      excluded_boundaries=excluded, dimensions=dimensions, overall_assessment=overall,
                      required_coverage=all_required)
    response["limitations"].extend([
        "Only extant records are checked; absent stage artifacts and semantic evidence support require the report checklist.",
        "Finding anchor support, historical provenance validity, rule authority/applicability, and review authorization meaning require agent review.",
        "Checks may add dimension standards, workflow, instructions, behavior for explicit reductions; long snake_case aliases are supported; missing dimensions remain incomplete.",
        "assessment.json is optional helper input for checking declared reductions; validation-report.md prose is not parsed as machine authority.",
    ])
    return response, 1 if errors or excluded else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("snapshot", help="copy bounded raw bytes into a fresh disjoint evidence directory")
    command.add_argument("--source", required=True)
    command.add_argument("--output", required=True, help="new directory; contains source/ and source-manifest.json")
    command = sub.add_parser("structure", help="observe YAML, metadata and supported local Markdown resources")
    command.add_argument("--source", required=True, help="skill directory or snapshot source/ directory")
    command = sub.add_parser("readback", help="compare original permitted bytes to a recorded source manifest")
    command.add_argument("--source", required=True)
    command.add_argument("--manifest", required=True)
    command = sub.add_parser("records", help="inspect extant run records, references, IDs and supported reductions")
    command.add_argument("--run-root", required=True)
    args = parser.parse_args(argv)
    try:
        observed, code = globals()[args.command](args)
    except (ObservationError, OSError, ValueError, UnicodeError, RecursionError, TypeError, AttributeError, KeyError) as exc:
        observed = result(args.command, "ERROR", [], error=str(exc))
        print(str(exc), file=sys.stderr)
        code = 2
    print(json.dumps(observed, ensure_ascii=False, indent=2, allow_nan=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
