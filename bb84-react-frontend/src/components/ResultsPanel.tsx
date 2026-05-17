import React from 'react'
import { useSimulationStore } from '../store/simulation'
import { Card, Title, Text, Metric, Badge } from '@tremor/react'

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

  const statusText = securityStatus || 'PENDING'

  return (
    <Card className="space-y-4">
      <Title>Simulation Results</Title>

      <div className="flex items-center justify-between">
        <Metric>{statusText}</Metric>
        <Badge color={qber && qber > 11 ? 'red' : 'green'} text={qber && qber > 11 ? 'Compromised' : 'Secure'} />
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
