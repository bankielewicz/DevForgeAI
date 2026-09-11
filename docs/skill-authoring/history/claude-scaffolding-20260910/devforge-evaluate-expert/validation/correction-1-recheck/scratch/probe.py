#!/usr/bin/env python3
"""Independent evaluator probe: run named inputs against the graders at two commits.

Loads both grader modules by absolute path, writes each probe's fixture files under
the evaluator's own scratch root, and prints one row per (probe, commit).
Nothing here writes inside the candidate package.
"""
import importlib.util
import json
import shutil
import sys
from pathlib import Path

FENCE = Path(__file__).resolve().parent
NEW = Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/"
           "providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/graders.py")
OLD = FENCE / "restored" / "graders_e641797.py"
FIXROOT = FENCE / "fixtures"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


G_NEW = load("graders_f8a5741", NEW)
G_OLD = load("graders_e641797", OLD)


def materialise(probe_id, files):
    root = FIXROOT / probe_id
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for rel, content in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    return root


def run(module, root, grader, args):
    budget = {"files_read": 0, "bytes_read": 0}
    try:
        out = module.GRADERS[grader](root, args, budget, {})
    except Exception as exc:  # noqa: BLE001
        return {"result": "EXCEPTION", "observed": type(exc).__name__, "reason": str(exc)}
    return {"result": out["result"], "observed": out["observed"], "reason": out["reason"]}


FM = "---\nname: fixture-scope-note\ndescription: A probe fixture.\n---\n\n"

PROBES = []


def probe(pid, note, files, grader, args, expect_new=None):
    PROBES.append({"id": pid, "note": note, "files": files, "grader": grader,
                   "args": args, "expect_new": expect_new})


# --------------------------------------------------------------------------
# Part 1 - the coordinator's own reproduction inputs (disposition "Grader repro")
# --------------------------------------------------------------------------
probe("PR13-01a-titled-link",
      "titled inline link to a missing file",
      {"SKILL.md": FM + '[required](missing.md "title")\n'},
      "package_relative_links", {"file": "SKILL.md"})

probe("PR13-01b-html-and-refdef",
      "HTML img src= plus a link reference definition, both missing",
      {"SKILL.md": FM + '<img src="missing.png">\n\n[missing]: nothere.md\n'},
      "package_relative_links", {"file": "SKILL.md"})

probe("PR13-01c-control-plain-missing",
      "control: plain inline link to a missing file",
      {"SKILL.md": FM + "[required](missing.md)\n"},
      "package_relative_links", {"file": "SKILL.md"})

probe("PR13-02-nested-fence",
      "four-backtick block quoting a three-backtick example",
      {"report/r.md": "# Report\n\n````markdown\nexample:\n```\nresult: PASS\n```\n````\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["result"]})

probe("PR13-03-colon-space",
      "unquoted description containing a colon-space",
      {"SKILL.md": "---\nname: fixture-scope-note\n"
                   "description: means the user experience: a schema\n---\n\nBody.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]})

# Each of the two EX-DEF-013 detectors alone (the grader names only the first hit).
probe("PR13-01b1-html-only",
      "HTML img src= alone",
      {"SKILL.md": FM + '<img src="missing.png">\n'},
      "package_relative_links", {"file": "SKILL.md"})

probe("PR13-01b2-refdef-only",
      "link reference definition alone",
      {"SKILL.md": FM + "[missing]: nothere.md\n"},
      "package_relative_links", {"file": "SKILL.md"})

# --------------------------------------------------------------------------
# Part 2 - regression hunt on the changed code
# --------------------------------------------------------------------------

# -- fences --
probe("REG-fence-tilde-open-backtick-close",
      "tilde-opened block; a backtick run must not close it",
      {"report/r.md": "# R\n\n~~~\nrecommendation: adopt\n```\n~~~\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "MISMATCH (field is example-only)")

probe("REG-fence-longer-closer",
      "three-backtick open, five-backtick close: closes",
      {"report/r.md": "# R\n\n```\nexample\n`````\nrecommendation: adopt\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "MATCH (line 6 is outside the block)")

probe("REG-fence-shorter-closer",
      "four-backtick open, three-backtick line inside, no real close: unclosed at EOF",
      {"report/r.md": "# R\n\n````\n```\nrecommendation: adopt\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "MISMATCH (still inside the block at EOF)")

probe("REG-fence-indented-3sp",
      "fence indented three spaces (still a fence in CommonMark)",
      {"report/r.md": "# R\n\n   ```\nrecommendation: adopt\n   ```\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "MISMATCH (inside the block)")

probe("REG-fence-indented-4sp",
      "fence indented four spaces: CommonMark makes this an indented code block, not a fence",
      {"report/r.md": "# R\n\n    ```\nrecommendation: adopt\n    ```\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "ambiguous; record behaviour")

probe("REG-fence-closer-with-info-string",
      "CommonMark: a closing fence may carry no info string; ```markdown must not close",
      {"report/r.md": "# R\n\n```\n```markdown\nrecommendation: adopt\n```\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "MISMATCH per CommonMark (field is inside the block)")

probe("REG-fence-tab-indent",
      "tab-indented fence line",
      {"report/r.md": "# R\n\n\t```\nrecommendation: adopt\n\t```\n"},
      "required_report_fields", {"file": "report/r.md", "fields": ["recommendation"]},
      "ambiguous; record behaviour")

probe("REG-fence-unclosed-eof-link",
      "unclosed fence at EOF hides a broken link from the link grader",
      {"SKILL.md": FM + "```\n[required](missing.md)\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "MATCH 0 local (fence swallows the rest) - documented behaviour")

# -- links --
probe("REG-link-image-missing",
      "image link to a missing file (supported subset)",
      {"SKILL.md": FM + "![alt](missing.png)\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "MISMATCH (destination does not exist)")

probe("REG-link-image-present",
      "image link to a present file",
      {"SKILL.md": FM + "![alt](assets/logo.png)\n", "assets/logo.png": "x\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "MATCH 1 local")

probe("REG-link-parens-in-dest",
      "destination containing parentheses",
      {"SKILL.md": FM + "[x](refs/a(1).md)\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "INDETERMINATE (nested parentheses are outside the subset)")

probe("REG-link-angle-dest-present",
      "angle-bracket destination naming a file that exists",
      {"SKILL.md": FM + "[x](<references/present.md>)\n", "references/present.md": "x\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "INDETERMINATE per runner-interface.md (angle brackets unsupported)")

probe("REG-link-multiple-per-line",
      "three links on one line, one of them broken",
      {"SKILL.md": FM + "[a](references/a.md) and [b](references/b.md) and [c](references/gone.md)\n",
       "references/a.md": "a\n", "references/b.md": "b\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "MISMATCH naming references/gone.md")

probe("REG-link-titled-present",
      "titled inline link whose destination DOES exist",
      {"SKILL.md": FM + '[x](references/present.md "title")\n', "references/present.md": "x\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "INDETERMINATE (unsupported representation)")

probe("REG-link-code-span-syntax",
      "link syntax shown inside an inline code span in prose",
      {"SKILL.md": FM + 'Write it as `[label](path "title")` in the report.\n'},
      "package_relative_links", {"file": "SKILL.md"},
      "no unresolvable destination exists; MATCH would be truthful")

probe("REG-link-external-titled",
      "titled EXTERNAL link, nothing local",
      {"SKILL.md": FM + '[docs](https://example.com/a "Docs")\n'},
      "package_relative_links", {"file": "SKILL.md"},
      "INDETERMINATE under the new rule; was MATCH 0 local")

probe("REG-link-refdef-continuation",
      "link reference definition with the destination on the following line",
      {"SKILL.md": FM + "[missing]:\n    nothere.md\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "not detected by REFERENCE_DEFINITION (needs trailing space/tab)")

probe("REG-link-colon-in-prose",
      "a bracketed phrase followed by a colon in ordinary prose",
      {"SKILL.md": FM + "[Note]: this is prose, not a link definition.\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "false INDETERMINATE risk on valid prose")

probe("REG-link-html-in-codespan",
      "an HTML attribute shown inside an inline code span",
      {"SKILL.md": FM + "Use `<img src=...>` sparingly.\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "false INDETERMINATE risk on prose")

probe("REG-link-data-src",
      "a data-src attribute (not a resource attribute)",
      {"SKILL.md": FM + '<div data-src="x">y</div>\n'},
      "package_relative_links", {"file": "SKILL.md"},
      "flagged by the \\b(?:src|href) pattern after a hyphen")

probe("REG-link-max-bound",
      "MAX_LINKS bound: 2100 resolvable local links",
      {"SKILL.md": FM + "".join(f"[l{i}](references/a.md)\n" for i in range(2100)),
       "references/a.md": "a\n"},
      "package_relative_links", {"file": "SKILL.md"},
      "INDETERMINATE once the bound is exceeded")

# -- scalars --
probe("REG-scalar-quoted-with-colon",
      "double-quoted value containing ': '",
      {"SKILL.md": '---\nname: n\ndescription: "means this: a schema"\n---\n\nB.\n'},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "MATCH (quoting makes it a valid scalar)")

probe("REG-scalar-single-quoted-with-colon",
      "single-quoted value containing ': '",
      {"SKILL.md": "---\nname: n\ndescription: 'means this: a schema'\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "MATCH")

probe("REG-scalar-quoted-plus-comment",
      "quoted value followed by a trailing comment",
      {"SKILL.md": '---\nname: n\ndescription: "a: b" # note\n---\n\nB.\n'},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "MATCH (YAML parses this to 'a: b')")

probe("REG-scalar-unquoted-comment-with-colon",
      "unquoted value whose trailing comment contains ': '",
      {"SKILL.md": "---\nname: n\ndescription: plain text # note: here\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "MATCH (comment stripped first)")

probe("REG-scalar-comment-only-value",
      "value consisting only of a comment (YAML null)",
      {"SKILL.md": "---\nname: n\ndescription: # placeholder\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "YAML value is null -> MISMATCH/INDETERMINATE, never MATCH")

probe("REG-scalar-trailing-colon",
      "unquoted value ending in a colon",
      {"SKILL.md": "---\nname: n\ndescription: see the following:\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "INDETERMINATE")

probe("REG-scalar-colon-no-space",
      "unquoted value containing a colon with no following space",
      {"SKILL.md": "---\nname: n\ndescription: ratio 3:1 of cases\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "MATCH (valid plain scalar)")

probe("REG-scalar-url-value",
      "unquoted value containing a URL",
      {"SKILL.md": "---\nname: n\ndescription: see https://example.com/a for detail\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "MATCH (valid plain scalar)")

probe("REG-scalar-empty-value",
      "empty value",
      {"SKILL.md": "---\nname: n\ndescription:\n---\n\nB.\n"},
      "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]},
      "INDETERMINATE unsupported")

probe("REG-scalar-colon-space-name-folder",
      "colon-space description: what name_folder_relation now reports",
      {"SKILL.md": "---\nname: fixtures\ndescription: means this: a schema\n---\n\nB.\n"},
      "name_folder_relation", {"file": "SKILL.md", "expect_equal": True},
      "INDETERMINATE; equality no longer assertable")

probe("REG-scalar-colon-space-present",
      "colon-space description: what frontmatter_present reports",
      {"SKILL.md": "---\nname: n\ndescription: means this: a schema\n---\n\nB.\n"},
      "frontmatter_present", {"file": "SKILL.md"},
      "MATCH (delimiters are present)")


def main():
    rows = []
    for spec in PROBES:
        root = materialise(spec["id"], spec["files"])
        old = run(G_OLD, root, spec["grader"], spec["args"])
        new = run(G_NEW, root, spec["grader"], spec["args"])
        rows.append({"probe": spec["id"], "note": spec["note"], "grader": spec["grader"],
                     "e641797": old, "f8a5741": new, "evaluator_expectation": spec["expect_new"]})
        print(f"== {spec['id']}  [{spec['grader']}]")
        print(f"   note      : {spec['note']}")
        print(f"   e641797   : {old['result']:14s} observed={old['observed']!r}")
        print(f"               reason={old['reason']}")
        print(f"   f8a5741   : {new['result']:14s} observed={new['observed']!r}")
        print(f"               reason={new['reason']}")
        if spec["expect_new"]:
            print(f"   evaluator : {spec['expect_new']}")
        print()
    (FENCE / "out" / "probe-results.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(rows)} probes")


if __name__ == "__main__":
    main()
