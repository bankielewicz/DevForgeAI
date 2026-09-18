mod support;
use devforgeai_codex_worker_probe::{
    request,
    runner::{self, Options},
};
use serde_json::json;
use std::{
    fs,
    sync::{
        Arc,
        atomic::{AtomicU8, Ordering},
    },
    time::Duration,
};

#[test]
fn wf_17() {
    for (key, value) in [
        ("run_id", json!("../escape")),
        ("worker_sha256", json!("0".repeat(64))),
        ("candidate_sha256", json!("A".repeat(64))),
        ("checkout_root", json!("relative/../root")),
    ] {
        let f = support::Fixture::new("WF-17");
        let sentinel = f.root.path().join("sentinel");
        fs::write(&sentinel, b"unchanged").unwrap();
        let mut v = serde_json::to_value(&f.request).unwrap();
        v[key] = value;
        fs::write(&f.input, v.to_string()).unwrap();
        assert!(request::validate(&f.input).is_err());
        assert!(!f.root.path().join("peer-trace.jsonl").exists());
        assert_eq!(fs::read(sentinel).unwrap(), b"unchanged");
    }
    let f = support::Fixture::new("WF-17");
    let mut v = serde_json::to_value(&f.request).unwrap();
    v["run_dir"] = json!(f.request.checkout_root.join("run"));
    fs::write(&f.input, v.to_string()).unwrap();
    assert!(request::validate(&f.input).is_err());
    let junction = f.root.path().join("junction");
    let status = std::process::Command::new("cmd.exe")
        .args(["/d", "/c", "mklink", "/J"])
        .arg(&junction)
        .arg(&f.request.checkout_root)
        .stdout(std::process::Stdio::null())
        .status()
        .unwrap();
    assert!(status.success(), "junction fixture setup failed");
    assert_eq!(request::resolve(&junction).unwrap_err(), "reparse_path");
    fs::remove_dir(junction).unwrap(); // Remove only the test-owned junction, never its target.
}
#[test]
fn wf_18() {
    for i in 1..=3 {
        let f = support::Fixture::new(&format!("WF-18-{i}"));
        let (exit, v) = f.run();
        assert_eq!(exit, 4);
        assert_eq!(v["reason"], "oracle_mismatch");
    }
}
#[test]
fn wf_19() {
    let f = support::Fixture::new("WF-19-1");
    let (exit, v) = f.run();
    assert_eq!(exit, 4);
    assert_eq!(v["fixture_unchanged"], false);
    let f = support::Fixture::new("WF-19-2");
    let options = Options {
        fail_write_after: Some(3),
        ..Default::default()
    };
    let (exit, v) = runner::run(&f.input, options, &mut |_| {}).unwrap();
    assert_eq!(exit, 4);
    assert_eq!(v["reason"], "evidence_write_failed");
    assert_eq!(v["tree_stopped"], true);
}
#[test]
fn wf_20() {
    for (variant, expected) in [(1, 0), (2, 5), (3, 7)] {
        let f = support::Fixture::new(&format!("WF-20-{variant}"));
        let control = Arc::new(AtomicU8::new(0));
        let options = Options {
            control: control.clone(),
            grace: Duration::from_millis(100),
            uncertain_cleanup: variant == 3,
            ..Default::default()
        };
        let (exit, v) = runner::run(&f.input, options, &mut |e| {
            if (variant == 1 && e["kind"] == "worker_event" && e["data"]["status"] == "completed")
                || (variant == 2 && e["kind"] == "turn_bound")
            {
                control.store(1, Ordering::SeqCst);
            }
        })
        .unwrap();
        assert_eq!(exit, expected, "{v}");
        if variant == 3 {
            assert!(v["tree_stopped"].is_null());
        }
    }
}
