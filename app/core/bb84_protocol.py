"""
BB84 Protocol main engine.

Orchestrates the complete BB84 QKD protocol simulation.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

from app.core.qubit import Qubit, create_qubit
from app.core.basis import generate_random_bases
from app.core.quantum_channel import QuantumChannel, ChannelConfig
from app.core.key_sifting import sift_key_from_bases, compare_with_alice_key
from app.core.qber import calculate_qber
from app.core.eve_attack import perform_eve_attack
from app.core.noise_model import apply_channel_noise
from app.core.security_analysis import perform_security_analysis
from app.config.settings import simulation_config
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


@dataclass
class SimulationResult:
    """Complete BB84 simulation result."""
    alice_bits: np.ndarray
    alice_bases: np.ndarray
    bob_bases: np.ndarray
    bob_measurements: np.ndarray
    sifted_key: np.ndarray
    matched_indices: np.ndarray
    
    qber_result: object  # QBERResult
    security_analysis: object  # SecurityAnalysis
    
    eve_present: bool
    eve_bases: Optional[List[int]] = None
    eve_measurements: Optional[List[int]] = None
    
    noise_applied: bool = False
    
    @property
    def is_secure(self) -> bool:
        """Channel security determination."""
        return self.security_analysis.threat_level == 'LOW'


class BB84Protocol:
    """
    Complete BB84 Quantum Key Distribution Protocol implementation.
    
    Protocol steps:
    1. Alice generates random bits and bases
    2. Alice encodes bits in qubits using chosen bases
    3. Bob receives qubits from Alice (may be intercepted by Eve)
    4. Bob measures qubits in random bases
    5. Alice and Bob publicly compare bases (not bits)
    6. Sift the key: keep only bits where bases matched
    7. Estimate QBER to detect eavesdropping
    8. Perform security analysis
    """
    
    def __init__(self, config: Optional[object] = None):
        """
        Initialize BB84 protocol.
        
        Args:
            config: SimulationConfig object
        """
        self.config = config or simulation_config
        self.channel = None
        self.last_result = None
    
    def run_simulation(self) -> SimulationResult:
        """
        Run complete BB84 simulation.
        
        Returns:
            SimulationResult with all protocol data and analysis
        """
        logger.info(f"Starting BB84 simulation with {self.config.num_qubits} qubits")
        
        # Step 1: Alice generates random bits
        seed = self.config.random_seed
        if seed is not None:
            np.random.seed(seed)
        
        alice_bits = np.random.randint(0, 2, self.config.num_qubits)
        logger.info(f"Generated Alice's random bits")
        
        # Step 2: Alice generates random bases
        alice_bases, _ = generate_random_bases(self.config.num_qubits, seed=None)
        logger.info(f"Generated Alice's random bases")
        
        # Step 3: Alice encodes qubits
        alice_qubits = [
            create_qubit(alice_bits[i], alice_bases[i])
            for i in range(self.config.num_qubits)
        ]
        logger.info(f"Encoded {len(alice_qubits)} qubits")
        
        # Step 4: Quantum transmission (may include Eve)
        eve_bases_list = None
        eve_measurements_list = None
        
        transmitted_qubits = alice_qubits.copy()
        
        # Eve intercept-resend attack
        if self.config.eve_active:
            logger.info(f"Eve active, intercept probability: {self.config.eve_intercept_probability}")
            transmitted_qubits, eve_bases_list, eve_measurements_list, eve_stats = perform_eve_attack(
                alice_qubits,
                self.config.eve_intercept_probability
            )
            logger.info(f"Eve intercepted {eve_stats.qubits_intercepted} qubits")
        
        # Channel noise
        if self.config.noise_active:
            logger.info(f"Noise active, probability: {self.config.noise_probability}")
            transmitted_qubits, noise_stats = apply_channel_noise(
                transmitted_qubits,
                self.config.noise_probability
            )
            logger.info(f"Noise flipped {noise_stats.flipped_bit_count} bits")
        
        # Step 5: Bob generates random bases and measures
        bob_bases, _ = generate_random_bases(self.config.num_qubits, seed=None)
        logger.info(f"Generated Bob's random bases and measuring...")
        
        bob_measurements = np.array([
            transmitted_qubits[i].measure(bob_bases[i])
            for i in range(self.config.num_qubits)
        ])
        logger.info(f"Bob completed measurements")
        
        # Step 6: Sifting
        sifting_result = sift_key_from_bases(
            alice_bits, alice_bases, bob_bases, bob_measurements
        )
        logger.info(f"Key sifting complete: {sifting_result.sifted_key_length} bits kept")
        
        # Step 7: QBER calculation
        error_positions, error_count = compare_with_alice_key(
            alice_bits, sifting_result.sifted_key, sifting_result.matched_indices
        )
        qber_result = calculate_qber(alice_bits, bob_measurements, sifting_result.matched_indices)
        logger.info(f"QBER: {qber_result.error_percentage:.2f}%")
        
        # Step 8: Security analysis
        security_result = perform_security_analysis(
            qber_result.error_percentage,
            sifting_result.sifted_key_length,
            self.config.num_qubits,
            self.config.eve_active
        )
        logger.info(f"Security status: {security_result.security_status}")
        
        # Create result object
        result = SimulationResult(
            alice_bits=alice_bits,
            alice_bases=alice_bases,
            bob_bases=bob_bases,
            bob_measurements=bob_measurements,
            sifted_key=sifting_result.sifted_key,
            matched_indices=sifting_result.matched_indices,
            qber_result=qber_result,
            security_analysis=security_result,
            eve_present=self.config.eve_active,
            eve_bases=eve_bases_list,
            eve_measurements=eve_measurements_list,
            noise_applied=self.config.noise_active
        )
        
        self.last_result = result
        logger.info("Simulation complete")
        
        return result
    
    def get_summary(self, result: Optional[SimulationResult] = None) -> str:
        """
        Get formatted text summary of simulation.
        
        Args:
            result: SimulationResult (uses last_result if not provided)
            
        Returns:
            Formatted summary string
        """
        result = result or self.last_result
        if not result:
            return "No simulation results available"
        
        from app.utils.constants import OUTPUT_SEPARATOR
        
        lines = [
            OUTPUT_SEPARATOR,
            "BB84 QUANTUM KEY DISTRIBUTION SIMULATION",
            OUTPUT_SEPARATOR,
            "",
            f"Protocol Configuration:",
            f"  Total Qubits:        {self.config.num_qubits}",
            f"  Eve Active:          {self.config.eve_active}",
            f"  Noise Active:        {self.config.noise_active}",
            "",
            f"Results:",
            f"  Matched Bases:       {len(result.matched_indices)}/{self.config.num_qubits}",
            f"  Sifted Key Length:   {result.sifted_key.shape[0]} bits",
            f"  Key Efficiency:      {len(result.matched_indices)/self.config.num_qubits*100:.1f}%",
            "",
            f"Security Analysis:",
            f"  QBER:                {result.qber_result.error_percentage:.2f}%",
            f"  Security Status:     {result.security_analysis.security_status}",
            f"  Threat Level:        {result.security_analysis.threat_level}",
            f"  Eve Probability:     {result.security_analysis.eve_probability:.1%}",
            "",
            f"Sifted Key (first 64 bits): {''.join(map(str, result.sifted_key[:64]))}",
            "",
            OUTPUT_SEPARATOR,
        ]
        
        return "\n".join(lines)


def run_bb84_simulation(num_qubits: int = 1000,
                        eve_active: bool = False,
                        noise_active: bool = False,
                        noise_prob: float = 0.05,
                        seed: Optional[int] = None) -> SimulationResult:
    """
    Convenience function to run BB84 simulation.
    
    Args:
        num_qubits: Number of qubits to transmit
        eve_active: Whether Eve performs intercept-resend attack
        noise_active: Whether to apply channel noise
        noise_prob: Noise bit flip probability
        seed: Random seed for reproducibility
        
    Returns:
        SimulationResult
    """
    config = simulation_config
    config.num_qubits = num_qubits
    config.eve_active = eve_active
    config.noise_active = noise_active
    config.noise_probability = noise_prob
    config.random_seed = seed
    
    protocol = BB84Protocol(config)
    return protocol.run_simulation()
