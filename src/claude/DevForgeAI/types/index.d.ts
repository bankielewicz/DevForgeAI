// The progress tracker adapter's $.state contract (SPEC-013 DM-03). $.state survives a reload of the module
// and empties on /clear, /resume and /branch; whether the session is interactive and the evaluation timer are
// module variables instead (BEH-01, BEH-06).

/** The open run: its ID, the last seq used, its event lines (DM-01) and its folder under devforgeai/progress/runs/. */
export type ProgressRun = {
  id: string
  skill: string
  seq: number
  lines: string[]
  dir: string
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
    }
  }
}
