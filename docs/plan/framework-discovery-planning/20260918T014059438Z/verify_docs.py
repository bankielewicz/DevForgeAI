"""Read-only documentation observations; writes reports only in this evidence run."""

import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit


RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
FRAMEWORK = ROOT / "docs/specs/framework"
SPEC = FRAMEWORK / "workflows/phase-1-brainstorm-spec.md"


def identity(path):
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "size_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def prose(text):
    result = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)[0]
            elif marker.group(1)[0] == fence:
                fence = None
            continue
        if fence is None:
            result.append(line)
    return "\n".join(result)


def anchors(path):
    text = prose(path.read_text(encoding="utf-8-sig"))
    found = set(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    duplicates = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, flags=re.M):
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        occurrence = duplicates.get(slug, 0)
        duplicates[slug] = occurrence + 1
        found.add(slug if occurrence == 0 else f"{slug}-{occurrence}")
    return found


def main():
    baseline = json.loads((RUN / "inputs-before.json").read_text(encoding="utf-8-sig"))
    selected = set(baseline["selected_existing_files"])
    allowed_new = baseline["intended_new_file"]
    errors = []
    before_paths = set()
    changes = []
    preserved = []
    original_phase_labels = []
    for entry in baseline["inputs"]:
        path = ROOT / entry["path"]
        before_paths.add(entry["path"])
        if not path.is_file():
            errors.append({"check": "preservation", "missing": entry["path"]})
            continue
        after = identity(path)
        if entry["path"].startswith("docs/specs/framework/") and path.suffix == ".md":
            original = RUN / "before" / path.name if entry["path"] in selected else path
            matches = re.findall(r"\b(?:phase|route)[ -]?[01]\b", original.read_text(encoding="utf-8-sig"), re.I)
            original_phase_labels.extend({"path": entry["path"], "label": value} for value in matches)
        unchanged = after["sha256"] == entry["sha256"] and after["size_bytes"] == entry["size_bytes"]
        if entry["path"] in selected:
            saved = RUN / "before" / path.name
            if not saved.is_file() or hashlib.sha256(saved.read_bytes()).hexdigest() != entry["sha256"]:
                errors.append({"check": "before_snapshot", "path": entry["path"]})
            if not unchanged:
                changes.append({"path": entry["path"], "before": entry, "after": after})
        elif not unchanged:
            errors.append({"check": "unselected_input_changed", "path": entry["path"]})
        else:
            preserved.append(after)

    for path in sorted(FRAMEWORK.rglob("*")):
        if path.is_file() and path.relative_to(ROOT).as_posix() not in before_paths:
            entry = identity(path)
            if entry["path"] != allowed_new:
                errors.append({"check": "unexpected_new_framework_file", "path": entry["path"]})
            changes.append({"path": entry["path"], "before": None, "after": entry})

    documents = sorted(FRAMEWORK.rglob("*.md"))
    links = []
    external_links = 0
    anchor_cache = {}
    for path in documents:
        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(ROOT).as_posix()
        if "\ufffd" in text:
            errors.append({"check": "replacement_character", "path": relative})
        for line_number, line in enumerate(prose(text).splitlines(), 1):
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", line):
                target = target.strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith("//"):
                    external_links += 1
                    continue
                linked = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                item = {"source": relative, "target": target, "exists": linked.exists()}
                if not item["exists"]:
                    errors.append({"check": "local_link", **item})
                elif parsed.fragment and linked.suffix.lower() == ".md":
                    if linked not in anchor_cache:
                        anchor_cache[linked] = anchors(linked)
                    item["anchor_exists"] = unquote(parsed.fragment) in anchor_cache[linked]
                    if not item["anchor_exists"]:
                        errors.append({"check": "heading_anchor", **item})
                links.append(item)
        if relative in selected or relative == allowed_new:
            if not text.startswith("---\n") or not re.search(r"^id: \S+$", text, re.M):
                errors.append({"check": "frontmatter", "path": relative})
            if len(re.findall(r"^\s*```", text, re.M)) % 2:
                errors.append({"check": "unbalanced_code_fence", "path": relative})
            if re.search(r"\b(?:TODO|TBD|FIXME)\b", text):
                errors.append({"check": "unresolved_placeholder", "path": relative})
            table_width = None
            for line_number, line in enumerate(text.splitlines(), 1):
                if line.startswith("|") and line.endswith("|"):
                    width = len(re.split(r"(?<!\\)\|", line)) - 2
                    if table_width is not None and width != table_width:
                        errors.append({"check": "table_width", "path": relative, "line": line_number})
                    table_width = width
                else:
                    table_width = None

    spec_text = SPEC.read_text(encoding="utf-8")
    requirements = re.findall(r"^\*\*(BR-\d{3})\s", spec_text, re.M)
    case_rows = re.findall(r"^\| (BV-\d{2}) \| ([^|]+) \|", spec_text, re.M)
    cases = [row[0] for row in case_rows]
    mapped = set()
    for _, references in case_rows:
        for reference in references.strip().split("/"):
            mapped.add(reference if reference.startswith("BR-") else "BR-" + reference)
    expected_requirements = {f"BR-{index:03d}" for index in range(1, 15)}
    expected_cases = {f"BV-{index:02d}" for index in range(1, 21)}
    if set(requirements) != expected_requirements or len(requirements) != 14:
        errors.append({"check": "requirement_inventory", "observed": requirements})
    if set(cases) != expected_cases or len(cases) != 20:
        errors.append({"check": "case_inventory", "observed": cases})
    if mapped != expected_requirements:
        errors.append({"check": "requirement_case_mapping", "missing": sorted(expected_requirements - mapped), "unknown": sorted(mapped - expected_requirements)})
    obsolete_names = []
    for path in [ROOT / name for name in selected] + [SPEC]:
        if re.search(r"\bspec-(?:create|review)\b", path.read_text(encoding="utf-8-sig")):
            obsolete_names.append(path.relative_to(ROOT).as_posix())
    if obsolete_names:
        errors.append({"check": "user_selected_workflow_names", "paths": obsolete_names})
    if original_phase_labels:
        errors.append({"check": "original_numbered_phase_search", "matches": original_phase_labels})

    exit_code = 0 if not errors else 1
    result = {
        "scope": "Documentation observations only; not skill or product QA",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "working_directory": str(ROOT),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "argv": [sys.executable, "-B", "-X", "utf8", str(Path(__file__).resolve())],
        "exit_code": exit_code,
        "markdown_documents": len(documents),
        "local_links_checked": len(links),
        "external_links_not_requested_or_revalidated": external_links,
        "changed_existing_files": sum(item["before"] is not None for item in changes),
        "new_specification_files": sum(item["before"] is None for item in changes),
        "unchanged_bound_inputs": len(preserved),
        "retained_before_snapshots": len(selected),
        "original_phase_0_or_1_labels": original_phase_labels,
        "specified_requirements": requirements,
        "specified_future_cases": cases,
        "requirement_mapping_complete": mapped == expected_requirements,
        "errors": errors,
        "skill_evaluation": "NOT_RUN",
        "product_tests": "NOT_RUN",
        "runtime_coverage": "NOT_RUN",
        "native_diagnostic": "NOT_RUN",
        "framework_acceptance": "NOT_EVALUATED",
        "limits": ["Local links and Markdown headings checked; external URLs not fetched.", "Requirement mappings check inventory, not future behavioral success.", "Preservation scope is the 35 recorded inputs plus retained document snapshots, not a repository-wide scan."]
    }
    for filename, value in [("verification.json", result), ("changed-file-manifest.json", changes), ("local-link-observations.json", links)]:
        (RUN / filename).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
