#!/usr/bin/env python3
"""Progress evaluator for DevForgeAI skill runs (SPEC-012).

Run from the project root:
    python3 evaluate.py evaluate --manifests DIR [--manifests DIR ...] --events FILE --out FILE
                                 [--root DIR] [--phases FILE]
    python3 evaluate.py check --manifests DIR --skill NAME --checklist FILE

`evaluate` (IF-01) reads a run's event log (devforgeai-events/1) and the skill's manifest
(devforgeai-manifest/1), in layers, and writes the run's progress state (devforgeai-progress/1).
It exits 0 when the state is written, with or without flags, and 2 when it can't run, with one line
on stderr. `check` (IF-02) compares a skill's checklist with its manifest: exit 0 when they match,
1 when the manifest is stale or missing, 2 when it can't run.

The evaluator is a pure function of its inputs (BEH-01): each call reads the whole event log, keeps
nothing between calls, and reads no clock. It uses the Python standard library only (QR-01), reads
only the files its command names and, with --root, the files a run wrote (QR-04), and writes only
--out.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from fnmatch import fnmatchcase
from pathlib import PurePosixPath

CHECKLIST_LINE = re.compile(r"^\s*- \[ \] (\d+)\. (.+?)\s*$")
DONE_TICK = re.compile(r"^\s*[-*]\s*\[[xX]\]\s*(\d+)\.")
SKIP_TICK = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s*(\d+)\..*\(skipped:\s*(.+?)\)\s*$")

STEP_KINDS = ("read", "think", "ask", "forge", "inspect", "report")
NEEDS = ("required", "conditional", "text-only")
RULE_TYPES = ("script", "answer", "write", "read")
SCOPES = ("frontmatter", "anywhere")
EVENT_FIELDS = {  # the fields each kind of event must carry (DM-02)
    "skill-loaded": {"format": str, "skill": str, "checklist": str},
    "tool": {"tool": str},
    "answer": {"answered": bool},
    "prompt": {},
    "reply": {"text": str},
    "turn": {"phase": str},
    "run-end": {"reason": str},
}
CHAIN = ("brainstorm", "prd", "architecture", "context", "epic", "story")
NOT_BUILT = {"story": "the story skill isn't built yet (SPEC-009)"}


class Fail(Exception):
    """A reason the evaluator can't run: exit 2, with the message on stderr."""


# ---- checklist and hash (§4) ---------------------------------------------------------------

def checklist_steps(text):
    """[(number, title)] for every checklist line in the text, in order."""
    steps = []
    for line in text.splitlines():
        m = CHECKLIST_LINE.match(line)
        if m:
            steps.append((int(m.group(1)), m.group(2)))
    return steps


def checklist_hash(text):
    """SPEC-012 §4's hash of a checklist, or None when the text holds no checklist line."""
    steps = checklist_steps(text)
    if not steps:
        return None
    rebuilt = "\n".join("- [ ] %d. %s" % (n, title) for n, title in steps)
    return "sha256:" + hashlib.sha256(rebuilt.encode("utf-8")).hexdigest()


# ---- reading files ----------------------------------------------------------------------------

def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        raise Fail("%s: %s" % (path, e.strerror or e))
    except UnicodeDecodeError:
        raise Fail("%s: not UTF-8 text" % path)


def read_json(path):
    try:
        return json.loads(read_text(path))
    except ValueError as e:
        raise Fail("%s: not valid JSON (%s)" % (path, e))


# ---- manifests (DM-01) and their layers (BEH-17) ---------------------------------------------

def check_manifest_shape(m, path):
    """The keys the evaluator relies on (ERR-04); the JSON Schema stays the full contract."""
    def bad(why):
        raise Fail("%s: %s" % (path, why))
    if not isinstance(m, dict):
        bad("not a manifest object")
    for key in ("format", "skill", "checklistHash", "steps"):
        if key not in m:
            bad("lacks %s" % key)
    if m["format"] != "devforgeai-manifest/1":
        bad("format is %r, not devforgeai-manifest/1" % m["format"])
    if not isinstance(m["steps"], dict):
        bad("steps isn't an object")
    for n, step in m["steps"].items():
        if not (isinstance(n, str) and n.isdigit() and isinstance(step, dict)):
            bad("step %r isn't a numbered object" % n)
        for key in ("title", "kind", "need"):
            if key not in step:
                bad("step %s lacks %s" % (n, key))
        if step["kind"] not in STEP_KINDS or step["need"] not in NEEDS:
            bad("step %s has an unknown kind or need" % n)
        for rule in step.get("evidence", []):
            if not isinstance(rule, dict) or rule.get("type") not in RULE_TYPES:
                bad("step %s has an evidence rule of unknown type" % n)
            if rule["type"] != "answer" and not isinstance(rule.get("pattern"), str):
                bad("step %s has a %s rule with no pattern" % (n, rule["type"]))
    for rule in m.get("contentRules", []):
        if not isinstance(rule, dict) or any(k not in rule for k in ("step", "path", "field", "scope", "allowed")):
            bad("a content rule lacks step, path, field, scope or allowed")
        if rule["scope"] not in SCOPES or str(rule["step"]) not in m["steps"]:
            bad("a content rule names an unknown scope or step")


def relaxation(base, later):
    """What a later layer removes or relaxes from the effective manifest, or None (BEH-17)."""
    if later["skill"] != base["skill"]:
        return "names skill %s instead of %s" % (later["skill"], base["skill"])
    if later["checklistHash"] != base["checklistHash"]:
        return "carries another checklistHash"
    for n, b in base["steps"].items():
        s = later["steps"].get(n)
        if s is None:
            return "removes step %s" % n
        if s["title"] != b["title"]:
            return "changes step %s's title" % n
        if s["kind"] != b["kind"]:
            return "changes step %s's kind from %s to %s" % (n, b["kind"], s["kind"])
        if s["need"] != b["need"] and s["need"] != "required":
            return "relaxes step %s's need from %s to %s" % (n, b["need"], s["need"])
        if b["need"] == "conditional" and s["need"] == "conditional" and s.get("when") != b.get("when"):
            return "changes step %s's when" % n
        if b.get("userOwned") and not s.get("userOwned"):
            return "makes step %s no longer user-owned" % n
        if b.get("gate") and s.get("gate") != b["gate"]:
            return "removes step %s's %s gate" % (n, b["gate"])
        for rule in b.get("evidence", []):
            if rule not in s.get("evidence", []):
                return "removes an evidence rule of step %s (%s)" % (n, json.dumps(rule, sort_keys=True))
    for n in later["steps"]:
        if n not in base["steps"]:
            return "adds step %s, which the earlier layers don't have" % n
    for rule in base.get("contentRules", []):
        if rule not in later.get("contentRules", []):
            return "removes the content rule on %s for step %s" % (rule["field"], rule["step"])
    return None


def load_manifest(folders, skill):
    """The effective manifest for a skill, and the files used, in layer order (BEH-17, ERR-04, ERR-09)."""
    effective, effective_file, layers = None, None, []
    for folder in folders:
        if not os.path.isdir(folder):
            raise Fail("%s: not a folder" % folder)
        path = folder.rstrip("/") + "/" + skill + ".json"
        if not os.path.isfile(path):
            continue
        m = read_json(path)
        check_manifest_shape(m, path)
        if effective is not None:
            problem = relaxation(effective, m)
            if problem:
                raise Fail("%s: %s, which an earlier layer set (%s)" % (path, problem, effective_file))
        effective, effective_file = m, path
        layers.append(path)
    return effective, layers


# ---- events (DM-02; BEH-02, ERR-01, ERR-02, ERR-03) -----------------------------------------

def well_formed(e):
    if not isinstance(e, dict):
        return False
    if not isinstance(e.get("run"), str) or not isinstance(e.get("time"), str):
        return False
    if not isinstance(e.get("seq"), int) or isinstance(e.get("seq"), bool) or e["seq"] < 1:
        return False
    fields = EVENT_FIELDS.get(e.get("kind"))
    if fields is None:
        return False
    return all(isinstance(e.get(k), t) for k, t in fields.items())


def read_events(path):
    """The run's events in seq order, up to and including run-end, and the counts (ERR-01, ERR-02, BEH-12)."""
    counts = {"events": 0, "malformed": 0, "outOfOrder": 0, "duplicates": 0, "unknownClaims": 0, "afterEnd": 0}
    valid = []
    for line in read_text(path).splitlines():
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except ValueError:
            counts["malformed"] += 1
            continue
        if well_formed(e):
            valid.append(e)
        else:
            counts["malformed"] += 1
    if not valid or valid[0]["kind"] != "skill-loaded":
        raise Fail("%s: the first event must be skill-loaded" % path)
    run, seen, kept, highest = valid[0]["run"], set(), [], 0
    for e in valid:
        if e["run"] != run:
            counts["malformed"] += 1
        elif e["seq"] in seen:
            counts["duplicates"] += 1
        else:
            seen.add(e["seq"])
            if e["seq"] < highest:
                counts["outOfOrder"] += 1
            highest = max(highest, e["seq"])
            kept.append(e)
    kept.sort(key=lambda e: e["seq"])
    counts["events"] = len(kept)
    events = []
    for e in kept:
        if events and events[-1]["kind"] == "run-end":
            counts["afterEnd"] += 1
        else:
            events.append(e)
    return events, counts


# ---- the progress state -----------------------------------------------------------------------

def skill_name(event):
    return event["skill"].split(":")[-1]


def build_state(events, counts, manifest, layers, root=None):
    loaded = events[0]
    skill = skill_name(loaded)
    event_hash = checklist_hash(loaded["checklist"])
    if manifest is None:
        manifest_state = "none"
    elif event_hash is None:
        manifest_state = "unverified"
    elif event_hash == manifest["checklistHash"]:
        manifest_state = "matched"
    else:
        manifest_state = "stale"
    ended = events[-1]["reason"] if events[-1]["kind"] == "run-end" else None
    steps = []
    if manifest_state in ("matched", "unverified"):
        for n in sorted(manifest["steps"], key=int):
            m = manifest["steps"][n]
            steps.append({"n": int(n), "title": m["title"], "kind": m["kind"], "need": m["need"],
                          "userOwned": bool(m.get("userOwned")), "state": "pending", "evidence": [],
                          "claim": None, "note": ""})
    else:
        for n, title in checklist_steps(loaded["checklist"]):
            steps.append({"n": n, "title": title, "kind": None, "need": "text-only", "userOwned": False,
                          "state": "pending", "evidence": [], "claim": None, "note": ""})
    state = {
        "format": "devforgeai-progress/1",
        "run": loaded["run"],
        "skill": skill,
        "manifest": {"state": manifest_state,
                     "manifestHash": manifest["checklistHash"] if manifest else None,
                     "checklistHash": event_hash, "layers": layers},
        "through": events[-1]["seq"],
        "ended": ended,
        "current": None,
        "steps": steps,
        "flags": [],
        "gate": {"kind": None, "seq": None, "refuse": False, "reason": None},
        "next": None,
        "counts": counts,
    }
    return state


def summary(state):
    """BEH-14's stdout line."""
    n = len(state["flags"])
    if state["current"] is not None:
        where = "step %d of %d" % (state["current"], len(state["steps"]))
    elif state["ended"] is not None:
        where = "ended (%s)" % state["ended"]
    else:
        where = "all %d steps reached" % len(state["steps"])
    line = "progress %s: %s, %d flag%s" % (state["skill"], where, n, "" if n == 1 else "s")
    return line + (", refuse" if state["gate"]["refuse"] else "")


def write_state(state, out):
    """Sorted keys, two-space indent, final newline; a temporary file, then a rename (BEH-14, ERR-08)."""
    folder = os.path.dirname(os.path.abspath(out))
    if not os.path.isdir(folder):
        raise Fail("%s: the folder %s doesn't exist" % (out, os.path.dirname(out) or "."))
    text = json.dumps(state, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    try:
        fd, tmp = tempfile.mkstemp(dir=folder, prefix=".state-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, out)
    except OSError as e:
        raise Fail("%s: %s" % (out, e.strerror or e))


# ---- commands -----------------------------------------------------------------------------------

def cmd_evaluate(args):
    folder = os.path.dirname(os.path.abspath(args.out))
    if not os.path.isdir(folder):
        raise Fail("%s: the folder %s doesn't exist" % (args.out, os.path.dirname(args.out) or "."))
    events, counts = read_events(args.events)
    manifest, layers = load_manifest(args.manifests, skill_name(events[0]))
    phases = read_json(args.phases) if args.phases else None
    state = build_state(events, counts, manifest, layers, root=args.root)
    if args.phases:
        state["phases"] = phases
    write_state(state, args.out)
    print(summary(state))
    return 0


def cmd_check(args):
    text = read_text(args.checklist)
    manifest, _ = load_manifest([args.manifests], args.skill)
    found = checklist_hash(text) or "sha256:none"
    if manifest is None:
        print("none %s" % found)
        return 1
    if manifest["checklistHash"] == found:
        print("matched %s" % found)
        return 0
    print("stale manifest %s checklist %s" % (manifest["checklistHash"], found))
    return 1


def parse(argv):
    p = argparse.ArgumentParser(prog="evaluate.py", description="DevForgeAI progress evaluator (SPEC-012)")
    sub = p.add_subparsers(dest="command", required=True)
    e = sub.add_parser("evaluate", help="write a run's progress state (IF-01)")
    e.add_argument("--manifests", action="append", required=True, help="a manifest folder; repeat, in layer order")
    e.add_argument("--events", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--root", help="the project root, for written files whose events carry no content")
    e.add_argument("--phases", help="a JSON file copied into the state's phases")
    c = sub.add_parser("check", help="compare a skill's checklist with its manifest (IF-02)")
    c.add_argument("--manifests", required=True)
    c.add_argument("--skill", required=True)
    c.add_argument("--checklist", required=True)
    return p.parse_args(argv)


def main(argv=None):
    args = parse(sys.argv[1:] if argv is None else argv)
    try:
        return cmd_evaluate(args) if args.command == "evaluate" else cmd_check(args)
    except Fail as e:
        print("%s: %s" % (args.command, e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
