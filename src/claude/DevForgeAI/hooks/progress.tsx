// DevForgeAI's progress tracker adapter for Claude Code (SPEC-013 v2). Skeleton: the hooks arrive in the build's
// later steps.
import type { Register } from 'claude-code'

export const register: Register = on => {
  on('session.start', async ($, e, next) => next(e))
}
