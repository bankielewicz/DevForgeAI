mod support;

use devforgeai_codex_worker_probe::{
    journal::Journal, process_windows::OwnedProcess, protocol::Session, runner::Options,
};
use serde_json::{Value, json};
use std::{
    fs,
    path::PathBuf,
    sync::atomic::Ordering,
    time::{Duration, Instant},
};
use windows_sys::Win32::{
    Foundation::CloseHandle,
    System::Threading::{
        OpenProcess, PROCESS_QUERY_LIMITED_INFORMATION, QueryFullProcessImageNameW,
    },
};

struct Observation {
    result: Result<(), String>,
    trace: Vec<Value>,
    events: Vec<Value>,
    evidence: String,
    startup_immediate: (u32, u32, Option<u32>),
    startup_after_5ms: (u32, u32, Option<u32>),
    startup_immediate_images: Vec<(u32, String)>,
    startup_after_5ms_images: Vec<(u32, String)>,
}

fn process_images(process: &OwnedProcess) -> Vec<(u32, String)> {
    process
        .process_ids()
        .unwrap()
        .into_iter()
        .map(|pid| {
            // SAFETY: the handle is opened read-only for this observed PID and
            // is closed in all successful OpenProcess paths.
            unsafe {
                let handle = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid);
                if handle.is_null() {
                    return (pid, "<open-failed>".to_owned());
                }
                let mut buffer = vec![0_u16; 32_768];
                let mut length = buffer.len() as u32;
                let ok = QueryFullProcessImageNameW(handle, 0, buffer.as_mut_ptr(), &mut length);
                CloseHandle(handle);
                if ok == 0 {
                    (pid, "<query-failed>".to_owned())
                } else {
                    buffer.truncate(length as usize);
                    (pid, String::from_utf16_lossy(&buffer))
                }
            }
        })
        .collect()
}

fn run(case: &str, rpc: Duration, cancelled: bool) -> Observation {
    // Keep the qualified immutable base fixture independent from the profile
    // peer's synthetic response selector.
    let fixture = support::Fixture::new("WF-01");
    let trace_path = fixture.root.path().join("profile-peer-trace.jsonl");
    let exe = PathBuf::from(env!("CARGO_BIN_EXE_profile-peer"));
    let args = vec![
        "--case".to_owned(),
        case.to_owned(),
        "--trace".to_owned(),
        trace_path.to_string_lossy().into_owned(),
        "--fixture-root".to_owned(),
        fixture.request.checkout_root.to_string_lossy().into_owned(),
    ];
    let mut process = OwnedProcess::spawn(&exe, &args, &fixture.request.checkout_root).unwrap();
    let startup_immediate = (
        process.active().unwrap(),
        process.created_processes().unwrap(),
        process.exit_code(),
    );
    let startup_immediate_images = process_images(&process);
    std::thread::sleep(Duration::from_millis(5));
    let startup_after_5ms = (
        process.active().unwrap(),
        process.created_processes().unwrap(),
        process.exit_code(),
    );
    let startup_after_5ms_images = process_images(&process);
    let options = Options {
        total: Duration::from_secs(3),
        rpc,
        teardown: Duration::from_secs(1),
        ..Default::default()
    };
    if cancelled {
        options.control.store(1, Ordering::SeqCst);
    }
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

    let trace = fs::read_to_string(&trace_path)
        .unwrap_or_default()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    let journal_text =
        fs::read_to_string(fixture.request.run_dir.join("journal.jsonl")).unwrap_or_default();
    let events = journal_text
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    let mut evidence = String::new();
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
        startup_immediate,
        startup_after_5ms,
        startup_immediate_images,
        startup_after_5ms_images,
    }
}

fn normal(case: &str) -> Observation {
    run(case, Duration::from_millis(500), false)
}

fn assert_rejected(case: &str, expected: &str, target_method: &str) {
    let observation = normal(case);
    assert_eq!(
        observation.result,
        Err(expected.to_owned()),
        "{case}: startup immediate={:?} {:?}, after_5ms={:?} {:?}",
        observation.startup_immediate,
        observation.startup_immediate_images,
        observation.startup_after_5ms,
        observation.startup_after_5ms_images
    );
    assert!(
        observation
            .trace
            .iter()
            .any(|request| request["method"] == target_method),
        "{case}: rejection happened before targeted {target_method} observation"
    );
    assert!(
        !observation.trace.iter().any(|request| matches!(
            request["method"].as_str(),
            Some("thread/start" | "turn/start")
        )),
        "{case}: preflight started work"
    );
}

#[test]
fn preflight_uses_the_exact_read_only_inventory_trace_and_starts_no_work() {
    let observation = normal("ok");
    assert_eq!(
        observation.result,
        Ok(()),
        "startup immediate={:?} {:?}, after_5ms={:?} {:?}",
        observation.startup_immediate,
        observation.startup_immediate_images,
        observation.startup_after_5ms,
        observation.startup_after_5ms_images
    );
    assert_eq!(observation.startup_after_5ms, (1, 1, None));
    let methods: Vec<_> = observation
        .trace
        .iter()
        .map(|request| request["method"].as_str().unwrap())
        .collect();
    assert_eq!(
        methods,
        [
            "initialize",
            "initialized",
            "config/read",
            "configRequirements/read",
            "experimentalFeature/list",
            "hooks/list",
            "plugin/list",
            "app/installed",
            "mcpServerStatus/list",
            "account/read",
            "model/list",
            "account/rateLimits/read",
        ]
    );
    assert!(!methods.iter().any(|method| method.starts_with("thread/")));
    assert!(!methods.iter().any(|method| method.starts_with("turn/")));
}

#[test]
fn preflight_rejects_active_or_conflicting_effective_config() {
    assert_rejected("active-config", "profile_unqualified", "config/read");
    assert_rejected(
        "requirement-conflict",
        "profile_unqualified",
        "configRequirements/read",
    );
}

#[test]
fn preflight_requires_every_disabled_feature_and_complete_pagination() {
    assert_rejected(
        "active-feature",
        "profile_unqualified",
        "experimentalFeature/list",
    );
    assert_rejected(
        "missing-feature",
        "profile_unqualified",
        "experimentalFeature/list",
    );
    assert_rejected(
        "feature-bad-cursor",
        "protocol_error",
        "experimentalFeature/list",
    );
    assert_rejected(
        "feature-loop",
        "profile_unqualified",
        "experimentalFeature/list",
    );
}

#[test]
fn preflight_accepts_schema_valid_omitted_final_cursors() {
    assert_eq!(normal("feature-omitted-cursor").result, Ok(()));
    assert_eq!(normal("mcp-omitted-cursor").result, Ok(()));
}

#[test]
fn preflight_rejects_active_hooks_plugins_apps_and_mcp_servers() {
    for case in [
        "active-hook",
        "hook-error",
        "active-plugin",
        "plugin-error",
        "active-app",
        "active-mcp",
        "mcp-loop",
    ] {
        let target = match case {
            "active-hook" | "hook-error" => "hooks/list",
            "active-plugin" | "plugin-error" => "plugin/list",
            "active-app" => "app/installed",
            _ => "mcpServerStatus/list",
        };
        assert_rejected(case, "profile_unqualified", target);
    }
}

#[test]
fn preflight_maps_rpc_failure_timeout_cancellation_and_work_notifications() {
    assert_rejected("rpc-error", "profile_unqualified", "config/read");
    let timeout = run("timeout", Duration::from_millis(50), false);
    assert_eq!(timeout.result, Err("deadline".to_owned()));
    let cancelled = run("cancelled", Duration::from_millis(500), true);
    assert_eq!(cancelled.result, Err("user_cancel".to_owned()));
    assert_rejected("notification", "protocol_error", "initialize");
}

#[test]
fn rate_limit_measurement_is_explicit_when_unavailable_and_blocks_when_exhausted() {
    for case in ["rate-limit-missing", "rate-limit-malformed"] {
        let observation = normal(case);
        assert_eq!(observation.result, Ok(()), "{case}");
        let rate_limit_events: Vec<_> = observation
            .events
            .iter()
            .filter(|event| event["kind"] == "worker_event")
            .filter_map(|event| event["data"].get("rate_limits"))
            .collect();
        assert_eq!(
            rate_limit_events,
            [&json!("not_measured")],
            "{case}: inability to measure must be explicit and cannot be an invented number"
        );
        assert!(
            !observation.trace.iter().any(|request| matches!(
                request["method"].as_str(),
                Some("thread/start" | "turn/start")
            )),
            "{case}: preflight started work"
        );
    }

    assert_rejected(
        "rate-limit-exhausted",
        "rate_limit_exhausted",
        "account/rateLimits/read",
    );
}

#[test]
fn profile_projection_does_not_persist_private_response_fields() {
    let observation = normal("secret-plugin");
    assert_eq!(observation.result, Ok(()));
    assert!(!observation.evidence.contains("PRIVATE_PLUGIN_SENTINEL"));
    assert!(!observation.evidence.contains("PRIVATE_LAYER_SECRET"));
    assert!(!observation.evidence.contains("PRIVATE_EMAIL"));
    assert!(!observation.evidence.contains("PRIVATE_RPC_MESSAGE"));
    let config = normal("secret-config");
    assert_eq!(config.result, Ok(()));
    assert!(!config.evidence.contains("PRIVATE_CONFIG_SENTINEL"));
}

#[test]
fn preflight_rejects_a_transient_descendant_even_after_it_exits() {
    assert_rejected("transient-descendant", "profile_unqualified", "initialize");
}
