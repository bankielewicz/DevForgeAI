#!/usr/bin/env python3
"""Deterministic anti-slop lint for self-contained web artifacts.

Adapted from Open Design ``apps/daemon/src/lint-artifact.ts`` at commit
10adca2cbf47be61829c74e21158ecccddf4c1cd. See references/ATTRIBUTIONS.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable


PURPLE_HEXES = (
    "#a855f7", "#9333ea", "#7c3aed", "#6d28d9", "#581c87",
    "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#ede9fe",
    "#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#312e81",
    "#818cf8", "#a5b4fc", "#c7d2fe", "#e0e7ff", "#eef2ff",
)
BLUE_HEXES = (
    "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af", "#1e3a8a",
    "#60a5fa", "#93c5fd", "#bfdbfe", "#0ea5e9", "#0284c7",
    "#0369a1", "#38bdf8", "#7dd3fc",
)
CYAN_HEXES = (
    "#06b6d4", "#0891b2", "#0e7490", "#155e75", "#164e63",
    "#22d3ee", "#67e8f9", "#a5f3fc",
)
AI_DEFAULT_INDIGO = (
    "#6366f1", "#4f46e5", "#4338ca", "#3730a3", "#8b5cf6", "#7c3aed", "#a855f7",
)
SLOP_EMOJI = (
    "✨", "🚀", "🎯", "⚡", "🔥", "💡", "📈", "🎨", "🛡️", "🌟",
    "💪", "🎉", "👋", "🙌", "✅", "⭐", "🏆",
)
INVENTED_METRICS = (
    re.compile(r"\b10×\s+(faster|better|easier)\b", re.I),
    re.compile(r"\b100×\s+(faster|better)\b", re.I),
    re.compile(r"\b99\.\d+%\s+uptime\b", re.I),
    re.compile(r"\bzero[- ]downtime\b", re.I),
    re.compile(r"\b3×\s+more\s+(productive|efficient)\b", re.I),
)
FILLER = (
    re.compile(r"\bfeature\s+(one|two|three|1|2|3)\b", re.I),
    re.compile(r"\blorem\s+ipsum\b", re.I),
    re.compile(r"\bdolor\s+sit\s+amet\b", re.I),
    re.compile(r"\bplaceholder\s+text\b", re.I),
    re.compile(r"\bsample\s+content\b", re.I),
)
GLOBAL_THEME_ATTRIBUTES = {"data-theme", "data-color-scheme", "data-mode"}
ROOT_FONT_PX = 16.0


def _comment_blind(text: str) -> str:
    def blank(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    return re.sub(r"<!--[\s\S]*?-->|/\*[\s\S]*?\*/", blank, text)


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, max(offset, 0)) + 1


def _literal(value: str) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    return compact if len(compact) <= 200 else compact[:197] + "…"


def _finding(
    text: str, finding_id: str, severity: str, match: re.Match[str] | None,
    message: str, fix: str, literal: str | None = None,
) -> dict[str, object]:
    found = literal if literal is not None else (match.group(0) if match else "")
    offset = match.start() if match else 0
    return {
        "id": finding_id,
        "severity": severity,
        "line": _line(text, offset),
        "literal": _literal(found),
        "message": message,
        "fix": fix,
    }


def _is_global_theme_selector(selector: str) -> bool:
    parts = [part.strip() for part in selector.split(",") if part.strip()]
    if not parts:
        return False
    for part in parts:
        tagged = re.fullmatch(r"(?::root|html|body)(?:\[([A-Za-z-]+)(?:[*^$|~]?=[^\]]*)?\])?", part)
        if tagged:
            attribute = tagged.group(1)
            if attribute and attribute.lower() not in GLOBAL_THEME_ATTRIBUTES:
                return False
            continue
        bare = re.fullmatch(r"\[([A-Za-z-]+)(?:[*^$|~]?=[^\]]*)?\]", part)
        if not bare or bare.group(1).lower() not in GLOBAL_THEME_ATTRIBUTES:
            return False
    return True


def _strip_legitimate_token_blocks(text: str) -> str:
    def clean_style(style_match: re.Match[str]) -> str:
        css = _comment_blind(style_match.group(2))

        def clean_rule(rule: re.Match[str]) -> str:
            selector, body = rule.group(1).strip(), rule.group(2)
            if not _is_global_theme_selector(selector):
                return rule.group(0)
            declarations = [part.strip() for part in body.split(";") if part.strip()]
            if not declarations:
                return rule.group(0)
            if not all(re.match(r"^--[\w-]+\s*:", item) or re.match(r"^color-scheme\s*:", item, re.I) for item in declarations):
                return rule.group(0)
            for declaration in declarations:
                token = re.match(r"^(--[\w-]+)\s*:\s*(.+)$", declaration)
                if not token or token.group(1).lower() == "--accent":
                    continue
                if any(color in token.group(2).lower() for color in AI_DEFAULT_INDIGO):
                    return rule.group(0)
            return ""

        css = re.sub(r"([^{}]*)\{([^{}]*)\}", clean_rule, css)
        return style_match.group(1) + css + style_match.group(3)

    return re.sub(r"(<style[^>]*>)([\s\S]*?)(</style>)", clean_style, text, flags=re.I)


def _parse_declarations(body: str) -> list[tuple[str, str]]:
    declarations = []
    for raw in body.split(";"):
        if ":" not in raw:
            continue
        prop, value = raw.split(":", 1)
        prop = prop.strip().lower()
        value = value.strip()
        if prop and value and not prop.startswith("--"):
            declarations.append((prop, value))
    return declarations


def _last(declarations: list[tuple[str, str]], prop: str) -> str | None:
    for name, value in reversed(declarations):
        if name == prop:
            return value
    return None


def _theme_token_maps(text: str) -> list[dict[str, str]]:
    scopes: list[tuple[bool, set[str], dict[str, str]]] = []
    for style in re.finditer(r"<style[^>]*>([\s\S]*?)</style>", text, re.I):
        css = _comment_blind(style.group(1))
        for rule in re.finditer(r"([^{}]*)\{([^{}]*)\}", css):
            selector = rule.group(1).strip()
            if not _is_global_theme_selector(selector):
                continue
            parts = [part.strip() for part in selector.split(",") if part.strip()]
            default = any(part in {":root", "html", "body"} for part in parts)
            variants = {part for part in parts if part not in {":root", "html", "body"}}
            tokens: dict[str, str] = {}
            for declaration in rule.group(2).split(";"):
                token = re.match(r"\s*(--[\w-]+)\s*:\s*(.+)\s*$", declaration)
                if token:
                    tokens[token.group(1)] = token.group(2).strip()
            if tokens:
                scopes.append((default, variants, tokens))
    keys = {"default"}
    for _, variants, _ in scopes:
        keys.update(variants)
    maps = {key: {} for key in keys}
    for default, variants, tokens in scopes:
        targets = maps.values() if default else (maps[key] for key in variants)
        for target in targets:
            target.update(tokens)
    return list(maps.values()) or [{}]


def _resolve_vars(body: str, tokens: dict[str, str]) -> str:
    result = body
    pattern = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)")
    for _ in range(4):
        next_value = pattern.sub(
            lambda match: tokens.get(match.group(1), (match.group(2) or match.group(0)).strip()),
            result,
        )
        if next_value == result:
            break
        result = next_value
    return result


def _tracking_adequate(body: str, token_maps: Iterable[dict[str, str]]) -> bool:
    for tokens in token_maps:
        declarations = _parse_declarations(_resolve_vars(body, tokens))
        spacing = _last(declarations, "letter-spacing")
        if spacing is None:
            return False
        match = re.match(r"^(-?\d*\.?\d+)\s*(em|px|rem)\b", spacing, re.I)
        if not match:
            return False
        value, unit = float(match.group(1)), match.group(2).lower()
        if unit == "em":
            if value < 0.06:
                return False
            continue
        tracking_px = value * ROOT_FONT_PX if unit == "rem" else value
        font_size = _last(declarations, "font-size")
        if font_size is None:
            if tracking_px < 1:
                return False
            continue
        size_match = re.match(r"^(-?\d*\.?\d+)\s*(px|rem)\b", font_size, re.I)
        if not size_match:
            return False
        size_px = float(size_match.group(1)) * (ROOT_FONT_PX if size_match.group(2).lower() == "rem" else 1)
        if size_px <= 0 or tracking_px < size_px * 0.06:
            return False
    return True


def lint_artifact(raw: str) -> dict[str, list[dict[str, object]]]:
    out: dict[str, list[dict[str, object]]] = {"p0": [], "p1": [], "p2": []}
    html = _comment_blind(raw)

    gradients = list(re.finditer(r"linear-gradient\([^)]*\)", html, re.I))
    purple = next(
        (match for match in gradients if any(color in match.group(0).lower() for color in PURPLE_HEXES) or re.search(r"\b(purple|violet)\b", match.group(0), re.I)),
        None,
    )
    if purple:
        out["p0"].append(_finding(raw, "purple-gradient", "P0", purple, "Violet/purple gradient is an AI-default trope.", "Use a flat design-token surface or one intentional accent intensity."))
    else:
        trust = next(
            (match for match in gradients if (any(color in match.group(0).lower() for color in BLUE_HEXES) or re.search(r"\bblue\b", match.group(0), re.I)) and (any(color in match.group(0).lower() for color in CYAN_HEXES) or re.search(r"\bcyan\b", match.group(0), re.I))),
            None,
        )
        if trust:
            out["p0"].append(_finding(raw, "trust-gradient", "P0", trust, "Blue-to-cyan trust gradient is a generic SaaS trope.", "Use a flat design-token color."))

    if not purple:
        indigo_scope = _strip_legitimate_token_blocks(html)
        match = next((re.search(re.escape(color), indigo_scope, re.I) for color in AI_DEFAULT_INDIGO if re.search(re.escape(color), indigo_scope, re.I)), None)
        if match:
            out["p0"].append(_finding(raw, "ai-default-indigo", "P0", match, "Default LLM indigo is hardcoded outside the declared active accent token.", "Use var(--accent); declare intentional brand indigo only as the global --accent token."))

    for emoji in SLOP_EMOJI:
        match = re.search(rf"<(?:h[1-6]|button|li|span class=[\"'][^\"']*icon[^\"']*[\"'])[^>]*>[^<]*{re.escape(emoji)}", html, re.I)
        if match:
            out["p0"].append(_finding(raw, "emoji-icon", "P0", match, f"Emoji {emoji} is used as a UI icon.", "Replace it with a small inline currentColor SVG or remove it."))
            break

    match = re.search(r"\.[a-z-]+\s*\{[^}]*border-left\s*:\s*\d+px\s+solid\s+[^;]+;[^}]*border-radius\s*:\s*[1-9]", html, re.I)
    if match:
        out["p0"].append(_finding(raw, "left-accent-card", "P0", match, "Rounded card with a colored left border is a canonical AI-card trope.", "Remove the left accent or the rounding; use a hairline border system."))

    match = re.search(r"(?:h1|h2|h3|\.h-?(?:hero|xl|lg|md))[^{}]*\{[^}]*font-family\s*:\s*[\"']?(?:Inter|Roboto|Arial|-apple-system|system-ui|SF\s+Pro)", html, re.I)
    if match:
        out["p0"].append(_finding(raw, "sans-display", "P0", match, "A heading overrides the bound display face with generic system sans.", "Use var(--font-display) unless the pinned direction explicitly selects utility sans."))

    for pattern in INVENTED_METRICS:
        match = pattern.search(html)
        if match:
            out["p0"].append(_finding(raw, "invented-metric", "P0", match, "Unverified business metric detected.", "Remove it or use a clearly labelled placeholder until supplied by the user."))
            break
    for pattern in FILLER:
        match = pattern.search(html)
        if match:
            out["p0"].append(_finding(raw, "filler-copy", "P0", match, "Generic filler copy detected.", "Use brief-specific copy or a clearly labelled placeholder."))
            break
    match = re.search(r"\.scrollIntoView\s*\(", html)
    if match:
        out["p0"].append(_finding(raw, "scroll-into-view", "P0", match, "Element.scrollIntoView can break iframe previews.", "Call scrollTo on the actual scroller."))

    token_maps = _theme_token_maps(html)
    caps_found = False
    for style in re.finditer(r"<style[^>]*>([\s\S]*?)</style>", html, re.I):
        css = style.group(1)
        for rule in re.finditer(r"([^{}]*)\{([^{}]*text-transform\s*:\s*uppercase[^{}]*)\}", css, re.I):
            if not _tracking_adequate(rule.group(2), token_maps):
                out["p1"].append(_finding(raw, "all-caps-no-tracking", "P1", rule, "Uppercase text lacks letter-spacing of at least 0.06em.", "Add letter-spacing: 0.08em to the same rule."))
                caps_found = True
                break
        if caps_found:
            break
    if not caps_found:
        for inline in re.finditer(r"(?:^|\s)style\s*=\s*([\"'])([\s\S]*?)\1", html, re.I):
            if re.search(r"text-transform\s*:\s*uppercase", inline.group(2), re.I) and not _tracking_adequate(inline.group(2), token_maps):
                out["p1"].append(_finding(raw, "all-caps-no-tracking", "P1", inline, "Inline uppercase text lacks letter-spacing of at least 0.06em.", "Add letter-spacing: 0.08em to the same style."))
                break

    match = re.search(r"<img[^>]+src=[\"']https?://(?:images\.unsplash\.com|placehold\.co|placekitten\.com|via\.placeholder\.com|picsum\.photos|loremflickr\.com)", html, re.I)
    if match:
        out["p1"].append(_finding(raw, "external-image", "P1", match, "External placeholder image CDN detected.", "Use a local or embedded asset."))

    style = re.search(r"<style[^>]*>([\s\S]*?)</style>", html, re.I)
    if style:
        without_root = re.sub(r":root\s*\{[^}]*\}", "", style.group(1))
        hexes = list(re.finditer(r"#[0-9a-fA-F]{3,8}\b", without_root))
        if len(hexes) > 12:
            out["p1"].append(_finding(raw, "raw-hex", "P1", hexes[0], f"{len(hexes)} raw hex values occur outside :root.", "Move colors into semantic :root tokens and reference them with var().", " ".join(match.group(0) for match in hexes[:6])))

    body = re.sub(r"<style[\s\S]*?</style>", "", html, flags=re.I)
    accent_matches = list(re.finditer(r"var\(--accent\)", body))
    if len(accent_matches) > 6:
        out["p1"].append(_finding(raw, "accent-overuse", "P1", accent_matches[0], f"Source approximation counted {len(accent_matches)} inline var(--accent) references; this is not a rendered visibility measurement.", "Reserve accent for one or two focal uses per screen."))

    sections = list(re.finditer(r"<section\b[^>]*>", html, re.I))
    untagged = [match for match in sections if not re.search(r"data-od-id\s*=|data-screen-label\s*=", match.group(0))]
    if untagged:
        out["p2"].append(_finding(raw, "missing-section-anchor", "P2", untagged[0], f"{len(untagged)} of {len(sections)} sections lack a comment-mode anchor.", "Add data-od-id or data-screen-label to every top-level section."))

    slides = list(re.finditer(r"<section\s+class\s*=\s*[\"'][^\"']*\bslide\b[^\"']*[\"']", html, re.I))
    if slides:
        missing_theme = [match for match in slides if not re.search(r"\b(light|dark|hero\s+light|hero\s+dark)\b", match.group(0))]
        if missing_theme:
            out["p0"].append(_finding(raw, "slide-theme-missing", "P0", missing_theme[0], f"{len(missing_theme)} slides lack a theme class.", "Add exactly one light, dark, hero light, or hero dark class."))
        themes = []
        for slide in slides:
            value = slide.group(0)
            themes.append("D" if re.search(r"\bdark\b", value) else "L" if re.search(r"\blight\b", value) else "?")
        for index in range(max(0, len(themes) - 2)):
            if themes[index] != "?" and len(set(themes[index:index + 3])) == 1:
                out["p1"].append(_finding(raw, "slide-rhythm", "P1", slides[index], "Three same-theme slides appear consecutively.", "Alternate the middle slide theme."))
                break

    motion = re.search(r"(?:^|[;{])\s*(?:transition(?:-[\w-]+)?|animation(?:-[\w-]+)?)\s*:", html, re.I)
    if motion and not re.search(r"prefers-reduced-motion\s*:\s*reduce", html, re.I):
        out["p2"].append(_finding(raw, "missing-reduced-motion", "P2", motion, "Motion declarations exist without a prefers-reduced-motion override.", "Add a reduce media query that disables or minimizes motion."))

    return out


def _payload(path: Path, data: bytes, findings: dict[str, list[dict[str, object]]]) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "artifact_sha256": hashlib.sha256(data).hexdigest(),
        "p0": findings["p0"],
        "p1": findings["p1"],
        "p2": findings["p2"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--format", choices=["json"], default=None)
    args = parser.parse_args(argv)
    path = Path(args.artifact)
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
        if not re.search(r"<[/!A-Za-z][^>]*>", text):
            raise ValueError("input is not an HTML artifact")
        findings = lint_artifact(text)
        payload = _payload(path, data, findings)
    except (OSError, UnicodeError, ValueError) as exc:
        if args.format == "json":
            print(json.dumps({"error": str(exc)}, sort_keys=True, separators=(",", ":")))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, sort_keys=False, separators=(",", ":")))
    else:
        for severity in ("p0", "p1", "p2"):
            for finding in findings[severity]:
                print(
                    f"[{finding['severity']}] {finding['id']} line {finding['line']}: "
                    f"{finding['message']} Fix: {finding['fix']}",
                    file=sys.stderr,
                )
    return 2 if findings["p0"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
