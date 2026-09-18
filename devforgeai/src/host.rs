//! Native local-only transport. The daemon alone owns the cache writer and lock.
use crate::{
    client,
    platform::{self, Paths},
    protocol::{
        ErrorCode, ProtocolError, REQUEST_LIMIT, RESPONSE_LIMIT, Request, Response, Result,
    },
    service::Service,
};
use std::{sync::Arc, time::Duration};
use tokio::io::{AsyncRead, AsyncWrite};

#[cfg(windows)]
fn pipe(paths: &Paths, first: bool) -> Result<tokio::net::windows::named_pipe::NamedPipeServer> {
    use windows_sys::Win32::Security::SECURITY_ATTRIBUTES;
    let descriptor = platform::windows::SecurityDescriptor::new(false)?;
    let mut attributes = SECURITY_ATTRIBUTES {
        nLength: std::mem::size_of::<SECURITY_ATTRIBUTES>() as u32,
        lpSecurityDescriptor: descriptor.0,
        bInheritHandle: 0,
    };
    unsafe {
        tokio::net::windows::named_pipe::ServerOptions::new()
            .first_pipe_instance(first)
            .reject_remote_clients(true)
            .create_with_security_attributes_raw(
                &paths.endpoint,
                (&mut attributes as *mut SECURITY_ATTRIBUTES).cast(),
            )
    }
    .map_err(platform::io_error)
}

#[cfg(windows)]
fn authenticate(stream: &tokio::net::windows::named_pipe::NamedPipeServer) -> Result<()> {
    use std::os::windows::io::AsRawHandle;
    use windows_sys::Win32::{Security::RevertToSelf, System::Pipes::ImpersonateNamedPipeClient};
    let expected = platform::current_identity()?;
    if unsafe { ImpersonateNamedPipeClient(stream.as_raw_handle()) } == 0 {
        return Err(ProtocolError::new(
            ErrorCode::AccessDenied,
            "Cannot authenticate pipe peer",
        ));
    }
    let actual = platform::windows::identity(true);
    // Continuing under a peer token is unsafe even if later requests would be rejected.
    if unsafe { RevertToSelf() } == 0 {
        std::process::abort();
    }
    if actual? != expected {
        return Err(ProtocolError::new(
            ErrorCode::AccessDenied,
            "Pipe peer identity differs",
        ));
    }
    Ok(())
}

async fn respond<S: AsyncRead + AsyncWrite + Unpin>(
    stream: &mut S,
    bytes: Vec<u8>,
    service: Arc<Service>,
) -> Result<()> {
    let environment = service.environment_id().to_owned();
    respond_with_executor(stream, bytes, &environment, |request| {
        tokio::task::spawn_blocking(move || service.execute(&request))
    })
    .await
}

// The dispatch task is a boundary: timeout or worker failure must still produce
// an envelope, without restarting or retrying an uncertain mutation.
async fn respond_with_executor<S, F>(
    stream: &mut S,
    bytes: Vec<u8>,
    environment: &str,
    execute: F,
) -> Result<()>
where
    S: AsyncRead + AsyncWrite + Unpin,
    F: FnOnce(Request) -> tokio::task::JoinHandle<Response>,
{
    let response = match Request::decode(&bytes) {
        Ok(request) => {
            let budget = request.timeout_ms;
            let request_id = request.request_id.clone();
            match tokio::time::timeout(Duration::from_millis(budget), execute(request)).await {
                Ok(Ok(response)) => response,
                Ok(Err(error)) => {
                    Response::failure(&request_id, ErrorCode::InternalError, error.to_string())
                }
                Err(_) => Response::failure(
                    &request_id,
                    ErrorCode::Timeout,
                    "Request timed out; mutation outcome may be uncertain",
                ),
            }
        }
        Err(error) => {
            let value: serde_json::Value = serde_json::from_slice(&bytes).unwrap_or_default();
            Response::from_error(value["request_id"].as_str().unwrap_or(""), error)
                .with_environment(environment)
        }
    };
    let bytes = serde_json::to_vec(&response)
        .map_err(|e| ProtocolError::new(ErrorCode::InternalError, e.to_string()))?;
    client::write_frame(stream, &bytes, RESPONSE_LIMIT).await
}

pub async fn serve(paths: Paths) -> Result<()> {
    let _owner = paths.lock()?;
    let service = Arc::new(Service::open(&paths.data)?);
    let slots = Arc::new(tokio::sync::Semaphore::new(64));
    let mut tasks = tokio::task::JoinSet::new();
    #[cfg(windows)]
    let mut listener = pipe(&paths, true)?;
    #[cfg(unix)]
    let listener = {
        use std::os::unix::fs::PermissionsExt;
        let endpoint = std::path::Path::new(&paths.endpoint);
        if endpoint.exists() {
            std::fs::remove_file(endpoint).map_err(platform::io_error)?;
        }
        let listener = tokio::net::UnixListener::bind(endpoint).map_err(platform::io_error)?;
        std::fs::set_permissions(endpoint, std::fs::Permissions::from_mode(0o600))
            .map_err(platform::io_error)?;
        listener
    };
    #[cfg(unix)]
    let mut terminate = tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
        .map_err(platform::io_error)?;
    loop {
        if service.is_stopping() {
            break;
        }
        #[cfg(windows)]
        tokio::select! {
            _=tokio::signal::ctrl_c()=>break,
            _=tokio::time::sleep(Duration::from_millis(20))=>{},
            connected=listener.connect()=>{
                connected.map_err(platform::io_error)?;
                let successor=pipe(&paths,false)?;let mut stream=std::mem::replace(&mut listener,successor);
                if let Ok(permit)=slots.clone().try_acquire_owned(){let service=service.clone();tasks.spawn(async move{
                    let _permit=permit;
                    let _=tokio::time::timeout(Duration::from_secs(120),async{
                        let bytes=client::read_frame(&mut stream,REQUEST_LIMIT).await?;
                        authenticate(&stream)?;respond(&mut stream,bytes,service).await
                    }).await;
                });}
            }
        }
        #[cfg(unix)]
        tokio::select! {
            _=tokio::signal::ctrl_c()=>break,
            _=terminate.recv()=>break,
            _=tokio::time::sleep(Duration::from_millis(20))=>{},
            connection=listener.accept()=>{
                let (mut stream,_)=connection.map_err(platform::io_error)?;
                if stream.peer_cred().map_err(platform::io_error)?.uid()!=unsafe{libc::geteuid()}{continue;}
                if let Ok(permit)=slots.clone().try_acquire_owned(){let service=service.clone();tasks.spawn(async move{
                    let _permit=permit;
                    let _=tokio::time::timeout(Duration::from_secs(120),async{
                        let bytes=client::read_frame(&mut stream,REQUEST_LIMIT).await?;respond(&mut stream,bytes,service).await
                    }).await;
                });}
            }
        }
        while tasks.try_join_next().is_some() {}
    }
    drop(listener);
    let shutdown = service.clone();
    tokio::task::spawn_blocking(move || shutdown.shutdown())
        .await
        .map_err(|e| ProtocolError::new(ErrorCode::InternalError, e.to_string()))??;
    // Give the accepted stop response time to drain; idle clients cannot prevent exit.
    let _ = tokio::time::timeout(Duration::from_secs(1), async {
        while tasks.join_next().await.is_some() {}
    })
    .await;
    tasks.abort_all();
    #[cfg(unix)]
    std::fs::remove_file(&paths.endpoint).map_err(platform::io_error)?;
    Ok(())
}

#[cfg(test)]
#[path = "../tests/unit/host.rs"]
mod repair_tests;
