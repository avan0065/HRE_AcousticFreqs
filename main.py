"""
Hybrid Rocket Engine Acoustic Frequency Simulator - Main Script.

This script coordinates the simulation workflow: it loads experimental
hotfire data, runs analytical oscillation calculations, executes multiple
interpolation methods (Linear, PCHIP, Akima), evaluates their execution times
and prediction accuracies (MAE, RMSE), and finally sizes an optimal
acoustic liner to mitigate target frequencies.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import importlib
import time

if 'oscillations' in sys.modules:
    importlib.reload(sys.modules['oscillations'])
if 'pchipinterpolation' in sys.modules:
    importlib.reload(sys.modules['pchipinterpolation'])
if 'akimainterpolation' in sys.modules:
    importlib.reload(sys.modules['akimainterpolation'])
if 'linearinterpolation' in sys.modules:
    importlib.reload(sys.modules['linearinterpolation'])
from oscillations import primary_oscillation
from pchipinterpolation import plot_pchip_interpolation
from akimainterpolation import plot_akima_interpolation
from linearinterpolation import plot_linear_interpolation

# Exclude some variables from pdoc
__pdoc__ = {
    "time_pchip": None,
    "time_akima": None,
    "time_linear": None,
    "linear_model": None,
    "pchip_model": None,
    "akima_model": None,
}

# Engine parameters
mdot = 1.5 
"""float: oxidser mass flow [kg/s]"""
OF_ratio = 6
"""float: oxidiser/fuel ratio"""
P_c = 1500000
"""float: chamber pressure [Pa]"""
L = 0.36
"""float: length of chamber [metres]"""
R = 302.3
"""float: gas constant [J/(kg*K)]"""
T_av = 2700
"""float: temperature [Kelvin]"""

# Measured fuel grain diameter data and frequency data from Matlab
D_fuelgrain = np.array([0.045, 0.07577, 0.05, 0.078, 0.048, 0.083])
"""array: fuel grain inner diameter [m]"""
solaris_freqs = np.array([884.77, 208.01, 612.97, 216.80, 732.42, 222.66])
"""array: frequencies determined from hotfire data [Hz]"""

# Define the range of diameters to calculate
D_min = np.arange(0.045, 0.080, 0.0025)
"""array: desired analysed diameters [m]"""

# Call analytical frequency function
freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)
"""array: frequencies determined from oscillation.py using D_min [Hz]"""

# Generate a fine range of diameter values for a smooth curve
D_fine = np.linspace(D_fuelgrain.min(), D_fuelgrain.max(), 300)
"""array: range of diameters to be interpolated [m]"""

# Timing Regime for Linear
_t0_linear = time.perf_counter()
linear_model = plot_linear_interpolation(D_fuelgrain, solaris_freqs)
freqs_linear = linear_model(D_fine)
"""array: frequencies determined from linearinterpolation.py using D_min [Hz]"""
_t1_linear = time.perf_counter()
time_linear = _t1_linear - _t0_linear
"""float: time needed to run linearinterpolation.py"""

# Timing Regime for PCHIP
_t0_pchip = time.perf_counter()
pchip_model = plot_pchip_interpolation(D_fuelgrain, solaris_freqs)
freqs_pchip = pchip_model(D_fine)
"""array: frequencies determined from PCHIPinterpolation.py using D_min [Hz]"""
_t1_pchip = time.perf_counter()
time_pchip = _t1_pchip - _t0_pchip
"""float: time needed to run PCHIPinterpolation.py"""

# Timing Regime for Akima
_t0_akima = time.perf_counter()
akima_model = plot_akima_interpolation(D_fuelgrain, solaris_freqs)
freqs_akima = akima_model(D_fine)
"""array: frequencies determined from akimainterpolation.py using D_min [Hz]"""
_t1_akima = time.perf_counter()
time_akima = _t1_akima - _t0_akima
"""float: time needed to run akimainterpolation.py"""

# Figure 1: Overlaid Plot (just experimental data)
plt.figure(figsize=(8, 5))
plt.scatter(D_fuelgrain, solaris_freqs, color='black', zorder=5, label='Experimental Points')
plt.plot(D_fine, freqs_pchip, color='green', label='PCHIP Interpolation')
plt.plot(D_fine, freqs_akima, color='red', label='Akima Interpolation')
plt.plot(D_fine, freqs_linear, color='orange', label='Linear Interpolation')
plt.title('Comparison of Analytical Frequencies, PCHIP, and Akima Experimental Trends')
plt.xlabel('Fuel Grain Port Diameter (d) [m]')
plt.ylabel('Frequency (f) [Hz]')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()

# Figure 2: Overlaid Plot (with analytical frequencies)
plt.figure(figsize=(8, 5))
plt.scatter(D_min, freqs, color='black', marker='s', label='Analytical Frequencies')
plt.plot(D_min, freqs, color='blue')
plt.scatter(D_fuelgrain, solaris_freqs, color='black', zorder=5, label='Experimental Points')
plt.plot(D_fine, freqs_pchip, color='green', label='PCHIP Interpolation')
plt.plot(D_fine, freqs_akima, color='red', label='Akima Interpolation')
plt.plot(D_fine, freqs_linear, color='orange', label='Linear Interpolation')
plt.title('Comparison of Analytical Frequencies and Interpolated Experimental Trends')
plt.xlabel('Fuel Grain Port Diameter (d) [m]')
plt.ylabel('Frequency (f) [Hz]')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()

# Evaluate interpolations at analytical diameter values
y_pchip = pchip_model(D_min)
"""array: PCHIP interpolation values at analytical diameter values"""
y_akima = akima_model(D_min)
"""array: Akima interpolation values at analytical diameter values"""
y_linear = linear_model(D_min)
"""array: Linear interpolation values at analytical diameter values"""

# Calculate RMSE
rmse_pchip = np.sqrt(np.mean((freqs - y_pchip) ** 2))
"""float: RMSE of PCHIP interpolation vs analytical"""
rmse_akima = np.sqrt(np.mean((freqs - y_akima) ** 2))
"""float: RMSE of Akima interpolation vs analytical"""
rmse_linear = np.sqrt(np.mean((freqs - y_linear) ** 2))
"""float: RMSE of linear interpolation vs analytical"""

# Calculate MAE
mae_pchip = np.mean(np.abs(freqs - y_pchip))
"""float: MAE of PCHIP interpolation vs analytical"""
mae_akima = np.mean(np.abs(freqs - y_akima))
"""float: MAE of Akima interpolation vs analytical"""
mae_linear = np.mean(np.abs(freqs - y_linear))
"""float: MAE of linear interpolation vs analytical"""

# Create comparison table
metrics_data = {
    'Interpolation Method': ['Linear', 'PCHIP', 'Akima'],
    'MAE (Hz)': [mae_linear, mae_pchip, mae_akima],
    'RMSE (Hz)': [rmse_linear, rmse_pchip, rmse_akima],
    'Execution Time (ms)': [time_linear * 1000, time_pchip * 1000, time_akima * 1000]
}
"""table: comparison of each interpolation method (RMSE, MAE, and timing)"""
metrics_df = pd.DataFrame(metrics_data)
print("\n--- Performance Evaluation Metrics ---")
print(metrics_df.to_string(index=False))

if 'liner_size' in sys.modules:
    importlib.reload(sys.modules['liner_size'])
from liner_size import acoustic_liner

# Calculate optimal liner size
target_freq, best_diameter_m, best_freq = acoustic_liner(freqs_pchip, R)
"""floats: target frequency and optimal diameter for a liner"""
print(f"The targeted frequency of the engine is {target_freq:.2f} Hz.")
print(f"The optimal liner hole diameter is {best_diameter_m*1000:.2f} mm with a target frequency of {best_freq:.2f} Hz.")
