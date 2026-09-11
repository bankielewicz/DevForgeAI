#!/usr/bin/env python3
"""Compare prior-17 assertion rows between the frozen e641797 run and the f8a5741 run."""
import json, sys
from pathlib import Path

def load(p):
    cases = {}
    for line in Path(p).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("record") != "case":
            continue
        cases[rec["case_id"]] = rec
    return cases

def rows(rec):
    out = {}
    for a in rec.get("assertions", []):
        out[a.get("assertion_id")] = {
            "grader": a.get("grader"), "result": a.get("result"),
            "observed": a.get("observed"), "reason": a.get("reason"),
            "evidence": a.get("evidence"),
        }
    return out

old_p, new_p, label = sys.argv[1], sys.argv[2], sys.argv[3]
old, new = load(old_p), load(new_p)
print(f"--- {label}: frozen={len(old)} cases, current={len(new)} cases")
added = [c for c in new if c not in old]
removed = [c for c in old if c not in new]
print(f"    added case_ids   : {sorted(added)}")
print(f"    removed case_ids : {sorted(removed)}")
drift = 0
for cid in old:
    if cid not in new:
        continue
    o, n = old[cid], new[cid]
    if o.get("execution_status") != n.get("execution_status"):
        drift += 1
        print(f"    DRIFT {cid}: execution_status {o.get('execution_status')} -> {n.get('execution_status')}")
    ro, rn = rows(o), rows(n)
    if set(ro) != set(rn):
        drift += 1
        print(f"    DRIFT {cid}: assertion ids {sorted(ro)} -> {sorted(rn)}")
        continue
    for aid in ro:
        if ro[aid] != rn[aid]:
            drift += 1
            print(f"    DRIFT {cid}/{aid}:")
            print(f"        frozen : {json.dumps(ro[aid], ensure_ascii=False)}")
            print(f"        current: {json.dumps(rn[aid], ensure_ascii=False)}")
    if o.get("metrics", {}).get("files_read") != n.get("metrics", {}).get("files_read") or \
       o.get("metrics", {}).get("bytes_read") != n.get("metrics", {}).get("bytes_read"):
        print(f"    note {cid}: metrics files/bytes {o.get('metrics')} -> {n.get('metrics')}")
print(f"    prior-case assertion drift rows: {drift}")
print()
print(f"--- {label}: NEW case rows")
for cid in sorted(added):
    n = new[cid]
    print(f"    {cid} tier={n.get('tier')} execution_status={n.get('execution_status')}")
    for a in n.get("assertions", []):
        print(f"        {a.get('assertion_id')} [{a.get('grader')}] {a.get('result')} observed={a.get('observed')!r}")
        print(f"            reason={a.get('reason')}")
print()
