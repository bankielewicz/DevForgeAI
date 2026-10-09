// DevForgeAI's progress tracker adapter for Claude Code (SPEC-013 v27).
//
// It records each run of a tracked skill as SPEC-012's event log, runs SPEC-012's evaluator on a timer, and shows
// the run in the status line, a two-row band above the prompt and toasts. In enforce mode it refuses the write
// gate's Write or Edit when that gate raised flags, refuses a question at SPEC-012's question gate (no step marked,
// no step tag, or another step's tag), and gives the model the report gate's flags. It records Claude Code's task list as step events.
// A tracked skill Claude loads mid-run pauses the open run on a trail, which unwinds when Claude goes back (BEH-29,
// BEH-30). A plugin skill whose SKILL.md metadata says devforgeai-tracked "false" is untracked: its load changes nothing
// and the turn it loads in records no tool events and no replies (BEH-02, versions 18 and 19). It fails open:
// when it can't run, the work goes on and the user is told (ADR-006 D1). Version 22: an answer event records the form Claude
// asked (BEH-37); a Bash command naming a document the run writes at its write gate is refused in enforce mode, and the
// documents a Bash call wrote are recorded after it (BEH-38); the line on continuing states the draft, the ask and the forms
// (BEH-39). Old run and session folders are pruned
// by progress/prune.py, which the adapter starts once per session and root (BEH-19). Versions 21 to 25: another mod's tool
// calls change nothing of the tracker (BEH-33); /progress prints the run (BEH-34); a row above the prompt warns that
// /devforgeai:precompact will run, and the adapter runs it once as if typed (BEH-35, BEH-36, BEH-41); a turn's tokens are a
// usage event (BEH-40) and a line of the session's odometer ledger (SPEC-016 BEH-10, ERR-06). Held with the dashboard, and not
// built here: the pane /progress will open (BEH-34), the tile that starts a skill (BEH-41's other setter, ERR-24) and
// BEH-01's /devforgeai:dashboard answer with tracking off. Version 27: a write of the tracker's that fails (the folder and its
// .gitignore, a run's events.jsonl, the odometer's file) is a hold, a retry and a remedy, not a stop: the run stays open, its lines
// stay in memory, the adapter tries again at the end of each main-loop turn and on `/progress retry`, and only after 10 failed turn
// tries, or at 4 MiB, does it stop as earlier versions did at once (BEH-42, ERR-03; SPEC-016 version 3 for the ledger).
//
// Every use of `$` stays in top-level functions of this file (claude plugin validate's rule); progress-core.ts
// holds the pure helpers.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'
import type { ProgressMode, ProgressModeSource, ProgressPaused, ProgressPrecompact, ProgressReturned, ProgressRun, ProgressSummary, ProgressWroteSeen } from '../types'
import {
  adherenceText, bandRows, byteSize, compactTexts, editResult, eventLine, exitOf, finalTimeout, fit, followsTaskList, hasTaskList,
  hintText, isAnswered, isEngine, isFailed, isPersonPrompt, isTracked, isUntrackedSkill, isWaiverQuestion, keptContent, markedStep, newFlagToasts,
  questionRefusal, questionTag, refusalCause, refusalText, replyText, reportContext, retentionOf, reviewItems, reviewQuestion,
  runId, runName, skillName, statusText, stepLabel, waiverAnswer, returnLine, pausedWith, keptTrail, endReason, hasRoom, trailNote, TRAIL_NOTE_START, stopsRun,
  exitQuestion, keptText, nestedExitQuestion, nestedKeptText, isDismissal, CONFIRMED, resumePlan, resumeQuestion, resumeLine,
  removeArgv, resumesOf, workFilePaths, workFilesDue, workFilesProblem, formOf, gatedOf, outsideWord, outsideRefusal, outsideMessage,
  folderOf, folderOfFile, changedFiles, signature, logNames, windowClosed, wroteText, withContext, ruleMatches, pathMatches,
  OUTSIDE_WRITE_TYPE, OUTSIDE_ADVICE, WROTE_CONTEXT_ROUTE, stepOfTask, stepStateOf, stuckAdvice, stuckText, summaryOf, taskIdOf, todoSteps, toolPath, FORMAT, IDLE_MS, LOG_LIMIT, NOTE_START, TASK_TAG,
  isFromMod, isOwnRun, fuelSetting, measuredShare, precompactRow, precompactDue, NO_PRECOMPACT, usageFields, ledgerLine, progressReport,
  addStart, takeStart, isCompaction,
  HOLD_TRIES, STOPPED_LINE, NOTHING_TO_RETRY, STOP_TOAST, errorLine, remedyRow, heldToast, recoveredToast, odometerGaveUpToast, heldLog,
  recoveredLog, gaveUpLog, savedAnswer, stillAnswer, liftedAnswer, stillStoppedAnswer, odometerOnAnswer, odometerStillAnswer,
} from './progress-core'
import type { Fields, Gated, HoldKind, HoldView, Listed, ProgressState, Refused, ReviewItem, ToolOutcome } from './progress-core'

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
const CLEANED = atom({ plugin: 'devforgeai', key: 'cleaned' } as const, [] as string[])
const WROTE_SEEN = atom({ plugin: 'devforgeai', key: 'wroteSeen' } as const, {} as ProgressWroteSeen)
const CLOSED = atom({ plugin: 'devforgeai', key: 'closedFor' } as const, null as string | null)
// The precompact row's values and BEH-36's run mark (versions 21, 23 and 25). They belong to the session, not to a run, so they
// are not part of the open run's Live values: the host empties them at /clear, /resume and /branch.
const PRECOMPACT = atom({ plugin: 'devforgeai', key: 'precompact' } as const, NO_PRECOMPACT as ProgressPrecompact)

// The open run's values, as the module holds them (version 14): every hook reads and writes these, never a $.state
// snapshot, since each dispatch's $.state reads one moment of its own (a hook that awaits across another's write would
// act on the old run). $.state keeps a mirror, written in order with the latest values, for a reload and the band.
type Live = {
  run: ProgressRun | null; summary: ProgressSummary | null; lastEventAt: number; marked: boolean; shown: string[]
  contextSent: number[]; tasks: Record<string, number>; todos: Record<string, string>; adhered: string | null
  refusals: Record<string, number>; refused: Refused[]; reviewed: string | null; trail: ProgressPaused[]
  returned: ProgressReturned[]
  /** The runs whose work files' cleanup was started (BEH-32), newest last, the last 50. */
  cleaned: string[]
  /** For each run, the documents a Bash call wrote that were recorded, by path: their size and mtimeMs as listed (BEH-38 (b);
   *  version 22), so an unchanged recorded file isn't recorded twice. The last 20 runs. */
  wroteSeen: ProgressWroteSeen
  /** The run whose last evaluation closed BEH-38's window (every step reached, ended, or its validator's step done), or null. */
  closedFor: string | null
}
let live: Live | null = null
let mirrorChain: Promise<unknown> = Promise.resolve()

function emptyLive(): Live {
  return { run: null, summary: null, lastEventAt: 0, marked: false, shown: [], contextSent: [], tasks: {}, todos: {},
    adhered: null, refusals: {}, refused: [], reviewed: null, trail: [], returned: [], cleaned: [], wroteSeen: {}, closedFor: null }
}

/** The module's values, read once from $.state after a load or a reload (BEH-17). */
async function hydrate($: E): Promise<Live> {
  if (live !== null) return live
  const run = await read($, RUN)
  const got: Live = {
    run, summary: await read($, SUMMARY), lastEventAt: await read($, LAST),
    marked: await read($, MARKED), shown: await read($, SHOWN), contextSent: await read($, SENT),
    tasks: await read($, TASKS), todos: await read($, TODOS), adhered: await read($, ADHERED),
    refusals: await read($, REFUSALS), refused: await read($, REFUSED), reviewed: await read($, REVIEWED),
    // An entry without its run, version 13's shape, is dropped (BEH-30); the mirror catches up at the next change.
    // A reload between the mirror's writes of a push can leave the open run on the trail too: it is dropped.
    trail: keptTrail(await read($, TRAIL)).filter(t => t.run!.id !== run?.id), returned: await read($, RETURNED),
    cleaned: await read($, CLEANED), wroteSeen: await read($, WROTE_SEEN), closedFor: await read($, CLOSED),
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
    case 'cleaned': await $.state.set({ plugin: 'devforgeai', key: 'cleaned' } as const, l.cleaned); break
    case 'wroteSeen': await $.state.set({ plugin: 'devforgeai', key: 'wroteSeen' } as const, l.wroteSeen); break
    case 'closedFor': await $.state.set({ plugin: 'devforgeai', key: 'closedFor' } as const, l.closedFor); break
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
/** The skills another plugin's mod is loading with a Skill tool call in flight, by name (BEH-33, Bryan 2026-10-08, "Leave the run
 *  open"): a skill.prompt for one of these, with no Claude's call and no typed command running the same name, is the mod's load
 *  and changes nothing of the tracker. */
const modLoading = new Map<string, number>()
/** Skills whose load inside a Skill call changed the open run (a push, an unwind, a switch): that call records nothing
 *  when it returns, in either run (BEH-29). */
const switchedIn = new Set<string>()
/** Bumped at each change of the open run (open, push, unwind): a hook that began under an older value began before
 *  the open run opened (BEH-30 (a), version 14). */
let tenure = 0
/** The skill name the person's command.run is running, until its next(e) settles: a typed skill's skill.prompt fires
 *  inside it (BEH-31, version 16; probe 2026-10-05). */
let typedName: string | null = null
/** The open run has recorded the event of a tool call or an answer whose hook began after it opened (BEH-30 (a)). */
let worked = false
/** The turn is marked (BEH-02, version 18): an untracked skill was loaded in it, by the person (the typed name), by Claude's
 *  Skill call (the in-flight set) or, from version 26, as the plugin's own precompact skill while BEH-36's pending mark is set.
 *  Set at that skill.prompt; turn.start doesn't clear it, since a typed load's skill.prompt comes before its turn starts. From
 *  version 26 it is bound to a turn (markBind) and ends by the turn-ID rule (markEndsAt). A tool call whose hook began while
 *  it was set records no tool event, and a reply arriving while it is set isn't recorded (version 19). */
let untrackedTurn = false
/** What the mark is bound to (BEH-02, version 26): a turn (its ID, and the IDs of the main-loop turns started since); 'next',
 *  a load bound to the next main-loop turn.start; or 'any', when no turn ID can be bound, so the next turn.complete ends it. */
type MarkBind = { kind: 'turn'; id: string; since: string[] } | { kind: 'next' } | { kind: 'any' }
let markBind: MarkBind | null = null
/** Whether the mark was set at a load of the plugin's own precompact skill, which is when its end is written to adapter.log. */
let markIsPrecompact = false
/** The main loop's current turn: the turnId of its latest turn.start, or null when none is known (version 26). */
let currentTurn: string | null = null
/** Where the kept name came from: the person's own command, or BEH-41's set (the adapter's own $.command.run). The load line says. */
let typedSource: 'person' | 'set' | null = null
let disabled = false
let modeSession: string | null = null
// The root the mode was resolved for: the local preference file is per checkout (BEH-16).
let modeRoot: string | null = null
let pluginSkills: string[] | null = null
let lastStatus: string | undefined
let pendingReport: { seq: number; text: string; run: string } | null = null
/** BEH-38 (b)'s enforce-mode texts waiting for the user's next prompt: the fallback of the P14 switch (WROTE_CONTEXT_ROUTE),
 *  and the route for a call whose answer is a deny. A separate slot from the report's, so neither clobbers the other. */
let pendingWrote: { run: string; text: string }[] = []
/** A run's manifests' gated rules, read once at its first Bash call (BEH-38), by run ID; the last 20. */
const gatedCache = new Map<string, Gated>()
// The open run's event lines: in the module and events.jsonl, since a $.state value holds at most 4,194,304
// characters (see types/index.d.ts); read back from the file after a reload.
// `written` is the number of those lines the file is known to hold: the rest run ahead of it while a hold lasts (version 27).
let held: { id: string; lines: string[]; written: number } | null = null
/** A hold (BEH-42, version 27): a write of the tracker's that failed, kept in the module's memory and not in $.state, since a reload
 *  loses the lines it keeps and a count that outlived them would describe nothing. `path` and `error` are the latest failed write's. */
type Hold = { path: string; error: string; firstAt: number; tries: number }
/** The open run's log: `held`'s lines run ahead of its events.jsonl (the folder and its .gitignore included). */
let runHold: Hold | null = null
/** The session's odometer file: `ledgerHeld` runs ahead of it. */
let odoHold: Hold | null = null
/** The ledger stopped at the tenth failed turn try (SPEC-016 ERR-06): `/progress retry` lifts it. */
let odoGaveUp = false
/** A new run's pruning waits for the write that creates its folder (BEH-19, version 27). */
let pendingPrune: { r: string; session: string; keepRun: string; continued: string | null } | null = null
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

// Versions 21 to 25. The fuel settings (DM-07, DM-08) are read when the module loads, as retentionDays is, and the notes of a
// setting that was out of range wait here for session.start, which has the `$` that register lacks.
let warnFuel = 30
let runFuel = 20
let settingNotes: string[] = []
/** Whether this session's latest registration of /progress succeeded (BEH-34, ERR-21). */
let progressOk = false
/** BEH-36's run mark in memory (BEH-36, BEH-35): $.state's precompact.ran is the copy a reload reads. The check and the set
 *  happen with no await between them, so two overlapping measurements start one run. */
let autoRun = false
/** BEH-41's set of pending command names (version 25), in the adapter's own memory and not in $.state: BEH-36's run adds
 *  precompact before its $.command.run, and a tile's Start (held with the dashboard) will add its skill's name. The plugin's own
 *  command.run hook takes a name when it sees that run; a failure takes its own name only; a reload, /clear, /resume, /branch
 *  and the session's end empty the set (not a turn's end: the run starts once the session is idle, after the turn). */
const starts = new Set<string>()

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
 *  to its last half when it passes 512 KiB, and a failed write is ignored. From version 27 no write is tried while a hold lasts or
 *  after the tracker has stopped (BEH-42): the lines wait in memory, the first 200, and the first write after the hold clears or the
 *  stop is lifted writes them ahead of its own line. */
async function adapterLog($: E, kind: string, text: string, runId?: string): Promise<void> {
  const step = logChain.then(async () => {
    const run = await get($, 'run')
    const now = new Date(await $.clock.now()).toISOString().replace(/\.\d{3}Z$/, 'Z')
    // One line per entry, whatever the text: model text can't add lines of its own (DM-02).
    const line = `${now} ${runId ?? run?.id ?? '-'} ${kind}: ${text.replace(/\s*[\r\n]+\s*/g, ' ')}\n`
    const root = logRoot
    if (root === null || runHold !== null || odoHold !== null || disabled) {
      // The first lines are kept (the early notices are the ones that matter); past 200, newer ones are dropped.
      if (early.length < 200) early = [...early, line]
      return
    }
    const lead = early.join('')
    early = []
    await appendLog($, root, lead + line)
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
  const text = statusText(l.summary, mode, idle, off, l.trail, holdKind())
  if (text === lastStatus) return
  lastStatus = text
  await $.ui.status(text)
  if (text !== undefined && !(await hasSurface($))) await $.ui.log(text)
}

/** Tracking can't go on for the session (ERR-03): a hold gave up, after 10 failed turn tries or at 4 MiB (BEH-42 (f)). The run and
 *  its held lines are dropped, the trail empties and its runs get no run-end (BEH-05, version 14), and the odometer's writes stop
 *  with it (SPEC-016 BEH-10); `/progress retry` is the way back (BEH-34). */
async function stopTracking($: E, reason: string): Promise<void> {
  disabled = true
  const had = (await hydrate($)).trail.length
  held = null
  runHold = null
  odoHold = null
  pendingPrune = null
  const dropped = ledgerHeld.length
  ledgerHeld = []
  await putMany($, () => ({ run: null, trail: [], returned: [] }))
  if (had) await adapterLog($, 'trail', `empty (tracking stopped: ${reason})`)
  if (dropped > 0) await adapterLog($, 'dashboard', `odometer: dropped ${dropped} lines: the tracker stopped`)
  await update($, OFF, () => reason)
  await notify($, STOP_TOAST)
  await refreshStatus($)
  redraw($)
}

/** The holds live in the module's memory and no $.state value changes with them, so nothing else would draw a change of them: a
 *  hold's start and clear, and the stop and its lift, redraw the band and its rows (BEH-42 (c)). */
function redraw($: E): void {
  try {
    $.ui.invalidate('ui.render')
  } catch {
    // nothing to redraw
  }
}

/** Which hold the status line, the row and /progress show: the run's wins when both exist (BEH-10, BEH-11). */
function holdKind(): HoldKind | null {
  return runHold !== null ? 'run' : odoHold !== null ? 'odometer' : null
}

/** The lines of the open run's log that the file lacks. */
function heldLacks(): number {
  return held === null ? 0 : Math.max(0, held.lines.length - held.written)
}

/** What the row, the toast and /progress say of the hold shown, or null. */
function holdView(): HoldView | null {
  if (runHold !== null) return { kind: 'run', lines: heldLacks(), path: runHold.path, error: runHold.error }
  if (odoHold !== null) return { kind: 'odometer', lines: ledgerHeld.length, path: odoHold.path, error: odoHold.error }
  return null
}

/** A write that failed: where, and the host's error. */
type Failed = { path: string; err: unknown }

/** A write of the tracker's has failed (BEH-42 (a), (c)): the hold starts, with one adapter.log line, one toast and a redraw; a hold
 *  that already lasts only takes the latest failed write's path and error. `lacks` is the number of lines the file lacks. */
async function holdStarts($: E, which: 'run' | 'odometer', path: string, err: unknown, lacks: number): Promise<void> {
  const error = errorLine(message(err))
  const at = await $.clock.now()
  const known = which === 'run' ? runHold : odoHold
  if (known !== null) {
    known.path = path
    known.error = error
    return
  }
  const hold: Hold = { path, error, firstAt: at, tries: 0 }
  if (which === 'run') runHold = hold
  else odoHold = hold
  // The kind is a literal at each call (VER-66's structure test reads it)
  if (which === 'run') await adapterLog($, 'write', heldLog(lacks, path, error))
  else await adapterLog($, 'dashboard', `odometer: ${heldLog(lacks, path, error)}`)
  await notify($, heldToast({ kind: which, lines: lacks, path, error }, progressOk))
  await refreshStatus($)
  redraw($)
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
  // The lines keep waiting while a hold lasts or the tracker has stopped (BEH-42).
  if (runHold !== null || odoHold !== null || disabled) return
  const waiting = early.join('')
  early = []
  if (waiting) {
    const step = logChain.then(() => appendLog($, r, waiting)).catch(() => undefined)
    logChain = step
    await step
  }
}

/** The .gitignore that keeps devforgeai/progress/ out of git, written again if it was deleted (BEH-15). `force` writes it whether or
 *  not it exists: the probe of BEH-34 after a stop, since a probe that skipped an existing file would claim a recovery it never
 *  tested. The failed write, or null. */
async function ensureIgnore($: E, r: string, force = false): Promise<Failed | null> {
  const file = `${progressDir(r)}/.gitignore`
  try {
    if (force || !(await $.fs.exists(file))) await $.fs.write(file, '*\n')
    return null
  } catch (err) {
    return { path: file, err }
  }
}

/** devforgeai/progress/ and its .gitignore in a run's root, before anything else is written there (BEH-15); the failed write, or
 *  null. A failure holds (BEH-42), it no longer stops tracking; no root is known to adapter.log or the ledger until it works. */
async function ensureDir($: E, r: string): Promise<Failed | null> {
  const failed = await ensureIgnore($, r)
  if (failed === null) await useLogRoot($, r)
  return failed
}

/** The open run's lines, read back from events.jsonl when the module was reloaded (BEH-17). A failed read
 *  throws, and nothing is cached: writing a fresh log over the real one would lose the run's events. */
async function linesOf($: E, run: ProgressRun): Promise<string[]> {
  if (held !== null && held.id === run.id) return held.lines
  const lines = (await $.fs.read(`${run.dir}/events.jsonl`)).split('\n').filter(Boolean)
  held = { id: run.id, lines, written: lines.length }
  return lines
}

/** One write of a run's whole log (no append in $.fs): the failed write, or null. */
async function putLog($: E, run: ProgressRun, text: string): Promise<Failed | null> {
  const path = `${run.dir}/events.jsonl`
  try {
    await $.fs.write(path, text)
    return null
  } catch (err) {
    return { path, err }
  }
}

/** Write the run's whole log (no append in $.fs); false when it can't be recorded: it would pass 4 MiB (ERR-11, or the end of a hold,
 *  BEH-42 (f)), or `open` is false and the write failed. `open` is false for a run that isn't the open one (a paused run's run-end):
 *  its lines aren't cached, and its full log stops nothing.
 *  Version 27 (BEH-42): the lines of the open run are the module's before the file has them. While a hold lasts, an event only
 *  advances them and writes nothing; a write that fails starts the hold and still counts as recorded; a paused run's failed write is
 *  dropped with one line and starts no hold. */
async function writeLog($: E, run: ProgressRun, lines: string[], open = true): Promise<boolean> {
  const text = lines.join('\n') + '\n'
  const big = byteSize(text) > LOG_LIMIT
  const known = held !== null && held.id === run.id ? held.written : null
  if (open && runHold !== null) {
    // No write for each event; the file the next try writes is whole (DM-02). The bound ends the hold, and 'event log full' isn't shown.
    if (big) {
      await giveUp($, 'bytes')
      return false
    }
    held = { id: run.id, lines, written: known ?? 0 }
    return true
  }
  if (big) {
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
  const failed = await putLog($, run, text)
  if (failed === null) {
    if (open) held = { id: run.id, lines, written: lines.length }
    else if (held !== null && held.id === run.id) held = null
    return true
  }
  if (!open) {
    await adapterLog($, 'write', `dropped 1 lines of ${run.id}: ${failed.path}: ${errorLine(message(failed.err))}`)
    return false
  }
  held = { id: run.id, lines, written: known ?? lines.length - 1 }
  await holdStarts($, 'run', failed.path, failed.err, lines.length - held.written)
  return true
}

/** A hold gave up (BEH-42 (f)): 10 failed turn tries, or the held log would pass 4 MiB. Tracking stops as ERR-03 did at the first
 *  failure before version 27. */
async function giveUp($: E, why: 'tries' | 'bytes'): Promise<void> {
  const hold = runHold
  if (hold === null) return
  const lost = heldLacks()
  await adapterLog($, 'write', why === 'tries' ? gaveUpLog(hold.tries, hold.path, hold.error, lost) : `gave up at 4 MiB: ${hold.path}; dropped ${lost} lines`)
  await stopTracking($, NO_WRITE)
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
  pendingWrote = []
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

/** A paused run's run-end, written while it isn't the open run; a log that can't be read gets none, and the switch,
 *  unwind or session end goes on (BEH-05, ERR-03). The run as it ended, or null. */
async function endPausedNow($: E, run: ProgressRun, reason: string): Promise<ProgressRun | null> {
  try {
    return (await appendEvent($, run, 'run-end', { reason }, false))?.run ?? null
  } catch (err) {
    await adapterLog($, 'error', `run-end of ${run.id}: ${firstLine(message(err))}`)
    return null
  }
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

// ---- the retry of a hold (BEH-42 (b), (e), (h)) ----

/** What a try came to, for /progress retry's answer. */
type Tried = { kind: HoldKind; ok: boolean; saved: number; path: string; error: string; lines: number; tries: number }

/** The hold of the run's log has cleared: the lines it kept are in the file (BEH-42 (e)). The run is marked, so the timer's next
 *  evaluation, the first since the hold and over the whole file, runs once (BEH-06); a new run's pruning, which waited for its
 *  folder, starts (BEH-19). */
async function runRecovered($: E, run: ProgressRun, wrote: number): Promise<void> {
  const hold = runHold
  if (hold === null) return
  runHold = null
  await useLogRoot($, rootOf(run))
  await adapterLog($, 'write', recoveredLog(hold.tries, `${run.dir}/events.jsonl`, wrote))
  await putFor($, run.id, () => ({ marked: true }))
  await notify($, recoveredToast(wrote))
  const prune = pendingPrune
  pendingPrune = null
  if (prune !== null && prune.keepRun === run.id) await startPrune($, prune.r, prune.session, prune.keepRun, prune.continued)
  await refreshStatus($)
  redraw($)
}

/** One try at the run's hold: the folder and its .gitignore if missing (BEH-15), then the whole log. `how` is 'turn' at a main-loop
 *  turn's end (a failure adds 1 to the count, and the tenth gives up), 'command' for /progress retry (it adds nothing), and 'leave'
 *  when the open run leaves memory (BEH-42 (h)): a failure then drops the run's unwritten lines with one line, and the hold goes on. */
async function tryRun($: E, how: 'turn' | 'command' | 'leave'): Promise<Tried | null> {
  const hold = runHold
  if (hold === null) return null
  const run = (await hydrate($)).run
  if (run === null) {
    // The run is gone (a stale hold): nothing is left to write.
    runHold = null
    await refreshStatus($)
    redraw($)
    return null
  }
  const lines = await linesOf($, run)
  const lacks = held !== null && held.id === run.id ? Math.max(0, held.lines.length - held.written) : 0
  const failed = (await ensureIgnore($, rootOf(run))) ?? (await putLog($, run, lines.join('\n') + '\n'))
  if (failed === null) {
    held = { id: run.id, lines, written: lines.length }
    await runRecovered($, run, lacks)
    return { kind: 'run', ok: true, saved: lacks, path: `${run.dir}/events.jsonl`, error: '', lines: 0, tries: hold.tries }
  }
  const error = errorLine(message(failed.err))
  hold.path = failed.path
  hold.error = error
  if (how === 'leave') {
    // The run's unwritten lines are written off: they stay in the cache, so that the run's run-end is still seen as written when a
    // second chain item ends the same run (finishSwitch), and nothing will write them; the next run's lines replace the cache.
    held = { id: run.id, lines, written: lines.length }
    await adapterLog($, 'write', `dropped ${lacks} lines of ${run.id}: ${failed.path}: ${error}`)
    return null
  }
  if (how === 'turn') hold.tries += 1
  const tried: Tried = { kind: 'run', ok: false, saved: 0, path: failed.path, error, lines: lacks, tries: hold.tries }
  if (how === 'turn' && hold.tries >= HOLD_TRIES) await giveUp($, 'tries')
  return tried
}

/** One try at the odometer's hold: the whole file, with the lines it holds and the lines held (SPEC-016 ERR-06). It runs in the
 *  ledger's own chain, so it never races a line being added. */
function tryOdometer($: E, how: 'turn' | 'command'): Promise<Tried | null> {
  return ledgerRun<Tried | null>(async () => {
    const hold = odoHold
    const file = ledgerFile
    if (hold === null) return null
    if (file === null) {
      odoHold = null
      await refreshStatus($)
      redraw($)
      return null
    }
    const count = ledgerHeld.length
    const lines = [...file.lines, ...ledgerHeld]
    const path = file.path
    try {
      await $.fs.write(path, lines.join('\n') + '\n')
    } catch (err) {
      const error = errorLine(message(err))
      hold.path = path
      hold.error = error
      if (how === 'turn') hold.tries += 1
      const tried: Tried = { kind: 'odometer', ok: false, saved: 0, path, error, lines: count, tries: hold.tries }
      if (how === 'turn' && hold.tries >= HOLD_TRIES) await odometerGivesUp($, hold, path, error)
      return tried
    }
    file.lines = lines
    ledgerHeld = ledgerHeld.slice(count)
    odoHold = null
    await adapterLog($, 'dashboard', `odometer: ${recoveredLog(hold.tries, path, count)}`)
    await notify($, recoveredToast(count))
    await refreshStatus($)
    redraw($)
    return { kind: 'odometer', ok: true, saved: count, path, error: '', lines: 0, tries: hold.tries }
  })
}

/** The odometer's hold gave up (SPEC-016 ERR-06): its held lines are dropped, nothing is written for the session until
 *  `/progress retry` lifts the stop, and the tracker goes on untouched. */
async function odometerGivesUp($: E, hold: Hold, path: string, error: string): Promise<void> {
  const dropped = ledgerHeld.length
  ledgerHeld = []
  odoHold = null
  odoGaveUp = true
  await adapterLog($, 'dashboard', `odometer: ${gaveUpLog(hold.tries, path, error, dropped)}`)
  await notify($, odometerGaveUpToast(path))
  await refreshStatus($)
  redraw($)
}

/** Try the holds once, in the record chain, so a try never races an event being recorded (BEH-42 (b)): the run's log first, then the
 *  odometer's file. `only` limits it to the holds that existed before this turn's own writes (a hold that starts in the turn's end is
 *  not tried in it). */
function retryHolds($: E, how: 'turn' | 'command', only?: { run: Hold | null; odo: Hold | null }): Promise<Tried[]> {
  return chained(async () => {
    const out: Tried[] = []
    if (runHold !== null && (only === undefined || only.run === runHold)) {
      const tried = await tryRun($, how)
      if (tried !== null) out.push(tried)
    }
    if (odoHold !== null && (only === undefined || only.odo === odoHold)) {
      const tried = await tryOdometer($, how)
      if (tried !== null) out.push(tried)
    }
    return out
  })
}

/** The run as it stands: events still being written, the evaluation in flight, then one evaluation of a marked run
 *  (BEH-26, BEH-28, BEH-30 (c)). */
async function settle($: E): Promise<void> {
  await recordChain
  if (inFlight !== null) await inFlight
  // No evaluation starts while the run's log is held: the file is behind the lines (BEH-42 (d)).
  if (!evaluating && !disabled && runHold === null && (await get($, 'marked'))) {
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

/** What a skill's load is (BEH-02): 'tracked' (one of the plugin's own, or a project or organization manifest's), 'untracked'
 *  (one of the plugin's own whose SKILL.md metadata has devforgeai-tracked "false", version 18) or 'other', which neither
 *  starts nor ends a run. A plugin skill's SKILL.md is read at each of its loads, never cached, so a deployed change shows
 *  at the next load; only a plugin skill can be untracked, and a manifest of its name changes nothing. A SKILL.md that can't
 *  be read leaves the skill tracked, with one adapter.log line (ERR-18). */
async function skillKind($: E, r: string, name: string): Promise<'tracked' | 'untracked' | 'other'> {
  if (pluginSkills === null) {
    try {
      pluginSkills = (await $.fs.list(`${$.plugin.root}/skills`)).filter(x => x.kind === 'dir').map(x => x.name)
    } catch {
      pluginSkills = []
    }
  }
  if (pluginSkills.includes(name)) {
    try {
      return isUntrackedSkill(await $.fs.read(`${$.plugin.root}/skills/${name}/SKILL.md`)) ? 'untracked' : 'tracked'
    } catch (err) {
      await adapterLog($, 'skill-read', `${name}: ${firstLine(message(err))}`)
      return 'tracked'
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
  return isTracked(name, pluginSkills, manifests) ? 'tracked' : 'other'
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
async function absorb($: E, run: ProgressRun, got: { state: ProgressState; text: string }, cleanup = false): Promise<void> {
  // One at a time: the run-end evaluation and a timer's can finish together, and each reads the shown flags and
  // adhered before it writes them, so a notice could otherwise show twice.
  const step = absorbChain.then(() => absorbNow($, run, got, cleanup))
  absorbChain = step.catch(() => undefined)
  await step
}

async function absorbNow($: E, run: ProgressRun, got: { state: ProgressState; text: string }, cleanup: boolean): Promise<void> {
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
  // BEH-38's window, from the last evaluated state (version 22): closed once every step is reached, the run has ended, or a
  // step with a script rule of target written is done; open again if a later evaluation says otherwise.
  const closed = windowClosed(got.state, (await gatedFor($, run)).scriptSteps)
  await putFor($, run.id, l => (closed === (l.closedFor === run.id) ? {} : { closedFor: closed ? run.id : null }))
  if (cleanup) await startCleanup($, run, got.state)
  await refreshStatus($)
}

/** The timer's work (BEH-06): it catches every error itself, since one it let escape reaches only the debug log (ERR-10). */
async function tick($: E): Promise<void> {
  try {
    await refreshStatus($)
    // While the run's log is held the timer starts no evaluation and clears no mark (BEH-06, BEH-42 (d)).
    if (evaluating || disabled || runHold !== null || !(await get($, 'marked'))) return
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
      await ensureIgnore($, rootOf(run))
      const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, EVALUATOR_TIMEOUT)
      const open = await get($, 'run')
      // A run that opened, paused or resumed while the evaluator ran keeps its own summary and flags (the module's values).
      if (open === null || open.id !== run.id) return
      if (typeof got === 'string') await failOpen($, got)
      else await absorb($, run, got, true)
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
  // A reload ends the holds and loses the lines they kept (BEH-42 (i)): the module's memory starts over, as it does in Claude Code
  // (a first session.start finds it empty already; the kit cannot reload the module, so its second session.start stands for one).
  const hadHold = runHold !== null || odoHold !== null
  if (odoHold !== null) {
    ledgerHeld = []
    ledgerFile = null
  }
  held = null
  runHold = null
  odoHold = null
  odoGaveUp = false
  pendingPrune = null
  const run = await get($, 'run')
  if (run !== null) {
    // A run opened in memory whose first write never worked has no events.jsonl: nothing is left to go on from (BEH-42 (i)).
    let missing = false
    try {
      missing = !(await $.fs.exists(`${run.dir}/events.jsonl`))
    } catch {
      missing = false  // a read that fails for another reason is BEH-17's
    }
    if (missing) {
      await putMany($, () => ({ run: null }))
      await adapterLog($, 'write', 'dropped the run: no events.jsonl after a reload', run.id)
      await refreshStatus($)
    } else {
      // After a reload the module's variables start over; the open run's folder exists, so its log goes there.
      await useLogRoot($, rootOf(run))
      await put($, 'marked', () => true)
    }
  }
  if (hadHold) redraw($)
}

/** A new run whose skill-loaded line is written but which isn't open yet (BEH-03, BEH-29). From version 27 `failure` names the write
 *  that failed: the run then opens in memory with its line held (BEH-42 (a)). */
type Opening = { run: ProgressRun; line: string; now: number; session: string; r: string; listed: boolean; taskList: boolean; checklist: string
  failure: Failed | null }

/** Write a new run's skill-loaded line in its own folder, in the root read as it loaded (BEH-03). A write that fails (the folder, its
 *  .gitignore or the line) is the Opening's `failure`, not a stop: the run opens in memory, and the caller's `afterOpen` starts the
 *  hold. Opening it is the caller's change, made with no await (version 14). */
async function prepareRun($: E, r: string, skill: string, checklist: string, extra: Fields = {}): Promise<Opening> {
  const dirFailed = await ensureDir($, r)
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
    mode: await read($, MODE), modeSource: await read($, SOURCE), ...extra,
  })
  const run: ProgressRun = { id, skill, seq: 1, dir, root: r }
  // A folder without its .gitignore is written nothing under (BEH-15).
  const failure = dirFailed ?? (await putLog($, run, line + '\n'))
  return { run, line, now, session, r, listed, taskList, checklist, failure }
}

/** A new run's values: the open one, with empty values (BEH-20: a list left from an earlier run gives no step events;
 *  BEH-25, BEH-26: the stuck notice and the review count per run). */
function opened(o: Opening): Partial<Live> {
  return { run: o.run, lastEventAt: o.now, marked: true, summary: null, shown: [], contextSent: [], tasks: {}, todos: {},
    refusals: {}, refused: [] }
}

/** After a new run is open: its lines, the hold a failed first write starts or a working one lifts, the off reason a full log left,
 *  the task-tools hint, pruning (which waits for the write that creates the folder, BEH-19). */
async function afterOpen($: E, o: Opening): Promise<void> {
  held = { id: o.run.id, lines: [o.line], written: o.failure === null ? 1 : 0 }
  if (o.failure !== null) {
    pendingPrune = { r: o.r, session: o.session, keepRun: o.run.id, continued: resumesOf(o.line) }
    await holdStarts($, 'run', o.failure.path, o.failure.err, 1)
  } else {
    pendingPrune = null
    // The new run's first write worked while a hold lasted: the hold is lifted (BEH-42 (h)).
    if (runHold !== null) await runRecovered($, o.run, 1)
  }
  if ((await read($, OFF)) === LOG_FULL) await update($, OFF, () => null)
  // A skill that follows the convention, in a session with no task tools, is placed by guessing: say so once (BEH-23).
  if (o.listed && !o.taskList && o.checklist.includes(TASK_TAG) && !(await read($, HINTED))) {
    const hint = hintText(o.run.skill)
    await update($, HINTED, () => true)
    await notify($, hint)
    await adapterLog($, 'tools-hint', hint)
  }
  if (o.failure === null) await startPrune($, o.r, o.session, o.run.id, resumesOf(o.line))
}

/** The run-end of the open run, inside a chain item (BEH-05); the run as it ended, or null with no open run. `leaving` is false for a
 *  run that stays the open one after its run-end (the deliberate stop, BEH-27); otherwise, while its log is held, the run-end joins
 *  the held lines and the run gets one write of its whole log (BEH-42 (h)). */
async function endOpenNow($: E, reason: string, leaving = true): Promise<ProgressRun | null> {
  const run = await get($, 'run')
  if (run === null) return null
  const into = await recordNow($, 'run-end', { reason }, true)
  pendingReport = null
  if (leaving && into !== null && runHold !== null) await tryRun($, 'leave')
  return (await get($, 'run')) ?? run
}

/** A load that doesn't nest (BEH-03, BEH-29): the open run ends with another-skill (a load that isn't Claude's ends every
 *  paused run too, bottom first, and empties the trail), is evaluated once more, and the new run opens. Two chain items
 *  with the evaluation between them, so no item holds an evaluation. */
async function switchRun($: E, r: string, name: string, checklist: string, endPaused: boolean, extra: Fields = {}): Promise<void> {
  const ended = await chained(async () => {
    const l = await hydrate($)
    if (endPaused && l.trail.length) {
      for (const p of l.trail) if (p.run !== null) await endPausedNow($, p.run, 'another-skill')
      await putMany($, () => ({ trail: [] }))
      await adapterLog($, 'trail', 'empty (a load with no Skill call of the main loop in flight)')
    }
    return endOpenNow($, 'another-skill')
  })
  await finishSwitch($, r, name, checklist, ended, endPaused, extra)
}

/** The rest of a switch: the ended run's last evaluation, then the new run, as one chain item. */
async function finishSwitch($: E, r: string, name: string, checklist: string, ended: ProgressRun | null, emptyTrail: boolean,
  extra: Fields = {}): Promise<void> {
  if (ended !== null) await finalEvaluation($, ended, EVALUATOR_TIMEOUT, true)
  await chained(async () => {
    await endOpenNow($, 'another-skill')  // a run an unwind resumed meanwhile ends too; the ended one is skipped
    const o = await prepareRun($, r, name, checklist, extra)
    await putMany($, () => {
      onSwitch()
      return { ...opened(o), ...(emptyTrail ? { trail: [] } : {}) }
    })
    await afterOpen($, o)
  })
}

/** Prune old run and session folders once per session ID and root, after the run's folder exists; nothing waits
 *  for it, and its result or failure goes to adapter.log only (BEH-19, ERR-12). */
async function startPrune($: E, r: string, session: string, keepRun: string, continued: string | null = null): Promise<void> {
  if (!python) return
  const key = `${session}\n${r}`
  if (pruned.has(key)) return
  pruned.add(key)
  const argv = [python, `${$.plugin.root}/progress/prune.py`, 'prune', '--root', r, '--days', String(retentionDays),
    '--keep-session', session, '--keep-run', keepRun, ...(continued === null ? [] : ['--keep-run', continued]),
    '--manifests', `${$.plugin.root}/progress/manifests`]
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

/** The work files' cleanup (BEH-32, IF-05; version 20): when an evaluation the timer started, or the final evaluation of a
 *  run that has just ended, says the open run's work files are due, run prune.py's remove once for the run's files and the
 *  continued run's. Nothing waits for it, nothing is shown, no event is recorded, and its failure is a log line (ERR-19). */
async function startCleanup($: E, run: ProgressRun, state: ProgressState): Promise<void> {
  try {
    if (!python || !workFilesDue(state) || (await get($, 'cleaned')).includes(run.id)) return
    // Recorded before anything awaits, in the module and in $.state: a second evaluation or a reload starts none; and only
    // while the run is the open one, so a paused run's files wait for the age pass.
    const mine = await putFor($, run.id, l => ({ cleaned: [...l.cleaned, run.id].slice(-50) }))
    if (!mine) return
    const own = workFilePaths(state)
    const continued = await continuedFiles($, run)
    if (own.length + continued.length === 0) return
    const argv = removeArgv(python, $.plugin.root, rootOf(run), own, continued)
    const finish = (text: string): Promise<void> => adapterLog($, 'workfiles', text, run.id)
    try {
      void $.process.run(argv, { cwd: rootOf(run), timeoutMs: PRUNE_TIMEOUT }).then(
        res => finish(res.exitCode === 0 ? firstLine(res.stdout) : firstLine(res.stderr) || `exit ${res.exitCode}`),
        err => finish(firstLine(message(err))),
      ).catch(() => undefined)
    } catch (err) {
      await finish(firstLine(message(err)))
    }
  } catch (err) {
    await adapterLog($, 'workfiles', firstLine(message(err)), run.id).catch(() => undefined)
  }
}

/** The paths the run it continues (its skill-loaded line's resumes, BEH-31) lists in its own state.json; none, with a log
 *  line saying why, when that file can't be used (ERR-19). That run only, never its ancestors. */
async function continuedFiles($: E, run: ProgressRun): Promise<string[]> {
  const resumes = resumesOf((await linesOf($, run))[0])
  if (resumes === null) return []
  const file = `${rootOf(run)}/devforgeai/progress/runs/${resumes}/state.json`
  let problem: string | null
  let paths: string[] = []
  try {
    const earlier: unknown = JSON.parse(await $.fs.read(file))
    problem = workFilesProblem(earlier)
    if (problem === null) paths = workFilePaths(earlier)
  } catch (err) {
    problem = firstLine(message(err))
  }
  if (problem !== null) await adapterLog($, 'workfiles', `${resumes}: not used: ${problem}`, run.id)
  return paths
}

/** Evaluate an ended run once more when there is time (BEH-05); taken in only while it is still the open run. */
async function finalEvaluation($: E, run: ProgressRun, timeoutMs: number | null, cleanup = false): Promise<void> {
  // Only when the run's log is written: a held log would leave the evaluator a stale file and a folder it can't write (BEH-42 (d)).
  if (timeoutMs === null || !python || runHold !== null) return
  await putFor($, run.id, () => ({ marked: false }))
  const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, timeoutMs)
  if (typeof got !== 'string') await absorb($, run, got, cleanup)
}

/** The state the run would have with one more event (BEH-08, BEH-21): the run's lines and the pending event in
 *  pending.jsonl, evaluated; null when it can't be had, which lets the call go on (fail open). */
async function pendingState($: E, kind: string, fields: Fields): Promise<{ state: ProgressState; seq: number; lines: readonly string[]; run: ProgressRun } | null> {
  await recordChain  // events still being written are part of the run the check judges
  const run = await get($, 'run')
  if (run === null) return null
  // While the run's log is held the check is not made: the call proceeds, with no pending file (BEH-08, BEH-21, BEH-42 (d)).
  if (runHold !== null) return null
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
    await countRefusal($, run, state.gate.kind ?? 'write', seq, cause.key, cause.step, cause.type, cause.message,
      stuckAdvice(cause.type, cause.userOwned))
  } catch (err) {
    // The notice is the user's; failing to give it never lets a refused call through (review N1).
    await recover($, 'tool.call', err)
  }
}

/** Count one refusal by its cause, keep it for the review, and tell the user once when the cause reaches 2 (BEH-25, BEH-26). */
async function countRefusal($: E, run: ProgressRun, gate: string, seq: number, key: string, step: number, type: string,
  text: string, advice: string): Promise<void> {
  let count = 0
  const kept = await putFor($, run.id, l => {
    count = (l.refusals[key] ?? 0) + 1
    return { refused: [...l.refused, { gate, seq, step, type, message: text }], refusals: { ...l.refusals, [key]: count } }
  })
  if (!kept || count !== 2) return
  const notice = stuckText(run.skill, step, text, advice)
  await notify($, notice)
  await adapterLog($, 'stuck', notice)
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
    await endOpenNow($, 'stopped', false)
    await putFor($, run.id, l => ({ summary: l.summary === null ? null : { ...l.summary, stoppedAt: n } }))
    const trail = (await hydrate($)).trail
    const top = trail[trail.length - 1]
    return top !== undefined && top.run !== null && unwindNow($, top.run.id)
  })
  if (resumed) await refreshStatus($)
}

/** A load Claude made with its Skill tool (BEH-29): what it came to. */
type LoadOutcome = { kind: 'own' } | { kind: 'unwound' } | { kind: 'pushed'; line: string } | { kind: 'cannot'; ended: ProgressRun | null } | { kind: 'failed' }

/** Claude's load of a tracked skill, as one chain item (BEH-29): of the open run's own skill, nothing while that run is
 *  unfinished; of a paused run's skill, an unwind to it (BEH-30 (d)); else a push when the open run can nest, or the
 *  open run's end. */
async function claudeLoadNow($: E, r: string, name: string, checklist: string): Promise<LoadOutcome> {
  const l = await hydrate($)
  const open = l.run
  if (open !== null && open.skill === name) {
    if (!(await finishedNow($))) return { kind: 'own' }
    // A finished run of the same skill ends and a new one opens, the trail kept: never a push, so the trail still
    // holds each skill once (version 15).
    return { kind: 'cannot', ended: await endOpenNow($, 'another-skill') }
  }
  const back = l.trail.find(t => t.skill === name && t.run !== null)
  if (back !== undefined) return (await unwindNow($, back.run!.id)) ? { kind: 'unwound' } : { kind: 'failed' }
  const step = await returnStepNow($)
  // A run that can't nest (no task IDs, no known step) ends, and the paused runs stay paused (BEH-03 for the open run).
  if (open === null || step === null) return { kind: 'cannot', ended: await endOpenNow($, 'another-skill') }
  // The open run is paused beneath another: while its log is held it gets one write of its whole log first (BEH-42 (h)).
  if (runHold !== null) await tryRun($, 'leave')
  const o = await prepareRun($, r, name, checklist)
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

/** Whether the open run is finished (BEH-29, version 15): ended, stopped (its run-end not yet evaluated), or every step
 *  reached. A run with no state yet is unfinished. */
async function finishedNow($: E): Promise<boolean> {
  const l = await hydrate($)
  if (l.run === null) return false
  if (l.summary !== null && (l.summary.ended !== null || l.summary.current === null)) return true
  return (await linesOf($, l.run)).some(x => x.includes('"kind":"run-end"'))
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
  // The run that returns leaves memory: while its log is held it gets one write of its whole log (BEH-42 (h)).
  if (runHold !== null) await tryRun($, 'leave')
  // A run whose review was already asked isn't asked again (BEH-26).
  if ((why === 'returned' || why === 'stopped') && openReviewed !== open.id) back.push({ run: top, refused: openRefused, reason: why })
  for (let i = above.length - 1; i >= 0; i--) {
    const p = above[i]
    if (p.run === null) continue
    const got = await endPausedNow($, p.run, 'returned')
    if (p.reviewed !== p.run.id) back.push({ run: got ?? p.run, refused: p.refused, reason: 'returned' })
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

/** The number of the skill's step with the write gate, from its manifests in the evaluator's order (IF-03), or null. */
async function writeGateOf($: E, r: string, skill: string): Promise<number | null> {
  const found: number[] = []
  for (const path of [`${$.plugin.root}/progress/manifests/${skill}.json`, `${r}/devforgeai/manifests/organization/${skill}.json`,
    `${r}/devforgeai/manifests/${skill}.json`]) {
    try {
      if (!(await $.fs.exists(path))) continue
      const steps = (JSON.parse(await $.fs.read(path)) as { steps?: Record<string, { gate?: string }> }).steps ?? {}
      for (const [n, step] of Object.entries(steps)) if (step.gate === 'write') found.push(Number(n))
    } catch {
      // an unreadable layer adds no gate; the evaluator reports it on its own (ERR-09)
    }
  }
  return found.length ? Math.min(...found) : null
}

/** The offer to continue an earlier run (BEH-31, version 16), at the person's typed load of a tracked skill, before its
 *  run opens: the skill-loaded fields and the line to add on Continue, or null for a run that opens as before. */
async function resumeOffer($: E, r: string, name: string): Promise<{ extra: Fields; line: string } | null> {
  let surfaces: readonly unknown[] = []
  try {
    surfaces = await $.session.surfaces()
  } catch {
    return null
  }
  if (surfaces.length === 0) return null
  // The offer evaluates the earlier run, which writes its state.json under the same devforgeai/progress/ that can't be written (ERR-17).
  if (runHold !== null) {
    await adapterLog($, 'resume', `no offer: the run's log is held (${NO_WRITE})`)
    return null
  }
  const runs = `${progressDir(r)}/runs`
  let latest: string | undefined
  try {
    if (!(await $.fs.exists(runs))) return null
    const named = new RegExp(`^[0-9]{8}T[0-9]{6}Z-${runName(name)}-[0-9a-f]{8}$`)  // the name run IDs give it (review S3)
    latest = (await $.fs.list(runs)).filter(x => x.kind === 'dir' && named.test(x.name)).map(x => x.name).sort().pop()
  } catch (err) {
    await adapterLog($, 'resume', `no offer: ${firstLine(message(err))}`)  // ERR-17
    return null
  }
  if (latest === undefined) return null
  const l = await hydrate($)
  const dir = `${runs}/${latest}`
  // The run open in this session while it hasn't ended is BEH-03's restart, and a paused run is the trail's.
  if (l.trail.some(t => t.run?.id === latest)) return null
  let lines: string[]
  try {
    lines = (await $.fs.read(`${dir}/events.jsonl`)).split('\n').filter(Boolean)
  } catch (err) {
    await adapterLog($, 'resume', `no offer: ${latest}: ${firstLine(message(err))}`)  // ERR-17
    return null
  }
  if (l.run?.id === latest && !lines.some(x => x.includes('"kind":"run-end"'))) return null
  const got = await evaluate($, r, `${dir}/events.jsonl`, `${dir}/state.json`, EVALUATOR_TIMEOUT)
  if (typeof got === 'string') {
    await adapterLog($, 'resume', `no offer: ${latest}: ${got}`)  // ERR-17
    return null
  }
  const plan = resumePlan(latest, got.state, lines, await writeGateOf($, r, name), await $.clock.now())
  if (plan === null) return null
  // BEH-39's <draft>: the work file the state names, while it still exists (a rejection counts as missing).
  if (plan.draftCandidate !== null) {
    try {
      if (await $.fs.exists(`${r}/${plan.draftCandidate}`)) plan.draft = plan.draftCandidate
    } catch {
      plan.draft = null
    }
  }
  await adapterLog($, 'resume', `offered ${latest} at step ${plan.step}`)
  let answer: string
  try {
    answer = await $.ui.ask(resumeQuestion(name, plan), { options: [`Continue from step ${plan.step}`, 'Start fresh'], header: 'Progress' })
  } catch (err) {
    // Esc is Start fresh; a dialog that can't be shown is too, and says why (ERR-17).
    await adapterLog($, 'resume', `fresh (${isDismissal(err) ? 'dismissed' : `the dialog failed: ${firstLine(message(err))}`})`)
    return null
  }
  if (answer !== `Continue from step ${plan.step}`) {
    await adapterLog($, 'resume', `fresh (${answer})`)
    return null
  }
  await adapterLog($, 'resume', `continued ${latest} at step ${plan.step}, carried ${plan.carried.join(', ')}`)
  return { extra: { resumes: latest, carried: plan.carried, answered: plan.answered, ...(plan.draft === null ? {} : { draft: plan.draft }) },
    line: resumeLine(name, plan) }
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
  // The state is stale and review.jsonl can't be written while the run's log is held: nothing is asked, and reviewed stays (BEH-26).
  if (runHold !== null) return
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
  if (runHold !== null || (await hydrate($)).returned.length === 0) return
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

// ---- Bash writes (BEH-38, version 22) ----

/** The gated rules of a run's skill, from its manifests in the evaluator's layer order (plugin, organization, project), read
 *  once per run and kept: the union of the layers' write rules, script rules and work-file patterns. A layer that can't be
 *  read adds nothing (the evaluator reports it on its own, ERR-09). A write pattern with a wildcard before its last / is
 *  skipped with one adapter.log line of kind bash when first read (BEH-38 (b)). */
async function gatedFor($: E, run: ProgressRun): Promise<Gated> {
  const kept = gatedCache.get(run.id)
  if (kept !== undefined) return kept
  const r = rootOf(run)
  const layers: unknown[] = []
  for (const path of [`${$.plugin.root}/progress/manifests/${run.skill}.json`, `${r}/devforgeai/manifests/organization/${run.skill}.json`,
    `${r}/devforgeai/manifests/${run.skill}.json`]) {
    try {
      if (await $.fs.exists(path)) layers.push(JSON.parse(await $.fs.read(path)))
    } catch {
      // an unreadable layer adds no rule
    }
  }
  const gated = gatedOf(layers)
  gatedCache.set(run.id, gated)
  for (const id of [...gatedCache.keys()].slice(0, -20)) gatedCache.delete(id)
  for (const w of gated.writes) {
    if (folderOf(w.pattern) === null) await adapterLog($, 'bash', `${w.pattern}: a wildcard before its last /, not listed`, run.id)
  }
  return gated
}

/** What BEH-38 watches for one Bash call: the open run, its root, its gated rules, its own draft paths and the folders to list. */
type Watch = { run: ProgressRun; root: string; gated: Gated; drafts: string[]; folders: string[] }

/** The run's own draft paths (BEH-38): this session's devforgeai/drafts/<skill>/<session ID>.md and the skill-loaded event's
 *  draft, each only when it matches a workFiles pattern of the manifest. */
async function ownDrafts($: E, run: ProgressRun, gated: Gated): Promise<string[]> {
  const out: string[] = []
  const add = (p: unknown) => {
    if (typeof p === 'string' && !out.includes(p) && gated.workFiles.some(w => pathMatches(p, w))) out.push(p)
  }
  try {
    const id = await $.session.id()
    if (typeof id === 'string' && SESSION_ID.test(id)) add(`devforgeai/drafts/${run.skill}/${id}.md`)
  } catch {
    // no session ID: no session draft
  }
  try {
    add((JSON.parse((await linesOf($, run))[0] ?? '{}') as Fields).draft)
  } catch {
    // no first line to read
  }
  return out
}

/** Whether BEH-38 applies to this Bash call: Claude Code's own call in the main loop (`engine` origin), a run open and its window
 *  not closed (before the first evaluation it is open). This is the one Bash-only origin check, BEH-38's own (version 25, BEH-33:
 *  its refusal and its check after cover Claude Code's own Bash calls only, so a call with no origin gets neither); BEH-33's
 *  filter for every tool (isFromMod, in the tool.call hook) returns before this for another mod's call and repeats nothing of it. */
async function bashWatch($: E, input: Fields, origin: unknown): Promise<Watch | null> {
  if (!isEngine(origin) || typeof input.command !== 'string') return null
  const l = await hydrate($)
  const run = l.run
  if (run === null || disabled || l.closedFor === run.id) return null
  const gated = await gatedFor($, run)
  const drafts = await ownDrafts($, run, gated)
  if (!gated.writes.length && !drafts.length) return null
  const folders: string[] = []
  for (const f of [...gated.writes.map(w => folderOf(w.pattern)), ...drafts.map(folderOfFile)]) {
    if (f !== null && !folders.includes(f)) folders.push(f)
  }
  return { run, root: rootOf(run), gated, drafts, folders }
}

type Listing = { files: Map<string, Listed>; failed: string[] }

/** BEH-38 (b)'s listing: each folder of the run's root, joined to the project-relative folder (never a bare path, since a
 *  command's cd moves Claude Code's own directory), as name, kind, size and mtimeMs. A missing folder lists as empty; any
 *  other failure skips that folder and writes an ERR-23 line. */
async function listFolders($: E, w: Watch): Promise<Listing> {
  const out: Listing = { files: new Map(), failed: [] }
  for (const folder of w.folders) {
    const dir = folder === '' ? w.root : `${w.root}/${folder.replace(/\/+$/, '')}`
    try {
      for (const e of await $.fs.list(dir)) out.files.set(`${folder}${e.name}`, { kind: e.kind, size: e.size, mtimeMs: e.mtimeMs })
    } catch (err) {
      let missing = false
      try {
        missing = !(await $.fs.exists(dir))
      } catch {
        missing = false
      }
      if (!missing) {
        out.failed.push(folder)
        await adapterLog($, 'bash', `${folder || '.'}: ${firstLine(message(err))}`, w.run.id)
      }
    }
  }
  return out
}

/** The paths among `paths` that another live run's log names (BEH-38 (b)): a folder under runs/ other than this run's and the
 *  run it continues, with no run-end and an events.jsonl modified in the last 30 minutes, whose log holds the path in a tool
 *  event. Read only for the candidates a listing found, never on every call. */
async function namedByLiveRuns($: E, w: Watch, paths: readonly string[]): Promise<Set<string>> {
  const named = new Set<string>()
  const runs = `${progressDir(w.root)}/runs`
  let dirs: string[]
  try {
    dirs = (await $.fs.list(runs)).filter(x => x.kind === 'dir').map(x => x.name)
  } catch {
    return named
  }
  const continued = resumesOf((await linesOf($, w.run))[0])
  const now = await $.clock.now()
  for (const id of dirs) {
    if (id === w.run.id || id === continued) continue
    let lines: string[]
    try {
      const mtime = (await $.fs.list(`${runs}/${id}`)).find(x => x.name === 'events.jsonl')?.mtimeMs
      if (typeof mtime !== 'number' || now - mtime > IDLE_MS) continue
      lines = (await $.fs.read(`${runs}/${id}/events.jsonl`)).split('\n').filter(Boolean)
    } catch {
      continue
    }
    for (const p of paths) {
      const got = logNames(lines, p)
      if (got.names && !got.ended) named.add(p)
    }
  }
  return named
}

/** BEH-38 (b): the documents the call created or changed, read, in order of path; the signatures to remember with them. */
async function wroteFiles($: E, w: Watch, before: Listing): Promise<{ path: string; content: string | undefined; sig: string }[]> {
  const after = await listFolders($, w)
  const changed = changedFiles(before.files, after.files, [...before.failed, ...after.failed])
    .filter(p => w.drafts.includes(p) || w.gated.writes.some(r => ruleMatches(p, r.pattern)))
  const seen = (await hydrate($)).wroteSeen[w.run.id] ?? {}
  const fresh = changed.filter(p => seen[p] !== signature(after.files.get(p)!))
  if (!fresh.length) return []
  const other = await namedByLiveRuns($, w, fresh)
  const out: { path: string; content: string | undefined; sig: string }[] = []
  for (const path of fresh) {
    if (other.has(path)) continue
    let content: string | undefined
    try {
      content = await $.fs.read(`${w.root}/${path}`)
    } catch (err) {
      await adapterLog($, 'bash', `${path}: ${firstLine(message(err))}`, w.run.id)
    }
    out.push({ path, content, sig: signature(after.files.get(path)!) })
  }
  return out
}

/** Enforce mode's immediate evaluation after a Bash call recorded documents (BEH-38 (b)): IF-03 on the run's recorded lines,
 *  into pending.json (never state.json, which the timer's evaluation writes), the flags raised at the wrote events' seqs, and
 *  the text for the model; null when there are none or the evaluation fails (ERR-23: it fails open). */
async function wroteCheck($: E, w: Watch, seqs: readonly number[], paths: readonly string[]): Promise<string | null> {
  if (!python) return null
  try {
    const got = await evaluate($, w.root, `${w.run.dir}/events.jsonl`, `${w.run.dir}/pending.json`, EVALUATOR_TIMEOUT)
    if (typeof got === 'string') {
      await adapterLog($, 'bash', `evaluation: ${got}`, w.run.id)
      return null
    }
    const flags = got.state.flags.filter(f => seqs.includes(f.seq))
    return flags.length ? wroteText(paths, flags.map(f => f.message)) : null
  } catch (err) {
    await adapterLog($, 'bash', `evaluation: ${firstLine(message(err))}`, w.run.id).catch(() => undefined)
    return null
  }
}

/** An answer event's fields (BEH-37, version 22): answered, the question's tag, and the form Claude asked, unless the tag says the
 *  question isn't the checklist's (outside). Never the user's answer. */
function formed(input: Fields, answered: boolean, logBytes: number): Fields {
  const tag = questionTag(input)
  return tag.outside === true ? { answered, ...tag } : { answered, ...tag, questions: formOf(input, logBytes) }
}

/** Enforce mode's write-gate check (BEH-08): the refusal text, or null to let the call go on. `count` is false for another mod's
 *  Write or Edit (BEH-33): it meets the gate all the same, but the refusal is nobody's of Claude's to count (BEH-25, BEH-26). */
async function enforceCheck($: E, fields: Fields, content: string | null, count = true): Promise<string | null> {
  const got = await pendingState($, 'tool', { ...fields, exit: 0, error: false, content: keptContent(content, await logBytes($)) })
  const run = await get($, 'run')
  if (got === null) return null
  const refusal = refusalText(got.state, got.seq, run !== null && (await follows($, run)) ? got.lines : null)
  if (refusal !== null && count) await noteRefusal($, got.state, got.seq, got.run)
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

// ---- /progress (BEH-34, ERR-21; version 21) ----

/** Register /progress (immediate, so it answers while Claude works) at session.start and after /clear, /resume and /branch, which
 *  fire none; registering a name again replaces it. A name the host refuses is logged (held until the session's first run, as every
 *  earlier line is) and marks the registration failed, so the command.run hook passes the command on (ERR-21). */
async function registerProgress($: E): Promise<void> {
  try {
    await $.command.register({ name: 'progress', description: 'Show the DevForgeAI run in progress', immediate: true })
    progressOk = true
  } catch (err) {
    progressOk = false
    await adapterLog($, 'command', firstLine(message(err)))
  }
}

/** What /progress prints (BEH-34): from the functions that build the status line and the band, so the three never disagree. While a
 *  hold lasts the remedy row's text is the last line (version 27). */
async function progressNow($: E): Promise<string> {
  const now = await $.clock.now()
  const mode = await read($, MODE)
  const off = await read($, OFF)
  const l = await hydrate($)
  const idle = !turnOpen && l.lastEventAt > 0 && now - l.lastEventAt > IDLE_MS
  const view = holdView()
  const remedy = view === null ? null : remedyRow(view, mode === 'enforce', progressOk)
  // A run is open but its first evaluation isn't in yet (the status line and the band show nothing either): BEH-34 gives no text
  // for it, and "no run is open" would be false. A builder's reading, for Bryan.
  if (l.run !== null && l.summary === null) return `${l.run.skill} run just started; its first evaluation isn't in yet.${remedy === null ? '' : `\n${remedy}`}`
  return progressReport(l.summary, l.run !== null, mode, idle, off, l.trail, holdKind(), remedy)
}

/** `/progress retry` (BEH-34, BEH-42): tries the held writes at once and says what came of it; after the tracker's stop it writes the
 *  .gitignore of devforgeai/progress/ in the session's root, and when that works lifts the stop for both files; after the ledger's
 *  own stop it tries the odometer's file. It records nothing and adds nothing to a hold's count. */
async function retryNow($: E): Promise<string> {
  if (disabled) {
    const root = await $.session.root()
    const failed = await ensureIgnore($, root, true)
    if (failed !== null) {
      const error = errorLine(message(failed.err))
      await adapterLog($, 'write', `retry failed: ${failed.path}: ${error}`)
      return stillStoppedAnswer(failed.path, error)
    }
    disabled = false
    odoGaveUp = false
    await update($, OFF, () => null)
    await useLogRoot($, root)
    await adapterLog($, 'write', 'stop lifted by /progress retry')
    await refreshStatus($)
    redraw($)
    return liftedAnswer()
  }
  const answers: string[] = []
  if (runHold !== null || odoHold !== null) {
    for (const t of await retryHolds($, 'command')) answers.push(t.ok ? savedAnswer(t.saved, t.path) : stillAnswer(t.path, t.error, t.lines, t.tries))
  }
  if (odoGaveUp) answers.push(await ledgerRun(() => liftOdometer($)))
  return answers.length ? answers.join('\n') : NOTHING_TO_RETRY
}

/** After the ledger's own stop: its file is written with the lines it holds; when that works the ledger writes again. */
async function liftOdometer($: E): Promise<string> {
  const file = ledgerFile
  if (file === null) return NOTHING_TO_RETRY
  try {
    await $.fs.write(file.path, file.lines.length ? file.lines.join('\n') + '\n' : '')
  } catch (err) {
    return odometerStillAnswer(file.path, errorLine(message(err)))
  }
  odoGaveUp = false
  await adapterLog($, 'dashboard', 'odometer: stop lifted by /progress retry')
  await refreshStatus($)
  redraw($)
  return odometerOnAnswer()
}

// ---- the precompact row and the automatic run (BEH-35, BEH-36, BEH-41, ERR-22; versions 21, 23 and 25) ----

/** The settings of DM-07 and DM-08, read when the module loads; a value that is not a whole number from 0 to 95 counts as its
 *  default and leaves a note for adapter.log (kind setting). */
function readFuelSettings(options: Fields | undefined): void {
  settingNotes = []
  const warn = fuelSetting(options?.precompactWarnFuel, 30)
  const run = fuelSetting(options?.precompactRunFuel, 20)
  warnFuel = warn.value
  runFuel = run.value
  if (warn.invalid) settingNotes.push(`precompactWarnFuel: ${String(options?.precompactWarnFuel)} is not a whole number from 0 to 95; using 30`)
  if (run.invalid) settingNotes.push(`precompactRunFuel: ${String(options?.precompactRunFuel)} is not a whole number from 0 to 95; using 20`)
}

/** What a session start announces: the notes of settings that were out of range, and /progress. */
async function announce($: E): Promise<void> {
  const notes = settingNotes
  settingNotes = []
  for (const note of notes) await adapterLog($, 'setting', note)
  await registerProgress($)
}

/** session.measure (BEH-35, BEH-36): keep the measured share, or clear it when the measurement has none; then, at or below the
 *  run share, start the run once. The mark is set in memory and in $.state before the command is asked for, so a second
 *  measurement or a reload starts none; BEH-41's set gets precompact first, so the plugin's own command.run hook takes the run for
 *  the person's typed one (BEH-02 then marks the handoff's turn). The command runs once the session is idle, so the hook does not
 *  wait for it (probe, 2026-10-08). */
async function measured($: E, raw: unknown): Promise<void> {
  const percent = measuredShare(raw)
  const was = await read($, PRECOMPACT)
  if (was.percent !== percent) await update($, PRECOMPACT, p => ({ ...p, percent }))
  if (percent === null || !precompactDue({ ...was, percent }, runFuel) || autoRun) return
  autoRun = true
  await update($, PRECOMPACT, p => ({ ...p, ran: true, pending: true }))   // one write: the run mark and the pending mark (version 26)
  const fuel = 100 - percent
  await notify($, `Fuel ${fuel}%: running /devforgeai:precompact`)
  await adapterLog($, 'precompact', `fuel ${fuel}%: started /devforgeai:precompact`)
  addStart(starts, 'devforgeai:precompact')
  try {
    void Promise.resolve($.command.run({ command: 'devforgeai:precompact' })).then(
      () => undefined,
      err => failedPrecompact($, err),
    ).catch(() => undefined)
  } catch (err) {
    await failedPrecompact($, err)
  }
}

/** ERR-22: the run mark stays (nothing is tried again before the next compaction), precompact, and only it, leaves BEH-41's set,
 *  and the row asks the person to run the skill. */
async function failedPrecompact($: E, err: unknown): Promise<void> {
  takeStart(starts, 'devforgeai:precompact')
  await adapterLog($, 'precompact', `could not run /devforgeai:precompact: ${firstLine(message(err))}`)
  await update($, PRECOMPACT, p => (p.failed && !p.pending ? p : { ...p, failed: true, pending: false }))   // and the pending mark (version 26)
}

/** A load of the plugin's own precompact skill hides the row until a compaction (BEH-35). */
async function hidePrecompact($: E): Promise<void> {
  if (!(await read($, PRECOMPACT)).hidden) await update($, PRECOMPACT, p => ({ ...p, hidden: true }))
}

/** Whether BEH-36 has started a run since the last compaction: in memory, or in $.state after a reload. */
async function precompactStarted($: E): Promise<boolean> {
  return autoRun || (await read($, PRECOMPACT)).ran
}

/** A compaction empties the row's values, the run mark and the pending mark (BEH-35), and so do /clear, /resume and /branch. */
async function resetPrecompact($: E): Promise<void> {
  autoRun = false
  const was = await read($, PRECOMPACT)
  // Written only when something changes (BEH-35), which redraws the band.
  if (was.percent !== null || was.hidden || was.ran || was.failed || was.pending) await update($, PRECOMPACT, () => NO_PRECOMPACT)
}

// ---- the marked turn (BEH-02; versions 18, 19 and 26) ----

/** A turn ID the host gave: a non-empty string; anything else is no ID. */
function turnIdOf(id: unknown): string | null {
  return typeof id === 'string' && id !== '' ? id : null
}

/** Mark the turn (BEH-02), in module memory and before anything that can fail: Claude's own load is bound to the turn already
 *  open (or to 'any' when its ID isn't known), any other marked load to the next main-loop turn.start. The tag for the load line. */
function markTurn(claude: boolean, precompact: boolean): string {
  untrackedTurn = true
  markIsPrecompact = precompact
  if (claude) {
    markBind = currentTurn !== null ? { kind: 'turn', id: currentTurn, since: [] } : { kind: 'any' }
    return currentTurn ?? 'any'
  }
  markBind = { kind: 'next' }
  return 'next'
}

/** A main-loop turn.start (version 26): it is the main loop's current turn; it binds a mark waiting for the next turn.start, and a
 *  bound mark keeps the IDs of the turns started since. */
function turnStarted(id: string | null): void {
  currentTurn = id
  if (markBind === null) return
  if (markBind.kind === 'next') markBind = id !== null ? { kind: 'turn', id, since: [] } : { kind: 'any' }
  else if (markBind.kind === 'turn' && id !== null) markBind = { ...markBind, since: [...markBind.since, id] }
}

/** The end of the mark, at the entry of a main-loop turn.complete (synchronously, before any await): it ends when the complete is
 *  of the bound turn or of a turn started after it, or the host gave no ID, or no ID could be bound ('any'); the complete of an
 *  earlier turn, and of any turn while the mark waits for its turn.start, ends nothing. The cleared line's fields, or null. */
function markEndsAt(id: string | null): { turn: string; bound: string } | null {
  const bind = markBind
  if (!untrackedTurn || bind === null) return null
  const ends = id === null || bind.kind === 'any' || (bind.kind === 'turn' && (id === bind.id || bind.since.includes(id)))
  if (!ends) return null
  const out = markIsPrecompact ? { turn: id ?? '-', bound: bind.kind === 'turn' ? bind.id : '-' } : null
  untrackedTurn = false
  markBind = null
  markIsPrecompact = false
  return out
}

/** A compaction (BEH-35) clears only a mark no turn.start has bound yet; a bound one ends at its own turn's complete. The cleared
 *  line is written when the mark was a precompact load's. */
async function markEndsAtCompaction($: E): Promise<void> {
  if (!untrackedTurn || markBind === null || markBind.kind !== 'next') return
  const logged = markIsPrecompact
  untrackedTurn = false
  markBind = null
  markIsPrecompact = false
  if (logged) await adapterLog($, 'precompact', 'cleared: by=compaction turn=- bound=-')
}

/** The session's end clears any mark and the turn IDs; the cleared line, naming the host's reason, is written before they are
 *  reset (version 26). /branch reports resume. */
async function markEndsAtSessionEnd($: E, reason: unknown): Promise<void> {
  if (untrackedTurn && markIsPrecompact) {
    const by = reason === 'clear' || reason === 'resume' || reason === 'logout' || reason === 'prompt_input_exit' ? reason : 'other'
    const bound = markBind !== null && markBind.kind === 'turn' ? markBind.id : '-'
    await adapterLog($, 'precompact', `cleared: by=${by} turn=- bound=${bound}`)
  }
  clearMarkMemory()
}

/** The mark and the turn IDs, emptied: the session's end, and the reset at /clear, /resume and /branch. */
function clearMarkMemory(): void {
  untrackedTurn = false
  markBind = null
  markIsPrecompact = false
  currentTurn = null
}

// ---- the odometer ledger (SPEC-016 BEH-10, ERR-06; built with version 25) ----

/** The session's file as the module knows it: the lines it holds (read back once, then its own), or stopped (ERR-06). */
type LedgerFile = { path: string; lines: string[]; stopped: boolean }
let ledgerFile: LedgerFile | null = null
/** Lines not yet in the file: they wait for a root (BEH-15: no run has opened one) or for a write that failed. */
let ledgerHeld: string[] = []
let ledgerChain: Promise<unknown> = Promise.resolve()
const ledgerNoted = new Set<string>()
/** At most this many lines wait in memory with no root to write to; a file holds about as many in 4 MiB. */
const LEDGER_HELD_LIMIT = 20000

/** One adapter.log line of kind dashboard for each session and cause (ERR-06). */
async function ledgerNote($: E, session: string, cause: string, text: string): Promise<void> {
  const key = `${session}\n${cause}`
  if (ledgerNoted.has(key)) return
  ledgerNoted.add(key)
  await adapterLog($, 'dashboard', `odometer: ${text}`)
}

/** Ledger work, one item at a time: a line being added and a try at the odometer's hold never race (BEH-42). */
function ledgerRun<T>(work: () => Promise<T>): Promise<T> {
  const step = ledgerChain.then(work)
  ledgerChain = step.catch(() => undefined)
  return step
}

/** One turn's line for the session's ledger, in the order the turns end. */
async function ledgerTurn($: E, turn: string, source: string, counts: { input: number; output: number; cacheRead: number; cacheWrite: number }): Promise<void> {
  const session = await $.session.id()
  const line = ledgerLine(session, turn, source, counts, await $.clock.now())
  await ledgerRun(() => ledgerAdd($, session, line)).catch(() => undefined)
}

/** Add a line and write the file whole, with $.fs having no append (SPEC-016 BEH-10): only the root of the latest run, only once
 *  a run has opened one (logRoot, BEH-15), reading the session's own file back once at the first write. A failed write is a hold
 *  (BEH-42): the lines wait for the next try, which is the end of a main-loop turn or `/progress retry`, and a subagent's line is
 *  added and not written while it lasts; after 10 failed turn tries the ledger stops for the session (ERR-06). A file that can't be
 *  read back, or would pass 4 MiB, is left alone for the session, and no retry lifts that. A stopped tracker keeps and writes nothing. */
async function ledgerAdd($: E, session: string, line: string): Promise<void> {
  if (typeof session !== 'string' || !SESSION_ID.test(session)) {
    await ledgerNote($, String(session), 'session', 'the session ID makes no path, so no line is kept')
    return
  }
  if (disabled || odoGaveUp) return
  const root = logRoot
  // The cap is for the wait only: once a run has opened a root the held lines are written, whatever their number.
  if (root === null && ledgerHeld.length >= LEDGER_HELD_LIMIT) {
    await ledgerNote($, session, 'held', 'no run has opened a root and the held lines are full: later lines are dropped')
    return
  }
  ledgerHeld.push(line)
  if (root === null) return
  const path = `${progressDir(root)}/odometer/${session}.jsonl`
  if (ledgerFile === null || ledgerFile.path !== path) {
    const fresh: LedgerFile = { path, lines: [], stopped: false }
    ledgerFile = fresh
    try {
      if (await $.fs.exists(path)) fresh.lines = (await $.fs.read(path)).split('\n').filter(Boolean)
    } catch (err) {
      fresh.stopped = true
      await ledgerNote($, session, 'read', `${path} can't be read back, so it is not written this session: ${firstLine(message(err))}`)
    }
  }
  const file = ledgerFile as LedgerFile
  if (file.stopped) {
    ledgerHeld = []
    return
  }
  const lines = [...file.lines, ...ledgerHeld]
  const text = lines.join('\n') + '\n'
  if (byteSize(text) > LOG_LIMIT) {
    file.stopped = true
    ledgerHeld = []
    const hadHold = odoHold !== null
    odoHold = null
    await ledgerNote($, session, 'full', `${path} would pass 4 MiB, so it is not written any more this session`)
    if (hadHold) {
      await refreshStatus($)
      redraw($)
    }
    return
  }
  // A hold: the line waits for the next try (BEH-42 (b)).
  if (odoHold !== null) return
  try {
    await $.fs.write(path, text)
    file.lines = lines
    ledgerHeld = []
  } catch (err) {
    await holdStarts($, 'odometer', path, err, ledgerHeld.length)
  }
}

export const register: Register = (on, options) => {
  // With tracking off, the adapter does nothing at all (BEH-01, DM-05).
  if ((options as Fields | undefined)?.tracking === 'off') return
  retentionDays = retentionOf((options as Fields | undefined)?.retentionDays)
  readFuelSettings(options as Fields | undefined)

  on('session.start', async ($, e, next) => {
    interactive = e.isInteractive
    if (interactive) {
      await setup($)
      await announce($)
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'session.start', next.error)
    return next(e)
  })

  // After /clear, /resume or /branch no session.start fires, and $.state is empty (BEH-06, BEH-16).
  on('classic.SessionStart', { source: ['clear', 'resume', 'fork'] }, async ($, e, next) => {
    if (interactive === true) {
      if (!disabled) {
        await resolveMode($, await $.session.root())
        ensureTimer($)
        // The new session starts with no row, no run mark and no pending name (BEH-35, BEH-41).
        starts.clear()
        clearMarkMemory()
        await resetPrecompact($)
      }
      // /progress is registered again, also while the tracker has stopped (the stop survives /clear, /resume and /branch), so that
      // `/progress retry` stays reachable (BEH-34, version 27).
      await registerProgress($)
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
      // A load made inside another plugin's mod's Skill call (BEH-33): no run ends, opens or pauses, nothing is offered, marked
      // or hidden, and the text goes on unchanged. Claude's own call and the person's typed command for the same name come first.
      if (modLoading.has(name) && !skillsLoading.has(name) && typedName !== name) return out
      // One read of the root serves every decision as the run opens (BEH-03): tracked, the folder, the mode.
      const r = await $.session.root()
      const kind = await skillKind($, r, name)
      if (kind === 'other') return out
      const precompact = name === 'precompact' && (pluginSkills ?? []).includes(name)
      const claude = skillsLoading.has(name)
      const kept = typedName === name
      let pending = false
      if (kind === 'untracked') {
        // An untracked skill's load opens no run, ends, pauses or unwinds nothing, offers nothing and changes no display
        // (BEH-02, version 18). The turn is marked by the person's load (the typed name BEH-31 keeps), BEH-41's set (the same
        // kept name), Claude's (BEH-29's in-flight set) or, from version 26, the plugin's own precompact skill while BEH-36's
        // pending mark is set (read from $.state, so a kept name or a set lost before the load loses nothing); a subagent's
        // load marks nothing. The mark is set first, before the hide and the consumption, so a rejected $.state write in either
        // skips nothing of it.
        if (precompact) {
          try {
            pending = (await read($, PRECOMPACT)).pending === true
          } catch {
            pending = false
          }
        }
        const typed = kept && typedSource !== 'set'
        const set = kept && typedSource === 'set'
        const marked = typed || set || claude || pending
        const tag = marked ? markTurn(claude, precompact) : '-'
        if (precompact) {
          await adapterLog($, 'precompact', `load: marked=${marked} typed=${typed} set=${set} claude=${claude} pending=${pending} turn=${tag}`)
        }
      }
      // A load of the plugin's own precompact skill hides the row until a compaction (BEH-35): the person's, Claude's, or one that
      // comes after BEH-36's run mark (which a reload keeps in $.state, so the hide depends on neither BEH-41's set nor the pending
      // mark); a subagent's load hides it only by the run mark. The load also consumes the pending mark, whichever path marked.
      // One write for both; a refused write is logged and skips nothing else.
      if (precompact) {
        try {
          const hide = kept || claude || (await precompactStarted($))
          const consume = kind === 'untracked' && pending
          if (hide || consume) await update($, PRECOMPACT, p => ({ ...p, hidden: p.hidden || hide, pending: consume ? false : p.pending }))
        } catch (err) {
          await adapterLog($, 'error', `precompact: ${firstLine(message(err))}`)
        }
      }
      if (kind === 'untracked') return out
      ensureTimer($)
      // A load that isn't Claude's (typed, or a subagent's) ends the open run and every paused run (BEH-03, BEH-29).
      if (!skillsLoading.has(name)) {
        // The person's typed load may continue an earlier run (BEH-31, version 16).
        let offer: { extra: Fields; line: string } | null = null
        if (typedName === name) {
          try {
            offer = await resumeOffer($, r, name)
          } catch (err) {
            await recover($, 'skill.prompt', err)  // the offer never stops the load (ERR-17)
          }
        }
        await switchRun($, r, name, out.text, true, offer?.extra ?? {})
        return offer === null ? out : { ...out, text: `${out.text}\n\n${offer.line}` }
      }
      // Claude's load with no unfinished run open and none paused is offered as a typed load is (BEH-31, version 17):
      // it nests nothing, and a fresh run would bury the unfinished one.
      let offer: { extra: Fields; line: string } | null = null
      const now = await hydrate($)
      const open = now.run
      const ended = open !== null && ((now.summary?.ended ?? null) !== null
        || (await linesOf($, open)).some(x => x.includes('"kind":"run-end"')))
      if (now.trail.length === 0 && (open === null || ended)) {
        try {
          offer = await resumeOffer($, r, name)
        } catch (err) {
          await recover($, 'skill.prompt', err)  // the offer never stops the load (ERR-17)
        }
      }
      // Claude's load (BEH-29): task-tool calls under way first, so a TaskUpdate of the same batch sets the return step.
      if (taskWork.size > 0) await Promise.race([Promise.allSettled([...taskWork]), $.clock.sleep(TASK_WAIT_MS)])
      const got = await chained(() => claudeLoadNow($, r, name, out.text))
      // The Skill call records nothing in either run once the open run changed (before skill.prompt returns).
      if (got.kind !== 'own') switchedIn.add(name)
      if (got.kind === 'cannot') await finishSwitch($, r, name, out.text, got.ended, false, offer?.extra ?? {})
      await refreshStatus($)
      if (got.kind === 'pushed') return { ...out, text: `${out.text}\n\n${got.line}` }
      if (got.kind === 'cannot' && offer !== null) return { ...out, text: `${out.text}\n\n${offer.line}` }
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
    // The open run's tenure as this hook began, before any await (BEH-30 (a)), and whether the turn was marked (BEH-02).
    const began = tenure
    const unrecorded = untrackedTurn
    const input = e as unknown as Fields
    const tool = String(input.tool)
    // Another plugin's mod (BEH-33, version 21): the call changes nothing of the tracker, and gives no event of any kind, no
    // step event, no task map entry, no Skill load for the trail, no question for BEH-21's check, no work for BEH-30 and no call for
    // BEH-02's marked turn; and it is no refusal of Claude's to count (BEH-25, BEH-26). It still meets the enforce-mode write gate
    // (BEH-08): where a call comes from relaxes no gate. BEH-38's two parts are Claude Code's own Bash calls only (its check in
    // bashWatch), so this return comes before them. A missing origin counts as Claude Code's (isFromMod).
    if (isFromMod(next.origin)) {
      // A Skill call of a mod keeps its skill's name in modLoading while it is in flight, so the skill.prompt that fires inside it
      // is not taken for a load nobody typed (which would end the open run): it changes nothing (BEH-33; skill.prompt).
      const modLoad = tool === 'Skill' && typeof input.skill === 'string' ? skillName(input.skill) : null
      if (modLoad !== null) modLoading.set(modLoad, (modLoading.get(modLoad) ?? 0) + 1)
      try {
        if ((tool === 'Write' || tool === 'Edit') && (await recording($, input.agentId)) && (await read($, MODE)) === 'enforce' && python) {
          const open = await get($, 'run')
          const r = open !== null ? rootOf(open) : await $.session.root()
          const refusal = await enforceCheck($, { tool, path: toolPath(r, tool, input) }, await contentOf($, r, tool, input), false)
          if (refusal !== null) {
            await adapterLog($, 'refused', firstLine(refusal.split('\n')[1] ?? refusal))
            if (!(await hasSurface($))) await $.ui.log(refusal)
            return { deny: refusal }
          }
        }
        return await next(e)
      } finally {
        if (modLoad !== null) {
          const n = (modLoading.get(modLoad) ?? 1) - 1
          if (n > 0) modLoading.set(modLoad, n)
          else modLoading.delete(modLoad)
        }
      }
    }
    // Registered before any await, so a question in the same batch finds it (BEH-21).
    const finish = TASK_TOOLS.includes(tool) ? startTaskWork() : null
    // The skills the main loop's Skill calls in flight are loading (BEH-29): skill.prompt fires inside the call.
    const loading = tool === 'Skill' && input.agentId === undefined && typeof input.skill === 'string' ? skillName(input.skill) : null
    if (loading !== null) skillsLoading.set(loading, (skillsLoading.get(loading) ?? 0) + 1)
    try {
      // Awaited, so the finally below runs after the call: a Skill call stays in flight while its skill.prompt fires,
      // with no run open too (version 17; returning next(e)'s promise unawaited ran the finally at once).
      if (!(await recording($, input.agentId))) return await next(e)
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
              : formed(input, isAnswered(outcome), await logBytes($)), true, began)
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
      // Bash writes (BEH-38, version 22): the call's own run, window and rules, for Claude Code's own calls only.
      const watch = tool === 'Bash' ? await bashWatch($, input, next.origin) : null
      if (watch !== null && (await read($, MODE)) === 'enforce') {
        const hit = outsideWord(String(input.command), watch.gated, watch.root)
        if (hit !== null) {
          const text = outsideRefusal(hit.word)
          // The refused call is recorded as an error, which is never evidence; its entry counts for BEH-25 and BEH-26.
          await chained(async () => {
            const into = await recordNow($, 'tool', { ...fields, exit: null, error: true }, true, began)
            const run = await get($, 'run')
            if (into !== null && run !== null && run.id === into) {
              await countRefusal($, run, 'write', run.seq, `write:${OUTSIDE_WRITE_TYPE}:${hit.step}`, hit.step, OUTSIDE_WRITE_TYPE,
                outsideMessage(hit.word), OUTSIDE_ADVICE)
            }
          })
          await adapterLog($, 'bash', `refused ${hit.word}`)
          if (!(await hasSurface($))) await $.ui.log(text)
          return { deny: text }
        }
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
      // BEH-38 (b): the listing before the call, in a recorded turn only.
      let before: Listing | null = null
      if (watch !== null && !unrecorded) {
        try {
          before = await listFolders($, watch)
        } catch (err) {
          await recover($, 'tool.call', err)
        }
      }
      const result = await next(e)
      if (loading !== null && switchedIn.delete(loading)) return result
      // A hook that began in a marked turn leaves no tool event, in any run, and a task-tool call changes no task map, gives
      // no step event and unwinds nothing (BEH-02, BEH-30 (a)). The Skill call that loaded the untracked skill began before
      // the mark, and answers and the enforce checks above are as before.
      if (unrecorded) return result
      try {
        const outcome = result as unknown as ToolOutcome
        const done: Fields = { ...fields, exit: exitOf(outcome), error: isFailed(outcome), content: keptContent(content, await logBytes($)) }
        let resumed = false
        // The documents the call wrote (BEH-38 (b)); a failure here records the call itself all the same.
        let wrote: { path: string; content: string | undefined; sig: string }[] = []
        if (watch !== null && before !== null) {
          try {
            wrote = await wroteFiles($, watch, before)
          } catch (err) {
            await adapterLog($, 'bash', firstLine(message(err)), watch.run.id)
          }
        }
        const wroteSeqs: number[] = []
        // One chain item: the unwind a TaskUpdate shows (BEH-30 (a)), before its own events, then its tool event, step
        // events and task map, all in the run open when they land.
        await chained(async () => {
          // The open run has worked, and this TaskUpdate began after it opened: the "mark and load" batch unwinds nothing.
          if (tool === 'TaskUpdate' && !isFailed(outcome) && worked && began === tenure) {
            const trail = (await hydrate($)).trail
            const at = pausedWith(trail, input.taskId)
            if (at >= 0 && trail[at].run !== null) resumed = await unwindNow($, trail[at].run!.id)
          }
          const into = await recordNow($, 'tool', done, true, began)
          if (into !== null && TASK_TOOLS.includes(tool)) await taskStepsNow($, into, tool, input, outcome)
          // Right after the call's own event, in order of path: one event with wrote for each document (BEH-38 (b)); error is
          // false whatever the exit, since the file is on disk.
          if (into !== null && watch !== null && into === watch.run.id) {
            for (const f of wrote) {
              const at = await recordNow($, 'tool', { tool, path: f.path, command: fields.command, exit: done.exit, error: false,
                content: keptContent(f.content, await logBytes($)), wrote: true }, true, began)
              const run = await get($, 'run')
              if (at !== null && run !== null) wroteSeqs.push(run.seq)
            }
            if (wroteSeqs.length) {
              await putFor($, into, l => ({ wroteSeen: { ...l.wroteSeen, [into]: { ...(l.wroteSeen[into] ?? {}),
                ...Object.fromEntries(wrote.map(f => [f.path, f.sig])) } } }))
              await putMany($, l => {
                const ids = Object.keys(l.wroteSeen)
                return ids.length > 20 ? { wroteSeen: Object.fromEntries(ids.slice(-20).map(id => [id, l.wroteSeen[id]])) } : null
              })
            }
          }
        })
        if (resumed) await refreshStatus($)
        // In enforce mode the evaluation runs at once and the model is told what the flags say (BEH-38 (b), probe P14).
        // While the run's log is held the documents are recorded into the held lines and no evaluation runs (BEH-38, BEH-42 (d)).
        if (wroteSeqs.length && watch !== null && runHold === null && (await read($, MODE)) === 'enforce') {
          const text = await wroteCheck($, watch, wroteSeqs, wrote.map(f => f.path))
          if (text !== null) {
            const carried = WROTE_CONTEXT_ROUTE === 'result' ? withContext(result, text) : null
            if (carried !== null) return carried as typeof result
            pendingWrote = [...pendingWrote, { run: watch.run.id, text }]
            await adapterLog($, 'context', `wrote flags at seq ${wroteSeqs.join(', ')}`)
          }
        }
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
    const open = (await get($, 'run'))?.id
    const enforcing = (await read($, MODE)) === 'enforce' && !e.text.trimStart().startsWith('/')
    const extra: string[] = []
    if (report !== null && report.run === open && enforcing) {
      pendingReport = null
      await putFor($, report.run, l => ({ contextSent: [...l.contextSent, report.seq] }))
      await adapterLog($, 'context', `report gate at seq ${report.seq}`)
      extra.push(report.text)
    }
    // BEH-38 (b)'s text of an earlier Bash call, once: a prompt that starts with '/' keeps it for the next one, and a run that
    // has changed drops it (the user has moved on).
    if (pendingWrote.length) {
      const mine = pendingWrote.filter(x => x.run === open)
      if (enforcing) {
        pendingWrote = []
        extra.push(...mine.map(x => x.text))
      } else if (mine.length !== pendingWrote.length) pendingWrote = mine
    }
    return extra.length ? next({ ...e, context: [...(e.context ?? []), ...extra] }) : next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'prompt.submit', next.error)
    return next(e)
  })

  on('turn.start', async ($, e, next) => {
    if ((e as unknown as Fields).agentId === undefined) {
      skillsLoading.clear()
      switchedIn.clear()
      // The main loop's current turn, which binds a waiting mark and joins a bound one's later turns (BEH-02, version 26).
      turnStarted(turnIdOf((e as unknown as Fields).turnId))
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
    // A reply in a marked turn is recorded in no run (BEH-02, version 19): a numbered tick in the untracked skill's reply
    // would otherwise count as the open run's step.
    const unrecorded = untrackedTurn
    if (!unrecorded && (await recording($, e.agentId))) {
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
    // The main loop's turn ends the mark of an untracked load, whatever its reason and whether or not a run is open (BEH-02): from
    // version 26 when it is the bound turn's complete, or a later-started turn's, or none is bound; ended here synchronously, as
    // before any await, and the cleared line follows.
    const ended = e.agentId === undefined ? markEndsAt(turnIdOf(e.turnId)) : null
    if (ended !== null) await adapterLog($, 'precompact', `cleared: by=turn.complete turn=${ended.turn} bound=${ended.bound}`)
    const main = await recording($, e.agentId)
    // The turn's tokens (BEH-40, SPEC-012 version 17's usage kind): valid counts only, else none.
    const usage = usageFields(e.turnId, e.usage)
    // The holds that exist as this turn ends: only they are tried at its end (BEH-42 (b)); one that starts in it is not.
    const holds = { run: runHold, odo: odoHold }
    if (main) {
      turnOpen = false
      if (usage === null) await record($, 'turn', { phase: 'end' }, false)
      else {
        // One chain item, so the usage event is the one right after the turn's end event (BEH-40). A count and no evidence: no mark.
        await chained(async () => {
          await recordNow($, 'turn', { phase: 'end' }, false)
          await recordNow($, 'usage', usage, false)
        })
      }
    }
    // The odometer ledger (SPEC-016 BEH-10): the main loop's turn and a subagent's alike, in an interactive session with tracking on
    // and not stopped (a stopped tracker stops the ledger, ERR-06).
    if (usage !== null && interactive === true && !disabled) {
      try {
        await ledgerTurn($, usage.turn, e.agentId ?? 'main', usage)
      } catch (err) {
        await recover($, 'turn.complete', err)
      }
    }
    // The retry point (BEH-42 (b)): a main-loop turn's end, whatever its reason, tries each hold once, the run's log first, after the
    // turn's own events are recorded and before the review below; a subagent's turn end tries nothing.
    if (interactive === true && !disabled && e.agentId === undefined && (holds.run !== null || holds.odo !== null)) {
      try {
        await retryHolds($, 'turn', holds)
      } catch (err) {
        await recover($, 'turn.complete', err)
      }
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
    // BEH-41 (version 25): this plugin's own $.command.run of a name in the set (BEH-36's precompact; a tile's skill, held with the
    // dashboard) counts as the person's typed command. The name leaves the set at once, and only it, so each name serves one run.
    const own = verb === undefined && interactive === true && !disabled && isOwnRun(e.origin, $.plugin.name) && takeStart(starts, e.command)
    if (verb === undefined && interactive === true && !disabled && (isPersonPrompt(e.origin) || own)) {
      // The person's command, kept while it runs: a typed skill's skill.prompt fires inside next(e) (BEH-31).
      const name = skillName(e.command)
      typedName = name
      typedSource = own ? 'set' : 'person'
      try {
        return await next(e)
      } finally {
        if (typedName === name) {
          typedName = null
          typedSource = null
        }
      }
    }
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

  // /progress (BEH-34; version 21): answers only while this session's latest registration succeeded and the tracker hasn't
  // stopped; otherwise the command goes on untouched, so whatever else owns the name runs. It records nothing, opens and ends
  // no run, asks nothing and works in both modes. (Opening the dashboard pane, version 24, is held with the dashboard.)
  // Version 27: the argument `retry` tries the held writes at once, and after the tracker's stop the command answers its one line, so
  // that `/progress retry` is the way back (BEH-34, BEH-42).
  on('command.run', { command: 'progress' }, async ($, e, next) => {
    if (!progressOk || interactive !== true) return next(e)
    const args = (e as unknown as Fields).args
    if (typeof args === 'string' && args.trim() === 'retry') return { text: await retryNow($) }
    return { text: disabled ? STOPPED_LINE : await progressNow($) }
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'command.run', next.error)
    return next(e)
  })

  // The precompact row and the automatic run (BEH-35, BEH-36): the measured share, kept or cleared; at or below the run share the
  // skill is started once, as if typed. Only in an interactive session with tracking on and not stopped; both modes.
  on('session.measure', async ($, e, next) => {
    const out = await next(e)
    if (interactive === true && !disabled) {
      try {
        await measured($, (e.context as { percent?: unknown } | undefined)?.percent)
      } catch (err) {
        await recover($, 'session.measure', err)
      }
    }
    return out
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'session.measure', next.error)
    return next(e)
  })

  // A compaction of a run that follows the task list keeps its marked step in the summary and ends with a note asking
  // Claude to bring the list in step (BEH-24). Anything after next(e) is caught here, so the compaction stands.
  on('session.compact', async ($, e, next) => {
    const carried = async () => {
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
    }
    const out = await carried()
    // A compaction of the main conversation (a result with messages, not a skip, and not the one made ahead of time) clears the
    // precompact row's values and the run mark, so the row and the run can happen again (BEH-35).
    if (interactive === true && !disabled && e.agentId === undefined && e.trigger !== 'precompute' && isCompaction(out)) {
      try {
        // A mark no turn.start has bound yet goes with the compaction; a bound one ends at its own turn's complete (version 26).
        await markEndsAtCompaction($)
        await resetPrecompact($)
      } catch (err) {
        await recover($, 'session.compact', err)
      }
    }
    return out
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'session.compact', next.error)
    return next(e)
  })

  // All session.end hooks share 1.5 seconds: run-end first, the last evaluation only if there is room (BEH-05). With
  // paused runs, each one's run-end, bottom first, then the open run's, while the budget has room (version 14).
  on('session.end', async ($, e, next) => {
    try {
      if (await recording($, undefined)) {
        const reason = e.reason === 'clear' ? 'clear' : 'session-end'
        const all = await chained(async () => {
          const trail = (await hydrate($)).trail
          for (const p of trail) {
            if (!hasRoom(next.budget.remainingMs)) return false
            if (p.run !== null) await endPausedNow($, p.run, reason)
          }
          if (trail.length && hasRoom(next.budget.remainingMs)) await adapterLog($, 'trail', `empty (${reason})`)
          if (trail.length && !hasRoom(next.budget.remainingMs)) return false
          await endOpenNow($, reason, hasRoom(next.budget.remainingMs))
          return true
        })
        const run = await get($, 'run')
        if (all && run !== null) await finalEvaluation($, run, finalTimeout(next.budget.remainingMs))
      }
    } finally {
      // The session's values go whatever happened above: /clear, /resume and /branch start a new one (DM-03).
      pendingReport = null
      pendingWrote = []
      lastStatus = undefined
      turnOpen = false
      // The mark's end is logged before the session's values are reset (version 26).
      await markEndsAtSessionEnd($, e.reason).catch(() => undefined)
      live = emptyLive()
      typedName = null
      typedSource = null
      clearMarkMemory()
      // A new session ID follows /clear, /resume and /branch: its lines wait for its first run (DM-02). The holds end with the session
      // (BEH-42 (h)): the open run got its last write above, and what it could not write is dropped.
      const hadHold = runHold !== null || odoHold !== null
      held = null
      runHold = null
      odoHold = null
      odoGaveUp = false  // the ledger's own stop is for the session whose file it was (SPEC-016 ERR-06)
      pendingPrune = null
      if (hadHold) redraw($)
      logRoot = null
      // The pending names (BEH-41) and the ledger's lines (SPEC-016 BEH-10) are the session's; its row and run mark go too.
      starts.clear()
      modLoading.clear()
      ledgerFile = null
      ledgerHeld = []
      await resetPrecompact($).catch(() => undefined)
    }
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
      if (interactive !== true || disabled || props.hasSurvey || rows < 1) return next(e)
      // The band while a run is open (BEH-11), and the precompact row while it is due (BEH-35): the band's row 1, then row 2,
      // then the row, so with too few rows the row goes first. With no run open the row is drawn alone.
      const hasBand = summary !== null && (await read($, RUN)) !== null
      const fuel = precompactRow(await read($, PRECOMPACT), warnFuel, runFuel)
      // The remedy row while a hold lasts (BEH-11, version 27): after the band's rows and before the fuel row, so with too few rows the
      // fuel row goes first and then this one. The holds are in the module's memory; their start and clear redraw the band.
      const view = holdView()
      const remedy = view === null ? null : remedyRow(view, (await read($, MODE)) === 'enforce', progressOk)
      if (!hasBand && fuel === null && remedy === null) return next(e)
      const band = hasBand && summary !== null ? bandRows(summary, await read($, MODE), keptTrail(await read($, TRAIL))) : null
      const width = Math.max(10, props.bodyColumns ?? 80)
      const { Box, Text, Button } = await $.ui.resolve(e)
      const rest = await next(e)
      const left = band === null ? '' : `${band.mode}  `
      const right = band === null ? '' : fit(`  ${band.flag}`, Math.max(0, width - left.length - band.button.length - 4))
      return (
        <Box flexDirection="column">
          {band !== null ? <Text>{fit(band.row1, width)}</Text> : null}
          {band !== null && rows >= 2 ? (
            <Box flexDirection="row">
              <Text>{left}</Text>
              <Button key="progress-mode" label={band.button} onPress={() => {
                void switchMode($)
              }} />
              <Text dimColor>{right}</Text>
            </Box>
          ) : null}
          {remedy !== null && rows >= (band !== null ? 3 : 1) ? <Text>{fit(remedy, width)}</Text> : null}
          {fuel !== null && rows >= (band !== null ? 2 : 0) + (remedy !== null ? 1 : 0) + 1 ? <Text>{fit(fuel, width)}</Text> : null}
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
