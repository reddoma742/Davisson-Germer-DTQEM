# examples/schottky/main_schottky.py
import sys
sys.path.append('../..')
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
from core.schottky_engine import SchottkyEngine

class SchottkyGUI:
    def __init__(self):
        self.engine = None
        self.output = widgets.Output()
        self._create_widgets()
        
    def _create_widgets(self):
        self.sliders = {
            'work_function': widgets.FloatSlider(value=4.5, min=2.0, max=6.0, step=0.1, description='Work function (eV)'),
            'T': widgets.FloatSlider(value=300, min=100, max=1500, step=10, description='T (K)'),
            'E_field': widgets.FloatSlider(value=1e8, min=0, max=1e9, step=1e7, description='E (V/m)', readout_format='.2e'),
            't_max_ns': widgets.FloatSlider(value=10, min=1, max=100, step=1, description='t_max (ns)'),
        }
        self.button_run = widgets.Button(description='Run Simulation', button_style='primary')
        self.button_run.on_click(self._run)
        ui = widgets.VBox(list(self.sliders.values()) + [self.button_run, self.output])
        display(ui)
        
    def _run(self, change):
        with self.output:
            clear_output(wait=True)
            phi = self.sliders['work_function'].value
            T = self.sliders['T'].value
            E = self.sliders['E_field'].value
            t_max_ns = self.sliders['t_max_ns'].value
            t_max = t_max_ns * 1e-9
            
            self.engine = SchottkyEngine(work_function_eV=phi)
            t_arr, P_v, V, D = self.engine.emission_dynamics(T, E, t_max, num_points=500)
            
            # Compute analytical current
            gamma = self.engine.emission_rate(T, E)
            current_pA = gamma * 1e12  # pA (since gamma is electrons/s, assuming unity charge, but rough estimate)
            
            fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,5))
            ax1.plot(t_arr*1e9, P_v, 'b-', lw=2)
            ax1.set_xlabel('Time (ns)')
            ax1.set_ylabel('Emission probability P_v(t)')
            ax1.set_title('Electron escape from metal (Schottky effect)')
            ax1.grid(alpha=0.3)
            
            ax2.plot(t_arr*1e9, V, 'g-', label='V(t) = 2|ρ01|')
            ax2.plot(t_arr*1e9, D, 'm--', label='D(t) = |ρ00-ρ11|')
            ax2.plot(t_arr*1e9, np.sqrt(V**2 + D**2), 'k:', label='√(V²+D²)')
            ax2.set_xlabel('Time (ns)')
            ax2.set_ylabel('V, D')
            ax2.set_title('Coherence and distinguishability')
            ax2.legend()
            ax2.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
            
            print(f"Schottky emission rate γ = {gamma:.2e} 1/s")
            print(f"Estimated current (area 1 nm²): {current_pA:.2f} pA")
            # At final time
            print(f"Final V = {V[-1]:.4f}, D = {D[-1]:.4f}, V²+D² = {V[-1]**2 + D[-1]**2:.4f}")

if __name__ == "__main__":
    print("Schottky effect simulation using DTQEM (Lindblad)")
    gui = SchottkyGUI()
