//! Independent QA; specification-derived fixtures, no product repair.
use devforgeai_index::index::{FileDisposition, capture, enumerate, extract};
use devforgeai_index::protocol::{
    ErrorCode, ProjectConfig, REQUEST_LIMIT, RESPONSE_LIMIT, Request, Response, read_frame,
    write_frame,
};
use devforgeai_index::storage::{Store, StoredFile};
use serde_json::json;
use std::{fs, io::Cursor, sync::atomic::AtomicBool};

#[test]
fn qa_u01_bom_preserves_original_byte_coordinates() {
    let bytes = b"\xef\xbb\xbffn apple() {}";
    let parsed = extract("rs", bytes, &AtomicBool::new(false)).unwrap();
    let decl = parsed
        .declarations
        .iter()
        .find(|d| d.name.as_deref() == Some("apple"))
        .unwrap();
    assert_eq!((decl.range.start, decl.range.end), (3, 16));
    assert_eq!(&bytes[decl.range.start..decl.range.end], b"fn apple() {}");
}
#[test]
fn qa_u02_all_structural_extension_aliases_capture_named_function() {
    for (ext, source, language) in [
        ("rs", "fn item() {}", "rust"),
        ("py", "def item(): pass", "python"),
        ("pyi", "def item(): ...", "python"),
        ("js", "function item() {}", "javascript"),
        ("jsx", "function item() { return <p/>; }", "javascript"),
        ("mjs", "function item() {}", "javascript"),
        ("cjs", "function item() {}", "javascript"),
        ("ts", "function item(): void {}", "typescript"),
        ("tsx", "function item() { return <p/>; }", "typescript"),
        ("mts", "function item(): void {}", "typescript"),
        ("cts", "function item(): void {}", "typescript"),
    ] {
        let p = extract(ext, source.as_bytes(), &AtomicBool::new(false)).unwrap();
        assert_eq!(p.language, language, "{ext}");
        assert!(!p.partial, "{ext}");
        let d = p
            .declarations
            .iter()
            .find(|d| d.name.as_deref() == Some("item"))
            .unwrap();
        assert_eq!(
            &source.as_bytes()[d.range.start..d.range.end],
            source.as_bytes(),
            "{ext}"
        );
    }
}
#[test]
fn qa_u03_python_docstring_and_method_ranges_are_exact() {
    let source = b"class C:\n    def f(self):\n        \"\"\"docs\"\"\"\n        return 1\n";
    let p = extract("py", source, &AtomicBool::new(false)).unwrap();
    let d = p
        .declarations
        .iter()
        .find(|d| d.name.as_deref() == Some("f"))
        .unwrap();
    assert_eq!(d.kind, "method");
    assert_eq!(d.documentation.len(), 1);
    assert_eq!(
        &source[d.documentation[0].start..d.documentation[0].end],
        b"\"\"\"docs\"\"\""
    );
    assert_eq!(
        &source[d.range.start..d.range.end],
        b"def f(self):\n        \"\"\"docs\"\"\"\n        return 1"
    );
    let parent = d.parent.unwrap();
    assert_eq!(p.declarations[parent].name.as_deref(), Some("C"));
}
#[test]
fn qa_u04_full_protocol_frame_limits_and_negative_headers() {
    for limit in [REQUEST_LIMIT, RESPONSE_LIMIT] {
        let data = vec![b'x'; limit];
        let mut wire = vec![];
        write_frame(&mut wire, &data, limit).unwrap();
        assert_eq!(&wire[..4], &(limit as u32).to_be_bytes());
        assert_eq!(read_frame(&mut Cursor::new(wire), limit).unwrap(), data);
        assert!(read_frame(&mut Cursor::new(((limit + 1) as u32).to_be_bytes()), limit).is_err());
        assert!(write_frame(&mut vec![], &vec![0; limit + 1], limit).is_err());
    }
}
#[test]
fn qa_u05_protocol_rejects_extra_fields_and_accepts_budget_edges() {
    for budget in [99, 100, 120000, 120001] {
        let value = json!({"protocol_version":1,"request_id":"550e8400-e29b-41d4-a716-446655440000","operation":"daemon.status","params":{},"timeout_ms":budget});
        assert_eq!(
            Request::decode(&serde_json::to_vec(&value).unwrap()).is_ok(),
            (100..=120000).contains(&budget)
        );
    }
    let value = json!({"protocol_version":1,"request_id":"550e8400-e29b-41d4-a716-446655440000","operation":"daemon.status","params":{"extra":true},"timeout_ms":10000});
    assert_eq!(
        Request::decode(&serde_json::to_vec(&value).unwrap())
            .unwrap_err()
            .code,
        ErrorCode::InvalidArgument
    );
}
#[test]
fn qa_u06_tray_displays_current_generation() {
    let status = json!({"project_id":"p","current_generation":"GEN-QA-417","last_reconciliation":1777777777,"coverage":"complete","freshness":"observed_current"});
    let text = devforgeai_index::tray::status_text(
        "local",
        &Response::success("r", json!({"daemon_state":"running"})),
        &[json!({"id":"p","name":"Project","root":"fixture"})],
        &[status],
    );
    assert!(
        text.contains("GEN-QA-417"),
        "DS-025 requires current generation in management window; actual={text}"
    );
}
#[test]
fn qa_u07_tray_displays_last_reconciliation() {
    let status = json!({"project_id":"p","current_generation":"GEN-QA-417","last_reconciliation":1777777777,"coverage":"complete","freshness":"observed_current"});
    let text = devforgeai_index::tray::status_text(
        "local",
        &Response::success("r", json!({"daemon_state":"running"})),
        &[json!({"id":"p","name":"Project","root":"fixture"})],
        std::slice::from_ref(&status),
    );
    let missing = devforgeai_index::tray::status_text(
        "local",
        &Response::success("r", json!({"daemon_state":"running"})),
        &[json!({"id":"p","name":"Project","root":"fixture"})],
        &[
            json!({"project_id":"p","current_generation":"GEN-QA-417","last_reconciliation":null,"coverage":"complete","freshness":"observed_current"}),
        ],
    );
    assert_ne!(
        text, missing,
        "DS-025 requires reconciliation display to distinguish a known reconciliation from none"
    );
}
#[test]
fn qa_i01_mandatory_exclusions_survive_default_override() {
    let t = tempfile::tempdir().unwrap();
    fs::create_dir_all(t.path().join(".agents/devforgeai")).unwrap();
    fs::create_dir_all(t.path().join("target")).unwrap();
    fs::create_dir_all(t.path().join(".hidden")).unwrap();
    for (path, bytes) in [
        (".env", "secret"),
        ("private.key", "secret"),
        (".agents/devforgeai/state.json", "{}"),
        ("target/yes.py", "pass"),
        (".hidden/yes.py", "pass"),
        ("yes.py", "pass"),
    ] {
        fs::write(t.path().join(path), bytes).unwrap();
    }
    let c = ProjectConfig {
        default_exclusions: Some(false),
        exclusions: Some(vec!["!.env".into()]),
        ..Default::default()
    };
    let files = enumerate(t.path(), &c, &[]).unwrap();
    for name in [".env", "private.key", ".agents/devforgeai"] {
        assert!(
            matches!(
                files.iter().find(|f| f.path == name).unwrap().disposition,
                FileDisposition::Excluded(_)
            ),
            "{name}"
        );
    }
    for name in ["target/yes.py", ".hidden/yes.py", "yes.py"] {
        assert_eq!(
            files.iter().find(|f| f.path == name).unwrap().disposition,
            FileDisposition::Eligible,
            "{name}"
        );
    }
}
#[test]
fn qa_i02_git_info_exclude_and_nested_negation() {
    let t = tempfile::tempdir().unwrap();
    fs::create_dir_all(t.path().join(".git/info")).unwrap();
    fs::create_dir(t.path().join("sub")).unwrap();
    fs::write(t.path().join(".git/info/exclude"), "secret.py\n").unwrap();
    fs::write(t.path().join(".gitignore"), "*.py\n").unwrap();
    fs::write(t.path().join("sub/.gitignore"), "!keep.py\n").unwrap();
    for p in ["secret.py", "drop.py", "sub/keep.py"] {
        fs::write(t.path().join(p), "pass").unwrap();
    }
    let f = enumerate(t.path(), &ProjectConfig::default(), &[]).unwrap();
    assert_eq!(
        f.iter()
            .find(|f| f.path == "sub/keep.py")
            .unwrap()
            .disposition,
        FileDisposition::Eligible
    );
    for n in ["secret.py", "drop.py"] {
        assert!(matches!(
            f.iter().find(|f| f.path == n).unwrap().disposition,
            FileDisposition::Excluded(_)
        ));
    }
}
#[test]
fn qa_i03_capture_size_boundary_and_hash_known_answer() {
    let t = tempfile::tempdir().unwrap();
    fs::write(t.path().join("file.txt"), b"abc").unwrap();
    let snap = capture(t.path(), "file.txt", 3, &AtomicBool::new(false)).unwrap();
    assert_eq!(snap.bytes, b"abc");
    assert_eq!(
        snap.sha256,
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );
    assert_eq!(
        capture(t.path(), "file.txt", 2, &AtomicBool::new(false)).unwrap_err(),
        "oversized"
    );
}
#[test]
fn qa_i04_generation_snapshots_remain_independent_of_live_bytes() {
    let t = tempfile::tempdir().unwrap();
    let mut s = Store::open(t.path()).unwrap();
    let hash = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
    let f = StoredFile {
        path: "file.txt".into(),
        sha256: Some(hash.into()),
        bytes: Some(b"abc".to_vec()),
        record: json!({"state":"indexed"}),
    };
    s.begin_generation("p", "g1").unwrap();
    s.stage_file("g1", &f).unwrap();
    s.publish("p", "g1", &json!({})).unwrap();
    s.begin_generation("p", "g2").unwrap();
    let bad = StoredFile {
        bytes: Some(b"abd".to_vec()),
        ..f
    };
    assert!(s.stage_file("g2", &bad).is_err());
    s.abandon("g2").unwrap();
    assert_eq!(s.current("p").unwrap().as_deref(), Some("g1"));
    assert_eq!(s.source("g1", "file.txt").unwrap().unwrap(), b"abc");
}
#[test]
fn qa_i05_replay_expiry_and_conflict_are_persistent() {
    let t = tempfile::tempdir().unwrap();
    let mut s = Store::open(t.path()).unwrap();
    s.remember_request("r", "same", &json!({"ok":true}), 1000)
        .unwrap();
    drop(s);
    let s = Store::open(t.path()).unwrap();
    assert_eq!(
        s.replay_request("r", "same", 1000 + 86399).unwrap(),
        Some(json!({"ok":true}))
    );
    assert!(s.replay_request("r", "different", 1001).is_err());
    assert!(
        s.replay_request("r", "same", 1000 + 86400)
            .unwrap()
            .is_none()
    );
}
