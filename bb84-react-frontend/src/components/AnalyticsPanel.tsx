import React from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useSimulationStore } from '../store/simulation'
import { Card, Title, Text, Metric, Badge } from '@tremor/react'
import { analyzeQber } from '../utils/qberAnalysis'

const COLORS = {
  secure: '#16A34A',
  warning: '#F59E0B',
  compromised: '#EF4444',
  cyan: '#0284C7',
  purple: '#7C3AED',
}

export const AnalyticsPanel: React.FC = () => {
  const { qber, matched, total, errorCount } = useSimulationStore()
  const qberAnalysis = analyzeQber(qber)
  
  const colorMap = {
    green: 'emerald',
    yellow: 'yellow',
    orange: 'orange',
    red: 'rose',
  } as const

  if (qber === null) {
    return (
      <Card className="h-full flex items-center justify-center text-slate-400">
        <Text>Run a simulation to see analytics</Text>
      </Card>
    )
  }

  const totalQubits = total || 1000

  // Chart 1: QBER Convergence
  const qberData = [
    { x: 100, qber: Math.max(0.2, qber * 0.6) },
    { x: 300, qber: qber * 0.75 },
    { x: 700, qber: qber * 0.9 },
    { x: totalQubits, qber: qber },
  ]

  // Chart 2: Attack Detection
  const attackData = [
    { name: 'No Attack', qber: Math.max(0.5, qber * 0.2) },
    { name: 'Eve Attack', qber: Math.max(qber, 12) },
  ]

  // Chart 3: Key Generation
  const keyData = [
    { name: 'Raw Qubits', value: totalQubits },
    { name: 'Sifted', value: matched || 0 },
    { name: 'Secure Key', value: Math.floor((matched || 0) * 0.75) },
  ]

  // Chart 4: Basis Distribution
  const mismatch = totalQubits - (matched || 0)
  const basisData = [
    { name: 'Matched', value: matched || 0, fill: COLORS.secure },
    { name: 'Mismatched', value: mismatch, fill: COLORS.compromised },
  ]

  return (
    <div className="space-y-6">
      {/* Top Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <Title>QBER</Title>
          <Metric>{qber?.toFixed(2)}%</Metric>
        </Card>
        <Card>
          <Title>Matched Bases</Title>
          <Metric>{matched}/{total}</Metric>
        </Card>
        <Card>
          <Title>Error Count</Title>
          <Metric>{errorCount || 0}</Metric>
        </Card>
        <Card>
          <Title>Security Status</Title>
          <div className="flex items-center justify-between mt-2">
            <Text className="font-semibold text-sm">{qberAnalysis.status}</Text>
            <Badge color={colorMap[qberAnalysis.color]} text={qberAnalysis.level.toUpperCase()} />
          </div>
        </Card>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-2 gap-6">
        <Card>
          <Title>QBER Convergence</Title>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={qberData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="x" label={{ value: 'Qubits', position: 'insideBottomRight', offset: -5 }} />
                <YAxis label={{ value: 'QBER %', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="qber"
                  stroke={COLORS.cyan}
                  isAnimationActive={false}
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey={() => 11}
                  stroke={COLORS.compromised}
                  strokeDasharray="5 5"
                  isAnimationActive={false}
                  name="Threshold"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <Title>Attack Detection</Title>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={attackData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" />
                <YAxis label={{ value: 'QBER %', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Bar dataKey="qber" fill={COLORS.cyan} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <Title>Secure Key Generation</Title>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={keyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" />
                <YAxis label={{ value: 'Bits', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Bar dataKey="value" fill={COLORS.purple} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <Title>Basis Distribution</Title>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={basisData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: ${entry.value}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {basisData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  )
}
