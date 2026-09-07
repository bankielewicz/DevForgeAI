"""Read-only structural validation; never execute code from the framework candidate."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import tomllib


# This is framework-owned validation code, never a candidate-provided module.
_runtime_spec = importlib.util.spec_from_file_location(
    "devforge_runtime_requirements", Path(__file__).with_name("runtime_requirements.py"))
runtime_requirements = importlib.util.module_from_spec(_runtime_spec)
_runtime_spec.loader.exec_module(runtime_requirements)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_files(root):
    pending = [root]
    while pending:
        for path in pending.pop().iterdir():
            if path.name in (".git", ".poc", "__pycache__"):
                continue
            rel = path.relative_to(root)
            if path.is_symlink():
                raise ValueError(f"symlink not accepted: {rel}")
            if path.is_dir():
                # Only the real root operational directory is outside source scope.
                if rel != Path(".devforge-runtime"):
                    pending.append(path)
            elif path.is_file():
                yield path


def validate(root):
    count = 0
    for path in source_files(root):
        rel = path.relative_to(root)
        if ".github" in rel.parts and "workflows" in rel.parts:
            raise ValueError("GitHub workflows belong in DevForge")
        if path.suffix == ".json":
            json.loads(path.read_text())
        if path.suffix == ".toml":
            data = tomllib.loads(path.read_text())
            if "agents" in rel.parts:
                require(all(data.get(k) for k in ("name", "description", "developer_instructions")), str(rel))
        if path.suffix == ".py":
            ast.parse(path.read_text(), filename=str(rel))
        if path.name == "SKILL.md":
            text = path.read_text()
            require(text.startswith("---\n"), str(rel))
            front = text.split("---\n", 2)[1]
            name = re.search(r"^name: ([a-z0-9-]+)$", front, re.M)
            require(name and name.group(1) == path.parent.name, str(rel))
            require(re.search(r"^description: .+", front, re.M), str(rel))
            count += 1
    require(not (root / "plugins/devforgeai").exists(), "retired shared plugin source still exists")
    core = ("devforge-brainstorm", "devforge-project-expert-creator", "devforge-develop", "devforge-review")
    requirements = {}
    for provider in ("claude", "codex"):
        plugin = root / f"providers/{provider}/plugins/devforgeai"
        manifest = plugin / f".{provider}-plugin/plugin.json"
        require(json.loads(manifest.read_text())["name"] == "devforgeai", str(manifest))
        require(all((plugin / "skills" / name / "SKILL.md").is_file() for name in core),
                f"{provider} core skill missing")
        requirement = runtime_requirements.load_requirement(plugin, provider)
        if requirement is not None:
            runtime_requirements.load_plugin_hooks(plugin, provider)
            requirements[provider] = requirement
        for cases in (plugin / "skills").glob("*/evals/evals.json"):
            data = json.loads(cases.read_text())
            require(data.get("skill_name") == cases.parents[1].name, f"wrong eval skill: {cases}")
            for case in data["evals"]:
                for relative in case.get("files", []):
                    fixture = cases.parent / relative
                    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
                            f"fixture path escapes eval root: {relative}")
                    require(fixture.is_file(), f"missing fixture: {fixture}")
    result = {"status": "PASS", "skills": count, "scope": "structure only", "behavior": "NOT_EVALUATED"}
    if requirements:
        result.update(runtime_requirements=requirements, runtime_host="NOT_VERIFIED")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.framework.resolve()), indent=2))
    except (ValueError, OSError, AssertionError, KeyError) as error:
        parser.exit(2, f"BLOCKED: {error}\n")
