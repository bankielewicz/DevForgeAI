"""Retain one read-only configuration/layer file inventory."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = Path("C:/Projects/DevForgeAI")
POWERSHELL = Path("C:/Program Files/PowerShell/7/pwsh.exe")
SCRIPT = Path(__file__).with_name("readback.ps1")

spec = spec_from_file_location("native_evidence_record", ROOT / "record.py")
if spec is None or spec.loader is None:
    raise RuntimeError("could not load evidence recorder")
record = module_from_spec(spec)
spec.loader.exec_module(record)

record.capture(
    "profile-research/17-config-layer-readback",
    [POWERSHELL, "-NoProfile", "-NonInteractive", "-File", SCRIPT],
    cwd=WORK,
    timeout=30,
)
