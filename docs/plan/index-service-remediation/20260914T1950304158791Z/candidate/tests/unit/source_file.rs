use super::*;

#[test]
fn source_parent_guards_reject_escape_and_non_directory_components() {
    let root = tempfile::tempdir().unwrap();
    let canonical = fs::canonicalize(root.path()).unwrap();
    fs::write(root.path().join("file.txt"), b"file").unwrap();
    assert!(
        matches!(open(&canonical, "../escape.txt"), Err(error) if error == "path_outside_project")
    );
    assert!(open(&canonical, "missing/file.txt").is_err());
    assert!(
        matches!(open(&canonical, "file.txt/child"), Err(error) if error == "directory_link_or_unavailable")
    );
    #[cfg(windows)]
    {
        let outside = tempfile::tempdir().unwrap();
        let file = outside.path().join("other.txt");
        fs::write(&file, b"outside").unwrap();
        assert!(
            matches!(open_leaf(&canonical, &file), Err(error) if error == "path_outside_project")
        );
    }
}
