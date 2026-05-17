"""
BB84 Quantum Key Distribution Simulator - Main Entry Point

A complete simulation platform for the BB84 quantum key distribution protocol,
demonstrating quantum communication security and eavesdropping detection.

Usage:
    python main.py                    # Run with default parameters
    python main.py --help             # Show help
    python main.py --qubits 5000      # Run with 5000 qubits
    python main.py --eve              # Include Eve's attack
    python main.py --noise 0.05       # Include 5% channel noise
"""

import argparse
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.bb84_protocol import BB84Protocol, run_bb84_simulation
from app.config.settings import simulation_config
from app.utils.exporters import ExportManager
from app.visualization.charts import BB84Visualizer
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


def main():
    """Main entry point."""
    
    parser = argparse.ArgumentParser(
        description="BB84 Quantum Key Distribution Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                      # Default 1000 qubits, no Eve, no noise
  python main.py --qubits 5000        # Simulate with 5000 qubits
  python main.py --eve                # Enable Eve intercept-resend attack
  python main.py --noise 0.05         # 5%% channel noise (bit flip probability)
  python main.py --eve --noise 0.02   # Both Eve and noise
  python main.py --seed 42            # Reproducible results
  python main.py --export             # Export results to CSV/JSON
  python main.py --gui                # Launch GUI (alpha)
        """
    )
    
    parser.add_argument(
        '--qubits', type=int, default=1000,
        help='Number of qubits to transmit (default: 1000)'
    )
    parser.add_argument(
        '--eve', action='store_true',
        help='Enable Eve intercept-resend attack'
    )
    parser.add_argument(
        '--eve-prob', type=float, default=1.0,
        help='Probability Eve intercepts each qubit (0.0-1.0, default: 1.0)'
    )
    parser.add_argument(
        '--noise', type=float, default=0.0,
        help='Channel noise probability (bit flip, 0.0-1.0, default: 0.0)'
    )
    parser.add_argument(
        '--seed', type=int, default=None,
        help='Random seed for reproducibility (default: None)'
    )
    parser.add_argument(
        '--export', action='store_true',
        help='Export results to CSV, JSON, and text files'
    )
    parser.add_argument(
        '--export-dir', type=str, default='outputs',
        help='Directory for exports (default: outputs)'
    )
    parser.add_argument(
        '--visualize', action='store_true',
        help='Generate visualization plots'
    )
    parser.add_argument(
        '--gui', action='store_true',
        help='Launch GUI interface'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Configure simulation
    simulation_config.num_qubits = args.qubits
    simulation_config.eve_active = args.eve
    simulation_config.eve_intercept_probability = args.eve_prob
    simulation_config.noise_active = args.noise > 0
    simulation_config.noise_probability = args.noise
    simulation_config.random_seed = args.seed
    
    if args.gui:
        try:
            from app.gui.main_window import launch_gui
            logger.info("Launching GUI...")
            launch_gui()
        except Exception as e:
            logger.error(f"GUI launch failed: {e}")
            logger.info("Falling back to CLI mode")
            run_cli_simulation(args)
    else:
        run_cli_simulation(args)


def run_cli_simulation(args):
    """Run simulation in CLI mode."""
    
    logger.info("=" * 70)
    logger.info("BB84 QUANTUM KEY DISTRIBUTION SIMULATOR")
    logger.info("=" * 70)
    logger.info("")
    
    if args.verbose:
        logger.info("Configuration:")
        logger.info(f"  Qubits: {args.qubits}")
        logger.info(f"  Eve Active: {args.eve}")
        if args.eve:
            logger.info(f"  Eve Intercept Probability: {args.eve_prob}")
        logger.info(f"  Noise Active: {args.noise > 0}")
        if args.noise > 0:
            logger.info(f"  Noise Probability: {args.noise}")
        logger.info(f"  Seed: {args.seed}")
        logger.info("")
    
    # Run simulation
    logger.info("Running BB84 protocol simulation...")
    result = run_bb84_simulation(
        num_qubits=args.qubits,
        eve_active=args.eve,
        noise_active=args.noise > 0,
        noise_prob=args.noise,
        seed=args.seed
    )
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("SIMULATION RESULTS")
    logger.info("=" * 70)
    logger.info("")
    
    # Print summary
    print_simulation_summary(result)
    
    # Export if requested
    if args.export:
        logger.info("")
        logger.info("Exporting results...")
        export_manager = ExportManager(args.export_dir)
        exports = export_manager.export_all(result)
        
        logger.info(f"Exports saved to {args.export_dir}/:")
        for format_name, filepath in exports.items():
            logger.info(f"  • {format_name}: {filepath}")
    
    # Visualize if requested
    if args.visualize:
        logger.info("")
        logger.info("Generating visualizations...")
        visualizer = BB84Visualizer()
        output_dir = os.path.join(args.export_dir, 'graphs')
        plots = visualizer.create_summary_visualization(result, output_dir)
        
        logger.info(f"Plots saved to {output_dir}:")
        for plot_name, filepath in plots.items():
            logger.info(f"  • {plot_name}: {filepath}")
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("Simulation complete!")
    logger.info("=" * 70)


def print_simulation_summary(result):
    """Print formatted simulation summary."""
    
    protocol = BB84Protocol()
    summary = protocol.get_summary(result)
    print(summary)
    
    # Additional details
    print(f"\nAdditional Information:")
    print(f"  Secure Key Rate: {result.security_analysis.secure_key_rate:.4f} bits/qubit")
    print(f"  Analysis Confidence: {result.security_analysis.confidence:.1%}")
    print(f"\nSecurity Recommendations:")
    for rec in result.security_analysis.recommendations:
        print(f"  • {rec}")


if __name__ == '__main__':
    main()
