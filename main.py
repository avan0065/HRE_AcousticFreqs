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

# Engine parameters
mdot = 1.5 # oxidiser mass flow [kg/s]
OF_ratio = 6 # oxidiser/fuel ratio
P_c = 1500000 # chamber pressure [Pa]
L = 0.36 # length of chamber [metres]
R = 302.3 # gas constant [J/(kg*K)]
T_av = 2700 # temperature [Kelvin]

# Measured fuel grain diameter data and frequency data from Matlab
D_fuelgrain = np.array([0.045, 0.07577, 0.05, 0.078, 0.048, 0.083])
solaris_freqs = np.array([884.77, 208.01, 612.97, 216.80, 732.42, 222.66])

# Define the range of diameters to calculate
D_min = np.arange(0.045, 0.080, 0.0025)

# Call analytical frequency function
freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)

# Generate a fine range of diameter values for a smooth curve
D_fine = np.linspace(D_fuelgrain.min(), D_fuelgrain.max(), 300)

# Timing Regime for Linear
t0_linear = time.perf_counter()
linear_model = plot_linear_interpolation(D_fuelgrain, solaris_freqs)
freqs_linear = linear_model(D_fine)
t1_linear = time.perf_counter()
time_linear = t1_linear - t0_linear

# Timing Regime for PCHIP
t0_pchip = time.perf_counter()
pchip_model = plot_pchip_interpolation(D_fuelgrain, solaris_freqs)
freqs_pchip = pchip_model(D_fine)
t1_pchip = time.perf_counter()
time_pchip = t1_pchip - t0_pchip

# Timing Regime for Akima
t0_akima = time.perf_counter()
akima_model = plot_akima_interpolation(D_fuelgrain, solaris_freqs)
freqs_akima = akima_model(D_fine)
t1_akima = time.perf_counter()
time_akima = t1_akima - t0_akima

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
y_akima = akima_model(D_min)
y_linear = linear_model(D_min)

# Calculate RMSE
rmse_pchip = np.sqrt(np.mean((freqs - y_pchip) ** 2))
rmse_akima = np.sqrt(np.mean((freqs - y_akima) ** 2))
rmse_linear = np.sqrt(np.mean((freqs - y_linear) ** 2))

# Calculate MAE
mae_pchip = np.mean(np.abs(freqs - y_pchip))
mae_akima = np.mean(np.abs(freqs - y_akima))
mae_linear = np.mean(np.abs(freqs - y_linear))

# Create comparison table
metrics_data = {
    'Interpolation Method': ['Linear', 'PCHIP', 'Akima'],
    'MAE (Hz)': [mae_linear, mae_pchip, mae_akima],
    'RMSE (Hz)': [rmse_linear, rmse_pchip, rmse_akima],
    'Execution Time (ms)': [time_linear * 1000, time_pchip * 1000, time_akima * 1000]
}
metrics_df = pd.DataFrame(metrics_data)
print("\n--- Performance Evaluation Metrics ---")
print(metrics_df.to_string(index=False))
