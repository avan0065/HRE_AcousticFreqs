
def primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min):
    import numpy as np
    import math
    """
    Calculates primary oscillation frequencies across a range of fuel grain port diameters.

    Parameters
    ----------
    mdot : float
        Oxidiser mass flow rate [kg/s].
    OF_ratio : float
        Oxidiser-to-fuel ratio.
    P_c : float
        Chamber pressure [Pa].
    L : float
        Length of the combustion chamber [m].
    R : float
        Specific gas constant [J/(kg*K)].
    T_av : float
        Average combustion temperature [K].
    D_min : array_like
        Array of minimum fuel grain port diameters [m]. (not changed by user)

    Returns
    -------
    freqs: list of floats
        Calculated primary oscillation frequencies corresponding to each port diameter.
    """

    freqs = [] # initialise the frequency array
    RT = R * T_av # find RT value from engine parameters
    # loop through each port diameter value
    for d in D_min:
        area = math.pi * (d/2)**2 # area of fuel grain port
        G_0 = mdot / area # oxidiser mass flux through the fuel grain port
        calculated_frequency = 0.2341 * (2 + (1 / OF_ratio)) * ((G_0 * RT) / (L * P_c))
        freqs.append(calculated_frequency)
    return freqs
