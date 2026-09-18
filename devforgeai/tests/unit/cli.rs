//! These are component checks of the actual bridge with a controlled OS process boundary.
use super::*;

#[cfg(windows)]
#[tokio::test]
async fn bridge_process_contract_handles_inventory_race_limits_and_envelopes() {
    let fixture = tempfile::tempdir().unwrap();
    let executable = fixture.path().join("bridge-peer.exe");
    let compiled = std::process::Command::new("rustc")
        .args(["--edition=2024", "tests/support/bridge_peer.rs", "-o"])
        .arg(&executable)
        .output()
        .unwrap();
    assert!(
        compiled.status.success(),
        "{}",
        String::from_utf8_lossy(&compiled.stderr)
    );
    let environment = WslEnvironment {
        distribution: "Fixture Ω & space".into(),
        user: "user space".into(),
        cli: "/path space/$(literal)/devforgeai".into(),
    };
    std::fs::write(
        fixture.path().join("distribution"),
        &environment.distribution,
    )
    .unwrap();
    for mode in [
        "stopped",
        "race",
        "inventory-failed",
        "utf8",
        "valid",
        "invalid-json",
        "identity",
        "version",
        "oversized",
        "timeout",
        "bootstrap",
    ] {
        std::fs::write(fixture.path().join("mode"), mode).unwrap();
        std::fs::write(fixture.path().join("inventory-count"), "0").unwrap();
        std::fs::write(fixture.path().join("arguments"), "").unwrap();
        let request = make(
            "daemon.handshake",
            json!({}),
            if mode == "timeout" { 300 } else { 3000 },
        );
        let mut response = Response::success(&request.request_id, json!({"fixture":true}));
        if mode == "identity" {
            response.request_id = "foreign".into();
        }
        if mode == "version" {
            response.protocol_version = 2;
        }
        let bytes = if mode == "invalid-json" {
            b"not-json".to_vec()
        } else {
            serde_json::to_vec(&response).unwrap()
        };
        std::fs::write(fixture.path().join("response"), bytes).unwrap();
        let bootstrap = mode == "bootstrap";
        let result = bridge_with_executable(&environment, &request, bootstrap, &executable).await;
        match mode {
            "stopped" | "race" => {
                assert_eq!(result.unwrap_err().code, ErrorCode::EnvironmentStopped)
            }
            "inventory-failed" => {
                assert_eq!(result.unwrap_err().code, ErrorCode::ServiceUnavailable)
            }
            "invalid-json" => assert_eq!(result.unwrap_err().code, ErrorCode::WslCliMissing),
            "identity" | "version" => {
                assert_eq!(result.unwrap_err().code, ErrorCode::ProtocolIncompatible)
            }
            "oversized" => assert_eq!(result.unwrap_err().code, ErrorCode::InvalidArgument),
            "timeout" => assert_eq!(result.unwrap_err().code, ErrorCode::Timeout),
            _ => assert_eq!(result.unwrap().data, json!({"fixture":true})),
        }
        let arguments = std::fs::read_to_string(fixture.path().join("arguments")).unwrap();
        if ["stopped", "race", "inventory-failed"].contains(&mode) {
            assert!(
                !arguments.contains("--exec"),
                "polling must not dispatch to a stopped target"
            );
        } else {
            let mut expected = vec![
                "--distribution",
                &environment.distribution,
                "--user",
                &environment.user,
                "--exec",
                &environment.cli,
                "bridge",
                "request",
            ];
            if bootstrap {
                expected.push("--bootstrap");
                assert!(!arguments.contains("--list"));
            }
            assert!(arguments.contains(&format!("{expected:?}")), "{arguments}");
            let observed = std::fs::read(fixture.path().join("request")).unwrap();
            assert_eq!(observed, serde_json::to_vec(&request).unwrap());
        }
    }
    let missing = fixture.path().join("missing.exe");
    assert_eq!(
        bridge_with_executable(
            &environment,
            &make("daemon.handshake", json!({}), 1000),
            true,
            &missing
        )
        .await
        .unwrap_err()
        .code,
        ErrorCode::WslCliMissing
    );
    assert_eq!(
        wsl_running(&environment.distribution, &missing)
            .await
            .unwrap_err()
            .code,
        ErrorCode::ServiceUnavailable
    );
}

#[test]
fn end_to_end_deadline_and_command_mapping_are_bounded() {
    let cli =
        Cli::try_parse_from(["devforgeai", "daemon", "status", "--timeout-ms", "100"]).unwrap();
    assert_eq!(
        remaining(&cli, Instant::now() - Duration::from_millis(1))
            .unwrap_err()
            .code,
        ErrorCode::Timeout
    );
    assert_eq!(cli.request().unwrap().unwrap().timeout_ms, 100);
}
