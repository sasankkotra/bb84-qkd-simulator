// Client-side BB84 simulation engine (TypeScript)

export type SimParams = {
  num_qubits: number
  eve_active: boolean
  noise_prob: number
  seed?: number | null
}

export type SimResult = {
  qber: number
  matched: number
  total: number
  sifted: number
  eve_detected: boolean
  error_count: number
  alice_bits: number[]
  bob_bits: number[]
  matched_indices: number[]
}

// Simple seeded RNG (Mulberry32)
function mulberry32(a: number) {
  return function () {
    let t = (a += 0x6d2b79f5)
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

export function runLocalSimulation(params: SimParams): SimResult {
  const { num_qubits, eve_active, noise_prob, seed } = params
  const rand = seed != null ? mulberry32(seed) : Math.random

  // Generate Alice bits and bases
  const alice_bits: number[] = new Array(num_qubits).fill(0).map(() => (rand() < 0.5 ? 0 : 1))
  const alice_bases: number[] = new Array(num_qubits).fill(0).map(() => (rand() < 0.5 ? 0 : 1)) // 0: +, 1: x

  // Prepare transmitted qubits as ideal bits with bases
  let transmitted_bits = alice_bits.slice()
  let transmitted_bases = alice_bases.slice()

  let eve_detected = false

  // Eve intercept-resend: measure in random basis and resend (introduces errors when bases mismatch)
  if (eve_active) {
    for (let i = 0; i < num_qubits; i++) {
      const eve_basis = rand() < 0.5 ? 0 : 1
      // If Eve basis != Alice basis, measurement may flip with 50% chance
      if (eve_basis !== alice_bases[i]) {
        transmitted_bits[i] = rand() < 0.5 ? 0 : 1
      } else {
        transmitted_bits[i] = alice_bits[i]
      }
    }
    eve_detected = true
  }

  // Apply channel noise: flip bits with probability noise_prob
  for (let i = 0; i < num_qubits; i++) {
    if (rand() < noise_prob) {
      transmitted_bits[i] = transmitted_bits[i] === 0 ? 1 : 0
    }
  }

  // Bob measures with his own random bases
  const bob_bases: number[] = new Array(num_qubits).fill(0).map(() => (rand() < 0.5 ? 0 : 1))
  const bob_measurements: number[] = new Array(num_qubits).fill(0)

  for (let i = 0; i < num_qubits; i++) {
    // If Bob chooses same basis as the transmission base, he gets the bit
    if (bob_bases[i] === transmitted_bases[i]) {
      bob_measurements[i] = transmitted_bits[i]
    } else {
      // If basis mismatch, measurement is random
      bob_measurements[i] = rand() < 0.5 ? 0 : 1
    }
  }

  // Sifting: positions where Alice and Bob bases match
  const matched_indices: number[] = []
  for (let i = 0; i < num_qubits; i++) {
    if (alice_bases[i] === bob_bases[i]) matched_indices.push(i)
  }

  const sifted_key = matched_indices.map((i) => alice_bits[i])
  const bob_sifted = matched_indices.map((i) => bob_measurements[i])

  // QBER: percentage of mismatches in sifted key
  let error_count = 0
  for (let i = 0; i < sifted_key.length; i++) {
    if (sifted_key[i] !== bob_sifted[i]) error_count++
  }
  const qber = sifted_key.length > 0 ? (error_count / sifted_key.length) * 100 : 0

  const result: SimResult = {
    qber: Number(qber.toFixed(4)),
    matched: matched_indices.length,
    total: num_qubits,
    sifted: sifted_key.length,
    eve_detected,
    error_count,
    alice_bits: alice_bits.slice(0, 128),
    bob_bits: bob_measurements.slice(0, 128),
    matched_indices: matched_indices.slice(0, 128),
  }

  return result
}
