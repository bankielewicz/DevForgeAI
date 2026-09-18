use devforgeai_index::protocol::{ErrorCode, Request, Response, read_frame, write_frame};
use std::io::Cursor;

const ID: &str = "550e8400-e29b-41d4-a716-446655440000";

fn request(operation: &str, params: &str) -> String {
    format!(
        r#"{{"protocol_version":1,"request_id":"{ID}","operation":"{operation}","timeout_ms":10000,"params":{params}}}"#
    )
}

#[test]
fn known_operations_accept_only_their_own_parameters() {
    for op in [
        "daemon.handshake",
        "daemon.status",
        "daemon.pause",
        "daemon.resume",
        "daemon.stop",
        "daemon.diagnostics",
        "project.list",
    ] {
        assert!(
            Request::decode(request(op, "{}").as_bytes()).is_ok(),
            "{op}"
        );
        assert_eq!(
            Request::decode(request(op, r#"{"shell":"echo bad"}"#).as_bytes())
                .unwrap_err()
                .code,
            ErrorCode::InvalidArgument
        );
    }
    for op in [
        "project.remove",
        "index.status",
        "index.rescan",
        "index.reindex",
        "index.reconcile",
    ] {
        assert!(
            Request::decode(request(op, &format!(r#"{{"project_id":"{ID}"}}"#)).as_bytes()).is_ok()
        );
        assert!(Request::decode(request(op, "{}").as_bytes()).is_err());
    }
    for op in ["job.status", "job.cancel"] {
        assert!(
            Request::decode(request(op, &format!(r#"{{"job_id":"{ID}"}}"#)).as_bytes()).is_ok()
        );
    }
    assert!(
        Request::decode(
            request("project.add", r#"{"root":"C:\\fixture","name":"Fixture"}"#).as_bytes()
        )
        .is_ok()
    );
    assert!(
        Request::decode(
            request(
                "project.update",
                &format!(r#"{{"project_id":"{ID}","config":{{"max_file_bytes":1024}}}}"#)
            )
            .as_bytes()
        )
        .is_ok()
    );
    assert!(
        Request::decode(
            request(
                "index.rebuild",
                &format!(r#"{{"project_id":"{ID}","affected_projects":["{ID}"]}}"#)
            )
            .as_bytes()
        )
        .is_ok()
    );
}

#[test]
fn version_negotiation_precedes_operation_validation() {
    let raw = request("arbitrary.shell", "{}")
        .replace("\"protocol_version\":1", "\"protocol_version\":2");
    assert_eq!(
        Request::decode(raw.as_bytes()).unwrap_err().code,
        ErrorCode::ProtocolIncompatible
    );
}

#[test]
fn rejects_invalid_unknown_missing_and_out_of_bounds_inputs() {
    for raw in [
        "null".into(),
        "[]".into(),
        "{}".into(),
        request("shell", "{}"),
        request("daemon.status", "null"),
        request("daemon.status", "{}").replace(ID, "bad"),
        request("daemon.status", "{}").replace("10000", "99"),
        request("daemon.status", "{}").replace("10000", "120001"),
        request(
            "project.update",
            &format!(r#"{{"project_id":"{ID}","config":{{"max_file_bytes":1023}}}}"#),
        ),
        request(
            "project.update",
            &format!(r#"{{"project_id":"{ID}","config":{{"unknown":true}}}}"#),
        ),
        request("daemon.status", "{}").replace("\"params\":", "\"extra\":true,\"params\":"),
    ] {
        assert_eq!(
            Request::decode(raw.as_bytes()).unwrap_err().code,
            ErrorCode::InvalidArgument,
            "{raw}"
        );
    }
    assert!(Request::decode(&vec![b' '; 1024 * 1024 + 1]).is_err());
    assert!(Request::decode(&[0xff]).is_err());
    for budget in [100, 120000] {
        assert!(
            Request::decode(
                request("daemon.status", "{}")
                    .replace("10000", &budget.to_string())
                    .as_bytes()
            )
            .is_ok()
        );
    }
}

#[test]
fn frame_has_network_byte_order_and_bounds_before_payload_allocation() {
    let mut bytes = Vec::new();
    write_frame(&mut bytes, b"abc", 3).unwrap();
    assert_eq!(bytes, [0, 0, 0, 3, b'a', b'b', b'c']);
    assert_eq!(read_frame(&mut Cursor::new(bytes), 3).unwrap(), b"abc");
    for bytes in [
        vec![0, 0, 0, 0],
        vec![0, 0, 0, 4],
        vec![0, 0, 0],
        vec![0, 0, 0, 3, b'a'],
    ] {
        assert!(read_frame(&mut Cursor::new(bytes), 3).is_err());
    }
    assert!(write_frame(&mut Vec::new(), b"four", 3).is_err());
    assert!(write_frame(&mut Vec::new(), b"", 3).is_err());
}

#[test]
fn response_envelope_and_exit_categories_remain_distinct() {
    let response = Response::failure(ID, ErrorCode::JobFailed, "job ended unsuccessfully");
    let value = serde_json::to_value(&response).unwrap();
    assert_eq!(value["request_id"], ID);
    assert_eq!(value["protocol_version"], 1);
    assert_eq!(value["ok"], false);
    assert!(value["data"].is_null());
    assert!(value["environment_id"].is_null());
    assert!(value["service_version"].is_null());
    assert_eq!(value["error"]["code"], "JOB_FAILED");
    assert_eq!(response.exit_code(), 11);
    let status = Response::success(ID, serde_json::json!({"outcome":"failed"}));
    assert_eq!(status.exit_code(), 0);
    assert!(serde_json::to_value(&status).unwrap()["error"].is_null());
    for (code, exit) in [
        (ErrorCode::InvalidArgument, 2),
        (ErrorCode::ServiceUnavailable, 3),
        (ErrorCode::ProtocolIncompatible, 4),
        (ErrorCode::IndexPaused, 5),
        (ErrorCode::ProjectNotFound, 6),
        (ErrorCode::Timeout, 7),
        (ErrorCode::StorageCorrupt, 8),
        (ErrorCode::RequestIdConflict, 9),
        (ErrorCode::AccessDenied, 10),
    ] {
        assert_eq!(Response::failure(ID, code, "test").exit_code(), exit);
    }
}
