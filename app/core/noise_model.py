"""
Noise Model module for BB84 QKD.

Simulates realistic channel noise in quantum transmission.
"""

import numpy as np
from dataclasses import dataclass
from typing import List
from app.core.qubit import Qubit


@dataclass
class NoiseStats:
    """Statistics about noise in transmission."""
    total_bits: int
    flipped_bit_count: int
    flip_percentage: float


def apply_channel_noise(
    qubits: List[Qubit],
    noise_probability: float
) -> tuple:
    """
    Apply random bit flip noise to qubits during transmission.
    
    Simulates:
    - Environmental disturbances
    - Detector imperfections
    - Fiber optic losses
    - Spontaneous emission
    
    Each qubit has independent probability of bit flip.
    
    Args:
        qubits: List of qubits to apply noise to
        noise_probability: Probability of bit flip for each qubit (0 to 1)
        
    Returns:
        Tuple of (noisy_qubits, noise_stats)
    """
    noisy_qubits = []
    flipped_positions = []
    
    for i, qubit in enumerate(qubits):
        if np.random.rand() < noise_probability:
            # Flip the bit
            noisy_qubit = Qubit(1 - qubit.bit, qubit.basis)
            noisy_qubits.append(noisy_qubit)
            flipped_positions.append(i)
        else:
            # No noise, qubit unchanged
            noisy_qubits.append(Qubit(qubit.bit, qubit.basis))
    
    flip_count = len(flipped_positions)
    flip_percentage = (flip_count / len(qubits) * 100) if len(qubits) > 0 else 0
    
    stats = NoiseStats(
        total_bits=len(qubits),
        flipped_bit_count=flip_count,
        flip_percentage=flip_percentage
    )
    
    return noisy_qubits, stats


def estimate_qber_from_noise(
    noise_probability: float,
    intercept_rate: float = 0.0
) -> float:
    """
    Estimate expected QBER contribution from noise and Eve.
    
    Theory:
    - Pure noise: ~noise_probability (bit flip occurs randomly)
    - Eve intercept-resend: ~12.5% per intercepted qubit
    - Combined: roughly additive for low values
    
    Args:
        noise_probability: Channel noise bit flip probability
        intercept_rate: Fraction of qubits Eve intercepts (0 to 1)
        
    Returns:
        Estimated QBER percentage
    """
    # Noise contribution
    noise_qber = noise_probability * 100
    
    # Eve contribution (if present)
    eve_qber = intercept_rate * 12.5  # ~12.5% QBER per full intercept
    
    # Combined (approximate)
    combined_qber = noise_qber + eve_qber
    
    return min(50.0, combined_qber)  # Cap at 50%


def compare_noise_levels(
    noise_levels: List[float],
    base_qber: float = 0.5
) -> dict:
    """
    Compare expected QBER at different noise levels.
    
    Args:
        noise_levels: List of noise probabilities to test
        base_qber: Base QBER from quantum measurement (typically 0.5%)
        
    Returns:
        Dictionary with noise level comparisons
    """
    comparison = {}
    
    for noise_prob in noise_levels:
        expected_qber = base_qber + (noise_prob * 100)
        is_secure = expected_qber < 11.0
        
        comparison[f"noise_{noise_prob:.2%}"] = {
            'noise_probability': noise_prob,
            'expected_qber_percent': expected_qber,
            'secure': is_secure
        }
    
    return comparison


def analyze_noise_source(
    measured_qber: float,
    expected_eve_qber: float = 12.5
) -> dict:
    """
    Analyze whether observed QBER is from noise or Eve.
    
    Args:
        measured_qber: Observed QBER percentage
        expected_eve_qber: Expected QBER if Eve present (~12.5%)
        
    Returns:
        Analysis dictionary
    """
    # Baseline is ~0-1% from quantum measurement
    baseline_qber = 1.0
    
    # If QBER is below ~5%, likely just measurement noise
    if measured_qber < 5:
        source = "MEASUREMENT_NOISE"
    # If QBER is 5-11%, could be channel noise
    elif measured_qber < 11:
        source = "CHANNEL_NOISE"
    # If QBER > 11%, likely Eve or severe channel issues
    else:
        source = "EVE_OR_SEVERE_NOISE"
    
    return {
        'measured_qber': measured_qber,
        'probable_source': source,
        'eve_likelihood': max(0, (measured_qber - 1) / 12.5),
        'recommendation': 'ABORT_COMMUNICATION' if source == "EVE_OR_SEVERE_NOISE" else 'PROCEED'
    }
