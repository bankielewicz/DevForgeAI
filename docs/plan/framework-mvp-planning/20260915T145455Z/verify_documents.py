"""Documentation observations only. Does not decide product/framework acceptance."""
from __future__ import annotations

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
MODIFIED = {
    "docs/plan/devforgeai-adaptive-framework-enhancement-notes.md",
    "docs/specs/framework/index.md",
    "docs/specs/framework/roadmap-and-decisions.md",
    "docs/specs/framework/guardrails-and-rust-runtime.md",
    "docs/specs/framework/knowledge-and-continuity.md",
}
CREATED = {
    "docs/plan/framework-mvp-next-session.md",
    "docs/specs/framework/runtime/architecture.md",
    "docs/specs/framework/mvp/scope.md",
    "docs/specs/framework/mvp/acceptance.md",
    "docs/specs/framework/evaluation/benchmark-protocol.md",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prose(content: str) -> str:
    return re.sub(r"^```.*?^```[^\n]*", "", content, flags=re.M | re.S)


def anchors(path: Path) -> set[str]:
    result = set()
    seen: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", prose(path.read_text(encoding="utf-8-sig")), re.M):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\-\s]", "", heading.lower()).strip().replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        result.add(slug if n == 0 else f"{slug}-{n}")
    return result


def main() -> int:
    failures = []
    documents = sorted(FRAMEWORK.rglob("*.md")) + [
        ROOT / "docs/plan/devforgeai-adaptive-framework-enhancement-notes.md",
        ROOT / "docs/plan/framework-mvp-next-session.md",
    ]
    ids = []
    for path in documents:
        content = path.read_text(encoding="utf-8-sig")
        front = re.match(r"---\r?\n(.*?)\r?\n---", content, re.S)
        identifier = re.search(r"^id:\s*(\S+)\s*$", front[1], re.M) if front else None
        if not identifier:
            failures.append(f"Missing frontmatter/id: {path}")
        else:
            ids.append(identifier[1])
        if path != ROOT / "docs/plan/devforgeai-adaptive-framework-enhancement-notes.md":
            if not front or "implementation_readiness: not-ready" not in front[1]:
                failures.append(f"Unexpected readiness claim: {path}")
    if len(ids) != len(set(ids)):
        failures.append("Duplicate document IDs")

    links = 0
    for path in documents:
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose(path.read_text(encoding="utf-8-sig"))):
            target = urlsplit(raw)
            if target.scheme or raw.startswith("//"):
                continue
            links += 1
            linked = (path.parent / unquote(target.path)).resolve() if target.path else path
            if linked == RUN / "verification.md" and not target.fragment:
                continue  # This command writes its own report after validation.
            if not linked.exists():
                failures.append(f"Missing link: {path.name} -> {raw}")
            elif target.fragment and linked.suffix == ".md" and unquote(target.fragment) not in anchors(linked):
                failures.append(f"Missing anchor: {path.name} -> {raw}")

    changes = []
    unchanged = 0
    copied = 0
    for entry in json.loads((RUN / "inputs-before.json").read_text(encoding="utf-8-sig")):
        path = ROOT / entry["path"]
        after = digest(path)
        same = after == entry["sha256"]
        if same:
            unchanged += 1
        elif entry["path"] not in MODIFIED:
            failures.append(f"Unexpected selected input change: {entry['path']}")
        else:
            changes.append(entry["path"])
        before_copy = RUN / "before" / entry["path"]
        if before_copy.exists():
            copied += 1
            if digest(before_copy) != entry["sha256"]:
                failures.append(f"Original copy mismatch: {entry['path']}")
    for rel in CREATED:
        if not (ROOT / rel).is_file():
            failures.append(f"Missing new document: {rel}")

    manifest = [{"path": rel, "sha256": digest(ROOT / rel), "bytes": (ROOT / rel).stat().st_size}
                for rel in sorted(MODIFIED | CREATED)]
    (RUN / "document-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    command = "python -B -X utf8 docs/plan/framework-mvp-planning/20260915T145455Z/verify_documents.py"
    result = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "documentation inventory, readiness labels, local links, selected input changes and retained original copies",
        "command": command, "cwd": str(ROOT), "python": platform.python_version(),
        "markdown_documents": len(documents), "local_links_checked": links,
        "unchanged_selected_inputs": unchanged, "modified_selected_inputs": sorted(changes),
        "original_copies_verified": copied, "delivered_documents": len(manifest),
        "failures": failures, "exit_code": 1 if failures else 0,
        "runtime_tests": "NOT_RUN: documentation-only task",
        "framework_acceptance": "NOT_EVALUATED",
    }
    (RUN / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report = ["# MVP planning documentation verification", "",
              f"Observed: {result['observed_at_utc']}", "",
              f"Documentation checks: {'FAIL' if failures else 'PASS'}; {len(documents)} Markdown documents, {links} local links.", "",
              f"Selected inputs: {unchanged} unchanged; {len(changes)} within the declared documentation edit set. Verified {copied} exact original copies. Delivery manifest: {len(manifest)} documents.", "",
              f"Command: `{command}`", "", f"Working directory: `{ROOT}`. Python {platform.python_version()}. Exit code: {result['exit_code']}.", "",
              "[Detailed observations](verification.json) · [Document identities](document-manifest.json) · [Inputs before editing](inputs-before.json) · [Independent review](review.md)", "",
              "These observations do not establish semantic completeness, implementation readiness, runtime support or performance. No product TDD, coverage, model trials, installation or framework acceptance was performed. Prior evidence was not rerun or rewritten."]
    if failures:
        report += ["", "Failures:", ""] + ["- " + failure for failure in failures]
    (RUN / "verification.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("markdown_documents", "local_links_checked", "unchanged_selected_inputs", "original_copies_verified", "failures", "exit_code")}))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
