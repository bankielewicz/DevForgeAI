"""Read back artifact placement and bytes; no product acceptance authority."""
import datetime
import json
from pathlib import Path
import re
from record import ROOT, PROJECT, digest, manifest, write

selected = r"C:\Projects\DevForgeAI\docs\plan\index-service-remediation\20260914T1950304158791Z"
assert str(ROOT) == selected
assert selected in (ROOT / "context.md").read_text(encoding="utf-8")
assert manifest() == json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
preservation = json.loads((ROOT / "preservation.json").read_text())
for row in preservation["verified_inputs_and_original_QA_artifacts"]:
    assert digest(Path(row["path"])) == row["expected"], row["path"]
source = json.loads((ROOT / "source-manifest.json").read_text())
for row in source["files"]:
    retained = ROOT / "candidate" / Path(row["path"]).relative_to(PROJECT)
    assert digest(retained) == row["sha256"]
for row in json.loads((ROOT / "runtime-artifacts.json").read_text())["binaries"]:
    assert digest(Path(row["source"])) == digest(Path(row["retained"])) == row["sha256"]

profile_count = 0
for attempt in ["coverage-final", "coverage-final-002"]:
    for row in json.loads((ROOT / "attempts" / attempt / "profile-manifest.json").read_text()):
        assert digest(Path(row["retained"])) == row["sha256"]
        profile_count += 1
extension = ROOT / "platform-extension-001"
expected_native = json.loads((extension / "expected.json").read_text())["files"]
for host in ["linux","wsl"]:
    native = extension / host
    assert json.loads((native / "source.json").read_text()) == expected_native
    for row in json.loads((native / "profile-manifest.json").read_text()):
        relative = row["retained"].split("/evidence/",1)[1]
        retained = native / relative
        assert digest(retained) == row["sha256"]
        profile_count += 1
    for directory in (native / "attempts").iterdir():
        receipt = json.loads((directory / "receipt.json").read_text())
        assert digest(directory / "source.json") == receipt["source_sha256"]
        for name in ["stdout.txt","stderr.txt"]:
            assert digest(directory / name) == receipt[name + "_sha256"]

def entry(path, root):
    relative = path.relative_to(root)
    required = root / relative
    actual = path.resolve()
    assert actual == required.resolve()
    actual.relative_to(ROOT)
    return {"name":relative.as_posix(),"required_path":str(required),"actual_path":str(actual),"bytes":actual.stat().st_size,"sha256":digest(actual)}

extension_artifacts = [entry(p,extension) for p in sorted(extension.rglob("*")) if p.is_file() and p.name != "extension-manifest.json"]
write(extension / "extension-manifest.json", {"root":str(extension),"candidate_manifest_sha256":digest(ROOT / "source-manifest.json"),"artifacts":extension_artifacts})

promised = ["context.md","inputs.json","initial-source-manifest.json","source-manifest.json","changed-files.json","runtime-artifacts.json","candidate.diff","metrics.json","test-inventory.json","tools.json","preservation.json","executions.jsonl","delivery.md","checkpoint.md","final-delivery.md","final-checkpoint.md","platform-extension-001/extension-report.md","platform-extension-001/extension-manifest.json"]
assert all((ROOT / name).is_file() for name in promised)
paths = [p for p in ROOT.iterdir() if p.is_file() and p.name not in ("handoff-manifest.json","verification.json")]
for directory in ["attempts","candidate","runtime","platform-extension-001"]:
    paths.extend(p for p in (ROOT / directory).rglob("*") if p.is_file())
artifacts = [entry(p,ROOT) for p in sorted(set(paths))]
write(ROOT / "handoff-manifest.json", {"selected_evidence_value":selected,"resolved_evidence_root":str(ROOT),"selection_source":"context.md pre-write distinct run selection and user-requested platform extension", "candidate_manifest_sha256":digest(ROOT / "source-manifest.json"),"build_manifest_sha256":digest(ROOT / "runtime-artifacts.json"),"current_delivery":"final-delivery.md","current_checkpoint":"final-checkpoint.md","artifacts":artifacts})
readback = []
for row in json.loads((ROOT / "handoff-manifest.json").read_text())["artifacts"]:
    path = Path(row["actual_path"])
    matches = str(path) == row["required_path"] and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"]
    assert matches, str(path)
    readback.append({"name":row["name"],"required_path":row["required_path"],"observed_path":str(path),"bytes_and_digest_match":matches})
links = []
for name in ["delivery.md","final-delivery.md","checkpoint.md","final-checkpoint.md","platform-extension-001/extension-report.md"]:
    path = ROOT / name
    content = path.read_text(encoding="utf-8")
    assert content
    prose = re.sub(r"```[^\n]*\n.*?```", "", content, flags=re.S)
    prose = re.sub(r"`[^`]*`", "", prose)
    for target in re.findall(r"\]\(([^)]+)\)",prose):
        if "://" not in target:
            linked = (path.parent / target).resolve()
            # verification.json is written immediately below after all other readback.
            exists = linked.exists() or linked == ROOT / "verification.json"
            assert exists, (name,target)
            links.append({"document":name,"target":target,"present_or_current_verification":exists})
write(ROOT / "verification.json", {"recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"original_selected_root":selected,"observed_root":str(ROOT),"handoff_manifest_sha256":digest(ROOT / "handoff-manifest.json"),"candidate_manifest_sha256":digest(ROOT / "source-manifest.json"),"original_input_entries_rehashed":len(preservation["verified_inputs_and_original_QA_artifacts"]),"candidate_retained_files_verified":len(source["files"]),"retained_profiles_verified":profile_count,"artifacts":readback,"document_links":links,"scope":"artifact identity and placement only; no QA finding closure or framework acceptance"})
assert json.loads((ROOT / "verification.json").read_text())["handoff_manifest_sha256"] == digest(ROOT / "handoff-manifest.json")
print(json.dumps({"artifacts_verified":len(artifacts),"profiles_verified":profile_count,"source_manifest_sha256":digest(ROOT / "source-manifest.json"),"handoff_manifest_sha256":digest(ROOT / "handoff-manifest.json"),"verification_sha256":digest(ROOT / "verification.json")},indent=2))
