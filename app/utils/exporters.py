"""
Export and reporting module for BB84 QKD.

Exports simulation results to CSV, PDF, and text formats.
"""

import json
import csv
import os
from datetime import datetime
from typing import Optional, Dict, Any

import numpy as np
from app.core.bb84_protocol import SimulationResult
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class ExportManager:
    """Manages export of simulation results."""
    
    def __init__(self, output_dir: str = "outputs/"):
        """Initialize export manager."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_to_csv(
        self,
        result: SimulationResult,
        filename: Optional[str] = None
    ) -> str:
        """
        Export simulation data to CSV.
        
        Args:
            result: SimulationResult object
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bb84_simulation_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, "csv", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Prepare data rows
        rows = []
        for i in range(result.alice_bits.shape[0]):
            row = {
                'index': i,
                'alice_bit': int(result.alice_bits[i]),
                'alice_basis': '+' if result.alice_bases[i] == 0 else '×',
                'bob_basis': '+' if result.bob_bases[i] == 0 else '×',
                'bob_measurement': int(result.bob_measurements[i]),
                'basis_match': int(result.alice_bases[i] == result.bob_bases[i]),
                'error': int(result.alice_bits[i] != result.bob_measurements[i]) if result.alice_bases[i] == result.bob_bases[i] else -1,
            }
            
            if result.eve_present and result.eve_bases and i < len(result.eve_bases):
                row['eve_basis'] = '+' if result.eve_bases[i] == 0 else ('×' if result.eve_bases[i] == 1 else 'N/A')
                row['eve_measurement'] = int(result.eve_measurements[i]) if result.eve_measurements[i] != -1 else -1
            
            rows.append(row)
        
        # Write CSV
        if rows:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        logger.info(f"Exported CSV to {filepath}")
        return filepath
    
    def export_to_json(
        self,
        result: SimulationResult,
        filename: Optional[str] = None
    ) -> str:
        """
        Export simulation summary to JSON.
        
        Args:
            result: SimulationResult object
            filename: Optional filename
            
        Returns:
            Path to created JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bb84_summary_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, "reports", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Prepare summary data
        summary = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'BB84 QKD',
            'configuration': {
                'total_qubits': int(result.alice_bits.shape[0]),
                'eve_present': result.eve_present,
                'noise_applied': result.noise_applied,
            },
            'results': {
                'matched_bases': int(len(result.matched_indices)),
                'sifted_key_length': int(result.sifted_key.shape[0]),
                'key_efficiency_percent': float(len(result.matched_indices) / result.alice_bits.shape[0] * 100),
                'qber_percent': float(result.qber_result.error_percentage),
            },
            'security': {
                'security_status': result.security_analysis.security_status,
                'threat_level': result.security_analysis.threat_level,
                'eve_probability': float(result.security_analysis.eve_probability),
                'is_secure': result.security_analysis.threat_level == 'LOW',
            },
            'recommendations': result.security_analysis.recommendations
        }
        
        # Write JSON
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Exported JSON to {filepath}")
        return filepath
    
    def export_to_text(
        self,
        result: SimulationResult,
        filename: Optional[str] = None
    ) -> str:
        """
        Export human-readable text report.
        
        Args:
            result: SimulationResult object
            filename: Optional filename
            
        Returns:
            Path to created text file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bb84_report_{timestamp}.txt"
        
        filepath = os.path.join(self.output_dir, "reports", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        lines = [
            "=" * 70,
            "BB84 QUANTUM KEY DISTRIBUTION - SIMULATION REPORT",
            "=" * 70,
            "",
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "SIMULATION CONFIGURATION:",
            f"  Total Qubits Transmitted: {result.alice_bits.shape[0]}",
            f"  Eve Attack Active: {result.eve_present}",
            f"  Channel Noise Active: {result.noise_applied}",
            "",
            "PROTOCOL RESULTS:",
            f"  Matching Bases Count: {len(result.matched_indices)}",
            f"  Sifted Key Length: {result.sifted_key.shape[0]} bits",
            f"  Key Generation Efficiency: {len(result.matched_indices) / result.alice_bits.shape[0] * 100:.1f}%",
            f"  First 128 bits of sifted key: {''.join(map(str, result.sifted_key[:128]))}",
            "",
            "SECURITY ANALYSIS:",
            f"  Quantum Bit Error Rate (QBER): {result.qber_result.error_percentage:.2f}%",
            f"  Error Count: {result.qber_result.error_count}/{result.qber_result.total_checked_bits}",
            f"  Security Status: {result.security_analysis.security_status}",
            f"  Threat Level: {result.security_analysis.threat_level}",
            f"  Eve Presence Probability: {result.security_analysis.eve_probability:.1%}",
            f"  Key Generation Rate: {result.security_analysis.key_generation_rate:.4f} bits/qubit",
            "",
            "SECURITY ASSESSMENT:",
        ]
        
        for rec in result.security_analysis.recommendations:
            lines.append(f"  • {rec}")
        
        lines.extend([
            "",
            "QUANTUM CHANNEL PROPERTIES:",
            f"  Theoretical Key Efficiency: 50%",
            f"  Actual Key Efficiency: {len(result.matched_indices) / result.alice_bits.shape[0] * 100:.1f}%",
            f"  Estimated Secure Key Rate: {result.security_analysis.secure_key_rate:.4f} bits/qubit",
            "",
            "=" * 70,
            "END OF REPORT",
            "=" * 70,
        ])
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Exported text report to {filepath}")
        return filepath
    
    def export_all(
        self,
        result: SimulationResult,
        base_name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Export to all formats.
        
        Args:
            result: SimulationResult object
            base_name: Base filename (timestamp added if not provided)
            
        Returns:
            Dictionary mapping format to filepath
        """
        if base_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"bb84_{timestamp}"
        
        exports = {
            'csv': self.export_to_csv(result, f"{base_name}.csv"),
            'json': self.export_to_json(result, f"{base_name}_summary.json"),
            'text': self.export_to_text(result, f"{base_name}_report.txt"),
        }
        
        logger.info(f"Exported all formats for {base_name}")
        return exports
