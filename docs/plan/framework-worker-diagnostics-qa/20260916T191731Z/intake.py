"""Bind the selected immutable inputs; no product execution or acceptance authority."""
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = Path(r"C:\Projects\DevForgeAI")
PKG = ROOT / "devforgeai/experiments/codex-worker-probe"
DEV = ROOT / "docs/plan/framework-worker-diagnostics/20260916T181820Z-dev"
MANIFEST = DEV / "candidate-v2-manifest.json"


def binding(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def save(name, value):
    path = RUN / name
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def main():
    assert binding(MANIFEST)["sha256"] == "419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540"
    manifest = json.loads(MANIFEST.read_text())
    checks = []
    for entry in manifest:
        for family, base in [("original", PKG), ("snapshot", DEV / "candidate-v2-snapshot")]:
            actual = binding(base / entry["path"])
            checks.append({"family": family, "relative": entry["path"], **actual,
                           "matches": all(actual[key] == entry[key] for key in ("bytes", "sha256"))})
    assert len(manifest) == 58 and all(c["matches"] for c in checks)
    historical = json.loads((DEV / "input-bindings.json").read_text())
    historical_checks = []
    for entry in historical:
        actual = binding(Path(entry["path"]))
        historical_checks.append({**actual, "matches": all(actual[key] == entry[key] for key in ("bytes", "sha256"))})
    selected = [ROOT / "AGENTS.md", MANIFEST, DEV / "qa-handoff.md",
                DEV / "diagnostic-contract.md", DEV / "delivery.md", DEV / "review-notes.md",
                DEV / "input-bindings.json", DEV / "baseline-manifest.json",
                DEV / "final-test-inventory.json", DEV / "final-coverage-analysis.json",
                ROOT / "docs/plan/advisor-runs/20260916T185825Z-diagnostic-handoff/qa-handoff-addendum.md",
                ROOT / "docs/plan/framework-worker-native-continuation/20260916T034357Z-source-identity/native-diagnostic-handoff.md"]
    selected += sorted((ROOT / ".agents/skills/qa").rglob("*.md"))
    selected += [ROOT / "docs/specs/framework/runtime" / name for name in (
        "codex-worker-feasibility-v1.md", "codex-worker-native-readiness-v1.md",
        "codex-worker-preflight-v1.md", "codex-worker-source-identity-v1.md")]
    save("input-bindings.json", [binding(p) for p in selected])
    save("candidate-readback-before.json", checks)
    save("historical-readback-before.json", historical_checks)
    save("source-inventory.json", [binding(p) for p in sorted((PKG / "src").glob("*.rs"))])
    save("first-party-inventory.json", [binding(PKG / e["path"]) for e in manifest])
    inherited = json.loads((DEV / "final-test-inventory.json").read_text())
    save("inherited-inventory.json", inherited)
    baseline = json.loads((DEV / "baseline-manifest.json").read_text())
    print(json.dumps({"candidate_files": len(manifest), "candidate_matches": len(checks),
                      "prior_input_count": len(historical_checks),
                      "prior_input_drift": [x for x in historical_checks if not x["matches"]],
                      "baseline_type": type(baseline).__name__, "git_present": (ROOT / ".git").exists(),
                      "run": str(RUN)}, indent=2))


if __name__ == "__main__":
    main()
