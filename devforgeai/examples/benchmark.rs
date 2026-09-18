//! Reproducible development benchmark, not a performance acceptance authority.
#[path = "../fixtures/generator.rs"]
mod generator;
use devforgeai_index::{protocol::Request, service::Service};
use serde_json::{Value, json};
use std::{
    sync::{
        Arc,
        atomic::{AtomicBool, Ordering},
    },
    thread,
    time::{Duration, Instant},
};
fn request(operation: &str, params: Value) -> Request {
    Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: operation.into(),
        timeout_ms: 120000,
        params,
    }
}
fn wait(service: &Service, job: &str) -> Value {
    let deadline = Instant::now() + Duration::from_secs(240);
    loop {
        let response = service.execute(&request("job.status", json!({"job_id":job})));
        assert!(response.ok, "{response:?}");
        let state = response.data["outcome"].as_str().unwrap();
        if !["queued", "running"].contains(&state) {
            assert_eq!(state, "succeeded", "{response:?}");
            return response.data;
        }
        assert!(Instant::now() < deadline, "benchmark job timeout");
        thread::sleep(Duration::from_millis(10));
    }
}
fn main() {
    eprintln!("Generating deterministic 10,000-file / 100 MiB fixture");
    let source = tempfile::tempdir().unwrap();
    let entries = generator::generate(source.path(), 10000, 100 * 1024 * 1024, 20260913).unwrap();
    let manifest = serde_json::to_vec(&entries).unwrap();
    let manifest_digest = devforgeai_index::index::digest(&manifest);
    if let Some(path) = std::env::args_os().nth(1) {
        std::fs::write(path, &manifest).unwrap();
    }
    let mut repetitions = Vec::new();
    for repetition in 0..3 {
        eprintln!("Repetition {}: preparing baseline", repetition + 1);
        // Regenerate the same baseline; edits in another repetition cannot carry over.
        generator::generate(source.path(), 10000, 100 * 1024 * 1024, 20260913).unwrap();
        let data = tempfile::tempdir().unwrap();
        let service = Arc::new(Service::open(data.path()).unwrap());
        let finished = Arc::new(AtomicBool::new(false));
        let mut readers = Vec::new();
        for _ in 0..4 {
            let service = service.clone();
            let done = finished.clone();
            readers.push(thread::spawn(move || {
                let mut micros = Vec::new();
                while !done.load(Ordering::Acquire) {
                    let started = Instant::now();
                    assert!(service.execute(&request("daemon.status", json!({}))).ok);
                    micros.push(started.elapsed().as_micros());
                    thread::sleep(Duration::from_millis(10));
                }
                micros
            }));
        }
        eprintln!("Repetition {}: cold indexing", repetition + 1);
        let start = Instant::now();
        let added = service.execute(&request(
            "project.add",
            json!({"root":source.path(),"name":"Benchmark"}),
        ));
        assert!(added.ok);
        let project = added.data["project_id"].as_str().unwrap();
        wait(&service, added.data["job_id"].as_str().unwrap());
        let cold_ms = start.elapsed().as_millis();
        eprintln!(
            "Repetition {}: cold {cold_ms} ms; warm indexing",
            repetition + 1
        );
        let start = Instant::now();
        let queued = service.execute(&request("index.rescan", json!({"project_id":project})));
        assert!(queued.ok, "{queued:?}");
        wait(&service, queued.data["job_id"].as_str().unwrap());
        let warm_ms = start.elapsed().as_millis();
        service.execute(&request("daemon.pause", json!({})));
        eprintln!(
            "Repetition {}: warm {warm_ms} ms; edit 100 files",
            repetition + 1
        );
        for entry in entries.iter().take(100) {
            let path = source.path().join(&entry.path);
            let mut bytes = std::fs::read(&path).unwrap();
            let last = bytes.len() - 2;
            bytes[last] = b'y';
            std::fs::write(path, bytes).unwrap();
        }
        let queued = service.execute(&request("index.rescan", json!({"project_id":project})));
        assert!(queued.ok);
        let start = Instant::now();
        service.execute(&request("daemon.resume", json!({})));
        wait(&service, queued.data["job_id"].as_str().unwrap());
        let edit_ms = start.elapsed().as_millis();
        finished.store(true, Ordering::Release);
        let mut latencies: Vec<u128> = readers
            .into_iter()
            .flat_map(|reader| reader.join().unwrap())
            .collect();
        latencies.sort();
        let idle_before = service
            .execute(&request("index.status", json!({"project_id":project})))
            .data;
        thread::sleep(Duration::from_secs(1));
        let idle_after = service
            .execute(&request("index.status", json!({"project_id":project})))
            .data;
        repetitions.push(json!({"repetition":repetition+1,"cold_ms":cold_ms,"warm_ms":warm_ms,"edit_100_ms":edit_ms,"concurrent_status_readers":4,"status_requests":latencies.len(),"status_p50_us":latencies[latencies.len()/2],"status_p95_us":latencies[latencies.len()*95/100],"coverage":idle_after,"idle_generation_unchanged":idle_before["current_generation"]==idle_after["current_generation"]}));
        service.shutdown().unwrap();
        println!("{}", repetitions.last().unwrap());
    }
    println!(
        "{}",
        json!({"seed":20260913,"files":10000,"bytes":100*1024*1024,"fixture_manifest_sha256":manifest_digest,"platform":std::env::consts::OS,"architecture":std::env::consts::ARCH,"logical_processors":thread::available_parallelism().unwrap().get(),"build_mode":if cfg!(debug_assertions){"debug"}else{"release"},"repetitions":repetitions,"cpu_and_peak_memory":"NOT_MEASURED","query_workload":"concurrent daemon.status requests; companion code-query benchmark not selected"})
    );
}
