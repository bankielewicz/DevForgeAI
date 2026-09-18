//! Protocol v1 owns wire limits, strict requests, and shared error categories.
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::io::{self, Read, Write};

pub const REQUEST_LIMIT: usize = 1024 * 1024;
pub const RESPONSE_LIMIT: usize = 8 * 1024 * 1024;
pub const DEFAULT_TIMEOUT_MS: u64 = 10_000;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum ErrorCode {
    InvalidArgument,
    InvalidRoot,
    UnsupportedPlatform,
    PathOutsideProject,
    ServiceUnavailable,
    EnvironmentStopped,
    WslCliMissing,
    ProtocolIncompatible,
    IndexNotReady,
    IndexIncomplete,
    IndexPaused,
    SnapshotExpired,
    StaleSymbol,
    ProjectNotFound,
    SymbolNotFound,
    JobNotFound,
    EnvironmentNotFound,
    Timeout,
    InternalError,
    StorageCorrupt,
    JobConflict,
    RequestIdConflict,
    InstanceConflict,
    RootOverlap,
    AccessDenied,
    JobFailed,
    JobCancelled,
    JobInterrupted,
}

impl ErrorCode {
    pub fn exit_code(self) -> i32 {
        use ErrorCode::*;
        match self {
            InvalidArgument | InvalidRoot | UnsupportedPlatform | PathOutsideProject => 2,
            ServiceUnavailable | EnvironmentStopped | WslCliMissing => 3,
            ProtocolIncompatible => 4,
            IndexNotReady | IndexIncomplete | IndexPaused | SnapshotExpired | StaleSymbol => 5,
            ProjectNotFound | SymbolNotFound | JobNotFound | EnvironmentNotFound => 6,
            Timeout => 7,
            InternalError | StorageCorrupt => 8,
            JobConflict | RequestIdConflict | InstanceConflict | RootOverlap => 9,
            AccessDenied => 10,
            JobFailed | JobCancelled | JobInterrupted => 11,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProtocolError {
    pub code: ErrorCode,
    pub message: String,
    pub details: Value,
}

impl ProtocolError {
    pub fn new(code: ErrorCode, message: impl Into<String>) -> Self {
        Self {
            code,
            message: message.into(),
            details: json!({}),
        }
    }
    pub fn details(mut self, details: Value) -> Self {
        self.details = details;
        self
    }
}

impl std::fmt::Display for ProtocolError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{:?}: {}", self.code, self.message)
    }
}
impl std::error::Error for ProtocolError {}
pub type Result<T> = std::result::Result<T, ProtocolError>;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Request {
    pub protocol_version: u32,
    pub request_id: String,
    pub operation: String,
    pub timeout_ms: u64,
    pub params: Value,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectConfig {
    pub exclusions: Option<Vec<String>>,
    pub text_extensions: Option<Vec<String>>,
    pub text_names: Option<Vec<String>>,
    pub default_exclusions: Option<bool>,
    pub max_file_bytes: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "operation", content = "params", deny_unknown_fields)]
pub enum Operation {
    #[serde(rename = "daemon.handshake")]
    Handshake {},
    #[serde(rename = "daemon.status")]
    Status {},
    #[serde(rename = "daemon.pause")]
    Pause {},
    #[serde(rename = "daemon.resume")]
    Resume {},
    #[serde(rename = "daemon.stop")]
    Stop {},
    #[serde(rename = "daemon.diagnostics")]
    Diagnostics {},
    #[serde(rename = "project.list")]
    ProjectList {},
    #[serde(rename = "project.add")]
    ProjectAdd { root: String, name: String },
    #[serde(rename = "project.update")]
    ProjectUpdate {
        project_id: String,
        config: ProjectConfig,
    },
    #[serde(rename = "project.remove")]
    ProjectRemove { project_id: String },
    #[serde(rename = "index.status")]
    IndexStatus { project_id: String },
    #[serde(rename = "index.rescan")]
    Rescan { project_id: String },
    #[serde(rename = "index.reindex")]
    Reindex { project_id: String },
    #[serde(rename = "index.reconcile")]
    Reconcile { project_id: String },
    #[serde(rename = "index.rebuild")]
    Rebuild {
        project_id: String,
        affected_projects: Vec<String>,
    },
    #[serde(rename = "job.status")]
    JobStatus { job_id: String },
    #[serde(rename = "job.cancel")]
    JobCancel { job_id: String },
}

pub fn valid_uuid(value: &str) -> bool {
    value.len() == 36
        && value.bytes().enumerate().all(|(i, c)| {
            if [8, 13, 18, 23].contains(&i) {
                c == b'-'
            } else {
                c.is_ascii_hexdigit()
            }
        })
}

impl Request {
    pub fn decode(bytes: &[u8]) -> Result<Self> {
        let invalid = |message| ProtocolError::new(ErrorCode::InvalidArgument, message);
        if bytes.len() > REQUEST_LIMIT {
            return Err(invalid("Request exceeds 1 MiB"));
        }
        // Version negotiation is deliberately independent of operation validation.
        let header: Value =
            serde_json::from_slice(bytes).map_err(|_| invalid("Invalid JSON request"))?;
        if header
            .get("protocol_version")
            .and_then(Value::as_u64)
            .is_some_and(|v| v != 1)
        {
            return Err(ProtocolError::new(
                ErrorCode::ProtocolIncompatible,
                "Protocol major version 1 required",
            ));
        }
        let request: Self =
            serde_json::from_slice(bytes).map_err(|_| invalid("Invalid request fields"))?;
        if request.protocol_version != 1
            || !valid_uuid(&request.request_id)
            || !(100..=120_000).contains(&request.timeout_ms)
        {
            return Err(invalid("Invalid version, UUID or timeout (100..120000 ms)"));
        }
        request.typed_operation()?;
        Ok(request)
    }

    pub fn typed_operation(&self) -> Result<Operation> {
        let operation: Operation =
            serde_json::from_value(json!({"operation":self.operation,"params":self.params}))
                .map_err(|_| {
                    ProtocolError::new(
                        ErrorCode::InvalidArgument,
                        "Unknown operation or invalid operation parameters",
                    )
                })?;
        let valid = match &operation {
            Operation::ProjectAdd { root, name } => {
                !root.is_empty() && !root.contains('\0') && !name.trim().is_empty()
            }
            Operation::ProjectUpdate { project_id, config } => {
                valid_uuid(project_id)
                    && config
                        .max_file_bytes
                        .is_none_or(|n| (1024..=50 * 1024 * 1024).contains(&n))
            }
            Operation::ProjectRemove { project_id }
            | Operation::IndexStatus { project_id }
            | Operation::Rescan { project_id }
            | Operation::Reindex { project_id }
            | Operation::Reconcile { project_id } => valid_uuid(project_id),
            Operation::Rebuild {
                project_id,
                affected_projects,
            } => {
                valid_uuid(project_id)
                    && !affected_projects.is_empty()
                    && affected_projects.iter().all(|id| valid_uuid(id))
            }
            Operation::JobStatus { job_id } | Operation::JobCancel { job_id } => valid_uuid(job_id),
            _ => true,
        };
        if !valid {
            return Err(ProtocolError::new(
                ErrorCode::InvalidArgument,
                "Invalid operation values",
            ));
        }
        Ok(operation)
    }
}

impl Operation {
    pub fn is_mutation(&self) -> bool {
        !matches!(
            self,
            Self::Handshake {}
                | Self::Status {}
                | Self::Diagnostics {}
                | Self::ProjectList {}
                | Self::IndexStatus { .. }
                | Self::JobStatus { .. }
        )
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Response {
    pub protocol_version: u32,
    pub request_id: String,
    pub service_version: Option<String>,
    pub environment_id: Option<String>,
    pub ok: bool,
    pub data: Value,
    pub error: Option<ProtocolError>,
}

impl Response {
    pub fn success(request_id: impl Into<String>, data: Value) -> Self {
        Self {
            protocol_version: 1,
            request_id: request_id.into(),
            service_version: None,
            environment_id: None,
            ok: true,
            data,
            error: None,
        }
    }
    pub fn failure(
        request_id: impl Into<String>,
        code: ErrorCode,
        message: impl Into<String>,
    ) -> Self {
        Self::from_error(request_id, ProtocolError::new(code, message))
    }
    pub fn from_error(request_id: impl Into<String>, error: ProtocolError) -> Self {
        Self {
            protocol_version: 1,
            request_id: request_id.into(),
            service_version: None,
            environment_id: None,
            ok: false,
            data: Value::Null,
            error: Some(error),
        }
    }
    pub fn with_environment(mut self, environment_id: &str) -> Self {
        self.environment_id = Some(environment_id.into());
        self.service_version = Some(env!("CARGO_PKG_VERSION").into());
        self
    }
    pub fn exit_code(&self) -> i32 {
        self.error.as_ref().map_or(0, |e| e.code.exit_code())
    }
}

pub fn read_frame(reader: &mut impl Read, limit: usize) -> io::Result<Vec<u8>> {
    let mut header = [0; 4];
    reader.read_exact(&mut header)?;
    let length = u32::from_be_bytes(header) as usize;
    if length == 0 || length > limit {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "Frame length outside bounds",
        ));
    }
    let mut bytes = vec![0; length];
    reader.read_exact(&mut bytes)?;
    Ok(bytes)
}

pub fn write_frame(writer: &mut impl Write, bytes: &[u8], limit: usize) -> io::Result<()> {
    if bytes.is_empty() || bytes.len() > limit || bytes.len() > u32::MAX as usize {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "Frame length outside bounds",
        ));
    }
    writer.write_all(&(bytes.len() as u32).to_be_bytes())?;
    writer.write_all(bytes)?;
    writer.flush()
}
