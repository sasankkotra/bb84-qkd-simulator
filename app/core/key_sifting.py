"""
Key Sifting module for BB84 QKD.

Implements the sifting process to extract the final secret key.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SiftingResult:
    """Result of key sifting process."""
    matched_indices: np.ndarray
    sifted_key: np.ndarray
    sifted_key_length: int
    key_efficiency: float  # Percentage of original bits retained
    total_qubits: int


def sift_key_from_bases(
    alice_bits: np.ndarray,
    alice_bases: np.ndarray,
    bob_bases: np.ndarray,
    bob_measurements: np.ndarray
) -> SiftingResult:
    """
    Sift the final key by keeping only bits where bases matched.
    
    Only positions where Alice and Bob used the same basis are kept.
    These positions should have correct measurements (if no noise/Eve).
    
    Args:
        alice_bits: Original bits Alice sent
        alice_bases: Bases Alice used for encoding
        bob_bases: Bases Bob used for measurement
        bob_measurements: Bob's measurement results
        
    Returns:
        SiftingResult with sifted key and statistics
    """
    # Find positions where bases match
    matched_indices = np.where(alice_bases == bob_bases)[0]
    
    # Extract bits only from matched positions
    sifted_key = bob_measurements[matched_indices]
    
    # Calculate efficiency
    total_qubits = len(alice_bits)
    sifted_length = len(sifted_key)
    efficiency = (sifted_length / total_qubits * 100) if total_qubits > 0 else 0
    
    return SiftingResult(
        matched_indices=matched_indices,
        sifted_key=sifted_key,
        sifted_key_length=sifted_length,
        key_efficiency=efficiency,
        total_qubits=total_qubits
    )


def compare_with_alice_key(
    alice_bits: np.ndarray,
    bob_sifted_key: np.ndarray,
    matched_indices: np.ndarray
) -> Tuple[np.ndarray, int]:
    """
    Compare Bob's sifted key with Alice's bits at matched positions.
    
    This is used to calculate QBER and detect eavesdropping.
    Note: In real BB84, Alice and Bob publish which positions had matching
    bases but NOT the actual bits. Here we do this for verification.
    
    Args:
        alice_bits: Alice's original bits
        bob_sifted_key: Bob's sifted key
        matched_indices: Indices where bases matched
        
    Returns:
        Tuple of (error_positions, error_count)
    """
    alice_sifted_key = alice_bits[matched_indices]
    errors = alice_sifted_key != bob_sifted_key
    error_positions = matched_indices[errors]
    error_count = np.sum(errors)
    
    return error_positions, error_count


def calculate_summary_statistics(sifting_result: SiftingResult) -> dict:
    """
    Calculate summary statistics from sifting.
    
    Args:
        sifting_result: Result from key sifting
        
    Returns:
        Dictionary of statistics
    """
    return {
        'total_qubits_sent': sifting_result.total_qubits,
        'matched_bases_count': sifting_result.sifted_key_length,
        'sifted_key_length': sifting_result.sifted_key_length,
        'key_efficiency_percent': sifting_result.key_efficiency,
        'theoretical_efficiency_percent': 50.0,  # Expected for random basis matching
    }
