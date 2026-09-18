"""Capture selected RCA source bytes; this is evidence collection, not validation."""
import hashlib
import json
import os
import platform
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\DevForgeAI")
OUT = Path(__file__).parent
V = "docs/plan/skill-validations/qa/20260914T1949120508210Z/"
A = "docs/plan/skill-authorings/qa/20260914T193851Z/"
R = "docs/plan/skill-authorings/qa/20260914T2000129113921Z-readback/"
PATHS = [
    "AGENTS.md", "docs/specs/qa-skill-spec.md", "docs/specs/qa-skill-postmvp-spec.md",
    "docs/plan/devforgeai-codex-rust-enforcement-design.md", "devforgeai/Cargo.toml",
    "devforgeai/README.md", "devforgeai/src/lib.rs",
    A + "authoring-record.json", A + "validation-request.json", A + "DELIVERY.md",
    R + "readback.py", R + "readback.json",
    V + "validation-report.md", V + "native-observations.json", V + "command-log.md",
    V + "handoff.json", V + "findings.json", V + "evaluation/results-001.jsonl",
    ".agents/skills/skill-builder/SKILL.md", ".agents/skills/skill-validator/SKILL.md",
    ".agents/skills/skill-validator/references/trials.md",
    ".agents/skills/skill-validator/references/reporting.md",
]
for case in ("QPV-01", "QPV-02", "QPV-06"):
    PATHS.extend(V + f"trials/{case}/attempt-002{suffix}" for suffix in
                 (".json", ".stdout.jsonl", ".stderr.txt"))
for base in ("src/agents/skills/dev/", ".agents/skills/dev/"):
    PATHS.extend(base + name for name in (
        "SKILL.md", "references/context.md", "references/implementation.md",
        "references/failure-delivery.md", "references/evidence-resume.md",
        "assets/delivery.md", "assets/traceability.md", "assets/checkpoint.md"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    for component in (path, *path.parents):
        info = component.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Link/reparse point rejected: {component}")
    before = path.stat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > 32 * 1024 * 1024:
        raise ValueError(f"Unbounded/nonregular input: {path}")
    data = path.read_bytes()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError(f"Input changed during read: {path}")
    return data


def main():
    if len(PATHS) != len(set(PATHS)) or len(PATHS) > 2000:
        raise ValueError("Invalid selected inventory")
    rows = []
    total = 0
    for index, relative in enumerate(PATHS, 1):
        source = ROOT / relative
        data = read(source)
        total += len(data)
        if total > 32 * 1024 * 1024:
            raise ValueError("Capture ceiling exceeded")
        target = OUT / "inputs" / f"{index:02}-{source.name}"
        target.parent.mkdir(exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        if read(target) != data or read(source) != data:
            raise ValueError(f"Capture drift: {source}")
        rows.append({"source": str(source), "snapshot": target.relative_to(OUT).as_posix(),
                     "bytes": len(data), "sha256": digest(data)})
    result = {"record_kind": "rca_source_capture", "recorded_utc": datetime.now(timezone.utc).isoformat(),
              "cwd": os.getcwd(), "python": sys.version, "host": platform.platform(),
              "scope": "Explicit RCA source list; no repository-wide or runtime validation claim",
              "omissions": [], "files": rows, "total_bytes": total,
              "command": "python -B -X utf8 docs/plan/root-cause-analyses/qa-completion/20260914T2024442802835Z/capture.py"}
    payload = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    target = OUT / "source-manifest.json"
    with target.open("xb") as stream:
        stream.write(payload)
    if read(target) != payload:
        raise ValueError("Manifest readback mismatch")
    print(json.dumps({"files": len(rows), "bytes": total, "manifest": str(target),
                      "sha256": digest(payload)}, indent=2))


if __name__ == "__main__":
    main()
