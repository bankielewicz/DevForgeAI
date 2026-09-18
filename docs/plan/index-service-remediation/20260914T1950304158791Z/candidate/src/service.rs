//! Management state and one scan coordinator, independent of transport/UI.
use crate::{
    index, platform,
    protocol::{ErrorCode, Operation, ProjectConfig, ProtocolError, Request, Response, Result},
    storage::{Store, StoredFile},
};
use notify::{RecommendedWatcher, RecursiveMode, Watcher};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::{
    collections::BTreeMap,
    fs,
    path::{Path, PathBuf},
    sync::{
        Arc, Mutex,
        atomic::{AtomicBool, Ordering},
    },
    thread::{self, JoinHandle},
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};

pub fn now() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs() as i64
}
fn internal(message: impl Into<String>) -> ProtocolError {
    ProtocolError::new(ErrorCode::InternalError, message)
}
fn id() -> String {
    uuid::Uuid::new_v4().to_string()
}

#[derive(Clone, Serialize, Deserialize)]
pub struct Project {
    pub id: String,
    pub name: String,
    pub root: PathBuf,
    pub config: ProjectConfig,
    pub created_at: i64,
    pub updated_at: i64,
    pub dirty: bool,
    pub revision: u64,
    pub last_reconciliation: Option<i64>,
    #[serde(default)]
    pub last_change_ms: Option<u128>,
    #[serde(default)]
    pub diagnostic_code: Option<String>,
    #[serde(default)]
    pub retry_after: Option<i64>,
}
#[derive(Clone, Serialize, Deserialize)]
pub struct Job {
    pub id: String,
    pub project_id: String,
    pub kind: String,
    pub outcome: String,
    pub created_at: i64,
    pub updated_at: i64,
    pub error: Option<String>,
    pub generation_id: Option<String>,
}
#[derive(Clone, Serialize, Deserialize)]
struct Receipt {
    payload: String,
    response: Response,
    created_at: i64,
}
#[derive(Clone, Default, Serialize, Deserialize)]
struct Registry {
    paused: bool,
    projects: BTreeMap<String, Project>,
    jobs: BTreeMap<String, Job>,
    receipts: BTreeMap<String, Receipt>,
}

struct Inner {
    data: PathBuf,
    environment: String,
    registry: Mutex<Registry>,
    store: Mutex<Option<Store>>,
    storage_error: Mutex<Option<ProtocolError>>,
    stopping: AtomicBool,
    cancellations: Mutex<BTreeMap<String, Arc<AtomicBool>>>,
}
pub struct Service {
    inner: Arc<Inner>,
    worker: Mutex<Option<JoinHandle<()>>>,
}

impl Inner {
    fn save(&self, state: &Registry) -> Result<()> {
        platform::atomic_write(
            &self.data.join("registrations.json"),
            &serde_json::to_vec(state).map_err(|e| internal(e.to_string()))?,
        )
    }
    fn with_store<T>(&self, action: impl FnOnce(&mut Store) -> Result<T>) -> Result<T> {
        let mut store = self
            .store
            .lock()
            .map_err(|_| internal("Storage mutex poisoned"))?;
        action(store.as_mut().ok_or_else(|| {
            self.storage_error
                .lock()
                .unwrap()
                .clone()
                .unwrap_or_else(|| {
                    ProtocolError::new(ErrorCode::StorageCorrupt, "Storage unavailable")
                })
        })?)
    }
    fn log(&self, request: &Request, response: &Response, duration: Duration) {
        use std::io::Write;
        let path = self.data.join("index.log");
        if path
            .metadata()
            .is_ok_and(|metadata| metadata.len() >= 10 * 1024 * 1024)
        {
            for i in (1..5).rev() {
                let _ = fs::rename(
                    self.data.join(format!("index.log.{i}")),
                    self.data.join(format!("index.log.{}", i + 1)),
                );
            }
            let _ = fs::rename(&path, self.data.join("index.log.1"));
        }
        if let Ok(mut file) = fs::OpenOptions::new().create(true).append(true).open(path) {
            let _ = writeln!(
                file,
                "{}",
                json!({"request_id":request.request_id,"operation":request.operation,"duration_ms":duration.as_millis(),"code":response.error.as_ref().map(|error|error.code),"at":now()})
            );
        }
    }
}

impl Service {
    /// The native host supplies the exclusive environment lock and private directory.
    pub fn open(data: &Path) -> Result<Self> {
        let path = data.join("registrations.json");
        let mut registry: Registry = if path.exists() {
            serde_json::from_slice(&fs::read(path).map_err(platform::io_error)?)
                .map_err(|error| ProtocolError::new(ErrorCode::StorageCorrupt, error.to_string()))?
        } else {
            Registry::default()
        };
        for job in registry.jobs.values_mut() {
            if ["running", "queued"].contains(&job.outcome.as_str()) {
                job.outcome = "interrupted".into();
                job.updated_at = now();
            }
        }
        for project in registry.projects.values_mut() {
            project.dirty = true;
            project.revision += 1;
        }
        let identity_path = data.join("environment-id");
        let environment = if identity_path.exists() {
            fs::read_to_string(identity_path).map_err(platform::io_error)?
        } else {
            let value = id();
            platform::atomic_write(&identity_path, value.as_bytes())?;
            value
        };
        let (store, error) = match Store::open(data) {
            Ok(mut store) => {
                store.discard_interrupted()?;
                (Some(store), None)
            }
            Err(error) => (None, Some(error)),
        };
        let inner = Arc::new(Inner {
            data: data.to_owned(),
            environment,
            registry: Mutex::new(registry),
            store: Mutex::new(store),
            storage_error: Mutex::new(error),
            stopping: AtomicBool::new(false),
            cancellations: Mutex::new(BTreeMap::new()),
        });
        inner.save(&inner.registry.lock().unwrap())?;
        let running = inner.clone();
        let worker = thread::Builder::new()
            .name("index-coordinator".into())
            .spawn(move || coordinator(running))
            .map_err(platform::io_error)?;
        Ok(Self {
            inner,
            worker: Mutex::new(Some(worker)),
        })
    }
    pub fn environment_id(&self) -> &str {
        &self.inner.environment
    }
    pub fn is_stopping(&self) -> bool {
        self.inner.stopping.load(Ordering::Acquire)
    }
    pub fn execute(&self, request: &Request) -> Response {
        let started = Instant::now();
        let result = Request::decode(&serde_json::to_vec(request).unwrap_or_default())
            .and_then(|request| request.typed_operation())
            .and_then(|operation| self.apply(request, operation, started));
        let response = match result {
            Ok(response) => response,
            Err(error) => Response::from_error(&request.request_id, error)
                .with_environment(&self.inner.environment),
        };
        self.inner.log(request, &response, started.elapsed());
        response
    }
    fn apply(&self, request: &Request, operation: Operation, started: Instant) -> Result<Response> {
        let mut state = self
            .inner
            .registry
            .lock()
            .map_err(|_| internal("Registry mutex poisoned"))?;
        let payload = serde_json::to_string(&json!({"operation":request.operation,"timeout_ms":request.timeout_ms,"params":request.params})).map_err(|e|internal(e.to_string()))?;
        state.receipts.retain(|_, r| now() - r.created_at < 86400);
        state.jobs.retain(|_, j| {
            ["queued", "running"].contains(&j.outcome.as_str()) || now() - j.updated_at < 7 * 86400
        });
        if let Some(receipt) = state.receipts.get(&request.request_id) {
            if receipt.payload != payload {
                return Err(ProtocolError::new(
                    ErrorCode::RequestIdConflict,
                    "Request ID has a different payload",
                ));
            }
            return Ok(receipt.response.clone());
        }
        if started.elapsed() >= Duration::from_millis(request.timeout_ms) {
            return Err(ProtocolError::new(
                ErrorCode::Timeout,
                "Request budget exhausted before mutation",
            ));
        }
        let mut changed = state.clone();
        let result = self.dispatch(&mut changed, &operation);
        let response = match result {
            Ok(value) => Response::success(&request.request_id, value),
            Err(error) => Response::from_error(&request.request_id, error),
        }
        .with_environment(&self.inner.environment);
        if operation.is_mutation() {
            changed.receipts.insert(
                request.request_id.clone(),
                Receipt {
                    payload,
                    response: response.clone(),
                    created_at: now(),
                },
            );
            self.inner.save(&changed)?;
            *state = changed;
        }
        Ok(response)
    }
    fn dispatch(&self, state: &mut Registry, operation: &Operation) -> Result<Value> {
        match operation {
            Operation::Handshake {} | Operation::Status {} => Ok(
                json!({"daemon_state":if self.is_stopping(){"stopping"}else{"running"},"indexing_mode":if state.paused{"paused"}else{"active"},"degraded":self.inner.store.lock().unwrap().is_none(),"projects":state.projects.len(),"parse_workers":2}),
            ),
            Operation::Diagnostics {} => Ok(
                json!({"storage_error":*self.inner.storage_error.lock().unwrap(),"log_path":self.inner.data.join("index.log"),"source_contents_logged":false}),
            ),
            Operation::Pause {} => {
                state.paused = true;
                Ok(json!({"indexing_mode":"paused"}))
            }
            Operation::Resume {} => {
                if state.paused {
                    state.paused = false;
                    for project in state.projects.values_mut() {
                        if project.dirty
                            || project.last_reconciliation.is_none()
                            || !project.root.is_dir()
                        {
                            project.dirty = true;
                            project.revision += 1;
                            project.retry_after = None;
                        }
                    }
                }
                Ok(json!({"indexing_mode":"active"}))
            }
            Operation::Stop {} => {
                self.inner.stopping.store(true, Ordering::Release);
                for cancel in self.inner.cancellations.lock().unwrap().values() {
                    cancel.store(true, Ordering::Release);
                }
                for job in state.jobs.values_mut() {
                    if job.outcome == "queued" {
                        job.outcome = "cancelled".into();
                        job.updated_at = now();
                    }
                }
                Ok(json!({"daemon_state":"stopping"}))
            }
            Operation::ProjectList {} => {
                Ok(json!({"projects":state.projects.values().collect::<Vec<_>>()}))
            }
            Operation::ProjectAdd { root, name } => {
                let root = platform::canonical_root(
                    Path::new(root),
                    std::env::var_os("WSL_DISTRO_NAME").is_some(),
                )?;
                platform::reject_overlap(
                    &root,
                    &state
                        .projects
                        .values()
                        .map(|p| p.root.clone())
                        .chain(Some(self.inner.data.clone()))
                        .collect::<Vec<_>>(),
                )?;
                let project = id();
                state.projects.insert(
                    project.clone(),
                    Project {
                        id: project.clone(),
                        name: name.clone(),
                        root,
                        config: ProjectConfig::default(),
                        created_at: now(),
                        updated_at: now(),
                        dirty: true,
                        revision: 1,
                        last_reconciliation: None,
                        last_change_ms: None,
                        diagnostic_code: None,
                        retry_after: None,
                    },
                );
                let job = if state.paused {
                    None
                } else {
                    Some(queue(state, &project, "rescan", false)?)
                };
                Ok(json!({"project_id":project,"job_id":job}))
            }
            Operation::ProjectUpdate { project_id, config } => {
                let project = state.projects.get_mut(project_id).ok_or_else(|| {
                    ProtocolError::new(ErrorCode::ProjectNotFound, "Unknown project")
                })?;
                // Validate globs without enumerating the project.
                let mut rules = ignore::gitignore::GitignoreBuilder::new(&project.root);
                for line in config.exclusions.as_deref().unwrap_or(&[]) {
                    rules.add_line(None, line).map_err(|e| {
                        ProtocolError::new(ErrorCode::InvalidArgument, e.to_string())
                    })?;
                }
                macro_rules! update {
                    ($field:ident) => {
                        if config.$field.is_some() {
                            project.config.$field = config.$field.clone();
                        }
                    };
                }
                update!(exclusions);
                update!(text_extensions);
                update!(text_names);
                update!(default_exclusions);
                update!(max_file_bytes);
                project.updated_at = now();
                project.dirty = true;
                project.revision += 1;
                project.retry_after = None;
                Ok(json!({"project_id":project_id,"dirty":true}))
            }
            Operation::ProjectRemove { project_id } => {
                if !state.projects.contains_key(project_id) {
                    return Err(ProtocolError::new(
                        ErrorCode::ProjectNotFound,
                        "Unknown project",
                    ));
                }
                for job in state.jobs.values_mut().filter(|j| {
                    j.project_id == *project_id
                        && ["queued", "running"].contains(&j.outcome.as_str())
                }) {
                    if let Some(cancel) = self.inner.cancellations.lock().unwrap().get(&job.id) {
                        cancel.store(true, Ordering::Release);
                    }
                    job.outcome = "cancelled".into();
                    job.updated_at = now();
                }
                self.inner
                    .with_store(|store| store.remove_project(project_id))?;
                state.projects.remove(project_id);
                Ok(
                    json!({"project_id":project_id,"application_cache_deleted":true,"source_deleted":false}),
                )
            }
            Operation::IndexStatus { project_id } => {
                let project = state.projects.get(project_id).ok_or_else(|| {
                    ProtocolError::new(ErrorCode::ProjectNotFound, "Unknown project")
                })?;
                let mut summary=self.inner.with_store(|store|store.summary(project_id)).ok().flatten().unwrap_or_else(||json!({"coverage":"unknown","eligible_count":0,"text_count":0,"structural_count":0,"excluded_count":0,"skipped_count":0,"failed_count":0}));
                summary["project_id"] = json!(project_id);
                summary["diagnostic_code"] = json!(project.diagnostic_code);
                summary["activity"] = json!(if project.diagnostic_code.is_some() {
                    "failed"
                } else if state
                    .jobs
                    .values()
                    .any(|job| job.project_id == *project_id && job.outcome == "running")
                {
                    "indexing"
                } else if state
                    .jobs
                    .values()
                    .any(|job| job.project_id == *project_id && job.outcome == "queued")
                {
                    "queued"
                } else {
                    "idle"
                });
                summary["dirty"] = json!(project.dirty);
                summary["freshness"] = json!(if project.dirty {
                    "dirty"
                } else if project.last_reconciliation.is_some() {
                    "observed_current"
                } else {
                    "unknown"
                });
                summary["observed_at"] = json!(now());
                summary["last_reconciliation"] = json!(project.last_reconciliation);
                summary["current_generation"] = json!(
                    self.inner
                        .with_store(|store| store.current(project_id))
                        .ok()
                        .flatten()
                );
                summary["jobs"] = json!(
                    state
                        .jobs
                        .values()
                        .filter(|j| j.project_id == *project_id
                            && ["queued", "running"].contains(&j.outcome.as_str()))
                        .collect::<Vec<_>>()
                );
                Ok(summary)
            }
            Operation::Rescan { project_id }
            | Operation::Reindex { project_id }
            | Operation::Reconcile { project_id } => {
                self.inner.with_store(|_| Ok(()))?;
                let kind = if matches!(operation, Operation::Reindex { .. }) {
                    "reindex"
                } else {
                    "rescan"
                };
                let job = queue(
                    state,
                    project_id,
                    kind,
                    matches!(operation, Operation::Reconcile { .. }),
                )?;
                Ok(json!({"job_id":job,"waiting_for_resume":state.paused}))
            }
            Operation::JobStatus { job_id } => {
                Ok(json!(state.jobs.get(job_id).ok_or_else(|| {
                    ProtocolError::new(ErrorCode::JobNotFound, "Unknown or expired job")
                })?))
            }
            Operation::JobCancel { job_id } => {
                let job = state.jobs.get_mut(job_id).ok_or_else(|| {
                    ProtocolError::new(ErrorCode::JobNotFound, "Unknown or expired job")
                })?;
                if job.outcome == "queued" {
                    job.outcome = "cancelled".into();
                    job.updated_at = now();
                }
                if let Some(cancel) = self.inner.cancellations.lock().unwrap().get(job_id) {
                    cancel.store(true, Ordering::Release);
                }
                Ok(json!(job))
            }
            Operation::Rebuild {
                project_id,
                affected_projects,
            } => {
                if !state.projects.contains_key(project_id) {
                    return Err(ProtocolError::new(
                        ErrorCode::ProjectNotFound,
                        "Unknown project",
                    ));
                }
                let expected: Vec<_> = state.projects.keys().cloned().collect();
                let mut supplied = affected_projects.clone();
                supplied.sort();
                if supplied != expected {
                    return Err(ProtocolError::new(
                        ErrorCode::InvalidArgument,
                        "Affected-project confirmation does not match",
                    )
                    .details(json!({"affected_projects":expected})));
                }
                if self.inner.store.lock().unwrap().is_some() {
                    return Err(ProtocolError::new(
                        ErrorCode::InvalidArgument,
                        "Rebuild is only for degraded storage; use reindex",
                    ));
                }
                let quarantine = self.inner.data.join(format!("quarantine-{}", id()));
                fs::create_dir(&quarantine).map_err(platform::io_error)?;
                for name in ["index.sqlite3", "index.sqlite3-wal", "index.sqlite3-shm"] {
                    let source = self.inner.data.join(name);
                    if source.exists() {
                        fs::rename(&source, quarantine.join(name)).map_err(platform::io_error)?;
                    }
                }
                *self.inner.store.lock().unwrap() = Some(Store::open(&self.inner.data)?);
                *self.inner.storage_error.lock().unwrap() = None;
                for project in state.projects.values_mut() {
                    project.dirty = true;
                    project.revision += 1;
                    project.last_reconciliation = None;
                }
                Ok(json!({"affected_projects":expected,"quarantine":quarantine}))
            }
        }
    }
    pub fn shutdown(&self) -> Result<()> {
        self.inner.stopping.store(true, Ordering::Release);
        for cancel in self.inner.cancellations.lock().unwrap().values() {
            cancel.store(true, Ordering::Release);
        }
        if let Some(worker) = self.worker.lock().unwrap().take() {
            worker
                .join()
                .map_err(|_| internal("Coordinator panicked"))?;
        }
        let mut state = self.inner.registry.lock().unwrap();
        for job in state.jobs.values_mut() {
            if ["queued", "running"].contains(&job.outcome.as_str()) {
                job.outcome = "cancelled".into();
                job.updated_at = now();
            }
        }
        self.inner.save(&state)
    }
}
impl Drop for Service {
    fn drop(&mut self) {
        let _ = self.shutdown();
    }
}

fn queue(state: &mut Registry, project: &str, kind: &str, join: bool) -> Result<String> {
    if !state.projects.contains_key(project) {
        return Err(ProtocolError::new(
            ErrorCode::ProjectNotFound,
            "Unknown project",
        ));
    }
    if let Some(job) = state
        .jobs
        .values()
        .find(|j| j.project_id == project && ["queued", "running"].contains(&j.outcome.as_str()))
    {
        if join && job.kind == kind {
            return Ok(job.id.clone());
        }
        return Err(ProtocolError::new(
            ErrorCode::JobConflict,
            "Project already has an indexing job",
        )
        .details(json!({"job_id":job.id})));
    }
    let job = id();
    state.jobs.insert(
        job.clone(),
        Job {
            id: job.clone(),
            project_id: project.into(),
            kind: kind.into(),
            outcome: "queued".into(),
            created_at: now(),
            updated_at: now(),
            error: None,
            generation_id: None,
        },
    );
    Ok(job)
}

fn coordinator(inner: Arc<Inner>) {
    let mut parsers = match index::ParsePool::new() {
        Ok(pool) => pool,
        Err(error) => {
            *inner.storage_error.lock().unwrap() = Some(internal(error));
            return;
        }
    };
    let mut watched = BTreeMap::<String, RecommendedWatcher>::new();
    while !inner.stopping.load(Ordering::Acquire) {
        let candidate = {
            let mut state = inner.registry.lock().unwrap();
            watched.retain(|project, _| state.projects.contains_key(project));
            for project in state.projects.values() {
                if !watched.contains_key(&project.id) {
                    let weak = Arc::downgrade(&inner);
                    let project_id = project.id.clone();
                    if let Ok(mut watcher) = notify::recommended_watcher(move |event| {
                        record_watch_event(&weak, &project_id, event)
                    }) && watcher
                        .watch(&project.root, RecursiveMode::Recursive)
                        .is_ok()
                    {
                        watched.insert(project.id.clone(), watcher);
                    }
                }
            }
            if state.paused || inner.store.lock().unwrap().is_none() {
                None
            } else {
                let dirty: Vec<_> = state
                    .projects
                    .values()
                    .filter(|project| {
                        (project.dirty
                            || project
                                .last_reconciliation
                                .is_none_or(|last| now() - last >= 300))
                            && project.retry_after.is_none_or(|deadline| now() >= deadline)
                            && project.last_change_ms.is_none_or(|last| {
                                SystemTime::now()
                                    .duration_since(UNIX_EPOCH)
                                    .unwrap_or_default()
                                    .as_millis()
                                    .saturating_sub(last)
                                    >= 500
                            })
                    })
                    .map(|p| p.id.clone())
                    .collect();
                for project in dirty {
                    let _ = queue(&mut state, &project, "rescan", true);
                }
                let queued = state
                    .jobs
                    .values_mut()
                    .find(|job| job.outcome == "queued")
                    .map(|job| {
                        job.outcome = "running".into();
                        job.updated_at = now();
                        job.clone()
                    });
                if queued.is_some() {
                    let _ = inner.save(&state);
                }
                queued
            }
        };
        if let Some(job) = candidate {
            let cancellation = Arc::new(AtomicBool::new(false));
            inner
                .cancellations
                .lock()
                .unwrap()
                .insert(job.id.clone(), cancellation.clone());
            let result = run_job(&inner, &job, &cancellation, &mut parsers);
            inner.cancellations.lock().unwrap().remove(&job.id);
            let mut state = inner.registry.lock().unwrap();
            if let Some(project) = state.projects.get_mut(&job.project_id) {
                if let Err(error) = &result {
                    if error.code != ErrorCode::JobCancelled {
                        project.diagnostic_code = Some(if error.code == ErrorCode::InvalidRoot {
                            "ROOT_UNAVAILABLE".into()
                        } else {
                            serde_json::to_value(error.code)
                                .unwrap_or_default()
                                .as_str()
                                .unwrap_or("INTERNAL_ERROR")
                                .into()
                        });
                        project.dirty = true;
                        project.retry_after = Some(now() + 30);
                    }
                } else {
                    project.diagnostic_code = None;
                    project.retry_after = None;
                }
            }
            if let Some(record) = state.jobs.get_mut(&job.id) {
                if record.outcome != "cancelled" {
                    match result {
                        Ok(generation) => {
                            record.outcome = "succeeded".into();
                            record.generation_id = Some(generation);
                        }
                        Err(error) => {
                            record.outcome = if cancellation.load(Ordering::Relaxed)
                                || inner.stopping.load(Ordering::Relaxed)
                            {
                                "cancelled"
                            } else {
                                "failed"
                            }
                            .into();
                            record.error = Some(error.to_string());
                        }
                    }
                }
                record.updated_at = now();
            }
            let _ = inner.save(&state);
        } else {
            thread::sleep(Duration::from_millis(50));
        }
    }
}

// Watcher failures invalidate reconciliation; access-only events must not create
// a scan loop. Keeping this callback separate permits deterministic event tests.
fn record_watch_event(
    weak: &std::sync::Weak<Inner>,
    project_id: &str,
    event: notify::Result<notify::Event>,
) {
    if event
        .as_ref()
        .is_ok_and(|event| matches!(event.kind, notify::EventKind::Access(_)))
    {
        return;
    }
    if let Some(inner) = weak.upgrade() {
        let mut state = inner.registry.lock().unwrap();
        if let Some(project) = state.projects.get_mut(project_id) {
            project.dirty = true;
            project.revision += 1;
            project.last_change_ms = Some(
                SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_millis(),
            );
            if event.is_err() {
                project.last_reconciliation = None;
            }
        }
    }
}

fn boundary(inner: &Inner, cancellation: &AtomicBool) -> Result<()> {
    loop {
        if cancellation.load(Ordering::Relaxed) || inner.stopping.load(Ordering::Acquire) {
            return Err(ProtocolError::new(ErrorCode::JobCancelled, "Job cancelled"));
        }
        if !inner.registry.lock().unwrap().paused {
            return Ok(());
        }
        thread::sleep(Duration::from_millis(20));
    }
}

fn writer_guard<'a>(
    inner: &'a Inner,
    cancelled: &AtomicBool,
) -> Result<std::sync::MutexGuard<'a, Registry>> {
    loop {
        boundary(inner, cancelled)?;
        let state = inner
            .registry
            .lock()
            .map_err(|_| internal("Registry mutex poisoned"))?;
        if !state.paused
            && !inner.stopping.load(Ordering::Acquire)
            && !cancelled.load(Ordering::Acquire)
        {
            return Ok(state);
        }
        drop(state);
    }
}

fn run_job(
    inner: &Inner,
    job: &Job,
    cancelled: &Arc<AtomicBool>,
    parsers: &mut index::ParsePool,
) -> Result<String> {
    boundary(inner, cancelled)?;
    let project = inner
        .registry
        .lock()
        .unwrap()
        .projects
        .get(&job.project_id)
        .cloned()
        .ok_or_else(|| ProtocolError::new(ErrorCode::ProjectNotFound, "Removed project"))?;
    let generation = id();
    if !project.root.is_dir() {
        return Err(ProtocolError::new(
            ErrorCode::InvalidRoot,
            "Registered root is unavailable",
        ));
    }
    inner.with_store(|store| store.begin_generation(&project.id, &generation))?;
    let result = (|| {
        let entries =
            index::enumerate_controlled(&project.root, &project.config, &[&inner.data], &|| {
                boundary(inner, cancelled).map_err(|error| error.to_string())
            })
            .map_err(internal)?;
        let previous = inner.with_store(|store| store.current(&project.id))?;
        let limit = project.config.max_file_bytes.unwrap_or(5 * 1024 * 1024);
        let mut eligible = 0;
        let mut text_count = 0;
        let mut structural = 0;
        let mut excluded = 0;
        let mut skipped = 0;
        let mut failed = 0;
        for entry in entries {
            boundary(inner, cancelled)?;
            let file = if entry.disposition == index::FileDisposition::Eligible {
                eligible += 1;
                match index::capture(&project.root, &entry.path, limit, cancelled) {
                    Ok(mut snapshot) => {
                        let cached = if job.kind != "reindex" {
                            previous.as_ref().and_then(|old| {
                                inner
                                    .with_store(|store| {
                                        store.cached_file(old, &entry.path, &snapshot.sha256)
                                    })
                                    .ok()
                                    .flatten()
                            })
                        } else {
                            None
                        };
                        let record = if let Some(cached) = cached {
                            cached
                        } else {
                            let extension = Path::new(&entry.path)
                                .extension()
                                .and_then(|e| e.to_str())
                                .unwrap_or("");
                            let (returned, parsed, _) = parsers
                                .parse(extension, snapshot, cancelled.clone())
                                .map_err(internal)?;
                            snapshot = returned;
                            match parsed {
                                Ok(extraction) => {
                                    json!({"state":"indexed","extraction":extraction,"byte_length":snapshot.bytes.len()})
                                }
                                Err(error) => json!({"state":"partial","reason":error}),
                            }
                        };
                        text_count += 1;
                        if record["extraction"]["language"]
                            .as_str()
                            .is_some_and(|lang| lang != "text")
                        {
                            structural += 1;
                        }
                        if record["extraction"]["partial"] == true || record["state"] == "partial" {
                            failed += 1;
                        }
                        StoredFile {
                            path: entry.path,
                            sha256: Some(snapshot.sha256),
                            bytes: Some(snapshot.bytes),
                            record,
                        }
                    }
                    Err(reason) => {
                        skipped += 1;
                        StoredFile {
                            path: entry.path,
                            sha256: None,
                            bytes: None,
                            record: json!({"state":"skipped","reason":reason}),
                        }
                    }
                }
            } else {
                match &entry.disposition {
                    index::FileDisposition::Excluded(_) => excluded += 1,
                    index::FileDisposition::Skipped(_) => skipped += 1,
                    index::FileDisposition::Error(_) => failed += 1,
                    _ => {}
                }
                StoredFile {
                    path: entry.path,
                    sha256: None,
                    bytes: None,
                    record: json!(entry.disposition),
                }
            };
            boundary(inner, cancelled)?;
            let state = writer_guard(inner, cancelled)?;
            if !state.projects.contains_key(&project.id) {
                return Err(ProtocolError::new(
                    ErrorCode::JobCancelled,
                    "Project removed",
                ));
            }
            // The registry guard serializes pause acknowledgement with each cache write.
            inner.with_store(|store| store.stage_file(&generation, &file))?;
        }
        boundary(inner, cancelled)?;
        let mut state = writer_guard(inner, cancelled)?;
        let current = state
            .projects
            .get_mut(&project.id)
            .ok_or_else(|| ProtocolError::new(ErrorCode::JobCancelled, "Project removed"))?;
        let coverage = if skipped == 0 && failed == 0 {
            "complete"
        } else {
            "partial"
        };
        let summary = json!({"coverage":coverage,"eligible_count":eligible,"text_count":text_count,"structural_count":structural,"excluded_count":excluded,"skipped_count":skipped,"failed_count":failed,"observed_at":now()});
        inner.with_store(|store| store.publish(&project.id, &generation, &summary))?;
        current.dirty = current.revision != project.revision;
        current.last_reconciliation = Some(now());
        inner.save(&state)?;
        Ok(generation.clone())
    })();
    if result.is_err() {
        let _ = inner.with_store(|store| store.abandon(&generation));
    }
    result
}

#[cfg(test)]
#[path = "../tests/unit/service.rs"]
mod repair_tests;
