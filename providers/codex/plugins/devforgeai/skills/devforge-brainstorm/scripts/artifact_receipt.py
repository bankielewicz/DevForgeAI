"""Read-only byte receipt and template-marker scan; Python 3 standard library only."""

import argparse
import hashlib
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(
        description="Hash UTF-8 artifacts and locate {{...}} markers. No schema or semantic validation. "
        "Exit 0: nonempty readable files without markers; 1: empty/markers; 2: read/decode error."
    )
    parser.add_argument("paths", type=Path, nargs="+", help="Absolute completed artifact paths")
    args = parser.parse_args()
    results = []
    exit_code = 0
    for path in args.paths:
        try:
            if not path.is_absolute():
                raise ValueError("an absolute artifact path is required")
            data = path.read_bytes()
            content = data.decode("utf-8")
            lines = [i for i, line in enumerate(content.splitlines(), 1) if re.search(r"\{\{.*?\}\}", line)]
            failed = not content.strip() or bool(lines)
            results.append({"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
                            "bytes": len(data), "placeholder_lines": lines,
                            "structural_outcome": "FAIL" if failed else "PASS"})
            exit_code = max(exit_code, int(failed))
        except (OSError, UnicodeError, ValueError) as exc:
            results.append({"path": str(path), "structural_outcome": "COULD_NOT_RUN", "cause": str(exc)})
            exit_code = 2
    print(json.dumps({"scope": "byte identity, nonempty UTF-8, same-line template markers only",
                      "semantic_validation": "NOT_EVALUATED", "files": results}, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
