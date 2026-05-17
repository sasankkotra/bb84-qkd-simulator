import React from 'react'
import { useSimulationStore } from '../store/simulation'

interface SliderInputProps {
  label: string
  min: number
  max: number
  step: number
  value: number
  onChange: (v: number) => void
  unit?: string
}

export const SliderInput: React.FC<SliderInputProps> = ({
  label,
  min,
  max,
  step,
  value,
  onChange,
  unit = '',
}) => {
  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <label className="text-sm font-semibold text-slate-700">{label}</label>
        <div className="flex items-center gap-2">
          <input
            type="number"
            min={min}
            max={max}
            value={value}
            onChange={(e) => onChange(Math.min(max, Math.max(min, parseFloat(e.target.value) || 0)))}
            className="input-field w-20"
          />
          {unit && <span className="text-xs text-slate-500">{unit}</span>}
        </div>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-cyan-600"
      />
    </div>
  )
}

export const ControlPanel: React.FC = () => {
  const {
    numQubits,
    seed,
    eveActive,
    noiseProbability,
    simulationSpeed,
    setNumQubits,
    setSeed,
    setEveActive,
    setNoiseProbability,
    setSimulationSpeed,
  } = useSimulationStore()

  return (
    <div className="glass p-6 space-y-6">
      <h2 className="text-lg font-bold text-cyan-700">Simulation Controls</h2>

      <SliderInput
        label="Number of Qubits"
        min={1}
        max={10000}
        step={100}
        value={numQubits}
        onChange={setNumQubits}
      />

      <SliderInput
        label="Random Seed"
        min={0}
        max={999999}
        step={1}
        value={seed}
        onChange={setSeed}
      />

      <div className="space-y-2">
        <label className="text-sm font-semibold text-slate-700">Eve Attack</label>
        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={eveActive}
            onChange={(e) => setEveActive(e.target.checked)}
            className="w-5 h-5 accent-cyan-600"
          />
          <span className="text-sm text-slate-600">Enable Eve Interception</span>
        </label>
      </div>

      <SliderInput
        label="Noise Probability"
        min={0}
        max={1}
        step={0.01}
        value={noiseProbability}
        onChange={setNoiseProbability}
      />

      <div className="space-y-2">
        <label className="text-sm font-semibold text-slate-700">Simulation Speed</label>
        <select
          value={simulationSpeed}
          onChange={(e) => setSimulationSpeed(e.target.value as 'Slow' | 'Normal' | 'Fast')}
          className="input-field w-full"
        >
          <option>Slow</option>
          <option>Normal</option>
          <option>Fast</option>
        </select>
      </div>
    </div>
  )
}
