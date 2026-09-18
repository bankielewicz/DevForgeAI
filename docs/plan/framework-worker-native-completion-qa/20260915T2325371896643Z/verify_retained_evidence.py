#!/usr/bin/env python3
"""Independent structural and privacy oracle over retained runtime evidence."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re


PROFILE_METHOD_ORDER = [
    "initialize",
    "initialized",
    "config/read",
    "configRequirements/read",
    "experimentalFeature/list",
    "hooks/list",
    "plugin/list",
    "app/installed",
    "mcpServerStatus/list",
    "account/read",
    "model/list",
    "account/rateLimits/read",
]
JOURNAL_KEYS = {"schema_version", "run_id", "seq", "observed_at", "elapsed_ms", "kind", "data"}
PRIVATE_MARKERS = [
    b"DEV_PRIVATE_SENTINEL_9201",
    b"PRIVATE_PLUGIN_SENTINEL",
    b"PRIVATE_LAYER_SECRET",
    b"PRIVATE_EMAIL",
    b"PRIVATE_RPC_MESSAGE",
    b"PRIVATE_CONFIG_SENTINEL",
]


def parse_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_root", type=Path)
    args = parser.parse_args()
    root = args.fixture_root.resolve(strict=True)
    failures: list[str] = []

    profile_traces = sorted(root.rglob("profile-peer-trace.jsonl"))
    if len(profile_traces) != 26:
        failures.append(f"profile trace count={len(profile_traces)}, expected=26")
    all_methods: Counter[str] = Counter()
    for trace_path in profile_traces:
        events = parse_jsonl(trace_path)
        methods = [str(event.get("method")) for event in events]
        all_methods.update(methods)
        ranks: list[int] = []
        for method in methods:
            if method.startswith("thread/") or method.startswith("turn/"):
                failures.append(f"{trace_path}: work method {method}")
            if method not in PROFILE_METHOD_ORDER:
                failures.append(f"{trace_path}: unexpected method {method}")
            else:
                ranks.append(PROFILE_METHOD_ORDER.index(method))
        if ranks != sorted(ranks):
            failures.append(f"{trace_path}: methods out of contract order")
        duplicates = [method for method, count in Counter(methods).items() if count > 1]
        if any(method not in {"experimentalFeature/list", "mcpServerStatus/list"} for method in duplicates):
            failures.append(f"{trace_path}: unexpected duplicate methods {duplicates}")

    journal_files = sorted(root.rglob("journal.jsonl"))
    journal_event_count = 0
    rate_not_measured = 0
    for journal_path in journal_files:
        events = parse_jsonl(journal_path)
        journal_event_count += len(events)
        seqs = [event.get("seq") for event in events]
        if seqs and seqs != list(range(1, len(seqs) + 1)):
            failures.append(f"{journal_path}: non-contiguous sequence")
        for event in events:
            if set(event) != JOURNAL_KEYS:
                failures.append(f"{journal_path}: unapproved journal envelope")
            data = event.get("data")
            if isinstance(data, dict) and "rate_limits" in data:
                if data != {"rate_limits": "not_measured"}:
                    failures.append(f"{journal_path}: invented or extended rate-limit payload")
                rate_not_measured += 1
    if rate_not_measured < 2:
        failures.append(f"explicit unmeasured-rate events={rate_not_measured}, expected at least 2")

    marker_hits: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        data = path.read_bytes()
        for marker in PRIVATE_MARKERS:
            if marker in data:
                marker_hits.append(f"{path}:{marker.decode('ascii')}")
    if marker_hits:
        failures.extend(f"private marker retained: {hit}" for hit in marker_hits)

    peer_cases: list[str] = []
    invalid_peer_case_bytes = 0
    for path in root.rglob("peer-case.txt"):
        try:
            peer_cases.append(path.read_text(encoding="ascii").strip())
        except UnicodeDecodeError:
            invalid_peer_case_bytes += 1
    parent_counts: Counter[str] = Counter()
    for case in peer_cases:
        match = re.fullmatch(r"WF-(\d{2})(?:-.+)?", case)
        if match and 1 <= int(match.group(1)) <= 20:
            parent_counts[f"WF-{match.group(1)}"] += 1
    missing_parents = [f"WF-{number:02d}" for number in range(1, 21) if not parent_counts[f"WF-{number:02d}"]]
    if missing_parents:
        failures.append(f"missing WF parents: {missing_parents}")

    result = {
        "schema_version": 1,
        "fixture_root": str(root),
        "profile_trace_count": len(profile_traces),
        "profile_method_counts": dict(sorted(all_methods.items())),
        "forbidden_work_methods": all_methods["thread/start"] + all_methods["turn/start"],
        "journal_file_count": len(journal_files),
        "journal_event_count": journal_event_count,
        "exact_rate_limits_not_measured_events": rate_not_measured,
        "private_marker_hits": marker_hits,
        "peer_case_file_count": len(peer_cases) + invalid_peer_case_bytes,
        "invalid_peer_case_byte_fixtures": invalid_peer_case_bytes,
        "wf_parent_observation_counts": dict(sorted(parent_counts.items())),
        "missing_wf_parents": missing_parents,
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
