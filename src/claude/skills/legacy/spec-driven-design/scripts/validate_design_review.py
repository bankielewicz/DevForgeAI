#!/usr/bin/env python3
"""Validate untrusted inline Design Jury evidence without trusting claimed scores."""

from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import math
import re
import struct
import sys
import zlib
from pathlib import Path
from typing import Any


WEIGHTS = {"designer": 0.0, "critic": 0.4, "brand": 0.2, "a11y": 0.2, "copy": 0.2}
SCORING_ROLES = ("critic", "brand", "a11y", "copy")
DIMENSIONS = {
    "critic": ("hierarchy", "type", "contrast", "rhythm", "space"),
    "brand": ("palette", "typography", "spacing"),
    "a11y": ("contrast", "focus", "headings", "alt_text", "target_sizes"),
    "copy": ("specificity", "voice", "action_naming", "length"),
}
EVIDENCE_RE = re.compile(
    r"(?:\b(?:artifact|source)\s+line:\d+\b|\b(?:desktop|mobile):\d+,\d+,\d+,\d+\b)",
    re.I,
)
PNG_CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
PNG_ADAM7_PASSES = (
    (0, 0, 8, 8),
    (4, 0, 8, 8),
    (0, 4, 4, 8),
    (2, 0, 4, 4),
    (0, 2, 2, 4),
    (1, 0, 2, 2),
    (0, 1, 1, 2),
)
PNG_MAX_DECODED_BYTES = 64 * 1024 * 1024


class ReviewError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReviewError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load(path: Path, label: str) -> dict[str, Any]:
    try:
        if path.is_symlink() or not path.is_file():
            raise ReviewError(f"{label} file missing or unsafe")
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs)
    except ReviewError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReviewError(f"malformed {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewError(f"malformed {label}: expected object")
    return value


def _sha(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ReviewError(f"hash input missing or unsafe: {path.name}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReviewError(f"invalid {label} score")
    number = float(value)
    if not math.isfinite(number) or not 0 <= number <= 10:
        raise ReviewError(f"invalid {label} score")
    return number


def _same(left: float, right: Any, label: str) -> None:
    claimed = _number(right, label)
    if abs(left - claimed) > 0.001:
        raise ReviewError(f"inflated or incorrect {label}")


def _ref(base: Path, value: Any, expected: Path, label: str) -> None:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ReviewError(f"invalid {label} path")
    candidate = (base / value).resolve(strict=False)
    if candidate != expected.resolve():
        raise ReviewError(f"{label} path mismatch")


def _png_scanline_layout(
    width: int, height: int, bit_depth: int, color_type: int, interlace: int,
) -> tuple[list[tuple[int, int]], int] | None:
    bits_per_pixel = PNG_CHANNELS[color_type] * bit_depth
    passes = PNG_ADAM7_PASSES if interlace else ((0, 0, 1, 1),)
    layout: list[tuple[int, int]] = []
    decoded_size = 0
    for x_start, y_start, x_step, y_step in passes:
        pass_width = 0 if width <= x_start else (width - x_start + x_step - 1) // x_step
        pass_height = 0 if height <= y_start else (height - y_start + y_step - 1) // y_step
        if pass_width == 0 or pass_height == 0:
            continue
        row_bytes = (pass_width * bits_per_pixel + 7) // 8
        decoded_size += pass_height * (row_bytes + 1)
        if decoded_size > PNG_MAX_DECODED_BYTES:
            return None
        layout.append((pass_height, row_bytes))
    return layout, decoded_size


def _png_image_stream_valid(
    compressed: bytes, width: int, height: int, bit_depth: int,
    color_type: int, interlace: int,
) -> bool:
    scanlines = _png_scanline_layout(width, height, bit_depth, color_type, interlace)
    if scanlines is None:
        return False
    layout, decoded_size = scanlines
    try:
        decoder = zlib.decompressobj()
        decoded = decoder.decompress(compressed, decoded_size + 1)
    except zlib.error:
        return False
    if (
        len(decoded) != decoded_size
        or not decoder.eof
        or decoder.unused_data
        or decoder.unconsumed_tail
    ):
        return False
    offset = 0
    for row_count, row_bytes in layout:
        for _ in range(row_count):
            if decoded[offset] > 4:
                return False
            offset += row_bytes + 1
    return offset == len(decoded)


def _parse_png_dimensions(
    data: bytes, expected_dimensions: tuple[int, int] | None = None,
) -> tuple[int, int] | None:
    if len(data) < 45 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    offset = 8
    chunk_index = 0
    dimensions: tuple[int, int] | None = None
    png_format: tuple[int, int, int, int, int] | None = None
    idat_seen = False
    idat_closed = False
    idat_payloads: list[bytes] = []
    while offset < len(data):
        if len(data) - offset < 12:
            return None
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data) or any(
            value not in range(ord("A"), ord("Z") + 1)
            and value not in range(ord("a"), ord("z") + 1)
            for value in chunk_type
        ):
            return None
        payload = data[offset + 8:offset + 8 + length]
        claimed_crc = struct.unpack(">I", data[offset + 8 + length:chunk_end])[0]
        if binascii.crc32(chunk_type + payload) & 0xFFFFFFFF != claimed_crc:
            return None

        if chunk_index == 0:
            if chunk_type != b"IHDR" or length != 13:
                return None
            width, height, bit_depth, color_type, compression, filtering, interlace = (
                struct.unpack(">IIBBBBB", payload)
            )
            allowed_depths = {
                0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8},
                4: {8, 16}, 6: {8, 16},
            }
            if (
                width == 0
                or height == 0
                or bit_depth not in allowed_depths.get(color_type, set())
                or compression != 0
                or filtering != 0
                or interlace not in {0, 1}
            ):
                return None
            dimensions = (width, height)
            if expected_dimensions is not None and dimensions != expected_dimensions:
                return None
            png_format = (width, height, bit_depth, color_type, interlace)
        elif chunk_type == b"IHDR":
            return None

        if chunk_type == b"IDAT":
            if dimensions is None or idat_closed:
                return None
            idat_seen = True
            idat_payloads.append(payload)
        elif idat_seen:
            idat_closed = True

        if chunk_type == b"IEND":
            if (
                length != 0
                or not idat_seen
                or chunk_end != len(data)
                or png_format is None
                or not _png_image_stream_valid(b"".join(idat_payloads), *png_format)
            ):
                return None
            return dimensions

        offset = chunk_end
        chunk_index += 1
    return None


def _png_dimensions(path: Path, expected: tuple[int, int]) -> tuple[int, int]:
    dimensions = _parse_png_dimensions(path.read_bytes(), expected)
    if dimensions is None:
        raise ReviewError(f"screenshot is not a valid PNG: {path.name}")
    return dimensions


def _validate_inputs(
    artifact: Path, lint_path: Path, render_path: Path, review_path: Path,
    review: dict[str, Any],
) -> None:
    base = review_path.parent
    artifact_hash = _sha(artifact)
    artifact_ref = review.get("artifact")
    if not isinstance(artifact_ref, dict):
        raise ReviewError("artifact evidence missing")
    _ref(base, artifact_ref.get("path"), artifact, "artifact")
    if artifact_ref.get("sha256") != artifact_hash:
        raise ReviewError("artifact hash mismatch")

    lint = _load(lint_path, "lint")
    if lint.get("artifact_sha256") != artifact_hash:
        raise ReviewError("lint artifact hash mismatch")
    if not isinstance(lint.get("p0"), list) or lint["p0"]:
        raise ReviewError("lint contains P0 findings")
    for key in ("p1", "p2"):
        if not isinstance(lint.get(key), list):
            raise ReviewError("malformed lint counts")
    lint_ref = review.get("lint")
    if not isinstance(lint_ref, dict):
        raise ReviewError("lint evidence missing")
    _ref(base, lint_ref.get("path"), lint_path, "lint")
    if lint_ref.get("sha256") != _sha(lint_path):
        raise ReviewError("lint report hash mismatch")
    counts = {key: len(lint[key]) for key in ("p0", "p1", "p2")}
    if lint_ref.get("counts") != counts:
        raise ReviewError("lint counts mismatch")

    render = _load(render_path, "render manifest")
    if render.get("artifact_sha256") != artifact_hash:
        raise ReviewError("render artifact hash mismatch")
    for field in ("console_errors", "page_errors", "failed_requests"):
        if not isinstance(render.get(field), list) or render[field]:
            raise ReviewError(f"render {field} are not empty")
    records = render.get("screenshots")
    if not isinstance(records, list) or len(records) != 2:
        raise ReviewError("required screenshots missing")
    expected = {"desktop": (1440, 900), "mobile": (390, 844)}
    seen: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or record.get("name") not in expected:
            raise ReviewError("invalid screenshot record")
        name = record["name"]
        if name in seen:
            raise ReviewError("duplicate screenshot record")
        screenshot = (render_path.parent / str(record.get("path", ""))).resolve(strict=False)
        if not screenshot.is_file() or screenshot.is_symlink():
            raise ReviewError(f"screenshot missing: {name}")
        if record.get("sha256") != _sha(screenshot):
            raise ReviewError(f"screenshot hash mismatch: {name}")
        if (record.get("width"), record.get("height")) != expected[name]:
            raise ReviewError(f"screenshot viewport mismatch: {name}")
        if _png_dimensions(screenshot, expected[name]) != expected[name]:
            raise ReviewError(f"screenshot dimensions mismatch: {name}")
        seen[name] = record
    if set(seen) != set(expected):
        raise ReviewError("required screenshots missing")

    render_ref = review.get("render")
    if not isinstance(render_ref, dict):
        raise ReviewError("render evidence missing")
    _ref(base, render_ref.get("path"), render_path, "render")
    if render_ref.get("sha256") != _sha(render_path):
        raise ReviewError("render manifest hash mismatch")
    review_screenshots = render_ref.get("screenshots")
    if not isinstance(review_screenshots, list) or len(review_screenshots) != 2:
        raise ReviewError("review screenshots missing")
    for record in review_screenshots:
        if not isinstance(record, dict) or record.get("name") not in seen:
            raise ReviewError("review screenshot mismatch")
        source = seen[record["name"]]
        for field in ("path", "sha256", "width", "height"):
            if record.get(field) != source.get(field):
                raise ReviewError("review screenshot hash or viewport mismatch")


def _validate_rounds(review: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[int, float]]:
    if review.get("weights") != WEIGHTS:
        raise ReviewError("jury weights mismatch")
    rounds = review.get("rounds")
    if not isinstance(rounds, list) or not 1 <= len(rounds) <= 3:
        raise ReviewError("round limit violated")
    composites: dict[int, float] = {}
    previous_bytes: int | None = None
    for index, round_data in enumerate(rounds, start=1):
        if not isinstance(round_data, dict) or round_data.get("round") != index:
            raise ReviewError("round sequence invalid")
        transcript = round_data.get("critique_transcript")
        if not isinstance(transcript, str) or not transcript:
            raise ReviewError("critique transcript missing")
        transcript_bytes = len(transcript.encode("utf-8"))
        if round_data.get("transcript_bytes") != transcript_bytes:
            raise ReviewError("transcript byte count mismatch")
        if previous_bytes is not None and transcript_bytes >= previous_bytes:
            raise ReviewError("transcript did not strictly shrink")
        previous_bytes = transcript_bytes

        panelists = round_data.get("panelists")
        if not isinstance(panelists, dict) or set(panelists) != set(WEIGHTS):
            raise ReviewError("jury roster mismatch")
        if not isinstance(panelists["designer"], dict) or not panelists["designer"].get("notes"):
            raise ReviewError("designer notes missing")
        panel_scores: dict[str, float] = {}
        for role in SCORING_ROLES:
            panel = panelists[role]
            if not isinstance(panel, dict):
                raise ReviewError(f"{role} panel missing")
            dimensions = panel.get("dimensions")
            if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS[role]):
                raise ReviewError(f"{role} dimension roster mismatch")
            scores = []
            for name in DIMENSIONS[role]:
                dimension = dimensions[name]
                if not isinstance(dimension, dict):
                    raise ReviewError(f"{role} {name} evidence missing")
                score = _number(dimension.get("score"), f"{role} {name}")
                evidence = dimension.get("evidence")
                if (
                    not isinstance(evidence, list)
                    or not evidence
                    or not all(isinstance(item, str) and EVIDENCE_RE.search(item) for item in evidence)
                ):
                    raise ReviewError(f"{role} {name} evidence missing or non-concrete")
                scores.append(score)
            score = sum(scores) / len(scores)
            _same(score, panel.get("claimed_score"), f"{role} panel score")
            panel_scores[role] = score
            must_fix = panel.get("must_fix")
            if not isinstance(must_fix, list):
                raise ReviewError(f"{role} MUST_FIX list missing")
            for item in must_fix:
                if (
                    not isinstance(item, dict)
                    or not isinstance(item.get("id"), str)
                    or not item.get("id")
                    or not isinstance(item.get("target"), str)
                    or not item.get("target")
                    or item.get("status") not in {"open", "resolved"}
                ):
                    raise ReviewError(f"invalid {role} MUST_FIX")
        composite = sum(panel_scores[role] * WEIGHTS[role] for role in SCORING_ROLES)
        _same(composite, round_data.get("claimed_composite"), "round composite")
        composites[index] = composite

        if index < len(rounds):
            targets: dict[str, set[str]] = {}
            for role in SCORING_ROLES:
                open_items = [item for item in panelists[role]["must_fix"] if item["status"] == "open"]
                if not open_items:
                    raise ReviewError(f"non-final round missing {role} MUST_FIX")
                targets[role] = {item["target"] for item in open_items}
            if not any(targets[role] - targets["critic"] for role in ("brand", "a11y", "copy")):
                raise ReviewError("MUST_FIX target divergence missing")
            if round_data.get("decision") != "continue":
                raise ReviewError("non-final round decision invalid")
    return rounds, composites


def validate(
    *, mode: str, artifact: Path, lint_path: Path, render_path: Path, review_path: Path,
) -> dict[str, Any]:
    if mode == "extract":
        raise ReviewError("Design Jury review data is inapplicable to extract mode")
    if mode not in {"story", "standalone"}:
        raise ReviewError("invalid review mode")
    review = _load(review_path, "design review")
    if review.get("schema_version") != "1.0" or review.get("mode") != mode:
        raise ReviewError("review schema or mode mismatch")
    _validate_inputs(artifact, lint_path, render_path, review_path, review)
    rounds, composites = _validate_rounds(review)
    selected = review.get("selected_round")
    if isinstance(selected, bool) or not isinstance(selected, int) or selected not in composites:
        raise ReviewError("selected round invalid")
    selected_round = rounds[selected - 1]
    open_items = [
        item
        for role in SCORING_ROLES
        for item in selected_round["panelists"][role]["must_fix"]
        if item["status"] == "open"
    ]
    composite = composites[selected]
    _same(composite, review.get("claimed_composite"), "final composite")
    passing = composite >= 8.0 and not open_items
    status = review.get("status")
    if passing:
        if status != "gate_passed" or selected != len(rounds):
            raise ReviewError("selected gate-passed round invalid")
        if selected_round.get("decision") != "gate_passed":
            raise ReviewError("gate-passed decision invalid")
        if review.get("remaining_must_fix") != []:
            raise ReviewError("gate_passed contains remaining MUST_FIX")
    else:
        if status != "below_threshold":
            raise ReviewError("open MUST_FIX requires below_threshold status")
        best_round = max(composites, key=composites.get)
        if selected != best_round:
            raise ReviewError("selected ship_best round is not highest composite")
        if selected_round.get("decision") != "ship_best":
            raise ReviewError("below_threshold decision must be ship_best")
        if review.get("remaining_must_fix") != open_items:
            raise ReviewError("remaining MUST_FIX list mismatch")
    return {
        "schema_version": "1.0",
        "structurally_honest": True,
        "status": status,
        "selected_round": selected,
        "composite": round(composite, 6),
        "remaining_must_fix": open_items,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["story", "standalone", "extract"])
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--lint", required=True)
    parser.add_argument("--render", required=True)
    parser.add_argument("--review", required=True)
    args = parser.parse_args(argv)
    try:
        result = validate(
            mode=args.mode,
            artifact=Path(args.artifact).resolve(),
            lint_path=Path(args.lint).resolve(),
            render_path=Path(args.render).resolve(),
            review_path=Path(args.review).resolve(),
        )
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except (OSError, ReviewError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
