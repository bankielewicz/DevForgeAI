#![cfg(windows)]
use devforgeai_index::{
    cli::{WslEnvironment, bridge},
    protocol::{ErrorCode, Request},
};
use serde_json::json;
fn request(operation: &str) -> Request {
    Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: operation.into(),
        timeout_ms: 10000,
        params: json!({}),
    }
}
#[tokio::test]
#[ignore = "Requires the explicitly built, isolated Ubuntu WSL fixture"]
async fn native_wsl_bridge_preserves_pause_and_environment_identity() {
    let environment = WslEnvironment {
        distribution: "Ubuntu".into(),
        user: "bryan".into(),
        cli: std::env::var("DEVFORGEAI_WSL_FIXTURE")
            .expect("Explicit native fixture path is required"),
    };
    let start = bridge(&environment, &request("daemon.handshake"), true)
        .await
        .unwrap();
    assert!(start.ok, "{start:?}");
    let identity = start.environment_id.unwrap();
    let testing_environment = environment.clone();
    let test = async move {
        let environment = testing_environment;
        let paused = bridge(&environment, &request("daemon.pause"), false)
            .await
            .unwrap();
        assert!(paused.ok);
        let again = bridge(&environment, &request("daemon.handshake"), true)
            .await
            .unwrap();
        assert_eq!(again.data["already_running"], true);
        assert_eq!(again.data["indexing_mode"], "paused");
        assert_eq!(again.environment_id.as_deref(), Some(identity.as_str()));
        let diagnostic = bridge(&environment, &request("daemon.diagnostics"), false)
            .await
            .unwrap();
        assert!(diagnostic.ok);
        let missing = WslEnvironment {
            cli: "/definitely-absent-devforgeai-fixture".into(),
            ..environment.clone()
        };
        assert_eq!(
            bridge(&missing, &request("daemon.status"), false)
                .await
                .unwrap_err()
                .code,
            ErrorCode::WslCliMissing
        );
    };
    // Stop our isolated daemon even when an assertion panics inside the test future.
    let result = tokio::spawn(test).await;
    let stopped = bridge(&environment, &request("daemon.stop"), false)
        .await
        .unwrap();
    assert!(stopped.ok);
    result.unwrap();
}
#[tokio::test]
#[ignore = "Read-only stopped-distribution probe; requires WSL inventory"]
async fn stopped_distribution_is_never_invoked_by_a_status_poll() {
    let environment = WslEnvironment {
        distribution: "DevForgeAI-absent-fixture-20260914".into(),
        user: "nobody".into(),
        cli: "/must/not/execute".into(),
    };
    assert_eq!(
        bridge(&environment, &request("daemon.status"), false)
            .await
            .unwrap_err()
            .code,
        ErrorCode::EnvironmentStopped
    );
}
