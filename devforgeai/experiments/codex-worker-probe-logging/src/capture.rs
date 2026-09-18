//! Bounded pipe accounting independent of protocol consumption and file logging.
use crate::{process_windows::Incoming, request};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    io::Read,
    sync::{
        Arc, Mutex,
        atomic::{AtomicUsize, Ordering},
        mpsc::SyncSender,
    },
    thread,
};
pub const MAX_OUTPUT: usize = 8 * 1024 * 1024;
pub const MAX_LINE: usize = 1024 * 1024;
pub const MAX_DETAIL: usize = 64;
pub const MAX_CLASSIFY: usize = 65536;
#[derive(Clone, Copy, Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Stream {
    Stdout,
    Stderr,
}
#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Chunk {
    pub bytes: usize,
    pub sha256: String,
}
#[derive(Clone, Copy, Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum Category {
    StrictConfigRejected,
    ConfigurationParseFailed,
    Unclassified,
}
fn classify(bytes: &[u8]) -> Category {
    let contains = |needle: &[u8]| bytes.windows(needle.len()).any(|b| b == needle);
    if bytes.starts_with(b"Error: ") && contains(b": unknown configuration field `") {
        Category::StrictConfigRejected
    } else if bytes.starts_with(b"Error: invalid transport\n") && contains(b"in `mcp_servers.") {
        Category::ConfigurationParseFailed
    } else {
        Category::Unclassified
    }
}
#[derive(Clone, Copy, Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ReadError {
    PipeReadFailed,
}
#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Summary {
    pub bytes: usize,
    pub sha256: String,
    pub eof: bool,
    pub read_error: Option<ReadError>,
    pub byte_overflow: bool,
    pub queue_overflow: bool,
    pub line_overflow: bool,
    pub detail_dropped: usize,
    pub utf8_valid: bool,
    pub lines: usize,
    pub final_line_bytes: usize,
    pub max_line_bytes: usize,
    pub queue_high_water: usize,
    pub category: Category,
    pub classifier_version: String,
    pub classification_truncated: bool,
}
#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Capture {
    pub stdout: Summary,
    pub stderr: Summary,
    pub drain_complete: bool,
}
impl Capture {
    pub fn validate(&self) -> request::Result<()> {
        for s in [&self.stdout, &self.stderr] {
            if !request::valid_digest(&s.sha256)
                || s.classifier_version != "startup-v1"
                || s.bytes > MAX_OUTPUT + 16384
                || s.final_line_bytes > s.bytes
                || s.lines > s.bytes
                || (s.bytes == 0 && s.sha256 != request::digest(b""))
            {
                return Err("evidence_corrupt".into());
            }
        }
        if self.drain_complete
            && (!self.stdout.eof
                || !self.stderr.eof
                || self.stdout.read_error.is_some()
                || self.stderr.read_error.is_some())
        {
            return Err("evidence_corrupt".into());
        }
        Ok(())
    }
}
#[derive(Default)]
pub(crate) struct State {
    bytes: usize,
    hash: Sha256,
    eof: bool,
    read_error: Option<ReadError>,
    byte_overflow: bool,
    queue_overflow: bool,
    line_overflow: bool,
    dropped: usize,
    invalid_utf8: bool,
    utf8_tail: Vec<u8>,
    lines: usize,
    line_bytes: usize,
    max_line_bytes: usize,
    queued: usize,
    queue_high_water: usize,
    prefix: Vec<u8>,
    pub chunks: Vec<Chunk>,
}
impl State {
    fn update(&mut self, bytes: &[u8], stderr: bool) {
        self.bytes += bytes.len();
        self.hash.update(bytes);
        if self.chunks.len() < MAX_DETAIL {
            self.chunks.push(Chunk {
                bytes: bytes.len(),
                sha256: request::digest(bytes),
            });
        } else {
            self.dropped += 1;
        }
        if stderr {
            let n = bytes.len().min(MAX_CLASSIFY - self.prefix.len());
            self.prefix.extend_from_slice(&bytes[..n]);
        }
        self.utf8_tail.extend_from_slice(bytes);
        match std::str::from_utf8(&self.utf8_tail) {
            Ok(_) => self.utf8_tail.clear(),
            Err(e) => {
                if e.error_len().is_some() {
                    self.invalid_utf8 = true;
                    self.utf8_tail.clear();
                } else {
                    self.utf8_tail.drain(..e.valid_up_to());
                }
            }
        }
        for b in bytes {
            if *b == b'\n' {
                self.lines += 1;
                self.line_bytes = 0;
            } else {
                self.line_bytes += 1;
                self.max_line_bytes = self.max_line_bytes.max(self.line_bytes);
            }
        }
    }
    pub fn summary(&self) -> Summary {
        Summary {
            bytes: self.bytes,
            sha256: format!("{:x}", self.hash.clone().finalize()),
            eof: self.eof,
            read_error: self.read_error,
            byte_overflow: self.byte_overflow,
            queue_overflow: self.queue_overflow,
            line_overflow: self.line_overflow,
            detail_dropped: self.dropped,
            utf8_valid: !self.invalid_utf8 && self.utf8_tail.is_empty(),
            lines: self.lines,
            final_line_bytes: self.line_bytes,
            max_line_bytes: self.max_line_bytes,
            queue_high_water: self.queue_high_water,
            category: classify(&self.prefix),
            classifier_version: "startup-v1".into(),
            classification_truncated: self.bytes > MAX_CLASSIFY && !self.prefix.is_empty(),
        }
    }
    pub fn error(&self) -> Option<&'static str> {
        if self.byte_overflow || self.queue_overflow || self.line_overflow {
            Some("output_limit")
        } else if self.read_error.is_some() {
            Some("pipe_read_failed")
        } else {
            None
        }
    }
    pub fn line_consumed(&mut self) {
        self.queued = self.queued.saturating_sub(1);
    }
}
pub(crate) type Shared = Arc<Mutex<State>>;
pub(crate) fn reader<R: Read + Send + 'static>(
    mut file: R,
    stderr: bool,
    tx: SyncSender<Incoming>,
    total: Arc<AtomicUsize>,
    state: Shared,
) -> thread::JoinHandle<()> {
    thread::spawn(move || {
        let mut block = [0; 8192];
        let mut line = Vec::new();
        let mut delivery = true;
        loop {
            let n = match file.read(&mut block) {
                Ok(0) => {
                    state.lock().unwrap().eof = true;
                    break;
                }
                Ok(n) => n,
                Err(_) => {
                    state.lock().unwrap().read_error = Some(ReadError::PipeReadFailed);
                    let _ = tx.try_send(Incoming::Error("pipe_read_failed"));
                    return;
                }
            };
            {
                state.lock().unwrap().update(&block[..n], stderr);
            }
            if total.fetch_add(n, Ordering::Relaxed) + n > MAX_OUTPUT {
                state.lock().unwrap().byte_overflow = true;
                let _ = tx.try_send(Incoming::Error("output_limit"));
                return;
            }
            if stderr {
                if tx
                    .try_send(Incoming::Stderr {
                        bytes: n,
                        sha256: request::digest(&block[..n]),
                    })
                    .is_err()
                {
                    state.lock().unwrap().dropped += 1;
                }
            } else if delivery {
                for b in &block[..n] {
                    if *b == b'\n' {
                        let mut state = state.lock().unwrap();
                        if tx
                            .try_send(Incoming::Line(std::mem::take(&mut line)))
                            .is_err()
                        {
                            state.queue_overflow = true;
                            delivery = false;
                            break;
                        }
                        state.queued += 1;
                        state.queue_high_water = state.queue_high_water.max(state.queued);
                    } else if line.len() == MAX_LINE {
                        state.lock().unwrap().line_overflow = true;
                        delivery = false;
                        line.clear();
                        break;
                    } else {
                        line.push(*b);
                    }
                }
            }
        }
        if !stderr {
            let _ = tx.try_send(if line.is_empty() {
                Incoming::End
            } else {
                Incoming::Error("protocol_error")
            });
        }
    })
}

#[cfg(test)]
#[path = "../tests/support/capture_cases.rs"]
mod tests;
