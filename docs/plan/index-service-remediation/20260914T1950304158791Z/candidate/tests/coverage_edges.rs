//! Contract-derived boundary and recovery checks for previously unexecuted paths.
use devforgeai_index::{
    index, platform,
    protocol::{ErrorCode, ProjectConfig},
    storage::{Store, StoredFile},
};
use serde_json::json;
use std::{
    fs,
    sync::{Arc, atomic::AtomicBool},
};

#[test]
fn enumeration_configuration_and_capture_failures_have_named_outcomes() {
    let root = tempfile::tempdir().unwrap();
    let no = AtomicBool::new(false);
    assert_eq!(
        index::enumerate(&root.path().join("missing"), &ProjectConfig::default(), &[]).unwrap_err(),
        "root_unavailable"
    );
    fs::write(root.path().join(".gitignore"), "[z-a]").unwrap();
    assert!(index::enumerate(root.path(), &ProjectConfig::default(), &[]).is_err());
    fs::remove_file(root.path().join(".gitignore")).unwrap();
    let bad = ProjectConfig {
        exclusions: Some(vec!["[z-a]".into()]),
        ..Default::default()
    };
    assert!(index::enumerate(root.path(), &bad, &[]).is_err());
    fs::create_dir(root.path().join("cache")).unwrap();
    fs::create_dir(root.path().join("nested")).unwrap();
    for name in [
        "nested/file.py",
        "readme",
        "yes.custom",
        "skip.py",
        "cache/data.txt",
    ] {
        fs::write(root.path().join(name), b"hello").unwrap();
    }
    let config = ProjectConfig {
        exclusions: Some(vec!["skip.py".into()]),
        text_names: Some(vec!["readme".into()]),
        text_extensions: Some(vec![".custom".into()]),
        ..Default::default()
    };
    let cache = fs::canonicalize(root.path().join("cache")).unwrap();
    let files = index::enumerate(root.path(), &config, &[&cache]).unwrap();
    for name in ["readme", "yes.custom", "nested/file.py"] {
        assert_eq!(
            files.iter().find(|f| f.path == name).unwrap().disposition,
            index::FileDisposition::Eligible
        );
    }
    assert_eq!(
        files
            .iter()
            .find(|f| f.path == "skip.py")
            .unwrap()
            .disposition,
        index::FileDisposition::Excluded("project_rule".into())
    );
    assert_eq!(
        files
            .iter()
            .find(|f| f.path == "cache")
            .unwrap()
            .disposition,
        index::FileDisposition::Excluded("mandatory".into())
    );
    assert_eq!(
        index::capture(root.path(), "nested/file.py", 5, &no)
            .unwrap()
            .bytes,
        b"hello"
    );
    assert_eq!(
        index::capture(root.path(), "missing", 5, &no).unwrap_err(),
        "file_unavailable"
    );
    assert!(index::capture(root.path(), "nested", 5, &no).is_err());
    assert_eq!(
        index::capture(root.path(), "../escape", 5, &no).unwrap_err(),
        "path_outside_project"
    );
    assert_eq!(
        index::capture(root.path(), "readme", 5, &AtomicBool::new(true)).unwrap_err(),
        "cancelled"
    );
    fs::write(root.path().join("invalid.txt"), [0xff, 0x80]).unwrap();
    assert_eq!(
        index::capture(root.path(), "invalid.txt", 5, &no).unwrap_err(),
        "unsupported_encoding"
    );
    let mut pool = index::ParsePool::new().unwrap();
    let snapshot = index::Snapshot {
        bytes: vec![b'x'; 50 * 1024 * 1024 + 1],
        sha256: "unused because rejected before parsing".into(),
    };
    assert_eq!(
        pool.parse("txt", snapshot, Arc::new(AtomicBool::new(false)))
            .unwrap_err(),
        "oversized"
    );
}

#[test]
fn extraction_keeps_import_ranges_and_interrupts_long_parser_work() {
    use std::sync::atomic::Ordering;
    for (extension, source, import) in [
        ("py", "import os\ndef f():\n    pass\n", "import os"),
        ("rs", "use std::io;\n// ordinary\nfn f() {}", "use std::io;"),
        (
            "js",
            "import x from 'x';\nfunction f() {}",
            "import x from 'x';",
        ),
    ] {
        let result = index::extract(extension, source.as_bytes(), &AtomicBool::new(false)).unwrap();
        assert!(
            result
                .imports
                .iter()
                .any(|r| &source[r.start..r.end] == import)
        );
        assert!(
            result
                .declarations
                .iter()
                .find(|d| d.name.as_deref() == Some("f"))
                .unwrap()
                .documentation
                .is_empty()
        );
    }
    let source = "x = (1 + 2)\n".repeat(2_000_000);
    let cancelled = Arc::new(AtomicBool::new(false));
    let worker_flag = cancelled.clone();
    let worker = std::thread::spawn(move || index::extract("py", source.as_bytes(), &worker_flag));
    std::thread::sleep(std::time::Duration::from_millis(30));
    cancelled.store(true, Ordering::Release);
    assert_eq!(worker.join().unwrap().unwrap_err(), "cancelled");
}

#[test]
fn slow_parser_work_has_a_cooperative_deadline() {
    let source = "x = (1 + 2)\n".repeat(3_000_000);
    let started = std::time::Instant::now();
    assert_eq!(
        index::extract("py", source.as_bytes(), &AtomicBool::new(false)).unwrap_err(),
        "parse_timeout"
    );
    assert!(started.elapsed() < std::time::Duration::from_secs(5));
}

#[test]
fn disappearing_entry_is_accounted_as_a_metadata_failure() {
    let root = tempfile::tempdir().unwrap();
    let file = root.path().join("vanishing.txt");
    fs::write(&file, b"before").unwrap();
    let checks = std::cell::Cell::new(0);
    let entries = index::enumerate_controlled(root.path(), &ProjectConfig::default(), &[], &|| {
        checks.set(checks.get() + 1);
        if checks.get() == 2 {
            fs::remove_file(&file).unwrap();
        }
        Ok(())
    })
    .unwrap();
    assert_eq!(entries.len(), 1);
    assert_eq!(entries[0].path, "vanishing.txt");
    assert_eq!(
        entries[0].disposition,
        index::FileDisposition::Error("metadata_unavailable".into())
    );
}

#[cfg(windows)]
#[test]
fn non_unicode_windows_filename_is_skipped_with_a_reason() {
    use std::os::windows::ffi::OsStringExt;
    let root = tempfile::tempdir().unwrap();
    let name = std::ffi::OsString::from_wide(&[0xd800, 0x2e, 0x74, 0x78, 0x74]);
    fs::write(root.path().join(name), b"unrepresentable path").unwrap();
    let entries = index::enumerate(root.path(), &ProjectConfig::default(), &[]).unwrap();
    assert_eq!(entries.len(), 1);
    assert_eq!(
        entries[0].disposition,
        index::FileDisposition::Skipped("non_utf8_path".into())
    );
}

#[cfg(windows)]
#[test]
fn native_junctions_are_never_traversed_or_used_as_private_directories() {
    let fixture = tempfile::tempdir().unwrap();
    let project = fixture.path().join("project");
    let outside = fixture.path().join("outside");
    fs::create_dir(&project).unwrap();
    fs::create_dir(&outside).unwrap();
    fs::write(outside.join("secret.txt"), b"outside").unwrap();
    let link = project.join("junction");
    let output = std::process::Command::new("cmd.exe")
        .args(["/D", "/C", "mklink", "/J"])
        .arg(&link)
        .arg(&outside)
        .output()
        .unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let result = index::enumerate(&project, &ProjectConfig::default(), &[]).unwrap();
    assert_eq!(result.len(), 1);
    assert_eq!(
        result[0].disposition,
        index::FileDisposition::Skipped("directory_link".into())
    );
    assert_eq!(
        platform::private_directory(&link).unwrap_err().code,
        ErrorCode::AccessDenied
    );
    assert_eq!(
        platform::windows::secure_directory(&link).unwrap_err().code,
        ErrorCode::AccessDenied
    );
    assert_eq!(
        index::capture(&project, "junction/secret.txt", 10, &AtomicBool::new(false)).unwrap_err(),
        "path_outside_project"
    );
    assert_eq!(fs::read(outside.join("secret.txt")).unwrap(), b"outside");
}

#[test]
fn schema_zero_backup_and_corrupt_cached_records_are_explicit() {
    let data = tempfile::tempdir().unwrap();
    let path = data.path().join("index.sqlite3");
    let old = rusqlite::Connection::open(&path).unwrap();
    old.execute_batch("CREATE TABLE old_metadata(value TEXT); INSERT INTO old_metadata VALUES('preserve'); PRAGMA user_version=0;").unwrap();
    drop(old);
    let original = fs::read(&path).unwrap();
    let mut store = Store::open(data.path()).unwrap();
    let backup = fs::read_dir(data.path())
        .unwrap()
        .map(|e| e.unwrap().path())
        .find(|p| {
            p.file_name()
                .unwrap()
                .to_string_lossy()
                .starts_with("schema-backup-")
        })
        .unwrap();
    assert_eq!(fs::read(backup).unwrap(), original);
    store.begin_generation("p", "g").unwrap();
    assert_eq!(
        store.begin_generation("p", "g").unwrap_err().code,
        ErrorCode::InternalError
    );
    let file = StoredFile {
        path: "test.txt".into(),
        bytes: Some(b"abc".to_vec()),
        sha256: Some(index::digest(b"abc")),
        record: json!({"state":"indexed"}),
    };
    store.stage_file("g", &file).unwrap();
    store
        .publish("p", "g", &json!({"coverage":"complete"}))
        .unwrap();
    assert_eq!(
        store
            .cached_file("g", "test.txt", &index::digest(b"abc"))
            .unwrap(),
        Some(json!({"state":"indexed"}))
    );
    let corrupt = rusqlite::Connection::open(&path).unwrap();
    corrupt
        .execute("UPDATE files SET record='broken'", [])
        .unwrap();
    corrupt
        .execute("UPDATE generations SET summary='broken'", [])
        .unwrap();
    assert_eq!(
        store
            .cached_file("g", "test.txt", &index::digest(b"abc"))
            .unwrap_err()
            .code,
        ErrorCode::StorageCorrupt
    );
    assert_eq!(
        store.summary("p").unwrap_err().code,
        ErrorCode::StorageCorrupt
    );
    assert_eq!(store.cached_file("g", "missing", "x").unwrap(), None);
    drop(store);
    drop(corrupt);
    assert!(
        matches!(Store::open(&data.path().join("missing")), Err(error) if error.code == ErrorCode::InternalError)
    );
}

#[test]
fn sqlite_integrity_failure_is_not_treated_as_a_migration_candidate() {
    let data = tempfile::tempdir().unwrap();
    let database = data.path().join("index.sqlite3");
    let connection = rusqlite::Connection::open(&database).unwrap();
    connection.execute_batch("PRAGMA ignore_check_constraints=ON; CREATE TABLE invalid_state(x INTEGER CHECK (x>0)); INSERT INTO invalid_state VALUES(-1);").unwrap();
    drop(connection);
    let original = fs::read(&database).unwrap();
    assert!(
        matches!(Store::open(data.path()), Err(error) if error.code == ErrorCode::StorageCorrupt)
    );
    assert_eq!(fs::read(&database).unwrap(), original);
    let empty = tempfile::tempdir().unwrap();
    assert_eq!(
        Store::open(empty.path())
            .unwrap()
            .replay_request("absent", "data", 0)
            .unwrap(),
        None
    );
}

#[cfg(windows)]
#[test]
fn preferences_read_errors_never_modify_startup_configuration() {
    let data = tempfile::tempdir().unwrap();
    let paths = platform::Paths::at(data.path().to_owned()).unwrap();
    let file = paths.data.join("tray-settings.json");
    fs::write(&file, b"{malformed").unwrap();
    assert_eq!(
        devforgeai_index::tray::preferences(&paths)
            .unwrap_err()
            .code,
        ErrorCode::InvalidArgument
    );
    fs::write(
        &file,
        br#"{"launch_at_sign_in":false,"start_local_daemon":true}"#,
    )
    .unwrap();
    let prefs = devforgeai_index::tray::preferences(&paths).unwrap();
    assert!(!prefs.launch_at_sign_in);
    assert!(prefs.start_local_daemon);
    // Only an isolated application fixture preference; launch=None never calls the Run key API.
    let saved = devforgeai_index::tray::set_preferences(&paths, None, Some(false)).unwrap();
    assert!(!saved.launch_at_sign_in);
    assert!(!saved.start_local_daemon);
    let reread = devforgeai_index::tray::set_preferences(&paths, None, None).unwrap();
    assert!(!reread.start_local_daemon);
    fs::remove_file(&file).unwrap();
    fs::create_dir(&file).unwrap();
    assert!(devforgeai_index::tray::preferences(&paths).is_err());
}
