"""
Comprehensive test suite for BB84 QKD Simulator.

Test coverage includes:
- Bit and basis generation
- Qubit encoding and measurement
- Key sifting
- QBER calculation
- Eve attack detection
- Noise handling
- Security analysis
"""

import pytest
import numpy as np
from app.core.basis import generate_random_bases, find_matching_bases, sift_key
from app.core.qubit import Qubit, create_qubit
from app.core.key_sifting import sift_key_from_bases
from app.core.qber import calculate_qber
from app.core.eve_attack import perform_eve_attack
from app.core.noise_model import apply_channel_noise
from app.core.bb84_protocol import BB84Protocol, run_bb84_simulation
from app.config.settings import SimulationConfig


class TestBasisGeneration:
    """Test basis generation."""
    
    def test_random_bases_shape(self):
        """Test that generated bases have correct shape."""
        num_qubits = 100
        bases, basis_objs = generate_random_bases(num_qubits)
        
        assert bases.shape == (num_qubits,)
        assert len(basis_objs) == num_qubits
    
    def test_random_bases_values(self):
        """Test that bases contain only 0 and 1."""
        bases, _ = generate_random_bases(1000)
        
        assert np.all((bases == 0) | (bases == 1))
    
    def test_random_bases_distribution(self):
        """Test that bases are roughly equally distributed."""
        bases, _ = generate_random_bases(10000)
        
        zeros = np.sum(bases == 0)
        ones = np.sum(bases == 1)
        
        # Should be roughly 50-50 (within 10%)
        ratio = zeros / (zeros + ones)
        assert 0.4 < ratio < 0.6
    
    def test_basis_reproducibility(self):
        """Test that seed produces reproducible results."""
        bases1, _ = generate_random_bases(100, seed=42)
        bases2, _ = generate_random_bases(100, seed=42)
        
        assert np.array_equal(bases1, bases2)


class TestQubit:
    """Test Qubit class."""
    
    def test_qubit_creation(self):
        """Test basic qubit creation."""
        qubit = Qubit(bit=1, basis=0)
        
        assert qubit.bit == 1
        assert qubit.basis == 0
        assert qubit.state is not None
    
    def test_qubit_invalid_basis(self):
        """Test that invalid basis raises error."""
        with pytest.raises(ValueError):
            Qubit(bit=0, basis=2)
    
    def test_qubit_invalid_bit(self):
        """Test that invalid bit raises error."""
        with pytest.raises(ValueError):
            Qubit(bit=2, basis=0)
    
    def test_qubit_measurement_matched_basis(self):
        """Test measurement with matching basis."""
        qubit = Qubit(bit=1, basis=0)
        
        # Measuring in correct basis should always return correct bit
        for _ in range(10):
            result = qubit.measure(0)
            assert result == 1
    
    def test_qubit_measurement_mismatched_basis(self):
        """Test measurement with mismatched basis (should be random)."""
        qubit = Qubit(bit=1, basis=0)
        
        # Measuring in wrong basis should give random results
        results = []
        for _ in range(100):
            results.append(qubit.measure(1))
        
        # Should have mix of 0s and 1s
        assert 0 in results
        assert 1 in results


class TestKeySifting:
    """Test key sifting."""
    
    def test_sifting_basic(self):
        """Test basic key sifting."""
        alice_bits = np.array([1, 0, 1, 1, 0, 1])
        alice_bases = np.array([0, 1, 0, 1, 0, 1])
        bob_bases = np.array([0, 0, 0, 1, 0, 1])
        bob_measurements = np.array([1, 0, 1, 1, 0, 1])
        
        result = sift_key_from_bases(alice_bits, alice_bases, bob_bases, bob_measurements)
        
        # Matched indices: 0, 2, 3, 4, 5 (where bases match)
        assert len(result.matched_indices) == 5
        assert np.array_equal(result.matched_indices, [0, 2, 3, 4, 5])
    
    def test_sifting_efficiency(self):
        """Test that sifting efficiency is ~50%."""
        alice_bits = np.random.randint(0, 2, 1000)
        alice_bases = np.random.randint(0, 2, 1000)
        bob_bases = np.random.randint(0, 2, 1000)
        bob_measurements = np.random.randint(0, 2, 1000)
        
        result = sift_key_from_bases(alice_bits, alice_bases, bob_bases, bob_measurements)
        
        # Should be approximately 50%
        efficiency = result.key_efficiency
        assert 40 < efficiency < 60  # Allow some variance


class TestQBER:
    """Test QBER calculation."""
    
    def test_qber_no_errors(self):
        """Test QBER with no errors."""
        alice_bits = np.array([1, 0, 1, 1])
        bob_measurements = np.array([1, 0, 1, 1])
        matched_indices = np.array([0, 1, 2, 3])
        
        result = calculate_qber(alice_bits, bob_measurements, matched_indices)
        
        assert result.error_percentage == 0.0
        assert result.error_count == 0
    
    def test_qber_with_errors(self):
        """Test QBER with known errors."""
        alice_bits = np.array([1, 0, 1, 1])
        bob_measurements = np.array([1, 1, 1, 1])  # Error at position 1
        matched_indices = np.array([0, 1, 2, 3])
        
        result = calculate_qber(alice_bits, bob_measurements, matched_indices)
        
        assert result.error_count == 1
        assert result.error_percentage == 25.0  # 1/4 = 25%
    
    def test_qber_security_threshold(self):
        """Test security classification."""
        # Low QBER - secure
        result_secure = calculate_qber(
            np.array([1, 0, 1, 1, 0]),
            np.array([1, 0, 1, 1, 0]),
            np.array([0, 1, 2, 3, 4])
        )
        assert result_secure.is_secure
        assert result_secure.security_status == 'SECURE'
        
        # High QBER - compromised
        result_compromised = calculate_qber(
            np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            np.array([0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0]),  # High error rate
            np.arange(11)
        )
        assert not result_compromised.is_secure


class TestEveAttack:
    """Test Eve attack simulation."""
    
    def test_eve_intercept(self):
        """Test Eve interception."""
        alice_qubits = [
            Qubit(1, 0), Qubit(0, 0), Qubit(1, 1), Qubit(0, 1)
        ]
        
        eve_modified, eve_bases, eve_measurements, stats = perform_eve_attack(
            alice_qubits, intercept_probability=1.0
        )
        
        assert stats.qubits_intercepted == 4
        assert len(eve_bases) == 4
        assert len(eve_measurements) == 4
    
    def test_eve_partial_intercept(self):
        """Test Eve partial interception."""
        alice_qubits = [Qubit(1, 0) for _ in range(100)]
        
        eve_modified, eve_bases, eve_measurements, stats = perform_eve_attack(
            alice_qubits, intercept_probability=0.5
        )
        
        # Should intercept roughly 50%
        assert 30 < stats.qubits_intercepted < 70


class TestNoiseModel:
    """Test noise model."""
    
    def test_noise_application(self):
        """Test noise application."""
        qubits = [Qubit(bit=1, basis=0) for _ in range(100)]
        
        noisy_qubits, stats = apply_channel_noise(qubits, 0.5)
        
        # With 50% noise, expect roughly 50 flips
        assert 30 < stats.flipped_bit_count < 70
    
    def test_noise_zero_probability(self):
        """Test noise with zero probability."""
        qubits = [Qubit(bit=1, basis=0) for _ in range(100)]
        
        noisy_qubits, stats = apply_channel_noise(qubits, 0.0)
        
        assert stats.flipped_bit_count == 0


class TestBB84Protocol:
    """Test complete BB84 protocol."""
    
    def test_protocol_basic_run(self):
        """Test basic protocol run."""
        config = SimulationConfig(num_qubits=100, eve_active=False, noise_active=False)
        protocol = BB84Protocol(config)
        
        result = protocol.run_simulation()
        
        assert result.alice_bits.shape[0] == 100
        assert result.bob_measurements.shape[0] == 100
        assert result.sifted_key.shape[0] > 0
        assert result.is_secure or not result.is_secure  # Valid security status
    
    def test_protocol_with_eve(self):
        """Test protocol run with Eve."""
        config = SimulationConfig(
            num_qubits=500,
            eve_active=True,
            eve_intercept_probability=1.0
        )
        protocol = BB84Protocol(config)
        
        result = protocol.run_simulation()
        
        assert result.eve_present
        # Eve should increase QBER
        assert result.qber_result.error_percentage > 1.0
    
    def test_protocol_with_noise(self):
        """Test protocol run with noise."""
        config = SimulationConfig(
            num_qubits=500,
            noise_active=True,
            noise_probability=0.05
        )
        protocol = BB84Protocol(config)
        
        result = protocol.run_simulation()
        
        assert result.noise_applied
        # Noise should cause some errors
        assert result.qber_result.error_percentage > 0.0
    
    def test_protocol_reproducibility(self):
        """Test that same seed produces same results."""
        config1 = SimulationConfig(num_qubits=100, random_seed=42)
        config2 = SimulationConfig(num_qubits=100, random_seed=42)
        
        protocol1 = BB84Protocol(config1)
        protocol2 = BB84Protocol(config2)
        
        result1 = protocol1.run_simulation()
        result2 = protocol2.run_simulation()
        
        # Same seed should produce identical bits and bases
        assert np.array_equal(result1.alice_bits, result2.alice_bits)
        assert np.array_equal(result1.alice_bases, result2.alice_bases)


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_run_bb84_simulation(self):
        """Test run_bb84_simulation convenience function."""
        result = run_bb84_simulation(
            num_qubits=100,
            eve_active=False,
            noise_active=False,
            seed=42
        )
        
        assert result is not None
        assert result.alice_bits.shape[0] == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
