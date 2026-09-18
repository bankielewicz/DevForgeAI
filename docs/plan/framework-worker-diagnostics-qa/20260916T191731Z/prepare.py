"""Read-only candidate audit and QA-owned inventory publication before execution."""
import difflib
import json
import re
from pathlib import Path
from intake import RUN, ROOT, PKG, DEV, MANIFEST, binding, save


def main():
    current = json.loads(MANIFEST.read_text())
    baseline = json.loads((DEV / "baseline-manifest.json").read_text())
    prior = {row["path"]: row for row in baseline}
    changes = []
    diffs = []
    syntax = []
    for row in current:
        name = row["path"]
        actual = binding(PKG / name)
        assert all(actual[k] == row[k] for k in ("bytes", "sha256"))
        old = prior.get(name)
        if old != row:
            changes.append(name)
            before = (DEV / "baseline-snapshot" / name).read_text().splitlines(True) if old else []
            after = (PKG / name).read_text().splitlines(True)
            diffs.extend(difflib.unified_diff(before, after, "baseline/"+name, "candidate/"+name))
        if name.endswith(".rs"):
            lines = (PKG / name).read_text().splitlines()
            syntax.append({"path": name, "lines": len(lines), "sha256": row["sha256"],
                "attributes": [{"line": i+1, "text": s.strip()} for i,s in enumerate(lines) if "#[" in s or "#![" in s],
                "test_names": re.findall(r"#\[test\]\s*fn\s+(\w+)", "\n".join(lines)),
                "imports": [{"line":i+1,"text":s.strip()} for i,s in enumerate(lines) if re.search(r"\b(use|extern crate|macro_rules!)\b",s)],
                "assertion_count": sum(len(re.findall(r"\bassert(?:_eq|_ne)?!",s)) for s in lines)})
    assert sum(len(row["test_names"]) for row in syntax) == 133
    save("syntax-inventory.json", syntax)
    (RUN / "independent-baseline.diff").write_text("".join(diffs), encoding="utf-8")
    save("changed-files.json", changes)
    inherited = json.loads((RUN / "inherited-inventory.json").read_text())["required_tests"]
    assert len(inherited) == len(set(inherited)) == 133
    units = [n for n in inherited if "::" in n]
    assert len(units) == 40
    cases = [{"id": "I%03d" % (i+1), "name": name, "category": "unit" if name in units else "integration",
              "provenance":"inherited", "readiness":"READY", "required":True,
              "criteria":["H1","H5","H6"], "status":"NOT_RUN"} for i,name in enumerate(inherited)]
    for p in sorted((RUN / "harness").glob("*.rs")):
        for name in re.findall(r"#\[test\]\s*fn\s+(qa_[ui]\d\d_\w+)",p.read_text()):
            cases.append({"id":name[3:6].upper().replace("U","QU").replace("I","QI"),"name":name,
                          "category":"unit" if name.startswith("qa_u") else "integration",
                          "provenance":"independent", "readiness":"READY", "required":True,
                          "criteria":["D1-D7 as mapped in test-plan.md"],"status":"NOT_RUN"})
    assert len(cases)==146 and sum(c["category"]=="unit" for c in cases)==46
    save("case-inventory.json", cases)
    save("harness-manifest-before.json",[binding(p) for p in sorted((RUN/"harness").rglob("*")) if p.is_file()])
    save("plan-binding.json",binding(RUN/"test-plan.md"))
    trials=ROOT/"docs/plan/framework-worker-trials"
    save("trials-before.json", sorted(str(p) for p in trials.iterdir()))
    save("checkpoint.json", {"intent":"run","plan_readiness":"READY","execution":"NOT_STARTED",
        "verdict":None,"candidate":binding(MANIFEST),"plan":binding(RUN/"test-plan.md"),
        "owned_processes":[],"next_safe_action":"Complete integrity review then bounded offline preparation",
        "native_codex_permitted":False})
    print(json.dumps({"changed_files":changes,"rust_files":len(syntax),"inherited_tests":133,
                      "required_total":len(cases),"required_units":46,"plan":binding(RUN/"test-plan.md")},indent=2))


if __name__=="__main__":
    main()
