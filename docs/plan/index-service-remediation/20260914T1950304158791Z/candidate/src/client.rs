//! One budget across connection, request and response. Never retries mutations.
use crate::{
    platform::Paths,
    protocol::{
        ErrorCode, ProtocolError, REQUEST_LIMIT, RESPONSE_LIMIT, Request, Response, Result,
    },
};
use std::time::Duration;
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};

pub(crate) async fn read_frame(
    stream: &mut (impl AsyncRead + Unpin),
    limit: usize,
) -> Result<Vec<u8>> {
    let length = stream.read_u32().await.map_err(transport)? as usize;
    if length == 0 || length > limit {
        return Err(ProtocolError::new(
            ErrorCode::InvalidArgument,
            "Frame exceeds size limit",
        ));
    }
    let mut bytes = vec![0; length];
    stream.read_exact(&mut bytes).await.map_err(transport)?;
    Ok(bytes)
}
pub(crate) async fn write_frame(
    stream: &mut (impl AsyncWrite + Unpin),
    bytes: &[u8],
    limit: usize,
) -> Result<()> {
    if bytes.is_empty() || bytes.len() > limit {
        return Err(ProtocolError::new(
            ErrorCode::InvalidArgument,
            "Frame exceeds size limit",
        ));
    }
    stream
        .write_u32(bytes.len() as u32)
        .await
        .map_err(transport)?;
    stream.write_all(bytes).await.map_err(transport)?;
    stream.flush().await.map_err(transport)
}
fn transport(error: std::io::Error) -> ProtocolError {
    ProtocolError::new(
        if error.kind() == std::io::ErrorKind::PermissionDenied {
            ErrorCode::AccessDenied
        } else {
            ErrorCode::ServiceUnavailable
        },
        error.to_string(),
    )
}
pub async fn local(paths: &Paths, request: &Request) -> Result<Response> {
    let bytes = serde_json::to_vec(request)
        .map_err(|e| ProtocolError::new(ErrorCode::InvalidArgument, e.to_string()))?;
    Request::decode(&bytes)?;
    tokio::time::timeout(Duration::from_millis(request.timeout_ms), async {
        #[cfg(windows)]
        let mut stream = loop {
            match tokio::net::windows::named_pipe::ClientOptions::new().open(&paths.endpoint) {
                Ok(stream) => break stream,
                Err(error) if error.raw_os_error() == Some(231) => {
                    tokio::time::sleep(Duration::from_millis(10)).await
                }
                Err(error) => return Err(transport(error)),
            }
        };
        #[cfg(unix)]
        let mut stream = tokio::net::UnixStream::connect(&paths.endpoint)
            .await
            .map_err(transport)?;
        #[cfg(unix)]
        if stream.peer_cred().map_err(transport)?.uid() != unsafe { libc::geteuid() } {
            return Err(ProtocolError::new(
                ErrorCode::AccessDenied,
                "Endpoint belongs to another UID",
            ));
        }
        write_frame(&mut stream, &bytes, REQUEST_LIMIT).await?;
        let bytes = read_frame(&mut stream, RESPONSE_LIMIT).await?;
        let response: Response = serde_json::from_slice(&bytes)
            .map_err(|e| ProtocolError::new(ErrorCode::ProtocolIncompatible, e.to_string()))?;
        if response.protocol_version != 1
            || response.request_id != request.request_id
            || response.ok != response.error.is_none()
            || !response.ok && !response.data.is_null()
        {
            return Err(ProtocolError::new(
                ErrorCode::ProtocolIncompatible,
                "Invalid response envelope",
            ));
        }
        Ok(response)
    })
    .await
    .map_err(|_| {
        ProtocolError::new(
            ErrorCode::Timeout,
            "Request timed out; mutation outcome may be uncertain",
        )
    })?
}

#[cfg(test)]
#[path = "../tests/unit/client.rs"]
mod repair_tests;
