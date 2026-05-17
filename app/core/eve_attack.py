"""
Eve Attack module for BB84 QKD.

Simulates Eve's intercept-resend eavesdropping attack.
"""

import numpy as np
from dataclasses import dataclass
from typing import List
from app.core.qubit import Qubit


@dataclass
class EveAttackStats:
    """Statistics about Eve's attack."""
    qubits_intercepted: int
    correct_basis_count: int
    incorrect_basis_count: int
    introduced_errors: int
    error_rate_percentage: float


def perform_eve_attack(
    qubits: List[Qubit],
    intercept_probability: float = 1.0
) -> tuple:
    """
    Simulate Eve's intercept-resend attack on BB84.
    
    Eve:
    1. Intercepts a qubit
    2. Randomly chooses a basis (50-50 chance)
    3. Measures the qubit
    4. Resends based on her measurement
    
    If Eve chooses wrong basis (50% chance), she collapses the qubit
    to a random state, introducing errors detectable via QBER.
    
    Args:
        qubits: List of qubits from Alice
        intercept_probability: Fraction to intercept (0 to 1)
        
    Returns:
        Tuple of (eve_modified_qubits, eve_bases, eve_measurements, attack_stats)
    """
    eve_bases = []
    eve_measurements = []
    eve_modified = []
    
    correct_basis_count = 0
    incorrect_basis_count = 0
    
    for i, qubit in enumerate(qubits):
        if np.random.rand() < intercept_probability:
            # Eve chooses random basis
            eve_basis = np.random.randint(0, 2)
            eve_bases.append(eve_basis)
            
            # Eve measures in her chosen basis
            eve_measurement = qubit.measure(eve_basis)
            eve_measurements.append(eve_measurement)
            
            # Track basis match
            if eve_basis == qubit.basis:
                correct_basis_count += 1
            else:
                incorrect_basis_count += 1
            
            # Eve resends based on her measurement
            eve_modified.append(Qubit(eve_measurement, eve_basis))
        else:
            # Eve doesn't intercept this qubit
            eve_bases.append(-1)
            eve_measurements.append(-1)
            eve_modified.append(qubit)
    
    qubits_intercepted = sum(1 for b in eve_bases if b != -1)
    
    # Errors introduced when Eve uses wrong basis
    # Expected: ~12.5% error rate when Eve intercepts (50% wrong basis * 50% measurement error)
    introduced_errors = incorrect_basis_count // 2  # Rough estimate
    error_rate = (introduced_errors / len(qubits) * 100) if len(qubits) > 0 else 0
    
    stats = EveAttackStats(
        qubits_intercepted=qubits_intercepted,
        correct_basis_count=correct_basis_count,
        incorrect_basis_count=incorrect_basis_count,
        introduced_errors=introduced_errors,
        error_rate_percentage=error_rate
    )
    
    return eve_modified, eve_bases, eve_measurements, stats


def detect_eve_from_qber(qber_percentage: float, threshold: float = 11.0) -> tuple:
    """
    Attempted detection of Eve based on QBER.
    
    Theory:
    - No Eve, no noise: QBER ~0%
    - No Eve, with noise: QBER ~5% (depends on channel noise)
    - With Eve: QBER ~12.5% (50% wrong basis * 50% measurement error)
    
    Threshold: If QBER > 11%, likely Eve present.
    
    Args:
        qber_percentage: Measured QBER
        threshold: QBER threshold for Eve detection
        
    Returns:
        Tuple of (eve_detected, confidence)
    """
    if qber_percentage > threshold:
        # Eve likely detected
        # Confidence increases with QBER above threshold
        confidence = min(1.0, (qber_percentage - threshold) / 10.0)
        return True, confidence
    return False, 0.0


def analyze_eve_impact(
    qber_without_eve: float,
    qber_with_eve: float
) -> dict:
    """
    Analyze the impact of Eve's attack on QBER.
    
    Args:
        qber_without_eve: QBER in normal channel
        qber_with_eve: QBER with Eve attacking
        
    Returns:
        Dictionary with analysis
    """
    qber_increase = qber_with_eve - qber_without_eve
    
    return {
        'baseline_qber': qber_without_eve,
        'qber_with_eve': qber_with_eve,
        'qber_increase': qber_increase,
        'eve_impact_percentage': (qber_increase / max(qber_without_eve, 1.0)) * 100,
        'eve_detectable': qber_with_eve > 11.0
    }
