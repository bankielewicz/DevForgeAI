"""Deterministic observations only; no DevForgeAI state or acceptance authority."""

import hashlib
import json
import re
import stat
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

VERSION = "1.0.0"
GRADER_IDS = ("package_links", "manifest_accounting")
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

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


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


def grade(grader_id, root, params):
    if not isinstance(params, dict):
        raise ValueError("grader params must be an object")
    if grader_id == "package_links":
        return package_links(root, params)
    if grader_id == "manifest_accounting":
        return manifest_accounting(root, params)
    raise ValueError("unknown grader: " + str(grader_id))
