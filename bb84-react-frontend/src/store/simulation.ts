import { create } from 'zustand'

export interface SimState {
  // Parameters
  numQubits: number
  seed: number
  eveActive: boolean
  noiseProbability: number
  simulationSpeed: 'Slow' | 'Normal' | 'Fast'
  
  // Results
  qber: number | null
  matched: number | null
  total: number | null
  securityStatus: string | null
  siftedKeyLength: number | null
  aliceBits: number[] | null
  bobBits: number[] | null
  matchedIndices: number[] | null
  eveDetected: boolean | null
  errorCount: number | null
  isRunning: boolean
  progress: number
  
  // Actions
  setNumQubits: (n: number) => void
  setSeed: (s: number) => void
  setEveActive: (e: boolean) => void
  setNoiseProbability: (n: number) => void
  setSimulationSpeed: (s: 'Slow' | 'Normal' | 'Fast') => void
  setRunning: (r: boolean) => void
  setProgress: (p: number) => void
  setResults: (results: Partial<SimState>) => void
  reset: () => void
}

const initialState = {
  numQubits: 1000,
  seed: 42,
  eveActive: false,
  noiseProbability: 0.05,
  simulationSpeed: 'Normal' as const,
  qber: null,
  matched: null,
  total: null,
  securityStatus: null,
  siftedKeyLength: null,
  aliceBits: null,
  bobBits: null,
  matchedIndices: null,
  eveDetected: null,
  errorCount: null,
  isRunning: false,
  progress: 0,
}

export const useSimulationStore = create<SimState>((set) => ({
  ...initialState,
  
  setNumQubits: (n) => set({ numQubits: n }),
  setSeed: (s) => set({ seed: s }),
  setEveActive: (e) => set({ eveActive: e }),
  setNoiseProbability: (n) => set({ noiseProbability: n }),
  setSimulationSpeed: (s) => set({ simulationSpeed: s }),
  setRunning: (r) => set({ isRunning: r }),
  setProgress: (p) => set({ progress: Math.min(100, p) }),
  
  setResults: (results) => set((state) => ({ ...state, ...results })),
  
  reset: () => set(initialState),
}))
