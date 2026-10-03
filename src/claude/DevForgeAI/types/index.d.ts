// The progress tracker adapter's $.state contract (SPEC-013 v5 DM-03). $.state survives a reload of the module
// and empties on /clear, /resume and /branch; whether the session is interactive and the evaluation timer are
// module variables instead (BEH-01, BEH-06).

/** The open run: its ID, skill, the last seq used, its folder under devforgeai/progress/runs/, and the root it
 *  opened in, which its paths, manifests and files use (BEH-03). Its event lines
 *  live in the module and events.jsonl, not here: one $.state value holds at most 4,194,304 characters, which a
 *  run's lines can pass before the log reaches its 4 MiB (found by the build's ERR-11 test). */
export type ProgressRun = {
  id: string
  skill: string
  seq: number
  dir: string
  root: string
}

/** What the status line and the band draw, taken from the last evaluation (SPEC-012 DM-03). */
export type ProgressSummary = {
  skill: string
  current: number | null
  steps: number
  flags: number
  yourTurn: boolean
  ended: string | null
  manifest: 'matched' | 'stale' | 'none' | 'unverified'
  states: string[]
  currentTitle: string | null
  lastFlag: string | null
}

export type ProgressMode = 'observe' | 'enforce'

export type ProgressModeSource = 'framework-default' | 'local'

declare module 'claude-code' {
  interface PluginState {
    devforgeai: {
      run: ProgressRun | null
      mode: ProgressMode
      modeSource: ProgressModeSource
      summary: ProgressSummary | null
      lastEventAt: number
      marked: boolean
      shown: string[]
      contextSent: number[]
      off: string | null
      /** The open run's task IDs and their step numbers (BEH-20); a new run starts empty. */
      tasks: Record<string, number>
      /** TodoWrite: each step's last status, by step number (BEH-20). */
      todos: Record<string, string>
      /** The task-tools hint was shown this session (BEH-23). */
      hinted: boolean
    }
  }
}
