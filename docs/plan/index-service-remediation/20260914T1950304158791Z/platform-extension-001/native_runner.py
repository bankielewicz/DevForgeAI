"""Native Linux/WSL evidence collection. Does not issue acceptance."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "devforgeai"
OUT = ROOT / "evidence"
EXPECTED = json.loads((ROOT / "expected.json").read_text())
ORIGINAL = Path("/home/me/Projects/index-qualification.iIHbKX/DevForgeAI/devforgeai")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")

def snapshot(root):
    return [{"path":p.relative_to(root).as_posix(), "bytes":p.stat().st_size, "sha256":digest(p)}
            for p in sorted(root.rglob("*")) if p.is_file() and "target" not in p.relative_to(root).parts and ".git" not in p.relative_to(root).parts]

def execute(name, args, env):
    directory = OUT / "attempts" / name
    directory.mkdir(parents=True, exist_ok=False)
    source = snapshot(PROJECT)
    write(directory / "source.json", source)
    assert source == EXPECTED["files"], "candidate drift before " + name
    start = time.monotonic()
    receipt = {"argv":args, "cwd":str(PROJECT), "started_at":datetime.datetime.now(datetime.timezone.utc).isoformat(), "source_sha256":digest(directory / "source.json"), "environment_overrides":{k:env[k] for k in ["DEVFORGEAI_INDEX_DATA", "LLVM_COV", "LLVM_PROFDATA"] if k in env}, "timeout_seconds":1800}
    print("START " + name, flush=True)
    with (directory / "stdout.txt").open("wb") as stdout, (directory / "stderr.txt").open("wb") as stderr:
        try:
            result = subprocess.run(args, cwd=PROJECT, env=env, stdout=stdout, stderr=stderr, timeout=1800)
            receipt.update(exit_code=result.returncode, outcome="observed_exit")
        except subprocess.TimeoutExpired:
            receipt.update(exit_code=None, outcome="timeout")
    receipt.update(elapsed_seconds=time.monotonic()-start, ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    for path in [directory / "stdout.txt", directory / "stderr.txt"]:
        receipt[path.name + "_sha256"] = digest(path)
    write(directory / "receipt.json", receipt)
    print("END " + name + " exit=" + str(receipt["exit_code"]), flush=True)
    return receipt

def main():
    assert sys.platform == "linux"
    OUT.mkdir(exist_ok=False)
    source = snapshot(PROJECT)
    write(OUT / "source.json", source)
    assert source == EXPECTED["files"], "transferred candidate mismatch"
    original = snapshot(ORIGINAL) if ORIGINAL.exists() else None
    write(OUT / "original-source-before.json", original)
    if original is not None:
        expected_original = json.loads((ROOT / "original-expected.json").read_text())
        observed = {row["path"]:row for row in original}
        write(OUT / "original-drift.json", [row["path"] for row in expected_original if row != observed.get(row["path"])])
    env = os.environ.copy()
    # Native source/build paths stay on ext4; default IPC fixture path stays short.
    env["DEVFORGEAI_INDEX_DATA"] = "/tmp/dfr-" + hashlib.sha256(str(ROOT).encode()).hexdigest()[:12]
    if platform.release().endswith("WSL2"):
        sysroot = subprocess.check_output(["rustc", "--print", "sysroot"], text=True).strip()
        llvm = Path(sysroot) / "lib/rustlib/x86_64-unknown-linux-gnu/bin"
        env["LLVM_COV"] = str(llvm / "llvm-cov")
        env["LLVM_PROFDATA"] = str(llvm / "llvm-profdata")
    else:
        env["LLVM_COV"] = "/usr/bin/llvm-cov-21"
        env["LLVM_PROFDATA"] = "/usr/bin/llvm-profdata-21"
    tools = {"platform":platform.platform(), "cwd":str(PROJECT.resolve()), "source_candidate_sha256":EXPECTED["windows_manifest_sha256"], "commands":[]}
    for args in [["rustc","-vV"], ["cargo","-vV"], ["cargo","llvm-cov","--version"], [env["LLVM_COV"],"--version"], [env["LLVM_PROFDATA"],"--version"]]:
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        tools["commands"].append({"argv":args,"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr,"executable":shutil.which(args[0])})
    write(OUT / "tools.json", tools)
    runs = []
    commands = [
        ("fmt", ["cargo","fmt","--all","--","--check"]),
        ("clippy", ["cargo","clippy","--locked","--offline","--all-targets","--","-D","warnings"]),
        ("build", ["cargo","build","--locked","--offline","--release","--bins","--example","wsl_fixture"]),
        ("coverage", ["cargo","llvm-cov","--locked","--offline","--all-targets","--ignore-run-fail","--json","--output-path",str(OUT / "coverage.json"),"--fail-under-lines","95","--ignore-filename-regex",r"[/\\](tests|examples|fixtures)[/\\]","--","--test-threads=1"]),
    ]
    for name,args in commands:
        runs.append(execute(name,args,env))
    profiles = OUT / "profiles"
    profiles.mkdir()
    retained = []
    target = PROJECT / "target/llvm-cov-target"
    for path in sorted(target.rglob("*")):
        if path.is_file() and path.suffix in (".profraw", ".profdata"):
            to = profiles / path.relative_to(target)
            to.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path,to)
            retained.append({"source":str(path),"retained":str(to),"bytes":to.stat().st_size,"sha256":digest(to)})
    write(OUT / "profile-manifest.json", retained)
    binaries = []
    for name in ["devforgeai", "devforgeai-indexd", "devforgeai-tray", "examples/wsl_fixture"]:
        binary = PROJECT / "target/release" / name
        if binary.exists():
            binaries.append({"path":str(binary),"bytes":binary.stat().st_size,"sha256":digest(binary)})
    after = snapshot(PROJECT)
    assert after == source, "test source drift"
    original_after = snapshot(ORIGINAL) if original is not None else None
    assert original_after == original, "original source drift"
    processes = []
    for p in Path("/proc").iterdir():
        if p.name.isdigit():
            try:
                executable = os.readlink(p / "exe")
                if str(ROOT) in executable:
                    processes.append({"pid":int(p.name),"executable":executable})
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                pass
    write(OUT / "completion.json", {"source_unchanged":True,"original_source_unchanged":True,"original_present":original is not None,"runs":runs,"binaries":binaries,"remaining_owned_processes":processes})
    print("COMPLETE " + str(OUT), flush=True)

if __name__ == "__main__":
    main()
