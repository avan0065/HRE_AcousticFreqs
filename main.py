import numpy as np
import matplotlib.pyplot as plt
from oscillations import primary_oscillation
from pchipinterpolation import plot_pchip_interpolation

# Engine parameters
mdot = 1.5 # oxidiser mass flow [kg/s]
OF_ratio = 6 # oxidiser/fuel ratio
P_c = 1500000 # chamber pressure [Pa]
L = 0.36 # length of chamber [metres]
R = 464 # gas constant [J/(kg*K)]
T_av = 3000 # temperature [Kelvin]

# Fuel grain diameter data and frequency data from Matlab
D_fuelgrain = np.array([0.045, 0.07577, 0.05, 0.078, 0.048, 0.083])
solaris_freqs = np.array([884.77, 208.01, 612.97, 216.80, 732.42, 222.66])

# Define the range of diameters to calculate
D_min = np.arange(0.04, 0.09, 0.005)

# Call analytical frequency function
freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)

# Call the PCHIP interpolator function
pchip_model = plot_pchip_interpolation(D_fuelgrain, solaris_freqs)

# Generate a fine range of diameter values for a smooth curve
D_fine = np.linspace(D_fuelgrain.min(), D_fuelgrain.max(), 300)
freqs_pchip = pchip_model(D_fine)

# Figure 1: Side-by-Side Plots (Analytical and Experimental)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1: Analytical
ax1.scatter(D_min, freqs, color='black', label='Analytical Frequencies')
ax1.plot(D_min, freqs, color='blue')
ax1.set_title('Calculated Primary Oscillation Frequency')
ax1.set_xlabel('Fuel Grain Port Diameter (d) [m]')
ax1.set_ylabel('Frequency (f) [Hz]')
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend()

# Subplot 2: Experimental PCHIP
ax2.plot(D_fine, freqs_pchip, color='darkorange', label='PCHIP Interpolation')
ax2.scatter(D_fuelgrain, solaris_freqs, color='black', s=50, zorder=5, label='Experimental Points')
ax2.set_title('PCHIP Interpolation of Experimental Data')
ax2.set_xlabel('Fuel Grain Port Diameter (d) [m]')
ax2.set_ylabel('Frequency (f) [Hz]')
ax2.grid(True, which="both", ls="--", alpha=0.5)
ax2.legend()

plt.tight_layout()
plt.show()

# Figure 2: Overlaid Plot
plt.figure(figsize=(8, 5))
plt.scatter(D_min, freqs, color='black', marker='s', label='Analytical Frequencies')
plt.plot(D_min, freqs, color='blue')
plt.plot(D_fine, freqs_pchip, color='darkorange', label='PCHIP Interpolation (Experimental)')
plt.scatter(D_fuelgrain, solaris_freqs, color='black', zorder=5, label='Experimental Points')
plt.title('Comparison of Analytical Frequencies & PCHIP Experimental Trend')
plt.xlabel('Fuel Grain Port Diameter (d) [m]')
plt.ylabel('Frequency (f) [Hz]')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()
