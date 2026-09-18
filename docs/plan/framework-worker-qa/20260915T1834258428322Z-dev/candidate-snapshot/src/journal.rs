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
    request_sha256: String,
    fixture: Vec<(String, String)>,
    worker_sha256: String,
    profile_sha256: Option<String>,
}

pub struct Journal {
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
        let inputs = Inputs {
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
        Ok(value)
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
            let outcome = e.data["outcome"].as_str().ok_or("evidence_corrupt")?;
            if ![
                "completed",
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
