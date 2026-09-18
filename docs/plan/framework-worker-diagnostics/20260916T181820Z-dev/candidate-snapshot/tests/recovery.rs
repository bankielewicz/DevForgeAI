mod support;
use devforgeai_codex_worker_probe::{
    journal::{Journal, inspect},
    request,
};
use serde_json::json;
use std::fs;

#[test]
fn wf_09() {
    let f = support::Fixture::new("WF-09");
    let mut journal = Journal::create(&f.request).unwrap();
    journal.append("admitted", json!({})).unwrap();
    let path = f.request.run_dir.join("journal.jsonl");
    let before = fs::read(&path).unwrap();
    assert!(request::validate(&f.input).is_err());
    let mut value: serde_json::Value =
        serde_json::from_slice(&fs::read(&f.input).unwrap()).unwrap();
    value["work_id"] = json!("changed");
    fs::write(&f.input, value.to_string()).unwrap();
    assert!(request::validate(&f.input).is_err());
    assert!(Journal::create(&f.request).is_err());
    assert_eq!(before, fs::read(path).unwrap());
}

#[test]
fn wf_10() {
    for last in ["spawn_intent", "turn_intent"] {
        let f = support::Fixture::new("WF-10");
        let status = std::process::Command::new(env!("CARGO_BIN_EXE_crash-driver"))
            .arg(&f.input)
            .arg(last)
            .status()
            .unwrap();
        assert_eq!(status.code(), Some(91));
        let before = fs::read(f.request.run_dir.join("journal.jsonl")).unwrap();
        assert_eq!(
            inspect(&f.request.run_dir, 0, 100).unwrap()["state"],
            "interrupted_unknown"
        );
        assert_eq!(
            before,
            fs::read(f.request.run_dir.join("journal.jsonl")).unwrap()
        );
    }
}

#[test]
fn wf_11() {
    let completed = support::Fixture::new("WF-11");
    let mut child = std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .args(["run", "--request"])
        .arg(&completed.input)
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::null())
        .spawn()
        .unwrap();
    let kept_stdin = child.stdin.take();
    assert_eq!(child.wait().unwrap().code(), Some(0));
    drop(kept_stdin);
    let observed = inspect(&completed.request.run_dir, 0, 100).unwrap();
    assert_eq!(observed["state"], "completed");
    assert_eq!(
        observed,
        inspect(&completed.request.run_dir, 0, 100).unwrap()
    );
    assert_eq!(
        completed
            .trace()
            .iter()
            .filter(|v| v["method"] == "turn/start")
            .count(),
        1
    );
    let f = support::Fixture::new("WF-11");
    let mut journal = Journal::create(&f.request).unwrap();
    journal.append("admitted", json!({})).unwrap();
    journal.append("terminal",json!({"outcome":"blocked","reason":"profile_unqualified","thread_id":null,"turn_id":null,
        "worker_exit_code":null,"tree_stopped":true,"fixture_unchanged":true,"oracle":"not_evaluated","usage":null,"open_work":["w"]})).unwrap();
    drop(journal);
    let first = inspect(&f.request.run_dir, 0, 1).unwrap();
    assert_eq!(first, inspect(&f.request.run_dir, 0, 1).unwrap());
    assert_eq!(first["state"], "blocked");
    let second = inspect(&f.request.run_dir, 1, 1).unwrap();
    assert_eq!(second["events"][0]["seq"], 2);
    assert_eq!(
        inspect(&f.request.run_dir, 2, 100).unwrap()["events"],
        json!([])
    );
    assert!(inspect(&f.request.run_dir, 3, 1).is_err());
    assert!(inspect(&f.request.run_dir, 0, 0).is_err());
}

#[test]
fn wf_12() {
    for variant in 0..4 {
        let f = support::Fixture::new("WF-12");
        let mut journal = Journal::create(&f.request).unwrap();
        journal.append("admitted", json!({})).unwrap();
        drop(journal);
        let path = f.request.run_dir.join("journal.jsonl");
        let mut bytes = fs::read(&path).unwrap();
        match variant {
            0 => bytes.extend_from_slice(b"{\"partial"),
            1 => bytes.extend_from_slice(b"broken\n"),
            2 => {
                let mut v: serde_json::Value = serde_json::from_slice(&bytes).unwrap();
                v["seq"] = json!(3);
                bytes = (v.to_string() + "\n").into_bytes();
            }
            _ => {
                fs::remove_file(f.request.run_dir.join("request.json")).unwrap();
            }
        }
        fs::write(&path, &bytes).unwrap();
        let result = inspect(&f.request.run_dir, 0, 100);
        if variant == 0 {
            assert_eq!(result.unwrap()["truncated_tail"], b"{\"partial".len());
        } else {
            assert_eq!(
                result.unwrap_err(),
                if variant == 3 {
                    "evidence_incomplete"
                } else {
                    "evidence_corrupt"
                }
            );
        }
        assert_eq!(bytes, fs::read(path).unwrap());
    }
}
