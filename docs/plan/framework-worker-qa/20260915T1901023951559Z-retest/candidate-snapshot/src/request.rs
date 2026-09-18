use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::os::windows::fs::MetadataExt;
use std::{
    fs,
    io::Read,
    path::{Component, Path, PathBuf},
};

pub const TASK: &[u8] = include_bytes!("../tests/fixtures/task.json");
pub const PROMPT: &str = include_str!("../tests/fixtures/prompt.txt");
pub const OUTPUT_SCHEMA: &str = include_str!("../tests/fixtures/output-schema.json");
pub type Result<T> = std::result::Result<T, String>;

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Request {
    pub schema_version: u32,
    pub project_id: String,
    pub checkout_id: String,
    pub work_id: String,
    pub run_id: String,
    pub candidate_sha256: String,
    pub checkout_root: PathBuf,
    pub run_dir: PathBuf,
    pub worker_executable: PathBuf,
    pub worker_sha256: String,
    pub adapter: String,
    pub scenario: String,
    // A Value makes explicit null required (Option would accept a missing field).
    #[serde(deserialize_with = "deserialize_profile")]
    pub profile: serde_json::Value,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Profile {
    pub model: String,
    pub effort: String,
    pub review_ref: PathBuf,
    pub review_sha256: String,
}
fn deserialize_profile<'de, D: serde::Deserializer<'de>>(
    d: D,
) -> std::result::Result<serde_json::Value, D::Error> {
    #[derive(Deserialize)]
    #[serde(untagged)]
    enum Input {
        Null(()),
        Reviewed(Profile),
    }
    match Input::deserialize(d)? {
        Input::Null(()) => Ok(serde_json::Value::Null),
        Input::Reviewed(p) => serde_json::to_value(p).map_err(serde::de::Error::custom),
    }
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Source {
    path: PathBuf,
    sha256: String,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Findings {
    native_read_only_available: bool,
    no_external_tool_or_hook_effects: bool,
    codex_managed_chatgpt: bool,
    no_custom_provider: bool,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Review {
    schema_version: u32,
    reviewer: String,
    trial_selection_ref: String,
    codex_sha256: String,
    checkout_root: PathBuf,
    model: String,
    effort: String,
    profile_sources: Vec<Source>,
    findings: Findings,
}

pub fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
pub fn hash_file(path: &Path) -> Result<String> {
    let path = resolve(path)?;
    let mut file = fs::File::open(path).map_err(|_| "input_missing")?;
    let mut hash = Sha256::new();
    let mut block = [0; 65536];
    loop {
        let n = file.read(&mut block).map_err(|_| "input_read_failed")?;
        if n == 0 {
            break;
        }
        hash.update(&block[..n]);
    }
    Ok(format!("{:x}", hash.finalize()))
}

pub fn bounded_read(path: &Path, max: u64) -> Result<Vec<u8>> {
    let path = resolve(path)?;
    let mut bytes = Vec::new();
    fs::File::open(path)
        .map_err(|_| "input_missing")?
        .take(max + 1)
        .read_to_end(&mut bytes)
        .map_err(|_| "input_read_failed")?;
    if bytes.len() as u64 > max {
        return Err("input_limit".into());
    }
    Ok(bytes)
}

pub fn valid_id(s: &str) -> bool {
    !s.is_empty()
        && s.len() <= 64
        && s.as_bytes()[0].is_ascii_alphanumeric()
        && s.bytes()
            .all(|b| b.is_ascii_alphanumeric() || b"._-".contains(&b))
}
pub fn valid_digest(s: &str) -> bool {
    s.len() == 64
        && s.bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

/// Reject traversal and all reparse components before canonicalization.
pub fn resolve(path: &Path) -> Result<PathBuf> {
    if !path.is_absolute() || path.components().any(|c| matches!(c, Component::ParentDir)) {
        return Err("invalid_path".into());
    }
    for part in path.ancestors() {
        let metadata = fs::symlink_metadata(part).map_err(|_| "input_missing")?;
        if metadata.file_attributes() & 0x400 != 0 {
            return Err("reparse_path".into());
        }
    }
    fs::canonicalize(path).map_err(|_| "invalid_path".into())
}

fn overlaps(a: &Path, b: &Path) -> bool {
    let a = a.to_string_lossy().to_lowercase();
    let b = b.to_string_lossy().to_lowercase();
    a == b || a.starts_with(&(b.clone() + "\\")) || b.starts_with(&(a + "\\"))
}

pub fn check_home_boundary(
    checkout: &Path,
    run: &Path,
    home: &Path,
    temp: &Path,
    peer: bool,
) -> Result<()> {
    if (overlaps(checkout, home) || overlaps(run, home))
        && !(peer && checkout.starts_with(temp) && run.starts_with(temp))
    {
        return Err("excluded_root".into());
    }
    Ok(())
}

impl Request {
    pub fn profile(&self) -> Result<Option<Profile>> {
        if self.adapter == "peer" {
            if !self.profile.is_null() {
                return Err("invalid_profile".into());
            }
            Ok(None)
        } else {
            let profile: Profile =
                serde_json::from_value(self.profile.clone()).map_err(|_| "invalid_profile")?;
            if profile.model.trim().is_empty()
                || profile.effort.trim().is_empty()
                || !valid_digest(&profile.review_sha256)
            {
                return Err("invalid_profile".into());
            }
            Ok(Some(profile))
        }
    }

    pub fn fixture_inventory(&self) -> Result<Vec<(String, String)>> {
        let root = resolve(&self.checkout_root)?;
        let mut inventory = Vec::new();
        for entry in fs::read_dir(&root).map_err(|_| "fixture_missing")? {
            let entry = entry.map_err(|_| "fixture_missing")?;
            let path = resolve(&entry.path())?;
            let name = entry
                .file_name()
                .into_string()
                .map_err(|_| "invalid_fixture")?;
            if !path.is_file()
                || !(name == "task.json" || self.adapter == "peer" && name == "peer-case.txt")
            {
                return Err("invalid_fixture".into());
            }
            let bytes = bounded_read(&path, 65536)?;
            if name == "task.json" && (bytes != TASK || digest(&bytes) != self.candidate_sha256) {
                return Err("fixture_changed".into());
            }
            if name == "peer-case.txt" {
                let value = std::str::from_utf8(&bytes).map_err(|_| "invalid_fixture")?;
                let value = value.strip_suffix('\n').ok_or("invalid_fixture")?;
                let parts: Vec<_> = value.split('-').collect();
                if !(parts.len() == 2 || parts.len() == 3)
                    || parts[0] != "WF"
                    || parts[1].len() != 2
                    || !matches!(parts[1].parse::<u8>(), Ok(1..=20))
                    || parts.len() == 3
                        && (parts[2].is_empty() || !parts[2].bytes().all(|b| b.is_ascii_digit()))
                {
                    return Err("invalid_fixture".into());
                }
            }
            inventory.push((name, digest(&bytes)));
        }
        inventory.sort();
        if !inventory.iter().any(|(n, _)| n == "task.json") {
            return Err("fixture_missing".into());
        }
        Ok(inventory)
    }

    pub fn verify_review(&self) -> Result<()> {
        let Some(p) = self.profile()? else {
            return Ok(());
        };
        let bytes = bounded_read(&p.review_ref, 65536)?;
        if digest(&bytes) != p.review_sha256 {
            return Err("profile_unqualified".into());
        }
        let r: Review = serde_json::from_slice(&bytes).map_err(|_| "profile_unqualified")?;
        if r.schema_version != 1
            || r.reviewer.trim().is_empty()
            || r.trial_selection_ref.trim().is_empty()
            || r.codex_sha256 != self.worker_sha256
            || resolve(&r.checkout_root)? != self.checkout_root
            || r.model != p.model
            || r.effort != p.effort
            || !r.findings.native_read_only_available
            || !r.findings.no_external_tool_or_hook_effects
            || !r.findings.codex_managed_chatgpt
            || !r.findings.no_custom_provider
        {
            return Err("profile_unqualified".into());
        }
        let mut seen = std::collections::HashSet::new();
        for source in r.profile_sources {
            let path = resolve(&source.path)?;
            let name = path
                .file_name()
                .unwrap_or_default()
                .to_string_lossy()
                .to_ascii_lowercase();
            if matches!(
                name.as_str(),
                "auth.json"
                    | "credentials.json"
                    | "credentials"
                    | "tokens.json"
                    | "id_rsa"
                    | "id_ed25519"
            ) {
                return Err("profile_unqualified".into());
            }
            if !seen.insert(path.to_string_lossy().to_lowercase())
                || hash_file(&path)? != source.sha256
            {
                return Err("profile_unqualified".into());
            }
        }
        Ok(())
    }
}

pub fn validate(path: &Path) -> Result<Request> {
    let bytes = bounded_read(path, 65536)?;
    let mut r: Request = serde_json::from_slice(&bytes).map_err(|_| "invalid_request")?;
    if r.schema_version != 1
        || [&r.project_id, &r.checkout_id, &r.work_id, &r.run_id]
            .iter()
            .any(|s| !valid_id(s))
        || !valid_digest(&r.candidate_sha256)
        || !valid_digest(&r.worker_sha256)
        || !matches!(r.adapter.as_str(), "peer" | "codex-0.154.0-stdio")
        || !matches!(r.scenario.as_str(), "complete" | "cancel")
    {
        return Err("invalid_request".into());
    }
    r.profile()?;
    r.checkout_root = resolve(&r.checkout_root)?;
    r.worker_executable = resolve(&r.worker_executable)?;
    if r.adapter == "peer" {
        let current = std::env::current_exe().map_err(|_| "invalid_worker")?;
        let mut directory = current.parent().ok_or("invalid_worker")?;
        if directory.file_name().is_some_and(|n| n == "deps") {
            directory = directory.parent().ok_or("invalid_worker")?;
        }
        if r.worker_executable != resolve(&directory.join("protocol-peer.exe"))? {
            return Err("invalid_worker".into());
        }
    } else {
        let discovery: serde_json::Value =
            serde_json::from_str(include_str!("../tests/fixtures/schema-command.json"))
                .map_err(|_| "invalid_worker")?;
        let selected = discovery["executable"].as_str().ok_or("invalid_worker")?;
        if r.worker_executable != resolve(Path::new(selected))? {
            return Err("invalid_worker".into());
        }
    }
    if !r.run_dir.is_absolute()
        || r.run_dir
            .components()
            .any(|c| matches!(c, Component::ParentDir))
    {
        return Err("invalid_path".into());
    }
    if r.run_dir.symlink_metadata().is_ok() {
        return Err("run_exists".into());
    }
    let parent = resolve(r.run_dir.parent().ok_or("invalid_path")?)?;
    r.run_dir = parent.join(r.run_dir.file_name().ok_or("invalid_path")?);
    if overlaps(&r.checkout_root, &r.run_dir) || r.checkout_root.parent() != Some(parent.as_path())
    {
        return Err("overlapping_roots".into());
    }
    let workspace = resolve(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .ancestors()
            .nth(3)
            .ok_or("invalid_path")?,
    )?;
    for name in ["src", "devforgeai", ".agents", ".codex", ".claude"] {
        let excluded = workspace.join(name);
        if overlaps(&r.checkout_root, &excluded) || overlaps(&r.run_dir, &excluded) {
            return Err("excluded_root".into());
        }
    }
    if let Some(home) = std::env::var_os("USERPROFILE") {
        check_home_boundary(
            &r.checkout_root,
            &r.run_dir,
            &resolve(Path::new(&home))?,
            &resolve(&std::env::temp_dir())?,
            r.adapter == "peer",
        )?;
    }
    if r.adapter != "peer" {
        let trial = workspace
            .join("docs/plan/framework-worker-trials")
            .join(&r.run_id);
        if r.checkout_root != trial.join("fixture") || r.run_dir != trial.join("run") {
            return Err("invalid_trial_layout".into());
        }
    }
    if hash_file(&r.worker_executable)? != r.worker_sha256 {
        return Err("worker_changed".into());
    }
    r.fixture_inventory()?;
    Ok(r)
}
