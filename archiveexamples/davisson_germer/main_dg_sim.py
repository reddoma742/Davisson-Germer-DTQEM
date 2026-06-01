# examples/davisson_germer/main_dg_sim.py
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

import sys
sys.path.append('../..')  # للوصول إلى مجلد core
from core.dg_engine import DavissonGermerEngine

class DavissonGermerGUI:
    def __init__(self):
        self.engine = None
        self.output = widgets.Output()
        self._create_widgets()

    def _create_widgets(self):
        self.sliders = {
            'energy_eV': widgets.FloatSlider(value=54.0, min=10.0, max=200.0, step=1.0, description='Energy (eV)'),
            'd_nm': widgets.FloatSlider(value=0.215, min=0.1, max=0.5, step=0.005, description='d (nm)'),
            'gamma_phi0': widgets.FloatSlider(value=1000.0, min=100.0, max=1e5, step=100.0, description='γφ₀ (1/s)', readout_format='.0f'),
            't_obs_us': widgets.FloatSlider(value=1.0, min=0.1, max=10.0, step=0.1, description='t_obs (μs)'),
            'sigma_deg': widgets.FloatSlider(value=2.0, min=0.5, max=5.0, step=0.1, description='Peak width σ (deg)')
        }
        self.button_run = widgets.Button(description='Run Simulation', button_style='primary')
        self.button_run.on_click(self._run)

        ui = widgets.VBox(list(self.sliders.values()) + [self.button_run, self.output])
        display(ui)

    def _run(self, change):
        with self.output:
            clear_output(wait=True)
            E_eV = self.sliders['energy_eV'].value
            d_nm = self.sliders['d_nm'].value
            gamma_phi0 = self.sliders['gamma_phi0'].value
            t_obs_us = self.sliders['t_obs_us'].value
            sigma_deg = self.sliders['sigma_deg'].value
            t_obs = t_obs_us * 1e-6

            # إنشاء المحرك
            self.engine = DavissonGermerEngine(gamma_phi0=gamma_phi0, t_obs=t_obs)

            # حساب طول موجة دي برولي وزاوية براج
            lam_m = self.engine.de_broglie_wavelength(E_eV)
            phi_list = self.engine.bragg_angles(d_nm, lam_m, n=1)
            if not phi_list:
                print("لا توجد زاوية براج صالحة (nλ > 2d).")
                return
            phi_peak = phi_list[0]

            # حساب V و D عند زاوية براج (نحصل عليها من الحالة الابتدائية θ)
            theta_deg = 180 - 2 * phi_peak
            V, D = self.engine.visibility_distinguishability_from_theta(theta_deg)
            comp = V*V + D*D

            # محاكاة شدة الحيود حول القمة
            phi_range = np.linspace(phi_peak - 10, phi_peak + 10, 200)
            intensity = self.engine.intensity_profile(phi_range, phi_peak, sigma_deg=sigma_deg)

            # محاكاة V و D لكل φ (بافتراض أن θ = 180 - 2φ)
            V_vals = []
            D_vals = []
            for phi in phi_range:
                th = 180 - 2 * phi
                v_loc, d_loc = self.engine.visibility_distinguishability_from_theta(th)
                V_vals.append(v_loc)
                D_vals.append(d_loc)

            # رسم
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            ax1.plot(phi_range, intensity, 'b-', lw=2)
            ax1.axvline(phi_peak, color='r', linestyle='--', label=f'Bragg angle {phi_peak:.2f}°')
            ax1.set_xlabel('Scattering angle φ (degrees)')
            ax1.set_ylabel('Diffracted intensity (a.u.)')
            ax1.set_title('Davisson–Germer diffraction pattern')
            ax1.legend()
            ax1.grid(alpha=0.3)

            ax2.plot(phi_range, V_vals, 'g-', label='Visibility V')
            ax2.plot(phi_range, D_vals, 'm--', label='Distinguishability D')
            ax2.axvline(phi_peak, color='gray', linestyle=':', label='Bragg peak')
            ax2.set_xlabel('Scattering angle φ (degrees)')
            ax2.set_ylabel('V, D')
            ax2.set_title('DTQEM predictions from crystal experiment')
            ax2.legend()
            ax2.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()

            # طباعة النتائج
            print(f"\n=== Davisson–Germer Simulation (γφ₀={gamma_phi0:.0f} 1/s, t_obs={t_obs_us:.1f} μs) ===")
            print(f"Electron energy: {E_eV} eV, de Broglie wavelength: {lam_m*1e10:.3f} Å")
            print(f"Crystal spacing: {d_nm} nm → Bragg angle: {phi_peak:.2f}°")
            print(f"Initial superposition angle θ = {theta_deg:.2f}° (θ = 180° - 2φ)")
            print(f"Visibility V = {V:.4f}, Distinguishability D = {D:.4f}")
            print(f"Complementarity V² + D² = {comp:.4f}")
            print("\nNote: V and D are computed from Lindblad evolution of the entangled state |ψ(θ)⟩.")
