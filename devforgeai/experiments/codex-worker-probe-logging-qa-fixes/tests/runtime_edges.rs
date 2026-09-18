mod support;

use devforgeai_codex_worker_probe::{
    journal::{self, Journal},
    request,
    runner::{self, Options},
};
use serde_json::{Value, json};
use std::{fs, path::PathBuf, process::Command, time::Duration};

#[test]
fn disappearing_fixture_after_admission_cannot_be_a_successful_run() {
    let fixture = support::Fixture::new("WF-19-1");
    let moved = fixture.root.path().join("preserved-missing-fixture");
    let sentinel = fixture.root.path().join("outside-sentinel.txt");
    fs::write(&sentinel, b"unchanged outside fixture").unwrap();
    let resolved_root = request::resolve(fixture.root.path()).unwrap();
    assert!(fixture.request.checkout_root.starts_with(&resolved_root));
    assert_eq!(
        request::resolve(moved.parent().unwrap()).unwrap(),
        resolved_root
    );
    assert!(!moved.exists());
    let mut events = Vec::new();
    let (code, terminal) = runner::run(
        &fixture.input,
        Options {
            total: Duration::from_secs(2),
            rpc: Duration::from_millis(500),
            grace: Duration::from_millis(100),
            teardown: Duration::from_secs(1),
            ..Default::default()
        },
        &mut |event| {
            events.push(event.clone());
            if event["kind"] == "admitted" {
                fs::rename(&fixture.request.checkout_root, &moved).unwrap();
            }
        },
    )
    .unwrap();
    assert_eq!(code, 4);
    assert_eq!(terminal["reason"], "fixture_changed");
    assert_eq!(terminal["fixture_unchanged"], false);
    assert_eq!(terminal["oracle"], "not_evaluated");
    assert_eq!(terminal["tree_stopped"], true);
    assert_eq!(terminal["worker_exit_code"], Value::Null);
    assert_eq!(terminal["thread_id"], Value::Null);
    assert_eq!(terminal["turn_id"], Value::Null);
    assert_eq!(
        events
            .iter()
            .filter(|e| e["kind"] == "spawn_intent")
            .count(),
        1
    );
    assert!(!events.iter().any(|e| e["kind"] == "server_started"));
    assert!(!fixture.root.path().join("peer-trace.jsonl").exists());
    assert_eq!(fs::read(moved.join("task.json")).unwrap(), request::TASK);
    assert_eq!(fs::read(sentinel).unwrap(), b"unchanged outside fixture");
}

#[test]
fn journal_creation_and_exclusive_writes_preserve_existing_bytes_on_failure() {
    let fixture = support::Fixture::new("WF-19-2");
    let parent_file = fixture.root.path().join("file-is-not-a-directory");
    fs::write(&parent_file, b"preserve parent").unwrap();
    let mut request = fixture.request.clone();
    request.run_dir = parent_file.join("run");
    assert_eq!(
        Journal::create(&request).err().as_deref(),
        Some("evidence_write_failed")
    );
    assert_eq!(fs::read(&parent_file).unwrap(), b"preserve parent");
    assert!(!fixture.request.run_dir.exists());
    let existing = fixture.root.path().join("existing-evidence.json");
    fs::write(&existing, b"original evidence\n").unwrap();
    assert_eq!(
        journal::write_new(&existing, b"replacement").unwrap_err(),
        "evidence_write_failed"
    );
    assert_eq!(fs::read(existing).unwrap(), b"original evidence\n");
    assert!(!fixture.root.path().join("peer-trace.jsonl").exists());
}

#[test]
fn source_cli_distinguishes_invalid_paths_from_unqualified_source_types() {
    let executable = env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe");
    let relative = Command::new(executable)
        .args(["profile-sources", "--checkout-root", "relative-fixture"])
        .output()
        .unwrap();
    assert_eq!(relative.status.code(), Some(2));
    assert!(relative.stdout.is_empty());
    assert_eq!(
        serde_json::from_slice::<Value>(&relative.stderr).unwrap(),
        json!({"error":"invalid_path"})
    );

    let storage = support::Fixture::new("WF-17");
    let workspace = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .unwrap()
        .to_path_buf();
    let trial_parent = workspace.join("docs/plan/framework-worker-trials");
    let trial = tempfile::Builder::new()
        .prefix("RT-source-type-")
        .tempdir_in(&trial_parent)
        .unwrap();
    let fixture = trial.path().join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    let user = storage.root.path().join("synthetic-user");
    let system = storage.root.path().join("synthetic-system");
    let wrong_type = user.join(".codex/config.toml");
    fs::create_dir_all(&wrong_type).unwrap();
    fs::create_dir(&system).unwrap();
    let output = Command::new(executable)
        .args(["profile-sources", "--checkout-root"])
        .arg(&fixture)
        .env("USERPROFILE", &user)
        .env("PROGRAMDATA", &system)
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(3));
    assert!(output.stdout.is_empty());
    assert_eq!(
        serde_json::from_slice::<Value>(&output.stderr).unwrap(),
        json!({"error":"profile_source_type"})
    );
    assert!(wrong_type.is_dir());
    assert_eq!(fs::read(fixture.join("task.json")).unwrap(), request::TASK);
    assert!(!trial.path().join("run").exists());
    fs::write(
        storage.root.path().join("source-cli.stdout.bin"),
        output.stdout,
    )
    .unwrap();
    fs::write(
        storage.root.path().join("source-cli.stderr.bin"),
        output.stderr,
    )
    .unwrap();
    if std::env::var_os("WF_TEST_EVIDENCE").is_some() {
        let _ = trial.keep();
    }
}

#[test]
fn public_preflight_review_rejects_a_peer_without_native_profile() {
    let fixture = support::Fixture::new("WF-01");
    assert_eq!(
        fixture.request.verify_preflight_review().unwrap_err(),
        "profile_unqualified"
    );
    assert!(!fixture.request.run_dir.exists());
    assert!(!fixture.root.path().join("peer-trace.jsonl").exists());
    assert_eq!(
        fs::read(fixture.request.checkout_root.join("task.json")).unwrap(),
        request::TASK
    );
}

#[test]
fn public_review_entrypoints_reject_untrusted_bytes_before_work() {
    for case in ["missing", "oversized", "digest-mismatch", "malformed"] {
        let fixture = support::Fixture::new("WF-17");
        let review_path = fixture.root.path().join("untrusted-review.json");
        let bytes = match case {
            "oversized" => vec![b' '; 65_537],
            "digest-mismatch" | "malformed" => b"not valid JSON".to_vec(),
            "missing" => Vec::new(),
            _ => unreachable!(),
        };
        if case != "missing" {
            fs::write(&review_path, &bytes).unwrap();
        }
        let mut native_request = fixture.request.clone();
        native_request.schema_version = 2;
        native_request.adapter = "codex-0.154.0-stdio".into();
        native_request.profile = json!({
            "model": "gpt-6-astra",
            "effort": "high",
            "review_ref": review_path,
            "review_sha256": if case == "digest-mismatch" {
                "0".repeat(64)
            } else {
                request::digest(&bytes)
            },
            "launch_policy_id": "codex-0.154.0-readonly-no-external-tools-v3",
            "launch_policy_sha256": "c8ef7b6184e20fd55833c9b8f7cd17b6dc1f0af494ca367c857953680dab1b49"
        });
        assert!(native_request.profile().unwrap().is_some());
        devforgeai_codex_worker_probe::launch_policy::args(
            &native_request.adapter,
            native_request.schema_version,
            native_request.profile["launch_policy_id"].as_str().unwrap(),
            native_request.profile["launch_policy_sha256"]
                .as_str()
                .unwrap(),
        )
        .expect("review test requires an otherwise qualified launch policy");
        assert_eq!(
            native_request.verify_preflight_review().unwrap_err(),
            "profile_unqualified",
            "{case}"
        );
        assert_eq!(
            native_request.verify_review().unwrap_err(),
            "profile_unqualified",
            "{case}"
        );
        assert!(!fixture.request.run_dir.exists(), "{case}");
        assert!(
            !fixture.root.path().join("peer-trace.jsonl").exists(),
            "{case}"
        );
        if case == "missing" {
            assert!(!review_path.exists());
        } else {
            assert_eq!(fs::read(review_path).unwrap(), bytes);
        }
        assert_eq!(
            fs::read(fixture.request.checkout_root.join("task.json")).unwrap(),
            request::TASK
        );
    }
}
