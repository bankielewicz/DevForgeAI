use devforgeai_index::protocol::{ErrorCode, Request};
use devforgeai_index::service::Service;
use serde_json::{Value, json};
use std::{
    fs, thread,
    time::{Duration, Instant},
};
use tempfile::tempdir;

fn req(operation: &str, params: Value) -> Request {
    Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: operation.into(),
        timeout_ms: 10000,
        params,
    }
}

#[test]
fn unavailable_root_has_a_bounded_retry_and_visible_diagnostic() {
    let data = tempdir().unwrap();
    let parent = tempdir().unwrap();
    let source = parent.path().join("project");
    fs::create_dir(&source).unwrap();
    fs::write(source.join("a.py"), "pass").unwrap();
    let service = Service::open(data.path()).unwrap();
    let added = service.execute(&req("project.add", json!({"root":source,"name":"failure"})));
    let project = added.data["project_id"].as_str().unwrap();
    wait(&service, added.data["job_id"].as_str().unwrap());
    service.execute(&req("daemon.pause", json!({})));
    fs::rename(&source, parent.path().join("moved")).unwrap();
    service.execute(&req("daemon.resume", json!({})));
    thread::sleep(Duration::from_millis(900));
    let state: Value =
        serde_json::from_slice(&fs::read(data.path().join("registrations.json")).unwrap()).unwrap();
    let failed = state["jobs"]
        .as_object()
        .unwrap()
        .values()
        .filter(|job| job["outcome"] == "failed")
        .count();
    assert!(
        failed <= 1,
        "An unavailable root must not cause a retry loop: {failed} failed jobs"
    );
    let status = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data;
    assert_eq!(status["activity"], "failed");
    assert_eq!(status["diagnostic_code"], "ROOT_UNAVAILABLE");
    assert_eq!(status["dirty"], true);
    service.shutdown().unwrap();
}
fn wait(service: &Service, job: &str) -> Value {
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        let response = service.execute(&req("job.status", json!({"job_id":job})));
        assert!(response.ok, "{response:?}");
        if !["queued", "running"].contains(&response.data["outcome"].as_str().unwrap()) {
            return response.data;
        }
        assert!(Instant::now() < deadline, "job timeout");
        thread::sleep(Duration::from_millis(20));
    }
}

#[test]
fn lifecycle_pause_resume_index_removal_and_retry_are_real() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    fs::write(
        source.path().join("main.py"),
        "def first():\n    return 1\n",
    )
    .unwrap();
    let service = Service::open(data.path()).unwrap();
    assert!(service.execute(&req("daemon.pause", json!({}))).ok);
    let add = req(
        "project.add",
        json!({"root":source.path(),"name":"Fixture"}),
    );
    let result = service.execute(&add);
    assert!(result.ok, "{result:?}");
    let project = result.data["project_id"].as_str().unwrap();
    assert_eq!(service.execute(&add).data, result.data);
    let mut changed = add.clone();
    changed.params["name"] = json!("Different");
    assert_eq!(
        service.execute(&changed).error.unwrap().code,
        ErrorCode::RequestIdConflict
    );
    let queued = service.execute(&req("index.rescan", json!({"project_id":project})));
    let job = queued.data["job_id"].as_str().unwrap();
    assert_eq!(queued.data["waiting_for_resume"], true);
    let conflict = service.execute(&req("index.reindex", json!({"project_id":project})));
    assert_eq!(conflict.error.unwrap().code, ErrorCode::JobConflict);
    assert!(service.execute(&req("daemon.resume", json!({}))).ok);
    assert_eq!(wait(&service, job)["outcome"], "succeeded");
    let status = service.execute(&req("index.status", json!({"project_id":project})));
    assert_eq!(status.data["coverage"], "complete");
    assert_eq!(status.data["structural_count"], 1);
    assert!(
        service
            .execute(&req("project.remove", json!({"project_id":project})))
            .ok
    );
    assert_eq!(
        fs::read_to_string(source.path().join("main.py")).unwrap(),
        "def first():\n    return 1\n"
    );
    service.shutdown().unwrap();
}

#[test]
fn paused_mode_and_jobs_survive_restart_without_hidden_resume() {
    let data = tempdir().unwrap();
    let service = Service::open(data.path()).unwrap();
    service.execute(&req("daemon.pause", json!({})));
    service.shutdown().unwrap();
    drop(service);
    let service = Service::open(data.path()).unwrap();
    assert_eq!(
        service.execute(&req("daemon.status", json!({}))).data["indexing_mode"],
        "paused"
    );
    service.shutdown().unwrap();
}

#[test]
fn resume_already_active_does_not_schedule_another_generation() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    fs::write(source.path().join("text.txt"), "unchanged").unwrap();
    let service = Service::open(data.path()).unwrap();
    let added = service.execute(&req(
        "project.add",
        json!({"root":source.path(),"name":"same"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    wait(&service, added.data["job_id"].as_str().unwrap());
    let before = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data["current_generation"]
        .clone();
    service.execute(&req("daemon.resume", json!({})));
    thread::sleep(Duration::from_millis(200));
    let after = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data["current_generation"]
        .clone();
    assert_eq!(before, after, "an already-active Resume must be idempotent");
    service.shutdown().unwrap();
}

#[test]
fn automatic_file_changes_are_debounced_before_publication() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    fs::write(source.path().join("text.txt"), "before").unwrap();
    let service = Service::open(data.path()).unwrap();
    let added = service.execute(&req(
        "project.add",
        json!({"root":source.path(),"name":"debounce"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    wait(&service, added.data["job_id"].as_str().unwrap());
    let before = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data["current_generation"]
        .clone();
    fs::write(source.path().join("text.txt"), "changed").unwrap();
    thread::sleep(Duration::from_millis(200));
    assert_eq!(
        service
            .execute(&req("index.status", json!({"project_id":project})))
            .data["current_generation"],
        before,
        "watcher work must wait for the 500ms debounce"
    );
    let deadline = Instant::now() + Duration::from_secs(5);
    loop {
        let current = service
            .execute(&req("index.status", json!({"project_id":project})))
            .data["current_generation"]
            .clone();
        if current != before {
            break;
        }
        assert!(Instant::now() < deadline);
        thread::sleep(Duration::from_millis(20));
    }
    service.shutdown().unwrap();
}

#[test]
fn project_configuration_cancellation_and_missing_ids_have_typed_outcomes() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    let service = Service::open(data.path()).unwrap();
    service.execute(&req("daemon.pause", json!({})));
    let added = service.execute(&req(
        "project.add",
        json!({"root":source.path(),"name":"typed"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    let missing = uuid::Uuid::new_v4().to_string();
    for operation in [
        "project.remove",
        "index.status",
        "index.rescan",
        "index.reindex",
        "index.reconcile",
    ] {
        assert_eq!(
            service
                .execute(&req(operation, json!({"project_id":missing})))
                .error
                .unwrap()
                .code,
            ErrorCode::ProjectNotFound
        );
    }
    for operation in ["job.status", "job.cancel"] {
        assert_eq!(
            service
                .execute(&req(operation, json!({"job_id":missing})))
                .error
                .unwrap()
                .code,
            ErrorCode::JobNotFound
        );
    }
    assert_eq!(
        service
            .execute(&req(
                "project.update",
                json!({"project_id":missing,"config":{}})
            ))
            .error
            .unwrap()
            .code,
        ErrorCode::ProjectNotFound
    );
    assert_eq!(
        service
            .execute(&req(
                "project.update",
                json!({"project_id":project,"config":{"max_file_bytes":1}})
            ))
            .error
            .unwrap()
            .code,
        ErrorCode::InvalidArgument
    );
    let updated=service.execute(&req("project.update",json!({"project_id":project,"config":{"exclusions":["skip/**"],"text_extensions":["fixture"],"text_names":["README"],"default_exclusions":false,"max_file_bytes":2048}})));
    assert!(updated.ok);
    let listed = service.execute(&req("project.list", json!({})));
    let config = &listed.data["projects"][0]["config"];
    assert_eq!(config["max_file_bytes"], 2048);
    assert_eq!(config["default_exclusions"], false);
    let first = service.execute(&req("index.reconcile", json!({"project_id":project})));
    let job = first.data["job_id"].as_str().unwrap();
    assert_eq!(
        service
            .execute(&req("index.reconcile", json!({"project_id":project})))
            .data["job_id"],
        job
    );
    assert_eq!(
        service
            .execute(&req("job.cancel", json!({"job_id":job})))
            .data["outcome"],
        "cancelled"
    );
    assert_eq!(
        service
            .execute(&req("job.cancel", json!({"job_id":job})))
            .data["outcome"],
        "cancelled"
    );
    let next = service.execute(&req("index.reindex", json!({"project_id":project})));
    assert!(next.ok);
    let next_id = next.data["job_id"].as_str().unwrap();
    assert!(
        service
            .execute(&req("project.remove", json!({"project_id":project})))
            .ok
    );
    assert_eq!(
        service
            .execute(&req("job.status", json!({"job_id":next_id})))
            .data["outcome"],
        "cancelled"
    );
    assert!(service.execute(&req("daemon.diagnostics", json!({}))).ok);
    service.shutdown().unwrap();
}

#[test]
fn restart_interrupts_jobs_expires_history_and_rotates_logs_without_source_content() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    let service = Service::open(data.path()).unwrap();
    service.execute(&req("daemon.pause", json!({})));
    let add = service.execute(&req(
        "project.add",
        json!({"root":source.path(),"name":"private source marker"}),
    ));
    let project = add.data["project_id"].as_str().unwrap();
    let queued = service.execute(&req("index.rescan", json!({"project_id":project})));
    let job = queued.data["job_id"].as_str().unwrap().to_owned();
    let identity = service.environment_id().to_owned();
    service.shutdown().unwrap();
    drop(service);
    let registry_path = data.path().join("registrations.json");
    let mut registry: Value = serde_json::from_slice(&fs::read(&registry_path).unwrap()).unwrap();
    registry["jobs"][&job]["outcome"] = json!("running");
    let old = "550e8400-e29b-41d4-a716-446655440000";
    let mut old_job = registry["jobs"][&job].clone();
    old_job["id"] = json!(old);
    old_job["outcome"] = json!("succeeded");
    old_job["updated_at"] = json!(0);
    registry["jobs"][old] = old_job;
    fs::write(&registry_path, serde_json::to_vec(&registry).unwrap()).unwrap();
    for number in 1..=5 {
        fs::write(
            data.path().join(format!("index.log.{number}")),
            format!("rotation-{number}"),
        )
        .unwrap();
    }
    let log = fs::File::create(data.path().join("index.log")).unwrap();
    log.set_len(10 * 1024 * 1024).unwrap();
    drop(log);
    let service = Service::open(data.path()).unwrap();
    assert_eq!(service.environment_id(), identity);
    assert_eq!(
        service
            .execute(&req("job.status", json!({"job_id":job})))
            .data["outcome"],
        "interrupted"
    );
    assert_eq!(
        service
            .execute(&req("job.status", json!({"job_id":old})))
            .error
            .unwrap()
            .code,
        ErrorCode::JobNotFound
    );
    assert_eq!(
        fs::metadata(data.path().join("index.log.1")).unwrap().len(),
        10 * 1024 * 1024
    );
    assert_eq!(
        fs::read_to_string(data.path().join("index.log.5")).unwrap(),
        "rotation-4"
    );
    let log = fs::read_to_string(data.path().join("index.log")).unwrap();
    assert!(!log.contains("private source marker"));
    for line in log.lines() {
        let row: Value = serde_json::from_str(line).unwrap();
        assert!(row["request_id"].is_string());
        assert!(row["duration_ms"].is_number());
        assert!(row.get("params").is_none());
    }
    service.shutdown().unwrap();
}

#[test]
fn mixed_file_reconciliation_has_exact_counters_reuses_bytes_and_preserves_prior_on_failure() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    for (name, bytes) in [
        ("good.py", b"def hello(): pass".as_slice()),
        ("syntax.rs", b"fn broken( {"),
        ("notes.txt", b"plain text"),
        ("binary.txt", b"\0\0"),
        ("utf16.txt", b"\xff\xfeh\0"),
        ("unknown.xyz", b"unused"),
        (".env", b"secret bytes"),
    ] {
        fs::write(source.path().join(name), bytes).unwrap();
    }
    let service = Service::open(data.path()).unwrap();
    let add = service.execute(&req(
        "project.add",
        json!({"root":source.path(),"name":"mixed"}),
    ));
    let project = add.data["project_id"].as_str().unwrap();
    assert_eq!(
        wait(&service, add.data["job_id"].as_str().unwrap())["outcome"],
        "succeeded"
    );
    service.execute(&req("daemon.pause", json!({})));
    let status = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data;
    for (name, count) in [
        ("eligible_count", 5),
        ("text_count", 3),
        ("structural_count", 2),
        ("excluded_count", 1),
        ("skipped_count", 3),
        ("failed_count", 1),
    ] {
        assert_eq!(status[name], count, "{name}: {status}");
    }
    assert_eq!(status["coverage"], "partial");
    let first = status["current_generation"].as_str().unwrap().to_owned();
    let job = service.execute(&req("index.rescan", json!({"project_id":project})));
    service.execute(&req("daemon.resume", json!({})));
    assert_eq!(
        wait(&service, job.data["job_id"].as_str().unwrap())["outcome"],
        "succeeded"
    );
    service.execute(&req("daemon.pause", json!({})));
    let next = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data;
    assert_ne!(next["current_generation"], first);
    let store = devforgeai_index::storage::Store::open(data.path()).unwrap();
    assert_eq!(
        store.source(&first, "good.py").unwrap(),
        Some(b"def hello(): pass".to_vec())
    );
    assert_eq!(
        store
            .source(next["current_generation"].as_str().unwrap(), "good.py")
            .unwrap(),
        Some(b"def hello(): pass".to_vec())
    );
    assert_eq!(store.source(&first, ".env").unwrap(), None);
    drop(store);
    fs::write(source.path().join(".gitignore"), "[z-a]").unwrap();
    let job = service.execute(&req("index.reindex", json!({"project_id":project})));
    service.execute(&req("daemon.resume", json!({})));
    assert_eq!(
        wait(&service, job.data["job_id"].as_str().unwrap())["outcome"],
        "failed"
    );
    let failed = service
        .execute(&req("index.status", json!({"project_id":project})))
        .data;
    assert_eq!(failed["current_generation"], next["current_generation"]);
    assert_eq!(failed["diagnostic_code"], "INTERNAL_ERROR");
    assert_eq!(failed["dirty"], true);
    service.shutdown().unwrap();
}

#[test]
fn invalid_registrations_globs_and_rebuilds_fail_without_mutation() {
    let data = tempdir().unwrap();
    fs::write(data.path().join("registrations.json"), b"{").unwrap();
    assert!(
        matches!(Service::open(data.path()), Err(error) if error.code == ErrorCode::StorageCorrupt)
    );
    fs::remove_file(data.path().join("registrations.json")).unwrap();
    let source = tempdir().unwrap();
    let service = Service::open(data.path()).unwrap();
    service.execute(&req("daemon.pause", json!({})));
    let added = service.execute(&req(
        "project.add",
        json!({"root":source.path(),"name":"valid"}),
    ));
    let project = added.data["project_id"].as_str().unwrap();
    let before = service.execute(&req("project.list", json!({}))).data;
    let invalid = service.execute(&req(
        "project.update",
        json!({"project_id":project,"config":{"exclusions":["[z-a]"]}}),
    ));
    assert_eq!(invalid.error.unwrap().code, ErrorCode::InvalidArgument);
    assert_eq!(
        service.execute(&req("project.list", json!({}))).data,
        before
    );
    let missing = "550e8400-e29b-41d4-a716-446655440000";
    for (id, affected, expected) in [
        (missing, vec![missing], ErrorCode::ProjectNotFound),
        (project, vec![missing], ErrorCode::InvalidArgument),
        (project, vec![project], ErrorCode::InvalidArgument),
    ] {
        assert_eq!(
            service
                .execute(&req(
                    "index.rebuild",
                    json!({"project_id":id,"affected_projects":affected})
                ))
                .error
                .unwrap()
                .code,
            expected
        );
    }
    assert_eq!(
        service
            .execute(&req(
                "project.add",
                json!({"root":source.path(),"name":"duplicate"})
            ))
            .error
            .unwrap()
            .code,
        ErrorCode::RootOverlap
    );
    service.shutdown().unwrap();
}
