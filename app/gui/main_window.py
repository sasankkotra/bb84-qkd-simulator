"""
GUI Main Window for BB84 QKD Simulator (Alpha).

Simple Tkinter-based GUI for parameter configuration and results visualization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from app.core.bb84_protocol import BB84Protocol
from app.config.settings import SimulationConfig
from app.visualization.charts import BB84Visualizer
from app.utils.exporters import ExportManager
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class BB84GUI:
    """Main GUI window for BB84 simulator."""
    
    def __init__(self, root):
        """Initialize GUI."""
        self.root = root
        self.root.title("BB84 Quantum Key Distribution Simulator")
        self.root.geometry("1200x800")
        
        self.simulation_result = None
        self.is_running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up GUI components."""
        # Create main frames
        left_frame = ttk.Frame(self.root, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        center_frame = ttk.Frame(self.root, padding="10")
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # LEFT PANEL: Parameters
        left_label = ttk.Label(left_frame, text="SIMULATION CONTROL", font=('Arial', 12, 'bold'))
        left_label.pack(pady=10)
        
        # Number of qubits
        ttk.Label(left_frame, text="Number of Qubits:").pack(anchor=tk.W, pady=5)
        self.qubits_var = tk.StringVar(value="1000")
        self.qubits_spinbox = ttk.Spinbox(
            left_frame, from_=100, to=10000, textvariable=self.qubits_var, width=10
        )
        self.qubits_spinbox.pack(anchor=tk.W, pady=5)
        
        # Eve checkbox
        self.eve_var = tk.BooleanVar(value=False)
        self.eve_check = ttk.Checkbutton(
            left_frame, text="Enable Eve Attack", variable=self.eve_var, state=tk.NORMAL
        )
        self.eve_check.pack(anchor=tk.W, pady=5)
        
        # Noise checkbox
        self.noise_var = tk.BooleanVar(value=False)
        self.noise_check = ttk.Checkbutton(
            left_frame, text="Enable Channel Noise", variable=self.noise_var
        )
        self.noise_check.pack(anchor=tk.W, pady=5)
        
        # Noise probability
        ttk.Label(left_frame, text="Noise Probability:").pack(anchor=tk.W, pady=5)
        self.noise_prob_var = tk.StringVar(value="0.05")
        self.noise_prob_spinbox = ttk.Spinbox(
            left_frame, from_=0.0, to=1.0, increment=0.01, textvariable=self.noise_prob_var, width=10
        )
        self.noise_prob_spinbox.pack(anchor=tk.W, pady=5)
        
        # Seed
        ttk.Label(left_frame, text="Random Seed (optional):").pack(anchor=tk.W, pady=5)
        self.seed_var = tk.StringVar(value="")
        self.seed_entry = ttk.Entry(left_frame, textvariable=self.seed_var, width=10)
        self.seed_entry.pack(anchor=tk.W, pady=5)
        
        # Run button
        self.run_button = ttk.Button(
            left_frame, text="RUN SIMULATION", command=self.run_simulation
        )
        self.run_button.pack(fill=tk.X, pady=15)
        
        # Export buttons
        ttk.Button(left_frame, text="Export CSV", command=self.export_csv).pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="Export JSON", command=self.export_json).pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="Export Report", command=self.export_report).pack(fill=tk.X, pady=5)
        
        # CENTER PANEL: Results display
        center_label = ttk.Label(center_frame, text="RESULTS", font=('Arial', 12, 'bold'))
        center_label.pack(pady=10)
        
        self.results_text = tk.Text(center_frame, height=30, width=60, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(center_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text['yscrollcommand'] = scrollbar.set
        
        # RIGHT PANEL: Status
        right_label = ttk.Label(right_frame, text="STATUS", font=('Arial', 12, 'bold'))
        right_label.pack(pady=10)
        
        self.status_text = tk.Text(right_frame, height=30, width=30, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def run_simulation(self):
        """Run simulation in background thread."""
        if self.is_running:
            messagebox.showwarning("Warning", "Simulation already running!")
            return
        
        self.is_running = True
        self.run_button.config(state=tk.DISABLED)
        
        # Run in background thread
        thread = threading.Thread(target=self._run_simulation_thread)
        thread.daemon = True
        thread.start()
    
    def _run_simulation_thread(self):
        """Background thread for simulation."""
        try:
            # Get parameters
            num_qubits = int(self.qubits_var.get())
            eve_active = self.eve_var.get()
            noise_active = self.noise_var.get()
            noise_prob = float(self.noise_prob_var.get())
            seed = None if self.seed_var.get() == "" else int(self.seed_var.get())
            
            self.update_status(f"Running simulation with {num_qubits} qubits...")
            
            # Create config and run
            config = SimulationConfig(
                num_qubits=num_qubits,
                eve_active=eve_active,
                noise_active=noise_active,
                noise_probability=noise_prob,
                random_seed=seed
            )
            
            protocol = BB84Protocol(config)
            self.simulation_result = protocol.run_simulation()
            
            # Display results
            summary = protocol.get_summary(self.simulation_result)
            self.root.after(0, self._display_results, summary)
            self.update_status("Simulation complete!")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))
    
    def _display_results(self, summary):
        """Display results in text widget."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, summary)
        self.results_text.config(state=tk.DISABLED)
    
    def update_status(self, message):
        """Update status text."""
        def update():
            self.status_text.config(state=tk.NORMAL)
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, message)
            self.status_text.config(state=tk.DISABLED)
        
        self.root.after(0, update)
    
    def export_csv(self):
        """Export results to CSV."""
        if not self.simulation_result:
            messagebox.showwarning("Warning", "Run simulation first!")
            return
        
        try:
            manager = ExportManager()
            filepath = manager.export_to_csv(self.simulation_result)
            messagebox.showinfo("Success", f"Exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
    
    def export_json(self):
        """Export results to JSON."""
        if not self.simulation_result:
            messagebox.showwarning("Warning", "Run simulation first!")
            return
        
        try:
            manager = ExportManager()
            filepath = manager.export_to_json(self.simulation_result)
            messagebox.showinfo("Success", f"Exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
    
    def export_report(self):
        """Export results to text report."""
        if not self.simulation_result:
            messagebox.showwarning("Warning", "Run simulation first!")
            return
        
        try:
            manager = ExportManager()
            filepath = manager.export_to_text(self.simulation_result)
            messagebox.showinfo("Success", f"Exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")


def launch_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    app = BB84GUI(root)
    root.mainloop()


if __name__ == '__main__':
    launch_gui()
