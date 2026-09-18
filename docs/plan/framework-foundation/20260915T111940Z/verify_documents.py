"""Bounded documentation observations only; no product or framework acceptance."""
from __future__ import annotations

import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
DOCS = ROOT / "docs/specs/framework"
NOTES = ROOT / "docs/plan/devforgeai-adaptive-framework-enhancement-notes.md"
REPORT = RUN / "verification.md"
EXPECTED = {
    "index.md", "foundation.md", "core-workflows.md",
    "work-items-and-dependencies.md", "project-context-and-policy.md",
    "skills-and-project-expertise.md", "subagents-and-context.md",
    "guardrails-and-rust-runtime.md", "quality-and-delivery.md",
    "expert-health-and-realignment.md", "knowledge-and-continuity.md",
    "installation-and-integrations.md", "roadmap-and-decisions.md",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prose(text: str) -> str:
    return re.sub(r"^```.*?^```[^\n]*", "", text, flags=re.M | re.S)


def anchors(path: Path) -> set[str]:
    content = prose(path.read_text(encoding="utf-8-sig"))
    result = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', content))
    seen: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", content, flags=re.M):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\-\s]", "", heading.lower()).strip().replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        result.add(slug if n == 0 else f"{slug}-{n}")
    return result


def main() -> int:
    failures: list[str] = []
    names = {p.name for p in DOCS.glob("*.md")}
    if names != EXPECTED:
        failures.append(f"Document inventory mismatch: {sorted(names ^ EXPECTED)}")
    documents = sorted(DOCS.glob("*.md")) + [NOTES]
    ids = []
    for path in documents:
        content = path.read_text(encoding="utf-8-sig")
        match = re.match(r"---\r?\n(.*?)\r?\n---", content, flags=re.S)
        if not match:
            failures.append(f"Missing frontmatter: {path.name}")
            continue
        identifier = re.search(r"^id: (.+)$", match[1], flags=re.M)
        if not identifier:
            failures.append(f"Missing id: {path.name}")
        else:
            ids.append(identifier[1].strip())
        if path.parent == DOCS and "implementation_readiness: not-ready" not in match[1]:
            failures.append(f"Unexpected readiness claim: {path.name}")
    if len(ids) != len(set(ids)):
        failures.append("Duplicate document IDs")

    local_links = 0
    linked_documents = documents + [p for p in (REPORT, RUN / "review.md") if p.exists()]
    for path in linked_documents:
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose(path.read_text(encoding="utf-8-sig"))):
            target = urlsplit(raw)
            if target.scheme or raw.startswith("//"):
                continue
            local_links += 1
            linked = (path.parent / unquote(target.path)).resolve() if target.path else path
            # This same command materializes its own report after computing observations.
            if linked == REPORT and not target.fragment:
                continue
            if not linked.exists():
                failures.append(f"Missing link: {path.name} -> {raw}")
            elif target.fragment and linked.suffix == ".md" and unquote(target.fragment) not in anchors(linked):
                failures.append(f"Missing anchor: {path.name} -> {raw}")

    preserved = []
    for entry in json.loads((RUN / "inputs-before.json").read_text(encoding="utf-8")):
        path = Path(entry["Path"])
        after = digest(path)
        matches = after == entry["Hash"].lower()
        preserved.append({"path": str(path), "before": entry["Hash"].lower(), "after": after, "unchanged": matches})
        if not matches:
            failures.append(f"Selected input changed: {path}")

    schema_path = DOCS / "references/codex-config-schema-20260915.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    counts = {"root_properties": len(schema["properties"]), "definitions": len(schema["definitions"])}
    if counts != {"root_properties": 98, "definitions": 171}:
        failures.append(f"Unexpected schema inventory: {counts}")
    if "description" not in schema["definitions"]["AgentRoleToml"]["properties"]:
        failures.append("Schema extraction lost the native description field")

    delivered = documents + [schema_path]
    manifest = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in delivered]
    (RUN / "document-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    outcome = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "documentation structure, links, selected input preservation and schema facts only",
        "command": "python -B -X utf8 docs/plan/framework-foundation/20260915T111940Z/verify_documents.py",
        "cwd": str(ROOT), "python": platform.python_version(),
        "document_count": len(documents), "local_links_checked": local_links,
        "schema_inventory": counts, "inputs": preserved, "failures": failures,
        "exit_code": 1 if failures else 0,
        "product_tests": "NOT_RUN: documentation-only delivery",
        "framework_acceptance": "NOT_EVALUATED",
    }
    (RUN / "verification.json").write_text(json.dumps(outcome, indent=2) + "\n", encoding="utf-8")
    lines = ["# Framework documentation verification", "",
             f"Observed: {outcome['observed_at_utc']}", "",
             f"Documentation checks: {'FAIL' if failures else 'PASS'}; {len(documents)} Markdown documents, {local_links} local links, {len(preserved)} selected pre-existing inputs checked for unchanged hashes.", "",
             "Command: `" + outcome["command"] + "`", "",
             f"Working directory: `{ROOT}`. Python {platform.python_version()}. Exit code: {outcome['exit_code']}.", "",
             "[Detailed observations](verification.json) · [Delivered document identities](document-manifest.json) · [Input identities before authoring](inputs-before.json) · [Adversarial review](review.md)", "",
             "The structural schema contains 98 root properties and 171 definitions; these are live upstream facts, not proof of per-agent applicability in the installed CLI.", "",
             "Manual factual and cross-document review is recorded separately. This checker does not prove semantic completeness, operational support, product TDD, coverage or protected acceptance. No product tests were run; framework acceptance NOT_EVALUATED."]
    if failures:
        lines += ["", "Observed failures:", ""] + ["- " + f for f in failures]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: outcome[k] for k in ("document_count", "local_links_checked", "schema_inventory", "failures", "exit_code")}))
    return outcome["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
