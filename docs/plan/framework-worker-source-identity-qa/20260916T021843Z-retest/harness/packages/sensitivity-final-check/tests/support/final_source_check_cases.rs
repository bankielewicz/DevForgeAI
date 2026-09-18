use super::*;
use std::{cell::Cell, fs};

#[test]
fn final_native_check_rejects_missing_review_for_work_and_preflight() {
    let request = request::Request {
        schema_version: 2,
        project_id: "p".into(),
        checkout_id: "c".into(),
        work_id: "w".into(),
        run_id: "r".into(),
        candidate_sha256: "a".repeat(64),
        checkout_root: std::path::PathBuf::from(r"C:\not-an-admitted-fixture"),
        run_dir: std::path::PathBuf::from(r"C:\not-an-admitted-run"),
        worker_executable: std::path::PathBuf::from(r"C:\not-an-admitted-worker.exe"),
        worker_sha256: "b".repeat(64),
        adapter: "codex-0.154.0-stdio".into(),
        scenario: "complete".into(),
        profile: Value::Null,
    };
    for preflight in [false, true] {
        assert_eq!(
            verify_before_spawn(&request, preflight).unwrap_err(),
            "profile_unqualified"
        );
    }
}

#[test]
fn si_t08_changed_source_after_intent_stops_before_real_process_creation() {
    let base = std::env::var_os("WF_TEST_EVIDENCE")
        .map(std::path::PathBuf::from)
        .unwrap_or_else(std::env::temp_dir);
    fs::create_dir_all(&base).unwrap();
    let root = tempfile::Builder::new()
        .prefix("SI-T08-")
        .tempdir_in(base)
        .unwrap();
    let fixture = root.path().join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    // Admission permits only the package-built protocol peer beside this test target.
    let current = std::env::current_exe().unwrap();
    let executable = current
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join("protocol-peer.exe");
    assert!(
        executable.is_file(),
        "build the required peer before this unit test"
    );
    let source = root.path().join("reviewed-config.toml");
    fs::write(&source, b"before\n").unwrap();
    let reviewed = request::hash_file(&source).unwrap();
    let input = root.path().join("request.json");
    fs::write(
        &input,
        serde_json::to_vec(&json!({
            "schema_version":1,"project_id":"p","checkout_id":"c","work_id":"w","run_id":"r",
            "candidate_sha256":request::digest(request::TASK),"checkout_root":fixture,
            "run_dir":root.path().join("run"),"worker_executable":executable,
            "worker_sha256":request::hash_file(&executable).unwrap(),"adapter":"peer",
            "scenario":"complete","profile":null
        }))
        .unwrap(),
    )
    .unwrap();
    request::validate(&input).expect("valid compiled child and immutable fixture before stimulus");
    assert_eq!(request::hash_file(&source).unwrap(), reviewed);
    let called = Cell::new(0);
    let mut kinds = Vec::new();
    let outcome = execute_with_final_check(
        &input,
        Options {
            total: Duration::from_secs(2),
            rpc: Duration::from_millis(250),
            grace: Duration::from_millis(20),
            teardown: Duration::from_secs(1),
            ..Default::default()
        },
        &mut |event| {
            let kind = event["kind"].as_str().unwrap().to_owned();
            if kind == "spawn_intent" {
                fs::write(&source, b"changed after qualification\n").unwrap();
            }
            kinds.push(kind);
        },
        false,
        &mut |_, _| {
            called.set(called.get() + 1);
            if request::hash_file(&source)? != reviewed {
                Err("profile_unqualified".into())
            } else {
                Ok(())
            }
        },
    )
    .unwrap();
    fs::write(
        root.path().join("observed.json"),
        serde_json::to_vec_pretty(&json!({
            "code":outcome.0,"terminal":outcome.1,"event_kinds":kinds,"final_checks":called.get()
        }))
        .unwrap(),
    )
    .unwrap();
    if std::env::var_os("WF_TEST_EVIDENCE").is_some() {
        let _ = root.keep();
    }
    assert_eq!(
        called.get(),
        1,
        "the runner must recheck after durable intent"
    );
    assert_eq!(outcome.0, 3);
    assert_eq!(outcome.1["reason"], "profile_unqualified");
    assert_eq!(outcome.1["tree_stopped"], true);
    assert_eq!(outcome.1["worker_exit_code"], Value::Null);
    assert!(kinds.iter().any(|kind| kind == "spawn_intent"));
    assert!(!kinds.iter().any(|kind| kind == "server_started"));
}

#[test]
fn qa_independent_final_check_is_after_intent_and_before_spawn() {
    use std::{cell::RefCell, rc::Rc};

    let root = tempfile::Builder::new()
        .prefix("QA-final-order-")
        .tempdir()
        .unwrap();
    let fixture = root.path().join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    let executable = std::env::current_exe()
        .unwrap()
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join("protocol-peer.exe");
    assert!(executable.is_file(), "protocol peer must be built first");
    let input = root.path().join("request.json");
    fs::write(
        &input,
        serde_json::to_vec(&json!({
            "schema_version":1,"project_id":"p","checkout_id":"c","work_id":"w","run_id":"qa-order",
            "candidate_sha256":request::digest(request::TASK),"checkout_root":fixture,
            "run_dir":root.path().join("run"),"worker_executable":executable,
            "worker_sha256":request::hash_file(&executable).unwrap(),"adapter":"peer",
            "scenario":"complete","profile":null
        }))
        .unwrap(),
    )
    .unwrap();
    request::validate(&input).expect("independent ordering fixture must be admitted");

    let observed = Rc::new(RefCell::new(Vec::<String>::new()));
    let emitted = observed.clone();
    let checked = Cell::new(0_u32);
    let checked_observations = observed.clone();
    let outcome = execute_with_final_check(
        &input,
        Options {
            total: Duration::from_secs(2),
            rpc: Duration::from_millis(250),
            grace: Duration::from_millis(20),
            teardown: Duration::from_secs(1),
            ..Default::default()
        },
        &mut |event| {
            emitted
                .borrow_mut()
                .push(event["kind"].as_str().unwrap().to_owned());
        },
        false,
        &mut |_, _| {
            checked.set(checked.get() + 1);
            assert!(
                checked_observations
                    .borrow()
                    .iter()
                    .any(|kind| kind == "spawn_intent"),
                "final check must observe durable spawn intent first"
            );
            Err("profile_unqualified".into())
        },
    )
    .unwrap();

    let kinds = observed.borrow();
    assert_eq!(checked.get(), 1);
    assert_eq!(outcome.0, 3);
    assert_eq!(outcome.1["reason"], "profile_unqualified");
    assert_eq!(outcome.1["worker_exit_code"], Value::Null);
    assert_eq!(outcome.1["tree_stopped"], true);
    assert!(!kinds.iter().any(|kind| kind == "server_started"));
    assert!(
        !root.path().join("peer-trace.jsonl").exists(),
        "the rejected final check must create no peer-side trace"
    );
}
