import { expect, mock, test } from 'claude-code/testing'
import type { Plugin } from 'claude-code/testing'

// The adapter driven through the test kit (SPEC-013 §9). The kit stands for Claude Code: the world below answers
// every call the module makes on $, so nothing touches disk (P12); the module's file writes are captured, its
// process runs (python, settings.py, evaluate.py) answered from a table, and its clock is mocked.

const ROOT = '/work'
const T0 = Date.UTC(2026, 9, 2, 12, 0, 0)
const PROGRESS = `${ROOT}/devforgeai/progress`
const SKILLS = ['architecture', 'brainstorm', 'context', 'documents-updater', 'epic', 'git', 'prd']
const CHECKLIST = 'Base directory for this skill: /x\n\n- [ ] 1. Intake\n- [ ] 2. Pick'

type Any = any // the kit's stubs take loosely typed events; the module itself is typed

type Over = {
  surfaces?: string[]
  python3?: boolean
  mode?: string
  modeStderr?: string
  setMode?: Any
  failSessionId?: boolean
  failVersion?: boolean
  failExists?: (path: string) => boolean
  failStatus?: boolean
  evaluate?: (argv: readonly string[]) => Any
  tool?: (e: Any) => Any
  failWrite?: (path: string) => boolean
  files?: Record<string, string>
}

type World = {
  files: Map<string, string>
  writes: string[]
  toasts: string[]
  logs: string[]
  statuses: Array<string | undefined>
  runs: string[][]
  contexts: string[][]
  tools: string[]
  clock: Any
}

const STATE = {
  format: 'devforgeai-progress/1', run: 'r', skill: 'brainstorm', current: 2, ended: null,
  manifest: { state: 'matched', manifestHash: null, checklistHash: null, layers: [] },
  steps: [
    { n: 1, title: 'Intake', state: 'done' },
    { n: 2, title: 'Pick', state: 'current' },
  ],
  flags: [],
  gate: { kind: null, seq: null, refuse: false, reason: null },
  next: null,
  counts: {},
}

function listOf(files: Map<string, string>, path: string): Any[] {
  if (path.endsWith('/skills')) return SKILLS.map(name => ({ name, kind: 'dir', size: 0 }))
  const prefix = path.replace(/\/+$/, '') + '/'
  const names = new Map<string, string>()
  for (const key of files.keys()) {
    if (!key.startsWith(prefix)) continue
    const rest = key.slice(prefix.length)
    const name = rest.split('/')[0]
    names.set(name, rest.includes('/') ? 'dir' : 'file')
  }
  return [...names].map(([name, kind]) => ({ name, kind, size: 0 }))
}

function processRun(w: World, over: Over, argv: readonly string[]): Any {
  if (argv[1] === '--version') {
    if (argv[0] === 'python3' && over.python3 !== false) return { value: { exitCode: 0, stdout: 'Python 3.12.3\n', stderr: '' } }
    return { deny: `failed to start: ENOENT: Executable not found in $PATH: "${argv[0]}"` }
  }
  const script = argv[1] ?? ''
  if (script.endsWith('/progress/settings.py') && argv[2] === 'mode') {
    return { value: { exitCode: 0, stdout: `${over.mode ?? 'observe framework-default'}\n`, stderr: over.modeStderr ?? '' } }
  }
  if (script.endsWith('/progress/settings.py') && argv[2] === 'set-mode') {
    const value = argv[argv.indexOf('--value') + 1]
    return over.setMode ?? { value: { exitCode: 0, stdout: `saved progress.mode=${value} to .claude/devforgeai.local.md\n`, stderr: '' } }
  }
  if (script.endsWith('/progress/evaluate.py') && argv[2] === 'evaluate') {
    const out = argv[argv.indexOf('--out') + 1]
    const answer = over.evaluate?.(argv) ?? { state: STATE }
    if (answer.deny !== undefined) return { deny: answer.deny }
    if (answer.state !== undefined) w.files.set(out, JSON.stringify(answer.state))
    if (answer.raw !== undefined) w.files.set(out, answer.raw)
    return { value: { exitCode: answer.exitCode ?? 0, stdout: 'progress brainstorm: step 2 of 2, 0 flags\n', stderr: answer.stderr ?? '' } }
  }
  return { deny: `unexpected process: ${argv.join(' ')}` }
}

// Every stub the module can reach, registered once (the kit allows one on() per event in a test).
function world(on: Any, over: Over = {}): World {
  const w: World = {
    files: new Map(Object.entries(over.files ?? {})), writes: [], toasts: [], logs: [], statuses: [], runs: [],
    contexts: [], tools: [],
    clock: mock.clock(on, { now: T0 }),
  }
  on('session.root', () => ({ value: ROOT }))
  on('session.id', () => (over.failSessionId ? { deny: 'no session id' } : { value: 's1' }))
  on('session.version', () => (over.failVersion ? { deny: 'no version' } : { value: { version: '2.1.287' } }))
  on('session.surfaces', () => ({ value: over.surfaces ?? ['terminal'] }))
  on('session.start', (_$: Any, e: Any) => ({ cwd: e.cwd }))
  on('classic.SessionStart', () => ({}))
  on('skill.prompt', (_$: Any, e: Any) => ({ text: e.text }))
  on('prompt.compose', () => ({ sections: [] }))
  on('prompt.submit', (_$: Any, e: Any) => {
    w.contexts.push([...(e.context ?? [])])
    return { text: e.text }
  })
  on('turn.start', (_$: Any, e: Any) => ({ turnId: e.turnId }))
  on('turn.complete', () => ({ text: '' }))
  on('session.end', (_$: Any, e: Any) => ({ sessionId: e.sessionId }))
  on('ui.render', () => ({ type: 'Text', props: {}, children: ['drawn by the mods after it'] }))
  on('ui.toast', (_$: Any, e: Any) => { w.toasts.push(e.text); return { value: undefined } })
  on('ui.log', (_$: Any, e: Any) => { w.logs.push(e.text); return { value: undefined } })
  on('ui.status', (_$: Any, e: Any) => {
    if (over.failStatus) return { deny: 'status line unavailable' }
    w.statuses.push(e.text)
    return { value: undefined }
  })
  on('fs.exists', (_$: Any, e: Any) => over.failExists?.(e.path) ? { deny: `EIO: ${e.path}` } : ({
    value: w.files.has(e.path) || [...w.files.keys()].some(k => k.startsWith(e.path.replace(/\/+$/, '') + '/')),
  }))
  on('fs.read', (_$: Any, e: Any) => (w.files.has(e.path) ? { value: w.files.get(e.path) } : { deny: `ENOENT: ${e.path}` }))
  on('fs.write', (_$: Any, e: Any) => {
    if (over.failWrite?.(e.path)) return { deny: `EACCES: ${e.path}` }
    w.files.set(e.path, e.text)
    w.writes.push(e.path)
    return { value: undefined }
  })
  on('fs.list', (_$: Any, e: Any) => ({ value: listOf(w.files, e.path) }))
  on('process.run', (_$: Any, e: Any) => {
    w.runs.push([...e.argv])
    return processRun(w, over, e.argv)
  })
  on('tool.call', (_$: Any, e: Any) => {
    w.tools.push(e.tool)
    return over.tool?.(e) ?? { result: 'ok' }
  })
  return w
}

async function start($: Any, interactive = true) {
  await $.session.start({ surface: interactive ? 'terminal' : null, isInteractive: interactive, cwd: ROOT })
}

async function load($: Any, skill = 'devforgeai:brainstorm') {
  await $.skill.prompt({ skill, text: CHECKLIST })
}

/** session.append can't complete in the kit (nothing answers beneath it), so its rejection is expected. */
async function respond($: Any, content: Any, agentId?: string) {
  try {
    await $.session.append({ door: 'response', uuid: `u${Math.random()}`, origin: { kind: 'model' }, agentId,
      message: { type: 'assistant', role: 'assistant', content } })
  } catch {
    // no implementation for session.append beneath the test
  }
}

function runFiles(w: World, name: string): string[] {
  return [...w.files.keys()].filter(k => k.startsWith(`${PROGRESS}/runs/`) && k.endsWith(`/${name}`)).sort()
}

/** The event logs of a skill's runs, in the order the runs were created, with the random digits normalised. */
function runsOf(w: World, skill = 'brainstorm'): string[][] {
  const order: string[] = []
  for (const path of w.writes) {
    if (path.startsWith(`${PROGRESS}/runs/`) && path.endsWith('/events.jsonl') && path.includes(`-${skill}-`) && !order.includes(path)) order.push(path)
  }
  return order.map(f => (w.files.get(f) ?? '').split('\n').filter(Boolean).map(l => l.replace(/-[0-9a-f]{8}"/, '-RANDOM8"')))
}

/** The events of the latest run of a skill. */
function eventsOf(w: World, skill = 'brainstorm'): string[] {
  const runs = runsOf(w, skill)
  return runs.length ? runs[runs.length - 1] : []
}

function kinds(lines: string[]): string[] {
  return lines.map(l => JSON.parse(l).kind)
}

const asker: Plugin = {
  name: 'asker',
  register(on) {
    on('command.run', { command: 'ask-me' }, async $ => {
      try {
        await $.ui.ask('Which one?', ['A', 'B'])
      } catch {
        // dismissed, or nobody to ask
      }
      return { text: 'asked' }
    })
  },
}

function bottomTool(e: Any): Any {
  if (e.tool === 'AskUserQuestion') {
    const q = e.questions?.[0]?.question ?? 'Q?'
    if (q === 'Dismiss me?') return { result: "Error: The user doesn't want to proceed with this tool use.", isError: true, text: "The user doesn't want to proceed with this tool use." }
    if (q === 'Type me?') return { result: { questions: e.questions, answers: { [q]: 'not sure' }, annotations: {} } }
    return { result: { questions: e.questions ?? [], answers: { [q]: 'Yes' }, annotations: {} } }
  }
  if (e.tool === 'Bash' && e.command === 'exit 3') return { result: 'Error: Exit code 3', isError: true, text: 'Exit code 3' }
  if (e.tool === 'Write' && e.file_path === `${ROOT}/tmp/refused.md`) return { deny: 'refused by a settings hook' }
  return { result: 'ok' }
}

// EXPECTED-EVENTS-BEGIN (VER-04; test_adapter_structure.py reads these lines and validates each against events.schema.json)
const EXPECTED_EVENTS = [
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":1,"time":"2026-10-02T12:00:00Z","kind":"skill-loaded","format":"devforgeai-events/1","skill":"brainstorm","checklist":"Base directory for this skill: /x\\n\\n- [ ] 1. Intake\\n- [ ] 2. Pick","host":"claude-code 2.1.287","mode":"observe","modeSource":"framework-default"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":2,"time":"2026-10-02T12:00:00Z","kind":"tool","tool":"Read","path":"docs/specs/brainstorm/BRN-001.md","exit":0,"error":false}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":3,"time":"2026-10-02T12:00:00Z","kind":"tool","tool":"Bash","command":"python3 scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md","exit":0,"error":false}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":4,"time":"2026-10-02T12:00:00Z","kind":"answer","answered":true}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":5,"time":"2026-10-02T12:00:00Z","kind":"answer","answered":true}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":6,"time":"2026-10-02T12:00:00Z","kind":"answer","answered":false}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":7,"time":"2026-10-02T12:00:00Z","kind":"tool","tool":"Bash","command":"exit 3","exit":3,"error":true}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":8,"time":"2026-10-02T12:00:00Z","kind":"tool","tool":"Write","path":"tmp/refused.md","exit":null,"error":true,"content":"no"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":9,"time":"2026-10-02T12:00:00Z","kind":"turn","phase":"start"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":10,"time":"2026-10-02T12:00:00Z","kind":"reply","text":"- [x] 1. Intake"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":11,"time":"2026-10-02T12:00:00Z","kind":"reply","text":"- [x] 2. Pick"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":12,"time":"2026-10-02T12:00:00Z","kind":"turn","phase":"end"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":13,"time":"2026-10-02T12:00:00Z","kind":"tool","tool":"Write","path":"docs/specs/brainstorm/BRN-001.md","exit":0,"error":false,"content":"---\\nid: BRN-001\\n---\\n"}',
  '{"run":"20261002T120000Z-brainstorm-RANDOM8","seq":14,"time":"2026-10-02T12:00:00Z","kind":"prompt"}',
]
// EXPECTED-EVENTS-END

test('VER-04: a scripted session writes exactly the expected event lines', { plugins: [asker] }, async ($, on) => {
  const w = world(on, { tool: bottomTool })
  await start($)
  await load($)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/docs/specs/brainstorm/BRN-001.md` } as Any)
  await $.tool.call({ tool: 'Bash', command: 'python3 scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md' } as Any)
  await $.tool.call({ tool: 'AskUserQuestion', questions: [{ question: 'Pick one?', header: 'Pick', options: [], multiSelect: false }] } as Any)
  await $.tool.call({ tool: 'AskUserQuestion', questions: [{ question: 'Type me?', header: 'Type', options: [], multiSelect: false }] } as Any)
  await $.tool.call({ tool: 'AskUserQuestion', questions: [{ question: 'Dismiss me?', header: 'No', options: [], multiSelect: false }] } as Any)
  await ($ as Any).command.run({ command: 'ask-me', args: '' })
  await $.tool.call({ tool: 'Bash', command: 'exit 3' } as Any)
  await $.tool.call({ tool: 'Write', file_path: `${ROOT}/tmp/refused.md`, content: 'no' } as Any)
  await ($ as Any).turn.start({ turnId: 't1' })
  await respond($, [{ type: 'text', text: '- [x] 1. Intake' }])
  await respond($, [{ type: 'tool_use', id: 'x', name: 'Bash', input: {} }])
  await respond($, [{ type: 'thinking', thinking: 'hmm' }])
  await respond($, [{ type: 'text', text: '- [x] 2. Pick' }])
  await ($ as Any).turn.complete({ turnId: 't1', answer: '- [x] 2. Pick', durationMs: 5, isAborted: false, reason: 'answer', usage: null })
  await $.tool.call({ tool: 'Write', file_path: `${ROOT}/docs/specs/brainstorm/BRN-001.md`, content: '---\nid: BRN-001\n---\n' } as Any)
  await ($ as Any).prompt.submit({ text: 'looks good', wait: false, origin: { kind: 'composer' } })
  await ($ as Any).prompt.submit({ text: '<task-notification>done</task-notification>', wait: false, origin: { kind: 'task-notification' } })
  await $.tool.call({ tool: 'Write', file_path: `${ROOT}/docs/x.md`, content: 'sub', agentId: 'a1' } as Any)
  await respond($, [{ type: 'text', text: '- [x] 9. subagent' }], 'a1')
  expect(eventsOf(w)).toEqual(EXPECTED_EVENTS)
}, )

test('VER-05: runs end at another skill or the same one, at /clear and at the session end; untracked skills do nothing', async ($, on) => {
  const w = world(on, { files: { [`${ROOT}/devforgeai/manifests/release.json`]: '{}' } })
  await start($)
  await load($)
  await load($, 'plugin-dev:create-plugin')
  expect(kinds(eventsOf(w))).toEqual(['skill-loaded'])
  await load($, 'devforgeai:prd')
  const first = eventsOf(w)
  expect(JSON.parse(first[first.length - 1])).toMatchObject({ kind: 'run-end', reason: 'another-skill' })
  await load($, 'devforgeai:prd')
  const prd = runsOf(w, 'prd')
  expect(prd.length).toBe(2)
  expect(JSON.parse(prd[0].slice(-1)[0])).toMatchObject({ kind: 'run-end', reason: 'another-skill' })
  await load($, 'release')
  expect(kinds(eventsOf(w, 'release'))).toEqual(['skill-loaded'])
  await ($ as Any).session.end({ reason: 'clear', sessionId: 's1', resume: { id: 's1' } })
  expect(JSON.parse(eventsOf(w, 'release').slice(-1)[0])).toMatchObject({ kind: 'run-end', reason: 'clear' })
  for (const id of runFiles(w, 'events.jsonl')) {
    expect(/runs\/[0-9]{8}T[0-9]{6}Z-[a-z][a-z0-9-]*-[0-9a-f]{8}\/events\.jsonl$/.test(id)).toBe(true)
  }
})

test('VER-05: session end with any other reason is session-end, and nothing ends a run while idle', async ($, on) => {
  const w = world(on)
  await start($)
  await load($)
  // The kit's mock clock runs at most 10,000 waits in one advance, so 31 minutes (past the 30-minute idle
  // display) stands for the spec's 24 hours: nothing in the adapter ends a run on time either way.
  for (let i = 0; i < 31; i++) await w.clock.advance(60 * 1000)
  expect(kinds(eventsOf(w))).toEqual(['skill-loaded'])
  expect((w.statuses.filter(Boolean).slice(-1)[0] ?? '').endsWith(' · idle')).toBe(true)
  await ($ as Any).session.end({ reason: 'resume', sessionId: 's1', resume: { id: 's1' } })
  expect(JSON.parse(eventsOf(w).slice(-1)[0])).toMatchObject({ kind: 'run-end', reason: 'session-end' })
})

test('VER-05: after /clear, /resume or /branch, classic.SessionStart resolves the mode and the next run opens', async ($, on) => {
  const w = world(on, { mode: 'enforce local' })
  await start($)
  await ($ as Any).session.end({ reason: 'clear', sessionId: 's1', resume: { id: 's1' } })
  await ($ as Any).classic.SessionStart({ source: 'fork' })
  const modeRuns = w.runs.filter(a => a[2] === 'mode').length
  expect(modeRuns).toBe(2)
  await load($)
  expect(JSON.parse(eventsOf(w)[0])).toMatchObject({ kind: 'skill-loaded', mode: 'enforce', modeSource: 'local' })
})

test('VER-10: a headless session records, writes and draws nothing', async ($, on) => {
  const w = world(on)
  await start($, false)
  await load($)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a.md` } as Any)
  expect(w.writes).toEqual([])
  expect(w.statuses.filter(Boolean)).toEqual([])
})

test('VER-10: the print trait also marks a session headless', async ($, on) => {
  const w = world(on)
  await start($)
  const before = w.writes.length
  await ($ as Any).prompt.compose({ model: 'm', promptModel: 'm', surfaces: [], tools: [], traits: ['lean', 'print', 'skills'], outputStyle: null })
  await load($)
  expect(w.writes.slice(before)).toEqual([])
  expect(runFiles(w, 'events.jsonl')).toEqual([])
})

test('VER-10 / ERR-08: a tracked skill before any session.start records nothing', async ($, on) => {
  const w = world(on)
  await load($)
  expect(w.writes).toEqual([])
})

test('VER-10: with tracking off, nothing is written or drawn', { options: { tracking: 'off' } } as Any, async ($: Any, on: Any) => {
  const w = world(on)
  await start($)
  await load($)
  expect(w.writes).toEqual([])
  expect(w.runs).toEqual([])
})

test('VER-10: where nothing draws, the adapter records as usual and notices also go to the transcript', async ($, on) => {
  const w = world(on, { surfaces: [], python3: false })
  await start($)
  await load($)
  expect(kinds(eventsOf(w))).toEqual(['skill-loaded'])
  expect(w.logs.some(l => l.includes('python not found'))).toBe(true)
})

test('VER-11: the files written are the progress folder\'s .gitignore, the run\'s log, current.json and adapter.log', async ($, on) => {
  const w = world(on, { files: { [`${ROOT}/.gitignore`]: 'node_modules\n' } })
  await start($)
  await load($)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a.md` } as Any)
  await w.clock.advance(600)
  const written = new Set(w.writes.map(p => p.replace(/runs\/[^/]+\//, 'runs/RUN/')))
  expect([...written].sort()).toEqual([
    `${PROGRESS}/.gitignore`, `${PROGRESS}/adapter.log`, `${PROGRESS}/current.json`, `${PROGRESS}/runs/RUN/events.jsonl`,
  ])
  expect(w.files.get(`${PROGRESS}/.gitignore`)).toBe('*\n')
  expect(w.files.get(`${ROOT}/.gitignore`)).toBe('node_modules\n')
  expect(w.writes.includes(`${ROOT}/.gitignore`)).toBe(false)
})

test('VER-11: a Write over 64 KiB is recorded without content', async ($, on) => {
  const w = world(on)
  await start($)
  await load($)
  await $.tool.call({ tool: 'Write', file_path: `${ROOT}/big.md`, content: 'x'.repeat(64 * 1024 + 1) } as Any)
  const last = JSON.parse(eventsOf(w).slice(-1)[0])
  expect(last.kind).toBe('tool')
  expect(last.content).toBeUndefined()
})

test('VER-11 / ERR-11: past 3 MiB no content is kept, and at 4 MiB the run stops with a notice', { timeoutMs: 120000 }, async ($, on) => {
  const w = world(on)
  await start($)
  await load($)
  const chunk = 'y'.repeat(60 * 1024)
  for (let i = 0; i < 60; i++) await $.tool.call({ tool: 'Write', file_path: `${ROOT}/c${i}.md`, content: chunk } as Any)
  const lines = eventsOf(w)
  const withContent = lines.filter(l => JSON.parse(l).content !== undefined).length
  expect(withContent > 40 && withContent < 60).toBe(true)
  for (let i = 0; i < 200; i++) await $.tool.call({ tool: 'Bash', command: 'z'.repeat(30 * 1024) } as Any)
  const size = (w.files.get(runFiles(w, 'events.jsonl')[0]) ?? '').length
  expect(size <= 4 * 1024 * 1024).toBe(true)
  expect(w.statuses.includes('progress: off (event log full)')).toBe(true)
})

test('VER-11 / ERR-03: when devforgeai/progress/ can\'t be written, tracking stops for the session', async ($, on) => {
  const w = world(on, { failWrite: p => p.startsWith(PROGRESS) })
  await start($)
  await load($)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a.md` } as Any)
  expect(w.statuses.includes('progress: off (cannot write devforgeai/progress)')).toBe(true)
  expect(w.toasts.filter(t => t.includes('cannot write devforgeai/progress')).length).toBe(1)
})

test('VER-13: a second session.start, as after a reload, keeps the open run and its seq', async ($, on) => {
  const w = world(on)
  await start($)
  await load($)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a.md` } as Any)
  await start($)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/b.md` } as Any)
  const lines = eventsOf(w)
  expect(kinds(lines)).toEqual(['skill-loaded', 'tool', 'tool'])
  expect(lines.map(l => JSON.parse(l).seq)).toEqual([1, 2, 3])
  expect(runFiles(w, 'events.jsonl').length).toBe(1)
})

test('VER-14: an Edit records the file it will leave, or no content when it can\'t be computed', async ($, on) => {
  const file = `${ROOT}/docs/a.md`
  const w = world(on, { files: { [file]: 'one two one', [`${ROOT}/big.md`]: 'q'.repeat(64 * 1024 + 1) } })
  await start($)
  await load($)
  await $.tool.call({ tool: 'Edit', file_path: file, old_string: 'two', new_string: 'TWO', replace_all: false } as Any)
  await $.tool.call({ tool: 'Edit', file_path: file, old_string: 'one', new_string: '1', replace_all: true } as Any)
  await $.tool.call({ tool: 'Edit', file_path: file, old_string: 'one', new_string: '1', replace_all: false } as Any)
  await $.tool.call({ tool: 'Edit', file_path: file, old_string: 'missing', new_string: 'x', replace_all: false } as Any)
  await $.tool.call({ tool: 'Edit', file_path: `${ROOT}/big.md`, old_string: 'q', new_string: 'r', replace_all: true } as Any)
  const contents = eventsOf(w).slice(1).map(l => JSON.parse(l).content)
  expect(contents).toEqual(['one TWO one', '1 two 1', undefined, undefined, undefined])
})

// ---- Phase 5: evaluation and display ----

function manifestsOf(argv: string[]): string[] {
  return argv.flatMap((a, i) => (a === '--manifests' ? [argv[i + 1]] : []))
}

test('VER-06: the evaluator runs with IF-03 argv and the layer folders that exist, once for a burst', async ($, on) => {
  const w = world(on, { files: {
    [`${ROOT}/devforgeai/manifests/organization/x.json`]: '{}', [`${ROOT}/devforgeai/manifests/release.json`]: '{}',
  } })
  await start($)
  await load($)
  for (let i = 0; i < 5; i++) await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a${i}.md` } as Any)
  expect(w.runs.filter(a => a[2] === 'evaluate').length).toBe(0)
  await w.clock.advance(600)
  const evals = w.runs.filter(a => a[2] === 'evaluate')
  expect(evals.length).toBe(1)
  const argv = evals[0]
  expect(argv[0]).toBe('python3')
  expect(argv[1].endsWith('/progress/evaluate.py')).toBe(true)
  const layers = manifestsOf(argv)
  expect(layers[0].endsWith('/progress/manifests')).toBe(true)
  expect(layers.slice(1)).toEqual([`${ROOT}/devforgeai/manifests/organization`, `${ROOT}/devforgeai/manifests`])
  expect(argv.slice(argv.indexOf('--root'))).toEqual(['--root', ROOT])
  expect(argv[argv.indexOf('--events') + 1].endsWith('/events.jsonl')).toBe(true)
  expect(w.files.get(`${PROGRESS}/current.json`)).toBe(JSON.stringify(STATE))
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/b.md` } as Any)
  await w.clock.advance(600)
  expect(w.runs.filter(a => a[2] === 'evaluate').length).toBe(2)
})

test('VER-06: without project layers only the plugin\'s manifests are passed', async ($, on) => {
  const w = world(on)
  await start($)
  await load($)
  await w.clock.advance(600)
  expect(manifestsOf(w.runs.filter(a => a[2] === 'evaluate')[0]).length).toBe(1)
})

const BAND = {
  plugin: 'devforgeai', component: 'AbovePrompt', requestId: 'band', viewport: { columns: 120, rows: 40 },
  props: { hasSurvey: false, isWorking: false, maxRows: 2, bodyColumns: 80, scroll: { offset: 0, bodyRows: 2 }, view: {} },
}

for (const surface of ['terminal', 'desktop'] as const) {
  test(`VER-12: the band on ${surface} shows the run and the mode button, and keeps what later mods draw`, async ($, on) => {
    const w = world(on)
    await start($)
    await load($)
    await w.clock.advance(600)
    const ui = await ($ as Any).ui.mount({ ...BAND, surface })
    expect(await ui.find({ text: /step 2 of 2: Pick/ })).toBeDefined()
    expect(await ui.find({ text: /drawn by the mods after it/ })).toBeDefined()
    const button = await ui.find({ key: 'progress-mode' })
    expect(button).toBeDefined()
    expect(button.props.hotkey).toBeUndefined()
    await ui.press({ key: 'progress-mode' })
    expect(w.runs.some(a => a[2] === 'set-mode' && a[a.length - 1] === 'enforce')).toBe(true)
    expect(w.statuses[w.statuses.length - 1]).toBe('brainstorm 2/2 · enforce')
    expect(w.toasts.some(t => t.includes('enforce mode, saved to .claude/devforgeai.local.md'))).toBe(true)
    await ui.unmount()
  })
}

test('VER-12: the band draws only row 1 in one row, nothing of its own during a survey or with no run, and fits the width', async ($, on) => {
  const w = world(on)
  await start($)
  const none = await ($ as Any).ui.mount({ ...BAND, surface: 'terminal' })
  expect(await none.find({ text: /brainstorm/ })).toBeUndefined()
  await none.unmount()
  await load($)
  await w.clock.advance(600)
  const one = await ($ as Any).ui.mount({ ...BAND, surface: 'terminal', props: { ...BAND.props, maxRows: 1, bodyColumns: 20 } })
  const row = await one.find({ type: 'Text', text: /brainstorm/ })
  expect(row).toBeDefined()
  expect(Array.from(String(row.children.join(''))).length <= 20).toBe(true)
  expect(await one.find({ key: 'progress-mode' })).toBeUndefined()
  await one.unmount()
  const survey = await ($ as Any).ui.mount({ ...BAND, surface: 'terminal', props: { ...BAND.props, hasSurvey: true } })
  expect(await survey.find({ text: /step 2 of 2/ })).toBeUndefined()
  expect(await survey.find({ text: /drawn by the mods after it/ })).toBeDefined()
  await survey.unmount()
})

test('VER-12: the status text is sent once while it stays the same, and a failed save keeps the mode', async ($, on) => {
  const w = world(on, { setMode: { value: { exitCode: 1, stdout: '', stderr: "settings: .claude/devforgeai.local.md isn't frontmatter-only; not changed\n" } } })
  await start($)
  await load($)
  for (let i = 0; i < 4; i++) await w.clock.advance(600)
  expect(w.statuses.filter(s => s === 'brainstorm 2/2').length).toBe(1)
  const ui = await ($ as Any).ui.mount({ ...BAND, surface: 'terminal' })
  await ui.press({ key: 'progress-mode' })
  expect(w.toasts.some(t => t.includes("couldn't save progress.mode") && t.includes('frontmatter-only'))).toBe(true)
  expect(w.statuses.some(s => (s ?? '').includes('enforce'))).toBe(false)
  await ui.unmount()
})

test('VER-12: each flag is toasted once, and ignored local entries give one toast at session start', async ($, on) => {
  const flagged = { ...STATE, flags: [{ gate: 'write', seq: 2, step: 1, type: 'skipped', message: 'step 1 had no answer' }] }
  const w = world(on, { evaluate: () => ({ state: flagged }), modeStderr: 'ignored .claude/devforgeai.local.md progress.mode (\'strict\' is not observe or enforce)\n' })
  await start($)
  expect(w.toasts.filter(t => t.startsWith('ignored .claude/devforgeai.local.md progress.mode')).length).toBe(1)
  await load($)
  await w.clock.advance(600)
  await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a.md` } as Any)
  await w.clock.advance(600)
  expect(w.toasts.filter(t => t.startsWith('✗ Step 1 skipped')).length).toBe(1)
  expect(w.statuses[w.statuses.length - 1]).toBe('brainstorm 2/2 · 1 flag')
})

// ---- Phase 6: enforce mode and failing open ----

const WRITE = { tool: 'Write', file_path: `${ROOT}/docs/specs/brainstorm/BRN-001.md`, content: 'disposition: promoted' }

function refusingAt(seq: number) {
  return (argv: readonly string[]) => (argv.some(a => a.endsWith('/pending.jsonl'))
    ? { state: { ...STATE, gate: { kind: 'write', seq, refuse: true, reason: 'x' },
      flags: [{ gate: 'write', seq, step: 1, type: 'skipped', message: 'step 1 had no answer from you' }] } }
    : { state: STATE })
}

test('VER-07: in enforce mode the write gate\'s Write is refused before it runs, and recorded as an error', async ($, on) => {
  const w = world(on, { mode: 'enforce local', evaluate: refusingAt(2) })
  await start($)
  await load($)
  const r = (await $.tool.call(WRITE as Any)) as Any
  expect(typeof r.deny).toBe('string')
  expect(r.deny).toContain('step 1 had no answer from you')
  expect(w.tools.includes('Write')).toBe(false)
  expect(JSON.parse(eventsOf(w).slice(-1)[0])).toMatchObject({ kind: 'tool', tool: 'Write', exit: null, error: true })
  expect(w.writes.filter(p => p.endsWith('/pending.jsonl')).length).toBe(1)
  expect(runFiles(w, 'pending.json').length).toBe(1)
})

test('VER-07: with refuse false or a gate at another seq the Write goes on; observe mode checks nothing', async ($, on) => {
  const w = world(on, { mode: 'enforce local', evaluate: refusingAt(7) })
  await start($)
  await load($)
  const r = (await $.tool.call(WRITE as Any)) as Any
  expect(r.deny).toBeUndefined()
  expect(w.tools.includes('Write')).toBe(true)
  expect(JSON.parse(eventsOf(w).slice(-1)[0])).toMatchObject({ kind: 'tool', tool: 'Write', exit: 0, error: false })
})

test('VER-07: observe mode refuses nothing and writes no pending check', async ($, on) => {
  const w = world(on, { evaluate: refusingAt(2) })
  await start($)
  await load($)
  const r = (await $.tool.call(WRITE as Any)) as Any
  expect(r.deny).toBeUndefined()
  expect(w.writes.some(p => p.endsWith('/pending.jsonl'))).toBe(false)
})

test('VER-07: where nothing draws, the refusal also goes to the transcript', async ($, on) => {
  const w = world(on, { mode: 'enforce local', evaluate: refusingAt(2), surfaces: [] })
  await start($)
  await load($)
  await $.tool.call(WRITE as Any)
  expect(w.logs.some(l => l.includes('refused this write at the write gate'))).toBe(true)
})

function reporting(kind: string) {
  return () => ({ state: { ...STATE, current: null, gate: { kind, seq: 3, refuse: true, reason: 'x' },
    flags: [{ gate: kind, seq: 3, step: 1, type: 'skipped', message: 'step 1 was skipped' }] } })
}

test('VER-08: in enforce mode the report gate\'s flags reach the model once, with a prompt that isn\'t a command', async ($, on) => {
  const w = world(on, { mode: 'enforce local', evaluate: reporting('report') })
  await start($)
  await load($)
  await w.clock.advance(600)
  await ($ as Any).prompt.submit({ text: '/devforgeai:prd', wait: false, origin: { kind: 'composer' } })
  await ($ as Any).prompt.submit({ text: 'please fix it', wait: false, origin: { kind: 'composer' } })
  await ($ as Any).prompt.submit({ text: 'and again', wait: false, origin: { kind: 'composer' } })
  expect(w.contexts.map(c => c.length)).toEqual([0, 1, 0])
  expect(w.contexts[1][0]).toContain('step 1 was skipped')
})

test('VER-08: observe mode and a run-end gate add no context', async ($, on) => {
  const w = world(on, { evaluate: reporting('report') })
  await start($)
  await load($)
  await w.clock.advance(600)
  await ($ as Any).prompt.submit({ text: 'please fix it', wait: false, origin: { kind: 'composer' } })
  expect(w.contexts.map(c => c.length)).toEqual([0])
})

test('VER-08: a run-end gate adds no context in enforce mode', async ($, on) => {
  const w = world(on, { mode: 'enforce local', evaluate: reporting('end') })
  await start($)
  await load($)
  await w.clock.advance(600)
  await ($ as Any).prompt.submit({ text: 'please fix it', wait: false, origin: { kind: 'composer' } })
  expect(w.contexts.map(c => c.length)).toEqual([0])
})

const FAILURES: Array<[string, Over, string]> = [
  ['python missing', { python3: false }, 'progress: off (python not found)'],
  ['evaluator exit 2', { evaluate: () => ({ exitCode: 2, stderr: 'evaluate: bad manifest\n' }) }, 'progress: off (evaluator: evaluate: bad manifest)'],
  ['evaluator timeout', { evaluate: () => ({ deny: 'timed out after 5000 ms' }) }, 'progress: off (evaluator timed out)'],
  ['--out not JSON', { evaluate: () => ({ exitCode: 0, raw: 'not json' }) }, 'progress: off (evaluator: its state is not readable)'],
]

for (const [name, over, status] of FAILURES) {
  test(`VER-09: ${name}: every call goes on, events are recorded, and the user is told once`, async ($, on) => {
    const w = world(on, { ...over, mode: 'enforce local' })
    await start($)
    await load($)
    const r1 = (await $.tool.call(WRITE as Any)) as Any
    await w.clock.advance(600)
    const r2 = (await $.tool.call({ tool: 'Read', file_path: `${ROOT}/a.md` } as Any)) as Any
    await w.clock.advance(600)
    expect(r1).toEqual({ result: 'ok' })
    expect(r2).toEqual({ result: 'ok' })
    expect(kinds(eventsOf(w))).toEqual(['skill-loaded', 'tool', 'tool'])
    expect(w.statuses.includes(status)).toBe(true)
    const reason = status.slice('progress: off ('.length, -1)
    expect(w.toasts.filter(t => t.includes(reason)).length).toBe(1)
    expect((w.files.get(`${PROGRESS}/adapter.log`) ?? '').includes(`fail-open: ${reason}`)).toBe(true)
  })
}

test('VER-09 / ERR-10: a timer callback that throws is caught, logged and treated as the evaluator failing', async ($, on) => {
  // The evaluation's own fs.exists fails, so the timer's code throws (a failed $.ui.status is only dropped).
  const w = world(on, { failExists: p => p.endsWith('/devforgeai/manifests/organization') })
  await start($)
  await load($)
  await w.clock.advance(600)
  expect((w.files.get(`${PROGRESS}/adapter.log`) ?? '').includes('fail-open: timer:')).toBe(true)
  expect(w.statuses.some(s => (s ?? '').startsWith('progress: off (timer:'))).toBe(true)
})

test('VER-09: a hook that throws before next passes its event on unchanged', async ($, on) => {
  const w = world(on, { failSessionId: true })
  const r = (await ($ as Any).session.start({ surface: 'terminal', isInteractive: true, cwd: ROOT })) as Any
  expect(r).toEqual({ cwd: ROOT })
  expect(w.toasts.some(t => t.startsWith('DevForgeAI progress: session.start:'))).toBe(true)
})

test('VER-09: a hook that fails after next keeps the result, and the user is told', async ($, on) => {
  const w = world(on, { failVersion: true })
  await start($)
  const out = (await ($ as Any).skill.prompt({ skill: 'devforgeai:brainstorm', text: CHECKLIST })) as Any
  expect(out).toEqual({ text: CHECKLIST })
  expect(runFiles(w, 'events.jsonl')).toEqual([])
  expect(w.toasts.some(t => t.startsWith('DevForgeAI progress: skill.prompt:'))).toBe(true)
})
