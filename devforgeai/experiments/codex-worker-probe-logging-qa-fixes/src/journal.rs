use crate::logging::{self, Level, Phase, Record};
use crate::request::{self, Request, Result};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::{
    fs::{self, File, OpenOptions},
    io::Write,
    path::Path,
    time::{Instant, SystemTime, UNIX_EPOCH},
};

pub const KINDS: &[&str] = &[
    "admitted",
    "spawn_intent",
    "server_started",
    "profile_checked",
    "thread_bound",
    "turn_intent",
    "turn_bound",
    "worker_event",
    "stop_requested",
    "process_exit",
    "terminal",
];
#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Event {
    pub schema_version: u32,
    pub run_id: String,
    pub seq: u64,
    pub observed_at: String,
    pub elapsed_ms: u64,
    pub kind: String,
    pub data: Value,
}
#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
struct Inputs {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    capture_schema: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    diagnostics: Option<logging::Binding>,
    request_sha256: String,
    fixture: Vec<(String, String)>,
    worker_sha256: String,
    profile_sha256: Option<String>,
}

pub struct Journal {
    diagnostics: logging::Sink,
    file: File,
    run_id: String,
    seq: u64,
    start: Instant,
    terminal: bool,
    fail_after: Option<u64>,
}
pub fn write_new(path: &Path, bytes: &[u8]) -> Result<()> {
    request::resolve(path.parent().ok_or("invalid_path")?)?;
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(path)
        .map_err(|_| "evidence_write_failed")?;
    file.write_all(bytes)
        .and_then(|()| file.sync_all())
        .map_err(|_| "evidence_write_failed".into())
}

fn utc() -> String {
    let seconds = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    let days = (seconds / 86400) as i64 + 719468;
    let era = days / 146097;
    let doe = days - era * 146097;
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = mp + if mp < 10 { 3 } else { -9 };
    let y = yoe + era * 400 + i64::from(m <= 2);
    format!(
        "{y:04}-{m:02}-{d:02}T{:02}:{:02}:{:02}Z",
        seconds / 3600 % 24,
        seconds / 60 % 60,
        seconds % 60
    )
}

impl Journal {
    pub fn create(request: &Request) -> Result<Self> {
        let config = logging::load(request)?;
        request::resolve(request.run_dir.parent().ok_or("invalid_path")?)?;
        fs::create_dir(&request.run_dir).map_err(|e| {
            if e.kind() == std::io::ErrorKind::AlreadyExists {
                "run_exists"
            } else {
                "evidence_write_failed"
            }
        })?;
        let bytes = serde_json::to_vec(request).map_err(|_| "evidence_write_failed")?;
        write_new(&request.run_dir.join("request.json"), &bytes)?;
        write_new(
            &request.run_dir.join("task.json"),
            &request::bounded_read(&request.checkout_root.join("task.json"), 65536)?,
        )?;
        let profile_sha256 = if let Some(profile) = request.profile()?
            && let Ok(review) = request::bounded_read(&profile.review_ref, 65536)
        {
            write_new(&request.run_dir.join("profile-review.json"), &review)?;
            Some(request::digest(&review))
        } else {
            None
        };
        let diagnostics = if let Some((config, bytes)) = &config {
            write_new(&request.run_dir.join("diagnostics-config.json"), bytes)?;
            Some(logging::Binding {
                level: config.level,
                sha256: request::digest(bytes),
            })
        } else {
            None
        };
        let level = diagnostics.as_ref().map_or(Level::Off, |d| d.level);
        let inputs = Inputs {
            capture_schema: Some(1),
            diagnostics,
            request_sha256: request::digest(&bytes),
            fixture: request.fixture_inventory()?,
            worker_sha256: request.worker_sha256.clone(),
            profile_sha256,
        };
        write_new(
            &request.run_dir.join("inputs.json"),
            &serde_json::to_vec(&inputs).map_err(|_| "evidence_write_failed")?,
        )?;
        let file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(request.run_dir.join("journal.jsonl"))
            .map_err(|_| "evidence_write_failed")?;
        Ok(Self {
            diagnostics: logging::Sink::new(&request.run_dir, level),
            file,
            run_id: request.run_id.clone(),
            seq: 0,
            start: Instant::now(),
            terminal: false,
            fail_after: None,
        })
    }
    /// Explicit library-only failure injection; never accepted from a production request.
    pub fn inject_write_failure_after(&mut self, seq: u64) {
        self.fail_after = Some(seq);
    }
    pub fn append(&mut self, kind: &str, data: Value) -> Result<Value> {
        if self.terminal || !KINDS.contains(&kind) || self.fail_after.is_some_and(|n| self.seq >= n)
        {
            return Err("evidence_write_failed".into());
        }
        let value = serde_json::to_value(Event {
            schema_version: 1,
            run_id: self.run_id.clone(),
            seq: self.seq + 1,
            observed_at: utc(),
            elapsed_ms: self.start.elapsed().as_millis() as u64,
            kind: kind.into(),
            data,
        })
        .map_err(|_| "evidence_write_failed")?;
        let mut bytes = serde_json::to_vec(&value).map_err(|_| "evidence_write_failed")?;
        bytes.push(b'\n');
        self.file
            .write_all(&bytes)
            .and_then(|()| self.file.sync_all())
            .map_err(|_| "evidence_write_failed")?;
        self.seq += 1;
        self.terminal = kind == "terminal";
        let phase = match kind {
            "admitted" => Some(Phase::Admitted),
            "spawn_intent" => Some(Phase::SpawnIntent),
            "server_started" => Some(Phase::ServerStarted),
            "stop_requested" => Some(Phase::StopRequested),
            _ => None,
        };
        if let Some(phase) = phase {
            self.diagnostics.record(
                Level::Minimal,
                Record::Phase {
                    phase,
                    elapsed_ms: self.start.elapsed().as_millis() as u64,
                },
            );
        }
        if kind == "server_started"
            && let Some(pid) = value["data"]["pid_observation"]
                .as_u64()
                .and_then(|p| u32::try_from(p).ok())
        {
            self.diagnostics.record(
                Level::Minimal,
                Record::Spawn {
                    pid,
                    elapsed_ms: self.start.elapsed().as_millis() as u64,
                },
            );
        }
        Ok(value)
    }
    pub fn log_launch(&mut self, args: &[String], native: bool) {
        self.diagnostics.record(
            Level::Verbose,
            Record::Launch {
                arguments: args.len(),
                argv_sha256: request::digest(&serde_json::to_vec(args).expect("argument vector")),
                policy_sha256: native.then(crate::launch_policy::digest),
            },
        );
    }
    pub fn log_rpc(&mut self, method: &str, duration: std::time::Duration, failed: bool) {
        self.diagnostics.record(
            Level::Verbose,
            Record::Rpc {
                rpc: logging::Rpc::from_method(method),
                elapsed_ms: duration.as_millis() as u64,
                failed,
            },
        );
    }
    pub fn log_phase(&mut self, phase: Phase) {
        self.diagnostics.record(
            Level::Verbose,
            Record::Phase {
                phase,
                elapsed_ms: self.start.elapsed().as_millis() as u64,
            },
        );
    }
    pub fn log_input_closed(&mut self) {
        self.log_phase(Phase::InputClosed);
    }
    pub fn log_capture(
        &mut self,
        capture: &crate::capture::Capture,
        chunks: &[(crate::capture::Stream, crate::capture::Chunk)],
        pre: Option<u32>,
        post: Option<u32>,
        stopped: bool,
    ) {
        self.diagnostics.record(
            Level::Minimal,
            Record::Exit {
                capture,
                pre_stop_exit_code: pre,
                post_stop_exit_code: post,
                tree_stopped: stopped,
            },
        );
        for (stream, chunk) in chunks {
            self.diagnostics.record(
                Level::Debug,
                Record::Chunk {
                    stream: *stream,
                    chunk,
                },
            );
        }
    }
    pub fn finish_diagnostics(&mut self) -> Result<Value> {
        Ok(json!({"method":"diagnostics_status","status":self.diagnostics.finish()}))
    }
}

pub fn inspect(dir: &Path, after: u64, limit: usize) -> Result<Value> {
    if !(1..=100).contains(&limit) {
        return Err("invalid_cursor".into());
    }
    let dir = request::resolve(dir).map_err(|_| "evidence_incomplete")?;
    let read = |name: &str, size| {
        request::bounded_read(&dir.join(name), size).map_err(|_| "evidence_incomplete".to_string())
    };
    let bytes = read("request.json", 65536)?;
    let request: Request = serde_json::from_slice(&bytes).map_err(|_| "evidence_corrupt")?;
    let inputs: Inputs =
        serde_json::from_slice(&read("inputs.json", 65536)?).map_err(|_| "evidence_corrupt")?;
    if inputs.capture_schema.is_some_and(|v| v != 1) {
        return Err("evidence_corrupt".into());
    }
    if request.schema_version == 3 && inputs.capture_schema != Some(1) {
        return Err("evidence_corrupt".into());
    }
    if let Some(binding) = &inputs.diagnostics {
        let bytes = read("diagnostics-config.json", logging::MAX_CONFIG)?;
        let config: logging::Config =
            serde_json::from_slice(&bytes).map_err(|_| "evidence_corrupt")?;
        if request.schema_version != 3
            || config.schema_version != 1
            || config.level != binding.level
            || request::digest(&bytes) != binding.sha256
            || request.diagnostics_sha256.as_deref() != Some(binding.sha256.as_str())
        {
            return Err("evidence_corrupt".into());
        }
    } else if request.schema_version == 3 {
        return Err("evidence_corrupt".into());
    }
    if request::digest(&bytes) != inputs.request_sha256
        || request.run_dir != dir
        || request::digest(&read("task.json", 65536)?) != request.candidate_sha256
        || inputs.worker_sha256 != request.worker_sha256
    {
        return Err("evidence_corrupt".into());
    }
    if let Some(hash) = inputs.profile_sha256
        && request::digest(&read("profile-review.json", 65536)?) != hash
    {
        return Err("evidence_corrupt".into());
    }
    // A missing referenced fixture is incomplete; a changed fixture is retained as an observed failure.
    request::resolve(&request.checkout_root.join("task.json"))
        .map_err(|_| "evidence_incomplete")?;
    request::resolve(&request.worker_executable).map_err(|_| "evidence_incomplete")?;
    if let Some(profile) = request.profile().map_err(|_| "evidence_corrupt")? {
        request::resolve(&profile.review_ref).map_err(|_| "evidence_incomplete")?;
    }
    let bytes = read("journal.jsonl", 32 * 1024 * 1024)?;
    let prefix = bytes.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1);
    let mut events = Vec::new();
    let mut seq = 0;
    let mut elapsed = 0;
    let mut state = "admitted".to_string();
    let mut terminal = false;
    let mut observed_result = None;
    let mut preflight_stages = std::collections::HashSet::new();
    let mut profile_checked = false;
    let mut identity_rechecked = false;
    let mut work_started = false;
    let mut spawned = false;
    let mut exit_summary = None;
    let mut diagnostics_status = None;
    for line in bytes[..prefix].split_inclusive(|b| *b == b'\n') {
        let e: Event = serde_json::from_slice(line).map_err(|_| "evidence_corrupt")?;
        if e.schema_version != 1
            || e.run_id != request.run_id
            || e.seq != seq + 1
            || e.elapsed_ms < elapsed
            || !KINDS.contains(&e.kind.as_str())
            || terminal
            || !e.observed_at.ends_with('Z')
        {
            return Err("evidence_corrupt".into());
        }
        seq = e.seq;
        elapsed = e.elapsed_ms;
        profile_checked |= e.kind == "profile_checked";
        work_started |= matches!(
            e.kind.as_str(),
            "thread_bound" | "turn_intent" | "turn_bound"
        );
        spawned |= e.kind == "server_started";
        if inputs.capture_schema.is_some() && e.kind == "process_exit" {
            let capture: crate::capture::Capture =
                serde_json::from_value(e.data["capture"].clone())
                    .map_err(|_| "evidence_corrupt")?;
            capture.validate()?;
            let _: Option<u32> = serde_json::from_value(e.data["pre_stop_exit_code"].clone())
                .map_err(|_| "evidence_corrupt")?;
            let worker_exit_code: Option<u32> = serde_json::from_value(
                e.data
                    .get("worker_exit_code")
                    .ok_or("evidence_corrupt")?
                    .clone(),
            )
            .map_err(|_| "evidence_corrupt")?;
            if exit_summary.is_some()
                || !spawned
                || !e.data["observed_before_stop"].is_boolean()
                || e.data.get("pre_stop_exit_code").is_none()
                || e.data["observed_before_stop"] != e.data["pre_stop_exit_code"].is_u64()
            {
                return Err("evidence_corrupt".into());
            }
            exit_summary = Some((capture, worker_exit_code));
        }
        if e.kind == "worker_event" {
            if e.data["method"] == "diagnostics_status" {
                if diagnostics_status.is_some() {
                    return Err("evidence_corrupt".into());
                }
                diagnostics_status = Some(
                    serde_json::from_value::<logging::Status>(e.data["status"].clone())
                        .map_err(|_| "evidence_corrupt")?,
                );
            }
            identity_rechecked |= e.data["method"] == "native_identity_rechecked";
            if let Some(stage) = e.data["preflight"].as_str() {
                preflight_stages.insert(stage.to_owned());
            }
        }
        if e.kind == "spawn_intent" {
            state = "interrupted_unknown".into();
        }
        if e.kind == "worker_event" && e.data["method"] == "final_result" {
            if observed_result.is_some() {
                return Err("evidence_corrupt".into());
            }
            observed_result = Some(e.data.clone());
        }
        if e.kind == "terminal" {
            if inputs.capture_schema.is_some() {
                if spawned && exit_summary.is_none() {
                    return Err("evidence_corrupt".into());
                }
                if let Some(status) = &diagnostics_status {
                    logging::inspect(&dir, inputs.diagnostics.as_ref(), status)?;
                } else if spawned || request.schema_version == 3 {
                    return Err("evidence_incomplete".into());
                }
            }
            let outcome = e.data["outcome"].as_str().ok_or("evidence_corrupt")?;
            if ![
                "completed",
                "preflight_checked",
                "blocked",
                "failed",
                "cancelled",
                "timed_out",
                "cleanup_uncertain",
            ]
            .contains(&outcome)
                || e.data["open_work"] != json!([request.work_id])
            {
                return Err("evidence_corrupt".into());
            }
            if inputs.capture_schema.is_some()
                && matches!(outcome, "completed" | "preflight_checked")
            {
                let (capture, worker_exit_code) =
                    exit_summary.as_ref().ok_or("evidence_corrupt")?;
                // validate() already checks EOF and reader errors when drain_complete is true.
                // A sound failed run may retain incomplete capture or an unobserved exit.
                if !capture.drain_complete
                    || capture.stdout.byte_overflow
                    || capture.stderr.byte_overflow
                    || *worker_exit_code != Some(0)
                    || e.data["worker_exit_code"] != 0
                {
                    return Err("evidence_corrupt".into());
                }
            }
            if outcome == "preflight_checked"
                && (!request.native_v2()
                    || request.adapter != "codex-0.154.0-stdio"
                    || !identity_rechecked
                    || !profile_checked
                    || work_started
                    || preflight_stages
                        != [
                            "config",
                            "requirements",
                            "features",
                            "hooks",
                            "plugins",
                            "apps",
                            "mcp",
                        ]
                        .into_iter()
                        .map(str::to_owned)
                        .collect()
                    || e.data["thread_id"] != Value::Null
                    || e.data["turn_id"] != Value::Null
                    || e.data["tree_stopped"] != true
                    || e.data["fixture_unchanged"] != true
                    || e.data["oracle"] != "not_evaluated"
                    || e.data["worker_exit_code"] != 0
                    || request
                        .fixture_inventory()
                        .map_err(|_| "evidence_corrupt")?
                        != inputs.fixture)
            {
                return Err("evidence_corrupt".into());
            }
            if outcome == "completed"
                && (e.data["tree_stopped"] != true
                    || e.data["fixture_unchanged"] != true
                    || e.data["oracle"] != "match")
            {
                return Err("evidence_corrupt".into());
            }
            if outcome == "completed" {
                let result = observed_result.as_ref().ok_or("evidence_corrupt")?;
                if result["thread_id"] != e.data["thread_id"]
                    || result["turn_id"] != e.data["turn_id"]
                    || !crate::oracle::matches(result["text"].as_str().ok_or("evidence_corrupt")?)
                    || request
                        .fixture_inventory()
                        .map_err(|_| "evidence_corrupt")?
                        != inputs.fixture
                    || e.data["worker_exit_code"] != 0
                {
                    return Err("evidence_corrupt".into());
                }
            }
            state = outcome.into();
            terminal = true;
        }
        if e.seq > after && events.len() < limit {
            events.push(serde_json::to_value(e).map_err(|_| "evidence_corrupt")?);
        }
    }
    if seq == 0 {
        return Err("evidence_incomplete".into());
    }
    if after > seq {
        return Err("invalid_cursor".into());
    }
    let next = events
        .last()
        .map_or(after, |e| e["seq"].as_u64().unwrap_or(after));
    Ok(
        json!({"run_id":request.run_id,"events":events,"next_after":next,"state":state,"truncated_tail":bytes.len()-prefix}),
    )
}

#[cfg(test)]
#[path = "../tests/support/journal_fault.rs"]
mod fault;
#[cfg(test)]
pub(crate) use fault::deny_optional_writes;
