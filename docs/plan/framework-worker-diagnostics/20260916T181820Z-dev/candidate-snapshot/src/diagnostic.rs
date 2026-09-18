//! Closed observations only; never inputs to qualification or dispatch.
use serde::Serialize;

#[derive(Clone, Copy, Debug, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ConfigSection {
    Effective,
    Origins,
    Layers,
}

#[derive(Clone, Copy, Debug, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ConfigPredicate {
    Shape,
    FixedKeys,
    ProviderMap,
    EndpointOverride,
    ModelProvider,
    LoginMethod,
    WebSearch,
    SandboxMode,
    ApprovalPolicy,
    Features,
    Apps,
    McpServers,
    Plugins,
    SelectedOrigin,
    SourcePaths,
    OriginSource,
    LayerSource,
    SessionFlagsCount,
}

#[derive(Clone, Copy, Serialize)]
#[serde(rename_all = "snake_case")]
pub(crate) enum SourceBoundary {
    PostSpawn,
    PostPreflight,
}

#[derive(Clone, Copy, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub(crate) enum RpcStage {
    Initialize,
    ConfigRead,
    OtherPreflight,
    FinalCheck,
}
impl RpcStage {
    pub(crate) fn from_method(method: &str) -> Self {
        match method {
            "initialize" => Self::Initialize,
            "config/read" => Self::ConfigRead,
            _ => Self::OtherPreflight,
        }
    }
    pub(crate) fn observed(self) -> bool {
        matches!(self, Self::Initialize | Self::ConfigRead)
    }
}

#[derive(Clone, Copy, Serialize)]
#[serde(rename_all = "snake_case")]
pub(crate) enum Checkpoint {
    BeforeSend,
    AfterReceive,
    FinalCheck,
}

#[derive(Serialize)]
#[serde(rename_all = "snake_case")]
pub(crate) enum ProcessPredicate {
    OnlyWorker,
    UnexpectedProcessCount,
    QueryFailed,
}

#[derive(Serialize)]
#[serde(rename_all = "snake_case")]
pub(crate) enum RpcPredicate {
    RpcError,
    ProtocolError,
    Deadline,
    UserCancel,
    ControlError,
    TransportError,
    ProcessGuardRejected,
}
impl RpcPredicate {
    pub(crate) fn from_reason(reason: &str) -> Self {
        match reason {
            "rpc_error" => Self::RpcError,
            "protocol_error" => Self::ProtocolError,
            "deadline" => Self::Deadline,
            "user_cancel" => Self::UserCancel,
            "invalid_control" => Self::ControlError,
            "profile_unqualified" => Self::ProcessGuardRejected,
            _ => Self::TransportError,
        }
    }
}

#[derive(Serialize)]
#[serde(tag = "stage", rename_all = "snake_case")]
pub(crate) enum Diagnostic {
    SourceReview {
        boundary: SourceBoundary,
        predicate: SourcePredicate,
    },
    ProcessAccounting {
        rpc: RpcStage,
        checkpoint: Checkpoint,
        predicate: ProcessPredicate,
        total_processes: Option<u32>,
        active_processes: Option<u32>,
    },
    Rpc {
        rpc: RpcStage,
        predicate: RpcPredicate,
    },
    ConfigValidation {
        section: ConfigSection,
        predicate: ConfigPredicate,
    },
}

#[derive(Serialize)]
#[serde(rename_all = "snake_case")]
pub(crate) enum SourcePredicate {
    ReviewRejected,
}
