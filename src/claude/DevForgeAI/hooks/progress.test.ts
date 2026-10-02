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
  setMode?: Any
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
    return { value: { exitCode: 0, stdout: `${over.mode ?? 'observe framework-default'}\n`, stderr: '' } }
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
    return { value: { exitCode: answer.exitCode ?? 0, stdout: 'progress brainstorm: step 2 of 2, 0 flags\n', stderr: answer.stderr ?? '' } }
  }
  return { deny: `unexpected process: ${argv.join(' ')}` }
}

// Every stub the module can reach, registered once (the kit allows one on() per event in a test).
function world(on: Any, over: Over = {}): World {
  const w: World = {
    files: new Map(Object.entries(over.files ?? {})), writes: [], toasts: [], logs: [], statuses: [], runs: [],
    clock: mock.clock(on, { now: T0 }),
  }
  on('session.root', () => ({ value: ROOT }))
  on('session.id', () => ({ value: 's1' }))
  on('session.version', () => ({ value: { version: '2.1.287' } }))
  on('session.surfaces', () => ({ value: over.surfaces ?? ['terminal'] }))
  on('session.start', (_$: Any, e: Any) => ({ cwd: e.cwd }))
  on('classic.SessionStart', () => ({}))
  on('skill.prompt', (_$: Any, e: Any) => ({ text: e.text }))
  on('prompt.compose', () => ({ sections: [] }))
  on('prompt.submit', (_$: Any, e: Any) => ({ text: e.text }))
  on('turn.start', (_$: Any, e: Any) => ({ turnId: e.turnId }))
  on('turn.complete', () => ({ text: '' }))
  on('session.end', (_$: Any, e: Any) => ({ sessionId: e.sessionId }))
  on('ui.render', () => ({ type: 'Text', props: {}, children: ['drawn by the mods after it'] }))
  on('ui.toast', (_$: Any, e: Any) => { w.toasts.push(e.text); return { value: undefined } })
  on('ui.log', (_$: Any, e: Any) => { w.logs.push(e.text); return { value: undefined } })
  on('ui.status', (_$: Any, e: Any) => { w.statuses.push(e.text); return { value: undefined } })
  on('fs.exists', (_$: Any, e: Any) => ({
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
  on('tool.call', (_$: Any, e: Any) => over.tool?.(e) ?? { result: 'ok' })
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

/** The events of the run whose skill-loaded names skill (the latest such run), with the random digits normalised. */
function eventsOf(w: World, skill = 'brainstorm'): string[] {
  const files = runFiles(w, 'events.jsonl').filter(f => f.includes(`-${skill}-`))
  const text = files.length ? w.files.get(files[files.length - 1]) ?? '' : ''
  return text.split('\n').filter(Boolean).map(l => l.replace(/-[0-9a-f]{8}"/, '-RANDOM8"'))
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
  expect(JSON.parse(eventsOf(w, 'prd').slice(-1)[0])).toMatchObject({ kind: 'run-end', reason: 'another-skill' })
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
  await w.clock.advance(24 * 60 * 60 * 1000)
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
  await ($ as Any).prompt.compose({ model: 'm', promptModel: 'm', surfaces: [], tools: [], traits: ['lean', 'print', 'skills'] })
  await load($)
  expect(w.writes).toEqual([])
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
    `${PROGRESS}/.gitignore`, `${PROGRESS}/current.json`, `${PROGRESS}/runs/RUN/events.jsonl`,
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

test('VER-11 / ERR-11: past 3 MiB no content is kept, and at 4 MiB the run stops with a notice', async ($, on) => {
  const w = world(on)
  await start($)
  await load($)
  const chunk = 'y'.repeat(60 * 1024)
  for (let i = 0; i < 52; i++) await $.tool.call({ tool: 'Write', file_path: `${ROOT}/c${i}.md`, content: chunk } as Any)
  const lines = eventsOf(w)
  const withContent = lines.filter(l => JSON.parse(l).content !== undefined).length
  expect(withContent < 52).toBe(true)
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
