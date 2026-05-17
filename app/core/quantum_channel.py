"""
Quantum Channel module for BB84 QKD.

Simulates quantum transmission with optional Eve interception and noise.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
from app.core.qubit import Qubit


@dataclass
class ChannelConfig:
    """Configuration for quantum channel behavior."""
    eve_present: bool = False
    eve_intercept_prob: float = 1.0  # Fraction of qubits Eve intercepts
    noise_active: bool = False
    noise_probability: float = 0.05  # Random bit flip probability


class QuantumChannel:
    """
    Simulates quantum transmission through a noisy channel.
    
    Supports:
    - Perfect transmission
    - Noisy transmission (random bit flips)
    - Eve interception and measurement
    """
    
    def __init__(self, config: Optional[ChannelConfig] = None):
        """
        Initialize quantum channel.
        
        Args:
            config: Channel configuration
        """
        self.config = config or ChannelConfig()
        self.eve_bases = None if not self.config.eve_present else []
        self.eve_measurements = None if not self.config.eve_present else []
        self.eve_caught_on = []  # Indices where Eve's choice differs from original
    
    def transmit(self, qubits: List[Qubit]) -> Tuple[List[Qubit], List[int], List[int]]:
        """
        Transmit qubits through channel.
        
        If Eve is active:
        - Eve measures each qubit with random basis
        - Eve resends based on measurement
        - This introduces errors if Eve's basis differs from Alice's
        
        If noise is active:
        - Random bit flips occur
        
        Args:
            qubits: List of qubits to transmit
            
        Returns:
            Tuple of (transmitted_qubits, eve_bases, eve_measurements)
        """
        transmitted = []
        eve_bases_arr = []
        eve_meas_arr = []
        
        for i, qubit in enumerate(qubits):
            transmitted_qubit = Qubit(qubit.bit, qubit.basis)
            
            # Eve interception
            if self.config.eve_present and np.random.rand() < self.config.eve_intercept_prob:
                # Eve chooses random basis
                eve_basis = np.random.randint(0, 2)
                eve_bases_arr.append(eve_basis)
                
                # Eve measures in her chosen basis
                eve_measurement = transmitted_qubit.measure(eve_basis)
                eve_meas_arr.append(eve_measurement)
                
                # Eve resends based on measurement
                transmitted_qubit = Qubit(eve_measurement, eve_basis)
                
                # Track if Eve's basis differed (potential detection)
                if eve_basis != qubit.basis:
                    self.eve_caught_on.append(i)
            else:
                eve_bases_arr.append(-1)  # -1 indicates Eve didn't intercept
                eve_meas_arr.append(-1)
            
            # Channel noise
            if self.config.noise_active and np.random.rand() < self.config.noise_probability:
                # Random bit flip
                transmitted_qubit.bit = 1 - transmitted_qubit.bit
            
            transmitted.append(transmitted_qubit)
        
        self.eve_bases = eve_bases_arr
        self.eve_measurements = eve_meas_arr
        
        return transmitted, eve_bases_arr, eve_meas_arr
    
    def get_eve_interception_count(self) -> int:
        """Get number of qubits Eve intercepted."""
        if not self.config.eve_present:
            return 0
        return sum(1 for b in self.eve_bases if b != -1)
    
    def reset(self):
        """Reset channel state."""
        self.eve_bases = None if not self.config.eve_present else []
        self.eve_measurements = None if not self.config.eve_present else []
        self.eve_caught_on = []
