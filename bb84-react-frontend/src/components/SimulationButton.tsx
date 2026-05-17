import React, { useState } from 'react'
import { useSimulationStore } from '../store/simulation'
import { runLocalSimulation } from '../sim/bb84'

export const SimulationButton: React.FC = () => {
  const {
    numQubits,
    seed,
    eveActive,
    noiseProbability,
    isRunning,
    progress,
    setRunning,
    setProgress,
    setResults,
    reset,
  } = useSimulationStore()

  const [error, setError] = useState<string | null>(null)

  const handleRun = async () => {
    setError(null)
    setRunning(true)
    setProgress(0)

    try {
      // Run local simulation and animate progress
      const progressSteps = 6
      for (let i = 1; i <= progressSteps; i++) {
        // small delay to show progress
        // faster when fewer qubits or Fast speed could be implemented later
        await new Promise((res) => setTimeout(res, 80))
        setProgress((i / progressSteps) * 90)
      }

      const result = runLocalSimulation({
        num_qubits: numQubits,
        eve_active: eveActive,
        noise_prob: noiseProbability,
        seed: seed,
      })

      // finalize progress
      setProgress(100)
      setResults({
        qber: result.qber,
        matched: result.matched,
        total: result.total,
        securityStatus: result.eve_detected ? 'Eve detected' : 'No eavesdropper detected',
        siftedKeyLength: result.sifted,
        eveDetected: result.eve_detected,
        errorCount: result.error_count,
        aliceBits: result.alice_bits,
        bobBits: result.bob_bits,
        matchedIndices: result.matched_indices,
        progress: 100,
      })
      setRunning(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Simulation failed')
      setRunning(false)
    }
  }

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-300 rounded-lg p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {isRunning && (
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-semibold text-slate-700">Simulation Progress</span>
            <span className="text-sm text-slate-500">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <button onClick={handleRun} disabled={isRunning} className="btn-primary disabled:opacity-50">
          {isRunning ? 'Running...' : 'Run Simulation'}
        </button>
        <button
          onClick={reset}
          disabled={isRunning}
          className="btn-secondary disabled:opacity-50"
        >
          Reset
        </button>
      </div>
    </div>
  )
}
