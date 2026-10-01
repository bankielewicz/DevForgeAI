"""Checks the context eval graders offline, with good and bad simulated runs (SPEC-011 §11 step 2).

For each case with regex or file_exists graders, after running its scaffold:
- a correct run (golden.good) passes every grader, and the skill's context_check.py check --snapshot;
- each targeted wrong run (golden.bad) fails exactly the graders it names;
- every grader fails in at least one wrong run: a run that writes nothing and says nothing, an automatic
  mutation (a changed byte for a whole-content grader, the file a file_exists-false grader forbids, the
  witness text of a not_contains grader), or a targeted run.
tool_used graders (VER-20, VER-26) can't be graded offline and are skipped.

Run from the repository root after make_evals.py, under the normal HOME (it imports make_evals):
    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/context/check_graders.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import golden as G  # noqa: E402
import make_evals as M  # noqa: E402

GRADE = Path("src/tests/context/grade_evals.mjs").resolve()


def grade(case, files, reply):
    """Runs the scaffold, applies the run's files (None deletes), and grades. Returns {grader: bool}."""
    case_dir = (M.ROOT / case.name).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        M.run_scaffold(case_dir, ws)
        for path, text in files.items():
            p = ws / path
            if text is None:
                p.unlink()
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text)
        (Path(tmp) / "reply.txt").write_text(reply)
        (Path(tmp) / "seeded.json").write_text(json.dumps(sorted(case.files)))
        out = subprocess.run(["node", str(GRADE), str(case_dir), str(ws), str(Path(tmp) / "reply.txt"),
                              str(Path(tmp) / "seeded.json")], capture_output=True, text=True, check=True)
    return {k: v for k, v in json.loads(out.stdout).items() if v is not None}


def script_check(case, files):
    """The correct run also passes the skill's context_check.py, checked against a snapshot of the scaffold
    (so a seeded document the case marks invalid, and leaves alone, is 'unchanged, invalid')."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        ws.mkdir()
        M.run_scaffold((M.ROOT / case.name).resolve(), ws)
        script = str(M.CONTEXT_CHECK.resolve())
        start = Path(tmp) / "start"
        subprocess.run([sys.executable, "-B", script, "snapshot", str(start)], cwd=ws, check=True, capture_output=True)
        for path, text in files.items():
            p = ws / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        out = subprocess.run([sys.executable, "-B", script, "check", "--snapshot", str(start)], cwd=ws,
                             capture_output=True, text=True)
    return out.returncode, out.stdout


def failing(results):
    return {k for k, v in results.items() if not v}


def apply(case, files, reply, edits):
    files = dict(files)
    for kind, path, old, new, count in edits:
        if kind == "reply":
            assert reply.count(old) == count, f"{case.name}: reply lacks {old!r}"
            reply = reply.replace(old, new)
        else:
            text = files[path] if path in files else case.files[path]
            assert text.count(old) == count, f"{case.name}: {path} has {text.count(old)} of {old!r}"
            files[path] = text.replace(old, new)
    return files, reply


def mutations(case, files, reply):
    """Automatic wrong runs: (grader, files, reply) where the grader must fail."""
    for g in case.graders:
        if g.type == "file_exists" and g.exists is False:
            path = g.target[:-3] + "/stray.md" if g.target.endswith("/**") else g.target
            yield g.name, dict(files, **{path: "stray\n"}), reply
        elif g.type == "regex" and g.match == "contains" and g.pattern.startswith("^") and g.pattern.endswith("$") \
                and g.target != "last_message" and ("-unchanged" in g.name):
            text = files.get(g.target, case.files.get(g.target))
            yield g.name, dict(files, **{g.target: text.replace("\n", " \n", 1)}), reply
        elif g.type == "regex" and g.match == "not_contains" and g.witness is not None:
            if g.target == "last_message":
                yield g.name, files, reply + g.witness
            else:
                text = files.get(g.target, case.files.get(g.target))
                yield g.name, dict(files, **{g.target: text + g.witness}), reply


def main():
    if not M.ROOT.is_dir():
        sys.exit("Run make_evals.py first, from the repository root.")
    problems, checked, runs = [], 0, 0
    for case in M.CASES:
        if all(g.type == "tool_used" for g in case.graders):
            continue
        files, reply = G.good(case)
        good = grade(case, files, reply)
        runs += 1
        names = set(good)
        caught = set()
        if failing(good):
            problems.append(f"{case.name}: the correct run fails {sorted(failing(good))}")
        code, out = script_check(case, files)
        if code != 0:
            problems.append(f"{case.name}: the correct run fails context_check.py:\n{out}")
        empty = failing(grade(case, {}, ""))
        runs += 1
        caught |= empty
        for name, mfiles, mreply in mutations(case, files, reply):
            got = failing(grade(case, mfiles, mreply))
            runs += 1
            if name not in got:
                problems.append(f"{case.name}: the mutation for {name} doesn't fail it")
            caught |= got
        for label, edits, expected in G.bad(case):
            bfiles, breply = apply(case, files, reply, edits)
            got = failing(grade(case, bfiles, breply))
            runs += 1
            if got != expected:
                problems.append(f"{case.name}: '{label}' fails {sorted(got)}, expected {sorted(expected)}")
            caught |= got
        for name in sorted(names - caught):
            problems.append(f"{case.name}: {name} never fails in any wrong run")
        checked += len(names)
    for p in problems:
        print("PROBLEM", p)
    print(f"{checked} graders checked over {runs} simulated runs: "
          + (f"{len(problems)} problem(s)" if problems else "every grader passes the correct run and fails a wrong one"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
