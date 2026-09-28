"""Supplemental native checks; these do not replace SPEC-006's owner manual cases."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from native_documents_updater_eval import PACKAGE, Server, inventory, save, git_state

E = PACKAGE/"import-evidence/documents-updater-20260928"
CASES = [
    {"id":"native-question-plan","fixture":"asks-for-unknown-baseline","mode":"plan",
     "prompts":["Update the changelog with the work on my branch."]},
    {"id":"proposal-apply-repeat","fixture":"updates-readme-and-changelog","mode":None,
     "prompts":["Draft the documentation updates for my uncommitted --json change, but do not touch files.",
                "Apply the documentation proposal you just prepared.",
                "Refresh the documentation again for the same uncommitted --json changes against HEAD."]},
    {"id":"invalid-revision","fixture":"updates-readme-and-changelog","mode":None,
     "prompts":["Update the README and changelog for the changes since the revision nonexistent-du-revision."]},
]
save(E/"supplemental-plan.json",{
    "cases":CASES,"status":"Frozen before runs",
    "purpose":"Native question-tool routing, proposal/apply/idempotence, and ERR-03.",
    "manual_VER_10_to_12":"NOT_RUN: these are controlled fixtures, not owner real-session or deployed-plugin acceptance."
})

def run(case):
    e=E/"supplemental"/case["id"]
    e.mkdir(parents=True,exist_ok=False)
    parent=Path(tempfile.mkdtemp(prefix="dfai-du-extra-"))
    cwd=parent/"project";cwd.mkdir()
    candidate=parent/"devforgeai";shutil.copytree(E/"candidate",candidate)
    scaffold=PACKAGE/"evals/documents-updater"/case["fixture"]/"scaffold.sh"
    r=subprocess.run(["bash",str(scaffold)],cwd=cwd,capture_output=True,text=True)
    save(e/"scaffold.json",{"exit":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
    r.check_returncode()
    save(e/"before.json",inventory(cwd));save(e/"git-before.json",git_state(cwd))
    shutil.copytree(cwd,e/"before-workspace",ignore=shutil.ignore_patterns(".git"))
    server=None;results=[]
    try:
        server=Server(e,cwd);server.setup(cwd,"plugin",candidate);server.mode=case["mode"]
        for number,prompt in enumerate(case["prompts"],1):
            before=inventory(cwd)
            result=server.turn(prompt,1200)
            after=inventory(cwd)
            results.append({"number":number,"prompt":prompt,"result":result,"before":before,"after":after})
            save(e/"turns.json",results)
            shutil.copytree(cwd,e/f"turn-{number}-workspace",ignore=shutil.ignore_patterns(".git"))
            if result["status"]!="completed":break
    except Exception as exc:
        save(e/"error.json",{"error":repr(exc)})
    finally:
        if server:server.close()
    save(e/"after.json",inventory(cwd));save(e/"git-after.json",git_state(cwd))
    print(json.dumps({"case":case["id"],"turn_statuses":[r["result"]["status"] for r in results]}),flush=True)

if __name__=="__main__":
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run,CASES))
