use super::*;
use crate::request::{digest, resolve};
use std::{
    fs,
    os::windows::fs::symlink_dir,
    path::{Path, PathBuf},
    process::Command,
};

const ADAPTER: &str = "codex-0.154.0-stdio";
const PHYSICAL: &str = r"C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe";
const ALIAS: &str = r"C:\Users\bryan\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe";
const PINNED_SHA256: &str = "be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde";
const EXE_BYTES: &[u8] = b"qa synthetic executable\n";

struct OwnedTree {
    root: tempfile::TempDir,
    reparses: Vec<PathBuf>,
}

impl OwnedTree {
    fn new(label: &str) -> Self {
        let parent = std::env::var_os("WF_TEST_EVIDENCE")
            .map(PathBuf::from)
            .unwrap_or_else(std::env::temp_dir);
        fs::create_dir_all(&parent).expect("create QA evidence parent");
        Self {
            root: tempfile::Builder::new()
                .prefix(&format!("qa-{label}-"))
                .tempdir_in(parent)
                .expect("create QA-owned fixture root"),
            reparses: Vec::new(),
        }
    }

    fn root(&self) -> &Path {
        self.root.path()
    }

    fn junction(&mut self, link: &Path, target: &Path) {
        fs::create_dir_all(link.parent().expect("junction parent"))
            .expect("create junction parent");
        let output = Command::new("cmd.exe")
            .args(["/d", "/c", "mklink", "/J"])
            .arg(link)
            .arg(target)
            .output()
            .expect("execute mklink for QA-owned fixture");
        assert!(
            output.status.success(),
            "QA junction setup failed: {}",
            String::from_utf8_lossy(&output.stderr)
        );
        self.reparses.push(link.to_path_buf());
    }

    fn track(&mut self, path: &Path) {
        self.reparses.push(path.to_path_buf());
    }
}

impl Drop for OwnedTree {
    fn drop(&mut self) {
        for path in self.reparses.iter().rev() {
            if fs::symlink_metadata(path).is_ok() {
                fs::remove_dir(path).expect("remove only QA-owned reparse point");
            }
        }
    }
}

struct Chain {
    tree: OwnedTree,
    alias: PathBuf,
    physical: PathBuf,
    first_link: PathBuf,
    first_target: PathBuf,
    second_link: PathBuf,
    second_target: PathBuf,
    sha256: String,
}

impl Chain {
    fn new(label: &str) -> Self {
        let mut tree = OwnedTree::new(label);
        let root = tree.root().to_path_buf();
        let first_link = root.join("launcher").join("bin");
        let second_link = root.join("packages").join("current");
        let second_target = root.join("packages").join("release-0.154.0");
        let first_target = second_link.join("bin");
        let physical = second_target.join("bin").join("codex.exe");
        fs::create_dir_all(physical.parent().unwrap()).expect("create synthetic release");
        fs::write(&physical, EXE_BYTES).expect("write synthetic executable");
        tree.junction(&second_link, &second_target);
        tree.junction(&first_link, &first_target);
        Self {
            tree,
            alias: first_link.join("codex.exe"),
            physical,
            first_link,
            first_target,
            second_link,
            second_target,
            sha256: digest(EXE_BYTES),
        }
    }

    fn identity(&self) -> Identity {
        Identity {
            schema_version: 1,
            adapter: ADAPTER.to_owned(),
            captured_alias: self.alias.clone(),
            physical_executable: self.physical.clone(),
            executable_sha256: self.sha256.clone(),
            junctions: vec![
                Junction {
                    path: self.first_link.clone(),
                    target: self.first_target.clone(),
                },
                Junction {
                    path: self.second_link.clone(),
                    target: self.second_target.clone(),
                },
            ],
        }
    }
}

fn must_reject(result: crate::request::Result<PathBuf>) {
    assert_eq!(result.expect_err("identity must reject"), "invalid_worker");
}

#[test]
fn qa_actual_record_admits_only_the_selected_physical_identity() {
    let selected = verify(Path::new(PHYSICAL), PINNED_SHA256, ADAPTER)
        .expect("selected physical identity and mapping must be current");
    assert_eq!(selected, resolve(Path::new(PHYSICAL)).unwrap());
    assert_eq!(resolve(Path::new(ALIAS)).unwrap_err(), "reparse_path");
    must_reject(verify(Path::new(ALIAS), PINNED_SHA256, ADAPTER));
    must_reject(verify(Path::new(PHYSICAL), &"0".repeat(64), ADAPTER));
    must_reject(verify(Path::new(PHYSICAL), PINNED_SHA256, "peer"));
}

#[test]
fn qa_exact_synthetic_mapping_and_same_bytes_elsewhere_are_distinguished() {
    let chain = Chain::new("exact-and-alternate");
    assert_eq!(
        chain
            .identity()
            .verify(&chain.physical, &chain.sha256, ADAPTER)
            .expect("exact synthetic identity must admit"),
        resolve(&chain.physical).unwrap()
    );
    let other = chain.tree.root().join("other").join("codex.exe");
    fs::create_dir_all(other.parent().unwrap()).unwrap();
    fs::write(&other, EXE_BYTES).unwrap();
    assert_eq!(crate::request::hash_file(&other).unwrap(), chain.sha256);
    must_reject(chain.identity().verify(&other, &chain.sha256, ADAPTER));
}

#[test]
fn qa_mapping_target_order_and_reparse_kind_substitutions_fail() {
    let chain = Chain::new("record-target-and-order");
    let mut wrong_target = chain.identity();
    wrong_target.junctions[0].target = chain.tree.root().join("wrong");
    must_reject(wrong_target.verify(&chain.physical, &chain.sha256, ADAPTER));
    let mut wrong_order = chain.identity();
    wrong_order.junctions.swap(0, 1);
    must_reject(wrong_order.verify(&chain.physical, &chain.sha256, ADAPTER));

    let mut chain = Chain::new("symlink-kind");
    fs::remove_dir(&chain.first_link).expect("remove QA-owned junction");
    chain.tree.reparses.retain(|path| path != &chain.first_link);
    symlink_dir(&chain.first_target, &chain.first_link).expect("create QA-owned directory symlink");
    let first_link = chain.first_link.clone();
    chain.tree.track(&first_link);
    must_reject(
        chain
            .identity()
            .verify(&chain.physical, &chain.sha256, ADAPTER),
    );
}

#[test]
fn qa_third_reparse_component_is_not_hidden_by_two_approved_substitutions() {
    let mut tree = OwnedTree::new("third-reparse");
    let root = tree.root().to_path_buf();
    let real_release = root.join("real-release");
    let third_link = root.join("release-link");
    let second_link = root.join("current");
    let first_link = root.join("launcher");
    let physical = real_release.join("bin").join("codex.exe");
    fs::create_dir_all(physical.parent().unwrap()).unwrap();
    fs::write(&physical, EXE_BYTES).unwrap();
    tree.junction(&third_link, &real_release);
    tree.junction(&second_link, &third_link);
    tree.junction(&first_link, &second_link.join("bin"));
    let identity = Identity {
        schema_version: 1,
        adapter: ADAPTER.to_owned(),
        captured_alias: first_link.join("codex.exe"),
        physical_executable: physical.clone(),
        executable_sha256: digest(EXE_BYTES),
        junctions: vec![
            Junction {
                path: first_link,
                target: second_link.join("bin"),
            },
            Junction {
                path: second_link,
                target: third_link,
            },
        ],
    };
    must_reject(identity.verify(&physical, &digest(EXE_BYTES), ADAPTER));
}

#[test]
fn qa_second_verification_detects_independent_byte_and_mapping_drift() {
    let mut chain = Chain::new("recheck-drift");
    chain
        .identity()
        .verify(&chain.physical, &chain.sha256, ADAPTER)
        .expect("first identity observation");
    fs::write(&chain.physical, b"changed after first observation\n").unwrap();
    must_reject(
        chain
            .identity()
            .verify(&chain.physical, &chain.sha256, ADAPTER),
    );

    fs::write(&chain.physical, EXE_BYTES).unwrap();
    chain
        .identity()
        .verify(&chain.physical, &chain.sha256, ADAPTER)
        .expect("restored identity observation");
    fs::remove_dir(&chain.first_link).expect("remove QA-owned launcher junction");
    chain.tree.reparses.retain(|path| path != &chain.first_link);
    let wrong = chain.tree.root().join("wrong-target");
    fs::create_dir_all(&wrong).unwrap();
    let first_link = chain.first_link.clone();
    chain.tree.junction(&first_link, &wrong);
    must_reject(
        chain
            .identity()
            .verify(&chain.physical, &chain.sha256, ADAPTER),
    );
}
