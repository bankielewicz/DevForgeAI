mod support;
use devforgeai_codex_worker_probe::{
    journal::{Journal, inspect},
    request::{self, Request},
};
use serde_json::json;
use std::fs;
#[test]
fn unapproved_peer_executable_is_rejected_before_spawn() {
    let f = support::Fixture::new("WF-17");
    let copied = f.root.path().join("unapproved.exe");
    fs::copy(&f.request.worker_executable, &copied).unwrap();
    let mut r = f.request.clone();
    r.worker_executable = copied;
    fs::write(&f.input, serde_json::to_vec(&r).unwrap()).unwrap();
    assert!(request::validate(&f.input).is_err());
}
#[test]
fn duplicate_nested_profile_is_rejected() {
    let f = support::Fixture::new("WF-17");
    let raw=serde_json::to_string(&f.request).unwrap().replace("\"profile\":null","\"profile\":{\"model\":\"a\",\"model\":\"b\",\"effort\":\"high\",\"review_ref\":\"C:/review\",\"review_sha256\":\"x\"}");
    assert!(serde_json::from_str::<Request>(&raw).is_err());
}
#[test]
fn terminal_claim_requires_observed_result() {
    let f = support::Fixture::new("WF-12");
    let mut j = Journal::create(&f.request).unwrap();
    j.append("admitted", json!({})).unwrap();
    j.append("terminal",json!({"outcome":"completed","reason":"completed","thread_id":"t","turn_id":"u","worker_exit_code":0,"tree_stopped":true,"fixture_unchanged":true,"oracle":"match","usage":null,"open_work":["w"]})).unwrap();
    assert_eq!(
        inspect(&f.request.run_dir, 0, 100).unwrap_err(),
        "evidence_corrupt"
    );
}
#[test]
fn successful_peer_has_observed_zero_exit() {
    let f = support::Fixture::new("WF-01");
    let (exit, v) = f.run();
    assert_eq!(exit, 0);
    assert_eq!(v["worker_exit_code"], 0);
}

#[test]
fn all_pre_response_notifications_are_reconciled() {
    let f = support::Fixture::new("WF-05-2");
    let (exit, v) = f.run();
    assert_eq!(exit, 4, "{v}");
    assert_eq!(v["reason"], "protocol_error");
}
#[test]
fn usage_retains_only_typed_counters() {
    let f = support::Fixture::new("WF-08-3");
    let (exit, v) = f.run();
    assert_eq!(exit, 0);
    assert!(!v.to_string().contains("untrusted-private"));
    assert_eq!(v["usage"]["total"]["totalTokens"], 17);
}

#[test]
fn duplicate_completions_are_idempotent_and_conflicts_fail() {
    for (case, code) in [("WF-05-3", 0), ("WF-05-4", 4)] {
        let f = support::Fixture::new(case);
        let (actual, terminal) = f.run();
        assert_eq!(actual, code, "{terminal}");
        let events = fs::read_to_string(f.request.run_dir.join("journal.jsonl")).unwrap();
        let events: Vec<serde_json::Value> = events
            .lines()
            .map(|line| serde_json::from_str(line).unwrap())
            .collect();
        assert_eq!(events.iter().filter(|e| e["kind"] == "terminal").count(), 1);
        assert_eq!(
            events
                .iter()
                .filter(|e| e["data"]["method"] == "final_result")
                .count(),
            1
        );
        if code == 4 {
            assert_eq!(terminal["reason"], "protocol_error");
        }
    }
}

#[test]
fn valid_output_cannot_override_nonzero_worker_exit() {
    let f = support::Fixture::new("WF-01-3");
    let (code, terminal) = f.run();
    assert_eq!(code, 4, "{terminal}");
    assert_eq!(terminal["reason"], "worker_failed");
    assert_eq!(terminal["worker_exit_code"], 9);
    assert_eq!(terminal["tree_stopped"], true);
}
#[test]
fn captured_native_launcher_reparse_is_rejected_without_launching() {
    let f = support::Fixture::new("WF-17");
    let mut r = f.request.clone();
    r.adapter = "codex-0.154.0-stdio".into();
    r.profile = json!({"model":"unexecuted","effort":"high","review_ref":f.root.path().join("not-selected-review.json"),"review_sha256":"0".repeat(64)});
    let discovery: serde_json::Value =
        serde_json::from_str(include_str!("fixtures/schema-command.json")).unwrap();
    r.worker_executable = discovery["executable"].as_str().unwrap().into();
    fs::write(&f.input, serde_json::to_vec(&r).unwrap()).unwrap();
    assert_eq!(request::validate(&f.input).unwrap_err(), "reparse_path");
    r.worker_executable = f.request.worker_executable.clone();
    fs::write(&f.input, serde_json::to_vec(&r).unwrap()).unwrap();
    assert_eq!(request::validate(&f.input).unwrap_err(), "reparse_path");
    assert!(!f.root.path().join("peer-trace.jsonl").exists());
}

#[test]
fn cancellation_before_ids_allows_cooperative_eof_exit() {
    use devforgeai_codex_worker_probe::runner::{self, Options};
    use std::sync::{
        Arc,
        atomic::{AtomicU8, Ordering},
    };
    use std::time::Duration;
    let f = support::Fixture::new("WF-15");
    let control = Arc::new(AtomicU8::new(0));
    let options = Options {
        control: control.clone(),
        grace: Duration::from_secs(1),
        ..Default::default()
    };
    let (code, terminal) = runner::run(&f.input, options, &mut |event| {
        if event["kind"] == "server_started" {
            control.store(1, Ordering::SeqCst);
        }
    })
    .unwrap();
    assert_eq!(code, 5);
    assert_eq!(
        terminal["worker_exit_code"], 0,
        "cooperative peer was forcibly killed: {terminal}"
    );
    assert_eq!(terminal["tree_stopped"], true);
    assert!(
        f.trace().is_empty(),
        "a request escaped the cancellation latch"
    );
}

#[test]
fn lost_interrupt_transport_still_waits_for_owned_process() {
    use devforgeai_codex_worker_probe::{
        process_windows::OwnedProcess, protocol::Session, runner::Options,
    };
    use std::time::{Duration, Instant};
    let f = support::Fixture::new("WF-15");
    let mut process =
        OwnedProcess::spawn(&f.request.worker_executable, &[], f.root.path()).unwrap();
    let mut journal = Journal::create(&f.request).unwrap();
    let options = Options {
        grace: Duration::from_secs(1),
        ..Default::default()
    };
    process.close_input();
    let mut emit = |_: &serde_json::Value| {};
    let mut session = Session::new(
        &mut process,
        &mut journal,
        &mut emit,
        &options,
        Instant::now() + Duration::from_secs(2),
    );
    session.thread = Some("bound-thread".into());
    session.turn = Some("bound-turn".into());
    session.interrupt();
    assert_eq!(session.process.exit_code(), Some(0));
    assert_eq!(session.process.active().unwrap(), 0);
}

#[test]
fn home_boundary_only_allows_peer_temporary_roots() {
    let f = support::Fixture::new("WF-17");
    let home = f.root.path();
    let temp = home.join("temp");
    assert!(
        request::check_home_boundary(
            &home.join("credential-fixture"),
            &home.join("run"),
            home,
            &temp,
            true
        )
        .is_err()
    );
    assert!(
        request::check_home_boundary(&temp.join("fixture"), &temp.join("run"), home, &temp, false)
            .is_err()
    );
    assert!(
        request::check_home_boundary(&temp.join("fixture"), &temp.join("run"), home, &temp, true)
            .is_ok()
    );
    let other = home.parent().unwrap().join("separate-project");
    assert!(
        request::check_home_boundary(
            &other.join("fixture"),
            &other.join("run"),
            home,
            &temp,
            false
        )
        .is_ok()
    );
}
