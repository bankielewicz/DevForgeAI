use std::process::Command;
#[test]
fn invalid_cli_is_json_and_nonzero() {
    for args in [
        vec![],
        vec!["run"],
        vec![
            "inspect",
            "--run-dir",
            "relative",
            "--after",
            "0",
            "--limit",
            "1",
        ],
    ] {
        let out = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
            .args(args)
            .output()
            .unwrap();
        assert_eq!(out.status.code(), Some(2));
        assert!(serde_json::from_slice::<serde_json::Value>(&out.stderr).is_ok());
    }
}
