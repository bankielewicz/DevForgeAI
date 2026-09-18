use devforgeai_codex_worker_probe::runner::{self, Options};
fn main() {
    let args: Vec<_> = std::env::args().collect();
    let result = runner::run(
        std::path::Path::new(&args[1]),
        Options::default(),
        &mut |event| {
            if event["kind"] == args[2] {
                std::process::exit(91);
            }
        },
    );
    panic!("crash point not reached: {result:?}");
}
