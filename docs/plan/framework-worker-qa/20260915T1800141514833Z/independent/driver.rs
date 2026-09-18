use devforgeai_codex_worker_probe::runner::{self, Options};
use std::{io::Write, path::Path, sync::{Arc,atomic::{AtomicU8,Ordering}}, time::Duration};
fn main() -> std::process::ExitCode {
    let args: Vec<String> = std::env::args().collect();
    let control = Arc::new(AtomicU8::new(0));
    if args.get(2).is_some_and(|s|s=="cancel") {
        let flag=control.clone();
        std::thread::spawn(move || {std::thread::sleep(Duration::from_millis(300)); flag.store(1,Ordering::SeqCst);});
    }
    let options=Options {total:Duration::from_millis(750),rpc:Duration::from_millis(500),
        grace:Duration::from_millis(200),teardown:Duration::from_millis(500),control,..Default::default()};
    match runner::run(Path::new(&args[1]),options,&mut |event| {
        println!("{event}"); std::io::stdout().flush().unwrap();
    }) {
        Ok((code,terminal))=>{eprintln!("{terminal}"); std::process::ExitCode::from(code as u8)},
        Err(error)=>{eprintln!("{error}");std::process::ExitCode::from(2)}
    }
}
