#!/usr/bin/env python3
"""Progress evaluator for DevForgeAI skill runs (SPEC-012 v8).

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
    "step": {"step": int, "state": str},
}
STEP_STATES = ("started", "done")
WAIVERS = ("proceed", "ask", "other")  # the waiver answer's values (DM-02, version 11)
TASK_TAG = "devforgeai_step"  # a skill whose text names it follows the task-list convention (§4, BEH-18)
# A command whose exit status isn't its script's: ;, |, a line break, or a & that sends a command to the background
# (&& and redirections such as 2>&1, &> and >& are fine) (BEH-06, version 7).
JOINED = re.compile(r"[;|\n]|(?<![&<>])&(?![&>])")


def joined(command):
    """Whether a command joins its parts so its exit status may be another command's (BEH-06); a backslash line
    continuation splits one command over two lines and joins nothing."""
    return bool(JOINED.search(command.replace("\\\n", " ")))
UNMARKED = ("a question was asked while no step was marked in progress in the task list: "
            "mark the step it belongs to in progress, then ask")
MISMATCHED = ("a question for step {n} was asked while step {k} was marked in progress: "
              "mark step {n} in progress, then ask")  # version 9
UNTAGGED = ("a question was asked without naming a step of the checklist: tag it with devforgeai_step:N "
            "for the step it belongs to, mark that step in progress, then ask")  # version 9
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
        if step.get("waivable") is True and step.get("userOwned") is not True:
            bad("step %s is waivable but not user-owned" % n)  # version 11: a waiver answers only the user's step
        for rule in step.get("evidence", []):
            if not isinstance(rule, dict) or rule.get("type") not in RULE_TYPES:
                bad("step %s has an evidence rule of unknown type" % n)
            if rule["type"] != "answer" and not isinstance(rule.get("pattern"), str):
                bad("step %s has a %s rule with no pattern" % (n, rule["type"]))
            if "exclude" in rule and (rule["type"] != "read" or not isinstance(rule["exclude"], list)
                                      or not all(isinstance(x, str) for x in rule["exclude"])):
                bad("step %s has an exclude that isn't a list of patterns on a read rule" % n)
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
        if bool(s.get("waivable")) != bool(b.get("waivable")):
            # waivable true relaxes a user-owned step, so only the base manifest sets it (BEH-17, version 11)
            return "changes step %s's waivable from %s to %s" % (n, bool(b.get("waivable")), bool(s.get("waivable")))
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
    if e["kind"] == "step" and (isinstance(e.get("step"), bool) or not isinstance(e.get("step"), int)
                                or e["step"] < 1 or e.get("state") not in STEP_STATES):
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
            if e["kind"] == "tool" and isinstance(e.get("path"), str):
                # Every tool's path is read like the rest (BEH-06): a leading ./ removed, as from a Glob at the root
                # or a Write's relative path, after repeated slashes collapse (a build departure, SPEC-012 §9).
                tool_path = re.sub(r"/{2,}", "/", e["path"])
                while tool_path.startswith("./"):
                    tool_path = tool_path[2:]
                e["path"] = tool_path
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


def rule_path_matches(path, rule):
    """A path or read token against a rule (BEH-06): patterns are relative to the project root, so one still starting
    with / or ../ matches none; then the pattern, as text or as a folder, and none of the rule's exclude patterns."""
    if path.startswith("/") or path.startswith("../"):
        return False
    return path_matches(path, rule["pattern"]) and not any(path_matches(path, x) for x in rule.get("exclude", ()))


def bash_readable(pattern):
    """Whether a read rule takes Bash evidence: no wildcard in its pattern's first path segment (BEH-06), since a
    token such as cat would match a pattern of *."""
    first = pattern.split("/", 1)[0]
    return bool(first) and not any(c in first for c in "*?[")


def read_tokens(command, roots):
    """A Bash command's read tokens (BEH-06): its words split at whitespace, every quote character removed, the
    characters ; ( ) stripped from both ends, a leading ./ removed, and a --root prefix and its / removed."""
    tokens = []
    for word in command.split():
        token = word.replace("'", "").replace('"', "").strip(";()")
        if token.startswith("./"):
            token = token[2:]
        for root in roots:
            if token.startswith(root + "/"):
                token = token[len(root) + 1:]
                break
        if token:
            tokens.append(token)
    return tokens


def names_a(candidate, written):
    """Whether a path or command token names one of the written files."""
    return any(candidate == w or candidate.endswith("/" + w) for w in written)


class Step:
    def __init__(self, n, title, kind=None, need="text-only", user_owned=False, gate=None, rules=(), when=None,
                 waivable=False, stoppable=False):
        self.n, self.title, self.kind, self.need = n, title, kind, need
        self.waivable = waivable
        self.stoppable = stoppable  # version 12: its 'Write nothing' answer may stop the run (SPEC-013 BEH-27)
        self.user_owned, self.gate, self.rules, self.when = user_owned, gate, list(rules), when
        self.strong = any(r["type"] in ("script", "answer") for r in self.rules)
        self.evidence = []      # dicts: seq, type, strength, detail
        self.claims = []        # dicts: seq, state, reason, in seq order
        self.event_claims = set()  # seqs of the claims that are done step events (BEH-05)
        self.joined = []        # (seq, script file name): runs of its script joined to another command (BEH-06)
        self.gate_state = None  # set by a gate: skipped, not-applicable, unconfirmed
        self.gate_note = ""     # the note that goes with not-applicable
        self.sticky = None      # a gate result later evidence can't undo: skipped, rule-broken
        self.unverifiable = False
        self.note = ""
        self.carried_answer = False  # version 14: the earlier run's answer stands for this carried step (BEH-20)

    def claim_before(self, upto):
        claims = [c for c in self.claims if c["seq"] < upto]
        return claims[-1] if claims else None

    def signals(self):
        """Seqs of this step's tool evidence and claims (answers excluded: they don't move windows; nor does carried
        evidence, BEH-20)."""
        return ([x["seq"] for x in self.evidence if x["type"] not in ("answer", "waiver", "carried")]
                + [c["seq"] for c in self.claims])

    def first_signal(self):
        # The waiver's stamp is no signal: it gives no 'seen late' note (BEH-19).
        seqs = [x["seq"] for x in self.evidence if x["type"] != "waiver"] + [c["seq"] for c in self.claims]
        return min(seqs) if seqs else None

    def reached(self, upto=INFINITY):
        return any(x["seq"] < upto for x in self.evidence) or any(c["seq"] < upto for c in self.claims)

    def answered(self, upto=INFINITY):
        return self.carried_answer or any(x["type"] == "answer" and x["seq"] < upto for x in self.evidence)

    def base_state(self, upto=INFINITY):
        """BEH-07's state from the evidence and claims before `upto`; carried while carried evidence is its only
        evidence, whatever claims it gets (BEH-20, version 14)."""
        evidence = [x for x in self.evidence if x["seq"] < upto]
        if evidence:
            return "carried" if all(x["type"] == "carried" for x in evidence) else "done"
        claim = self.claim_before(upto)
        if claim is None:
            return "pending"
        if claim["state"] == "skipped":
            return "skipped-with-reason"
        return "claimed" if self.strong else "done"

    def not_applicable_by_event(self, upto=INFINITY):
        """A conditional step a done step event marked with no evidence: the skill found it didn't apply (BEH-07). A
        later done tick, as a checklist restated after a compaction gives, doesn't undo that; a skipped one does."""
        claims = [c for c in self.claims if c["seq"] < upto]
        return (self.need == "conditional" and bool(claims) and claims[-1]["state"] == "done"
                and any(c["seq"] in self.event_claims for c in claims)
                and not any(x["seq"] < upto for x in self.evidence))

    def expected_evidence(self):
        what = []
        for rule in self.rules:
            if rule["type"] == "script":
                what.append("a successful run of %s%s" % (rule["pattern"],
                                                          " on a written file" if rule.get("target") else ""))
            elif rule["type"] == "answer":
                what.append("an answer from you")
            else:
                text = "a %s of %s" % (rule["type"], rule["pattern"])
                if rule.get("exclude"):
                    text += " except " + ", ".join(rule["exclude"])
                what.append(text)
        return " or ".join(what)

    def skipped_expectation(self):
        """What a skipped flag says the step expected (BEH-08): its evidence, or a tick when no rule is strong."""
        if not self.rules:
            return "a tick in the reply text"
        expected = self.expected_evidence()
        return expected if self.strong else expected + ", or a tick in the reply text"


def field_values(text, field, scope):
    """The values of a field in a document, line by line (SPEC-012 §4); no YAML parsing."""
    lines = text.splitlines()
    if scope == "frontmatter":
        marks = [i for i, line in enumerate(lines) if line.strip() == "---"][:2]
        lines = lines[marks[0] + 1:marks[1]] if len(marks) == 2 else []
    pattern = re.compile(r"^\s*(?:-\s+)?" + re.escape(field) + r":\s*[\"']?([^\s\"'#,}]+)")
    return [m.group(1) for m in (pattern.match(line) for line in lines) if m]


GATE_WORDS = {"write": "the write gate", "report": "the report", "end": "the run ended"}


class Run:
    """One run's steps, judged from its events (BEH-04 to BEH-13)."""

    def __init__(self, events, manifest, manifest_state, root):
        self.events, self.root = events, root
        # The --root prefixes a Bash read token may carry: as given, and absolute (BEH-06); each event's tokens once.
        self.token_cache = {}
        self.roots = sorted({r.rstrip("/") for r in (root, os.path.abspath(root))}, key=len, reverse=True) if root else []
        self.tracked = manifest_state in ("matched", "unverified")
        loaded = events[0]
        if self.tracked:
            self.steps = [Step(int(n), m["title"], m["kind"], m["need"], bool(m.get("userOwned")),
                               m.get("gate"), m.get("evidence", []), m.get("when"), m.get("waivable") is True,
                               m.get("stoppable") is True)
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
        self.flagged = set()        # (step, type) already flagged
        # A run follows the task list when its host has one and its skill names the convention's tag (BEH-18).
        self.follows = loaded.get("taskList") is True and TASK_TAG in loaded["checklist"]
        self.step_events = []       # (seq, step, state) of the step events naming a known step, in seq order
        self.unmarked = []          # seqs of the answer events at a question gate (BEH-08)
        self.questions = {}         # seq: (flag type, the step its flag names or None, the step in progress)
        self.gate = {"kind": None, "seq": None, "refuse": False, "reason": None}
        notes = {"stale": "manifest out of date; tracking ticks only",
                 "none": "no manifest for this skill; tracking ticks only",
                 "unverified": "the checklist wasn't seen in the skill-loaded event; using the manifest as is"}
        self.manifest_note = notes.get(manifest_state)
        # The waiver (BEH-19, version 11): the run's first answered waiver answer; a later one and a dismissed one
        # don't count.
        self.waiver_event = next((e for e in events if e["kind"] == "answer" and e.get("answered") is True
                                  and e.get("waiver") in WAIVERS), None)
        self.waiver = self.waiver_event["waiver"] if self.waiver_event else None

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
            if hit is None or joined(command) or e.get("exit") != rule.get("exit", 0):
                return None
            if rule.get("target") == "written" and not any(names_a(t, self.written_before(e["seq"])) for t in tokens):
                return None
            return "%s exit %d" % (PurePosixPath(hit).name, e["exit"])
        if kind == "read" and tool == "Bash":
            command = e.get("command")
            if not isinstance(command, str) or e.get("exit") != rule.get("exit", 0) or not bash_readable(rule["pattern"]):
                return None
            if e["seq"] not in self.token_cache:
                self.token_cache[e["seq"]] = read_tokens(command, self.roots)
            for token in self.token_cache[e["seq"]]:
                if not rule_path_matches(token, rule):
                    continue
                if rule.get("target") == "written" and not names_a(token, self.written_before(e["seq"])):
                    continue
                return "Bash %s" % token
            return None
        path = e.get("path")
        if not isinstance(path, str):
            return None
        if kind == "write" and tool in ("Write", "Edit") and path_matches(path, rule["pattern"]):
            return "%s %s" % (tool, path)
        if kind == "read" and tool in ("Read", "Glob", "Grep"):
            if not rule_path_matches(path, rule):
                return None
            if rule.get("target") == "written" and not names_a(path, self.written_before(e["seq"])):
                return None
            return "%s %s" % (tool, path)
        return None

    def joined_run(self, rule, e):
        """The script's file name when a Bash command names a script rule's script but joins it to another command,
        which hides its exit status (BEH-06, version 7); else None. With target written, a token must also name a
        written file, as for evidence, so a read of the script (cat … | head) isn't reported as a run."""
        command = e.get("command")
        if rule["type"] != "script" or e.get("tool") != "Bash" or not isinstance(command, str) \
                or e.get("error") is True or not joined(command):
            return None
        tokens = command.split()
        hit = next((t for t in tokens if fnmatchcase(PurePosixPath(t).name, rule["pattern"])), None)
        if hit is None:
            return None
        if rule.get("target") == "written":
            written = self.written_before(e["seq"])
            if not any(names_a(t.strip("'\";()|&"), written) for t in tokens):
                return None
        return PurePosixPath(hit).name

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
                joined = self.joined_run(rule, e)
                if joined:
                    step.joined.append((e["seq"], joined))

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

    def take_step(self, e):
        step = self.by_n.get(e["step"])
        if step is None:  # ERR-06
            self.unknown_claims += 1
            return
        self.step_events.append((e["seq"], step.n, e["state"]))
        if e["state"] == "done":  # a claim, as a tick is (BEH-05)
            step.claims.append({"seq": e["seq"], "state": "done", "reason": None})
            step.event_claims.add(e["seq"])

    def take_carried(self):
        """The steps an earlier run carried into this one (BEH-20, version 14): strong evidence of type carried at the
        skill-loaded event's seq; answered names the carried user-owned steps whose answer stands. A number the
        checklist doesn't have, or an answered one that isn't a carried user-owned step, is ignored (ERR-10)."""
        loaded = self.events[0]
        carried = loaded.get("carried") if isinstance(loaded.get("carried"), list) else []
        answered = loaded.get("answered") if isinstance(loaded.get("answered"), list) else []
        resumes = loaded.get("resumes")
        detail = "carried from the earlier run %s" % resumes if isinstance(resumes, str) else "carried from an earlier run"
        taken = set()
        for n in carried:
            if isinstance(n, bool) or not isinstance(n, int) or n not in self.by_n or n in taken:
                continue
            taken.add(n)
            self.by_n[n].evidence.append({"seq": loaded["seq"], "type": "carried", "strength": "strong", "detail": detail})
        for n in answered:
            if not isinstance(n, bool) and isinstance(n, int) and n in taken and self.by_n[n].user_owned:
                self.by_n[n].carried_answer = True

    def collect(self):
        self.take_carried()
        for e in self.events:
            if e["kind"] == "tool":
                self.take_tool(e)
            elif e["kind"] == "reply":
                self.take_reply(e)
            elif e["kind"] == "step":
                self.take_step(e)

    def in_progress(self, upto=INFINITY):
        """The step in progress before `upto`: the step whose latest step event is started, the latest started when
        several are (BEH-07, BEH-18); None when no step is. A mark stands until a step event ends it (version 8)."""
        latest = {}
        for seq, n, state in self.step_events:
            if seq >= upto:
                break
            latest[n] = (state, seq)
        started = [(seq, n) for n, (state, seq) in latest.items() if state == "started"]
        return max(started)[1] if started else None


    # -- gates' positions --

    def write_gate_seq(self):
        if self.write_gate is None:
            return None
        seqs = [x["seq"] for x in self.write_gate.evidence if x["type"] == "write"]
        return min(seqs) if seqs else None

    def report_gate_seq(self):
        if self.report_gate is None:
            return None
        seqs = [c["seq"] for c in self.report_gate.claims if c["state"] == "done"]
        return min(seqs) if seqs else None

    def end_seq(self):
        return self.events[-1]["seq"] if self.events[-1]["kind"] == "run-end" else None

    def gate_seq_for(self, step):
        """The seq of the first gate that checks a step, or INFINITY."""
        seqs = []
        w, r, end = self.write_gate_seq(), self.report_gate_seq(), self.end_seq()
        if w is not None and step.n < self.write_gate.n:
            seqs.append(w)
        if r is not None and step.n < self.report_gate.n:
            seqs.append(r)
        if end is not None:
            seqs.append(end)
        return min(seqs) if seqs else INFINITY

    # -- answers (BEH-09, with the departure recorded in SPEC-012 §9) --

    def window(self, step):
        """(opens, closes, closes without the step's own claim) for a user-owned step."""
        after = [seq for s in self.steps if s.n > step.n for seq in s.signals()]
        hard = min([self.gate_seq_for(step)] + after)
        # "Over the whole log" is bounded by the window's own close: evidence of an earlier step that
        # comes after the gate (a re-read, say) mustn't move the opening past the close.
        # BEH-09 (version 4): each earlier step's start, the later of its first tool evidence and its first claim
        # before the close. A re-read, re-listing or re-tick of a finished step doesn't move the opening; a step ticked
        # only after the answer does. A conditional step that isn't the user's (an inspection) can come at any time.
        before = []
        for s in self.steps:
            if s.n >= step.n or (s.need == "conditional" and not s.user_owned):
                continue
            evidence = [x["seq"] for x in s.evidence if x["type"] not in ("answer", "waiver", "carried") and x["seq"] < hard]
            claims = [c["seq"] for c in s.claims if c["seq"] < hard]
            firsts = ([min(evidence)] if evidence else []) + ([min(claims)] if claims else [])
            if firsts:
                before.append(max(firsts))
        opens = max(before) if before else self.events[0]["seq"]
        return opens, min([hard] + [c["seq"] for c in step.claims]), hard

    def assign_answers(self):
        owned = [s for s in self.steps if s.user_owned]
        answers = []
        for e in self.events:
            if e["kind"] not in ("answer", "prompt"):
                continue
            if e["kind"] == "answer" and "waiver" in e:
                continue  # in every run, a waiver answer is placed by no mark, tag or window, and gates nothing (BEH-18)
            counts = e["kind"] == "prompt" or e["answered"]
            # BEH-18: step events place answers: the step in progress takes each one; a step that isn't the user's
            # keeps it as its own exchange, such as an intake question, so it counts for no user-owned step.
            n = self.in_progress(e["seq"]) if self.step_events else None
            if self.follows and e["kind"] == "answer":
                self.take_tagged(e, n, counts)
            elif n is not None:
                if counts and self.by_n[n].user_owned:
                    self.by_n[n].evidence.append(self.answer_evidence(e))
            elif self.follows and self.tracked:
                pass  # a typed prompt with no step in progress counts for no step and raises nothing (BEH-18)
            elif counts:
                answers.append(e)  # BEH-09's windows place the rest
        if not owned:
            return
        windows = {s.n: self.window(s) for s in owned}
        unplaced = []
        for e in answers:
            step = next((s for s in owned if windows[s.n][0] < e["seq"] < windows[s.n][1]), None)
            if step is None:
                unplaced.append(e)
            else:
                step.evidence.append(self.answer_evidence(e))
        # A step's own claim hands later answers on to the next user-owned step; it doesn't lose them.
        for e in unplaced:
            step = next((s for s in owned if windows[s.n][0] < e["seq"] < windows[s.n][2]), None)
            if step is not None:
                step.evidence.append(self.answer_evidence(e))

    def take_tagged(self, e, n, counts):
        """An answer in a run that follows the task list (BEH-18, version 9). Claude writes both the question's tag and
        the mark, so the tag is a check on the mark, never a placement of its own: the answer counts for the step in
        progress `n` only when its tag names that step. Otherwise it is a question gate whose answer counts for no step,
        checked in this order: no step in progress, no tag, another step's tag. An answer whose question says it is
        outside the checklist, or one asked once every step is reached, is neither: it counts for no step and raises
        nothing (version 10)."""
        tag = e.get("step")
        if isinstance(tag, bool) or not isinstance(tag, int) or tag < 1:
            tag = None  # a tag of another type counts as no tag
        elif tag not in self.by_n:  # ERR-06: a step the checklist doesn't have counts as no tag
            self.unknown_claims += 1
            tag = None
        if tag is None and e.get("outside") is True:
            return
        if n is not None and tag == n:
            if counts and self.by_n[n].user_owned:
                self.by_n[n].evidence.append(self.answer_evidence(e))
            return
        if not self.tracked:
            return  # every gate needs a matched or unverified manifest
        if all(s.reached(e["seq"]) for s in self.steps):
            return  # the checklist is finished: a later question isn't its own, and counts for no step (version 10)
        if n is None:
            kind, named = "unmarked-question", tag
        elif tag is None:
            kind, named = "untagged-question", n
        else:
            kind, named = "mismatched-question", tag
        self.unmarked.append(e["seq"])
        self.questions[e["seq"]] = (kind, named, n)

    def waived(self, step, upto=INFINITY):
        """A Proceed waiver, answered before `upto`, answers a waivable step (BEH-19, version 11)."""
        return (step.waivable and self.waiver == "proceed" and self.tracked
                and self.waiver_event["seq"] < upto)

    def add_waiver_evidence(self):
        """Stamp each waived step's evidence at the first gate or checked write after the waiver that checks it, so it
        isn't reached, current or 'seen late' before then (BEH-19)."""
        if not (self.waiver == "proceed" and self.tracked):
            return
        start = self.waiver_event["seq"]
        w = self.write_gate_seq()
        for step in self.steps:
            if not step.waivable:
                continue
            points = [self.gate_seq_for(step)]
            if w is not None:
                points += [e["seq"] for e in self.events
                           if e["kind"] == "tool" and e["seq"] >= w and e.get("tool") in ("Write", "Edit")
                           and e.get("error") is not True and isinstance(e.get("path"), str)
                           and any(int(rule["step"]) == step.n and path_matches(e["path"], rule["path"])
                                   for rule in self.content_rules)]
            points = [p for p in points if p != INFINITY and p > start]
            if points:
                step.evidence.append({"seq": min(points), "type": "waiver", "strength": "strong",
                                      "detail": "your start-of-run answer: Proceed without questions"})

    @staticmethod
    def answer_evidence(e):
        return {"seq": e["seq"], "type": "answer", "strength": "strong",
                "detail": "answer" if e["kind"] == "answer" else "prompt"}

    # -- gates (BEH-08, BEH-10, BEH-11, BEH-12) --

    def flag(self, new, gate, seq, step, kind, message, once=True):
        if once:
            if (step.n, kind) in self.flagged:
                return
            self.flagged.add((step.n, kind))
        f = {"gate": gate, "seq": seq, "step": step.n, "type": kind, "message": message}
        self.flags.append(f)
        new.append(f)

    def check_steps(self, new, gate, seq, steps):
        for step in steps:
            if step.sticky or step.not_applicable_by_event(seq):
                continue
            if step.user_owned:
                if gate in ("report", "end") and not step.answered(seq) and not self.waived(step, seq) \
                        and not step.unverifiable:
                    step.gate_state, step.gate_note = "not-applicable", "no answer; left open"
                continue
            state = step.base_state(seq)
            joined = [name for s, name in step.joined if s < seq]
            # A run of the step's script whose exit status another command hid: the flag names it (BEH-08, version 7).
            hidden = ("step %d (%s): %s ran, but the command joined it to another, which hides its exit status: run it "
                      "as a command of its own" % (step.n, step.title, joined[-1])) if joined else None
            if state == "pending":
                if step.need == "required":
                    step.gate_state = "skipped"
                    self.flag(new, gate, seq, step, "skipped", hidden or "step %d (%s) has no evidence or tick before %s: expected %s"
                              % (step.n, step.title, GATE_WORDS[gate], step.skipped_expectation()))
                elif step.need == "conditional":
                    step.gate_state, step.gate_note = "not-applicable", step.when or ""
                else:
                    step.gate_state = "unconfirmed"
            elif state == "claimed":
                self.flag(new, gate, seq, step, "claimed-not-evidenced", hidden or "step %d (%s) is ticked, but %s wasn't seen"
                          % (step.n, step.title, step.expected_evidence()))

    def content_of(self, e):
        if isinstance(e.get("content"), str):
            return e["content"]
        if not self.root:
            return None
        root = os.path.realpath(self.root)
        target = os.path.realpath(os.path.join(root, e["path"]))
        if target != root and not target.startswith(root + os.sep):
            return None
        try:
            with open(target, encoding="utf-8") as f:
                return f.read()
        except (OSError, UnicodeDecodeError):
            return None

    def check_content(self, new, e):
        for rule in self.content_rules:
            if not path_matches(e["path"], rule["path"]):
                continue
            step = self.by_n[int(rule["step"])]
            if step.answered(e["seq"]) or self.waived(step, e["seq"]):
                continue
            text = self.content_of(e)
            if text is None:
                step.unverifiable = True
                continue
            bad = [v for v in field_values(text, rule["field"], rule["scope"]) if v not in rule["allowed"]]
            if bad:
                step.sticky = "skipped"
                self.flag(new, "write", e["seq"], step, "skipped", "step %d (%s) had no answer from you before %s was written"
                          % (step.n, step.title, e["path"]))
                self.write_gate.sticky = "rule-broken"
                self.flag(new, "write", e["seq"], self.write_gate, "rule-broken",
                          "%s sets %s: %s, which needs your answer at step %d" % (e["path"], rule["field"], bad[0], step.n),
                          once=False)
            elif step.sticky is None:
                step.gate_state, step.gate_note = "not-applicable", "no answer; left open"

    def check_gates(self):
        if not self.tracked:
            return
        w, r, end = self.write_gate_seq(), self.report_gate_seq(), self.end_seq()
        content = {}
        if w is not None:
            for e in self.events:
                if e["kind"] == "tool" and e["seq"] >= w and e.get("tool") in ("Write", "Edit") \
                        and e.get("error") is not True and isinstance(e.get("path"), str) \
                        and any(path_matches(e["path"], rule["path"]) for rule in self.content_rules):
                    content[e["seq"]] = e
        questions = self.questions
        points = sorted({p for p in (w, r, end) if p is not None} | set(content) | set(questions))
        for seq in points:
            new = []
            if seq in questions:
                # The question gate checks no step. Its flag names the question's tagged step, or an untagged one's
                # step in progress, or, with neither, the step the run would reach next (versions 6 and 9).
                kind, named, marked = questions[seq]
                message = {"unmarked-question": UNMARKED, "untagged-question": UNTAGGED,
                           "mismatched-question": MISMATCHED.format(n=named, k=marked)}[kind]
                step = self.by_n[named if named is not None else self.next_to_reach(seq)]
                self.flag(new, "question", seq, step, kind, message, once=False)
            if seq == w:
                self.check_steps(new, "write", seq, [s for s in self.steps if s.n < self.write_gate.n])
            if seq in content:
                self.check_content(new, content[seq])
            if seq == r:
                self.check_steps(new, "report", seq, [s for s in self.steps if s.n < self.report_gate.n])
            if seq == end:
                highest = self.highest_reached()
                if highest is not None:
                    self.check_steps(new, "end", seq, [s for s in self.steps if s.n <= highest])
            kind = "end" if seq == end else "report" if seq == r else "question" if seq in questions else "write"
            self.gate = {"kind": kind, "seq": seq, "refuse": bool(new), "reason": new[0]["message"] if new else None}

    # -- positions --

    def highest_reached(self, upto=INFINITY):
        reached = [s.n for s in self.steps if s.reached(upto)]
        return max(reached) if reached else None

    def next_to_reach(self, upto):
        """The step after the highest reached before `upto`, or the last step when every step is reached."""
        highest = self.highest_reached(upto)
        later = [s.n for s in self.steps if highest is None or s.n > highest]
        return later[0] if later else self.steps[-1].n

    def current(self):
        if self.end_seq() is not None or not self.steps:
            return None
        if self.step_events:
            n = self.in_progress()
            if n is not None:
                return n
        highest = self.highest_reached()
        if highest is None:
            return self.steps[0].n
        later = [s.n for s in self.steps if s.n > highest]
        return later[0] if later else None

    # -- the next step (BEH-13) --

    def next_step(self, skill):
        report_done = self.report_gate is not None and self.final_state(self.report_gate) == "done"
        if not (report_done or self.end_seq() is not None):
            return None
        if skill not in CHAIN or skill == CHAIN[-1]:
            return None
        following = CHAIN[CHAIN.index(skill) + 1]
        if following in NOT_BUILT:
            return {"skill": following, "available": False, "note": NOT_BUILT[following]}
        return {"skill": following, "available": True, "note": ""}

    # -- assembling the state --

    def final_state(self, step):
        if step.sticky:
            return step.sticky
        if step.not_applicable_by_event():
            return "not-applicable"
        base = step.base_state()
        if base == "claimed" and step.gate_state == "not-applicable":
            return "not-applicable"
        if base in ("done", "claimed", "skipped-with-reason", "carried"):
            return base
        return step.gate_state or "pending"

    def step_notes(self, current):
        ended = self.end_seq() is not None
        highest = self.highest_reached()
        for step in self.steps:
            state, note = self.final_state(step), ""
            if step.unverifiable and not step.sticky and state != "not-applicable":
                note = "content not available; rule not checked"
            elif state == "not-applicable":
                note = (step.when or "") if step.not_applicable_by_event() else step.gate_note
            else:
                first = step.first_signal()
                if first is not None:
                    earlier = [s.n for s in self.steps if s.n > step.n and s.first_signal() is not None
                               and s.first_signal() < first]
                    if earlier:
                        note = "seen late (after step %d)" % max(earlier)
                if not note and state == "pending":
                    if highest is not None and step.n > highest and (ended or current is None):
                        note = "not reached"
                    elif ended and highest is None:
                        note = "not reached"
                    elif current is not None and step.n < current:
                        note = "not seen yet"
            step.note = note
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
            if step.stoppable:
                records[-1]["stoppable"] = True  # version 12: only a stoppable step carries the field (DM-03)
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
    run.assign_answers()
    run.add_waiver_evidence()
    run.check_gates()
    counts = dict(counts, unknownClaims=run.unknown_claims, unmarkedQuestions=len(run.unmarked),
                  stepEvents=len(run.step_events))  # the step events naming a step the checklist has
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
        "next": run.next_step(skill),
        "counts": counts,
        "waiver": run.waiver,
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
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=folder, prefix=".state-", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, out)
    except OSError as e:
        if tmp is not None and os.path.exists(tmp):  # leave nothing but --out behind (QR-04)
            try:
                os.remove(tmp)
            except OSError:
                pass
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
