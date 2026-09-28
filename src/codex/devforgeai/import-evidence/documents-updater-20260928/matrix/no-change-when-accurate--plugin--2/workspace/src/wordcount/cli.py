"""Command-line entry point for wordcount."""
import argparse
import json
import sys


def count_words(text):
    return len(text.split())


def count_lines(text):
    return len(text.splitlines())


def count(text):
    return {"words": count_words(text), "lines": count_lines(text)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount", description="Count words and lines in a text file.")
    parser.add_argument("path", help="text file to count")
    parser.add_argument("--lines", action="store_true", help="print only the line count")
    parser.add_argument("--json", action="store_true", help="print the counts as a JSON object")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        counts = count(f.read())
    if args.json:
        print(json.dumps(counts))
    elif args.lines:
        print(counts["lines"])
    else:
        print(f"{counts['words']} words, {counts['lines']} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
