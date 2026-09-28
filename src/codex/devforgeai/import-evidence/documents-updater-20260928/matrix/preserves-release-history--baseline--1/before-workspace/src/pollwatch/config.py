"""Loads pollwatch.toml."""
import tomllib

DEFAULTS = {"url": None, "poll_interval_seconds": 30}


def load(path="pollwatch.toml"):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    config = {**DEFAULTS, **data}
    if not config["url"]:
        raise ValueError("pollwatch.toml must set url")
    if int(config["poll_interval_seconds"]) < 5:
        raise ValueError("poll_interval_seconds must be at least 5")
    return config
