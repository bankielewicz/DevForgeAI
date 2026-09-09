"""Read-only author eval: declared source identity, never a runtime/acceptance gate.

Requires PyYAML. JSON objects and Markdown YAML/JSON frontmatter are supported.
Structured references and recognized IO tables are enumerated, not just the first
match. Prose, missing_inputs meaning, other table layouts, source selection,
authorization, adoption and chronological delivery ALWAYS require manual review.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml


class UniqueLoader(yaml.SafeLoader):
    """Do not silently discard a repeated mapping key before inspection."""


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError("duplicate mapping key: " + str(key))
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)
SCHEMA = "devforge.artifact/v1"
ID = r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]+"
REFERENCE_FIELDS = {"upstream", "execution_ref", "supersedes"}
MANUAL_REQUIRED = [
    "All table identities, including unrecognized layouts and qualified native locators",
    "Every prose, missing_inputs and saved-response identity claim and source attribution",
    "Selected row retention versus actual heading section locators; missing-source-ID disclosure",
    "Required artifact delivery, ownership, user adoption and native completion",
    "Ledger/handoff readback then external receipt then final delivery chronology",
    "Historical receipt validity, current applicability and dependent continuation separately",
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metadata(text):
    """Parse only an object's own declaration, never nested examples or body text."""
    if text.startswith("---\n"):
        lines = text.splitlines()
        end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
        if end is None:
            raise ValueError("unterminated frontmatter")
        value = yaml.load("\n".join(lines[1:end]), Loader=UniqueLoader)
    elif text.lstrip().startswith("{"):
        value = yaml.load(text, Loader=UniqueLoader)
    else:
        return {}
    return value if isinstance(value, dict) else {}


def visible_lines(text):
    frontmatter = text.startswith("---\n")
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        if frontmatter:
            if number > 1 and line.strip() == "---":
                frontmatter = False
            continue
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


def heading_ids(text):
    """Actual H1-H6 IDs, with adjacent explicit anchors; row IDs are excluded."""
    found = set()
    pending = None
    for _, line in visible_lines(text):
        anchor = re.fullmatch(r'\s*<a\s+(?:id|name)=["\'](' + ID + r')["\']\s*>\s*</a>\s*', line)
        if anchor:
            pending = anchor.group(1)
            continue
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            title = heading.group(1)
            suffix = re.search(r"\[(" + ID + r")\]$", title)
            prefix = re.match(r"^(" + ID + r")\s+[—–-]\s+", title)
            if suffix or prefix:
                found.add((suffix or prefix).group(1))
            if pending:
                found.add(pending)
            pending = None
        elif line.strip():
            pending = None
    return found


def source_info(path):
    data = path.read_bytes()
    text = data.decode("utf-8")
    declaration = metadata(text)
    declared = declaration.get("schema_version") == SCHEMA
    valid = (isinstance(declaration.get("artifact_id"), str)
             and bool(declaration["artifact_id"])
             and type(declaration.get("revision")) is int
             and declaration["revision"] > 0)
    return {
        "kind": "declared-artifact" if declared else "raw-source",
        "identity_complete": valid if declared else None,
        "artifact_id": declaration.get("artifact_id") if declared else None,
        "revision": declaration.get("revision") if declared else None,
        "sha256": sha(data), "heading_ids": sorted(heading_ids(text)),
        "native_receipt_id": declaration.get("receipt_id"),
    }


def resolve(roots, store, path):
    if store not in roots:
        raise ValueError("unselected store: " + str(store))
    rel = Path(path)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("reference path is not store-relative")
    base = Path(roots[store]).resolve()
    target = (base / rel).resolve()
    if not target.is_relative_to(base):
        raise ValueError("reference leaves selected store")
    return target


def inspect_document(document, roots):
    """Return bounded observations; PASS never discharges MANUAL_REQUIRED."""
    result = {"document": str(document), "occurrences": [], "table_occurrences": [],
              "issues": [], "manual_review": "REQUIRED", "manual_required": MANUAL_REQUIRED,
              "scope": "Recognized structured reference identity/hash/sections and IO table identities only",
              "pyyaml_version": yaml.__version__}

    def issue(where, code, detail):
        result["issues"].append({"where": where, "code": code, "detail": detail})

    def inspect_ref(ref, where, required):
        occurrence = {"where": where, "reference": ref, "requires_identity_keys": required}
        result["occurrences"].append(occurrence)
        if required:
            for key in ("artifact_id", "revision", "store", "path", "sha256", "sections"):
                if key not in ref:
                    issue(where, "missing-reference-key", key)
        if "path" not in ref:
            issue(where, "missing-path", "Cannot resolve reference")
            return
        if (not required and not any(k in ref for k in ("artifact_id", "revision", "store"))
                and isinstance(ref["path"], str) and Path(ref["path"]).is_absolute()):
            # Runtime absolute locations are allowed evidence metadata, outside
            # artifact reference mappings. A grader may need the observed native
            # mount map to resolve them; no host-path or byte identity is inferred.
            occurrence.update(recognition="absolute-evidence-locator-manual-required",
                              manual_review="REQUIRED",
                              cause="Resolve actual native location and complete bytes using the observed boundary map")
            return
        try:
            target = resolve(roots, ref.get("store", "project"), ref["path"])
            info = source_info(target)
            occurrence.update(target=str(target), source=info)
        except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as exc:
            issue(where, "source-unresolved", str(exc))
            return
        if ref.get("sha256") != info["sha256"]:
            issue(where, "digest-mismatch", "Claim does not bind complete target bytes")
        claims_identity = required or "artifact_id" in ref or "revision" in ref
        if claims_identity:
            claim = (ref.get("artifact_id"), ref.get("revision"))
            actual = (info["artifact_id"], info["revision"])
            if info["kind"] == "raw-source" and claim != (None, None):
                issue(where, "raw-identity-promotion", "Native/title/selected-target labels are not the containing source's artifact identity")
            elif info["kind"] == "declared-artifact" and (not info["identity_complete"] or claim != actual):
                issue(where, "declared-identity-mismatch", {"claimed": claim, "declared": actual})
        sections = ref.get("sections", [])
        if not isinstance(sections, list) or any(not isinstance(s, str) for s in sections):
            issue(where, "invalid-sections-shape", "Expected list of actual heading IDs")
        else:
            for section in sections:
                if section not in info["heading_ids"]:
                    issue(where, "nonheading-section", section)

    def walk(value, where="$", reference_context=False):
        if isinstance(value, dict):
            # A raw locator with path/hash is inspected even inside nested evidence.
            candidate = ("path" in value and ("sha256" in value or "artifact_id" in value))
            if candidate or (reference_context and any(k in value for k in ("artifact_id", "revision", "path"))):
                inspect_ref(value, where, reference_context)
            for key, child in value.items():
                # A source's own envelope is not itself a reference.
                walk(child, where + "." + str(key), key in REFERENCE_FIELDS)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, where + "[" + str(index) + "]", reference_context)

    try:
        text = Path(document).read_text(encoding="utf-8")
        result["document_sha256"] = sha(Path(document).read_bytes())
        walk(metadata(text))
    except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as exc:
        issue("$", "document-unreadable-or-ambiguous", str(exc))
        result["result"] = "COULD_NOT_RUN"
        return result

    # Table detection is deliberately bounded. Every observed row is retained for
    # manual assessment, including rows whose locator/identity syntax is unknown.
    header = None
    for number, line in visible_lines(text):
        if not line.strip().startswith("|"):
            header = None
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        normalized = [c.casefold() for c in cells]
        if all(k in normalized for k in ("direction", "artifact id/revision", "store/path", "sha-256")):
            header = {key: normalized.index(key) for key in normalized}
            continue
        if header is None or len(cells) <= max(header.values()) or all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        row = {"line": number, "cells": cells, "manual_review": "REQUIRED"}
        result["table_occurrences"].append(row)
        locator = cells[header["store/path"]].replace("`", "")
        match = re.fullmatch(r"(project|authority)\s*[:/]\s*(.+)", locator)
        if not match:
            row["recognition"] = "unrecognized-locator"
            continue
        try:
            info = source_info(resolve(roots, match.group(1), match.group(2)))
            row.update(source=info, recognition="resolved-source")
        except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as exc:
            row.update(recognition="unresolved-source", cause=str(exc))
            continue
        where = "table:" + str(number)
        if cells[header["sha-256"]] != info["sha256"]:
            issue(where, "table-digest-mismatch", locator)
        identity = cells[header["artifact id/revision"]]
        claim = re.fullmatch(r"(" + ID + r")@(\d+|None|null)(?:\s+(?:selector|snapshot))?", identity)
        if claim:
            claimed = (claim.group(1), int(claim.group(2)) if claim.group(2).isdigit() else None)
            if info["kind"] == "raw-source":
                issue(where, "table-raw-identity-promotion", identity)
            elif claimed != (info["artifact_id"], info["revision"]):
                issue(where, "table-declared-identity-mismatch", identity)
        else:
            row["identity_recognition"] = "manual-required"
    result["result"] = "FAIL" if result["issues"] else "PASS"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--authority", type=Path)
    args = parser.parse_args()
    roots = {"project": args.project}
    if args.authority:
        roots["authority"] = args.authority
    result = inspect_document(args.document, roots)
    print(json.dumps(result, indent=2))
    return {"PASS": 0, "FAIL": 1, "COULD_NOT_RUN": 2}[result["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
