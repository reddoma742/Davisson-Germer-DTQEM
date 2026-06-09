import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# إنشاء مجلد figures إذا لم يكن موجوداً
Path("figures").mkdir(exist_ok=True)

# المعاملات
T_ref = 300.0
b0 = 0.8055
T_star = 3.82

# درجات الحرارة
T = np.linspace(0.1, 20, 500)

# النموذج الخطي
b_lin = b0 * T / T_ref

# نموذج التشبع (coth) - تجنب القسمة على صفر
x = T_star / np.maximum(T, 1e-12)
b_sat = b0 * (T_star / T_ref) * x / np.tanh(x)

# الرسم
plt.figure(figsize=(6, 4))
plt.plot(T, b_sat, 'b-', linewidth=2.5, label=r'$b_{\mathrm{eff}}(T)$')
plt.plot(T, b_lin, 'r--', linewidth=1.5, label=r'Linear $b \propto T$')
plt.axvline(T_star, color='green', linestyle=':', linewidth=2, label=r'$T^* = 3.82\,\mathrm{K}$')

plt.xlabel(r'Temperature $T$ (K)', fontsize=11)
plt.ylabel(r'$b_{\mathrm{eff}}(T)$', fontsize=11)
plt.title(r'Effective Thermal Coefficient $b_{\mathrm{eff}}(T)$', fontsize=12, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(alpha=0.3)

# حفظ الشكل
plt.savefig('figures/figure_b_eff.png', dpi=150, bbox_inches='tight')
plt.show()  # <--- أضف هذا لرؤية الصورة
plt.close()

print("✅ تم إنشاء figure_b_eff.png في مجلد figures/")
