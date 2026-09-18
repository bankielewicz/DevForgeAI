import hashlib
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parent
RUN = ROOT.parent
PROJECT = Path(r"C:\Projects\DevForgeAI\devforgeai")
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def normalize(rows):
    return sorted([{"path":Path(row["path"]).relative_to(PROJECT).as_posix(),"bytes":row["bytes"],"sha256":row["sha256"]} for row in rows], key=lambda row:row["path"])
manifest = json.loads((RUN / "source-manifest.json").read_text())
expected = {"windows_manifest_sha256":digest(RUN / "source-manifest.json"),"files":normalize(manifest["files"])}
(ROOT / "expected.json").write_text(json.dumps(expected,indent=2)+"\n")
old = json.loads((RUN / "initial-source-manifest.json").read_text())
(ROOT / "original-expected.json").write_text(json.dumps(normalize(old["files"]),indent=2)+"\n")
archive = ROOT / "candidate.tar.gz"
with tarfile.open(archive, "x:gz") as tar:
    for row in manifest["files"]:
        path = Path(row["path"])
        assert digest(path) == row["sha256"], str(path)
        tar.add(path, arcname="devforgeai/"+path.relative_to(PROJECT).as_posix())
    for name in ["native_runner.py", "expected.json", "original-expected.json"]:
        tar.add(ROOT / name, arcname=name)
    tar.add(PROJECT.parent / "AGENTS.md", arcname="AGENTS.md")
    tar.add(PROJECT.parent / "docs/plan/devforgeai-index-service-mvp-spec.md", arcname="selected-spec.md")
result = {"path":str(archive),"bytes":archive.stat().st_size,"sha256":digest(archive),"source_manifest_sha256":expected["windows_manifest_sha256"]}
(ROOT / "transfer-manifest.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result))
