#![cfg(windows)]
//! Native pipe peers exercising the client's framing, envelope and deadline boundary.
use devforgeai_index::{
    client,
    platform::Paths,
    protocol::{ErrorCode, RESPONSE_LIMIT, Request, Response},
};
use serde_json::json;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::test]
async fn native_client_rejects_invalid_peers_and_enforces_deadline() {
    for case in [
        "zero",
        "oversized",
        "truncated",
        "json",
        "version",
        "identity",
        "error-data",
        "ok-error",
        "timeout",
        "valid",
    ] {
        let request = Request {
            protocol_version: 1,
            request_id: uuid::Uuid::new_v4().to_string(),
            operation: "daemon.status".into(),
            params: json!({}),
            timeout_ms: 150,
        };
        let endpoint = format!(r"\\.\pipe\DevForgeAI-client-test-{}", uuid::Uuid::new_v4());
        let mut server = tokio::net::windows::named_pipe::ServerOptions::new()
            .first_pipe_instance(true)
            .create(&endpoint)
            .unwrap();
        let paths = Paths {
            data: Default::default(),
            runtime: Default::default(),
            endpoint,
        };
        let sent = request.clone();
        let peer = tokio::spawn(async move {
            server.connect().await.unwrap();
            let len = server.read_u32().await.unwrap();
            let mut bytes = vec![0; len as usize];
            server.read_exact(&mut bytes).await.unwrap();
            let observed = Request::decode(&bytes).unwrap();
            assert_eq!(observed.request_id, sent.request_id);
            if case == "timeout" {
                tokio::time::sleep(std::time::Duration::from_millis(250)).await;
                return;
            }
            if case == "zero" {
                server.write_u32(0).await.unwrap();
                return;
            }
            if case == "oversized" {
                server.write_u32((RESPONSE_LIMIT + 1) as u32).await.unwrap();
                return;
            }
            if case == "truncated" {
                server.write_u32(20).await.unwrap();
                server.write_all(b"few").await.unwrap();
                return;
            }
            let mut response = serde_json::to_value(Response::success(
                &sent.request_id,
                json!({"daemon_state":"running"}),
            ))
            .unwrap();
            match case {
                "version" => response["protocol_version"] = json!(2),
                "identity" => response["request_id"] = json!("wrong-id"),
                "error-data" => {
                    response = serde_json::to_value(Response::failure(
                        &sent.request_id,
                        ErrorCode::InternalError,
                        "broken",
                    ))
                    .unwrap();
                    response["data"] = json!({});
                }
                "ok-error" => {
                    response = serde_json::to_value(Response::failure(
                        &sent.request_id,
                        ErrorCode::InternalError,
                        "broken",
                    ))
                    .unwrap();
                    response["ok"] = json!(true);
                }
                _ => {}
            }
            let bytes = if case == "json" {
                b"not-json".to_vec()
            } else {
                serde_json::to_vec(&response).unwrap()
            };
            server.write_u32(bytes.len() as u32).await.unwrap();
            server.write_all(&bytes).await.unwrap();
            server.flush().await.unwrap();
            // Keep the native server endpoint alive until the client consumes its response.
            tokio::time::sleep(std::time::Duration::from_millis(40)).await;
        });
        let result = client::local(&paths, &request).await;
        if case == "valid" {
            assert_eq!(result.unwrap().data["daemon_state"], "running");
        } else {
            let expected = match case {
                "zero" | "oversized" => ErrorCode::InvalidArgument,
                "truncated" => ErrorCode::ServiceUnavailable,
                "timeout" => ErrorCode::Timeout,
                _ => ErrorCode::ProtocolIncompatible,
            };
            assert_eq!(result.unwrap_err().code, expected, "{case}");
        }
        peer.await.unwrap();
    }
}

#[tokio::test]
async fn cli_rejects_missing_job_fields_and_preserves_remote_errors() {
    for case in [
        "job-id",
        "outcome",
        "interrupted",
        "job-error",
        "preview",
        "preview-error",
        "stop-error",
        "start-error",
    ] {
        let data = tempfile::tempdir().unwrap();
        let paths = Paths::at(data.path().to_owned()).unwrap();
        let endpoint = paths.endpoint.clone();
        let mut server = tokio::net::windows::named_pipe::ServerOptions::new()
            .first_pipe_instance(true)
            .create(&endpoint)
            .unwrap();
        let count = if ["outcome", "interrupted", "job-error", "stop-error"].contains(&case) {
            2
        } else {
            1
        };
        let peer = tokio::spawn(async move {
            for number in 0..count {
                server.connect().await.unwrap();
                let next = tokio::net::windows::named_pipe::ServerOptions::new()
                    .create(&endpoint)
                    .unwrap();
                let mut stream = std::mem::replace(&mut server, next);
                let length = stream.read_u32().await.unwrap();
                let mut bytes = vec![0; length as usize];
                stream.read_exact(&mut bytes).await.unwrap();
                let request = Request::decode(&bytes).unwrap();
                let mut response = Response::success(&request.request_id, json!({}));
                if number == 0 {
                    match case {
                        "preview" => {
                            assert_eq!(request.operation, "project.list");
                            response.data = json!({"projects":false});
                        }
                        "preview-error" | "start-error" => {
                            response = Response::failure(
                                &request.request_id,
                                ErrorCode::StorageCorrupt,
                                "fixture unavailable",
                            );
                        }
                        "stop-error" => {
                            assert_eq!(request.operation, "daemon.stop");
                            response.data = json!({"daemon_state":"stopping"});
                        }
                        "job-id" => {
                            assert_eq!(request.operation, "index.rescan");
                        }
                        _ => {
                            assert_eq!(request.operation, "index.rescan");
                            response.data =
                                json!({"job_id":"550e8400-e29b-41d4-a716-446655440000"});
                        }
                    }
                } else {
                    match case {
                        "interrupted" => response.data = json!({"outcome":"interrupted"}),
                        "job-error" => {
                            response = Response::failure(
                                &request.request_id,
                                ErrorCode::JobNotFound,
                                "expired",
                            )
                        }
                        "stop-error" => response.protocol_version = 2,
                        _ => {}
                    }
                }
                let bytes = serde_json::to_vec(&response).unwrap();
                stream.write_u32(bytes.len() as u32).await.unwrap();
                stream.write_all(&bytes).await.unwrap();
                stream.flush().await.unwrap();
                tokio::time::sleep(std::time::Duration::from_millis(40)).await;
            }
        });
        let mut args = match case {
            "preview" | "preview-error" => vec![
                "index",
                "rebuild",
                "--project",
                "550e8400-e29b-41d4-a716-446655440000",
                "--yes",
                "--affected-projects",
                "550e8400-e29b-41d4-a716-446655440000",
            ],
            "stop-error" => vec!["daemon", "stop"],
            "start-error" => vec!["daemon", "start"],
            _ => vec![
                "index",
                "rescan",
                "--project",
                "550e8400-e29b-41d4-a716-446655440000",
                "--wait",
            ],
        };
        args.extend(["--json", "--timeout-ms", "2000"]);
        let output = tokio::process::Command::new(env!("CARGO_BIN_EXE_devforgeai"))
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(args)
            .output()
            .await
            .unwrap();
        let code = match case {
            "preview-error" | "start-error" => 8,
            "stop-error" => 4,
            "interrupted" => 11,
            "job-error" => 6,
            _ => 2,
        };
        assert_eq!(
            output.status.code(),
            Some(code),
            "{case}: {}",
            String::from_utf8_lossy(&output.stdout)
        );
        let response: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(response["ok"], false);
        tokio::time::timeout(std::time::Duration::from_secs(3), peer)
            .await
            .unwrap()
            .unwrap();
    }
}
