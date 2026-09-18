use devforgeai_index::index::{FileDisposition, capture, enumerate, extract};
use devforgeai_index::protocol::ProjectConfig;
use std::fs;
use std::sync::atomic::AtomicBool;
use tempfile::tempdir;

#[cfg(unix)]
#[test]
fn capture_rejects_directory_links_and_outside_targets_but_allows_internal_file_links() {
    use std::os::unix::fs::symlink;
    let directory = tempdir().unwrap();
    let outside = tempdir().unwrap();
    fs::create_dir(directory.path().join("real")).unwrap();
    fs::write(directory.path().join("real/item.py"), "def inside(): pass").unwrap();
    fs::write(outside.path().join("secret.py"), "secret").unwrap();
    symlink(
        directory.path().join("real"),
        directory.path().join("alias"),
    )
    .unwrap();
    symlink(
        outside.path().join("secret.py"),
        directory.path().join("outside.py"),
    )
    .unwrap();
    symlink(
        directory.path().join("real/item.py"),
        directory.path().join("inside.py"),
    )
    .unwrap();
    let cancelled = AtomicBool::new(false);
    assert!(
        capture(directory.path(), "alias/item.py", 1024, &cancelled).is_err(),
        "Directory links must never be traversed, even within the root"
    );
    assert!(capture(directory.path(), "outside.py", 1024, &cancelled).is_err());
    assert_eq!(
        capture(directory.path(), "inside.py", 1024, &cancelled)
            .unwrap()
            .bytes,
        b"def inside(): pass"
    );
}

#[test]
fn eligibility_accounts_for_exclusions_encodings_and_untracked_files() {
    let directory = tempdir().unwrap();
    let root = directory.path();
    fs::create_dir(root.join(".git")).unwrap();
    fs::write(root.join(".gitignore"), "ignored.py\n").unwrap();
    for (path, bytes) in [
        ("main.py", &b"def work():\n    return 1\n"[..]),
        ("readme.md", &b"text"[..]),
        (".env", &b"secret"[..]),
        ("private.key", &b"secret"[..]),
        ("ignored.py", &b"pass"[..]),
        ("binary.py", &[0, 1][..]),
        ("utf16.txt", &[255, 254, 65, 0][..]),
        ("other.xyz", &b"unknown"[..]),
        ("bom.txt", &[239, 187, 191, 65][..]),
    ] {
        fs::write(root.join(path), bytes).unwrap();
    }
    fs::create_dir(root.join("node_modules")).unwrap();
    fs::write(root.join("node_modules/dependency.js"), "export {};").unwrap();
    let files = enumerate(root, &ProjectConfig::default(), &[]).unwrap();
    let status = |name: &str| {
        files
            .iter()
            .find(|f| f.path == name)
            .unwrap()
            .disposition
            .clone()
    };
    assert_eq!(status("main.py"), FileDisposition::Eligible);
    assert_eq!(status("readme.md"), FileDisposition::Eligible);
    for path in [".env", "private.key", "ignored.py", "node_modules"] {
        assert!(matches!(status(path), FileDisposition::Excluded(_)));
    }
    let cancellation = AtomicBool::new(false);
    for (name, reason) in [
        ("binary.py", "binary"),
        ("utf16.txt", "unsupported_encoding"),
        ("other.xyz", "unsupported_extension"),
    ] {
        if name == "other.xyz" {
            assert_eq!(status(name), FileDisposition::Skipped(reason.into()));
        } else {
            assert_eq!(
                capture(root, name, 5 * 1024 * 1024, &cancellation).unwrap_err(),
                reason
            );
        }
    }
    assert_eq!(
        capture(root, "bom.txt", 1024, &cancellation).unwrap().bytes,
        [239, 187, 191, 65]
    );
    assert_eq!(
        capture(root, "main.py", 2, &cancellation).unwrap_err(),
        "oversized"
    );
    assert_eq!(
        capture(root, "../escape", 1024, &cancellation).unwrap_err(),
        "path_outside_project"
    );
}

#[test]
fn adapters_extract_real_declarations_docs_and_exact_source_ranges() {
    let fixtures = [
        (
            "rs",
            "/// useful documentation\nfn work() { helper(); }\n",
            "rust",
        ),
        (
            "py",
            "def work():\n    \"\"\"useful documentation\"\"\"\n    helper()\n",
            "python",
        ),
        (
            "js",
            "/** useful documentation */\nfunction work() { helper(); }\n",
            "javascript",
        ),
        ("jsx", "function work() { return <div/>; }\n", "javascript"),
        (
            "ts",
            "/** useful documentation */\nfunction work(): void { helper(); }\n",
            "typescript",
        ),
        ("tsx", "function work() { return <div/>; }\n", "typescript"),
    ];
    for (extension, text, language) in fixtures {
        let parsed = extract(extension, text.as_bytes(), &AtomicBool::new(false)).unwrap();
        assert_eq!(parsed.language, language);
        assert!(!parsed.partial, "{extension}");
        let work = parsed
            .declarations
            .iter()
            .find(|s| s.name.as_deref() == Some("work"))
            .unwrap();
        assert!(text[work.range.start..work.range.end].contains("work"));
        if text.contains("useful documentation") {
            assert!(
                work.documentation
                    .iter()
                    .any(|range| text[range.start..range.end].contains("useful documentation")),
                "{extension}"
            );
        }
        if text.contains("helper") {
            assert!(parsed.calls.iter().any(|c| c.name == "helper"));
        }
    }
}

#[test]
fn syntax_errors_are_partial_and_cancellation_is_observed() {
    let parsed = extract(
        "py",
        b"def good():\n    return 1\ndef broken(:\n",
        &AtomicBool::new(false),
    )
    .unwrap();
    assert!(parsed.partial);
    assert!(
        parsed
            .declarations
            .iter()
            .any(|s| s.name.as_deref() == Some("good"))
    );
    assert_eq!(
        extract("rs", b"fn work() {}", &AtomicBool::new(true)).unwrap_err(),
        "cancelled"
    );
}

#[test]
fn file_header_is_not_documentation_and_nested_parent_is_retained() {
    let text = b"# file header\n\nclass Outer:\n    def method(self):\n        # internal note\n        return lambda: 1\n";
    let parsed = extract("py", text, &AtomicBool::new(false)).unwrap();
    let outer = parsed
        .declarations
        .iter()
        .find(|s| s.name.as_deref() == Some("Outer"))
        .unwrap();
    assert!(outer.documentation.is_empty());
    let method = parsed
        .declarations
        .iter()
        .find(|s| s.name.as_deref() == Some("method"))
        .unwrap();
    assert_eq!(method.parent, Some(outer.id));
    assert!(!method.comments.is_empty());
    assert!(parsed.declarations.iter().any(|s| s.name.is_none()));
}

#[test]
fn enumeration_observes_cooperative_stop_between_entries() {
    let directory = tempdir().unwrap();
    for i in 0..20 {
        fs::write(directory.path().join(format!("file{i}.txt")), "text").unwrap();
    }
    let calls = std::cell::Cell::new(0);
    let result = devforgeai_index::index::enumerate_controlled(
        directory.path(),
        &ProjectConfig::default(),
        &[],
        &|| {
            calls.set(calls.get() + 1);
            if calls.get() > 3 {
                Err("cancelled".into())
            } else {
                Ok(())
            }
        },
    );
    assert_eq!(result.unwrap_err(), "cancelled");
    assert_eq!(calls.get(), 4);
}

#[test]
fn two_parser_workers_preserve_snapshot_bytes_and_cancellation() {
    let mut pool = devforgeai_index::index::ParsePool::new().unwrap();
    let mut workers = std::collections::BTreeSet::new();
    for _ in 0..4 {
        let bytes = b"fn original() {}".to_vec();
        let snapshot = devforgeai_index::index::Snapshot {
            sha256: devforgeai_index::index::digest(&bytes),
            bytes: bytes.clone(),
        };
        let (snapshot, result, worker) = pool
            .parse("rs", snapshot, std::sync::Arc::new(AtomicBool::new(false)))
            .unwrap();
        assert_eq!(snapshot.bytes, bytes);
        assert_eq!(
            result.unwrap().declarations[0].name.as_deref(),
            Some("original")
        );
        workers.insert(worker);
    }
    assert_eq!(workers.len(), 2);
}
