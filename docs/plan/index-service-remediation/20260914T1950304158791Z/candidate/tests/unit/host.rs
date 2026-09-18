use super::*;

#[tokio::test]
async fn invalid_protocol_is_rejected_with_identity_before_dispatch() {
    let data = tempfile::tempdir().unwrap();
    let service = Arc::new(Service::open(data.path()).unwrap());
    let request = serde_json::json!({"protocol_version":99,"request_id":"550e8400-e29b-41d4-a716-446655440000","operation":"daemon.pause","timeout_ms":1000,"params":{}});
    for bytes in [serde_json::to_vec(&request).unwrap(), b"malformed".to_vec()] {
        let (mut server, mut reader) = tokio::io::duplex(4096);
        respond(&mut server, bytes, service.clone()).await.unwrap();
        let bytes = client::read_frame(&mut reader, RESPONSE_LIMIT)
            .await
            .unwrap();
        let response: Response = serde_json::from_slice(&bytes).unwrap();
        assert!(!response.ok);
        assert_eq!(
            response.environment_id.as_deref(),
            Some(service.environment_id())
        );
    }
    let status = Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: "daemon.status".into(),
        timeout_ms: 1000,
        params: serde_json::json!({}),
    };
    assert_eq!(service.execute(&status).data["indexing_mode"], "active");
    let (mut closed, reader) = tokio::io::duplex(4);
    drop(reader);
    assert!(
        respond(
            &mut closed,
            serde_json::to_vec(&status).unwrap(),
            service.clone()
        )
        .await
        .is_err()
    );
    service.shutdown().unwrap();
}

#[tokio::test]
async fn dispatch_failure_and_timeout_produce_one_envelope_without_retry() {
    for timed_out in [false, true] {
        let request = Request {
            protocol_version: 1,
            request_id: uuid::Uuid::new_v4().to_string(),
            operation: "daemon.pause".into(),
            timeout_ms: 100,
            params: serde_json::json!({}),
        };
        let (mut server, mut reader) = tokio::io::duplex(4096);
        let calls = Arc::new(std::sync::atomic::AtomicUsize::new(0));
        let observed = calls.clone();
        let completed = Arc::new(std::sync::atomic::AtomicBool::new(false));
        let completion = completed.clone();
        respond_with_executor(
            &mut server,
            serde_json::to_vec(&request).unwrap(),
            "fixture",
            move |request| {
                observed.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                tokio::spawn(async move {
                    if !timed_out {
                        panic!("controlled dispatch task failure");
                    }
                    tokio::time::sleep(Duration::from_millis(180)).await;
                    completion.store(true, std::sync::atomic::Ordering::SeqCst);
                    Response::success(request.request_id, serde_json::json!({}))
                })
            },
        )
        .await
        .unwrap();
        let bytes = client::read_frame(&mut reader, RESPONSE_LIMIT)
            .await
            .unwrap();
        let response: Response = serde_json::from_slice(&bytes).unwrap();
        assert_eq!(response.request_id, request.request_id);
        assert_eq!(
            response.error.unwrap().code,
            if timed_out {
                ErrorCode::Timeout
            } else {
                ErrorCode::InternalError
            }
        );
        assert_eq!(calls.load(std::sync::atomic::Ordering::SeqCst), 1);
        if timed_out {
            assert!(!completed.load(std::sync::atomic::Ordering::SeqCst));
            tokio::time::sleep(Duration::from_millis(100)).await;
            assert!(
                completed.load(std::sync::atomic::Ordering::SeqCst),
                "timeout must not claim to have cancelled an in-flight mutation"
            );
        }
    }
}

#[cfg(windows)]
#[tokio::test]
async fn unconnected_pipe_cannot_authenticate_a_peer() {
    let paths = Paths {
        data: Default::default(),
        runtime: Default::default(),
        endpoint: format!(r"\\.\pipe\DevForgeAI-auth-fixture-{}", uuid::Uuid::new_v4()),
    };
    let listener = pipe(&paths, true).unwrap();
    assert_eq!(
        authenticate(&listener).unwrap_err().code,
        ErrorCode::AccessDenied
    );
}
