#[tokio::main]
async fn main() -> std::process::ExitCode {
    std::process::ExitCode::from(devforgeai_index::cli::run(std::env::args().collect()).await as u8)
}
