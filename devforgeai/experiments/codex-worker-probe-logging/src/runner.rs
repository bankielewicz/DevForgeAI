use crate::{
    journal::Journal,
    process_windows::OwnedProcess,
    protocol::Session,
    request::{self, Result},
};
use serde_json::{Value, json};
use std::{
    path::Path,
    sync::{Arc, atomic::AtomicU8},
    time::{Duration, Instant},
};
pub struct Options {
    pub total: Duration,
    pub rpc: Duration,
    pub grace: Duration,
    pub teardown: Duration,
    pub control: Arc<AtomicU8>,
    pub fail_write_after: Option<u64>,
    pub uncertain_cleanup: bool,
}
impl Default for Options {
    fn default() -> Self {
        Self {
            total: Duration::from_secs(120),
            rpc: Duration::from_secs(10),
            grace: Duration::from_secs(5),
            teardown: Duration::from_secs(5),
            control: Arc::new(AtomicU8::new(0)),
            fail_write_after: None,
            uncertain_cleanup: false,
        }
    }
}
pub fn run(input: &Path, options: Options, emit: &mut dyn FnMut(&Value)) -> Result<(i32, Value)> {
    execute(input, options, emit, false)
}
pub fn preflight(
    input: &Path,
    options: Options,
    emit: &mut dyn FnMut(&Value),
) -> Result<(i32, Value)> {
    execute(input, options, emit, true)
}
fn execute(
    input: &Path,
    options: Options,
    emit: &mut dyn FnMut(&Value),
    preflight: bool,
) -> Result<(i32, Value)> {
    execute_with_final_check(input, options, emit, preflight, &mut verify_before_spawn)
}

// Public entry points always use this compiled verification. Only private unit tests
// can replace the checker to exercise drift at the real runner's spawn boundary.
fn verify_before_spawn(r: &request::Request, preflight: bool) -> Result<()> {
    if r.native_v2() {
        if preflight {
            r.verify_preflight_review().map(|_| ())
        } else {
            r.verify_review()
        }
        .map_err(|_| "profile_unqualified".to_owned())?;
        crate::native_identity::verify(&r.worker_executable, &r.worker_sha256, &r.adapter)?;
    }
    crate::logging::load(r)?;
    Ok(())
}

fn execute_with_final_check(
    input: &Path,
    options: Options,
    emit: &mut dyn FnMut(&Value),
    preflight: bool,
    final_check: &mut dyn FnMut(&request::Request, bool) -> Result<()>,
) -> Result<(i32, Value)> {
    let r = request::validate(input)?;
    if preflight && (!r.native_v2() || r.adapter != "codex-0.154.0-stdio") {
        return Err("invalid_request".into());
    }
    let inventory = r.fixture_inventory()?;
    let mut journal = Journal::create(&r)?;
    if let Some(n) = options.fail_write_after {
        journal.inject_write_failure_after(n);
    }
    emit(&journal.append("admitted",json!({"project_id":r.project_id,"checkout_id":r.checkout_id,"work_id":r.work_id,"candidate_sha256":r.candidate_sha256}))?);
    let mut reason = "completed".to_string();
    let mut thread = None;
    let mut turn = None;
    let mut usage = Value::Null;
    let mut exit = None;
    let mut stopped = Some(true);
    // Inspection may observe an unqualified review, but can never dispatch work.
    let qualified = if r.adapter == "peer" {
        Ok(())
    } else {
        if std::env::vars_os().any(|(key, _)| {
            let key = key.to_string_lossy().to_ascii_uppercase();
            key.contains("API_KEY") || key.contains("ACCESS_TOKEN") || key == "OPENAI_BASE_URL"
        }) {
            Err("profile_unqualified".into())
        } else {
            if preflight {
                r.verify_preflight_review().map(|_| ())
            } else {
                r.verify_review()
            }
            .map_err(|_| "profile_unqualified".to_string())
        }
    };
    if let Err(e) = qualified {
        reason = e;
    } else {
        let deadline = Instant::now() + options.total;
        if r.native_v2() {
            request::resolve(&r.checkout_root)?;
            crate::native_identity::verify(&r.worker_executable, &r.worker_sha256, &r.adapter)?;
            emit(&journal.append(
                "worker_event",
                json!({"method":"native_identity_rechecked","worker_sha256":r.worker_sha256}),
            )?);
        }
        emit(&journal.append(
            "spawn_intent",
            json!({"worker_sha256":r.worker_sha256,"adapter":r.adapter}),
        )?);
        let args = if r.adapter == "peer" {
            vec![
                "--fixture-root".into(),
                r.checkout_root.to_string_lossy().into_owned(),
            ]
        } else if r.native_v2() {
            let profile = r.profile()?.ok_or("invalid_profile")?;
            crate::launch_policy::args(
                &r.adapter,
                r.schema_version,
                profile
                    .launch_policy_id
                    .as_deref()
                    .ok_or("invalid_profile")?,
                profile
                    .launch_policy_sha256
                    .as_deref()
                    .ok_or("invalid_profile")?,
            )?
        } else {
            vec!["app-server".into(), "--listen".into(), "stdio://".into()]
        };
        journal.log_launch(&args, r.native_v2());
        // No journal callback or argument construction may intervene after this check.
        let spawn = final_check(&r, preflight).and_then(|()| {
            OwnedProcess::spawn(&r.worker_executable, &args, &r.checkout_root)
                .map_err(|_| "spawn_failed".to_owned())
        });
        match spawn {
            Err(e) if e == "invalid_worker" => return Err(e),
            Err(e) => reason = e,
            Ok(mut process) => {
                let mut pre_stop_exit_code = None;
                let result =
                    journal.append("server_started", json!({"pid_observation":process.pid}));
                if let Ok(e) = result {
                    emit(&e);
                } else {
                    reason = "evidence_write_failed".into();
                }
                if reason == "completed" {
                    let mut session =
                        Session::new(&mut process, &mut journal, emit, &options, deadline);
                    let result = if preflight {
                        session
                            .source_review(crate::diagnostic::SourceBoundary::PostSpawn, || {
                                r.verify_preflight_review()
                            })
                            .and_then(|sources| session.preflight(&r, &sources))
                            .and_then(|()| {
                                session.source_review(
                                    crate::diagnostic::SourceBoundary::PostPreflight,
                                    || r.verify_preflight_review().map(|_| ()),
                                )
                            })
                    } else {
                        session.dispatch(&r)
                    };
                    if let Err(e) = result {
                        pre_stop_exit_code = session.process.exit_code();
                        reason = e;
                        if session
                            .record("stop_requested", json!({"reason":reason}))
                            .is_err()
                        {
                            reason = "evidence_write_failed".into();
                        }
                        if pre_stop_exit_code.is_some() {
                            session
                                .process
                                .drain_until(Instant::now() + options.teardown);
                        }
                        session.interrupt();
                    } else if preflight {
                        reason = "preflight_checked".into();
                    }
                    thread = session.thread;
                    turn = session.turn;
                    usage = session.usage;
                } else {
                    process.close_input();
                    process.wait_stopped(options.grace);
                }
                if reason == "completed" || reason == "preflight_checked" {
                    process.close_input();
                    process.wait_stopped(options.grace);
                }
                pre_stop_exit_code = pre_stop_exit_code.or_else(|| process.exit_code());
                journal.log_input_closed();
                let actual_stopped = process.stop(options.teardown);
                stopped = if actual_stopped && !options.uncertain_cleanup {
                    Some(true)
                } else {
                    None
                };
                exit = process.exit_code();
                if (reason == "completed" || reason == "preflight_checked") && exit != Some(0) {
                    reason = "worker_failed".into();
                }
                let capture = process.capture();
                if reason == "completed" || reason == "preflight_checked" {
                    if let Some(error) = process.stream_error() {
                        reason = error.into();
                    } else if !capture.drain_complete {
                        reason = "capture_incomplete".into();
                    }
                }
                journal.log_capture(
                    &capture,
                    &process.chunks(),
                    pre_stop_exit_code,
                    exit,
                    actual_stopped,
                );
                match journal.append(
                    "process_exit",
                    json!({"worker_exit_code":exit,"tree_stopped":stopped,"observed_before_stop":pre_stop_exit_code.is_some(),"pre_stop_exit_code":pre_stop_exit_code,"capture":capture}),
                ) {
                    Ok(e) => emit(&e),
                    Err(_) => reason = "evidence_write_failed".into(),
                }
            }
        }
    }
    if journal
        .finish_diagnostics()
        .and_then(|data| journal.append("worker_event", data))
        .map(|e| emit(&e))
        .is_err()
    {
        reason = "evidence_write_failed".into();
    }
    let unchanged = r
        .fixture_inventory()
        .map(|i| i == inventory)
        .unwrap_or(false);
    if !unchanged {
        reason = "fixture_changed".into();
    }
    let oracle = if reason == "completed" {
        "match"
    } else if reason == "oracle_mismatch" {
        "mismatch"
    } else {
        "not_evaluated"
    };
    let (code, outcome) = if stopped != Some(true) {
        (7, "cleanup_uncertain")
    } else {
        match reason.as_str() {
            "completed" => (0, "completed"),
            "preflight_checked" => (0, "preflight_checked"),
            "profile_unqualified" | "rate_limit_exhausted" => (3, "blocked"),
            "user_cancel" => (5, "cancelled"),
            "deadline" => (6, "timed_out"),
            _ => (4, "failed"),
        }
    };
    let terminal = json!({"outcome":outcome,"reason":if code==7 {"cleanup_unknown"} else {&reason},"thread_id":thread,"turn_id":turn,"worker_exit_code":exit,"tree_stopped":stopped,"fixture_unchanged":unchanged,"oracle":oracle,"usage":usage,"open_work":[r.work_id]});
    match journal.append("terminal", terminal.clone()) {
        Ok(e) => {
            emit(&e);
            Ok((code, terminal))
        }
        Err(_) => Ok((
            if code == 7 { 7 } else { 4 },
            json!({"outcome":if code==7 {"cleanup_uncertain"}else{"failed"},"reason":"evidence_write_failed","tree_stopped":stopped}),
        )),
    }
}

#[cfg(test)]
#[path = "../tests/support/final_source_check_cases.rs"]
mod final_source_check_cases;
