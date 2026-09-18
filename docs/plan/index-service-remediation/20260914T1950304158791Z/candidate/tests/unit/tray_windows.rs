use super::*;

#[test]
fn busy_tray_does_not_enqueue_duplicate_work_and_closed_ui_releases_worker() {
    let data = tempfile::tempdir().unwrap();
    let paths = Paths::at(data.path().to_owned()).unwrap();
    let (sender, requests) = mpsc::channel();
    let (responses, receiver) = mpsc::channel();
    let mut ui = Ui {
        paths: paths.clone(),
        controls: BTreeMap::new(),
        sender,
        receiver,
        poll: PollState::new(Instant::now()),
        aliases: vec!["local".into()],
        projects: vec![],
        statuses: vec![],
        busy: false,
        selected: "local".into(),
    };
    for _ in 0..2 {
        enqueue(
            &mut ui,
            Work {
                alias: "local".into(),
                operation: "daemon.status".into(),
                params: json!({}),
                start: false,
                exit_after: false,
            },
        );
    }
    assert!(ui.busy);
    assert_eq!(requests.try_recv().unwrap().operation, "daemon.status");
    assert!(requests.try_recv().is_err());
    drop(ui);
    let (send, receive) = mpsc::channel();
    send.send(Work {
        alias: "local".into(),
        operation: "daemon.status".into(),
        params: json!({}),
        start: false,
        exit_after: false,
    })
    .unwrap();
    let (done, finished) = mpsc::channel();
    let thread = std::thread::spawn(move || {
        worker(0, paths, receive, responses);
        done.send(()).unwrap();
    });
    finished.recv_timeout(Duration::from_secs(3)).unwrap();
    thread.join().unwrap();
    assert!(
        send.send(Work {
            alias: "local".into(),
            operation: "daemon.status".into(),
            params: json!({}),
            start: false,
            exit_after: false
        })
        .is_err()
    );
}

#[test]
fn polling_during_absent_or_reentrant_ui_state_returns_without_work() {
    unsafe {
        UI.with(|cell| {
            assert!(cell.borrow().is_none());
            poll(std::ptr::null_mut());
            let _borrow = cell.borrow_mut();
            poll(std::ptr::null_mut());
        });
    }
}

#[tokio::test]
async fn stop_exit_reports_timeout_while_a_peer_remains_running() {
    use std::sync::{
        Arc,
        atomic::{AtomicBool, Ordering},
    };
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    let data = tempfile::tempdir().unwrap();
    let paths = Paths::at(data.path().to_owned()).unwrap();
    let endpoint = paths.endpoint.clone();
    let mut server = tokio::net::windows::named_pipe::ServerOptions::new()
        .first_pipe_instance(true)
        .create(&endpoint)
        .unwrap();
    let stop = Arc::new(AtomicBool::new(false));
    let stop_peer = stop.clone();
    let peer = tokio::spawn(async move {
        let mut observations = 0;
        while !stop_peer.load(Ordering::Acquire) {
            if tokio::time::timeout(Duration::from_millis(20), server.connect())
                .await
                .is_err()
            {
                continue;
            }
            let next = tokio::net::windows::named_pipe::ServerOptions::new()
                .create(&endpoint)
                .unwrap();
            let mut stream = std::mem::replace(&mut server, next);
            let length = stream.read_u32().await.unwrap();
            let mut bytes = vec![0; length as usize];
            stream.read_exact(&mut bytes).await.unwrap();
            let request = Request::decode(&bytes).unwrap();
            assert!(["daemon.stop", "daemon.status"].contains(&request.operation.as_str()));
            observations += 1;
            let response = Response::success(request.request_id, json!({"daemon_state":"running"}));
            let bytes = serde_json::to_vec(&response).unwrap();
            stream.write_u32(bytes.len() as u32).await.unwrap();
            stream.write_all(&bytes).await.unwrap();
            stream.flush().await.unwrap();
            tokio::time::sleep(Duration::from_millis(10)).await;
        }
        observations
    });
    let (commands, work) = mpsc::channel();
    let (send, updates) = mpsc::channel();
    let thread = std::thread::spawn(move || worker(0, paths, work, send));
    commands
        .send(Work {
            alias: "local".into(),
            operation: "daemon.stop".into(),
            params: json!({}),
            start: false,
            exit_after: true,
        })
        .unwrap();
    let update =
        tokio::task::spawn_blocking(move || updates.recv_timeout(Duration::from_secs(13)).unwrap())
            .await
            .unwrap();
    assert!(update.exit_after);
    assert_eq!(update.response.error.unwrap().code, ErrorCode::Timeout);
    assert!(
        !peer.is_finished(),
        "the still-running peer must not be terminated by a stop timeout"
    );
    stop.store(true, Ordering::Release);
    drop(commands);
    tokio::task::spawn_blocking(move || thread.join().unwrap())
        .await
        .unwrap();
    assert!(peer.await.unwrap() > 2);
}
