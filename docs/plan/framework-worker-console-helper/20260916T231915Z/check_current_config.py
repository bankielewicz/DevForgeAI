"""Replay only in memory; retain transport metadata, never configured commands/env."""
import hashlib
import json
from pathlib import Path

import tomli

from verify_overrides import replay

RUN = Path(__file__).resolve().parent
config_path = Path(r"C:\Users\bryan\.codex\config.toml")
before = config_path.read_bytes()
config = tomli.loads(before.decode("utf-8-sig"))
argv = json.loads((RUN / "green-ps7/stdout.bin").read_bytes())["argv"]
effective = replay(argv, config)
rows = []
for name, server in effective.get("mcp_servers", {}).items():
    command = isinstance(server.get("command"), str)
    url = isinstance(server.get("url"), str)
    assert command != url, "Missing or conflicting MCP transport after correction"
    assert server.get("enabled") is False, "Existing MCP server was not disabled"
    rows.append({"name": name, "has_stdio_command": command, "has_http_url": url, "enabled": False})
assert set(effective["mcp_servers"]) == set(config["mcp_servers"])
assert config_path.read_bytes() == before
result = {"config_sha256": hashlib.sha256(before).hexdigest(), "mcp_servers": rows,
          "new_mcp_entries": 0, "config_modified": False, "native_codex_launches": 0,
          "scope": "In-memory CLI override replay, not full typed Codex configuration validation"}
with (RUN / "current-config-replay.json").open("x", encoding="utf-8") as output:
    json.dump(result, output, indent=2)
    output.write("\n")
print(json.dumps(result, indent=2))
