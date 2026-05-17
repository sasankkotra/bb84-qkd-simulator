"""
Qubit module for BB84 QKD.

Implements the quantum bit abstraction and state representations.
"""

from dataclasses import dataclass
from typing import Optional
from app.utils.constants import (
    BASIS_RECTILINEAR, BASIS_DIAGONAL,
    QUANTUM_STATE_MAP, MEASUREMENT_CORRECT, MEASUREMENT_INCORRECT
)


@dataclass
class Qubit:
    """
    Represents a quantum bit in the BB84 protocol.
    
    Attributes:
        bit: The classical bit value (0 or 1)
        basis: The basis used for encoding (0=rectilinear, 1=diagonal)
        state: The quantum state symbol for visualization
    """
    
    bit: int
    basis: int
    state: Optional[str] = None
    
    def __post_init__(self):
        """Initialize quantum state based on bit and basis."""
        if self.bit not in [0, 1]:
            raise ValueError(f"Bit must be 0 or 1, got {self.bit}")
        if self.basis not in [BASIS_RECTILINEAR, BASIS_DIAGONAL]:
            raise ValueError(f"Invalid basis: {self.basis}")
        
        # Set quantum state symbol
        self.state = QUANTUM_STATE_MAP[(self.basis, self.bit)]
    
    @property
    def is_rectilinear_basis(self) -> bool:
        """Check if encoded in rectilinear basis."""
        return self.basis == BASIS_RECTILINEAR
    
    @property
    def is_diagonal_basis(self) -> bool:
        """Check if encoded in diagonal basis."""
        return self.basis == BASIS_DIAGONAL
    
    def measure(self, measurement_basis: int) -> int:
        """
        Measure the qubit in a given basis.
        
        Rules:
        - If measurement_basis matches encoding basis: Always return correct bit
        - If measurement_basis doesn't match: Return random (50-50) outcome
        
        This simulates quantum measurement collapse behavior.
        
        Args:
            measurement_basis: Basis to measure in (0 or 1)
            
        Returns:
            Measured bit value (0 or 1)
        """
        import numpy as np
        
        if measurement_basis not in [BASIS_RECTILINEAR, BASIS_DIAGONAL]:
            raise ValueError(f"Invalid measurement basis: {measurement_basis}")
        
        # Correct measurement - basis matches
        if measurement_basis == self.basis:
            return self.bit
        
        # Incorrect measurement - random outcome
        return np.random.randint(0, 2)
    
    def __str__(self) -> str:
        """String representation."""
        basis_symbol = "+" if self.basis == BASIS_RECTILINEAR else "×"
        return f"Qubit(bit={self.bit}, basis={basis_symbol}, state={self.state})"
    
    def __repr__(self) -> str:
        return self.__str__()


def create_qubit(bit: int, basis: int) -> Qubit:
    """Factory function to create a qubit."""
    return Qubit(bit=bit, basis=basis)