import React from 'react'
import { useSimulationStore } from '../store/simulation'
import { Card, Title, Text, Metric, Badge } from '@tremor/react'
import { analyzeQber } from '../utils/qberAnalysis'

export const ResultsPanel: React.FC = () => {
  const {
    matched,
    total,
    qber,
    securityStatus,
    siftedKeyLength,
    eveDetected,
    errorCount,
  } = useSimulationStore()

  const qberAnalysis = analyzeQber(qber)
  
  const colorMap = {
    green: 'emerald',
    yellow: 'yellow',
    orange: 'orange',
    red: 'rose',
  } as const

  return (
    <Card className="space-y-4">
      <Title>Simulation Results</Title>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <Title className="text-lg">{qberAnalysis.status}</Title>
          <Badge color={colorMap[qberAnalysis.color]} text={qberAnalysis.level.toUpperCase()} />
        </div>
        <Text className="text-sm italic">{qberAnalysis.description}</Text>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Text className="font-semibold">Alice Data</Text>
          <Text>Transmitted {total || 0} qubits</Text>
          <Text>Used random bases for encoding</Text>
        </div>

        <div>
          <Text className="font-semibold">Bob Data</Text>
          <Text>Measured {total || 0} photons</Text>
          <Text>Matched bases: {matched || 0} / {total || 0}</Text>
        </div>
      </div>

      <div>
        <Text className="font-semibold">Security Analysis</Text>
        <div className="grid grid-cols-3 gap-4 mt-2">
          <Card>
            <Title>QBER</Title>
            <Metric>{qber?.toFixed(2) || '--'}%</Metric>
          </Card>
          <Card>
            <Title>Error Count</Title>
            <Metric>{errorCount || 0}</Metric>
          </Card>
          <Card>
            <Title>Sifted Key</Title>
            <Metric>{siftedKeyLength || 0} bits</Metric>
          </Card>
        </div>
      </div>

      {eveDetected && (
        <Card>
          <Text className="text-red-600 font-semibold">⚠️ Eve Attack Detected!</Text>
          <Text>QBER exceeds security threshold. Channel is compromised.</Text>
        </Card>
      )}
    </Card>
  )
}
