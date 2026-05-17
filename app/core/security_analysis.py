"""
Security Analysis module for BB84 QKD.

Advanced analysis of quantum channel security and attack detection.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict
from app.utils.constants import (
    SECURE_STATUS, POSSIBLY_COMPROMISED_STATUS, COMPROMISED_STATUS,
    SECURITY_THRESHOLD_PERCENT
)


@dataclass
class SecurityAnalysis:
    """Comprehensive security analysis."""
    security_status: str
    qber_percentage: float
    eve_probability: float
    key_generation_rate: float  # bits per qubit sent
    secure_key_rate: float  # theoretical secret key rate
    recommendations: List[str]
    threat_level: str  # LOW, MEDIUM, HIGH
    confidence: float  # 0 to 1


def perform_security_analysis(
    qber: float,
    sifted_key_length: int,
    total_qubits: int,
    eve_detected: bool = False
) -> SecurityAnalysis:
    """
    Perform comprehensive security analysis of the protocol run.
    
    Args:
        qber: Measured QBER percentage
        sifted_key_length: Length of sifted key
        total_qubits: Total qubits transmitted
        eve_detected: Whether Eve was detected
        
    Returns:
        SecurityAnalysis object
    """
    # Determine security status
    threshold = SECURITY_THRESHOLD_PERCENT
    
    if qber > threshold + 5:  # High QBER
        status = COMPROMISED_STATUS
        threat_level = "HIGH"
    elif qber > threshold:  # Borderline
        status = POSSIBLY_COMPROMISED_STATUS
        threat_level = "MEDIUM"
    else:  # Good
        status = SECURE_STATUS
        threat_level = "LOW"
    
    # Estimate Eve probability
    eve_prob = max(0, (qber - 1) / 12.5)
    eve_prob = min(1.0, eve_prob)
    
    # Key generation rate: bits of final key per qubit sent
    if total_qubits > 0:
        key_rate = sifted_key_length / total_qubits
    else:
        key_rate = 0
    
    # Secure key rate: theoretical usable key after privacy amplification
    # Typically: R_secure = R_raw * (1 - 2*H(QBER))
    # where H is binary entropy function
    secure_rate = estimate_secure_key_rate(key_rate, qber)
    
    # Generate recommendations
    recommendations = generate_recommendations(status, qber, eve_prob)
    
    # Confidence in analysis (related to sifted key size)
    confidence = min(1.0, sifted_key_length / 100.0)
    
    return SecurityAnalysis(
        security_status=status,
        qber_percentage=qber,
        eve_probability=eve_prob,
        key_generation_rate=key_rate,
        secure_key_rate=secure_rate,
        recommendations=recommendations,
        threat_level=threat_level,
        confidence=confidence
    )


def estimate_secure_key_rate(
    raw_key_rate: float,
    qber_percentage: float
) -> float:
    """
    Estimate usable secure key rate after privacy amplification.
    
    Formula: R_secure = R_raw * (1 - 2*H(QBER))
    where H(x) = -x*log2(x) - (1-x)*log2(1-x) is binary entropy
    
    Args:
        raw_key_rate: Raw key generation rate
        qber_percentage: QBER as percentage
        
    Returns:
        Estimated secure key rate
    """
    # Convert percentage to fraction
    qber = qber_percentage / 100.0
    
    # Clamp to valid range for entropy
    qber = max(0.001, min(0.499, qber))
    
    # Binary entropy function
    def binary_entropy(x):
        if x <= 0 or x >= 1:
            return 0
        return -x * np.log2(x) - (1 - x) * np.log2(1 - x)
    
    h_qber = binary_entropy(qber)
    
    # Secure rate (with privacy amplification)
    secure_rate = raw_key_rate * (1 - 2 * h_qber)
    
    return max(0, secure_rate)


def statistical_qber_analysis(
    qber_list: List[float],
    confidence_level: float = 0.95
) -> Dict:
    """
    Perform statistical analysis on multiple QBER measurements.
    
    Args:
        qber_list: List of QBER measurements
        confidence_level: Statistical confidence (0 to 1)
        
    Returns:
        Dictionary with statistics
    """
    qber_array = np.array(qber_list)
    
    mean_qber = np.mean(qber_array)
    std_qber = np.std(qber_array)
    min_qber = np.min(qber_array)
    max_qber = np.max(qber_array)
    
    # Estimate confidence interval
    z_score = 1.96  # 95% confidence
    margin_of_error = z_score * std_qber / np.sqrt(len(qber_list))
    
    return {
        'mean_qber': mean_qber,
        'std_qber': std_qber,
        'min_qber': min_qber,
        'max_qber': max_qber,
        'confidence_interval': (
            mean_qber - margin_of_error,
            mean_qber + margin_of_error
        ),
        'above_threshold_count': np.sum(qber_array > SECURITY_THRESHOLD_PERCENT),
        'stability': 1 - (std_qber / mean_qber) if mean_qber > 0 else 0
    }


def generate_recommendations(
    status: str,
    qber: float,
    eve_prob: float
) -> List[str]:
    """
    Generate security recommendations based on analysis.
    
    Args:
        status: Security status
        qber: QBER percentage
        eve_prob: Eve probability (0 to 1)
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    if status == SECURE_STATUS:
        recommendations.append("Channel appears secure. Proceed with key exchange.")
        if eve_prob > 0.1:
            recommendations.append("NOTE: Minor eavesdropping probability detected. Increase qubit count for confidence.")
    
    elif status == POSSIBLY_COMPROMISED_STATUS:
        recommendations.append("CAUTION: QBER slightly elevated. Channel may have noise or eavesdropping.")
        recommendations.append("Consider: Repeat test, check hardware, or abort if security critical.")
        if eve_prob > 0.3:
            recommendations.append("Eve presence is moderately likely.")
    
    else:  # COMPROMISED
        recommendations.append("ALERT: QBER significantly elevated. Possible eavesdropping detected.")
        recommendations.append("RECOMMENDATION: ABORT key exchange immediately.")
        recommendations.append("Actions: Check quantum channel, investigate noise sources.")
    
    if qber < 3:
        recommendations.append("Channel quality is excellent.")
    elif qber > 20:
        recommendations.append("Check for hardware faults or severe noise.")
    
    return recommendations


def compare_scenarios(
    scenarios: Dict[str, dict]
) -> Dict:
    """
    Compare security analysis across multiple scenarios.
    
    Args:
        scenarios: Dictionary with scenario names and their analysis results
        
    Returns:
        Comparison dictionary
    """
    comparison = {}
    
    for name, result in scenarios.items():
        comparison[name] = {
            'qber': result.get('qber', 0),
            'secure': result.get('qber', 100) < SECURITY_THRESHOLD_PERCENT,
            'threat_level': 'HIGH' if result.get('qber', 0) > SECURITY_THRESHOLD_PERCENT + 5 else 'MEDIUM' if result.get('qber', 0) > SECURITY_THRESHOLD_PERCENT else 'LOW'
        }
    
    return comparison
