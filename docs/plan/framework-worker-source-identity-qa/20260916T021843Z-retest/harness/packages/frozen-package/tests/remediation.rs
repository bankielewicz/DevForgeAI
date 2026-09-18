mod support;
use devforgeai_codex_worker_probe::{
    journal::Journal,
    process_windows::OwnedProcess,
    protocol::Session,
    runner::{self, Options},
};
use serde_json::{Value, json};
use std::{
    fs,
    os::windows::io::{AsRawHandle, FromRawHandle, OwnedHandle},
    sync::{
        Arc,
        atomic::{AtomicU8, Ordering},
    },
    time::{Duration, Instant},
};
use windows_sys::Win32::{
    Foundation::WAIT_OBJECT_0,
    System::Threading::{OpenProcess, PROCESS_SYNCHRONIZE, WaitForSingleObject},
};

fn held(pid: u32) -> OwnedHandle {
    unsafe {
        let h = OpenProcess(PROCESS_SYNCHRONIZE, 0, pid);
        assert!(!h.is_null());
        OwnedHandle::from_raw_handle(h)
    }
}

#[test]
fn full_pipe_server_reply_deadline_and_cancel_stop_descendants() {
    for cancel in [false, true] {
        let f = support::Fixture::new("WF-16-90");
        let control = Arc::new(AtomicU8::new(0));
        let signal = control.clone();
        let path = f.input.clone();
        let started = Instant::now();
        let worker = std::thread::spawn(move || {
            runner::run(
                &path,
                Options {
                    total: Duration::from_millis(750),
                    rpc: Duration::from_millis(500),
                    grace: Duration::from_millis(200),
                    teardown: Duration::from_millis(500),
                    control,
                    ..Default::default()
                },
                &mut |_| {},
            )
            .unwrap()
        });
        let ids = loop {
            if let Ok(bytes) = fs::read(f.root.path().join("peer-pids.json"))
                && let Ok(ids) = serde_json::from_slice::<Value>(&bytes)
            {
                break ids;
            }
            assert!(started.elapsed() < Duration::from_secs(2));
            std::thread::sleep(Duration::from_millis(2));
        };
        let handles = [
            held(ids["peer"].as_u64().unwrap() as u32),
            held(ids["descendant"].as_u64().unwrap() as u32),
        ];
        if cancel {
            while !f.root.path().join("full-pipe-ready").exists() {
                assert!(started.elapsed() < Duration::from_secs(2));
                std::thread::sleep(Duration::from_millis(2));
            }
            std::thread::sleep(Duration::from_millis(100));
            signal.store(1, Ordering::SeqCst);
        }
        while !worker.is_finished() && started.elapsed() < Duration::from_secs(3) {
            std::thread::sleep(Duration::from_millis(5));
        }
        assert!(
            worker.is_finished(),
            "write blocked deadline/control thread"
        );
        let (code, terminal) = worker.join().unwrap();
        assert_eq!(code, if cancel { 5 } else { 6 }, "{terminal}");
        assert_eq!(
            terminal["reason"],
            if cancel { "user_cancel" } else { "deadline" }
        );
        assert_eq!(terminal["tree_stopped"], true);
        assert_eq!(terminal["fixture_unchanged"], true);
        for h in handles {
            assert_eq!(
                unsafe { WaitForSingleObject(h.as_raw_handle(), 0) },
                WAIT_OBJECT_0
            );
        }
    }
}

#[test]
fn ordinary_rpc_write_and_interrupt_share_bounded_teardown() {
    for cancel in [0, 1, 2] {
        let f = support::Fixture::new("WF-15");
        let mut process = OwnedProcess::spawn(
            &f.request.worker_executable,
            &["--hold".into()],
            f.root.path(),
        )
        .unwrap();
        let handle = held(process.pid);
        let control = Arc::new(AtomicU8::new(0));
        let signal = control.clone();
        let setter = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(50));
            signal.store(cancel, Ordering::SeqCst);
        });
        let start = Instant::now();
        let result = process.send_until(&json!({"id":1,"method":"initialize","params":{"clientInfo":{"name":"x".repeat(262144)}}}), start + Duration::from_millis(150), Some(&control));
        assert_eq!(
            result.unwrap_err(),
            match cancel {
                0 => "deadline",
                1 => "user_cancel",
                _ => "invalid_control",
            }
        );
        setter.join().unwrap();
        let mut journal = Journal::create(&f.request).unwrap();
        let options = Options {
            grace: Duration::from_millis(100),
            ..Default::default()
        };
        let mut emit = |_: &Value| {};
        let mut session = Session::new(
            &mut process,
            &mut journal,
            &mut emit,
            &options,
            Instant::now(),
        );
        session.thread = Some("thread-1".into());
        session.turn = Some("turn-1".into());
        session.interrupt();
        assert!(process.stop(Duration::from_millis(500)));
        assert!(start.elapsed() < Duration::from_secs(1));
        assert_eq!(
            unsafe { WaitForSingleObject(handle.as_raw_handle(), 0) },
            WAIT_OBJECT_0
        );
    }
}

#[test]
fn interrupt_write_into_full_pipe_obeys_single_grace_budget() {
    let f = support::Fixture::new("WF-15");
    let mut process = OwnedProcess::spawn(
        &f.request.worker_executable,
        &["--hold".into()],
        f.root.path(),
    )
    .unwrap();
    let handle = held(process.pid);
    // Windows CreatePipe's default buffer holds this complete 4096-byte line.
    // Its successful completion leaves no pending write, but no free pipe space.
    let fill = json!({"pad":"x".repeat(4085)});
    assert_eq!(serde_json::to_vec(&fill).unwrap().len() + 1, 4096);
    process
        .send_until(&fill, Instant::now() + Duration::from_secs(1), None)
        .unwrap();
    let mut journal = Journal::create(&f.request).unwrap();
    let options = Options {
        grace: Duration::from_millis(150),
        ..Default::default()
    };
    let mut emit = |_: &Value| {};
    let mut session = Session::new(
        &mut process,
        &mut journal,
        &mut emit,
        &options,
        Instant::now(),
    );
    session.thread = Some("thread-1".into());
    session.turn = Some("turn-1".into());
    let start = Instant::now();
    session.interrupt();
    assert!(start.elapsed() >= Duration::from_millis(140));
    assert!(start.elapsed() < Duration::from_millis(400));
    assert!(process.stop(Duration::from_millis(500)));
    assert_eq!(
        unsafe { WaitForSingleObject(handle.as_raw_handle(), 0) },
        WAIT_OBJECT_0
    );
}

#[test]
fn malformed_error_payloads_never_reach_journal_or_stdout() {
    for case in (90..=104)
        .map(|n| format!("WF-07-{n}"))
        .chain((90..=93).map(|n| format!("WF-04-{n}")))
    {
        let f = support::Fixture::new(&case);
        let mut child =
            std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
                .args(["run", "--request"])
                .arg(&f.input)
                .stdin(std::process::Stdio::piped())
                .stdout(std::process::Stdio::piped())
                .stderr(std::process::Stdio::piped())
                .spawn()
                .unwrap();
        // Keep control stdin open until the real terminal exits.
        let input = child.stdin.take().unwrap();
        let out = child.wait_with_output().unwrap();
        drop(input);
        assert_eq!(out.status.code(), Some(4), "{case}");
        let journal = fs::read(f.request.run_dir.join("journal.jsonl")).unwrap();
        for bytes in [&out.stdout, &out.stderr, &journal] {
            assert!(
                !String::from_utf8_lossy(bytes).contains("DEV_PRIVATE_SENTINEL_9201"),
                "{case}"
            );
        }
        let events: Vec<Value> = String::from_utf8(journal)
            .unwrap()
            .lines()
            .map(|s| serde_json::from_str(s).unwrap())
            .collect();
        let category = events.iter().find_map(|e| e["data"].get("error_category"));
        let expected = match case.as_str() {
            "WF-07-93" => Some(json!({"httpConnectionFailed":{"httpStatusCode":503}})),
            "WF-07-94" => Some(json!({"activeTurnNotSteerable":{"turnKind":"review"}})),
            "WF-07-95" => Some(json!({"responseStreamDisconnected":{"httpStatusCode":null}})),
            "WF-07-96" => Some(json!({"responseTooManyFailedAttempts":{}})),
            "WF-07-97" => Some(json!({"responseStreamConnectionFailed":{"httpStatusCode":429}})),
            _ => None,
        };
        assert_eq!(category, expected.as_ref(), "{case}");
        let terminal = &events.last().unwrap()["data"];
        assert_eq!(terminal["tree_stopped"], true);
        assert_eq!(terminal["fixture_unchanged"], true);
        assert_eq!(
            terminal["reason"],
            if expected.is_some() {
                "provider_failed"
            } else if case == "WF-04-93" {
                "rpc_error"
            } else {
                "protocol_error"
            }
        );
        if case == "WF-04-93" {
            assert!(events.iter().any(|e| e["data"]["error_code"] == -32603));
        }
    }
}
