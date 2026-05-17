"""
QBER (Quantum Bit Error Rate) module for BB84 QKD.

Implements QBER calculation and security analysis.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple
from app.config.settings import simulation_config
from app.utils.constants import (
    SECURE_STATUS, COMPROMISED_STATUS, POSSIBLY_COMPROMISED_STATUS,
    SECURITY_THRESHOLD_PERCENT
)


@dataclass
class QBERResult:
    """Result of QBER calculation."""
    error_count: int
    total_checked_bits: int
    error_percentage: float
    security_status: str
    is_secure: bool
    eve_probability: float  # Estimated probability Eve is present


def calculate_qber(
    alice_bits: np.ndarray,
    bob_measurements: np.ndarray,
    matched_indices: np.ndarray
) -> QBERResult:
    """
    Calculate Quantum Bit Error Rate (QBER).
    
    QBER = (Number of errors / Total sifted bits) * 100
    
    The QBER indicates the quality of the quantum channel.
    - Low QBER (< 11%): Normal channel, likely SECURE
    - High QBER (> 11%): Indicates noise or eavesdropping
    
    Args:
        alice_bits: Alice's original bits
        bob_measurements: Bob's measurement results for all qubits
        matched_indices: Indices where bases matched
        
    Returns:
        QBERResult with analysis
    """
    # Get bits where bases matched
    alice_sifted = alice_bits[matched_indices]
    bob_sifted = bob_measurements[matched_indices]
    
    # Count errors
    error_count = np.sum(alice_sifted != bob_sifted)
    total_checked = len(matched_indices)
    
    # Calculate error percentage
    qber_percent = (error_count / total_checked * 100) if total_checked > 0 else 0
    
    # Determine security status
    threshold = simulation_config.SECURITY_THRESHOLD
    
    if qber_percent < threshold:
        security_status = SECURE_STATUS
        is_secure = True
    elif qber_percent < (threshold + 5):  # 5% margin
        security_status = POSSIBLY_COMPROMISED_STATUS
        is_secure = False
    else:
        security_status = COMPROMISED_STATUS
        is_secure = False
    
    # Estimate Eve probability
    # With random basis choice, Eve introduces ~25% error in mismatched bases
    # This corresponds to ~12.5% in sifted key if Eve intercepts all
    eve_probability = max(0, (qber_percent - 1) / 12.5)  # 1% is baseline noise
    eve_probability = min(1.0, eve_probability)
    
    return QBERResult(
        error_count=error_count,
        total_checked_bits=total_checked,
        error_percentage=qber_percent,
        security_status=security_status,
        is_secure=is_secure,
        eve_probability=eve_probability
    )


def estimate_eve_presence(qber_result: QBERResult) -> Tuple[bool, float]:
    """
    Estimate if Eve is present based on QBER.
    
    Args:
        qber_result: QBER calculation result
        
    Returns:
        Tuple of (eve_likely_present, confidence_0_to_1)
    """
    eve_threshold = SECURITY_THRESHOLD_PERCENT
    if qber_result.error_percentage > eve_threshold:
        confidence = min(1.0, qber_result.eve_probability)
        return True, confidence
    return False, 0.0


def compare_qber_values(qber1: float, qber2: float) -> str:
    """
    Compare two QBER values and describe the difference.
    
    Args:
        qber1: First QBER percentage
        qber2: Second QBER percentage
        
    Returns:
        Description of comparison
    """
    diff = qber2 - qber1
    if abs(diff) < 1:
        return "QBER values are approximately equal"
    elif diff > 1:
        return f"QBER increased by {diff:.2f}% (possible eavesdropping detected)"
    else:
        return f"QBER decreased by {abs(diff):.2f}%"
