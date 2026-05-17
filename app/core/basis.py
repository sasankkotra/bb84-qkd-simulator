"""
Basis module for BB84 QKD.

Implements basis generation and manipulation for the BB84 protocol.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from app.utils.constants import BASIS_RECTILINEAR, BASIS_DIAGONAL, BASIS_SYMBOL_MAP


@dataclass
class Basis:
    """Represents a quantum basis."""
    
    value: int  # 0 = Rectilinear, 1 = Diagonal
    
    def __post_init__(self):
        """Validate basis value."""
        if self.value not in [BASIS_RECTILINEAR, BASIS_DIAGONAL]:
            raise ValueError(f"Invalid basis value: {self.value}")
    
    @property
    def symbol(self) -> str:
        """Get symbol representation of basis."""
        return BASIS_SYMBOL_MAP[self.value]
    
    @property
    def is_rectilinear(self) -> bool:
        """Check if basis is rectilinear."""
        return self.value == BASIS_RECTILINEAR
    
    @property
    def is_diagonal(self) -> bool:
        """Check if basis is diagonal."""
        return self.value == BASIS_DIAGONAL
    
    def __str__(self) -> str:
        return self.symbol
    
    def __repr__(self) -> str:
        return f"Basis({self.symbol})"


def generate_random_bases(num_qubits: int, seed: int = None) -> Tuple[np.ndarray, List[Basis]]:
    """
    Generate random bases for a given number of qubits.
    
    Args:
        num_qubits: Number of qubits to generate bases for
        seed: Optional random seed for reproducibility
        
    Returns:
        Tuple of (numpy array of basis values, list of Basis objects)
    """
    if seed is not None:
        np.random.seed(seed)
    
    basis_values = np.random.randint(0, 2, num_qubits)
    basis_objects = [Basis(int(val)) for val in basis_values]
    
    return basis_values, basis_objects


def find_matching_bases(
    alice_bases: np.ndarray,
    bob_bases: np.ndarray
) -> np.ndarray:
    """
    Find indices where Alice and Bob used the same basis.
    
    Args:
        alice_bases: Array of Alice's basis choices
        bob_bases: Array of Bob's basis choices
        
    Returns:
        Array of indices where bases match
    """
    return np.where(alice_bases == bob_bases)[0]


def sift_key(
    bits: np.ndarray,
    matching_indices: np.ndarray
) -> np.ndarray:
    """
    Extract bits only from matching basis positions.
    
    Args:
        bits: Array of all bits
        matching_indices: Indices where bases matched
        
    Returns:
        Sifted key (bits at matching positions)
    """
    return bits[matching_indices]


def calculate_key_efficiency(
    total_qubits: int,
    sifted_key_length: int
) -> float:
    """
    Calculate the key generation efficiency.
    
    Statistics: With random basis choices, ~50% should match on average.
    
    Args:
        total_qubits: Total number of qubits sent
        sifted_key_length: Length after sifting
        
    Returns:
        Efficiency ratio as percentage
    """
    if total_qubits == 0:
        return 0.0
    return (sifted_key_length / total_qubits) * 100
