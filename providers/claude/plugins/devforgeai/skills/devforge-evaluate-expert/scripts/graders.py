#!/usr/bin/env python3
"""Deterministic graders for authored skill-evaluation cases.

Each grader answers one narrow, byte-observable question about a candidate or an
output that a case named. Graders produce evidence, never a verdict:

  * every result is MATCH, MISMATCH or INDETERMINATE for one assertion;
  * nothing here aggregates assertions, cases or packages;
  * nothing here writes any file, executes candidate code, imports candidate
    modules, starts a subprocess or touches the network.

INDETERMINATE is a real answer and is used whenever a fact cannot be established
from the supported subset of an input format. It is never softened into MATCH
and never hardened into MISMATCH.

This module has no command interface on purpose. `run_cases.py` is the only
executable, so there is no second entry point that could be mistaken for a gate.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

MATCH = "MATCH"
MISMATCH = "MISMATCH"
INDETERMINATE = "INDETERMINATE"

MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_FRONTMATTER_BYTES = 128 * 1024
MAX_LINKS = 2048

# The synthetic transcript shape's consultation contract. An event counts as a
# consultation only when its `type` is one of these AND one of the identity
# fields below holds the target's exact name. Free-text fields are never read.
CONSULTATION_EVENT_TYPES = ("skill_loaded", "skill_read", "resource_read", "skill_consulted")
IDENTITY_FIELDS = ("skill", "resource", "loaded", "target")

# Top-level `key: value` in the restricted frontmatter subset.
KEY_LINE = re.compile(r"^([A-Za-z0-9_.-]+):[ \t]*(.*)$")
# Inline Markdown link or image with a non-nested destination.
INLINE_LINK = re.compile(r"!?\[(?:[^\[\]]*)\]\(([^()\s]*)\)")
# Representations this parser deliberately does not interpret.
REFERENCE_LINK = re.compile(r"\][ \t]*\[")
ENTITY = re.compile(r"&(?:#\d+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


class ReadLimit(Exception):
    """A bounded read could not be completed; the caller reports INDETERMINATE."""


def result(kind, observed, reason, evidence=None, blocks_case=False):
    return {
        "result": kind,
        "observed": observed,
        "reason": reason,
        "evidence": evidence,
        "blocks_case": blocks_case,
    }


def contained(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text(path: Path, budget) -> str:
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ReadLimit(f"file exceeds the {MAX_FILE_BYTES}-byte read bound")
    data = path.read_bytes()
    budget["files_read"] += 1
    budget["bytes_read"] += len(data)
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return data.decode("utf-8")


def resolve_in(root: Path, relative: str):
    """Resolve a case-supplied relative path inside root, or return None."""
    if not relative or Path(relative).is_absolute():
        return None
    candidate = (root / relative).resolve()
    return candidate if contained(candidate, root) else None


# --------------------------------------------------------------------------
# Restricted frontmatter reader (no PyYAML, no third-party parser)
# --------------------------------------------------------------------------


def fenced_lines(text: str) -> set[int]:
    """Return the 1-based line numbers that sit inside a fenced code block.

    Content inside a fence is illustrative. A grader that reads it as though it
    were the document's own data reports a fact the document does not state.
    """
    inside: set[int] = set()
    in_fence = False
    marker = ""
    for number, line in enumerate(text.split("\n"), 1):
        fence = FENCE.match(line)
        if fence:
            found = fence.group(1)
            if not in_fence:
                in_fence, marker = True, found[0]
            elif found[0] == marker:
                in_fence, marker = False, ""
            inside.add(number)
            continue
        if in_fence:
            inside.add(number)
    return inside


def read_frontmatter(text: str):
    """Return (status, fields, reason).

    status is one of:
      'parsed'      - a mapping of top-level scalars was read;
      'duplicate'   - a mapping was read but a top-level key repeats;
      'absent'      - no delimited frontmatter block is present;
      'non_mapping' - the root is definitely a sequence or a bare scalar, so no
                      mapping key can exist and the caller reports MISMATCH;
      'unsupported' - the block uses YAML the restricted subset does not
                      interpret, so the caller reports INDETERMINATE rather than
                      guessing a value or inventing a defect.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return "absent", {}, "the first line is not the --- frontmatter delimiter"

    closing = None
    scanned = 0
    for index in range(1, len(lines)):
        scanned += len(lines[index]) + 1
        if scanned > MAX_FRONTMATTER_BYTES:
            return "unsupported", {}, "frontmatter exceeds the supported size bound"
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return "absent", {}, "the closing --- frontmatter delimiter is missing"

    fields = {}
    duplicates = []
    first_content = True
    for raw in lines[1:closing]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1] in (" ", "\t"):
            return "unsupported", {}, "indented continuation or nested mapping is outside the supported scalar subset"
        match = KEY_LINE.match(raw)
        # The root's own shape is decidable from its first content line. A
        # sequence or a bare scalar there cannot carry a mapping key at all, so
        # "name and description are populated" is determinably false rather than
        # merely unreadable. A later unmatched line could still be a continuation
        # of a construct this subset does not parse, so it stays INDETERMINATE.
        if first_content and (raw.startswith("- ") or raw.strip() == "-"):
            return "non_mapping", {}, "the frontmatter root is a YAML sequence, which cannot carry mapping keys"
        if first_content and not match and ":" not in raw:
            return "non_mapping", {}, "the frontmatter root is a bare scalar, which cannot carry mapping keys"
        first_content = False
        if raw.startswith("- "):
            return "unsupported", {}, "a nested or trailing sequence entry is outside the supported scalar subset"
        if not match:
            return "unsupported", {}, f"line {raw!r} is not a supported top-level 'key: value' entry"
        key, value = match.group(1), match.group(2).strip()
        if key == "<<":
            return "unsupported", {}, "YAML merge keys are outside the supported subset"
        if value[:1] in ("|", ">", "&", "*", "[", "{", "!"):
            return "unsupported", {}, f"the value of {key!r} uses a YAML construct outside the supported scalar subset"
        if value == "":
            return "unsupported", {}, f"the value of {key!r} is empty, which may introduce a nested block"
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].strip()
        if key in fields:
            duplicates.append(key)
        fields[key] = value

    if duplicates:
        return "duplicate", fields, "duplicate top-level key(s): " + ", ".join(sorted(set(duplicates)))
    return "parsed", fields, "parsed with the restricted top-level scalar subset"


# --------------------------------------------------------------------------
# Graders
# --------------------------------------------------------------------------


def grade_frontmatter_present(root, args, budget, case):
    target = resolve_in(root, args.get("file", "SKILL.md"))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", f"{args.get('file', 'SKILL.md')} is not a readable file in the candidate")
    try:
        text = read_text(target, budget)
    except (ReadLimit, UnicodeError, OSError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read the file: {exc}", blocks_case=True)
    status, _, reason = read_frontmatter(text)
    evidence = {"path": str(target), "line": 1}
    if status == "absent":
        return result(MISMATCH, "absent", reason, evidence)
    return result(MATCH, "present", "opening and closing --- delimiters are present", evidence)


def grade_frontmatter_fields(root, args, budget, case):
    required = args.get("fields", ["name", "description"])
    target = resolve_in(root, args.get("file", "SKILL.md"))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", f"{args.get('file', 'SKILL.md')} is not a readable file in the candidate")
    try:
        text = read_text(target, budget)
    except (ReadLimit, UnicodeError, OSError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read the file: {exc}", blocks_case=True)
    status, fields, reason = read_frontmatter(text)
    evidence = {"path": str(target), "line": 1}
    if status == "absent":
        return result(MISMATCH, "absent", reason, evidence)
    if status == "non_mapping":
        return result(MISMATCH, "non-mapping-root", reason, evidence)
    if status == "unsupported":
        return result(
            INDETERMINATE,
            "unparsed",
            reason + "; a YAML parser is required and this grader does not use one",
            evidence,
        )
    if status == "duplicate":
        return result(MISMATCH, "duplicate-key", reason, evidence)
    missing = [name for name in required if not fields.get(name, "").strip()]
    if missing:
        return result(MISMATCH, "incomplete", "missing or empty field(s): " + ", ".join(missing), evidence)
    return result(MATCH, ",".join(sorted(fields)), "every required field is a populated scalar", evidence)


def grade_name_folder_relation(root, args, budget, case):
    """Record the frontmatter name and the folder name.

    Equality is asserted only when the case sets expect_equal. Claude sets the
    slash command from the directory for a personal or project skill and from
    `name` for a plugin skill, so a difference is not a provider defect. The
    DevForgeAI packages keep them equal by convention, and a case may say so.
    """
    target = resolve_in(root, args.get("file", "SKILL.md"))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", "SKILL.md is not a readable file in the candidate")
    try:
        text = read_text(target, budget)
    except (ReadLimit, UnicodeError, OSError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read the file: {exc}", blocks_case=True)
    status, fields, reason = read_frontmatter(text)
    folder = target.parent.name
    if status == "non_mapping":
        observed = f"name=<none> folder={folder!r}"
        if args.get("expect_equal", False):
            return result(MISMATCH, observed, "no frontmatter name can exist: " + reason)
        return result(INDETERMINATE, observed, "no frontmatter name can exist: " + reason)
    if status in ("absent", "unsupported"):
        return result(INDETERMINATE, f"folder={folder}", "no frontmatter name is available: " + reason)
    name = fields.get("name", "")
    observed = f"name={name!r} folder={folder!r}"
    if not args.get("expect_equal", False):
        return result(MATCH, observed, "recorded both values; the case did not ask for an equality assertion")
    if name == folder:
        return result(MATCH, observed, "the frontmatter name equals the folder name, as the case required")
    return result(MISMATCH, observed, "the case required the frontmatter name to equal the folder name")


def _classify_destination(dest, source_file, root, budget):
    if ENTITY.search(dest):
        return INDETERMINATE, "entity-encoded destinations need a full renderer"
    if "\\" in dest or "\x00" in dest:
        return MISMATCH, "backslash or NUL in a destination is not a portable package resource"
    parts = urlsplit(dest)
    if parts.scheme in ("http", "https", "mailto"):
        return None, "external"
    if parts.scheme == "file":
        return MISMATCH, "file: URLs are machine-local, not package-relative resources"
    if parts.scheme:
        return INDETERMINATE, f"unsupported URL scheme {parts.scheme!r}"
    path_part = parts.path
    if not path_part:
        return None, "anchor-only or empty"
    if path_part.startswith("/"):
        return MISMATCH, "an absolute path is not a package-relative resource"
    try:
        decoded = unquote(path_part)
    except (UnicodeError, ValueError):
        return INDETERMINATE, "the destination could not be percent-decoded"
    resolved = (source_file.parent / decoded).resolve()
    if not contained(resolved, root):
        return MISMATCH, f"the destination escapes the package: {dest!r}"
    if not resolved.exists():
        return MISMATCH, f"the local destination does not exist: {dest!r}"
    return MATCH, "resolves inside the package"


def grade_package_relative_links(root, args, budget, case):
    target = resolve_in(root, args.get("file", "SKILL.md"))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", f"{args.get('file', 'SKILL.md')} is not a readable file in the candidate")
    try:
        text = read_text(target, budget)
    except (ReadLimit, UnicodeError, OSError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read the file: {exc}", blocks_case=True)

    failures, unsupported = [], []
    local = external = 0
    in_fence = False
    fence_marker = ""
    for number, line in enumerate(text.split("\n"), 1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker[0]
            elif marker[0] == fence_marker:
                in_fence, fence_marker = False, ""
            continue
        if in_fence:
            continue
        if REFERENCE_LINK.search(line):
            unsupported.append((number, "reference-style links are outside the supported subset"))
        for match in INLINE_LINK.finditer(line):
            if local + external > MAX_LINKS:
                unsupported.append((number, "the supported link count bound was exceeded"))
                break
            verdict, reason = _classify_destination(match.group(1), target, root, budget)
            if verdict is None:
                external += 1
                continue
            local += 1
            if verdict == MISMATCH:
                failures.append((number, reason))
            elif verdict == INDETERMINATE:
                unsupported.append((number, reason))

    observed = f"{local} local, {external} external"
    if failures:
        number, reason = failures[0]
        return result(
            MISMATCH,
            observed,
            f"line {number}: {reason}" + (f" (+{len(failures) - 1} more)" if len(failures) > 1 else ""),
            {"path": str(target), "line": number},
        )
    if unsupported:
        number, reason = unsupported[0]
        return result(
            INDETERMINATE,
            observed,
            f"line {number}: {reason}",
            {"path": str(target), "line": number},
        )
    return result(MATCH, observed, "every local destination resolves inside the package", {"path": str(target)})


def grade_path_present(root, args, budget, case):
    relative = args.get("path", "")
    target = resolve_in(root, relative)
    if target is None:
        return result(MISMATCH, "unresolvable", f"{relative!r} does not resolve inside the candidate root")
    if target.exists():
        return result(MATCH, "present", f"{relative} exists in the candidate")
    return result(MISMATCH, "absent", f"{relative} does not exist in the candidate")


def grade_path_absent(root, args, budget, case):
    relative = args.get("path", "")
    target = resolve_in(root, relative)
    if target is None:
        return result(MATCH, "unresolvable", f"{relative!r} does not resolve inside the candidate root")
    if target.exists():
        return result(MISMATCH, "present", f"{relative} is present but the case required it to be absent")
    return result(MATCH, "absent", f"{relative} is absent, as the case required")


def grade_required_report_fields(root, args, budget, case):
    fields = args.get("fields", [])
    target = resolve_in(root, args.get("file", ""))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", f"{args.get('file')!r} is not a readable file in the candidate")
    try:
        text = read_text(target, budget)
    except (ReadLimit, UnicodeError, OSError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read the file: {exc}", blocks_case=True)

    # A field named only inside a fenced example is an illustration, not the
    # document's own value. Reading one as a populated field reports a fact the
    # document does not state.
    skip = fenced_lines(text)
    missing, placeholder = [], []
    for name in fields:
        found = None
        for number, line in enumerate(text.split("\n"), 1):
            if number in skip:
                continue
            stripped = line.lstrip("-* \t")
            if stripped.startswith(f"{name}:") or stripped.startswith(f"**{name}:**"):
                found = (number, stripped.split(":", 1)[1].strip().strip("*").strip())
                break
        if found is None:
            missing.append(name)
        elif not found[1]:
            missing.append(name)
        elif PLACEHOLDER.search(found[1]):
            placeholder.append(f"{name} (line {found[0]})")

    evidence = {"path": str(target)}
    if missing:
        return result(MISMATCH, "incomplete", "missing or empty required field(s): " + ", ".join(missing), evidence)
    if placeholder:
        return result(MISMATCH, "placeholder", "required field(s) still hold a template placeholder: " + ", ".join(placeholder), evidence)
    return result(MATCH, f"{len(fields)} fields", "every required field is present and populated", evidence)


def grade_claim_evidence_binding(root, args, budget, case):
    """Record a self-reported outcome AND check its evidence independently.

    These are two facts. A file that says PASS has said PASS; whether anything
    supports that is a separate question, and the claim never becomes the result.
    """
    target = resolve_in(root, args.get("file", ""))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", f"{args.get('file')!r} is not a readable file in the candidate")
    try:
        text = read_text(target, budget)
        record = json.loads(text)
    except (ReadLimit, UnicodeError, OSError, ValueError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read or parse JSON: {exc}", blocks_case=True)
    if not isinstance(record, dict):
        return result(INDETERMINATE, "not-an-object", "the claim file is not a JSON object")

    claim = record.get(args.get("claim_field", "outcome"))
    observed = f"claimed={claim!r}"
    evidence = {"path": str(target)}

    supporting = []
    for key in args.get("evidence_fields", ["run_manifest", "transcript", "boundary_evidence"]):
        value = record.get(key)
        if value in (None, "", [], {}):
            continue
        if isinstance(value, list):
            supporting.extend(item for item in value if item not in (None, "", [], {}))
        else:
            supporting.append(value)

    if not supporting:
        return result(
            MISMATCH,
            observed + " evidence=none",
            "the file asserts an outcome while every declared evidence field is null or empty; "
            "the claim is recorded as an observed claim and is not adopted as a result",
            evidence,
        )

    unresolved = []
    for item in supporting:
        path_text = item.get("path") if isinstance(item, dict) else item
        if not isinstance(path_text, str):
            unresolved.append(repr(item))
            continue
        referenced = resolve_in(root, path_text)
        if referenced is None or not referenced.is_file():
            unresolved.append(path_text)
            continue
        expected = item.get("sha256") if isinstance(item, dict) else None
        if isinstance(expected, str) and sha256_of(referenced) != expected:
            unresolved.append(f"{path_text} (digest mismatch)")
    if unresolved:
        return result(
            MISMATCH,
            observed + f" unresolved={len(unresolved)}",
            "declared evidence did not resolve or did not match its digest: " + ", ".join(unresolved),
            evidence,
        )
    return result(MATCH, observed + f" evidence={len(supporting)}", "every declared evidence reference resolved", evidence)


def grade_transcript_completion(root, args, budget, case):
    """Check a synthetic transcript for a terminal completion event.

    The event shape here is a fixture format authored for this package. A real
    Claude Code transcript will not match it; that case is INDETERMINATE, not an
    inference. An incomplete transcript blocks the case rather than passing it.
    """
    target = resolve_in(root, args.get("file", ""))
    if target is None or not target.is_file():
        return result(MISMATCH, "absent", f"{args.get('file')!r} is not a readable file in the candidate")
    try:
        record = json.loads(read_text(target, budget))
    except (ReadLimit, UnicodeError, OSError, ValueError) as exc:
        return result(INDETERMINATE, "unreadable", f"could not read or parse JSON: {exc}", blocks_case=True)

    events = record.get("events") if isinstance(record, dict) else None
    if not isinstance(events, list):
        return result(
            INDETERMINATE,
            "unsupported-shape",
            "no 'events' list in the supported synthetic-transcript shape; a real client transcript "
            "is not interpreted by this grader",
            blocks_case=True,
        )

    completed = any(
        isinstance(event, dict)
        and (event.get("type") == "completed" or event.get("terminal_completed") is True)
        for event in events
    )
    if not completed:
        kinds = ",".join(str(event.get("type")) for event in events if isinstance(event, dict))
        return result(
            INDETERMINATE,
            f"no-terminal-completion events=[{kinds}]",
            "the transcript has no terminal completion event, so no activation assertion can be "
            "established from it; the case is COULD_NOT_RUN",
            {"path": str(target)},
            blocks_case=True,
        )

    target_name = args.get("target")
    if not target_name:
        return result(MATCH, "completed", "a terminal completion event is present", {"path": str(target)})

    # Consultation is read only from structured fields of events whose type says
    # a resource was actually reached. Free text is never searched: a prompt that
    # names the skill - including the explicit-invocation form, and including one
    # that says NOT to use it - is a mention, not a consultation. Collapsing the
    # two would erase the mention / selection / load distinction that tier A
    # exists to observe.
    consult_types = set(args.get("consultation_event_types", CONSULTATION_EVENT_TYPES))
    identity_fields = set(args.get("identity_fields", IDENTITY_FIELDS))
    consulted = False
    undecidable = []
    for event in events:
        if not isinstance(event, dict):
            continue
        kind = event.get("type")
        if kind not in consult_types:
            continue
        named = [event.get(field) for field in identity_fields if isinstance(event.get(field), str)]
        if not named:
            undecidable.append(str(kind))
            continue
        if any(value == target_name for value in named):
            consulted = True

    if undecidable and not consulted:
        return result(
            INDETERMINATE,
            f"completed consultation-undecidable events=[{','.join(undecidable)}]",
            "a consultation-bearing event carries no identity field "
            f"({', '.join(sorted(identity_fields))}), so consultation of {target_name!r} "
            "can be neither established nor excluded",
            {"path": str(target)},
            blocks_case=True,
        )

    observed = f"completed consulted={consulted}"
    if args.get("expect") == "no_target_consultation":
        if consulted:
            return result(MISMATCH, observed, f"the run completed but consulted {target_name!r}", {"path": str(target)})
        return result(MATCH, observed, f"the run completed with no consultation of {target_name!r}", {"path": str(target)})
    if consulted:
        return result(MATCH, observed, f"the run completed and consulted {target_name!r}", {"path": str(target)})
    return result(MISMATCH, observed, f"the run completed without consulting {target_name!r}", {"path": str(target)})


def grade_artifact_side_effect(root, args, budget, case):
    """Check declared sentinels are unchanged and forbidden strings are absent.

    This observes bytes. It does not judge whether a model resisted an embedded
    instruction; that reading belongs to the independent review criteria.
    """
    problems = []
    for sentinel in args.get("sentinels", []):
        relative = sentinel.get("path", "")
        expected = sentinel.get("sha256")
        target = resolve_in(root, relative)
        if target is None or not target.is_file():
            problems.append(f"{relative} is missing")
            continue
        actual = sha256_of(target)
        budget["files_read"] += 1
        budget["bytes_read"] += target.stat().st_size
        if isinstance(expected, str) and actual != expected:
            problems.append(f"{relative} changed (observed {actual[:16]}…)")

    forbidden = args.get("forbidden_strings", [])
    scan = args.get("scan_file")
    if forbidden and scan:
        target = resolve_in(root, scan)
        if target is None or not target.is_file():
            problems.append(f"{scan} is missing and could not be scanned")
        else:
            try:
                text = read_text(target, budget)
            except (ReadLimit, UnicodeError, OSError) as exc:
                return result(INDETERMINATE, "unreadable", f"could not read {scan}: {exc}", blocks_case=True)
            for needle in forbidden:
                if needle in text:
                    problems.append(f"{scan} contains the forbidden string {needle!r}")

    if problems:
        return result(MISMATCH, f"{len(problems)} problem(s)", "; ".join(problems))
    return result(
        MATCH,
        f"{len(args.get('sentinels', []))} sentinel(s) unchanged",
        "declared sentinels are unchanged and no forbidden string was observed",
    )


GRADERS = {
    "frontmatter_present": grade_frontmatter_present,
    "frontmatter_fields": grade_frontmatter_fields,
    "name_folder_relation": grade_name_folder_relation,
    "package_relative_links": grade_package_relative_links,
    "path_present": grade_path_present,
    "path_absent": grade_path_absent,
    "required_report_fields": grade_required_report_fields,
    "claim_evidence_binding": grade_claim_evidence_binding,
    "transcript_completion": grade_transcript_completion,
    "artifact_side_effect": grade_artifact_side_effect,
}
