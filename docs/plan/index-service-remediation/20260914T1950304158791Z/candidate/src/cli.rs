//! Terminal management commands. All daemon data flows through the shared client.
use crate::{
    client, host,
    platform::{self, Paths},
    protocol::{
        ErrorCode, ProtocolError, REQUEST_LIMIT, RESPONSE_LIMIT, Request, Response, Result,
    },
};
use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::{
    collections::BTreeMap,
    path::PathBuf,
    process::Stdio,
    time::{Duration, Instant},
};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[derive(Parser)]
#[command(
    name = "devforgeai",
    version,
    about = "Local source index management; index observations are not framework acceptance."
)]
struct Cli {
    #[arg(long, global = true)]
    json: bool,
    #[arg(long, global = true, default_value = "local")]
    environment: String,
    #[arg(long,global=true,default_value_t=10000,value_parser=clap::value_parser!(u64).range(100..=120000))]
    timeout_ms: u64,
    #[command(subcommand)]
    command: Command,
}
#[derive(Subcommand)]
enum Command {
    Daemon {
        #[command(subcommand)]
        action: Daemon,
    },
    Project {
        #[command(subcommand)]
        action: Project,
    },
    Index {
        #[command(subcommand)]
        action: Index,
    },
    Job {
        #[command(subcommand)]
        action: Job,
    },
    Environment {
        #[command(subcommand)]
        action: Environment,
    },
    Tray {
        #[command(subcommand)]
        action: Option<Tray>,
    },
    #[command(hide = true)]
    Bridge {
        #[command(subcommand)]
        action: Bridge,
    },
}
#[derive(Subcommand)]
enum Daemon {
    Start,
    Run,
    Status,
    Pause,
    Resume,
    Stop,
    Diagnostics,
}
#[derive(Subcommand)]
enum Project {
    Add {
        #[arg(long)]
        root: String,
        #[arg(long)]
        name: String,
    },
    List,
    Update {
        #[arg(long)]
        project: String,
        #[arg(long)]
        config_file: PathBuf,
    },
    Remove {
        #[arg(long)]
        project: String,
        #[arg(long, required = true)]
        yes: bool,
    },
}
#[derive(Subcommand)]
enum Index {
    Status {
        #[arg(long)]
        project: String,
    },
    Rescan {
        #[arg(long)]
        project: String,
        #[arg(
            long,
            help = "Wait for successful completion; failed/cancelled/interrupted jobs exit 11"
        )]
        wait: bool,
    },
    Reindex {
        #[arg(long)]
        project: String,
        #[arg(
            long,
            help = "Wait for successful completion; timeout does not cancel the job"
        )]
        wait: bool,
    },
    Rebuild {
        #[arg(long)]
        project: String,
        #[arg(long, required = true)]
        yes: bool,
        #[arg(long, value_delimiter = ',', required = true)]
        affected_projects: Vec<String>,
    },
}
#[derive(Subcommand)]
enum Job {
    Status {
        #[arg(long)]
        job: String,
    },
    Cancel {
        #[arg(long)]
        job: String,
    },
}
#[derive(Subcommand)]
enum Environment {
    AddWsl {
        #[arg(long)]
        alias: String,
        #[arg(long)]
        distribution: String,
        #[arg(long)]
        user: String,
        #[arg(long)]
        cli: String,
    },
    List,
    Remove {
        #[arg(long)]
        alias: String,
    },
}
#[derive(Subcommand)]
enum Bridge {
    Request {
        #[arg(long)]
        bootstrap: bool,
    },
}
#[derive(Subcommand)]
enum Tray {
    Settings {
        #[command(subcommand)]
        action: Settings,
    },
}
#[derive(Subcommand)]
enum Settings {
    Show,
    Set {
        #[arg(long)]
        launch_at_sign_in: Option<bool>,
        #[arg(long)]
        start_local_daemon: Option<bool>,
    },
}

fn invalid(message: impl Into<String>) -> ProtocolError {
    ProtocolError::new(ErrorCode::InvalidArgument, message)
}
fn make(operation: &str, params: Value, timeout: u64) -> Request {
    Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: operation.into(),
        timeout_ms: timeout,
        params,
    }
}
impl Cli {
    fn request(&self) -> Result<Option<Request>> {
        let (operation, params) = match &self.command {
            Command::Daemon { action } => match action {
                Daemon::Status => ("daemon.status", json!({})),
                Daemon::Pause => ("daemon.pause", json!({})),
                Daemon::Resume => ("daemon.resume", json!({})),
                Daemon::Stop => ("daemon.stop", json!({})),
                Daemon::Diagnostics => ("daemon.diagnostics", json!({})),
                _ => return Ok(None),
            },
            Command::Project { action } => match action {
                Project::Add { root, name } => ("project.add", json!({"root":root,"name":name})),
                Project::List => ("project.list", json!({})),
                Project::Remove { project, .. } => {
                    ("project.remove", json!({"project_id":project}))
                }
                Project::Update {
                    project,
                    config_file,
                } => {
                    let bytes =
                        std::fs::read(config_file).map_err(|error| invalid(error.to_string()))?;
                    if bytes.len() > REQUEST_LIMIT {
                        return Err(invalid("Configuration exceeds request limit"));
                    }
                    let config: Value = serde_json::from_slice(&bytes)
                        .map_err(|error| invalid(error.to_string()))?;
                    (
                        "project.update",
                        json!({"project_id":project,"config":config}),
                    )
                }
            },
            Command::Index { action } => match action {
                Index::Status { project } => ("index.status", json!({"project_id":project})),
                Index::Rescan { project, .. } => ("index.rescan", json!({"project_id":project})),
                Index::Reindex { project, .. } => ("index.reindex", json!({"project_id":project})),
                Index::Rebuild {
                    project,
                    affected_projects,
                    ..
                } => (
                    "index.rebuild",
                    json!({"project_id":project,"affected_projects":affected_projects}),
                ),
            },
            Command::Job { action } => match action {
                Job::Status { job } => ("job.status", json!({"job_id":job})),
                Job::Cancel { job } => ("job.cancel", json!({"job_id":job})),
            },
            _ => return Ok(None),
        };
        let request = make(operation, params, self.timeout_ms);
        Request::decode(&serde_json::to_vec(&request).map_err(|e| invalid(e.to_string()))?)
            .map(Some)
    }
}
pub fn parse_request(args: &[&str]) -> Result<Option<Request>> {
    Cli::try_parse_from(args)
        .map_err(|e| invalid(e.to_string()))?
        .request()
}

pub async fn run(args: Vec<String>) -> i32 {
    let json_mode = args.iter().any(|arg| arg == "--json");
    let cli = match Cli::try_parse_from(&args) {
        Ok(cli) => cli,
        Err(error) => {
            if matches!(
                error.kind(),
                clap::error::ErrorKind::DisplayHelp | clap::error::ErrorKind::DisplayVersion
            ) {
                if json_mode {
                    emit(
                        &Response::success(
                            uuid::Uuid::new_v4().to_string(),
                            json!({"help":error.to_string()}),
                        ),
                        true,
                    );
                } else {
                    print!("{error}");
                }
                return 0;
            }
            let response =
                Response::from_error(uuid::Uuid::new_v4().to_string(), invalid(error.to_string()));
            emit(&response, json_mode);
            return response.exit_code();
        }
    };
    // Validate CLI inputs before creating any application directories.
    let request = match cli.request() {
        Ok(request) => request,
        Err(error) => {
            let response = Response::from_error(uuid::Uuid::new_v4().to_string(), error);
            emit(&response, cli.json);
            return response.exit_code();
        }
    };
    let result = execute_cli(&cli, request).await;
    let response = result
        .unwrap_or_else(|error| Response::from_error(uuid::Uuid::new_v4().to_string(), error));
    emit(
        &response,
        cli.json || matches!(cli.command, Command::Bridge { .. }),
    );
    response.exit_code()
}
fn emit(response: &Response, json_mode: bool) {
    if json_mode {
        println!(
            "{}",
            serde_json::to_string(response).expect("Response is JSON serializable")
        );
    } else if let Some(error) = &response.error {
        eprintln!("{error}");
    } else {
        println!(
            "{}",
            serde_json::to_string_pretty(&response.data).expect("Data is JSON serializable")
        );
    }
}

async fn execute_cli(cli: &Cli, request: Option<Request>) -> Result<Response> {
    let paths = Paths::discover()?;
    let started = Instant::now();
    match &cli.command {
        Command::Daemon {
            action: Daemon::Run,
        } => {
            if cli.environment != "local" {
                return Err(invalid("daemon run is local only"));
            }
            host::serve(paths).await?;
            return Ok(Response::success(
                uuid::Uuid::new_v4().to_string(),
                json!({"daemon_state":"stopped"}),
            ));
        }
        Command::Daemon {
            action: Daemon::Start,
        } => {
            let request = make("daemon.handshake", json!({}), cli.timeout_ms);
            return if cli.environment == "local" {
                start(&paths, &request).await
            } else {
                route(&paths, &cli.environment, &request, true).await
            };
        }
        Command::Environment { action } => return environment(&paths, action),
        Command::Tray { action } => {
            if cli.environment != "local" {
                return Err(invalid(
                    "Tray preferences and launch are local Windows operations",
                ));
            }
            let data = match action {
                None => {
                    crate::tray::launch()?;
                    json!({"tray":"launched_or_focused"})
                }
                Some(Tray::Settings {
                    action: Settings::Show,
                }) => json!(crate::tray::preferences(&paths)?),
                Some(Tray::Settings {
                    action:
                        Settings::Set {
                            launch_at_sign_in,
                            start_local_daemon,
                        },
                }) => json!(crate::tray::set_preferences(
                    &paths,
                    *launch_at_sign_in,
                    *start_local_daemon
                )?),
            };
            return Ok(Response::success(uuid::Uuid::new_v4().to_string(), data));
        }
        Command::Bridge {
            action: Bridge::Request { bootstrap },
        } => {
            use std::io::Read;
            if cli.environment != "local" {
                return Err(invalid("Bridge is local only"));
            }
            let mut bytes = Vec::new();
            std::io::stdin()
                .take((REQUEST_LIMIT + 1) as u64)
                .read_to_end(&mut bytes)
                .map_err(platform::io_error)?;
            let request = Request::decode(&bytes)?;
            if *bootstrap {
                if request.operation != "daemon.handshake" {
                    return Err(invalid("Bootstrap requires daemon.handshake"));
                }
                return start(&paths, &request).await;
            }
            return client::local(&paths, &request).await;
        }
        _ => {}
    }
    let request = request.ok_or_else(|| invalid("No management operation selected"))?;
    if let Command::Index {
        action: Index::Rebuild {
            affected_projects, ..
        },
    } = &cli.command
    {
        let preview = route(
            &paths,
            &cli.environment,
            &make("project.list", json!({}), remaining(cli, started)?),
            false,
        )
        .await?;
        if !preview.ok {
            return Ok(preview);
        }
        let mut expected: Vec<String> = preview.data["projects"]
            .as_array()
            .ok_or_else(|| invalid("Invalid project preview"))?
            .iter()
            .filter_map(|project| project["id"].as_str().map(String::from))
            .collect();
        expected.sort();
        eprintln!(
            "Rebuild affects cached data for projects: {}",
            expected.join(",")
        );
        let mut supplied = affected_projects.clone();
        supplied.sort();
        if supplied != expected {
            return Err(invalid(
                "--affected-projects does not match current preview",
            ));
        }
    }
    let result = route(&paths, &cli.environment, &request, false).await;
    let mut response = match result {
        Err(error)
            if cli.environment == "local"
                && error.code == ErrorCode::ServiceUnavailable
                && matches!(
                    cli.command,
                    Command::Daemon {
                        action: Daemon::Status | Daemon::Stop
                    }
                ) =>
        {
            return Ok(Response::success(
                &request.request_id,
                json!({"daemon_state":"stopped","already_stopped":true}),
            ));
        }
        Err(error) => return Err(error),
        Ok(response) => response,
    };
    if matches!(
        cli.command,
        Command::Daemon {
            action: Daemon::Stop
        }
    ) && response.ok
    {
        loop {
            let status = make("daemon.handshake", json!({}), remaining(cli, started)?);
            match route(&paths, &cli.environment, &status, false).await {
                Err(error) if error.code == ErrorCode::ServiceUnavailable => {
                    // Endpoint closure alone precedes final storage flush and lock release.
                    if cli.environment == "local" && paths.lock().is_err() {
                        tokio::time::sleep(Duration::from_millis(20)).await;
                        continue;
                    }
                    response.data = json!({"daemon_state":"stopped","already_stopped":false});
                    break;
                }
                Err(error) => return Err(error),
                Ok(_) => tokio::time::sleep(Duration::from_millis(20)).await,
            }
        }
    }
    if matches!(
        cli.command,
        Command::Index {
            action: Index::Rescan { wait: true, .. } | Index::Reindex { wait: true, .. }
        }
    ) && response.ok
    {
        let job = response.data["job_id"]
            .as_str()
            .ok_or_else(|| invalid("Missing job ID"))?
            .to_owned();
        loop {
            let status = make(
                "job.status",
                json!({"job_id":job}),
                remaining(cli, started)?,
            );
            let next = route(&paths, &cli.environment, &status, false).await?;
            if !next.ok {
                return Ok(next);
            }
            let outcome = next.data["outcome"]
                .as_str()
                .ok_or_else(|| invalid("Missing job outcome"))?;
            match outcome {
                "succeeded" => {
                    response.data = next.data;
                    break;
                }
                "failed" | "cancelled" | "interrupted" => {
                    let code = match outcome {
                        "cancelled" => ErrorCode::JobCancelled,
                        "interrupted" => ErrorCode::JobInterrupted,
                        _ => ErrorCode::JobFailed,
                    };
                    return Ok(Response::from_error(
                        &request.request_id,
                        ProtocolError::new(code, "Waited job ended unsuccessfully")
                            .details(next.data),
                    ));
                }
                _ => tokio::time::sleep(Duration::from_millis(25)).await,
            }
        }
    }
    Ok(response)
}
fn remaining(cli: &Cli, started: Instant) -> Result<u64> {
    let left = cli
        .timeout_ms
        .saturating_sub(started.elapsed().as_millis() as u64);
    if left < 100 {
        Err(ProtocolError::new(
            ErrorCode::Timeout,
            "End-to-end deadline expired; jobs and mutations are not cancelled",
        ))
    } else {
        Ok(left)
    }
}

pub async fn start(paths: &Paths, request: &Request) -> Result<Response> {
    let started = Instant::now();
    match client::local(paths, request).await {
        Ok(mut response) => {
            if response.ok {
                response.data["already_running"] = json!(true);
            }
            return Ok(response);
        }
        Err(error) if error.code == ErrorCode::ServiceUnavailable => {}
        Err(error) => return Err(error),
    }
    let executable = std::env::current_exe()
        .map_err(platform::io_error)?
        .with_file_name(if cfg!(windows) {
            "devforgeai-indexd.exe"
        } else {
            "devforgeai-indexd"
        });
    #[cfg(unix)]
    let mut command = std::process::Command::new(&executable);
    #[cfg(unix)]
    command
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null());
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        unsafe {
            command.pre_exec(|| {
                if libc::setsid() < 0 {
                    return Err(std::io::Error::last_os_error());
                }
                Ok(())
            });
        }
    }
    #[cfg(unix)]
    let mut child = command.spawn().map_err(platform::io_error)?;
    #[cfg(windows)]
    let mut child = platform::windows::spawn_detached(&executable)?;
    loop {
        if started.elapsed() >= Duration::from_millis(request.timeout_ms) {
            return Err(ProtocolError::new(
                ErrorCode::Timeout,
                "Daemon startup deadline expired; child was not force-killed",
            ));
        }
        let mut probe = request.clone();
        probe.timeout_ms = request
            .timeout_ms
            .saturating_sub(started.elapsed().as_millis() as u64)
            .max(100);
        match client::local(paths, &probe).await {
            Ok(mut response) => {
                response.data["already_running"] =
                    json!(child.try_wait().map_err(platform::io_error)?.is_some());
                return Ok(response);
            }
            Err(error) if error.code == ErrorCode::ServiceUnavailable => {}
            Err(error) => return Err(error),
        }
        #[cfg(unix)]
        let exited = child
            .try_wait()
            .map_err(platform::io_error)?
            .map(|status| status.code().unwrap_or(-1));
        #[cfg(windows)]
        let exited = child.try_wait().map_err(platform::io_error)?;
        if let Some(status) = exited
            && status != 9
        {
            return Err(ProtocolError::new(
                ErrorCode::ServiceUnavailable,
                format!("Daemon exited before handshake: {status}"),
            ));
        }
        tokio::time::sleep(Duration::from_millis(20)).await;
    }
}

#[derive(Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WslEnvironment {
    pub distribution: String,
    pub user: String,
    pub cli: String,
}
pub fn aliases(paths: &Paths) -> Result<BTreeMap<String, WslEnvironment>> {
    let file = paths.data.join("environments.json");
    if !file.exists() {
        return Ok(BTreeMap::new());
    }
    serde_json::from_slice(&std::fs::read(file).map_err(platform::io_error)?)
        .map_err(|error| invalid(error.to_string()))
}
fn environment(paths: &Paths, action: &Environment) -> Result<Response> {
    let mut aliases = aliases(paths)?;
    let data = match action {
        Environment::List => json!({"local":true,"wsl":aliases}),
        Environment::AddWsl {
            alias,
            distribution,
            user,
            cli,
        } => {
            if !cfg!(windows) {
                return Err(ProtocolError::new(
                    ErrorCode::UnsupportedPlatform,
                    "WSL aliases are Windows-only",
                ));
            }
            if alias.trim().is_empty()
                || alias == "local"
                || distribution.trim().is_empty()
                || user.trim().is_empty()
                || !cli.starts_with('/')
                || [alias, distribution, user, cli]
                    .iter()
                    .any(|value| value.contains('\0'))
            {
                return Err(invalid("Invalid WSL alias, identity or absolute CLI path"));
            }
            aliases.insert(
                alias.clone(),
                WslEnvironment {
                    distribution: distribution.clone(),
                    user: user.clone(),
                    cli: cli.clone(),
                },
            );
            platform::atomic_write(
                &paths.data.join("environments.json"),
                &serde_json::to_vec(&aliases).map_err(|e| invalid(e.to_string()))?,
            )?;
            json!({"alias":alias,"registered":true})
        }
        Environment::Remove { alias } => {
            if alias == "local" {
                return Err(invalid("local cannot be removed"));
            }
            if aliases.remove(alias).is_none() {
                return Err(ProtocolError::new(
                    ErrorCode::EnvironmentNotFound,
                    "Unknown alias",
                ));
            }
            platform::atomic_write(
                &paths.data.join("environments.json"),
                &serde_json::to_vec(&aliases).map_err(|e| invalid(e.to_string()))?,
            )?;
            json!({"alias":alias,"unregistered":true})
        }
    };
    Ok(Response::success(uuid::Uuid::new_v4().to_string(), data))
}

pub async fn route(
    paths: &Paths,
    environment: &str,
    request: &Request,
    bootstrap: bool,
) -> Result<Response> {
    if environment == "local" {
        return if bootstrap {
            start(paths, request).await
        } else {
            client::local(paths, request).await
        };
    }
    let environment = aliases(paths)?.remove(environment).ok_or_else(|| {
        ProtocolError::new(ErrorCode::EnvironmentNotFound, "Unknown environment alias")
    })?;
    bridge(&environment, request, bootstrap).await
}

pub async fn bridge(
    environment: &WslEnvironment,
    request: &Request,
    bootstrap: bool,
) -> Result<Response> {
    bridge_with_executable(
        environment,
        request,
        bootstrap,
        std::path::Path::new("wsl.exe"),
    )
    .await
}

// Keep OS process construction at an explicit boundary so protocol checks can
// exercise a controlled peer without starting or depending on a WSL installation.
async fn bridge_with_executable(
    environment: &WslEnvironment,
    request: &Request,
    bootstrap: bool,
    executable: &std::path::Path,
) -> Result<Response> {
    if !cfg!(windows) {
        return Err(ProtocolError::new(
            ErrorCode::UnsupportedPlatform,
            "WSL relay requires Windows",
        ));
    }
    tokio::time::timeout(Duration::from_millis(request.timeout_ms), async {
        if !bootstrap && !wsl_running(&environment.distribution, executable).await? {
            return Err(ProtocolError::new(
                ErrorCode::EnvironmentStopped,
                "Distribution is stopped; only explicit Start may launch it",
            ));
        }
        let mut command = tokio::process::Command::new(executable);
        command.args([
            "--distribution",
            &environment.distribution,
            "--user",
            &environment.user,
            "--exec",
            &environment.cli,
            "bridge",
            "request",
        ]);
        if bootstrap {
            command.arg("--bootstrap");
        }
        command
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .kill_on_drop(true);
        #[cfg(windows)]
        command.creation_flags(0x08000000);
        // Recheck immediately before invoking a Linux executable. WSL may still stop
        // between this observation and CreateProcess; inventory is not a lifecycle lock.
        if !bootstrap && !wsl_running(&environment.distribution, executable).await? {
            return Err(ProtocolError::new(
                ErrorCode::EnvironmentStopped,
                "Distribution stopped before bridge invocation",
            ));
        }
        let mut child = command
            .spawn()
            .map_err(|error| ProtocolError::new(ErrorCode::WslCliMissing, error.to_string()))?;
        let mut input = child
            .stdin
            .take()
            .ok_or_else(|| invalid("Missing bridge stdin"))?;
        input
            .write_all(&serde_json::to_vec(request).map_err(|e| invalid(e.to_string()))?)
            .await
            .map_err(platform::io_error)?;
        drop(input);
        let mut bytes = Vec::new();
        child
            .stdout
            .take()
            .ok_or_else(|| invalid("Missing bridge stdout"))?
            .take((RESPONSE_LIMIT + 1) as u64)
            .read_to_end(&mut bytes)
            .await
            .map_err(platform::io_error)?;
        if bytes.len() > RESPONSE_LIMIT {
            return Err(invalid("Bridge response exceeds 8 MiB"));
        }
        let status = child.wait().await.map_err(platform::io_error)?;
        let response: Response = serde_json::from_slice(&bytes).map_err(|_| {
            ProtocolError::new(
                ErrorCode::WslCliMissing,
                format!(
                    "Bridge returned no valid envelope ({status}); verify configured Linux CLI"
                ),
            )
        })?;
        if response.request_id != request.request_id || response.protocol_version != 1 {
            return Err(ProtocolError::new(
                ErrorCode::ProtocolIncompatible,
                "Bridge envelope mismatch",
            ));
        }
        Ok(response)
    })
    .await
    .map_err(|_| {
        ProtocolError::new(
            ErrorCode::Timeout,
            "WSL bridge deadline expired; mutation outcome may be uncertain",
        )
    })?
}
async fn wsl_running(distribution: &str, executable: &std::path::Path) -> Result<bool> {
    let mut command = tokio::process::Command::new(executable);
    command
        .args(["--list", "--running", "--quiet"])
        .kill_on_drop(true);
    #[cfg(windows)]
    command.creation_flags(0x08000000);
    let output = command
        .output()
        .await
        .map_err(|error| ProtocolError::new(ErrorCode::ServiceUnavailable, error.to_string()))?;
    if !output.status.success() {
        return Err(ProtocolError::new(
            ErrorCode::ServiceUnavailable,
            "WSL inventory failed",
        ));
    }
    let text = if output.stdout.contains(&0) {
        String::from_utf16_lossy(
            &output
                .stdout
                .as_chunks::<2>()
                .0
                .iter()
                .map(|pair| u16::from_le_bytes([pair[0], pair[1]]))
                .collect::<Vec<_>>(),
        )
    } else {
        String::from_utf8_lossy(&output.stdout).into_owned()
    };
    Ok(text
        .trim_start_matches('\u{feff}')
        .lines()
        .any(|line| line.trim_end_matches('\r') == distribution))
}

#[cfg(test)]
#[path = "../tests/unit/cli.rs"]
mod repair_tests;
