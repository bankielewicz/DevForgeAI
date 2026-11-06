"""Where the pinned jsonschema environments are (#122, #155).

`src/tests/process/make_jsonschema_envs.sh` builds them under the main checkout's `tmp/test-envs/`, which every
worktree shares. The policy and context scripts' tests load this file by path with importlib, so it isn't a test
module and needs no package.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SETUP = "no pinned environment: run bash src/tests/process/make_jsonschema_envs.sh"


def base():
    """The main checkout's root (the parent of git's common dir); this checkout's root when git can't tell."""
    try:
        p = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           capture_output=True, text=True)
    except OSError:
        return ROOT
    out = p.stdout.strip()
    return Path(out).parent if p.returncode == 0 and out else ROOT


def python(version):
    """The interpreter of the environment pinned to this jsonschema version."""
    return base() / f"tmp/test-envs/jsonschema-{version}/bin/python"
