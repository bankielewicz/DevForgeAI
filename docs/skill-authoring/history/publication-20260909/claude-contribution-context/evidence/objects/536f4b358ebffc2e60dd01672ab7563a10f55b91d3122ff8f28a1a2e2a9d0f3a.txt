#!/usr/bin/env python3
"""Report leftover template placeholders and print SHA-256 digests.

Two deterministic facts a DevForge artifact needs before it is presented as
ready: that no required field still holds a {{placeholder}}, and the digest
that upstream/handoff tables reference. Everything else about an artifact
requires judgment and is not checked here.

Usage:
    python3 check_artifact.py FILE [FILE ...]

Exit status is 1 if any placeholder remains, so this can gate a claim of
completion. A placeholder in prose the user is meant to fill later is still
reported: decide whether the field is required, and say so rather than
silently shipping it.
"""

import hashlib
import re
import sys

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


def main(argv):
    paths = argv[1:]
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    found_any = False
    for path in paths:
        try:
            data = open(path, "rb").read()
        except OSError as exc:
            print(f"{path}: COULD_NOT_RUN ({exc.strerror})")
            found_any = True
            continue

        print(f"\n{path}")
        print(f"  sha256: {hashlib.sha256(data).hexdigest()}")

        hits = []
        for lineno, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
            for match in PLACEHOLDER.finditer(line):
                hits.append((lineno, match.group(0)))

        if hits:
            found_any = True
            print(f"  placeholders remaining: {len(hits)}")
            for lineno, text in hits:
                print(f"    line {lineno}: {text}")
        else:
            print("  placeholders remaining: none")

    if found_any:
        print("\nUnresolved placeholders or unreadable files: this artifact is a draft.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
