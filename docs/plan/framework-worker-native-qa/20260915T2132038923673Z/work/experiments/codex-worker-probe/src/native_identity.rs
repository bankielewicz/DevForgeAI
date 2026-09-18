//! Narrow observation of the pinned launcher junctions; never a general path exemption.
use crate::request::{Result, hash_file, resolve};
use serde::Deserialize;
use std::{
    fs,
    os::windows::{ffi::OsStrExt, fs::MetadataExt},
    path::{Component, Path, PathBuf, Prefix},
};
use windows_sys::Win32::{
    Foundation::{CloseHandle, INVALID_HANDLE_VALUE},
    Storage::FileSystem::{
        CreateFileW, FILE_ATTRIBUTE_TAG_INFO, FILE_FLAG_BACKUP_SEMANTICS,
        FILE_FLAG_OPEN_REPARSE_POINT, FILE_SHARE_DELETE, FILE_SHARE_READ, FILE_SHARE_WRITE,
        FileAttributeTagInfo, GetFileInformationByHandleEx, OPEN_EXISTING,
    },
};

pub const RECORD: &str = include_str!("native-executable-identity.json");
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Junction {
    path: PathBuf,
    target: PathBuf,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Identity {
    schema_version: u32,
    adapter: String,
    captured_alias: PathBuf,
    physical_executable: PathBuf,
    executable_sha256: String,
    junctions: Vec<Junction>,
}

fn normalized(path: &Path) -> PathBuf {
    let text = path.as_os_str().to_string_lossy();
    PathBuf::from(
        text.strip_prefix(r"\\?\")
            .or_else(|| text.strip_prefix(r"\??\"))
            .unwrap_or(&text),
    )
}
fn same(a: &Path, b: &Path) -> bool {
    normalized(a)
        .as_os_str()
        .eq_ignore_ascii_case(normalized(b).as_os_str())
}
fn local_absolute(path: &Path) -> bool {
    path.is_absolute()
        && !path.components().any(|c| matches!(c, Component::ParentDir))
        && matches!(path.components().next(), Some(Component::Prefix(p)) if matches!(p.kind(), Prefix::Disk(_) | Prefix::VerbatimDisk(_)))
}
fn first_reparse(path: &Path) -> Result<Option<PathBuf>> {
    if !local_absolute(path) {
        return Err("invalid_worker".into());
    }
    for part in path.ancestors().collect::<Vec<_>>().into_iter().rev() {
        if fs::symlink_metadata(part)
            .map_err(|_| "invalid_worker")?
            .file_attributes()
            & 0x400
            != 0
        {
            return Ok(Some(part.to_path_buf()));
        }
    }
    Ok(None)
}

fn directory_junction(path: &Path) -> Result<bool> {
    let wide: Vec<_> = path.as_os_str().encode_wide().chain(Some(0)).collect();
    // Open the reparse point itself. The handle is owned only here, queried synchronously,
    // and closed on every successfully opened path. No target or executable is run.
    let handle = unsafe {
        CreateFileW(
            wide.as_ptr(),
            0,
            FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
            std::ptr::null(),
            OPEN_EXISTING,
            FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS,
            std::ptr::null_mut(),
        )
    };
    if handle == INVALID_HANDLE_VALUE {
        return Err("invalid_worker".into());
    }
    let mut info = FILE_ATTRIBUTE_TAG_INFO::default();
    let ok = unsafe {
        GetFileInformationByHandleEx(
            handle,
            FileAttributeTagInfo,
            (&mut info as *mut FILE_ATTRIBUTE_TAG_INFO).cast(),
            std::mem::size_of_val(&info) as u32,
        )
    };
    unsafe {
        CloseHandle(handle);
    }
    Ok(ok != 0 && info.FileAttributes & 0x10 != 0 && info.ReparseTag == 0xa0000003)
}

impl Identity {
    fn verify(&self, supplied: &Path, digest: &str, adapter: &str) -> Result<PathBuf> {
        self.verify_inner(supplied, digest, adapter)
            .map_err(|_| "invalid_worker".into())
    }

    fn verify_inner(&self, supplied: &Path, digest: &str, adapter: &str) -> Result<PathBuf> {
        if self.schema_version != 1
            || self.junctions.len() != 2
            || self.adapter != "codex-0.154.0-stdio"
            || adapter != self.adapter
            || same(&self.junctions[0].path, &self.junctions[1].path)
            || digest != self.executable_sha256
            || !local_absolute(supplied)
        {
            return Err("invalid_worker".into());
        }
        let physical = resolve(&self.physical_executable)?;
        let selected = resolve(supplied)?;
        if !same(&selected, &physical) {
            return Err("invalid_worker".into());
        }
        let mut observed = self.captured_alias.clone();
        for junction in &self.junctions {
            let first = first_reparse(&observed)?.ok_or("invalid_worker")?;
            if !same(&first, &junction.path) || !directory_junction(&first)? {
                return Err("invalid_worker".into());
            }
            let target = fs::read_link(&first).map_err(|_| "invalid_worker")?;
            if !same(&target, &junction.target) || !local_absolute(&target) {
                return Err("invalid_worker".into());
            }
            let suffix = observed
                .strip_prefix(&first)
                .map_err(|_| "invalid_worker")?;
            observed = normalized(&target).join(suffix);
        }
        // No remaining reparse point is allowed after the two inspected substitutions.
        if !same(&resolve(&observed)?, &physical) || hash_file(&physical)? != digest {
            return Err("invalid_worker".into());
        }
        Ok(physical)
    }
}

/// Verify only the compiled-in identity, both at admission and immediately before spawn.
/// Caller-controlled identity records are deliberately not an API.
pub fn verify(path: &Path, digest: &str, adapter: &str) -> Result<PathBuf> {
    let identity: Identity = serde_json::from_str(RECORD).map_err(|_| "invalid_worker")?;
    identity.verify(path, digest, adapter)
}

#[cfg(test)]
#[path = "../tests/support/identity_cases.rs"]
mod tests;
