//! Closed, secret-free validation of Codex pre-thread profile observations.
use crate::diagnostic::{ConfigPredicate, ConfigSection};
use crate::request::Result;
use serde_json::{Map, Value, json};
use std::{
    collections::HashSet,
    path::{Component, Path, PathBuf},
};

const MAX_PAGES: usize = 10;
const MAX_PAGE_ITEMS: usize = 100;
const MAX_INVENTORY_ITEMS: usize = 1_000;
// Closed against the pinned rust-v0.154.0 feature registry. These flags are
// compatibility no-ops, presentation/protocol metadata, or bounded transport
// and first-party model-service behavior. Every other enabled flag is rejected.
const ALLOWED_ENABLED_FEATURES: &[&str] = &[
    "collaboration_modes",
    "compaction_image_budget",
    "content_item_kinds",
    "enable_request_compression",
    "fast_mode",
    "item_ids",
    "mentions_v2",
    "personality",
    "remote_compaction_v2",
    "resize_all_images",
    "secret_auth_storage",
    "steer",
    "terminal_resize_reflow",
    "tool_search_always_defer_mcp_tools",
    "tui_app_server",
    "unbounded_connection_retries",
    "unified_exec_zsh_fork",
];
const MCP_IDS: &[&str] = &["node_repl", "openaiDeveloperDocs"];
const APP_IDS: &[&str] = &["connector_openai_codex_document_control"];
const PLUGIN_IDS: &[&str] = &[
    "documents@openai-primary-runtime",
    "pdf@openai-primary-runtime",
    "spreadsheets@openai-primary-runtime",
    "presentations@openai-primary-runtime",
    "template-creator@openai-primary-runtime",
    "sites@openai-bundled",
    "visualize@openai-bundled",
    "codex-app-tools@openai-bundled",
    "computer-use@openai-bundled",
    "unified-computer-use@openai-bundled",
    "browser@openai-bundled",
    "chrome@openai-bundled",
];

fn malformed<T>() -> Result<T> {
    Err("protocol_error".into())
}

fn unqualified<T>() -> Result<T> {
    Err("profile_unqualified".into())
}

fn object(value: &Value) -> Result<&Map<String, Value>> {
    value.as_object().ok_or_else(|| "protocol_error".into())
}

fn array(value: Option<&Value>) -> Result<&Vec<Value>> {
    value
        .and_then(Value::as_array)
        .ok_or_else(|| "protocol_error".into())
}

fn bounded_string(value: Option<&Value>, max: usize) -> Result<&str> {
    let value = value
        .and_then(Value::as_str)
        .ok_or_else(|| "protocol_error".to_owned())?;
    if value.is_empty() || value.len() > max {
        return malformed();
    }
    Ok(value)
}

fn required_bool(value: Option<&Value>) -> Result<bool> {
    value
        .and_then(Value::as_bool)
        .ok_or_else(|| "protocol_error".into())
}

fn exact_keys(map: &Map<String, Value>, expected: &[&str]) -> Result<()> {
    if map.len() != expected.len() || !expected.iter().all(|key| map.contains_key(*key)) {
        return unqualified();
    }
    Ok(())
}

fn normalized_path(path: &Path) -> Result<String> {
    if !path.is_absolute()
        || path
            .components()
            .any(|part| matches!(part, Component::ParentDir | Component::CurDir))
    {
        return unqualified();
    }
    let mut value = path.to_string_lossy().replace('/', "\\");
    if let Some(stripped) = value.strip_prefix(r"\\?\") {
        value = stripped.to_owned();
    } else if let Some(stripped) = value.strip_prefix(r"\??\") {
        value = stripped.to_owned();
    }
    while value.len() > 3 && value.ends_with('\\') {
        value.pop();
    }
    Ok(value.to_ascii_lowercase())
}

fn path_covered(path: &Path, covered: &HashSet<String>) -> Result<()> {
    if !covered.contains(&normalized_path(path)?) {
        return unqualified();
    }
    Ok(())
}

fn false_map(value: Option<&Value>, required: &[&str], exact: bool) -> Result<()> {
    let map = value.and_then(Value::as_object).ok_or("protocol_error")?;
    if exact {
        exact_keys(map, required)?;
    }
    for required_name in required {
        let entry = map
            .get(*required_name)
            .and_then(Value::as_object)
            .ok_or("profile_unqualified")?;
        if entry.get("enabled") != Some(&Value::Bool(false)) {
            return unqualified();
        }
        if exact {
            exact_keys(entry, &["enabled"])?;
        }
    }
    for entry in map.values() {
        let entry = entry.as_object().ok_or("protocol_error")?;
        if entry.get("enabled") != Some(&Value::Bool(false)) {
            return unqualified();
        }
    }
    Ok(())
}

fn fixed_feature_map(value: Option<&Value>, exact: bool) -> Result<()> {
    let features = value.and_then(Value::as_object).ok_or("protocol_error")?;
    if exact {
        exact_keys(features, crate::launch_policy::REQUIRED_DISABLED_FEATURES)?;
    }
    for name in crate::launch_policy::REQUIRED_DISABLED_FEATURES {
        if features.get(*name) != Some(&Value::Bool(false)) {
            return unqualified();
        }
    }
    Ok(())
}

fn fixed_apps(value: Option<&Value>, exact: bool) -> Result<()> {
    let apps = value.and_then(Value::as_object).ok_or("protocol_error")?;
    if exact {
        exact_keys(apps, &["_default", APP_IDS[0]])?;
    }
    let default = apps
        .get("_default")
        .and_then(Value::as_object)
        .ok_or("profile_unqualified")?;
    if default.get("enabled") != Some(&Value::Bool(false)) {
        return unqualified();
    }
    if exact {
        exact_keys(default, &["enabled"])?;
    }
    for (name, entry) in apps {
        if name == "_default" {
            continue;
        }
        let entry = entry.as_object().ok_or("protocol_error")?;
        if entry.get("enabled") != Some(&Value::Bool(false)) {
            return unqualified();
        }
        if exact {
            exact_keys(entry, &["enabled"])?;
        }
    }
    if !APP_IDS.iter().all(|name| apps.contains_key(*name)) {
        return unqualified();
    }
    Ok(())
}

fn fixed_config(config: &Value, exact: bool, predicate: &mut ConfigPredicate) -> Result<()> {
    *predicate = ConfigPredicate::Shape;
    let config = object(config)?;
    if exact {
        *predicate = ConfigPredicate::FixedKeys;
        exact_keys(
            config,
            &[
                "model_provider",
                "forced_login_method",
                "web_search",
                "sandbox_mode",
                "approval_policy",
                "features",
                "apps",
                "mcp_servers",
                "plugins",
            ],
        )?;
    }
    *predicate = ConfigPredicate::ProviderMap;
    if let Some(providers) = config.get("model_providers") {
        match providers {
            Value::Null => {}
            Value::Object(entries) if entries.is_empty() => {}
            Value::Object(_) => return unqualified(),
            _ => return malformed(),
        }
    }
    *predicate = ConfigPredicate::EndpointOverride;
    for endpoint in [
        "chatgpt_base_url",
        "openai_base_url",
        "api_base",
        "base_url",
    ] {
        if let Some(value) = config.get(endpoint) {
            match value {
                Value::Null => {}
                Value::String(value) if value.is_empty() => {}
                Value::String(_) => return unqualified(),
                _ => return malformed(),
            }
        }
    }
    for (key, expected, category) in [
        ("model_provider", "openai", ConfigPredicate::ModelProvider),
        (
            "forced_login_method",
            "chatgpt",
            ConfigPredicate::LoginMethod,
        ),
        ("web_search", "disabled", ConfigPredicate::WebSearch),
        ("sandbox_mode", "read-only", ConfigPredicate::SandboxMode),
        ("approval_policy", "never", ConfigPredicate::ApprovalPolicy),
    ] {
        *predicate = category;
        if config.get(key).and_then(Value::as_str) != Some(expected) {
            return unqualified();
        }
    }
    *predicate = ConfigPredicate::Features;
    fixed_feature_map(config.get("features"), exact)?;
    *predicate = ConfigPredicate::Apps;
    fixed_apps(config.get("apps"), exact)?;
    *predicate = ConfigPredicate::McpServers;
    false_map(config.get("mcp_servers"), MCP_IDS, exact)?;
    *predicate = ConfigPredicate::Plugins;
    false_map(config.get("plugins"), PLUGIN_IDS, exact)?;
    Ok(())
}

fn selected_session_origin(origins: &Map<String, Value>, key: &str) -> Result<()> {
    let origin = origins
        .get(key)
        .and_then(Value::as_object)
        .ok_or("profile_unqualified")?;
    bounded_string(origin.get("version"), 128)?;
    let name = origin
        .get("name")
        .and_then(Value::as_object)
        .ok_or("protocol_error")?;
    if name.get("type").and_then(Value::as_str) != Some("sessionFlags") {
        return unqualified();
    }
    Ok(())
}

fn validate_config_source(
    source: &Map<String, Value>,
    expected_cwd: &str,
    covered: &HashSet<String>,
) -> Result<bool> {
    match bounded_string(source.get("type"), 64)? {
        "sessionFlags" => Ok(false),
        "packagedDefaults" | "system" | "legacyManagedConfigTomlFromFile" => {
            let path = PathBuf::from(bounded_string(source.get("file"), 32_768)?);
            path_covered(&path, covered)?;
            Ok(true)
        }
        "user" => {
            if !matches!(source.get("profile"), None | Some(Value::Null)) {
                return unqualified();
            }
            let path = PathBuf::from(bounded_string(source.get("file"), 32_768)?);
            path_covered(&path, covered)?;
            Ok(true)
        }
        "project" => {
            let folder = PathBuf::from(bounded_string(source.get("dotCodexFolder"), 32_768)?);
            let project_root = folder.parent().ok_or("profile_unqualified")?;
            let project_root = normalized_path(project_root)?;
            if expected_cwd != project_root && !expected_cwd.starts_with(&(project_root + "\\")) {
                return unqualified();
            }
            path_covered(&folder.join("config.toml"), covered)?;
            Ok(true)
        }
        "mdm" | "enterpriseManaged" | "legacyManagedConfigTomlFromMdm" => unqualified(),
        _ => unqualified(),
    }
}

/// Validate effective configuration and return a projection safe for the journal.
pub fn validate_config(
    value: &Value,
    expected_cwd: &Path,
    covered_sources: &[PathBuf],
) -> Result<Value> {
    validate_config_observed(value, expected_cwd, covered_sources).map_err(|failure| failure.reason)
}

/// Original error plus closed location of the first failing check. No payload retained.
#[derive(Debug)]
pub struct ConfigRejection {
    pub reason: String,
    pub section: ConfigSection,
    pub predicate: ConfigPredicate,
}

pub fn validate_config_observed(
    value: &Value,
    expected_cwd: &Path,
    covered_sources: &[PathBuf],
) -> std::result::Result<Value, ConfigRejection> {
    let mut section = ConfigSection::Effective;
    let mut predicate = ConfigPredicate::Shape;
    validate_config_inner(
        value,
        expected_cwd,
        covered_sources,
        &mut section,
        &mut predicate,
    )
    .map_err(|reason| ConfigRejection {
        reason,
        section,
        predicate,
    })
}

fn validate_config_inner(
    value: &Value,
    expected_cwd: &Path,
    covered_sources: &[PathBuf],
    section: &mut ConfigSection,
    predicate: &mut ConfigPredicate,
) -> Result<Value> {
    let root = object(value)?;
    fixed_config(
        root.get("config").ok_or("protocol_error")?,
        false,
        predicate,
    )?;
    *section = ConfigSection::Origins;
    *predicate = ConfigPredicate::Shape;
    let origins = root
        .get("origins")
        .and_then(Value::as_object)
        .ok_or("protocol_error")?;
    *predicate = ConfigPredicate::SelectedOrigin;
    for key in [
        "model_provider",
        "forced_login_method",
        "web_search",
        "sandbox_mode",
        "approval_policy",
    ] {
        selected_session_origin(origins, key)?;
    }
    *predicate = ConfigPredicate::SourcePaths;
    let expected_cwd = normalized_path(expected_cwd)?;
    let covered: HashSet<String> = covered_sources
        .iter()
        .map(|path| normalized_path(path))
        .collect::<Result<_>>()?;
    *predicate = ConfigPredicate::Shape;
    if origins.len() > MAX_INVENTORY_ITEMS {
        return malformed();
    }
    for origin in origins.values() {
        *predicate = ConfigPredicate::Shape;
        let origin = object(origin)?;
        bounded_string(origin.get("version"), 128)?;
        let source = origin
            .get("name")
            .and_then(Value::as_object)
            .ok_or("protocol_error")?;
        *predicate = ConfigPredicate::OriginSource;
        validate_config_source(source, &expected_cwd, &covered)?;
    }
    *section = ConfigSection::Layers;
    *predicate = ConfigPredicate::Shape;
    let layers = array(root.get("layers"))?;
    if layers.is_empty() || layers.len() > 64 {
        return malformed();
    }
    let mut session_flags = 0usize;
    let mut disk_layers = 0usize;
    for layer in layers {
        *predicate = ConfigPredicate::Shape;
        let layer = object(layer)?;
        bounded_string(layer.get("version"), 128)?;
        if !matches!(
            layer.get("disabledReason"),
            None | Some(Value::Null) | Some(Value::String(_))
        ) {
            return malformed();
        }
        let source = layer
            .get("name")
            .and_then(Value::as_object)
            .ok_or("protocol_error")?;
        let source_type = bounded_string(source.get("type"), 64)?;
        *predicate = ConfigPredicate::LayerSource;
        let disk_source = validate_config_source(source, &expected_cwd, &covered)?;
        match source_type {
            "sessionFlags" => {
                session_flags += 1;
                *predicate = ConfigPredicate::Shape;
                fixed_config(
                    layer.get("config").ok_or("protocol_error")?,
                    true,
                    predicate,
                )?;
            }
            _ if disk_source => {
                disk_layers += 1;
            }
            _ => return unqualified(),
        }
    }
    *predicate = ConfigPredicate::SessionFlagsCount;
    if session_flags != 1 {
        return unqualified();
    }
    Ok(json!({
        "approval_policy":"never",
        "apps_default_enabled":false,
        "config_layer_count":layers.len(),
        "covered_disk_layer_count":disk_layers,
        "forced_login_method":"chatgpt",
        "model_provider":"openai",
        "sandbox_mode":"read-only",
        "session_flags_layers":session_flags,
        "web_search":"disabled"
    }))
}

/// The selected trial contract permits only an explicit null requirements result.
pub fn validate_requirements(value: &Value) -> Result<Value> {
    let value = object(value)?;
    match value.get("requirements") {
        Some(Value::Null) => Ok(json!({"requirements_present":false})),
        Some(_) => unqualified(),
        None => malformed(),
    }
}

fn validate_cursor(
    page: &Map<String, Value>,
    last: bool,
    cursors: &mut HashSet<String>,
) -> Result<()> {
    match page.get("nextCursor") {
        None | Some(Value::Null) if last => Ok(()),
        Some(Value::String(cursor)) if !last && !cursor.is_empty() && cursor.len() <= 4096 => {
            if !cursors.insert(cursor.clone()) {
                return malformed();
            }
            Ok(())
        }
        _ => malformed(),
    }
}

/// Validate all bounded feature pages and retain counts only.
pub fn validate_feature_pages(pages: &[Value], required: &[&str]) -> Result<Value> {
    if pages.is_empty() || pages.len() > MAX_PAGES || required.is_empty() {
        return malformed();
    }
    let required: HashSet<&str> = required.iter().copied().collect();
    let pinned: HashSet<&str> = crate::launch_policy::REQUIRED_DISABLED_FEATURES
        .iter()
        .copied()
        .collect();
    if required.is_empty() || required != pinned {
        return malformed();
    }
    let mut seen = HashSet::new();
    let mut cursors = HashSet::new();
    let mut count = 0usize;
    for (page_number, page) in pages.iter().enumerate() {
        let page = object(page)?;
        let data = array(page.get("data"))?;
        if data.len() > MAX_PAGE_ITEMS {
            return malformed();
        }
        for item in data {
            let item = object(item)?;
            let name = bounded_string(item.get("name"), 256)?;
            required_bool(item.get("defaultEnabled"))?;
            if !matches!(
                bounded_string(item.get("stage"), 64)?,
                "beta" | "underDevelopment" | "stable" | "deprecated" | "removed"
            ) {
                return malformed();
            }
            let enabled = required_bool(item.get("enabled"))?;
            if !seen.insert(name.to_owned()) {
                return malformed();
            }
            if enabled && !ALLOWED_ENABLED_FEATURES.contains(&name) {
                return unqualified();
            }
            count += 1;
        }
        validate_cursor(page, page_number + 1 == pages.len(), &mut cursors)?;
    }
    if !required.iter().all(|name| seen.contains(*name)) {
        return unqualified();
    }
    Ok(json!({"disabled_required":required.len(),"feature_count":count,"pages":pages.len()}))
}

/// Validate hook discovery for exactly one cwd. Hook definitions never enter the projection.
pub fn validate_hooks(value: &Value, expected_cwd: &Path) -> Result<Value> {
    let root = object(value)?;
    let data = array(root.get("data"))?;
    if data.len() != 1 {
        return unqualified();
    }
    let entry = object(&data[0])?;
    let cwd = PathBuf::from(bounded_string(entry.get("cwd"), 32_768)?);
    if normalized_path(&cwd)? != normalized_path(expected_cwd)? {
        return unqualified();
    }
    let errors = array(entry.get("errors"))?;
    let warnings = array(entry.get("warnings"))?;
    if !errors.is_empty() || !warnings.is_empty() {
        return unqualified();
    }
    let hooks = array(entry.get("hooks"))?;
    if hooks.len() > MAX_INVENTORY_ITEMS {
        return malformed();
    }
    let mut keys = HashSet::new();
    for hook in hooks {
        let hook = object(hook)?;
        let key = bounded_string(hook.get("key"), 1024)?;
        if !keys.insert(key.to_owned()) || required_bool(hook.get("enabled"))? {
            return unqualified();
        }
        bounded_string(hook.get("currentHash"), 1024)?;
        hook.get("displayOrder")
            .and_then(Value::as_i64)
            .ok_or("protocol_error")?;
        required_bool(hook.get("isManaged"))?;
        bounded_string(hook.get("sourcePath"), 32_768)?;
        hook.get("timeoutSec")
            .and_then(Value::as_u64)
            .ok_or("protocol_error")?;
        if !matches!(
            bounded_string(hook.get("eventName"), 64)?,
            "preToolUse"
                | "permissionRequest"
                | "postToolUse"
                | "preCompact"
                | "postCompact"
                | "sessionStart"
                | "sessionEnd"
                | "userPromptSubmit"
                | "subagentStart"
                | "subagentStop"
                | "stop"
                | "interrupt"
        ) || !matches!(
            bounded_string(hook.get("source"), 64)?,
            "system"
                | "user"
                | "project"
                | "mdm"
                | "sessionFlags"
                | "plugin"
                | "cloudRequirements"
                | "cloudManagedConfig"
                | "legacyManagedConfigFile"
                | "legacyManagedConfigMdm"
                | "unknown"
        ) || !matches!(
            bounded_string(hook.get("trustStatus"), 64)?,
            "managed" | "untrusted" | "trusted" | "modified"
        ) {
            return malformed();
        }
        match bounded_string(hook.get("handlerType"), 64)? {
            "command" => {
                bounded_string(hook.get("command"), 32_768)?;
            }
            "mcpTool" => {
                bounded_string(hook.get("server"), 256)?;
                bounded_string(hook.get("tool"), 256)?;
            }
            "prompt" | "agent" => {}
            _ => return malformed(),
        }
    }
    Ok(json!({"configured_hook_count":hooks.len(),"cwd_count":1,"errors":0,"warnings":0}))
}

fn plugin_source(value: Option<&Value>) -> Result<()> {
    let source = value.and_then(Value::as_object).ok_or("protocol_error")?;
    match bounded_string(source.get("type"), 64)? {
        "local" => {
            bounded_string(source.get("path"), 32_768)?;
        }
        "git" => {
            bounded_string(source.get("url"), 32_768)?;
        }
        "npm" => {
            bounded_string(source.get("package"), 1024)?;
        }
        "remote" => {}
        _ => return malformed(),
    }
    Ok(())
}

/// Validate local-only plugin discovery and retain counts only.
pub fn validate_plugins(value: &Value) -> Result<Value> {
    let root = object(value)?;
    let marketplaces = array(root.get("marketplaces"))?;
    if marketplaces.len() > MAX_PAGE_ITEMS {
        return malformed();
    }
    if !array(root.get("marketplaceLoadErrors"))?.is_empty() {
        return unqualified();
    }
    if let Some(featured) = root.get("featuredPluginIds") {
        for id in array(Some(featured))? {
            bounded_string(Some(id), 1024)?;
        }
    }
    let mut ids = HashSet::new();
    let mut count = 0usize;
    let mut installed = 0usize;
    for marketplace in marketplaces {
        let marketplace = object(marketplace)?;
        bounded_string(marketplace.get("name"), 1024)?;
        if !matches!(
            marketplace.get("path"),
            None | Some(Value::Null) | Some(Value::String(_))
        ) {
            return malformed();
        }
        for plugin in array(marketplace.get("plugins"))? {
            if count >= MAX_INVENTORY_ITEMS {
                return malformed();
            }
            let plugin = object(plugin)?;
            let id = bounded_string(plugin.get("id"), 1024)?;
            if !ids.insert(id.to_owned()) || required_bool(plugin.get("enabled"))? {
                return unqualified();
            }
            bounded_string(plugin.get("name"), 1024)?;
            if !matches!(
                bounded_string(plugin.get("authPolicy"), 64)?,
                "ON_INSTALL" | "ON_USE"
            ) || !matches!(
                bounded_string(plugin.get("installPolicy"), 64)?,
                "NOT_AVAILABLE" | "AVAILABLE" | "INSTALLED_BY_DEFAULT"
            ) {
                return malformed();
            }
            plugin_source(plugin.get("source"))?;
            installed += usize::from(required_bool(plugin.get("installed"))?);
            count += 1;
        }
    }
    Ok(
        json!({"enabled_plugin_count":0,"installed_plugin_count":installed,"marketplace_count":marketplaces.len(),"plugin_count":count}),
    )
}

/// Validate committed app runtime state and retain counts only.
pub fn validate_apps(value: &Value) -> Result<Value> {
    let root = object(value)?;
    let apps = array(root.get("apps"))?;
    if apps.len() > MAX_INVENTORY_ITEMS {
        return malformed();
    }
    let mut ids = HashSet::new();
    for app in apps {
        let app = object(app)?;
        let id = bounded_string(app.get("id"), 1024)?;
        if !ids.insert(id.to_owned())
            || required_bool(app.get("enabled"))?
            || required_bool(app.get("callable"))?
        {
            return unqualified();
        }
        if !matches!(
            app.get("runtimeName"),
            None | Some(Value::Null) | Some(Value::String(_))
        ) {
            return malformed();
        }
    }
    Ok(json!({"app_count":apps.len(),"callable_app_count":0,"enabled_app_count":0}))
}

/// Validate all bounded MCP status pages and retain counts only.
pub fn validate_mcp_pages(pages: &[Value]) -> Result<Value> {
    if pages.is_empty() || pages.len() > MAX_PAGES {
        return malformed();
    }
    let mut names = HashSet::new();
    let mut cursors = HashSet::new();
    let mut count = 0usize;
    for (page_number, page) in pages.iter().enumerate() {
        let page = object(page)?;
        let data = array(page.get("data"))?;
        if data.len() > MAX_PAGE_ITEMS {
            return malformed();
        }
        for server in data {
            let server = object(server)?;
            let name = bounded_string(server.get("name"), 1024)?;
            if !names.insert(name.to_owned()) {
                return malformed();
            }
            if server.get("runtimeStatus").and_then(Value::as_str) != Some("disabled") {
                return unqualified();
            }
            if !matches!(
                bounded_string(server.get("authStatus"), 64)?,
                "unknown" | "unsupported" | "notLoggedIn" | "bearerToken" | "oAuth"
            ) {
                return malformed();
            }
            if !server
                .get("tools")
                .and_then(Value::as_object)
                .is_some_and(Map::is_empty)
                || !array(server.get("resources"))?.is_empty()
                || !array(server.get("resourceTemplates"))?.is_empty()
                || !matches!(server.get("toolsError"), None | Some(Value::Null))
            {
                return unqualified();
            }
            count += 1;
        }
        validate_cursor(page, page_number + 1 == pages.len(), &mut cursors)?;
    }
    Ok(json!({"disabled_server_count":count,"pages":pages.len(),"server_count":count}))
}
