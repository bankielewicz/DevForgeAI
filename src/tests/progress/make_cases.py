#!/usr/bin/env python3
"""Generate SPEC-012's test cases for the progress evaluator.

Each case is a folder under cases/ holding:
- events.jsonl: the run's event log (devforgeai-events/1), one JSON object per line;
- args.json: how test_evaluate.py runs the evaluator on it: the manifest folders in layer order
  ("@plugin" is the plugin's own folder; other paths are relative to the case folder), and the
  optional --root and --phases paths;
- any manifests, root files or phases file the case needs;
- expected.json: the evaluator's output, written by --write-expected once the property tests pass
  and reviewed against the case's VER item.

Everything is deterministic: fixed times, fixed run IDs, and checklists read from the skills'
SKILL.md, so regenerating gives byte-identical files.

Run from the repository root:
    python3 -B src/tests/progress/make_cases.py                   write the cases
    python3 -B src/tests/progress/make_cases.py --check           exit 1 if a generated file would change
    python3 -B src/tests/progress/make_cases.py --write-expected  also write expected.json for each case
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SKILLS = ROOT / "src/claude/DevForgeAI/skills"
PLUGIN_MANIFESTS = "src/claude/DevForgeAI/progress/manifests"
EVALUATE = "src/claude/DevForgeAI/progress/evaluate.py"
CASES = HERE / "cases"
T0 = datetime(2026, 10, 2, 12, 0, 0, tzinfo=timezone.utc)
CHECKLIST_LINE = re.compile(r"^\s*- \[ \] (\d+)\. (.+?)\s*$")


def checklist_block(skill):
    """The checklist lines of a skill's SKILL.md, as written."""
    text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    return "\n".join(line for line in text.splitlines() if CHECKLIST_LINE.match(line))


def checklist_hash(text):
    """SPEC-012 §4's hash, written separately from evaluate.py's so the two can check each other."""
    rebuilt = []
    for line in text.splitlines():
        m = CHECKLIST_LINE.match(line)
        if m:
            rebuilt.append("- [ ] %s. %s" % (m.group(1), m.group(2)))
    return "sha256:" + hashlib.sha256("\n".join(rebuilt).encode("utf-8")).hexdigest()


class Log:
    """Builds one run's events with fixed run ID, seq and times."""

    def __init__(self, skill, checklist=None, run_suffix="0000abcd"):
        self.run = "20261002T120000Z-%s-%s" % (skill, run_suffix)
        self.events = []
        self.add("skill-loaded", format="devforgeai-events/1", skill=skill,
                 checklist=checklist if checklist is not None else checklist_block(skill),
                 host="claude-code 2.1.287")

    def add(self, kind, **fields):
        seq = len(self.events) + 1
        event = {"run": self.run, "seq": seq, "kind": kind,
                 "time": (T0 + timedelta(seconds=seq)).strftime("%Y-%m-%dT%H:%M:%SZ")}
        event.update({k: v for k, v in fields.items() if v is not None})
        self.events.append(event)
        return self

    def tool(self, tool, path=None, command=None, exit_code=None, error=None, content=None):
        return self.add("tool", tool=tool, path=path, command=command, exit=exit_code, error=error,
                        content=content)

    def bash(self, command, exit_code=0):
        return self.tool("Bash", command=command, exit_code=exit_code)

    def read(self, path):
        return self.tool("Read", path=path)

    def glob(self, pattern):
        return self.tool("Glob", path=pattern)

    def write(self, path, content=None):
        return self.tool("Write", path=path, content=content)

    def answer(self, answered=True):
        return self.add("answer", answered=answered)

    def prompt(self):
        return self.add("prompt")

    def reply(self, text):
        return self.add("reply", text=text)

    def tick(self, *steps):
        return self.reply("\n".join("- [x] %d. done" % n for n in steps))

    def turn(self, phase):
        return self.add("turn", phase=phase)

    def end(self, reason):
        return self.add("run-end", reason=reason)

    def lines(self):
        return [json.dumps(e, sort_keys=True, ensure_ascii=False) for e in self.events]


# ---- document contents ------------------------------------------------------------------------

def brn(dispositions, status="draft", reasons=None):
    ideas = []
    for i, d in enumerate(dispositions, 1):
        reason = (reasons or {}).get(i, "null")
        ideas.append('  - id: IDEA-%02d\n    status: active\n    idea: "Idea %d"\n'
                     "    disposition: %s\n    reason: %s" % (i, i, d, reason))
    return ("---\nid: BRN-002\ntype: brainstorm\ntitle: \"Getting teens into the library\"\n"
            "status: %s\nversion: 1\n---\n\n# BRN-002\n\n```yaml items\nideas:\n%s\n```\n"
            % (status, "\n".join(ideas)))


def arch(outcome="null"):
    return ("---\nid: ARCH-001\ntype: arch\nstatus: draft\nversion: 1\noutcome: %s\n---\n\n"
            "# ARCH-001\n" % outcome)


def adr(status="accepted"):
    return "---\nid: ADR-004\ntype: adr\nstatus: %s\nversion: 1\n---\n\n# ADR-004\n" % status


POLICY = "python3 .claude/skills/devforgeai/skills/architecture/scripts/validate_policy.py docs/specs/policy"
VALIDATE = ("python3 .claude/skills/devforgeai/skills/brainstorm/scripts/validate_brn.py "
            "docs/specs/brainstorm/BRN-002.md")
VALIDATE_OTHER = ("python3 .claude/skills/devforgeai/skills/brainstorm/scripts/validate_brn.py "
                  "docs/specs/brainstorm/BRN-001.md")
BRN_PATH = "docs/specs/brainstorm/BRN-002.md"
ARCH_PATH = "docs/specs/arch/ARCH-001.md"
ADR_PATH = "docs/specs/adr/ADR-004.md"
PROMOTED = ["promoted"] * 9 + ["open"] * 6


def arch_start(log):
    return log.bash(POLICY).glob("docs/specs/prd/PRD-*.md").read("docs/specs/prd/PRD-001.md")


def arch_to_six(log):
    return arch_start(log).glob("docs/specs/arch/ARCH-*.md").tick(1, 2, 3, 4, 6)


def brn_start(log):
    return log.glob("docs/specs/brainstorm/BRN-*.md").tick(1, 2, 3, 4)


# ---- cases --------------------------------------------------------------------------------------
# Each builder returns (log, args, extra files {relative path: text}).

CASE_BUILDERS = {}


def case(name):
    def register(fn):
        CASE_BUILDERS[name] = fn
        return fn
    return register


def plugin_only(**extra):
    args = {"manifests": ["@plugin"], "root": None, "phases": None}
    args.update(extra)
    return args


@case("arch-reading")  # VER-03, the prototype's moment 1
def _():
    return arch_start(Log("architecture")), plugin_only(), {}


@case("arch-late-step-before")  # VER-04, cut before the late Glob
def _():
    return arch_start(Log("architecture")).tick(1, 2, 3).tick(6), plugin_only(), {}


@case("arch-late-step")  # VER-04
def _():
    log = arch_start(Log("architecture")).tick(1, 2, 3).tick(6).glob("docs/specs/arch/ARCH-*.md")
    return log, plugin_only(), {}


@case("arch-your-turn-waiting")  # VER-05, moment 3
def _():
    return arch_to_six(Log("architecture")).turn("end"), plugin_only(), {}


@case("arch-your-turn")  # VER-05
def _():
    return arch_to_six(Log("architecture")).turn("end").answer(), plugin_only(), {}


@case("arch-outcome-unconfirmed")  # VER-06, moment 4 as the architecture skill's rules have it
def _():
    log = arch_to_six(Log("architecture")).answer().answer().answer()
    log.write(ADR_PATH, adr("accepted")).write(ARCH_PATH, arch("create"))  # ADRs first, as SKILL.md step 9
    return log, plugin_only(), {}


@case("arch-outcome-confirmed")  # VER-06's variant
def _():
    log = arch_to_six(Log("architecture")).answer().answer().answer().tick(7).answer()
    log.write(ADR_PATH, adr("accepted")).write(ARCH_PATH, arch("create"))  # ADRs first, as SKILL.md step 9
    return log, plugin_only(), {}


@case("arch-adr-accepted-unanswered")  # VER-07
def _():
    return arch_to_six(Log("architecture")).write(ADR_PATH, adr("accepted")), plugin_only(), {}


@case("arch-adr-proposed-unanswered")  # VER-07's variant
def _():
    return arch_to_six(Log("architecture")).write(ADR_PATH, adr("proposed")), plugin_only(), {}


@case("brn-left-open")  # VER-08, moment 5, SPEC-001 VER-02's path
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(["open"] * 15)).bash(VALIDATE)
    return log.tick(6, 7).tick(8), plugin_only(), {}


@case("brn-unconfirmed")  # VER-09
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(PROMOTED)).bash(VALIDATE)
    return log.tick(6, 7).tick(8), plugin_only(), {}


@case("brn-unconfirmed-cut")  # VER-17, brn-unconfirmed's log cut after the BRN write
def _():
    return brn_start(Log("brainstorm")).write(BRN_PATH, brn(PROMOTED)), plugin_only(), {}


@case("brn-unconfirmed-status")  # VER-09's variant
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(["open"] * 15, status="converged"))
    return log.bash(VALIDATE).tick(6, 7).tick(8), plugin_only(), {}


@case("brn-answer-early")  # VER-10
def _():
    log = Log("brainstorm").glob("docs/specs/brainstorm/BRN-*.md").answer().tick(1, 2, 3, 4)
    return log.write(BRN_PATH, brn(PROMOTED)), plugin_only(), {}


@case("brn-answer-after")  # VER-10's variant
def _():
    log = Log("brainstorm").glob("docs/specs/brainstorm/BRN-*.md").answer().tick(1, 2, 3, 4).answer()
    return log.write(BRN_PATH, brn(PROMOTED)), plugin_only(), {}


@case("brn-ticked-then-answered")  # BEH-09 departure: step 5 ticked as Claude asks; the answer still counts
def _():
    log = Log("brainstorm").glob("docs/specs/brainstorm/BRN-*.md").tick(1, 2, 3, 4, 5).answer()
    return log.write(BRN_PATH, brn(PROMOTED)), plugin_only(), {}


@case("brn-validation-claimed")  # VER-11
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(["open"] * 15))
    return log.tick(6, 7).tick(8), plugin_only(), {}


@case("brn-validation-failed")  # VER-11's variant: the script exits 1
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(["open"] * 15)).bash(VALIDATE, exit_code=1)
    return log.tick(6, 7).tick(8), plugin_only(), {}


@case("brn-validation-other-file")  # VER-11's variant: the script checks another file
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(["open"] * 15)).bash(VALIDATE_OTHER)
    return log.tick(6, 7).tick(8), plugin_only(), {}


@case("brn-root-file")  # BEH-10's --root branch: the Write carries no content
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH)
    return log, plugin_only(root="root"), {"root/" + BRN_PATH: brn(PROMOTED)}


SHIPIT = ("- [ ] 1. Gather the changes\n- [ ] 2. Read the release notes\n- [ ] 3. Push\n"
          "- [ ] 4. Report")


@case("skipped-with-reason")  # VER-12, a manifest of its own in the case folder
def _():
    manifest = {
        "format": "devforgeai-manifest/1", "skill": "shipit", "checklistHash": checklist_hash(SHIPIT),
        "steps": {
            "1": {"title": "Gather the changes", "kind": "think", "need": "text-only"},
            "2": {"title": "Read the release notes", "kind": "read", "need": "required",
                  "evidence": [{"type": "read", "pattern": "docs/"}]},
            "3": {"title": "Push", "kind": "forge", "need": "required",
                  "evidence": [{"type": "script", "pattern": "push.sh"}]},
            "4": {"title": "Report", "kind": "report", "need": "required", "gate": "report"}}}
    log = Log("shipit", checklist=SHIPIT).read("docs/RELEASE.md").tick(1, 2)
    log.reply("- [x] 3. Push (skipped: no remote)").tick(4)
    return log, {"manifests": ["manifests"], "root": None, "phases": None}, {
        "manifests/shipit.json": json.dumps(manifest, indent=2) + "\n"}


@case("stale-manifest")  # VER-13: one title differs from the manifest's hashed text
def _():
    stale = checklist_block("brainstorm").replace("6. Write the BRN", "6. Write the BRN file")
    return Log("brainstorm", checklist=stale).tick(1, 2, 3), plugin_only(), {}


@case("no-manifest")  # VER-13: prd has no manifest yet
def _():
    return Log("prd").tick(1, 2), plugin_only(), {}


@case("evidence-only")  # VER-14: no reply events at all
def _():
    log = arch_start(Log("architecture")).glob("docs/specs/arch/ARCH-*.md").answer().answer()
    log.write(ADR_PATH, adr("accepted")).write(ARCH_PATH, arch("null")).read(ARCH_PATH)
    return log.end("another-skill"), plugin_only(), {}


@case("phases")  # VER-17: --phases is copied unchanged
def _():
    log = brn_start(Log("brainstorm")).write(BRN_PATH, brn(["open"] * 15)).bash(VALIDATE)
    phases = {"note": "a later spec defines phases", "list": ["brainstorm", "prd"]}
    return log.tick(6, 7).tick(8), plugin_only(phases="phases.json"), {
        "phases.json": json.dumps(phases, indent=2) + "\n"}


@case("epic-ended")  # VER-17: next after epic is story, which isn't built
def _():
    return Log("epic").tick(1, 2).end("another-skill"), plugin_only(), {}


@case("layer-adds-rule")  # VER-20: a project layer adds a content rule
def _():
    plugin = json.loads((ROOT / PLUGIN_MANIFESTS / "brainstorm.json").read_text(encoding="utf-8"))
    project = dict(plugin)  # a later layer restates the earlier one in full, then adds (BEH-17)
    project["contentRules"] = plugin["contentRules"] + [
        {"step": 5, "path": "docs/specs/brainstorm/BRN-*.md", "field": "reason", "scope": "anywhere",
         "allowed": ["null"]}]
    content = brn(["open"] * 15, reasons={2: '"keeps-teens"'})
    log = brn_start(Log("brainstorm")).write(BRN_PATH, content)
    return log, {"manifests": ["@plugin", "project"], "root": None, "phases": None}, {
        "project/brainstorm.json": json.dumps(project, indent=2) + "\n"}


TEAM_REVIEW = "- [ ] 1. Gather the reviews\n- [ ] 2. Report"


@case("layer-own-skill")  # VER-20: a project's own skill, which the plugin lacks
def _():
    manifest = {"format": "devforgeai-manifest/1", "skill": "team-review",
                "checklistHash": checklist_hash(TEAM_REVIEW),
                "steps": {"1": {"title": "Gather the reviews", "kind": "read", "need": "required",
                                "evidence": [{"type": "read", "pattern": "reviews/"}]},
                          "2": {"title": "Report", "kind": "report", "need": "required", "gate": "report"}}}
    log = Log("team-review", checklist=TEAM_REVIEW).read("reviews/2026-10-02.md").tick(1, 2)
    return log, {"manifests": ["@plugin", "project"], "root": None, "phases": None}, {
        "project/team-review.json": json.dumps(manifest, indent=2) + "\n"}


@case("messy-log")  # VER-15: ERR-01, ERR-02, ERR-05, ERR-06, BEH-12, QR-04
def _():
    log = Log("brainstorm").glob("docs/specs/brainstorm/BRN-*.md").tick(1, 2, 3, 4)
    log.reply("- [x] 40. Not a step").write(BRN_PATH).end("session-end").tick(5).read("docs/x.md")
    lines = log.lines()
    no_seq = dict(log.events[1]); del no_seq["seq"]
    other_run = dict(log.events[1]); other_run["run"] = "20261002T120000Z-brainstorm-ffffffff"
    other_run["seq"] = 900
    duplicate = dict(log.events[1]); duplicate["kind"] = "prompt"; duplicate.pop("path", None)
    duplicate.pop("tool", None)
    out = [lines[0], "this line is not JSON", lines[1],
           json.dumps(duplicate, sort_keys=True),              # repeats seq 2: dropped (duplicates 1)
           json.dumps(no_seq, sort_keys=True),                 # malformed
           json.dumps(other_run, sort_keys=True),              # malformed (another run)
           lines[3], lines[2]] + lines[4:]                     # seq 3 after seq 4 (outOfOrder 1)
    return out, plugin_only(), {}


# ---- version 2 -----------------------------------------------------------------------------------

LIST_BRNS = "for f in docs/specs/brainstorm/*.md; do head -3 $f; done"


@case("bash-reads")  # VER-22: a Bash listing of the folder is step 1's read evidence
def _():
    log = Log("brainstorm").bash(LIST_BRNS).tick(2, 3, 4).write(BRN_PATH, brn(["open"] * 15))
    return log, plugin_only(), {}


@case("bash-reads-failed")  # VER-22 and VER-24: the listing exits 2, so the write gate flags step 1
def _():
    log = Log("brainstorm").bash(LIST_BRNS, exit_code=2).tick(2, 3, 4).write(BRN_PATH, brn(["open"] * 15))
    return log, plugin_only(), {}


@case("bash-reads-error")  # VER-22: a call with error true is never evidence
def _():
    log = Log("brainstorm").tool("Bash", command=LIST_BRNS, exit_code=0, error=True).tick(2, 3, 4)
    return log.write(BRN_PATH, brn(["open"] * 15)), plugin_only(), {}


@case("bash-reads-forms")  # VER-22: a leading ./ and quotes are read past
def _():
    log = Log("brainstorm").bash("ls ./docs/specs/brainstorm/").bash('ls "docs/specs/brainstorm/"')
    return log.bash("ls 'docs/specs/brainstorm'"), plugin_only(), {}


@case("arch-bash-reads")  # VER-22: cat of the PRD meets steps 2 and 3; grep of the written ARCH meets step 10
def _():
    log = Log("architecture").bash(POLICY).bash("cat docs/specs/prd/PRD-001.md").tick(1, 2, 3, 4, 6)
    log.answer().answer().tick(7).answer().write(ARCH_PATH, arch("create"))
    log.bash("grep -n outcome docs/specs/arch/ARCH-002.md").bash("grep -n outcome docs/specs/arch/ARCH-001.md")
    return log, plugin_only(), {}


@case("arch-inspect")  # VER-23: only a read outside docs/specs/, .claude/ and devforgeai/ is step 5's evidence
def _():
    log = arch_start(Log("architecture")).read(".claude/devforgeai.local.md").read("devforgeai/progress/current.json")
    log.read("/home/u/.claude/plugins/devforgeai/skills/architecture/references/output-rules.md")
    log.bash("cat src/booking/service.py").tool("Grep", path=".").read("src/booking/service.py")
    return log, plugin_only(), {}


DECIDE = ("- [ ] 1. Gather\n- [ ] 2. Decide\n- [ ] 3. Inspect\n- [ ] 4. Check\n- [ ] 5. Write\n"
          "- [ ] 6. Report")


@case("no-rule-step")  # VER-24: the skipped flag's message for a step with no rule, a read with exclude, a script
def _():
    manifest = {
        "format": "devforgeai-manifest/1", "skill": "decide", "checklistHash": checklist_hash(DECIDE),
        "steps": {
            "1": {"title": "Gather", "kind": "read", "need": "required",
                  "evidence": [{"type": "read", "pattern": "notes/"}]},
            "2": {"title": "Decide", "kind": "think", "need": "required"},
            "3": {"title": "Inspect", "kind": "read", "need": "required",
                  "evidence": [{"type": "read", "pattern": "*", "exclude": ["notes/", "out/"]}]},
            "4": {"title": "Check", "kind": "inspect", "need": "required",
                  "evidence": [{"type": "script", "pattern": "check.sh"}]},
            "5": {"title": "Write", "kind": "forge", "need": "required", "gate": "write",
                  "evidence": [{"type": "write", "pattern": "out/*.md"}]},
            "6": {"title": "Report", "kind": "report", "need": "required", "gate": "report"}}}
    log = Log("decide", checklist=DECIDE).read("notes/a.md").write("out/x.md")
    return log, {"manifests": ["manifests"], "root": None, "phases": None}, {
        "manifests/decide.json": json.dumps(manifest, indent=2) + "\n"}


# ---- version 3 -----------------------------------------------------------------------------------

def brn_answered():
    return Log("brainstorm").glob("docs/specs/brainstorm/BRN-*.md").tick(1, 2, 3, 4).reply("Confirm these?").answer()


def arch_answered():
    return arch_to_six(Log("architecture")).answer().answer().tick(7).answer()


@case("answer-then-listing")  # VER-26: a listing to pick the ID, after step 5's answer, doesn't lose it
def _():
    log = brn_answered().bash("ls docs/specs/brainstorm/").write(BRN_PATH, brn(PROMOTED))
    return log, plugin_only(), {}


@case("answer-then-reticks")  # VER-26: a checklist ticked again after the answer doesn't lose it
def _():
    log = brn_answered().tick(1, 2, 3, 4, 5).write(BRN_PATH, brn(PROMOTED))
    return log, plugin_only(), {}


@case("arch-answer-then-listing")  # VER-26: architecture's listing to pick the ID, after step 8's answer
def _():
    log = arch_answered().bash("ls docs/specs/arch/ docs/specs/adr/").write(ARCH_PATH, arch("create"))
    return log, plugin_only(), {}


@case("arch-answer-then-inspection")  # VER-26: step 5's inspection after step 8's answer
def _():
    log = arch_answered().read("README.md").tool("Grep", path=".").write(ARCH_PATH, arch("create"))
    return log, plugin_only(), {}


@case("arch-dot-paths")  # VER-27: ./ tool paths read like the rest
def _():
    log = Log("architecture").bash(POLICY).glob("./docs/specs/prd/PRD-*.md").read("./docs/specs/prd/PRD-001.md")
    return log, plugin_only(), {}


# ---- version 4 -----------------------------------------------------------------------------------

@case("intake-then-tick")  # VER-28: step 1 ticked only after the answer: the answer was intake's, not step 5's
def _():
    log = Log("brainstorm").glob("docs/specs/brainstorm/BRN-*.md").answer().reply("- [x] 1. done")
    return log.write(BRN_PATH, brn(PROMOTED)), plugin_only(), {}


@case("arch-retick-after-answer")  # VER-28: pins the limit §13 names; its expected state is versions 3 and 4's verdict
def _():
    log = arch_start(Log("architecture")).glob("docs/specs/arch/ARCH-*.md").tick(1, 2, 3, 4, 6)
    log.reply("- [x] 7. Which queue: SQS (Recommended) or Kafka?").answer().reply("- [x] 7. done")
    return log.write(ADR_PATH, adr("accepted")).write(ARCH_PATH, arch("create")), plugin_only(), {}


@case("write-dot-path")  # VER-29: a Write's ./ path reaches the write gate
def _():
    return brn_start(Log("brainstorm")).write("./" + BRN_PATH, brn(PROMOTED)), plugin_only(), {}


# ---- writing ------------------------------------------------------------------------------------

def generated():
    """{relative path under cases/: text} for every generated file."""
    files = {}
    for name, build in CASE_BUILDERS.items():
        log, args, extra = build()
        lines = log if isinstance(log, list) else log.lines()
        files[name + "/events.jsonl"] = "\n".join(lines) + "\n"
        files[name + "/args.json"] = json.dumps(args, indent=2, sort_keys=True) + "\n"
        for rel, text in extra.items():
            files[name + "/" + rel] = text
    return files


def evaluate_args(name, out, interpreter=(sys.executable, "-B")):
    """The command that runs evaluate.py on a case, with paths relative to the repository root."""
    folder = CASES / name
    args = json.loads((folder / "args.json").read_text(encoding="utf-8"))
    rel = lambda p: str(p.relative_to(ROOT))
    cmd = list(interpreter) + [EVALUATE, "evaluate"]
    for m in args["manifests"]:
        cmd += ["--manifests", PLUGIN_MANIFESTS if m == "@plugin" else rel(folder / m)]
    cmd += ["--events", rel(folder / "events.jsonl"), "--out", str(out)]
    if args.get("root"):
        cmd += ["--root", rel(folder / args["root"])]
    if args.get("phases"):
        cmd += ["--phases", rel(folder / args["phases"])]
    return cmd


def main(argv):
    files = generated()
    if "--check" in argv:
        stale = [p for p, t in files.items()
                 if not (CASES / p).exists() or (CASES / p).read_text(encoding="utf-8") != t]
        for p in stale:
            print("would change: cases/" + p)
        return 1 if stale else 0
    for name in CASE_BUILDERS:
        folder = CASES / name
        if folder.exists():
            keep = folder / "expected.json"
            saved = keep.read_text(encoding="utf-8") if keep.exists() else None
            shutil.rmtree(folder)
            if saved is not None:
                folder.mkdir(parents=True)
                keep.write_text(saved, encoding="utf-8")
    for rel, text in sorted(files.items()):
        path = CASES / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print("wrote %d files in %d cases" % (len(files), len(CASE_BUILDERS)))
    if "--write-expected" in argv:
        for name in CASE_BUILDERS:
            out = CASES / name / "expected.json"
            proc = subprocess.run(evaluate_args(name, out), cwd=ROOT, capture_output=True, text=True)
            if proc.returncode != 0:
                print("%s: exit %d: %s" % (name, proc.returncode, proc.stderr.strip()))
                return 1
        print("wrote expected.json for %d cases" % len(CASE_BUILDERS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
