#!/usr/bin/env python3
"""Read-only structural inspection of one skill; never evaluates its behavior."""
from __future__ import annotations

import argparse
from bisect import bisect_right
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit

if sys.version_info < (3, 11):
    print("inspect_skill.py requires Python 3.11 or newer.", file=sys.stderr)
    raise SystemExit(2)
import tomllib

SCHEMA = "devforge.skill-structure/v1"
MAX_ENTRIES = 4096
MAX_DEPTH = 32
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024
MAX_FRONTMATTER_BYTES = 128 * 1024
MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
MAX_LINK_MARKERS = 4096
CHUNK_BYTES = 65536
RULES = {
    "S001": "Skill root is an accessible directory.",
    "S002": "Package inventory and exact-byte hashes are complete within bounds.",
    "S003": "SKILL.md exists as a readable UTF-8 file.",
    "S004": "SKILL.md has safely parsed YAML mapping frontmatter without duplicate keys.",
    "S005": "Frontmatter name and description are nonempty strings.",
    "S006": "Name follows the 1-64-character naming rules and matches the folder.",
    "S007": "Local Markdown file links in SKILL.md and references resolve inside the package.",
    "S008": "Package symlinks are resolvable and remain inside the package.",
    "S009": "The selected source/installed evaluation packaging rule is satisfied.",
    "S010": "Inventoried JSON files parse without duplicate keys or non-JSON numbers.",
    "S011": "Inventoried TOML files parse with Python tomllib.",
    "S012": "Inventoried Python files parse with ast.parse without execution.",
    "S013": "The selected specification is readable and its exact bytes are hashed.",
}


def contained(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def exception_text(error: Exception) -> str:
    return f"{type(error).__name__}: {error}"


class Inspector:
    def __init__(self, root: Path, specification: Path, mode: str):
        self.root, self.specification, self.mode = root, specification, mode
        self.problems: dict[str, list[tuple[str, str, dict]]] = {
            identifier: [] for identifier in RULES
        }
        self.notes: dict[str, list[str]] = {identifier: [] for identifier in RULES}
        self.evidence: dict[str, list[dict]] = {identifier: [] for identifier in RULES}
        self.hashes: dict[str, str] = {}
        self.data: dict[str, bytes] = {}
        self.total_bytes = 0
        self.entry_count = 0
        self.inventory_complete = True
        self.spec_hash: str | None = None
        self.root_ok = False
        self.evals_present = False

    def note(self, identifier: str, reason: str, path: Path | None = None):
        self.notes[identifier].append(reason)
        if path is not None:
            self.evidence[identifier].append({"path": str(path)})

    def problem(self, identifier: str, outcome: str, reason: str,
                path: Path, line: int | None = None):
        evidence = {"path": str(path)}
        if isinstance(line, int) and line > 0:
            evidence["line"] = line
        self.problems[identifier].append((outcome, reason, evidence))

    def incomplete(self, reason: str, path: Path):
        self.inventory_complete = False
        self.problem("S002", "COULD_NOT_RUN", reason, path)

    def bytes_for(self, path: Path, *, package: bool) -> bytes | None:
        """Bounded, streamed read; return no digest for an incomplete read."""
        rule = "S002" if package else "S013"
        try:
            resolved = path.resolve(strict=True)
            if package and not contained(resolved, self.root):
                self.problem("S008", "FAIL", "Resolved resource escapes the package.", path)
                self.incomplete("Escaping resource was not read.", path)
                return None
            with resolved.open("rb") as stream:
                before = os.fstat(stream.fileno())
                if not stat.S_ISREG(before.st_mode):
                    self.problem(rule, "COULD_NOT_RUN", "Resource is not a regular file.", path)
                    if package:
                        self.inventory_complete = False
                    return None
                if before.st_size > MAX_FILE_BYTES:
                    raise OverflowError(f"File exceeds {MAX_FILE_BYTES} bytes.")
                chunks: list[bytes] = []
                size = 0
                digest = hashlib.sha256()
                while True:
                    chunk = stream.read(CHUNK_BYTES)
                    if not chunk:
                        break
                    size += len(chunk)
                    if package:
                        self.total_bytes += len(chunk)
                    if size > MAX_FILE_BYTES:
                        raise OverflowError(f"File exceeds {MAX_FILE_BYTES} bytes while reading.")
                    if package and self.total_bytes > MAX_TOTAL_BYTES:
                        raise OverflowError(f"Package reads exceed {MAX_TOTAL_BYTES} bytes.")
                    digest.update(chunk)
                    chunks.append(chunk)
                after = os.fstat(stream.fileno())
                current = resolved.stat()
                identity = lambda value: (
                    value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns
                )
                if identity(before) != identity(after) or identity(after) != identity(current):
                    raise RuntimeError("Resource changed while being read.")
            if package:
                relative = path.relative_to(self.root).as_posix()
                self.hashes[relative] = digest.hexdigest()
            else:
                self.spec_hash = digest.hexdigest()
            return b"".join(chunks)
        except (OSError, RuntimeError, OverflowError) as error:
            self.problem(rule, "COULD_NOT_RUN", exception_text(error), path)
            if package:
                self.inventory_complete = False
            return None

    def inventory(self):
        try:
            if not self.root.is_dir():
                self.problem("S001", "COULD_NOT_RUN",
                             "The supplied root is missing or is not a directory.", self.root)
                self.inventory_complete = False
                return
            self.root_ok = True
            self.note("S001", "Directory found.", self.root)
        except OSError as error:
            self.problem("S001", "COULD_NOT_RUN", exception_text(error), self.root)
            self.inventory_complete = False
            return
        stack = [(self.root, 0)]
        while stack:
            directory, depth = stack.pop()
            if depth > MAX_DEPTH:
                self.incomplete(f"Directory depth exceeds {MAX_DEPTH}.", directory)
                continue
            try:
                # scandir iteration itself is bounded; do not materialize huge directories.
                with os.scandir(directory) as entries:
                    for entry in entries:
                        self.entry_count += 1
                        path = Path(entry.path)
                        if self.entry_count > MAX_ENTRIES:
                            self.incomplete(f"Inventory exceeds {MAX_ENTRIES} entries.", path)
                            stack.clear()
                            return
                        if path.relative_to(self.root).parts[0] == "evals":
                            self.evals_present = True
                        try:
                            item_stat = entry.stat(follow_symlinks=False)
                            if stat.S_ISLNK(item_stat.st_mode):
                                try:
                                    destination = path.resolve(strict=True)
                                except (FileNotFoundError, RuntimeError) as error:
                                    self.problem("S008", "FAIL",
                                                 "Broken or cyclic symlink: " + exception_text(error), path)
                                    self.incomplete("Unresolvable symlink was not read.", path)
                                    continue
                                except OSError as error:
                                    self.problem("S008", "COULD_NOT_RUN",
                                                 "Cannot inspect symlink: " + exception_text(error), path)
                                    self.incomplete("Unreadable symlink was not read.", path)
                                    continue
                                if not contained(destination, self.root):
                                    self.problem("S008", "FAIL", "Symlink escapes the package.", path)
                                    self.incomplete("Escaping symlink was not read.", path)
                                    continue
                                self.note("S008", "Contained symlink.", path)
                                if destination.is_dir():
                                    # Avoid aliased recursive inventories and directory cycles.
                                    self.incomplete("Contained directory symlinks are not traversed.", path)
                                    continue
                                if not destination.is_file():
                                    self.incomplete("Symlink target is not a regular file.", path)
                                    continue
                            elif stat.S_ISDIR(item_stat.st_mode):
                                stack.append((path, depth + 1))
                                continue
                            elif not stat.S_ISREG(item_stat.st_mode):
                                self.incomplete("Special filesystem entry is not inspected.", path)
                                continue
                            if self.total_bytes >= MAX_TOTAL_BYTES:
                                self.incomplete(f"Package read budget of {MAX_TOTAL_BYTES} bytes exhausted.", path)
                                continue
                            content = self.bytes_for(path, package=True)
                            if content is not None:
                                self.data[path.relative_to(self.root).as_posix()] = content
                        except OSError as error:
                            self.incomplete(exception_text(error), path)
            except OSError as error:
                self.incomplete(exception_text(error), directory)
        self.note("S002", f"Hashed {len(self.hashes)} files; read {self.total_bytes} package bytes. "
                  f"Limits: {MAX_ENTRIES} entries, depth {MAX_DEPTH}, "
                  f"{MAX_FILE_BYTES} bytes/file, {MAX_TOTAL_BYTES} total bytes.", self.root)
        if not self.inventory_complete and not self.problems["S008"]:
            self.problem("S008", "COULD_NOT_RUN",
                         "Incomplete inventory prevents a complete symlink assertion.", self.root)

    def frontmatter(self):
        skill_path = self.root / "SKILL.md"
        raw = self.data.get("SKILL.md")
        if raw is None:
            try:
                absent = self.root_ok and not skill_path.exists() and not skill_path.is_symlink()
                is_directory = self.root_ok and skill_path.is_dir()
            except OSError:
                absent, is_directory = False, False
            self.problem("S003", "FAIL" if absent or is_directory else "COULD_NOT_RUN",
                         "SKILL.md is missing." if absent else "SKILL.md is a directory." if is_directory else
                         "SKILL.md could not be read as an inventoried regular file.", skill_path)
            self.frontmatter_unavailable(skill_path)
            return
        try:
            content = raw.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            self.problem("S003", "FAIL", exception_text(error), skill_path)
            self.frontmatter_unavailable(skill_path)
            return
        self.note("S003", "SKILL.md decoded as UTF-8 (an optional BOM is accepted).", skill_path)
        lines = content.splitlines()
        if not lines or lines[0] != "---":
            self.problem("S004", "FAIL", "Frontmatter must begin on the first line with ---.", skill_path, 1)
            self.fields_unavailable(skill_path)
            return
        end = next((index for index in range(1, len(lines)) if lines[index] == "---"), None)
        if end is None:
            self.problem("S004", "FAIL", "The closing --- frontmatter delimiter is missing.", skill_path, 1)
            self.fields_unavailable(skill_path)
            return
        front = "\n".join(lines[1:end])
        if len(front.encode("utf-8")) > MAX_FRONTMATTER_BYTES:
            self.problem("S004", "COULD_NOT_RUN",
                         f"Frontmatter exceeds {MAX_FRONTMATTER_BYTES} bytes.", skill_path)
            self.fields_unavailable(skill_path)
            return
        try:
            import yaml
        except ImportError as error:
            self.problem("S004", "COULD_NOT_RUN",
                         "PyYAML is unavailable; no replacement YAML parser is used. " +
                         exception_text(error), skill_path)
            self.fields_unavailable(skill_path)
            return

        class UniqueSafeLoader(yaml.SafeLoader):
            pass

        def construct_mapping(loader, node, deep=False):
            loader.flatten_mapping(node)
            mapping = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as error:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping", node.start_mark,
                        "unhashable mapping key", key_node.start_mark
                    ) from error
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping", node.start_mark,
                        f"duplicate mapping key {key!r}", key_node.start_mark
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        UniqueSafeLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
        )
        try:
            metadata = yaml.load(front, Loader=UniqueSafeLoader)
        except yaml.YAMLError as error:
            mark = getattr(error, "problem_mark", None)
            self.problem("S004", "FAIL", exception_text(error), skill_path,
                         mark.line + 2 if mark is not None else None)
            self.fields_unavailable(skill_path)
            return
        except (RecursionError, MemoryError) as error:
            self.problem("S004", "COULD_NOT_RUN", exception_text(error), skill_path)
            self.fields_unavailable(skill_path)
            return
        if not isinstance(metadata, dict):
            self.problem("S004", "FAIL", "Frontmatter must be a YAML mapping.", skill_path)
            self.fields_unavailable(skill_path)
            return
        self.note("S004", f"Parsed with PyYAML {getattr(yaml, '__version__', 'unknown')}; "
                  "safe loader and duplicate-key rejection.", skill_path)
        for name in ("name", "description"):
            if not isinstance(metadata.get(name), str) or not metadata[name].strip():
                self.problem("S005", "FAIL", f"{name} must be a nonempty string.", skill_path)
        self.note("S005", "Additional frontmatter fields are permitted; their semantics are not evaluated.")
        name = metadata.get("name")
        if not isinstance(name, str):
            self.problem("S006", "COULD_NOT_RUN", "No string name is available for naming checks.", skill_path)
        elif not 1 <= len(name) <= 64 or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is None:
            self.problem("S006", "FAIL",
                         "Name must be 1–64 ASCII lowercase letters/digits with single internal hyphens.", skill_path)
        elif name != self.root.name:
            self.problem("S006", "FAIL", f"Name {name!r} differs from folder {self.root.name!r}.", skill_path)
        else:
            self.note("S006", "Name format and exact folder match satisfied.", skill_path)

    def frontmatter_unavailable(self, path: Path):
        self.problem("S004", "COULD_NOT_RUN", "Readable UTF-8 SKILL.md is required.", path)
        self.fields_unavailable(path)

    def fields_unavailable(self, path: Path):
        for rule in ("S005", "S006"):
            self.problem(rule, "COULD_NOT_RUN", "Parsed frontmatter is unavailable.", path)

    def syntax(self):
        counts = {"S010": 0, "S011": 0, "S012": 0}
        for relative, raw in sorted(self.data.items()):
            path = self.root / relative
            suffix = path.suffix.lower()
            rule = {".json": "S010", ".toml": "S011", ".py": "S012"}.get(suffix)
            if rule is None:
                continue
            counts[rule] += 1
            try:
                if suffix == ".json":
                    def unique_object(pairs):
                        result = {}
                        for key, value in pairs:
                            if key in result:
                                raise ValueError(f"Duplicate JSON key {key!r}.")
                            result[key] = value
                        return result

                    def invalid_constant(value):
                        raise ValueError(f"{value} is not a JSON number.")

                    json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object,
                               parse_constant=invalid_constant)
                elif suffix == ".toml":
                    tomllib.loads(raw.decode("utf-8"))
                else:
                    # Bytes preserve Python's declared source encoding.
                    ast.parse(raw, filename=str(path), mode="exec")
                self.evidence[rule].append({"path": str(path)})
            except (UnicodeError, ValueError, SyntaxError) as error:
                self.problem(rule, "FAIL", exception_text(error), path,
                             getattr(error, "lineno", None))
            except (RecursionError, MemoryError) as error:
                self.problem(rule, "COULD_NOT_RUN", exception_text(error), path)
        for rule, count in counts.items():
            self.note(rule, f"Parsed {count} applicable inventoried files; no schema or runtime behavior checked.")
            if not self.inventory_complete:
                self.problem(rule, "COULD_NOT_RUN",
                             "Incomplete inventory prevents a complete file-type assertion.", self.root)

    def markdown(self):
        counts = {"local": 0, "external": 0, "anchor": 0}
        for relative, raw in sorted(self.data.items()):
            if relative != "SKILL.md" and not (
                relative.startswith("references/") and Path(relative).suffix.lower() == ".md"
            ):
                continue
            path = self.root / relative
            if len(raw) > MAX_MARKDOWN_BYTES:
                self.problem("S007", "COULD_NOT_RUN",
                             f"Markdown exceeds {MAX_MARKDOWN_BYTES} bytes.", path)
                continue
            try:
                body = raw.decode("utf-8-sig")
            except UnicodeDecodeError as error:
                self.problem("S007", "FAIL", exception_text(error), path)
                continue
            if relative == "SKILL.md":
                lines = body.splitlines(keepends=True)
                if lines and lines[0].strip() == "---":
                    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
                    if closing is not None:
                        body = "".join("\n" if line.endswith("\n") else "" for line in lines[:closing + 1]) + "".join(lines[closing + 1:])
            destinations, unsupported = markdown_destinations(body)
            for line, reason in unsupported:
                self.problem("S007", "COULD_NOT_RUN", reason, path, line)
            for destination, line in destinations:
                if re.search(r"&(?:#\d+|#x[0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]+);", destination):
                    continue  # The extractor records this unsupported representation.
                target = re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_\x60{|}~])", r"\1", destination)
                if target.startswith("#") or not target:
                    counts["anchor"] += 1
                    continue
                if re.match(r"^[A-Za-z]:[/\\]", target):
                    self.problem("S007", "FAIL", "Drive-absolute links are not portable package resources.", path, line)
                    continue
                try:
                    parsed = urlsplit(target)
                except ValueError as error:
                    self.problem("S007", "FAIL", "Invalid link destination: " + str(error), path, line)
                    continue
                if parsed.scheme.lower() == "file":
                    self.problem("S007", "FAIL", "file: links are machine-local, not package-relative resources.", path, line)
                    continue
                if parsed.scheme or parsed.netloc:
                    counts["external"] += 1
                    continue
                decoded = unquote(parsed.path)
                if not decoded:
                    counts["anchor"] += 1
                    continue
                counts["local"] += 1
                try:
                    if "\0" in decoded or "\\" in decoded:
                        self.problem("S007", "FAIL",
                                     "Local Markdown destinations must use portable paths without NUL or backslashes.", path, line)
                        continue
                    resolved = (path.parent / decoded).resolve(strict=True)
                    if not contained(resolved, self.root):
                        self.problem("S007", "FAIL", f"Link escapes the package: {destination!r}.", path, line)
                    elif not resolved.is_file() and not resolved.is_dir():
                        self.problem("S007", "FAIL", f"Link does not identify a file or directory: {destination!r}.", path, line)
                    else:
                        self.evidence["S007"].append({"path": str(path), "line": line})
                except FileNotFoundError:
                    self.problem("S007", "FAIL", f"Local link target is missing: {destination!r}.", path, line)
                except (OSError, RuntimeError) as error:
                    self.problem("S007", "COULD_NOT_RUN",
                                 f"Cannot resolve {destination!r}: {exception_text(error)}", path, line)
        self.note("S007", f"Examined {counts['local']} local links; ignored {counts['external']} external URLs "
                  f"and {counts['anchor']} empty/anchor-only destinations. Anchor existence is not checked.")
        if not self.inventory_complete or "SKILL.md" not in self.data:
            self.problem("S007", "COULD_NOT_RUN", "The required Markdown inventory is incomplete.", self.root)

    def run(self) -> dict:
        self.bytes_for(self.specification, package=False)
        if self.spec_hash is not None:
            self.note("S013", "Specification bytes hashed; specification meaning is not evaluated.", self.specification)
        self.inventory()
        if not self.inventory_complete:
            self.problem("S008", "COULD_NOT_RUN",
                         "Incomplete inventory prevents a complete symlink assertion.", self.root)
        if not self.root_ok:
            for identifier in ("S002", "S008", "S009"):
                self.problem(identifier, "COULD_NOT_RUN", "An accessible skill root is required.", self.root)
        self.frontmatter()
        self.syntax()
        self.markdown()
        if self.mode == "installed" and self.evals_present:
            self.problem("S009", "FAIL", "Top-level evals exists in an installed package.", self.root / "evals")
        elif not self.inventory_complete:
            self.problem("S009", "COULD_NOT_RUN", "Incomplete inventory prevents a packaging assertion.", self.root)
        else:
            self.note("S009", "Source mode permits evals; absent evals is not a structural defect."
                      if self.mode == "source" else "No top-level evals found in installed mode.", self.root)
        checks = []
        for identifier, default_reason in RULES.items():
            problems = self.problems[identifier]
            outcomes = {outcome for outcome, _, _ in problems}
            outcome = "FAIL" if "FAIL" in outcomes else "COULD_NOT_RUN" if outcomes else "PASS"
            reasons = [reason for _, reason, _ in problems] + self.notes[identifier]
            evidence = self.evidence[identifier] + [item for _, _, item in problems]
            # Keep every distinct unreadable/invalid file, while avoiding repeated identical locators.
            unique_evidence = list({json.dumps(item, sort_keys=True): item for item in evidence}.values())
            checks.append({"id": identifier, "outcome": outcome,
                           "reason": " ".join(reasons) if reasons else default_reason,
                           "evidence": unique_evidence})
        outcomes = {item["outcome"] for item in checks}
        overall = "FAIL" if "FAIL" in outcomes else "COULD_NOT_RUN" if "COULD_NOT_RUN" in outcomes else "PASS"
        return {
            "schema_version": SCHEMA,
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "skill_root": str(self.root),
            "mode": self.mode,
            "specification": {"path": str(self.specification), "sha256": self.spec_hash},
            "files_sha256": dict(sorted(self.hashes.items())),
            "checks": checks,
            "overall": overall,
            "behavior": "NOT_EVALUATED",
        }


def markdown_destinations(text: str) -> tuple[list[tuple[str, int]], list[tuple[int, str]]]:
    """Extract common Markdown file-link syntax; flag unsupported constructs.

    This is a bounded resource-link reader, not a complete CommonMark renderer.
    See structural-checks.md for the exact supported scope.
    """
    masked = list(text)
    offset = 0
    fence = None
    unsupported: list[tuple[int, str]] = []
    for line in text.splitlines(keepends=True):
        marker = re.match(r" {0,3}(\x60{3,}|~{3,})", line)
        if fence:
            for i in range(offset, offset + len(line)):
                if masked[i] != "\n":
                    masked[i] = " "
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
        elif marker:
            fence = marker.group(1)
            for i in range(offset, offset + len(line)):
                if masked[i] != "\n":
                    masked[i] = " "
        elif line.startswith("    ") or line.startswith("\t"):
            # A full Markdown renderer is needed to distinguish nested-list prose from code.
            if re.search(r"\[[^\]]+\]\s*(?:\(|\[|:)|<[^>]+(?:href|src)\s*=", line):
                unsupported.append((text.count("\n", 0, offset) + 1,
                                    "Indented link syntax requires Markdown renderer review."))
            for i in range(offset, offset + len(line)):
                if masked[i] != "\n":
                    masked[i] = " "
        offset += len(line)
    body = "".join(masked)
    # Code spans use matching delimiter lengths. Preserve line numbers.
    body = re.sub(r"(\x60+)(?!\x60)([\s\S]*?)(?<!\x60)\1(?!\x60)",
                  lambda match: re.sub(r"[^\n]", " ", match.group()), body)
    result: list[tuple[str, int]] = []
    definitions: dict[str, tuple[str, int]] = {}
    if body.count("[") > MAX_LINK_MARKERS:
        unsupported.append((1, f"Markdown link markers exceed {MAX_LINK_MARKERS}."))
        return result, unsupported
    line_ends = [match.start() for match in re.finditer("\n", body)]

    def line_at(position):
        return bisect_right(line_ends, position - 1) + 1

    def normalize(label):
        return " ".join(label.split()).casefold()

    def destination_at(position):
        position0 = position
        if position < len(body) and body[position] == "<":
            end = position + 1
            while end < len(body):
                if body[end] == "\\":
                    end += 2
                    continue
                if body[end] == ">":
                    return body[position + 1:end], end + 1
                if body[end] == "\n":
                    return None
                end += 1
            return None
        depth = 0
        while position < len(body):
            char = body[position]
            if char == "\\":
                position += 2
                continue
            if char.isspace() or (char == ")" and depth == 0):
                break
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            if depth > 32:
                return None
            position += 1
        if depth:
            return None
        return body[position0:position], position

    for match in re.finditer(r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*", body):
        parsed = destination_at(match.end())
        if parsed is None or not parsed[0]:
            unsupported.append((line_at(match.start()), "Unparsed Markdown reference destination."))
            continue
        key = normalize(match.group(1))
        definitions.setdefault(key, (parsed[0], line_at(match.start())))
        result.append((parsed[0], line_at(match.start())))
    i = 0
    while i < len(body):
        if body[i] == "\\":
            i += 2
            continue
        if body[i] != "[":
            i += 1
            continue
        start, depth, end = i, 1, i + 1
        while end < len(body) and depth:
            if body[end] == "\\":
                end += 2
                continue
            if body[end] == "[":
                depth += 1
            elif body[end] == "]":
                depth -= 1
            end += 1
        if depth:
            i += 1
            continue
        label = body[start + 1:end - 1]
        if end < len(body) and body[end] == "(":
            pos = end + 1
            while pos < len(body) and body[pos].isspace():
                pos += 1
            parsed = destination_at(pos)
            if parsed is None:
                unsupported.append((line_at(start), "Unparsed inline Markdown link destination."))
            else:
                target, stop = parsed
                tail = body[stop:]
                # Optional quoted/parenthesized titles; escaped characters are accepted.
                title_end = re.match(r'\s*(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\((?:\\.|[^)\\])*\))?\s*\)', tail)
                if title_end is None:
                    unsupported.append((line_at(start), "Unsupported or malformed inline Markdown link ending."))
                else:
                    result.append((target, line_at(start)))
                    end = stop + title_end.end()
        elif end < len(body) and body[end] == "[":
            close = body.find("]", end + 1)
            if close != -1:
                reference = body[end + 1:close] or label
                if normalize(reference) in definitions:
                    result.append((definitions[normalize(reference)][0], line_at(start)))
                end = close + 1
        elif normalize(label) in definitions and not (end < len(body) and body[end] == ":"):
            result.append((definitions[normalize(label)][0], line_at(start)))
        i = max(end, i + 1)
    for match in re.finditer(r"<(?:a|img|link|script)\b[^>]*(?:href|src)\s*=", body, re.IGNORECASE):
        unsupported.append((line_at(match.start()), "HTML resource attributes are outside the Markdown link parser."))
    # Markdown URLs containing entities need a full renderer to resolve reliably.
    for destination, line in result:
        if re.search(r"&(?:#\d+|#x[0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]+);", destination):
            unsupported.append((line, "Entity-encoded link destinations require renderer review."))
    return result, unsupported


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only structural checks for one skill. Does not run skill code or evaluate behavior."
    )
    parser.add_argument("--skill-root", required=True, type=Path, help="Candidate skill folder.")
    parser.add_argument("--specification", required=True, type=Path, help="Selected specification file to hash.")
    parser.add_argument("--mode", choices=("source", "installed"), default="source",
                        help="Installed mode prohibits top-level evals; source mode permits it.")
    parser.add_argument("--output", required=True, type=Path,
                        help="New JSON file outside the skill root; parent directory must exist.")
    args = parser.parse_args()
    try:
        root = args.skill_root.expanduser().resolve()
        specification = args.specification.expanduser().resolve()
        output = args.output.expanduser().resolve()
        if contained(output, root):
            raise ValueError("Output must be outside the candidate skill tree.")
        if output == specification:
            raise ValueError("Output must not replace the selected specification.")
        if output.exists() or output.is_symlink():
            raise FileExistsError("Output already exists; previous reports are never overwritten.")
        report = Inspector(root, specification, args.mode).run()
        # Exclusive creation provides collision protection even after the initial path check.
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
        print(f"{report['overall']}: {output}")
        return {"PASS": 0, "FAIL": 1, "COULD_NOT_RUN": 2}[report["overall"]]
    except Exception as error:
        # Unexpected implementation/environment errors must never look like passing checks.
        print("No complete structural report was produced: " + exception_text(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
