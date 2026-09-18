"""Recover the exact QA helper bytes bound immediately before attempt 35."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


EXPECTED = "06975d49d6ed74d672d67c161d3985b45ea94a480cc2752f604e8a1830ad40d5"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corrected", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = args.corrected.resolve(strict=True).read_bytes()
    newline = "\r\n" if b"\r\n" in data else "\n"
    corrected = """    let mut omitted_binding = ReviewCase::new(\"QA-review-omitted-binding-\");
    omitted_binding.review[\"profile_sources\"] = json!([]);
    omitted_binding.bind();
    assert!(
        omitted_binding.verify(false).is_err(),
        \"review qualification must reject an omitted physical source binding\"
    );

    let mut extra_binding = ReviewCase::new(\"QA-review-extra-binding-\");
    extra_binding.review[\"profile_sources\"]
        .as_array_mut()
        .unwrap()
        .push(json!({
            \"path\": extra_binding._root.path().join(\"unreviewed.toml\"),
            \"sha256\": \"d\".repeat(64)
        }));
    extra_binding.bind();
    assert!(
        extra_binding.verify(false).is_err(),
        \"review qualification must reject an extra physical source binding\"
    );""".replace("\n", newline).encode()
    original = r'''    let mut wrong_mapping = ReviewCase::new("QA-review-wrong-mapping-");
    wrong_mapping.inventory["junctions"] = json!([{
        "path": r"C:\\qa\\latest",
        "target": r"C:\\qa\\version",
        "reparse_tag": 0xa000000c_u32
    }]);
    wrong_mapping.bind_inventory();
    assert!(
        wrong_mapping.verify(false).is_err(),
        "review parsing must reject a malformed or wrong-tag inventory mapping"
    );'''.replace("\n", newline).encode()
    if data.count(corrected) != 1:
        raise SystemExit("corrected block not found exactly once")
    recovered = data.replace(corrected, original)
    digest = hashlib.sha256(recovered).hexdigest()
    if digest != EXPECTED:
        raise SystemExit(f"recovered digest mismatch: {digest}")
    output = args.output.resolve(strict=False)
    if output.exists():
        raise SystemExit("output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(recovered)
    print(f"recovered_sha256={digest}")
    print(f"recovered_bytes={len(recovered)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
