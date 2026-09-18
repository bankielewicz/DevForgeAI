"""Capture development command evidence; never makes product acceptance decisions."""
import argparse
import hashlib
import json
import pathlib
import platform
import subprocess
import datetime

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("attempt")
    parser.add_argument("stage")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    destination = ROOT / "attempts" / args.attempt
    destination.mkdir(parents=True, exist_ok=False)
    source = PROJECT / "devforgeai"
    manifest = [{"path": str(p.relative_to(PROJECT)), "sha256": sha(p)}
                for p in sorted(source.rglob("*")) if p.is_file()
                and "target" not in p.relative_to(source).parts]
    (destination / "candidate.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    started = now()
    exit_code = None
    outcome = "unknown"
    with (destination / "stdout.txt").open("wb") as out, (destination / "stderr.txt").open("wb") as err:
        try:
            process = subprocess.Popen(command, cwd=source, stdout=out, stderr=err)
            try:
                exit_code = process.wait(timeout=args.timeout)
                outcome = "observed-exit"
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                outcome = "timeout-recorder-child-terminated"
        except OSError as error:
            err.write(str(error).encode("utf-8"))
            outcome = "launch-error"
    receipt = {"attempt_id": args.attempt, "stage": args.stage,
               "command": command, "working_directory": str(source),
               "platform": platform.platform(), "architecture": platform.machine(),
               "started_at": started, "ended_at": now(), "timeout_seconds": args.timeout,
               "exit_code": exit_code, "outcome": outcome,
               "candidate": {"path": str(destination / "candidate.json"),
                             "sha256": sha(destination / "candidate.json")},
               "streams": {name: {"path": str(destination / name), "sha256": sha(destination / name)}
                           for name in ["stdout.txt", "stderr.txt"]}}
    with (ROOT / "executions.jsonl").open("a", encoding="utf-8") as output:
        output.write(json.dumps(receipt) + "\n")
    print(json.dumps(receipt))
    for name in ["stdout.txt", "stderr.txt"]:
        print((destination / name).read_text(encoding="utf-8", errors="replace")[-16000:])
    raise SystemExit(exit_code if exit_code is not None else 124)

if __name__ == "__main__":
    main()
