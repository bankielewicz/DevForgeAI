"""Display raw LLVM zero-count segment starts; counts remain LLVM's line metric."""
import json
from pathlib import Path
import sys

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["data"][0]
for f in data["files"]:
    path = Path(f["filename"])
    if len(sys.argv) > 2 and path.name not in sys.argv[2:]:
        continue
    print(path.name, f["summary"]["lines"])
    lines = path.read_text(encoding="utf-8").splitlines()
    points = sorted({s[0] for s in f["segments"] if s[2] == 0 and s[3] and s[4]})
    for number in points:
        print(f"{number}: {lines[number-1]}")
print("TOTAL", data["totals"]["lines"])
