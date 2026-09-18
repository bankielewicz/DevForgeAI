mod support;
use devforgeai_codex_worker_probe::{
    journal::{self, Journal},
    process_windows::{Incoming, OwnedProcess},
    request,
    runner::{self, Options},
};
use serde_json::json;
use std::{
    fs,
    io::Write,
    process::{Command, Stdio},
    time::Duration,
};

#[test]
fn protocol_typed_events_duplicates_pagination_and_failures() {
    for sub in 6..=24 {
        let f = support::Fixture::new(&format!("WF-04-{sub}"));
        let (exit, v) = f.run();
        assert_eq!(exit, 4, "sub {sub}: {v}");
        let expected = match sub {
            13 | 14 => "tool_activity",
            20 => "worker_interrupted",
            22 => "worker_exited",
            24 => "rpc_error",
            _ => "protocol_error",
        };
        assert_eq!(v["reason"], expected, "sub {sub}: {v}");
    }
    for (sub, exit) in [
        (6, 3),
        (7, 3),
        (9, 0),
        (10, 3),
        (11, 4),
        (12, 4),
        (13, 0),
        (14, 3),
    ] {
        let f = support::Fixture::new(&format!("WF-03-{sub}"));
        let (actual, v) = f.run();
        assert_eq!(actual, exit, "sub {sub}: {v}");
    }
    let f = support::Fixture::new("WF-01-2");
    let (exit, v) = f.run();
    assert_eq!(exit, 0, "{v}");
}

#[test]
fn cli_control_and_inspect_paths() {
    for bytes in [b"invalid\n".to_vec(), vec![b'x'; 1025], vec![]] {
        let f = support::Fixture::new("WF-15");
        let mut child = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
            .args(["run", "--request"])
            .arg(&f.input)
            .stdin(Stdio::piped())
            .stdout(Stdio::null())
            .spawn()
            .unwrap();
        child.stdin.take().unwrap().write_all(&bytes).unwrap();
        assert_eq!(
            child.wait().unwrap().code(),
            Some(if bytes.is_empty() { 5 } else { 4 })
        );
    }
    let f = support::Fixture::new("WF-01");
    assert_eq!(f.run().0, 0);
    for (after, limit, exit) in [
        ("0", "2", 0),
        ("999", "1", 2),
        ("no", "2", 2),
        ("0", "101", 2),
    ] {
        let out = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
            .args(["inspect", "--run-dir"])
            .arg(&f.request.run_dir)
            .args(["--after", after, "--limit", limit])
            .output()
            .unwrap();
        assert_eq!(out.status.code(), Some(exit));
    }
    let out = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .args(["inspect", "--run-dir"])
        .arg(f.root.path().join("missing"))
        .args(["--after", "0", "--limit", "1"])
        .output()
        .unwrap();
    assert_eq!(out.status.code(), Some(4));
    let out = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .args(["run", "--request", "relative"])
        .output()
        .unwrap();
    assert_eq!(out.status.code(), Some(2));
    let out = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .args(["run", "--request"])
        .arg(f.root.path().join("missing.json"))
        .output()
        .unwrap();
    assert_eq!(out.status.code(), Some(2));
}

#[test]
fn fixture_inventory_and_bounded_request_reads() {
    for (name, bytes) in [
        ("extra", b"x".as_slice()),
        ("peer-case.txt", b"WF-99\n"),
        ("peer-case.txt", b"WF-01"),
        ("peer-case.txt", b"WF-01-a\n"),
        ("peer-case.txt", b"\xff\n"),
    ] {
        let f = support::Fixture::new("WF-17");
        fs::write(f.request.checkout_root.join(name), bytes).unwrap();
        assert!(request::validate(&f.input).is_err());
    }
    let f = support::Fixture::new("WF-17");
    fs::remove_file(f.request.checkout_root.join("task.json")).unwrap();
    assert!(request::validate(&f.input).is_err());
    fs::write(&f.input, vec![b' '; 65537]).unwrap();
    assert_eq!(request::validate(&f.input).unwrap_err(), "input_limit");
    assert!(request::valid_id("a._-Z9"));
    assert!(!request::valid_id(""));
    assert!(!request::valid_id(&"a".repeat(65)));
    let f = support::Fixture::new("WF-17");
    assert!(f.request.verify_review().is_ok());
    let mut r = f.request.clone();
    r.profile = json!({"model":"a","effort":"b","review_ref":"x","review_sha256":"0".repeat(64)});
    assert!(r.profile().is_err());
    r = f.request.clone();
    r.run_dir = "relative".into();
    fs::write(&f.input, serde_json::to_vec(&r).unwrap()).unwrap();
    assert!(request::validate(&f.input).is_err());
}

#[test]
fn journal_corruption_is_not_promoted() {
    for variant in 0..8 {
        let f = support::Fixture::new("WF-12");
        let mut j = Journal::create(&f.request).unwrap();
        if variant == 0 {
            assert_eq!(
                journal::inspect(&f.request.run_dir, 0, 1).unwrap_err(),
                "evidence_incomplete"
            );
            continue;
        }
        j.append("admitted", json!({})).unwrap();
        if variant == 1 {
            fs::write(f.request.run_dir.join("task.json"), b"different").unwrap();
        }
        if variant == 2 {
            j.append(
                "terminal",
                json!({"outcome":"impossible","open_work":["w"]}),
            )
            .unwrap();
        }
        if variant == 3 {
            j.append(
                "terminal",
                json!({"outcome":"completed","open_work":["w"],"tree_stopped":false}),
            )
            .unwrap();
        }
        if variant == 4 {
            j.append("worker_event", json!({"method":"final_result"}))
                .unwrap();
            j.append("worker_event", json!({"method":"final_result"}))
                .unwrap();
        }
        if variant == 5 {
            j.append(
                "worker_event",
                json!({"method":"final_result","text":"{}","thread_id":"t","turn_id":"u"}),
            )
            .unwrap();
            j.append("terminal",json!({"outcome":"completed","open_work":["w"],"tree_stopped":true,"fixture_unchanged":true,"oracle":"match","thread_id":"t","turn_id":"u"})).unwrap();
        }
        if variant == 6 {
            fs::write(f.request.run_dir.join("inputs.json"), b"{}").unwrap();
        }
        if variant == 7 {
            fs::write(f.request.run_dir.join("request.json"), b"{}").unwrap();
        }
        assert_eq!(
            journal::inspect(&f.request.run_dir, 0, 100).unwrap_err(),
            "evidence_corrupt"
        );
        assert!(j.append("unknown", json!({})).is_err());
    }
}

#[test]
fn process_failure_and_pipe_ownership() {
    let f = support::Fixture::new("WF-17");
    let bad = f.root.path().join("not executable.exe");
    fs::write(&bad, b"not an executable").unwrap();
    assert!(OwnedProcess::spawn(&bad, &[], f.root.path()).is_err());
    assert!(
        OwnedProcess::spawn(
            &f.request.worker_executable,
            &["x\0y".into()],
            f.root.path()
        )
        .is_err()
    );
    let mut p = OwnedProcess::spawn(&f.request.worker_executable, &[], f.root.path()).unwrap();
    assert!(!p.wait_stopped(Duration::ZERO));
    p.send(&json!({"roundtrip":"quoted \"text\""})).unwrap();
    match p.incoming.recv_timeout(Duration::from_secs(2)).unwrap() {
        Incoming::Line(bytes) => assert_eq!(
            serde_json::from_slice::<serde_json::Value>(&bytes).unwrap()["roundtrip"],
            "quoted \"text\""
        ),
        _ => panic!("missing echo"),
    }
    assert!(p.stop(Duration::from_secs(5)));
    assert!(p.send(&json!({})).is_err());
}

#[test]
fn scenario_cancel_and_evidence_failure_precedence() {
    let f = support::Fixture::new("WF-20");
    let mut r = f.request.clone();
    r.scenario = "cancel".into();
    fs::write(&f.input, serde_json::to_vec(&r).unwrap()).unwrap();
    assert_eq!(f.run().0, 5);
    for n in [0, 1, 2, 3] {
        let f = support::Fixture::new("WF-19-2");
        let result = runner::run(
            &f.input,
            Options {
                fail_write_after: Some(n),
                uncertain_cleanup: n == 3,
                ..Default::default()
            },
            &mut |_| {},
        );
        if n < 2 {
            assert!(result.is_err());
        } else {
            assert_eq!(result.unwrap().0, if n == 3 { 7 } else { 4 });
        }
    }
}
