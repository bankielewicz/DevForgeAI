#!/usr/bin/env python3
"""
Validate design.md — Deterministic Quality Gate

Checks that design.md meets minimum completeness thresholds.
Returns JSON with pass/fail per check, warnings, and an overall status.
Exit code 0 = all hard checks pass. Exit code 1 = one or more hard checks failed.

Hard checks block the workflow. Warnings are reported but do not block.

Usage:
    python validate_design_md.py <design_md_path> [--expected-components=N] [--mode=story|standalone|extract]

Examples:
    python validate_design_md.py devforgeai/specs/ui/design.md
    python validate_design_md.py devforgeai/specs/ui/design.md --expected-components=30
"""

import json
import re
import sys
from pathlib import Path


# ── Hard Thresholds (block workflow) ────────────────────────────
MIN_AVG_LINES_PER_COMPONENT = 40
MIN_PROPS_PER_COMPONENT = 1
REQUIRED_COMPONENT_SECTIONS_YAML = ["visual:", "data:", "accessibility:"]
REQUIRED_COMPONENT_SECTIONS_MD = ["#### Visual", "#### Data", "#### Accessibility"]
MIN_TOKEN_NORMALIZATION_PCT = 70  # RESEARCH-003 R2: Hard gate (not warning)

# ── Soft Thresholds (warn only) ─────────────────────────────────
WARN_MIN_STATES = 2              # default + 1 interactive
WARN_MIN_CONTENT_ELEMENTS = 2
WARN_MIN_DATA_CONTEXT_LINES = 20
WARN_MIN_GLOBAL_ACCESSIBILITY_LINES = 10

SCHEMA_1_1_METADATA = (
    "schema_version", "document_type", "project", "created", "updated",
    "source_skill", "source_mode", "mode", "platform", "story_id", "epic_id",
)
SCHEMA_1_1_GROUPS = (
    "design_intent", "tokens", "components", "layouts", "interactions",
    "animations", "accessibility", "data_context",
)
VALID_MODES = {"story", "standalone", "extract"}
VALID_PLATFORMS = {"web", "gui", "tui"}


def read_file(path: str) -> str:
    """Read file content, exit with error if not found."""
    p = Path(path)
    if not p.exists():
        print(json.dumps({
            "status": "ERROR",
            "error": f"File not found: {path}",
            "checks": {},
            "warnings": {}
        }, indent=2))
        sys.exit(1)
    return p.read_text(encoding="utf-8")


def find_component_blocks(content: str) -> list:
    """
    Split design.md into per-component text blocks.
    Supports TWO formats:
      - YAML:     '  - id: "COMP-NNN"' (old format)
      - Markdown: '### COMP-NNN: ComponentName' (new format)
    Returns list of {"id": "COMP-NNN", "text": "...", "format": "yaml"|"markdown"}
    """
    # Try YAML format first
    pattern_yaml = re.compile(r'^  - id: "COMP-\d{3}"', re.MULTILINE)
    starts_yaml = [m.start() for m in pattern_yaml.finditer(content)]

    # Try Markdown format
    pattern_md = re.compile(r'^### COMP-\d{3,4}:', re.MULTILINE)
    starts_md = [m.start() for m in pattern_md.finditer(content)]

    # Use whichever format found components (prefer the one with more matches)
    if len(starts_yaml) >= len(starts_md) and starts_yaml:
        starts = starts_yaml
        fmt = "yaml"
        id_extractor = lambda text: re.search(r'"(COMP-\d{3})"', text)
        section_end_pattern = re.compile(r'^# =+', re.MULTILINE)
    elif starts_md:
        starts = starts_md
        fmt = "markdown"
        id_extractor = lambda text: re.search(r'(COMP-\d{3,4})', text)
        # Markdown components end at next ### COMP- or next ## section header
        section_end_pattern = re.compile(r'^## [A-Z]', re.MULTILINE)
    else:
        return []

    # Find end of component inventory
    inventory_end = len(content)
    for m in section_end_pattern.finditer(content):
        if m.start() > starts[-1]:
            inventory_end = m.start()
            break

    blocks = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else inventory_end
        block_text = content[start:end]
        id_match = id_extractor(block_text)
        comp_id = id_match.group(1) if id_match else f"UNKNOWN-{i}"
        blocks.append({"id": comp_id, "text": block_text, "format": fmt})

    return blocks


def count_lines(text: str) -> int:
    """Count non-empty, non-pure-separator lines. Includes markdown table rows."""
    return sum(
        1 for line in text.splitlines()
        if line.strip()
        and not line.strip().startswith("# ")  # Skip markdown H1/comments but keep ### and ####
        and not re.match(r'^[|\-\s:]+$', line.strip())  # Skip table separator rows (|---|---|)
    )


def check_component_sections(block: dict) -> list:
    """Check that a component block contains all required sections.
    Handles both YAML format (visual:, data:, accessibility:) and
    Markdown format (#### Visual, #### Data, #### Accessibility).
    """
    fmt = block.get("format", "yaml")
    text = block["text"]
    missing = []

    if fmt == "markdown":
        for section in REQUIRED_COMPONENT_SECTIONS_MD:
            if section not in text:
                missing.append(section.replace("#### ", "").lower())
    else:
        for section in REQUIRED_COMPONENT_SECTIONS_YAML:
            if section not in text:
                missing.append(section.rstrip(":"))

    return missing


def count_props(block_text: str) -> int:
    """Count props entries. Handles YAML ('- name:' under props:) and Markdown table formats."""
    # YAML format: count "- name:" lines under props: section
    in_props = False
    props_indent = None
    yaml_count = 0

    for line in block_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if stripped == "props:" or stripped.startswith("props:"):
            in_props = True
            props_indent = indent
            continue
        if in_props:
            if indent <= props_indent and stripped:
                in_props = False
                continue
            if stripped.startswith("- name:"):
                yaml_count += 1

    if yaml_count > 0:
        return yaml_count

    # Markdown format: look for props row in #### Data table
    # Format: "| props | activePersona: string; currentPage: string; onNavigate: callback |"
    for line in block_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("| props") or stripped.startswith("|props"):
            cells = stripped.split("|")
            if len(cells) >= 3:
                props_cell = cells[2].strip()
                if not props_cell or props_cell in ("—", "-", "none", "N/A"):
                    return 0
                # Count semicolons as separators
                return props_cell.count(";") + 1

    return 0


def count_states(block_text: str) -> int:
    """
    Count state entries under 'states:'.
    State names are direct children of states: (e.g., default:, hover:, focused:).
    Skips nested sub-keys like description:, visual_overrides:, and their children.
    """
    in_states = False
    states_indent = None
    count = 0

    for line in block_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # Enter states section
        if stripped == "states:" or stripped.startswith("states:"):
            in_states = True
            states_indent = indent
            continue

        if in_states:
            # Exit: line at same or lower indent than states:
            if indent <= states_indent and stripped:
                in_states = False
                continue

            # State name = direct child of states: (indent = states_indent + 2..6)
            # Must be "word:" format (not "- item" list syntax)
            if (states_indent < indent <= states_indent + 6
                    and ":" in stripped
                    and not stripped.startswith("-")):
                key = stripped.split(":")[0].strip()
                # State names are like: default, hover, focused, active, disabled, etc.
                # Skip known sub-keys that appear inside a state definition
                if key not in ("description", "visual_overrides", "background",
                               "border_color", "shadow", "cursor", "transform",
                               "opacity", "pointer_events", "outline", "ring",
                               "color", "display", "animation", "font_weight",
                               "border_left_color", "sidebar_width",
                               "sidebar_transform", "overlay_visible"):
                    count += 1

    return count


def count_content_elements(block_text: str) -> int:
    """Count content elements (lines with '- element:')."""
    return sum(
        1 for line in block_text.splitlines()
        if line.strip().startswith("- element:")
    )


def has_section(block_text: str, section_name: str) -> bool:
    """Check if a section key exists in the block."""
    return f"{section_name}:" in block_text


def check_token_normalization(blocks: list) -> tuple:
    """
    Check that component visual values use semantic token references
    (e.g., 'colors.surface', 'spacing.md') rather than raw CSS values
    (e.g., '#1a2b3c', 'rgba(...)', '16px').

    Promotes token normalization from a soft warning to a hard gate.

    Research evidence:
    - SpecifyUI: 14.4% higher structural fidelity with token constraints
      (Source: arxiv.org/html/2509.07334v1)
    - Pandya: CSS variable audit enforcement prevents LLM hallucination
      (Source: hvpandya.com/llm-design-systems)

    Returns: (normalization_pct, raw_examples, total_inspected)
    """
    # Token reference pattern: e.g., colors.surface, spacing.md, borders.radius.lg
    TOKEN_REF = re.compile(
        r'\b(?:colors|spacing|typography|borders|shadows|motion|z_index)\.\w+'
    )

    # Raw value patterns that SHOULD be token references
    RAW_PATTERNS = [
        re.compile(r'#[0-9a-fA-F]{3,8}\b'),       # hex colors
        re.compile(r'rgba?\s*\([^)]+\)'),            # rgb/rgba
        re.compile(r'hsla?\s*\([^)]+\)'),            # hsl/hsla
    ]

    # Visual property keys to inspect (both YAML key: and Markdown table key)
    VISUAL_KEYS = {
        'background', 'color', 'border', 'border_color', 'border_radius',
        'shadow', 'padding', 'margin', 'gap', 'typography', 'ring',
        'backdrop_filter',
    }

    token_count = 0
    raw_count = 0
    raw_examples = []

    for block in blocks:
        comp_id = block["id"]
        fmt = block.get("format", "yaml")

        for line in block["text"].splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            key = None
            value = None

            if fmt == "yaml" and ':' in stripped and not stripped.startswith('-'):
                parts = stripped.split(':', 1)
                key = parts[0].strip().strip('"')
                value = parts[1].strip().strip('"').strip("'")
            elif fmt == "markdown" and stripped.startswith('|'):
                cells = [c.strip() for c in stripped.split('|')]
                cells = [c for c in cells if c]
                if len(cells) >= 2:
                    key = cells[0].strip().lower().replace(' ', '_')
                    value = cells[1].strip()

            if not key or not value or key not in VISUAL_KEYS:
                continue

            has_token = bool(TOKEN_REF.search(value))
            has_raw = any(p.search(value) for p in RAW_PATTERNS)

            if has_token and not has_raw:
                token_count += 1
            elif has_raw and not has_token:
                raw_count += 1
                if len(raw_examples) < 5:
                    raw_examples.append({
                        "component": comp_id,
                        "key": key,
                        "value": value[:80]
                    })
            elif has_token and has_raw:
                # Mixed value (e.g., "borders.width.default solid colors.border")
                # Contains tokens — count as normalized
                token_count += 1

    total = token_count + raw_count
    if total == 0:
        return 100.0, [], 0

    pct = round((token_count / total) * 100, 1)
    return pct, raw_examples, total


def find_section_lines(content: str, section_name: str) -> int:
    """
    Count non-empty lines in a top-level YAML section.
    A top-level section starts with a key at indent 0 (no leading spaces)
    and ends at the next top-level key, section comment, or document boundary.
    """
    lines = content.splitlines()
    in_section = False
    section_lines = 0

    for line in lines:
        raw_indent = len(line) - len(line.lstrip()) if line.strip() else 999

        if not in_section:
            # Match the section start: key at indent 0
            if raw_indent == 0 and line.strip().startswith(f"{section_name}:"):
                in_section = True
                continue
        else:
            stripped = line.strip()
            # Stop at: next top-level key (indent 0, word:), section comment, or ---
            if raw_indent == 0 and stripped:
                if (re.match(r'^[a-z_]+:', stripped)
                        or stripped.startswith("# =")
                        or stripped == "---"
                        or stripped == "```"):
                    break
            if stripped and not stripped.startswith("#"):
                section_lines += 1

    return section_lines


def _scalar(content: str, key: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(key)}\s*:\s*["\']?([^"\'\n#]+)', content, re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_schema_contract(content: str, mode: str | None) -> dict:
    """Validate schema-1.1 ordering/applicability while preserving 1.0 reads."""
    version = _scalar(content, "schema_version")
    if version == "1.0":
        return {"passed": True, "schema_version": "1.0", "errors": []}
    errors = []
    if version != "1.1":
        return {
            "passed": False,
            "schema_version": version,
            "errors": ["schema_version must be 1.0 or 1.1"],
        }
    if mode not in VALID_MODES:
        errors.append("schema 1.1 validation requires --mode=story|standalone|extract")

    top_level = [
        match.group(1)
        for match in re.finditer(r"^([a-z_]+)\s*:", content, re.MULTILINE)
    ]
    document_mode = _scalar(content, "mode")
    platform = _scalar(content, "platform")
    review_required = mode in {"story", "standalone"} and platform == "web"
    expected_sequence = [*SCHEMA_1_1_METADATA, *SCHEMA_1_1_GROUPS]
    if review_required:
        expected_sequence.append("design_review")
    contract_keys = set(expected_sequence) | {"design_review"}
    present_sequence = [key for key in top_level if key in contract_keys]

    for key in SCHEMA_1_1_METADATA + SCHEMA_1_1_GROUPS:
        if top_level.count(key) != 1:
            errors.append(f"schema 1.1 requires exactly one {key} group or metadata field")
    if present_sequence != expected_sequence:
        errors.append(
            "schema 1.1 metadata and applicable groups 1-10 are missing or out of order"
        )

    if document_mode not in VALID_MODES:
        errors.append("mode metadata must be story, standalone, or extract")
    elif mode in VALID_MODES and document_mode != mode:
        errors.append("document mode does not match --mode")
    if platform not in VALID_PLATFORMS:
        errors.append("platform metadata must be web, gui, or tui")

    review_count = top_level.count("design_review")
    if review_required and review_count != 1:
        errors.append("generated web story/standalone schema 1.1 requires design_review")
    if not review_required and review_count > 0:
        errors.append("design_review is inapplicable to GUI, TUI, or extract mode")
    if review_count == 1 and find_section_lines(content, "design_review") == 0:
        errors.append("design_review must be non-empty")
    return {"passed": not errors, "schema_version": "1.1", "errors": errors}


def validate(content: str, expected_components: int = 0, mode: str | None = None) -> dict:
    """Run all validation checks and return structured results."""
    checks = {}      # Hard checks — block on failure
    warnings = {}    # Soft checks — report only
    all_pass = True
    schema_contract = validate_schema_contract(content, mode)
    if schema_contract["schema_version"] == "1.1":
        checks["schema_1_1_contract"] = schema_contract
        if not schema_contract["passed"]:
            all_pass = False

    # ── Hard Check 1: Component count ──
    blocks = find_component_blocks(content)
    actual_count = len(blocks)
    threshold = expected_components if expected_components > 0 else 1
    passed = actual_count >= threshold
    checks["component_count"] = {
        "passed": passed,
        "expected": f">={threshold}",
        "actual": actual_count,
    }
    if not passed:
        all_pass = False

    if actual_count == 0:
        for name in ["avg_lines_per_component", "required_sections", "min_props"]:
            checks[name] = {"passed": False, "detail": "No components found"}
        return {"status": "FAILED", "checks": checks, "warnings": {}}

    # ── Hard Check 2: Average lines per component ──
    line_counts = [count_lines(b["text"]) for b in blocks]
    avg_lines = sum(line_counts) / len(line_counts)
    passed = avg_lines >= MIN_AVG_LINES_PER_COMPONENT
    checks["avg_lines_per_component"] = {
        "passed": passed,
        "expected": f">={MIN_AVG_LINES_PER_COMPONENT}",
        "actual": round(avg_lines, 1),
    }
    if not passed:
        all_pass = False
        thin = [
            {"id": blocks[i]["id"], "lines": line_counts[i]}
            for i in range(len(blocks))
            if line_counts[i] < MIN_AVG_LINES_PER_COMPONENT
        ]
        checks["avg_lines_per_component"]["thin_components"] = thin[:10]

    # ── Hard Check 3: Required sections (visual, data, accessibility) ──
    missing_sections = {}
    for block in blocks:
        missing = check_component_sections(block)
        if missing:
            missing_sections[block["id"]] = missing
    passed = len(missing_sections) == 0
    checks["required_sections"] = {
        "passed": passed,
        "expected": "all components have visual, data, accessibility",
        "actual": f"{len(missing_sections)} components missing sections",
    }
    if not passed:
        all_pass = False
        checks["required_sections"]["failures"] = missing_sections

    # ── Hard Check 4: Minimum props per component ──
    low_props = {}
    for block in blocks:
        prop_count = count_props(block["text"])
        if prop_count < MIN_PROPS_PER_COMPONENT:
            low_props[block["id"]] = prop_count
    passed = len(low_props) == 0
    checks["min_props"] = {
        "passed": passed,
        "expected": f">={MIN_PROPS_PER_COMPONENT} props per component",
        "actual": f"{len(low_props)} components below threshold",
    }
    if not passed:
        all_pass = False
        checks["min_props"]["failures"] = low_props

    # ── Hard Check 5: Token normalization (RESEARCH-003 R2) ──
    # Enforces that visual values use semantic token references, not raw CSS.
    # SpecifyUI: 14.4% higher structural fidelity (arxiv.org/html/2509.07334v1)
    # Pandya: CSS variable audit prevents LLM hallucination (hvpandya.com/llm-design-systems)
    norm_pct, raw_examples, norm_total = check_token_normalization(blocks)
    passed = norm_pct >= MIN_TOKEN_NORMALIZATION_PCT
    checks["token_normalization"] = {
        "passed": passed,
        "expected": f">={MIN_TOKEN_NORMALIZATION_PCT}%",
        "actual": f"{norm_pct}%",
        "inspected_values": norm_total,
    }
    if not passed:
        all_pass = False
        if raw_examples:
            checks["token_normalization"]["raw_value_examples"] = raw_examples

    # ── Warning 1: States per component ──
    low_states = {}
    for block in blocks:
        state_count = count_states(block["text"])
        if state_count < WARN_MIN_STATES:
            low_states[block["id"]] = state_count
    warnings["states_per_component"] = {
        "threshold": f">={WARN_MIN_STATES}",
        "below_threshold": len(low_states),
        "total_components": actual_count,
    }
    if low_states:
        warnings["states_per_component"]["components"] = low_states

    # ── Warning 2: Content elements per component ──
    low_content = {}
    for block in blocks:
        elem_count = count_content_elements(block["text"])
        if elem_count < WARN_MIN_CONTENT_ELEMENTS:
            low_content[block["id"]] = elem_count
    warnings["content_elements"] = {
        "threshold": f">={WARN_MIN_CONTENT_ELEMENTS}",
        "below_threshold": len(low_content),
        "total_components": actual_count,
    }
    if low_content:
        warnings["content_elements"]["components"] = low_content

    # ── Warning 3: Data Context section size ──
    data_ctx_lines = find_section_lines(content, "data_context")
    warnings["data_context_lines"] = {
        "threshold": f">={WARN_MIN_DATA_CONTEXT_LINES}",
        "actual": data_ctx_lines,
        "passed": data_ctx_lines >= WARN_MIN_DATA_CONTEXT_LINES,
    }

    # ── Warning 4: Global Accessibility section size ──
    acc_lines = find_section_lines(content, "accessibility")
    warnings["global_accessibility_lines"] = {
        "threshold": f">={WARN_MIN_GLOBAL_ACCESSIBILITY_LINES}",
        "actual": acc_lines,
        "passed": acc_lines >= WARN_MIN_GLOBAL_ACCESSIBILITY_LINES,
    }

    return {
        "status": "PASSED" if all_pass else "FAILED",
        "checks": checks,
        "warnings": warnings,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_design_md.py <design_md_path> [--expected-components=N] [--mode=story|standalone|extract]")
        sys.exit(1)

    design_path = sys.argv[1]
    expected_components = 0
    mode = None

    for arg in sys.argv[2:]:
        if arg.startswith("--expected-components="):
            try:
                expected_components = int(arg.split("=")[1])
            except ValueError:
                print(f"Warning: Invalid --expected-components value: {arg}")
        elif arg.startswith("--mode="):
            candidate = arg.split("=", 1)[1]
            if candidate not in VALID_MODES:
                print(f"ERROR: Invalid --mode value: {candidate}")
                sys.exit(1)
            mode = candidate

    content = read_file(design_path)
    result = validate(content, expected_components, mode)

    output = json.dumps(result, indent=2)
    print(output)

    # Summary
    hard_total = len(result["checks"])
    hard_passed = sum(1 for c in result["checks"].values() if c.get("passed", False))
    hard_failed = hard_total - hard_passed
    warn_count = sum(
        1 for w in result["warnings"].values()
        if not w.get("passed", True) or w.get("below_threshold", 0) > 0
    )

    status_icon = "✅" if result["status"] == "PASSED" else "❌"
    print(f"\n{status_icon} {result['status']}: {hard_passed}/{hard_total} hard checks passed, {hard_failed} failed, {warn_count} warnings")

    sys.exit(0 if result["status"] == "PASSED" else 1)


if __name__ == "__main__":
    main()
