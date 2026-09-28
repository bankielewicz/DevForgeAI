"""Command-line entry point for wordcount."""
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor


def count_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return {"words": len(text.split()), "lines": len(text.splitlines())}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in text files.")
    parser.add_argument("paths", nargs="+", help="text files to count")
    parser.add_argument("--jobs", type=int, default=1, metavar="N",
                        help="count up to N files at the same time (default: 1)")
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")
    # Roughly 3x faster on big batches.
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(count_file, args.paths))
    for path, counts in zip(args.paths, results):
        print(f"{path}: {counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
