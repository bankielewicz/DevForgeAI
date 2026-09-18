#[tokio::main]
async fn main() {
    let result = match devforgeai_index::platform::Paths::discover() {
        Ok(paths) => devforgeai_index::host::serve(paths).await,
        Err(error) => Err(error),
    };
    if let Err(error) = result {
        eprintln!("{error}");
        std::process::exit(error.code.exit_code());
    }
}
