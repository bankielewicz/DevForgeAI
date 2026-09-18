use crate::capture::{self, Shared};
use crate::request::Result;
use std::{
    ffi::OsStr,
    fs::File,
    io::Write,
    os::windows::{
        ffi::OsStrExt,
        io::{AsRawHandle, FromRawHandle, OwnedHandle},
    },
    path::Path,
    ptr::{null, null_mut},
    sync::{
        Arc,
        atomic::{AtomicU8, AtomicUsize, Ordering},
        mpsc::{self, Receiver},
    },
    thread,
    time::{Duration, Instant},
};
use windows_sys::Win32::{
    Foundation::*,
    Security::SECURITY_ATTRIBUTES,
    System::{JobObjects::*, Pipes::CreatePipe, Threading::*},
};

pub enum Incoming {
    Line(Vec<u8>),
    Stderr { bytes: usize, sha256: String },
    End,
    Error(&'static str),
}
pub struct OwnedProcess {
    job: OwnedHandle,
    process: OwnedHandle,
    input: Option<mpsc::SyncSender<Vec<u8>>>,
    written: Receiver<Result<()>>,
    writer: thread::JoinHandle<()>,
    write_pending: bool,
    pub incoming: Receiver<Incoming>,
    pub stderr: Receiver<Incoming>,
    readers: Vec<thread::JoinHandle<()>>,
    streams: [Shared; 2],
    pub pid: u32,
}
fn wide(s: &OsStr) -> Vec<u16> {
    s.encode_wide().chain(Some(0)).collect()
}
fn checked(ok: i32) -> Result<()> {
    if ok == 0 {
        Err(format!(
            "windows_error_{}",
            std::io::Error::last_os_error().raw_os_error().unwrap_or(0)
        ))
    } else {
        Ok(())
    }
}
fn owned(handle: HANDLE) -> Result<OwnedHandle> {
    if handle.is_null() || handle == INVALID_HANDLE_VALUE {
        return Err("invalid_handle".into());
    }
    // SAFETY: API returned a fresh owned kernel handle.
    Ok(unsafe { OwnedHandle::from_raw_handle(handle) })
}
fn pipe(parent_reads: bool) -> Result<(OwnedHandle, OwnedHandle)> {
    let sa = SECURITY_ATTRIBUTES {
        nLength: std::mem::size_of::<SECURITY_ATTRIBUTES>() as u32,
        lpSecurityDescriptor: null_mut(),
        bInheritHandle: 1,
    };
    let (mut read, mut write) = (null_mut(), null_mut());
    // SAFETY: valid out pointers, both handles immediately enter RAII ownership.
    unsafe {
        checked(CreatePipe(&mut read, &mut write, &sa, 0))?;
        let read = owned(read)?;
        let write = owned(write)?;
        let parent = if parent_reads {
            read.as_raw_handle()
        } else {
            write.as_raw_handle()
        };
        checked(SetHandleInformation(parent, HANDLE_FLAG_INHERIT, 0))?;
        Ok((read, write))
    }
}
struct Attributes {
    allocation: Vec<usize>,
    initialized: bool,
}
impl Attributes {
    fn new() -> Result<Self> {
        let mut size = 0;
        unsafe {
            InitializeProcThreadAttributeList(null_mut(), 2, 0, &mut size);
        }
        if size == 0 {
            return Err("attribute_size_failed".into());
        }
        let mut a = Self {
            allocation: vec![0; size.div_ceil(std::mem::size_of::<usize>())],
            initialized: false,
        };
        unsafe {
            checked(InitializeProcThreadAttributeList(a.ptr(), 2, 0, &mut size))?;
        }
        a.initialized = true;
        Ok(a)
    }
    fn ptr(&mut self) -> LPPROC_THREAD_ATTRIBUTE_LIST {
        self.allocation.as_mut_ptr().cast()
    }
}
impl Drop for Attributes {
    fn drop(&mut self) {
        if self.initialized {
            unsafe {
                DeleteProcThreadAttributeList(self.ptr());
            }
        }
    }
}

fn quote(arg: &str) -> String {
    let mut result = String::from("\"");
    let mut slashes = 0;
    for c in arg.chars() {
        if c == '\\' {
            slashes += 1;
            continue;
        }
        result.extend(std::iter::repeat_n(
            '\\',
            if c == '"' { slashes * 2 + 1 } else { slashes },
        ));
        result.push(c);
        slashes = 0;
    }
    result.extend(std::iter::repeat_n('\\', slashes * 2));
    result.push('"');
    result
}

impl OwnedProcess {
    pub fn spawn(exe: &Path, args: &[String], cwd: &Path) -> Result<Self> {
        let exe = crate::request::resolve(exe)?;
        let cwd = crate::request::resolve(cwd)?;
        let (child_in, parent_in) = pipe(false)?;
        let (parent_out, child_out) = pipe(true)?;
        let (parent_err, child_err) = pipe(true)?;
        // SAFETY: all structures initialized, handle/attribute buffers outlive CreateProcessW.
        unsafe {
            let job = owned(CreateJobObjectW(null(), null()))?;
            let mut limits: JOBOBJECT_EXTENDED_LIMIT_INFORMATION = std::mem::zeroed();
            limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
            checked(SetInformationJobObject(
                job.as_raw_handle(),
                JobObjectExtendedLimitInformation,
                (&limits as *const JOBOBJECT_EXTENDED_LIMIT_INFORMATION).cast(),
                std::mem::size_of_val(&limits) as u32,
            ))?;
            let mut attributes = Attributes::new()?;
            let jobs = [job.as_raw_handle()];
            let handles = [
                child_in.as_raw_handle(),
                child_out.as_raw_handle(),
                child_err.as_raw_handle(),
            ];
            checked(UpdateProcThreadAttribute(
                attributes.ptr(),
                0,
                PROC_THREAD_ATTRIBUTE_JOB_LIST as usize,
                jobs.as_ptr().cast(),
                std::mem::size_of_val(&jobs),
                null_mut(),
                null(),
            ))?;
            checked(UpdateProcThreadAttribute(
                attributes.ptr(),
                0,
                PROC_THREAD_ATTRIBUTE_HANDLE_LIST as usize,
                handles.as_ptr().cast(),
                std::mem::size_of_val(&handles),
                null_mut(),
                null(),
            ))?;
            let mut startup: STARTUPINFOEXW = std::mem::zeroed();
            startup.StartupInfo.cb = std::mem::size_of_val(&startup) as u32;
            startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES;
            startup.StartupInfo.hStdInput = handles[0];
            startup.StartupInfo.hStdOutput = handles[1];
            startup.StartupInfo.hStdError = handles[2];
            startup.lpAttributeList = attributes.ptr();
            let exe_w = wide(exe.as_os_str());
            let cwd_w = wide(cwd.as_os_str());
            let mut command = quote(&exe.to_string_lossy());
            for arg in args {
                if arg.contains('\0') {
                    return Err("invalid_argument".into());
                }
                command.push(' ');
                command.push_str(&quote(arg));
            }
            let mut command_w = wide(OsStr::new(&command));
            let mut info: PROCESS_INFORMATION = std::mem::zeroed();
            checked(CreateProcessW(
                exe_w.as_ptr(),
                command_w.as_mut_ptr(),
                null(),
                null(),
                1,
                EXTENDED_STARTUPINFO_PRESENT | DETACHED_PROCESS,
                null(),
                cwd_w.as_ptr(),
                &startup.StartupInfo,
                &mut info,
            ))?;
            let process = owned(info.hProcess)?;
            let _thread = owned(info.hThread)?;
            drop(child_in);
            drop(child_out);
            drop(child_err);
            let (tx, rx) = mpsc::sync_channel(128);
            let (err_tx, err_rx) = mpsc::sync_channel(32);
            let total = Arc::new(AtomicUsize::new(0));
            let streams: [Shared; 2] = Default::default();
            let readers = vec![
                capture::reader(
                    File::from(parent_out),
                    false,
                    tx,
                    total.clone(),
                    streams[0].clone(),
                ),
                capture::reader(
                    File::from(parent_err),
                    true,
                    err_tx,
                    total,
                    streams[1].clone(),
                ),
            ];
            // Only this thread owns stdin. One outstanding write is permitted; the
            // session waits on completion while continuing to poll its stop limits.
            let (input, outgoing) = mpsc::sync_channel::<Vec<u8>>(1);
            let (finished, written) = mpsc::sync_channel(1);
            let writer = thread::spawn(move || {
                let mut file = File::from(parent_in);
                while let Ok(bytes) = outgoing.recv() {
                    let result = file
                        .write_all(&bytes)
                        .map_err(|_| "pipe_write_failed".into());
                    let failed = result.is_err();
                    if finished.send(result).is_err() || failed {
                        break;
                    }
                }
            });
            Ok(Self {
                job,
                process,
                input: Some(input),
                written,
                writer,
                write_pending: false,
                incoming: rx,
                stderr: err_rx,
                readers,
                streams,
                pid: info.dwProcessId,
            })
        }
    }
    pub fn stream_error(&self) -> Option<&'static str> {
        self.streams.iter().find_map(|s| s.lock().unwrap().error())
    }
    pub fn line_consumed(&self) {
        self.streams[0].lock().unwrap().line_consumed();
    }
    pub fn capture(&self) -> capture::Capture {
        let stdout = self.streams[0].lock().unwrap().summary();
        let stderr = self.streams[1].lock().unwrap().summary();
        let drain_complete = self.readers.is_empty()
            && stdout.eof
            && stderr.eof
            && stdout.read_error.is_none()
            && stderr.read_error.is_none();
        capture::Capture {
            stdout,
            stderr,
            drain_complete,
        }
    }
    pub fn chunks(&self) -> Vec<(capture::Stream, capture::Chunk)> {
        self.streams
            .iter()
            .enumerate()
            .flat_map(|(i, s)| {
                s.lock().unwrap().chunks.clone().into_iter().map(move |c| {
                    (
                        if i == 0 {
                            capture::Stream::Stdout
                        } else {
                            capture::Stream::Stderr
                        },
                        c,
                    )
                })
            })
            .collect()
    }
    pub fn drain_until(&mut self, deadline: Instant) -> bool {
        while !self.readers.iter().all(|r| r.is_finished()) && Instant::now() < deadline {
            thread::sleep(Duration::from_millis(2));
        }
        let mut pending = Vec::new();
        for reader in self.readers.drain(..) {
            if reader.is_finished() {
                let _ = reader.join();
            } else {
                pending.push(reader);
            }
        }
        self.readers = pending;
        self.readers.is_empty()
    }
    fn cancel_readers(&self) {
        for reader in &self.readers {
            unsafe {
                windows_sys::Win32::System::IO::CancelSynchronousIo(reader.as_raw_handle());
            }
        }
    }
    pub fn send(&mut self, value: &serde_json::Value) -> Result<()> {
        self.send_until(value, Instant::now() + Duration::from_secs(10), None)
    }
    pub fn send_until(
        &mut self,
        value: &serde_json::Value,
        deadline: Instant,
        control: Option<&AtomicU8>,
    ) -> Result<()> {
        let input = self.input.as_ref().ok_or("pipe_closed")?;
        // An interrupted write has uncertain delivery. Never queue a retry or
        // another message behind it; teardown releases the pipe via job death.
        if self.write_pending {
            return Err("pipe_write_pending".into());
        }
        let mut bytes = serde_json::to_vec(value).map_err(|_| "protocol_error")?;
        bytes.push(b'\n');
        let check = || {
            match control.map(|c| c.load(Ordering::SeqCst)).unwrap_or(0) {
                0 => {}
                1 => return Err("user_cancel".to_string()),
                _ => return Err("invalid_control".to_string()),
            }
            if Instant::now() >= deadline {
                return Err("deadline".into());
            }
            Ok(())
        };
        check()?;
        input.try_send(bytes).map_err(|_| "pipe_write_failed")?;
        self.write_pending = true;
        loop {
            check()?;
            match self.written.recv_timeout(
                Duration::from_millis(5).min(deadline.saturating_duration_since(Instant::now())),
            ) {
                Ok(result) => {
                    self.write_pending = false;
                    return result;
                }
                Err(mpsc::RecvTimeoutError::Timeout) => {}
                Err(mpsc::RecvTimeoutError::Disconnected) => return Err("pipe_write_failed".into()),
            }
        }
    }
    pub fn active(&self) -> Result<u32> {
        Ok(self.accounting()?.ActiveProcesses)
    }
    pub fn created_processes(&self) -> Result<u32> {
        Ok(self.accounting()?.TotalProcesses)
    }
    /// Bounded diagnostic snapshot of this held job, never a historical PID action.
    pub fn process_ids(&self) -> Result<Vec<u32>> {
        #[repr(C)]
        struct ProcessIds {
            assigned: u32,
            listed: u32,
            ids: [usize; 64],
        }
        let mut list = ProcessIds {
            assigned: 0,
            listed: 0,
            ids: [0; 64],
        };
        unsafe {
            checked(QueryInformationJobObject(
                self.job.as_raw_handle(),
                JobObjectBasicProcessIdList,
                (&mut list as *mut ProcessIds).cast(),
                std::mem::size_of_val(&list) as u32,
                null_mut(),
            ))?;
        }
        if list.assigned != list.listed || list.listed > 64 {
            return Err("process_inventory_incomplete".into());
        }
        Ok(list.ids[..list.listed as usize]
            .iter()
            .map(|pid| *pid as u32)
            .collect())
    }
    fn accounting(&self) -> Result<JOBOBJECT_BASIC_ACCOUNTING_INFORMATION> {
        let mut info: JOBOBJECT_BASIC_ACCOUNTING_INFORMATION = unsafe { std::mem::zeroed() };
        unsafe {
            checked(QueryInformationJobObject(
                self.job.as_raw_handle(),
                JobObjectBasicAccountingInformation,
                (&mut info as *mut JOBOBJECT_BASIC_ACCOUNTING_INFORMATION).cast(),
                std::mem::size_of_val(&info) as u32,
                null_mut(),
            ))?;
        }
        Ok(info)
    }
    /// Includes exited descendants, so a short-lived integration cannot disappear
    /// from the no-child preflight observation.
    pub fn only_worker_started(&self) -> Result<bool> {
        let (total, active) = self.process_counts()?;
        Ok(total == 1 && active == 1)
    }
    /// Both counts from the same held-job accounting query used by the guard.
    pub(crate) fn process_counts(&self) -> Result<(u32, u32)> {
        let info = self.accounting()?;
        Ok((info.TotalProcesses, info.ActiveProcesses))
    }
    pub fn exit_code(&self) -> Option<u32> {
        unsafe {
            if WaitForSingleObject(self.process.as_raw_handle(), 0) != WAIT_OBJECT_0 {
                return None;
            }
            let mut code = 0;
            if GetExitCodeProcess(self.process.as_raw_handle(), &mut code) == 0 {
                None
            } else {
                Some(code)
            }
        }
    }
    pub fn stop(&mut self, bound: Duration) -> bool {
        self.input.take();
        unsafe {
            TerminateJobObject(self.job.as_raw_handle(), 1);
        }
        let deadline = Instant::now() + bound;
        let stopped = self.wait_stopped(bound);
        if !self.drain_until(deadline) {
            self.cancel_readers();
            self.drain_until(deadline);
        }
        stopped && self.readers.is_empty()
    }
    pub fn close_input(&mut self) {
        self.input.take();
    }
    pub fn wait_stopped(&self, bound: Duration) -> bool {
        let deadline = Instant::now() + bound;
        loop {
            if self.exit_code().is_some() && self.active() == Ok(0) && self.writer.is_finished() {
                return true;
            }
            if Instant::now() >= deadline {
                return false;
            }
            thread::sleep(Duration::from_millis(5));
        }
    }
}
impl Drop for OwnedProcess {
    fn drop(&mut self) {
        self.cancel_readers();
        self.input.take();
        unsafe {
            TerminateJobObject(self.job.as_raw_handle(), 1);
        }
    }
}

#[cfg(test)]
#[path = "../tests/support/query_handle.rs"]
mod query_handle;
#[cfg(test)]
pub(crate) use query_handle::without_query;
