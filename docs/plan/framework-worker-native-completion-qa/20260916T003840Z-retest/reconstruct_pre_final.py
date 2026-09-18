"""Reconstruct the three document revisions referenced by the preserved pre-final seal."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "pre-final-snapshot"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(data: bytes, old: bytes, new: bytes) -> bytes:
    if data.count(old) != 1:
        raise SystemExit(f"expected one occurrence of {old!r}, found {data.count(old)}")
    return data.replace(old, new, 1)


def write_exact(name: str, data: bytes, expected: str) -> None:
    if digest(data) != expected:
        raise SystemExit(
            f"{name}: reconstructed bytes={len(data)} digest={digest(data)} != {expected}"
        )
    (OUT / name).write_bytes(data)


def main() -> int:
    OUT.mkdir(exist_ok=True)

    report = (ROOT / "qa-report.md").read_bytes()
    report = replace_once(
        report,
        b"Five nonproduct execution/custody issues remain visible in `failed-attempts.md`:",
        b"Four nonproduct errors remain visible in `failed-attempts.md`:",
    )
    report = replace_once(
        report,
        b"5. The first successful seal omitted external fixture entries and was overwritten before its bytes were retained. No product/raw result changed. The corrected external-aware seal was verified and preserved as `artifact-manifest-pre-final.json` before this disclosure and the final seal.\n\n",
        b"\n",
    )
    report = replace_once(
        report,
        b"None is counted as a product case or pass. Product streams, raw coverage, candidate bindings and available setup-error records were preserved. The preliminary successful artifact index is the disclosed exception; its bytes and digest are unavailable.",
        b"None is counted as a product case or pass. All original bytes/partial records were preserved.",
    )
    write_exact(
        "qa-report.md",
        report,
        "e736bdfb892b17aa446137ba0a513ae30bd6d32c80bd068fb3d60da3524f23cf",
    )

    failed = (ROOT / "failed-attempts.md").read_bytes()
    marker = b"\n## Artifact-seal external-fixture correction"
    if failed.count(marker) != 1:
        raise SystemExit("failed-attempts custody marker is not unique")
    failed = failed.split(marker, 1)[0]
    write_exact(
        "failed-attempts.md",
        failed,
        "9353c494d05ca2aae2b72914afae575c05da33a44745e53d043e275a0f2affa2",
    )

    handoff = (ROOT / "handoff-manifest.json").read_bytes()
    handoff = replace_once(
        handoff,
        b"6e32e519a5aba3e923b8f04818cebf199cac992c54985db45f7c248ba22ad478",
        b"e736bdfb892b17aa446137ba0a513ae30bd6d32c80bd068fb3d60da3524f23cf",
    )
    handoff = replace_once(
        handoff,
        b"a7ebba5358038eb368e0cb48a40372660e0f4be601ef5ce527341467eea636e0",
        b"9353c494d05ca2aae2b72914afae575c05da33a44745e53d043e275a0f2affa2",
    )
    handoff = replace_once(
        handoff,
        b',\n    {"path":"artifact-manifest-pre-final.json","sha256":"1a33c5a7e3840f9044aecd2ac7d2d9c7c7687e588786644ed7f098a27876958e"}',
        b"",
    )
    write_exact(
        "handoff-manifest.json",
        handoff,
        "96e754c263ae9c445f97b83fd426b87fce0598c15419851f6e0625c58fdab9af",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
