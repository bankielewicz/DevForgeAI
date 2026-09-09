#!/usr/bin/env python3
"""Deterministic receipt checks for a checkpoint/transfer handoff.

Two modes, kept separate because they establish different things. Read the scope
statements before reporting any result from this script.

MODE 1 - receipt verification (--expected-sha256). A guarantee:
  digest_format        the claimed digest is exactly 64 lowercase hexadecimal characters.
  digest_matches_bytes recomputing SHA-256 over the file's bytes reproduces that digest.

MODE 2 - self-receipt inspection (--self-receipt-inspection). NOT a guarantee. A
document must not carry a receipt for itself, but that is a claim about meaning, and
this script only sees text. It therefore reports rather than adjudicates:
  no_digest_present    PASS only when the file contains no 64-hex token at all. In that
                       case, and only in that case, the absence of a self-receipt is
                       established by the absence of any digest.
  literal_self_digest  FAIL when the file literally contains its own final digest.
                       This predicate cannot be made to fail by construction, because a
                       SHA-256 fixed point is not reachable by appending a digest to the
                       text being hashed. It is retained for completeness and is
                       explicitly NOT a tested guarantee; do not count it as one.
  unadjudicated        Every other digest occurrence is listed with its line number and
                       reported COULD_NOT_RUN. A digest naming another file is legitimate
                       and is not failed here; a self-receipt split across lines is not
                       passed here either. Both need separate inspection by the author.

What neither mode establishes: that the content is correct, complete, authorized or
accepted, or that the workflow's no-self-receipt rule was honoured. That rule is upheld
by the documented write order - finish the referenced records, hash them, write the
handoff, read it back, and deliver its digest outside its bytes - not by this script.

Prerequisites: Python 3.8+ standard library only. No network, no configuration. This
project's packaging does not preserve executable mode bits, so invoke through the
interpreter: `python3 /absolute/path/to/check_receipt.py --help`.

Exit status:
  0  every requested check passed (PASS)
  2  a requested check failed (FAIL)
  3  the file could not be read (COULD_NOT_RUN)
  4  the invocation asserted nothing (COULD_NOT_RUN)
  5  inspection ran but could not adjudicate one or more digest occurrences
     (COULD_NOT_RUN); distinct from 3 so a caller can tell "could not read the file"
     from "read it, and these lines need separate inspection"

Output is one `check=<name> outcome=<label>` line per check plus a final `overall=<label>`
line, using only the vocabulary PASS, FAIL, COULD_NOT_RUN.
"""

import argparse
import hashlib
import os
import re
import sys

EXIT_PASS = 0
EXIT_FAIL = 2
EXIT_UNREADABLE = 3
EXIT_BAD_INVOCATION = 4
EXIT_UNADJUDICATED = 5

FULL_DIGEST = re.compile(r"^[0-9a-f]{64}$")
ANY_DIGEST = re.compile(r"\b[0-9a-fA-F]{64}\b")


def read_bytes(path):
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as error:
        print(f"check=read_file outcome=COULD_NOT_RUN cause={error.__class__.__name__}: {error}")
        return None


def report(name, outcome, detail):
    print(f"check={name} outcome={outcome} {detail}")
    return outcome


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verify a handoff receipt, and separately list digest occurrences for author inspection.",
        epilog="Receipt verification is a guarantee. Self-receipt inspection is a listing, not a guarantee.",
    )
    parser.add_argument("--file", required=True, help="path to the file being receipted")
    parser.add_argument(
        "--expected-sha256",
        default=None,
        help="the 64-character lowercase digest to verify; omit for inspection-only use",
    )
    parser.add_argument(
        "--self-receipt-inspection",
        action="store_true",
        help="list digest occurrences this script cannot adjudicate, for separate inspection",
    )
    args = parser.parse_args(argv)

    if args.expected_sha256 is None and not args.self_receipt_inspection:
        print("check=invocation outcome=COULD_NOT_RUN "
              "cause=nothing asserted: pass --expected-sha256, --self-receipt-inspection, or both")
        print("overall=COULD_NOT_RUN")
        return EXIT_BAD_INVOCATION

    data = read_bytes(args.file)
    if data is None:
        print("overall=COULD_NOT_RUN")
        return EXIT_UNREADABLE

    actual = hashlib.sha256(data).hexdigest()
    print(f"file={args.file}")
    print(f"computed_sha256={actual}")

    failed = False
    unadjudicated = False

    if args.expected_sha256 is not None:
        claimed = args.expected_sha256
        if report("digest_format", "PASS" if FULL_DIGEST.match(claimed) else "FAIL",
                  f"claimed_length={len(claimed)} (a receipt is 64 lowercase hex characters)") == "FAIL":
            failed = True
        # Compared in full even when the format is wrong, so an abbreviation is never
        # accepted as a prefix match: only byte-for-byte equality passes.
        if report("digest_matches_bytes", "PASS" if claimed == actual else "FAIL",
                  f"claimed={claimed} computed={actual}") == "FAIL":
            failed = True

    if args.self_receipt_inspection:
        text = data.decode("utf-8", errors="replace")
        occurrences = []
        for number, line in enumerate(text.splitlines(), start=1):
            for token in ANY_DIGEST.findall(line):
                occurrences.append((number, token))

        if not occurrences:
            report("no_digest_present", "PASS",
                   "the file contains no 64-hex token, so it records no receipt for anything, "
                   "itself included")
        else:
            report("no_digest_present", "COULD_NOT_RUN",
                   f"{len(occurrences)} digest occurrence(s) present, so absence of a "
                   "self-receipt is not established by this check")

        if actual.encode("ascii") in data:
            report("literal_self_digest", "FAIL",
                   "the file contains its own final digest")
            failed = True
        else:
            report("literal_self_digest", "PASS",
                   "the file does not contain its own final digest. NON-DISCRIMINATING: a "
                   "SHA-256 fixed point is not constructible, so this predicate cannot be made "
                   "to fail and is not a tested guarantee")

        if occurrences:
            lines = sorted({n for n, _ in occurrences})
            report("unadjudicated_digest_occurrences", "COULD_NOT_RUN",
                   f"lines {lines} carry a 64-hex token. This script cannot tell a legitimate "
                   "reference to another file from a receipt for this one, including forms split "
                   "across lines. Inspect these lines and confirm none is a receipt for "
                   f"{os.path.basename(args.file)}")
            unadjudicated = True

    if failed:
        print("overall=FAIL")
        print("scope=receipt verification is byte identity and format only; self-receipt "
              "inspection is a listing, not a guarantee; neither is semantic acceptance")
        return EXIT_FAIL
    if unadjudicated:
        print("overall=COULD_NOT_RUN")
        print("scope=receipt verification is byte identity and format only; self-receipt "
              "inspection is a listing, not a guarantee; neither is semantic acceptance")
        return EXIT_UNADJUDICATED
    print("overall=PASS")
    print("scope=receipt verification is byte identity and format only; self-receipt "
          "inspection is a listing, not a guarantee; neither is semantic acceptance")
    return EXIT_PASS


if __name__ == "__main__":
    sys.exit(main())
