#!/usr/bin/env python3
"""Validate a completed GitHub incident review against the fixed report contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Sequence


REQUIRED_H2 = (
    "Review snapshot",
    "Disposition",
    "Executive ruling",
    "Provenance",
    "Claim ledger",
    "Reproduction and negative-path verification",
    "Related and duplicate incidents",
    "Scope and coupling",
    "Acceptance criteria audit",
    "Linked implementation and CI",
    "Findings",
    "Required amendments",
    "Recommended GitHub actions",
    "Copy-ready postings",
    "Final ruling",
)
REQUIRED_H3 = ("Reviewed incident", "Canonical incident")
INCIDENT_DISPOSITIONS = frozenset(
    {"VALID", "VALID_WITH_AMENDMENTS", "INVALID", "INCONCLUSIVE"}
)
IMPLEMENTATION_DISPOSITIONS = frozenset(
    {"NOT_APPLICABLE", "ACCEPT", "CHANGES_REQUIRED", "HOLD_INCONCLUSIVE"}
)
DUPLICATE_CLASSES = frozenset(
    {"EXACT_DUPLICATE", "OVERLAP", "RELATED", "RECURRENCE", "NONE", "INCONCLUSIVE"}
)
PROVENANCE_LABELS = (
    "Repository remote",
    "Default branch",
    "Base SHA",
    "Head SHA",
    "Tree status",
    "Evidence captured at",
    "Evidence manifest",
    "Evidence SHA256",
)
DECISION_SECTIONS = (
    "Executive ruling",
    "Required amendments",
    "Recommended GitHub actions",
    "Final ruling",
)
ASPIRATIONAL = (
    "should eventually",
    "ideally",
    "in the future",
    "nice to have",
    "consider",
    "maybe",
    "perhaps",
)
PLACEHOLDER = re.compile(
    r"<[A-Z][A-Z0-9_|-]*>|\b(?:TODO|TBD|FIXME)\b|\{\{[^}]+\}\}", re.IGNORECASE
)


def _section(content: str, heading: str, level: int = 2) -> str:
    marker = f"{'#' * level} {heading}"
    start = content.find(marker)
    if start < 0:
        return ""
    body_start = start + len(marker)
    next_heading = re.search(rf"^#{{1,{level}}}\s+", content[body_start:], re.MULTILINE)
    end = body_start + next_heading.start() if next_heading else len(content)
    return content[body_start:end].strip()


def _value(section: str, label: str) -> str | None:
    match = re.search(rf"^-\s*{re.escape(label)}:\s*(.+?)\s*$", section, re.MULTILINE)
    return match.group(1).strip() if match else None


def _decision_text(content: str) -> str:
    joined = "\n".join(_section(content, heading) for heading in DECISION_SECTIONS)
    without_fences = re.sub(r"```.*?```", "", joined, flags=re.DOTALL)
    return "\n".join(
        line for line in without_fences.splitlines() if not line.lstrip().startswith(">")
    ).lower()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_manifest(value: str, review_path: Path) -> Path | None:
    requested = Path(value)
    candidates = (
        (requested,) if requested.is_absolute() else (review_path.parent / requested, Path.cwd() / requested)
    )
    return next((candidate.resolve() for candidate in candidates if candidate.is_file()), None)


def _validate_evidence_manifest(
    provenance: str, review_path: Path
) -> list[str]:
    errors: list[str] = []
    manifest_value = _value(provenance, "Evidence manifest")
    expected_hash = _value(provenance, "Evidence SHA256")
    if not manifest_value or not expected_hash:
        return errors
    manifest_path = _resolve_manifest(manifest_value, review_path)
    if manifest_path is None:
        return [f"evidence manifest not found: {manifest_value}"]
    actual_hash = _sha256(manifest_path)
    if actual_hash.lower() != expected_hash.lower():
        errors.append(
            f"evidence manifest hash mismatch: expected {expected_hash.lower()}, got {actual_hash}"
        )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid evidence manifest JSON: {exc}")
        return errors
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        errors.append("evidence manifest requires a non-empty files object")
        return errors
    evidence_root = manifest_path.parent.resolve()
    for relative, entry in files.items():
        if not isinstance(relative, str) or not isinstance(entry, dict):
            errors.append(f"invalid evidence manifest entry: {relative!r}")
            continue
        expected_file_hash = entry.get("sha256")
        if not isinstance(expected_file_hash, str) or not re.fullmatch(
            r"[0-9a-fA-F]{64}", expected_file_hash
        ):
            errors.append(f"invalid evidence file SHA256: {relative}")
            continue
        evidence_path = (evidence_root / relative).resolve()
        if not evidence_path.is_relative_to(evidence_root):
            errors.append(f"evidence path escapes manifest directory: {relative}")
            continue
        if not evidence_path.is_file():
            errors.append(f"evidence file not found: {relative}")
            continue
        actual_file_hash = _sha256(evidence_path)
        if actual_file_hash.lower() != expected_file_hash.lower():
            errors.append(
                f"evidence file hash mismatch: {relative}: expected "
                f"{expected_file_hash.lower()}, got {actual_file_hash}"
            )
    return errors


def validate(content: str, *, review_path: Path) -> list[str]:
    errors: list[str] = []
    for heading in REQUIRED_H2:
        if f"## {heading}" not in content:
            errors.append(f"missing required heading: {heading}")
    for heading in REQUIRED_H3:
        if f"### {heading}" not in content:
            errors.append(f"missing required heading: {heading}")

    placeholder = PLACEHOLDER.search(content)
    if placeholder:
        errors.append(f"unresolved placeholder: {placeholder.group(0)}")

    disposition = _section(content, "Disposition")
    incident = _value(disposition, "Incident")
    implementation = _value(disposition, "Linked implementation")
    if incident not in INCIDENT_DISPOSITIONS:
        errors.append(f"invalid incident disposition: {incident!r}")
    if implementation not in IMPLEMENTATION_DISPOSITIONS:
        errors.append(f"invalid linked implementation disposition: {implementation!r}")

    provenance = _section(content, "Provenance")
    for label in PROVENANCE_LABELS:
        if not _value(provenance, label):
            errors.append(f"missing provenance: {label}")
    evidence_hash = _value(provenance, "Evidence SHA256")
    if evidence_hash and not re.fullmatch(r"[0-9a-fA-F]{64}", evidence_hash):
        errors.append("invalid provenance SHA256: expected 64 hexadecimal characters")
    elif evidence_hash:
        errors.extend(_validate_evidence_manifest(provenance, review_path))

    claim_ledger = _section(content, "Claim ledger")
    if "| C-" not in claim_ledger:
        errors.append("claim ledger requires at least one stable claim ID")
    if not any(classification in claim_ledger for classification in ("GROUNDED", "DERIVED", "INCONCLUSIVE")):
        errors.append("claim ledger requires a provenance classification")

    reproduction = _section(content, "Reproduction and negative-path verification")
    if "Positive" not in reproduction or "Negative" not in reproduction:
        errors.append("reproduction requires positive and negative paths")

    duplicates = _section(content, "Related and duplicate incidents")
    duplicate_class = _value(duplicates, "Classification")
    if duplicate_class not in DUPLICATE_CLASSES:
        errors.append(f"invalid duplicate classification: {duplicate_class!r}")
    if "First-pass queries" not in duplicates or "Second-pass queries" not in duplicates:
        errors.append("duplicate analysis requires first-pass and second-pass queries")
    if "Candidate matrix" not in duplicates and "| Candidate |" not in duplicates:
        errors.append("duplicate analysis requires a candidate matrix")

    decision_text = _decision_text(content)
    for phrase in ASPIRATIONAL:
        if re.search(rf"\b{re.escape(phrase)}\b", decision_text):
            errors.append(f"aspirational decision wording is forbidden: {phrase!r}")

    if duplicate_class == "EXACT_DUPLICATE":
        canonical = _value(duplicates, "Canonical incident")
        canonical_post = _section(content, "Canonical incident", level=3)
        reviewed_post = _section(content, "Reviewed incident", level=3)
        actions = _section(content, "Recommended GitHub actions").lower()
        if not canonical or canonical.upper() == "N/A":
            errors.append("exact duplicate requires a canonical incident URL")
        if not canonical_post or canonical_post.upper() == "N/A":
            errors.append("exact duplicate requires a canonical incident posting")
        if "duplicate" not in reviewed_post.lower():
            errors.append("exact duplicate requires a reviewed incident duplicate posting")
        if not re.search(r"\bclos(?:e|ing)\b", actions) or "not planned" not in actions:
            errors.append("exact duplicate requires a close-as-not-planned recommendation")
        if "both post" not in actions:
            errors.append("exact duplicate closure must occur after both postings")

    return errors


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a completed provenance-backed GitHub incident review."
    )
    parser.add_argument("review", type=Path, help="Completed Markdown review file.")
    parser.add_argument(
        "--format", choices=("text", "json"), default="text", help="Diagnostic output format."
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        content = args.review.read_text(encoding="utf-8")
    except OSError as exc:
        errors = [f"cannot read review: {exc}"]
    else:
        errors = validate(content, review_path=args.review.resolve())

    if args.format == "json":
        print(json.dumps({"status": "invalid" if errors else "valid", "errors": errors}, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print("VALID: GitHub incident review contract satisfied")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
