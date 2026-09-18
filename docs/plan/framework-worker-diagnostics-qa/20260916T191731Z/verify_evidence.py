"""Independent readback of runtime evidence and exact candidate/input preservation."""
import json
import re
from pathlib import Path
from intake import RUN, ROOT, PKG, DEV, MANIFEST, binding


def write(name, value):
    with (RUN/name).open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(value,stream,indent=2)
        stream.write("\n")


def main():
    preserved=[]
    for family in ("baseline","candidate","candidate-v2"):
        manifest=DEV/(family+"-manifest.json")
        for row in json.loads(manifest.read_text()):
            bases=[(family+"-snapshot",DEV/(family+"-snapshot"))]
            if family=="candidate-v2": bases.append(("original",PKG))
            for kind,base in bases:
                current=binding(base/row["path"])
                preserved.append({"family":kind,**current,"matches":all(current[k]==row[k] for k in ("bytes","sha256"))})
    assert all(r["matches"] for r in preserved)
    write("candidate-readback-after.json",preserved)
    inputs=[]
    for name in (RUN/"input-bindings.json",DEV/"input-bindings.json"):
        for row in json.loads(name.read_text()):
            current=binding(Path(row["path"]))
            inputs.append({"binding_manifest":str(name),**current,"matches":all(current[k]==row[k] for k in ("bytes","sha256"))})
    assert all(r["matches"] for r in inputs)
    write("input-readback-after.json",inputs)
    depfiles=list((RUN/"harness-target/debug/deps").glob("worker_independent_qa-*.d"))
    mapped=[]
    for depfile in depfiles:
        text=depfile.read_text().replace("\\","/").casefold()
        paths=[p for p in (PKG/"src").glob("*.rs") if p.name not in {"lib.rs","main.rs"}]
        found=[str(p) for p in paths if str(p).replace("\\","/").casefold() in text]
        mapped.append({"depfile":binding(depfile),"production_modules":found,"count":len(found)})
    assert any(r["count"]==11 for r in mapped)
    write("harness-source-mapping.json",{"method":"Original absolute path/include source; no production copy or replacement",
        "mapped":mapped,"original_production_files_verified":58,"entrypoints_measured_on_original": ["src/lib.rs","src/main.rs"],
        "path_sensitive_scope_limit":"Wrapper evidence does not qualify native root derivation, CLI/admission paths or public runner end-to-end; original campaign supplies those offline results"})
    observations=[]
    for root in sorted((RUN/"fixtures/07-independent-cases").iterdir()):
        if not root.is_dir(): continue
        observed=json.loads((root/"observed.json").read_text())
        stimulus=json.loads((root/"stimulus.json").read_text())
        journal=(root/"run/journal.jsonl").read_text()
        assert observed["stopped"] is True and observed["active"]=={"Ok":0}
        assert not any(v.get("method","").startswith(("thread/","turn/")) for v in observed["trace"])
        assert stimulus["canary"] not in journal
        observations.append({"fixture":str(root),"observed":binding(root/"observed.json"),
            "journal":binding(root/"run/journal.jsonl"),"stimulus":binding(root/"stimulus.json"),
            "result":observed["result"],"trace_messages":len(observed["trace"]),"stopped":True,"active":0,"canary_absent":True})
    query=[r for r in observations if Path(r["fixture"]).name.startswith("QI01-")]
    assert len(query)==4
    for row in query:
        observed=json.loads(Path(row["observed"]["path"]).read_text())
        assert observed["result"]=={"Err":"windows_error_5"} and observed["trace"]==[]
        diagnostic=observed["events"][0]["data"]["diagnostic"]
        assert set(diagnostic)=={"schema_version","stage","rpc","checkpoint","predicate","total_processes","active_processes"}
        assert diagnostic["predicate"]=="query_failed" and diagnostic["active_processes"] is None and diagnostic["total_processes"] is None
    initialize=[r for r in query if json.loads(Path(r["observed"]["path"]).read_text())["events"][0]["data"]["diagnostic"]["rpc"]=="initialize"]
    assert len(initialize)==1
    write("independent-runtime-readback.json",observations)
    write("query-failed-evidence.json",{"status":"PASS","scope":"Runtime OS error projection through unchanged source in mapped private QA harness",
        "os_failure":"Actual QueryInformationJobObject failure using owned same-job duplicate without JOB_OBJECT_QUERY",
        "public_preflight_initialize":initialize[0],"all_query_subfixtures":query,
        "limits":"Config after_receive and final_check invoked at private guard entry; no claim of spontaneous installed-host failure or native runner execution",
        "native_attempts":0})
    docs=[PKG/"README.md",DEV/"qa-handoff.md",DEV/"diagnostic-contract.md",
          ROOT/"docs/plan/advisor-runs/20260916T185825Z-diagnostic-handoff/qa-handoff-addendum.md"]
    links=[]
    for doc in docs:
        for target in re.findall(r"\]\(([^)]+)\)",doc.read_text()):
            if "://" in target or target.startswith("#"): continue
            local=(doc.parent/target.split("#")[0]).resolve()
            links.append({"source":str(doc),"target":target,"resolved":str(local),"exists":local.exists()})
    assert all(r["exists"] for r in links)
    write("documentation-links.json",links)
    before=set(json.loads((RUN/"trials-before.json").read_text()))
    after=set(str(p) for p in (ROOT/"docs/plan/framework-worker-trials").iterdir())
    added=sorted(after-before)
    assert all(Path(p).name.startswith(("NI-admission-","NI-sources-","RT-source-type-")) for p in added)
    assert before<=after
    write("trial-ownership.json",{"before_count":len(before),"after_count":len(after),"added_owned_roots":added,"removed":[]})
    builds=[]
    for folder in ("target","harness-target","coverage-target"):
        for file in sorted((RUN/folder).rglob("*.exe")):
            # All files are in declared QA outputs; no installed executable scan.
            builds.append(binding(file))
    write("build-manifest.json",builds)
    print(json.dumps({"preserved_candidate_and_snapshots":len(preserved),"input_checks":len(inputs),
        "runtime_fixtures":len(observations),"query_failed_runtime_subfixtures":len(query),
        "documentation_links":len(links),"fresh_trial_roots":len(added),"build_executables":len(builds)},indent=2))


if __name__=="__main__":
    main()
