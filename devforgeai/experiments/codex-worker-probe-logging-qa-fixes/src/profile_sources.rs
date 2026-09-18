use crate::{
    native_identity,
    request::{Result, digest, resolve, valid_digest},
};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    ffi::OsStr,
    fs,
    io::Read,
    os::windows::fs::MetadataExt,
    path::{Component, Path, PathBuf},
};

pub const PLUGIN_SOURCE_RECORD: &[u8] = include_bytes!("plugin-source-identity.json");
const SCHEMA_VERSION: u32 = 2;
const SOURCE_IDENTITY_SCHEMA_VERSION: u32 = 1;
const SOURCE_IDENTITY_ADAPTER: &str = "codex-0.154.0-stdio";
const DIRECTORY_JUNCTION_TAG: u32 = 0xa0000003;
const SELECTED_LOGICAL_PATH: &str =
    r"C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest";
const SELECTED_PHYSICAL_TARGET: &str =
    r"C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\26.908.70816";
const MAX_FILE_BYTES: u64 = 1_048_576;
const MAX_TOTAL_BYTES: u64 = 8_388_608;
const MAX_ENTRIES: usize = 2_048;
const MAX_DIRECTORY_CHILDREN: usize = 1_024;
const MAX_ANCESTOR_DEPTH: usize = 32;
const MAX_RULE_DEPTH: usize = 8;

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Inventory {
    schema_version: u32,
    fixture_cwd: PathBuf,
    roots: InventoryRoots,
    source_identity_sha256: String,
    junctions: Vec<PluginJunction>,
    entries: Vec<SourceEntry>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
struct PluginJunction {
    path: PathBuf,
    target: PathBuf,
    reparse_tag: u32,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
struct PluginSourceIdentity {
    schema_version: u32,
    adapter: String,
    junctions: Vec<PluginJunction>,
}

#[derive(Clone, Debug)]
struct PluginSourcePolicy {
    digest: String,
    junctions: Vec<PluginJunction>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
struct InventoryRoots {
    ancestor_root: PathBuf,
    workspace_root: PathBuf,
    user_codex_root: PathBuf,
    program_data_codex_root: PathBuf,
    plugin_cache_root: PathBuf,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(deny_unknown_fields)]
struct SourceEntry {
    family: SourceFamily,
    path: PathBuf,
    state: SourceState,
    sha256: Option<String>,
    bytes: Option<u64>,
    items: Option<u32>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "snake_case")]
enum SourceFamily {
    Ancestor,
    User,
    Rules,
    System,
    Plugin,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "snake_case")]
enum SourceState {
    File,
    Absent,
    DirectoryIndex,
}

#[derive(Clone, Debug)]
struct Roots {
    ancestor_root: PathBuf,
    workspace_root: PathBuf,
    user_codex_root: PathBuf,
    program_data_codex_root: PathBuf,
    plugin_cache_root: PathBuf,
}

impl Roots {
    fn actual(fixture_cwd: &Path) -> Result<Self> {
        let package = strict_resolve(Path::new(env!("CARGO_MANIFEST_DIR")))?;
        let workspace_root = package
            .ancestors()
            .nth(3)
            .ok_or("profile_source_workspace")?
            .to_path_buf();
        let fixture = strict_resolve(fixture_cwd)?;
        let ancestor_root = fixture
            .ancestors()
            .last()
            .ok_or("profile_source_fixture_scope")?
            .to_path_buf();
        let user_profile = required_absolute_env("USERPROFILE")?;
        let program_data = required_absolute_env("ProgramData")?;
        let user_codex_root = user_profile.join(".codex");
        Ok(Self {
            ancestor_root,
            workspace_root,
            plugin_cache_root: user_codex_root.join("plugins").join("cache"),
            user_codex_root,
            program_data_codex_root: program_data.join("OpenAI").join("Codex"),
        })
    }
}

impl PluginSourcePolicy {
    fn compiled(roots: &Roots) -> Result<Self> {
        Self::from_record(PLUGIN_SOURCE_RECORD, &roots.plugin_cache_root)
    }

    fn from_record(record: &[u8], plugin_cache_root: &Path) -> Result<Self> {
        let identity: PluginSourceIdentity =
            serde_json::from_slice(record).map_err(|_| "profile_source_identity")?;
        let expected_path = Path::new(SELECTED_LOGICAL_PATH);
        let expected_target = Path::new(SELECTED_PHYSICAL_TARGET);
        let Some(junction) = identity.junctions.first() else {
            return Err("profile_source_identity".into());
        };
        if identity.schema_version != SOURCE_IDENTITY_SCHEMA_VERSION
            || identity.adapter != SOURCE_IDENTITY_ADAPTER
            || identity.junctions.len() != 1
            || junction.reparse_tag != DIRECTORY_JUNCTION_TAG
            || !plain_local_path(&junction.path)
            || !plain_local_path(&junction.target)
            || !native_identity::same(&junction.path, expected_path)
            || !native_identity::same(&junction.target, expected_target)
            || junction.path.parent() != junction.target.parent()
        {
            return Err("profile_source_identity".into());
        }
        let selected = PluginJunction {
            path: native_identity::normalized(&junction.path),
            target: native_identity::normalized(&junction.target),
            reparse_tag: junction.reparse_tag,
        };
        let selected_cache_root = expected_path
            .ancestors()
            .nth(3)
            .ok_or("profile_source_identity")?;
        let junctions = if native_identity::same(plugin_cache_root, selected_cache_root) {
            vec![selected]
        } else {
            Vec::new()
        };
        Ok(Self {
            digest: digest(record),
            junctions,
        })
    }

    #[cfg(test)]
    fn empty_for_regressions() -> Self {
        Self {
            digest: digest(b"test-only-empty-plugin-source-identity-v1"),
            junctions: Vec::new(),
        }
    }
}

fn plain_local_path(path: &Path) -> bool {
    native_identity::local_absolute(path)
        && !path
            .components()
            .any(|part| matches!(part, Component::CurDir | Component::ParentDir))
}

impl Inventory {
    pub fn fixture_cwd(&self) -> &Path {
        &self.fixture_cwd
    }

    pub fn file_paths(&self) -> Vec<PathBuf> {
        self.file_bindings()
            .into_iter()
            .map(|(path, _)| path)
            .collect()
    }

    pub fn file_bindings(&self) -> Vec<(PathBuf, String)> {
        let mut files: Vec<_> = self
            .entries
            .iter()
            .filter_map(|entry| {
                if entry.state == SourceState::File {
                    entry
                        .sha256
                        .as_ref()
                        .map(|digest| (entry.path.clone(), digest.clone()))
                } else {
                    None
                }
            })
            .collect();
        files.sort();
        files
    }

    pub fn verify(&self) -> Result<()> {
        let roots = Roots::actual(&self.fixture_cwd)?;
        let policy = PluginSourcePolicy::compiled(&roots)?;
        verify_with_policy(self, &roots, &policy)
    }
}

pub fn collect(fixture_cwd: &Path) -> Result<Inventory> {
    let roots = Roots::actual(fixture_cwd)?;
    let policy = PluginSourcePolicy::compiled(&roots)?;
    collect_with_policy(fixture_cwd, &roots, &policy)
}

fn collect_with_policy(
    fixture_cwd: &Path,
    roots: &Roots,
    policy: &PluginSourcePolicy,
) -> Result<Inventory> {
    collect_with_policy_using(fixture_cwd, roots, policy, || {})
}

fn collect_with_policy_using<F>(
    fixture_cwd: &Path,
    roots: &Roots,
    policy: &PluginSourcePolicy,
    before_final_mapping_check: F,
) -> Result<Inventory>
where
    F: FnOnce(),
{
    let fixture_cwd = strict_resolve(fixture_cwd)?;
    require_directory(&fixture_cwd)?;
    let ancestor_root = strict_resolve(&roots.ancestor_root)?;
    let workspace_root = strict_resolve(&roots.workspace_root)?;
    require_directory(&ancestor_root)?;
    require_directory(&workspace_root)?;
    if !workspace_root.starts_with(&ancestor_root) || !fixture_cwd.starts_with(&workspace_root) {
        return Err("profile_source_fixture_scope".into());
    }

    let user_codex_root = expected_path(&roots.user_codex_root)?.0;
    let program_data_codex_root = expected_path(&roots.program_data_codex_root)?.0;
    let plugin_cache_root = expected_path(&roots.plugin_cache_root)?.0;
    let normalized_roots = InventoryRoots {
        ancestor_root: ancestor_root.clone(),
        workspace_root,
        user_codex_root: user_codex_root.clone(),
        program_data_codex_root: program_data_codex_root.clone(),
        plugin_cache_root: plugin_cache_root.clone(),
    };
    verify_policy_mappings(policy)?;
    let mut collector = Collector::default();

    for directory in scoped_ancestors(&ancestor_root, &fixture_cwd)? {
        for relative in [
            Path::new("AGENTS.md"),
            Path::new("AGENTS.override.md"),
            Path::new(".codex/config.toml"),
            Path::new(".codex/requirements.toml"),
            Path::new(".codex/hooks.json"),
        ] {
            collector.add_file_or_absent(SourceFamily::Ancestor, &directory.join(relative))?;
        }
    }

    for name in [
        "config.toml",
        "requirements.toml",
        "hooks.json",
        "AGENTS.md",
        "AGENTS.override.md",
    ] {
        collector.add_file_or_absent(SourceFamily::User, &user_codex_root.join(name))?;
    }
    collector.walk_rules(&user_codex_root.join("rules"), 0)?;

    for name in ["config.toml", "requirements.toml", "hooks.json"] {
        collector.add_file_or_absent(SourceFamily::System, &program_data_codex_root.join(name))?;
    }
    collector.walk_plugins(&plugin_cache_root, policy)?;

    if collector.observed_junctions != policy.junctions {
        return Err("profile_source_identity".into());
    }
    before_final_mapping_check();
    verify_policy_mappings(policy)?;

    collector.entries.sort_by(|left, right| {
        (
            left.family,
            &left.path,
            left.state,
            &left.sha256,
            left.bytes,
            left.items,
        )
            .cmp(&(
                right.family,
                &right.path,
                right.state,
                &right.sha256,
                right.bytes,
                right.items,
            ))
    });
    Ok(Inventory {
        schema_version: SCHEMA_VERSION,
        fixture_cwd,
        roots: normalized_roots,
        source_identity_sha256: policy.digest.clone(),
        junctions: collector.observed_junctions,
        entries: collector.entries,
    })
}

fn verify_policy_mappings(policy: &PluginSourcePolicy) -> Result<()> {
    for mapping in &policy.junctions {
        verify_reviewed_junction(&mapping.path, mapping)?;
    }
    Ok(())
}

fn verify_with_policy(
    inventory: &Inventory,
    roots: &Roots,
    policy: &PluginSourcePolicy,
) -> Result<()> {
    if !inventory.valid_shape() {
        return Err("profile_source_schema".into());
    }
    if inventory.source_identity_sha256 != policy.digest || inventory.junctions != policy.junctions
    {
        return Err("profile_source_identity".into());
    }
    let fresh = collect_with_policy(&inventory.fixture_cwd, roots, policy)?;
    if &fresh != inventory {
        return Err("profile_source_drift".into());
    }
    Ok(())
}

#[cfg(test)]
fn collect_with_roots(fixture_cwd: &Path, roots: &Roots) -> Result<Inventory> {
    collect_with_policy(
        fixture_cwd,
        roots,
        &PluginSourcePolicy::empty_for_regressions(),
    )
}

#[cfg(test)]
fn verify_with_roots(inventory: &Inventory, roots: &Roots) -> Result<()> {
    verify_with_policy(
        inventory,
        roots,
        &PluginSourcePolicy::empty_for_regressions(),
    )
}

impl Inventory {
    fn valid_shape(&self) -> bool {
        self.schema_version == SCHEMA_VERSION
            && valid_digest(&self.source_identity_sha256)
            && valid_junction_shape(&self.junctions)
            && self.entries.iter().all(|entry| match entry.state {
                SourceState::File => {
                    entry.sha256.as_deref().is_some_and(valid_digest)
                        && entry.bytes.is_some_and(|bytes| bytes <= MAX_FILE_BYTES)
                        && entry.items.is_none()
                }
                SourceState::Absent => {
                    entry.sha256.is_none() && entry.bytes.is_none() && entry.items.is_none()
                }
                SourceState::DirectoryIndex => {
                    entry.sha256.as_deref().is_some_and(valid_digest)
                        && entry.bytes.is_none()
                        && entry
                            .items
                            .is_some_and(|items| items as usize <= MAX_DIRECTORY_CHILDREN)
                }
            })
    }
}

fn valid_junction_shape(junctions: &[PluginJunction]) -> bool {
    let mut paths = std::collections::HashSet::new();
    junctions.iter().all(|junction| {
        junction.reparse_tag == DIRECTORY_JUNCTION_TAG
            && plain_local_path(&junction.path)
            && plain_local_path(&junction.target)
            && !native_identity::same(&junction.path, &junction.target)
            && paths.insert(
                native_identity::normalized(&junction.path)
                    .to_string_lossy()
                    .to_ascii_lowercase(),
            )
    })
}

#[derive(Default)]
struct Collector {
    entries: Vec<SourceEntry>,
    total_bytes: u64,
    observed_junctions: Vec<PluginJunction>,
}

impl Collector {
    fn push(&mut self, entry: SourceEntry) -> Result<()> {
        if self.entries.len() >= MAX_ENTRIES {
            return Err("profile_source_limit".into());
        }
        self.entries.push(entry);
        Ok(())
    }

    fn add_file_or_absent(&mut self, family: SourceFamily, path: &Path) -> Result<()> {
        let (path, exists) = expected_path(path)?;
        if !exists {
            return self.push(SourceEntry {
                family,
                path,
                state: SourceState::Absent,
                sha256: None,
                bytes: None,
                items: None,
            });
        }
        self.add_file(family, &path)
    }

    fn add_file(&mut self, family: SourceFamily, path: &Path) -> Result<()> {
        if forbidden_name(path.file_name().unwrap_or_default()) {
            return Err("profile_source_forbidden_name".into());
        }
        let path = strict_resolve(path)?;
        let metadata = fs::metadata(&path).map_err(|_| "profile_source_inaccessible")?;
        if !metadata.is_file() {
            return Err("profile_source_type".into());
        }
        let bytes = metadata.len();
        if bytes > MAX_FILE_BYTES
            || self
                .total_bytes
                .checked_add(bytes)
                .is_none_or(|total| total > MAX_TOTAL_BYTES)
        {
            return Err("profile_source_limit".into());
        }
        let first = hash_once(&path, bytes)?;
        let second = hash_once(&path, bytes)?;
        let final_metadata = fs::metadata(&path).map_err(|_| "profile_source_inaccessible")?;
        if first != second || final_metadata.len() != bytes || !final_metadata.is_file() {
            return Err("profile_source_drift".into());
        }
        self.total_bytes += bytes;
        self.push(SourceEntry {
            family,
            path,
            state: SourceState::File,
            sha256: Some(first),
            bytes: Some(bytes),
            items: None,
        })
    }

    fn add_directory_index(
        &mut self,
        family: SourceFamily,
        directory: &Path,
        members: &[Member],
    ) -> Result<()> {
        let mut encoded = Vec::new();
        for member in members {
            let name = member.name.as_bytes();
            encoded.push(match member.kind {
                MemberKind::File => b'f',
                MemberKind::Directory => b'd',
                MemberKind::Junction => b'j',
            });
            encoded.extend_from_slice(&(name.len() as u32).to_le_bytes());
            encoded.extend_from_slice(name);
        }
        self.push(SourceEntry {
            family,
            path: strict_resolve(directory)?,
            state: SourceState::DirectoryIndex,
            sha256: Some(digest(&encoded)),
            bytes: None,
            items: Some(members.len() as u32),
        })
    }

    fn walk_rules(&mut self, directory: &Path, depth: usize) -> Result<()> {
        let (directory, exists) = expected_path(directory)?;
        if !exists {
            return self.push(SourceEntry {
                family: SourceFamily::Rules,
                path: directory,
                state: SourceState::Absent,
                sha256: None,
                bytes: None,
                items: None,
            });
        }
        if depth > MAX_RULE_DEPTH {
            return Err("profile_source_limit".into());
        }
        require_directory(&directory)?;
        let members = stable_directory(&directory)?;
        self.add_directory_index(SourceFamily::Rules, &directory, &members)?;
        for member in members {
            match member.kind {
                MemberKind::File => self.add_file(SourceFamily::Rules, &member.path)?,
                MemberKind::Directory => self.walk_rules(&member.path, depth + 1)?,
                MemberKind::Junction => {
                    return Err(format!("profile_source_reparse:{}", member.path.display()));
                }
            }
        }
        Ok(())
    }

    fn walk_plugins(&mut self, cache: &Path, policy: &PluginSourcePolicy) -> Result<()> {
        let (cache, exists) = expected_path(cache)?;
        if !exists {
            return self.push(SourceEntry {
                family: SourceFamily::Plugin,
                path: cache,
                state: SourceState::Absent,
                sha256: None,
                bytes: None,
                items: None,
            });
        }
        require_directory(&cache)?;
        let providers = stable_directory(&cache)?;
        self.add_directory_index(SourceFamily::Plugin, &cache, &providers)?;
        for provider in providers {
            if provider.kind != MemberKind::Directory {
                return Err("profile_source_unrecognized".into());
            }
            self.walk_plugin_provider(&provider.path, policy)?;
        }
        Ok(())
    }

    fn walk_plugin_provider(&mut self, provider: &Path, policy: &PluginSourcePolicy) -> Result<()> {
        let plugins = stable_directory(provider)?;
        self.add_directory_index(SourceFamily::Plugin, provider, &plugins)?;
        for plugin in plugins {
            if plugin.kind != MemberKind::Directory {
                return Err("profile_source_unrecognized".into());
            }
            self.walk_plugin(&plugin.path, policy)?;
        }
        Ok(())
    }

    fn walk_plugin(&mut self, plugin: &Path, policy: &PluginSourcePolicy) -> Result<()> {
        let members = stable_plugin_directory(plugin, policy)?;
        self.add_directory_index(SourceFamily::Plugin, plugin, &members)?;
        for mapping in policy.junctions.iter().filter(|mapping| {
            mapping
                .path
                .parent()
                .is_some_and(|parent| native_identity::same(parent, plugin))
        }) {
            let alias_observed = members.iter().any(|member| {
                member.kind == MemberKind::Junction
                    && native_identity::same(&member.path, &mapping.path)
            });
            let target_observed = members.iter().any(|member| {
                member.kind == MemberKind::Directory
                    && native_identity::same(&member.path, &mapping.target)
            });
            if !alias_observed
                || !target_observed
                || self
                    .observed_junctions
                    .iter()
                    .any(|observed| native_identity::same(&observed.path, &mapping.path))
            {
                return Err("profile_source_identity".into());
            }
            self.observed_junctions.push(mapping.clone());
        }
        for member in members {
            match member.kind {
                MemberKind::Directory => self.walk_plugin_version(&member.path)?,
                MemberKind::Junction => {}
                MemberKind::File if member.name == ".codex-remote-plugin-install.json" => {
                    self.add_file(SourceFamily::Plugin, &member.path)?
                }
                MemberKind::File => return Err("profile_source_unrecognized".into()),
            }
        }
        Ok(())
    }

    fn walk_plugin_version(&mut self, version: &Path) -> Result<()> {
        let members = stable_directory(version)?;
        self.add_directory_index(SourceFamily::Plugin, version, &members)?;
        for member in members {
            match (member.kind, member.name.as_str()) {
                (
                    MemberKind::File,
                    ".mcp.json" | ".app.json" | "hooks.json" | "config.toml" | "requirements.toml",
                ) => self.add_file(SourceFamily::Plugin, &member.path)?,
                (MemberKind::Directory, ".codex-plugin") => {
                    self.walk_plugin_control(&member.path)?
                }
                _ => {}
            }
        }
        Ok(())
    }

    fn walk_plugin_control(&mut self, directory: &Path) -> Result<()> {
        let members = stable_directory(directory)?;
        self.add_directory_index(SourceFamily::Plugin, directory, &members)?;
        for member in members {
            match (member.kind, member.name.as_str()) {
                (
                    MemberKind::File,
                    "plugin.json" | "hooks.json" | "config.toml" | "requirements.toml",
                ) => self.add_file(SourceFamily::Plugin, &member.path)?,
                _ => return Err("profile_source_unrecognized".into()),
            }
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct Member {
    name: String,
    path: PathBuf,
    kind: MemberKind,
}

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
enum MemberKind {
    File,
    Directory,
    Junction,
}

fn stable_directory(directory: &Path) -> Result<Vec<Member>> {
    let first = directory_snapshot(directory)?;
    let second = directory_snapshot(directory)?;
    if first != second {
        return Err("profile_source_drift".into());
    }
    Ok(first)
}

fn stable_plugin_directory(directory: &Path, policy: &PluginSourcePolicy) -> Result<Vec<Member>> {
    let first = directory_snapshot_with_policy(directory, Some(policy))?;
    let second = directory_snapshot_with_policy(directory, Some(policy))?;
    if first != second {
        return Err("profile_source_drift".into());
    }
    Ok(first)
}

fn directory_snapshot(directory: &Path) -> Result<Vec<Member>> {
    directory_snapshot_with_policy(directory, None)
}

fn directory_snapshot_with_policy(
    directory: &Path,
    policy: Option<&PluginSourcePolicy>,
) -> Result<Vec<Member>> {
    let directory = strict_resolve(directory)?;
    require_directory(&directory)?;
    let reader = fs::read_dir(&directory).map_err(|_| "profile_source_inaccessible")?;
    let mut members = Vec::new();
    for item in reader {
        if members.len() >= MAX_DIRECTORY_CHILDREN {
            return Err("profile_source_limit".into());
        }
        let item = item.map_err(|_| "profile_source_inaccessible")?;
        let name = item
            .file_name()
            .into_string()
            .map_err(|_| "profile_source_non_utf8")?;
        if forbidden_name(OsStr::new(&name)) {
            return Err("profile_source_forbidden_name".into());
        }
        let path = directory.join(&name);
        let metadata = fs::symlink_metadata(&path).map_err(|_| "profile_source_inaccessible")?;
        let kind = if metadata.file_attributes() & 0x400 != 0 {
            let Some(mapping) = policy.and_then(|policy| {
                policy
                    .junctions
                    .iter()
                    .find(|mapping| native_identity::same(&mapping.path, &path))
            }) else {
                return Err(format!("profile_source_reparse:{}", path.display()));
            };
            verify_reviewed_junction(&path, mapping)?;
            MemberKind::Junction
        } else if metadata.is_file() {
            MemberKind::File
        } else if metadata.is_dir() {
            MemberKind::Directory
        } else {
            return Err("profile_source_type".into());
        };
        members.push(Member { name, path, kind });
    }
    members.sort_by(|left, right| {
        (left.name.to_ascii_lowercase(), &left.name, left.kind).cmp(&(
            right.name.to_ascii_lowercase(),
            &right.name,
            right.kind,
        ))
    });
    Ok(members)
}

fn verify_reviewed_junction(path: &Path, mapping: &PluginJunction) -> Result<()> {
    let error = || format!("profile_source_reparse:{}", path.display());
    if mapping.reparse_tag != DIRECTORY_JUNCTION_TAG
        || !native_identity::same(path, &mapping.path)
        || path
            .parent()
            .zip(mapping.target.parent())
            .is_none_or(|(left, right)| !native_identity::same(left, right))
    {
        return Err("profile_source_identity".into());
    }
    let parent = strict_resolve(path.parent().ok_or("profile_source_identity")?)?;
    require_directory(&parent)?;
    let first = native_identity::first_reparse(path).map_err(|_| error())?;
    if first
        .as_deref()
        .is_none_or(|first| !native_identity::same(first, path))
        || !native_identity::directory_junction(path).map_err(|_| error())?
    {
        return Err(error());
    }
    let target = fs::read_link(path).map_err(|_| error())?;
    if !plain_local_path(&target) || !native_identity::same(&target, &mapping.target) {
        return Err("profile_source_identity".into());
    }
    if native_identity::first_reparse(&target)
        .map_err(|_| error())?
        .is_some()
    {
        return Err(error());
    }
    let target = strict_resolve(&target)?;
    require_directory(&target)?;
    Ok(())
}

fn hash_once(path: &Path, expected_bytes: u64) -> Result<String> {
    let mut file = fs::File::open(path).map_err(|_| "profile_source_inaccessible")?;
    let mut hasher = Sha256::new();
    let mut total = 0_u64;
    let mut block = [0_u8; 65_536];
    loop {
        let read = file
            .read(&mut block)
            .map_err(|_| "profile_source_inaccessible")?;
        if read == 0 {
            break;
        }
        total = total
            .checked_add(read as u64)
            .ok_or("profile_source_limit")?;
        if total > MAX_FILE_BYTES {
            return Err("profile_source_limit".into());
        }
        hasher.update(&block[..read]);
    }
    if total != expected_bytes {
        return Err("profile_source_drift".into());
    }
    Ok(format!("{:x}", hasher.finalize()))
}

fn strict_resolve(path: &Path) -> Result<PathBuf> {
    resolve(path).map_err(|error| {
        if error == "reparse_path" {
            format!("profile_source_reparse:{}", path.display())
        } else {
            format!("profile_source_path:{}", path.display())
        }
    })
}

fn expected_path(path: &Path) -> Result<(PathBuf, bool)> {
    if !path.is_absolute()
        || path
            .components()
            .any(|component| matches!(component, Component::ParentDir))
    {
        return Err("profile_source_path".into());
    }
    let mut existing = path;
    loop {
        match fs::symlink_metadata(existing) {
            Ok(_) => {
                let resolved = strict_resolve(existing)?;
                if existing == path {
                    return Ok((resolved, true));
                }
                let suffix = path
                    .strip_prefix(existing)
                    .map_err(|_| "profile_source_path")?;
                return Ok((resolved.join(suffix), false));
            }
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
                existing = existing.parent().ok_or("profile_source_path")?;
            }
            Err(_) => return Err("profile_source_inaccessible".into()),
        }
    }
}

fn require_directory(path: &Path) -> Result<()> {
    if fs::metadata(path)
        .map_err(|_| "profile_source_inaccessible")?
        .is_dir()
    {
        Ok(())
    } else {
        Err("profile_source_type".into())
    }
}

fn required_absolute_env(name: &str) -> Result<PathBuf> {
    let value = std::env::var_os(name).ok_or("profile_source_environment")?;
    let path = PathBuf::from(value);
    if !path.is_absolute()
        || path
            .components()
            .any(|component| matches!(component, Component::ParentDir))
    {
        return Err("profile_source_environment".into());
    }
    Ok(path)
}

fn scoped_ancestors(root: &Path, leaf: &Path) -> Result<Vec<PathBuf>> {
    let mut result = Vec::new();
    let mut current = leaf;
    loop {
        if result.len() >= MAX_ANCESTOR_DEPTH {
            return Err("profile_source_limit".into());
        }
        result.push(current.to_path_buf());
        if current == root {
            break;
        }
        current = current.parent().ok_or("profile_source_fixture_scope")?;
    }
    result.reverse();
    Ok(result)
}

fn forbidden_name(name: &OsStr) -> bool {
    let Some(name) = name.to_str() else {
        return true;
    };
    let lower = name.to_ascii_lowercase();
    lower == "auth.json"
        || lower.starts_with(".env")
        || lower.contains("credential")
        || lower.contains("secret")
        || lower.contains("token")
}

#[cfg(test)]
#[path = "../tests/support/profile_sources_cases.rs"]
mod cases;

#[cfg(test)]
#[path = "../tests/support/profile_sources_edges.rs"]
mod edges;

#[cfg(test)]
#[path = "../tests/support/plugin_source_identity_cases.rs"]
mod plugin_source_identity_cases;
