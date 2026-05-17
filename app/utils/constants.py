"""
Constants used throughout the BB84 QKD Simulator.

This module defines all constant values used in the protocol,
including basis representations, quantum states, and security thresholds.
"""

# Basis representations
BASIS_RECTILINEAR = 0
BASIS_DIAGONAL = 1

BASIS_SYMBOL_MAP = {
    BASIS_RECTILINEAR: "+",
    BASIS_DIAGONAL: "×"
}

BASIS_NAME_MAP = {
    BASIS_RECTILINEAR: "Rectilinear",
    BASIS_DIAGONAL: "Diagonal"
}

# Quantum states (for visualization)
QUANTUM_STATE_MAP = {
    (BASIS_RECTILINEAR, 0): "→",   # Horizontal
    (BASIS_RECTILINEAR, 1): "↑",   # Vertical
    (BASIS_DIAGONAL, 0): "↗",      # Diagonal up-right
    (BASIS_DIAGONAL, 1): "↖",      # Diagonal up-left
}

# Measurement outcomes
MEASUREMENT_CORRECT = 1
MEASUREMENT_INCORRECT = 0

# Security thresholds
SECURITY_THRESHOLD_PERCENT = 11.0  # QBER above this = possible eavesdropping
SECURE_STATUS = "SECURE"
COMPROMISED_STATUS = "COMPROMISED"
POSSIBLY_COMPROMISED_STATUS = "POSSIBLY COMPROMISED"

# Protocol phase names
PHASE_BIT_GENERATION = "Bit Generation"
PHASE_BASIS_PREPARATION = "Basis Preparation"
PHASE_TRANSMISSION = "Transmission"
PHASE_MEASUREMENT = "Measurement"
PHASE_SIFTING = "Key Sifting"
PHASE_ANALYSIS = "Security Analysis"

# Statistics parameters
STATISTICAL_RUNS = 100  # Number of runs for statistical analysis

# Output formatting
OUTPUT_WIDTH = 50
OUTPUT_SEPARATOR = "=" * OUTPUT_WIDTH

# File paths
DEFAULT_GRAPH_DIR = "outputs/graphs/"
DEFAULT_REPORT_DIR = "outputs/reports/"
DEFAULT_LOG_DIR = "outputs/logs/"
DEFAULT_CSV_DIR = "outputs/csv/"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = "INFO"
