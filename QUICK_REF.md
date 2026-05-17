# BB84 QKD Simulator - Quick Reference

## Installation & First Run

```bash
# Install
cd bb84-qkd-simulator
pip install -r requirements.txt

# Run
python main.py
```

## Common Commands

```bash
# Basic simulation (1000 qubits)
python main.py

# With Eve attack
python main.py --eve

# With noise
python main.py --noise 0.05

# Full simulation with exports and visualizations
python main.py --qubits 5000 --eve --noise 0.05 --export --visualize --seed 42

# GUI mode
python main.py --gui

# Run tests
pytest tests/test_bb84.py -v

# Test with coverage
pytest tests/test_bb84.py --cov=app --cov-report=html
```

## Key Results Interpretation

### QBER (Quantum Bit Error Rate)

| QBER | Meaning | Action |
|------|---------|--------|
| < 1% | Perfect channel | ✅ All OK |
| 1-5% | Normal noise | ✅ Likely secure |
| 5-11% | High noise or concerns | ⚠️ Investigate |
| > 11% | Eve or severe noise | ❌ ABORT |

### Threat Levels

- **GREEN (LOW)**: QBER < 11%, channel appears secure
- **YELLOW (MEDIUM)**: QBER 11-16%, possible eavesdropping
- **RED (HIGH)**: QBER > 16%, abort communication

## Python API Quick Examples

### Basic Simulation

```python
from app.core.bb84_protocol import run_bb84_simulation

result = run_bb84_simulation(num_qubits=1000)
print(f"QBER: {result.qber_result.error_percentage:.2f}%")
print(f"Secure: {result.is_secure}")
```

### With Eve Attack

```python
result = run_bb84_simulation(
    num_qubits=1000,
    eve_active=True,
    eve_intercept_probability=1.0
)

print(f"Eve detected: {result.qber_result.error_percentage > 11}")
```

### With Noise

```python
result = run_bb84_simulation(
    num_qubits=1000,
    noise_active=True,
    noise_prob=0.05  # 5% bit flip rate
)
```

### Advanced Configuration

```python
from app.config.settings import SimulationConfig
from app.core.bb84_protocol import BB84Protocol

config = SimulationConfig(
    num_qubits=2000,
    eve_active=True,
    eve_intercept_probability=0.8,  # Eve intercepts 80%
    noise_active=True,
    noise_probability=0.02,          # 2% noise
    random_seed=42                   # Reproducible
)

protocol = BB84Protocol(config)
result = protocol.run_simulation()

# Access results
print(f"QBER: {result.qber_result.error_percentage:.2f}%")
print(f"Status: {result.security_analysis.security_status}")
print(f"Recommendations: {result.security_analysis.recommendations}")
```

### Export Results

```python
from app.utils.exporters import ExportManager

manager = ExportManager(output_dir='outputs')

# Export all formats
exports = manager.export_all(result)
# Returns: {'csv': '...', 'json': '...', 'text': '...'}

# Or individual formats
manager.export_to_csv(result)
manager.export_to_json(result)
manager.export_to_text(result)
```

### Visualization

```python
from app.visualization.charts import BB84Visualizer

visualizer = BB84Visualizer()

# Generate all plots
plots = visualizer.create_summary_visualization(result)

# Or individual plots
visualizer.plot_eve_comparison({'Normal': 1.2, 'With Eve': 12.5}, 
                               save_path='outputs/graphs/comparison.png')
```

## Output File Locations

- **Graphs**: `outputs/graphs/`
- **CSV Data**: `outputs/csv/`
- **Reports**: `outputs/reports/`
- **Logs**: `outputs/logs/`

## Module Dependencies

- **Core Protocol**: `app/core/bb84_protocol.py` (depends on all core modules)
- **Tests**: `tests/test_bb84.py` (imports core modules)
- **GUI**: `app/gui/main_window.py` (imports core + visualization)
- **Visualization**: `app/visualization/charts.py` (matplotlib-based)

## Troubleshooting

### Import Errors
```bash
# Make sure you're in project root
cd bb84-qkd-simulator
python main.py  # Not: python app/core/bb84_protocol.py
```

### Matplotlib Issues
```bash
# If plots not showing, try
pip install --upgrade matplotlib
```

### Virtual Environment
```bash
# Create and activate
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

## Performance Notes

- **1000 qubits**: < 1 second
- **10,000 qubits**: < 5 seconds
- **100,000 qubits**: ~30-60 seconds
- **1,000,000 qubits**: ~5-10 minutes

Uses NumPy vectorization for efficiency.

## Security Assumptions

1. **Quantum measurement**: Correct basis → correct bit, wrong basis → random
2. **Eve's attack**: Intercept-resend with random basis choice
3. **Channel**: Quantum channel (not classical)
4. **Eavesdropping**: Eve produces detectable QBER increase
5. **Privacy**: Classical channel secure for basis comparison

## Educational Concepts

### What Students Learn

1. **Quantum Measurement**: Non-destructive measurement is impossible
2. **Basis Incompleteness**: Two bases are mutually unbiased
3. **Eavesdropping Detection**: Eve's measurements introduce errors
4. **Key Sifting**: Only ~50% of bits become key
5. **Security Analysis**: QBER indicates channel security

### Demo Sequence

1. Run basic simulation → observe QBER ≈ 1%
2. Enable Eve → observe QBER ≈ 12.5%
3. Discuss why Eve causes errors
4. Run statistical analysis with multiple runs
5. Compare scenarios (noise, Eve, combined)

## Citation

If using this simulator in research or publication:

```
@software{bb84_simulator_2024,
  title={BB84 Quantum Key Distribution Simulator},
  year={2024},
  url={https://github.com/yourusername/bb84-qkd-simulator}
}
```

---

**See README.md for detailed documentation**
