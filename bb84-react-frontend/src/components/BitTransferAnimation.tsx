import React from 'react'
import { useSimulationStore } from '../store/simulation'

const MAX_DISPLAY = 64

export const BitTransferAnimation: React.FC = () => {
  const { aliceBits, bobBits, matchedIndices, isRunning, progress } = useSimulationStore()

  const bits = aliceBits || []
  const bob = bobBits || []
  const matched = new Set(matchedIndices || [])

  const displayCount = Math.min(bits.length, MAX_DISPLAY)

  // create an array of indexes to display
  const idx = Array.from({ length: displayCount }, (_, i) => i)

  return (
    <div className="w-full my-6">
      <div className="flex items-center justify-between mb-2">
        <div className="text-sm font-medium text-slate-600">Alice</div>
        <div className="text-sm font-medium text-slate-600">Channel</div>
        <div className="text-sm font-medium text-slate-600">Bob</div>
      </div>

      <div className="relative h-12 overflow-hidden">
        {idx.map((i) => {
          const bit = bits[i]
          const bobBit = bob[i]
          const isMatch = matched.has(i)
          const left = `${(i / displayCount) * 100}%`
          const delay = `${i * 30}ms`

          const color = isMatch ? 'bg-green-500' : 'bg-red-500'

          return (
            <div
              key={i}
              style={{ left }}
              className={`absolute top-0 w-6 h-6 rounded-full flex items-center justify-center text-white ${color} animate-transfer`} 
              role="img"
              aria-label={`bit-${i}`} 
              title={`Alice:${bit} → Bob:${bobBit} ${isMatch ? 'match' : 'mismatch'}`} 
            >
              <span className="text-xs font-mono">{bit}</span>
              <style>{`
                .animate-transfer{
                  transform: translateX(0);
                  animation: move-${i} 1500ms linear ${delay} forwards;
                }
                @keyframes move-${i} {
                  0% { transform: translateX(0); opacity: 1 }
                  70% { transform: translateX(300%); opacity: 1 }
                  100% { transform: translateX(600%); opacity: ${isRunning ? 0.2 : 1} }
                }
              `}</style>
            </div>
          )
        })}
      </div>

      <div className="mt-3 text-xs text-slate-500">Progress: {Math.round(progress)}%</div>
    </div>
  )
}
