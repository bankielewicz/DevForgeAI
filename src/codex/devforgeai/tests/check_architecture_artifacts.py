"""Schema-check retained Architecture trial artifacts, separately from source scores."""
import argparse
import hashlib
import json
from pathlib import Path
import make_architecture_evals as fixtures

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--stage", default="matrix", choices=["smoke", "matrix", "supplemental"])
    args = parser.parse_args()
    fixtures.SCHEMAS = Path(__file__).resolve().parents[4] / "src/schemas"
    rows = []
    for result in sorted((args.evidence / args.stage).glob("*/result.json")):
        trial = result.parent
        before = json.loads((trial / "before.json").read_text())
        workspace = trial / "workspace"
        for kind in ["arch", "adr"]:
            for path in sorted((workspace / "docs/specs" / kind).glob("*.md")):
                relative = path.relative_to(workspace).as_posix()
                sha = hashlib.sha256(path.read_bytes()).hexdigest()
                row = {"trial": trial.name, "path": relative, "sha256": sha,
                       "authored_or_modified": before.get(relative) != sha}
                try:
                    fixtures.validate(str(path), path.read_text(), kind + ".schema.json")
                    row["status"] = "PASS"
                except Exception as exc:
                    row.update(status="FAIL", error=str(exc))
                rows.append(row)
    output = {"scope": "JSON Schema structure only; does not verify decision acceptance, readiness semantics, or actual provenance identity.",
              "stage": args.stage, "artifacts": rows,
              "authored_or_modified_count": sum(r["authored_or_modified"] for r in rows),
              "failures": sum(r["status"] == "FAIL" for r in rows)}
    (args.evidence / (args.stage + "-artifact-schema-checks.json")).write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k:v for k,v in output.items() if k != "artifacts"}, indent=2))
    raise SystemExit(1 if output["failures"] else 0)

if __name__ == "__main__":
    main()
