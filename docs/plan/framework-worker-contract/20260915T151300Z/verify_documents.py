"""Documentation observations only; no runtime or framework acceptance authority."""
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
CONTRACT = FRAMEWORK / "runtime/codex-worker-feasibility-v1.md"
FIXTURES = FRAMEWORK / "runtime/fixtures/codex-worker-v1"
CHANGED = {
    "docs/specs/framework/index.md",
    "docs/specs/framework/runtime/architecture.md",
    "docs/specs/framework/roadmap-and-decisions.md",
    "docs/plan/framework-mvp-next-session.md",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path):
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def prose(text):
    return re.sub(r"^```.*?^```[^\n]*", "", text, flags=re.M | re.S)


def anchors(path):
    seen = {}
    result = set()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", prose(path.read_text(encoding="utf-8-sig")), re.M):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\-\s]", "", heading.lower()).strip().replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if count == 0 else f"{slug}-{count}")
    return result


def main():
    failures = []
    before = json.loads((RUN / "inputs-before.json").read_text(encoding="utf-8-sig"))
    unchanged = 0
    for entry in before:
        path = ROOT / entry["path"]
        if sha(path) == entry["sha256"]:
            unchanged += 1
        elif entry["path"] not in CHANGED:
            failures.append("Unexpected input change: " + entry["path"])
    drift = json.loads((RUN / "input-drift.json").read_text(encoding="utf-8-sig"))
    if not all(row["matches"] for row in drift):
        failures.append("Prior handoff drift")
    input_hashes = {row["path"]: row["sha256"] for row in before}
    input_hashes.update({row["path"]: row["actual_sha256"] for row in drift})
    for name in CHANGED:
        if sha(RUN / "originals" / Path(name).name) != input_hashes[name]:
            failures.append("Prior copy mismatch: " + name)

    schemas = sorted((RUN / "codex-schema").rglob("*.json"))
    for path in schemas:
        json.loads(path.read_text(encoding="utf-8-sig"))
    save(RUN / "schema-manifest.json", [record(path) for path in schemas])

    contract = CONTRACT.read_text(encoding="utf-8")
    json_blocks = re.findall(r"```json\n(.*?)\n```", contract, re.S)
    if (FIXTURES / "task.json").read_bytes() != (json_blocks[0] + "\n").encode():
        failures.append("Task fixture bytes differ from contract")
    if (FIXTURES / "expected.json").read_bytes() != (json_blocks[1] + "\n").encode():
        failures.append("Expected fixture bytes differ from contract")
    prompt_template = re.findall(r"```text\n(.*?)\n```", contract, re.S)[1]
    prompt = prompt_template.replace("<TASK_BYTES>", json_blocks[0]) + "\n"
    (FIXTURES / "prompt.txt").write_bytes(prompt.encode("utf-8"))
    for path in FIXTURES.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    offline_ids = re.findall(r"^\| (WF-\d+) \|", contract, re.M)
    if offline_ids != [f"WF-{number:02}" for number in range(1, 21)]:
        failures.append("Offline required-case inventory mismatch")
    if "**two mandatory cases**" not in contract or not all(name in contract for name in ("WN-01", "WN-02")):
        failures.append("Native required-case inventory mismatch")

    # Compare documented wire examples with the locally generated schema's keys.
    wire_fields = {
        "v2/ThreadStartParams.json": {"model", "modelProvider", "cwd", "sandbox", "approvalPolicy", "approvalsReviewer", "ephemeral"},
        "v2/TurnStartParams.json": {"threadId", "input", "model", "effort", "cwd", "approvalPolicy", "approvalsReviewer", "sandboxPolicy", "outputSchema"},
        "v2/TurnInterruptParams.json": {"threadId", "turnId"},
        "v2/GetAccountParams.json": {"refreshToken"},
        "v2/ModelListParams.json": {"cursor", "limit"},
    }
    for name, fields in wire_fields.items():
        path = RUN / "codex-schema" / name
        if not path.exists():
            failures.append("Missing selected schema: " + name)
            continue
        schema = json.loads(path.read_text(encoding="utf-8"))
        if not fields.issubset(schema.get("properties", {})):
            failures.append("Wire field drift: " + name)

    documents = sorted(FRAMEWORK.rglob("*.md")) + [
        ROOT / "docs/plan/devforgeai-adaptive-framework-enhancement-notes.md",
        ROOT / "docs/plan/framework-mvp-next-session.md",
        ROOT / "docs/plan/framework-worker-coding-handoff.md",
        RUN / "sources.md", RUN / "review.md",
    ]
    links = 0
    generated = {RUN / "verification.md", RUN / "delivery-manifest.json"}
    for path in documents:
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose(path.read_text(encoding="utf-8-sig"))):
            target = urlsplit(raw)
            if target.scheme or raw.startswith("//"):
                continue
            links += 1
            linked = (path.parent / unquote(target.path)).resolve() if target.path else path
            if linked in generated and not target.fragment:
                continue
            if not linked.exists():
                failures.append(f"Missing link: {path.relative_to(ROOT)} -> {raw}")
            elif target.fragment and linked.suffix == ".md" and unquote(target.fragment) not in anchors(linked):
                failures.append(f"Missing anchor: {path.name} -> {raw}")
    ids = []
    for path in documents:
        content = path.read_text(encoding="utf-8-sig")
        front = re.match(r"---\r?\n(.*?)\r?\n---", content, re.S)
        if front:
            match = re.search(r"^id:\s*(\S+)", front[1], re.M)
            if match:
                ids.append(match[1])
        if path == CONTRACT and "implementation_readiness: ready-for-offline-harness" not in content:
            failures.append("Contract readiness drift")
    if len(ids) != len(set(ids)):
        failures.append("Duplicate documentation IDs")
    result = {
        "observed_at": datetime.now(timezone.utc).isoformat(), "scope": "documentation observations only",
        "status": "PASS" if not failures else "FAIL", "documents": len(documents), "local_links": links,
        "schema_files": len(schemas), "unchanged_selected_inputs": unchanged,
        "matched_handoff_inputs": len(drift), "preserved_originals": len(CHANGED),
        "offline_required_cases_specified": 20, "native_required_cases_specified": 2,
        "product_tests": "NOT_RUN", "coverage": "NOT_RUN", "native_trials": "NOT_RUN",
        "framework_acceptance": "NOT_RUN", "independent_review": "NOT_RUN", "failures": failures,
        "python": platform.python_version(), "cwd": str(ROOT), "executable": sys.executable,
    }
    # Preserve every documentation-check attempt, including failed attempts.
    attempt = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    save(RUN / f"verification-{attempt}.json", result)
    save(RUN / "verification.json", result)
    verification = f"""# Worker contract documentation verification

Observed: {result['observed_at']}

Documentation checks: **{result['status']}**. {len(documents)} Markdown documents, {links} local links, {len(schemas)} generated Codex schema JSON files parsed. The selected wire field names match the installed schema. Fixture bytes match the contract, and the required inventory contains 20 offline plus two native cases.

Ten prior handoff hashes matched before editing. Four original document copies are retained byte-for-byte; {unchanged} other selected inputs are unchanged. [Input drift](input-drift.json), [before identities](inputs-before.json), [discovery receipts](discovery.json), [schema receipt](schema-command.json), [schema identities](schema-manifest.json), [source observations](sources.md), [author review](review.md), [detailed results](verification.json), [delivery identities](delivery-manifest.json).

Command: `python -B -X utf8 docs/plan/framework-worker-contract/20260915T151300Z/verify_documents.py`

Cwd: `C:\\Projects\\DevForgeAI`; executable `{sys.executable}`; Python {platform.python_version()}; exit {0 if not failures else 1}. Failed and successful check attempts are retained as timestamped JSON files.

Checks cover local links/anchors, selected byte preservation, JSON parsing, fixture/readiness/inventory consistency and selected wire property names. Author semantic review is recorded separately; no independent review was performed in this session. These observations do not establish complete schema conformance, native support, runtime behavior or protected acceptance.

Runtime tests, coverage, native Codex trials, independent product QA and framework acceptance: **NOT_RUN**. Current result is a specified nonproduction feasibility contract ready for offline implementation; native execution remains blocked on profile review and explicit trial selection. No product implementation, operational configuration change, installation or remote synchronization was performed.
"""
    (RUN / "verification.md").write_text(verification, encoding="utf-8")
    deliverables = documents + [ROOT / "AGENTS.md", RUN / "verification.md", RUN / "verify_documents.py"] + sorted(FIXTURES.iterdir())
    save(RUN / "delivery-manifest.json", [record(path) for path in sorted(set(deliverables))])
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
