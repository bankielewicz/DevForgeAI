Hybrid Architecture Analysis: CLI + Python Library + gRPC Service



&nbsp; A three-tier hybrid is not only possible but potentially optimal for TreeLint. Let me analyze this:



&nbsp; ---

&nbsp; Architecture Options Expanded



&nbsp; Option 5: Three-Tier Hybrid (CLI + Python Lib + gRPC Service)



&nbsp; Architecture Layers:



&nbsp; ┌─────────────────────────────────────────────────────────────┐

&nbsp; │ Layer 1: Rust Core (treelint binary)                       │

&nbsp; │   - Tree-sitter parsing engine                             │

&nbsp; │   - Query pattern matching                                 │

&nbsp; │   - AST caching and incremental updates                    │

&nbsp; └─────────────────────────────────────────────────────────────┘

&nbsp;                            ↓

&nbsp;         ┌──────────────────┴──────────────────┐

&nbsp;         ↓                  ↓                   ↓

&nbsp; ┌───────────────┐  ┌─────────────────┐  ┌──────────────────┐

&nbsp; │ Layer 2a:     │  │ Layer 2b:       │  │ Layer 2c:        │

&nbsp; │ CLI Interface │  │ Python Library  │  │ gRPC Service     │

&nbsp; │               │  │ (PyO3 bindings) │  │ (Optional daemon)│

&nbsp; └───────────────┘  └─────────────────┘  └──────────────────┘

&nbsp;         ↓                  ↓                   ↓

&nbsp; ┌───────────────┐  ┌─────────────────┐  ┌──────────────────┐

&nbsp; │ Use Case 1:   │  │ Use Case 2:     │  │ Use Case 3:      │

&nbsp; │ Manual use    │  │ DevForgeAI      │  │ Continuous       │

&nbsp; │ CI/CD         │  │ subagents       │  │ validation       │

&nbsp; │ External tools│  │ (direct import) │  │ (performance)    │

&nbsp; └───────────────┘  └─────────────────┘  └──────────────────┘



&nbsp; ---

&nbsp; Three-Tier Benefits



&nbsp; Layer 2a: CLI Interface (For Humans \& CI/CD)



&nbsp; Usage:

&nbsp; treelint analyze --pattern=anti-patterns src/

&nbsp; treelint query custom.scm src/



&nbsp; Best For:

&nbsp; - Manual debugging

&nbsp; - CI/CD pipelines (stateless)

&nbsp; - External tool integration

&nbsp; - Shell scripting



&nbsp; DevForgeAI Use Case:

&nbsp; - Fallback when service unavailable

&nbsp; - CI/CD environments (ephemeral runners)



&nbsp; ---

&nbsp; Layer 2b: Python Library (For DevForgeAI Subagents)



&nbsp; Usage:

&nbsp; # Direct import (zero subprocess overhead)

&nbsp; import treelint



&nbsp; analyzer = treelint.Analyzer(workspace=".")

&nbsp; violations = analyzer.query\_pattern("anti-patterns", "src/")

&nbsp; # Returns native Python objects



&nbsp; Best For:

&nbsp; - DevForgeAI Python subagents (context-validator, security-auditor)

&nbsp; - Python QA scripts

&nbsp; - Tight integration (no JSON parsing)



&nbsp; Token Savings:

&nbsp; - CLI invocation: ~500 tokens

&nbsp; - Library import: ~100 tokens

&nbsp; - Savings: 80%



&nbsp; ---

&nbsp; Layer 2c: gRPC Service (For Performance)



&nbsp; Usage:

&nbsp; # Start service (optional)

&nbsp; treelint serve start



&nbsp; # CLI auto-detects service

&nbsp; treelint query --pattern=anti-patterns src/

&nbsp; # Uses gRPC service if available (cached AST)

&nbsp; # Falls back to CLI mode if service down



&nbsp; Best For:

&nbsp; - Large codebases (100K+ lines)

&nbsp; - Continuous validation (watch mode)

&nbsp; - Real-time feedback during development

&nbsp; - Multiple concurrent queries



&nbsp; Performance:

&nbsp; Without service (CLI mode):

&nbsp;   Query 1: 500ms (parse + query)

&nbsp;   Query 2: 500ms (re-parse + query)

&nbsp;   Query 3: 500ms (re-parse + query)

&nbsp;   Total: 1,500ms



&nbsp; With service (gRPC mode):

&nbsp;   Initial: 500ms (parse + cache)

&nbsp;   Query 1: 50ms (cached AST)

&nbsp;   Query 2: 50ms (cached AST)

&nbsp;   Query 3: 50ms (cached AST)

&nbsp;   Total: 650ms (57% faster)



&nbsp; ---

&nbsp; Implementation Complexity



&nbsp; Option 2: CLI + Python Library



&nbsp; Complexity: Medium-High

&nbsp; - Rust CLI: Base complexity

&nbsp; - PyO3 bindings: +8 points

&nbsp; - Python packaging: +4 points

&nbsp; - Total: Base + 12



&nbsp; Option 3: CLI + gRPC Service



&nbsp; Complexity: High

&nbsp; - Rust CLI: Base complexity

&nbsp; - gRPC server (tonic): +10 points

&nbsp; - Filesystem watching: +5 points

&nbsp; - State management: +6 points

&nbsp; - Total: Base + 21



&nbsp; Option 5: CLI + Python Lib + gRPC Service



&nbsp; Complexity: Very High

&nbsp; - Rust CLI: Base complexity

&nbsp; - PyO3 bindings: +8 points

&nbsp; - gRPC service: +10 points

&nbsp; - Auto-detection logic: +4 points

&nbsp; - Total: Base + 22



&nbsp; But...

&nbsp; - Layers are independent (can develop incrementally)

&nbsp; - Python lib works standalone (doesn't require service)

&nbsp; - Service works standalone (doesn't require Python lib)

&nbsp; - Only ~1 additional complexity point for "glue code"



&nbsp; ---

&nbsp; Incremental Implementation Path



&nbsp; Phase 1 (v1.0): CLI-Only + Hybrid Grammars



&nbsp; Timeline: 3-4 weeks

&nbsp; Deliverables:

&nbsp; - Rust binary with 5 bundled grammars

&nbsp; - CLI interface (analyze, query commands)

&nbsp; - JSON output for DevForgeAI integration

&nbsp; - Auto-install for non-bundled grammars



&nbsp; DevForgeAI Integration:

&nbsp; # Subprocess invocation

&nbsp; subprocess.run(\['treelint', 'query', ...])



&nbsp; Complexity: Medium (Base + 12 for grammar bundling)



&nbsp; ---

&nbsp; Phase 2 (v1.1): Add Python Library



&nbsp; Timeline: 1-2 weeks (incremental)

&nbsp; Deliverables:

&nbsp; - PyO3 bindings for core analyzer

&nbsp; - Python package: pip install treelint

&nbsp; - Native Python API (no subprocess)



&nbsp; DevForgeAI Integration:

&nbsp; # Direct import (80% token savings)

&nbsp; import treelint

&nbsp; violations = treelint.query\_pattern("anti-patterns", "src/")



&nbsp; Complexity: +8 points (PyO3, Python packaging)



&nbsp; ---

&nbsp; Phase 3 (v1.2): Add gRPC Service



&nbsp; Timeline: 2-3 weeks (incremental)

&nbsp; Deliverables:

&nbsp; - gRPC server (tonic crate)

&nbsp; - Filesystem watching (notify crate)

&nbsp; - AST caching with incremental updates

&nbsp; - Service management commands



&nbsp; DevForgeAI Integration:

&nbsp; # Python library auto-detects service

&nbsp; import treelint



&nbsp; analyzer = treelint.Analyzer()  # Detects gRPC service if running

&nbsp; violations = analyzer.query\_pattern("anti-patterns", "src/")

&nbsp; # Uses gRPC if available (fast), falls back to direct parse (reliable)



&nbsp; Complexity: +14 points (gRPC, watching, caching, auto-detection)



&nbsp; ---

&nbsp; Three-Tier Architecture Details



&nbsp; Rust Core Implementation



&nbsp; // src/lib.rs - Core library (used by all layers)

&nbsp; pub struct TreeLintAnalyzer {

&nbsp;     workspace: PathBuf,

&nbsp;     parser: Parser,

&nbsp;     grammar\_manager: GrammarManager,

&nbsp; }



&nbsp; impl TreeLintAnalyzer {

&nbsp;     pub fn query\_pattern(\&mut self, pattern: \&str, path: \&str) -> Result<Vec<Violation>> {

&nbsp;         let language = self.detect\_language(path)?;

&nbsp;         let grammar = self.grammar\_manager.get\_grammar(language)?;



&nbsp;         self.parser.set\_language(grammar)?;

&nbsp;         let tree = self.parser.parse\_file(path)?;



&nbsp;         let query = self.load\_pattern(pattern)?;

&nbsp;         let matches = query.matches(tree.root\_node());



&nbsp;         Ok(self.extract\_violations(matches))

&nbsp;     }

&nbsp; }



&nbsp; ---

&nbsp; Layer 2a: CLI (main.rs)



&nbsp; // src/main.rs

&nbsp; use clap::{Parser, Subcommand};

&nbsp; use treelint::TreeLintAnalyzer;



&nbsp; #\[derive(Parser)]

&nbsp; struct Cli {

&nbsp;     #\[command(subcommand)]

&nbsp;     command: Commands,

&nbsp; }



&nbsp; #\[derive(Subcommand)]

&nbsp; enum Commands {

&nbsp;     Analyze {

&nbsp;         #\[arg(long)]

&nbsp;         pattern: String,

&nbsp;         path: PathBuf,

&nbsp;     },

&nbsp;     Query {

&nbsp;         query\_file: PathBuf,

&nbsp;         path: PathBuf,

&nbsp;     },

&nbsp;     Serve(ServeCommand),

&nbsp; }



&nbsp; fn main() -> Result<()> {

&nbsp;     let cli = Cli::parse();



&nbsp;     match cli.command {

&nbsp;         Commands::Analyze { pattern, path } => {

&nbsp;             let mut analyzer = TreeLintAnalyzer::new(".")?;

&nbsp;             let violations = analyzer.query\_pattern(\&pattern, \&path)?;

&nbsp;             println!("{}", serde\_json::to\_string\_pretty(\&violations)?);

&nbsp;         }

&nbsp;         // ... other commands

&nbsp;     }

&nbsp; }



&nbsp; ---

&nbsp; Layer 2b: Python Library (PyO3)



&nbsp; // src/python.rs (optional, v1.1+)

&nbsp; use pyo3::prelude::\*;



&nbsp; #\[pyclass]

&nbsp; struct Analyzer {

&nbsp;     inner: TreeLintAnalyzer,

&nbsp;     service\_client: Option<ServiceClient>,

&nbsp; }



&nbsp; #\[pymethods]

&nbsp; impl Analyzer {

&nbsp;     #\[new]

&nbsp;     fn new(workspace: Option<String>) -> PyResult<Self> {

&nbsp;         let workspace = workspace.unwrap\_or\_else(|| ".".to\_string());



&nbsp;         // Auto-detect gRPC service

&nbsp;         let service\_client = ServiceClient::try\_connect("localhost:50051").ok();



&nbsp;         Ok(Analyzer {

&nbsp;             inner: TreeLintAnalyzer::new(\&workspace)?,

&nbsp;             service\_client,

&nbsp;         })

&nbsp;     }



&nbsp;     fn query\_pattern(\&mut self, pattern: \&str, path: \&str) -> PyResult<Vec<Violation>> {

&nbsp;         // Use service if available (fast)

&nbsp;         if let Some(client) = \&self.service\_client {

&nbsp;             if let Ok(result) = client.query(pattern, path) {

&nbsp;                 return Ok(result);

&nbsp;             }

&nbsp;         }



&nbsp;         // Fallback to direct parse (reliable)

&nbsp;         Ok(self.inner.query\_pattern(pattern, path)?)

&nbsp;     }

&nbsp; }



&nbsp; #\[pymodule]

&nbsp; fn treelint(\_py: Python, m: \&PyModule) -> PyResult<()> {

&nbsp;     m.add\_class::<Analyzer>()?;

&nbsp;     Ok(())

&nbsp; }



&nbsp; Python Usage:

&nbsp; import treelint



&nbsp; # Auto-detects service, falls back to direct parsing

&nbsp; analyzer = treelint.Analyzer(workspace=".")

&nbsp; violations = analyzer.query\_pattern("anti-patterns", "src/")



&nbsp; ---

&nbsp; Layer 2c: gRPC Service (Optional)



&nbsp; // src/service.rs (optional, v1.2+)

&nbsp; use tonic::{transport::Server, Request, Response, Status};



&nbsp; pub struct TreeLintService {

&nbsp;     cache: Arc<RwLock<AstCache>>,

&nbsp;     watcher: FileWatcher,

&nbsp; }



&nbsp; #\[tonic::async\_trait]

&nbsp; impl treelint\_proto::code\_lens\_server::TreeLint for TreeLintService {

&nbsp;     async fn query(

&nbsp;         \&self,

&nbsp;         request: Request<QueryRequest>,

&nbsp;     ) -> Result<Response<QueryResponse>, Status> {

&nbsp;         let req = request.into\_inner();



&nbsp;         // Use cached AST (incremental parsing)

&nbsp;         let cache = self.cache.read().await;

&nbsp;         let tree = cache.get\_tree(\&req.path)

&nbsp;             .ok\_or\_else(|| Status::not\_found("File not in cache"))?;



&nbsp;         // Execute query on cached tree

&nbsp;         let violations = execute\_query(\&req.pattern, tree)?;



&nbsp;         Ok(Response::new(QueryResponse { violations }))

&nbsp;     }

&nbsp; }



&nbsp; // Start server

&nbsp; #\[tokio::main]

&nbsp; async fn main() -> Result<()> {

&nbsp;     let service = TreeLintService::new(".")?;



&nbsp;     Server::builder()

&nbsp;         .add\_service(TreeLintServer::new(service))

&nbsp;         .serve("127.0.0.1:50051".parse()?)

&nbsp;         .await?;



&nbsp;     Ok(())

&nbsp; }



&nbsp; ---

&nbsp; DevForgeAI Integration Patterns (Three-Tier)



&nbsp; Pattern 1: Simple (CLI Only - v1.0)



&nbsp; # context-validator subagent

&nbsp; import subprocess

&nbsp; import json



&nbsp; result = subprocess.run(\['treelint', 'query', '--pattern=layer-boundaries', 'src/'],

&nbsp;                        capture\_output=True, text=True, check=True)

&nbsp; violations = json.loads(result.stdout)



&nbsp; Token Cost: ~500 tokens

&nbsp; Performance: 500ms per query

&nbsp; Pros: Works immediately, no dependencies

&nbsp; Cons: Slower, subprocess overhead



&nbsp; ---

&nbsp; Pattern 2: Optimized (Python Library - v1.1)



&nbsp; # context-validator subagent (with Python library)

&nbsp; import treelint



&nbsp; # Library auto-detects service, falls back to direct parsing

&nbsp; analyzer = treelint.Analyzer(workspace=".")

&nbsp; violations = analyzer.query\_pattern("layer-boundaries", "src/")



&nbsp; Token Cost: ~100 tokens (80% savings)

&nbsp; Performance: 500ms without service, 50ms with service

&nbsp; Pros: Zero subprocess overhead, native Python objects

&nbsp; Cons: Requires Python package installation



&nbsp; ---

&nbsp; Pattern 3: Maximum Performance (Service - v1.2)



&nbsp; # context-validator subagent (with service)

&nbsp; import treelint



&nbsp; # Start service once (in /dev command initialization)

&nbsp; treelint.ensure\_service\_running(workspace=".")



&nbsp; # All subsequent queries use cached AST

&nbsp; analyzer = treelint.Analyzer()  # Connects to service

&nbsp; violations = analyzer.query\_pattern("layer-boundaries", "src/")



&nbsp; Token Cost: ~100 tokens

&nbsp; Performance: 50ms per query (90% faster)

&nbsp; Pros: Maximum performance, continuous validation

&nbsp; Cons: Requires service management



&nbsp; ---

&nbsp; Recommended Three-Tier Architecture



&nbsp; 🎯 RECOMMENDED: Progressive Enhancement Pattern



&nbsp; v1.0 (Weeks 1-4): CLI-Only

&nbsp; Rust binary (CLI interface)

&nbsp;   ↓

&nbsp; DevForgeAI: Bash subprocess invocation



&nbsp; v1.1 (Weeks 5-6): Add Python Library

&nbsp; Rust binary + PyO3 bindings

&nbsp;   ↓

&nbsp; Python package (pip install treelint)

&nbsp;   ↓

&nbsp; DevForgeAI: Direct Python import (80% token savings)



&nbsp; v1.2 (Weeks 7-9): Add gRPC Service

&nbsp; Rust binary + Python library + gRPC daemon

&nbsp;   ↓

&nbsp; Service mode (optional performance boost)

&nbsp;   ↓

&nbsp; DevForgeAI: Python library auto-detects service



&nbsp; Each layer is independent and backward-compatible.



&nbsp; ---

&nbsp; Implementation Strategy



&nbsp; Phase 1: Rust Core + CLI (v1.0)



&nbsp; Crates:

&nbsp; \[dependencies]

&nbsp; tree-sitter = "0.20"

&nbsp; clap = { version = "4.4", features = \["derive"] }

&nbsp; serde = { version = "1.0", features = \["derive"] }

&nbsp; serde\_json = "1.0"

&nbsp; anyhow = "1.0"



&nbsp; Entry Point:

&nbsp; // src/main.rs

&nbsp; fn main() -> Result<()> {

&nbsp;     let cli = Cli::parse();

&nbsp;     let analyzer = TreeLintAnalyzer::new(\&cli.workspace)?;



&nbsp;     match cli.command {

&nbsp;         Commands::Analyze { pattern, path } => {

&nbsp;             let violations = analyzer.query\_pattern(\&pattern, \&path)?;

&nbsp;             println!("{}", serde\_json::to\_string\_pretty(\&violations)?);

&nbsp;         }

&nbsp;     }

&nbsp; }



&nbsp; DevForgeAI Integration:

&nbsp; # Simple subprocess call

&nbsp; subprocess.run(\['treelint', 'query', ...])



&nbsp; Milestone: Functional CLI tool, works in DevForgeAI



&nbsp; ---

&nbsp; Phase 2: Add Python Bindings (v1.1)



&nbsp; Additional Crates:

&nbsp; \[dependencies]

&nbsp; pyo3 = { version = "0.20", features = \["extension-module"], optional = true }



&nbsp; \[lib]

&nbsp; name = "treelint"

&nbsp; crate-type = \["cdylib", "rlib"]  # Both Python extension and Rust library



&nbsp; \[features]

&nbsp; python = \["pyo3"]



&nbsp; Python Module:

&nbsp; // src/python.rs

&nbsp; use pyo3::prelude::\*;



&nbsp; #\[pyclass]

&nbsp; struct Analyzer {

&nbsp;     inner: TreeLintAnalyzer,

&nbsp; }



&nbsp; #\[pymethods]

&nbsp; impl Analyzer {

&nbsp;     #\[new]

&nbsp;     fn new(workspace: Option<String>) -> PyResult<Self> {

&nbsp;         Ok(Analyzer {

&nbsp;             inner: TreeLintAnalyzer::new(\&workspace.unwrap\_or(".".into()))?,

&nbsp;         })

&nbsp;     }



&nbsp;     fn query\_pattern(\&mut self, pattern: \&str, path: \&str) -> PyResult<Vec<Violation>> {

&nbsp;         Ok(self.inner.query\_pattern(pattern, path)?)

&nbsp;     }

&nbsp; }



&nbsp; #\[pymodule]

&nbsp; fn treelint(\_py: Python, m: \&PyModule) -> PyResult<()> {

&nbsp;     m.add\_class::<Analyzer>()?;

&nbsp;     Ok(())

&nbsp; }



&nbsp; Build:

&nbsp; # Build Python wheel

&nbsp; maturin build --release



&nbsp; # Install

&nbsp; pip install target/wheels/treelint-\*.whl



&nbsp; DevForgeAI Integration:

&nbsp; # Direct import (80% token savings)

&nbsp; import treelint

&nbsp; analyzer = treelint.Analyzer()

&nbsp; violations = analyzer.query\_pattern("anti-patterns", "src/")



&nbsp; Milestone: Zero-overhead DevForgeAI integration



&nbsp; ---

&nbsp; Phase 3: Add gRPC Service (v1.2)



&nbsp; Additional Crates:

&nbsp; \[dependencies]

&nbsp; # gRPC server

&nbsp; tonic = { version = "0.11", optional = true }

&nbsp; prost = { version = "0.12", optional = true }



&nbsp; # Async runtime

&nbsp; tokio = { version = "1.35", features = \["full"], optional = true }



&nbsp; # Filesystem watching

&nbsp; notify = { version = "6.1", optional = true }



&nbsp; \[build-dependencies]

&nbsp; tonic-build = "0.11"  # Compile .proto files



&nbsp; \[features]

&nbsp; service = \["tonic", "prost", "tokio", "notify"]



&nbsp; gRPC Protocol Definition:

&nbsp; // proto/treelint.proto

&nbsp; syntax = "proto3";

&nbsp; package treelint;



&nbsp; service TreeLint {

&nbsp;     rpc Query(QueryRequest) returns (QueryResponse);

&nbsp;     rpc Watch(WatchRequest) returns (stream FileChange);

&nbsp;     rpc GetHealth(HealthRequest) returns (HealthResponse);

&nbsp; }



&nbsp; message QueryRequest {

&nbsp;     string pattern = 1;

&nbsp;     string path = 2;

&nbsp;     string workspace = 3;

&nbsp; }



&nbsp; message QueryResponse {

&nbsp;     repeated Violation violations = 1;

&nbsp;     uint32 cache\_hit = 2;

&nbsp;     uint32 parse\_time\_ms = 3;

&nbsp; }



&nbsp; Service Implementation:

&nbsp; // src/service.rs

&nbsp; #\[tonic::async\_trait]

&nbsp; impl TreeLint for TreeLintService {

&nbsp;     async fn query(\&self, req: Request<QueryRequest>) -> Result<Response<QueryResponse>, Status> {

&nbsp;         let req = req.into\_inner();



&nbsp;         // Check cache first

&nbsp;         let cache = self.cache.read().await;

&nbsp;         if let Some(tree) = cache.get(\&req.path) {

&nbsp;             // Fast path: Use cached AST

&nbsp;             let violations = self.execute\_query(\&req.pattern, tree)?;

&nbsp;             return Ok(Response::new(QueryResponse {

&nbsp;                 violations,

&nbsp;                 cache\_hit: true,

&nbsp;                 parse\_time\_ms: 0,

&nbsp;             }));

&nbsp;         }

&nbsp;         drop(cache);



&nbsp;         // Slow path: Parse and cache

&nbsp;         let tree = self.parse\_and\_cache(\&req.path).await?;

&nbsp;         let violations = self.execute\_query(\&req.pattern, \&tree)?;



&nbsp;         Ok(Response::new(QueryResponse {

&nbsp;             violations,

&nbsp;             cache\_hit: false,

&nbsp;             parse\_time\_ms: tree.parse\_duration\_ms,

&nbsp;         }))

&nbsp;     }

&nbsp; }



&nbsp; Python Library Enhancement:

&nbsp; # Python library auto-detects gRPC service

&nbsp; import treelint



&nbsp; # Transparently uses service if available

&nbsp; analyzer = treelint.Analyzer()

&nbsp; violations = analyzer.query\_pattern("anti-patterns", "src/")

&nbsp; # Internally: Checks localhost:50051, uses gRPC if available, else direct parse



&nbsp; Milestone: Maximum performance for power users



&nbsp; ---

&nbsp; Auto-Detection Logic (Three-Tier)



&nbsp; Smart Client Selection



&nbsp; # Python library (treelint/\_\_init\_\_.py)

&nbsp; class Analyzer:

&nbsp;     def \_\_init\_\_(self, workspace="."):

&nbsp;         self.workspace = workspace



&nbsp;         # Try gRPC service first

&nbsp;         self.service\_client = self.\_try\_connect\_service()



&nbsp;         # Fallback to native Rust library (PyO3)

&nbsp;         self.native\_analyzer = None

&nbsp;         if not self.service\_client:

&nbsp;             try:

&nbsp;                 from . import \_treelint\_native  # PyO3 extension

&nbsp;                 self.native\_analyzer = \_treelint\_native.Analyzer(workspace)

&nbsp;             except ImportError:

&nbsp;                 pass  # Will use CLI fallback



&nbsp;     def query\_pattern(self, pattern: str, path: str):

&nbsp;         # 1. Try gRPC service (fastest, ~50ms)

&nbsp;         if self.service\_client:

&nbsp;             try:

&nbsp;                 return self.service\_client.query(pattern, path)

&nbsp;             except Exception:

&nbsp;                 pass  # Fallback to next option



&nbsp;         # 2. Try native library (fast, ~500ms)

&nbsp;         if self.native\_analyzer:

&nbsp;             return self.native\_analyzer.query\_pattern(pattern, path)



&nbsp;         # 3. Fallback to CLI subprocess (always works)

&nbsp;         import subprocess

&nbsp;         result = subprocess.run(

&nbsp;             \['treelint', 'query', '--pattern', pattern, path],

&nbsp;             capture\_output=True, text=True, check=True

&nbsp;         )

&nbsp;         return json.loads(result.stdout)



&nbsp; Benefit: Optimal performance when available, guaranteed reliability always



&nbsp; ---

&nbsp; DevForgeAI Subagent Integration (Final Form)



&nbsp; context-validator Enhanced



&nbsp; # .claude/agents/context-validator.md



&nbsp; import treelint



&nbsp; # Initialize once per validation session

&nbsp; analyzer = treelint.Analyzer(workspace=".")



&nbsp; def validate\_layer\_boundaries() -> list\[dict]:

&nbsp;     """

&nbsp;     Validate architectural layer boundaries using TreeLint.



&nbsp;     Performance modes:

&nbsp;     - With gRPC service: ~50ms (cached AST)

&nbsp;     - Without service (PyO3): ~500ms (direct parse)

&nbsp;     - Fallback (CLI): ~600ms (subprocess + parse)



&nbsp;     Auto-detects best available method.

&nbsp;     """

&nbsp;     violations = analyzer.query\_pattern(

&nbsp;         pattern="layer-boundaries",

&nbsp;         path="src/domain/"

&nbsp;     )



&nbsp;     if violations:

&nbsp;         for v in violations:

&nbsp;             log\_violation(

&nbsp;                 file=v\['file'],

&nbsp;                 line=v\['line'],

&nbsp;                 message=f"Layer boundary violation: {v\['message']}"

&nbsp;             )



&nbsp;     return violations



&nbsp; def validate\_dependency\_injection() -> list\[dict]:

&nbsp;     """Detect direct instantiation (violates DI pattern)."""

&nbsp;     violations = analyzer.query\_pattern(

&nbsp;         pattern="direct-instantiation",

&nbsp;         path="src/"

&nbsp;     )

&nbsp;     return violations



&nbsp; def validate\_anti\_patterns() -> list\[dict]:

&nbsp;     """Check all anti-patterns from anti-patterns.md."""

&nbsp;     patterns = \[

&nbsp;         "god-objects",

&nbsp;         "sql-concatenation",

&nbsp;         "hardcoded-secrets",

&nbsp;         "magic-numbers",

&nbsp;     ]



&nbsp;     all\_violations = \[]

&nbsp;     for pattern in patterns:

&nbsp;         violations = analyzer.query\_pattern(pattern, "src/")

&nbsp;         all\_violations.extend(violations)



&nbsp;     return all\_violations



&nbsp; Token Efficiency:

&nbsp; - Without service: ~100 tokens per query (PyO3 direct call)

&nbsp; - With service: ~100 tokens per query (gRPC auto-detected)

&nbsp; - Multiple patterns: 3x 100 = 300 tokens (vs 3x 500 = 1,500 with subprocess)



&nbsp; Savings: 80%



&nbsp; ---

&nbsp; Installation Experience



&nbsp; For End Users



&nbsp; v1.0: CLI Binary

&nbsp; # Download single binary (25MB with 5 bundled grammars)

&nbsp; curl -L .../treelint-linux -o /usr/local/bin/treelint

&nbsp; chmod +x /usr/local/bin/treelint



&nbsp; # Ready to use

&nbsp; treelint analyze --pattern=anti-patterns src/



&nbsp; v1.1: CLI + Python Library

&nbsp; # Binary already installed (from v1.0)



&nbsp; # Add Python library

&nbsp; pip install treelint

&nbsp; # Downloads wheel (~5MB, contains PyO3 bindings)



&nbsp; # Now can import in Python

&nbsp; python -c "import treelint; print(treelint.\_\_version\_\_)"



&nbsp; v1.2: CLI + Python + Service

&nbsp; # Binary and Python lib already installed



&nbsp; # Service mode is opt-in

&nbsp; treelint serve start --workspace=.



&nbsp; # Python library auto-detects service

&nbsp; python -c "import treelint; a = treelint.Analyzer(); print(a.using\_service)"

&nbsp; # True (using gRPC service)



&nbsp; # Stop service

&nbsp; treelint serve stop



&nbsp; Progressive enhancement - each layer adds capability without breaking previous layers.



&nbsp; ---

&nbsp; Recommendation



&nbsp; 🎯 BUILD: Three-Tier Hybrid (Incremental)



&nbsp; Answer for Claude's Ideation:



&nbsp; Architecture pattern: Three-tier hybrid (progressive enhancement)



&nbsp; v1.0 (Initial): CLI-only tool

&nbsp; - Pure Rust binary with CLI interface

&nbsp; - Invoked via Bash tool from DevForgeAI subagents

&nbsp; - JSON output for machine parsing

&nbsp; - Works immediately after installation

&nbsp; - Standard Unix tool pattern



&nbsp; v1.1 (Enhancement): Add Python Library

&nbsp; - PyO3 bindings to Rust core

&nbsp; - pip install treelint (Python package)

&nbsp; - Direct library import in DevForgeAI subagents

&nbsp; - 80% token reduction (100 vs 500 tokens per query)

&nbsp; - Zero subprocess overhead



&nbsp; v1.2 (Performance): Add gRPC Service

&nbsp; - Optional background daemon (treelint serve start)

&nbsp; - AST caching with filesystem watching

&nbsp; - Incremental parsing (50ms vs 500ms)

&nbsp; - Python library auto-detects service

&nbsp; - Graceful fallback to direct parsing



&nbsp; Auto-Detection Logic:

&nbsp; - Python library tries: gRPC service → PyO3 native → CLI subprocess

&nbsp; - Uses fastest available method automatically

&nbsp; - Transparent to user (developer doesn't choose)



&nbsp; Why This Approach:

&nbsp; 1. Start simple (CLI works for everyone)

&nbsp; 2. Optimize integration (Python library for DevForgeAI)

&nbsp; 3. Add performance (service for large codebases)

&nbsp; 4. Each layer independent (can skip v1.2 if service not needed)

&nbsp; 5. Learn Rust incrementally (FFI → PyO3 → async/gRPC)



&nbsp; DevForgeAI Integration Evolution:

&nbsp; - v1.0: subprocess.run(\['treelint', ...]) - Works but slower

&nbsp; - v1.1: import treelint; analyzer.query(...) - Fast, low tokens

&nbsp; - v1.2: Same API, 10x faster (service caching)



&nbsp; Implementation Priority:

&nbsp; - v1.0 (CLI): CRITICAL - Foundation, immediate DevForgeAI integration

&nbsp; - v1.1 (Python): HIGH - 80% token savings, better DX

&nbsp; - v1.2 (Service): MEDIUM - Performance optimization, not required



&nbsp; Timeline:

&nbsp; - v1.0: Weeks 1-4 (CLI + grammar bundling)

&nbsp; - v1.1: Weeks 5-6 (PyO3 bindings + Python packaging)

&nbsp; - v1.2: Weeks 7-9 (gRPC service + filesystem watching)



&nbsp; This progressive approach allows shipping value early (v1.0) while building toward optimal integration (v1.2).



&nbsp; ---

&nbsp; Why Three-Tier is Better Than Two-Tier



&nbsp; Option 2 (CLI + Python) Limitations



&nbsp; Without gRPC Service:

&nbsp; - Every query re-parses files (500ms each)

&nbsp; - Light QA runs 4x per story = 2 seconds overhead

&nbsp; - No incremental parsing benefits

&nbsp; - Misses tree-sitter's main strength (caching)



&nbsp; Option 3 (CLI + gRPC) Limitations



&nbsp; Without Python Library:

&nbsp; - DevForgeAI still uses subprocess (500 token overhead)

&nbsp; - JSON serialization/deserialization overhead

&nbsp; - No token efficiency gains

&nbsp; - Complex integration for simple cases



&nbsp; Option 5 (Three-Tier) Advantages



&nbsp; Best of All Worlds:

&nbsp; - ✅ Simple cases: CLI subprocess (v1.0)

&nbsp; - ✅ DevForgeAI integration: Python import (v1.1)

&nbsp; - ✅ Performance: gRPC service (v1.2)

&nbsp; - ✅ Graceful degradation: Auto-fallback at each layer

&nbsp; - ✅ User choice: Pick complexity level (CLI-only? +Python? +Service?)



&nbsp; ---

&nbsp; Learning Path with Three-Tier



&nbsp; Rust Skills Acquired



&nbsp; v1.0 Phase (CLI):

&nbsp; - ✅ Rust fundamentals (ownership, borrowing)

&nbsp; - ✅ CLI development (clap)

&nbsp; - ✅ Tree-sitter FFI (unsafe blocks)

&nbsp; - ✅ Error handling (Result, anyhow)

&nbsp; - ✅ Cross-compilation



&nbsp; v1.1 Phase (Python Library):

&nbsp; - ✅ PyO3 (Rust ↔ Python interop)

&nbsp; - ✅ Memory management across FFI

&nbsp; - ✅ Python type conversion

&nbsp; - ✅ Packaging (maturin, wheels)



&nbsp; v1.2 Phase (gRPC Service):

&nbsp; - ✅ Async Rust (tokio)

&nbsp; - ✅ gRPC (tonic, prost)

&nbsp; - ✅ Concurrent data structures (Arc, RwLock)

&nbsp; - ✅ Filesystem watching (notify)

&nbsp; - ✅ Service architecture



&nbsp; By completion: Production-grade Rust expertise across CLI, FFI, async, and services



&nbsp; ---

&nbsp; Token Efficiency Comparison



&nbsp; Light QA Validation (4 queries per story)



&nbsp; v1.0 (CLI only):

&nbsp; Query 1: subprocess call = 500 tokens

&nbsp; Query 2: subprocess call = 500 tokens

&nbsp; Query 3: subprocess call = 500 tokens

&nbsp; Query 4: subprocess call = 500 tokens

&nbsp; Total: 2,000 tokens per story



&nbsp; v1.1 (CLI + Python Library):

&nbsp; Query 1: Python import = 100 tokens

&nbsp; Query 2: Python import = 100 tokens

&nbsp; Query 3: Python import = 100 tokens

&nbsp; Query 4: Python import = 100 tokens

&nbsp; Total: 400 tokens per story (80% savings)



&nbsp; v1.2 (CLI + Python + Service):

&nbsp; Query 1: Python import = 100 tokens (same as v1.1)

&nbsp; Query 2-4: Same 100 tokens each

&nbsp; Total: 400 tokens per story (same as v1.1)



&nbsp; BUT: Performance improves (500ms → 50ms per query)



&nbsp; Token Savings: v1.1 and v1.2 both achieve 80% reduction

&nbsp; Performance Savings: v1.2 adds 90% speed improvement



&nbsp; ---

&nbsp; Answer for Ideation Session



&nbsp; Complete Response for Claude



&nbsp; Architecture pattern: Three-tier hybrid with progressive enhancement



&nbsp; Layer 1 - Rust Core (Always):

&nbsp; - Core tree-sitter parsing engine

&nbsp; - Query pattern matching

&nbsp; - Grammar management

&nbsp; - Violation detection logic



&nbsp; Layer 2a - CLI Interface (v1.0):

&nbsp; - Command-line tool invoked via Bash

&nbsp; - JSON output for automation

&nbsp; - Works immediately after binary installation

&nbsp; - Standard Unix tool pattern

&nbsp; - DevForgeAI Integration: subprocess.run(\['treelint', ...])



&nbsp; Layer 2b - Python Library (v1.1):

&nbsp; - PyO3 bindings to Rust core

&nbsp; - pip install treelint (Python package)

&nbsp; - Direct import in DevForgeAI subagents

&nbsp; - Native Python objects (no JSON parsing)

&nbsp; - 80% token reduction (100 vs 500 tokens per query)

&nbsp; - DevForgeAI Integration: import treelint; analyzer.query(...)



&nbsp; Layer 2c - gRPC Service (v1.2):

&nbsp; - Optional background daemon for performance

&nbsp; - AST caching with incremental parsing

&nbsp; - Filesystem watching for real-time updates

&nbsp; - Python library auto-detects and uses service

&nbsp; - 90% performance improvement (50ms vs 500ms)

&nbsp; - DevForgeAI Integration: Same Python API, 10x faster



&nbsp; Auto-Detection Strategy:

&nbsp; Python library attempts in order:

&nbsp; 1. gRPC service (if running) → 50ms, cached AST

&nbsp; 2. PyO3 native (if available) → 500ms, direct parse

&nbsp; 3. CLI subprocess (always works) → 600ms, subprocess + parse



&nbsp; Why Three-Tier:

&nbsp; 1. Ship value early (v1.0 CLI works in DevForgeAI immediately)

&nbsp; 2. Optimize integration (v1.1 Python lib = 80% token savings)

&nbsp; 3. Add performance (v1.2 service = 90% speed improvement)

&nbsp; 4. Each layer independent (can stop at v1.1 if service not needed)

&nbsp; 5. Learn Rust progressively (CLI → PyO3 → async gRPC)



&nbsp; Implementation Priority:

&nbsp; - v1.0: CRITICAL (foundation, immediate DevForgeAI value)

&nbsp; - v1.1: HIGH (massive token savings for subagents)

&nbsp; - v1.2: MEDIUM (performance boost, optional)



&nbsp; Binary Distribution:

&nbsp; - v1.0: Single Rust binary (~25MB with 5 bundled grammars)

&nbsp; - v1.1: Rust binary + Python wheel (~30MB total)

&nbsp; - v1.2: Same binaries + service mode (no size increase)



&nbsp; This architecture allows DevForgeAI to start using TreeLint immediately (v1.0) while building toward optimal

&nbsp; integration (v1.1) and maximum performance (v1.2), learning Rust deeply along the way.

