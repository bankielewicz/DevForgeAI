//! QA-LOG-01/02 development regressions; public CLI observations are read-only.
mod support;
use devforgeai_codex_worker_probe::{
    journal::{self, Journal},
    request,
    runner::{self, Options},
};
use serde_json::{Value, json};
use std::{collections::BTreeMap, fs, path::Path, process::Command, time::Duration};

fn rows(f: &support::Fixture) -> Vec<Value> {
    fs::read_to_string(f.request.run_dir.join("journal.jsonl"))
        .unwrap()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect()
}

fn write_rows(f: &support::Fixture, rows: &[Value]) {
    fs::write(
        f.request.run_dir.join("journal.jsonl"),
        rows.iter()
            .map(|row| format!("{row}\n"))
            .collect::<String>(),
    )
    .unwrap();
}

fn inventory(root: &Path) -> BTreeMap<String, Vec<u8>> {
    let mut files = BTreeMap::new();
    for entry in fs::read_dir(root).unwrap() {
        let entry = entry.unwrap();
        let path = entry.path();
        if entry.file_type().unwrap().is_dir() {
            files.extend(inventory(&path));
        } else {
            files.insert(path.to_string_lossy().into_owned(), fs::read(path).unwrap());
        }
    }
    files
}

// Expected state/code come from the contract, never the inspector under test.
// Byte/membership readback includes fixture, peer trace, request and all run files.
fn observation(f: &support::Fixture, label: &str, expected: &str) -> bool {
    let before = inventory(f.root.path());
    let library = journal::inspect(&f.request.run_dir, 0, 100);
    let cli = Command::new(env!("CARGO_BIN_EXE_devforgeai-codex-worker-probe"))
        .arg("inspect")
        .arg("--run-dir")
        .arg(&f.request.run_dir)
        .args(["--after", "0", "--limit", "100"])
        .output()
        .unwrap();
    assert_eq!(inventory(f.root.path()), before, "inspection changed bytes");
    let rejected = expected == "evidence_corrupt";
    let agrees = if rejected {
        library.as_ref().err().map(String::as_str) == Some(expected)
            && cli.status.code() == Some(4)
            && cli.stdout.is_empty()
            && serde_json::from_slice::<Value>(&cli.stderr).unwrap()["error"] == expected
    } else {
        library.as_ref().is_ok_and(|v| v["state"] == expected)
            && cli.status.code() == Some(0)
            && cli.stderr.is_empty()
            && serde_json::from_slice::<Value>(&cli.stdout).unwrap()["state"] == expected
    };
    fs::write(
        f.root.path().join(format!("{label}-stdout.txt")),
        &cli.stdout,
    )
    .unwrap();
    fs::write(
        f.root.path().join(format!("{label}-stderr.txt")),
        &cli.stderr,
    )
    .unwrap();
    fs::write(
        f.root.path().join(format!("{label}-observation.json")),
        serde_json::to_vec_pretty(&json!({
            "expected":expected,"library":library,"cli_exit_code":cli.status.code(),
            "read_only":true,"expectation_met":agrees
        }))
        .unwrap(),
    )
    .unwrap();
    agrees
}

fn configured(case: &str, level: &str) -> support::Fixture {
    let mut f = support::Fixture::new(case);
    let config = json!({"schema_version":1,"level":level,"redaction_policy":"closed-v1"});
    let bytes = serde_json::to_vec(&config).unwrap();
    let path = f.root.path().join("logging.json");
    fs::write(&path, &bytes).unwrap();
    f.request.schema_version = 3;
    f.request.diagnostics_ref = Some(path);
    f.request.diagnostics_sha256 = Some(request::digest(&bytes));
    fs::write(&f.input, serde_json::to_vec(&f.request).unwrap()).unwrap();
    f
}

fn completed(level: &str) -> support::Fixture {
    let f = configured("WF-01", level);
    assert_eq!(f.run().0, 0);
    assert!(observation(&f, "control", "completed"));
    f
}

// Historical-record fixture only: no native admission, worker launch or qualification.
// Uses the same typed journal writer as existing preflight recovery tests.
fn preflight(schema: u32) -> support::Fixture {
    let mut f = if schema == 3 {
        configured("WF-11", "off")
    } else {
        support::Fixture::new("WF-11")
    };
    let review = f.root.path().join("review.json");
    fs::write(&review, b"{}").unwrap();
    fs::remove_file(f.request.checkout_root.join("peer-case.txt")).unwrap();
    f.request.schema_version = schema;
    f.request.adapter = "codex-0.154.0-stdio".into();
    f.request.profile = json!({"model":"gpt-6-astra","effort":"high","review_ref":review,
        "review_sha256":request::digest(b"{}"),"launch_policy_id":"p","launch_policy_sha256":"0".repeat(64)});
    let mut j = Journal::create(&f.request).unwrap();
    j.append("admitted", json!({})).unwrap();
    j.append(
        "worker_event",
        json!({"method":"native_identity_rechecked"}),
    )
    .unwrap();
    j.append("spawn_intent", json!({})).unwrap();
    j.append("server_started", json!({"pid_observation":123}))
        .unwrap();
    for stage in [
        "config",
        "requirements",
        "features",
        "hooks",
        "plugins",
        "apps",
        "mcp",
    ] {
        j.append("worker_event", json!({"preflight":stage,"observation":{}}))
            .unwrap();
    }
    j.append("profile_checked", json!({"mode":"chatgpt","plan":"pro"}))
        .unwrap();
    let stream = json!({"bytes":0,"sha256":request::digest(b""),"eof":true,"read_error":null,
        "byte_overflow":false,"queue_overflow":false,"line_overflow":false,"detail_dropped":0,
        "utf8_valid":true,"lines":0,"final_line_bytes":0,"max_line_bytes":0,"queue_high_water":0,
        "category":"unclassified","classifier_version":"startup-v1","classification_truncated":false});
    j.append(
        "process_exit",
        json!({"worker_exit_code":0,"tree_stopped":true,
        "observed_before_stop":false,"pre_stop_exit_code":null,
        "capture":{"stdout":stream,"stderr":stream,"drain_complete":true}}),
    )
    .unwrap();
    let status = j.finish_diagnostics().unwrap();
    j.append("worker_event", status).unwrap();
    j.append(
        "terminal",
        json!({"outcome":"preflight_checked","reason":"preflight_checked",
        "thread_id":null,"turn_id":null,"worker_exit_code":0,"tree_stopped":true,
        "fixture_unchanged":true,"oracle":"not_evaluated","usage":null,"open_work":["w"]}),
    )
    .unwrap();
    drop(j);
    assert!(observation(&f, "control", "preflight_checked"));
    f
}

const CAPTURE_MUTATIONS: &[&str] = &[
    "drain",
    "stdout_eof",
    "stderr_eof",
    "stdout_error",
    "stderr_error",
    "stdout_overflow",
    "stderr_overflow",
];
const EXIT_MUTATIONS: &[&str] = &[
    "missing",
    "null",
    "nonzero",
    "string",
    "negative",
    "too_large",
    "boolean",
    "terminal_nonzero",
    "both_nonzero",
];

fn mutate(f: &support::Fixture, mutation: &str) {
    let mut data = rows(f);
    fs::write(
        f.root.path().join("journal-before.jsonl"),
        fs::read(f.request.run_dir.join("journal.jsonl")).unwrap(),
    )
    .unwrap();
    let exit = &mut data
        .iter_mut()
        .find(|row| row["kind"] == "process_exit")
        .unwrap()["data"];
    match mutation {
        "drain" => exit["capture"]["drain_complete"] = json!(false),
        "missing" => {
            exit.as_object_mut().unwrap().remove("worker_exit_code");
        }
        "null" => exit["worker_exit_code"] = Value::Null,
        "nonzero" | "both_nonzero" => exit["worker_exit_code"] = json!(29),
        "string" => exit["worker_exit_code"] = json!("0"),
        "negative" => exit["worker_exit_code"] = json!(-1),
        "too_large" => exit["worker_exit_code"] = json!(u64::from(u32::MAX) + 1),
        "boolean" => exit["worker_exit_code"] = json!(true),
        "terminal_nonzero" => {}
        _ => {
            let (stream, field) = mutation.split_once('_').unwrap();
            match field {
                "eof" => {
                    exit["capture"][stream]["eof"] = json!(false);
                    exit["capture"]["drain_complete"] = json!(false);
                }
                "error" => {
                    exit["capture"][stream]["read_error"] = json!("pipe_read_failed");
                    exit["capture"]["drain_complete"] = json!(false);
                }
                "overflow" => exit["capture"][stream]["byte_overflow"] = json!(true),
                _ => panic!("unknown mutation"),
            }
        }
    }
    if matches!(mutation, "terminal_nonzero" | "both_nonzero") {
        data.last_mut().unwrap()["data"]["worker_exit_code"] = json!(29);
    }
    write_rows(f, &data);
}

#[test]
fn qa_log_01_completed_requires_complete_capture_at_every_level() {
    let mut accepted = Vec::new();
    for level in ["off", "minimal", "verbose", "debug"] {
        for mutation in CAPTURE_MUTATIONS {
            let f = completed(level);
            mutate(&f, mutation);
            if !observation(&f, mutation, "evidence_corrupt") {
                accepted.push((level, *mutation));
            }
        }
    }
    assert!(
        accepted.is_empty(),
        "incomplete success accepted: {accepted:?}"
    );
}

#[test]
fn qa_log_01_preflight_requires_complete_capture() {
    let mut accepted = Vec::new();
    for schema in [2, 3] {
        for mutation in CAPTURE_MUTATIONS {
            let f = preflight(schema);
            mutate(&f, mutation);
            if !observation(&f, mutation, "evidence_corrupt") {
                accepted.push((schema, *mutation));
            }
        }
    }
    assert!(
        accepted.is_empty(),
        "incomplete preflight accepted: {accepted:?}"
    );
}

#[test]
fn qa_log_02_completed_requires_present_typed_matching_exit() {
    let mut accepted = Vec::new();
    for level in ["off", "debug"] {
        for mutation in EXIT_MUTATIONS {
            let f = completed(level);
            mutate(&f, mutation);
            if !observation(&f, mutation, "evidence_corrupt") {
                accepted.push((level, *mutation));
            }
        }
    }
    assert!(accepted.is_empty(), "invalid exit accepted: {accepted:?}");
}

#[test]
fn qa_log_02_preflight_requires_present_typed_matching_exit() {
    let mut accepted = Vec::new();
    for schema in [2, 3] {
        for mutation in EXIT_MUTATIONS {
            let f = preflight(schema);
            mutate(&f, mutation);
            if !observation(&f, mutation, "evidence_corrupt") {
                accepted.push((schema, *mutation));
            }
        }
    }
    assert!(
        accepted.is_empty(),
        "invalid preflight exit accepted: {accepted:?}"
    );
}

#[test]
fn qa_log_02_failed_run_still_requires_post_stop_field_presence() {
    let f = configured("WF-07", "off");
    assert_eq!(f.run().0, 4);
    assert!(observation(&f, "control", "failed"));
    mutate(&f, "missing");
    assert!(observation(&f, "missing", "evidence_corrupt"));
}

#[test]
fn failure_outcomes_preserve_incomplete_capture_and_nullable_exits() {
    for (case, outcome, code) in [
        ("WF-03-1", "blocked", 3),
        ("WF-04-70", "failed", 4),
        ("WF-01", "cancelled", 5),
        ("WF-16-1", "timed_out", 6),
        ("WF-01", "cleanup_uncertain", 7),
    ] {
        for stream in ["stdout", "stderr"] {
            let mut f = configured(case, "off");
            if outcome == "cancelled" {
                f.request.scenario = "cancel".into();
                fs::write(&f.input, serde_json::to_vec(&f.request).unwrap()).unwrap();
            }
            let (actual, terminal) = runner::run(
                &f.input,
                Options {
                    total: Duration::from_secs(3),
                    rpc: Duration::from_millis(200),
                    grace: Duration::from_millis(100),
                    uncertain_cleanup: outcome == "cleanup_uncertain",
                    ..Default::default()
                },
                &mut |_| {},
            )
            .unwrap();
            assert_eq!(actual, code, "{outcome}: {terminal}");
            assert_eq!(terminal["outcome"], outcome);
            if outcome == "failed" {
                assert_eq!(terminal["worker_exit_code"], 1);
            }
            assert!(observation(&f, "control", outcome));
            let mut data = rows(&f);
            let exit = &mut data
                .iter_mut()
                .find(|row| row["kind"] == "process_exit")
                .unwrap()["data"];
            exit["capture"]["drain_complete"] = json!(false);
            exit["capture"][stream]["eof"] = json!(false);
            exit["capture"][stream]["read_error"] = json!("pipe_read_failed");
            exit["capture"][stream]["byte_overflow"] = json!(true);
            write_rows(&f, &data);
            assert!(observation(&f, "incomplete", outcome));
            data.iter_mut()
                .find(|row| row["kind"] == "process_exit")
                .unwrap()["data"]["worker_exit_code"] = Value::Null;
            data.last_mut().unwrap()["data"]["worker_exit_code"] = Value::Null;
            write_rows(&f, &data);
            assert!(observation(&f, "explicit-null", outcome));
        }
    }
}

#[test]
fn historical_schema_one_and_two_remain_inspectable() {
    for schema in [1, 2] {
        let f = if schema == 1 {
            let f = support::Fixture::new("WF-01");
            assert_eq!(f.run().0, 0);
            f
        } else {
            preflight(2)
        };
        let path = f.request.run_dir.join("inputs.json");
        let mut inputs: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
        inputs.as_object_mut().unwrap().remove("capture_schema");
        fs::write(path, inputs.to_string()).unwrap();
        let mut data = rows(&f);
        for row in &mut data {
            if row["kind"] == "process_exit" {
                row["data"] = json!({"worker_exit_code":0,"tree_stopped":true});
            }
        }
        data.retain(|row| row["data"]["method"] != "diagnostics_status");
        for (index, row) in data.iter_mut().enumerate() {
            row["seq"] = json!(index + 1);
        }
        write_rows(&f, &data);
        assert!(observation(
            &f,
            "historical",
            if schema == 1 {
                "completed"
            } else {
                "preflight_checked"
            }
        ));
    }
}

#[test]
fn current_schema_one_capture_cannot_bypass_success_checks() {
    let mut accepted = Vec::new();
    for mutation in ["drain", "missing", "nonzero"] {
        let f = support::Fixture::new("WF-01");
        assert_eq!(f.run().0, 0);
        assert!(observation(&f, "control", "completed"));
        mutate(&f, mutation);
        if !observation(&f, mutation, "evidence_corrupt") {
            accepted.push(mutation);
        }
    }
    assert!(
        accepted.is_empty(),
        "current schema 1 bypassed checks: {accepted:?}"
    );
}

#[test]
fn interrupted_prefix_keeps_incomplete_capture_as_observation() {
    let f = completed("off");
    mutate(&f, "stdout_error");
    let mut data = rows(&f);
    data.pop();
    write_rows(&f, &data);
    assert!(observation(&f, "interrupted", "interrupted_unknown"));
}

#[test]
fn dropped_detail_and_pre_stop_timing_do_not_invalidate_complete_capture() {
    let f = completed("debug");
    let mut data = rows(&f);
    let exit = &mut data
        .iter_mut()
        .find(|row| row["kind"] == "process_exit")
        .unwrap()["data"];
    exit["observed_before_stop"] = json!(false);
    exit["pre_stop_exit_code"] = Value::Null;
    for stream in ["stdout", "stderr"] {
        exit["capture"][stream]["detail_dropped"] = json!(99);
        exit["capture"][stream]["classification_truncated"] = json!(true);
    }
    write_rows(&f, &data);
    assert!(observation(&f, "detail-only", "completed"));
}
