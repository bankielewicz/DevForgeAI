use devforgeai_index::{client, host, platform::Paths, protocol::Request};
use serde_json::json;
use std::time::Duration;
use tempfile::tempdir;

#[tokio::test]
async fn native_local_transport_roundtrips_and_stops_without_tcp() {
    let directory = tempdir().unwrap();
    let paths = Paths::at(directory.path().join("private")).unwrap();
    let server_paths = paths.clone();
    let server = tokio::spawn(async move { host::serve(server_paths).await });
    let request = |operation: &str| Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: operation.into(),
        timeout_ms: 1000,
        params: json!({}),
    };
    let mut ready = false;
    for _ in 0..100 {
        if client::local(&paths, &request("daemon.handshake"))
            .await
            .is_ok_and(|response| response.ok)
        {
            ready = true;
            break;
        }
        tokio::time::sleep(Duration::from_millis(20)).await;
    }
    assert!(ready, "native host did not become ready");
    let status = client::local(&paths, &request("daemon.status"))
        .await
        .unwrap();
    assert!(status.ok);
    assert!(status.environment_id.is_some());
    assert_eq!(status.data["daemon_state"], "running");
    assert!(
        client::local(&paths, &request("daemon.pause"))
            .await
            .unwrap()
            .ok
    );
    assert_eq!(
        client::local(&paths, &request("daemon.status"))
            .await
            .unwrap()
            .data["indexing_mode"],
        "paused"
    );
    assert!(
        client::local(&paths, &request("daemon.stop"))
            .await
            .unwrap()
            .ok
    );
    tokio::time::timeout(Duration::from_secs(5), server)
        .await
        .unwrap()
        .unwrap()
        .unwrap();
    assert!(
        client::local(&paths, &request("daemon.status"))
            .await
            .is_err()
    );
}
