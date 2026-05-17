# BB84 Quantum Key Distribution Simulator

A production-quality academic simulation platform for the **BB84 Quantum Key Distribution (QKD) protocol** in Python.

This project demonstrates secure quantum communication, eavesdropping detection, and security analysis through an interactive simulator that is:

- **Scientifically Accurate**: Implements the BB84 protocol with realistic quantum measurement behavior
- **Educational**: Clear code structure, comprehensive comments, and explanatory visualizations
- **Modular**: Clean separation of concerns with independent, reusable components
- **Extensible**: Designed for future extensions (BB92, E91, noise models, etc.)
- **Production-Ready**: Type hints, logging, error handling, and comprehensive testing

---

## 🎯 Quick Start

### Installation

```bash
# Clone or navigate to project directory
cd bb84-qkd-simulator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Simulator

**CLI Mode (Default):**
```bash
# Run with default parameters (1000 qubits, no attacks)
python main.py

# Simulate Eve's intercept-resend attack
python main.py --eve

# Add 5% channel noise
python main.py --noise 0.05

# Both Eve and noise
python main.py --eve --noise 0.05 --eve-prob 0.8

# Export results
python main.py --export --visualize

# Use reproducible random seed
python main.py --seed 42 --qubits 5000

# Launch GUI (Tkinter)
python main.py --gui
```

**Python API:**
```python
from app.core.bb84_protocol import run_bb84_simulation

# Run simulation
result = run_bb84_simulation(
    num_qubits=1000,
    eve_active=True,
    noise_active=True,
    noise_prob=0.05,
    seed=42
)

# Access results
print(f"QBER: {result.qber_result.error_percentage:.2f}%")
print(f"Secure: {result.security_analysis.threat_level}")
print(f"Sifted key length: {result.sifted_key.shape[0]}")
```

---

## 📋 Usage Examples

### Example 1: Normal Secure Channel

```bash
python main.py --qubits 2000 --verbose
```

Expected output:
- QBER: ~1% (measurement noise only)
- Security Status: SECURE
- Key Efficiency: ~50%

### Example 2: Eve Attack Detection

```bash
python main.py --qubits 2000 --eve --seed 42
```

Expected output:
- QBER: ~12.5% (Eve introduces errors)
- Security Status: COMPROMISED
- Eve Detection: Successful
- Sifted key compromised

### Example 3: Noisy Channel

```bash
python main.py --qubits 2000 --noise 0.05
```

Expected output:
- QBER: ~5-8% (channel noise)
- Security Status: POSSIBLY COMPROMISED or SECURE (borderline)
- Channel quality issues detected

### Example 4: Combined Challenges

```bash
python main.py --qubits 5000 --eve --noise 0.03 --eve-prob 0.7 --export --visualize
```

---

## 🏗️ Architecture

### Project Structure

```
bb84-qkd-simulator/
│
├── app/
│   ├── core/                    # Core protocol implementation
│   │   ├── bb84_protocol.py    # Main BB84 engine
│   │   ├── qubit.py            # Quantum bit abstraction
│   │   ├── basis.py            # Rectilinear/Diagonal bases
│   │   ├── quantum_channel.py  # Transmission with Eve/noise
│   │   ├── key_sifting.py      # Extract final key
│   │   ├── qber.py             # Quantum bit error rate
│   │   ├── eve_attack.py       # Eavesdropping simulation
│   │   ├── noise_model.py      # Channel noise
│   │   └── security_analysis.py # Threat assessment
│   │
│   ├── visualization/           # Plotting and charts
│   │   └── charts.py           # matplotlib visualizations
│   │
│   ├── gui/                     # Tkinter interface
│   │   └── main_window.py      # GUI application
│   │
│   ├── utils/                   # Utilities
│   │   ├── constants.py        # Protocol constants
│   │   ├── logger.py           # Logging setup
│   │   ├── exporters.py        # CSV/JSON/PDF export
│   │   └── validators.py       # Input validation
│   │
│   └── config/
│       └── settings.py          # Configuration objects
│
├── tests/                       # Comprehensive test suite  
│   └── test_bb84.py            # Unit and integration tests
│
├── outputs/                     # Generated files
│   ├── graphs/                 # Saved plots
│   ├── reports/                # Exported reports
│   ├── csv/                    # Raw data exports
│   └── logs/                   # Simulation logs
│
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── LICENSE                      # MIT license
```

### Core Components

#### 1. **Qubit** (`app/core/qubit.py`)
- Represents quantum bits with basis encoding
- Simulates quantum measurement collapse
- Correct measurement when basis matches
- Random outcome when basis mismatches

#### 2. **Basis** (`app/core/basis.py`)
- Rectilinear (+) and Diagonal (×) bases
- Basis matching for key sifting
- Efficiency calculations

#### 3. **BB84Protocol** (`app/core/bb84_protocol.py`)
- Main simulation engine
- Orchestrates entire protocol
- Manages Alice, Bob, Eve interactions
- Produces results and analysis

#### 4. **QuantumChannel** (`app/core/quantum_channel.py`)
- Simulates quantum transmission
- Optional Eve interception
- Optional channel noise
- Bit flip errors

#### 5. **KeySifting** (`app/core/key_sifting.py`)
- Extracts bits where bases matched
- Calculates efficiency
- Prepares data for QBER

#### 6. **QBER** (`app/core/qber.py`)
- Calculates Quantum Bit Error Rate
- Determines security status
- Estimates Eve presence probability
- Privacy amplification calculations

#### 7. **SecurityAnalysis** (`app/core/security_analysis.py`)
- Comprehensive threat assessment
- Statistical analysis
- Recommendations generation
- Scenario comparison

---

## 🔬 BB84 Protocol Theory

### Protocol Steps

1. **Alice generates random bits**: `[1,0,1,1,0,1,...]`

2. **Alice generates random bases**: `[+,×,+,×,...] `
   - `+` = Rectilinear (0)
   - `×` = Diagonal (1)

3. **Alice encodes qubits**:
   - (bit=1, basis=+) → Vertical polarization
   - (bit=0, basis=+) → Horizontal polarization
   - (bit=1, basis=×) → Diagonal up-left
   - (bit=0, basis=×) → Diagonal down-right

4. **Quantum transmission**:
   - Optional Eve interception
   - Optional channel noise

5. **Bob measures qubits**:
   - Chooses random basis for each qubit
   - Measures in that basis
   - **If basis matches**: Gets correct bit
   - **If basis differs**: Gets random result

6. **Basis sifting**:
   - Alice and Bob publicly compare bases (NOT bits)
   - Keep only bits where bases matched
   - ~50% of bits retained

7. **QBER calculation**:
   - Publicly compare a subset of sifted bits
   - Calculate error rate
   - If QBER > 11%: Eavesdropping likely detected
   - If QBER < 11%: Channel appears secure

### Security Properties

- **No eavesdropping**: QBER ≈ 0-1% (quantum measurement noise)
- **Eve present**: QBER ≈ 12.5% (Eve wrong basis ≈ 50% of time)
- **Channel noise**: QBER ≈ noise_probability × 100%
- **Threshold**: QBER > 11% indicates problem

---

## 📊 Simulation Output

### Console Output
```
==================================================
BB84 QUANTUM KEY DISTRIBUTION SIMULATION
==================================================

Protocol Configuration:
  Total Qubits:        1000
  Eve Active:          False
  Noise Active:        False

Results:
  Matched Bases:       513/1000
  Sifted Key Length:   513 bits
  Key Efficiency:      51.3%

Security Analysis:
  QBER:                1.17%
  Security Status:     SECURE
  Threat Level:        LOW
  Eve Probability:     0.0%

==================================================
```

### Exported Files

1. **CSV File** (`outputs/csv/bb84_*.csv`)
   - Row per qubit with complete data
   - Alice bits, bases, measurements
   - Bob bases, measurements, errors
   - Eve data (if present)

2. **JSON Summary** (`outputs/reports/bb84_*_summary.json`)
   - Configuration
   - Key metrics
   - Security assessment
   - Recommendations

3. **Text Report** (`outputs/reports/bb84_*_report.txt`)
   - Human-readable summary
   - Detailed analysis
   - Recommendations

4. **Plots** (`outputs/graphs/`)
   - QBER summary chart
   - Basis distribution pie chart  
   - Key length analysis

---

## 🧪 Testing

Run comprehensive test suite:

```bash
cd bb84-qkd-simulator
pytest tests/test_bb84.py -v

# With coverage report
pytest tests/test_bb84.py --cov=app --cov-report=html
```

Test coverage:
- ✅ Bit and basis generation
- ✅ Qubit encoding/measurement
- ✅ Key sifting logic
- ✅ QBER calculations
- ✅ Eve attack simulation
- ✅ Noise handling
- ✅ Security analysis
- ✅ Protocol reproducibility
- **Target**: 85%+ coverage

---

## 🎨 Visualization

### Available Plots

1. **QBER vs Qubit Count**
   - Shows QBER convergence
   - Security threshold line
   - Secure/compromised regions

2. **Eve Attack Comparison**
   - Normal transmission QBER
   - Intercept-resend attack QBER
   - Difference visualization

3. **Basis Match Distribution**
   - Pie chart of matched/mismatched
   - Expected ~50% match rate

4. **Secure Key Length Analysis**
   - Original bits
   - After sifting
   - After privacy amplification

5. **Noise Impact**
   - QBER at different noise levels
   - Threshold crossings

Generate all plots:
```bash
python main.py --qubits 5000 --visualize
```

---

## ⚙️ Configuration

### SimulationConfig

```python
from app.config.settings import SimulationConfig

config = SimulationConfig(
    num_qubits=1000,              # Qubits to transmit
    random_seed=42,               # For reproducibility
    eve_active=False,             # Eve intercept-resend
    eve_intercept_probability=1.0,# Fraction Eve intercepts
    noise_active=False,           # Channel noise
    noise_probability=0.05,       # Bit flip rate
)
```

### Visualization Config

```python
from app.config.settings import visualization_config

visualization_config.figure_dpi = 120
visualization_config.export_dpi = 300
visualization_config.style = "seaborn-v0_8-darkgrid"
```

---

## 🔐 Security Analysis

### Threat Levels

| QBER | Status | Threat Level | Action |
|------|--------|--------------|--------|
| < 3% | Good | LOW | Proceed |
| 3-11% | Acceptable | LOW | Proceed with caution |
| 11-16% | Warning | MEDIUM | Investigate |
| > 16% | Danger | HIGH | ABORT |

### Eve Detection

```python
eve_detected, confidence = detect_eve_from_qber(qber_result.error_percentage)
```

- Confidence increases with QBER above threshold
- Statistical analysis across multiple runs improves detection

### Privacy Amplification

Secure key rate after privacy amplification:

$$R_{secure} = R_{raw} \times (1 - 2H(QBER))$$

where $H(x) = -x\log_2(x) - (1-x)\log_2(1-x)$

---

## 📚 Academic Background

### BB84 Protocol
- **Proposed**: Charles Bennett & Gilles Brassard, 1984
- **Principle**: Quantum mechanics prevents eavesdropping without detection
- **Security**: Unconditional security (information-theoretic)

### Key Concepts
- **Quantum superposition**: Qubits exist in multiple states
- **Measurement collapse**: Measuring changes quantum state
- **Basis incompleteness**: Two bases are mutually unbiased
- **Eavesdropping detection**: Eve's measurements introduce detectable errors

### Quantum Measurement Rules
1. Measure in correct basis → Always get original bit
2. Measure in wrong basis → Random result (50-50)
3. Eve's wrong basis measurement collapses qubit to random state

---

## 🚀 Advanced Features

### Multi-Scenario Analysis

```python
from app.core.bb84_protocol import run_bb84_simulation

scenarios = {
    'clean': run_bb84_simulation(num_qubits=1000, eve_active=False),
    'eve': run_bb84_simulation(num_qubits=1000, eve_active=True),
    'noise': run_bb84_simulation(num_qubits=1000, noise_active=True, noise_prob=0.05),
    'combined': run_bb84_simulation(num_qubits=1000, eve_active=True, noise_active=True),
}

# Compare QBER across scenarios
for name, result in scenarios.items():
    print(f"{name}: QBER = {result.qber_result.error_percentage:.2f}%")
```

### Statistical Analysis

```python
from app.core.security_analysis import statistical_qber_analysis

qber_measurements = [1.2, 1.3, 1.5, 1.1, 1.4]  # Multiple runs
stats = statistical_qber_analysis(qber_measurements)

print(f"Mean QBER: {stats['mean_qber']:.2f}%")
print(f"Confidence interval: {stats['confidence_interval']}")
```

---

## 🧩 Extensibility

### Adding New Features

1. **New Protocol** (e.g., BB92):
   - Create `app/core/bb92_protocol.py`
   - Reuse `Qubit`, `QuantumChannel` components
   - Implement protocol-specific logic

2. **New Noise Model**:
   - Extend `app/core/noise_model.py`
   - Add realistic physical effects
   - Call from `quantum_channel.py`

3. **Advanced Visualization**:
   - Add methods to `app/visualization/charts.py`
   - Use matplotlib for 2D, matplotlib3d for 3D
   - Save to `outputs/graphs/`

### Example: Custom Attack

```python
from app.core.qubit import Qubit
from typing import List

def eve_phase_encode_attack(qubits: List[Qubit]):
    """
    Custom Eve attack: phase encoding modifications.
    """
    # Implement phase-based attack
    modified = []
    for qubit in qubits:
        # Custom logic here
        modified.append(qubit)
    return modified
```

---

## 🐛 Debugging

### Enable Verbose Logging

```bash
python main.py --verbose
```

### Check Logs

```bash
tail -f outputs/logs/bb84_simulation.log
```

### Debug in Python

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from app.core.bb84_protocol import BB84Protocol
from app.config.settings import SimulationConfig

config = SimulationConfig(num_qubits=100, random_seed=42)
protocol = BB84Protocol(config)
result = protocol.run_simulation()
```

---

## 📦 Dependencies

- **numpy** (≥1.24.0): Numerical computing
- **matplotlib** (≥3.8.0): Visualization
- **scipy** (≥1.12.0): Scientific computing
- **pytest** (≥7.4.0): Testing framework
- **pytest-cov** (≥4.1.0): Code coverage

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Photon polarization animation**
2. **Bell state measurement**
3. **E91 protocol implementation**  
4. **Decoy state method**
5. **Web interface (Flask/FastAPI)**
6. **Additional noise models**
7. **Performance optimization for 1M+ qubits**

---

## 📞 Support & References

### References
- Bennett & Brassard (1984): "Quantum cryptography: Public key distribution and coin tossing"
- Shor & Preskill (2000): "Simple proof of security of the BB84 quantum key distribution protocol"
- Bruss (1998): "Optimal eavesdropping in quantum cryptography with six states"

### External Links
- [Quantum Key Distribution on Wikipedia](https://en.wikipedia.org/wiki/Quantum_key_distribution)
- [BB84 Protocol Details](https://en.wikipedia.org/wiki/BB84)
- [NIST PQC](https://csrc.nist.gov/projects/post-quantum-cryptography)

---

## 🎓 Educational Use

This simulator is ideal for:
- Quantum information courses
- Cryptography workshops  
- Security demonstrations
- Academic research prototypes
- Public engagement

### Classroom Activity
1. Configure basic simulation (1000 qubits, no attacks)
2. Observe: ~50% key efficiency, QBER ~1%
3. Enable Eve, observe QBER jump to ~12.5%
4. Discuss security implications
5. Compare with other protocols

---

## 🔮 Future Roadmap

- [ ] Interactive quantum state visualization
- [ ] Real-time live simulation dashboard
- [ ] Cloud deployment option
- [ ] GPU acceleration for 10M+ qubit simulations
- [ ] Alternative protocols (E91, BB92, COW)
- [ ] Machine learning attack detection
- [ ] Web-based interface

---

**Built with ❤️ for quantum cryptography education and research**
