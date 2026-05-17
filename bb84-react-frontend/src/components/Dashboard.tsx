import React from 'react'
import { ControlPanel } from './ControlPanel'
import { SimulationButton } from './SimulationButton'
import { AnalyticsPanel } from './AnalyticsPanel'
import { ResultsPanel } from './ResultsPanel'
import { BitTransferAnimation } from './BitTransferAnimation'

export const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold gradient-text">BB84 Quantum Key Distribution</h1>
              <p className="text-slate-500 text-sm mt-1">Secure Quantum Communication Analysis Dashboard</p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-semibold text-slate-700" id="clock">
                --:--:--
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Bit transfer animation */}
        <div className="max-w-7xl mx-auto px-6">
          <BitTransferAnimation />
        </div>

        <div className="grid grid-cols-3 gap-8">
          {/* Left Panel - Controls */}
          <div className="space-y-6">
            <ControlPanel />
            <SimulationButton />
          </div>

          {/* Center Panel - Analytics */}
          <div className="col-span-2">
            <AnalyticsPanel />
          </div>
        </div>

        {/* Bottom Results Panel */}
        <div className="mt-8 grid grid-cols-3 gap-8">
          <ResultsPanel />
          <div className="col-span-2" />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-sm text-slate-500">
          <p>BB84 QKD Simulator © 2026 | Quantum Security Research</p>
        </div>
      </footer>

      <script>{`
        setInterval(() => {
          const now = new Date();
          document.getElementById('clock').textContent = now.toLocaleTimeString();
        }, 1000);
      `}</script>
    </div>
  )
}
