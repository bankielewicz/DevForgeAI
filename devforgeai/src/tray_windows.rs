use super::*;
use crate::platform::windows::wide;
use crate::{
    cli,
    protocol::{Request, Response},
};
use serde_json::{Value, json};
use std::{cell::RefCell, collections::BTreeMap, sync::mpsc};
use windows_sys::Win32::UI::Input::KeyboardAndMouse::EnableWindow;
use windows_sys::Win32::{
    Foundation::*,
    Graphics::Gdi::*,
    System::{Com::CoTaskMemFree, LibraryLoader::*, Registry::*},
    UI::{Shell::*, WindowsAndMessaging::*},
};

const CLASS: &str = "DevForgeAIIndexTrayV1";
const DONE: u32 = WM_APP + 1;
const TRAY: u32 = WM_APP + 2;
const ENV: i32 = 101;
const PROJECT: i32 = 102;
const ROOT: i32 = 103;
const NAME: i32 = 104;
const STATUS: i32 = 105;
const EXCLUSIONS: i32 = 106;
const START: i32 = 201;
const PAUSE: i32 = 202;
const RESUME: i32 = 203;
const STOP: i32 = 204;
const ADD: i32 = 205;
const RESCAN: i32 = 206;
const REINDEX: i32 = 207;
const CANCEL: i32 = 208;
const REMOVE: i32 = 209;
const EDIT: i32 = 210;
const BROWSE: i32 = 211;
const OPEN: i32 = 212;
const EXIT: i32 = 213;
const STOP_EXIT: i32 = 214;
const SETTINGS: i32 = 215;
struct Work {
    alias: String,
    operation: String,
    params: Value,
    start: bool,
    exit_after: bool,
}
struct Update {
    alias: String,
    response: Response,
    projects: Vec<Value>,
    statuses: Vec<Value>,
    exit_after: bool,
}
struct Ui {
    paths: Paths,
    controls: BTreeMap<i32, HWND>,
    sender: mpsc::Sender<Work>,
    receiver: mpsc::Receiver<Update>,
    poll: PollState,
    aliases: Vec<String>,
    projects: Vec<Value>,
    statuses: Vec<Value>,
    busy: bool,
    selected: String,
}
thread_local! {static UI:RefCell<Option<Ui>>=const{RefCell::new(None)};}

pub fn startup(enabled: bool) -> Result<()> {
    unsafe {
        let mut key = std::ptr::null_mut();
        let result = RegOpenKeyExW(
            HKEY_CURRENT_USER,
            wide(r"Software\Microsoft\Windows\CurrentVersion\Run").as_ptr(),
            0,
            KEY_SET_VALUE,
            &mut key,
        );
        if result != 0 {
            return Err(platform::io_error(std::io::Error::from_raw_os_error(
                result as i32,
            )));
        }
        let value = wide("DevForgeAIIndexTray");
        let result = if enabled {
            let executable = std::env::current_exe()
                .map_err(platform::io_error)?
                .with_file_name("devforgeai-tray.exe");
            let command = wide(format!("\"{}\"", executable.display()));
            RegSetValueExW(
                key,
                value.as_ptr(),
                0,
                REG_SZ,
                command.as_ptr().cast(),
                (command.len() * 2) as u32,
            )
        } else {
            RegDeleteValueW(key, value.as_ptr())
        };
        RegCloseKey(key);
        if result != 0 && result != ERROR_FILE_NOT_FOUND {
            return Err(platform::io_error(std::io::Error::from_raw_os_error(
                result as i32,
            )));
        }
    }
    Ok(())
}

fn request(operation: &str, params: Value) -> Request {
    Request {
        protocol_version: 1,
        request_id: uuid::Uuid::new_v4().to_string(),
        operation: operation.into(),
        timeout_ms: 10000,
        params,
    }
}
fn worker(window: usize, paths: Paths, receive: mpsc::Receiver<Work>, send: mpsc::Sender<Update>) {
    let runtime = match tokio::runtime::Runtime::new() {
        Ok(runtime) => runtime,
        Err(_) => return,
    };
    for work in receive {
        let mut response = runtime
            .block_on(cli::route(
                &paths,
                &work.alias,
                &request(&work.operation, work.params),
                work.start,
            ))
            .unwrap_or_else(|error| Response::from_error(uuid::Uuid::new_v4().to_string(), error));
        if work.exit_after && response.ok {
            let stopped = runtime.block_on(async {
                let started = Instant::now();
                while started.elapsed() < Duration::from_secs(10) {
                    match cli::route(
                        &paths,
                        &work.alias,
                        &request("daemon.status", json!({})),
                        false,
                    )
                    .await
                    {
                        Err(error) if error.code == ErrorCode::ServiceUnavailable => return true,
                        _ => tokio::time::sleep(Duration::from_millis(50)).await,
                    }
                }
                false
            });
            if !stopped {
                response = Response::failure(
                    uuid::Uuid::new_v4().to_string(),
                    ErrorCode::Timeout,
                    "Stop was not confirmed; daemon was not force-killed",
                );
            }
        }
        let mut projects = Vec::new();
        let mut statuses = Vec::new();
        if response.ok
            && work.operation != "daemon.stop"
            && let Ok(list) = runtime.block_on(cli::route(
                &paths,
                &work.alias,
                &request("project.list", json!({})),
                false,
            ))
        {
            projects = list.data["projects"]
                .as_array()
                .cloned()
                .unwrap_or_default();
            for project in &projects {
                if let Ok(status) = runtime.block_on(cli::route(
                    &paths,
                    &work.alias,
                    &request("index.status", json!({"project_id":project["id"]})),
                    false,
                )) {
                    statuses.push(status.data);
                }
            }
        }
        if send
            .send(Update {
                alias: work.alias,
                response,
                projects,
                statuses,
                exit_after: work.exit_after,
            })
            .is_err()
        {
            break;
        }
        unsafe {
            PostMessageW(window as HWND, DONE, 0, 0);
        }
    }
}

unsafe fn text(control: HWND) -> String {
    unsafe {
        let length = GetWindowTextLengthW(control);
        let mut bytes = vec![0u16; length as usize + 1];
        GetWindowTextW(control, bytes.as_mut_ptr(), bytes.len() as i32);
        String::from_utf16_lossy(&bytes[..length as usize])
    }
}
unsafe fn set_text(control: HWND, value: &str) {
    unsafe {
        SetWindowTextW(control, wide(value).as_ptr());
    }
}
unsafe fn child(
    parent: HWND,
    class: &str,
    label: &str,
    style: u32,
    id: i32,
    rect: (i32, i32, i32, i32),
) -> HWND {
    unsafe {
        let window = CreateWindowExW(
            0,
            wide(class).as_ptr(),
            wide(label).as_ptr(),
            WS_CHILD | WS_VISIBLE | style,
            rect.0,
            rect.1,
            rect.2,
            rect.3,
            parent,
            id as usize as HMENU,
            GetModuleHandleW(std::ptr::null()),
            std::ptr::null(),
        );
        SendMessageW(
            window,
            WM_SETFONT,
            GetStockObject(DEFAULT_GUI_FONT) as usize,
            1,
        );
        window
    }
}
unsafe fn icon(window: HWND, operation: u32, label: &str) {
    unsafe {
        let mut data: NOTIFYICONDATAW = std::mem::zeroed();
        data.cbSize = std::mem::size_of::<NOTIFYICONDATAW>() as u32;
        data.hWnd = window;
        data.uID = 1;
        data.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
        data.uCallbackMessage = TRAY;
        data.hIcon = LoadIconW(std::ptr::null_mut(), IDI_APPLICATION);
        for (to, from) in data.szTip.iter_mut().zip(wide(label)) {
            *to = from;
        }
        Shell_NotifyIconW(operation, &data);
    }
}
fn enqueue(ui: &mut Ui, work: Work) {
    if ui.busy {
        return;
    }
    ui.busy = true;
    for id in START..=EDIT {
        if let Some(control) = ui.controls.get(&id) {
            unsafe {
                EnableWindow(*control, 0);
            }
        }
    }
    let _ = ui.sender.send(work);
}
unsafe fn poll(window: HWND) {
    unsafe {
        UI.with(|cell| {
            let Ok(mut value) = cell.try_borrow_mut() else {
                return;
            };
            let Some(ui) = value.as_mut() else {
                return;
            };
            if !ui.busy && ui.poll.begin(Instant::now(), IsWindowVisible(window) != 0) {
                let alias = ui.selected.clone();
                enqueue(
                    ui,
                    Work {
                        alias,
                        operation: "daemon.status".into(),
                        params: json!({}),
                        start: false,
                        exit_after: false,
                    },
                );
            }
        });
    }
}

unsafe fn apply_update(window: HWND) {
    unsafe {
        UI.with(|cell|{let Ok(mut value)=cell.try_borrow_mut()else{return;};let Some(ui)=value.as_mut()else{return;};while let Ok(update)=ui.receiver.try_recv(){
        ui.busy=false;ui.poll.finish(Instant::now(),IsWindowVisible(window)!=0,!update.response.ok);
        if update.exit_after{
            let close=update.response.ok||MessageBoxW(window,wide("Stop timed out. Close the tray and leave the daemon's outcome unresolved?").as_ptr(),wide(format!("Stop {} and exit",update.alias)).as_ptr(),MB_YESNO|MB_ICONWARNING)==IDYES;
            if close{DestroyWindow(window);return;}
        }
        let mode=if !update.response.ok{"disconnected/error"}else if update.response.data["indexing_mode"]=="paused"{"paused"}else{"active"};
        icon(window,NIM_MODIFY,&format!("DevForgeAI Index: {mode} ({})",update.alias));
        set_text(ui.controls[&STATUS],&super::status_text(&update.alias,&update.response,&update.projects,&update.statuses));
        if update.alias==ui.selected{
            let selection=SendMessageW(ui.controls[&PROJECT],CB_GETCURSEL,0,0);let selected=ui.projects.get(selection as usize).map(|p|p["id"].clone());
            ui.projects=update.projects;ui.statuses=update.statuses;SendMessageW(ui.controls[&PROJECT],CB_RESETCONTENT,0,0);
            let mut new_selection=0;
            for (i,project) in ui.projects.iter().enumerate(){let title=format!("{} — {}",project["name"].as_str().unwrap_or(""),project["root"].as_str().unwrap_or(""));SendMessageW(ui.controls[&PROJECT],CB_ADDSTRING,0,wide(title).as_ptr() as isize);if Some(&project["id"])==selected.as_ref(){new_selection=i;}}
            SendMessageW(ui.controls[&PROJECT],CB_SETCURSEL,new_selection,0);
        }
        for id in START..=EDIT{if let Some(control)=ui.controls.get(&id){let enabled=if [RESCAN,REINDEX,CANCEL,REMOVE,EDIT].contains(&id){!ui.projects.is_empty()&&update.response.ok}else{true};EnableWindow(*control,i32::from(enabled));}}
    }});
    }
}

unsafe fn action(window: HWND, command: i32) {
    unsafe {
        if command == OPEN {
            ShowWindow(window, SW_SHOW);
            SetForegroundWindow(window);
            return;
        }
        if command == EXIT {
            DestroyWindow(window);
            return;
        }
        UI.with(|cell|{let Ok(mut value)=cell.try_borrow_mut()else{return;};let Some(ui)=value.as_mut()else{return;};
        if command==ENV{let index=SendMessageW(ui.controls[&ENV],CB_GETCURSEL,0,0);if let Some(alias)=ui.aliases.get(index as usize){ui.selected=alias.clone();ui.poll=PollState::new(Instant::now());ui.projects.clear();ui.statuses.clear();EnableWindow(ui.controls[&BROWSE],i32::from(ui.selected=="local"));}return;}
        if ui.busy{return;}
        if command==SETTINGS{
            let launch=MessageBoxW(window,wide("Launch the tray at Windows sign-in? Yes enables the per-user startup entry; No disables it.").as_ptr(),wide("Explicit startup preference").as_ptr(),MB_YESNOCANCEL|MB_ICONQUESTION);
            if launch==IDCANCEL{return;}
            let daemon=MessageBoxW(window,wide("Start the local daemon when this tray starts? This never starts WSL.").as_ptr(),wide("Local daemon preference").as_ptr(),MB_YESNOCANCEL|MB_ICONQUESTION);
            if daemon==IDCANCEL{return;}
            match set_preferences(&ui.paths,Some(launch==IDYES),Some(daemon==IDYES)){Ok(prefs)=>set_text(ui.controls[&STATUS],&format!("Saved preferences: {}",json!(prefs))),Err(error)=>set_text(ui.controls[&STATUS],&error.to_string())}return;
        }
        if command==BROWSE{
            if ui.selected!="local"{return;}
            let mut info:BROWSEINFOW=std::mem::zeroed();info.hwndOwner=window;info.ulFlags=BIF_RETURNONLYFSDIRS;
            let selection=SHBrowseForFolderW(&info);if !selection.is_null(){let mut path=[0u16;32768];if SHGetPathFromIDListW(selection,path.as_mut_ptr())!=0{let end=path.iter().position(|v|*v==0).unwrap_or(path.len());set_text(ui.controls[&ROOT],&String::from_utf16_lossy(&path[..end]));}CoTaskMemFree(selection.cast());}return;
        }
        let project_index=SendMessageW(ui.controls[&PROJECT],CB_GETCURSEL,0,0);let project=ui.projects.get(project_index as usize).cloned();
        let (operation,params,start)=match command{
            START=>("daemon.handshake",json!({}),true),PAUSE=>("daemon.pause",json!({}),false),RESUME=>("daemon.resume",json!({}),false),
            STOP|STOP_EXIT=>{if MessageBoxW(window,wide(format!("Stop only the daemon in {}? WSL and other daemons remain running.",ui.selected)).as_ptr(),wide(format!("Stop {}",ui.selected)).as_ptr(),MB_YESNO|MB_ICONQUESTION)!=IDYES{return;}("daemon.stop",json!({}),false)},
            ADD=>("project.add",json!({"root":text(ui.controls[&ROOT]),"name":text(ui.controls[&NAME])}),false),
            RESCAN|REINDEX|REMOVE|EDIT|CANCEL=>{
                let Some(project)=project else{set_text(ui.controls[&STATUS],"Select a registered project first.");return;};
                let project_id=project["id"].clone();
                match command{
                    RESCAN=>("index.rescan",json!({"project_id":project_id}),false),REINDEX=>("index.reindex",json!({"project_id":project_id}),false),
                    REMOVE=>{if MessageBoxW(window,wide(format!("Remove {} ({})? This unregisters the project and deletes only its application cache and snapshots. Source files remain.",project["name"],project["root"])).as_ptr(),wide("Confirm cache removal").as_ptr(),MB_YESNO|MB_ICONWARNING)!=IDYES{return;}("project.remove",json!({"project_id":project_id}),false)},
                    EDIT=>{let exclusions:Vec<String>=text(ui.controls[&EXCLUSIONS]).lines().filter(|line|!line.is_empty()).map(String::from).collect();("project.update",json!({"project_id":project_id,"config":{"exclusions":exclusions}}),false)},
                    _=>{let job=ui.statuses.iter().find(|s|s["project_id"]==project_id).and_then(|s|s["jobs"].as_array()).and_then(|jobs|jobs.first()).map(|job|job["id"].clone());let Some(job)=job else{set_text(ui.controls[&STATUS],"No active job for this project.");return;};("job.cancel",json!({"job_id":job}),false)}
                }
            },_=>return,
        };
        let alias=ui.selected.clone();set_text(ui.controls[&STATUS],"Request in progress. Success is shown only after acknowledgment; accepted jobs may remain queued or running.");
        enqueue(ui,Work{alias,operation:operation.into(),params,start,exit_after:command==STOP_EXIT});
    });
    }
}

unsafe extern "system" fn procedure(
    window: HWND,
    message: u32,
    wparam: WPARAM,
    lparam: LPARAM,
) -> LRESULT {
    unsafe {
        match message {
            WM_COMMAND => {
                let id = (wparam & 0xffff) as i32;
                if id != ENV || ((wparam >> 16) & 0xffff) == CBN_SELCHANGE as usize {
                    action(window, id);
                }
                0
            }
            WM_TIMER => {
                poll(window);
                0
            }
            DONE => {
                apply_update(window);
                0
            }
            TRAY => {
                if lparam as u32 == WM_LBUTTONDBLCLK {
                    action(window, OPEN);
                } else if lparam as u32 == WM_RBUTTONUP {
                    let menu = CreatePopupMenu();
                    for (id, label) in [
                        (OPEN, "Open status"),
                        (START, "Start selected daemon"),
                        (PAUSE, "Pause indexing"),
                        (RESUME, "Resume indexing"),
                        (STOP, "Stop selected daemon"),
                        (SETTINGS, "Startup settings"),
                        (STOP_EXIT, "Stop selected daemon and exit..."),
                        (EXIT, "Exit tray (leave daemons running)"),
                    ] {
                        AppendMenuW(menu, MF_STRING, id as usize, wide(label).as_ptr());
                    }
                    let mut point = POINT { x: 0, y: 0 };
                    GetCursorPos(&mut point);
                    SetForegroundWindow(window);
                    let selected = TrackPopupMenu(
                        menu,
                        TPM_RETURNCMD | TPM_RIGHTBUTTON,
                        point.x,
                        point.y,
                        0,
                        window,
                        std::ptr::null(),
                    );
                    DestroyMenu(menu);
                    if selected != 0 {
                        action(window, selected);
                    }
                }
                0
            }
            WM_CLOSE => {
                ShowWindow(window, SW_HIDE);
                0
            }
            WM_DESTROY => {
                KillTimer(window, 1);
                icon(window, NIM_DELETE, "");
                PostQuitMessage(0);
                0
            }
            _ => DefWindowProcW(window, message, wparam, lparam),
        }
    }
}

pub fn run() -> Result<()> {
    unsafe {
        let previous = FindWindowW(wide(CLASS).as_ptr(), std::ptr::null());
        if !previous.is_null() {
            ShowWindow(previous, SW_SHOW);
            SetForegroundWindow(previous);
            return Ok(());
        }
        let paths = Paths::discover()?;
        let lock = std::fs::OpenOptions::new()
            .create(true)
            .truncate(false)
            .write(true)
            .open(paths.runtime.join("tray.lock"))
            .map_err(platform::io_error)?;
        fs2::FileExt::try_lock_exclusive(&lock)
            .map_err(|error| ProtocolError::new(ErrorCode::InstanceConflict, error.to_string()))?;
        let instance = GetModuleHandleW(std::ptr::null());
        let class_name = wide(CLASS);
        let mut class: WNDCLASSW = std::mem::zeroed();
        class.lpszClassName = class_name.as_ptr();
        class.hInstance = instance;
        class.lpfnWndProc = Some(procedure);
        class.hCursor = LoadCursorW(std::ptr::null_mut(), IDC_ARROW);
        class.hbrBackground = (COLOR_WINDOW + 1) as HBRUSH;
        if RegisterClassW(&class) == 0 {
            return Err(platform::io_error(std::io::Error::last_os_error()));
        }
        let window = CreateWindowExW(
            0,
            class_name.as_ptr(),
            wide("DevForgeAI Index — project management").as_ptr(),
            WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            920,
            730,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            instance,
            std::ptr::null(),
        );
        if window.is_null() {
            return Err(platform::io_error(std::io::Error::last_os_error()));
        }
        let mut controls = BTreeMap::new();
        child(window, "STATIC", "Environment", 0, 0, (16, 12, 120, 20));
        controls.insert(
            ENV,
            child(
                window,
                "COMBOBOX",
                "",
                CBS_DROPDOWNLIST as u32 | WS_VSCROLL,
                ENV,
                (140, 8, 350, 200),
            ),
        );
        child(window, "STATIC", "Project", 0, 0, (16, 48, 120, 20));
        controls.insert(
            PROJECT,
            child(
                window,
                "COMBOBOX",
                "",
                CBS_DROPDOWNLIST as u32 | WS_VSCROLL,
                PROJECT,
                (140, 44, 730, 240),
            ),
        );
        for (i, (id, label)) in [
            (START, "Start"),
            (PAUSE, "Pause"),
            (RESUME, "Resume"),
            (STOP, "Stop"),
            (RESCAN, "Rescan"),
            (REINDEX, "Full reindex"),
            (CANCEL, "Cancel job"),
            (REMOVE, "Remove"),
        ]
        .iter()
        .enumerate()
        {
            controls.insert(
                *id,
                child(
                    window,
                    "BUTTON",
                    label,
                    BS_PUSHBUTTON as u32,
                    *id,
                    (16 + i as i32 * 108, 82, 102, 30),
                ),
            );
        }
        child(
            window,
            "STATIC",
            "Root (Windows path or explicit Linux path for WSL)",
            0,
            0,
            (16, 124, 600, 20),
        );
        controls.insert(
            ROOT,
            child(
                window,
                "EDIT",
                "",
                WS_BORDER | ES_AUTOHSCROLL as u32,
                ROOT,
                (16, 148, 680, 26),
            ),
        );
        controls.insert(
            BROWSE,
            child(
                window,
                "BUTTON",
                "Choose folder",
                0,
                BROWSE,
                (708, 148, 162, 28),
            ),
        );
        child(window, "STATIC", "Display name", 0, 0, (16, 188, 110, 20));
        controls.insert(
            NAME,
            child(
                window,
                "EDIT",
                "",
                WS_BORDER | ES_AUTOHSCROLL as u32,
                NAME,
                (140, 184, 550, 26),
            ),
        );
        controls.insert(
            ADD,
            child(
                window,
                "BUTTON",
                "Register project",
                0,
                ADD,
                (708, 184, 162, 28),
            ),
        );
        child(
            window,
            "STATIC",
            "Exclusion globs (one per line; apply replaces project exclusions)",
            0,
            0,
            (16, 224, 740, 20),
        );
        controls.insert(
            EXCLUSIONS,
            child(
                window,
                "EDIT",
                "",
                WS_BORDER | ES_MULTILINE as u32 | ES_AUTOVSCROLL as u32 | WS_VSCROLL,
                EXCLUSIONS,
                (16, 248, 674, 64),
            ),
        );
        controls.insert(
            EDIT,
            child(
                window,
                "BUTTON",
                "Apply exclusions",
                0,
                EDIT,
                (708, 248, 162, 28),
            ),
        );
        controls.insert(
            SETTINGS,
            child(
                window,
                "BUTTON",
                "Startup settings",
                0,
                SETTINGS,
                (708, 284, 162, 28),
            ),
        );
        controls.insert(STATUS,child(window,"EDIT","Disconnected. Select an environment; Start is explicit. Choose a project to enable project controls.",WS_BORDER|ES_MULTILINE as u32|ES_READONLY as u32|ES_AUTOVSCROLL as u32|WS_VSCROLL,STATUS,(16,330,854,330)));
        let mut aliases = vec!["local".to_owned()];
        aliases.extend(cli::aliases(&paths)?.keys().cloned());
        for alias in &aliases {
            SendMessageW(
                controls[&ENV],
                CB_ADDSTRING,
                0,
                wide(alias).as_ptr() as isize,
            );
        }
        SendMessageW(controls[&ENV], CB_SETCURSEL, 0, 0);
        let (sender, receive) = mpsc::channel();
        let (send, receiver) = mpsc::channel();
        let thread_paths = paths.clone();
        let worker_window = window as usize;
        std::thread::spawn(move || worker(worker_window, thread_paths, receive, send));
        let prefs = preferences(&paths)?;
        UI.with(|cell| {
            *cell.borrow_mut() = Some(Ui {
                paths,
                controls,
                sender,
                receiver,
                poll: PollState::new(Instant::now()),
                aliases,
                projects: vec![],
                statuses: vec![],
                busy: false,
                selected: "local".into(),
            })
        });
        icon(window, NIM_ADD, "DevForgeAI Index: disconnected");
        SetTimer(window, 1, 500, None);
        ShowWindow(window, SW_SHOW);
        UpdateWindow(window);
        if prefs.start_local_daemon {
            action(window, START);
        } else {
            poll(window);
        }
        let mut message: MSG = std::mem::zeroed();
        loop {
            let result = GetMessageW(&mut message, std::ptr::null_mut(), 0, 0);
            if result == 0 {
                break;
            }
            if result < 0 {
                return Err(platform::io_error(std::io::Error::last_os_error()));
            }
            TranslateMessage(&message);
            DispatchMessageW(&message);
        }
        UI.with(|cell| {
            cell.borrow_mut().take();
        });
        drop(lock);
        Ok(())
    }
}

#[cfg(test)]
#[path = "../tests/unit/tray_windows.rs"]
mod repair_tests;
