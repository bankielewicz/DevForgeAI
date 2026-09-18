// Independent stimuli from DFF-WORKER-FEAS-01. No product imports.
use serde_json::{Value,json};
use std::{fs::{self,OpenOptions},io::{self,BufRead,Write},path::PathBuf,time::Duration};
fn send(v:Value){println!("{v}");io::stdout().flush().unwrap();}
fn hold(){loop{std::thread::sleep(Duration::from_secs(1));}}
fn main(){
    let args:Vec<String>=std::env::args().collect();
    if args[1]=="--sleep" {hold();}
    if args[1]=="--hold" {
        let child=std::process::Command::new(std::env::current_exe().unwrap()).arg("--sleep").stdin(std::process::Stdio::inherit()).stdout(std::process::Stdio::inherit()).stderr(std::process::Stdio::inherit()).spawn().unwrap();
        fs::write(PathBuf::from(&args[2]).join("boundary-pids.json"),json!({"peer":std::process::id(),"descendant":child.id()}).to_string()).unwrap();
        hold();
    }
    let root=PathBuf::from(&args[2]);
    let case=fs::read_to_string(root.join("peer-case.txt")).unwrap();
    let mut trace=OpenOptions::new().create_new(true).write(true).open(root.parent().unwrap().join("qa-trace.jsonl")).unwrap();
    fs::write(root.parent().unwrap().join("qa-peer-pid.txt"),std::process::id().to_string()).unwrap();
    let mut step=0;
    for line in io::stdin().lock().lines(){
        let line=line.unwrap();
        writeln!(trace,"{line}").unwrap();trace.sync_all().unwrap();
        let v:Value=serde_json::from_str(&line).unwrap();
        let id=v["id"].clone();
        let method=v["method"].as_str().unwrap();
        if case.contains("WF-04-9") && method=="initialize" {
            let code=if case.contains("WF-04-94"){json!(-32010)}else if case.contains("WF-04-95"){json!(7.25)}else{json!({"extra":"QA_PRIVATE_SENTINEL_7159"})};
            send(json!({"id":id,"error":{"code":code,"message":"QA_PRIVATE_SENTINEL_7159","data":{"hidden":"QA_PRIVATE_SENTINEL_7159"}}}));
            continue;
        }
        if case.contains("WF-16-90") || case.contains("WF-16-91") {
            assert_eq!(method,"initialize");
            // Legal JSON string ID within the incoming line budget; force synchronous reply > pipe capacity.
            send(json!({"id":"q".repeat(262144),"method":"qa/unsupported","params":{}}));
            fs::write(root.parent().unwrap().join("large-request-sent"),b"262144-byte id; no further stdin reads").unwrap();
            hold();
        }
        if method=="turn/interrupt"{
            assert_eq!(v["params"],json!({"threadId":"qa-thread","turnId":"qa-turn"}));
            send(json!({"id":id,"result":{}}));
            continue;
        }
        let expected=["initialize","initialized","account/read","model/list","account/rateLimits/read","thread/start","turn/start"];
        assert_eq!(method,expected[step]);
        if method!="initialized" {assert_eq!(id.as_u64(),Some(if step==0 {1}else{step as u64}));}
        let p=&v["params"];
        let result=match method {
            "initialize"=>{assert_eq!(p,&json!({"clientInfo":{"name":"devforgeai_worker_probe","version":"0.1.0"},"capabilities":{"experimentalApi":false}}));json!({"userAgent":"independent-qa"})},
            "initialized"=>{assert_eq!(p,&json!({}));step+=1;continue},
            "account/read"=>{assert_eq!(p,&json!({"refreshToken":false}));json!({"account":{"type":"chatgpt","planType":"pro","email":"synthetic-private@example.invalid"},"requiresOpenaiAuth":true})},
            "model/list"=>{assert_eq!(p,&json!({"limit":100,"cursor":null}));json!({"data":[{"id":"test-model","model":"test-model","supportedReasoningEfforts":[{"reasoningEffort":"test-effort","description":"synthetic"}]}],"nextCursor":null})},
            "account/rateLimits/read"=>{assert_eq!(p,&json!({}));json!({"rateLimits":{"primary":{"usedPercent":0},"secondary":null}})},
            "thread/start"=>{
                assert_eq!(p,&json!({"model":"test-model","modelProvider":"openai","cwd":root,"sandbox":"read-only","approvalPolicy":"never","approvalsReviewer":"user","ephemeral":true}));
                json!({"thread":{"id":"qa-thread"},"cwd":root,"model":"test-model","modelProvider":"openai","approvalPolicy":if case.contains("WF-02-90"){"on-request"}else{"never"},"approvalsReviewer":"user","sandbox":{"type":"readOnly","networkAccess":false}})
            },
            "turn/start"=>{
                let prompt=include_str!("../../../../../docs/specs/framework/runtime/fixtures/codex-worker-v1/prompt.txt");
                let schema:Value=serde_json::from_str(include_str!("../../../../../docs/specs/framework/runtime/fixtures/codex-worker-v1/output-schema.json")).unwrap();
                assert_eq!(p,&json!({"threadId":"qa-thread","model":"test-model","effort":"test-effort","cwd":root,"approvalPolicy":"never","approvalsReviewer":"user","sandboxPolicy":{"type":"readOnly","networkAccess":false},"input":[{"type":"text","text":prompt}],"outputSchema":schema}));
                json!({"turn":{"id":"qa-turn","status":"inProgress","items":[],"error":null}})
            },_=>unreachable!()
        };
        assert!(v.get("jsonrpc").is_none());
        send(json!({"id":id,"result":result}));
        step+=1;
        if method=="turn/start" {
            let mut text=include_str!("../../../../../docs/specs/framework/runtime/fixtures/codex-worker-v1/expected.json").to_string();
            if case.contains("WF-18-90"){text=text.replace("cancelled","dispatched");}
            if case.contains("WF-18-91"){text=text.replacen('{',"{\"extra\":true,",1);}
            if case.contains("WF-18-92"){text=text.replacen("\"id\":\"A\"","\"id\":\"A\",\"id\":\"A\"",1);}
            let items=if case.contains("WF-18-93"){vec![]}else{vec![json!({"id":"qa-final","type":"agentMessage","phase":"final_answer","text":text})]};
            let marker="QA_PRIVATE_SENTINEL_7159";
            let sub=case.trim().split('-').nth(2).unwrap_or("0");
            let category=match sub {
                "90"=>json!({"unexpectedPrivateField":marker}),
                "91"=>json!({"httpConnectionFailed":{"httpStatusCode":65535,"extension":{"marker":marker}}}),
                "92"=>json!({"responseStreamDisconnected":{"httpStatusCode":0,"extension":marker}}),
                "93"=>json!({"responseTooManyFailedAttempts":{"httpStatusCode":null,"extension":marker}}),
                "94"=>json!({"responseStreamConnectionFailed":{"extension":marker}}),
                "95"=>json!({"activeTurnNotSteerable":{"turnKind":"compact","extension":marker}}),
                "96"=>json!("usageLimitExceeded"),
                "97"=>json!({"httpConnectionFailed":{"httpStatusCode":65536,"extension":marker}}),
                "98"=>json!({"httpConnectionFailed":{"httpStatusCode":false,"extension":marker}}),
                "99"=>json!({"activeTurnNotSteerable":{"turnKind":marker}}),
                _=>json!({"unknown":marker}),
            };
            let error=if case.contains("WF-07-"){json!({"message":marker,"additionalDetails":marker,"codexErrorInfo":category})}else{Value::Null};
            send(json!({"method":"turn/completed","params":{"threadId":"qa-thread","turn":{"id":"qa-turn","status":if error.is_null(){"completed"}else{"failed"},"items":items,"error":error}}}));
        }
    }
}
