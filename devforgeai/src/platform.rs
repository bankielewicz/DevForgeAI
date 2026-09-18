//! Native user ownership, private paths and local-only root validation.
use crate::protocol::{ErrorCode, ProtocolError, Result};
use fs2::FileExt;
use std::fs::{self, File, OpenOptions};
use std::path::{Path, PathBuf};

pub fn io_error(error: std::io::Error) -> ProtocolError {
    ProtocolError::new(
        if error.kind() == std::io::ErrorKind::PermissionDenied {
            ErrorCode::AccessDenied
        } else {
            ErrorCode::InternalError
        },
        error.to_string(),
    )
}

#[derive(Clone, Debug)]
pub struct Paths {
    pub data: PathBuf,
    pub runtime: PathBuf,
    pub endpoint: String,
}
impl Paths {
    pub fn discover() -> Result<Self> {
        // Explicit test/development isolation. No default data is touched when supplied.
        if let Some(path) = std::env::var_os("DEVFORGEAI_INDEX_DATA") {
            return Self::at(PathBuf::from(path));
        }
        #[cfg(windows)]
        let data = PathBuf::from(std::env::var_os("LOCALAPPDATA").ok_or_else(|| {
            ProtocolError::new(ErrorCode::InternalError, "LOCALAPPDATA unavailable")
        })?)
        .join("DevForgeAI/Index");
        #[cfg(unix)]
        let data = std::env::var_os("XDG_STATE_HOME")
            .map(PathBuf::from)
            .or_else(|| {
                std::env::var_os("HOME").map(|home| PathBuf::from(home).join(".local/state"))
            })
            .ok_or_else(|| {
                ProtocolError::new(ErrorCode::InternalError, "User state directory unavailable")
            })?
            .join("devforgeai/index");
        Self::at(data)
    }
    pub fn at(data: PathBuf) -> Result<Self> {
        if !data.is_absolute() {
            return Err(ProtocolError::new(
                ErrorCode::InvalidRoot,
                "Data directory must be absolute",
            ));
        }
        private_directory(&data)?;
        let data = fs::canonicalize(data).map_err(io_error)?;
        let runtime = data.join("runtime");
        private_directory(&runtime)?;
        #[cfg(windows)]
        let endpoint = format!(
            r"\\.\pipe\DevForgeAI-Index-{}-{}",
            current_identity()?,
            &crate::index::digest(data.to_string_lossy().as_bytes())[..16]
        );
        #[cfg(unix)]
        let endpoint = runtime
            .join("index.sock")
            .to_str()
            .ok_or_else(|| ProtocolError::new(ErrorCode::InvalidRoot, "Runtime path is not UTF-8"))?
            .to_owned();
        Ok(Self {
            data,
            runtime,
            endpoint,
        })
    }
    pub fn lock(&self) -> Result<File> {
        let file = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(false)
            .open(self.runtime.join("owner.lock"))
            .map_err(io_error)?;
        file.try_lock_exclusive()
            .map_err(|error| ProtocolError::new(ErrorCode::InstanceConflict, error.to_string()))?;
        Ok(file)
    }
    /// Call under the exclusive environment lock on first initialization.
    pub fn environment_id(&self) -> Result<String> {
        let path = self.data.join("environment-id");
        if path.exists() {
            let value = fs::read_to_string(path).map_err(io_error)?;
            if !crate::protocol::valid_uuid(&value) {
                return Err(ProtocolError::new(
                    ErrorCode::StorageCorrupt,
                    "Invalid environment identity",
                ));
            }
            return Ok(value);
        }
        let id = uuid::Uuid::new_v4().to_string();
        atomic_write(&path, id.as_bytes())?;
        Ok(id)
    }
}

pub fn atomic_write(path: &Path, bytes: &[u8]) -> Result<()> {
    use std::io::Write;
    let temporary = path.with_extension(format!("{}.tmp", uuid::Uuid::new_v4()));
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&temporary)
        .map_err(io_error)?;
    file.write_all(bytes).map_err(io_error)?;
    file.sync_all().map_err(io_error)?;
    drop(file);
    fs::rename(&temporary, path).map_err(io_error)?;
    #[cfg(unix)]
    if let Some(parent) = path.parent() {
        File::open(parent)
            .and_then(|file| file.sync_all())
            .map_err(io_error)?;
    }
    Ok(())
}

pub fn canonical_root(root: &Path, wsl: bool) -> Result<PathBuf> {
    if !root.is_absolute() {
        return Err(ProtocolError::new(
            ErrorCode::InvalidRoot,
            "Root must be absolute",
        ));
    }
    #[cfg(windows)]
    {
        let text = root.to_string_lossy();
        if text.starts_with(r"\\") && !text.starts_with(r"\\?\") || text.starts_with(r"\\?\UNC\") {
            return Err(ProtocolError::new(
                ErrorCode::InvalidRoot,
                "Network roots are unsupported",
            ));
        }
    }
    if wsl
        && root
            .components()
            .nth(1)
            .is_some_and(|p| p.as_os_str() == "mnt")
        && root
            .components()
            .nth(2)
            .is_some_and(|p| p.as_os_str().len() == 1)
    {
        return Err(ProtocolError::new(
            ErrorCode::InvalidRoot,
            "Windows-mounted WSL roots are unsupported",
        ));
    }
    let canonical = fs::canonicalize(root)
        .map_err(|error| ProtocolError::new(ErrorCode::InvalidRoot, error.to_string()))?;
    if !canonical.is_dir() {
        return Err(ProtocolError::new(
            ErrorCode::InvalidRoot,
            "Root is not a directory",
        ));
    }
    Ok(canonical)
}

pub fn reject_overlap(root: &Path, others: &[PathBuf]) -> Result<()> {
    for other in others {
        for ancestor in root.ancestors() {
            if same_file::is_same_file(ancestor, other).map_err(io_error)? {
                return Err(ProtocolError::new(
                    ErrorCode::RootOverlap,
                    "Root overlaps an existing project",
                ));
            }
        }
        for ancestor in other.ancestors() {
            if same_file::is_same_file(ancestor, root).map_err(io_error)? {
                return Err(ProtocolError::new(
                    ErrorCode::RootOverlap,
                    "Root overlaps an existing project",
                ));
            }
        }
    }
    Ok(())
}

pub fn private_directory(path: &Path) -> Result<()> {
    if fs::symlink_metadata(path).is_ok_and(|m| m.file_type().is_symlink()) {
        return Err(ProtocolError::new(
            ErrorCode::AccessDenied,
            "Private directory cannot be a symlink",
        ));
    }
    fs::create_dir_all(path).map_err(io_error)?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::{MetadataExt, PermissionsExt};
        let metadata = fs::symlink_metadata(path).map_err(io_error)?;
        if metadata.uid() != unsafe { libc::geteuid() } {
            return Err(ProtocolError::new(
                ErrorCode::AccessDenied,
                "Private directory has another owner",
            ));
        }
        fs::set_permissions(path, fs::Permissions::from_mode(0o700)).map_err(io_error)?;
    }
    #[cfg(windows)]
    windows::secure_directory(path)?;
    Ok(())
}

pub fn current_identity() -> Result<String> {
    #[cfg(windows)]
    {
        windows::identity(false)
    }
    #[cfg(unix)]
    {
        Ok(unsafe { libc::geteuid() }.to_string())
    }
}

#[cfg(windows)]
pub mod windows {
    use super::*;
    use std::os::windows::ffi::OsStrExt;
    use windows_sys::Win32::{
        Foundation::*, Security::Authorization::*, Security::*, System::Threading::*,
    };

    pub struct DetachedChild(HANDLE);
    impl DetachedChild {
        pub fn try_wait(&mut self) -> std::io::Result<Option<i32>> {
            unsafe {
                if WaitForSingleObject(self.0, 0) == WAIT_TIMEOUT {
                    return Ok(None);
                }
                let mut code = 0;
                if GetExitCodeProcess(self.0, &mut code) == 0 {
                    return Err(std::io::Error::last_os_error());
                }
                Ok(Some(code as i32))
            }
        }
    }
    impl Drop for DetachedChild {
        fn drop(&mut self) {
            unsafe {
                CloseHandle(self.0);
            }
        }
    }
    /// A fixed executable with no inherited handles or shell interpretation.
    pub fn spawn_detached(executable: &Path) -> Result<DetachedChild> {
        unsafe {
            let application = wide(executable);
            let mut command = wide(format!("\"{}\"", executable.display()));
            let mut startup: STARTUPINFOW = std::mem::zeroed();
            startup.cb = std::mem::size_of::<STARTUPINFOW>() as u32;
            let mut process: PROCESS_INFORMATION = std::mem::zeroed();
            if CreateProcessW(
                application.as_ptr(),
                command.as_mut_ptr(),
                std::ptr::null(),
                std::ptr::null(),
                0,
                CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP,
                std::ptr::null(),
                std::ptr::null(),
                &startup,
                &mut process,
            ) == 0
            {
                return Err(io_error(std::io::Error::last_os_error()));
            }
            CloseHandle(process.hThread);
            Ok(DetachedChild(process.hProcess))
        }
    }

    pub fn wide(value: impl AsRef<std::ffi::OsStr>) -> Vec<u16> {
        value.as_ref().encode_wide().chain(Some(0)).collect()
    }
    pub fn identity(thread: bool) -> Result<String> {
        unsafe {
            let mut token = std::ptr::null_mut();
            let opened = if thread {
                OpenThreadToken(GetCurrentThread(), TOKEN_QUERY, 1, &mut token)
            } else {
                OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &mut token)
            };
            if opened == 0 {
                return Err(io_error(std::io::Error::last_os_error()));
            }
            let result = token_identity(token);
            CloseHandle(token);
            result
        }
    }
    unsafe fn token_identity(token: HANDLE) -> Result<String> {
        unsafe {
            let mut needed = 0;
            GetTokenInformation(token, TokenUser, std::ptr::null_mut(), 0, &mut needed);
            let mut buffer = vec![0usize; (needed as usize).div_ceil(std::mem::size_of::<usize>())];
            if GetTokenInformation(
                token,
                TokenUser,
                buffer.as_mut_ptr().cast(),
                needed,
                &mut needed,
            ) == 0
            {
                return Err(io_error(std::io::Error::last_os_error()));
            }
            let user = &*(buffer.as_ptr().cast::<TOKEN_USER>());
            let mut sid = std::ptr::null_mut();
            if ConvertSidToStringSidW(user.User.Sid, &mut sid) == 0 {
                return Err(io_error(std::io::Error::last_os_error()));
            }
            let mut length = 0;
            while *sid.add(length) != 0 {
                length += 1;
            }
            let value = String::from_utf16_lossy(std::slice::from_raw_parts(sid, length));
            LocalFree(sid.cast());
            Ok(value)
        }
    }
    pub struct SecurityDescriptor(pub PSECURITY_DESCRIPTOR);
    impl SecurityDescriptor {
        pub fn new(inherit: bool) -> Result<Self> {
            let flags = if inherit { "OICI" } else { "" };
            let descriptor = wide(format!(
                "D:P(A;{flags};GA;;;{})(A;{flags};GA;;;SY)(A;{flags};GA;;;BA)",
                current_identity()?
            ));
            let mut pointer = std::ptr::null_mut();
            if unsafe {
                ConvertStringSecurityDescriptorToSecurityDescriptorW(
                    descriptor.as_ptr(),
                    1,
                    &mut pointer,
                    std::ptr::null_mut(),
                )
            } == 0
            {
                return Err(io_error(std::io::Error::last_os_error()));
            }
            Ok(Self(pointer))
        }
    }
    impl Drop for SecurityDescriptor {
        fn drop(&mut self) {
            unsafe {
                LocalFree(self.0);
            }
        }
    }
    pub fn secure_directory(path: &Path) -> Result<()> {
        use std::os::windows::fs::MetadataExt;
        if fs::symlink_metadata(path)
            .map_err(io_error)?
            .file_attributes()
            & 0x400
            != 0
        {
            return Err(ProtocolError::new(
                ErrorCode::AccessDenied,
                "Private directory cannot be a reparse point",
            ));
        }
        let descriptor = SecurityDescriptor::new(true)?;
        if unsafe {
            SetFileSecurityW(
                wide(path).as_ptr(),
                DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION,
                descriptor.0,
            )
        } == 0
        {
            return Err(io_error(std::io::Error::last_os_error()));
        }
        Ok(())
    }

    #[cfg(test)]
    mod repair_tests {
        include!("../tests/unit/platform_windows.rs");
    }
}
