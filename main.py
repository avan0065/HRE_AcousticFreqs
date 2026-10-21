import numpy as np
import matplotlib.pyplot as plt
from oscillations import primary_oscillation

# USER CHANGE these parameters
mdot = 1.5 # oxidiser mass flow [kg/s]
OF_ratio = 6 # oxidiser/fuel ratio
P_c = 1500000 # chamber pressure [Pa]
L = 0.36 # length of chamber [metres]
R = 464 # gas constant [J/(kg*K)]
T_av = 3000 # temperature [Kelvin]

# Define the range of diameters to calculate (regression)
D_min = np.arange(0.02, 0.1, 0.01)

# call the function
freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)

# Slice or pad to ensure they match if the module still has a hardcoded array shape
if len(freqs) != len(D_min):
    print(f"Warning: Length mismatch. Function returned {len(freqs)} values, but D_min has {len(D_min)} values.")
    # Sync length for plotting
    min_len = min(len(freqs), len(D_min))
    plot_D = D_min[:min_len]
    plot_freqs = freqs[:min_len]
else:
    plot_D = D_min
    plot_freqs = freqs

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(plot_D, plot_freqs, color='blue', alpha=0.7, edgecolors='black', label='Predicted Frequencies')
plt.title('Predicted Primary Oscillation Frequency vs. Port Diameter')
plt.xlabel('Fuel Grain Port Diameter (d) [m]')
plt.ylabel('Frequency (f) [Hz]')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()
