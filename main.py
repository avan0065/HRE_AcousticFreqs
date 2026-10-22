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
D_min = np.arange(0.04, 0.085, 0.005)

# call the function
freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)

plot_D = D_min
plot_freqs = freqs

# Create the scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(plot_D, plot_freqs, color='blue', alpha=0.7, edgecolors='black', label='Analytical Frequencies')
plt.title('Calculated Primary Oscillation Frequency vs. Port Diameter')
plt.xlabel('Fuel Grain Port Diameter (d) [m]')
plt.ylabel('Frequency (f) [Hz]')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()

# 
