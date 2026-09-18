use devforgeai_codex_worker_probe::request;
use serde_json::json;
use sha2::{Digest, Sha256};
use std::fs;

#[test]
fn valid_fixture_is_admitted_and_invalid_fields_are_rejected() {
    let root = tempfile::tempdir().unwrap();
    let fixture = root.path().join("fixture");
    fs::create_dir(&fixture).unwrap();
    let task = include_bytes!("fixtures/task.json");
    fs::write(fixture.join("task.json"), task).unwrap();
    let exe = std::path::PathBuf::from(env!("CARGO_BIN_EXE_protocol-peer"));
    let mut v = json!({"schema_version":1,"project_id":"p","checkout_id":"c","work_id":"w","run_id":"r",
        "candidate_sha256":format!("{:x}",Sha256::digest(task)),"checkout_root":fixture,"run_dir":root.path().join("run"),
        "worker_executable":exe,"worker_sha256":format!("{:x}",Sha256::digest(fs::read(&exe).unwrap())),
        "adapter":"peer","scenario":"complete","profile":null});
    let path = root.path().join("input.json");
    fs::write(&path, v.to_string()).unwrap();
    assert!(request::validate(&path).is_ok());
    v["extra"] = json!(true);
    fs::write(&path, v.to_string()).unwrap();
    assert!(request::validate(&path).is_err());
    v.as_object_mut().unwrap().remove("extra");
    for (field, bad) in [
        ("project_id", json!("../x")),
        ("schema_version", json!(2)),
        ("candidate_sha256", json!("0".repeat(64))),
        ("worker_sha256", json!("0".repeat(64))),
        ("adapter", json!("shell")),
        ("scenario", json!("retry")),
        ("profile", json!({})),
        ("run_dir", json!(fixture)),
        ("checkout_root", json!("relative")),
    ] {
        let mut bad_v = v.clone();
        bad_v[field] = bad;
        fs::write(&path, bad_v.to_string()).unwrap();
        assert!(request::validate(&path).is_err(), "{field}");
    }
    fs::write(
        &path,
        v.to_string().replacen("{", "{\"schema_version\":1,", 1),
    )
    .unwrap();
    assert!(request::validate(&path).is_err());
}
