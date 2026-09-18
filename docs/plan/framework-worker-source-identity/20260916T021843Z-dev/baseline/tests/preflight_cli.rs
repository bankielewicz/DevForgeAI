use std::process::Command;
mod support;

#[test]
fn preflight_is_a_closed_terminal_operation() {
    let executable = env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe");
    let output = Command::new(executable)
        .args([
            "preflight",
            "--request",
            "C:\\definitely-absent-native-preflight-input.json",
        ])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(2));
    assert_eq!(
        serde_json::from_slice::<serde_json::Value>(&output.stderr).unwrap()["error"],
        "input_missing"
    );
    assert!(output.stdout.is_empty());
    let output = Command::new(executable)
        .args([
            "preflight",
            "--request",
            "relative.json",
            "--config",
            "hooks=false",
        ])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(2));
    assert_eq!(
        serde_json::from_slice::<serde_json::Value>(&output.stderr).unwrap()["error"],
        "invalid_arguments"
    );
}

#[test]
fn inspection_mode_rejects_peers_and_source_inventory_is_observable_without_launch() {
    use devforgeai_codex_worker_probe::request;
    use std::{fs, path::PathBuf};
    let executable = env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe");
    let peer = support::Fixture::new("WF-01");
    let output = Command::new(executable)
        .args(["preflight", "--request"])
        .arg(&peer.input)
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(2));
    assert_eq!(
        serde_json::from_slice::<serde_json::Value>(&output.stderr).unwrap()["error"],
        "invalid_request"
    );
    assert!(!peer.request.run_dir.exists());
    let workspace = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .unwrap()
        .to_path_buf();
    let parent = workspace.join("docs/plan/framework-worker-trials");
    fs::create_dir_all(&parent).unwrap();
    let owned = tempfile::Builder::new()
        .prefix("NI-sources-")
        .tempdir_in(parent)
        .unwrap();
    let fixture = owned.path().join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    let user = peer.root.path().join("synthetic-user");
    let system = peer.root.path().join("synthetic-system");
    fs::create_dir(&user).unwrap();
    fs::create_dir(&system).unwrap();
    let output = Command::new(executable)
        .args(["profile-sources", "--checkout-root"])
        .arg(&fixture)
        .env("USERPROFILE", &user)
        .env("PROGRAMDATA", &system)
        .output()
        .unwrap();
    assert_eq!(
        output.status.code(),
        Some(0),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let inventory: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(inventory["schema_version"], 1);
    assert!(
        inventory["entries"]
            .as_array()
            .unwrap()
            .iter()
            .any(|entry| entry["state"] == "absent")
    );
    fs::write(owned.path().join("source-inventory.json"), &output.stdout).unwrap();
    for argument in [&user, &fixture] {
        if argument == &fixture {
            fs::write(fixture.join("extra.txt"), b"extra").unwrap();
        }
        let denied = Command::new(executable)
            .args(["profile-sources", "--checkout-root"])
            .arg(argument)
            .output()
            .unwrap();
        assert_eq!(denied.status.code(), Some(2));
    }
    if std::env::var_os("WF_TEST_EVIDENCE").is_some() {
        let _ = owned.keep();
    }
}
