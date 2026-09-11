#!/usr/bin/env python3
"""Verify every sha256 in derivation.json and the authoring file-manifest.json."""
import hashlib, json, subprocess, sys
from pathlib import Path

WT = Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910")
SKILL_REL = "providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert"
SKILL = WT / SKILL_REL
AUTH = WT / "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-evaluate-expert/authoring"

def sha_file(p: Path):
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def sha_git(rev, relpath):
    r = subprocess.run(["git", "-C", str(WT), "show", f"{rev}:{relpath}"],
                       capture_output=True)
    if r.returncode != 0:
        return None
    return hashlib.sha256(r.stdout).hexdigest()

rows = []
def check(group, label, declared, actual, note=""):
    if declared is None:
        status = "DECLARED_NULL"
    elif actual is None:
        status = "TARGET_UNRESOLVED"
    elif declared == actual:
        status = "MATCH"
    else:
        status = "MISMATCH"
    rows.append({"group": group, "label": label, "declared": declared,
                 "actual": actual, "status": status, "note": note})

d = json.loads((SKILL / "references/derivation.json").read_text(encoding="utf-8"))

# A. governing specification, pinned revision
gs = d["governing_specification"]
check("derivation:governing_specification", gs["path"], gs["sha256"],
      sha_git(gs["revision"], gs["path"]), f"rev {gs['revision'][:7]}")

# B. derivations
for i, dv in enumerate(d["derivations"]):
    dest = dv.get("destination")
    ds = dv.get("destination_sha256")
    if ds is None:
        check("derivation:destination", dest, None, None, "declared null (section reference)")
    else:
        check("derivation:destination", dest, ds, sha_file(SKILL / dest), "current bytes")
    src = dv.get("source", {})
    if src.get("sha256"):
        rev = src.get("revision", "")
        if len(rev) == 40:
            actual = sha_git(rev, src["path"])
            note = f"rev {rev[:7]}"
        else:
            actual = sha_file(WT / src["path"])
            note = f"revision literal {rev!r}; checked against this worktree"
        check("derivation:source", src["path"], src["sha256"], actual, note)
    for j, pr in enumerate(dv.get("prior_destination_sha256_chain", []) or []):
        loc = (pr.get("preserved_at") or {}).get("locator", "")
        rev = loc.split()[-1] if loc else ""
        check("derivation:prior_chain", f"{dest} @{pr.get('revision')}", pr["sha256"],
              sha_git(rev, f"{SKILL_REL}/{dest}") if rev else None, loc)

# C. new_in_this_package
for e in d["new_in_this_package"]:
    p = e.get("path")
    if e.get("sha256") is None:
        check("derivation:new", p, None, None, "declared null (directory)")
    else:
        check("derivation:new", p, e["sha256"], sha_file(SKILL / p), "current bytes")
    for pr in e.get("prior_sha256_chain", []) or []:
        loc = (pr.get("preserved_at") or {}).get("locator", "")
        rev = loc.split("commit ")[-1].split()[0] if "commit " in loc else ""
        check("derivation:prior_chain", f"{p} @{pr.get('revision')}", pr["sha256"],
              sha_git(rev, f"{SKILL_REL}/{p}") if rev else None, loc)

# D. correction_1 workspace pins
for key in ("coordinator_authorization", "task_packet"):
    node = d["correction_1"][key]
    check("derivation:correction_1", node["path"], node["sha256"], sha_file(Path(node["path"])),
          "absolute workspace path")

# E. authoring file manifest
man = json.loads((AUTH / "file-manifest.json").read_text(encoding="utf-8"))
print("file-manifest.json top-level keys:", list(man.keys()))
for k in ("revision", "schema_version", "candidate_commit", "recorded_at_utc"):
    if k in man:
        print(f"  {k}: {man[k]!r}")

def manifest_entries(obj, base=""):
    out = []
    if isinstance(obj, dict):
        if "sha256" in obj and ("path" in obj or "file" in obj):
            out.append((obj.get("path") or obj.get("file"), obj["sha256"]))
        for v in obj.values():
            out.extend(manifest_entries(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(manifest_entries(v))
    return out

entries = manifest_entries(man)
for p, s in entries:
    cands = [SKILL / p, WT / p, Path(p) if p.startswith("/") else None, AUTH / p]
    actual, used = None, None
    for c in cands:
        if c is None:
            continue
        a = sha_file(c)
        if a is not None:
            actual, used = a, str(c)
            if a == s:
                break
    check("file-manifest", p, s, actual, f"resolved {used}")

Path(sys.argv[1]).write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")

from collections import Counter
for group in sorted({r["group"] for r in rows}):
    c = Counter(r["status"] for r in rows if r["group"] == group)
    print(f"{group:34s} total={sum(c.values()):3d}  " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))
print()
print(f"ALL: total={len(rows)}  " + "  ".join(f"{k}={v}" for k, v in sorted(Counter(r['status'] for r in rows).items())))
print()
for r in rows:
    if r["status"] not in ("MATCH", "DECLARED_NULL"):
        print(f"  !! {r['status']} [{r['group']}] {r['label']}")
        print(f"     declared={r['declared']}")
        print(f"     actual  ={r['actual']}   ({r['note']})")
