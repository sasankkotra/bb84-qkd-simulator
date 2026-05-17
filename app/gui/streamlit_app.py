"""
Streamlit UI for BB84 QKD Simulator

Run with:

    pip install -r requirements.txt
    streamlit run app/gui/streamlit_app.py

This UI lets users enter parameters interactively (number of qubits, seed,
Eve active, noise settings) and run the simulation. It also shows results,
creates summary visualizations, and provides export/download buttons.
"""

import sys
from pathlib import Path

# Add project root to path so Streamlit can find app module
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st

from app.core.bb84_protocol import run_bb84_simulation, BB84Protocol
from app.visualization.charts import BB84Visualizer
from app.utils.exporters import ExportManager


def sidebar_inputs():
    st.sidebar.header("Simulation Parameters")
    num_qubits = st.sidebar.number_input("Number of qubits", min_value=10, max_value=100000, value=1000, step=10)
    seed = st.sidebar.number_input("Random seed (optional, 0 means None)", min_value=0, value=42)
    if seed == 0:
        seed = None

    eve_active = st.sidebar.checkbox("Enable Eve (intercept-resend)", value=False)
    noise_active = st.sidebar.checkbox("Enable channel noise", value=False)
    noise_prob = st.sidebar.slider("Noise probability", min_value=0.0, max_value=0.5, value=0.05, step=0.01)

    st.sidebar.markdown("---")
    st.sidebar.header("Output Options")
    do_export = st.sidebar.checkbox("Export results (CSV/JSON/Text)", value=False)
    create_plots = st.sidebar.checkbox("Create summary plots", value=True)

    return {
        'num_qubits': int(num_qubits),
        'seed': seed,
        'eve_active': eve_active,
        'noise_active': noise_active,
        'noise_prob': float(noise_prob),
        'do_export': do_export,
        'create_plots': create_plots,
    }


def display_result(result, params):
    """Display simulation result, metrics, visualizations, and exports."""
    protocol = BB84Protocol()  # for using get_summary() convenience
    summary_text = protocol.get_summary(result)

    st.subheader("Simulation Summary")
    st.code(summary_text)

    # Key metrics
    qber = result.qber_result.error_percentage
    sifted_len = int(result.sifted_key.shape[0])
    matched = int(len(result.matched_indices))

    col1, col2, col3 = st.columns(3)
    col1.metric("QBER (%)", f"{qber:.2f}")
    col2.metric("Matched bases", f"{matched}/{params['num_qubits']}")
    col3.metric("Sifted key length", f"{sifted_len} bits")

    # Visualizations
    vis = BB84Visualizer()
    if params['create_plots']:
        st.subheader("Visualizations")
        plots = vis.create_summary_visualization(result, output_dir="outputs/graphs/")
        for name, path in plots.items():
            if Path(path).exists():
                st.image(path, caption=name)

    # Exports
    if params['do_export']:
        st.subheader("Export Results")
        exporter = ExportManager(output_dir="outputs/")
        exported = exporter.export_all(result)

        for fmt, path in exported.items():
            p = Path(path)
            if p.exists():
                with open(p, 'rb') as f:
                    data = f.read()
                st.download_button(label=f"Download {fmt.upper()}", data=data, file_name=p.name)

    st.success("Simulation complete.")


def run_preset(preset_name):
    """Run a preset scenario and display results."""
    params = {
        'num_qubits': 1000,
        'seed': 42,
        'eve_active': False,
        'noise_active': False,
        'noise_prob': 0.05,
        'do_export': True,
        'create_plots': True,
    }

    preset_configs = {
        'Secure Channel': {
            'num_qubits': 1000,
            'eve_active': False,
            'noise_active': False,
            'noise_prob': 0.0,
            'description': 'Clean quantum channel with no attacks or noise.',
        },
        'Eve Attack': {
            'num_qubits': 1000,
            'eve_active': True,
            'noise_active': False,
            'noise_prob': 0.0,
            'description': 'Eve performs intercept-resend attack. QBER should spike to ~25%.',
        },
        'Noisy Channel (5%)': {
            'num_qubits': 1000,
            'eve_active': False,
            'noise_active': True,
            'noise_prob': 0.05,
            'description': '5% channel noise. QBER ~5%, but still SECURE.',
        },
        'Eve + Noise': {
            'num_qubits': 2000,
            'eve_active': True,
            'noise_active': True,
            'noise_prob': 0.03,
            'description': 'Combined attack: Eve intercepts + 3% channel noise.',
        },
        'High-Noise (10%)': {
            'num_qubits': 1000,
            'eve_active': False,
            'noise_active': True,
            'noise_prob': 0.10,
            'description': '10% channel noise approaching security threshold.',
        },
        'Dense Protocol (5000 qubits)': {
            'num_qubits': 5000,
            'eve_active': False,
            'noise_active': False,
            'noise_prob': 0.0,
            'description': 'Large qubit count for statistical stability.',
        },
        'Quick Demo (100 qubits)': {
            'num_qubits': 100,
            'eve_active': False,
            'noise_active': False,
            'noise_prob': 0.0,
            'description': 'Fast simulation for testing. ~50 bits in sifted key.',
        },
    }

    if preset_name not in preset_configs:
        st.error(f"Unknown preset: {preset_name}")
        return

    config = preset_configs[preset_name]
    st.info(f"**{preset_name}**: {config['description']}")

    with st.spinner(f"Running {preset_name}..."):
        result = run_bb84_simulation(
            num_qubits=config['num_qubits'],
            eve_active=config['eve_active'],
            noise_active=config['noise_active'],
            noise_prob=config['noise_prob'],
            seed=42
        )

    display_result(result, params)


def main():
    st.title("BB84 QKD Simulator — Interactive")
    st.write(
        "Interactive BB84 Quantum Key Distribution simulator. Choose a preset scenario or configure custom parameters."
    )

    tab1, tab2 = st.tabs(["Quick Presets", "Custom Simulation"])

    with tab1:
        st.subheader("Preset Scenarios")
        st.write("Click any button to run a pre-configured scenario.")

        preset_cols = st.columns(2)
        presets = [
            'Secure Channel',
            'Eve Attack',
            'Noisy Channel (5%)',
            'Eve + Noise',
            'High-Noise (10%)',
            'Dense Protocol (5000 qubits)',
            'Quick Demo (100 qubits)',
        ]

        for i, preset in enumerate(presets):
            col = preset_cols[i % 2]
            if col.button(preset, key=f"preset_{preset}", use_container_width=True):
                run_preset(preset)

    with tab2:
        st.subheader("Custom Parameters")
        st.markdown("**Input guidance**")
        st.markdown(
            "- `Number of qubits`: higher values give more stable QBER estimates (try 1000+). "
            "For quick demos use 100–500.\n"
            "- `Random seed`: integer for reproducible results; 0 = random seed.\n"
            "- `Enable Eve`: simulates intercept-resend attacker (introduces ~25% QBER).\n"
            "- `Enable channel noise`: simulates independent bit-flips with chosen probability."
        )

        params = sidebar_inputs()
        run = st.button("Run Custom Simulation")

        if run:
            with st.spinner("Running BB84 simulation..."):
                result = run_bb84_simulation(
                    num_qubits=params['num_qubits'],
                    eve_active=params['eve_active'],
                    noise_active=params['noise_active'],
                    noise_prob=params['noise_prob'],
                    seed=params['seed']
                )

            display_result(result, params)


if __name__ == "__main__":
    main()
