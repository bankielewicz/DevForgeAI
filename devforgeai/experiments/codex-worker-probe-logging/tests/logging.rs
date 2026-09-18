mod support;
use devforgeai_codex_worker_probe::{
    journal, request,
    runner::{self, Options},
};
use serde_json::{Value, json};
use std::{fs, time::Duration};

fn events(f: &support::Fixture) -> Vec<Value> {
    fs::read_to_string(f.request.run_dir.join("journal.jsonl"))
        .unwrap()
        .lines()
        .map(|l| serde_json::from_str(l).unwrap())
        .collect()
}
fn configured(case: &str, level: &str) -> support::Fixture {
    let f = support::Fixture::new(case);
    let config =
        json!({"schema_version":1,"level":level,"redaction_policy":"closed-v1"}).to_string();
    let path = f.root.path().join("logging.json");
    fs::write(&path, &config).unwrap();
    let mut r: Value = serde_json::from_slice(&fs::read(&f.input).unwrap()).unwrap();
    r["schema_version"] = json!(3);
    r["diagnostics_ref"] = json!(path);
    r["diagnostics_sha256"] = json!(request::digest(config.as_bytes()));
    fs::write(&f.input, r.to_string()).unwrap();
    f
}

#[test]
fn early_stderr_and_silent_exit_survive_without_protocol_receive() {
    for (case, bytes, category) in [
        (
            "WF-04-70",
            b"Error: config.toml:90:1: unknown configuration field `history.notify`\n".as_slice(),
            "strict_config_rejected",
        ),
        ("WF-04-71", b"".as_slice(), "unclassified"),
    ] {
        let f = support::Fixture::new(case);
        let options = Options {
            grace: Duration::from_millis(100),
            ..Default::default()
        };
        let (_, terminal) = runner::run(&f.input, options, &mut |v| {
            if v["kind"] == "server_started" {
                std::thread::sleep(Duration::from_millis(200));
            }
        })
        .unwrap();
        assert_eq!(terminal["tree_stopped"], true);
        let rows = events(&f);
        let exit = &rows.iter().find(|v| v["kind"] == "process_exit").unwrap()["data"];
        let capture = &exit["capture"];
        assert_eq!(capture["stderr"]["bytes"], bytes.len(), "{exit}");
        assert_eq!(capture["stderr"]["sha256"], request::digest(bytes));
        assert_eq!(capture["stderr"]["eof"], true);
        assert_eq!(capture["stdout"]["eof"], true);
        assert_eq!(capture["stderr"]["category"], category);
        assert_eq!(exit["pre_stop_exit_code"], 1);
        assert_eq!(exit["observed_before_stop"], true);
        assert_eq!(exit["worker_exit_code"], 1);
        assert_eq!(capture["drain_complete"], true);
        assert!(journal::inspect(&f.request.run_dir, 0, 100).is_ok());
    }
}

#[test]
fn levels_preserve_mandatory_evidence_and_never_store_child_canaries() {
    for level in ["off", "minimal", "verbose", "debug"] {
        let f = configured("WF-04-72", level);
        let (_, terminal) = f.run();
        assert_eq!(terminal["tree_stopped"], true);
        let rows = events(&f);
        assert!(rows.iter().any(|v| {
            v["kind"] == "process_exit"
                && v["data"]["capture"]["stderr"]["bytes"]
                    .as_u64()
                    .unwrap_or(0)
                    > 0
        }));
        let log = f.request.run_dir.join("diagnostics.jsonl");
        assert_eq!(log.exists(), level != "off");
        if level != "off" {
            let text = fs::read_to_string(&log).unwrap();
            assert!(text.contains("\"event\":\"spawn\""));
            assert!(text.contains("\"event\":\"exit\""));
            assert_eq!(
                text.contains("\"event\":\"launch\""),
                level == "verbose" || level == "debug"
            );
            assert_eq!(text.contains("\"event\":\"chunk\""), level == "debug");
        }
        for name in ["journal.jsonl", "diagnostics.jsonl"] {
            if let Ok(text) = fs::read_to_string(f.request.run_dir.join(name)) {
                assert!(!text.contains("CANARY_SECRET_29417"));
                assert!(!text.contains("Bearer sk-"));
            }
        }
        assert!(journal::inspect(&f.request.run_dir, 0, 100).is_ok());
    }
}

#[test]
fn delayed_consumer_drains_more_than_32_chunks_without_deadlock() {
    let f = support::Fixture::new("WF-04-73");
    let bytes = vec![b'x'; 600_000];
    let (_, terminal) = runner::run(&f.input, Options::default(), &mut |v| {
        if v["kind"] == "server_started" {
            std::thread::sleep(Duration::from_millis(300));
        }
    })
    .unwrap();
    assert_eq!(terminal["tree_stopped"], true);
    let rows = events(&f);
    let summary = &rows.iter().find(|v| v["kind"] == "process_exit").unwrap()["data"]["capture"];
    assert_eq!(summary["stderr"]["bytes"], 600_000);
    assert_eq!(summary["stderr"]["sha256"], request::digest(&bytes));
    assert_eq!(summary["drain_complete"], true);
}

#[test]
fn policy_targets_real_mcp_keys_under_literal_cli_dotted_key_rules() {
    let v: Value =
        serde_json::from_str(devforgeai_codex_worker_probe::launch_policy::RECORD).unwrap();
    let keys: Vec<_> = v["argv"]
        .as_array()
        .unwrap()
        .iter()
        .filter_map(|v| v.as_str())
        .filter_map(|s| s.split_once('='))
        .map(|(k, _)| k)
        .collect();
    assert!(keys.contains(&"mcp_servers.node_repl.enabled"));
    assert!(keys.contains(&"mcp_servers.openaiDeveloperDocs.enabled"));
    assert!(keys.iter().all(|k| !k.contains('"')));
}

#[test]
fn config_rejects_malformed_unknown_missing_drift_and_escape_before_spawn() {
    let invalid = [
        r#"{"schema_version":2,"level":"off","redaction_policy":"closed-v1"}"#,
        r#"{"schema_version":1,"level":"trace","redaction_policy":"closed-v1"}"#,
        r#"{"schema_version":1,"level":"debug","redaction_policy":"raw"}"#,
        r#"{"schema_version":1,"level":"off","redaction_policy":"closed-v1","path":"CANARY_SECRET_29417"}"#,
        r#"{"schema_version":1,"level":"off","level":"debug","redaction_policy":"closed-v1"}"#,
        "{}",
        "{broken",
        "null",
    ];
    for bytes in invalid
        .iter()
        .map(|s| s.as_bytes().to_vec())
        .chain([vec![b' '; 4097]])
    {
        let f = configured("WF-01", "off");
        let mut r: Value = serde_json::from_slice(&fs::read(&f.input).unwrap()).unwrap();
        fs::write(r["diagnostics_ref"].as_str().unwrap(), &bytes).unwrap();
        r["diagnostics_sha256"] = json!(request::digest(&bytes));
        fs::write(&f.input, r.to_string()).unwrap();
        assert_eq!(
            runner::run(&f.input, Options::default(), &mut |_| {}).unwrap_err(),
            "invalid_diagnostics"
        );
        assert!(!f.request.run_dir.exists());
        assert!(!f.root.path().join("peer-trace.jsonl").exists());
    }
    for field in ["diagnostics_ref", "diagnostics_sha256"] {
        for value in [Value::Null, json!("relative"), json!("f".repeat(64))] {
            let f = configured("WF-01", "off");
            let mut r: Value = serde_json::from_slice(&fs::read(&f.input).unwrap()).unwrap();
            r[field] = value;
            fs::write(&f.input, r.to_string()).unwrap();
            assert!(request::validate(&f.input).is_err());
            assert!(!f.request.run_dir.exists());
        }
    }
    let f = configured("WF-01", "off");
    let mut r: Value = serde_json::from_slice(&fs::read(&f.input).unwrap()).unwrap();
    r["schema_version"] = json!(1);
    fs::write(&f.input, r.to_string()).unwrap();
    assert!(request::validate(&f.input).is_err());
}

#[test]
fn config_drift_after_intent_is_rejected_at_final_boundary() {
    let f = configured("WF-01", "debug");
    let (_, v) = runner::run(&f.input, Options::default(), &mut |v| {
        if v["kind"] == "spawn_intent" {
            fs::write(f.root.path().join("logging.json"), b"{}").unwrap();
        }
    })
    .unwrap();
    assert_eq!(v["reason"], "invalid_diagnostics");
    assert!(!events(&f).iter().any(|e| e["kind"] == "server_started"));
    assert!(!f.root.path().join("peer-trace.jsonl").exists());
}

#[test]
fn inspector_rejects_missing_summary_log_and_modified_log() {
    for mutation in ["summary", "missing", "changed", "status"] {
        let f = configured("WF-01", "debug");
        assert_eq!(f.run().0, 0);
        assert!(journal::inspect(&f.request.run_dir, 0, 100).is_ok());
        match mutation {
            "summary" | "status" => {
                let mut rows = events(&f);
                for row in &mut rows {
                    if mutation == "summary" && row["kind"] == "process_exit" {
                        row["data"].as_object_mut().unwrap().remove("capture");
                    }
                    if mutation == "status" && row["data"]["method"] == "diagnostics_status" {
                        row["data"]["status"]["diagnostics_incomplete"] = json!(true);
                    }
                }
                fs::write(
                    f.request.run_dir.join("journal.jsonl"),
                    rows.iter().map(|v| format!("{v}\n")).collect::<String>(),
                )
                .unwrap();
            }
            "missing" => fs::remove_file(f.request.run_dir.join("diagnostics.jsonl")).unwrap(),
            _ => fs::write(f.request.run_dir.join("diagnostics.jsonl"), b"changed\n").unwrap(),
        }
        assert!(
            journal::inspect(&f.request.run_dir, 0, 100).is_err(),
            "{mutation}"
        );
    }
}

#[test]
fn arbitrary_protocol_method_names_cannot_become_log_text_at_any_level() {
    for level in ["off", "minimal", "verbose", "debug"] {
        for case in ["WF-04-74", "WF-04-75"] {
            let f = configured(case, level);
            let mut emitted = Vec::new();
            let (_, v) = runner::run(
                &f.input,
                Options {
                    rpc: Duration::from_millis(500),
                    ..Default::default()
                },
                &mut |e| emitted.push(e.clone()),
            )
            .unwrap();
            assert_eq!(v["tree_stopped"], true);
            assert!(
                !serde_json::to_string(&emitted)
                    .unwrap()
                    .contains("CANARY_SECRET_29417")
            );
            for name in ["journal.jsonl", "diagnostics.jsonl"] {
                if let Ok(bytes) = fs::read_to_string(f.request.run_dir.join(name)) {
                    assert!(
                        !bytes.contains("CANARY_SECRET_29417"),
                        "{level}/{case}/{name}"
                    );
                }
            }
        }
    }
}

#[test]
fn config_exact_size_and_real_junction_boundary() {
    let f = configured("WF-01", "off");
    let path = f.root.path().join("logging.json");
    let mut bytes = fs::read(&path).unwrap();
    bytes.resize(4096, b' ');
    fs::write(&path, &bytes).unwrap();
    let mut r: Value = serde_json::from_slice(&fs::read(&f.input).unwrap()).unwrap();
    r["diagnostics_sha256"] = json!(request::digest(&bytes));
    fs::write(&f.input, r.to_string()).unwrap();
    assert!(request::validate(&f.input).is_ok());
    let real = f.root.path().join("real-config");
    let alias = f.root.path().join("alias-config");
    fs::create_dir(&real).unwrap();
    fs::copy(&path, real.join("logging.json")).unwrap();
    let output = std::process::Command::new("cmd.exe")
        .args(["/d", "/c", "mklink", "/J"])
        .arg(&alias)
        .arg(&real)
        .output()
        .unwrap();
    assert!(
        output.status.success(),
        "junction setup failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    r["diagnostics_ref"] = json!(alias.join("logging.json"));
    fs::write(&f.input, r.to_string()).unwrap();
    assert_eq!(
        runner::run(&f.input, Options::default(), &mut |_| {}).unwrap_err(),
        "invalid_diagnostics"
    );
    assert!(!f.request.run_dir.exists());
    assert!(!f.root.path().join("peer-trace.jsonl").exists());
}

#[test]
fn historical_evidence_inspection_keeps_legacy_input_compatibility() {
    let f = support::Fixture::new("WF-01");
    assert_eq!(f.run().0, 0);
    let path = f.request.run_dir.join("inputs.json");
    let mut inputs: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
    inputs.as_object_mut().unwrap().remove("capture_schema");
    fs::write(path, inputs.to_string()).unwrap();
    let mut rows = events(&f);
    for row in &mut rows {
        if row["kind"] == "process_exit" {
            row["data"] = json!({"worker_exit_code":0,"tree_stopped":true});
        }
    }
    fs::write(
        f.request.run_dir.join("journal.jsonl"),
        rows.iter().map(|v| format!("{v}\n")).collect::<String>(),
    )
    .unwrap();
    assert_eq!(
        journal::inspect(&f.request.run_dir, 0, 100).unwrap()["state"],
        "completed"
    );
}
