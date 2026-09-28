"""Command-line entry point for pollwatch."""
import argparse
import time
import urllib.request

from pollwatch.config import load


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pollwatch")
    parser.add_argument("--config", default="pollwatch.toml")
    parser.add_argument("--once", action="store_true", help="poll one time and exit")
    args = parser.parse_args(argv)
    config = load(args.config)
    last = None
    while True:
        with urllib.request.urlopen(config["url"]) as response:
            status = response.status
        if status != last:
            print(f"status {status}")
            last = status
        if args.once:
            return 0
        time.sleep(int(config["poll_interval_seconds"]))
