mod support;
use devforgeai_codex_worker_probe::runner::{self, Options};
use serde_json::Value;
use std::{
    fs,
    io::Write,
    os::windows::io::{AsRawHandle, FromRawHandle, OwnedHandle},
    process::{Command, Stdio},
    sync::{
        Arc,
        atomic::{AtomicU8, Ordering},
    },
    time::{Duration, Instant},
};
use windows_sys::Win32::{
    Foundation::WAIT_OBJECT_0,
    System::Threading::{
        OpenProcess, PROCESS_QUERY_LIMITED_INFORMATION, PROCESS_SYNCHRONIZE, WaitForSingleObject,
    },
};
fn held(f: &support::Fixture) -> Vec<OwnedHandle> {
    let deadline = Instant::now() + Duration::from_secs(5);
    loop {
        if let Ok(bytes) = fs::read(f.root.path().join("peer-pids.json"))
            && let Ok(v) = serde_json::from_slice::<Value>(&bytes)
        {
            return ["peer", "descendant"]
                .iter()
                .map(|key| unsafe {
                    let handle = OpenProcess(
                        PROCESS_SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION,
                        0,
                        v[key].as_u64().unwrap() as u32,
                    );
                    assert!(!handle.is_null());
                    OwnedHandle::from_raw_handle(handle)
                })
                .collect();
        }
        assert!(Instant::now() < deadline, "peer readiness missing");
        std::thread::sleep(Duration::from_millis(5));
    }
}
fn stopped(handles: &[OwnedHandle]) {
    for h in handles {
        assert_eq!(
            unsafe { WaitForSingleObject(h.as_raw_handle(), 5000) },
            WAIT_OBJECT_0
        );
    }
}
#[test]
fn wf_13() {
    let f = support::Fixture::new("WF-13-1");
    let mut driver = Command::new(env!("CARGO_BIN_EXE_console-driver"))
        .arg(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .arg(&f.input)
        .spawn()
        .unwrap();
    let handles = held(&f);
    let start = Instant::now();
    fs::write(f.root.path().join("signal-ready"), b"ready").unwrap();
    assert_eq!(driver.wait().unwrap().code(), Some(5));
    stopped(&handles);
    assert!(start.elapsed() < Duration::from_secs(11));
    let f = support::Fixture::new("WF-13-2");
    let mut child = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .args(["run", "--request"])
        .arg(&f.input)
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let handles = held(&f);
    let start = Instant::now();
    child
        .stdin
        .take()
        .unwrap()
        .write_all(b"{\"op\":\"cancel\"}\n")
        .unwrap();
    let out = child.wait_with_output().unwrap();
    assert_eq!(
        out.status.code(),
        Some(5),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    stopped(&handles);
    assert!(start.elapsed() < Duration::from_secs(11));
}
#[test]
fn wf_14() {
    let f = support::Fixture::new("WF-14");
    let mut child = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .args(["run", "--request"])
        .arg(&f.input)
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .spawn()
        .unwrap();
    let handles = held(&f);
    child.kill().unwrap();
    child.wait().unwrap();
    stopped(&handles);
}
#[test]
fn wf_15() {
    for stage in ["turn_bound", "thread_bound", "server_started"] {
        let f = support::Fixture::new("WF-15");
        let control = Arc::new(AtomicU8::new(0));
        let options = Options {
            control: control.clone(),
            grace: Duration::from_millis(100),
            ..Default::default()
        };
        let (exit, v) = runner::run(&f.input, options, &mut |e| {
            if e["kind"] == stage {
                control.store(1, Ordering::SeqCst);
            }
        })
        .unwrap();
        assert_eq!(exit, 5, "{v}");
        assert_eq!(v["tree_stopped"], true);
        if stage == "thread_bound" {
            assert!(!f.trace().iter().any(|v| v["method"] == "turn/start"));
        }
    }
}
#[test]
fn wf_16() {
    for sub in 1..=4 {
        let f = support::Fixture::new(&format!("WF-16-{sub}"));
        let options = if sub == 1 {
            Options {
                total: Duration::from_secs(5),
                rpc: Duration::from_millis(300),
                ..Default::default()
            }
        } else {
            Options::default()
        };
        let start = Instant::now();
        let (exit, v) = runner::run(&f.input, options, &mut |_| {}).unwrap();
        assert_eq!(exit, if sub == 1 || sub == 4 { 6 } else { 4 }, "{v}");
        assert_eq!(
            v["reason"],
            if sub == 1 || sub == 4 {
                "deadline"
            } else {
                "output_limit"
            }
        );
        assert_eq!(v["tree_stopped"], true);
        if sub == 4 {
            assert!(start.elapsed() >= Duration::from_secs(120));
            assert!(start.elapsed() < Duration::from_secs(131));
        }
    }
}
