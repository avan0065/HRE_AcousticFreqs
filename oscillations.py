import numpy as np
import math

def primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av):
    """
    Calculates primary oscillation frequencies across a range of fuel grain port diameters.
    """
    freqs = [] # initialise the frequency array
    RT = R * T_av # find RT value from engine parameters
    # minimum diameter of the fuel grain port
    D_min = np.arange(0.01, 20.0, 0.05)
    # loop through each port diameter value
    for d in D_min:
        area = math.pi * (d/2)**2 # area of fuel grain port
        G_0 = mdot / area # oxidiser mass flux through the fuel grain port
        calculated_frequency = 0.2341 * (2 + (1/OF_ratio)) * ((G_0 * RT) / (L * P_c))
        freqs.append(calculated_frequency)
    return freqs
