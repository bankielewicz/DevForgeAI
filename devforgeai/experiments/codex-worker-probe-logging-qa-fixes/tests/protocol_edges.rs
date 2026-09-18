mod support;

use devforgeai_codex_worker_probe::{
    journal::Journal, process_windows::OwnedProcess, protocol::Session, request, runner::Options,
};
use serde_json::{Value, json};
use std::{
    fs,
    path::PathBuf,
    time::{Duration, Instant},
};

struct Observation {
    result: Result<(), String>,
    trace: Vec<Value>,
    events: Vec<Value>,
    evidence: String,
}

fn run(case: &str) -> Observation {
    let fixture = support::Fixture::new("WF-01");
    let trace_path = fixture.root.path().join("protocol-edges-trace.jsonl");
    let exe = PathBuf::from(env!("CARGO_BIN_EXE_protocol-edges-peer"));
    let args = vec![
        "--case".to_owned(),
        case.to_owned(),
        "--trace".to_owned(),
        trace_path.to_string_lossy().into_owned(),
        "--fixture-root".to_owned(),
        fixture.request.checkout_root.to_string_lossy().into_owned(),
    ];
    let mut process = OwnedProcess::spawn(&exe, &args, &fixture.request.checkout_root).unwrap();
    let options = Options {
        total: Duration::from_secs(3),
        rpc: Duration::from_millis(500),
        teardown: Duration::from_secs(1),
        ..Default::default()
    };
    let mut journal = Journal::create(&fixture.request).unwrap();
    let mut emitted = Vec::new();
    let result = {
        let mut emit = |value: &Value| emitted.push(value.clone());
        let mut session = Session::new(
            &mut process,
            &mut journal,
            &mut emit,
            &options,
            Instant::now() + options.total,
        );
        session.preflight(
            &fixture.request,
            &[fixture.request.checkout_root.join("peer-case.txt")],
        )
    };
    assert!(
        process.stop(options.teardown),
        "{case}: process tree not stopped"
    );
    assert_eq!(process.active(), Ok(0), "{case}: active process remained");
    drop(journal);

    assert_eq!(
        fs::read(fixture.request.checkout_root.join("task.json")).unwrap(),
        request::TASK,
        "{case}: fixture task changed"
    );
    assert_eq!(
        fs::read_to_string(fixture.request.checkout_root.join("peer-case.txt")).unwrap(),
        "WF-01\n",
        "{case}: fixture selector changed"
    );
    let trace = fs::read_to_string(trace_path)
        .unwrap()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    let journal_text = fs::read_to_string(fixture.request.run_dir.join("journal.jsonl")).unwrap();
    let events = journal_text
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    let mut evidence = String::new();
    evidence.push_str(&fs::read_to_string(&fixture.input).unwrap());
    evidence
        .push_str(&fs::read_to_string(fixture.request.checkout_root.join("task.json")).unwrap());
    for name in ["request.json", "task.json", "inputs.json", "journal.jsonl"] {
        let path = fixture.request.run_dir.join(name);
        if path.exists() {
            evidence.push_str(&fs::read_to_string(path).unwrap());
        }
    }
    Observation {
        result,
        trace,
        events,
        evidence,
    }
}

fn assert_no_work(observation: &Observation, case: &str) {
    assert_eq!(
        observation
            .trace
            .first()
            .and_then(|message| message.get("method"))
            .and_then(Value::as_str),
        Some("initialize"),
        "{case}: mandatory trace was empty or did not start at initialize"
    );
    assert!(
        !observation.trace.iter().any(|message| matches!(
            message.get("method").and_then(Value::as_str),
            Some("thread/start" | "turn/start")
        )),
        "{case}: preflight started work"
    );
}

#[test]
fn server_requests_are_denied_with_the_captured_response_and_never_granted() {
    let approval = run("approval-request");
    assert_eq!(
        approval.result,
        Err("approval_required".to_owned()),
        "PE-01"
    );
    assert_eq!(
        approval.trace.last(),
        Some(&json!({"id":"server-approval","result":{"decision":"cancel"}})),
        "PE-01"
    );
    assert_no_work(&approval, "PE-01");
    assert!(
        !approval.evidence.contains("PRIVATE_APPROVAL_REQUEST"),
        "PE-01"
    );

    let unsupported = run("unsupported-request");
    assert_eq!(
        unsupported.result,
        Err("unsupported_request".to_owned()),
        "PE-02"
    );
    assert_eq!(
        unsupported.trace.last(),
        Some(&json!({"id":77,"error":{"code":-32601,"message":"Method not supported"}})),
        "PE-02"
    );
    assert_no_work(&unsupported, "PE-02");
    assert!(
        !unsupported.evidence.contains("PRIVATE_UNSUPPORTED_REQUEST"),
        "PE-02"
    );

    let malformed = run("malformed-request-id");
    assert_eq!(malformed.result, Err("protocol_error".to_owned()), "PE-03");
    assert_eq!(
        malformed.trace.len(),
        1,
        "PE-03: malformed ID received a response"
    );
    assert_no_work(&malformed, "PE-03");
}

#[test]
fn stderr_is_drained_as_omitted_content_without_persisting_private_bytes() {
    let observation = run("stderr");
    assert_eq!(observation.result, Ok(()), "PE-04");
    assert_no_work(&observation, "PE-04");
    let stderr_events: Vec<_> = observation
        .events
        .iter()
        .filter(|event| event["data"]["stream"] == "stderr")
        .collect();
    assert!(!stderr_events.is_empty(), "PE-04");
    assert!(
        stderr_events
            .iter()
            .all(|event| event["data"]["content"] == "omitted"),
        "PE-04"
    );
    let observed_bytes: u64 = stderr_events
        .iter()
        .map(|event| event["data"]["bytes"].as_u64().expect("PE-04 byte count"))
        .sum();
    assert_eq!(
        observed_bytes,
        b"PRIVATE_STDERR_SENTINEL\n".len() as u64,
        "PE-04"
    );
    assert!(
        stderr_events.iter().all(|event| event["data"]["sha256"]
            .as_str()
            .is_some_and(|s| s.len() == 64)),
        "PE-04"
    );
    assert!(
        !observation.evidence.contains("PRIVATE_STDERR_SENTINEL"),
        "PE-04"
    );
}

#[test]
fn feature_pagination_enforces_page_size_repeated_cursor_and_page_count_bounds() {
    for (case, expected, id) in [
        ("feature-overflow", "protocol_error", "PE-05"),
        ("feature-repeat-cursor", "profile_unqualified", "PE-06"),
        ("feature-ten-pages", "profile_unqualified", "PE-09"),
    ] {
        let observation = run(case);
        assert_eq!(observation.result, Err(expected.to_owned()), "{id}");
        assert_no_work(&observation, id);
    }
}

#[test]
fn unavailable_or_invalid_rate_limit_measurements_are_explicit_and_sanitized() {
    for (case, private, id) in [
        ("rate-limit-rpc-error", "PRIVATE_RATE_LIMIT_ERROR", "PE-07"),
        ("rate-limit-negative", "", "PE-08"),
    ] {
        let observation = run(case);
        assert_eq!(observation.result, Ok(()), "{id}");
        assert_no_work(&observation, id);
        let measurements: Vec<_> = observation
            .events
            .iter()
            .filter_map(|event| event["data"].get("rate_limits"))
            .collect();
        assert_eq!(measurements, [&json!("not_measured")], "{id}");
        if !private.is_empty() {
            assert!(!observation.evidence.contains(private), "{id}");
        }
    }
}
