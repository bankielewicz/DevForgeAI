use devforgeai_codex_worker_probe::{request,process_windows::OwnedProcess,journal::Journal,protocol::Session,runner::Options};
use serde_json::{Value,json};
use std::{fs,path::Path,sync::{Arc,atomic::{AtomicU8,Ordering}},time::{Duration,Instant},os::windows::io::{OwnedHandle,FromRawHandle,AsRawHandle}};
use windows_sys::Win32::System::Threading::{OpenProcess,PROCESS_SYNCHRONIZE,WaitForSingleObject};

pub fn run(input:&Path,mode:&str){
    let r=request::validate(input).unwrap();
    let base=input.parent().unwrap();
    let mut p=OwnedProcess::spawn(&r.worker_executable,&["--hold".into(),base.to_string_lossy().into_owned()],&r.checkout_root).unwrap();
    let ready=Instant::now()+Duration::from_secs(2);
    let ids:Value=loop{if let Ok(b)=fs::read(base.join("boundary-pids.json")){if let Ok(v)=serde_json::from_slice(&b){break v;}} assert!(Instant::now()<ready);std::thread::sleep(Duration::from_millis(2));};
    let handles:Vec<OwnedHandle>=["peer","descendant"].iter().map(|k|unsafe{let h=OpenProcess(PROCESS_SYNCHRONIZE,0,ids[k].as_u64().unwrap() as u32);assert!(!h.is_null());OwnedHandle::from_raw_handle(h)}).collect();
    let before:Vec<u32>=handles.iter().map(|h|unsafe{WaitForSingleObject(h.as_raw_handle(),0)}).collect();
    assert_eq!(before,vec![258,258]);
    let control=Arc::new(AtomicU8::new(0));
    let start=Instant::now();
    let mut send_reason=String::from("filled");
    let mut second_reason=None;
    if mode=="interrupt"{
        let fill=json!({"x":"z".repeat(4087)});
        assert_eq!(serde_json::to_vec(&fill).unwrap().len()+1,4096);
        p.send_until(&fill,Instant::now()+Duration::from_secs(1),None).unwrap();
    }else{
        let flag=control.clone();let value=if mode=="cancel"{1}else if mode=="invalid"{2}else{0};
        let setter=std::thread::spawn(move||{std::thread::sleep(Duration::from_millis(80));flag.store(value,Ordering::SeqCst);});
        send_reason=p.send_until(&json!({"id":31,"method":"thread/start","params":{"padding":"p".repeat(131072)}}),Instant::now()+Duration::from_millis(250),Some(&control)).unwrap_err();
        setter.join().unwrap();
        assert_eq!(send_reason,if mode=="cancel"{"user_cancel"}else if mode=="invalid"{"invalid_control"}else{"deadline"});
        second_reason=Some(p.send_until(&json!({"id":32,"method":"forbidden-second-send"}),Instant::now()+Duration::from_millis(100),None).unwrap_err());
        assert_eq!(second_reason.as_deref(),Some("pipe_write_pending"));
    }
    let mut j=Journal::create(&r).unwrap();let opts=Options{grace:Duration::from_millis(180),..Default::default()};let mut emit=|_:&Value|{};
    let mut s=Session::new(&mut p,&mut j,&mut emit,&opts,Instant::now()+Duration::from_secs(1));
    s.thread=Some("qa-thread".into());s.turn=Some("qa-turn".into());
    let interrupt_start=Instant::now();s.interrupt();let interrupt_ms=interrupt_start.elapsed().as_millis();
    assert!(interrupt_ms<400);
    if mode=="interrupt"{assert!(interrupt_ms>=170);}
    assert!(p.stop(Duration::from_millis(500)));
    let after:Vec<u32>=handles.iter().map(|h|unsafe{WaitForSingleObject(h.as_raw_handle(),0)}).collect();
    assert_eq!(after,vec![0,0]);assert_eq!(p.active().unwrap(),0);
    let elapsed=start.elapsed().as_millis();assert!(elapsed<1200);
    println!("{}",json!({"mode":mode,"send_reason":send_reason,"second_reason":second_reason,"interrupt_ms":interrupt_ms,"elapsed_ms":elapsed,"initial_waits":before,"final_waits":after,"job_active":p.active().unwrap(),"worker_exit":p.exit_code(),"held_pids":ids}));
}
