"""Summarize immutable profile-research subprocess receipts and verify their hashes."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


attempts = []
for attempt in sorted(path for path in ROOT.iterdir() if path.is_dir() and path.name[:2].isdigit()):
    receipt_path = attempt / "receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    stdout_path = attempt / "stdout.txt"
    stderr_path = attempt / "stderr.txt"
    manifest_path = attempt / "candidate-manifest.json"
    attempts.append(
        {
            "id": attempt.name,
            "argv": receipt["argv"],
            "cwd": receipt["cwd"],
            "start": receipt["start"],
            "end": receipt["end"],
            "elapsed_seconds": receipt["elapsed_seconds"],
            "exit_code": receipt["exit_code"],
            "executable_sha256": receipt["executable_sha256"],
            "candidate_manifest_sha256": receipt["candidate_manifest_sha256"],
            "candidate_manifest_matches": digest(manifest_path)
            == receipt["candidate_manifest_sha256"],
            "stdout_sha256": receipt["stdout_sha256"],
            "stdout_matches": digest(stdout_path) == receipt["stdout_sha256"],
            "stderr_sha256": receipt["stderr_sha256"],
            "stderr_matches": digest(stderr_path) == receipt["stderr_sha256"],
            "receipt_sha256": digest(receipt_path),
        }
    )

summary = {
    "schema_version": 1,
    "attempt_count": len(attempts),
    "all_stream_hashes_match": all(
        item["stdout_matches"] and item["stderr_matches"] for item in attempts
    ),
    "all_candidate_manifest_hashes_match": all(
        item["candidate_manifest_matches"] for item in attempts
    ),
    "candidate_manifest_sha256_values": sorted(
        {item["candidate_manifest_sha256"] for item in attempts}
    ),
    "attempts": attempts,
}
(ROOT / "probe-summary.json").write_text(
    json.dumps(summary, indent=2) + "\n", encoding="utf-8"
)
