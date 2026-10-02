// DevForgeAI's progress tracker adapter for Claude Code (SPEC-013 v3).
//
// It records each run of a tracked skill as SPEC-012's event log, runs SPEC-012's evaluator on a timer, and shows
// the run in the status line, a two-row band above the prompt and toasts. In enforce mode it refuses the write
// gate's Write or Edit when that gate raised flags, and gives the model the report gate's flags. It fails open:
// when it can't run, the work goes on and the user is told (ADR-006 D1). Old run and session folders are pruned
// by progress/prune.py, which the adapter starts once per session and root (BEH-19).
//
// Every use of `$` stays in top-level functions of this file (claude plugin validate's rule); progress-core.ts
// holds the pure helpers.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'
import type { ProgressMode, ProgressModeSource, ProgressRun, ProgressSummary } from '../types'
import {
  bandRows, byteSize, editResult, eventLine, exitOf, finalTimeout, fit, isAnswered, isEngine, isFailed,
  isPersonPrompt, isTracked, keptContent, newFlagToasts, refusalText, replyText, reportContext, retentionOf, runId,
  skillName, statusText, summaryOf, toolPath, FORMAT, IDLE_MS, LOG_LIMIT,
} from './progress-core'
import type { Fields, ProgressState, ToolOutcome } from './progress-core'

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
let turnOpen = false
let disabled = false
let modeSession: string | null = null
// The root the mode was resolved for: the local preference file is per checkout (BEH-16).
let modeRoot: string | null = null
let pluginSkills: string[] | null = null
let lastStatus: string | undefined
let pendingReport: { seq: number; text: string } | null = null
// The open run's event lines: in the module and events.jsonl, since a $.state value holds at most 4,194,304
// characters (see types/index.d.ts); read back from the file after a reload.
let held: { id: string; lines: string[] } | null = null
let allReachedFor: string | null = null
let bandChain: Promise<unknown> = Promise.resolve()
let logChain: Promise<unknown> = Promise.resolve()
let recordChain: Promise<unknown> = Promise.resolve()
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
    const run = await read($, RUN)
    const now = new Date(await $.clock.now()).toISOString().replace(/\.\d{3}Z$/, 'Z')
    const line = `${now} ${run?.id ?? '-'} ${kind}: ${text}\n`
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
  const last = await read($, LAST)
  const idle = !turnOpen && last > 0 && now - last > IDLE_MS
  const text = statusText(await read($, SUMMARY), await read($, MODE), idle, await read($, OFF))
  if (text === lastStatus) return
  lastStatus = text
  await $.ui.status(text)
  if (text !== undefined && !(await hasSurface($))) await $.ui.log(text)
}

/** Tracking can't go on for the session (ERR-03). */
async function stopTracking($: E, reason: string): Promise<void> {
  disabled = true
  await update($, RUN, () => null)
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

/** Write the run's whole log (no append in $.fs); false when it can't be written or would pass 4 MiB. */
async function writeLog($: E, run: ProgressRun, lines: string[]): Promise<boolean> {
  const text = lines.join('\n') + '\n'
  if (byteSize(text) > LOG_LIMIT) {
    await update($, RUN, () => null)
    await update($, OFF, () => LOG_FULL)
    await notify($, `DevForgeAI progress: off (${LOG_FULL})`, `full:${run.id}`)
    await refreshStatus($)
    return false
  }
  try {
    await $.fs.write(`${run.dir}/events.jsonl`, text)
    held = { id: run.id, lines }
    return true
  } catch {
    await stopTracking($, NO_WRITE)
    return false
  }
}

/** Append one event to the open run (BEH-04); `mark` asks the timer to evaluate (BEH-06). Events are recorded one
 *  at a time, so two hooks that overlap can't take the same seq or lose each other's line. */
async function record($: E, kind: string, fields: Fields, mark = true): Promise<void> {
  const step = recordChain.then(() => recordNow($, kind, fields, mark))
  recordChain = step.catch(() => undefined)
  await step
}

async function recordNow($: E, kind: string, fields: Fields, mark: boolean): Promise<void> {
  const run = await read($, RUN)
  if (run === null || disabled) return
  const now = await $.clock.now()
  // The seq comes from the run's own lines: a $.state read inside one dispatch sees that dispatch's moment, so
  // overlapping hooks would read the same seq from it.
  const held = await linesOf($, run)
  const seq = held.length + 1
  const lines = [...held, eventLine(run.id, seq, now, kind, fields)]
  const next: ProgressRun = { ...run, seq }
  if (!(await writeLog($, next, lines))) return
  await update($, RUN, () => next)
  await update($, LAST, () => now)
  if (mark) await update($, MARKED, () => true)
}

async function logBytes($: E): Promise<number> {
  const run = await read($, RUN)
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

/** Take an evaluation in: the session's current.json, the summary, toasts, the report gate's context (BEH-06, BEH-09,
 *  BEH-12). */
async function absorb($: E, run: ProgressRun, got: { state: ProgressState; text: string }): Promise<void> {
  try {
    await $.fs.write(`${await sessionDir($, rootOf(run))}/current.json`, got.text)
  } catch {
    // renderers read current.json; the run's own state.json is written
  }
  const off = await read($, OFF)
  if (off !== null && off !== LOG_FULL && off !== NO_PYTHON && off !== NO_WRITE) await update($, OFF, () => null)
  await update($, SUMMARY, () => summaryOf(got.state))
  const shown = await read($, SHOWN)
  const fresh = newFlagToasts(got.state, shown)
  if (fresh.keys.length) await update($, SHOWN, () => [...shown, ...fresh.keys])
  for (const toast of fresh.toasts) await notify($, toast)
  if (got.state.current === null && got.state.ended === null && allReachedFor !== run.id) {
    allReachedFor = run.id
    await notify($, `✓ ${got.state.skill}: all steps reached`)
  }
  const report = reportContext(got.state)
  const sent = await read($, SENT)
  pendingReport = report !== null && !sent.includes(report.seq) && got.state.ended === null ? report : null
  await refreshStatus($)
}

/** The timer's work (BEH-06): it catches every error itself, since one it let escape reaches only the debug log (ERR-10). */
async function tick($: E): Promise<void> {
  try {
    await refreshStatus($)
    if (evaluating || disabled || !(await read($, MARKED))) return
    const run = await read($, RUN)
    if (run === null) return
    evaluating = true
    try {
      await update($, MARKED, () => false)
      // The folder's .gitignore may have gone with a `git clean` while the run went on (BEH-15).
      await ensureIgnore($, rootOf(run)).catch(() => undefined)
      const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, EVALUATOR_TIMEOUT)
      const open = await read($, RUN)
      // A run that opened while the evaluator ran keeps its own summary and flags.
      if (open === null || open.id !== run.id) return
      if (typeof got === 'string') await failOpen($, got)
      else await absorb($, run, got)
    } finally {
      evaluating = false
    }
  } catch (err) {
    await failOpen($, `timer: ${message(err)}`).catch(() => undefined)
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
  const run = await read($, RUN)
  if (run !== null) {
    // After a reload the module's variables start over; the open run's folder exists, so its log goes there.
    await useLogRoot($, rootOf(run))
    await update($, MARKED, () => true)
  }
}

/** Open a run for a tracked skill in the root read as it loaded (BEH-03). */
async function openRun($: E, r: string, skill: string, checklist: string): Promise<void> {
  if (!(await ensureDir($, r))) return
  // The mode is resolved here, after the folder exists, so a new root's mode line lands in that root's log (BEH-16).
  if (modeSession !== (await $.session.id()) || modeRoot !== r) await resolveMode($, r)
  const now = await $.clock.now()
  const id = runId(now, skill, crypto.getRandomValues(new Uint8Array(4)))
  const dir = `${progressDir(r)}/runs/${id}`
  const version = await $.session.version()
  const line = eventLine(id, 1, now, 'skill-loaded', {
    format: FORMAT, skill, checklist, host: `claude-code ${version.version}`,
    mode: await read($, MODE), modeSource: await read($, SOURCE),
  })
  const run: ProgressRun = { id, skill, seq: 1, dir, root: r }
  if (!(await writeLog($, run, [line]))) return
  await update($, RUN, () => run)
  await update($, LAST, () => now)
  await update($, MARKED, () => true)
  await update($, SUMMARY, () => null)
  await update($, SHOWN, () => [])
  await update($, SENT, () => [])
  if ((await read($, OFF)) === LOG_FULL) await update($, OFF, () => null)
  pendingReport = null
  await startPrune($, r, id)
}

/** Prune old run and session folders once per session ID and root, after the run's folder exists; nothing waits
 *  for it, and its result or failure goes to adapter.log only (BEH-19, ERR-12). */
async function startPrune($: E, r: string, keepRun: string): Promise<void> {
  if (!python) return
  const session = await $.session.id()
  const key = `${session}\n${r}`
  if (pruned.has(key)) return
  pruned.add(key)
  const argv = [python, `${$.plugin.root}/progress/prune.py`, 'prune', '--root', r, '--days', String(retentionDays),
    '--keep-session', session, '--keep-run', keepRun]
  void $.process.run(argv, { cwd: r, timeoutMs: PRUNE_TIMEOUT }).then(
    res => adapterLog($, 'prune', res.exitCode === 0 ? firstLine(res.stdout) : firstLine(res.stderr) || `exit ${res.exitCode}`),
    err => adapterLog($, 'prune', firstLine(message(err))),
  ).catch(() => undefined)
}

/** End the open run, and evaluate it once more when there is time (BEH-05). */
async function endRun($: E, reason: string, timeoutMs: number | null): Promise<void> {
  await record($, 'run-end', { reason })
  pendingReport = null
  const run = await read($, RUN)
  if (run === null || timeoutMs === null || !python) return
  await update($, MARKED, () => false)
  const got = await evaluate($, rootOf(run), `${run.dir}/events.jsonl`, `${run.dir}/state.json`, timeoutMs)
  if (typeof got !== 'string') await absorb($, run, got)
}

/** Enforce mode's write-gate check (BEH-08): the refusal text, or null to let the call go on. */
async function enforceCheck($: E, fields: Fields, content: string | null): Promise<string | null> {
  const run = await read($, RUN)
  if (run === null) return null
  const seq = (await linesOf($, run)).length + 1
  const line = eventLine(run.id, seq, await $.clock.now(), 'tool', {
    ...fields, exit: 0, error: false, content: keptContent(content, await logBytes($)),
  })
  try {
    await $.fs.write(`${run.dir}/pending.jsonl`, [...(await linesOf($, run)), line].join('\n') + '\n')
  } catch {
    return null
  }
  const got = await evaluate($, rootOf(run), `${run.dir}/pending.jsonl`, `${run.dir}/pending.json`, EVALUATOR_TIMEOUT)
  if (typeof got === 'string') {
    await failOpen($, got)
    return null
  }
  return refusalText(got.state, seq)
}

/** The band's button: save the other mode with settings.py (IF-02, BEH-13). */
async function switchMode($: E): Promise<void> {
  const target: ProgressMode = (await read($, MODE)) === 'enforce' ? 'observe' : 'enforce'
  if (!python) {
    await notify($, `DevForgeAI progress: couldn't save progress.mode (${NO_PYTHON})`)
    return
  }
  const open = await read($, RUN)
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
  const run = await read($, RUN)
  await adapterLog($, 'switch', `${target} (local), at seq ${run?.seq ?? 0}`)
  await notify($, `DevForgeAI progress: ${target} mode, saved to .claude/devforgeai.local.md`)
  await refreshStatus($)
}

async function recording($: E, agentId: unknown): Promise<boolean> {
  return interactive === true && !disabled && agentId === undefined && (await read($, RUN)) !== null
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
      if ((await read($, RUN)) !== null) await endRun($, 'another-skill', EVALUATOR_TIMEOUT)
      await openRun($, r, name, out.text)
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
    const input = e as unknown as Fields
    if (!(await recording($, input.agentId))) return next(e)
    const tool = String(input.tool)
    if (tool === 'AskUserQuestion') {
      const result = await next(e)
      try {
        // A mod's $.ui.ask arrives here too; only Claude Code's own question is the user's answer (BEH-04).
        if (isEngine(next.origin)) await record($, 'answer', { answered: isAnswered(result as unknown as ToolOutcome) })
      } catch (err) {
        await recover($, 'tool.call', err)
      }
      return result
    }
    const open = await read($, RUN)
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
        await record($, 'tool', { ...fields, exit: null, error: true, content: keptContent(content, await logBytes($)) })
        await adapterLog($, 'refused', firstLine(refusal.split('\n')[1] ?? refusal))
        if (!(await hasSurface($))) await $.ui.log(refusal)
        return { deny: refusal }
      }
    }
    const result = await next(e)
    try {
      const outcome = result as unknown as ToolOutcome
      await record($, 'tool', {
        ...fields, exit: exitOf(outcome), error: isFailed(outcome), content: keptContent(content, await logBytes($)),
      })
    } catch (err) {
      await recover($, 'tool.call', err)
    }
    return result
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
      const sent = await read($, SENT)
      await update($, SENT, () => [...sent, report.seq])
      await adapterLog($, 'context', `report gate at seq ${report.seq}`)
      return next({ ...e, context: [...(e.context ?? []), report.text] })
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'prompt.submit', next.error)
    return next(e)
  })

  on('turn.start', async ($, e, next) => {
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
    if (await recording($, e.agentId)) {
      turnOpen = false
      await record($, 'turn', { phase: 'end' }, false)
    }
    return next(e)
  }).catch(async ($, e, next) => {
    if (!next.called) await recover($, 'turn.complete', next.error)
    return next(e)
  })

  // All session.end hooks share 1.5 seconds: run-end first, the last evaluation only if there is room (BEH-05).
  on('session.end', async ($, e, next) => {
    if (await recording($, undefined)) {
      await endRun($, e.reason === 'clear' ? 'clear' : 'session-end', finalTimeout(next.budget.remainingMs))
    }
    pendingReport = null
    lastStatus = undefined
    turnOpen = false
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
      const band = bandRows(summary, await read($, MODE))
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
