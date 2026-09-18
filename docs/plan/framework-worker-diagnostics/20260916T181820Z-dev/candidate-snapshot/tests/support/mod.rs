#![allow(dead_code)] // Shared fixture API is consumed by different integration test binaries.
use devforgeai_codex_worker_probe::request::{self, Request};
use serde_json::json;
use std::{fs, path::PathBuf};
pub struct TestRoot {
    dir: Option<tempfile::TempDir>,
    retained: bool,
}
impl TestRoot {
    fn new(case: &str) -> Self {
        if let Some(base) = std::env::var_os("WF_TEST_EVIDENCE") {
            fs::create_dir_all(&base).unwrap();
            Self {
                dir: Some(
                    tempfile::Builder::new()
                        .prefix(case)
                        .tempdir_in(base)
                        .unwrap(),
                ),
                retained: true,
            }
        } else {
            Self {
                dir: Some(tempfile::tempdir().unwrap()),
                retained: false,
            }
        }
    }
    pub fn path(&self) -> &std::path::Path {
        self.dir.as_ref().unwrap().path()
    }
}
impl Drop for TestRoot {
    fn drop(&mut self) {
        if self.retained {
            let _ = self.dir.take().unwrap().keep();
        }
    }
}
pub struct Fixture {
    pub root: TestRoot,
    pub request: Request,
    pub input: PathBuf,
}
impl Fixture {
    pub fn new(case: &str) -> Self {
        let root = TestRoot::new(case);
        let checkout = root.path().join("fixture");
        fs::create_dir(&checkout).unwrap();
        fs::write(checkout.join("task.json"), request::TASK).unwrap();
        fs::write(checkout.join("peer-case.txt"), format!("{case}\n")).unwrap();
        let exe = PathBuf::from(env!("CARGO_BIN_EXE_protocol-peer"));
        let value = json!({"schema_version":1,"project_id":"p","checkout_id":"c","work_id":"w","run_id":"r",
            "candidate_sha256":request::digest(request::TASK),"checkout_root":checkout,"run_dir":root.path().join("run"),
            "worker_executable":exe,"worker_sha256":request::hash_file(&exe).unwrap(),"adapter":"peer","scenario":"complete","profile":null});
        let input = root.path().join("input.json");
        fs::write(&input, value.to_string()).unwrap();
        let request = request::validate(&input).unwrap();
        Self {
            root,
            request,
            input,
        }
    }
    pub fn run(&self) -> (i32, serde_json::Value) {
        let options = devforgeai_codex_worker_probe::runner::Options {
            total: std::time::Duration::from_secs(3),
            rpc: std::time::Duration::from_millis(500),
            grace: std::time::Duration::from_millis(100),
            ..Default::default()
        };
        devforgeai_codex_worker_probe::runner::run(&self.input, options, &mut |_| {}).unwrap()
    }
    pub fn trace(&self) -> Vec<serde_json::Value> {
        fs::read_to_string(self.root.path().join("peer-trace.jsonl"))
            .unwrap()
            .lines()
            .map(|s| serde_json::from_str(s).unwrap())
            .collect()
    }
}
