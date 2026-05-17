# Streamlit Interactive GUI

## Quick Start

### Installation

1. Install dependencies (if not already done):
```bash
pip install -r requirements.txt
```

2. Launch the UI:
```bash
streamlit run app/gui/streamlit_app.py
```

The UI will open in your browser at `http://localhost:8501`.

---

## Using the UI

The Streamlit interface has **two tabs**: Quick Presets and Custom Simulation.

### Tab 1: Quick Presets

Click any button to instantly run a pre-configured scenario:

| Preset | Qubits | Config | Use Case |
|--------|--------|--------|----------|
| **Secure Channel** | 1000 | No Eve, no noise | Baseline clean run |
| **Eve Attack** | 1000 | Eve intercepts | See high QBER (~25%) |
| **Noisy Channel (5%)** | 1000 | 5% bit-flip noise | Real-world channel simulation |
| **Eve + Noise** | 2000 | Eve + 3% noise | Combined threat scenario |
| **High-Noise (10%)** | 1000 | 10% bit-flip noise | Extreme noise tolerance test |
| **Dense Protocol (5000 qubits)** | 5000 | Large scale | Verify statistical stability |
| **Quick Demo (100 qubits)** | 100 | Fast run | Quick testing & learning |

Each preset runs with `seed=42` for reproducibility.

### Tab 2: Custom Simulation

Configure your own parameters using the sidebar and run a custom simulation.

#### Input Parameters

**Simulation Settings (Sidebar):**
- **Number of qubits** (10–100,000)
  - *Lower*: 100–500 for quick demos
  - *Higher*: 1000+ for stable QBER estimates
  - *Interactive*: Click run multiple times to see variance decrease

- **Random seed** (integer or 0)
  - *Non-zero*: Creates reproducible results
  - *0*: Uses a random seed each time
  - *Common*: Use 42 for consistent demos

- **Enable Eve** (checkbox)
  - When checked: Eve intercepts and resends all qubits
  - Expected QBER: ~25% (detector about ½ of qubits with wrong basis)
  - Security status: COMPROMISED (threat level HIGH)

- **Enable channel noise** (checkbox)
  - When checked: Applies independent bit-flip to each qubit
  - Noise probability: Control with slider

- **Noise probability** (0.0–0.5)
  - 0.05 = 5% (typical realistic channel)
  - 0.10 = 10% (high-quality fiber or free-space link)
  - 0.20+ = Severely degraded link

**Output Options (Sidebar):**
- **Export results (CSV/JSON/Text)**: Toggles file exports to `outputs/`
- **Create summary plots**: Toggles visualization generation

---

## Understanding the Output

### 📊 Simulation Summary
Text-based summary showing:
- Total qubits sent
- Eve active / noise active status
- Matched bases count
- Sifted key length & efficiency
- QBER value
- Security status (SECURE / COMPROMISED)
- Threat level (LOW / MEDIUM / HIGH)

### 📈 Key Metrics (Three Columns)
- **QBER (%)**: Quantum Bit Error Rate
  - < 11% → **SECURE** (no detectable attack)
  - ≥ 11% → **COMPROMISED** (eavesdropper likely)
- **Matched bases**: Count / total qubits (~50% expected)
- **Sifted key length**: Secure bits extracted

### 📉 Visualizations (If enabled)

Three plots are generated:

1. **QBER Summary**: Bar chart showing QBER with security threshold
2. **Basis Distribution**: Pie & bar charts of matched vs. mismatched bases
3. **Secure Key Length**: Waterfall showing bits lost through sifting & authentication

### 💾 Export Files (If enabled)

Three formats are created in `outputs/`:

**CSV** (`outputs/csv/`):
- Row per qubit with: index, Alice bit, basis (+ or ×), Bob basis, Bob measurement, match, error flag
- Useful for external analysis, plotting, or research

**JSON** (`outputs/reports/`):
- Machine-readable summary: config, results, security info, recommendations
- Ideal for programmatic access

**Text Report** (`outputs/reports/`):
- Human-readable report with full analysis & recommendations
- Print-friendly format

---

## Example Workflows

### Workflow 1: Understand Eve Detection

1. Click **Secure Channel** preset → note QBER ~0%
2. Click **Eve Attack** preset → QBER jumps to ~25%
3. Compare: Eve's attack is immediately visible!

### Workflow 2: Explore Noise vs. Eve

1. Set custom: **1000 qubits, no Eve, 5% noise** → Run
   - QBER ~5%, Status: SECURE
2. Set custom: **1000 qubits, Eve on, no noise** → Run
   - QBER ~25%, Status: COMPROMISED
3. Set custom: **1000 qubits, Eve on, 3% noise** → Run
   - QBER ~28%, Status: COMPROMISED

→ *Insight*: Eve's effect dominates and is easily distinguished from noise.

### Workflow 3: Verify Protocol Properties

1. Run **Secure Channel** twice with seed 42 → Same QBER (reproducible)
2. Run **Secure Channel** once with seed 0 → Different QBER (random)
3. Try **Dense Protocol (5000 qubits)** → QBER very close to 0% (statistical stability)

---

## Input Guidance & Tips

| Scenario | Qubits | Eve | Noise | Seed | Expected QBER |
|----------|--------|-----|-------|------|----------------|
| **Learning** | 100 | ✗ | ✗ | 42 | ~0% (varies) |
| **Demo** | 1000 | ✗ | ✗ | 42 | ~0% (stable) |
| **Eve Demo** | 1000 | ✓ | ✗ | 42 | ~25% |
| **Realistic** | 1000 | ✗ | ✓ (0.05) | 0 | ~5% |
| **Challenge** | 2000 | ✓ | ✓ (0.03) | 42 | ~28% |
| **Large Scale** | 10000 | ✗ | ✗ | 0 | ~0% (tighter) |

### When to Use Random Seed (0)

- **Stress testing**: Run multiple times to see variance
- **Real-world simulation**: Each run is independent (like real quantum)
- **Learning**: See realistic QBER fluctuations

### When to Use Fixed Seed (e.g., 42)

- **Demos**: Show consistent, reproducible results
- **Debugging**: Isolate changes to parameters only
- **Classroom**: Same result every time for all students

---

## Common Questions

### Q: Why does QBER vary each run?
**A**: Without Eve or noise, quantum basis errors are random. Run for 1000+ qubits to stabilize around 0%. With Eve, QBER stays ~25% (stable). With noise, QBER ≈ noise probability.

### Q: How do I know if Eve is present?
**A**: Check QBER:
- < 11% → **Probably not** (SECURE)
- ≥ 11% & ≤ 20% → **Possibly** (noise vs. eve ambiguous)
- ≥ 20% → **Definitely** (COMPROMISED)

### Q: What's a "sifted key"?
**A**: After Alice & Bob compare bases publicly (not bits), they keep only bits where bases matched (~50%). This is the sifted key.

### Q: Can I export and use the key?
**A**: No—this is a simulator. Real BB84 would include additional privacy amplification & authentication steps. The exported key shows the algorithm output for educational purposes.

### Q: Why max 100K qubits?
**A**: To keep simulations interactive (< 30 seconds). For research, modify `number_input` range in `app/gui/streamlit_app.py`.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Run `streamlit run app/gui/streamlit_app.py --server.port 8502` |
| Plots not showing | Enable "Create summary plots" checkbox in sidebar |
| Export button grayed out | Enable "Export results (CSV/JSON/Text)" first |
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit` |
| `ModuleNotFoundError: app` | Run from project root: `cd /path/to/bb84-qkd-simulator/` |

---

## File Structure

```
app/gui/
├── streamlit_app.py          ← Main UI file (what you run)
└── main_window.py            ← Tkinter GUI (alternative)

outputs/
├── csv/                       ← Exported qubit-by-qubit data
├── reports/                   ← JSON summaries & text reports
└── graphs/                    ← PNG visualizations
```

---

## Extending the UI

Want to add more presets or customize? Edit `app/gui/streamlit_app.py`:

```python
# In run_preset(), add to preset_configs dict:
'My Scenario': {
    'num_qubits': 2000,
    'eve_active': True,
    'noise_active': True,
    'noise_prob': 0.02,
    'description': 'My custom setup description.',
}
```

Then click button to run!

---

## Performance Notes

- **100 qubits**: ~0.1 sec
- **1000 qubits**: ~1 sec
- **10,000 qubits**: ~10 sec
- **100,000 qubits**: ~100 sec

Streamlit reruns entire script on interaction, so reload time = simulation time + rendering.

---

## Related Documentation

- See [README.md](README.md) for protocol theory
- See [QUICK_REF.md](QUICK_REF.md) for API examples
- See [main.py](main.py) for CLI usage
