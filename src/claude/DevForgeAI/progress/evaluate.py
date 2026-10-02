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


INFINITY = float("inf")


def path_matches(path, pattern):
    """A path against a rule's pattern; a pattern ending in / means anything inside that folder."""
    if pattern.endswith("/"):
        return path.startswith(pattern) or path == pattern[:-1]
    return fnmatchcase(path, pattern)


def names_a(candidate, written):
    """Whether a path or command token names one of the written files."""
    return any(candidate == w or candidate.endswith("/" + w) for w in written)


class Step:
    def __init__(self, n, title, kind=None, need="text-only", user_owned=False, gate=None, rules=(), when=None):
        self.n, self.title, self.kind, self.need = n, title, kind, need
        self.user_owned, self.gate, self.rules, self.when = user_owned, gate, list(rules), when
        self.strong = any(r["type"] in ("script", "answer") for r in self.rules)
        self.evidence = []      # dicts: seq, type, strength, detail
        self.claims = []        # dicts: seq, state, reason, in seq order
        self.gate_state = None  # set by a gate: skipped, not-applicable, unconfirmed
        self.sticky = None      # a gate result later evidence can't undo: skipped, rule-broken
        self.note = ""
        self.unverifiable = False

    def claim_before(self, upto):
        claims = [c for c in self.claims if c["seq"] < upto]
        return claims[-1] if claims else None

    def first_signal(self):
        seqs = [x["seq"] for x in self.evidence] + [c["seq"] for c in self.claims]
        return min(seqs) if seqs else None

    def reached(self, upto=INFINITY):
        return any(x["seq"] < upto for x in self.evidence) or any(c["seq"] < upto for c in self.claims)

    def answered(self, upto=INFINITY):
        return any(x["type"] == "answer" and x["seq"] < upto for x in self.evidence)

    def base_state(self, upto=INFINITY):
        """BEH-07's state from the evidence and claims before `upto`."""
        if any(x["seq"] < upto for x in self.evidence):
            return "done"
        claim = self.claim_before(upto)
        if claim is None:
            return "pending"
        if claim["state"] == "skipped":
            return "skipped-with-reason"
        return "claimed" if self.strong else "done"


class Run:
    """One run's steps, judged from its events (BEH-04 to BEH-13)."""

    def __init__(self, events, manifest, manifest_state, root):
        self.events, self.root = events, root
        self.tracked = manifest_state in ("matched", "unverified")
        loaded = events[0]
        if self.tracked:
            self.steps = [Step(int(n), m["title"], m["kind"], m["need"], bool(m.get("userOwned")),
                               m.get("gate"), m.get("evidence", []), m.get("when"))
                          for n, m in sorted(manifest["steps"].items(), key=lambda kv: int(kv[0]))]
            self.content_rules = manifest.get("contentRules", [])
        else:
            self.steps = [Step(n, title) for n, title in checklist_steps(loaded["checklist"])]
            self.content_rules = []
        self.by_n = {s.n: s for s in self.steps}
        self.write_gate = next((s for s in self.steps if s.gate == "write"), None)
        self.report_gate = next((s for s in self.steps if s.gate == "report"), None)
        self.written = []           # (seq, path): files the write-gate step wrote
        self.unknown_claims = 0
        self.flags = []
        self.gate = {"kind": None, "seq": None, "refuse": False, "reason": None}
        notes = {"stale": "manifest out of date; tracking ticks only",
                 "none": "no manifest for this skill; tracking ticks only",
                 "unverified": "the checklist wasn't seen in the skill-loaded event; using the manifest as is"}
        self.manifest_note = notes.get(manifest_state)

    # -- evidence and claims (BEH-05, BEH-06) --

    def written_before(self, seq):
        return [p for s, p in self.written if s < seq]

    def rule_matches(self, rule, e):
        tool, kind = e.get("tool"), rule["type"]
        if e.get("error") is True:
            return None
        if kind == "script":
            command = e.get("command")
            if tool != "Bash" or not isinstance(command, str):
                return None
            tokens = command.split()
            hit = next((t for t in tokens if fnmatchcase(PurePosixPath(t).name, rule["pattern"])), None)
            if hit is None or e.get("exit") != rule.get("exit", 0):
                return None
            if rule.get("target") == "written" and not any(names_a(t, self.written_before(e["seq"])) for t in tokens):
                return None
            return "%s exit %d" % (PurePosixPath(hit).name, e["exit"])
        path = e.get("path")
        if not isinstance(path, str):
            return None
        if kind == "write" and tool in ("Write", "Edit") and path_matches(path, rule["pattern"]):
            return "%s %s" % (tool, path)
        if kind == "read" and tool in ("Read", "Glob", "Grep") and path_matches(path, rule["pattern"]):
            if rule.get("target") == "written" and not names_a(path, self.written_before(e["seq"])):
                return None
            return "%s %s" % (tool, path)
        return None

    def take_tool(self, e):
        if self.write_gate is not None:
            for rule in self.write_gate.rules:
                if rule["type"] == "write" and e.get("error") is not True and e.get("tool") in ("Write", "Edit") \
                        and isinstance(e.get("path"), str) and path_matches(e["path"], rule["pattern"]):
                    self.written.append((e["seq"], e["path"]))
                    break
        for step in self.steps:
            for rule in step.rules:
                if rule["type"] == "answer":
                    continue
                detail = self.rule_matches(rule, e)
                if detail:
                    strength = "strong" if rule["type"] == "script" else "medium"
                    step.evidence.append({"seq": e["seq"], "type": rule["type"], "strength": strength,
                                          "detail": detail})
                    break

    def take_reply(self, e):
        for line in e["text"].splitlines():
            m = SKIP_TICK.match(line)
            if m:
                n, claim = int(m.group(1)), {"seq": e["seq"], "state": "skipped", "reason": m.group(2)}
            else:
                m = DONE_TICK.match(line)
                if not m:
                    continue
                n, claim = int(m.group(1)), {"seq": e["seq"], "state": "done", "reason": None}
            if n not in self.by_n:
                self.unknown_claims += 1
            else:
                self.by_n[n].claims.append(claim)

    def collect(self):
        for e in self.events:
            if e["kind"] == "tool":
                self.take_tool(e)
            elif e["kind"] == "reply":
                self.take_reply(e)

    # -- positions --

    def highest_reached(self, upto=INFINITY):
        reached = [s.n for s in self.steps if s.reached(upto)]
        return max(reached) if reached else None

    def current(self):
        if self.events[-1]["kind"] == "run-end" or not self.steps:
            return None
        highest = self.highest_reached()
        if highest is None:
            return self.steps[0].n
        later = [s.n for s in self.steps if s.n > highest]
        return later[0] if later else None

    # -- assembling the state --

    def final_state(self, step):
        if step.sticky:
            return step.sticky
        base = step.base_state()
        if base in ("done", "claimed", "skipped-with-reason"):
            return base
        return step.gate_state or "pending"

    def step_notes(self, current):
        ended = self.events[-1]["kind"] == "run-end"
        highest = self.highest_reached()
        for step in self.steps:
            first = step.first_signal()
            if first is not None:
                earlier = [s.n for s in self.steps if s.n > step.n and s.first_signal() is not None
                           and s.first_signal() < first]
                if earlier and not step.note:
                    step.note = "seen late (after step %d)" % max(earlier)
            if self.final_state(step) == "pending" and not step.note:
                if ended or (current is None and highest is not None and step.n > highest):
                    if highest is None or step.n > highest:
                        step.note = "not reached"
                elif current is not None and step.n < current:
                    step.note = "not seen yet"
        if self.manifest_note and self.steps:
            first = self.steps[0]
            first.note = self.manifest_note + ("; " + first.note if first.note else "")

    def step_records(self, current):
        last = self.events[-1]
        waiting = last["kind"] == "turn" and last.get("phase") == "end"
        records = []
        for step in self.steps:
            state = self.final_state(step)
            if step.n == current and state == "pending":
                state = "your-turn" if step.user_owned and not step.answered() and waiting else "current"
            claim = step.claims[-1] if step.claims else None
            records.append({"n": step.n, "title": step.title, "kind": step.kind, "need": step.need,
                            "userOwned": step.user_owned, "state": state,
                            "evidence": sorted(step.evidence, key=lambda x: x["seq"]),
                            "claim": dict(claim) if claim else None, "note": step.note})
        return records


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
    run = Run(events, manifest, manifest_state, root)
    run.collect()
    counts = dict(counts, unknownClaims=run.unknown_claims)
    current = run.current()
    run.step_notes(current)
    state = {
        "format": "devforgeai-progress/1",
        "run": loaded["run"],
        "skill": skill,
        "manifest": {"state": manifest_state,
                     "manifestHash": manifest["checklistHash"] if manifest else None,
                     "checklistHash": event_hash, "layers": layers},
        "through": events[-1]["seq"],
        "ended": events[-1]["reason"] if events[-1]["kind"] == "run-end" else None,
        "current": current,
        "steps": run.step_records(current),
        "flags": run.flags,
        "gate": run.gate,
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
