use super::*;
use crate::request::digest;
use std::{
    fs,
    os::windows::fs::symlink_dir,
    path::{Path, PathBuf},
};

struct TestContext {
    root: tempfile::TempDir,
    fixture: PathBuf,
    roots: Roots,
}

impl TestContext {
    fn new(case: &str) -> Self {
        let base = std::env::var_os("WF_TEST_EVIDENCE")
            .map(PathBuf::from)
            .unwrap_or_else(std::env::temp_dir);
        fs::create_dir_all(&base).unwrap();
        let root = tempfile::Builder::new()
            .prefix(&format!("{case}-"))
            .tempdir_in(base)
            .unwrap();
        let ancestor_root = root.path().join("source-root");
        let workspace_root = ancestor_root.join("workspace");
        let fixture = workspace_root.join("docs").join("fixture");
        let user_codex_root = root.path().join("user").join(".codex");
        let program_data_codex_root = root
            .path()
            .join("program-data")
            .join("OpenAI")
            .join("Codex");
        let plugin_cache_root = user_codex_root.join("plugins").join("cache");
        for directory in [
            &fixture,
            &user_codex_root,
            &program_data_codex_root,
            &plugin_cache_root,
        ] {
            fs::create_dir_all(directory).unwrap();
        }
        Self {
            root,
            fixture,
            roots: Roots {
                ancestor_root,
                workspace_root,
                user_codex_root,
                program_data_codex_root,
                plugin_cache_root,
            },
        }
    }

    fn write(&self, path: impl AsRef<Path>, bytes: &[u8]) {
        let path = path.as_ref();
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        fs::write(path, bytes).unwrap();
    }

    fn add_plugin(&self) -> PathBuf {
        let version = self
            .roots
            .plugin_cache_root
            .join("publisher")
            .join("plugin")
            .join("1.2.3");
        self.write(
            version.join(".codex-plugin").join("plugin.json"),
            br#"{"name":"plugin","hooks":{}}"#,
        );
        self.write(version.join(".mcp.json"), br#"{"mcpServers":{}}"#);
        version
    }
}

#[test]
fn inventory_is_deterministic_digest_only_and_records_absence() {
    let context = TestContext::new("NI-T08-inventory");
    let secret_marker = "raw-config-must-not-be-retained";
    context.write(
        context.roots.user_codex_root.join("config.toml"),
        format!("model = 'test' # {secret_marker}\n").as_bytes(),
    );
    context.write(
        context.roots.workspace_root.join("AGENTS.md"),
        b"workspace instruction\n",
    );
    context.write(
        context.roots.user_codex_root.join("rules/default.rules"),
        b"prefix_rule(pattern=[\"cargo\"], decision=\"allow\")\n",
    );
    context.add_plugin();

    let first = collect_with_roots(&context.fixture, &context.roots).unwrap();
    let second = collect_with_roots(&context.fixture, &context.roots).unwrap();
    assert_eq!(first, second);
    assert_eq!(first.schema_version, SCHEMA_VERSION);
    assert_eq!(
        first.fixture_cwd,
        crate::request::resolve(&context.fixture).unwrap()
    );

    let encoded = serde_json::to_vec(&first).unwrap();
    assert!(!String::from_utf8_lossy(&encoded).contains(secret_marker));
    assert!(first.entries.iter().any(|entry| {
        entry.state == SourceState::Absent
            && entry.path.ends_with(Path::new("hooks.json"))
            && entry.sha256.is_none()
    }));
    assert!(first.entries.iter().any(|entry| {
        entry.state == SourceState::File
            && entry.path.ends_with(Path::new("config.toml"))
            && entry.sha256
                == Some(digest(
                    format!("model = 'test' # {secret_marker}\n").as_bytes(),
                ))
    }));
    assert!(
        first
            .file_paths()
            .iter()
            .any(|path| path.ends_with(Path::new(
                "publisher/plugin/1.2.3/.codex-plugin/plugin.json"
            )))
    );

    let mut value: serde_json::Value = serde_json::from_slice(&encoded).unwrap();
    value["unexpected"] = serde_json::json!(true);
    assert!(serde_json::from_value::<Inventory>(value).is_err());
}

#[test]
fn credential_named_files_are_rejected_before_content_is_read() {
    let context = TestContext::new("NI-T08-no-credentials");
    context.write(
        context.roots.user_codex_root.join("rules/auth.json"),
        b"credential bytes must never be opened",
    );
    let error = collect_with_roots(&context.fixture, &context.roots).unwrap_err();
    assert_eq!(error, "profile_source_forbidden_name");
}

#[test]
fn any_reparse_in_the_selected_plugin_tree_fails_closed() {
    let context = TestContext::new("NI-T08-plugin-reparse");
    let plugin_root = context
        .roots
        .plugin_cache_root
        .join("publisher")
        .join("plugin");
    let version = plugin_root.join("1.2.3");
    fs::create_dir_all(&version).unwrap();
    let latest = plugin_root.join("latest");
    symlink_dir(&version, &latest)
        .unwrap_or_else(|error| panic!("required reparse fixture unavailable: {error}"));
    let error = collect_with_roots(&context.fixture, &context.roots).unwrap_err();
    assert!(error.starts_with("profile_source_reparse:"), "{error}");
    fs::remove_dir(&latest).unwrap();
}

#[test]
fn directory_membership_and_fresh_verification_detect_drift() {
    let context = TestContext::new("NI-T10-source-drift");
    context.write(
        context.roots.user_codex_root.join("rules/default.rules"),
        b"first\n",
    );
    let before = collect_with_roots(&context.fixture, &context.roots).unwrap();
    verify_with_roots(&before, &context.roots).unwrap();
    let before_index = before
        .entries
        .iter()
        .find(|entry| {
            entry.family == SourceFamily::Rules && entry.state == SourceState::DirectoryIndex
        })
        .unwrap()
        .sha256
        .clone();

    context.write(
        context.roots.user_codex_root.join("rules/additional.rules"),
        b"second\n",
    );
    assert_eq!(
        verify_with_roots(&before, &context.roots).unwrap_err(),
        "profile_source_drift"
    );
    let after = collect_with_roots(&context.fixture, &context.roots).unwrap();
    let after_index = after
        .entries
        .iter()
        .find(|entry| {
            entry.family == SourceFamily::Rules && entry.state == SourceState::DirectoryIndex
        })
        .unwrap()
        .sha256
        .clone();
    assert_ne!(before_index, after_index);
}

#[test]
fn fixture_outside_fixed_workspace_and_oversized_source_are_rejected() {
    let context = TestContext::new("NI-T08-bounds");
    assert_eq!(
        collect_with_roots(context.root.path(), &context.roots).unwrap_err(),
        "profile_source_fixture_scope"
    );

    context.write(
        context.roots.user_codex_root.join("config.toml"),
        &vec![b'x'; (MAX_FILE_BYTES + 1) as usize],
    );
    assert_eq!(
        collect_with_roots(&context.fixture, &context.roots).unwrap_err(),
        "profile_source_limit"
    );
}

#[test]
fn deserialized_entry_shape_is_validated_before_bindings_are_used() {
    let context = TestContext::new("NI-T08-closed-entry");
    context.write(
        context.roots.user_codex_root.join("config.toml"),
        b"model = 'test'\n",
    );
    let mut inventory = collect_with_roots(&context.fixture, &context.roots).unwrap();
    let file = inventory
        .entries
        .iter_mut()
        .find(|entry| entry.state == SourceState::File)
        .unwrap();
    file.sha256 = None;
    assert_eq!(
        verify_with_roots(&inventory, &context.roots).unwrap_err(),
        "profile_source_schema"
    );
    assert!(inventory.file_bindings().is_empty());
}
