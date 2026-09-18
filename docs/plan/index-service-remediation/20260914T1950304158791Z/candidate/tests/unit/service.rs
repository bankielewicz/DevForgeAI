use super::*;

// Control only scheduling. Real service dispatch, persistence, SQLite and parsing remain active.
fn fixture(data: &Path) -> Service {
    Service {
        inner: Arc::new(Inner {
            data: data.to_owned(),
            environment: id(),
            registry: Mutex::new(Registry::default()),
            store: Mutex::new(Some(Store::open(data).unwrap())),
            storage_error: Mutex::new(None),
            stopping: AtomicBool::new(false),
            cancellations: Mutex::new(BTreeMap::new()),
        }),
        worker: Mutex::new(None),
    }
}
fn request(operation: &str, params: Value) -> Request {
    Request {
        protocol_version: 1,
        request_id: id(),
        operation: operation.into(),
        timeout_ms: 100,
        params,
    }
}

#[test]
fn mutation_deadline_precedes_dispatch_and_stop_cancels_active_tokens() {
    let data = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    let pause = request("daemon.pause", json!({}));
    let result = service.apply(
        &pause,
        Operation::Pause {},
        Instant::now() - Duration::from_secs(1),
    );
    assert_eq!(result.unwrap_err().code, ErrorCode::Timeout);
    assert!(!service.inner.registry.lock().unwrap().paused);
    assert!(service.inner.registry.lock().unwrap().receipts.is_empty());
    let token = Arc::new(AtomicBool::new(false));
    service
        .inner
        .cancellations
        .lock()
        .unwrap()
        .insert("running".into(), token.clone());
    assert!(service.execute(&request("daemon.stop", json!({}))).ok);
    assert!(token.load(Ordering::Acquire));
    assert!(service.is_stopping());
    assert_eq!(
        boundary(&service.inner, &AtomicBool::new(false))
            .unwrap_err()
            .code,
        ErrorCode::JobCancelled
    );
}

#[test]
fn paused_writer_waits_for_resume_and_cancellation_never_acquires_it() {
    let data = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    service.inner.registry.lock().unwrap().paused = true;
    let inner = service.inner.clone();
    let (send, receive) = std::sync::mpsc::channel();
    let waiting = thread::spawn(move || {
        let guard = writer_guard(&inner, &AtomicBool::new(false)).unwrap();
        assert!(!guard.paused);
        send.send(()).unwrap();
    });
    assert!(receive.recv_timeout(Duration::from_millis(70)).is_err());
    service.inner.registry.lock().unwrap().paused = false;
    receive.recv_timeout(Duration::from_secs(1)).unwrap();
    waiting.join().unwrap();
    assert!(
        matches!(writer_guard(&service.inner, &AtomicBool::new(true)), Err(error) if error.code == ErrorCode::JobCancelled)
    );
}

#[test]
fn unavailable_storage_and_removed_projects_cannot_publish() {
    let data = tempfile::tempdir().unwrap();
    let root = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    let added = service.execute(&request(
        "project.add",
        json!({"root":root.path(),"name":"fixture"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    let job_id = added.data["job_id"].as_str().unwrap();
    let job = service.inner.registry.lock().unwrap().jobs[job_id].clone();
    service
        .inner
        .registry
        .lock()
        .unwrap()
        .jobs
        .get_mut(job_id)
        .unwrap()
        .outcome = "running".into();
    let status = service.execute(&request("index.status", json!({"project_id":project})));
    assert_eq!(status.data["activity"], "indexing");
    let token = Arc::new(AtomicBool::new(false));
    service
        .inner
        .cancellations
        .lock()
        .unwrap()
        .insert(job_id.into(), token.clone());
    service.execute(&request("job.cancel", json!({"job_id":job_id})));
    assert!(token.load(Ordering::Acquire));
    token.store(false, Ordering::Release);
    assert!(
        service
            .execute(&request("project.remove", json!({"project_id":project})))
            .ok
    );
    assert!(token.load(Ordering::Acquire));
    let mut parsers = index::ParsePool::new().unwrap();
    assert_eq!(
        run_job(
            &service.inner,
            &job,
            &Arc::new(AtomicBool::new(false)),
            &mut parsers
        )
        .unwrap_err()
        .code,
        ErrorCode::ProjectNotFound
    );
    *service.inner.store.lock().unwrap() = None;
    assert_eq!(
        service.inner.with_store(|_| Ok(())).unwrap_err().code,
        ErrorCode::StorageCorrupt
    );
    assert_eq!(
        service
            .execute(&request("index.rescan", json!({"project_id":project})))
            .error
            .unwrap()
            .code,
        ErrorCode::StorageCorrupt
    );
}

#[test]
fn unverified_freshness_and_shutdown_queue_results_are_explicit() {
    let data = tempfile::tempdir().unwrap();
    let root = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    let added = service.execute(&request(
        "project.add",
        json!({"root":root.path(),"name":"fixture"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    service
        .inner
        .registry
        .lock()
        .unwrap()
        .projects
        .get_mut(project)
        .unwrap()
        .dirty = false;
    assert_eq!(
        service
            .execute(&request("index.status", json!({"project_id":project})))
            .data["freshness"],
        "unknown"
    );
    let token = Arc::new(AtomicBool::new(false));
    service
        .inner
        .cancellations
        .lock()
        .unwrap()
        .insert("token".into(), token.clone());
    service.shutdown().unwrap();
    assert!(token.load(Ordering::Acquire));
    let registry: Value =
        serde_json::from_slice(&fs::read(data.path().join("registrations.json")).unwrap()).unwrap();
    assert_eq!(
        registry["jobs"][added.data["job_id"].as_str().unwrap()]["outcome"],
        "cancelled"
    );
}

#[test]
fn failed_registry_persistence_does_not_commit_a_mode_change() {
    let data = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    fs::create_dir(data.path().join("registrations.json")).unwrap();
    let response = service.execute(&request("daemon.pause", json!({})));
    assert!(!response.ok);
    assert!(!service.inner.registry.lock().unwrap().paused);
    assert!(service.inner.registry.lock().unwrap().receipts.is_empty());
    assert!(service.shutdown().is_err());
}

#[test]
fn poisoned_state_locks_report_internal_errors_without_mutation() {
    let data = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    let inner = service.inner.clone();
    assert!(
        thread::spawn(move || {
            let _guard = inner.registry.lock().unwrap();
            panic!("simulated failed registry owner");
        })
        .join()
        .is_err()
    );
    assert_eq!(
        service
            .execute(&request("daemon.pause", json!({})))
            .error
            .unwrap()
            .code,
        ErrorCode::InternalError
    );
    service.inner.registry.clear_poison();
    assert!(!service.inner.registry.lock().unwrap().paused);
    let inner = service.inner.clone();
    assert!(
        thread::spawn(move || {
            let _guard = inner.store.lock().unwrap();
            panic!("simulated failed writer owner");
        })
        .join()
        .is_err()
    );
    assert_eq!(
        service.inner.with_store(|_| Ok(())).unwrap_err().code,
        ErrorCode::InternalError
    );
    service.inner.store.clear_poison();
    service.shutdown().unwrap();
}

#[test]
fn watcher_access_errors_removed_projects_and_expired_owners_are_distinct() {
    let data = tempfile::tempdir().unwrap();
    let root = tempfile::tempdir().unwrap();
    let service = fixture(data.path());
    let added = service.execute(&request(
        "project.add",
        json!({"root":root.path(),"name":"watch"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    {
        let mut registry = service.inner.registry.lock().unwrap();
        let state = registry.projects.get_mut(project).unwrap();
        state.dirty = false;
        state.last_reconciliation = Some(100);
    }
    let weak = Arc::downgrade(&service.inner);
    record_watch_event(
        &weak,
        project,
        Ok(notify::Event::new(notify::EventKind::Access(
            notify::event::AccessKind::Read,
        ))),
    );
    assert!(!service.inner.registry.lock().unwrap().projects[project].dirty);
    record_watch_event(
        &weak,
        project,
        Err(notify::Error::generic("controlled watcher failure")),
    );
    let updated = service.inner.registry.lock().unwrap().projects[project].clone();
    assert!(updated.dirty);
    assert_eq!(updated.last_reconciliation, None);
    assert_eq!(updated.revision, 2);
    assert!(updated.last_change_ms.is_some());
    service
        .inner
        .registry
        .lock()
        .unwrap()
        .projects
        .remove(project);
    record_watch_event(
        &weak,
        project,
        Ok(notify::Event::new(notify::EventKind::Any)),
    );
    assert!(service.inner.registry.lock().unwrap().projects.is_empty());
    record_watch_event(
        &std::sync::Weak::new(),
        "absent",
        Err(notify::Error::generic("expired owner")),
    );
}

#[test]
fn parser_timeout_publishes_partial_coverage_with_captured_source() {
    let data = tempfile::tempdir().unwrap();
    let root = tempfile::tempdir().unwrap();
    let source = "x = (1 + 2)\n".repeat(3_000_000);
    fs::write(root.path().join("large.py"), &source).unwrap();
    let service = fixture(data.path());
    let added = service.execute(&request(
        "project.add",
        json!({"root":root.path(),"name":"bounded parser"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    let job = {
        let mut registry = service.inner.registry.lock().unwrap();
        registry
            .projects
            .get_mut(project)
            .unwrap()
            .config
            .max_file_bytes = Some(50 * 1024 * 1024);
        registry.jobs[added.data["job_id"].as_str().unwrap()].clone()
    };
    let mut parsers = index::ParsePool::new().unwrap();
    let generation = run_job(
        &service.inner,
        &job,
        &Arc::new(AtomicBool::new(false)),
        &mut parsers,
    )
    .unwrap();
    let summary = service
        .inner
        .with_store(|store| store.summary(project))
        .unwrap()
        .unwrap();
    assert_eq!(summary["coverage"], "partial");
    assert_eq!(summary["text_count"], 1);
    assert_eq!(summary["failed_count"], 1);
    assert_eq!(
        service
            .inner
            .with_store(|store| store.source(&generation, "large.py"))
            .unwrap()
            .unwrap(),
        source.as_bytes()
    );
}
