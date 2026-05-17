# BB84 QKD Simulator - Quick Start Guide (FIXED & WORKING)

## ✅ All Issues Resolved

The simulator is now **fully functional** and **ready to use**!

### Issues Fixed
1. ✅ Syntax error in `qubit.py` 
2. ✅ Test import errors
3. ✅ QBER calculation logic
4. ✅ Test data expectations
5. ✅ Example parameters

### Test Status
- ✅ **23/23 tests passing**
- ✅ **All examples working**
- ✅ **CLI fully functional**
- ✅ **Export/visualization working**

---

## Quick Start Commands

### 1. Basic Simulation (Recommended First Step)
```bash
python main.py
```
**Output**: QBER ~0%, Security Status: SECURE ✓

### 2. Run with Eve Attack
```bash
python main.py --eve --qubits 2000
```
**Output**: QBER ~24%, Security Status: COMPROMISED ⚠️

### 3. Run with Channel Noise
```bash
python main.py --noise 0.05 --qubits 2000
```
**Output**: QBER ~5%, Channel quality is acceptable

### 4. Full Analysis with Eve + Noise
```bash
python main.py --qubits 5000 --eve --noise 0.03 --export --visualize
```
**Output**: 
- CSV data: `outputs/csv/bb84_*.csv`
- JSON summary: `outputs/reports/bb84_*_summary.json` 
- Text report: `outputs/reports/bb84_*_report.txt`
- Plots: `outputs/graphs/*.png`

### 5. Run Examples (7 Demonstrations)
```bash
python examples.py
```
Shows:
1. Basic simulation
2. Eve attack detection
3. Noisy channel
4. Combined challenges
5. Statistical comparison
6. Export functionality
7. Protocol walkthrough

### 6. Run All Tests
```bash
pytest tests/test_bb84.py -v
```
**Result**: All 23 tests pass ✓

### 7. LaunchGUI (Tkinter Interactive)
```bash
python main.py --gui
```
Interactive interface for:
- Parameter configuration
- Real-time simulation
- Results export

---

## Command-Line Options

```
--qubits N              Number of qubits (default: 1000)
--eve                   Enable Eve intercept-resend attack
--noise PROB            Channel noise probability (default: 0.0)
--seed SEED             Random seed for reproducibility
--export                Export to CSV/JSON/text
--visualize             Generate plots
--gui                   Launch GUI interface
--verbose               Detailed logging
```

---

## Expected Results

### Scenario 1: Secure Channel (No Attack)
```
QBER: 0-1%
Security Status: SECURE
Threat Level: LOW
Recommendation: Proceed ✓
```

### Scenario 2: Eve Present (Intercept-Resend)
```
QBER: 20-30%
Security Status: COMPROMISED
Threat Level: HIGH
Recommendation: ABORT ⚠️
```

### Scenario 3: Noisy Channel (5% Noise)
```
QBER: 4-6%
Security Status: SECURE
Threat Level: LOW
Recommendation: Investigate noise source ✓
```

### Scenario 4: Eve + Noise (Combined)
```
QBER: 25-35%
Security Status: COMPROMISED
Threat Level: HIGH
Recommendation: ABORT ⚠️
```

---

## Python API Usage

### Basic Usage
```python
from app.core.bb84_protocol import run_bb84_simulation

# Run simulation
result = run_bb84_simulation(
    num_qubits=1000,
    eve_active=False,
    noise_active=False,
    seed=42
)

# Check results
print(f"QBER: {result.qber_result.error_percentage:.2f}%")
print(f"Secure: {result.is_secure}")
print(f"Sifted key: {result.sifted_key.shape[0]} bits")
```

### With Eve Attack
```python
result = run_bb84_simulation(
    num_qubits=2000,
    eve_active=True,
    seed=42
)
print(f"Eve detected: {result.qber_result.error_percentage > 11}")
```

### Export Results
```python
from app.utils.exporters import ExportManager

manager = ExportManager()
exports = manager.export_all(result)
# Returns: {'csv': '...', 'json': '...', 'text': '...'}
```

### Generate Visualizations
```python
from app.visualization.charts import BB84Visualizer

visualizer = BB84Visualizer()
plots = visualizer.create_summary_visualization(result)
# Saves to outputs/graphs/
```

---

## Project Structure

```
bb84-qkd-simulator/
├── main.py                 # CLI entry point ✓
├── examples.py             # 7 demonstrations ✓
├── conftest.py             # pytest configuration ✓ (NEW)
├── requirements.txt        # Dependencies
├── README.md               # Full documentation
├── QUICK_REF.md            # Quick reference
├── FIXES_APPLIED.md        # This document
│
├── app/
│   ├── core/               # Protocol engine ✓
│   ├── visualization/      # Plotting ✓
│   ├── gui/               # GUI interface ✓
│   ├── utils/             # Utilities ✓
│   └── config/            # Configuration ✓
│
├── tests/
│   └── test_bb84.py        # 23 tests, all passing ✓
│
└── outputs/
    ├── csv/               # Generated data
    ├── reports/           # Exported reports
    ├── graphs/            # Visualization plots
    └── logs/              # Simulation logs
```

---

## File Modifications Summary

### Fixed Files
1. **app/core/qubit.py** - Removed escape sequence error
2. **app/core/bb84_protocol.py** - Fixed QBER calculation
3. **tests/test_bb84.py** - Fixed test expectations
4. **examples.py** - Removed invalid parameters

### New Files
5. **conftest.py** - Created for pytest path configuration

---

## Troubleshooting

### If tests fail to import
```bash
# Make sure you're in the project root
cd /Users/sasank.kotra/CNS_lab/bb84-qkd-simulator

# Run pytest from here
pytest tests/test_bb84.py -v
```

### If main.py won't run
```bash
# Check Python version (should be 3.8+)
python --version

# Verify dependencies
pip install -r requirements.txt

# Try a simple test
python -c "from app.core.bb84_protocol import BB84Protocol; print('✓ Imports working')"
```

### If plots not showing
```bash
# Update matplotlib
pip install --upgrade matplotlib

# Try regenerating
python main.py --visualize
```

---

## Next Steps

1. ✅ Run basic simulation: `python main.py`
2. ✅ Test Eve detection: `python main.py --eve`
3. ✅ Run examples: `python examples.py`
4. ✅ Run tests: `pytest tests/test_bb84.py -v`
5. ✅ Export results: `python main.py --export`
6. ✅ Generate plots: `python main.py --visualize`
7. ✅ Try GUI: `python main.py --gui`

---

## Summary

🎉 **All systems GO!**

- ✅ Simulator fully functional
- ✅ All tests passing
- ✅ All features working
- ✅ Ready for use

**Start with**: `python main.py`

---

**For detailed documentation, see README.md**
