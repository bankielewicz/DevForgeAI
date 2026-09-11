#!/usr/bin/env python3
"""Verify every sha256 recorded in the authoring file-manifest.json."""
import hashlib, json, subprocess, sys
from collections import Counter
from pathlib import Path

WT = Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910")
SKILL = WT / "providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert"
AUTH = WT / "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring"

def sha_file(p):
    p = Path(p)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def sha_git(rev, rel):
    r = subprocess.run(["git", "-C", str(WT), "show", f"{rev}:{rel}"], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None

man = json.loads((AUTH / "file-manifest.json").read_text(encoding="utf-8"))
base = man["base_commit"]
rows = []

def add(group, label, declared, actual, note):
    rows.append({"group": group, "label": label, "declared": declared, "actual": actual,
                 "status": "MATCH" if declared == actual else ("TARGET_UNRESOLVED" if actual is None else "MISMATCH"),
                 "note": note})

for rel, s in man["runtime_files_sha256"].items():
    add("manifest:runtime", rel, s, sha_file(SKILL / rel), "current bytes under the skill root")
for rel, s in man["authored_eval_files_sha256"].items():
    add("manifest:authored_eval", rel, s, sha_file(SKILL / rel), "current bytes under the skill root")
for rel, s in man["authoring_records_sha256"].items():
    add("manifest:authoring_records", rel, s, sha_file(AUTH / rel), "current bytes under the authoring dir")
for rel, s in man["governing_inputs_sha256"].items():
    a = sha_git(base, rel)
    note = f"repo at base_commit {base[:7]}"
    if a != s:
        a2 = sha_file(WT / rel)
        if a2 == s:
            a, note = a2, "current working tree (base_commit bytes differ)"
    add("manifest:governing_inputs", rel, s, a, note)

# any remaining 64-hex strings anywhere else in the manifest
def hexes(o, p=""):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            out += hexes(v, p + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += hexes(v, p + f"[{i}]")
    elif isinstance(o, str):
        import re
        for m in re.findall(r"\b[0-9a-f]{64}\b", o):
            out.append((p, m))
    return out
covered = set(man["runtime_files_sha256"].values()) | set(man["authored_eval_files_sha256"].values()) \
        | set(man["authoring_records_sha256"].values()) | set(man["governing_inputs_sha256"].values())
extra = [(p, h) for p, h in hexes(man) if h not in covered]

Path(sys.argv[1]).write_text(json.dumps({"rows": rows, "prose_digests": extra}, indent=2) + "\n", encoding="utf-8")

for g in sorted({r["group"] for r in rows}):
    c = Counter(r["status"] for r in rows if r["group"] == g)
    print(f"{g:30s} total={sum(c.values()):3d}  " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))
print(f"ALL manifest table digests: total={len(rows)}  " +
      "  ".join(f"{k}={v}" for k, v in sorted(Counter(r['status'] for r in rows).items())))
for r in rows:
    if r["status"] != "MATCH":
        print(f"  !! {r['status']} [{r['group']}] {r['label']}\n     declared={r['declared']}\n     actual  ={r['actual']} ({r['note']})")
print()
print("digests appearing only in manifest prose (not table entries):")
for p, h in extra:
    print(f"  {p} -> {h}")
print()
print("counts declared:", man["counts"])
print("actual runtime entries:", len(man["runtime_files_sha256"]),
      "authored_eval entries:", len(man["authored_eval_files_sha256"]))
