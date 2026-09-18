#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/diagnostic.rs"]
mod diagnostic;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/effective_profile.rs"]
mod effective_profile;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/journal.rs"]
mod journal;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/launch_policy.rs"]
mod launch_policy;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/native_identity.rs"]
mod native_identity;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/oracle.rs"]
mod oracle;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/profile_sources.rs"]
mod profile_sources;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/request.rs"]
mod request;
#[path = "C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/runner.rs"]
mod runner;

mod process_windows {
    include!("C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/process_windows.rs");
}

mod protocol {
    include!("C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe/src/protocol.rs");

    pub fn initialize_probe(session: &mut Session<'_>) -> Result<Value> {
        session.preflight_guard = true;
        let result = session.rpc("initialize", json!({"synthetic":true}));
        session.preflight_guard = false;
        result
    }
}

use journal::Journal;
use process_windows::{Incoming, OwnedProcess};
use protocol::Session;
use request::Request;
use runner::Options;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::{
    fs,
    path::{Path, PathBuf},
    time::{Duration, Instant},
};

const STDERR_BLOCK: &[u8] = b"synthetic-startup-failure: early exit\n";

fn request(case_root: &Path, fixture: &Path, exe: &Path, case: &str) -> Request {
    Request {
        schema_version: 1,
        project_id: "offline-startup-repro".into(),
        checkout_id: "synthetic-fixture".into(),
        work_id: case.into(),
        run_id: case.into(),
        candidate_sha256: request::digest(request::TASK),
        checkout_root: fixture.to_owned(),
        run_dir: case_root.join("run"),
        worker_executable: exe.to_owned(),
        worker_sha256: request::hash_file(exe).unwrap(),
        adapter: "peer".into(),
        scenario: "no-work-startup".into(),
        profile: Value::Null,
    }
}

fn fixture(case_root: &Path) -> PathBuf {
    let fixture = case_root.join("fixture");
    fs::create_dir(&fixture).unwrap();
    fs::write(fixture.join("task.json"), request::TASK).unwrap();
    fixture
}

fn journal_events(run_dir: &Path) -> Vec<Value> {
    fs::read_to_string(run_dir.join("journal.jsonl"))
        .unwrap()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect()
}

fn stderr_events(events: &[Value]) -> Vec<Value> {
    events
        .iter()
        .filter(|event| event["data"]["stream"] == "stderr")
        .cloned()
        .collect()
}

fn diagnostics(events: &[Value]) -> Vec<Value> {
    events
        .iter()
        .filter_map(|event| event["data"].get("diagnostic").cloned())
        .collect()
}

fn wait_for_exit(process: &OwnedProcess) -> u32 {
    let deadline = Instant::now() + Duration::from_secs(2);
    loop {
        if let Some(code) = process.exit_code() {
            return code;
        }
        assert!(Instant::now() < deadline, "synthetic early child did not exit");
        std::thread::sleep(Duration::from_millis(5));
    }
}

fn early_exit(base: &Path, exe: &Path) -> Value {
    let root = base.join("SR-01-early-exit");
    fs::create_dir(&root).unwrap();
    let fixture = fixture(&root);
    let request = request(&root, &fixture, exe, "SR-01");
    let mut process = OwnedProcess::spawn(exe, &["early-exit".into()], &fixture).unwrap();
    let child_exit_code = wait_for_exit(&process);
    let counts_before = (process.created_processes().unwrap(), process.active().unwrap());
    assert_eq!(child_exit_code, 23);
    assert_eq!(counts_before, (1, 0));

    let mut journal = Journal::create(&request).unwrap();
    let options = Options {
        total: Duration::from_secs(2),
        rpc: Duration::from_millis(250),
        teardown: Duration::from_secs(2),
        ..Default::default()
    };
    let mut emitted = Vec::new();
    let result = {
        let mut emit = |event: &Value| emitted.push(event.clone());
        let mut session = Session::new(
            &mut process,
            &mut journal,
            &mut emit,
            &options,
            Instant::now() + options.total,
        );
        let result = session.preflight(&request, &[fixture.join("task.json")]);
        assert!(session.thread.is_none() && session.turn.is_none());
        result
    };
    assert_eq!(result, Err("profile_unqualified".into()));

    let receive_deadline = Instant::now() + Duration::from_secs(1);
    let mut queued_stderr = Vec::new();
    let mut saw_end = false;
    while Instant::now() < receive_deadline && (!saw_end || queued_stderr.is_empty()) {
        match process.incoming.recv_timeout(Duration::from_millis(20)) {
            Ok(Incoming::Stderr { bytes, sha256 }) => {
                queued_stderr.push(json!({"bytes":bytes,"sha256":sha256}));
            }
            Ok(Incoming::End) => saw_end = true,
            Ok(Incoming::Line(_)) => panic!("early child produced stdout"),
            Ok(Incoming::Error(reason)) => panic!("reader failed: {reason}"),
            Err(std::sync::mpsc::RecvTimeoutError::Timeout) => {}
            Err(std::sync::mpsc::RecvTimeoutError::Disconnected) => break,
        }
    }
    let expected_hash = format!("{:x}", Sha256::digest(STDERR_BLOCK));
    assert_eq!(
        queued_stderr,
        vec![json!({"bytes":STDERR_BLOCK.len(),"sha256":expected_hash})]
    );
    drop(journal);
    let persisted = journal_events(&request.run_dir);
    assert_eq!(persisted, emitted);
    assert!(stderr_events(&persisted).is_empty());
    assert_eq!(
        diagnostics(&persisted),
        vec![
            json!({
                "schema_version":1,
                "stage":"process_accounting",
                "rpc":"initialize",
                "checkpoint":"before_send",
                "predicate":"unexpected_process_count",
                "total_processes":1,
                "active_processes":0
            }),
            json!({
                "schema_version":1,
                "stage":"rpc",
                "rpc":"initialize",
                "predicate":"process_guard_rejected"
            })
        ]
    );
    let stopped = process.stop(options.teardown);
    let active_after = process.active().unwrap();
    assert!(stopped);
    assert_eq!(active_after, 0);
    let observed = json!({
        "case":"SR-01",
        "result":result,
        "counts_before":{"total":counts_before.0,"active":counts_before.1},
        "child_exit_code":child_exit_code,
        "journal_stderr_events":stderr_events(&persisted),
        "queued_receiver_stderr":queued_stderr,
        "saw_stdout_end":saw_end,
        "diagnostics":diagnostics(&persisted),
        "tree_stopped":stopped,
        "active_after":active_after,
        "thread_id":Value::Null,
        "turn_id":Value::Null
    });
    fs::write(root.join("observed.json"), serde_json::to_vec_pretty(&observed).unwrap()).unwrap();
    observed
}

fn receive_control(base: &Path, exe: &Path) -> Value {
    let root = base.join("SR-02-receive-control");
    fs::create_dir(&root).unwrap();
    let fixture = fixture(&root);
    let request = request(&root, &fixture, exe, "SR-02");
    let mut process = OwnedProcess::spawn(exe, &["control".into()], &fixture).unwrap();
    let counts_before = (process.created_processes().unwrap(), process.active().unwrap());
    assert_eq!(counts_before, (1, 1));
    let mut journal = Journal::create(&request).unwrap();
    let options = Options {
        total: Duration::from_secs(2),
        rpc: Duration::from_secs(1),
        teardown: Duration::from_secs(2),
        ..Default::default()
    };
    let mut emitted = Vec::new();
    let result = {
        let mut emit = |event: &Value| emitted.push(event.clone());
        let mut session = Session::new(
            &mut process,
            &mut journal,
            &mut emit,
            &options,
            Instant::now() + options.total,
        );
        let result = protocol::initialize_probe(&mut session);
        assert!(session.thread.is_none() && session.turn.is_none());
        result
    };
    assert_eq!(result, Ok(json!({"synthetic":"initialize-ok"})));
    drop(journal);
    let persisted = journal_events(&request.run_dir);
    assert_eq!(persisted, emitted);
    let expected_hash = format!("{:x}", Sha256::digest(STDERR_BLOCK));
    let stderr = stderr_events(&persisted);
    assert_eq!(stderr.len(), 1);
    assert_eq!(stderr[0]["data"], json!({
        "stream":"stderr",
        "bytes":STDERR_BLOCK.len(),
        "sha256":expected_hash,
        "content":"omitted"
    }));
    assert_eq!(
        diagnostics(&persisted),
        vec![
            json!({"schema_version":1,"stage":"process_accounting","rpc":"initialize","checkpoint":"before_send","predicate":"only_worker","total_processes":1,"active_processes":1}),
            json!({"schema_version":1,"stage":"process_accounting","rpc":"initialize","checkpoint":"after_receive","predicate":"only_worker","total_processes":1,"active_processes":1})
        ]
    );
    let stopped = process.stop(options.teardown);
    let active_after = process.active().unwrap();
    assert!(stopped);
    assert_eq!(active_after, 0);
    let observed = json!({
        "case":"SR-02",
        "result":result,
        "counts_before":{"total":counts_before.0,"active":counts_before.1},
        "journal_stderr_events":stderr,
        "diagnostics":diagnostics(&persisted),
        "tree_stopped":stopped,
        "active_after":active_after,
        "thread_id":Value::Null,
        "turn_id":Value::Null
    });
    fs::write(root.join("observed.json"), serde_json::to_vec_pretty(&observed).unwrap()).unwrap();
    observed
}

fn main() {
    let base = PathBuf::from(std::env::var_os("STARTUP_REPRO_EVIDENCE").expect("evidence root"));
    fs::create_dir(&base).unwrap();
    let exe = std::env::current_exe()
        .unwrap()
        .parent()
        .unwrap()
        .join("synthetic-peer.exe");
    assert!(exe.is_file());
    let before = request::hash_file(&exe).unwrap();
    let early = early_exit(&base, &exe);
    let control = receive_control(&base, &exe);
    assert_eq!(request::hash_file(&exe).unwrap(), before);
    let summary = json!({
        "schema_version":1,
        "outcome":"observed",
        "early_exit":early,
        "receive_control":control,
        "synthetic_peer":{"path":exe,"sha256":before},
        "native_codex_launched":false
    });
    fs::write(base.join("summary.json"), serde_json::to_vec_pretty(&summary).unwrap()).unwrap();
    println!("{}", serde_json::to_string(&summary).unwrap());
}
