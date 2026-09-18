"""Compare coverage segment execution without assigning causality or merging profiles."""
import json
from pathlib import Path
from intake import RUN, DEV, PKG, binding


def protocol(path):
    data = json.loads(path.read_text())
    return next(row for unit in data["data"] for row in unit["files"]
                if Path(row["filename"]).name == "protocol.rs")


def main():
    old_path = DEV / "final-coverage.json"
    new_path = RUN / "coverage.json"
    old, new = protocol(old_path), protocol(new_path)
    a = {(r[0], r[1]): r for r in old["segments"]}
    b = {(r[0], r[1]): r for r in new["segments"]}
    assert set(a) == set(b), "Segment layout changed"
    source = (PKG / "src/protocol.rs").read_text().splitlines()
    changes = []
    for key in sorted(a):
        if a[key][3] and b[key][3] and bool(a[key][2]) != bool(b[key][2]):
            changes.append({"line": key[0], "column": key[1], "developer": a[key], "qa": b[key],
                            "source_line": source[key[0]-1]})
    value = {"developer": binding(old_path), "qa": binding(new_path),
             "protocol_developer": old["summary"]["lines"], "protocol_qa": new["summary"]["lines"],
             "execution_presence_changes": changes,
             "interpretation": "Observed segment execution differences only; no causal claim or coverage retry."}
    with (RUN / "coverage-comparison.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")
    print(json.dumps(value, indent=2))


if __name__ == "__main__":
    main()
