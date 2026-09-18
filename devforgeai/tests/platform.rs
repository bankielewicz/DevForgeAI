use devforgeai_index::platform::{Paths, canonical_root, reject_overlap};
use std::fs;
use tempfile::tempdir;

#[test]
fn roots_are_absolute_local_and_nonoverlapping() {
    let temp = tempdir().unwrap();
    let root = temp.path();
    fs::create_dir(root.join("nested")).unwrap();
    let canonical = canonical_root(root, false).unwrap();
    assert!(canonical_root(std::path::Path::new("relative"), false).is_err());
    assert!(reject_overlap(&canonical, std::slice::from_ref(&canonical)).is_err());
    assert!(
        reject_overlap(
            &canonical_root(&root.join("nested"), false).unwrap(),
            &[canonical]
        )
        .is_err()
    );
    #[cfg(windows)]
    assert!(canonical_root(std::path::Path::new(r"\\server\share"), false).is_err());
}

#[test]
fn private_environment_identity_and_exclusive_lock_survive_reopen() {
    let temp = tempdir().unwrap();
    let paths = Paths::at(temp.path().join("private")).unwrap();
    let owner = paths.lock().unwrap();
    assert!(paths.lock().is_err());
    let identity = paths.environment_id().unwrap();
    assert!(devforgeai_index::protocol::valid_uuid(&identity));
    assert_eq!(paths.environment_id().unwrap(), identity);
    drop(owner);
    assert!(paths.lock().is_ok());
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        assert_eq!(
            fs::metadata(&paths.data).unwrap().permissions().mode() & 0o777,
            0o700
        );
    }
}

#[test]
fn invalid_roots_identity_and_atomic_write_errors_are_explicit() {
    use devforgeai_index::{platform, protocol::ErrorCode};
    use std::path::{Path, PathBuf};
    let temp = tempdir().unwrap();
    assert_eq!(
        Paths::at(PathBuf::from("relative")).unwrap_err().code,
        ErrorCode::InvalidRoot
    );
    let file = temp.path().join("file");
    fs::write(&file, b"first").unwrap();
    assert_eq!(
        canonical_root(&file, false).unwrap_err().code,
        ErrorCode::InvalidRoot
    );
    assert_eq!(
        canonical_root(&temp.path().join("missing"), false)
            .unwrap_err()
            .code,
        ErrorCode::InvalidRoot
    );
    assert!(platform::private_directory(&file).is_err());
    platform::atomic_write(&file, b"second").unwrap();
    assert_eq!(fs::read(&file).unwrap(), b"second");
    assert!(platform::atomic_write(&temp.path().join("absent/file"), b"not written").is_err());
    let paths = Paths::at(temp.path().join("data")).unwrap();
    fs::write(paths.data.join("environment-id"), "not-a-uuid").unwrap();
    assert_eq!(
        paths.environment_id().unwrap_err().code,
        ErrorCode::StorageCorrupt
    );
    let nested = paths.data.join("child");
    fs::create_dir(&nested).unwrap();
    assert_eq!(
        reject_overlap(&paths.data, &[nested]).unwrap_err().code,
        ErrorCode::RootOverlap
    );
    assert_eq!(
        platform::io_error(std::io::Error::from(std::io::ErrorKind::PermissionDenied)).code,
        ErrorCode::AccessDenied
    );
    assert_eq!(
        platform::io_error(std::io::Error::from(std::io::ErrorKind::NotFound)).code,
        ErrorCode::InternalError
    );
    assert!(reject_overlap(&temp.path().join("missing"), &[temp.path().to_owned()]).is_err());
    #[cfg(windows)]
    {
        assert_eq!(
            canonical_root(Path::new(r"\\?\UNC\server\share"), false)
                .unwrap_err()
                .code,
            ErrorCode::InvalidRoot
        );
        assert!(platform::windows::spawn_detached(&temp.path().join("absent.exe")).is_err());
        assert!(
            platform::windows::identity(true).is_err(),
            "fixture thread is not impersonating"
        );
        assert!(platform::windows::secure_directory(&temp.path().join("missing")).is_err());
    }
}
