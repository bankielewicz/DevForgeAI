"""Run only the selected offline Pester tests and retain their raw outputs."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
TRIAL = ROOT.parents[1] / "framework-worker-trials/20260917T122229Z-logging-diagnostic"
sys.path.insert(0, str(TRIAL))
from supervisor import capture, binding, write_new

run = ROOT / "attempts/10-powershell-host"
run.mkdir(exist_ok=False)
write_new(run / "suite-definition.json", {"required_cases": 7,
    "runtime_sources": [binding(Path(r"C:\Projects\DevForgeAI\Invoke-CodexWorkerDiagnostic.ps1"))],
    "tests": [binding(ROOT / "tests/OperatorHarness.Tests.ps1")],
    "denominator": "All executable lines of the root PowerShell entrypoint; no exclusions",
    "reason_for_host_context": "Pester temporary test registry and environment discovery were denied in the sandbox",
    "native_codex": "NOT_RUN"})
receipt = capture([r"C:\Program Files\PowerShell\7\pwsh.exe", "-NoProfile", "-File",
    str(ROOT / "run_powershell_checks.ps1"), "-EvidencePath", str(run)], ROOT,
    run / "execution", cancel_after=50, grace=2, reap=1, finalize=2, hold_stdin=False)
print((run / "execution/stdout.bin").read_text())
print((run / "execution/stderr.bin").read_text())
raise SystemExit(receipt["process_exit_code"] if receipt["process_exit_code"] is not None else 125)
