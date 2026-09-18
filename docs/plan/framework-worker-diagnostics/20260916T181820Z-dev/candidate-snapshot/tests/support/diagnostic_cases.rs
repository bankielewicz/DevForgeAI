use super::*;
use std::{fs, path::PathBuf};

fn with_session(test: impl FnOnce(&mut Session<'_>, &Request)) -> Vec<Value> {
    let base = std::env::var_os("WF_TEST_EVIDENCE")
        .map(PathBuf::from)
        .unwrap_or_else(std::env::temp_dir);
    fs::create_dir_all(&base).unwrap();
    let root = tempfile::Builder::new()
        .prefix("diagnostic-")
        .tempdir_in(base)
        .unwrap();
    let fixture = root.path().join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    fs::write(fixture.join("peer-case.txt"), "WF-01\n").unwrap();
    let exe = std::env::current_exe()
        .unwrap()
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join("protocol-peer.exe");
    let r = Request {
        schema_version: 1,
        project_id: "p".into(),
        checkout_id: "c".into(),
        work_id: "w".into(),
        run_id: "r".into(),
        candidate_sha256: request::digest(request::TASK),
        checkout_root: fixture.clone(),
        run_dir: root.path().join("run"),
        worker_executable: exe.clone(),
        worker_sha256: request::hash_file(&exe).unwrap(),
        adapter: "peer".into(),
        scenario: "complete".into(),
        profile: Value::Null,
    };
    let inventory = r.fixture_inventory().unwrap();
    let mut process = OwnedProcess::spawn(
        &exe,
        &[
            "--fixture-root".into(),
            fixture.to_string_lossy().into_owned(),
        ],
        &fixture,
    )
    .unwrap();
    let mut journal = Journal::create(&r).unwrap();
    let options = Options {
        total: Duration::from_secs(2),
        rpc: Duration::from_millis(250),
        grace: Duration::from_millis(20),
        teardown: Duration::from_secs(1),
        ..Default::default()
    };
    let mut emitted = Vec::new();
    {
        let mut emit = |v: &Value| emitted.push(v.clone());
        let mut session = Session::new(
            &mut process,
            &mut journal,
            &mut emit,
            &options,
            Instant::now() + options.total,
        );
        test(&mut session, &r);
        assert!(session.thread.is_none());
        assert!(session.turn.is_none());
    }
    assert!(process.stop(options.teardown));
    assert_eq!(process.active(), Ok(0));
    assert_eq!(r.fixture_inventory().unwrap(), inventory);
    let trace = fs::read_to_string(root.path().join("peer-trace.jsonl")).unwrap_or_default();
    assert!(!trace.contains("thread/start") && !trace.contains("turn/start"));
    drop(journal);
    let persisted = fs::read_to_string(r.run_dir.join("journal.jsonl")).unwrap();
    let events: Vec<Value> = persisted
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    assert_eq!(emitted, events);
    if std::env::var_os("WF_TEST_EVIDENCE").is_some() {
        let _ = root.keep();
    }
    events
}

#[test]
fn diagnostic_source_review_preserves_real_denial_at_both_boundaries() {
    let events = with_session(|session, r| {
        let mut native = r.clone();
        native.schema_version = 2;
        native.adapter = "codex-0.154.0-stdio".into();
        native.profile = json!({
            "model":"gpt-6-astra","effort":"high",
            "review_ref":r.checkout_root.parent().unwrap().join("missing-review.json"),
            "review_sha256":"a".repeat(64),
            "launch_policy_id":crate::launch_policy::ID,
            "launch_policy_sha256":crate::launch_policy::digest()
        });
        assert_eq!(
            native.verify_preflight_review(),
            Err("profile_unqualified".into())
        );
        // Real dispatch calls the post-spawn review before ANY RPC; no native spawn.
        assert_eq!(session.dispatch(&native), Err("profile_unqualified".into()));
        assert_eq!(
            session.source_review(SourceBoundary::PostPreflight, || native.verify_review()),
            Err("profile_unqualified".into())
        );
        assert_eq!(
            session.source_review(SourceBoundary::PostSpawn, || Ok(7)),
            Ok(7)
        );
    });
    let observed: Vec<_> = events.iter().map(|e| e["data"].clone()).collect();
    assert_eq!(observed, ["post_spawn", "post_preflight"].map(|boundary| json!({"diagnostic":{
        "schema_version":1,"stage":"source_review","boundary":boundary,"predicate":"review_rejected"
    }})));
}

#[test]
fn diagnostic_source_write_failure_is_not_success_and_never_serializes_error_text() {
    let events = with_session(|session, _| {
        let result: Result<()> = session.source_review(SourceBoundary::PostSpawn, || {
            Err("PRIVATE_SOURCE_DETAIL".into())
        });
        assert_eq!(result, Err("PRIVATE_SOURCE_DETAIL".into()));
        session.journal.inject_write_failure_after(1);
        let result: Result<()> = session.source_review(SourceBoundary::PostPreflight, || {
            Err("profile_unqualified".into())
        });
        assert_eq!(result, Err("evidence_write_failed".into()));
    });
    assert_eq!(events.len(), 1);
    assert!(
        !serde_json::to_string(&events)
            .unwrap()
            .contains("PRIVATE_SOURCE_DETAIL")
    );
}

#[test]
fn diagnostic_process_guard_keeps_zero_active_denied_before_send_and_at_final_check() {
    let events = with_session(|session, _| {
        assert!(session.process.stop(Duration::from_secs(1)));
        for (rpc, checkpoint) in [
            (RpcStage::ConfigRead, Checkpoint::BeforeSend),
            (RpcStage::FinalCheck, Checkpoint::FinalCheck),
        ] {
            assert_eq!(
                session.process_guard(rpc, checkpoint),
                Err("profile_unqualified".into())
            );
        }
    });
    assert_eq!(events.len(), 2);
    for (event, (rpc, checkpoint)) in events.iter().zip([
        ("config_read", "before_send"),
        ("final_check", "final_check"),
    ]) {
        assert_eq!(
            event["data"],
            json!({"diagnostic":{
                "schema_version":1,"stage":"process_accounting","rpc":rpc,"checkpoint":checkpoint,
                "predicate":"unexpected_process_count","total_processes":1,"active_processes":0
            }})
        );
    }
}
