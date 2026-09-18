use super::*;
use std::{
    ffi::OsString,
    fs,
    os::windows::ffi::OsStringExt,
    path::{Path, PathBuf},
};

const SPEC_MAX_FILE_BYTES: u64 = 1_048_576;
const SPEC_MAX_TOTAL_BYTES: u64 = 8_388_608;
const SPEC_MAX_ENTRIES: usize = 2_048;
const SPEC_MAX_DIRECTORY_CHILDREN: usize = 1_024;
const SPEC_MAX_ANCESTOR_LEVELS: usize = 32;
const SPEC_MAX_RULE_LEVELS: usize = 8;

struct EdgeContext {
    root: Option<tempfile::TempDir>,
}

impl EdgeContext {
    fn new(case: &str) -> Self {
        let base = std::env::var_os("WF_TEST_EVIDENCE")
            .map(PathBuf::from)
            .unwrap_or_else(std::env::temp_dir);
        fs::create_dir_all(&base).unwrap();
        Self {
            root: Some(
                tempfile::Builder::new()
                    .prefix(&format!("{case}-"))
                    .tempdir_in(base)
                    .unwrap(),
            ),
        }
    }

    fn root(&self) -> &Path {
        self.root.as_ref().unwrap().path()
    }

    fn path(&self, relative: impl AsRef<Path>) -> PathBuf {
        self.root().join(relative)
    }

    fn write(&self, relative: impl AsRef<Path>, bytes: &[u8]) -> PathBuf {
        let path = self.path(relative);
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        fs::write(&path, bytes).unwrap();
        path
    }
}

impl Drop for EdgeContext {
    fn drop(&mut self) {
        if std::env::var_os("WF_TEST_EVIDENCE").is_some() {
            let _ = self.root.take().unwrap().keep();
        }
    }
}

fn absent_entry() -> SourceEntry {
    SourceEntry {
        family: SourceFamily::User,
        path: PathBuf::from(r"C:\absent"),
        state: SourceState::Absent,
        sha256: None,
        bytes: None,
        items: None,
    }
}

fn valid_inventory() -> Inventory {
    Inventory {
        schema_version: 1,
        fixture_cwd: PathBuf::from(r"C:\fixture"),
        roots: InventoryRoots {
            ancestor_root: PathBuf::from(r"C:\"),
            workspace_root: PathBuf::from(r"C:\workspace"),
            user_codex_root: PathBuf::from(r"C:\user\.codex"),
            program_data_codex_root: PathBuf::from(r"C:\ProgramData\OpenAI\Codex"),
            plugin_cache_root: PathBuf::from(r"C:\user\.codex\plugins\cache"),
        },
        entries: vec![
            SourceEntry {
                family: SourceFamily::User,
                path: PathBuf::from(r"C:\user\.codex\config.toml"),
                state: SourceState::File,
                sha256: Some("a".repeat(64)),
                bytes: Some(SPEC_MAX_FILE_BYTES),
                items: None,
            },
            absent_entry(),
            SourceEntry {
                family: SourceFamily::Rules,
                path: PathBuf::from(r"C:\user\.codex\rules"),
                state: SourceState::DirectoryIndex,
                sha256: Some("b".repeat(64)),
                bytes: None,
                items: Some(SPEC_MAX_DIRECTORY_CHILDREN as u32),
            },
        ],
    }
}

#[test]
fn closed_inventory_shape_rejects_invalid_state_tuples_and_version() {
    assert_eq!(MAX_FILE_BYTES, SPEC_MAX_FILE_BYTES);
    assert_eq!(MAX_DIRECTORY_CHILDREN, SPEC_MAX_DIRECTORY_CHILDREN);
    assert!(valid_inventory().valid_shape());

    let mut invalid = Vec::new();

    let mut value = valid_inventory();
    value.schema_version = 2;
    invalid.push(value);

    let mut value = valid_inventory();
    value.entries[0].sha256 = Some("not-a-digest".into());
    invalid.push(value);

    let mut value = valid_inventory();
    value.entries[0].bytes = Some(SPEC_MAX_FILE_BYTES + 1);
    invalid.push(value);

    let mut value = valid_inventory();
    value.entries[0].items = Some(0);
    invalid.push(value);

    let mut value = valid_inventory();
    value.entries[1].sha256 = Some("c".repeat(64));
    invalid.push(value);

    let mut value = valid_inventory();
    value.entries[2].bytes = Some(0);
    invalid.push(value);

    let mut value = valid_inventory();
    value.entries[2].items = Some((SPEC_MAX_DIRECTORY_CHILDREN + 1) as u32);
    invalid.push(value);

    for inventory in invalid {
        assert!(!inventory.valid_shape());
    }
}

#[test]
fn collector_enforces_entry_and_aggregate_byte_bounds() {
    assert_eq!(MAX_ENTRIES, SPEC_MAX_ENTRIES);
    assert_eq!(MAX_TOTAL_BYTES, SPEC_MAX_TOTAL_BYTES);

    let mut entries = Collector {
        entries: vec![absent_entry(); SPEC_MAX_ENTRIES],
        total_bytes: 0,
    };
    assert_eq!(
        entries.push(absent_entry()).unwrap_err(),
        "profile_source_limit"
    );

    let context = EdgeContext::new("SI-E02-total-bytes");
    let mut bytes = Collector::default();
    for index in 0..8 {
        let source = context.write(
            format!("source-{index}.toml"),
            &vec![b'x'; SPEC_MAX_FILE_BYTES as usize],
        );
        bytes.add_file(SourceFamily::User, &source).unwrap();
    }
    assert_eq!(bytes.total_bytes, SPEC_MAX_TOTAL_BYTES);
    let next = context.write("one-byte-over.toml", b"x");
    assert_eq!(
        bytes.add_file(SourceFamily::User, &next).unwrap_err(),
        "profile_source_limit"
    );
}

#[test]
fn rule_and_ancestor_depth_bounds_fail_closed() {
    assert_eq!(MAX_RULE_DEPTH, SPEC_MAX_RULE_LEVELS);
    assert_eq!(MAX_ANCESTOR_DEPTH, SPEC_MAX_ANCESTOR_LEVELS);

    let context = EdgeContext::new("SI-E03-rule-depth");
    let rules = context.path("rules");
    let mut deepest = rules.clone();
    for index in 0..=SPEC_MAX_RULE_LEVELS {
        deepest = deepest.join(format!("level-{index}"));
    }
    fs::create_dir_all(&deepest).unwrap();
    assert_eq!(
        Collector::default().walk_rules(&rules, 0).unwrap_err(),
        "profile_source_limit"
    );

    let root = context.path("ancestors");
    let mut accepted = root.clone();
    for index in 0..(SPEC_MAX_ANCESTOR_LEVELS - 1) {
        accepted = accepted.join(format!("a-{index}"));
    }
    assert_eq!(
        scoped_ancestors(&root, &accepted).unwrap().len(),
        SPEC_MAX_ANCESTOR_LEVELS
    );
    let too_deep = accepted.join("one-too-many");
    assert_eq!(
        scoped_ancestors(&root, &too_deep).unwrap_err(),
        "profile_source_limit"
    );
    assert_eq!(
        scoped_ancestors(
            &context.path("different-root"),
            &context.path("outside-root/leaf"),
        )
        .unwrap_err(),
        "profile_source_fixture_scope"
    );
}

#[test]
fn directory_member_bound_and_required_file_type_are_enforced() {
    let context = EdgeContext::new("SI-E04-directory-bound");
    let crowded = context.path("crowded");
    fs::create_dir_all(&crowded).unwrap();
    for index in 0..=SPEC_MAX_DIRECTORY_CHILDREN {
        fs::write(crowded.join(format!("member-{index:04}")), b"").unwrap();
    }
    assert_eq!(
        directory_snapshot(&crowded).unwrap_err(),
        "profile_source_limit"
    );

    let wrong_type = context.path("config.toml");
    fs::create_dir_all(&wrong_type).unwrap();
    assert_eq!(
        Collector::default()
            .add_file_or_absent(SourceFamily::User, &wrong_type)
            .unwrap_err(),
        "profile_source_type"
    );
    assert_eq!(
        require_directory(&context.write("ordinary-file", b"x")).unwrap_err(),
        "profile_source_type"
    );
}

#[test]
fn plugin_tree_grammar_rejects_unknown_members_and_indexes_controls() {
    let provider_file = EdgeContext::new("SI-E05-provider-file");
    let cache = provider_file.path("cache");
    fs::create_dir_all(&cache).unwrap();
    fs::write(cache.join("provider"), b"not a directory").unwrap();
    assert_eq!(
        Collector::default().walk_plugins(&cache).unwrap_err(),
        "profile_source_unrecognized"
    );

    let plugin_file = EdgeContext::new("SI-E05-plugin-file");
    let cache = plugin_file.path("cache");
    fs::create_dir_all(cache.join("provider")).unwrap();
    fs::write(cache.join("provider/plugin"), b"not a directory").unwrap();
    assert_eq!(
        Collector::default().walk_plugins(&cache).unwrap_err(),
        "profile_source_unrecognized"
    );

    let unknown_plugin_member = EdgeContext::new("SI-E05-plugin-member");
    let cache = unknown_plugin_member.path("cache");
    fs::create_dir_all(cache.join("provider/plugin")).unwrap();
    fs::write(cache.join("provider/plugin/unexpected.json"), b"{}").unwrap();
    assert_eq!(
        Collector::default().walk_plugins(&cache).unwrap_err(),
        "profile_source_unrecognized"
    );

    let unknown_control = EdgeContext::new("SI-E05-control-member");
    let cache = unknown_control.path("cache");
    fs::create_dir_all(cache.join("provider/plugin/1.0/.codex-plugin")).unwrap();
    fs::write(
        cache.join("provider/plugin/1.0/.codex-plugin/unexpected.json"),
        b"{}",
    )
    .unwrap();
    assert_eq!(
        Collector::default().walk_plugins(&cache).unwrap_err(),
        "profile_source_unrecognized"
    );

    let accepted = EdgeContext::new("SI-E05-controls");
    let cache = accepted.path("cache");
    let plugin = cache.join("provider/plugin");
    let version = plugin.join("1.0");
    fs::create_dir_all(version.join(".codex-plugin")).unwrap();
    fs::write(
        plugin.join(".codex-remote-plugin-install.json"),
        b"{\"installed\":true}",
    )
    .unwrap();
    fs::write(version.join("README.md"), b"payload, not a control input").unwrap();
    fs::write(version.join(".codex-plugin/plugin.json"), b"{}").unwrap();
    let mut collector = Collector::default();
    collector.walk_plugins(&cache).unwrap();
    assert!(collector.entries.iter().any(|entry| {
        entry.state == SourceState::File
            && entry.path.ends_with(".codex-remote-plugin-install.json")
    }));
    assert!(
        collector.entries.iter().any(|entry| {
            entry.state == SourceState::File && entry.path.ends_with("plugin.json")
        })
    );
    assert!(
        !collector
            .entries
            .iter()
            .any(|entry| { entry.state == SourceState::File && entry.path.ends_with("README.md") })
    );
}

#[test]
fn credential_like_and_non_unicode_names_fail_closed() {
    for name in [
        "auth.json",
        "AUTH.JSON",
        ".env",
        ".env.production",
        "client-credential.toml",
        "secret-store.json",
        "access-token.txt",
    ] {
        assert!(forbidden_name(OsString::from(name).as_os_str()), "{name}");
    }
    assert!(!forbidden_name(OsString::from("config.toml").as_os_str()));

    let invalid_unicode = OsString::from_wide(&[0xd800]);
    assert!(forbidden_name(&invalid_unicode));
}

#[test]
fn hash_size_drift_and_non_absolute_paths_fail_closed() {
    let context = EdgeContext::new("SI-E07-hash-path");
    let small = context.write("small.toml", b"abc");
    assert_eq!(hash_once(&small, 4).unwrap_err(), "profile_source_drift");

    let oversized = context.write(
        "oversized.toml",
        &vec![b'x'; (SPEC_MAX_FILE_BYTES + 1) as usize],
    );
    assert_eq!(
        hash_once(&oversized, SPEC_MAX_FILE_BYTES + 1).unwrap_err(),
        "profile_source_limit"
    );

    assert_eq!(
        expected_path(Path::new("relative/config.toml")).unwrap_err(),
        "profile_source_path"
    );
    assert_eq!(
        expected_path(Path::new(r"C:\source\..\escape.toml")).unwrap_err(),
        "profile_source_path"
    );
    assert!(
        strict_resolve(Path::new("relative"))
            .unwrap_err()
            .starts_with("profile_source_path:")
    );
}

#[test]
fn missing_paths_are_explicit_and_directory_order_is_stable() {
    let context = EdgeContext::new("SI-E08-absence-order");
    let missing = context.path("missing/deeper/config.toml");
    let (resolved_missing, exists) = expected_path(&missing).unwrap();
    assert!(!exists);
    assert_eq!(
        resolved_missing,
        strict_resolve(context.root())
            .unwrap()
            .join("missing/deeper/config.toml")
    );

    let directory = context.path("ordered");
    fs::create_dir_all(&directory).unwrap();
    for name in ["zeta", "Alpha", "beta"] {
        fs::write(directory.join(name), b"").unwrap();
    }
    let names: Vec<_> = directory_snapshot(&directory)
        .unwrap()
        .into_iter()
        .map(|member| member.name)
        .collect();
    assert_eq!(names, ["Alpha", "beta", "zeta"]);
}
