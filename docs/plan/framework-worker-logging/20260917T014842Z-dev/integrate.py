from pathlib import Path
p=Path(r'C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging')
def edit(name,fn):
    f=p/name; f.write_text(fn(f.read_text()),encoding='utf-8',newline='\n')
edit('src/lib.rs',lambda s:s+'\npub mod capture;\npub mod logging;\n')
edit('src/request.rs',lambda s:s.replace('    pub schema_version: u32,','    pub schema_version: u32,\n    #[serde(default, skip_serializing_if = "Option::is_none")]\n    pub diagnostics_ref: Option<PathBuf>,\n    #[serde(default, skip_serializing_if = "Option::is_none")]\n    pub diagnostics_sha256: Option<String>,',1)
    .replace('impl Request {','impl Request {\n    pub fn native_v2(&self) -> bool { self.schema_version >= 2 && self.adapter != "peer" }')
    .replace('                    2 => {','                    2 | 3 => {')
    .replace('if self.schema_version != 2','if !self.native_v2()')
    .replace('if self.schema_version == 2','if self.native_v2()')
    .replace('r.schema_version == 2 && r.adapter == "codex-0.154.0-stdio"','r.schema_version == 2 && r.adapter == "codex-0.154.0-stdio" || r.schema_version == 3')
    .replace('    r.profile()?;','    r.profile()?;\n    crate::logging::load(&r)?;',1)
    .replace('if r.schema_version == 2','if r.native_v2()'))
for file in ['tests/support/diagnostic_cases.rs','tests/support/final_source_check_cases.rs','tests/support/review_v2_cases.rs']:
    edit(file,lambda s:s.replace('schema_version: 2,','schema_version: 2, diagnostics_ref: None, diagnostics_sha256: None,').replace('schema_version: 1,','schema_version: 1, diagnostics_ref: None, diagnostics_sha256: None,'))
edit('src/process_windows.rs',lambda s:s.replace('use sha2::{Digest, Sha256};','use crate::capture::{self, Shared};').replace('io::{Read, Write}','io::Write')
    .replace('    pub incoming: Receiver<Incoming>,','    pub incoming: Receiver<Incoming>,\n    pub stderr: Receiver<Incoming>,\n    readers: Vec<thread::JoinHandle<()>>,\n    streams: [Shared; 2],')
    .replace(s[s.index('fn reader('):s.index('impl OwnedProcess {')],'')
    .replace('let (tx, rx) = mpsc::sync_channel(32);','let (tx, rx) = mpsc::sync_channel(128);\n            let (err_tx, err_rx) = mpsc::sync_channel(32);')
    .replace('reader(File::from(parent_out), false, tx.clone(), total.clone());\n            reader(File::from(parent_err), true, tx, total);','let streams: [Shared; 2] = Default::default();\n            let readers = vec![\n                capture::reader(File::from(parent_out), false, tx, total.clone(), streams[0].clone()),\n                capture::reader(File::from(parent_err), true, err_tx, total, streams[1].clone()),\n            ];')
    .replace('                incoming: rx,','                incoming: rx, stderr:err_rx, readers, streams,')
    .replace('    pub fn send(&mut self,','    pub fn stream_error(&self)->Option<&\'static str> { self.streams.iter().find_map(|s|s.lock().unwrap().error()) }\n    pub fn capture(&self)->capture::Capture {\n        let stdout=self.streams[0].lock().unwrap().summary();\n        let stderr=self.streams[1].lock().unwrap().summary();\n        let drain_complete=self.readers.is_empty() && stdout.eof && stderr.eof && stdout.read_error.is_none() && stderr.read_error.is_none();\n        capture::Capture {stdout,stderr,drain_complete}\n    }\n    pub fn chunks(&self)->Vec<(capture::Stream,capture::Chunk)> {\n        self.streams.iter().enumerate().flat_map(|(i,s)| s.lock().unwrap().chunks.clone().into_iter().map(move |c|(if i==0 {capture::Stream::Stdout} else {capture::Stream::Stderr},c))).collect()\n    }\n    pub fn drain_until(&mut self, deadline:Instant)->bool {\n        while !self.readers.iter().all(|r|r.is_finished()) && Instant::now()<deadline { thread::sleep(Duration::from_millis(2)); }\n        let mut pending=Vec::new();\n        for reader in self.readers.drain(..) {\n            if reader.is_finished() { let _=reader.join(); } else { pending.push(reader); }\n        }\n        self.readers=pending; self.readers.is_empty()\n    }\n    fn cancel_readers(&self) {\n        for reader in &self.readers { unsafe { windows_sys::Win32::System::IO::CancelSynchronousIo(reader.as_raw_handle()); } }\n    }\n    pub fn send(&mut self,')
    .replace('        self.wait_stopped(bound)','        let deadline=Instant::now()+bound;\n        let stopped=self.wait_stopped(bound);\n        if !self.drain_until(deadline) { self.cancel_readers(); self.drain_until(deadline); }\n        stopped && self.readers.is_empty()')
    .replace('impl Drop for OwnedProcess {\n    fn drop(&mut self) {','impl Drop for OwnedProcess {\n    fn drop(&mut self) {\n        self.cancel_readers();'))
edit('src/protocol.rs',lambda s:s.replace('if r.schema_version == 2','if r.native_v2()')
    .replace('            match self.process.incoming.recv_timeout(','''            if let Some(error)=self.process.stream_error() { return Err(error.into()); }
            while let Ok(Incoming::Stderr{bytes,sha256})=self.process.stderr.try_recv() {
                self.record("worker_event",json!({"stream":"stderr","bytes":bytes,"sha256":sha256,"content":"omitted"}))?;
            }
            match self.process.incoming.recv_timeout(''')
    .replace('        let result = self.rpc_inner(method, params);','        let started=Instant::now();\n        let result = self.rpc_inner(method, params);\n        self.journal.log_rpc(method,started.elapsed(),result.is_err());'))
edit('src/runner.rs',lambda s:s.replace('if r.schema_version == 2','if r.native_v2()').replace('r.schema_version != 2','!r.native_v2()')
    .replace('    Ok(())\n}\n\nfn execute_with_final_check','    crate::logging::load(r)?;\n    Ok(())\n}\n\nfn execute_with_final_check')
    .replace('        // No journal callback','        journal.log_launch(&args, r.native_v2());\n        // No journal callback')
    .replace('            Ok(mut process) => {','            Ok(mut process) => {\n                let mut pre_stop_exit_code=None;')
    .replace('                        reason = e;','                        pre_stop_exit_code=session.process.exit_code();\n                        reason = e;')
    .replace('                        session.interrupt();','                        if pre_stop_exit_code.is_some() { session.process.drain_until(Instant::now()+options.teardown); }\n                        session.interrupt();')
    .replace('                let actual_stopped = process.stop(options.teardown);','                pre_stop_exit_code=pre_stop_exit_code.or_else(||process.exit_code());\n                journal.log_input_closed();\n                let actual_stopped = process.stop(options.teardown);')
    .replace('                match journal.append(\n                    "process_exit",\n                    json!({"worker_exit_code":exit,"tree_stopped":stopped}),\n                ) {','''                let capture=process.capture();
                journal.log_capture(&capture, &process.chunks(), pre_stop_exit_code, exit, actual_stopped);
                match journal.append(
                    "process_exit",
                    json!({"worker_exit_code":exit,"tree_stopped":stopped,"observed_before_stop":pre_stop_exit_code.is_some(),"pre_stop_exit_code":pre_stop_exit_code,"capture":capture}),
                ) {''')
    .replace('    let unchanged = r','    if let Err(_) = journal.finish_diagnostics().and_then(|data|journal.append("worker_event",data)).map(|e|emit(&e)) { reason="evidence_write_failed".into(); }\n    let unchanged = r'))
edit('src/launch_policy.rs',lambda s:s.replace('readonly-no-external-tools-v2','readonly-no-external-tools-v3').replace('schema_version != 2','!(2..=3).contains(&schema_version)'))
