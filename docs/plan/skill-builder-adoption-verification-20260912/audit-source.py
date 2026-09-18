"""Retain source-only change receipts and verify the final package manifest."""
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
evidence = Path(__file__).resolve().parent
suffix = "-release" if "--release" in sys.argv else ""
package = evidence.parents[2] / "src/agents/skills/skill-builder"
before = evidence / "builder-before"
def sha(data):
    return hashlib.sha256(data).hexdigest()
def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}
old, new = files(before), files(package)
manifest = json.loads(new["evals/build-manifest.json"])
assert manifest["artifacts"] == {p: sha(d) for p, d in new.items() if p != "evals/build-manifest.json"}
changes, patch = [], []
for name in sorted(set(old) | set(new)):
    if old.get(name) == new.get(name):
        continue
    changes.append({"path": name, "change": "added" if name not in old else "removed" if name not in new else "modified",
                    "before_sha256": sha(old[name]) if name in old else None, "after_sha256": sha(new[name]) if name in new else None})
    patch.extend(difflib.unified_diff(old.get(name, b"").decode("utf-8").splitlines(True), new.get(name, b"").decode("utf-8").splitlines(True),
                                    fromfile="before/" + name, tofile="after/" + name))
assert not any(r["change"] == "removed" for r in changes)
assert all(old[p] == new[p] for p in old if p.startswith("evals/fixtures/") or p.startswith("tests/test_") or p == "tests/fixture_data.py")
(evidence / ("development-source" + suffix + ".diff")).write_text("".join(patch), encoding="utf-8")
receipt = {"builder_manifest_sha256": sha(new["evals/build-manifest.json"]), "package_files": len(new),
           "changes": changes, "legacy_fixture_and_test_bytes_preserved": True, "removed_files": [],
           "operational_writes_performed": False, "installation_performed": False}
(evidence / ("source-change-receipt" + suffix + ".json")).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
shutil.copytree(package, evidence / ("builder-final" + suffix))
print(json.dumps({"manifest": receipt["builder_manifest_sha256"], "package_files": len(new),
                  "modified": sum(r["change"] == "modified" for r in changes), "added": sum(r["change"] == "added" for r in changes),
                  "legacy_fixture_and_test_bytes_preserved": True}))
