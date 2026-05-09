# examples/tunneling/main_tunneling.py
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# استيراد المحرك من المجلد core
import sys
sys.path.append('../..')  # للوصول إلى مجلد core من المثال
from core.tunneling_engine import TunnelingEngine

class TunnelingGUI:
    def __init__(self):
        self.model = None
        self.output = widgets.Output()
        self.warning = widgets.HTML(value="")
        self._create_widgets()

    def _create_widgets(self):
        self.sliders = {
            'Delta_meV': widgets.FloatSlider(value=1.0, min=0.1, max=10.0, step=0.1, description='Δ (meV)'),
            'gamma_phi0': widgets.FloatSlider(value=1e10, min=1e8, max=1e13, step=1e9, description='γφ₀ (1/s)', readout_format='.2e'),
            'gamma_relax0': widgets.FloatSlider(value=0.0, min=0.0, max=1e11, step=1e9, description='γrel₀ (1/s)', readout_format='.2e'),
            'T': widgets.FloatSlider(value=0.0, min=0.0, max=300.0, step=1.0, description='T (K)'),
            't_max_ps': widgets.FloatSlider(value=10.0, min=1.0, max=50.0, step=1.0, description='t_max (ps)')
            'measurement_rate': widgets.FloatSlider(value=0.0, min=0.0, max=1e13, step=1e11, description='Γ_meas (1/s)', readout_format='.2e'),
        
        }
        self.button_run = widgets.Button(description='Run Simulation', button_style='primary')
        self.button_run.on_click(self._run)

        ui = widgets.VBox(list(self.sliders.values()) + [self.button_run, self.output, self.warning])
        display(ui)

    def _run(self, change):
        with self.output:
            clear_output(wait=True)
            Delta_meV = self.sliders['Delta_meV'].value
            gamma_phi0 = self.sliders['gamma_phi0'].value
            gamma_relax0 = self.sliders['gamma_relax0'].value
            T = self.sliders['T'].value
            t_max_ps = self.sliders['t_max_ps'].value
            t_max = t_max_ps * 1e-12

            # إنشاء المحرك باستخدام المعاملات المدخلة
            self.model = TunnelingEngine(Delta_eV=Delta_meV/1000.0, gamma_phi0=gamma_phi0, gamma_relax0=gamma_relax0)
            t_arr, P, V, D = self.model.tunneling_dynamics(T, t_max, num_points=500)

            # الحل المعزول للمقارنة
            P_iso = self.model.isolated_P_right(t_arr, Delta_meV/1000.0)

            # حساب زمن النفقية الأول والمعاملات
            tau_num = self.model.first_tunneling_time(t_arr, P)
            tau_iso = self.model.first_tunneling_time(t_arr, P_iso)
            gamma_eff = self.model.effective_gamma_phi(t_arr, V)

            # الرسم
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            ax1.plot(t_arr*1e12, P_iso, 'b--', label='Isolated (theory)')
            ax1.plot(t_arr*1e12, P, 'r-', label=f'DTQEM: γφ₀={gamma_phi0:.1e}')
            ax1.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
            ax1.set_xlabel('Time (ps)')
            ax1.set_ylabel('P_right(t)')
            ax1.set_title('Tunneling dynamics')
            ax1.legend()
            ax1.grid(alpha=0.3)

            ax2.plot(t_arr*1e12, V, 'g-', label='V(t) = 2|ρ₀₁|')
            ax2.plot(t_arr*1e12, D, 'm--', label='D(t) = |ρ₀₀-ρ₁₁|')
            ax2.plot(t_arr*1e12, np.sqrt(V**2 + D**2), 'k:', label='√(V²+D²)')
            ax2.set_xlabel('Time (ps)')
            ax2.set_ylabel('V, D')
            ax2.set_title('Wave‑particle balance during tunneling')
            ax2.legend()
            ax2.grid(alpha=0.3)

            ax3 = ax2.twinx()
            ax3.plot(t_arr*1e12, S, 'c:', label='Entropy S(t)')
            ax3.set_ylabel('Entropy (nats)', color='c')

            plt.tight_layout()
            plt.show()

            # طباعة التقرير
            print(f"\n=== Tunneling Results (Δ = {Delta_meV:.2f} meV, T = {T} K) ===")
            print(f"Isolated tunneling time: {tau_iso*1e12:.2f} ps")
            print(f"DTQEM tunneling time:   {tau_num*1e12:.2f} ps")
            print(f"Effective γφ₀ from V(t): {gamma_eff:.2e} 1/s")
            print(f"Entanglement lifetime: {self.model.entanglement_lifetime(T)*1e12:.2f} ps")
            if not np.isnan(tau_num):
                idx = np.argmin(np.abs(t_arr - tau_num))
                V_tau = V[idx]
                D_tau = D[idx]
                comp = V_tau*V_tau + D_tau*D_tau
                self.warning.value = f"✓ At tunneling time: V = {V_tau:.3f}, D = {D_tau:.3f}, V²+D² = {comp:.5f}"
            else:
                self.warning.value = "⚠️ Could not compute tunneling time (threshold not reached)."

if __name__ == "__main__":
    print("DTQEM - Quantum Tunneling Module with Time Sovereignty")
    print("Inspired by the analytical balance condition V = D")
    gui = TunnelingGUI()
