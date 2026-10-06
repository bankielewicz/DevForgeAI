export type Look = 'A' | 'B' | 'C'

declare module 'claude-code' {
  interface PluginState {
    'dashboard-probe': {
      theme: Look
      character: string
      isAnimating: boolean
      trackMode: 'enforce' | 'observe'
      note: string
      rpmNote: string
    }
  }
}
