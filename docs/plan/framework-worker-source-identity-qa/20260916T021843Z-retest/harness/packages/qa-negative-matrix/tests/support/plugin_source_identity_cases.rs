use super::*;
use std::{
    fs,
    os::windows::{fs::MetadataExt, fs::symlink_dir},
    path::{Path, PathBuf},
    process::Command,
    sync::atomic::{AtomicU64, Ordering},
};

const JUNCTION_TAG: u32 = 0xa0000003;
const EMPTY_OBJECT_LINE_SHA256: &str =
    "ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356";
const EXACT_PLUGIN_DIRECTORY_INDEX_SHA256: &str =
    "c4cf4274ec57eee85a24f2ef31cf319393f936cbf1c9dd6568e8d8f2897e0ade";
static MKLINK_ATTEMPT: AtomicU64 = AtomicU64::new(1);

struct JunctionContext {
    root: Option<tempfile::TempDir>,
    fixture: PathBuf,
    roots: Roots,
    reparse_points: Vec<PathBuf>,
}

impl JunctionContext {
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
            root: Some(root),
            fixture,
            roots: Roots {
                ancestor_root,
                workspace_root,
                user_codex_root,
                program_data_codex_root,
                plugin_cache_root,
            },
            reparse_points: Vec::new(),
        }
    }

    fn selected_paths(&self) -> (PathBuf, PathBuf) {
        let plugin = self
            .roots
            .plugin_cache_root
            .join("openai-bundled")
            .join("chrome");
        let target = plugin.join("26.908.70816");
        (plugin.join("latest"), target)
    }

    fn create_physical_target(&self, target: &Path) {
        fs::create_dir_all(target.join(".codex-plugin")).unwrap();
        fs::write(target.join(".codex-plugin").join("plugin.json"), b"{}\n").unwrap();
        fs::write(target.join(".mcp.json"), b"{}\n").unwrap();
    }

    fn selected_mapping(&self) -> PluginJunction {
        let (path, target) = self.selected_paths();
        PluginJunction {
            path,
            target,
            reparse_tag: JUNCTION_TAG,
        }
    }

    fn exact_mapping(&mut self) -> PluginJunction {
        let mapping = self.selected_mapping();
        self.create_physical_target(&mapping.target);
        let path = mapping.path.clone();
        let target = mapping.target.clone();
        self.junction(&path, &target);
        mapping
    }

    fn policy(&self, mapping: PluginJunction) -> PluginSourcePolicy {
        PluginSourcePolicy {
            digest: digest(b"synthetic-reviewed-plugin-source-identity-v1"),
            junctions: vec![mapping],
        }
    }

    fn junction(&mut self, path: &Path, target: &Path) {
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        let output = Command::new("cmd.exe")
            .args(["/d", "/c", "mklink", "/J"])
            .arg(path)
            .arg(target)
            .output()
            .unwrap();
        assert!(
            output.status.success(),
            "junction fixture setup failed: stdout={} stderr={}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
        let metadata = fs::symlink_metadata(path).unwrap();
        assert_ne!(metadata.file_attributes() & 0x400, 0);
        assert_eq!(fs::read_link(path).unwrap(), target);
        let attempt = MKLINK_ATTEMPT.fetch_add(1, Ordering::SeqCst);
        let evidence = self
            .root
            .as_ref()
            .unwrap()
            .path()
            .join(format!("mklink-{attempt:03}"));
        fs::write(evidence.with_extension("stdout"), &output.stdout).unwrap();
        fs::write(evidence.with_extension("stderr"), &output.stderr).unwrap();
        fs::write(
            evidence.with_extension("status.txt"),
            format!(
                "exit_code={:?}\npath={}\ntarget={}\n",
                output.status.code(),
                path.display(),
                target.display()
            ),
        )
        .unwrap();
        self.reparse_points.push(path.to_path_buf());
    }

    fn track_reparse(&mut self, path: &Path) {
        self.reparse_points.push(path.to_path_buf());
    }
}

impl Drop for JunctionContext {
    fn drop(&mut self) {
        for path in self.reparse_points.iter().rev() {
            if fs::symlink_metadata(path).is_ok() {
                let _ = fs::remove_dir(path);
            }
        }
        if std::env::var_os("WF_TEST_EVIDENCE").is_some()
            && let Some(root) = self.root.take()
        {
            let _ = root.keep();
        }
    }
}

#[test]
fn si_t01_exact_reviewed_junction_reads_physical_sources_once() {
    let mut context = JunctionContext::new("SI-T01-exact-junction");
    let mapping = context.exact_mapping();
    let policy = context.policy(mapping.clone());
    let inventory = collect_with_policy(&context.fixture, &context.roots, &policy)
        .expect("the exact reviewed directory junction must be admitted");
    let physical_target = strict_resolve(&mapping.target).unwrap();
    let plugin_json = physical_target.join(".codex-plugin").join("plugin.json");
    let file_bindings = inventory.file_bindings();
    assert_eq!(
        file_bindings
            .iter()
            .filter(|(path, digest)| { path == &plugin_json && digest == EMPTY_OBJECT_LINE_SHA256 })
            .count(),
        1
    );
    let unique: std::collections::HashSet<_> = file_bindings
        .iter()
        .map(|(path, _)| path.to_string_lossy().to_ascii_lowercase())
        .collect();
    assert_eq!(unique.len(), file_bindings.len());
    let physical_plugin = strict_resolve(mapping.target.parent().unwrap()).unwrap();
    let plugin_index = inventory
        .entries
        .iter()
        .find(|entry| entry.state == SourceState::DirectoryIndex && entry.path == physical_plugin)
        .unwrap();
    assert_eq!(plugin_index.items, Some(2));
    assert_eq!(
        plugin_index.sha256.as_deref(),
        Some(EXACT_PLUGIN_DIRECTORY_INDEX_SHA256)
    );
    assert!(
        inventory
            .entries
            .iter()
            .all(|entry| !entry.path.starts_with(&mapping.path))
    );
    assert_eq!(inventory.source_identity_sha256, policy.digest);
    assert_eq!(inventory.junctions, vec![mapping]);
}

fn assert_source_rejected(result: Result<Inventory>) {
    let error = result.expect_err("source identity must reject");
    assert!(
        error == "profile_source_identity"
            || error.starts_with("profile_source_reparse:")
            || error.starts_with("profile_source_path:"),
        "unexpected rejection: {error}"
    );
}

#[test]
fn si_t02_changed_same_byte_escaping_and_missing_targets_reject() {
    let mut changed = JunctionContext::new("SI-T02-changed-target");
    let mapping = changed.selected_mapping();
    changed.create_physical_target(&mapping.target);
    let replacement = mapping.target.with_file_name("26.908.70817");
    changed.create_physical_target(&replacement);
    changed.junction(&mapping.path, &replacement);
    let policy = changed.policy(mapping);
    assert_source_rejected(collect_with_policy(
        &changed.fixture,
        &changed.roots,
        &policy,
    ));

    let mut escaping = JunctionContext::new("SI-T02-escaping-target");
    let mapping = escaping.selected_mapping();
    escaping.create_physical_target(&mapping.target);
    let outside = escaping
        .root
        .as_ref()
        .unwrap()
        .path()
        .join("outside-version");
    escaping.create_physical_target(&outside);
    escaping.junction(&mapping.path, &outside);
    let policy = escaping.policy(mapping);
    assert_source_rejected(collect_with_policy(
        &escaping.fixture,
        &escaping.roots,
        &policy,
    ));

    let mut missing = JunctionContext::new("SI-T02-missing-target");
    let mapping = missing.selected_mapping();
    missing.junction(&mapping.path, &mapping.target);
    let policy = missing.policy(mapping);
    assert_source_rejected(collect_with_policy(
        &missing.fixture,
        &missing.roots,
        &policy,
    ));
}

#[test]
fn si_t03_wrong_type_ordinary_and_missing_junction_reject() {
    let mut symbolic = JunctionContext::new("SI-T03-directory-symlink");
    let mapping = symbolic.selected_mapping();
    symbolic.create_physical_target(&mapping.target);
    fs::create_dir_all(mapping.path.parent().unwrap()).unwrap();
    symlink_dir(&mapping.target, &mapping.path)
        .unwrap_or_else(|error| panic!("directory-symlink fixture unavailable: {error}"));
    symbolic.track_reparse(&mapping.path);
    assert_ne!(
        fs::symlink_metadata(&mapping.path)
            .unwrap()
            .file_attributes()
            & 0x400,
        0
    );
    let policy = symbolic.policy(mapping);
    assert_source_rejected(collect_with_policy(
        &symbolic.fixture,
        &symbolic.roots,
        &policy,
    ));

    let ordinary = JunctionContext::new("SI-T03-ordinary-directory");
    let mapping = ordinary.selected_mapping();
    ordinary.create_physical_target(&mapping.target);
    fs::create_dir_all(&mapping.path).unwrap();
    let policy = ordinary.policy(mapping);
    assert_source_rejected(collect_with_policy(
        &ordinary.fixture,
        &ordinary.roots,
        &policy,
    ));

    let missing = JunctionContext::new("SI-T03-missing-junction");
    let mapping = missing.selected_mapping();
    missing.create_physical_target(&mapping.target);
    let policy = missing.policy(mapping);
    assert_source_rejected(collect_with_policy(
        &missing.fixture,
        &missing.roots,
        &policy,
    ));
}

#[test]
fn si_t04_unlisted_loop_nested_reparse_and_wrong_depth_reject() {
    let mut unlisted = JunctionContext::new("SI-T04-unlisted-alternate-root");
    let mapping = unlisted.exact_mapping();
    assert_source_rejected(collect_with_policy(
        &unlisted.fixture,
        &unlisted.roots,
        &PluginSourcePolicy::empty_for_regressions(),
    ));
    assert!(mapping.path.exists());

    let mut looped = JunctionContext::new("SI-T04-loop");
    let plugin = looped
        .roots
        .plugin_cache_root
        .join("publisher")
        .join("plugin");
    fs::create_dir_all(&plugin).unwrap();
    let loop_path = plugin.join("loop");
    looped.junction(&loop_path, &plugin);
    assert_source_rejected(collect_with_policy(
        &looped.fixture,
        &looped.roots,
        &PluginSourcePolicy::empty_for_regressions(),
    ));

    let mut nested = JunctionContext::new("SI-T04-nested-control-reparse");
    let mapping = nested.exact_mapping();
    let control = mapping.target.join(".codex-plugin");
    fs::remove_dir_all(&control).unwrap();
    let outside_control = nested.root.as_ref().unwrap().path().join("outside-control");
    fs::create_dir(&outside_control).unwrap();
    fs::write(outside_control.join("plugin.json"), b"{}\n").unwrap();
    symlink_dir(&outside_control, &control)
        .unwrap_or_else(|error| panic!("control symlink fixture unavailable: {error}"));
    nested.track_reparse(&control);
    let policy = nested.policy(mapping);
    assert_source_rejected(collect_with_policy(&nested.fixture, &nested.roots, &policy));

    let mut wrong_depth = JunctionContext::new("SI-T04-wrong-depth");
    let outside_provider = wrong_depth
        .root
        .as_ref()
        .unwrap()
        .path()
        .join("provider-target");
    fs::create_dir(&outside_provider).unwrap();
    let provider_alias = wrong_depth.roots.plugin_cache_root.join("provider-alias");
    wrong_depth.junction(&provider_alias, &outside_provider);
    assert_source_rejected(collect_with_policy(
        &wrong_depth.fixture,
        &wrong_depth.roots,
        &PluginSourcePolicy::empty_for_regressions(),
    ));
}

#[test]
fn si_t05_physical_bytes_and_indexed_membership_drift_invalidate_inventory() {
    let mut bytes = JunctionContext::new("SI-T05-byte-drift");
    let mapping = bytes.exact_mapping();
    let policy = bytes.policy(mapping.clone());
    let inventory = collect_with_policy(&bytes.fixture, &bytes.roots, &policy).unwrap();
    fs::write(
        mapping.target.join(".codex-plugin").join("plugin.json"),
        b"changed\n",
    )
    .unwrap();
    assert_eq!(
        verify_with_policy(&inventory, &bytes.roots, &policy).unwrap_err(),
        "profile_source_drift"
    );

    let mut membership = JunctionContext::new("SI-T05-membership-drift");
    let mapping = membership.exact_mapping();
    let policy = membership.policy(mapping.clone());
    let inventory = collect_with_policy(&membership.fixture, &membership.roots, &policy).unwrap();
    fs::write(mapping.target.join("README.md"), b"new membership\n").unwrap();
    assert_eq!(
        verify_with_policy(&inventory, &membership.roots, &policy).unwrap_err(),
        "profile_source_drift"
    );

    let mut final_mapping = JunctionContext::new("SI-T05-final-mapping-drift");
    let mapping = final_mapping.exact_mapping();
    let replacement = mapping.target.with_file_name("26.908.70817");
    final_mapping.create_physical_target(&replacement);
    let policy = final_mapping.policy(mapping.clone());
    let alias = mapping.path.clone();
    let result = collect_with_policy_using(
        &final_mapping.fixture,
        &final_mapping.roots,
        &policy,
        || {
            fs::remove_dir(&alias).unwrap();
            let output = Command::new("cmd.exe")
                .args(["/d", "/c", "mklink", "/J"])
                .arg(&alias)
                .arg(&replacement)
                .output()
                .unwrap();
            assert!(
                output.status.success(),
                "final-check drift setup failed: {}",
                String::from_utf8_lossy(&output.stderr)
            );
        },
    );
    assert_source_rejected(result);
}

#[test]
fn si_t06_schema_identity_and_mapping_tampering_reject() {
    let mut context = JunctionContext::new("SI-T06-schema");
    let mapping = context.exact_mapping();
    let policy = context.policy(mapping.clone());
    let inventory = collect_with_policy(&context.fixture, &context.roots, &policy).unwrap();
    assert!(inventory.valid_shape());

    let mut old = inventory.clone();
    old.schema_version = 1;
    assert_eq!(
        verify_with_policy(&old, &context.roots, &policy).unwrap_err(),
        "profile_source_schema"
    );
    let mut forged = inventory.clone();
    forged.source_identity_sha256 = "0".repeat(64);
    assert_eq!(
        verify_with_policy(&forged, &context.roots, &policy).unwrap_err(),
        "profile_source_identity"
    );
    let mut omitted = inventory.clone();
    omitted.junctions.clear();
    assert_eq!(
        verify_with_policy(&omitted, &context.roots, &policy).unwrap_err(),
        "profile_source_identity"
    );
    let mut extra = inventory.clone();
    extra.junctions.push(mapping.clone());
    assert!(!extra.valid_shape());
    let mut wrong_tag = inventory.clone();
    wrong_tag.junctions[0].reparse_tag = 0xa000000c;
    assert!(!wrong_tag.valid_shape());

    let value = serde_json::to_value(&inventory).unwrap();
    for field in ["source_identity_sha256", "junctions"] {
        let mut missing = value.clone();
        missing.as_object_mut().unwrap().remove(field);
        assert!(
            serde_json::from_value::<Inventory>(missing).is_err(),
            "{field}"
        );
        let mut null = value.clone();
        null[field] = serde_json::Value::Null;
        assert!(
            serde_json::from_value::<Inventory>(null).is_err(),
            "null {field}"
        );
    }
    let mut unknown = value.clone();
    unknown["unknown"] = serde_json::json!(true);
    assert!(serde_json::from_value::<Inventory>(unknown).is_err());
    for field in ["path", "target", "reparse_tag"] {
        let mut missing = value.clone();
        missing["junctions"][0]
            .as_object_mut()
            .unwrap()
            .remove(field);
        assert!(
            serde_json::from_value::<Inventory>(missing).is_err(),
            "junction.{field}"
        );
        let mut wrong_type = value.clone();
        wrong_type["junctions"][0][field] = serde_json::Value::Bool(true);
        assert!(
            serde_json::from_value::<Inventory>(wrong_type).is_err(),
            "junction wrong type {field}"
        );
        let mut null = value.clone();
        null["junctions"][0][field] = serde_json::Value::Null;
        assert!(
            serde_json::from_value::<Inventory>(null).is_err(),
            "junction null {field}"
        );
    }
    let mut junction_unknown = value.clone();
    junction_unknown["junctions"][0]["unexpected"] = serde_json::json!(true);
    assert!(serde_json::from_value::<Inventory>(junction_unknown).is_err());
    let encoded = serde_json::to_string(&inventory).unwrap();
    let duplicate = format!(r#"{{"schema_version":2,{}"#, &encoded[1..]);
    assert!(serde_json::from_str::<Inventory>(&duplicate).is_err());

    let selected_cache = Path::new(SELECTED_LOGICAL_PATH).ancestors().nth(3).unwrap();
    let selected = PluginSourcePolicy::from_record(PLUGIN_SOURCE_RECORD, selected_cache).unwrap();
    assert_eq!(selected.junctions.len(), 1);
    let disjoint = PluginSourcePolicy::from_record(
        PLUGIN_SOURCE_RECORD,
        Path::new(r"C:\synthetic-user\.codex\plugins\cache"),
    )
    .unwrap();
    assert!(disjoint.junctions.is_empty());

    let mut record: serde_json::Value = serde_json::from_slice(PLUGIN_SOURCE_RECORD).unwrap();
    record["junctions"][0]["target"] = serde_json::json!(r"C:\other\version");
    let bytes = serde_json::to_vec(&record).unwrap();
    assert!(
        PluginSourcePolicy::from_record(&bytes, Path::new(r"C:\Users\bryan\.codex\plugins\cache"))
            .is_err()
    );
    let mut record: serde_json::Value = serde_json::from_slice(PLUGIN_SOURCE_RECORD).unwrap();
    record["unknown"] = serde_json::json!(true);
    assert!(
        PluginSourcePolicy::from_record(&serde_json::to_vec(&record).unwrap(), selected_cache,)
            .is_err()
    );
}

#[test]
fn qa_independent_mapping_tag_target_member_schema_matrix() {
    let mut changed_target = JunctionContext::new("QA-target-identity");
    let selected = changed_target.selected_mapping();
    changed_target.create_physical_target(&selected.target);
    let same_bytes_elsewhere = selected.target.with_file_name("same-bytes-elsewhere");
    changed_target.create_physical_target(&same_bytes_elsewhere);
    changed_target.junction(&selected.path, &same_bytes_elsewhere);
    let selected_policy = changed_target.policy(selected);
    assert!(
        collect_with_policy(
            &changed_target.fixture,
            &changed_target.roots,
            &selected_policy,
        )
        .is_err(),
        "same control bytes at an unreviewed target must not establish identity"
    );

    let mut wrong_tag = JunctionContext::new("QA-tag-identity");
    let selected = wrong_tag.exact_mapping();
    let mut wrong_tag_policy = wrong_tag.policy(selected);
    wrong_tag_policy.junctions[0].reparse_tag = 0xa000000c;
    assert!(
        collect_with_policy(&wrong_tag.fixture, &wrong_tag.roots, &wrong_tag_policy).is_err(),
        "a real directory junction must not satisfy a symbolic-link tag claim"
    );

    let mut membership = JunctionContext::new("QA-membership-schema");
    let selected = membership.exact_mapping();
    let policy = membership.policy(selected.clone());
    let inventory = collect_with_policy(&membership.fixture, &membership.roots, &policy)
        .expect("exact reviewed mapping setup must collect before the negative stimuli");
    assert_eq!(inventory.junctions.len(), 1);
    assert_eq!(inventory.junctions[0].path, selected.path);
    assert_eq!(inventory.junctions[0].target, selected.target);
    assert_eq!(inventory.junctions[0].reparse_tag, JUNCTION_TAG);
    let bindings = inventory.file_bindings();
    let unique_bindings: std::collections::HashSet<_> = bindings
        .iter()
        .map(|(path, _)| path.to_string_lossy().to_ascii_lowercase())
        .collect();
    assert_eq!(unique_bindings.len(), bindings.len());
    assert!(
        bindings
            .iter()
            .all(|(path, _)| !path.starts_with(&selected.path)),
        "physical controls must not be read through the logical alias"
    );
    let plugin_directory = selected.target.parent().unwrap();
    let mut independent_members = Vec::new();
    for child in fs::read_dir(plugin_directory).unwrap() {
        let child = child.unwrap();
        let name = child.file_name().into_string().unwrap();
        let metadata = fs::symlink_metadata(child.path()).unwrap();
        let kind = if metadata.file_attributes() & 0x400 != 0 {
            b'j'
        } else if metadata.is_dir() {
            b'd'
        } else {
            b'f'
        };
        independent_members.push((name, kind));
    }
    independent_members.sort_by(|left, right| {
        (left.0.to_ascii_lowercase(), &left.0, left.1).cmp(&(
            right.0.to_ascii_lowercase(),
            &right.0,
            right.1,
        ))
    });
    let mut encoded_members = Vec::new();
    for (name, kind) in &independent_members {
        encoded_members.push(*kind);
        encoded_members.extend_from_slice(&(name.len() as u32).to_le_bytes());
        encoded_members.extend_from_slice(name.as_bytes());
    }
    let expected_index = format!("{:x}", sha2::Sha256::digest(&encoded_members));
    let canonical_plugin_directory = fs::canonicalize(plugin_directory).unwrap();
    let observed_index = inventory
        .entries
        .iter()
        .find(|entry| {
            entry.state == SourceState::DirectoryIndex && entry.path == canonical_plugin_directory
        })
        .expect("plugin member index must be retained");
    assert_eq!(observed_index.items, Some(independent_members.len() as u32));
    assert_eq!(
        observed_index.sha256.as_deref(),
        Some(expected_index.as_str())
    );

    fs::write(selected.target.join("new-control.txt"), b"member drift\n").unwrap();
    assert!(
        verify_with_policy(&inventory, &membership.roots, &policy).is_err(),
        "an added indexed member must invalidate the retained inventory"
    );

    let mut schema_context = JunctionContext::new("QA-schema-wire");
    let schema_mapping = schema_context.exact_mapping();
    let schema_policy = schema_context.policy(schema_mapping);
    let schema_inventory = collect_with_policy(
        &schema_context.fixture,
        &schema_context.roots,
        &schema_policy,
    )
    .unwrap();
    let mut old_schema = serde_json::to_value(&schema_inventory).unwrap();
    old_schema["schema_version"] = serde_json::json!(1);
    let old_schema: Inventory = serde_json::from_value(old_schema).unwrap();
    assert!(
        verify_with_policy(&old_schema, &schema_context.roots, &schema_policy).is_err(),
        "schema 1 cannot qualify schema 2"
    );

    let mut unknown_field = serde_json::to_value(&schema_inventory).unwrap();
    unknown_field["qa_unknown"] = serde_json::json!(true);
    assert!(serde_json::from_value::<Inventory>(unknown_field).is_err());

    let mut wrong_inventory_tag = schema_inventory.clone();
    wrong_inventory_tag.junctions[0].reparse_tag = 0xa000000c;
    assert!(
        verify_with_policy(&wrong_inventory_tag, &schema_context.roots, &schema_policy,).is_err(),
        "an inventory cannot relabel the observed junction type"
    );
}
