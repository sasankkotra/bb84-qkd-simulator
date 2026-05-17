"""
BB84 QKD Simulator - Example Script

This script demonstrates various use cases of the BB84 simulator.
Run with: python examples.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.bb84_protocol import BB84Protocol, run_bb84_simulation
from app.config.settings import SimulationConfig
from app.visualization.charts import BB84Visualizer
from app.utils.exporters import ExportManager


def example_1_basic_simulation():
    """Example 1: Basic simulation with default parameters."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic BB84 Simulation (1000 qubits, no attacks)")
    print("="*70)
    
    result = run_bb84_simulation(num_qubits=1000, seed=42)
    
    print(f"\nResults:")
    print(f"  QBER: {result.qber_result.error_percentage:.2f}%")
    print(f"  Sifted key length: {result.sifted_key.shape[0]} bits")
    print(f"  Security Status: {result.security_analysis.security_status}")
    print(f"  Threat Level: {result.security_analysis.threat_level}")
    

def example_2_eve_attack():
    """Example 2: Eve intercept-resend attack."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Eve Intercept-Resend Attack (1000 qubits)")
    print("="*70)
    
    result = run_bb84_simulation(
        num_qubits=1000,
        eve_active=True,
        seed=42
    )
    
    print(f"\nResults:")
    print(f"  QBER: {result.qber_result.error_percentage:.2f}%")
    print(f"  Eve Detected: {result.qber_result.error_percentage > 11}")
    print(f"  Security Status: {result.security_analysis.security_status}")
    print(f"  Eve Probability: {result.security_analysis.eve_probability:.1%}")
    

def example_3_noisy_channel():
    """Example 3: Noisy quantum channel."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Noisy Channel (5% noise, 1000 qubits)")
    print("="*70)
    
    result = run_bb84_simulation(
        num_qubits=1000,
        noise_active=True,
        noise_prob=0.05,
        seed=42
    )
    
    print(f"\nResults:")
    print(f"  QBER: {result.qber_result.error_percentage:.2f}%")
    print(f"  Likely cause: Channel noise")
    print(f"  Security Status: {result.security_analysis.security_status}")
    

def example_4_combined_challenges():
    """Example 4: Both Eve and noise."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Combined Challenges (Eve + 3% Noise, 2000 qubits)")
    print("="*70)
    
    result = run_bb84_simulation(
        num_qubits=2000,
        eve_active=True,
        noise_active=True,
        noise_prob=0.03,
        seed=42
    )
    
    print(f"\nResults:")
    print(f"  QBER: {result.qber_result.error_percentage:.2f}%")
    print(f"  Sifted key: {result.sifted_key.shape[0]} bits")
    print(f"  Security Status: {result.security_analysis.security_status}")
    

def example_5_statistical_comparison():
    """Example 5: Compare multiple scenarios statistically."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Statistical Comparison of Scenarios")
    print("="*70)
    
    scenarios = {
        'Secure Channel': run_bb84_simulation(num_qubits=1000, seed=42),
        'With Eve': run_bb84_simulation(num_qubits=1000, eve_active=True, seed=42),
        'With Noise': run_bb84_simulation(num_qubits=1000, noise_active=True, noise_prob=0.05, seed=42),
        'Eve + Noise': run_bb84_simulation(num_qubits=1000, eve_active=True, noise_active=True, noise_prob=0.03, seed=42),
    }
    
    print(f"\nScenario Comparison:")
    print(f"{'Scenario':<20} {'QBER':<12} {'Status':<20} {'Threat'}")
    print("-" * 70)
    
    for name, result in scenarios.items():
        qber = result.qber_result.error_percentage
        status = result.security_analysis.security_status
        threat = result.security_analysis.threat_level
        print(f"{name:<20} {qber:>7.2f}%     {status:<20} {threat}")


def example_6_export_results():
    """Example 6: Export and visualize results."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Export Results to Files")
    print("="*70)
    
    result = run_bb84_simulation(num_qubits=1000, eve_active=True, seed=42)
    
    # Export to multiple formats
    manager = ExportManager(output_dir='outputs')
    exports = manager.export_all(result)
    
    print(f"\nExported files:")
    for format_name, filepath in exports.items():
        print(f"  • {format_name}: {filepath}")
    
    # Generate visualizations
    visualizer = BB84Visualizer()
    plots = visualizer.create_summary_visualization(result, 'outputs/graphs/')
    
    print(f"\nGenerated plots:")
    for plot_name, filepath in plots.items():
        print(f"  • {plot_name}: {filepath}")


def example_7_protocol_walkthrough():
    """Example 7: Detailed protocol walkthrough."""
    print("\n" + "="*70)
    print("EXAMPLE 7: BB84 Protocol Walkthrough")
    print("="*70)
    
    config = SimulationConfig(
        num_qubits=10,  # Small for readability
        random_seed=42
    )
    
    protocol = BB84Protocol(config)
    result = protocol.run_simulation()
    
    print(f"\nDetailed Algorithm Steps:")
    print(f"\n1. Alice's bits and bases:")
    print(f"   Bits:  {' '.join(map(str, result.alice_bits[:20]))}")
    print(f"   Bases: {' '.join('+' if b==0 else '×' for b in result.alice_bases[:20])}")
    
    print(f"\n2. Bob's measurement bases:")
    print(f"   Bases: {' '.join('+' if b==0 else '×' for b in result.bob_bases[:20])}")
    
    print(f"\n3. Basis matching:")
    matches = result.alice_bases == result.bob_bases
    print(f"   Match: {' '.join('✓' if m else '✗' for m in matches[:20])}")
    
    print(f"\n4. Key sifting:")
    print(f"   Matched positions: {list(result.matched_indices[:10])}")
    print(f"   Sifted key (first 20): {' '.join(map(str, result.sifted_key[:20]))}")
    
    print(f"\n5. Security Analysis:")
    print(f"   QBER: {result.qber_result.error_percentage:.2f}%")
    print(f"   Status: {result.security_analysis.security_status}")


def main():
    """Run all examples."""
    
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  BB84 QUANTUM KEY DISTRIBUTION SIMULATOR - EXAMPLES".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        example_1_basic_simulation()
        example_2_eve_attack()
        example_3_noisy_channel()
        example_4_combined_challenges()
        example_5_statistical_comparison()
        example_6_export_results()
        example_7_protocol_walkthrough()
        
        print("\n" + "="*70)
        print("All examples completed successfully!")
        print("="*70)
        
        print("\nNext steps:")
        print("  • Review generated files in outputs/")
        print("  • Modify parameters in examples.py and re-run")
        print("  • Run tests: pytest tests/test_bb84.py -v")
        print("  • Launch GUI: python main.py --gui")
        print("  • See README.md for detailed documentation")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
