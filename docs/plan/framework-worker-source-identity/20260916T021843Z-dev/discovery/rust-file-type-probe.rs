use std::fs;
use std::os::windows::fs::MetadataExt;
use std::path::Path;

fn main() -> std::io::Result<()> {
    let root = Path::new(
        r"C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome",
    );
    let mut rows = fs::read_dir(root)?
        .filter_map(Result::ok)
        .map(|entry| -> std::io::Result<_> {
            let file_type = entry.file_type()?;
            let metadata = fs::symlink_metadata(entry.path())?;
            Ok((
                entry.file_name().to_string_lossy().into_owned(),
                file_type.is_dir(),
                file_type.is_file(),
                file_type.is_symlink(),
                metadata.file_attributes(),
            ))
        })
        .collect::<std::io::Result<Vec<_>>>()?;
    rows.sort();
    for (name, is_dir, is_file, is_symlink, attrs) in rows {
        println!(
            "name={name};is_dir={is_dir};is_file={is_file};is_symlink={is_symlink};attrs=0x{attrs:08x}"
        );
    }
    Ok(())
}
