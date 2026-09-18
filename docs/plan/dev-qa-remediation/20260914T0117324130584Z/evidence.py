"""Retain command attempts and bounded source snapshots for this remediation only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
def sha(data):
    return hashlib.sha256(data).hexdigest()
def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
def snapshot(source, out):
    rows = []
    total = 0
    pending = [source]
    while pending:
        for p in sorted(pending.pop().iterdir()):
            if p.is_symlink() or p.lstat().st_file_attributes & 0x400:
                raise ValueError("link/reparse point: " + str(p))
            if p.name.lower() in {"backup", "backups", "devforgeai_cli", "__pycache__", ".git"}:
                continue
            if p.is_dir():
                pending.append(p)
            elif p.is_file():
                data = p.read_bytes()
                total += len(data)
                if total > 32*1024*1024 or len(rows) >= 2000:
                    raise ValueError("snapshot limit")
                rel = p.relative_to(source)
                dest = out / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("xb") as stream:
                    stream.write(data)
                if dest.read_bytes() != data:
                    raise ValueError("snapshot readback")
                rows.append({"path": rel.as_posix(), "bytes": len(data), "sha256": sha(data)})
            else:
                raise ValueError("special file")
    rows.sort(key=lambda r:r["path"])
    return {"root":str(source),"files":rows,"package_digest":sha(json.dumps(rows,ensure_ascii=False,separators=(",",":")).encode())}
def execute(label, argv, timeout=120, env=None):
    dest = ROOT / "commands" / label
    dest.mkdir(parents=True, exist_ok=False)
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.monotonic()
    state = "EXITED"
    with (dest/"stdout.txt").open("xb") as stdout, (dest/"stderr.txt").open("xb") as stderr:
        try:
            cp = subprocess.run(argv, cwd=PROJECT, stdout=stdout, stderr=stderr,
                                timeout=timeout, env=env)
            code=cp.returncode
        except subprocess.TimeoutExpired:
            code=None
            state="TIMEOUT"
    receipt={"argv":argv,"cwd":str(PROJECT),"start":start,"end":datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "elapsed":time.monotonic()-tick,"timeout":timeout,"state":state,"exit_code":code,
             "stdout":{"path":str(dest/"stdout.txt"),"sha256":sha((dest/"stdout.txt").read_bytes())},
             "stderr":{"path":str(dest/"stderr.txt"),"sha256":sha((dest/"stderr.txt").read_bytes())}}
    save(dest/"receipt.json",receipt)
    print(json.dumps(receipt))
    print((dest/"stdout.txt").read_text(encoding="utf-8",errors="replace")[-16000:])
    print((dest/"stderr.txt").read_text(encoding="utf-8",errors="replace")[-16000:])
    return code
if __name__=="__main__":
    if sys.argv[1]=="capture":
        for name in ("skill-builder","skill-validator","dev"):
            save(ROOT/"before"/(name+"-manifest.json"),snapshot(PROJECT/"src/agents/skills"/name,ROOT/"before"/name))
        save(ROOT/"scope.json",{"authorization":"User: Implement the plan; permanent fixes for both causes.",
             "plan":str(PROJECT/"docs/plan/dev-qa-remediation-plan.md"),
             "coverage_denominator":["src/agents/skills/skill-builder/scripts/authoring.py"],
             "coverage_exclusions":[],"coverage_floor":95,"pass_rate_floor":95,
             "interpretation":"Supporting custody helper executed lines; not framework Rust qualification.",
             "platform":sys.platform,"python":sys.version,"executable":sys.executable})
    else:
        sys.exit(execute(sys.argv[1],sys.argv[2:]) or 0)
