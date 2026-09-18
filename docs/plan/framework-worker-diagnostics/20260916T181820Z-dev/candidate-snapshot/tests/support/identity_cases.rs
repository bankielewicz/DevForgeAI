use super::*;
use crate::request::{digest, resolve};
use std::{
    fs,
    os::windows::fs::symlink_dir,
    path::{Path, PathBuf},
    process::Command,
    sync::atomic::{AtomicU64, Ordering},
};

const ADAPTER: &str = "codex-0.154.0-stdio";
const EXECUTABLE_BYTES: &[u8] = b"synthetic codex executable bytes\n";
static MKLINK_ATTEMPT: AtomicU64 = AtomicU64::new(1);

struct TestTree {
    directory: Option<tempfile::TempDir>,
    reparse_points: Vec<PathBuf>,
    retain: bool,
}

impl TestTree {
    fn new(case: &str) -> Self {
        let base = std::env::var_os("WF_TEST_EVIDENCE")
            .map(PathBuf::from)
            .unwrap_or_else(std::env::temp_dir);
        fs::create_dir_all(&base).expect("create identity test evidence base");
        let directory = tempfile::Builder::new()
            .prefix(&format!("{case}-"))
            .tempdir_in(base)
            .expect("create identity test directory");
        Self {
            directory: Some(directory),
            reparse_points: Vec::new(),
            retain: std::env::var_os("WF_TEST_EVIDENCE").is_some(),
        }
    }

    fn path(&self) -> &Path {
        self.directory
            .as_ref()
            .expect("test directory exists")
            .path()
    }

    fn junction(&mut self, link: &Path, target: &Path) {
        create_junction(link, target);
        if !self.reparse_points.iter().any(|known| known == link) {
            self.reparse_points.push(link.to_path_buf());
        }
    }

    fn track_reparse(&mut self, path: &Path) {
        if !self.reparse_points.iter().any(|known| known == path) {
            self.reparse_points.push(path.to_path_buf());
        }
    }
}

impl Drop for TestTree {
    fn drop(&mut self) {
        // Remove only test-owned reparse points before retaining or recursively
        // removing the ordinary test tree. This never follows or deletes a target,
        // and prevents a retained loop fixture from confusing later evidence walks.
        for path in self.reparse_points.iter().rev() {
            if fs::symlink_metadata(path).is_ok() {
                let _ = fs::remove_dir(path);
            }
        }
        if self.retain
            && let Some(directory) = self.directory.take()
        {
            let _ = directory.keep();
        }
    }
}

struct SyntheticChain {
    tree: TestTree,
    captured_alias: PathBuf,
    physical: PathBuf,
    first_junction: PathBuf,
    first_target: PathBuf,
    second_junction: PathBuf,
    second_target: PathBuf,
    digest: String,
}

impl SyntheticChain {
    fn new(case: &str) -> Self {
        let mut tree = TestTree::new(case);
        let root = tree.path().to_path_buf();
        let first_junction = root.join("captured").join("Codex").join("bin");
        let second_junction = root.join("packages").join("standalone").join("current");
        let second_target = root
            .join("packages")
            .join("standalone")
            .join("releases")
            .join("0.154.0");
        let first_target = second_junction.join("bin");
        let physical = second_target.join("bin").join("codex.exe");
        fs::create_dir_all(physical.parent().unwrap()).expect("create physical parent");
        fs::write(&physical, EXECUTABLE_BYTES).expect("write synthetic executable");
        tree.junction(&second_junction, &second_target);
        tree.junction(&first_junction, &first_target);
        let captured_alias = first_junction.join("codex.exe");
        let digest = digest(EXECUTABLE_BYTES);
        Self {
            tree,
            captured_alias,
            physical,
            first_junction,
            first_target,
            second_junction,
            second_target,
            digest,
        }
    }

    fn identity(&self) -> Identity {
        Identity {
            schema_version: 1,
            adapter: ADAPTER.to_owned(),
            captured_alias: self.captured_alias.clone(),
            physical_executable: self.physical.clone(),
            executable_sha256: self.digest.clone(),
            junctions: vec![
                Junction {
                    path: self.first_junction.clone(),
                    target: self.first_target.clone(),
                },
                Junction {
                    path: self.second_junction.clone(),
                    target: self.second_target.clone(),
                },
            ],
        }
    }

    fn replace_junction(&mut self, link: &Path, target: &Path) {
        fs::remove_dir(link).expect("remove only the test-owned junction");
        self.tree.junction(link, target);
    }
}

fn create_junction(link: &Path, target: &Path) {
    fs::create_dir_all(link.parent().expect("junction parent")).expect("create junction parent");
    let output = Command::new("cmd.exe")
        .args(["/d", "/c", "mklink", "/J"])
        .arg(link)
        .arg(target)
        .output()
        .expect("start mklink for test-owned junction");
    let attempt = MKLINK_ATTEMPT.fetch_add(1, Ordering::SeqCst);
    let evidence = link.parent().unwrap().join(format!("mklink-{attempt:03}"));
    fs::write(evidence.with_extension("stdout"), &output.stdout).unwrap();
    fs::write(evidence.with_extension("stderr"), &output.stderr).unwrap();
    fs::write(
        evidence.with_extension("status.txt"),
        format!(
            "exit_code={:?}\nlink={}\ntarget={}\n",
            output.status.code(),
            link.display(),
            target.display()
        ),
    )
    .unwrap();
    assert!(
        output.status.success(),
        "junction fixture setup failed: {} -> {}; stdout={}; stderr={}",
        link.display(),
        target.display(),
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

fn assert_invalid(result: Result<PathBuf>) {
    assert_eq!(result.expect_err("identity must reject"), "invalid_worker");
}

#[test]
fn exact_two_junction_chain_admits_only_the_physical_executable() {
    let chain = SyntheticChain::new("NI-T01-exact-chain");
    let admitted = chain
        .identity()
        .verify(&chain.physical, &chain.digest, ADAPTER)
        .expect("exact pinned mapping must admit");
    assert_eq!(admitted, resolve(&chain.physical).unwrap());
    assert_eq!(resolve(&chain.captured_alias).unwrap_err(), "reparse_path");
}

#[test]
fn same_bytes_at_another_physical_path_do_not_bypass_identity() {
    let chain = SyntheticChain::new("NI-T02-alternate-target");
    let alternate = chain
        .tree
        .path()
        .join("alternate")
        .join("bin")
        .join("codex.exe");
    fs::create_dir_all(alternate.parent().unwrap()).unwrap();
    fs::write(&alternate, EXECUTABLE_BYTES).unwrap();
    assert_eq!(crate::request::hash_file(&alternate).unwrap(), chain.digest);
    assert_invalid(chain.identity().verify(&alternate, &chain.digest, ADAPTER));
}

#[test]
fn changed_target_and_changed_mapping_order_are_rejected() {
    let mut chain = SyntheticChain::new("NI-T02-changed-target");
    let wrong_target = chain.tree.path().join("wrong-current").join("bin");
    fs::create_dir_all(&wrong_target).unwrap();
    let first = chain.first_junction.clone();
    chain.replace_junction(&first, &wrong_target);
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &chain.digest, ADAPTER),
    );

    let chain = SyntheticChain::new("NI-T02-order");
    let mut identity = chain.identity();
    identity.junctions.swap(0, 1);
    assert_invalid(identity.verify(&chain.physical, &chain.digest, ADAPTER));
}

#[test]
fn directory_symlink_cannot_substitute_for_a_junction() {
    let mut chain = SyntheticChain::new("NI-T02-symlink-substitution");
    fs::remove_dir(&chain.first_junction).expect("remove only the test-owned junction");
    symlink_dir(&chain.first_target, &chain.first_junction).unwrap_or_else(|error| {
        panic!("required Windows directory-symlink fixture could not be created: {error}")
    });
    let first = chain.first_junction.clone();
    chain.tree.track_reparse(&first);
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &chain.digest, ADAPTER),
    );
}

#[test]
fn missing_physical_digest_mismatch_and_unsupported_adapter_are_rejected() {
    let chain = SyntheticChain::new("NI-T03-invalid-worker");
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &"0".repeat(64), ADAPTER),
    );
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &chain.digest, "peer"),
    );

    fs::remove_file(&chain.physical).expect("remove synthetic executable");
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &chain.digest, ADAPTER),
    );
}

#[test]
fn identity_schema_and_record_adapter_are_closed() {
    let chain = SyntheticChain::new("NI-T03-record-fields");
    let mut identity = chain.identity();
    identity.schema_version = 2;
    assert_invalid(identity.verify(&chain.physical, &chain.digest, ADAPTER));

    let mut identity = chain.identity();
    identity.adapter = "peer".to_owned();
    assert_invalid(identity.verify(&chain.physical, &chain.digest, "peer"));
}

#[test]
fn additional_reparse_after_the_two_mappings_is_rejected() {
    let mut tree = TestTree::new("NI-T04-extra-reparse");
    let root = tree.path().to_path_buf();
    let physical = root.join("real-release").join("bin").join("codex.exe");
    fs::create_dir_all(physical.parent().unwrap()).unwrap();
    fs::write(&physical, EXECUTABLE_BYTES).unwrap();
    let unexpected = root.join("release-link");
    tree.junction(&unexpected, &root.join("real-release"));
    let second = root.join("packages").join("current");
    tree.junction(&second, &unexpected);
    let first = root.join("captured").join("bin");
    tree.junction(&first, &second.join("bin"));
    let identity = Identity {
        schema_version: 1,
        adapter: ADAPTER.to_owned(),
        captured_alias: first.join("codex.exe"),
        physical_executable: physical.clone(),
        executable_sha256: digest(EXECUTABLE_BYTES),
        junctions: vec![
            Junction {
                path: first,
                target: second.join("bin"),
            },
            Junction {
                path: second,
                target: unexpected,
            },
        ],
    };
    assert_invalid(identity.verify(&physical, &digest(EXECUTABLE_BYTES), ADAPTER));
}

#[test]
fn repeated_junction_mapping_is_rejected_as_a_loop() {
    let mut tree = TestTree::new("NI-T04-loop");
    let root = tree.path().join("loop-root");
    fs::create_dir_all(&root).unwrap();
    let physical = root.join("codex.exe");
    fs::write(&physical, EXECUTABLE_BYTES).unwrap();
    let repeated = root.join("again");
    tree.junction(&repeated, &root);
    let identity = Identity {
        schema_version: 1,
        adapter: ADAPTER.to_owned(),
        captured_alias: repeated.join("again").join("codex.exe"),
        physical_executable: physical.clone(),
        executable_sha256: digest(EXECUTABLE_BYTES),
        junctions: vec![
            Junction {
                path: repeated.clone(),
                target: root.clone(),
            },
            Junction {
                path: repeated,
                target: root,
            },
        ],
    };
    assert_invalid(identity.verify(&physical, &digest(EXECUTABLE_BYTES), ADAPTER));
}

#[test]
fn mapping_and_bytes_are_rechecked_and_drift_is_rejected() {
    let mut chain = SyntheticChain::new("NI-T05-recheck");
    chain
        .identity()
        .verify(&chain.physical, &chain.digest, ADAPTER)
        .unwrap();

    fs::write(&chain.physical, b"changed after admission\n").unwrap();
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &chain.digest, ADAPTER),
    );
    fs::write(&chain.physical, EXECUTABLE_BYTES).unwrap();
    chain
        .identity()
        .verify(&chain.physical, &chain.digest, ADAPTER)
        .unwrap();

    let drifted_target = chain.tree.path().join("drifted-current").join("bin");
    fs::create_dir_all(&drifted_target).unwrap();
    let first = chain.first_junction.clone();
    chain.replace_junction(&first, &drifted_target);
    assert_invalid(
        chain
            .identity()
            .verify(&chain.physical, &chain.digest, ADAPTER),
    );
}
