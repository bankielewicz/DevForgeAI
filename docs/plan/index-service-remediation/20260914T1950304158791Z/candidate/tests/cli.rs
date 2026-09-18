use devforgeai_index::cli::parse_request;
use serde_json::json;

#[test]
fn cli_maps_management_flags_to_the_shared_protocol() {
    let request = parse_request(&[
        "devforgeai",
        "index",
        "rescan",
        "--project",
        "550e8400-e29b-41d4-a716-446655440000",
        "--json",
    ])
    .unwrap()
    .unwrap();
    assert_eq!(request.operation, "index.rescan");
    assert_eq!(
        request.params,
        json!({"project_id":"550e8400-e29b-41d4-a716-446655440000"})
    );
    assert_eq!(request.timeout_ms, 10000);
    assert!(parse_request(&["devforgeai", "index", "rescan"]).is_err());
    assert!(
        parse_request(&[
            "devforgeai",
            "project",
            "remove",
            "--project",
            "550e8400-e29b-41d4-a716-446655440000"
        ])
        .is_err()
    );
    assert!(parse_request(&["devforgeai", "daemon", "status", "--timeout-ms", "99"]).is_err());
    assert!(parse_request(&["devforgeai", "daemon", "status", "--unknown"]).is_err());
}

#[test]
fn binary_emits_one_json_envelope_for_invalid_input() {
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .args(["index", "rescan", "--json"])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(2));
    let envelope: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(envelope["ok"], false);
    assert_eq!(envelope["error"]["code"], "INVALID_ARGUMENT");
}

#[test]
fn help_and_human_output_have_correct_streams_and_exit_codes() {
    for arguments in [vec!["--help", "--json"], vec!["--version", "--json"]] {
        let output = std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .args(arguments)
            .output()
            .unwrap();
        assert!(output.status.success());
        let value: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(value["ok"], true);
        assert!(
            value["data"]["help"]
                .as_str()
                .unwrap()
                .contains("devforgeai")
        );
    }
    let data = tempfile::tempdir().unwrap();
    for (arguments, expected) in [
        (vec!["daemon", "status"], 0),
        (vec!["project", "list"], 3),
        (vec!["--help"], 0),
    ] {
        let output = std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(&arguments)
            .output()
            .unwrap();
        assert_eq!(output.status.code(), Some(expected));
        if expected == 3 {
            assert!(output.stdout.is_empty());
            assert!(String::from_utf8_lossy(&output.stderr).contains("ServiceUnavailable"));
        } else {
            assert!(!output.stdout.is_empty());
        }
    }
}

#[cfg(windows)]
#[test]
fn windows_default_path_and_binary_startup_failures_are_isolated() {
    let directory = tempfile::tempdir().unwrap();
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .env_remove("DEVFORGEAI_INDEX_DATA")
        .env("LOCALAPPDATA", directory.path())
        .args(["daemon", "status", "--json"])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(0));
    assert!(directory.path().join("DevForgeAI/Index/runtime").is_dir());
    for binary in [
        env!("CARGO_BIN_EXE_devforgeai-indexd"),
        env!("CARGO_BIN_EXE_devforgeai-tray"),
    ] {
        let output = std::process::Command::new(binary)
            .env("DEVFORGEAI_INDEX_DATA", "relative")
            .output()
            .unwrap();
        assert_eq!(output.status.code(), Some(2));
    }
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .env_remove("DEVFORGEAI_INDEX_DATA")
        .env_remove("LOCALAPPDATA")
        .args(["daemon", "status", "--json"])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(8));
    assert_eq!(
        serde_json::from_slice::<serde_json::Value>(&output.stdout).unwrap()["error"]["code"],
        "INTERNAL_ERROR"
    );
}
