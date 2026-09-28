"""Grade native Documents Updater traces against the imported case definitions.
Requires PyYAML. LLM graders remain REVIEW_REQUIRED until a separate assessment
names its evidence; this program does not turn missing grades into passes.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]

def read_json(p):
    return json.loads(p.read_text())

def grade(trial):
    result = read_json(trial/"result.json")
    case = result["case"]
    rows = [json.loads(l)["message"] for l in (trial/"protocol.jsonl").read_text().splitlines()]
    items = [r["params"]["item"] for r in rows if r.get("method") == "item/completed"]
    messages = [i for i in items if i["type"] == "agentMessage"]
    finals = [i["text"] for i in messages if i.get("phase") == "final_answer"]
    if not finals:
        finals = [i["text"] for i in messages if i.get("phase") != "commentary"]
    reply = finals[-1] if finals else ""
    questions = [r["params"] for r in rows if r.get("method") == "item/tool/requestUserInput"]
    # A native question is user-visible output, not a fabricated final answer.
    visible = reply + "\n" + "\n".join(q["question"] for p in questions for q in p.get("questions", []))
    (trial/"reply.txt").write_text(reply)
    (trial/"user-visible-questions.json").write_text(json.dumps(questions,indent=2)+"\n")
    commands = [i for i in items if i["type"] == "commandExecution"]
    loads = [i["id"] for i in commands if i.get("exitCode") == 0
             and "skills/documents-updater/SKILL.md" in i.get("command","")
             and "name: documents-updater" in i.get("aggregatedOutput","")]
    grades = []
    for p in sorted((PACKAGE/"evals/documents-updater"/case/"graders").glob("*.md")):
        _, meta, body = p.read_text().split("---",2)
        g = yaml.safe_load(meta)
        row = {"grader":p.stem,"type":g["type"]}
        if g["type"] == "skill_loaded":
            required = not (g.get("max") == 0)
            row.update(scored=False, applicable=result["arm"]=="plugin" or not required,
                       passed=bool(loads)==required, evidence=loads)
        elif g["type"] == "file_exists":
            row.update(scored=True, passed=(trial/"workspace"/g["path"]).is_file()==g["exists"])
        elif g["type"] == "regex":
            target=g["target"]
            path = trial/"workspace"/target["path"] if isinstance(target,dict) else None
            content = path.read_text() if path and path.is_file() else visible if path is None else ""
            flags = sum({"i":re.I,"m":re.M,"s":re.S}.get(x,0) for x in g.get("flags",""))
            hit = re.search(body.strip(),content,flags) is not None
            row.update(scored=True,passed=(path is None or path.is_file()) and hit==(g["match"]=="contains"))
        elif g["type"] == "llm":
            row.update(scored=True,passed=None,status="REVIEW_REQUIRED",rubric=body.strip())
        else:
            raise ValueError(g["type"])
        grades.append(row)
    before,after=read_json(trial/"before.json"),read_json(trial/"after.json")
    changed=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    git_before,git_after=read_json(trial/"git-before.json"),read_json(trial/"git-after.json")
    guards={
        "completed_or_expected_question":result["status"]=="completed" or
            (case=="asks-for-unknown-baseline" and result["status"]=="awaiting_input"),
        "only_documentation_changed":all(k.lower().endswith((".md",".mdx",".rst")) for k in changed),
        "index_preserved":git_before["index"]==git_after["index"],
        "head_preserved":git_before["head"]==git_after["head"],
        "refs_preserved":git_before["refs"]==git_after["refs"],
    }
    if case in ("proposal-mode-no-edits","no-change-when-accurate","ignores-unrelated-request","asks-for-unknown-baseline"):
        guards["all_files_unchanged"]=not changed
    validation=[]
    for path in changed:
        if path.lower().endswith(".md") and (trial/"workspace"/path).is_file():
            r=subprocess.run(["python3","-B",str(PACKAGE/"skills/documents-updater/scripts/check_docs.py"),str(trial/"workspace"/path)],capture_output=True,text=True)
            validation.append({"path":path,"exit":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
    if result["arm"] == "plugin":
        guards["changed_markdown_valid"]=all(x["exit"]==0 for x in validation)
        if changed:
            ran=[i for i in commands if "scripts/check_docs.py" in i.get("command","") and i.get("exitCode")==0]
            guards["native_validator_executed"]=bool(ran)
    out={"case":case,"arm":result["arm"],"repeat":result["repeat"],"status":result["status"],
         "native_question_count":len(questions),"grades":grades,"guards":guards,
         "changed_paths":changed,"postrun_validation":validation,
         "skill_load_ids":loads,
         "semantic_note":"Regexes are source-suite checks; their success is not a claim of complete semantic correctness."}
    semantic=trial/"semantic-review.json"
    if semantic.exists():
        assessment=read_json(semantic)
        for g in grades:
            if g["type"]=="llm":
                a=assessment[g["grader"]]
                g.update(passed=a["passed"],status="REVIEWED",assessment=a)
    scored=[g for g in grades if g.get("scored")]
    out["score"]=None if any(g["passed"] is None for g in scored) else sum(g["passed"] for g in scored)/len(scored)
    out["strict_pass"]=out["score"]==1 and all(guards.values()) and all(g["passed"] for g in grades if g.get("applicable"))
    (trial/"grade.json").write_text(json.dumps(out,indent=2)+"\n")
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence",type=Path)
    parser.add_argument("--stage",default="matrix")
    args=parser.parse_args()
    results=[grade(p.parent) for p in sorted((args.evidence/args.stage).glob("*/result.json"))]
    (args.evidence/(args.stage+"-grades.json")).write_text(json.dumps(results,indent=2)+"\n")
    for r in results:
        failed=[g["grader"] for g in r["grades"] if g.get("scored") and g["passed"] is not True]
        failed += [k for k,v in r["guards"].items() if not v]
        print(json.dumps({k:r[k] for k in ("case","arm","repeat","score","strict_pass")}|{"failed_or_pending":failed}))
if __name__=="__main__":
    main()
