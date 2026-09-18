import os
import sys


def main():
    raw = os.environ.get("LIMIT", "").strip()
    try:
        value = int(raw)
    except ValueError:
        print("error: invalid limit")
        return 2
    if value < 1 or value > 100:
        print("error: invalid limit")
        return 2
    print(f"limit={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
