use crate::{
    journal::Journal,
    oracle,
    process_windows::{Incoming, OwnedProcess},
    request::{self, Request, Result},
    runner::Options,
};
use serde_json::{Value, json};
use std::{
    collections::{HashMap, VecDeque},
    sync::atomic::Ordering,
    time::{Duration, Instant},
};

// Captured 0.154.0 CodexErrorInfo: retain only recognized typed fields.
// Nested objects may gain fields upstream; those fields are never evidence.
fn error_category(value: &Value) -> Result<Value> {
    if value.is_null() {
        return Ok(Value::Null);
    }
    if let Some(name) = value.as_str() {
        return if [
            "contextWindowExceeded",
            "sessionBudgetExceeded",
            "usageLimitExceeded",
            "rateLimitExceeded",
            "serverOverloaded",
            "cyberPolicy",
            "misalignmentPolicyViolation",
            "internalServerError",
            "unauthorized",
            "badRequest",
            "threadRollbackFailed",
            "sandboxError",
            "other",
        ]
        .contains(&name)
        {
            Ok(json!(name))
        } else {
            Err("protocol_error".into())
        };
    }
    let object = value.as_object().ok_or("protocol_error")?;
    if object.len() != 1 {
        return Err("protocol_error".into());
    }
    let (name, fields) = object.iter().next().ok_or("protocol_error")?;
    let fields = fields.as_object().ok_or("protocol_error")?;
    let detail = match name.as_str() {
        "httpConnectionFailed"
        | "responseStreamConnectionFailed"
        | "responseStreamDisconnected"
        | "responseTooManyFailedAttempts" => match fields.get("httpStatusCode") {
            None => json!({}),
            Some(Value::Null) => json!({"httpStatusCode":null}),
            Some(code) => {
                let code = code
                    .as_u64()
                    .filter(|n| *n <= u16::MAX.into())
                    .ok_or("protocol_error")?;
                json!({"httpStatusCode":code})
            }
        },
        "activeTurnNotSteerable" => {
            let kind = fields
                .get("turnKind")
                .and_then(Value::as_str)
                .ok_or("protocol_error")?;
            if !["review", "compact"].contains(&kind) {
                return Err("protocol_error".into());
            }
            json!({"turnKind":kind})
        }
        _ => return Err("protocol_error".into()),
    };
    Ok(json!({name:detail}))
}

pub struct Session<'a> {
    pub process: &'a mut OwnedProcess,
    pub journal: &'a mut Journal,
    pub emit: &'a mut dyn FnMut(&Value),
    pub options: &'a Options,
    pub deadline: Instant,
    pub thread: Option<String>,
    pub turn: Option<String>,
    pub usage: Value,
    next_id: u64,
    responses: HashMap<u64, Value>,
    pending: VecDeque<Value>,
    items: HashMap<String, Value>,
    completed_observation: Option<Value>,
}
impl<'a> Session<'a> {
    pub fn new(
        process: &'a mut OwnedProcess,
        journal: &'a mut Journal,
        emit: &'a mut dyn FnMut(&Value),
        options: &'a Options,
        deadline: Instant,
    ) -> Self {
        Self {
            process,
            journal,
            emit,
            options,
            deadline,
            thread: None,
            turn: None,
            usage: Value::Null,
            next_id: 1,
            responses: HashMap::new(),
            pending: VecDeque::new(),
            items: HashMap::new(),
            completed_observation: None,
        }
    }
    pub fn record(&mut self, kind: &str, data: Value) -> Result<()> {
        let event = self.journal.append(kind, data)?;
        (self.emit)(&event);
        Ok(())
    }
    fn control(&self) -> Result<()> {
        match self.options.control.load(Ordering::SeqCst) {
            0 => Ok(()),
            1 => Err("user_cancel".into()),
            _ => Err("invalid_control".into()),
        }
    }
    fn receive(&mut self, deadline: Instant, stopping: bool) -> Result<Value> {
        loop {
            if !stopping {
                self.control()?;
            }
            if Instant::now() >= deadline {
                return Err("deadline".into());
            }
            match self.process.incoming.recv_timeout(
                Duration::from_millis(5).min(deadline.saturating_duration_since(Instant::now())),
            ) {
                Ok(Incoming::Line(bytes)) => {
                    let v: Value = serde_json::from_slice(&bytes).map_err(|_| "protocol_error")?;
                    if !v.is_object() || v.get("jsonrpc").is_some() {
                        return Err("protocol_error".into());
                    }
                    if let Some(method) = v.get("method") {
                        let method = method.as_str().ok_or("protocol_error")?;
                        if let Some(id) = v.get("id") {
                            if !(id.is_string() || id.is_u64()) {
                                return Err("protocol_error".into());
                            }
                            let approval = matches!(
                                method,
                                "item/commandExecution/requestApproval"
                                    | "item/fileChange/requestApproval"
                            );
                            let response = if approval {
                                json!({"id":id,"result":{"decision":"cancel"}})
                            } else {
                                json!({"id":id,"error":{"code":-32601,"message":"Method not supported"}})
                            };
                            self.process.send_until(
                                &response,
                                deadline,
                                if stopping {
                                    None
                                } else {
                                    Some(&self.options.control)
                                },
                            )?;
                            self.record("worker_event",json!({"method":method.chars().take(128).collect::<String>(),"bytes":bytes.len(),"rejection":if approval {"approval_required"} else {"unsupported_request"}}))?;
                            return Err(if approval {
                                "approval_required"
                            } else {
                                "unsupported_request"
                            }
                            .into());
                        }
                    }
                    return Ok(v);
                }
                Ok(Incoming::Stderr { bytes, sha256 }) => self.record(
                    "worker_event",
                    json!({"stream":"stderr","bytes":bytes,"sha256":sha256,"content":"omitted"}),
                )?,
                Ok(Incoming::Error(reason)) => return Err(reason.into()),
                Ok(Incoming::End) => return Err("worker_exited".into()),
                Err(std::sync::mpsc::RecvTimeoutError::Disconnected) => {
                    return Err("worker_exited".into());
                }
                Err(std::sync::mpsc::RecvTimeoutError::Timeout) => {}
            }
        }
    }
    fn response(&mut self, v: &Value, expected: Option<u64>) -> Result<bool> {
        let id = v["id"].as_u64().ok_or("protocol_error")?;
        if let Some(old) = self.responses.get(&id) {
            if old != v {
                return Err("protocol_error".into());
            }
            return Ok(false);
        }
        if Some(id) != expected {
            return Err("protocol_error".into());
        }
        if v.get("result").is_some() == v.get("error").is_some() {
            return Err("protocol_error".into());
        }
        self.responses.insert(id, v.clone());
        Ok(true)
    }
    fn rpc(&mut self, method: &str, params: Value) -> Result<Value> {
        self.control()?;
        if Instant::now() >= self.deadline {
            return Err("deadline".into());
        }
        let id = self.next_id;
        self.next_id += 1;
        let deadline = self.deadline.min(Instant::now() + self.options.rpc);
        self.process.send_until(
            &json!({"id":id,"method":method,"params":params}),
            deadline,
            Some(&self.options.control),
        )?;
        loop {
            let v = self.receive(deadline, false)?;
            if v.get("method").is_some() {
                if self.pending.len() >= 32 {
                    return Err("protocol_error".into());
                }
                self.pending.push_back(v);
                continue;
            }
            if !self.response(&v, Some(id))? {
                continue;
            }
            if let Some(error) = v.get("error") {
                let code = error["code"].as_i64().ok_or("protocol_error")?;
                self.record("worker_event", json!({"rpc":method,"error_code":code}))?;
                return Err("rpc_error".into());
            }
            return Ok(v["result"].clone());
        }
    }
    fn bind_id(v: &Value) -> Result<String> {
        let s = v.as_str().ok_or("protocol_error")?;
        if s.is_empty() || s.len() > 256 {
            return Err("protocol_error".into());
        }
        Ok(s.into())
    }
    pub fn dispatch(&mut self, r: &Request) -> Result<()> {
        self.rpc("initialize",json!({"clientInfo":{"name":"devforgeai_worker_probe","version":"0.1.0"},"capabilities":{"experimentalApi":false}}))?;
        self.process.send_until(
            &json!({"method":"initialized","params":{}}),
            self.deadline.min(Instant::now() + self.options.rpc),
            Some(&self.options.control),
        )?;
        let account = self
            .rpc("account/read", json!({"refreshToken":false}))
            .map_err(|e| {
                if e == "rpc_error" {
                    "profile_unqualified".into()
                } else {
                    e
                }
            })?;
        if account["account"]["type"] != "chatgpt" || account["account"]["planType"] != "pro" {
            return Err("profile_unqualified".into());
        }
        let profile = r.profile()?;
        let (model, effort) = profile.as_ref().map_or(("test-model", "test-effort"), |p| {
            (p.model.as_str(), p.effort.as_str())
        });
        let mut cursor = Value::Null;
        let mut available = false;
        for _ in 0..10 {
            let list = self
                .rpc("model/list", json!({"limit":100,"cursor":cursor}))
                .map_err(|e| {
                    if e == "rpc_error" {
                        "profile_unqualified".into()
                    } else {
                        e
                    }
                })?;
            let models = list["data"].as_array().ok_or("protocol_error")?;
            if models.len() > 100 {
                return Err("protocol_error".into());
            }
            available |= models.iter().any(|m| {
                m["model"] == model
                    && m["supportedReasoningEfforts"]
                        .as_array()
                        .is_some_and(|a| a.iter().any(|e| e["reasoningEffort"] == effort))
            });
            cursor = list["nextCursor"].clone();
            if cursor.is_null() || available {
                break;
            }
            if !cursor.is_string() {
                return Err("protocol_error".into());
            }
        }
        if !available {
            return Err("profile_unqualified".into());
        }
        match self.rpc("account/rateLimits/read", json!({})) {
            Ok(limits) => {
                let exhausted = ["primary", "secondary"].iter().any(|k| {
                    limits["rateLimits"][k]["usedPercent"]
                        .as_f64()
                        .is_some_and(|n| n >= 100.0)
                });
                if exhausted {
                    return Err("rate_limit_exhausted".into());
                }
            }
            Err(e) if e == "rpc_error" => {
                self.record("worker_event", json!({"rate_limits":"not_measured"}))?
            }
            Err(e) => return Err(e),
        }
        self.record(
            "profile_checked",
            json!({"mode":"chatgpt","plan":"pro","model":model,"effort":effort}),
        )?;
        let thread=self.rpc("thread/start",json!({"model":model,"modelProvider":"openai","cwd":r.checkout_root,"sandbox":"read-only","approvalPolicy":"never","approvalsReviewer":"user","ephemeral":true}))?;
        if thread["model"] != model
            || thread["modelProvider"] != "openai"
            || thread["approvalPolicy"] != "never"
            || thread["approvalsReviewer"] != "user"
            || thread["cwd"] != json!(r.checkout_root)
            || thread["sandbox"]["type"] != "readOnly"
            || thread["sandbox"]["networkAccess"] != false
        {
            return Err("profile_unqualified".into());
        }
        self.thread = Some(Self::bind_id(&thread["thread"]["id"])?);
        self.record("thread_bound", json!({"thread_id":self.thread}))?;
        self.control()?;
        self.record("turn_intent", json!({"thread_id":self.thread}))?;
        let turn=self.rpc("turn/start",json!({"threadId":self.thread,"model":model,"effort":effort,"cwd":r.checkout_root,"approvalPolicy":"never","approvalsReviewer":"user","sandboxPolicy":{"type":"readOnly","networkAccess":false},"input":[{"type":"text","text":request::PROMPT}],"outputSchema":serde_json::from_str::<Value>(request::OUTPUT_SCHEMA).map_err(|_|"protocol_error")?}))?;
        self.turn = Some(Self::bind_id(&turn["turn"]["id"])?);
        self.record(
            "turn_bound",
            json!({"thread_id":self.thread,"turn_id":self.turn}),
        )?;
        if r.scenario == "cancel" {
            self.options.control.store(1, Ordering::SeqCst);
        }
        let mut completed = false;
        loop {
            if completed && self.pending.is_empty() {
                return Ok(());
            }
            if !completed {
                self.control()?;
            }
            let v = if let Some(v) = self.pending.pop_front() {
                v
            } else {
                self.receive(self.deadline, false)?
            };
            completed |= self.event(v)?;
        }
    }
    fn item(&mut self, item: &Value) -> Result<()> {
        let id = Self::bind_id(&item["id"])?;
        let kind = item["type"].as_str().ok_or("protocol_error")?;
        if kind == "reasoning" {
            return Ok(());
        }
        if kind != "agentMessage" {
            return Err("tool_activity".into());
        }
        if !item["text"].is_string()
            || !(item["phase"].is_null()
                || matches!(item["phase"].as_str(), Some("final_answer" | "commentary")))
        {
            return Err("protocol_error".into());
        }
        let selected = json!({"id":id,"type":kind,"text":item["text"],"phase":item["phase"]});
        if let Some(old) = self.items.insert(id, selected.clone())
            && old != selected
        {
            return Err("protocol_error".into());
        }
        Ok(())
    }
    fn event(&mut self, v: Value) -> Result<bool> {
        let Some(method) = v.get("method").and_then(Value::as_str) else {
            self.response(&v, None)?;
            return Ok(false);
        };
        let p = &v["params"];
        let known = matches!(
            method,
            "item/started"
                | "item/completed"
                | "item/agentMessage/delta"
                | "turn/started"
                | "turn/completed"
                | "thread/tokenUsage/updated"
        );
        if !known {
            self.record("worker_event",json!({"method":method.chars().take(128).collect::<String>(),"bytes":v.to_string().len(),"unknown":true}))?;
            return Ok(false);
        }
        if p["threadId"].as_str() != self.thread.as_deref() {
            return Err("protocol_error".into());
        }
        let turn_id = if method.starts_with("turn/") {
            &p["turn"]["id"]
        } else {
            &p["turnId"]
        };
        if turn_id.as_str() != self.turn.as_deref() {
            return Err("protocol_error".into());
        }
        match method {
            "item/completed" => self.item(&p["item"])?,
            "item/started" => {
                Self::bind_id(&p["item"]["id"])?;
                if !matches!(
                    p["item"]["type"].as_str(),
                    Some("agentMessage" | "reasoning")
                ) {
                    return Err("tool_activity".into());
                }
            }
            "item/agentMessage/delta" => {
                Self::bind_id(&p["itemId"])?;
                if !p["delta"].is_string() {
                    return Err("protocol_error".into());
                }
            }
            "thread/tokenUsage/updated" => {
                let u = &p["tokenUsage"];
                for scope in ["total", "last"] {
                    for key in [
                        "totalTokens",
                        "inputTokens",
                        "cachedInputTokens",
                        "outputTokens",
                        "reasoningOutputTokens",
                    ] {
                        if u[scope][key].as_u64().is_none() {
                            return Err("protocol_error".into());
                        }
                    }
                }
                let mut usage = serde_json::Map::new();
                for scope in ["total", "last"] {
                    let mut counters = serde_json::Map::new();
                    for key in [
                        "totalTokens",
                        "inputTokens",
                        "cachedInputTokens",
                        "outputTokens",
                        "reasoningOutputTokens",
                        "cacheWriteInputTokens",
                    ] {
                        if let Some(value) = u[scope].get(key) {
                            if !value.is_u64() {
                                return Err("protocol_error".into());
                            }
                            counters.insert(key.into(), value.clone());
                        }
                    }
                    usage.insert(scope.into(), Value::Object(counters));
                }
                self.usage = Value::Object(usage);
            }
            "turn/started" => {
                if p["turn"]["status"] != "inProgress" {
                    return Err("protocol_error".into());
                }
            }
            "turn/completed" => {
                if let Some(old) = &self.completed_observation {
                    if old != &v {
                        return Err("protocol_error".into());
                    }
                    return Ok(true);
                }
                let turn = &p["turn"];
                let status = turn["status"].as_str().ok_or("protocol_error")?;
                if !["completed", "interrupted", "failed"].contains(&status) {
                    return Err("protocol_error".into());
                }
                for item in turn["items"].as_array().ok_or("protocol_error")? {
                    self.item(item)?;
                }
                let category = error_category(&turn["error"]["codexErrorInfo"])?;
                self.record("worker_event",json!({"method":method,"thread_id":self.thread,"turn_id":self.turn,"status":status,"error_category":category}))?;
                if status == "failed" {
                    return Err("provider_failed".into());
                }
                if status == "interrupted" {
                    return Err("worker_interrupted".into());
                }
                let finals: Vec<_> = self
                    .items
                    .values()
                    .filter(|i| {
                        i["phase"] == "final_answer"
                            || i["phase"].is_null() && self.items.len() == 1
                    })
                    .collect();
                if finals.len() != 1
                    || !oracle::matches(finals[0]["text"].as_str().ok_or("oracle_mismatch")?)
                {
                    return Err("oracle_mismatch".into());
                }
                let result = finals[0]["text"].clone();
                self.record("worker_event",json!({"method":"final_result","thread_id":self.thread,"turn_id":self.turn,"text":result}))?;
                self.completed_observation = Some(v);
                return Ok(true);
            }
            _ => {}
        }
        self.record(
            "worker_event",
            json!({"method":method,"thread_id":self.thread,"turn_id":self.turn}),
        )?;
        Ok(false)
    }
    pub fn interrupt(&mut self) {
        let deadline = Instant::now() + self.options.grace;
        if self.thread.is_none() || self.turn.is_none() {
            self.process.close_input();
            self.process.wait_stopped(self.options.grace);
            return;
        }
        let id = self.next_id;
        self.next_id += 1;
        if self.process.send_until(&json!({"id":id,"method":"turn/interrupt","params":{"threadId":self.thread,"turnId":self.turn}}), deadline, None).is_err() {
            self.process.close_input();
            self.process.wait_stopped(deadline.saturating_duration_since(Instant::now()));
            return;
        }
        while Instant::now() < deadline {
            match self.receive(deadline, true) {
                Ok(v) if v.get("method").is_some() => {
                    if v["method"] == "turn/completed"
                        && v["params"]["threadId"].as_str() == self.thread.as_deref()
                        && v["params"]["turn"]["id"].as_str() == self.turn.as_deref()
                        && v["params"]["turn"]["status"] == "interrupted"
                    {
                        let _=self.record("worker_event",json!({"method":"turn/completed","status":"interrupted","thread_id":self.thread,"turn_id":self.turn}));
                        break;
                    }
                }
                Ok(v) => {
                    if self.response(&v, Some(id)).is_err() {
                        break;
                    }
                }
                Err(_) => break,
            }
        }
        self.process.close_input();
        self.process
            .wait_stopped(deadline.saturating_duration_since(Instant::now()));
    }
}
