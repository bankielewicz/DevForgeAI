"""Read/verify authored package and publish its byte manifest; no native invocation."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[4]
package = root / "src/agents/skills/advisor"
required = ["SKILL.md", "agents/openai.yaml", "assets/briefing-template.md", "assets/request.schema.json",
            "references/briefing-rules.md", "references/response-format.md", "references/execution.md",
            "references/evaluation.md", "scripts/advisor_run.py", "evals/run_evaluation.py",
            "evals/cases.jsonl", "evals/case.schema.json", "tests/test_advisor.py", "tests/test_extended.py"]
missing = [name for name in required if not (package / name).is_file()]
if missing:
    raise SystemExit("Missing required artifacts: " + repr(missing))
files = sorted(p for p in package.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "artifact-manifest.json")
links = 0
for path in files:
    if path.suffix == ".py":
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    if path.suffix == ".json":
        json.loads(path.read_text(encoding="utf-8"))
    if path.suffix == ".md":
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if not target.startswith(("https://", "http://", "#")):
                assert (path.parent / target.split("#")[0]).is_file(), (path, target)
                links += 1
sources = {
    "C:/Users/bryan/.codex/prompts/advisor.md": "2bb2e9b5c0d226c4778bc61dc8cd39e2a87aa04611538f541dd4d4cee7719aba",
    "C:/Users/bryan/.codex/advisor/contract.md": "af4cd7f0505c92a186c29edc17328107ac2103f6069109c5aacac04da32b18ab",
}
for path, expected in sources.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, "Source changed: " + path
manifest = {"schema": "advisor-artifact-manifest-v1", "files": {
    p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
    "external_contract": {"path": "C:/Users/bryan/.codex/advisor/contract.md", "sha256": sources["C:/Users/bryan/.codex/advisor/contract.md"]},
    "runtime": "Python >=3.10 standard library; native authenticated Claude CLI", "framework_acceptance": "NOT_EVALUATED"}
manifest_path = package / "artifact-manifest.json"
if "--publish" in sys.argv:
    with manifest_path.open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2, ensure_ascii=True)
        stream.write("\n")
else:
    assert json.loads(manifest_path.read_text(encoding="utf-8")) == manifest, "Manifest does not match package bytes"
print(json.dumps({"files": len(files), "local_links_checked": links, "python_syntax": "PASS", "json_syntax": "PASS", "original_sources_unchanged": True,
                  "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}))
