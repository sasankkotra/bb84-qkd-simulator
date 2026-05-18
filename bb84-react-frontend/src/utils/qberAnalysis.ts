// QBER threshold detection logic for BB84 security analysis

export type SecurityLevel = 'secure' | 'warning' | 'compromised' | 'attack'

export interface QberAnalysis {
  level: SecurityLevel
  status: string
  color: 'green' | 'yellow' | 'orange' | 'red'
  description: string
}

export function analyzeQber(qber: number | null): QberAnalysis {
  if (qber === null) {
    return {
      level: 'secure',
      status: 'PENDING',
      color: 'green',
      description: 'Run a simulation to analyze security',
    }
  }

  // QBER < 11%: Secure
  if (qber < 11) {
    return {
      level: 'secure',
      status: 'SECURE CHANNEL',
      color: 'green',
      description: 'QBER below ~11%. Channel is secure. No eavesdropping detected.',
    }
  }

  // QBER 11-15%: Warning/Compromised
  if (qber < 15) {
    return {
      level: 'warning',
      status: 'COMMUNICATION COMPROMISED',
      color: 'orange',
      description: 'QBER at ~11-15%. Communication or channel integrity may be compromised.',
    }
  }

  // QBER 15-25%: Very Compromised
  if (qber < 25) {
    return {
      level: 'compromised',
      status: 'INSECURE CHANNEL',
      color: 'orange',
      description: 'QBER at ~15-25%. Strong indication of eavesdropping or broken channel.',
    }
  }

  // QBER >= 25%: Attack Detected
  return {
    level: 'attack',
    status: 'ATTACK DETECTED',
    color: 'red',
    description: 'QBER above 25%. Severe Eve attack or critical channel failure detected.',
  }
}
