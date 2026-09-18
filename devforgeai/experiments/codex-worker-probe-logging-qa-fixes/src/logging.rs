//! Closed, non-authoritative diagnostic output. Never accepts child text.
use crate::request::{self, Request, Result};
use serde::{Deserialize, Serialize};
use serde_json::json;
use sha2::{Digest, Sha256};
use std::{
    fs::{File, OpenOptions},
    io::Write,
    path::Path,
};

pub const MAX_CONFIG: u64 = 4096;
pub const MAX_EVENTS: usize = 512;
pub const MAX_BYTES: usize = 1024 * 1024;

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, PartialOrd, Ord, Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Level {
    #[default]
    Off,
    Minimal,
    Verbose,
    Debug,
}
#[derive(Clone, Copy, Deserialize, Serialize)]
pub enum Redaction {
    #[serde(rename = "closed-v1")]
    ClosedV1,
}
#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Config {
    pub schema_version: u32,
    pub level: Level,
    pub redaction_policy: Redaction,
}
#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Binding {
    pub level: Level,
    pub sha256: String,
}

pub fn load(r: &Request) -> Result<Option<(Config, Vec<u8>)>> {
    if r.schema_version != 3 {
        return if r.diagnostics_ref.is_none() && r.diagnostics_sha256.is_none() {
            Ok(None)
        } else {
            Err("invalid_diagnostics".into())
        };
    }
    let path = r.diagnostics_ref.as_ref().ok_or("invalid_diagnostics")?;
    let hash = r
        .diagnostics_sha256
        .as_deref()
        .filter(|h| request::valid_digest(h))
        .ok_or("invalid_diagnostics")?;
    let bytes = request::bounded_read(path, MAX_CONFIG).map_err(|_| "invalid_diagnostics")?;
    let config: Config = serde_json::from_slice(&bytes).map_err(|_| "invalid_diagnostics")?;
    if config.schema_version != 1 || request::digest(&bytes) != hash {
        return Err("invalid_diagnostics".into());
    }
    Ok(Some((config, bytes)))
}

#[derive(Clone, Copy, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Phase {
    Admitted,
    SpawnIntent,
    ServerStarted,
    StopRequested,
    PostSpawn,
    PostPreflight,
    InputClosed,
}
#[derive(Clone, Copy, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Rpc {
    Initialize,
    ConfigRead,
    Other,
}
impl Rpc {
    pub fn from_method(method: &str) -> Self {
        match method {
            "initialize" => Self::Initialize,
            "config/read" => Self::ConfigRead,
            _ => Self::Other,
        }
    }
}
#[derive(Serialize)]
#[serde(tag = "event", rename_all = "snake_case")]
pub enum Record<'a> {
    Phase {
        phase: Phase,
        elapsed_ms: u64,
    },
    Spawn {
        pid: u32,
        elapsed_ms: u64,
    },
    Launch {
        arguments: usize,
        argv_sha256: String,
        policy_sha256: Option<String>,
    },
    Rpc {
        rpc: Rpc,
        elapsed_ms: u64,
        failed: bool,
    },
    Exit {
        capture: &'a crate::capture::Capture,
        pre_stop_exit_code: Option<u32>,
        post_stop_exit_code: Option<u32>,
        tree_stopped: bool,
    },
    Chunk {
        stream: crate::capture::Stream,
        chunk: &'a crate::capture::Chunk,
    },
}
#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Status {
    pub level: Level,
    pub bytes: usize,
    pub events: usize,
    pub sha256: String,
    pub diagnostics_incomplete: bool,
    pub dropped: usize,
}
pub struct Sink {
    level: Level,
    file: Option<File>,
    bytes: usize,
    events: usize,
    hash: Sha256,
    incomplete: bool,
    dropped: usize,
}
impl Sink {
    pub fn new(dir: &Path, level: Level) -> Self {
        let file = if level == Level::Off {
            None
        } else {
            OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(dir.join("diagnostics.jsonl"))
                .ok()
        };
        let incomplete = level != Level::Off && file.is_none();
        Self {
            level,
            file,
            bytes: 0,
            events: 0,
            hash: Sha256::new(),
            incomplete,
            dropped: 0,
        }
    }
    pub fn record(&mut self, level: Level, record: Record<'_>) {
        if self.level < level || self.level == Level::Off {
            return;
        }
        // Only typed records are accepted here. Serialization cannot contain raw payloads.
        let mut bytes = serde_json::to_vec(&json!({"schema_version":1,"record":record}))
            .expect("typed JSON record");
        bytes.push(b'\n');
        self.write(&bytes);
    }
    fn write(&mut self, bytes: &[u8]) {
        if self.incomplete || self.events == MAX_EVENTS || self.bytes + bytes.len() > MAX_BYTES {
            self.incomplete = true;
            self.dropped += 1;
            return;
        }
        if self
            .file
            .as_mut()
            .is_none_or(|f| f.write_all(bytes).and_then(|()| f.flush()).is_err())
        {
            self.incomplete = true;
            self.dropped += 1;
            return;
        }
        self.hash.update(bytes);
        self.bytes += bytes.len();
        self.events += 1;
    }
    pub fn finish(&mut self) -> Status {
        if let Some(file) = self.file.take() {
            self.incomplete |= file.sync_all().is_err();
        }
        Status {
            level: self.level,
            bytes: self.bytes,
            events: self.events,
            sha256: format!("{:x}", self.hash.clone().finalize()),
            diagnostics_incomplete: self.incomplete,
            dropped: self.dropped,
        }
    }
}

pub fn inspect(dir: &Path, binding: Option<&Binding>, status: &Status) -> Result<()> {
    let level = binding.map_or(Level::Off, |b| b.level);
    if status.level != level || status.diagnostics_incomplete || status.dropped != 0 {
        return Err("evidence_incomplete".into());
    }
    if level == Level::Off {
        if dir.join("diagnostics.jsonl").symlink_metadata().is_ok()
            || status.bytes != 0
            || status.events != 0
            || status.sha256 != request::digest(b"")
        {
            return Err("evidence_corrupt".into());
        }
    } else {
        let bytes = request::bounded_read(&dir.join("diagnostics.jsonl"), MAX_BYTES as u64)
            .map_err(|_| "evidence_incomplete")?;
        if bytes.len() != status.bytes
            || request::digest(&bytes) != status.sha256
            || status.events > MAX_EVENTS
            || !bytes.ends_with(b"\n")
        {
            return Err("evidence_corrupt".into());
        }
        let mut count = 0;
        for line in bytes.split_inclusive(|b| *b == b'\n') {
            let v: serde_json::Value =
                serde_json::from_slice(line).map_err(|_| "evidence_corrupt")?;
            if v["schema_version"] != 1 || !v["record"].is_object() {
                return Err("evidence_corrupt".into());
            }
            count += 1;
        }
        if count != status.events {
            return Err("evidence_corrupt".into());
        }
    }
    Ok(())
}

#[cfg(test)]
#[path = "../tests/support/logging_cases.rs"]
mod tests;
