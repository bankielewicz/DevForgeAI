#!/usr/bin/env python3
"""
Skill Initializer - Creates a new Claude Code skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--resources scripts,references,assets] [--examples]
                  [--allowed-tools Read,Write,Edit] [--model opus] [--effort High]

The parent directory is whatever the current request selects — the project's .claude/skills,
a development tree the project declares, or a staging parent whose files are copied into an
authoring candidate. This helper has no default; the caller resolves the destination.

Examples:
    init_skill.py my-new-skill --path .claude/skills
    init_skill.py my-new-skill --path .claude/skills --resources scripts,references
    init_skill.py my-api-helper --path skills/staging --resources scripts --examples
    init_skill.py my-skill --path .claude/skills --allowed-tools Read,Grep,Glob
"""

import argparse
import re
import sys
from pathlib import Path

from authoring import safe

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: Describe what this skill does AND the contexts that should trigger it.]"
{optional_frontmatter}---

# {skill_title}

[TODO: Add the task-specific guidance Claude needs. Reference supporting files only when they are relevant.]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference for {skill_title}

Replace this placeholder with maintained, task-specific details that Claude
would not reliably know, such as operational constraints, local schemas, or
fragile integration behavior.

Delete this file if no supported workflow needs it.
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def normalize_skill_name(skill_name):
    """Normalize a skill name to lowercase hyphen-case."""
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def parse_resources(raw_resources):
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        allowed = ", ".join(sorted(ALLOWED_RESOURCES))
        print(f"[ERROR] Unknown resource type(s): {', '.join(invalid)}")
        print(f"   Allowed: {allowed}")
        sys.exit(1)
    deduped = []
    seen = set()
    for resource in resources:
        if resource not in seen:
            deduped.append(resource)
            seen.add(resource)
    return deduped


def parse_allowed_tools(raw_tools):
    """Split a comma-separated allowed-tools list, preserving Bash(...) entries intact."""
    if not raw_tools:
        return []
    tools, depth, current = [], 0, ""
    for char in raw_tools:
        if char == "," and depth == 0:
            tools.append(current.strip())
            current = ""
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        current += char
    tools.append(current.strip())
    return [tool for tool in tools if tool]


def build_frontmatter(allowed_tools, model, effort):
    """Emit only the optional keys actually supplied; never invent a policy value."""
    lines = []
    if allowed_tools:
        lines.append("allowed-tools:")
        lines.extend(f"  - {tool}" for tool in allowed_tools)
    if model:
        lines.append(f"model: {model}")
    if effort:
        lines.append(f"effort: {effort}")
    return "".join(f"{line}\n" for line in lines)


def create_resource_dirs(
    skill_dir, skill_name, skill_title, resources, include_examples
):
    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        if resource == "scripts":
            if include_examples:
                example_script = resource_dir / "example.py"
                example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
                example_script.chmod(0o755)
                print("[OK] Created scripts/example.py")
            else:
                print("[OK] Created scripts/")
        elif resource == "references":
            if include_examples:
                example_reference = resource_dir / "api_reference.md"
                example_reference.write_text(
                    EXAMPLE_REFERENCE.format(skill_title=skill_title)
                )
                print("[OK] Created references/api_reference.md")
            else:
                print("[OK] Created references/")
        elif resource == "assets":
            if include_examples:
                example_asset = resource_dir / "example_asset.txt"
                example_asset.write_text(EXAMPLE_ASSET)
                print("[OK] Created assets/example_asset.txt")
            else:
                print("[OK] Created assets/")


def init_skill(skill_name, path, resources, include_examples, allowed_tools, model, effort):
    """
    Initialize a new Claude Code skill directory with a template SKILL.md.

    Returns:
        Path to created skill directory, or None if error
    """
    try:
        skill_dir = safe(safe(path, write=True) / skill_name, write=True)
    except ValueError as e:
        print(f"[ERROR] Destination rejected: {e}")
        print("   Select a parent directory outside excluded boundaries, with no")
        print("   traversal segments and no links or junctions on the path.")
        return None

    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
        optional_frontmatter=build_frontmatter(allowed_tools, model, effort),
    )

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content)
        print("[OK] Created SKILL.md")
    except Exception as e:
        print(f"[ERROR] Error creating SKILL.md: {e}")
        return None

    if resources:
        try:
            create_resource_dirs(
                skill_dir, skill_name, skill_title, resources, include_examples
            )
        except Exception as e:
            print(f"[ERROR] Error creating resource directories: {e}")
            return None

    print(f"\n[OK] Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    if resources:
        if include_examples:
            print(
                "2. Customize or delete the example files in scripts/, references/, and assets/"
            )
        else:
            print("2. Add resources to scripts/, references/, and assets/ as needed")
    else:
        print(
            "2. Create resource directories only if needed (scripts/, references/, assets/)"
        )
    print("3. Narrow allowed-tools to the capabilities the skill actually needs")
    print("4. Complete authoring custody and return the manual validator request.")
    print("Validation and testing: NOT_PERFORMED. This helper does not run checks.")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Create a new Claude Code skill directory with a SKILL.md template.",
    )
    parser.add_argument("skill_name", help="Skill name (normalized to hyphen-case)")
    parser.add_argument("--path", required=True, help="Output directory for the skill")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated list: scripts,references,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Create example files inside the selected resource directories",
    )
    parser.add_argument(
        "--allowed-tools",
        default="",
        help="Comma-separated allowed-tools entries, e.g. Read,Grep,Bash(python:*)",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Model override; omit to inherit the configured session",
    )
    parser.add_argument(
        "--effort",
        default="",
        help="Effort override; omit to inherit the configured session",
    )
    args = parser.parse_args()

    raw_skill_name = args.skill_name
    skill_name = normalize_skill_name(raw_skill_name)
    if not skill_name:
        print("[ERROR] Skill name must include at least one letter or digit.")
        sys.exit(1)
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        print(
            f"[ERROR] Skill name '{skill_name}' is too long ({len(skill_name)} characters). "
            f"Maximum is {MAX_SKILL_NAME_LENGTH} characters."
        )
        sys.exit(1)
    if skill_name != raw_skill_name:
        print(f"Note: Normalized skill name from '{raw_skill_name}' to '{skill_name}'.")

    resources = parse_resources(args.resources)
    if args.examples and not resources:
        print("[ERROR] --examples requires --resources to be set.")
        sys.exit(1)

    allowed_tools = parse_allowed_tools(args.allowed_tools)
    path = args.path

    print(f"Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    if resources:
        print(f"   Resources: {', '.join(resources)}")
        if args.examples:
            print("   Examples: enabled")
    else:
        print("   Resources: none (create as needed)")
    if allowed_tools:
        print(f"   Allowed tools: {', '.join(allowed_tools)}")
    print()

    result = init_skill(
        skill_name, path, resources, args.examples, allowed_tools, args.model, args.effort
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
