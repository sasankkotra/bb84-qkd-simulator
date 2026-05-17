"""
Pytest configuration for BB84 QKD Simulator tests.

This file ensures that the app module can be imported from tests.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
