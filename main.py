import numpy as np
import matplotlib.pyplot as plt
from oscillations import primary_oscillation

# Engine parameters
mdot = 1.5 # oxidiser mass flow [kg/s]
OF_ratio = 6 # oxidiser/fuel ratio
P_c = 1500000 # chamber pressure [Pa]
L = 0.36 # length of chamber [metres]
R = 464 # gas constant [J/(kg*K)]
T_av = 3000 # temperature [Kelvin]

# Fuel grain diameter data and frequency data from Matlab
D_fuelgrain = np.array([0.045, 0.07577, 0.05, 0.078, 0.048, 0.083])
solaris_freqs = np.array([884.77, 208.01, 292.97, 216.80, 732.42, 222.66])

# Define the range of diameters to calculate
D_min = np.arange(0.04, 0.085, 0.005)

# call the function
freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)

plot_D = D_min
plot_freqs = freqs

# Create the scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(plot_D, plot_freqs, color='blue', alpha=0.7, edgecolors='black', label='Analytical Frequencies')
plt.plot(plot_D, plot_freqs, color='black')
plt.title('Calculated Primary Oscillation Frequency vs. Port Diameter')
plt.xlabel('Fuel Grain Port Diameter (d) [m]')
plt.ylabel('Frequency (f) [Hz]')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()
