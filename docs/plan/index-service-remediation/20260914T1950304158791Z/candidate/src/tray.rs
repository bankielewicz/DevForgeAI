//! Optional Windows human interface over the shared management client.
use crate::{
    platform::{self, Paths},
    protocol::{ErrorCode, ProtocolError, Result},
};
use serde::{Deserialize, Serialize};
use std::time::{Duration, Instant};

/// Human-facing status; protocol envelopes remain available through the CLI.
pub fn status_text(
    alias: &str,
    response: &crate::protocol::Response,
    projects: &[serde_json::Value],
    statuses: &[serde_json::Value],
) -> String {
    let mut lines = vec![format!("Environment: {alias}")];
    if let Some(error) = &response.error {
        lines.push(format!(
            "Disconnected or request failed: {}",
            serde_json::to_value(error.code)
                .unwrap_or_default()
                .as_str()
                .unwrap_or("ERROR")
        ));
        lines.push(error.message.clone());
        if !error.details.is_null() && error.details != serde_json::json!({}) {
            lines.push(format!("Details: {}", error.details));
        }
    } else {
        let mode = if response.data["indexing_mode"] == "paused" {
            "Paused — indexing waits for Resume"
        } else if response.data["daemon_state"] == "stopping" {
            "Stopping"
        } else if response.data["daemon_state"] == "running"
            || response.data.get("already_running").is_some()
        {
            "Running"
        } else {
            "Connected — request acknowledged"
        };
        lines.push(mode.into());
        if response.data["degraded"] == true {
            lines.push("Cache needs recovery. Use daemon diagnostics and the confirmed index rebuild command.".into());
        }
        if projects.is_empty() {
            lines.push("No registered projects.".into());
        }
        for project in projects {
            lines.push(String::new());
            lines.push(format!(
                "{} — {}",
                project["name"].as_str().unwrap_or("Unnamed project"),
                project["root"].as_str().unwrap_or("")
            ));
            if let Some(status) = statuses
                .iter()
                .find(|status| status["project_id"] == project["id"])
            {
                lines.push(format!(
                    "Coverage: {}   Freshness: {}",
                    status["coverage"].as_str().unwrap_or("unknown"),
                    status["freshness"].as_str().unwrap_or("unknown")
                ));
                lines.push(format!(
                    "Current generation: {}",
                    status["current_generation"].as_str().unwrap_or("unknown")
                ));
                lines.push(format!(
                    "Last reconciliation (Unix seconds, UTC): {}",
                    status["last_reconciliation"]
                        .as_i64()
                        .map(|seconds| seconds.to_string())
                        .unwrap_or_else(|| "unknown".into())
                ));
                let count = |name: &str| status[name].as_u64().unwrap_or(0);
                lines.push(format!(
                    "{} text / {} structural / {} excluded / {} skipped / {} failed",
                    count("text_count"),
                    count("structural_count"),
                    count("excluded_count"),
                    count("skipped_count"),
                    count("failed_count")
                ));
                if let Some(jobs) = status["jobs"].as_array() {
                    for job in jobs {
                        lines.push(format!(
                            "{}: {}",
                            job["kind"].as_str().unwrap_or("Job"),
                            job["outcome"].as_str().unwrap_or("unknown")
                        ));
                    }
                }
            }
        }
    }
    lines.join("\r\n")
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Preferences {
    pub launch_at_sign_in: bool,
    pub start_local_daemon: bool,
}
pub struct PollState {
    in_flight: bool,
    next: Instant,
}
impl PollState {
    pub fn new(now: Instant) -> Self {
        Self {
            in_flight: false,
            next: now,
        }
    }
    pub fn begin(&mut self, now: Instant, _visible: bool) -> bool {
        if self.in_flight || now < self.next {
            return false;
        }
        self.in_flight = true;
        true
    }
    pub fn finish(&mut self, now: Instant, visible: bool, failed: bool) {
        self.in_flight = false;
        self.next = now + Duration::from_secs(if visible && !failed { 5 } else { 30 });
    }
}
fn supported() -> Result<()> {
    if cfg!(windows) {
        Ok(())
    } else {
        Err(ProtocolError::new(
            ErrorCode::UnsupportedPlatform,
            "Tray is Windows-only",
        ))
    }
}
pub fn preferences(paths: &Paths) -> Result<Preferences> {
    supported()?;
    let file = paths.data.join("tray-settings.json");
    if !file.exists() {
        return Ok(Preferences::default());
    }
    serde_json::from_slice(&std::fs::read(file).map_err(platform::io_error)?)
        .map_err(|error| ProtocolError::new(ErrorCode::InvalidArgument, error.to_string()))
}
pub fn set_preferences(
    paths: &Paths,
    launch: Option<bool>,
    daemon: Option<bool>,
) -> Result<Preferences> {
    let mut prefs = preferences(paths)?;
    if let Some(value) = launch {
        #[cfg(windows)]
        windows::startup(value)?;
        prefs.launch_at_sign_in = value;
    }
    if let Some(value) = daemon {
        prefs.start_local_daemon = value;
    }
    platform::atomic_write(
        &paths.data.join("tray-settings.json"),
        &serde_json::to_vec(&prefs)
            .map_err(|e| ProtocolError::new(ErrorCode::InternalError, e.to_string()))?,
    )?;
    Ok(prefs)
}
pub fn launch() -> Result<()> {
    supported()?;
    #[cfg(windows)]
    {
        let path = std::env::current_exe()
            .map_err(platform::io_error)?
            .with_file_name("devforgeai-tray.exe");
        platform::windows::spawn_detached(&path)?;
    }
    Ok(())
}
pub fn run() -> Result<()> {
    supported()?;
    #[cfg(windows)]
    {
        windows::run()
    }
    #[cfg(not(windows))]
    Ok(())
}

#[cfg(windows)]
#[path = "tray_windows.rs"]
mod windows;
