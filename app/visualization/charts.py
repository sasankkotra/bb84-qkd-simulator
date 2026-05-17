"""
Visualization module for BB84 QKD.

Creates publication-quality plots and graphs.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Optional, Dict
import os

from app.config.settings import visualization_config
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class BB84Visualizer:
    """Creates visualizations for BB84 simulation results."""
    
    def __init__(self, config=None):
        """Initialize visualizer with configuration."""
        self.config = config or visualization_config
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_qber_vs_qubit_count(
        self,
        qubit_counts: List[int],
        qber_values: List[float],
        save_path: Optional[str] = None,
        title: str = "QBER vs Qubit Count"
    ) -> plt.Figure:
        """
        Plot QBER evolution as qubit count increases.
        
        Args:
            qubit_counts: List of qubit counts
            qber_values: Corresponding QBER percentages
            save_path: Optional path to save figure
            title: Plot title
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.config.figure_dpi)
        
        ax.plot(qubit_counts, qber_values, 'o-', linewidth=2, markersize=6, label='Measured QBER')
        ax.axhline(y=11, color='r', linestyle='--', linewidth=2, label='Security Threshold (11%)')
        ax.fill_between(qubit_counts, 0, 11, alpha=0.2, color='green', label='Secure Region')
        ax.fill_between(qubit_counts, 11, 100, alpha=0.2, color='red', label='Compromised Region')
        
        ax.set_xlabel('Number of Qubits', fontsize=12, fontweight='bold')
        ax.set_ylabel('QBER (%)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 30])
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.export_dpi, bbox_inches='tight')
            logger.info(f"Saved QBER plot to {save_path}")
        
        return fig
    
    def plot_eve_comparison(
        self,
        scenarios: Dict[str, float],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare QBER under normal and Eve attack scenarios.
        
        Args:
            scenarios: Dict with scenario names and QBER values
            save_path: Optional path to save figure
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.config.figure_dpi)
        
        scenario_names = list(scenarios.keys())
        scenario_values = list(scenarios.values())
        
        colors = ['green' if v < 11 else 'red' for v in scenario_values]
        bars = ax.bar(scenario_names, scenario_values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, value in zip(bars, scenario_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.axhline(y=11, color='r', linestyle='--', linewidth=2, alpha=0.5, label='Threshold')
        ax.set_ylabel('QBER (%)', fontsize=12, fontweight='bold')
        ax.set_title('QBER Comparison: Normal vs Eve Attack', fontsize=14, fontweight='bold')
        ax.set_ylim([0, max(scenario_values) + 5])
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.export_dpi, bbox_inches='tight')
            logger.info(f"Saved Eve comparison plot to {save_path}")
        
        return fig
    
    def plot_basis_match_distribution(
        self,
        match_count: int,
        total_qubits: int,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Visualize matched and mismatched bases distribution.
        
        Args:
            match_count: Number of matching bases
            total_qubits: Total qubits sent
            save_path: Optional path to save figure
            
        Returns:
            Matplotlib figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=self.config.figure_dpi)
        
        # Pie chart
        mismatch_count = total_qubits - match_count
        sizes = [match_count, mismatch_count]
        labels = ['Matched Bases', 'Mismatched Bases']
        colors = ['#50fa7b', '#ff79c6']
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
        ax1.set_title('Basis Match Distribution', fontsize=12, fontweight='bold')
        
        # Bar chart
        categories = ['Matched', 'Mismatched']
        values = [match_count, mismatch_count]
        ax2.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax2.set_title('Basis Comparison Results', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        for i, v in enumerate(values):
            ax2.text(i, v + 10, str(v), ha='center', fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.export_dpi, bbox_inches='tight')
            logger.info(f"Saved basis distribution plot to {save_path}")
        
        return fig
    
    def plot_secure_key_length(
        self,
        total_bits: int,
        sifted_bits: int,
        authentication_overhead: float = 0.25,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Visualize key reduction through sifting and privacy amplification.
        
        Args:
            total_bits: Original bits sent
            sifted_bits: Bits after sifting
            authentication_overhead: Fraction lost to authentication
            save_path: Optional path to save figure
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.config.figure_dpi)
        
        secure_bits = int(sifted_bits * (1 - authentication_overhead))
        
        stages = ['Total Qubits', 'After Sifting', 'Secure Key\n(after auth)']
        lengths = [total_bits, sifted_bits, secure_bits]
        colors = ['#489fdf', '#50fa7b', '#ffb86c']
        
        bars = ax.bar(stages, lengths, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        
        # Add value labels
        for bar, length in zip(bars, lengths):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(length)}\nbits', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.set_ylabel('Number of Bits', fontsize=12, fontweight='bold')
        ax.set_title('Secure Key Length Analysis', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.export_dpi, bbox_inches='tight')
            logger.info(f"Saved key length plot to {save_path}")
        
        return fig
    
    def plot_noise_impact(
        self,
        noise_levels: List[float],
        qber_values: List[float],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare QBER at different noise levels.
        
        Args:
            noise_levels: List of noise probabilities (0-1)
            qber_values: Corresponding QBER percentages
            save_path: Optional path to save figure
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.config.figure_dpi)
        
        noise_percent = [n * 100 for n in noise_levels]
        ax.plot(noise_percent, qber_values, 'o-', linewidth=2.5, markersize=8, color='#ff79c6')
        ax.axhline(y=11, color='r', linestyle='--', linewidth=2, alpha=0.7, label='Security Threshold')
        
        ax.fill_between(noise_percent, 0, 11, alpha=0.15, color='green')
        ax.fill_between(noise_percent, 11, 30, alpha=0.15, color='red')
        
        ax.set_xlabel('Channel Noise Level (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('QBER (%)', fontsize=12, fontweight='bold')
        ax.set_title('Quantum Channel Noise Impact', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.export_dpi, bbox_inches='tight')
            logger.info(f"Saved noise impact plot to {save_path}")
        
        return fig
    
    def create_summary_visualization(
        self,
        result,
        output_dir: str = "outputs/graphs/"
    ) -> Dict[str, str]:
        """
        Create all summary visualizations.
        
        Args:
            result: SimulationResult object
            output_dir: Directory to save plots
            
        Returns:
            Dictionary mapping plot names to file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        
        plots = {}
        
        # Plot 1: Simple QBER bar chart
        fig1, ax = plt.subplots(figsize=(8, 6), dpi=self.config.figure_dpi)
        qber = result.qber_result.error_percentage
        color = 'red' if qber > 11 else 'green'
        ax.bar(['QBER'], [qber], color=color, alpha=0.7, edgecolor='black', linewidth=2, width=0.5)
        ax.axhline(y=11, color='r', linestyle='--', linewidth=2, alpha=0.5)
        ax.set_ylabel('QBER (%)', fontsize=12, fontweight='bold')
        ax.set_title('Quantum Bit Error Rate', fontsize=14, fontweight='bold')
        ax.set_ylim([0, 25])
        ax.text(0, qber + 1, f'{qber:.2f}%', ha='center', fontsize=12, fontweight='bold')
        
        path1 = os.path.join(output_dir, 'qber_summary.png')
        plt.savefig(path1, dpi=self.config.export_dpi, bbox_inches='tight')
        plt.close(fig1)
        plots['qber_summary'] = path1
        
        # Plot 2: Basis distribution
        matched = len(result.matched_indices)
        total = result.alice_bits.shape[0]
        path2 = os.path.join(output_dir, 'basis_distribution.png')
        self.plot_basis_match_distribution(matched, total, path2)
        plt.close()
        plots['basis_distribution'] = path2
        
        # Plot 3: Key length analysis
        sifted = result.sifted_key.shape[0]
        path3 = os.path.join(output_dir, 'key_length_analysis.png')
        self.plot_secure_key_length(total, sifted, save_path=path3)
        plt.close()
        plots['key_length_analysis'] = path3
        
        logger.info(f"Created {len(plots)} visualizations in {output_dir}")
        return plots
