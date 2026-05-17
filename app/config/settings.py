"""
Configuration settings for BB84 QKD Simulator.

This module contains all configurable parameters for the BB84 protocol simulation,
including security thresholds, visualization settings, and performance tuning.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationConfig:
    """Configuration for BB84 simulation parameters."""
    
    # Protocol parameters
    num_qubits: int = 1000
    random_seed: Optional[int] = None
    
    # Eve attack parameters
    eve_active: bool = False
    eve_intercept_probability: float = 1.0  # 0 to 1, fraction of qubits Eve intercepts
    
    # Noise parameters
    noise_active: bool = False
    noise_probability: float = 0.05  # Bit flip probability
    
    # Security parameters
    SECURITY_THRESHOLD: float = 11.0  # QBER threshold percentage
    
    # Sifting parameters
    min_sifted_key_length: int = 50  # Minimum required sifted key length
    
    
@dataclass
class VisualizationConfig:
    """Configuration for visualization and plotting."""
    
    # Plot settings
    figure_dpi: int = 100
    figure_size_width: float = 12.0
    figure_size_height: float = 8.0
    
    # Style settings
    style: str = "seaborn-v0_8-darkgrid"
    color_scheme: str = "husl"
    
    # Export settings
    export_format: str = "png"
    export_dpi: int = 300
    
    
@dataclass
class GUIConfig:
    """Configuration for GUI parameters."""
    
    # Window settings
    window_width: int = 1600
    window_height: int = 1000
    
    # Theme
    theme: str = "dark"  # "dark" or "light"
    font_family: str = "Helvetica"
    font_size_normal: int = 10
    font_size_title: int = 14
    
    # Colors for dark theme
    bg_color: str = "#1e1e2e"
    fg_color: str = "#ffffff"
    panel_bg: str = "#282a36"
    accent_color: str = "#50fa7b"
    warning_color: str = "#ff79c6"
    

@dataclass
class ExportConfig:
    """Configuration for export and reporting."""
    
    # CSV export settings
    csv_delimiter: str = ","
    csv_encoding: str = "utf-8"
    
    # PDF report settings
    pdf_title: str = "BB84 QKD Simulation Report"
    pdf_author: str = "BB84 Simulator"
    
    # Report include options
    include_graphs: bool = True
    include_raw_data: bool = True
    include_analysis: bool = True


# Global instances
simulation_config = SimulationConfig()
visualization_config = VisualizationConfig()
gui_config = GUIConfig()
export_config = ExportConfig()
