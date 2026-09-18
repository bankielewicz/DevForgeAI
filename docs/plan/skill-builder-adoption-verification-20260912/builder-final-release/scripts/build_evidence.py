"""Read selected inputs and emit build evidence; never write destination files."""

import argparse
import hashlib
import json
import math
import re
import stat
import sys
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
MAX_BYTES = 32 * 1024 * 1024
MAX_FILES = 2000
EXCLUDED = {"backup", "backups", "devforgeai_cli"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def linked(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def selected(path):
    path = Path(path).absolute()
    for item in [path, *path.parents]:
        if item.name.casefold() in EXCLUDED:
            raise ValueError("excluded input boundary: " + item.name)
        if (item.exists() or item.is_symlink()) and linked(item):
            raise ValueError("link/reparse input boundary")
    return path.resolve()


def relative_path(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("expected a nonempty forward-slash relative path")
    parts = value.split("/")
    if value.startswith("/") or any(p in ("", ".", "..") for p in parts):
        raise ValueError("unsafe relative path")
    if any(p.casefold() in EXCLUDED for p in parts):
        raise ValueError("excluded relative path")
    return value


def within(root, value):
    path = selected(root / relative_path(value))
    if not path.is_relative_to(root):
        raise ValueError("path escapes snapshot root")
    return path


def read_bytes(path):
    path = selected(path)
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError("input must be a regular file no larger than 32 MiB")
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError("input grew beyond 32 MiB")
    return data


def json_value(data):
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

    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant, parse_float=finite_float)


def name_from_markdown(path):
    # YAML is used only by the resolver, not by the evaluation runner/graders.
    try:
        import yaml
    except ImportError as exc:
        raise ValueError("PyYAML is required for specification frontmatter lookup") from exc
    data = read_bytes(path)
    text = data.decode("utf-8-sig")
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        return None

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError("duplicate YAML frontmatter key: " + str(key))
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        header = yaml.load(match.group(1), Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError("invalid YAML frontmatter: " + str(path)) from exc
    if not isinstance(header, dict):
        raise ValueError("frontmatter must be a mapping: " + str(path))
    name = header.get("skill_name")
    if name is not None and not isinstance(name, str):
        raise ValueError("skill_name must be a string: " + str(path))
    return name


def resolve_spec(args):
    project = selected(args.project_root)
    if not project.is_dir():
        raise ValueError("project-root must be an existing directory")
    excluded, matches = [], []
    if args.spec:
        raw = Path(args.spec)
        path = selected(raw if raw.is_absolute() else project / raw)
        if not path.is_file() or path.suffix.casefold() != ".md":
            return 1, {"status": "SPEC_GAPS", "reason_code": "MISSING_INPUT", "candidates": [], "requested_path": str(path)}
        matches = [path]
        declared_name = name_from_markdown(path)
    else:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.name) or len(args.name) > 64:
            raise ValueError("invalid skill name")
        seen_files, total_bytes = 0, 0
        for base in (project / "docs/plan", project / "docs/design/specs"):
            base = selected(base)
            if not base.exists():
                continue
            if not base.is_dir():
                raise ValueError("specification search root is not a directory")
            pending = [base]
            while pending:
                for item in sorted(pending.pop().iterdir()):
                    if item.name.casefold() in EXCLUDED or linked(item):
                        excluded.append(str(item))
                        continue
                    if item.is_dir():
                        pending.append(item)
                    elif item.is_file() and item.suffix.casefold() == ".md":
                        seen_files += 1
                        total_bytes += item.stat().st_size
                        if seen_files > MAX_FILES or total_bytes > MAX_BYTES:
                            raise ValueError("specification lookup exceeds 2000 Markdown files or 32 MiB")
                        if name_from_markdown(item) == args.name:
                            matches.append(item.resolve())
        declared_name = args.name
    if len(matches) != 1:
        return 1, {"status": "SPEC_GAPS", "reason_code": "MISSING_INPUT" if not matches else "AMBIGUOUS_INPUT", "candidates": [str(p) for p in sorted(matches)], "excluded_boundaries": excluded}
    data = read_bytes(matches[0])
    return 0, {"status": "RESOLVED", "path": str(matches[0]), "skill_name": declared_name, "bytes": len(data), "sha256": sha(data), "excluded_boundaries": excluded}


def input_record(args):
    if not re.fullmatch(r"[a-zA-Z0-9_.-]{1,100}", args.id):
        raise ValueError("invalid input ID")
    relative_path(args.snapshot_path)
    path = selected(args.file)
    data = read_bytes(path)
    record = {
        "input": {"id": args.id, "path": args.snapshot_path, "resolved_path": str(path), "role": args.role, "bytes": len(data), "sha256": sha(data)},
    }
    if args.start_byte is not None or args.end_byte is not None:
        start = 0 if args.start_byte is None else args.start_byte
        end = len(data) if args.end_byte is None else args.end_byte
        if start < 0 or end <= start or end > len(data):
            raise ValueError("source byte range outside input")
        record["source_ref"] = {"input_id": args.id, "start_byte": start, "end_byte": end, "sha256": sha(data[start:end])}
    return 0, record


def inventory(folder):
    if not folder.is_dir():
        raise ValueError("snapshot directory missing")
    files, total = {}, 0
    pending = [folder]
    while pending:
        for item in sorted(pending.pop().iterdir()):
            path = selected(item)
            if path.is_dir():
                pending.append(path)
            elif path.is_file():
                if len(files) >= MAX_FILES or total + path.stat().st_size > MAX_BYTES:
                    raise ValueError("snapshot exceeds 2000 files or 32 MiB")
                data = read_bytes(path)
                total += len(data)
                if total > MAX_BYTES:
                    raise ValueError("snapshot grew beyond 32 MiB")
                files[path.relative_to(folder).as_posix()] = sha(data)
            else:
                raise ValueError("snapshot contains a non-regular file")
    return files


def revision_plan(args):
    root = selected(args.snapshot_root)
    if not root.is_dir():
        raise ValueError("snapshot-root must be a directory")
    request = json_value(read_bytes(within(root, args.request)))
    required_fields = {"schema_version", "run_id", "baseline", "current", "candidate", "after", "required_paths", "owned_paths", "prior_build", "baseline_before", "baseline_after"}
    optional_fields = {"rows", "status", "applied_paths", "baseline_advanced", "readback_passed", "evaluation_passed", "retry_of"}
    version = request.get("schema_version") if isinstance(request, dict) else None
    if version == "2":
        required_fields = (required_fields - {"prior_build"}) | {"prior_origin", "adoption_origin"}
    if not isinstance(request, dict) or not required_fields <= set(request) or set(request) - required_fields - optional_fields or version not in ("1", "2"):
        raise ValueError("revision request does not match schema 1 or 2")
    if version == "2":
        import graders
        problems = []
        _, observed_baseline = graders.revision_origin(root, graders.snapshot(root), request, problems)
        if problems:
            return 1, {"status": "INVALID_EVIDENCE", "observations": problems}
    folders = [within(root, request[name]) for name in ("baseline", "current", "candidate", "after")]
    if any(a == b or a.is_relative_to(b) or b.is_relative_to(a) for i, a in enumerate(folders) for b in folders[i+1:]):
        raise ValueError("revision snapshots must be disjoint")
    before, current, candidate, after = [inventory(p) for p in folders]
    if version == "2" and before != observed_baseline:
        return 1, {"status": "INVALID_EVIDENCE", "observations": ["B differs from verified prior origin"]}
    if after != current:
        raise ValueError("a new revision preview requires unchanged current and after snapshots")
    for name in ("required_paths", "owned_paths"):
        values = request[name]
        if not isinstance(values, list) or any(not isinstance(p, str) for p in values) or len(set(values)) != len(values):
            raise ValueError(name + " must contain unique relative paths")
        for value in values:
            relative_path(value)
    required = set(request["required_paths"])
    owned = set(request["owned_paths"])
    if owned != set(before):
        raise ValueError("owned paths do not match the prior generated baseline")
    if not required <= set(candidate):
        return 1, {"status": "SPEC_GAPS", "reason_code": "MISSING_INPUT", "affected_outputs": sorted(required - set(candidate)), "description": "Proposed generated snapshot omits required artifacts."}
    rows = []
    for path in sorted(set(before) | set(current) | set(candidate)):
        b, c, n = before.get(path), current.get(path), candidate.get(path)
        if path not in owned and c is not None and n is not None:
            action, reason = "CONFLICT", "Proposed path is occupied and not previously owned."
        elif c == b:
            action, reason = "USE_NEW", "Current bytes equal the verified prior baseline."
        elif c == n:
            action, reason = "KEEP_CURRENT", "Current bytes already equal the new candidate."
        elif n == b:
            action, reason = "KEEP_CURRENT", "Generation is unchanged; retain the user's current bytes."
        else:
            action, reason = "CONFLICT", "Current and generated changes diverge from the baseline."
        resulting = n if action == "USE_NEW" else c
        if path in required and resulting is None:
            action, reason = "CONFLICT", "The selected result would omit a required artifact."
        ownership = "generated" if path in owned or path in candidate else "retained_user"
        if version == "2" and path in owned and request["prior_origin"]["kind"] == "adopted":
            ownership = "adopted"
        rows.append({"path": path, "ownership": ownership, "b_sha256": b, "c_sha256": c, "n_sha256": n, "action": action, "reason": reason})
    conflict = any(row["action"] == "CONFLICT" for row in rows)
    plan = {key: request[key] for key in required_fields}
    if "retry_of" in request:
        plan["retry_of"] = request["retry_of"]
    plan.update(rows=rows, status="CONFLICT" if conflict else "PLANNED", applied_paths=[], baseline_advanced=False, readback_passed=False, evaluation_passed=False)
    return (1 if conflict else 0), plan


def adoption_plan(args):
    """Account for captured bytes only; never publish an origin or touch target."""
    import graders
    root = selected(args.snapshot_root)
    request = json_value(read_bytes(within(root, args.request)))
    graders.fields(request, {"operation", "record"})
    if request["operation"] != "adopt":
        raise ValueError("explicit adopt operation required; validation is not adoption")
    record = dict(request["record"])
    graders.fields(record, graders.ADOPTION_FIELDS - {"retained_user_paths", "recording_state"},
                   {"retained_user_paths", "recording_state", "known_defects", "handoff"})
    files = graders.snapshot(root)
    observed = inventory(within(root, record["snapshot_root"]))
    managed = graders.strings(record["managed_paths"], False)
    if not set(managed) <= set(observed):
        raise ValueError("managed paths include an unobserved file")
    record.setdefault("retained_user_paths", sorted(set(observed) - set(managed)))
    record.setdefault("recording_state", "ADOPTED")
    problems = []
    graders.adoption_record(root, files, record, problems)
    if problems:
        record["recording_state"] = "INCOMPLETE"
        return 1, {"status": "INVALID_EVIDENCE", "record": record, "observations": problems}
    return 0, record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    resolver = commands.add_parser("resolve-spec", help="Find one specification without traversing excluded boundaries")
    resolver.add_argument("--project-root", required=True)
    selection = resolver.add_mutually_exclusive_group(required=True)
    selection.add_argument("--spec")
    selection.add_argument("--name")
    source = commands.add_parser("input-record", help="Record actual input bytes and one source range")
    source.add_argument("--file", required=True)
    source.add_argument("--id", required=True)
    source.add_argument("--snapshot-path", required=True)
    source.add_argument("--role", default="spec")
    source.add_argument("--start-byte", type=int)
    source.add_argument("--end-byte", type=int)
    revision = commands.add_parser("revision-plan", help="Propose B/C/N actions without applying them")
    revision.add_argument("--snapshot-root", required=True)
    revision.add_argument("--request", required=True)
    adoption = commands.add_parser("adoption-plan", help="Account for an explicitly selected captured adoption without publication")
    adoption.add_argument("--snapshot-root", required=True)
    adoption.add_argument("--request", required=True)
    args = parser.parse_args(argv)
    try:
        code, value = {"resolve-spec": resolve_spec, "input-record": input_record, "revision-plan": revision_plan, "adoption-plan": adoption_plan}[args.operation](args)
        print(json.dumps(value, sort_keys=True, allow_nan=False))
        return code
    except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": type(exc).__name__ + ": " + str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
