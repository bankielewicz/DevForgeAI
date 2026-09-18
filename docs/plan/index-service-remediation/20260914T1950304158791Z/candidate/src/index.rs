//! Source observations from immutable UTF-8 bytes, with bounded parser work.
use crate::protocol::ProjectConfig;
use ignore::gitignore::{Gitignore, GitignoreBuilder};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs;
use std::io::Read;
use std::ops::ControlFlow;
use std::path::{Component, Path};
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::{Duration, Instant};
use tree_sitter::{Node, ParseOptions, Parser, Query, QueryCursor, StreamingIterator};

pub const QUERY_VERSION: &str = "1";
const TEXT_EXTENSIONS: &[&str] = &[
    "md", "mdx", "txt", "json", "jsonc", "yaml", "yml", "toml", "ini", "cfg", "xml", "csv", "sql",
    "sh", "ps1", "cs", "html", "css",
];
const STRUCTURAL_EXTENSIONS: &[&str] = &[
    "rs", "py", "pyi", "js", "jsx", "mjs", "cjs", "ts", "tsx", "mts", "cts",
];
const BUILD_DIRS: &[&str] = &[
    "node_modules",
    "target",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    "coverage",
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "state", content = "reason", rename_all = "snake_case")]
pub enum FileDisposition {
    Eligible,
    Excluded(String),
    Skipped(String),
    Error(String),
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileEntry {
    pub path: String,
    pub disposition: FileDisposition,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Snapshot {
    pub bytes: Vec<u8>,
    pub sha256: String,
}

pub fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

type ParseReply = (Snapshot, Result<Extraction, String>, String);
struct ParseTask {
    extension: String,
    snapshot: Snapshot,
    cancelled: std::sync::Arc<AtomicBool>,
    reply: std::sync::mpsc::SyncSender<ParseReply>,
}

/// Two persistent parser workers with rendezvous queues. The scan coordinator
/// admits one captured file at a time, so uncommitted source stays below 50 MiB.
/// Worker concurrency can increase later without changing the snapshot contract.
pub struct ParsePool {
    senders: Vec<std::sync::mpsc::SyncSender<ParseTask>>,
    workers: Vec<std::thread::JoinHandle<()>>,
    next: usize,
}
impl ParsePool {
    pub fn new() -> Result<Self, String> {
        let mut pool = Self {
            senders: Vec::new(),
            workers: Vec::new(),
            next: 0,
        };
        for number in 0..2 {
            let (send, receive) = std::sync::mpsc::sync_channel::<ParseTask>(0);
            let name = format!("index-parser-{number}");
            pool.workers.push(
                std::thread::Builder::new()
                    .name(name.clone())
                    .spawn(move || {
                        for task in receive {
                            let parsed =
                                extract(&task.extension, &task.snapshot.bytes, &task.cancelled);
                            let _ = task.reply.send((task.snapshot, parsed, name.clone()));
                        }
                    })
                    .map_err(|error| error.to_string())?,
            );
            pool.senders.push(send);
        }
        Ok(pool)
    }
    pub fn parse(
        &mut self,
        extension: &str,
        snapshot: Snapshot,
        cancelled: std::sync::Arc<AtomicBool>,
    ) -> Result<ParseReply, String> {
        if snapshot.bytes.len() > 50 * 1024 * 1024 {
            return Err("oversized".into());
        }
        let (reply, receive) = std::sync::mpsc::sync_channel(0);
        self.senders[self.next]
            .send(ParseTask {
                extension: extension.into(),
                snapshot,
                cancelled,
                reply,
            })
            .map_err(|_| "parser_worker_unavailable")?;
        self.next = (self.next + 1) % self.senders.len();
        receive
            .recv()
            .map_err(|_| "parser_worker_unavailable".into())
    }
}
impl Drop for ParsePool {
    fn drop(&mut self) {
        self.senders.clear();
        for worker in self.workers.drain(..) {
            let _ = worker.join();
        }
    }
}

fn is_directory_link(metadata: &fs::Metadata) -> bool {
    #[cfg(windows)]
    {
        use std::os::windows::fs::MetadataExt;
        metadata.file_attributes() & 0x400 != 0
    }
    #[cfg(not(windows))]
    {
        metadata.file_type().is_symlink()
    }
}

fn ignore_rules(directory: &Path) -> Result<Gitignore, String> {
    let mut builder = GitignoreBuilder::new(directory);
    for file in [
        directory.join(".gitignore"),
        directory.join(".git/info/exclude"),
    ] {
        if file.is_file()
            && let Some(error) = builder.add(file)
        {
            return Err(error.to_string());
        }
    }
    builder.build().map_err(|error| error.to_string())
}

pub fn enumerate(
    root: &Path,
    config: &ProjectConfig,
    data_roots: &[&Path],
) -> Result<Vec<FileEntry>, String> {
    enumerate_controlled(root, config, data_roots, &|| Ok(()))
}

struct ScanOutput<'a> {
    entries: Vec<FileEntry>,
    checkpoint: &'a dyn Fn() -> Result<(), String>,
}

pub fn enumerate_controlled(
    root: &Path,
    config: &ProjectConfig,
    data_roots: &[&Path],
    checkpoint: &dyn Fn() -> Result<(), String>,
) -> Result<Vec<FileEntry>, String> {
    let root = fs::canonicalize(root).map_err(|_| "root_unavailable")?;
    let mut builder = GitignoreBuilder::new(&root);
    for pattern in config.exclusions.as_deref().unwrap_or(&[]) {
        builder
            .add_line(None, pattern)
            .map_err(|error| error.to_string())?;
    }
    let explicit = builder.build().map_err(|error| error.to_string())?;
    let mut result = ScanOutput {
        entries: Vec::new(),
        checkpoint,
    };
    walk(
        &root,
        &root,
        config,
        data_roots,
        &explicit,
        &mut Vec::new(),
        &mut result,
    )?;
    result.entries.sort_by(|a, b| a.path.cmp(&b.path));
    Ok(result.entries)
}

fn walk(
    root: &Path,
    directory: &Path,
    config: &ProjectConfig,
    data_roots: &[&Path],
    explicit: &Gitignore,
    stack: &mut Vec<Gitignore>,
    result: &mut ScanOutput<'_>,
) -> Result<(), String> {
    (result.checkpoint)()?;
    stack.push(ignore_rules(directory)?);
    let entries = fs::read_dir(directory).map_err(|_| "root_or_directory_unavailable")?;
    for entry in entries {
        (result.checkpoint)()?;
        let entry = entry.map_err(|error| error.to_string())?;
        let path = entry.path();
        let relative = path
            .strip_prefix(root)
            .map_err(|_| "path_outside_project")?;
        let Some(relative_text) = relative.to_str() else {
            result.entries.push(FileEntry {
                path: relative.to_string_lossy().into(),
                disposition: FileDisposition::Skipped("non_utf8_path".into()),
            });
            continue;
        };
        let name = entry.file_name();
        let name = name.to_string_lossy();
        let metadata = match fs::symlink_metadata(&path) {
            Ok(value) => value,
            Err(_) => {
                result.entries.push(FileEntry {
                    path: relative_text.replace('\\', "/"),
                    disposition: FileDisposition::Error("metadata_unavailable".into()),
                });
                continue;
            }
        };
        let linked = is_directory_link(&metadata);
        let is_directory = metadata.is_dir() || (linked && path.is_dir());
        let extension = path.extension().and_then(|v| v.to_str()).unwrap_or("");
        let mandatory = [".git", ".hg", ".svn"].contains(&name.as_ref())
            || relative.starts_with(".agents/devforgeai")
            || data_roots
                .iter()
                .any(|data| path == **data || path.starts_with(data));
        let sensitive = name == ".env"
            || name.starts_with(".env.")
            || ["key", "p12", "pfx"].contains(&extension)
            || ["id_rsa", "id_ed25519", "credentials"].contains(&name.as_ref());
        let ignored = stack
            .iter()
            .rev()
            .find_map(|rule| {
                let matched = rule.matched(&path, is_directory);
                if matched.is_none() {
                    None
                } else {
                    Some(matched.is_ignore())
                }
            })
            .unwrap_or(false);
        let disposition = if mandatory {
            FileDisposition::Excluded("mandatory".into())
        } else if is_directory && linked {
            FileDisposition::Skipped("directory_link".into())
        } else if sensitive {
            FileDisposition::Excluded("sensitive_default".into())
        } else if config.default_exclusions.unwrap_or(true)
            && is_directory
            && BUILD_DIRS.contains(&name.as_ref())
        {
            FileDisposition::Excluded("build_default".into())
        } else if explicit.matched(&path, is_directory).is_ignore() {
            FileDisposition::Excluded("project_rule".into())
        } else if ignored {
            FileDisposition::Excluded("git_rule".into())
        } else if is_directory {
            walk(root, &path, config, data_roots, explicit, stack, result)?;
            continue;
        } else if linked
            && fs::canonicalize(&path).map_or(true, |resolved| !resolved.starts_with(root))
        {
            FileDisposition::Skipped("linked_file_outside_root".into())
        } else if !metadata.is_file() && !linked {
            FileDisposition::Skipped("non_regular_file".into())
        } else if STRUCTURAL_EXTENSIONS.contains(&extension)
            || TEXT_EXTENSIONS.contains(&extension)
            || config.text_extensions.as_ref().is_some_and(|list| {
                list.iter()
                    .any(|value| value.trim_start_matches('.') == extension)
            })
            || config
                .text_names
                .as_ref()
                .is_some_and(|list| list.iter().any(|value| value == name.as_ref()))
        {
            FileDisposition::Eligible
        } else {
            FileDisposition::Skipped("unsupported_extension".into())
        };
        result.entries.push(FileEntry {
            path: relative_text.replace('\\', "/"),
            disposition,
        });
    }
    stack.pop();
    Ok(())
}

pub fn capture(
    root: &Path,
    relative: &str,
    limit: u64,
    cancelled: &AtomicBool,
) -> Result<Snapshot, String> {
    if Path::new(relative)
        .components()
        .any(|part| !matches!(part, Component::Normal(_)))
    {
        return Err("path_outside_project".into());
    }
    let root = fs::canonicalize(root).map_err(|_| "root_unavailable")?;
    let path = root.join(relative);
    for _ in 0..3 {
        if cancelled.load(Ordering::Relaxed) {
            return Err("cancelled".into());
        }
        let target = fs::canonicalize(&path).map_err(|_| "file_unavailable")?;
        if !target.starts_with(&root) {
            return Err("path_outside_project".into());
        }
        let opened = crate::source_file::open(&root, relative)?;
        let before = opened.file.metadata().map_err(|_| "metadata_unavailable")?;
        if !before.is_file() {
            return Err("non_regular_file".into());
        }
        if before.len() > limit {
            return Err("oversized".into());
        }
        let mut bytes = Vec::new();
        (&opened.file)
            .take(limit.saturating_add(1))
            .read_to_end(&mut bytes)
            .map_err(|_| "read_error")?;
        if bytes.len() as u64 > limit {
            return Err("oversized".into());
        }
        let after = opened.file.metadata().map_err(|_| "file_unavailable")?;
        if before.len() != after.len()
            || before.modified().ok() != after.modified().ok()
            || fs::canonicalize(&path).ok().as_ref() != Some(&target)
        {
            continue;
        }
        if bytes.starts_with(&[0xff, 0xfe]) || bytes.starts_with(&[0xfe, 0xff]) {
            return Err("unsupported_encoding".into());
        }
        if bytes.contains(&0) {
            return Err("binary".into());
        }
        if std::str::from_utf8(&bytes).is_err() {
            return Err("unsupported_encoding".into());
        }
        return Ok(Snapshot {
            sha256: digest(&bytes),
            bytes,
        });
    }
    Err("unstable".into())
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct SourceRange {
    pub start: usize,
    pub end: usize,
}
impl SourceRange {
    fn from(node: Node<'_>) -> Self {
        Self {
            start: node.start_byte(),
            end: node.end_byte(),
        }
    }
    fn contains(&self, other: &Self) -> bool {
        self.start <= other.start && self.end >= other.end
    }
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Declaration {
    pub id: usize,
    pub name: Option<String>,
    pub kind: String,
    pub parent: Option<usize>,
    pub range: SourceRange,
    pub signature: SourceRange,
    pub documentation: Vec<SourceRange>,
    pub comments: Vec<SourceRange>,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Call {
    pub name: String,
    pub range: SourceRange,
    pub parent: Option<usize>,
    pub resolution: String,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Extraction {
    pub language: String,
    pub adapter_version: String,
    pub query_version: String,
    pub partial: bool,
    pub declarations: Vec<Declaration>,
    pub comments: Vec<SourceRange>,
    pub imports: Vec<SourceRange>,
    pub calls: Vec<Call>,
}

pub fn extract(
    extension: &str,
    bytes: &[u8],
    cancelled: &AtomicBool,
) -> Result<Extraction, String> {
    if cancelled.load(Ordering::Relaxed) {
        return Err("cancelled".into());
    }
    let adapter = match extension {
        "rs" => Some((
            "rust",
            "0.24.2",
            tree_sitter_rust::LANGUAGE.into(),
            include_str!("../queries/rust.scm"),
        )),
        "py" | "pyi" => Some((
            "python",
            "0.25.0",
            tree_sitter_python::LANGUAGE.into(),
            include_str!("../queries/python.scm"),
        )),
        "js" | "jsx" | "mjs" | "cjs" => Some((
            "javascript",
            "0.25.0",
            tree_sitter_javascript::LANGUAGE.into(),
            include_str!("../queries/javascript.scm"),
        )),
        "ts" | "mts" | "cts" => Some((
            "typescript",
            "0.23.2",
            tree_sitter_typescript::LANGUAGE_TYPESCRIPT.into(),
            include_str!("../queries/typescript.scm"),
        )),
        "tsx" => Some((
            "typescript",
            "0.23.2",
            tree_sitter_typescript::LANGUAGE_TSX.into(),
            include_str!("../queries/typescript.scm"),
        )),
        _ => None,
    };
    let mut result = Extraction {
        language: "text".into(),
        adapter_version: "1".into(),
        query_version: QUERY_VERSION.into(),
        partial: false,
        declarations: vec![],
        comments: vec![],
        imports: vec![],
        calls: vec![],
    };
    let Some((language_name, version, language, query_source)) = adapter else {
        return Ok(result);
    };
    result.language = language_name.into();
    result.adapter_version = version.into();
    let mut parser = Parser::new();
    parser
        .set_language(&language)
        .map_err(|error| error.to_string())?;
    let started = Instant::now();
    let mut progress = |_: &tree_sitter::ParseState| {
        if cancelled.load(Ordering::Relaxed) || started.elapsed() >= Duration::from_secs(2) {
            ControlFlow::Break(())
        } else {
            ControlFlow::Continue(())
        }
    };
    let tree = parser
        .parse_with_options(
            &mut |offset, _| &bytes[offset..],
            None,
            Some(ParseOptions::new().progress_callback(&mut progress)),
        )
        .ok_or_else(|| {
            if cancelled.load(Ordering::Relaxed) {
                "cancelled"
            } else {
                "parse_timeout"
            }
            .to_owned()
        })?;
    result.partial = tree.root_node().has_error();
    let query = Query::new(&language, query_source).map_err(|error| error.to_string())?;
    let mut cursor = QueryCursor::new();
    let mut matches = cursor.matches(&query, tree.root_node(), bytes);
    while let Some(matched) = matches.next() {
        if cancelled.load(Ordering::Relaxed) {
            return Err("cancelled".into());
        }
        if started.elapsed() >= Duration::from_secs(2) {
            return Err("parse_timeout".into());
        }
        for capture in matched.captures {
            let node = capture.node;
            let tag = query.capture_names()[capture.index as usize];
            let range = SourceRange::from(node);
            if let Some(kind) = tag.strip_prefix("declaration.") {
                let name = node
                    .child_by_field_name("name")
                    .map(|name| String::from_utf8_lossy(&bytes[name.byte_range()]).into_owned());
                let body = node.child_by_field_name("body");
                let mut documentation = Vec::new();
                if language_name == "python" {
                    if let Some(first) = body.and_then(|body| body.named_child(0))
                        && first.kind() == "expression_statement"
                        && first.named_child(0).is_some_and(|n| {
                            n.kind() == "string" || n.kind() == "concatenated_string"
                        })
                    {
                        documentation.push(SourceRange::from(first));
                    }
                } else {
                    let mut previous = node.prev_named_sibling();
                    let mut declaration_start = range.start;
                    while let Some(comment) = previous {
                        let text = &bytes[comment.byte_range()];
                        let between = &bytes[comment.end_byte()..declaration_start];
                        if (text.starts_with(b"///") && !text.starts_with(b"////")
                            || text.starts_with(b"/**") && !text.starts_with(b"/***"))
                            && between.iter().all(u8::is_ascii_whitespace)
                            && between.iter().filter(|b| **b == b'\n').count() <= 1
                        {
                            documentation.push(SourceRange::from(comment));
                            declaration_start = comment.start_byte();
                            previous = comment.prev_named_sibling();
                        } else {
                            break;
                        }
                    }
                    documentation.reverse();
                }
                result.declarations.push(Declaration {
                    id: result.declarations.len(),
                    name,
                    kind: kind.into(),
                    parent: None,
                    range,
                    signature: SourceRange {
                        start: range.start,
                        end: body.map_or(range.end, |n| n.start_byte()),
                    },
                    documentation,
                    comments: vec![],
                });
            } else if tag == "comment" {
                result.comments.push(range);
            } else if tag == "import" {
                result.imports.push(range);
            } else if tag == "call"
                && let Some(function) = node.child_by_field_name("function")
                && ![
                    "subscript",
                    "subscript_expression",
                    "call",
                    "call_expression",
                ]
                .contains(&function.kind())
            {
                result.calls.push(Call {
                    name: String::from_utf8_lossy(&bytes[function.byte_range()]).into_owned(),
                    range,
                    parent: None,
                    resolution: "syntactic_candidate".into(),
                });
            }
        }
    }
    let ranges: Vec<_> = result
        .declarations
        .iter()
        .map(|declaration| (declaration.id, declaration.range))
        .collect();
    for declaration in &mut result.declarations {
        declaration.parent = ranges
            .iter()
            .filter(|(id, range)| *id != declaration.id && range.contains(&declaration.range))
            .min_by_key(|(_, range)| range.end - range.start)
            .map(|(id, _)| *id);
        declaration.comments = result
            .comments
            .iter()
            .filter(|range| declaration.range.contains(range))
            .copied()
            .collect();
    }
    let types: Vec<_> = result.declarations.iter().map(|d| d.kind.clone()).collect();
    for declaration in &mut result.declarations {
        if declaration.kind == "function"
            && declaration.parent.is_some_and(|id| types[id] == "class")
        {
            declaration.kind = "method".into();
        }
    }
    for call in &mut result.calls {
        call.parent = ranges
            .iter()
            .filter(|(_, range)| range.contains(&call.range))
            .min_by_key(|(_, range)| range.end - range.start)
            .map(|(id, _)| *id);
    }
    Ok(result)
}
