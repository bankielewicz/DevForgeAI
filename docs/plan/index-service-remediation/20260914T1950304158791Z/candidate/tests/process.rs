//! Real CLI/daemon child processes using exclusively temporary fixture roots.
use serde_json::{Value, json};
use std::{
    fs,
    path::Path,
    process::Command,
    thread,
    time::{Duration, Instant},
};
use tempfile::tempdir;

fn cli(data: &Path, args: &[&str]) -> (i32, Value) {
    use std::process::Stdio;
    eprintln!("CLI begin {:?} in {}", args, data.display());
    let output = tempfile::NamedTempFile::new().unwrap();
    let errors = tempfile::NamedTempFile::new().unwrap();
    let mut child = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .env("DEVFORGEAI_INDEX_DATA", data)
        .args(args)
        .arg("--json")
        .stdin(Stdio::null())
        .stdout(output.reopen().unwrap())
        .stderr(errors.reopen().unwrap())
        .spawn()
        .unwrap();
    let started = Instant::now();
    let status = loop {
        if let Some(status) = child.try_wait().unwrap() {
            break status;
        }
        if started.elapsed() > Duration::from_secs(20) {
            let _ = child.kill();
            let _ = child.wait();
            panic!(
                "CLI child exceeded test deadline: {:?}; stdout={}; stderr={}",
                args,
                fs::read_to_string(output.path()).unwrap(),
                fs::read_to_string(errors.path()).unwrap()
            );
        }
        thread::sleep(Duration::from_millis(10));
    };
    let bytes = fs::read(output.path()).unwrap();
    let value = serde_json::from_slice(&bytes).unwrap_or_else(|error| {
        panic!(
            "{error}: stdout={} stderr={}",
            String::from_utf8_lossy(&bytes),
            fs::read_to_string(errors.path()).unwrap()
        )
    });
    eprintln!("CLI end {:?}: {}", args, status);
    (status.code().unwrap(), value)
}
struct Cleanup<'a>(&'a Path);
impl Drop for Cleanup<'_> {
    fn drop(&mut self) {
        let _ = cli(self.0, &["daemon", "stop"]);
    }
}

#[test]
fn management_errors_configuration_and_aliases_preserve_boundaries() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    let _cleanup = Cleanup(data.path());
    let missing = "550e8400-e29b-41d4-a716-446655440000";
    assert_eq!(
        cli(data.path(), &["daemon", "stop"]).1["data"]["already_stopped"],
        true
    );
    assert_eq!(cli(data.path(), &["project", "list"]).0, 3);
    assert_eq!(
        cli(data.path(), &["daemon", "run", "--environment", "other"]).0,
        2
    );
    assert_eq!(cli(data.path(), &["tray", "--environment", "other"]).0, 2);
    assert_eq!(
        cli(
            data.path(),
            &["bridge", "request", "--environment", "other"]
        )
        .0,
        2
    );
    assert_eq!(
        cli(
            data.path(),
            &["daemon", "status", "--environment", "missing"]
        )
        .0,
        6
    );
    assert_eq!(
        cli(
            data.path(),
            &["daemon", "start", "--environment", "missing"]
        )
        .0,
        6
    );
    assert_eq!(
        cli(data.path(), &["environment", "list"]).1["data"]["local"],
        true
    );
    assert_eq!(
        cli(data.path(), &["environment", "remove", "--alias", "local"]).0,
        2
    );
    assert_eq!(
        cli(
            data.path(),
            &["environment", "remove", "--alias", "missing"]
        )
        .0,
        6
    );
    #[cfg(windows)]
    {
        for (alias, distribution, user, executable) in [
            ("local", "Fixture", "user", "/bin/devforgeai"),
            ("", "Fixture", "user", "/bin/devforgeai"),
            ("fixture", " ", "user", "/bin/devforgeai"),
            ("fixture", "Fixture", " ", "/bin/devforgeai"),
            ("fixture", "Fixture", "user", "relative"),
        ] {
            assert_eq!(
                cli(
                    data.path(),
                    &[
                        "environment",
                        "add-wsl",
                        "--alias",
                        alias,
                        "--distribution",
                        distribution,
                        "--user",
                        user,
                        "--cli",
                        executable
                    ]
                )
                .0,
                2
            );
        }
        // Registration is fixture metadata only: never dispatch this alias to WSL.
        assert_eq!(
            cli(
                data.path(),
                &[
                    "environment",
                    "add-wsl",
                    "--alias",
                    "fixture",
                    "--distribution",
                    "Not a real distribution",
                    "--user",
                    "fixture user",
                    "--cli",
                    "/fixture path/devforgeai"
                ]
            )
            .0,
            0
        );
        let listed = cli(data.path(), &["environment", "list"]);
        assert_eq!(
            listed.1["data"]["wsl"]["fixture"]["cli"],
            "/fixture path/devforgeai"
        );
        assert_eq!(
            cli(
                data.path(),
                &["environment", "remove", "--alias", "fixture"]
            )
            .0,
            0
        );
        assert_eq!(
            cli(data.path(), &["environment", "list"]).1["data"]["wsl"],
            json!({})
        );
        let prefs = cli(data.path(), &["tray", "settings", "show"]);
        assert_eq!(prefs.0, 0);
        assert_eq!(
            prefs.1["data"],
            json!({"launch_at_sign_in":false,"start_local_daemon":false})
        );
        // None of these fixture-only settings commands requests a Windows Run-key change.
        assert_eq!(
            cli(
                data.path(),
                &["tray", "settings", "set", "--start-local-daemon", "false"]
            )
            .0,
            0
        );
    }
    fs::write(data.path().join("environments.json"), b"invalid json").unwrap();
    assert_eq!(cli(data.path(), &["environment", "list"]).0, 2);
    fs::write(data.path().join("environments.json"), b"{}").unwrap();
    assert_eq!(cli(data.path(), &["daemon", "start"]).0, 0);
    assert_eq!(
        cli(data.path(), &["daemon", "start"]).1["data"]["already_running"],
        true
    );
    assert_eq!(
        cli(data.path(), &["daemon", "diagnostics"]).1["data"]["source_contents_logged"],
        false
    );
    assert_eq!(cli(data.path(), &["daemon", "pause"]).0, 0);
    let added = cli(
        data.path(),
        &[
            "project",
            "add",
            "--root",
            source.path().to_str().unwrap(),
            "--name",
            "Config",
        ],
    );
    let project = added.1["data"]["project_id"].as_str().unwrap();
    assert_eq!(
        cli(data.path(), &["project", "list"]).1["data"]["projects"][0]["id"],
        project
    );
    assert_eq!(
        cli(data.path(), &["index", "status", "--project", project]).1["data"]["current_generation"],
        Value::Null
    );
    let config = data.path().join("fixture-config.json");
    let update = [
        "project",
        "update",
        "--project",
        project,
        "--config-file",
        config.to_str().unwrap(),
    ];
    assert_eq!(cli(data.path(), &update).0, 2);
    fs::write(&config, b"{").unwrap();
    assert_eq!(cli(data.path(), &update).0, 2);
    fs::write(&config, vec![b' '; 1024 * 1024 + 1]).unwrap();
    assert_eq!(cli(data.path(), &update).0, 2);
    fs::write(
        &config,
        br#"{"exclusions":["*.secret"],"max_file_bytes":1024}"#,
    )
    .unwrap();
    assert_eq!(cli(data.path(), &update).0, 0);
    assert_eq!(
        cli(data.path(), &["project", "list"]).1["data"]["projects"][0]["config"]["max_file_bytes"],
        1024
    );
    let queued = cli(data.path(), &["index", "rescan", "--project", project]);
    let job = queued.1["data"]["job_id"].as_str().unwrap();
    assert_eq!(
        cli(data.path(), &["job", "cancel", "--job", job]).1["data"]["outcome"],
        "cancelled"
    );
    assert_eq!(cli(data.path(), &["job", "status", "--job", job]).0, 0);
    assert_eq!(cli(data.path(), &["job", "status", "--job", missing]).0, 6);
    let timed = cli(
        data.path(),
        &[
            "index",
            "rescan",
            "--project",
            project,
            "--wait",
            "--timeout-ms",
            "200",
        ],
    );
    assert_eq!(timed.0, 7);
    assert_eq!(
        cli(data.path(), &["index", "status", "--project", project]).1["data"]["jobs"][0]["outcome"],
        "queued",
        "deadline must not cancel queued work"
    );
}

#[test]
fn waiting_for_cancelled_or_failed_jobs_uses_exit_eleven() {
    for cancel in [true, false] {
        let data = tempdir().unwrap();
        let parent = tempdir().unwrap();
        let source = parent.path().join("project");
        fs::create_dir(&source).unwrap();
        let _cleanup = Cleanup(data.path());
        assert_eq!(cli(data.path(), &["daemon", "start"]).0, 0);
        assert_eq!(cli(data.path(), &["daemon", "pause"]).0, 0);
        let added = cli(
            data.path(),
            &[
                "project",
                "add",
                "--root",
                source.to_str().unwrap(),
                "--name",
                "Wait",
            ],
        );
        let project = added.1["data"]["project_id"].as_str().unwrap().to_owned();
        let wait_data = data.path().to_owned();
        let wait_project = project.clone();
        let waiting = thread::spawn(move || {
            cli(
                &wait_data,
                &["index", "reindex", "--project", &wait_project, "--wait"],
            )
        });
        let deadline = Instant::now() + Duration::from_secs(5);
        let job = loop {
            let status = cli(data.path(), &["index", "status", "--project", &project]);
            if let Some(id) = status.1["data"]["jobs"][0]["id"].as_str() {
                break id.to_owned();
            }
            assert!(Instant::now() < deadline);
            thread::sleep(Duration::from_millis(10));
        };
        if cancel {
            assert_eq!(cli(data.path(), &["job", "cancel", "--job", &job]).0, 0);
        } else {
            fs::rename(&source, parent.path().join("moved")).unwrap();
            assert_eq!(cli(data.path(), &["daemon", "resume"]).0, 0);
        }
        let result = waiting.join().unwrap();
        assert_eq!(result.0, 11, "{result:?}");
        assert_eq!(
            result.1["error"]["code"],
            if cancel {
                "JOB_CANCELLED"
            } else {
                "JOB_FAILED"
            }
        );
        assert_eq!(cli(data.path(), &["job", "status", "--job", &job]).0, 0);
    }
}

#[test]
fn bridge_input_validation_and_foreground_daemon_are_terminal_accessible() {
    use std::io::Write;
    use std::process::Stdio;
    let data = tempdir().unwrap();
    let _cleanup = Cleanup(data.path());
    let request = json!({"protocol_version":1,"request_id":"550e8400-e29b-41d4-a716-446655440000","operation":"daemon.status","params":{},"timeout_ms":1000});
    for (bytes, bootstrap, expected) in [
        (b"invalid".to_vec(), false, 2),
        (serde_json::to_vec(&request).unwrap(), true, 2),
        (serde_json::to_vec(&request).unwrap(), false, 3),
    ] {
        let mut command = Command::new(env!("CARGO_BIN_EXE_devforgeai"));
        command
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["bridge", "request"]);
        if bootstrap {
            command.arg("--bootstrap");
        }
        let mut child = command
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .spawn()
            .unwrap();
        child.stdin.take().unwrap().write_all(&bytes).unwrap();
        let output = child.wait_with_output().unwrap();
        assert_eq!(output.status.code(), Some(expected));
        let envelope: Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(envelope["ok"], false);
    }
    let mut handshake = request.clone();
    handshake["operation"] = json!("daemon.handshake");
    let mut bootstrap = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .env("DEVFORGEAI_INDEX_DATA", data.path())
        .args(["bridge", "request", "--bootstrap"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    bootstrap
        .stdin
        .take()
        .unwrap()
        .write_all(&serde_json::to_vec(&handshake).unwrap())
        .unwrap();
    let output = bootstrap.wait_with_output().unwrap();
    assert!(output.status.success());
    assert_eq!(
        serde_json::from_slice::<Value>(&output.stdout).unwrap()["data"]["daemon_state"],
        "running"
    );
    assert_eq!(cli(data.path(), &["daemon", "stop"]).0, 0);
    let mut foreground = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .env("DEVFORGEAI_INDEX_DATA", data.path())
        .args(["daemon", "run", "--json"])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        if cli(data.path(), &["daemon", "status"]).1["data"]["daemon_state"] == "running" {
            break;
        }
        if Instant::now() >= deadline {
            let _ = foreground.kill();
            panic!("foreground daemon did not start");
        }
        thread::sleep(Duration::from_millis(20));
    }
    assert_eq!(cli(data.path(), &["daemon", "stop"]).0, 0);
    let output = foreground.wait_with_output().unwrap();
    assert_eq!(output.status.code(), Some(0));
    assert_eq!(
        serde_json::from_slice::<Value>(&output.stdout).unwrap()["data"]["daemon_state"],
        "stopped"
    );
}

#[cfg(windows)]
#[test]
fn bootstrap_reports_child_exit_and_timeout_without_force_kill() {
    let fixture = tempdir().unwrap();
    let data = tempdir().unwrap();
    let daemon = fixture.path().join("devforgeai-indexd.exe");
    let compiled = Command::new("rustc")
        .args(["--edition=2024", "tests/support/bootstrap_peer.rs", "-o"])
        .arg(&daemon)
        .output()
        .unwrap();
    assert!(
        compiled.status.success(),
        "{}",
        String::from_utf8_lossy(&compiled.stderr)
    );
    let executable = fixture.path().join("devforgeai.exe");
    fs::copy(env!("CARGO_BIN_EXE_devforgeai"), &executable).unwrap();
    for (mode, expected) in [("exit", 3), ("delay", 7)] {
        fs::write(fixture.path().join("mode"), mode).unwrap();
        let output = Command::new(&executable)
            .env("DEVFORGEAI_INDEX_DATA", data.path())
            .args(["daemon", "start", "--json", "--timeout-ms", "200"])
            .output()
            .unwrap();
        assert_eq!(
            output.status.code(),
            Some(expected),
            "{}",
            String::from_utf8_lossy(&output.stdout)
        );
        let response: Value = serde_json::from_slice(&output.stdout).unwrap();
        if mode == "delay" {
            assert!(fixture.path().join("started").exists());
            assert!(!fixture.path().join("finished").exists());
            let deadline = Instant::now() + Duration::from_secs(2);
            while !fixture.path().join("finished").exists() {
                assert!(Instant::now() < deadline);
                thread::sleep(Duration::from_millis(10));
            }
            assert!(
                response["error"]["message"]
                    .as_str()
                    .unwrap()
                    .contains("not force-killed")
            );
        } else {
            assert!(
                response["error"]["message"]
                    .as_str()
                    .unwrap()
                    .contains("23")
            );
        }
    }
}

#[test]
fn detached_daemon_does_not_keep_cli_stdout_pipe_open() {
    use std::{io::Read, process::Stdio, sync::mpsc};
    let data = tempdir().unwrap();
    let _cleanup = Cleanup(data.path());
    let mut child = Command::new(env!("CARGO_BIN_EXE_devforgeai"))
        .env("DEVFORGEAI_INDEX_DATA", data.path())
        .args(["daemon", "start", "--json"])
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .unwrap();
    let mut pipe = child.stdout.take().unwrap();
    let (send, receive) = mpsc::channel();
    let reader = thread::spawn(move || {
        let mut bytes = Vec::new();
        pipe.read_to_end(&mut bytes).unwrap();
        let _ = send.send(bytes);
    });
    let started = Instant::now();
    let status = loop {
        if let Some(status) = child.try_wait().unwrap() {
            break status;
        }
        assert!(started.elapsed() < Duration::from_secs(15));
        thread::sleep(Duration::from_millis(10));
    };
    assert!(status.success());
    let output = receive.recv_timeout(Duration::from_secs(2));
    let stop = cli(data.path(), &["daemon", "stop"]);
    assert_eq!(stop.0, 0);
    reader.join().unwrap();
    assert!(
        output.is_ok(),
        "detached daemon inherited and retained the CLI stdout pipe"
    );
    let value: Value = serde_json::from_slice(&output.unwrap()).unwrap();
    assert_eq!(value["ok"], true);
}

#[test]
fn simultaneous_starts_and_process_level_index_lifecycle() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    let _cleanup = Cleanup(data.path());
    let first = data.path().to_owned();
    let second = first.clone();
    let a = thread::spawn(move || cli(&first, &["daemon", "start"]));
    let b = thread::spawn(move || cli(&second, &["daemon", "start"]));
    let a = a.join().unwrap();
    let b = b.join().unwrap();
    assert_eq!(a.0, 0, "{:?}", a.1);
    assert_eq!(b.0, 0, "{:?}", b.1);
    assert_eq!(a.1["environment_id"], b.1["environment_id"]);
    assert_eq!(cli(data.path(), &["daemon", "pause"]).0, 0);
    fs::write(
        source.path().join("module.py"),
        "def alpha():\n    return 1\n",
    )
    .unwrap();
    let root = source.path().to_str().unwrap();
    let add = cli(
        data.path(),
        &[
            "project",
            "add",
            "--root",
            root,
            "--name",
            "Fixture Ω spaces",
        ],
    );
    assert_eq!(add.0, 0, "{:?}", add.1);
    let project = add.1["data"]["project_id"].as_str().unwrap();
    let queued = cli(data.path(), &["index", "rescan", "--project", project]);
    assert_eq!(queued.0, 0);
    let job = queued.1["data"]["job_id"].as_str().unwrap();
    assert_eq!(
        cli(data.path(), &["job", "status", "--job", job]).1["data"]["outcome"],
        "queued"
    );
    assert_eq!(cli(data.path(), &["daemon", "resume"]).0, 0);
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        let status = cli(data.path(), &["job", "status", "--job", job]);
        if status.1["data"]["outcome"] == "succeeded" {
            break;
        }
        assert!(Instant::now() < deadline, "{:?}", status.1);
        thread::sleep(Duration::from_millis(20));
    }
    assert_eq!(
        cli(
            data.path(),
            &["index", "reindex", "--project", project, "--wait"]
        )
        .0,
        0
    );
    let before = fs::read(source.path().join("module.py")).unwrap();
    assert_eq!(
        cli(
            data.path(),
            &["project", "remove", "--project", project, "--yes"]
        )
        .0,
        0
    );
    assert_eq!(fs::read(source.path().join("module.py")).unwrap(), before);
    assert_eq!(cli(data.path(), &["daemon", "stop"]).0, 0);
    assert_eq!(
        cli(data.path(), &["daemon", "status"]).1["data"]["daemon_state"],
        "stopped"
    );
}

#[test]
fn corrupt_storage_can_be_rebuilt_only_with_exact_project_confirmation() {
    let data = tempdir().unwrap();
    let source = tempdir().unwrap();
    let _cleanup = Cleanup(data.path());
    assert_eq!(cli(data.path(), &["daemon", "start"]).0, 0);
    assert_eq!(cli(data.path(), &["daemon", "pause"]).0, 0);
    let add = cli(
        data.path(),
        &[
            "project",
            "add",
            "--root",
            source.path().to_str().unwrap(),
            "--name",
            "Recovery",
        ],
    );
    let project = add.1["data"]["project_id"].as_str().unwrap();
    assert_eq!(cli(data.path(), &["daemon", "stop"]).0, 0);
    fs::write(data.path().join("index.sqlite3"), b"retained corrupt bytes").unwrap();
    assert_eq!(cli(data.path(), &["daemon", "start"]).0, 0);
    assert_eq!(
        cli(data.path(), &["daemon", "status"]).1["data"]["degraded"],
        true
    );
    assert_ne!(
        cli(
            data.path(),
            &[
                "index",
                "rebuild",
                "--project",
                project,
                "--yes",
                "--affected-projects",
                "00000000-0000-0000-0000-000000000000"
            ]
        )
        .0,
        0
    );
    assert_eq!(
        fs::read(data.path().join("index.sqlite3")).unwrap(),
        b"retained corrupt bytes"
    );
    let rebuilt = cli(
        data.path(),
        &[
            "index",
            "rebuild",
            "--project",
            project,
            "--yes",
            "--affected-projects",
            project,
        ],
    );
    assert_eq!(rebuilt.0, 0, "{:?}", rebuilt.1);
    let quarantine = Path::new(rebuilt.1["data"]["quarantine"].as_str().unwrap());
    assert_eq!(
        fs::read(quarantine.join("index.sqlite3")).unwrap(),
        b"retained corrupt bytes"
    );
    assert_eq!(
        cli(data.path(), &["daemon", "status"]).1["data"]["degraded"],
        json!(false)
    );
}
