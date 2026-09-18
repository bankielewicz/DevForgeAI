use devforgeai_codex_worker_probe::{journal::{self, Journal}, request::{self, Request}, runner::{self,Options}, process_windows::OwnedProcess, protocol::Session, logging::{self,Level,Phase,Record}};
use serde_json::{Value,json};
use sha2::{Digest,Sha256};
use std::{fs, path::{Path,PathBuf}, time::{Duration,Instant}};
fn hash(bytes: &[u8])->String {format!("{:x}",Sha256::digest(bytes))}
fn base(id:&str)->PathBuf {
    let base=PathBuf::from(std::env::var_os("WF_TEST_EVIDENCE").unwrap());
    fs::create_dir_all(&base).unwrap();
    tempfile::Builder::new().prefix(id).tempdir_in(base).unwrap().keep()
}
fn save(path:impl AsRef<Path>,value:&Value) {fs::write(path,serde_json::to_vec_pretty(value).unwrap()).unwrap();}
fn read(path:impl AsRef<Path>)->Value {serde_json::from_slice(&fs::read(path).unwrap()).unwrap()}
fn rows(dir:&Path)->Vec<Value> {fs::read_to_string(dir.join("journal.jsonl")).unwrap().lines().map(|s|serde_json::from_str(s).unwrap()).collect()}
fn write_rows(dir:&Path,rows:&[Value]) {fs::write(dir.join("journal.jsonl"),rows.iter().map(|r|format!("{r}\n")).collect::<String>()).unwrap();}
struct Fixture {root:PathBuf,input:PathBuf,r:Request}
fn fixture(id:&str,case:&str,level:Option<&str>)->Fixture {
    let root=base(id);let checkout=root.join("fixture");fs::create_dir(&checkout).unwrap();
    let task=include_bytes!("C:/Projects/DevForgeAI/docs/specs/framework/runtime/fixtures/codex-worker-v1/task.json");
    fs::write(checkout.join("task.json"),task).unwrap();
    fs::write(checkout.join("peer-case.txt"),format!("{case}\n")).unwrap();
    let worker=PathBuf::from(env!("CARGO_BIN_EXE_protocol-peer"));
    let mut v=json!({"schema_version":1,"project_id":"qa","checkout_id":"qa-c","work_id":"qa-w","run_id":"qa-r",
      "candidate_sha256":hash(task),"checkout_root":checkout,"run_dir":root.join("run"),
      "worker_executable":worker,"worker_sha256":hash(&fs::read(&worker).unwrap()),"adapter":"peer","scenario":"complete","profile":null});
    if let Some(level)=level {
        let bytes=serde_json::to_vec(&json!({"schema_version":1,"level":level,"redaction_policy":"closed-v1"})).unwrap();
        let config=root.join("QA_CANARY_config_path_7391.json");fs::write(&config,&bytes).unwrap();
        v["schema_version"]=json!(3);v["diagnostics_ref"]=json!(config);v["diagnostics_sha256"]=json!(hash(&bytes));
    }
    let input=root.join("input.json");save(&input,&v);
    let r=request::validate(&input).unwrap();
    Fixture{root,input,r}
}
fn options()->Options {Options{total:Duration::from_secs(4),rpc:Duration::from_millis(750),grace:Duration::from_millis(150),teardown:Duration::from_secs(2),..Default::default()}}
fn run(f:&Fixture)->(i32,Value,Vec<Value>) {
    let mut emitted=Vec::new();
    let (code,t)=runner::run(&f.input,options(),&mut |v|emitted.push(v.clone())).unwrap();
    assert_eq!(t["tree_stopped"],true,"{t}");assert_eq!(t["fixture_unchanged"],true);
    assert_eq!(rows(&f.r.run_dir),emitted);
    save(f.root.join("result.json"),&json!({"code":code,"terminal":t,"events":emitted}));
    (code,t,emitted)
}
fn capture(args:&[&str],delay:Duration)->(PathBuf,Value) {
    let root=base("capture");let exe=Path::new(env!("CARGO_BIN_EXE_qa-byte-peer"));
    let mut p=OwnedProcess::spawn(exe,&args.iter().map(|s|s.to_string()).collect::<Vec<_>>(),&root).unwrap();
    p.close_input();std::thread::sleep(delay);
    let deadline=Instant::now()+Duration::from_secs(4);
    while p.exit_code().is_none() && Instant::now()<deadline {std::thread::sleep(Duration::from_millis(2));}
    let before=p.exit_code();
    let joined=p.drain_until(deadline);
    let stopped=p.stop(Duration::from_secs(2));
    let value=json!({"capture":p.capture(),"joined":joined,"pre":before,"post":p.exit_code(),"stopped":stopped,"active":p.active().unwrap(),"error":p.stream_error()});
    save(root.join("capture.json"),&value);
    assert!(stopped);assert_eq!(value["active"],0);
    (root,value)
}
fn expected()->Value {serde_json::from_str(include_str!("expected.json")).unwrap()}
fn exact(v:&Value,key:&str) {
    let ex=&expected()[key];
    for stream in ["stdout","stderr"] {
        assert_eq!(v["capture"][stream]["bytes"],ex[stream]["bytes"],"{key}/{stream}/{v}");
        assert_eq!(v["capture"][stream]["sha256"],ex[stream]["sha256"],"{key}/{stream}/{v}");
    }
}

#[test]
fn qa_01_config_denials_and_exact_boundary() {
    for bad in [b"{}".to_vec(),b"null".to_vec(),b"{".to_vec(),
       br#"{"schema_version":1,"level":"raw","redaction_policy":"closed-v1"}"#.to_vec(),
       br#"{"schema_version":1,"level":"debug","redaction_policy":"closed-v1","secret":"QA_CANARY_7391"}"#.to_vec(),
       br#"{"schema_version":1,"level":"off","level":"debug","redaction_policy":"closed-v1"}"#.to_vec(),
       br#"{"schema_version":1,"level":"debug","redaction_policy":"raw"}"#.to_vec(), vec![b' ';4097]] {
        let f=fixture("qa01","WF-01",Some("off"));let mut input=read(&f.input);
        let path=PathBuf::from(input["diagnostics_ref"].as_str().unwrap());fs::write(&path,&bad).unwrap();
        input["diagnostics_sha256"]=json!(hash(&bad));save(&f.input,&input);
        assert_eq!(runner::run(&f.input,options(),&mut |_|{}).unwrap_err(),"invalid_diagnostics");
        assert!(!f.r.run_dir.exists());assert!(!f.root.join("peer-trace.jsonl").exists());
    }
    for mode in ["digest","traversal","junction"] {
        let f=fixture("qa01","WF-01",Some("off"));let mut input=read(&f.input);
        if mode=="digest" {input["diagnostics_sha256"]=json!("0".repeat(64));}
        else if mode=="traversal" {
            let sub=f.root.join("other");fs::create_dir(&sub).unwrap();
            input["diagnostics_ref"]=json!(sub.join("../QA_CANARY_config_path_7391.json"));
        } else {
            let target=f.root.join("real-config");fs::create_dir(&target).unwrap();
            fs::copy(f.r.diagnostics_ref.as_ref().unwrap(),target.join("QA_CANARY_config_path_7391.json")).unwrap();
            let alias=f.root.join("alias");
            save(f.root.join("junction-input.json"),&json!({"executable":"cmd.exe","args":["/d","/c","mklink","/J",alias.to_str().unwrap(),target.to_str().unwrap()]}));
            let out=std::process::Command::new("cmd.exe").args(["/d","/c","mklink","/J"]).arg(&alias).arg(&target).output().unwrap();
            save(f.root.join("junction-output.json"),&json!({"exit":out.status.code(),"stdout":String::from_utf8_lossy(&out.stdout),"stderr":String::from_utf8_lossy(&out.stderr)}));
            assert!(out.status.success(),"junction setup: {:?}",out);
            input["diagnostics_ref"]=json!(alias.join("QA_CANARY_config_path_7391.json"));
        }
        save(&f.input,&input);
        assert_eq!(runner::run(&f.input,options(),&mut |_|{}).unwrap_err(),"invalid_diagnostics");
        assert!(!f.r.run_dir.exists());
    }
    let f=fixture("qa01-bound","WF-01",Some("off"));let mut input=read(&f.input);
    let path=PathBuf::from(input["diagnostics_ref"].as_str().unwrap());let mut bytes=fs::read(&path).unwrap();bytes.resize(4096,b' ');
    fs::write(&path,&bytes).unwrap();input["diagnostics_sha256"]=json!(hash(&bytes));save(&f.input,&input);
    assert_eq!(run(&f).0,0);assert_eq!(fs::read(f.r.run_dir.join("diagnostics-config.json")).unwrap(),bytes);
}
#[test]
fn qa_02_drift_and_legacy_composition() {
    let f=fixture("qa02","WF-01",Some("debug"));let original=fs::read(f.r.diagnostics_ref.as_ref().unwrap()).unwrap();
    let mut emitted=vec![];
    let (code,t)=runner::run(&f.input,options(),&mut |v| {
        emitted.push(v.clone());
        if v["kind"]=="spawn_intent" {fs::write(f.r.diagnostics_ref.as_ref().unwrap(),b"{}").unwrap();}
    }).unwrap();
    assert_eq!(code,4);assert_eq!(t["reason"],"invalid_diagnostics");
    assert!(!emitted.iter().any(|v|v["kind"]=="server_started"));assert!(!f.root.join("peer-trace.jsonl").exists());
    assert_eq!(fs::read(f.r.run_dir.join("diagnostics-config.json")).unwrap(),original);
    save(f.root.join("observed.json"),&json!({"code":code,"terminal":t,"events":emitted}));
    let legacy=fixture("qa02-legacy","WF-01",None);
    assert_eq!(run(&legacy).0,0);assert!(!legacy.r.run_dir.join("diagnostics.jsonl").exists());
    for schema in [1,2,4] {
        let f=fixture("qa02-version","WF-01",Some("debug"));let mut input=read(&f.input);input["schema_version"]=json!(schema);save(&f.input,&input);
        assert!(request::validate(&f.input).is_err());assert!(!f.r.run_dir.exists());
    }
}
#[test]
fn qa_03_early_exit_classification() {
    for (name,category) in [("silent","unclassified"),("config","strict_config_rejected"),("mcp","configuration_parse_failed"),("negative","unclassified")] {
        let (_,v)=capture(&[name],Duration::from_millis(100));exact(&v,name);
        assert_eq!(v["pre"],29);assert_eq!(v["post"],29);assert_eq!(v["joined"],true);
        assert_eq!(v["capture"]["drain_complete"],true);
        assert_eq!(v["capture"]["stderr"]["category"],category);
        assert_eq!(v["capture"]["stderr"]["classifier_version"],"startup-v1");
    }
}
#[test]
fn qa_04_raw_utf8_final_line_and_argv() {
    let (_,v)=capture(&["utf8"],Duration::from_millis(150));exact(&v,"utf8");
    assert_eq!(v["capture"]["stdout"]["utf8_valid"],false);assert_eq!(v["capture"]["stderr"]["utf8_valid"],false);
    assert_eq!(v["capture"]["stdout"]["lines"],1);assert_eq!(v["capture"]["stdout"]["final_line_bytes"],14);
    assert_eq!(v["capture"]["drain_complete"],true);assert_eq!(v["pre"],29);assert_eq!(v["post"],29);
    let args=["argv","with space","quote\"inside",r"trailing\","日本語"];
    let (_,v)=capture(&args,Duration::from_millis(100));
    exact(&v,"argv");assert_eq!(v["capture"]["stdout"]["utf8_valid"],true);
}
#[test]
fn qa_05_delayed_consumer_and_budgets() {
    let (_,v)=capture(&["flood"],Duration::from_millis(400));exact(&v,"flood");
    assert_eq!(v["capture"]["drain_complete"],true);assert_eq!(v["capture"]["stderr"]["classification_truncated"],true);
    assert!(v["capture"]["stderr"]["detail_dropped"].as_u64().unwrap()>0);
    for (mode,n,flag) in [("line",1048576,"line_overflow"),("line",1048577,"line_overflow"),("queue",128,"queue_overflow"),("queue",129,"queue_overflow"),("bytes",8388608,"byte_overflow"),("bytes",8388609,"byte_overflow")] {
        let (_,v)=capture(&[mode,&n.to_string()],Duration::from_millis(300));exact(&v,&format!("{mode}-{n}"));
        let stream=if mode=="bytes" {"stderr"}else{"stdout"};
        let overflow=n==1048577||n==129||n==8388609;
        assert_eq!(v["capture"][stream][flag],overflow,"{v}");
        assert_eq!(v["error"],if overflow {json!("output_limit")}else{Value::Null});
        assert_eq!(v["capture"]["drain_complete"],!(mode=="bytes" && overflow));
    }
}
#[test]
fn qa_06_levels_and_capture_privacy() {
    for level in ["off","minimal","verbose","debug"] {
        let f=fixture("qa06","WF-04-72",Some(level));let (_,_,events)=run(&f);
        assert_eq!(events.iter().filter(|v|v["kind"]=="process_exit").count(),1);
        let exit=events.iter().position(|v|v["kind"]=="process_exit").unwrap();
        assert!(exit<events.iter().position(|v|v["kind"]=="terminal").unwrap());
        let capture=&events[exit]["data"]["capture"];
        assert_eq!(capture["stderr"]["sha256"],expected()["inherited-canary"]["stderr"]["sha256"]);
        assert_eq!(capture["stderr"]["eof"],true);assert_eq!(capture["drain_complete"],true);
        let path=f.r.run_dir.join("diagnostics.jsonl");assert_eq!(path.exists(),level!="off");
        let diagnostic=if path.exists(){fs::read_to_string(&path).unwrap()}else{String::new()};
        for text in [serde_json::to_string(&events).unwrap(),diagnostic.clone()] {
            assert!(!text.contains("CANARY_SECRET_29417"));assert!(!text.contains("QA_CANARY_config_path_7391"));assert!(!text.contains("Bearer sk-"));
        }
        if level!="off" {
            let logs:Vec<Value>=diagnostic.lines().map(|s|serde_json::from_str(s).unwrap()).collect();
            assert!(logs.iter().any(|v|v["record"]["event"]=="spawn"));assert!(logs.iter().any(|v|v["record"]["event"]=="exit"));
            assert_eq!(logs.iter().any(|v|v["record"]["event"]=="launch"),level=="verbose"||level=="debug");
            assert_eq!(logs.iter().any(|v|v["record"]["event"]=="chunk"),level=="debug");
            for v in logs {assert_eq!(v.as_object().unwrap().len(),2);}
        }
        assert!(journal::inspect(&f.r.run_dir,0,100).is_ok());
    }
}
#[test]
fn qa_07_sink_faults_caps_and_required_write_failure() {
    let dir=base("qa07");fs::create_dir(dir.join("diagnostics.jsonl")).unwrap();
    let mut sink=logging::Sink::new(&dir,Level::Debug);
    sink.record(Level::Minimal,Record::Phase{phase:Phase::Admitted,elapsed_ms:1});
    let status=sink.finish();assert!(status.diagnostics_incomplete);assert_eq!(status.dropped,1);
    let dir=base("qa07-events");let mut sink=logging::Sink::new(&dir,Level::Debug);
    for n in 0..512 {sink.record(Level::Minimal,Record::Phase{phase:Phase::Admitted,elapsed_ms:n});}
    let status=sink.finish();assert_eq!(status.events,512);assert!(!status.diagnostics_incomplete);
    // finish closes this sink; use a fresh sink to test one event beyond the cap.
    let dir=base("qa07-over");let mut sink=logging::Sink::new(&dir,Level::Debug);
    for n in 0..513 {sink.record(Level::Minimal,Record::Phase{phase:Phase::Admitted,elapsed_ms:n});}
    let status=sink.finish();assert_eq!(status.events,512);assert_eq!(status.dropped,1);assert!(status.diagnostics_incomplete);
    let f=fixture("qa07-required","WF-01",Some("debug"));
    let (code,t)=runner::run(&f.input,Options{fail_write_after:Some(3),..options()},&mut |_|{}).unwrap();
    assert_eq!(code,4);assert_eq!(t["reason"],"evidence_write_failed");assert_eq!(t["tree_stopped"],true);
}
#[test]
fn qa_08_untrusted_server_request_privacy() {
    for level in ["off","minimal","verbose","debug"] {
        let f=fixture("qa08","WF-01",Some(level));let mut journal=Journal::create(&f.r).unwrap();
        let mut p=OwnedProcess::spawn(Path::new(env!("CARGO_BIN_EXE_qa-byte-peer")),&["secret-request".into()],&f.r.checkout_root).unwrap();
        let opts=options();let mut emitted=vec![];
        let result={let mut emit=|v:&Value|emitted.push(v.clone());let mut session=Session::new(&mut p,&mut journal,&mut emit,&opts,Instant::now()+opts.total);session.dispatch(&f.r)};
        assert_eq!(result,Err("unsupported_request".into()));
        p.close_input();p.wait_stopped(Duration::from_secs(1));assert!(p.stop(Duration::from_secs(2)));
        journal.log_capture(&p.capture(),&p.chunks(),p.exit_code(),p.exit_code(),true);
        let status=journal.finish_diagnostics().unwrap();journal.append("worker_event",status).unwrap();drop(journal);
        for text in [serde_json::to_string(&emitted).unwrap(),fs::read_to_string(f.r.run_dir.join("journal.jsonl")).unwrap(),fs::read_to_string(f.r.run_dir.join("diagnostics.jsonl")).unwrap_or_default()] {
            assert!(!text.contains("QA_CANARY"),"privacy canary retained: {text}");
        }
        assert_eq!(p.active(),Ok(0));
    }
}
#[test]
fn qa_09_inspector_rejects_inconsistent_capture() {
    // Each mutation starts from a fresh real completed run and an accepted control.
    let mut accepted=Vec::new();
    for mutation in ["missing-capture","drain-false","eof-false","read-error","overflow","post-code","missing-post","missing-status","bad-log"] {
        let f=fixture("qa09","WF-01",Some("debug"));assert_eq!(run(&f).0,0);
        assert_eq!(journal::inspect(&f.r.run_dir,0,100).unwrap()["state"],"completed");
        let original=rows(&f.r.run_dir);let mut changed=original.clone();
        for row in &mut changed {
            if row["kind"]=="process_exit" {
                match mutation {
                    "missing-capture"=>{row["data"].as_object_mut().unwrap().remove("capture");},
                    "drain-false"=>row["data"]["capture"]["drain_complete"]=json!(false),
                    "eof-false"=>{row["data"]["capture"]["stdout"]["eof"]=json!(false);row["data"]["capture"]["drain_complete"]=json!(false);},
                    "read-error"=>{row["data"]["capture"]["stdout"]["read_error"]=json!("pipe_read_failed");row["data"]["capture"]["drain_complete"]=json!(false);},
                    "overflow"=>row["data"]["capture"]["stdout"]["byte_overflow"]=json!(true),
                    "post-code"=>row["data"]["worker_exit_code"]=json!(29),
                    "missing-post"=>{row["data"].as_object_mut().unwrap().remove("worker_exit_code");},
                    _=>{}
                }
            }
            if mutation=="missing-status" && row["data"]["method"]=="diagnostics_status" {row["data"]["method"]=json!("unrelated");}
        }
        fs::write(f.root.join("journal-before.jsonl"),original.iter().map(|r|format!("{r}\n")).collect::<String>()).unwrap();
        write_rows(&f.r.run_dir,&changed);
        if mutation=="bad-log" {fs::write(f.r.run_dir.join("diagnostics.jsonl"),b"{}\n").unwrap();}
        let result=journal::inspect(&f.r.run_dir,0,100);
        save(f.root.join("mutation-result.json"),&json!({"mutation":mutation,"result":result}));
        if result.is_ok() {accepted.push(mutation.to_owned());}
    }
    assert!(accepted.is_empty(),"inspector accepted inconsistent completed evidence: {accepted:?}");
}
#[test]
fn qa_10_legacy_and_interrupted_prefix() {
    let f=fixture("qa10","WF-01",None);assert_eq!(run(&f).0,0);
    let mut inputs=read(f.r.run_dir.join("inputs.json"));inputs.as_object_mut().unwrap().remove("capture_schema");save(f.r.run_dir.join("inputs.json"),&inputs);
    let mut events=rows(&f.r.run_dir);
    for row in &mut events {if row["kind"]=="process_exit"{row["data"]=json!({"worker_exit_code":0,"tree_stopped":true});}}
    write_rows(&f.r.run_dir,&events);
    let historical=journal::inspect(&f.r.run_dir,0,100).unwrap();assert_eq!(historical["state"],"completed");
    let f=fixture("qa10-prefix","WF-01",Some("debug"));let mut j=Journal::create(&f.r).unwrap();
    j.append("admitted",json!({})).unwrap();j.append("spawn_intent",json!({})).unwrap();drop(j);
    let path=f.r.run_dir.join("journal.jsonl");let mut bytes=fs::read(&path).unwrap();bytes.extend_from_slice(b"{unfinished");fs::write(&path,&bytes).unwrap();
    let observed=journal::inspect(&f.r.run_dir,0,1).unwrap();assert_eq!(observed["state"],"interrupted_unknown");assert_eq!(observed["truncated_tail"],11);
    assert_eq!(fs::read(path).unwrap(),bytes);
}
#[test]
fn qa_11_policy_and_native_schema() {
    let old=read("C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/restrictive-launch-policy.json");
    let new:Value=serde_json::from_str(devforgeai_codex_worker_probe::launch_policy::RECORD).unwrap();
    assert_eq!(old["argv"].as_array().unwrap().len(),116);assert_eq!(new["argv"].as_array().unwrap().len(),116);
    let mut changed=0;
    for (a,b) in old["argv"].as_array().unwrap().iter().zip(new["argv"].as_array().unwrap()) {
        if a!=b {changed+=1;let(a,b)=(a.as_str().unwrap(),b.as_str().unwrap());let (key,value)=a.split_once('=').unwrap();assert_eq!(b,format!("{}={value}",key.replace('"',"")));}
    }
    assert_eq!(changed,15);assert_ne!(old["policy_id"],new["policy_id"]);
    let f=fixture("qa11","WF-01",Some("debug"));let mut r=f.r.clone();r.adapter="codex-0.154.0-stdio".into();
    r.profile=json!({"model":"gpt-6-astra","effort":"high","review_ref":f.root.join("unqualified.json"),"review_sha256":"0".repeat(64),"launch_policy_id":new["policy_id"],"launch_policy_sha256":devforgeai_codex_worker_probe::launch_policy::digest()});
    assert!(r.native_v2());assert!(r.profile().unwrap().is_some());assert!(r.verify_preflight_review().is_err());assert!(r.verify_review().is_err());
    for version in [1,4] {assert!(devforgeai_codex_worker_probe::launch_policy::args("codex-0.154.0-stdio",version,new["policy_id"].as_str().unwrap(),&devforgeai_codex_worker_probe::launch_policy::digest()).is_err());}
    assert!(!f.r.run_dir.exists());
}
#[test]
fn qa_12_independent_trace_and_oracle() {
    for (case,code,reason) in [("WF-01",0,"completed"),("WF-02-1",3,"profile_unqualified"),("WF-18-3",4,"oracle_mismatch"),("WF-01-3",4,"worker_failed")] {
        let f=fixture("qa12",case,Some("debug"));let (actual,t,events)=run(&f);assert_eq!(actual,code);assert_eq!(t["reason"],reason);
        let trace:Vec<Value>=fs::read_to_string(f.root.join("peer-trace.jsonl")).unwrap().lines().map(|s|serde_json::from_str(s).unwrap()).collect();
        assert_eq!(trace.iter().filter(|v|v["method"]=="initialize").count(),1);
        assert_eq!(trace.iter().filter(|v|v["method"]=="turn/start").count(),usize::from(case!="WF-02-1"));
        assert!(!trace.iter().any(|v|matches!(v["method"].as_str(),Some("command/exec"|"config/write"|"account/login/start"))));
        if case=="WF-01" {
            let observed=events.iter().find(|v|v["data"]["method"]=="final_result").unwrap();
            let expected:Value=serde_json::from_str(include_str!("C:/Projects/DevForgeAI/docs/specs/framework/runtime/fixtures/codex-worker-v1/expected.json")).unwrap();
            let result:Value=serde_json::from_str(observed["data"]["text"].as_str().unwrap()).unwrap();assert_eq!(result,expected);
            assert_eq!(t["worker_exit_code"],0);
        }
    }
}
#[test]
fn qa_13_preservation_and_documentation() {
    let evidence=Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap();
    for name in ["candidate-manifest.json","preserved-manifest.json","input-manifest.json"] {
        let manifest=read(evidence.join(name));
        for item in manifest.as_array().unwrap() {assert_eq!(hash(&fs::read(item["path"].as_str().unwrap()).unwrap()),item["sha256"]);}
    }
    let readme=fs::read_to_string("C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe-logging-qa-fixes/README.md").unwrap();
    assert!(readme.contains("schema_version")&&readme.contains("diagnostics_sha256"));
    assert!(readme.contains("separate explicit selection"));
}
