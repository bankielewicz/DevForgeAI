"""Reduce retained raw observations without issuing protected acceptance."""
from decimal import Decimal, getcontext
import json
import re
from pathlib import Path
import sys
from intake import RUN, PKG, DEV, MANIFEST, ROOT, binding

getcontext().prec = 40


def write(name, value):
    with (RUN / name).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def outcomes(attempt):
    directory = RUN / "attempts" / attempt
    receipt = json.loads((directory / "receipt.json").read_text())
    text = (directory / "stdout.bin").read_text()
    rows = re.findall(r"^test (\S+) \.\.\. (ok|FAILED|ignored)\s*$", text, re.M)
    if len(rows) != len(set(n for n, _ in rows)):
        raise RuntimeError("Repeated logical case in " + attempt)
    return receipt, dict(rows)


def main():
    original, original_rows = outcomes("12-original-all-targets")
    independent, independent_rows = outcomes("07-independent-cases")
    expected = json.loads((RUN / "case-inventory.json").read_text())
    normal_inventory = set(re.findall(r"^(\S+): test\s*$", (RUN / "attempts/02-original-inventory/stdout.bin").read_text(), re.M))
    inherited = {r["name"] for r in expected if r["provenance"] == "inherited"}
    assert normal_inventory == inherited == set(original_rows)
    new = {r["name"] for r in expected if r["provenance"] == "independent"}
    independent_by_name = {n.split("::")[-1]: outcome for n, outcome in independent_rows.items()}
    assert set(independent_by_name) == new
    for case in expected:
        table = original_rows if case["provenance"] == "inherited" else independent_by_name
        case["status"] = {"ok":"PASS", "FAILED":"FAIL", "ignored":"NOT_RUN"}[table[case["name"]]]
        case["attempt"] = "12-original-all-targets" if case["provenance"] == "inherited" else "07-independent-cases"
    counts = {}
    for label, rows in [("unit", [c for c in expected if c["category"] == "unit"]),
                        ("integration", [c for c in expected if c["category"] == "integration"]),
                        ("overall", expected)]:
        passed = sum(c["status"] == "PASS" for c in rows)
        counts[label] = {"passed": passed, "required": len(rows), "percentage": str(Decimal(passed)*100/len(rows)),
                         "floor_met": passed*100 >= len(rows)*95}
    if sys.argv[1] == "tests":
        write("case-results.json",expected)
        write("test-analysis.json",{"counts":counts,"receipts":[binding(RUN / "attempts" / a / "receipt.json") for a in ("07-independent-cases","12-original-all-targets")],
                                    "setup_error_attempt":"05-harness-inventory: no tests ran", "duplicate_credit":False})
        print(json.dumps(counts,indent=2))
        return
    coverage_receipt, coverage_rows = outcomes("13-original-coverage")
    assert set(coverage_rows) == inherited
    assert coverage_receipt["exit_code"] == 0 and not coverage_receipt["timeout"]
    assert all(x == "ok" for x in coverage_rows.values())
    raw = json.loads((RUN / "coverage.json").read_text())
    files = {}
    wanted = {str(p.resolve()).casefold(): p for p in (PKG / "src").glob("*.rs")}
    for data in raw["data"]:
        for row in data["files"]:
            path = str(Path(row["filename"]).resolve()).casefold()
            if path in wanted:
                assert path not in files, "duplicate runtime coverage file"
                files[path] = {"path": str(wanted[path]), **row["summary"]["lines"], "source":binding(wanted[path])}
    # lib.rs consists solely of module declarations; LLVM may omit this zero-line file.
    lib_key = str((PKG / "src/lib.rs").resolve()).casefold()
    if lib_key not in files:
        lines = (PKG / "src/lib.rs").read_text().splitlines()
        assert all(not s.strip() or s.startswith("//") or re.fullmatch(r"pub mod \w+;", s) for s in lines)
        files[lib_key] = {"path": str(PKG / "src/lib.rs"), "covered":0,"count":0,"percent":0,
                          "source":binding(PKG / "src/lib.rs"),"reason":"Only module declarations; no executable code"}
    assert set(files) == set(wanted), "Incomplete first-party source denominator"
    old = {str(Path(r["path"]).resolve()).casefold(): r for r in json.loads((DEV/"final-coverage-analysis.json").read_text())["files"]}
    for key,row in files.items():
        row["developer_covered"] = old[key]["covered"]
        row["developer_count"] = old[key]["count"]
        row["covered_delta"] = row["covered"]-old[key]["covered"]
        row["count_delta"] = row["count"]-old[key]["count"]
    covered = sum(r["covered"] for r in files.values())
    count = sum(r["count"] for r in files.values())
    analysis = {"files":list(files.values()),"covered":covered,"count":count,
        "percentage":str(Decimal(covered)*100/count),"floor_met":covered*100>=count*95,
        "first_party_exclusions":[],"source_count":len(wanted),"coverage_contributors":133,
        "independent_harness_profiles_merged":False,"branch_coverage":"NOT_RUN",
        "branch_reason":"cargo llvm-cov 0.8.4 --branch requires nightly; installed toolchains are stable 1.97.1 and 1.93 only; no installation selected",
        "raw":binding(RUN/"coverage.json"),"receipt":binding(RUN/"attempts/13-original-coverage/receipt.json"),
        "tests":counts,"instrumented_test_passes":len(coverage_rows)}
    write("coverage-analysis.json",analysis)
    print(json.dumps({k:v for k,v in analysis.items() if k != "files"},indent=2))


if __name__=="__main__":
    main()
