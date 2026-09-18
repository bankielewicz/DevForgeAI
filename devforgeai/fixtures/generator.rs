use serde::Serialize;
use sha2::{Digest, Sha256};
use std::{fs, io, path::Path};

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Entry {
    pub path: String,
    pub bytes: usize,
    pub sha256: String,
    pub language: String,
}
pub fn generate(
    root: &Path,
    count: usize,
    total_bytes: usize,
    seed: u64,
) -> io::Result<Vec<Entry>> {
    if count == 0 || total_bytes / count < 256 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "Fixture requires at least 256 bytes per file",
        ));
    }
    let mut entries = Vec::new();
    let mut random = seed;
    for i in 0..count {
        random = random
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let (language, extension, head) = match i % 5 {
            0 => (
                "rust",
                "rs",
                format!("/// fixture {random}\nfn item_{i}() -> u32 {{ 1 }}\n// "),
            ),
            1 => (
                "python",
                "py",
                format!("def item_{i}():\n    \"\"\"fixture {random}\"\"\"\n    return 1\n# "),
            ),
            2 => {
                if i % 10 == 2 {
                    (
                        "javascript",
                        "js",
                        format!(
                            "/** fixture {random} */\nfunction item_{i}() {{ return 1; }}\n// "
                        ),
                    )
                } else {
                    (
                        "javascript",
                        "jsx",
                        format!("function item_{i}() {{ return <div/>; }}\n// fixture {random} "),
                    )
                }
            }
            3 => {
                if i % 10 == 3 {
                    (
                        "typescript",
                        "ts",
                        format!(
                            "/** fixture {random} */\nfunction item_{i}(): number {{ return 1; }}\n// "
                        ),
                    )
                } else {
                    (
                        "typescript",
                        "tsx",
                        format!("function item_{i}() {{ return <div/>; }}\n// fixture {random} "),
                    )
                }
            }
            _ => (
                "text",
                "md",
                format!("# Fixture {random}\nItem {i} documentation.\n"),
            ),
        };
        let size = total_bytes / count + usize::from(i < total_bytes % count);
        let mut bytes = head.into_bytes();
        bytes.resize(size - 1, b'x');
        bytes.push(b'\n');
        let path = format!("fixture-{i:05}.{extension}");
        fs::write(root.join(&path), &bytes)?;
        entries.push(Entry {
            path,
            bytes: bytes.len(),
            sha256: format!("{:x}", Sha256::digest(&bytes)),
            language: language.into(),
        });
    }
    Ok(entries)
}
