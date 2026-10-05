// DevForgeAI's progress tracker adapter for Claude Code (SPEC-013 v14).
//
// It records each run of a tracked skill as SPEC-012's event log, runs SPEC-012's evaluator on a timer, and shows
// the run in the status line, a two-row band above the prompt and toasts. In enforce mode it refuses the write
// gate's Write or Edit when that gate raised flags, refuses a question at SPEC-012's question gate (no step marked,
// no step tag, or another step's tag), and gives the model the report gate's flags. It records Claude Code's task list as step events.
// A tracked skill Claude loads mid-run pauses the open run on a trail, which unwinds when Claude goes back (BEH-29,
// BEH-30). It fails open:
// when it can't run, the work goes on and the user is told (ADR-006 D1). Old run and session folders are pruned
// by progress/prune.py, which the adapter starts once per session and root (BEH-19).
//
// Every use of `$` stays in top-level functions of this file (claude plugin validate's rule); progress-core.ts
// holds the pure helpers.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'
import type { ProgressMode, ProgressModeSource, ProgressPaused, ProgressReturned, ProgressRun, ProgressSummary } from '../types'
import {
  adherenceText, bandRows, byteSize, compactTexts, editResult, eventLine, exitOf, finalTimeout, fit, followsTaskList, hasTaskList,
  hintText, isAnswered, isEngine, isFailed, isPersonPrompt, isTracked, isWaiverQuestion, keptContent, markedStep, newFlagToasts,
  questionRefusal, questionTag, refusalCause, refusalText, replyText, reportContext, retentionOf, reviewItems, reviewQuestion,
  runId, skillName, statusText, stepLabel, waiverAnswer, returnLine, pausedWith, keptTrail, endReason, hasRoom, trailNote, TRAIL_NOTE_START, stopsRun,
  exitQuestion, keptText, nestedExitQuestion, nestedKeptText, isDismissal, CONFIRMED,
  stepOfTask, stepStateOf, stuckAdvice, stuckText, summaryOf, taskIdOf, todoSteps, toolPath, FORMAT, IDLE_MS, LOG_LIMIT, NOTE_START, TASK_TAG,
} from './progress-core'
import type { Fields, ProgressState, Refused, ReviewItem, ToolOutcome } from './progress-core'

type E = EngineInterface

const RUN = atom({ plugin: 'devforgeai', key: 'run' } as const, null as ProgressRun | null)
const MODE = atom({ plugin: 'devforgeai', key: 'mode' } as const, 'observe' as ProgressMode)
const SOURCE = atom({ plugin: 'devforgeai', key: 'modeSource' } as const, 'framework-default' as ProgressModeSource)
const SUMMARY = atom({ plugin: 'devforgeai', key: 'summary' } as const, null as ProgressSummary | null)
const LAST = atom({ plugin: 'devforgeai', key: 'lastEventAt' } as const, 0)
const MARKED = atom({ plugin: 'devforgeai', key: 'marked' } as const, false)
const SHOWN = atom({ plugin: 'devforgeai', key: 'shown' } as const, [] as string[])
const SENT = atom({ plugin: 'devforgeai', key: 'contextSent' } as const, [] as number[])
const OFF = atom({ plugin: 'devforgeai', key: 'off' } as const, null as string | null)
const TASKS = atom({ plugin: 'devforgeai', key: 'tasks' } as const, {} as Record<string, number>)
const TODOS = atom({ plugin: 'devforgeai', key: 'todos' } as const, {} as Record<string, string>)
const HINTED = atom({ plugin: 'devforgeai', key: 'hinted' } as const, false)
const ADHERED = atom({ plugin: 'devforgeai', key: 'adhered' } as const, null as string | null)
const REFUSALS = atom({ plugin: 'devforgeai', key: 'refusals' } as const, {} as Record<string, number>)
const REFUSED = atom({ plugin: 'devforgeai', key: 'refused' } as const, [] as Refused[])
const REVIEWED = atom({ plugin: 'devforgeai', key: 'reviewed' } as const, null as string | null)
const TRAIL = atom({ plugin: 'devforgeai', key: 'trail' } as const, [] as ProgressPaused[])
const RETURNED = atom({ plugin: 'devforgeai', key: 'returned' } as const, [] as ProgressReturned[])

// The open run's values, as the module holds them (version 14): every hook reads and writes these, never a $.state
// snapshot, since each dispatch's $.state reads one moment of its own (a hook that awaits across another's write would
// act on the old run). $.state keeps a mirror, written in order with the latest values, for a reload and the band.
type Live = {
  run: ProgressRun | null; summary: ProgressSummary | null; lastEventAt: number; marked: boolean; shown: string[]
  contextSent: number[]; tasks: Record<string, number>; todos: Record<string, string>; adhered: string | null
  refusals: Record<string, number>; refused: Refused[]; reviewed: string | null; trail: ProgressPaused[]
  returned: ProgressReturned[]
}
let live: Live | null = null
let mirrorChain: Promise<unknown> = Promise.resolve()

function emptyLive(): Live {
  return { run: null, summary: null, lastEventAt: 0, marked: false, shown: [], contextSent: [], tasks: {}, todos: {},
    adhered: null, refusals: {}, refused: [], reviewed: null, trail: [], returned: [] }
}

/** The module's values, read once from $.state after a load or a reload (BEH-17). */
async function hydrate($: E): Promise<Live> {
  if (live !== null) return live
  const got: Live = {
    run: await read($, RUN), summary: await read($, SUMMARY), lastEventAt: await read($, LAST),
    marked: await read($, MARKED), shown: await read($, SHOWN), contextSent: await read($, SENT),
    tasks: await read($, TASKS), todos: await read($, TODOS), adhered: await read($, ADHERED),
    refusals: await read($, REFUSALS), refused: await read($, REFUSED), reviewed: await read($, REVIEWED),
    // An entry without its run, version 13's shape, is dropped (BEH-30); the mirror catches up at the next change.
    trail: keptTrail(await read($, TRAIL)), returned: await read($, RETURNED),
  }
  if (live === null) live = got
  return live
}

async function get<K extends keyof Live>($: E, key: K): Promise<Live[K]> {
  return (await hydrate($))[key]
}

/** Change one value: the module's at once (no await between reading and writing it), then $.state's mirror. */
async function put<K extends keyof Live>($: E, key: K, change: (value: Live[K]) => Live[K]): Promise<Live[K]> {
  const l = await hydrate($)
  const value = change(l[key])
  l[key] = value
  await mirrorAll($, [key])
  return value
}

/** Change several values at once (version 14): `change` reads the module's values and returns the new ones with no await
 *  between, or null for no change; then each key is mirrored in the order given. True when it changed them. */
async function putMany($: E, change: (l: Live) => Partial<Live> | null): Promise<boolean> {
  const l = await hydrate($)
  const next = change(l)
  if (next === null) return false
  Object.assign(l, next)
  await mirrorAll($, Object.keys(next) as (keyof Live)[])
  return true
}

/** putMany, only while `runId` is the open run: an evaluation, a refusal or an event of a run that a switch has paused,
 *  returned or ended changes nothing of the run open now (BEH-30). */
async function putFor($: E, runId: string, change: (l: Live) => Partial<Live>): Promise<boolean> {
  return putMany($, l => (l.run !== null && l.run.id === runId ? change(l) : null))
}

async function mirrorAll($: E, keys: (keyof Live)[]): Promise<void> {
  const step = mirrorChain.then(async () => {
    for (const key of keys) await mirror($, key)
  })
  mirrorChain = step.catch(() => undefined)
  await step.catch(() => undefined)
}

/** Write the module's latest value of one key to $.state (literal refs, as claude plugin validate reads them). */
async function mirror($: E, key: keyof Live): Promise<void> {
  const l = live
  if (l === null) return
  switch (key) {
    case 'run': await $.state.set({ plugin: 'devforgeai', key: 'run' } as const, l.run); break
    case 'summary': await $.state.set({ plugin: 'devforgeai', key: 'summary' } as const, l.summary); break
    case 'lastEventAt': await $.state.set({ plugin: 'devforgeai', key: 'lastEventAt' } as const, l.lastEventAt); break
    case 'marked': await $.state.set({ plugin: 'devforgeai', key: 'marked' } as const, l.marked); break
    case 'shown': await $.state.set({ plugin: 'devforgeai', key: 'shown' } as const, l.shown); break
    case 'contextSent': await $.state.set({ plugin: 'devforgeai', key: 'contextSent' } as const, l.contextSent); break
    case 'tasks': await $.state.set({ plugin: 'devforgeai', key: 'tasks' } as const, l.tasks); break
    case 'todos': await $.state.set({ plugin: 'devforgeai', key: 'todos' } as const, l.todos); break
    case 'adhered': await $.state.set({ plugin: 'devforgeai', key: 'adhered' } as const, l.adhered); break
    case 'refusals': await $.state.set({ plugin: 'devforgeai', key: 'refusals' } as const, l.refusals); break
    case 'refused': await $.state.set({ plugin: 'devforgeai', key: 'refused' } as const, l.refused); break
    case 'reviewed': await $.state.set({ plugin: 'devforgeai', key: 'reviewed' } as const, l.reviewed); break
    case 'trail': await $.state.set({ plugin: 'devforgeai', key: 'trail' } as const, l.trail); break
    case 'returned': await $.state.set({ plugin: 'devforgeai', key: 'returned' } as const, l.returned); break
  }
}

const EVALUATOR_TIMEOUT = 5000
const START_TIMEOUT = 3000
const PRUNE_TIMEOUT = 10000
const LOG_FULL = 'event log full'
const NO_PYTHON = 'python not found'
const NO_WRITE = 'cannot write devforgeai/progress'

// Values of the process, not the session: they outlive /clear, which empties $.state (DM-03).
let interactive: boolean | null = null
let python: string | null | undefined
let timerOn = false
let evaluating = false
// The timer's evaluation in flight, which the review waits for (BEH-26).
let inFlight: Promise<void> | null = null
let turnOpen = false
/** The skills the main loop's Skill tool calls in flight are loading, by name (BEH-29); emptied at each main-loop turn. */
const skillsLoading = new Map<string, number>()
/** Skills whose load inside a Skill call changed the open run (a push, an unwind, a switch): that call records nothing
 *  when it returns, in either run (BEH-29). */
const switchedIn = new Set<string>()
/** Bumped at each change of the open run (open, push, unwind): a hook that began under an older value began before
 *  the open run opened (BEH-30 (a), version 14). */
let tenure = 0
/** The open run has recorded the event of a tool call or an answer whose hook began after it opened (BEH-30 (a)). */
let worked = false
let disabled = false
let modeSession: string | null = null
// The root the mode was resolved for: the local preference file is per checkout (BEH-16).
let modeRoot: string | null = null
let pluginSkills: string[] | null = null
let lastStatus: string | undefined
let pendingReport: { seq: number; text: string; run: string } | null = null
// The open run's event lines: in the module and events.jsonl, since a $.state value holds at most 4,194,304
// characters (see types/index.d.ts); read back from the file after a reload.
let held: { id: string; lines: string[] } | null = null
let allReachedFor: string | null = null
let bandChain: Promise<unknown> = Promise.resolve()
let logChain: Promise<unknown> = Promise.resolve()
let recordChain: Promise<unknown> = Promise.resolve()
let absorbChain: Promise<unknown> = Promise.resolve()
// adapter.log lines wait here until a run has created devforgeai/progress/ with its .gitignore (BEH-15), so a
// session that runs no tracked skill writes nothing in the project. Then they go to the session's folder in the
// root of the latest run (DM-02).
let logRoot: string | null = null
let early: string[] = []
const ADAPTER_LOG_LIMIT = 512 * 1024
const noticed = new Set<string>()
// The session IDs and roots already pruned (BEH-19), and the retentionDays setting (DM-06).
const pruned = new Set<string>()
let retentionDays = 30
// Whether the open run follows the task list, read once per run from its skill-loaded line.
let followsFor: { id: string; value: boolean } | null = null
// Task-tool calls whose step events aren't recorded yet: a question check waits for them (BEH-21), so a question
// sent in the same batch as the TaskUpdate that marks its step isn't refused. The wait is bounded.
const taskWork = new Set<Promise<void>>()
const TASK_WAIT_MS = 2000
const TASK_TOOLS = ['TaskCreate', 'TaskUpdate', 'TodoWrite']

/** Register a task-tool call as under way; the function returned ends it. */
function startTaskWork(): () => void {
  let finish = () => {}
  const work = new Promise<void>(resolve => {
    finish = resolve
  })
  taskWork.add(work)
  void work.then(() => taskWork.delete(work))
  return finish
}

function message(err: unknown): string {
  return err instanceof Error ? err.message : String(err)
}

function firstLine(text: string): string {
  return text.split('\n').map(l => l.trim()).filter(Boolean)[0] ?? ''
}

function progressDir(r: string): string {
  return `${r}/devforgeai/progress`
}

const SESSION_ID = /^[A-Za-z0-9_-]+$/

/** The session's own folder (DM-02): its ID changes at /clear, /resume and /branch, which start a new one. A session
 *  ID is a UUID; one of another shape (empty, or holding '/' or '..') never makes a path (BEH-15). */
async function sessionDir($: E, r: string): Promise<string> {
  const id = await $.session.id()
  if (typeof id !== 'string' || !SESSION_ID.test(id)) throw new Error('unusable session ID')
  return `${progressDir(r)}/sessions/${id}`
}

/** The root a run opened in; a run kept in $.state from before version 3 has none, so it comes from the folder. */
function rootOf(run: ProgressRun): string {
  return run.root ?? run.dir.replace(/\/devforgeai\/progress\/runs\/[^/]+$/, '')
}

async function hasSurface($: E): Promise<boolean> {
  try {
    return (await $.session.surfaces()).length > 0
  } catch {
    return true
  }
}

/** A toast, and where nothing draws a dim transcript line too (BEH-01); `key` shows it once per session. */
async function notify($: E, text: string, key?: string): Promise<void> {
  if (key !== undefined) {
    if (noticed.has(key)) return
    noticed.add(key)
  }
  try {
    await $.ui.toast(text)
    if (!(await hasSurface($))) await $.ui.log(text)
  } catch {
    // a notice that can't be shown changes nothing
  }
}

/** One line in the session's adapter.log (DM-02); held in memory until a run has created the folder, kept
 *  to its last half when it passes 512 KiB, and a failed write is ignored. */
async function adapterLog($: E, kind: string, text: string): Promise<void> {
  const step = logChain.then(async () => {
    const run = await get($, 'run')
    const now = new Date(await $.clock.now()).toISOString().replace(/\.\d{3}Z$/, 'Z')
    // One line per entry, whatever the text: model text can't add lines of its own (DM-02).
    const line = `${now} ${run?.id ?? '-'} ${kind}: ${text.replace(/\s*[\r\n]+\s*/g, ' ')}\n`
    if (logRoot === null) {
      // The first lines are kept (the early notices are the ones that matter); past 200, newer ones are dropped.
      if (early.length < 200) early = [...early, line]
      return
    }
    await appendLog($, logRoot, line)
  }).catch(() => undefined)
  logChain = step
  await step
}

async function appendLog($: E, r: string, lines: string): Promise<void> {
  const path = `${await sessionDir($, r)}/adapter.log`
  let before = (await $.fs.exists(path)) ? await $.fs.read(path) : ''
  if (byteSize(before) > ADAPTER_LOG_LIMIT) before = before.slice(Math.floor(before.length / 2)).replace(/^[^\n]*\n/, '')
  await $.fs.write(path, before + lines)
}

/** The status line, sent only when its text changes (BEH-10). */
async function refreshStatus($: E): Promise<void> {
  const now = await $.clock.now()
  const mode = await read($, MODE)
  const off = await read($, OFF)
  // The open run's values and the trail as one moment of the module (version 14).
  const l = await hydrate($)
  const idle = !turnOpen && l.lastEventAt > 0 && now - l.lastEventAt > IDLE_MS
  const text = statusText(l.summary, mode, idle, off, l.trail)
  if (text === lastStatus) return
  lastStatus = text
  await $.ui.status(text)
  if (text !== undefined && !(await hasSurface($))) await $.ui.log(text)
}

/** Tracking can't go on for the session (ERR-03): the trail empties and its runs get no run-end (BEH-05, version 14). */
async function stopTracking($: E, reason: string): Promise<void> {
  disabled = true
  const had = (await hydrate($)).trail.length
  await putMany($, () => ({ run: null, trail: [], returned: [] }))
  if (had) await adapterLog($, 'trail', `empty (tracking stopped: ${reason})`)
  await update($, OFF, () => reason)
  await notify($, `DevForgeAI progress: off (${reason})`, `off:${reason}`)
  await refreshStatus($)
}

/** The evaluator can't run, or failed: the work goes on, the user is told (BEH-14, ERR-01, ERR-02, ERR-07). */
async function failOpen($: E, reason: string): Promise<void> {
  await update($, OFF, () => reason)
  await notify($, `DevForgeAI progress: off (${reason})`, `fail-open:${reason}`)
  await adapterLog($, 'fail-open', reason)
  await refreshStatus($)
}

/** A hook's own code failed: log it, tell the user once, and let the event go on (BEH-14). */
async function recover($: E, hook: string, err: unknown): Promise<void> {
  const text = `${hook}: ${message(err)}`
  await adapterLog($, 'error', text)
  await notify($, `DevForgeAI progress: ${text}`, `error:${text}`)
}

/** Send the session's log to a root's folder, writing the lines held until then the first time (BEH-15). */
async function useLogRoot($: E, r: string): Promise<void> {
  const first = logRoot === null
  logRoot = r
  if (!first) return
  const held = early.join('')
  early = []
  if (held) {
    const step = logChain.then(() => appendLog($, r, held)).catch(() => undefined)
    logChain = step
    await step
  }
}

/** The .gitignore that keeps devforgeai/progress/ out of git, written again if it was deleted (BEH-15). */
async function ensureIgnore($: E, r: string): Promise<void> {
  const file = `${progressDir(r)}/.gitignore`
  if (!(await $.fs.exists(file))) await $.fs.write(file, '*\n')
}

/** devforgeai/progress/ and its .gitignore in a run's root, before anything else is written there (BEH-15). */
async function ensureDir($: E, r: string): Promise<boolean> {
  try {
    await ensureIgnore($, r)
    await useLogRoot($, r)
    return true
  } catch {
    await stopTracking($, NO_WRITE)
    return false
  }
}

/** The open run's lines, read back from events.jsonl when the module was reloaded (BEH-17). A failed read
 *  throws, and nothing is cached: writing a fresh log over the real one would lose the run's events. */
async function linesOf($: E, run: ProgressRun): Promise<string[]> {
  if (held !== null && held.id === run.id) return held.lines
  const lines = (await $.fs.read(`${run.dir}/events.jsonl`)).split('\n').filter(Boolean)
  held = { id: run.id, lines }
  return lines
}

/** Write the run's whole log (no append in $.fs); false when it can't be written or would pass 4 MiB. `open` is false
 *  for a run that isn't the open one (a paused run's run-end, a new run before the switch): its lines aren't cached,
 *  and its full log stops nothing. */
async function writeLog($: E, run: ProgressRun, lines: string[], open = true): Promise<boolean> {
  const text = lines.join('\n') + '\n'
  if (byteSize(text) > LOG_LIMIT) {
    if (!open) return false
    // Tracking stops for the session: the trail empties and its runs get no run-end (BEH-05, version 14).
    const had = (await hydrate($)).trail.length
    await putMany($, () => ({ run: null, trail: [] }))
    if (had) await adapterLog($, 'trail', `empty (${LOG_FULL})`)
    await update($, OFF, () => LOG_FULL)
    await notify($, `DevForgeAI progress: off (${LOG_FULL})`, `full:${run.id}`)
    await refreshStatus($)
    return false
  }
  try {
    await $.fs.write(`${run.dir}/events.jsonl`, text)
    if (open) held = { id: run.id, lines }
    else if (held !== null && held.id === run.id) held = null
    return true
  } catch {
    await stopTracking($, NO_WRITE)
    return false
  }
}

/** One item of the record chain: events, and every change of which run is open (a push, an unwind, a switch, a stop,
 *  session.end's run-ends), happen one at a time, so an event never lands in a run's log after its switch (version 14).
 *  Inside an item, call only what never waits on the chain: recordNow, appendEvent, endOpenNow, linesOf, writeLog,
 *  putMany, putFor, adapterLog, prepareRun, afterOpen, returnStepNow, unwindNow, claudeLoadNow, taskStepsNow,
 *  stopTracking. Never record, settle, pendingState, review, switchRun, finishSwitch, finalEvaluation, stopIfAsked or
 *  turnEndUnwind, which wait on the chain and would wait on the item itself. */
function chained<T>(work: () => Promise<T>): Promise<T> {
  const step = recordChain.then(work)
  recordChain = step.catch(() => undefined)
  return step
}

/** The open run changes (open, push, unwind): inside the change of putMany, so a hook starting during the mirror
 *  already sees the new tenure (BEH-30 (a)). */
function onSwitch(): void {
  tenure += 1
  worked = false
  pendingReport = null
}

/** Append one event to the open run (BEH-04); `mark` asks the timer to evaluate (BEH-06). Events are recorded one
 *  at a time, so two hooks that overlap can't take the same seq or lose each other's line. `began` is the tenure
 *  the event's hook began under (tool and answer events). */
async function record($: E, kind: string, fields: Fields, mark = true, began = -1): Promise<void> {
  await chained(() => recordNow($, kind, fields, mark, began))
}

/** One event in a run's log: the open run's (cached lines) or another's (read from its file). Null when nothing was
 *  written: a second run-end, or a log that can't be written. */
async function appendEvent($: E, run: ProgressRun, kind: string, fields: Fields, open: boolean): Promise<{ run: ProgressRun; now: number } | null> {
  const now = await $.clock.now()
  // The seq comes from the run's own lines: a $.state read inside one dispatch sees that dispatch's moment, so
  // overlapping hooks would read the same seq from it.
  const lines = open ? await linesOf($, run) : (await $.fs.read(`${run.dir}/events.jsonl`)).split('\n').filter(Boolean)
  // A run already ended (a deliberate stop, BEH-27) gets no second run-end, checked inside the chain (BEH-05, v12);
  // events after the stop (the turn's end) may follow it, so any run-end in the log counts.
  if (kind === 'run-end' && lines.some(l => l.includes('"kind":"run-end"'))) return null
  const seq = lines.length + 1
  const next: ProgressRun = { ...run, seq }
  if (!(await writeLog($, next, [...lines, eventLine(run.id, seq, now, kind, fields)], open))) return null
  return { run: next, now }
}

/** Record into the open run, inside a chain item; the ID of the run it recorded into, or null. */
async function recordNow($: E, kind: string, fields: Fields, mark: boolean, began = -1): Promise<string | null> {
  const run = await get($, 'run')
  if (run === null || disabled) return null
  const got = await appendEvent($, run, kind, fields, true)
  if (got === null) return null
  await putFor($, run.id, () => ({ run: got.run, lastEventAt: got.now, ...(mark ? { marked: true } : {}) }))
  if ((kind === 'tool' || kind === 'answer') && began === tenure) worked = true
  return run.id
}

/** The run as it stands: events still being written, the evaluation in flight, then one evaluation of a marked run
 *  (BEH-26, BEH-28, BEH-30 (c)). */
async function settle($: E): Promise<void> {
  await recordChain
  if (inFlight !== null) await inFlight
  if (!evaluating && !disabled && (await get($, 'marked'))) {
    inFlight = evaluateMarked($)
    await inFlight
  }
}

async function logBytes($: E): Promise<number> {
  const run = await get($, 'run')
  return run === null ? 0 : byteSize((await linesOf($, run)).join('\n'))
}

/** A Write's content, or the file an Edit will leave (DM-01, ERR-06). */
async function contentOf($: E, r: string, tool: string, input: Fields): Promise<string | null> {
  if (tool === 'Write') return typeof input.content === 'string' ? input.content : null
  if (tool !== 'Edit' || typeof input.file_path !== 'string') return null
  try {
    const path = input.file_path.startsWith('/') ? input.file_path : `${r}/${input.file_path}`
    const file = await $.fs.read(path)
    return editResult(file, String(input.old_string ?? ''), String(input.new_string ?? ''), input.replace_all === true)
  } catch {
    return null
  }
}

/** The skills that open a run: the plugin's own, and those a project or organization manifest names (BEH-02). */
async function tracked($: E, r: string, name: string): Promise<boolean> {
  if (pluginSkills === null) {
    try {
      pluginSkills = (await $.fs.list(`${$.plugin.root}/skills`)).filter(x => x.kind === 'dir').map(x => x.name)
    } catch {
      pluginSkills = []
    }
  }
  const manifests: string[] = []
  for (const dir of [`${r}/devforgeai/manifests`, `${r}/devforgeai/manifests/organization`]) {
    try {
      if (await $.fs.exists(dir)) {
        for (const x of await $.fs.list(dir)) if (x.kind === 'file' && x.name.endsWith('.json')) manifests.push(x.name.slice(0, -5))
      }
    } catch {
      // an unreadable folder adds no manifest
    }
  }
  return isTracked(name, pluginSkills, manifests)
}

/** Find python3, then python (IF-03, ERR-01). */
async function findPython($: E): Promise<void> {
  if (python !== undefined) return
  const r = await $.session.root()
  for (const name of ['python3', 'python']) {
    try {
      const res = await $.process.run([name, '--version'], { cwd: r, timeoutMs: START_TIMEOUT })
      if (res.exitCode === 0) {
        python = name
        return
      }
    } catch {
      // not installed: try the next name
    }
  }
  python = null
  await failOpen($, NO_PYTHON)
}

/** Resolve progress.mode for a root with settings.py (IF-01, BEH-16). */
async function resolveMode($: E, r: string): Promise<void> {
  let mode: ProgressMode = 'observe'
  let source: ProgressModeSource = 'framework-default'
  if (python) {
    try {
      const res = await $.process.run([python, `${$.plugin.root}/progress/settings.py`, 'mode', '--root', r],
        { cwd: r, timeoutMs: START_TIMEOUT })
      const [value, from] = res.stdout.trim().split(/\s+/)
      if (res.exitCode === 0 && (value === 'observe' || value === 'enforce')) {
        mode = value
        source = from === 'local' ? 'local' : 'framework-default'
      }
      const ignored = res.stderr.split('\n').map(l => l.trim()).filter(l => l.startsWith('ignored '))
      for (const line of ignored) await adapterLog($, 'ignored', line)
      if (ignored.length) await notify($, ignored.join('\n'), `ignored:${ignored.join('|')}`)
    } catch (err) {
      await adapterLog($, 'error', `settings.py mode: ${message(err)}`)
    }
  }
  await update($, MODE, () => mode)
  await update($, SOURCE, () => source)
  modeSession = await $.session.id()
  modeRoot = r
  await adapterLog($, 'mode', `${mode} (${source})`)
}

/** Run the evaluator (IF-03) in a run's root; the state, or why it couldn't be had (ERR-01, ERR-02, ERR-07). */
async function evaluate($: E, r: string, events: string, out: string, timeoutMs: number): Promise<{ state: ProgressState; text: string } | string> {
  if (!python) return NO_PYTHON
  const plugin = $.plugin.root
  const argv = [python, `${plugin}/progress/evaluate.py`, 'evaluate', '--manifests', `${plugin}/progress/manifests`]
  if (await $.fs.exists(`${r}/devforgeai/manifests/organization`)) argv.push('--manifests', `${r}/devforgeai/manifests/organization`)
  if (await $.fs.exists(`${r}/devforgeai/manifests`)) argv.push('--manifests', `${r}/devforgeai/manifests`)
  argv.push('--events', events, '--out', out, '--root', r)
  let res
  try {
    res = await $.process.run(argv, { cwd: r, timeoutMs })
  } catch (err) {
    return /time/i.test(message(err)) ? 'evaluator timed out' : `evaluator: ${firstLine(message(err))}`
  }
  if (res.exitCode !== 0) return `evaluator: ${firstLine(res.stderr) || `exit ${res.exitCode}`}`
  try {
    const text = await $.fs.read(out)
    return { state: JSON.parse(text) as ProgressState, text }
  } catch {
    return 'evaluator: its state is not readable'
  }
}

/** Whether a run follows the task list (SPEC-012 BEH-18), read from its skill-loaded line once per run. */
async function follows($: E, run: ProgressRun): Promise<boolean> {
  if (followsFor === null || followsFor.id !== run.id) followsFor = { id: run.id, value: followsTaskList((await linesOf($, run))[0]) }
  return followsFor.value
}

/** The run's lines when it follows the task list, else null: the write line and the user's toast sentence read the
 *  task list's mark from them (BEH-08, BEH-12). */
async function followingLines($: E, run: ProgressRun): Promise<readonly string[] | null> {
  return (await follows($, run)) ? linesOf($, run) : null
}

/** What a compaction of a run that follows the task list keeps, and its closing note (BEH-24). The marked step counts
 *  only when the last evaluation's steps have it, with its title from there; with no evaluation yet, its number alone.
 *  `reached` is true when that evaluation shows every step reached, which leaves the note out (version 8). */
async function compactNotes($: E, run: ProgressRun): Promise<{ marked: number | null; reached: boolean; instruction: string; note: string }> {
  const lines = await linesOf($, run)
  let state: ProgressState | null = null
  try {
    state = JSON.parse(await $.fs.read(`${run.dir}/state.json`)) as ProgressState
  } catch {
    // no evaluation yet
  }
  const steps = state !== null && Array.isArray(state.steps) ? state.steps : null
  const marked = markedStep(lines, Infinity, steps)
  const label = marked === null ? null : steps !== null ? stepLabel(steps, marked) : `step ${marked}`
  const reached = state !== null && state.current === null && state.ended === null
  return { marked, reached, ...compactTexts(run.skill, label) }
}

/** Whether the session has a task list, from the tools it offers now, deferred ones included (DM-01); when the list
 *  can't be read, none, and `read` is false, so no hint blames the session's tools (ERR-14). */
async function taskListOf($: E): Promise<{ taskList: boolean; read: boolean }> {
  try {
    return { taskList: hasTaskList((await $.tool.list()).map(t => t.name)), read: true }
  } catch (err) {
    await adapterLog($, 'tools', firstLine(message(err)))
    return { taskList: false, read: false }
  }
}

/** Step events from a task tool's call that didn't fail, recorded after its tool event, in the run it was recorded
 *  into, inside the same chain item (BEH-20, ERR-13): the tool event, its step events and its task map land together. */
async function taskStepsNow($: E, into: string, tool: string, input: Fields, outcome: ToolOutcome): Promise<void> {
  if (isFailed(outcome)) return
  const l = await hydrate($)
  if (l.run === null || l.run.id !== into) return
  if (tool === 'TaskCreate') {
    const id = taskIdOf(outcome.text)
    const step = stepOfTask(input)
    if (id === null || step === null) {
      // The subject is the model's text: one line of it, so it can't add lines of its own to adapter.log.
      await adapterLog($, 'task', `no step for task: ${firstLine(String(input.subject ?? ''))}`)
      return
    }
    await putFor($, into, x => ({ tasks: { ...x.tasks, [id]: step } }))
  } else if (tool === 'TaskUpdate') {
    const step = l.tasks[String(input.taskId)]
    const state = stepStateOf(input.status)
    if (step !== undefined && state !== null) await recordNow($, 'step', { step, state }, true)
  } else if (tool === 'TodoWrite') {
    const result = (outcome as Fields).result
    let events: Fields[] = []
    await putFor($, into, x => {
      const got = todoSteps(input.todos, x.todos, result && typeof result === 'object' ? (result as Fields).oldTodos : undefined)
      events = got.events
      return { todos: got.statuses }
    })
    for (const e of events) await recordNow($, 'step', e, true)
  }
}

/** Take an evaluation in: the session's current.json, the summary, toasts, the report gate's context (BEH-06, BEH-09,
 *  BEH-12). */
async function absorb($: E, run: ProgressRun, got: { state: ProgressState; text: string }): Promise<void> {
  // One at a time: the run-end evaluation and a timer's can finish together, and each reads the shown flags and
  // adhered before it writes them, so a notice could otherwise show twice.
  const step = absorbChain.then(() => absorbNow($, run, got))
  absorbChain = step.catch(() => undefined)
  await step
}

async function absorbNow($: E, run: ProgressRun, got: { state: ProgressState; text: string }): Promise<void> {
  // An evaluation whose run isn't the open run changes nothing: a push, an unwind or a switch came first (BEH-30).
  if ((await hydrate($)).run?.id !== run.id) return
  try {
    await $.fs.write(`${await sessionDir($, rootOf(run))}/current.json`, got.text)
  } catch {
    // renderers read current.json; the run's own state.json is written
  }
  const off = await read($, OFF)
  if (off !== null && off !== LOG_FULL && off !== NO_PYTHON && off !== NO_WRITE) await update($, OFF, () => null)
  const following = await followingLines($, run)
  let fresh: { keys: string[]; toasts: string[] } = { keys: [], toasts: [] }
  // The stopping answer's step stays with a stopped run's summary (BEH-10, version 12).
  const open = await putFor($, run.id, l => {
    fresh = newFlagToasts(got.state, l.shown, following)
    return { summary: { ...summaryOf(got.state), stoppedAt: got.state.ended === 'stopped' ? l.summary?.stoppedAt ?? null : null },
      ...(fresh.keys.length ? { shown: [...l.shown, ...fresh.keys] } : {}) }
  })
  if (!open) return
  for (const toast of fresh.toasts) await notify($, toast)
  if (got.state.current === null && got.state.ended === null && allReachedFor !== run.id) {
    allReachedFor = run.id
    await notify($, `✓ ${got.state.skill}: all steps reached`)
  }
  // SPEC-012 §4's second level: a run that follows the task list and didn't keep it is told so once (BEH-22).
  const adherence = adherenceText(got.state)
  // $.state's adhered decides, so a reload of the module doesn't repeat the notice (version 6).
  if (adherence !== null && (await get($, 'adhered')) !== run.id && (await follows($, run))
    && (await putFor($, run.id, () => ({ adhered: run.id })))) {
    await notify($, adherence)
    await adapterLog($, 'adherence', adherence)
  }
  const report = reportContext(got.state)
  const l = await hydrate($)
  if (l.run?.id === run.id) {
    pendingReport = report !== null && !l.contextSent.includes(report.seq) && got.state.ended === null ? { ...report, run: run.id } : null
  }
  await refreshStatus($)
}

/** The timer's work (BEH-06): it catches every error itself, since one it let escape reaches only the debug log (ERR-10). */
async function tick($: E): Promise<void> {
  try {
    await refreshStatus($)
    if (evaluating || disabled || !(await get($, 'marked'))) return
    inFlight = evaluateMarked($)
    await inFlight
  } catch (err) {
    await failOpen($, `timer: ${message(err)}`).catch(() => undefined)
  }
}

/** One evaluation of the open run, as the timer runs it (BEH-06); the review waits for it (BEH-26). */
async function evaluateMarked($: E): Promise<void> {
  evaluating = true  // before any await, so the timer and the review never start two evaluations
  try {
    const run = await get($, 'run')
    if (run === null) return
    try {
      await putFor($, run.id, () => ({ marked: false }))
      // The folder's .gitignore may have gone with a `git clean` while the run went on (BEH-15).
      await ensureIgnore($, rootOf(run)).catch(() => undefined)
      const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, EVALUATOR_TIMEOUT)
      const open = await get($, 'run')
      // A run that opened, paused or resumed while the evaluator ran keeps its own summary and flags (the module's values).
      if (open === null || open.id !== run.id) return
      if (typeof got === 'string') await failOpen($, got)
      else await absorb($, run, got)
    } finally {
      evaluating = false
    }
  } finally {
    evaluating = false
    inFlight = null
  }
}

function ensureTimer($: E): void {
  if (timerOn) return
  timerOn = true
  $.clock.every(500, () => {
    void tick($)
  })
}

/** What every interactive session does first: python, the mode, the timer (BEH-01, BEH-06, BEH-16, BEH-17). */
async function setup($: E): Promise<void> {
  await findPython($)
  await resolveMode($, await $.session.root())
  ensureTimer($)
  const run = await get($, 'run')
  if (run !== null) {
    // After a reload the module's variables start over; the open run's folder exists, so its log goes there.
    await useLogRoot($, rootOf(run))
    await put($, 'marked', () => true)
  }
}

/** A new run whose skill-loaded line is written but which isn't open yet (BEH-03, BEH-29). */
type Opening = { run: ProgressRun; line: string; now: number; session: string; r: string; listed: boolean; taskList: boolean; checklist: string }

/** Write a new run's skill-loaded line in its own folder, in the root read as it loaded (BEH-03); null when nothing can be
 *  opened (ERR-03 has stopped tracking). Opening it is the caller's change, made with no await (version 14). */
async function prepareRun($: E, r: string, skill: string, checklist: string): Promise<Opening | null> {
  if (!(await ensureDir($, r))) return null
  const session = await $.session.id()
  // The mode is resolved here, after the folder exists, so a new root's mode line lands in that root's log (BEH-16).
  if (modeSession !== session || modeRoot !== r) await resolveMode($, r)
  const now = await $.clock.now()
  const id = runId(now, skill, crypto.getRandomValues(new Uint8Array(4)))
  const dir = `${progressDir(r)}/runs/${id}`
  const version = await $.session.version()
  const { taskList, read: listed } = await taskListOf($)
  const line = eventLine(id, 1, now, 'skill-loaded', {
    format: FORMAT, skill, checklist, host: `claude-code ${version.version}`, taskList,
    mode: await read($, MODE), modeSource: await read($, SOURCE),
  })
  const run: ProgressRun = { id, skill, seq: 1, dir, root: r }
  if (!(await writeLog($, run, [line], false))) return null
  return { run, line, now, session, r, listed, taskList, checklist }
}

/** A new run's values: the open one, with empty values (BEH-20: a list left from an earlier run gives no step events;
 *  BEH-25, BEH-26: the stuck notice and the review count per run). */
function opened(o: Opening): Partial<Live> {
  return { run: o.run, lastEventAt: o.now, marked: true, summary: null, shown: [], contextSent: [], tasks: {}, todos: {},
    refusals: {}, refused: [] }
}

/** After a new run is open: its lines, the off reason a full log left, the task-tools hint, pruning. */
async function afterOpen($: E, o: Opening): Promise<void> {
  held = { id: o.run.id, lines: [o.line] }
  if ((await read($, OFF)) === LOG_FULL) await update($, OFF, () => null)
  // A skill that follows the convention, in a session with no task tools, is placed by guessing: say so once (BEH-23).
  if (o.listed && !o.taskList && o.checklist.includes(TASK_TAG) && !(await read($, HINTED))) {
    const hint = hintText(o.run.skill)
    await update($, HINTED, () => true)
    await notify($, hint)
    await adapterLog($, 'tools-hint', hint)
  }
  await startPrune($, o.r, o.session, o.run.id)
}

/** The run-end of the open run, inside a chain item (BEH-05); the run as it ended, or null with no open run. */
async function endOpenNow($: E, reason: string): Promise<ProgressRun | null> {
  const run = await get($, 'run')
  if (run === null) return null
  await recordNow($, 'run-end', { reason }, true)
  pendingReport = null
  return (await get($, 'run')) ?? run
}

/** A load that doesn't nest (BEH-03, BEH-29): the open run ends with another-skill (a load that isn't Claude's ends every
 *  paused run too, bottom first, and empties the trail), is evaluated once more, and the new run opens. Two chain items
 *  with the evaluation between them, so no item holds an evaluation. */
async function switchRun($: E, r: string, name: string, checklist: string, endPaused: boolean): Promise<void> {
  const ended = await chained(async () => {
    const l = await hydrate($)
    if (endPaused && l.trail.length) {
      for (const p of l.trail) if (p.run !== null) await appendEvent($, p.run, 'run-end', { reason: 'another-skill' }, false)
      await putMany($, () => ({ trail: [] }))
      await adapterLog($, 'trail', 'empty (a load with no Skill call of the main loop in flight)')
    }
    return endOpenNow($, 'another-skill')
  })
  await finishSwitch($, r, name, checklist, ended, endPaused)
}

/** The rest of a switch: the ended run's last evaluation, then the new run, as one chain item. */
async function finishSwitch($: E, r: string, name: string, checklist: string, ended: ProgressRun | null, emptyTrail: boolean): Promise<void> {
  if (ended !== null) await finalEvaluation($, ended, EVALUATOR_TIMEOUT)
  await chained(async () => {
    await endOpenNow($, 'another-skill')  // a run an unwind resumed meanwhile ends too; the ended one is skipped
    const o = await prepareRun($, r, name, checklist)
    if (o === null) return
    await putMany($, () => {
      onSwitch()
      return { ...opened(o), ...(emptyTrail ? { trail: [] } : {}) }
    })
    await afterOpen($, o)
  })
}

/** Prune old run and session folders once per session ID and root, after the run's folder exists; nothing waits
 *  for it, and its result or failure goes to adapter.log only (BEH-19, ERR-12). */
async function startPrune($: E, r: string, session: string, keepRun: string): Promise<void> {
  if (!python) return
  const key = `${session}\n${r}`
  if (pruned.has(key)) return
  pruned.add(key)
  const argv = [python, `${$.plugin.root}/progress/prune.py`, 'prune', '--root', r, '--days', String(retentionDays),
    '--keep-session', session, '--keep-run', keepRun]
  try {
    void $.process.run(argv, { cwd: r, timeoutMs: PRUNE_TIMEOUT }).then(
      res => adapterLog($, 'prune', res.exitCode === 0 ? firstLine(res.stdout) : firstLine(res.stderr) || `exit ${res.exitCode}`),
      err => adapterLog($, 'prune', firstLine(message(err))),
    ).catch(() => undefined)
  } catch (err) {
    // Pruning never tells the user anything: its failure is a log line (ERR-12).
    await adapterLog($, 'prune', firstLine(message(err)))
  }
}

/** Evaluate an ended run once more when there is time (BEH-05); taken in only while it is still the open run. */
async function finalEvaluation($: E, run: ProgressRun, timeoutMs: number | null): Promise<void> {
  if (timeoutMs === null || !python) return
  await putFor($, run.id, () => ({ marked: false }))
  const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, timeoutMs)
  if (typeof got !== 'string') await absorb($, run, got)
}

/** The state the run would have with one more event (BEH-08, BEH-21): the run's lines and the pending event in
 *  pending.jsonl, evaluated; null when it can't be had, which lets the call go on (fail open). */
async function pendingState($: E, kind: string, fields: Fields): Promise<{ state: ProgressState; seq: number; lines: readonly string[]; run: ProgressRun } | null> {
  await recordChain  // events still being written are part of the run the check judges
  const run = await get($, 'run')
  if (run === null) return null
  const lines = [...(await linesOf($, run))]
  const seq = lines.length + 1
  const line = eventLine(run.id, seq, await $.clock.now(), kind, fields)
  try {
    await $.fs.write(`${run.dir}/pending.jsonl`, [...lines, line].join('\n') + '\n')
  } catch {
    return null
  }
  const got = await evaluate($, rootOf(run), `${run.dir}/pending.jsonl`, `${run.dir}/pending.json`, EVALUATOR_TIMEOUT)
  if (typeof got === 'string') {
    await failOpen($, got)
    return null
  }
  return { state: got.state, seq, lines, run }
}

/** The same refusal twice in a run tells the user once (BEH-25): counted by the gate's kind and the first flag raised
 *  at the refused seq, in $.state's refusals, which a new run empties. */
async function noteRefusal($: E, state: ProgressState, seq: number, run: ProgressRun): Promise<void> {
  try {
    const cause = refusalCause(state, seq)
    if (cause === null) return
    // Every refusal is kept for the run's review: a refused question leaves no event (BEH-25, BEH-26). Kept in the run
    // the check judged, while it is still the open run (version 14).
    const gate = state.gate.kind ?? 'write'
    let count = 0
    const kept = await putFor($, run.id, l => {
      count = (l.refusals[cause.key] ?? 0) + 1
      return { refused: [...l.refused, { gate, seq, step: cause.step, type: cause.type, message: cause.message }],
        refusals: { ...l.refusals, [cause.key]: count } }
    })
    if (!kept || count !== 2) return
    const text = stuckText(run.skill, cause.step, cause.message, stuckAdvice(cause.type, cause.userOwned))
    await notify($, text)
    await adapterLog($, 'stuck', text)
  } catch (err) {
    // The notice is the user's; failing to give it never lets a refused call through (review N1).
    await recover($, 'tool.call', err)
  }
}

/** The deliberate stop (BEH-27, version 12): an answer of 'Write nothing' to one question tagged with a step the latest
 *  state marks stoppable ends the run with run-end stopped. A state that can't be read stops nothing. A nested run's
 *  stop resumes the run just beneath (BEH-30 (b), version 14). */
async function stopIfAsked($: E, input: Fields, outcome: ToolOutcome): Promise<void> {
  const run = await get($, 'run')
  if (run === null) return
  let state: ProgressState
  try {
    state = JSON.parse(await $.fs.read(`${run.dir}/state.json`)) as ProgressState
  } catch {
    return
  }
  if (!stopsRun(input, outcome, state.steps ?? [])) return
  const n = questionTag(input).step ?? null
  // The run-end marks the run and the timer evaluates it: no tool call waits for an evaluation (BEH-06).
  const resumed = await chained(async () => {
    if ((await get($, 'run'))?.id !== run.id) return false
    await endOpenNow($, 'stopped')
    await putFor($, run.id, l => ({ summary: l.summary === null ? null : { ...l.summary, stoppedAt: n } }))
    const trail = (await hydrate($)).trail
    const top = trail[trail.length - 1]
    return top !== undefined && top.run !== null && unwindNow($, top.run.id)
  })
  if (resumed) await refreshStatus($)
}

/** A load Claude made with its Skill tool (BEH-29): what it came to. */
type LoadOutcome = { kind: 'own' } | { kind: 'unwound' } | { kind: 'pushed'; line: string } | { kind: 'cannot'; ended: ProgressRun | null } | { kind: 'failed' }

/** Claude's load of a tracked skill, as one chain item (BEH-29): of the open run's own skill, nothing; of a paused run's
 *  skill, an unwind to it (BEH-30 (d)); else a push when the open run can nest, or the open run's end. */
async function claudeLoadNow($: E, r: string, name: string, checklist: string): Promise<LoadOutcome> {
  const l = await hydrate($)
  const open = l.run
  if (open !== null && open.skill === name) return { kind: 'own' }
  const back = l.trail.find(t => t.skill === name && t.run !== null)
  if (back !== undefined) return (await unwindNow($, back.run!.id)) ? { kind: 'unwound' } : { kind: 'failed' }
  const step = await returnStepNow($)
  // A run that can't nest (no task IDs, no known step) ends, and the paused runs stay paused (BEH-03 for the open run).
  if (open === null || step === null) return { kind: 'cannot', ended: await endOpenNow($, 'another-skill') }
  const o = await prepareRun($, r, name, checklist)
  if (o === null) return { kind: 'failed' }
  const pushed = await putMany($, x => {
    if (x.run === null || x.run.id !== open.id) return null
    onSwitch()
    return { trail: [...x.trail, pausedOf(x, step)], ...opened(o) }
  })
  if (!pushed) return { kind: 'failed' }
  await afterOpen($, o)
  await adapterLog($, 'trail', `push ${open.skill} at step ${step} (${(await hydrate($)).trail.length} on the trail)`)
  return { kind: 'pushed', line: returnLine(open.skill, step) }
}

/** The open run's return step, or null when it can't nest (BEH-29): it hasn't ended, it has task IDs, and its task list
 *  marks a step (filtered by its last state's steps), else its summary has a current step. */
async function returnStepNow($: E): Promise<number | null> {
  const l = await hydrate($)
  const run = l.run
  if (run === null || (l.summary !== null && l.summary.ended !== null) || Object.keys(l.tasks).length === 0) return null
  const lines = await linesOf($, run)
  if (lines.some(x => x.includes('"kind":"run-end"'))) return null  // stopped, its run-end not yet evaluated
  let steps: ProgressState['steps'] | null = null
  try {
    steps = (JSON.parse(await $.fs.read(`${run.dir}/state.json`)) as ProgressState).steps ?? null
  } catch {
    // no evaluation yet: the marked step stands as the task list gives it
  }
  return markedStep(lines, Infinity, steps) ?? l.summary?.current ?? null
}

/** The open run as a trail entry (DM-03 ProgressPaused). */
function pausedOf(l: Live, step: number): ProgressPaused {
  return { skill: l.run!.skill, step, tasks: { ...l.tasks }, run: l.run, summary: l.summary, marked: l.marked, shown: l.shown,
    contextSent: l.contextSent, todos: l.todos, adhered: l.adhered, refusals: l.refusals, refused: l.refused, reviewed: l.reviewed }
}

/** Unwind the trail to the paused run `target`, as one chain item (BEH-30): run-end returned in each run above it that
 *  hasn't ended, top first, each kept in returned for the turn's review with a stopped open run; then the target opens
 *  with its saved values. False when there is nothing to unwind (a queued unwind re-tests its condition). */
async function unwindNow($: E, target: string): Promise<boolean> {
  const l = await hydrate($)
  const open = l.run
  const at = l.trail.findIndex(t => t.run !== null && t.run.id === target)
  if (at < 0 || open === null) return false
  const openRefused = l.refused
  const openReviewed = l.reviewed
  const above = l.trail.slice(at + 1)
  const back: ProgressReturned[] = []
  await recordNow($, 'run-end', { reason: 'returned' }, true)  // a stopped run keeps its one run-end
  const top = await get($, 'run')
  if (top === null || top.id !== open.id) return false  // its log couldn't be written: tracking stopped
  const why = endReason(await linesOf($, top))
  // A run whose review was already asked isn't asked again (BEH-26).
  if ((why === 'returned' || why === 'stopped') && openReviewed !== open.id) back.push({ run: top, refused: openRefused, reason: why })
  for (let i = above.length - 1; i >= 0; i--) {
    const p = above[i]
    if (p.run === null) continue
    const got = await appendEvent($, p.run, 'run-end', { reason: 'returned' }, false)
    if (p.reviewed !== p.run.id) back.push({ run: got?.run ?? p.run, refused: p.refused, reason: 'returned' })
  }
  const now = await $.clock.now()
  const t = l.trail[at]
  const resumed = await putMany($, x => {
    if (x.run === null || x.run.id !== open.id || x.trail[at]?.run?.id !== target) return null
    onSwitch()
    return { trail: x.trail.slice(0, at), returned: [...x.returned, ...back], run: t.run, summary: t.summary, lastEventAt: now,
      marked: true, shown: t.shown, contextSent: t.contextSent, tasks: t.tasks, todos: t.todos, adhered: t.adhered,
      refusals: t.refusals, refused: t.refused, reviewed: t.reviewed }
  })
  if (resumed) await adapterLog($, 'trail', `unwind to ${t.skill} at step ${t.step} (${above.length + 1} returned, ${at} on the trail)`)
  return resumed
}

/** BEH-30 (c): at an answered turn's end, after its events are recorded and evaluated, an open nested run whose state shows
 *  every step reached returns, and the run just beneath resumes with a turn end of its own: one level per turn end. */
async function turnEndUnwind($: E): Promise<void> {
  await settle($)
  const reached = (l: Live) => l.run !== null && l.trail.length > 0 && l.summary !== null && l.summary.current === null && l.summary.ended === null
  const first = await hydrate($)
  if (!reached(first)) return
  const openId = first.run!.id
  const resumed = await chained(async () => {
    const l = await hydrate($)
    const top = l.trail[l.trail.length - 1]
    if (!reached(l) || l.run!.id !== openId || top.run === null) return false
    return unwindNow($, top.run.id)
  })
  if (!resumed) return
  await record($, 'turn', { phase: 'end' }, false)
  await refreshStatus($)
}

/** The compaction's last message names the trail while it isn't empty and a run is open (BEH-29); an earlier one goes. */
async function withTrailNote<T>($: E, run: ProgressRun, out: T): Promise<T> {
  try {
    const trail = await get($, 'trail')
    const o = out as unknown as { messages?: { role: string; text?: unknown; toolUses: unknown[] }[] }
    if (!trail.length || !Array.isArray(o.messages)) return out
    const kept = o.messages.filter(m => !(typeof m.text === 'string' && m.text.startsWith(TRAIL_NOTE_START)))
    return { ...o, messages: [...kept, { role: 'user' as const, text: trailNote(run.skill, trail), toolUses: [] }] } as unknown as T
  } catch (err) {
    await recover($, 'session.compact', err)
    return out
  }
}

/** The end-of-run review (BEH-26, ERR-15): once every step of the open run is reached, once per run, in a session
 *  where something draws, each item (one per cause) is asked in Claude Code's own dialog, Accept or Challenge, and the
 *  answers go to the run's review.jsonl and adapter.log. Nothing is sent to Claude. */
async function review($: E): Promise<void> {
  // The review judges the state the turn ended in: events still being written, an evaluation under way and events
  // not yet evaluated come first, so a last step reached in the turn's final reply is seen (review M1).
  await settle($)
  const run = await get($, 'run')
  const summary = await get($, 'summary')
  if (run === null || summary === null) return
  // Every step reached with the run open, or a run the user stopped (BEH-27; version 12).
  if (summary.ended !== 'stopped' && (summary.current !== null || summary.ended !== null)) return
  if ((await get($, 'reviewed')) === run.id) return
  // Where nothing draws, or the surfaces can't be read, no dialog can be answered: no review (BEH-26).
  let surfaces: readonly unknown[] = []
  try {
    surfaces = await $.session.surfaces()
  } catch {
    return
  }
  if (surfaces.length === 0) return
  let flags: ProgressState['flags'] = []
  try {
    flags = (JSON.parse(await $.fs.read(`${run.dir}/state.json`)) as ProgressState).flags ?? []
  } catch {
    flags = []
  }
  const items = reviewItems(await get($, 'refused'), flags)
  if (items.length === 0) return
  if (!(await putFor($, run.id, () => ({ reviewed: run.id })))) return
  await askReview($, run, items)
}

/** The runs that returned or stopped while nested this turn (BEH-26, BEH-30; version 14), top first, before the open
 *  run's own review: each evaluated once more from its own log (not taken in), and asked when it has an item, whether
 *  or not every step was reached. Each leaves returned as it is taken; where nothing draws, all are dropped unasked. */
async function reviewReturned($: E): Promise<void> {
  if ((await hydrate($)).returned.length === 0) return
  let draws = false
  try {
    draws = (await $.session.surfaces()).length > 0
  } catch {
    draws = false
  }
  if (!draws) {
    await putMany($, () => ({ returned: [] }))
    return
  }
  for (;;) {
    const entry = (await hydrate($)).returned[0]
    if (entry === undefined) return
    await putMany($, l => ({ returned: l.returned.filter(x => x !== entry) }))
    const run = entry.run
    if (run === null) continue
    const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, EVALUATOR_TIMEOUT)
    let flags: ProgressState['flags'] = []
    if (typeof got !== 'string') flags = got.state.flags ?? []
    else {
      try {
        flags = (JSON.parse(await $.fs.read(`${run.dir}/state.json`)) as ProgressState).flags ?? []
      } catch {
        flags = []
      }
    }
    const items = reviewItems(entry.refused, flags)
    if (items.length) await askReview($, run, items, entry.reason)
  }
}

/** One run's review dialog (BEH-26, ERR-15): each item asked in Claude Code's own dialog, Accept or Challenge, the
 *  answers in the run's review.jsonl and adapter.log; a dismissal leaves the rest of this run's items unasked. */
async function askReview($: E, run: ProgressRun, items: ReviewItem[], ended?: 'returned' | 'stopped'): Promise<void> {
  const lines: string[] = []
  let dismissed: string | null = null
  let said = false
  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    let answer = 'dismissed'
    let reason: string | null = null
    if (dismissed === null) {
      try {
        const got = await $.ui.ask(reviewQuestion(run.skill, i + 1, items.length, item),
          { options: ['Accept', 'Challenge'], header: 'Review' })
        if (got === 'Accept') answer = 'accept'
        else {
          answer = 'challenge'
          reason = got === 'Challenge' ? null : got
        }
      } catch (err) {
        dismissed = firstLine(message(err)) || 'dismissed'
      }
    }
    const now = new Date(await $.clock.now()).toISOString().replace(/\.\d{3}Z$/, 'Z')
    lines.push(JSON.stringify({ time: now, run: run.id, item: i + 1, gate: item.gate, seq: item.seq, step: item.step,
      type: item.type, message: item.message, refused: item.count, answer, reason }))
    try {
      await $.fs.write(`${run.dir}/review.jsonl`, lines.join('\n') + '\n')
    } catch {
      // the review's record can't be kept; the answers still go to adapter.log
    }
    // ERR-15: the item the dialog was dismissed on names why; the ones after it were never asked.
    const why = dismissed !== null && !said ? ` (${dismissed})` : ''
    if (why) said = true
    const whose = ended === undefined ? '' : `${run.skill} ${run.id} (${ended}) `
    await adapterLog($, 'review', `${whose}${i + 1}/${items.length} ${answer}: ${item.step} ${item.type}${why}`)
  }
  await notify($, `${run.skill}: your review is in devforgeai/progress/runs/${run.id}/review.jsonl`)
}

/** Enforce mode's write-gate check (BEH-08): the refusal text, or null to let the call go on. */
async function enforceCheck($: E, fields: Fields, content: string | null): Promise<string | null> {
  const got = await pendingState($, 'tool', { ...fields, exit: 0, error: false, content: keptContent(content, await logBytes($)) })
  const run = await get($, 'run')
  if (got === null) return null
  const refusal = refusalText(got.state, got.seq, run !== null && (await follows($, run)) ? got.lines : null)
  if (refusal !== null) await noteRefusal($, got.state, got.seq, got.run)
  return refusal
}

/** A refused question's first line as a toast (BEH-12), and where nothing draws its whole text in the transcript
 *  (BEH-21). */
async function refusedToast($: E, refusal: string): Promise<void> {
  try {
    await $.ui.toast(firstLine(refusal))
    if (!(await hasSurface($))) await $.ui.log(refusal)
  } catch {
    // a notice that can't be shown changes nothing
  }
}

/** Enforce mode's question check (BEH-21): the evaluator decides whether the run follows the task list. The pending
 *  answer carries the question's step tag, and the refusal's text follows the question gate's flag (version 8). */
async function questionCheck($: E, input: Fields): Promise<string | null> {
  if (taskWork.size > 0) await Promise.race([Promise.allSettled([...taskWork]), $.clock.sleep(TASK_WAIT_MS)])
  const tag = questionTag(input)
  const got = await pendingState($, 'answer', { answered: true, ...tag })
  if (got === null) return null
  // The mark and the tag as the check judged them: the lines written to pending.jsonl (review N2), and a tag naming a
  // step the checklist has (review N3; SPEC-012 ERR-06).
  const marked = markedStep(got.lines, Infinity, got.state.steps)
  const tagged = tag.step !== undefined && got.state.steps.some(s => s.n === tag.step)
  const refusal = questionRefusal(got.state, got.seq, marked, tagged)
  if (refusal !== null) await noteRefusal($, got.state, got.seq, got.run)
  return refusal
}

/** The band's button: save the other mode with settings.py (IF-02, BEH-13). */
async function switchMode($: E): Promise<void> {
  const target: ProgressMode = (await read($, MODE)) === 'enforce' ? 'observe' : 'enforce'
  if (!python) {
    await notify($, `DevForgeAI progress: couldn't save progress.mode (${NO_PYTHON})`)
    return
  }
  const open = await get($, 'run')
  const r = open !== null ? rootOf(open) : await $.session.root()
  let res
  try {
    res = await $.process.run([python, `${$.plugin.root}/progress/settings.py`, 'set-mode', '--root', r, '--value', target],
      { cwd: r, timeoutMs: EVALUATOR_TIMEOUT })
  } catch (err) {
    await notify($, `DevForgeAI progress: couldn't save progress.mode (${message(err)})`)
    return
  }
  if (res.exitCode !== 0) {
    const why = firstLine(res.stderr) || `exit ${res.exitCode}`
    await adapterLog($, 'error', `set-mode: ${why}`)
    await notify($, `DevForgeAI progress: couldn't save progress.mode (${why})`)
    return
  }
  await update($, MODE, () => target)
  await update($, SOURCE, () => 'local')
  const run = await get($, 'run')
  await adapterLog($, 'switch', `${target} (local), at seq ${run?.seq ?? 0}`)
  await notify($, `DevForgeAI progress: ${target} mode, saved to .claude/devforgeai.local.md`)
  await refreshStatus($)
}

async function recording($: E, agentId: unknown): Promise<boolean> {
  return interactive === true && !disabled && agentId === undefined && (await get($, 'run')) !== null
}

export const register: Register = (on, options) => {
  // With tracking off, the adapter does nothing at all (BEH-01, DM-05).
  if ((options as Fields | undefined)?.tracking === 'off') return
  retentionDays = retentionOf((options as Fields | undefined)?.retentionDays)

  on('session.start', async ($, e, next) => {
    interactive = e.isInteractive
    if (interactive) await setup($)
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'session.start', next.error)
    return next(e)
  })

  // After /clear, /resume or /branch no session.start fires, and $.state is empty (BEH-06, BEH-16).
  on('classic.SessionStart', { source: ['clear', 'resume', 'fork'] }, async ($, e, next) => {
    if (interactive === true && !disabled) {
      await resolveMode($, await $.session.root())
      ensureTimer($)
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'classic.SessionStart', next.error)
    return next(e)
  })

  // A second headless signal (BEH-01; §9, P8).
  on('prompt.compose', async ($, e, next) => {
    if ((e.traits ?? []).includes('print')) interactive = false
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'prompt.compose', next.error)
    return next(e)
  })

  on('skill.prompt', async ($, e, next) => {
    const out = await next(e)
    if (interactive !== true || disabled) return out
    try {
      const name = skillName(e.skill)
      // One read of the root serves every decision as the run opens (BEH-03): tracked, the folder, the mode.
      const r = await $.session.root()
      if (!(await tracked($, r, name))) return out
      ensureTimer($)
      // A load that isn't Claude's (typed, or a subagent's) ends the open run and every paused run (BEH-03, BEH-29).
      if (!skillsLoading.has(name)) {
        await switchRun($, r, name, out.text, true)
        return out
      }
      // Claude's load (BEH-29): task-tool calls under way first, so a TaskUpdate of the same batch sets the return step.
      if (taskWork.size > 0) await Promise.race([Promise.allSettled([...taskWork]), $.clock.sleep(TASK_WAIT_MS)])
      const got = await chained(() => claudeLoadNow($, r, name, out.text))
      // The Skill call records nothing in either run once the open run changed (before skill.prompt returns).
      if (got.kind !== 'own') switchedIn.add(name)
      if (got.kind === 'cannot') await finishSwitch($, r, name, out.text, got.ended, false)
      await refreshStatus($)
      if (got.kind === 'pushed') return { ...out, text: `${out.text}\n\n${got.line}` }
    } catch (err) {
      // After next, a failure is the adapter's own: tell the user, keep the skill's text (BEH-14).
      await recover($, 'skill.prompt', err)
    }
    return out
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'skill.prompt', next.error)
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    // The open run's tenure as this hook began, before any await (BEH-30 (a)).
    const began = tenure
    const input = e as unknown as Fields
    const tool = String(input.tool)
    // Registered before any await, so a question in the same batch finds it (BEH-21).
    const finish = TASK_TOOLS.includes(tool) ? startTaskWork() : null
    // The skills the main loop's Skill calls in flight are loading (BEH-29): skill.prompt fires inside the call.
    const loading = tool === 'Skill' && input.agentId === undefined && typeof input.skill === 'string' ? skillName(input.skill) : null
    if (loading !== null) skillsLoading.set(loading, (skillsLoading.get(loading) ?? 0) + 1)
    try {
      if (!(await recording($, input.agentId))) return next(e)
      if (tool === 'AskUserQuestion') {
        // Claude Code's own question only: a mod's $.ui.ask arrives here too (BEH-04, BEH-21).
        // The waiver question is never a question gate, so it isn't checked (BEH-21, version 10).
        if (isEngine(next.origin) && (await read($, MODE)) === 'enforce' && python && !isWaiverQuestion(input)) {
          let refusal: string | null = null
          try {
            refusal = await questionCheck($, input)
          } catch (err) {
            // A check that fails lets the question go on, and its answer is still recorded (fail open).
            await recover($, 'tool.call', err)
          }
          if (refusal !== null) {
            // The user never saw the question, so nothing is recorded for it.
            await adapterLog($, 'refused', firstLine(refusal))
            await refusedToast($, refusal)
            return { deny: refusal }
          }
        }
        const result = await next(e)
        try {
          // A mod's $.ui.ask arrives here too; only Claude Code's own question is the user's answer (BEH-04).
          if (isEngine(next.origin)) {
            const outcome = result as unknown as ToolOutcome
            await record($, 'answer', isWaiverQuestion(input)
              ? { answered: isAnswered(outcome), waiver: waiverAnswer(input, outcome) }
              : { answered: isAnswered(outcome), ...questionTag(input) }, true, began)
            if (!isWaiverQuestion(input)) await stopIfAsked($, input, outcome)
          }
        } catch (err) {
          await recover($, 'tool.call', err)
        }
        return result
      }
      const open = await get($, 'run')
      const r = open !== null ? rootOf(open) : await $.session.root()
      const content = await contentOf($, r, tool, input)
      const fields: Fields = {
        tool,
        path: toolPath(r, tool, input),
        command: tool === 'Bash' && typeof input.command === 'string' ? input.command : undefined,
      }
      if ((tool === 'Write' || tool === 'Edit') && (await read($, MODE)) === 'enforce' && python) {
        const refusal = await enforceCheck($, fields, content)
        if (refusal !== null) {
          await record($, 'tool', { ...fields, exit: null, error: true, content: keptContent(content, await logBytes($)) }, true, began)
          await adapterLog($, 'refused', firstLine(refusal.split('\n')[1] ?? refusal))
          if (!(await hasSurface($))) await $.ui.log(refusal)
          return { deny: refusal }
        }
      }
      const result = await next(e)
      if (loading !== null && switchedIn.delete(loading)) return result
      try {
        const outcome = result as unknown as ToolOutcome
        const done: Fields = { ...fields, exit: exitOf(outcome), error: isFailed(outcome), content: keptContent(content, await logBytes($)) }
        let resumed = false
        // One chain item: the unwind a TaskUpdate shows (BEH-30 (a)), before its own events, then its tool event, step
        // events and task map, all in the run open when they land.
        await chained(async () => {
          if (tool === 'TaskUpdate' && !isFailed(outcome) && worked) {
            const trail = (await hydrate($)).trail
            const at = pausedWith(trail, input.taskId)
            if (at >= 0 && trail[at].run !== null) resumed = await unwindNow($, trail[at].run!.id)
          }
          const into = await recordNow($, 'tool', done, true, began)
          if (into !== null && TASK_TOOLS.includes(tool)) await taskStepsNow($, into, tool, input, outcome)
        })
        if (resumed) await refreshStatus($)
      } catch (err) {
        await recover($, 'tool.call', err)
      }
      return result
    } finally {
      finish?.()
      if (loading !== null) {
        const n = (skillsLoading.get(loading) ?? 1) - 1
        if (n > 0) skillsLoading.set(loading, n)
        else {
          skillsLoading.delete(loading)
          switchedIn.delete(loading)
        }
      }
    }
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'tool.call', next.error)
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    if (!(await recording($, undefined))) return next(e)
    // A prompt that starts with '/' runs a command or loads a skill; it is no answer. The one that loads a skill
    // arrives here after skill.prompt has opened the run (VER-15's dogfood run found it counted for step 5).
    if (isPersonPrompt(e.origin) && isEngine(next.origin) && !e.text.trimStart().startsWith('/')) await record($, 'prompt', {})
    const report = pendingReport
    if (report !== null && (await read($, MODE)) === 'enforce' && !e.text.trimStart().startsWith('/')) {
      pendingReport = null
      await putFor($, report.run, l => ({ contextSent: [...l.contextSent, report.seq] }))
      await adapterLog($, 'context', `report gate at seq ${report.seq}`)
      return next({ ...e, context: [...(e.context ?? []), report.text] })
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'prompt.submit', next.error)
    return next(e)
  })

  on('turn.start', async ($, e, next) => {
    if ((e as unknown as Fields).agentId === undefined) {
      skillsLoading.clear()
      switchedIn.clear()
    }
    if (await recording($, (e as unknown as Fields).agentId)) {
      turnOpen = true
      await record($, 'turn', { phase: 'start' }, false)
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'turn.start', next.error)
    return next(e)
  })

  // Claude's text, one row per kept block, so ticks written between tool calls arrive (§9, P7). Recorded before
  // next(e): the row is kept either way.
  on('session.append', { door: 'response' }, async ($, e, next) => {
    if (await recording($, e.agentId)) {
      try {
        const text = replyText((e.message as unknown as Fields).content)
        if (text) await record($, 'reply', { text })
      } catch (err) {
        await recover($, 'session.append', err)
      }
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'session.append', next.error)
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const main = await recording($, e.agentId)
    if (main) {
      turnOpen = false
      await record($, 'turn', { phase: 'end' }, false)
    }
    const result = await next(e)
    // Only a turn Claude answered is reviewed: after Esc, a refusal or an error the next answered turn asks (BEH-26).
    // A nested run with every step reached returns first (BEH-30 (c)); the returned runs are asked before the open run.
    if (interactive === true && !disabled && e.agentId === undefined && e.reason === 'answer') {
      try {
        if (main) await turnEndUnwind($)
        await reviewReturned($)
        await review($)
      } catch (err) {
        await recover($, 'turn.complete', err)
      }
    }
    return result
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'turn.complete', next.error)
    return next(e)
  })

  // Confirming an exit (BEH-28, ERR-16; version 12): /clear, /exit and /resume typed while a run is unfinished ask
  // first, in Claude Code's own dialog. A confirmation, not a gate: it refuses nothing Claude does (ADR-006 D1 v2).
  on('command.run', async ($, e, next) => {
    const verb = CONFIRMED[e.command]
    if (verb === undefined || interactive !== true || disabled || !isPersonPrompt(e.origin)) return next(e)
    // The run as it stands: events still being written and not yet evaluated come first, as for the review.
    await settle($)
    const l = await hydrate($)
    const run = l.run
    const summary = l.summary
    const beneath = l.trail[l.trail.length - 1]
    let question: string
    let kept: string
    if (run !== null && beneath !== undefined) {
      // A paused run is unfinished: asked whatever the open run's state (version 14).
      question = nestedExitQuestion(run.skill, summary, beneath, l.trail.length - 1, verb)
      kept = nestedKeptText(run.skill, beneath)
    } else {
      if (run === null || summary === null || summary.ended !== null || summary.current === null) return next(e)
      question = exitQuestion(summary.skill, summary.current, summary.steps, verb)
      kept = keptText(summary.skill, summary.current)
    }
    if (!(await hasSurface($))) return next(e)
    let got: string
    try {
      got = await $.ui.ask(question, { options: [`${verb} anyway`, 'Keep working'], header: 'Progress' })
    } catch (err) {
      if (isDismissal(err)) {
        await adapterLog($, 'exit', `kept /${e.command}: dismissed`)
        return { text: kept }
      }
      // A dialog that can't be shown lets the command run: the confirmation fails open (ERR-16).
      await adapterLog($, 'exit', `ran /${e.command}: the dialog failed: ${firstLine(message(err))}`)
      return next(e)
    }
    if (got === `${verb} anyway`) {
      await adapterLog($, 'exit', `ran /${e.command}`)
      return next(e)
    }
    await adapterLog($, 'exit', `kept /${e.command}`)
    return { text: kept }
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'command.run', next.error)
    return next(e)
  })

  // A compaction of a run that follows the task list keeps its marked step in the summary and ends with a note asking
  // Claude to bring the list in step (BEH-24). Anything after next(e) is caught here, so the compaction stands.
  on('session.compact', async ($, e, next) => {
    const run = await get($, 'run')
    if (interactive === true && !disabled && run !== null && e.agentId === undefined && !(await follows($, run))) {
      return withTrailNote($, run, await next(e))
    }
    if (interactive !== true || disabled || run === null || e.agentId !== undefined) return next(e)
    const keep = await compactNotes($, run)
    const out = await next({ ...e, instructions: e.instructions ? `${e.instructions}\n\n${keep.instruction}` : keep.instruction })
    try {
      if (!('messages' in out) || !Array.isArray(out.messages)) return out
      await adapterLog($, 'compact', (keep.marked === null ? 'no step marked' : `step ${keep.marked} marked`)
        + (keep.reached ? ', every step reached: no note' : ''))
      // An earlier note, as a summary made ahead of time or a second compaction carries, goes: never two (version 8).
      const kept = out.messages.filter(m => !(typeof m.text === 'string' && m.text.startsWith(NOTE_START)))
      if (keep.reached) return withTrailNote($, run, kept.length ? { ...out, messages: kept } : out)
      return withTrailNote($, run, { ...out, messages: [...kept, { role: 'user' as const, text: keep.note, toolUses: [] }] })
    } catch (err) {
      await recover($, 'session.compact', err)
      return out
    }
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'session.compact', next.error)
    return next(e)
  })

  // All session.end hooks share 1.5 seconds: run-end first, the last evaluation only if there is room (BEH-05). With
  // paused runs, each one's run-end, bottom first, then the open run's, while the budget has room (version 14).
  on('session.end', async ($, e, next) => {
    if (await recording($, undefined)) {
      const reason = e.reason === 'clear' ? 'clear' : 'session-end'
      const all = await chained(async () => {
        const trail = (await hydrate($)).trail
        for (const p of trail) {
          if (!hasRoom(next.budget.remainingMs)) return false
          if (p.run !== null) await appendEvent($, p.run, 'run-end', { reason }, false)
        }
        if (trail.length && !hasRoom(next.budget.remainingMs)) return false
        await endOpenNow($, reason)
        return true
      })
      const run = await get($, 'run')
      if (all && run !== null) await finalEvaluation($, run, finalTimeout(next.budget.remainingMs))
    }
    pendingReport = null
    lastStatus = undefined
    turnOpen = false
    live = emptyLive()
    // A new session ID follows /clear, /resume and /branch: its lines wait for its first run (DM-02).
    logRoot = null
    return next(e)
  }).catch(async ($, e, next) => {
    return next(e)
  })

  // The band above the prompt (BEH-11): two rows of text, then what the mods after it draw.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const previous = bandChain
    let finish = () => {}
    bandChain = new Promise<void>(resolve => {
      finish = resolve
    })
    try {
      await previous
      const summary = await read($, SUMMARY)
      const props = e.props as unknown as { hasSurvey?: boolean; maxRows?: number; bodyColumns?: number }
      const rows = props.maxRows ?? 2
      if (interactive !== true || disabled || summary === null || (await read($, RUN)) === null || props.hasSurvey || rows < 1) {
        return next(e)
      }
      const band = bandRows(summary, await read($, MODE), await read($, TRAIL))
      const width = Math.max(10, props.bodyColumns ?? 80)
      const { Box, Text, Button } = await $.ui.resolve(e)
      const rest = await next(e)
      const left = `${band.mode}  `
      const right = fit(`  ${band.flag}`, Math.max(0, width - left.length - band.button.length - 4))
      return (
        <Box flexDirection="column">
          <Text>{fit(band.row1, width)}</Text>
          {rows >= 2 ? (
            <Box flexDirection="row">
              <Text>{left}</Text>
              <Button key="progress-mode" label={band.button} onPress={() => {
                void switchMode($)
              }} />
              <Text dimColor>{right}</Text>
            </Box>
          ) : null}
          {rest}
        </Box>
      )
    } finally {
      finish()
    }
  }).catch(async ($, e, next) => {
    return next(e)
  })
}
