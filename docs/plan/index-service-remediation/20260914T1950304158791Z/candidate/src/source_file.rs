//! Handle-based source opening. Directory links are never followed during capture.
use std::{
    fs::{self, File},
    path::{Component, Path},
};

pub struct OpenSource {
    pub file: File,
    // On Windows, excluding DELETE sharing prevents directory replacement until capture ends.
    _directories: Vec<File>,
}

pub fn open(root: &Path, relative: &str) -> Result<OpenSource, String> {
    let requested = root.join(relative);
    let mut directories = guard_parents(root, Path::new(relative))?;
    let target = fs::canonicalize(&requested).map_err(|_| "file_unavailable")?;
    let target_relative = target
        .strip_prefix(root)
        .map_err(|_| "path_outside_project")?;
    directories.extend(guard_parents(root, target_relative)?);
    let file = open_leaf(root, target_relative)?;
    if !file
        .metadata()
        .map_err(|_| "metadata_unavailable")?
        .is_file()
    {
        return Err("non_regular_file".into());
    }
    Ok(OpenSource {
        file,
        _directories: directories,
    })
}

#[cfg(test)]
#[path = "../tests/unit/source_file.rs"]
mod repair_tests;

#[cfg(unix)]
fn directory_at(parent: Option<&File>, path: &std::ffi::OsStr) -> Result<File, String> {
    use std::os::{
        fd::{AsRawFd, FromRawFd},
        unix::ffi::OsStrExt,
    };
    let name = std::ffi::CString::new(path.as_bytes()).map_err(|_| "invalid_path")?;
    let fd = unsafe {
        libc::openat(
            parent.map_or(libc::AT_FDCWD, AsRawFd::as_raw_fd),
            name.as_ptr(),
            libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC,
        )
    };
    if fd < 0 {
        return Err("directory_link_or_unavailable".into());
    }
    Ok(unsafe { File::from_raw_fd(fd) })
}
#[cfg(unix)]
fn guard_parents(root: &Path, relative: &Path) -> Result<Vec<File>, String> {
    let mut files = vec![directory_at(None, root.as_os_str())?];
    if let Some(parent) = relative.parent() {
        for component in parent.components() {
            let Component::Normal(name) = component else {
                return Err("path_outside_project".into());
            };
            files.push(directory_at(files.last(), name)?);
        }
    }
    Ok(files)
}
#[cfg(unix)]
fn open_leaf(root: &Path, relative: &Path) -> Result<File, String> {
    use std::os::{
        fd::{AsRawFd, FromRawFd},
        unix::ffi::OsStrExt,
    };
    let parents = guard_parents(root, relative)?;
    let name = std::ffi::CString::new(relative.file_name().ok_or("invalid_path")?.as_bytes())
        .map_err(|_| "invalid_path")?;
    let fd = unsafe {
        libc::openat(
            parents.last().ok_or("root_unavailable")?.as_raw_fd(),
            name.as_ptr(),
            libc::O_RDONLY | libc::O_NOFOLLOW | libc::O_NONBLOCK | libc::O_CLOEXEC,
        )
    };
    if fd < 0 {
        return Err("file_changed_or_unavailable".into());
    }
    Ok(unsafe { File::from_raw_fd(fd) })
}

#[cfg(windows)]
fn guard_parents(root: &Path, relative: &Path) -> Result<Vec<File>, String> {
    use std::os::windows::fs::{MetadataExt, OpenOptionsExt};
    use windows_sys::Win32::Storage::FileSystem::*;
    let mut paths = vec![root.to_owned()];
    if let Some(parent) = relative.parent() {
        for component in parent.components() {
            let Component::Normal(name) = component else {
                return Err("path_outside_project".into());
            };
            paths.push(paths.last().ok_or("root_unavailable")?.join(name));
        }
    }
    let mut files = Vec::new();
    for path in paths {
        let file = fs::OpenOptions::new()
            .access_mode(FILE_READ_ATTRIBUTES)
            .share_mode(FILE_SHARE_READ | FILE_SHARE_WRITE)
            .custom_flags(FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT)
            .open(path)
            .map_err(|_| "directory_unavailable")?;
        let metadata = file.metadata().map_err(|_| "metadata_unavailable")?;
        if !metadata.is_dir() || metadata.file_attributes() & FILE_ATTRIBUTE_REPARSE_POINT != 0 {
            return Err("directory_link_or_unavailable".into());
        }
        files.push(file);
    }
    Ok(files)
}
#[cfg(windows)]
fn open_leaf(root: &Path, relative: &Path) -> Result<File, String> {
    use std::os::windows::{
        fs::{MetadataExt, OpenOptionsExt},
        io::AsRawHandle,
    };
    use windows_sys::Win32::Storage::FileSystem::*;
    let file = fs::OpenOptions::new()
        .read(true)
        .share_mode(FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE)
        .custom_flags(FILE_FLAG_OPEN_REPARSE_POINT)
        .open(root.join(relative))
        .map_err(|_| "file_unavailable")?;
    if file
        .metadata()
        .map_err(|_| "metadata_unavailable")?
        .file_attributes()
        & FILE_ATTRIBUTE_REPARSE_POINT
        != 0
    {
        return Err("file_changed_or_unavailable".into());
    }
    let mut name = vec![0u16; 32768];
    let length = unsafe {
        GetFinalPathNameByHandleW(
            file.as_raw_handle(),
            name.as_mut_ptr(),
            name.len() as u32,
            0,
        )
    } as usize;
    if length == 0 || length >= name.len() {
        return Err("file_path_unavailable".into());
    }
    let actual =
        std::path::PathBuf::from(String::from_utf16(&name[..length]).map_err(|_| "invalid_path")?);
    if !actual.starts_with(root) {
        return Err("path_outside_project".into());
    }
    Ok(file)
}
