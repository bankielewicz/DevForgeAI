use super::*;
use crate::{fixture_config, process_windows::qa_without_query};
use std::{fs, path::PathBuf};

struct Observed { result: Result<()>, events: Vec<Value>, trace: Vec<Value>, root: PathBuf, elapsed: Duration }

fn exercise(case: &str, mode: &str, control: u8, fail_after: Option<u64>,
    action: impl FnOnce(&mut Session<'_>, &Request) -> Result<()>) -> Observed {
    let base = PathBuf::from(std::env::var_os("WF_TEST_EVIDENCE").unwrap());
    fs::create_dir_all(&base).unwrap();
    let root = tempfile::Builder::new().prefix(case).tempdir_in(base).unwrap().keep();
    let fixture = root.join("fixture"); fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    let exe = std::env::current_exe().unwrap().parent().unwrap().parent().unwrap().join("qa-peer.exe");
    let r = Request { schema_version:1, project_id:"qa".into(), checkout_id:"fixture".into(), work_id:case.into(), run_id:"qa".into(),
        candidate_sha256:request::digest(request::TASK), checkout_root:fixture.clone(), run_dir:root.join("run"),
        worker_sha256:request::hash_file(&exe).unwrap(), worker_executable:exe.clone(), adapter:"peer".into(), scenario:"complete".into(), profile:Value::Null };
    let before = r.fixture_inventory().unwrap();
    let canary = format!("QA_SESSION_{case}_E38421");
    fs::write(root.join("stimulus.json"), json!({"mode":mode,"control":control,"fail_after":fail_after,"canary":canary}).to_string()).unwrap();
    let mut process = OwnedProcess::spawn(&exe, &[mode.into(),root.to_string_lossy().into_owned(),canary.clone()], &fixture).unwrap();
    assert_eq!((process.created_processes().unwrap(),process.active().unwrap()), (1,1));
    let mut journal = Journal::create(&r).unwrap();
    if let Some(n) = fail_after { journal.inject_write_failure_after(n); }
    let options = Options { total:Duration::from_secs(3), rpc:Duration::from_millis(180), grace:Duration::from_millis(20), teardown:Duration::from_secs(2), ..Default::default() };
    options.control.store(control, Ordering::SeqCst);
    let mut events = Vec::new();
    let start = Instant::now();
    let result = {
        let mut emit = |event: &Value| events.push(event.clone());
        let mut session = Session::new(&mut process,&mut journal,&mut emit,&options,Instant::now()+options.total);
        let result = action(&mut session,&r);
        assert!(session.thread.is_none() && session.turn.is_none());
        result
    };
    let stopped = process.stop(options.teardown);
    let active = process.active();
    drop(journal);
    let persisted = fs::read_to_string(r.run_dir.join("journal.jsonl")).unwrap();
    let readback: Vec<Value> = persisted.lines().map(|line| serde_json::from_str(line).unwrap()).collect();
    let trace: Vec<Value> = fs::read_to_string(root.join("trace.jsonl")).unwrap_or_default().lines().map(|line|serde_json::from_str(line).unwrap()).collect();
    let elapsed = start.elapsed();
    fs::write(root.join("observed.json"),serde_json::to_vec_pretty(&json!({"result":result,"events":events,"trace":trace,"stopped":stopped,"active":active,"elapsed_ms":elapsed.as_millis()})).unwrap()).unwrap();
    assert!(stopped); assert_eq!(active, Ok(0));
    assert_eq!(readback,events);
    assert_eq!(r.fixture_inventory().unwrap(),before);
    assert!(!trace.iter().any(|v| v["method"].as_str().is_some_and(|s|s.starts_with("thread/") || s.starts_with("turn/"))));
    assert!(!persisted.contains(&canary), "canary leaked into product journal");
    Observed { result, events, trace, root, elapsed }
}

fn diagnostic_events(observation: &Observed) -> Vec<Value> {
    observation.events.iter().filter_map(|event|event["data"].get("diagnostic").cloned()).collect()
}
fn accounting(rpc: &str, checkpoint: &str, predicate: &str, total: Value, active: Value) -> Value {
    json!({"schema_version":1,"stage":"process_accounting","rpc":rpc,"checkpoint":checkpoint,
        "predicate":predicate,"total_processes":total,"active_processes":active})
}

#[test]
fn qa_i01_query_failed_runtime() {
    // Real API failure in preflight initialize and config RPC, plus later guard boundaries.
    for (index, rpc, checkpoint) in [(0,"initialize","before_send"),(1,"config_read","before_send"),(2,"config_read","after_receive"),(3,"final_check","final_check")] {
        let observation = exercise(&format!("QI01-{index}"), "ok", 0, None, |session,r| {
            qa_without_query(session.process, |process| {
                let mut nested = Session::new(process, session.journal, session.emit,session.options,session.deadline);
                match index {
                    0 => nested.preflight(r,&[r.checkout_root.join("task.json")]),
                    1 => { nested.preflight_guard=true; nested.rpc("config/read",json!({})).map(|_|()) },
                    2 => nested.process_guard(RpcStage::ConfigRead,Checkpoint::AfterReceive),
                    _ => nested.process_guard(RpcStage::FinalCheck,Checkpoint::FinalCheck),
                }
            })
        });
        assert_eq!(observation.result,Err("windows_error_5".into()));
        assert!(observation.trace.is_empty(), "failed query must precede send");
        let mut expected = vec![accounting(rpc,checkpoint,"query_failed",Value::Null,Value::Null)];
        if index < 2 { expected.push(json!({"schema_version":1,"stage":"rpc","rpc":rpc,"predicate":"other_rpc_failure"})); }
        assert_eq!(diagnostic_events(&observation),expected);
    }
}

#[test]
fn qa_i02_query_failed_write_precedence() {
    let observation = exercise("QI02", "ok", 0, Some(0), |session,r| {
        qa_without_query(session.process, |process| {
            let mut nested=Session::new(process,session.journal,session.emit,session.options,session.deadline);
            nested.preflight(r,&[r.checkout_root.join("task.json")])
        })
    });
    assert_eq!(observation.result,Err("evidence_write_failed".into()));
    assert!(observation.events.is_empty() && observation.trace.is_empty());
}

fn native_review_request(r: &Request, review: &std::path::Path, digest: &str) -> Request {
    let mut native=r.clone(); native.schema_version=2; native.adapter="codex-0.154.0-stdio".into();
    native.profile=json!({"model":"gpt-6-astra","effort":"high","review_ref":review,"review_sha256":digest,
        "launch_policy_id":"codex-0.154.0-readonly-no-external-tools-v2","launch_policy_sha256":crate::launch_policy::digest()});
    native
}

#[test]
fn qa_i03_source_review_boundaries() {
    let observation=exercise("QI03", "ok", 0, None, |session,r| {
        let native=native_review_request(r,&r.checkout_root.parent().unwrap().join("absent-review.json"),&"c".repeat(64));
        let first=session.dispatch(&native);
        assert_eq!(first,Err("profile_unqualified".into()));
        session.source_review(SourceBoundary::PostPreflight,||native.verify_review())
    });
    assert_eq!(observation.result,Err("profile_unqualified".into()));
    assert!(observation.trace.is_empty());
    assert_eq!(diagnostic_events(&observation),["post_spawn","post_preflight"].map(|boundary|json!({"schema_version":1,"stage":"source_review","boundary":boundary,"predicate":"review_rejected"})));
    let failed=exercise("QI03-write", "ok", 0, Some(0), |session,r| {
        let native=native_review_request(r,&r.checkout_root.parent().unwrap().join("absent-review.json"),&"c".repeat(64));
        session.source_review(SourceBoundary::PostPreflight,||native.verify_review())
    });
    assert_eq!(failed.result,Err("evidence_write_failed".into()));
    assert!(failed.events.is_empty() && failed.trace.is_empty());
}

#[test]
fn qa_i04_rpc_and_config_privacy() {
    for (mode, reason, stage) in [("error-init","rpc_error","initialize"),("error-config","profile_unqualified","config_read"),("server-request","unsupported_request","initialize")] {
        let observation=exercise(&format!("QI04-{mode}"),mode,0,None,|session,r| session.preflight(r,&[r.checkout_root.join("task.json")]));
        assert_eq!(observation.result,Err(reason.into()));
        assert!(diagnostic_events(&observation).contains(&json!({"schema_version":1,"stage":"rpc","rpc":stage,"predicate":if mode=="server-request" {"other_rpc_failure"} else {"rpc_error"}})));
    }
    let bad=exercise("QI04-denial","bad-config",0,None,|session,r|session.preflight(r,&[r.checkout_root.join("task.json")]));
    assert_eq!(bad.result,Err("profile_unqualified".into()));
    assert!(diagnostic_events(&bad).contains(&json!({"schema_version":1,"stage":"config_validation","section":"effective","predicate":"approval_policy"})));
    let good=exercise("QI04-projection","ok",0,None,|session,r|session.preflight(r,&[r.checkout_root.join("task.json")]));
    // Peer intentionally ends at the following requirements RPC. Only config success is claimed.
    assert_eq!(good.result,Err("profile_unqualified".into()));
    let projections:Vec<_>=good.events.iter().filter(|v|v["data"]["preflight"]=="config").map(|v|v["data"]["observation"].clone()).collect();
    assert_eq!(projections,vec![fixture_config::expected_projection()]);
    let expected:Vec<_>=["initialize","config_read"].into_iter().flat_map(|rpc|["before_send","after_receive"].map(move |point|accounting(rpc,point,"only_worker",json!(1),json!(1)))).collect();
    assert_eq!(diagnostic_events(&good),expected);
}

#[test]
fn qa_i05_exited_descendant() {
    for (mode,rpc) in [("descendant-init","initialize"),("descendant-config","config_read")] {
        let observation=exercise(&format!("QI05-{rpc}"),mode,0,None,|session,r|session.preflight(r,&[r.checkout_root.join("task.json")]));
        assert!(observation.root.join("child-exited").is_file());
        assert_eq!(observation.result,Err("profile_unqualified".into()));
        assert!(diagnostic_events(&observation).contains(&accounting(rpc,"after_receive","unexpected_process_count",json!(2),json!(1))));
        assert!(diagnostic_events(&observation).contains(&json!({"schema_version":1,"stage":"rpc","rpc":rpc,"predicate":"process_guard_rejected"})));
    }
}

#[test]
fn qa_i06_cancel_deadline() {
    for (mode,control,reason,label) in [("ok",1,"user_cancel","user_cancel"),("ok",2,"invalid_control","control_error"),("hang",0,"deadline","deadline")] {
        let observation=exercise(&format!("QI06-{label}"),mode,control,None,|session,r|session.preflight(r,&[r.checkout_root.join("task.json")]));
        assert_eq!(observation.result,Err(reason.into()));
        assert!(diagnostic_events(&observation).contains(&json!({"schema_version":1,"stage":"rpc","rpc":"initialize","predicate":label})));
        assert!(observation.elapsed<Duration::from_secs(3));
        if control!=0 { assert!(observation.trace.is_empty()); }
    }
    let failed=exercise("QI06-write","ok",0,Some(0),|session,r|session.preflight(r,&[r.checkout_root.join("task.json")]));
    assert_eq!(failed.result,Err("evidence_write_failed".into()));
    assert!(failed.events.is_empty() && failed.trace.is_empty());
}

#[test]
fn qa_i07_false_review_no_authority() {
    let observation=exercise("QI07","ok",0,None,|session,r|{
        let review=r.checkout_root.parent().unwrap().join("false-review.json");
        let value=json!({"schema_version":2,"reviewer":"independent synthetic QA","trial_selection_ref":"offline only",
            "codex_sha256":r.worker_sha256,"checkout_root":r.checkout_root,"model":"gpt-6-astra","effort":"high","profile_sources":[],
            "findings":{"native_read_only_available":false,"no_external_tool_or_hook_effects":false,"codex_managed_chatgpt":false,"no_custom_provider":false},
            "launch_policy_id":"codex-0.154.0-readonly-no-external-tools-v2","launch_policy_sha256":crate::launch_policy::digest(),
            "source_inventory_ref":r.checkout_root.parent().unwrap().join("never-collected-inventory.json"),"source_inventory_sha256":"d".repeat(64)});
        let bytes=serde_json::to_vec(&value).unwrap(); fs::write(&review,&bytes).unwrap();
        let native=native_review_request(r,&review,&request::digest(&bytes));
        assert_eq!(native.verify_review(),Err("profile_unqualified".into()));
        let public_original: probe::request::Request=serde_json::from_value(serde_json::to_value(&native).unwrap()).unwrap();
        assert_eq!(public_original.verify_review(),Err("profile_unqualified".into()));
        // An emitted successful accounting observation is evidence, never a review mutation.
        session.process_guard(RpcStage::Initialize,Checkpoint::BeforeSend)?;
        assert_eq!(native.verify_review(),Err("profile_unqualified".into()));
        assert_eq!(public_original.verify_review(),Err("profile_unqualified".into()));
        assert_eq!(fs::read(&review).unwrap(),bytes);
        let mut injected=value.clone(); injected["diagnostic"]=json!({"predicate":"only_worker","accepted":true});
        let injected_path=review.with_file_name("injected-review.json");
        let injected_bytes=serde_json::to_vec(&injected).unwrap(); fs::write(&injected_path,&injected_bytes).unwrap();
        let injected_request=native_review_request(r,&injected_path,&request::digest(&injected_bytes));
        assert_eq!(injected_request.verify_review(),Err("profile_unqualified".into()));
        session.source_review(SourceBoundary::PostPreflight,||native.verify_review())
    });
    assert_eq!(observation.result,Err("profile_unqualified".into()));
    assert!(observation.trace.is_empty());
    assert_eq!(diagnostic_events(&observation),vec![accounting("initialize","before_send","only_worker",json!(1),json!(1)),json!({"schema_version":1,"stage":"source_review","boundary":"post_preflight","predicate":"review_rejected"})]);
}
