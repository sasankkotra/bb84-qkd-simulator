import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface SimulationParams {
  num_qubits: number
  eve_active: boolean
  noise_prob: number
  seed: number
}

export interface SimulationResult {
  qber: number
  matched: number
  total: number
  security_status: string
  sifted: number
  eve_detected: boolean
  error_count: number
}

export const simulateStream = async (params: SimulationParams, onProgress: (data: any) => void) => {
  try {
    const queryParams = new URLSearchParams({
      num_qubits: params.num_qubits.toString(),
      eve_active: params.eve_active.toString(),
      noise_prob: params.noise_prob.toString(),
      seed: params.seed.toString(),
    })

    const response = await fetch(`${API_BASE}/simulate/stream?${queryParams}`, {
      method: 'GET',
    })

    if (!response.ok) throw new Error('Simulation failed')

    const reader = response.body?.getReader()
    if (!reader) return

    const decoder = new TextDecoder()
    let eventType = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('event:')) {
          eventType = line.slice(6).trim()
        } else if (line.startsWith('data:') && eventType) {
          const data = line.slice(5).trim()
          if (data) {
            try {
              const parsed = JSON.parse(data)
              onProgress({ type: eventType, data: parsed })
            } catch (e) {
              // Ignore parse errors
            }
          }
        }
      }
    }
  } catch (error) {
    console.error('Simulation error:', error)
    throw error
  }
}

export default api
